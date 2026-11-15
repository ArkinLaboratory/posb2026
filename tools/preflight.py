#!/usr/bin/env python3
"""Everything a session or problem set must satisfy before it is released.

    python tools/preflight.py 5          # session 5 and anything it posts
    python tools/preflight.py 5 --ps 2   # ...and PS2 explicitly
    python tools/preflight.py --all      # every built session

WHY THIS EXISTS
The release ritual has two halves. One half is mechanical -- does the deck
build, is the handout PDF stale, is the notebook actually on `main`, is the
print copy older than the file it came from -- and a human running that half
from a checklist will eventually skip a line at 7am. The other half is
irreducibly manual: clicking in Gradescope and Canvas, which no script here can
or should do.

So this tool owns the whole of the first half, and
docs/session-release-checklist.md owns the second and says so. If you find
yourself adding a *derivable* check to that document, add it here instead.

Exit code is 0 only when every blocking check passes. WARN items do not block:
they are things that are missing on purpose sometimes (a session with no
notebook, a handout with no answer sheet yet).
"""
import argparse
import datetime
import importlib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OK, WARN, FAIL = "PASS", "WARN", "FAIL"
_MARK = {OK: "\033[32mPASS\033[0m", WARN: "\033[33mWARN\033[0m",
         FAIL: "\033[31mFAIL\033[0m"}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, what, detail=""):
        self.rows.append((status, what, detail))

    def show(self, title):
        print(f"\n{title}")
        print("=" * max(len(title), 62))
        for status, what, detail in self.rows:
            print(f"  {_MARK[status]}  {what}")
            if detail:
                for line in str(detail).rstrip().split("\n"):
                    print(f"        \033[2m{line}\033[0m")

    @property
    def blocking(self):
        return [r for r in self.rows if r[0] == FAIL]


def run(cmd):
    """Run a repo tool. Returns (ok, combined output)."""
    p = subprocess.run([sys.executable, *cmd], cwd=ROOT,
                       capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def tail(text, n=4):
    lines = [l for l in text.split("\n") if l.strip()]
    return "\n".join(lines[-n:])


# ---------------------------------------------------------------- session ---
def check_session(n, rep):
    sid = f"s{n:02d}"
    from tools.schedule import sessions
    meta = sessions().get(n)
    if meta is None:
        rep.add(FAIL, f"session {n} is not in course.yaml")
        return
    rep.add(OK, f"session {n} — {meta['date']:%A %d %B} — {meta.get('title','')}")

    # Early sessions carry README.md; sessions 20 onward carry DESIGN.md
    # with NUMBERS.md and REBUILD beside it. Accepting only README.md left
    # this gate red for four consecutive sessions with nothing to fix, and
    # a permanently red line is how a reader learns to discount the report
    # it sits in -- which is what this tool's own docstring warns about.
    plans = (sorted((ROOT / "sessions").glob(f"{sid}-*/README.md"))
             or sorted((ROOT / "sessions").glob(f"{sid}-*/DESIGN.md")))
    rep.add(OK if plans else FAIL, "session plan",
            plans[0].relative_to(ROOT) if plans
            else f"no sessions/{sid}-*/README.md or DESIGN.md")

    decks = list((ROOT / "decks").glob(f"{sid}_*.py"))
    if not decks:
        rep.add(FAIL, "deck source", f"no decks/{sid}_*.py")
        return
    name = decks[0].stem
    ok, out = run(["tools/build_decks.py", name, "--check"])
    rep.add(OK if ok else FAIL, f"deck builds clean ({name})", "" if ok else tail(out))
    for flag, label in [("no glyph", "missing font glyphs"),
                        ("shown as slots", "paper figures not embedded"),
                        ("too few slides", "under-slided segments"),
                        ("longer than", "over-long student block")]:
        if flag in out:
            rep.add(WARN, f"deck: {label}", tail(out, 3))

    # a taught deck must have a PDF to upload
    build = ROOT / "private" / "build" / "decks"
    mod = importlib.import_module(f"decks.{name}")
    pptx = build / f"{mod.FILENAME}.pptx"
    pdf = build / f"{mod.FILENAME}.pdf"
    rep.add(OK if pdf.exists() else WARN, "deck PDF built (for bCourses)",
            "" if pdf.exists() else "run: python tools/build_decks.py --pdf " + name)

    # THE THURSDAY-MORNING CHECK. Everything above asks whether the SOURCE is
    # right. This asks whether the FILE YOU WILL OPEN was made from it. The
    # sequence that breaks it is ordinary: the deck is built and approved on
    # Wednesday, the source is edited Wednesday night, and on Thursday nothing
    # says the .pptx on disk predates the edit. Hashes, not mtimes -- see
    # tools/manifest.py for why.
    from tools import manifest
    for art, what in [(pptx, "deck .pptx"), (pdf, "deck .pdf")]:
        status, detail = manifest.verify(art)
        if status == "absent":
            rep.add(WARN, f"{what} on this machine", manifest.LABEL[status])
        elif status in manifest.FAIL:
            rep.add(FAIL, f"{what}: {manifest.LABEL[status]}",
                    "\n".join(f"{how:<8} {p}" for p, how in detail[:6])
                    + ("\n" if detail else "")
                    + "run: python tools/build_decks.py --pdf " + name)
        else:
            rep.add(OK, f"{what} matches its sources")

    # ...and whether the copy you present from predates a source change.
    #
    # NOT a content comparison. Every deck in private/taught/ carries
    # docProps Application="Microsoft Macintosh PowerPoint", AppVersion 16,
    # lastModifiedBy "Adam Arkin" -- all four of them -- while the build is
    # pristine python-pptx (AppVersion 14, "Steve Canny", the template's
    # author). The taught copy is always a PowerPoint round-trip, so it never
    # matches the build byte-for-byte OR content-for-content, and a check that
    # compares them fires on every session forever.
    #
    # It also means overwriting a taught copy with `cp` destroys whatever was
    # done to it in PowerPoint. So this reports and never proposes a copy.
    #
    # What IS worth knowing: was the copy made before or after the sources
    # changed? Both files are local and both are produced here, so mtime
    # answers that -- the objection in manifest.py is about files that travel
    # between machines, which these do not.
    import datetime
    import json as _json

    if meta["date"] < datetime.date.today():
        # Afterwards the two are SUPPOSED to diverge: taught/ is a record of
        # what was shown, and the source keeps moving. Comparing a past session
        # turns a correct, permanent difference into a permanent FAIL.
        copies = sorted(p for p in (ROOT / "private" / "taught").glob(f"*Session{n:02d}*.pptx")
                    if not p.name.startswith("~$"))   # PowerPoint lock file, not a deck
        rep.add(OK if copies else WARN, f"private/taught/ record for session {n}",
                f"{copies[0].name} — as shown on {meta['date']:%d %B}; "
                f"divergence from the current source is expected" if copies
                else "no record of what was actually shown")
        return

    copies = sorted(p for p in (ROOT / "private" / "taught").glob(f"*Session{n:02d}*.pptx")
                    if not p.name.startswith("~$"))   # PowerPoint lock file, not a deck
    if not copies:
        rep.add(WARN, f"private/taught/ has no deck for session {n}",
                "not approved for teaching yet")
        return

    want = manifest.deck_content(pptx)
    for c in copies:
        got = manifest.deck_content(c)
        if got is None or want is None:
            rep.add(WARN, f"{c.name} could not be read")
            continue
        wt, wm, wn = want
        gt, gm, gn = got
        why = []
        if gn != wn:
            why.append(f"slide count {gn} vs {wn} in the build")
        if gt != wt:
            why.append("the slide TEXT differs")
        if gm != wm:
            why.append("an embedded FIGURE differs")
        stamp = datetime.datetime.fromtimestamp(c.stat().st_mtime)
        if why:
            rep.add(FAIL, f"{c.name} is not the current deck",
                    "; ".join(why) +
                    f"\ncopied {stamp:%d %b %H:%M}. Do NOT cp over it blind — "
                    f"PowerPoint saved this file, so it may carry edits that are "
                    f"not in decks/{name}.py. Diff first, port anything you want "
                    f"to keep back into the source, then rebuild and re-copy.")
        else:
            rep.add(OK, f"{c.name} matches the build on text and figures",
                    f"copied {stamp:%d %b %H:%M}; styling not compared, since "
                    f"PowerPoint rewrites it on save")


# --------------------------------------------------------------- handouts ---
def check_handouts(n, rep):
    sid = f"s{n:02d}"
    # Answers and board notes moved into private/ on 18 October -- they were
    # being published to a public repo from handouts/ and board-notes/.
    srcs = sorted((ROOT / "handouts").glob(f"{sid}-*.md")) + \
        sorted((ROOT / "private" / "handouts").glob(f"{sid}-*.md"))
    boards = sorted((ROOT / "private" / "board-notes").glob(f"{sid}-*.md"))
    if not srcs:
        rep.add(WARN, "handout", f"no handouts/{sid}-*.md (not every session has one)")
    # Staleness is the stamp's question, not the filesystem's. An mtime
    # comparison says only which of the two files was written last, and on
    # 1 November it was wrong in BOTH directions at once:
    # s22-control-answers.pdf was reported STALE on a four-day-old mtime while
    # its recorded digest matched its source exactly and all four pages were
    # pixel-identical to a fresh render -- and four genuinely stale s20/s21
    # handouts PASSED, two days before session 20 is taught, because their
    # PDFs happened to have been written after their sources. The false pass
    # is the worse half. build_handouts.py --check compares the digest the
    # build recorded against the digest the source produces now, which is the
    # question being asked.
    _, _ho = run(["tools/build_handouts.py", "--check"])
    stale_now = set()
    if "stale:" in _ho:
        stale_now = {x.strip() for x in
                     _ho.split("stale:", 1)[1].split(". Run")[0].split(",")
                     if x.strip()}

    for s in srcs + boards:
        pdf = s.with_suffix(".pdf")
        if not pdf.exists():
            rep.add(FAIL, f"{s.name} -> PDF", "run: python tools/build_handouts.py " + sid)
        elif s.name in stale_now:
            rep.add(FAIL, f"{s.name} PDF is STALE", "run: python tools/build_handouts.py " + sid)
        else:
            # The odd-page-count warning was a duplexing concern. Handouts
            # became home guides -- read on a screen the evening after class,
            # answers posted beside them -- and are not printed, so an odd
            # page count costs nothing. Adam, 2 November 2026: "We stopped
            # printing handouts.. they are home guides."
            rep.add(OK, f"{pdf.name} ({_pages(pdf)} pages)", "")

    if srcs and not any("-answers" in s.name for s in srcs):
        rep.add(WARN, "answer sheet", "no private/handouts/%s-*-answers.md — students get nothing back" % sid)

    # REMOVED 7 November 2026 -- the staged print copy.
    #
    # 2026/handouts-to-print/ held a hand-made -PRINT-THIS.pdf per handout, and
    # this block warned when one was missing and FAILED when one was stale.
    # Handouts are home guides now and nothing is printed, so every session
    # from 20 on opened with a WARN nobody could clear and the folder stopped
    # at s19. A check that cannot be satisfied trains you to read past the
    # whole WARN column, which is the real cost. The folder is left alone.


def _pages(pdf):
    try:
        return sum(1 for _ in __import__("re").finditer(
            rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    except Exception:
        return None


# --------------------------------------------------------------- readings ---
def check_readings(n, rep):
    # --report, not the bare command: the default rewrites docs/readings.md,
    # which is tracked, so preflight used to dirty the working tree on every
    # run. --check would not dirty it either but prints no assignment chain,
    # which is the thing the loop below reads.
    ok, out = run(["tools/build_readings.py", "--report"])
    rep.add(OK if ok else FAIL, "readings.yaml validates", "" if ok else tail(out))
    for line in out.split("\n"):
        if f"discusses" in line and f"s{n:02d} assigns" in line:
            rep.add(OK, "this session hands out a paper", line.strip())


# ------------------------------------------------------------ problem set ---
def check_ps(num, rep):
    tag = f"ps{num:02d}"
    master = ROOT / "private" / "sources" / f"{tag}.py"
    rep.add(OK if master.exists() else FAIL, f"{tag} master", master.relative_to(ROOT))
    nbs = list((ROOT / "problem-sets").glob(f"{tag}-*/{tag}.ipynb"))
    if not nbs:
        rep.add(FAIL, f"{tag} student notebook", f"run: python tools/build_problem_sets.py {tag}")
        return
    nb = nbs[0]
    rep.add(OK, f"{tag} student notebook", nb.relative_to(ROOT))

    # the failure you cannot take back
    src = "\n".join("".join(c.get("source", []))
                    for c in json.loads(nb.read_text())["cells"])
    leaks = [w for w in ("BEGIN SOLUTION", "END SOLUTION", "hidden: true") if w in src]
    rep.add(FAIL if leaks else OK, f"{tag} notebook contains no solutions",
            "LEAKED: " + ", ".join(leaks) if leaks else "")

    desc = ROOT / "private" / "build" / tag / "canvas-description.html"
    readme_p = nb.parent / "README.md"
    if not desc.exists():
        rep.add(WARN, f"{tag} Canvas description not built",
                f"run: python tools/build_canvas_description.py {tag}")
    elif readme_p.exists() and desc.stat().st_mtime < readme_p.stat().st_mtime:
        rep.add(FAIL, f"{tag} Canvas description is STALE",
                f"run: python tools/build_canvas_description.py {tag}")
    else:
        rep.add(OK, f"{tag} Canvas description", desc.relative_to(ROOT))

    readme = nb.parent / "README.md"
    rep.add(OK if readme.exists() else FAIL, f"{tag} README (this IS the Canvas description)",
            readme.relative_to(ROOT) if readme.exists() else "missing")
    if readme.exists():
        body = readme.read_text()
        for needle, what in [("datahub.berkeley.edu", "DataHub link"),
                             ("colab.research.google.com", "Colab link")]:
            rep.add(OK if needle in body else FAIL, f"{tag} README carries the {what}")

    # The artifact that makes "confirm full marks" a step you can actually run.
    # Without it the only submittable notebook is the student one, which scores
    # zero by construction, and the master, which otter rejects outright with
    # "Received submission for assignment 'None'".
    solved = ROOT / "private" / "build" / tag / f"{tag}-solved.ipynb"
    if not solved.exists():
        rep.add(WARN, f"{tag} solved notebook not built",
                f"run: python tools/build_problem_sets.py {tag}  "
                f"(needed to test the autograder)")
    else:
        meta = json.loads(solved.read_text()).get("metadata", {}).get("otter", {})
        got = meta.get("assignment_name")
        if got != tag:
            rep.add(FAIL, f"{tag} solved notebook has the wrong identity",
                    f"assignment_name={got!r}, expected {tag!r} -- "
                    f"Gradescope will reject it")
        elif solved.stat().st_mtime < master.stat().st_mtime:
            rep.add(FAIL, f"{tag} solved notebook is STALE",
                    f"run: python tools/build_problem_sets.py {tag}")
        else:
            rep.add(OK, f"{tag} solved notebook (submit to test the autograder)",
                    solved.relative_to(ROOT))

    dist = ROOT / "private" / "build" / tag / "dist" / "autograder"
    zips = sorted(dist.glob("*.zip")) if dist.is_dir() else []
    rep.add(OK if zips else FAIL, f"{tag} autograder zip",
            zips[-1].relative_to(ROOT) if zips else
            f"run: python tools/build_problem_sets.py {tag}")
    if zips:
        _check_zip(zips[-1], tag, rep)


def _manual_questions(master_text):
    """The manually graded questions a master declares, as {name: points}.

    A question block is `name: qN`, `points: K` and `manual: true` in any
    order inside one otter config string, so match on the name and then look
    for the other two keys within the same block.
    """
    out = {}
    for m in re.finditer(r"name:\s*(q[0-9a-z]+)((?:\\n[a-z_]+:\s*[^\\\"']+)*)",
                         master_text):
        name, rest = m.group(1), m.group(2)
        if "manual: true" not in rest:
            continue
        pts = re.search(r"points:\s*([0-9]+)", rest)
        out[name] = int(pts.group(1)) if pts else None
    return out


def check_reader_brief(num, rep):
    """A set with manually graded questions needs a brief the reader can use.

    This is the gate that was missing. PS6, PS7 and PS8 were built, released
    and (for two of them) graded with no brief at all, because nothing asked.
    The brief is to the manual half what the solved notebook is to the
    autograded half, and it gets the same two checks -- it exists, and it is
    not older than the master it was written from -- plus a coverage check,
    because a brief that is merely PRESENT can still be missing half the
    questions and nothing would say so.
    """
    tag = f"ps{num:02d}"
    master = ROOT / "private" / "sources" / f"{tag}.py"
    if not master.exists():
        return
    manual = _manual_questions(master.read_text())
    if not manual:
        rep.add(OK, f"{tag} has no manually graded questions", "no reader brief needed")
        return

    total = sum(v for v in manual.values() if v)
    names = ", ".join(sorted(manual))
    brief = ROOT / "private" / "reader-briefs" / f"{tag}.md"
    if not brief.exists():
        rep.add(FAIL, f"{tag} reader brief MISSING",
                f"{len(manual)} manual question(s) worth {total} points "
                f"({names}) have no marking instructions.\n"
                f"write: private/reader-briefs/{tag}.md  "
                f"(bar: private/review/brief-bar.md)")
        return

    body = brief.read_text()

    # Staleness by CONTENT, not mtime. A brief and its master are written in
    # one sitting and land seconds apart in either order (ps04: master 46 s
    # newer, nothing wrong), and a master can be touched afterwards for a line
    # that cannot invalidate a marking rule (ps05: the out-date, 4 October).
    # An mtime gate reports both as failures, and a gate that is always red is
    # a gate nobody reads. So a brief carries the hash of the master it was
    # checked against, in a trailer:
    #
    #     <!-- checked-against: sha256:<64 hex> on YYYY-MM-DD -->
    #
    # which is the same contract as the .build/*.sha sidecars, kept inside the
    # one human-readable file so it cannot drift away from what it describes.
    want = hashlib.sha256(master.read_bytes()).hexdigest()
    stamp = re.search(r"checked-against:\s*sha256:([0-9a-f]{64})(?:\s+on\s+(\S+))?",
                      body)
    if not stamp:
        delta = master.stat().st_mtime - brief.stat().st_mtime
        rep.add(WARN, f"{tag} reader brief carries no checked-against stamp",
                f"cannot tell whether it matches the master "
                f"(master is {delta:+.0f}s relative to the brief).\n"
                f"after checking it, append:\n"
                f"    <!-- checked-against: sha256:{want} on YYYY-MM-DD -->")
    elif stamp.group(1) != want:
        rep.add(FAIL, f"{tag} reader brief is STALE",
                f"checked against sha256:{stamp.group(1)[:12]}…"
                f"{' on ' + stamp.group(2) if stamp.group(2) else ''}, "
                f"master is now sha256:{want[:12]}…\n"
                f"a solution or a point value may have moved under it -- "
                f"re-check against private/sources/{tag}.py, then restamp")
    else:
        rep.add(OK, f"{tag} reader brief matches its master",
                f"{brief.relative_to(ROOT)}  sha256:{want[:12]}…"
                f"{' checked ' + stamp.group(2) if stamp.group(2) else ''}")

    missing = [q for q in sorted(manual)
               if not re.search(rf"\b{q}\b", body, re.I)]
    rep.add(FAIL if missing else OK,
            f"{tag} reader brief covers every manual question",
            f"not mentioned: {', '.join(missing)}" if missing
            else f"{len(manual)} question(s), {total} points")


def _check_zip(zpath, tag, rep):
    """Two things about the zip that no eye catches and Gradescope will not tell
    you.

    THE POINT TOTAL. Gradescope's "Autograder Points" field must be the
    autograded subtotal alone -- the manual questions are added by the rubric --
    and that subtotal lives nowhere except inside the zip's test files. Typing
    the whole-set total there is silent: every student's score is simply wrong
    by the manual points, and the first person to notice is a student.

    THE FROZEN COPY OF posb/. The zip carries files/posb/, so once the Docker
    image is built the autograder runs against THAT snapshot -- while the
    student's notebook, pulled fresh from `main` by nbgitpuller, imports the
    current one. Edit posb/data.py after the build and the synthetic data the
    student fits is not the synthetic data the hidden test checks. Nothing
    anywhere reports this; the submission just fails.
    """
    import ast
    import zipfile

    z = zipfile.ZipFile(zpath)

    total, per = 0, []
    for n in sorted(z.namelist()):
        if not (n.startswith("tests/") and n.endswith(".py")):
            continue
        body = z.read(n).decode()
        try:
            ns = {}
            exec(compile(ast.parse(body), n, "exec"), ns)      # OK_FORMAT dict
            pts = ns["test"]["points"]
        except Exception:
            rep.add(WARN, f"{tag}: cannot read points from {n}")
            continue
        total += pts
        per.append(f"{ns['test']['name']} {pts}")
    rep.add(OK, f"{tag} AUTOGRADER POINTS = {total}   <- type this into Gradescope",
            "  ".join(per) + "\n(manual questions are added by the rubric, not here)")

    drift = []
    for n in z.namelist():
        if not n.startswith("files/posb/") or not n.endswith(".py"):
            continue
        repo = ROOT / n[len("files/"):]
        import hashlib
        inzip = hashlib.sha256(z.read(n)).hexdigest()
        onrepo = hashlib.sha256(repo.read_bytes()).hexdigest() if repo.is_file() else None
        if inzip != onrepo:
            drift.append(n[len("files/"):] + (" (missing from repo)" if onrepo is None else ""))
    rep.add(FAIL if drift else OK,
            f"{tag} zip's posb/ matches the repo"
            if not drift else f"{tag} zip's posb/ is BEHIND the repo",
            "" if not drift else
            "\n".join(drift) + f"\nthe autograder would run against a different "
            f"posb/ than the student imports.\nrun: python tools/build_problem_sets.py {tag}"
            f"  and re-upload the zip")


# -------------------------------------------------------------- repo-wide ---
def check_repo(rep):
    for cmd, label in [(["tools/check_doc_links.py"], "every relative doc link resolves"),
                       (["tools/check_schedule.py"], "schedule is consistent"),
                       (["tools/check_links.py"], "every committed notebook is reachable on main"),
                       (["tools/build_figures.py", "--verify"], "figures match their generators")]:
        ok, out = run(cmd)
        rep.add(OK if ok else FAIL, label, "" if ok else tail(out, 6))


# ------------------------------------------------- the platform, imported ---
#
# Everything above this line asks about files. These three gates ask about
# things that were written down as prose and never executed, and each one has
# already cost a term's worth of damage:
#
#   1. the bCourses upload settings, which refused a package M3's own
#      description asked for;
#   2. the graded items due soon whose platform state nobody has looked at;
#   3. the exam row count, which decision 18 said to check against the pilot's
#      timing table and which nothing checked.
#
# None of them need a network. The platform half is imported to disk by
# tools/import_platform_manifest.py and read from there.


def _syllabus_items(rep):
    """The syllabus's graded items, or None after reporting the parse failure.

    A table parse that silently matches nothing is a check that has stopped
    checking while still reporting green -- the same class of defect as prose
    nobody executes. So the parse raises and this reports it as blocking.
    """
    from tools import graded_items as gi
    try:
        items = gi.all_graded()
    except gi.SyllabusParseError as e:
        rep.add(FAIL, "syllabus graded-item tables parse", str(e))
        return None
    pkg = [i.ident for i in items if i.needs_package]
    rep.add(OK, f"syllabus graded-item tables parse ({len(items)} items)",
            f"{sum(1 for i in items if i.kind in ('milestone', 'final-proposal'))} "
            f"milestone/final, {sum(1 for i in items if i.kind == 'ps')} sets, "
            f"{sum(1 for i in items if i.kind == 'exam')} exams; "
            f"deliverable includes a package: {', '.join(pkg) or 'none'}")
    # course.yaml carries no graded due dates, so it cannot be the authority
    # for one -- but it does carry the term, and a weekday the syllabus claims
    # is checkable against it. "Thu Nov 12" that is not a Thursday is a typo
    # that students read before anyone else does.
    bad = [f"{i.ident}: syllabus says {i.weekday_claimed.title()}, "
           f"{i.due:%d %B %Y} is a {i.due:%A}  (syllabus.md:{i.line})"
           for i in items if not i.weekday_ok]
    rep.add(FAIL if bad else OK, "every graded due date falls on the weekday "
            "the syllabus claims", "\n".join(bad))
    return items


def check_platform(rep):
    """GATE 1. Does the platform let students hand in what the syllabus asks for?

    M3 was created on bCourses by copying M1 and M2, which carried
    allowed_extensions ["pdf"]. M3 is the first milestone whose deliverable
    includes a code package, and its own Canvas description said so -- "Four to
    five pages, PDF, plus the first version of your package" -- while its
    upload settings refused anything but PDF. Nineteen students submitted
    write-ups and four emailed their packages overnight. The identical defect
    was then found waiting on the graded final project, due 14 December.

    Both facts needed to catch it were knowable with no network: the syllabus
    Length column says a package is handed in, and the platform said pdf-only.
    Nothing held both at once.

    The missing manifest is itself the finding, so this runs even when there is
    nothing to read. Silence there would re-create the defect exactly -- nobody
    looking at the platform, and nothing saying so.
    """
    from tools import graded_items as gi
    items = _syllabus_items(rep)
    if items is None:
        return
    deliverables = [i for i in items
                    if i.kind in ("milestone", "final-proposal")]

    man = gi.load_manifest()
    if man is None:
        rep.add(WARN, "bCourses platform state has never been imported",
                f"{gi.rel(gi.MANIFEST)} does not exist, so the "
                f"upload settings of {len(deliverables)} graded deliverable(s) "
                f"are unchecked -- including "
                f"{', '.join(i.ident for i in deliverables if i.needs_package)}"
                f", whose deliverable includes a package.\n"
                f"In a session with browser access, fetch\n"
                f"    /api/v1/courses/1557313/assignments?per_page=100\n"
                f"save the body, then run:\n"
                f"    python tools/import_platform_manifest.py <that file>")
        return

    stamps = []
    for item in deliverables:
        e = gi.match_entry(item, man)
        if e is None:
            rep.add(FAIL, f"{item.ident} has no entry in the platform manifest",
                    f"the syllabus has it due {item.due:%a %d %b} "
                    f"(syllabus.md:{item.line}) and the imported platform state "
                    f"does not mention it. Either the assignment does not "
                    f"exist on bCourses or the import missed it -- re-import, "
                    f'and if the name does not carry "{item.ident}", add '
                    f'"item": "{item.ident}" to its manifest entry by hand.')
            continue
        read_at = gi.entry_read_at(e, man)
        if read_at:
            stamps.append((read_at, item.ident))
        name = e.get("name") or f"id {e.get('id')}"
        ext = [str(x).lower().lstrip(".")
               for x in (e.get("allowed_extensions") or [])]
        if item.needs_package and gi.pdf_only(e):
            rep.add(FAIL,
                    f"{item.ident} asks for a package and bCourses refuses "
                    f"everything but PDF",
                    f'syllabus.md:{item.line} Length column reads '
                    f'"{item.length}"\n'
                    f'bCourses "{name}" (id {e.get("id")}) has '
                    f'allowed_extensions {ext}\n'
                    f"A student with a working package cannot upload it. This "
                    f"is the M3 defect: fix the assignment's Allowed File "
                    f"Extensions on bCourses (add zip, ipynb, py, or clear the "
                    f"list), then re-import the manifest.")
        elif item.needs_package:
            rep.add(OK, f"{item.ident} accepts a package",
                    f'"{item.length}" vs allowed_extensions '
                    f'{ext or "[any]"}')
        else:
            rep.add(OK, f"{item.ident} upload settings",
                    f'"{item.length}", allowed_extensions {ext or "[any]"}')
        if not e.get("published", True):
            rep.add(WARN, f"{item.ident} is UNPUBLISHED on bCourses",
                    f'"{name}" -- students cannot see or submit to it')

    # A stale manifest is a check that has stopped checking: it reports on a
    # platform state that may have been copied, edited or re-created since.
    if stamps:
        oldest, which = min(stamps)
        age = (datetime.datetime.now(datetime.timezone.utc) - oldest).days
        rep.add(WARN if age > gi.STALE_DAYS else OK,
                f"platform manifest read {age} day(s) ago"
                + (f" \u2014 older than {gi.STALE_DAYS} days" if age > gi.STALE_DAYS
                   else ""),
                f"oldest entry is {which}, read {oldest:%Y-%m-%d %H:%M} UTC."
                + (" A stale manifest is a check that has stopped checking. "
                   "Re-fetch /api/v1/courses/1557313/assignments?per_page=100 "
                   "and re-run tools/import_platform_manifest.py."
                   if age > gi.STALE_DAYS else ""))


def check_graded_soon(rep):
    """GATE 2. Anything graded that is due soon, and whether anyone has looked.

    docs/session-release-checklist.md carried this as a blockquote: "Still to
    place, when each module is built: M2 in Week 9 (placed 18 Oct), M3 in Week
    12 (due Thu 12 Nov), M4 in Week 15 (due Tue 1 Dec)." It was prose in a
    document rather than a check in the build, and M3's platform state went
    unexamined until two days after its due date.

    This is about attention, not correctness, so it prints the list on every
    run and never blocks. When nothing is inside the horizon it says what is
    next anyway, because a row that disappears when it is quiet is a row you
    stop expecting to see.
    """
    from tools import graded_items as gi
    HORIZON = 14
    try:
        items = gi.all_graded()
    except gi.SyllabusParseError:
        return                       # already reported by check_platform
    man = gi.load_manifest()
    today = datetime.date.today()
    soon = [i for i in items if i.graded and i.due
            and today <= i.due <= today + datetime.timedelta(days=HORIZON)]

    if not soon:
        nxt = [i for i in items if i.graded and i.due and i.due > today]
        rep.add(OK, f"nothing graded is due in the next {HORIZON} days",
                f"next up: {nxt[0].ident} on {nxt[0].due:%a %d %b} "
                f"({(nxt[0].due - today).days} days)" if nxt
                else "nothing graded remains on the syllabus")
        return

    lines, unseen = [], []
    for i in soon:
        days = (i.due - today).days
        e = gi.match_entry(i, man) if man else None
        if e is None:
            why = "no manifest entry" if man else "platform never imported"
        else:
            read_at = gi.entry_read_at(e, man)
            created = gi._utc(e.get("created_at"))
            if read_at is None:
                why = "manifest entry carries no read timestamp"
            elif created and read_at < created:
                why = (f"manifest read {read_at:%d %b} predates the "
                       f"assignment's creation {created:%d %b} \u2014 this "
                       f"entry cannot be describing it")
            else:
                why = None
        lines.append(f"{i.ident:<11} due {i.due:%a %d %b} (in {days:>2}d)  "
                     + (f"\u2717 {why}" if why else "\u2713 platform state read"))
        if why:
            unseen.append(i.ident)

    rep.add(WARN if unseen else OK,
            f"{len(soon)} graded item(s) due within {HORIZON} days"
            + (f"; {len(unseen)} with no examined platform state" if unseen
               else "; all platform states examined"),
            "\n".join(lines)
            + ("\nM3's platform state went unexamined until two days after it "
               "was due. Look at these on bCourses, then re-import: "
               "python tools/import_platform_manifest.py <blob>"
               if unseen else ""))


def check_exam_budget(rep):
    """GATE 3. The exam row budget, against the pilot's own timing table.

    Decision 18, in blueprint.md and in the pilot write-up, in the same words
    both times: "the pilot's per-item timing table is a build artifact, the row
    budget is checked against it mechanically with the margin printed, the
    build fails when a pilot's total exceeds the item-time budget, and a pilot
    total above ~85% of budget means cutting scored skills."

    The margin prints whether or not anything fails. A check that only speaks
    on failure teaches nobody where the edge is, and the 2026 midterm was lost
    in exactly that gap -- the numbers existed, nobody saw them next to each
    other.

    A past exam reports the same arithmetic at WARN. It cannot be fixed and a
    permanent FAIL on it would train a reader to discount this whole report.
    """
    from tools import exam_budget as eb
    from tools import graded_items as gi
    SEV = {"pass": OK, "warn": WARN, "fail": FAIL}
    today = datetime.date.today()

    try:
        exams = [i for i in gi.all_graded() if i.kind == "exam"]
    except gi.SyllabusParseError:
        exams = []
    by_name = {"midterm": "MIDTERM", "final": "FINAL-EXAM"}
    sched = {i.ident: i for i in exams}

    seen = set()
    for name, d in eb.exam_dirs():
        ident = by_name.get(name.lower())
        seen.add(ident)
        item = sched.get(ident)
        past = bool(item and item.due and item.due < today)
        try:
            r = eb.assess(d, today=today)
        except eb.ExamConfigError as e:
            rep.add(WARN if past else FAIL,
                    f"{name}: no usable row budget", str(e))
            continue
        except ValueError as e:
            rep.add(FAIL, f"{name}: budget.json date is unreadable", str(e))
            continue
        for sev, what, detail in r["findings"]:
            rep.add(SEV[sev], what, detail)
        cfg_date = r["config"]["date"]
        if item and item.due and cfg_date and cfg_date != item.due:
            rep.add(FAIL, f"{name}: budget.json and the syllabus disagree on "
                    f"the date",
                    f"budget.json says {cfg_date}, syllabus.md:{item.line} "
                    f"says {item.due}. One of them is what students will "
                    f"believe.")
        elif cfg_date is None:
            rep.add(WARN, f"{name}: budget.json names no date",
                    "without it this gate cannot tell a paper still to be sat "
                    "from a historical record, and reports the strict verdict")

    # An exam with no build directory is the one case the gates above cannot
    # see. Two human pilots, an ambiguity pass and room to cut and rebuild is
    # a month and more of lead time, so this becomes worth saying well before
    # the week of the exam.
    for item in exams:
        if item.ident in seen or not item.due or item.due < today:
            continue
        days = (item.due - today).days
        if days <= eb.LEAD_DAYS:
            rep.add(WARN, f"{item.ident} is in {days} days and has no build "
                    f"directory",
                    f"{item.title} \u2014 {item.due:%a %d %B} "
                    f"(syllabus.md:{item.line}). Nothing under private/ holds "
                    f"an exam.md for it, so there is no row count and no pilot "
                    f"timing table to check. The row cap comes from the "
                    f"minutes BEFORE any item is written: at "
                    f"{eb.DEFAULTS['target_minutes_per_row']} min/row, 120 "
                    f"minutes of item time is "
                    f"{int(120 // eb.DEFAULTS['target_minutes_per_row'])} rows.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?", type=int)
    ap.add_argument("--ps", type=int, default=None)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    rep = Report()
    if a.session:
        check_session(a.session, rep)
        check_handouts(a.session, rep)
        check_readings(a.session, rep)
    if a.ps is not None:
        check_ps(a.ps, rep)
        check_reader_brief(a.ps, rep)
    check_repo(rep)
    # Repo-wide and cheap (file reads, no subprocess), so they run on every
    # invocation for the same reason check_repo does: a gate you have to
    # remember a flag for is a gate that is not on when it matters.
    check_platform(rep)
    check_graded_soon(rep)
    check_exam_budget(rep)

    title = (f"PREFLIGHT — session {a.session}" if a.session else "PREFLIGHT")
    if a.ps is not None:
        title += f" + PS{a.ps}"
    rep.show(title)

    bad = rep.blocking
    print()
    if bad:
        print(f"\033[31m{len(bad)} blocking item(s). Not ready to release.\033[0m")
        print("Everything above is mechanical. The manual half — Gradescope and")
        print("bCourses — is in docs/session-release-checklist.md.")
        sys.exit(1)
    print("\033[32mAll mechanical checks pass.\033[0m")
    print("Now do the manual half: docs/session-release-checklist.md")


if __name__ == "__main__":
    main()
