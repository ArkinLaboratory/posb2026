#!/usr/bin/env python3
"""The exam row budget, checked against the pilot's own timing table.

WHY THIS EXISTS
The midterm shipped 25 scored rows into 60 minutes of item time -- 2.4 minutes
a row, below the three-minute floor `private/midterm/blueprint.md` had already
declared to be the rate at which "you cannot compute anything". Two humans sat
the paper beforehand and one produced a per-item timing table by hand at
quarter-minute resolution, totalling 58:45 against the 60-minute budget: 98% of
the clock. Every wording and rubric finding from those pilots was acted on.
Nobody checked the shipped row count against the timing table. Class average
45.65%, SD 11.47.

The rule was then written down twice -- in the blueprint's retrospective and in
`private/midterm/reviews/human-pilot-2026-10-12.md` -- in the same words both
times: "the pilot's per-item timing table is a build artifact, the row budget
is checked against it mechanically with the margin printed, the build fails
when a pilot's total exceeds the item-time budget, and a pilot total above ~85%
of budget means cutting scored skills." It was prose in two documents and
nothing executed it.

WHAT IS CONFIGURABLE, AND WHY IT IS NOT A ROW COUNT
The 2027 rule from the blueprint is stated in MINUTES PER ROW, "not in a row
count or a duration, because either can look defensible while their ratio does
not". So `budget.json` names the minutes and the rate, and the row cap is
derived: 120 minutes at 4.5 minutes a row is 26 rows, which is the "roughly 27
rows" the final's design calls for. An explicit `rows_cap` overrides the
derivation when a paper has a reason, and the reason belongs in the file.

PAST EXAMS DO NOT BLOCK
A sat exam cannot be fixed and its arithmetic cannot come right, so reporting
the midterm as FAIL forever would make this gate the thing preflight's own
docstring warns about -- "a permanently red line is how a reader learns to
discount the report it sits in". A past exam reports the same arithmetic at
WARN: visible, honest, non-blocking. An exam still to be sat gets the full
teeth. This mirrors how `check_session` already treats a session that has
already been taught.

THE TIMING-TABLE FORMAT IS THE ONE A HUMAN ALREADY PRODUCED
Josh wrote his table as a markdown table with repeated `| item | time |`
column pairs, times as `m:ss`, some bolded, a `TOTAL` row with empty leading
cells and short rows padded with blanks. That is what is parsed, because
requiring a format no tester has ever produced is how you get no timing table
at all.
"""
import datetime
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "private"

#: An exam needs human pilots, an ambiguity pass, and room to cut and rebuild.
#: The blueprint budgets "tier-1 and tier-2 pilots with humans and a dedicated
#: ambiguity pass" for the final; that is a month and more, so the absence of a
#: build directory becomes worth saying well before the week of the exam.
LEAD_DAYS = 45

DEFAULTS = {
    # Minutes of item time. Required -- there is no defensible default.
    "item_time_minutes": None,
    # The 2027 rule from blueprint.md's retrospective.
    "target_minutes_per_row": 4.5,
    # Below this the blueprint's own words are "you cannot compute anything".
    "floor_minutes_per_row": 3.0,
    # "A pilot total above ~85% of budget means cutting scored skills."
    "warn_fraction": 0.85,
    # Optional explicit cap, overriding item_time / target.
    "rows_cap": None,
    # ISO date of the sitting. Cross-checked against the syllabus.
    "date": None,
}

CONFIG_NAME = "budget.json"


class ExamConfigError(RuntimeError):
    pass


# ----------------------------------------------------------------- config ---
def exam_dirs(root=None):
    """Every private/<name>/ that holds an exam paper, by name.

    Discovery is by content -- a directory with an `exam.md` in it -- so a
    `private/final/` that does not exist yet is simply absent, and one that
    appears is picked up with no list to edit.
    """
    base = Path(root) if root else PRIVATE
    if not base.is_dir():
        return []
    return sorted((d.name, d) for d in base.iterdir()
                  if d.is_dir() and (d / "exam.md").is_file())


def load_config(exam_dir):
    """budget.json with defaults applied and the derived row cap filled in."""
    d = Path(exam_dir)
    p = (d if d.is_absolute() else ROOT / d) / CONFIG_NAME
    if not p.is_file():
        raise ExamConfigError(
            f"{_rel(p)} does not exist. An exam cannot be row-"
            f"budgeted without one. Write it:\n"
            f'    {{"item_time_minutes": 120, "date": "2026-12-16"}}\n'
            f"  target_minutes_per_row defaults to "
            f"{DEFAULTS['target_minutes_per_row']}, the floor to "
            f"{DEFAULTS['floor_minutes_per_row']}, the warning band to "
            f"{DEFAULTS['warn_fraction']:.0%} of budget.")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ExamConfigError(f"{_rel(p)} is not valid JSON: {e}")
    unknown = set(raw) - set(DEFAULTS) - {"exam", "note"}
    if unknown:
        raise ExamConfigError(
            f"{_rel(p)}: unknown key(s) {sorted(unknown)}. A "
            f"misspelled key is a setting that silently does nothing.")
    cfg = dict(DEFAULTS)
    cfg.update(raw)
    if not cfg["item_time_minutes"]:
        raise ExamConfigError(
            f"{_rel(p)}: item_time_minutes is required.")
    for k in ("item_time_minutes", "target_minutes_per_row",
              "floor_minutes_per_row", "warn_fraction"):
        cfg[k] = float(cfg[k])
    if cfg["rows_cap"] is None:
        cfg["rows_cap"] = int(math.floor(
            cfg["item_time_minutes"] / cfg["target_minutes_per_row"]))
        cfg["rows_cap_derived"] = True
    else:
        cfg["rows_cap"] = int(cfg["rows_cap"])
        cfg["rows_cap_derived"] = False
    if cfg["date"]:
        cfg["date"] = datetime.date.fromisoformat(str(cfg["date"]))
    return cfg


# ------------------------------------------------------------------- rows ---
ROW_HEAD = re.compile(r'^(?:## |\*\*)([A-Z]\d+(?:\.\d+)?) ·(.*)$', re.M)
PTS = re.compile(r'·\s*(\d+)\s*pts?\b')


def scored_rows(rubric_path):
    """[(label, points)] for every scored row the rubric declares.

    The same shape `private/midterm/marking_sheet.py` extracts, by the same
    pattern, but with no hardcoded list of labels -- a row is scored when its
    heading declares points. On the midterm this returns exactly the 25 labels
    in that file's SCORED list, 100 points, and correctly skips the four block
    headings (B1, B2, B3, C1) that carry none.
    """
    text = Path(rubric_path).read_text(encoding="utf-8")
    stop = text.find("\n## Checks")
    stop = stop if stop > 0 else len(text)
    out = []
    for m in ROW_HEAD.finditer(text):
        if m.start() >= stop:
            continue
        pts = PTS.search(m.group(2))
        if pts:
            out.append((m.group(1), int(pts.group(1))))
    return out


# ----------------------------------------------------------- timing table ---
_TIME = re.compile(r'^(\d{1,3}):([0-5]\d)$')


def _clean(cell):
    return re.sub(r"[*_` ]", "", cell or "").strip()


def _seconds(cell):
    c = _clean(cell)
    m = _TIME.match(c)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    if re.fullmatch(r"\d+(?:\.\d+)?", c):     # bare minutes, e.g. '2.5'
        return int(round(float(c) * 60))
    return None


def parse_timing_tables(text):
    """Every per-item timing table in a markdown document.

    A table qualifies when its header row is made of `item`/`time` cells --
    one pair or several side by side. Returns a list of
    {"items": {label: seconds}, "declared_total": seconds|None,
     "line": header line number}.
    """
    lines = text.split("\n")
    tables = []
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("|"):
            continue
        head = [_clean(c).lower() for c in ln.strip().strip("|").split("|")]
        if not head or "item" not in head or "time" not in head:
            continue
        if not set(head) <= {"item", "time", ""}:
            continue
        if i + 1 >= len(lines) or not re.match(r"\s*\|[\s|:-]+\|?\s*$",
                                              lines[i + 1]):
            continue
        items, declared = {}, None
        for j in range(i + 2, len(lines)):
            row = lines[j]
            if not row.lstrip().startswith("|"):
                break
            cells = [c for c in row.strip().strip("|").split("|")]
            for k in range(0, len(cells) - 1, 2):
                label, val = _clean(cells[k]), cells[k + 1]
                if not label:
                    continue
                if label.upper() == "TOTAL":
                    declared = _seconds(val)
                    continue
                secs = _seconds(val)
                if secs is not None:
                    items[label] = secs
        if items:
            tables.append({"items": items, "declared_total": declared,
                           "line": i + 1})
    return tables


def pilot_tables(exam_dir):
    """[(path, table)] for every timing table under the exam directory.

    Looked for in the exam directory itself and in `reviews/`, which is where
    the midterm's human pilot landed.
    """
    d = Path(exam_dir)
    found = []
    for p in sorted(list(d.glob("*.md")) + list((d / "reviews").glob("*.md"))):
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for t in parse_timing_tables(text):
            found.append((p, t))
    return found


# --------------------------------------------------------------- verdicts ---
def _rel(p):
    """Path as written in the repo, whether it came in absolute or relative."""
    p = Path(p)
    try:
        return p.resolve().relative_to(ROOT)
    except ValueError:
        return p


def mmss(seconds):
    sign = "-" if seconds < 0 else ""
    s = int(round(abs(seconds)))
    return f"{sign}{s // 60}:{s % 60:02d}"


def assess(exam_dir, today=None):
    """The whole row-budget verdict for one exam directory.

    Returns {"name", "config", "rows", "points", "pilots": [...],
             "findings": [(severity, what, detail)], "past": bool}
    where severity is one of "pass", "warn", "fail" and the caller maps those
    onto its own report. Margins are reported whether or not anything failed:
    a check that only speaks on failure teaches nobody where the edge is.
    """
    d = Path(exam_dir)
    d = d if d.is_absolute() else ROOT / d
    today = today or datetime.date.today()
    cfg = load_config(d)
    past = bool(cfg["date"] and cfg["date"] < today)
    budget_s = cfg["item_time_minutes"] * 60
    out = {"name": d.name, "config": cfg, "past": past, "pilots": [],
           "findings": [], "rows": None, "points": None}

    rubric = d / "rubric.md"
    if not rubric.is_file():
        out["findings"].append(
            ("warn", f"{d.name}: no rubric.md, so no row count",
             f"expected {_rel(rubric)}"))
        return out

    rows = scored_rows(rubric)
    out["rows"], out["points"] = len(rows), sum(p for _, p in rows)
    n = len(rows)
    if n == 0:
        out["findings"].append(
            ("fail", f"{d.name}: rubric.md declares no scored rows",
             "every row heading must carry '· N pts' -- either the paper "
             "is empty or the rubric's heading style has moved"))
        return out

    rate = cfg["item_time_minutes"] / n
    cap = cfg["rows_cap"]
    how = "derived" if cfg["rows_cap_derived"] else "set explicitly"
    out["findings"].append(
        ("pass" if n <= cap else ("warn" if past else "fail"),
         f"{d.name}: {n} scored rows against a cap of {cap}"
         + ("" if n <= cap else f" — {n - cap} over"),
         f"{cfg['item_time_minutes']:.0f} min of item time at "
         f"{cfg['target_minutes_per_row']} min/row = {cap} rows ({how}); "
         f"{out['points']} points across {n} rows"))
    out["findings"].append(
        ("pass" if rate >= cfg["floor_minutes_per_row"]
         else ("warn" if past else "fail"),
         f"{d.name}: {rate:.2f} min/row against a {cfg['floor_minutes_per_row']}"
         f" min floor",
         f"{cfg['item_time_minutes']:.0f} min / {n} rows. Margin "
         f"{rate - cfg['floor_minutes_per_row']:+.2f} min/row against the "
         f"floor, {rate - cfg['target_minutes_per_row']:+.2f} against the "
         f"{cfg['target_minutes_per_row']} min/row target"))

    pilots = pilot_tables(d)
    if not pilots:
        out["findings"].append(
            ("warn", f"{d.name}: no pilot timing table found",
             "the pilot's per-item table is a build artifact, not an email. "
             "Ask the tester for per-item times at quarter-minute resolution "
             "and commit the table into this directory or its reviews/ "
             "subdirectory. Shape: a markdown table whose header cells are "
             "'item' and 'time', times as m:ss. See "
             "private/midterm/reviews/human-pilot-2026-10-12.md"))
        return out

    for path, t in pilots:
        total = sum(t["items"].values())
        frac = total / budget_s
        rec = {"path": path, "items": len(t["items"]), "total": total,
               "declared": t["declared_total"], "fraction": frac,
               "line": t["line"]}
        out["pilots"].append(rec)
        where = f"{_rel(path)}:{t['line']}"
        margin = budget_s - total
        detail = (f"{len(t['items'])} timed items summing to {mmss(total)} of "
                  f"{cfg['item_time_minutes']:.0f}:00 budget — "
                  f"{frac:.0%}, margin {mmss(margin)}\n{where}")
        if t["declared_total"] is not None and \
                abs(t["declared_total"] - total) > 15:
            out["findings"].append(
                ("warn", f"{d.name}: pilot table's own TOTAL does not add up",
                 f"table says {mmss(t['declared_total'])}, its items sum to "
                 f"{mmss(total)}\n{where}"))
        if total > budget_s:
            sev = "warn" if past else "fail"
            out["findings"].append(
                (sev, f"{d.name}: pilot total EXCEEDS the item-time budget",
                 detail + "\nCut scored skills, not redundancy: cutting "
                 "redundancy does not reduce the number of distinct things a "
                 "student must parse and set up, and breadth is what costs "
                 "minutes."))
        elif frac > cfg["warn_fraction"]:
            out["findings"].append(
                ("warn", f"{d.name}: pilot total is "
                         f"{frac:.0%} of budget, over the "
                         f"{cfg['warn_fraction']:.0%} band",
                 detail + "\nA pilot total above this band means cutting "
                 "scored skills. Two testers at 98% and 100%+ in October was "
                 "not a near miss; it was the finding."))
        else:
            out["findings"].append(
                ("pass", f"{d.name}: pilot total {mmss(total)} is "
                         f"{frac:.0%} of budget", detail))
    return out
