#!/usr/bin/env python3
"""Validate readings.yaml against course.yaml and regenerate docs/readings.md.

    python tools/build_readings.py            # validate + write docs/readings.md
    python tools/build_readings.py --check    # validate only; non-zero on error

The one invariant worth having a build step for:

    a paper discussed in session N is assigned at the end of session N-1

plus the things that make an assignment real rather than nominal: it names what
to read, it is findable (DOI or URL), and no single class hands out more than
the syllabus promises. Everything else here is bookkeeping in service of that.

Why a checker rather than a habit: the failure mode is silent. A paper that was
never assigned looks exactly like one that was, right up until the discussion
segment lands in a room where nobody has read it -- and by then the period is
gone. This runs in CI.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.schedule import ROOT, course, num, readings_spec, sessions, sid  # noqa: E402

OUT = ROOT / "docs" / "readings.md"


def load():
    return course(), sessions(), readings_spec()


# ---------------------------------------------------------------------------
# the rule
# ---------------------------------------------------------------------------

def previous_teaching_session(n, sessions):
    """The meeting before session n that can carry an assignment.

    Exams are skipped: you do not hand out a paper at the end of the midterm.
    Returns None if there is no earlier session at all (session 1).
    """
    for m in range(n - 1, 0, -1):
        s = sessions.get(m)
        if s and s.get("kind") != "exam":
            return m
    return None


def resolve(spec, sessions):
    """Attach an assigning session to every declared reading.

    Returns (rows, errors). A row is a dict with everything the report needs;
    errors are strings, and any error is fatal.
    """
    rows, errors = [], []
    limits = spec.get("limits", {})
    max_notice = limits.get("max_days_notice", 14)

    for key, items in (spec.get("readings") or {}).items():
        try:
            n = num(key)
        except ValueError as e:
            errors.append(f"readings.yaml: {e}")
            continue
        if n not in sessions:
            errors.append(f"readings.yaml: {key} is not a session in course.yaml")
            continue
        if sessions[n].get("kind") == "exam":
            errors.append(f"readings.yaml: {key} is an exam; it cannot discuss a paper")
            continue

        for item in items or []:
            k = item.get("key", "<no key>")
            where = f"{key}/{k}"

            if item.get("assign_in"):
                try:
                    a = num(item["assign_in"])
                except ValueError as e:
                    errors.append(f"{where}: {e}")
                    continue
                if a not in sessions:
                    errors.append(f"{where}: assign_in {item['assign_in']} "
                                  f"is not a session")
                    continue
                if sessions[a].get("kind") == "exam":
                    errors.append(f"{where}: assign_in {item['assign_in']} is the "
                                  f"midterm -- pick a teaching session")
                    continue
                explicit = True
            else:
                a = previous_teaching_session(n, sessions)
                explicit = False
                if a is None:
                    errors.append(
                        f"{where}: session {n} has no earlier meeting, so this "
                        f"paper cannot be assigned in the previous class. Either "
                        f"move the discussion or set assign_in and hand it out "
                        f"before the term (bCourses, week 0).")
                    continue

            # the invariant
            if a >= n:
                errors.append(f"{where}: assigned in s{a:02d}, discussed in "
                              f"s{n:02d} -- assignment must come first")
                continue

            notice = (sessions[n]["date"] - sessions[a]["date"]).days
            if notice > max_notice:
                errors.append(f"{where}: {notice} days between assignment "
                              f"(s{a:02d}) and discussion (s{n:02d}); limit is "
                              f"{max_notice}. They will not remember.")

            if not (item.get("doi") or item.get("url")):
                errors.append(f"{where}: needs a doi or a url")
            if not item.get("short"):
                from decks.theme import short_cite
                errors.append(f"{where}: needs `short` -- the slide version of "
                              f"the citation. Suggestion: "
                              f"{short_cite(item)!r}, but check the authors.")
            if not item.get("focus"):
                errors.append(f"{where}: needs `focus` -- what, specifically, "
                              f"to read. 'Read the paper' is not an assignment.")

            rows.append({
                "discuss": n, "assign": a, "explicit": explicit,
                "notice": notice, **item,
                "required": item.get("required", True),
                "pages": item.get("pages"),
            })

    rows.sort(key=lambda r: (r["assign"], r["discuss"], r.get("key", "")))
    return rows, errors


def limits_for(spec, a):
    """The load limits in force for the class that hands work out on day `a`.

    Per-session overrides exist so that one session needing two papers does not
    quietly license every session to assign two. An override must carry a
    `reason`; an unexplained exception is indistinguishable from a cap that was
    simply raised until it stopped complaining.
    """
    limits = dict(spec.get("limits", {}))
    over = (limits.pop("overrides", None) or {}).get(sid(a)) or {}
    limits.update(over)
    return limits, over


def check_load(rows, spec):
    """No class hands out more than the syllabus promises."""
    errors = []
    by_assign = {}
    for r in rows:
        if r["required"]:
            by_assign.setdefault(r["assign"], []).append(r)

    declared = set((spec.get("limits", {}).get("overrides") or {}))
    for key in sorted(declared):
        try:
            a = num(key)
        except ValueError as e:
            errors.append(f"limits.overrides: {e}")
            continue
        if not (spec["limits"]["overrides"][key] or {}).get("reason"):
            errors.append(f"limits.overrides.{key}: needs a `reason`")
        if a not in by_assign:
            errors.append(f"limits.overrides.{key}: {key} does not assign any "
                          f"required reading, so the override does nothing. "
                          f"Delete it rather than leaving it to be inherited.")

    for a, items in sorted(by_assign.items()):
        limits, over = limits_for(spec, a)
        max_n = limits.get("max_required_per_assignment", 1)
        max_p = limits.get("max_required_pages_per_assignment", 12)
        if len(items) > max_n:
            errors.append(f"s{a:02d} assigns {len(items)} required papers; "
                          f"the limit is {max_n} "
                          f"({', '.join(i.get('key', '?') for i in items)})")
        pages = sum(i["pages"] or 0 for i in items)
        if pages > max_p:
            errors.append(f"s{a:02d} assigns {pages} required pages; "
                          f"the limit is {max_p}")
    return errors


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def fmt(d):
    return d.strftime("%a %b ").replace(" 0", " ") + str(d.day)


def render(course, sessions, spec, rows):
    n_teaching = sum(1 for s in sessions.values() if s.get("kind") != "exam")
    covered = sorted({r["discuss"] for r in rows})
    lines = [
        "# Readings",
        "",
        "[← back to README](../README.md) · See also [References](references.md)",
        "",
        "**Generated by `tools/build_readings.py` from `readings.yaml`. "
        "Do not edit by hand.**",
        "",
        "There is no textbook. Readings are primary literature, and the rule is",
        "fixed:",
        "",
        "> **A paper discussed in class is assigned at the end of the previous",
        "> class**, with a named figure or section to focus on.",
        "",
        "That is a promise in both directions. You will always have had a full",
        "class period's notice; and the discussion segments assume you used it.",
        "",
        f"Declared so far: **{len(rows)} reading(s)** across "
        f"**{len(covered)} of {n_teaching} teaching sessions**.",
        "",
        "---",
        "",
        "## By date",
        "",
        "| Handed out | Read by | Paper | Focus on |",
        "|---|---|---|---|",
    ]
    for r in rows:
        a, n = sessions[r["assign"]], sessions[r["discuss"]]
        link = r.get("url") or (f"https://doi.org/{r['doi']}" if r.get("doi") else "")
        cite = r.get("cite", r.get("key", "?"))
        cite = f"[{cite}]({link})" if link else cite
        opt = "" if r["required"] else " *(optional)*"
        focus = " ".join((r.get("focus") or "").split())
        lines.append(
            f"| end of S{r['assign']} · {fmt(a['date'])} "
            f"| S{r['discuss']} · {fmt(n['date'])} "
            f"| {cite}{opt} | {focus} |")

    missing = [n for n, s in sorted(sessions.items())
               if s.get("kind") != "exam" and n not in covered]
    lines += [
        "",
        "## Sessions with no reading declared",
        "",
        "Not every session needs one — some are derivation sessions and the",
        "reading is the notebook. But each of these is an open decision, not a",
        "decision already made:",
        "",
        ", ".join(f"S{n}" for n in missing) if missing else "*None.*",
        "",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------

def main():
    check_only = "--check" in sys.argv
    course, sessions, spec = load()
    rows, errors = resolve(spec, sessions)
    errors += check_load(rows, spec)

    if errors:
        print("readings.yaml FAILED:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    text = render(course, sessions, spec, rows)
    if check_only:
        if OUT.exists() and OUT.read_text() == text:
            print(f"OK: {len(rows)} reading(s); docs/readings.md up to date")
            return
        sys.exit("--check: docs/readings.md is stale. "
                 "Run `python tools/build_readings.py`.")

    OUT.write_text(text)
    print(f"OK: {len(rows)} reading(s) -> {OUT.relative_to(ROOT)}")
    for r in rows:
        print(f"  s{r['assign']:02d} assigns -> s{r['discuss']:02d} discusses  "
              f"{r.get('key')}  ({r['notice']} days)")


if __name__ == "__main__":
    main()
