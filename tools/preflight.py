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
import importlib
import json
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

    plans = list((ROOT / "sessions").glob(f"{sid}-*/README.md"))
    rep.add(OK if plans else FAIL, "session plan",
            plans[0].relative_to(ROOT) if plans else "no sessions/%s-*/README.md" % sid)

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
    srcs = sorted((ROOT / "handouts").glob(f"{sid}-*.md"))
    boards = sorted((ROOT / "board-notes").glob(f"{sid}-*.md"))
    if not srcs:
        rep.add(WARN, "handout", f"no handouts/{sid}-*.md (not every session has one)")
    for s in srcs + boards:
        pdf = s.with_suffix(".pdf")
        if not pdf.exists():
            rep.add(FAIL, f"{s.name} -> PDF", "run: python tools/build_handouts.py " + sid)
        elif pdf.stat().st_mtime < s.stat().st_mtime:
            rep.add(FAIL, f"{s.name} PDF is STALE", "run: python tools/build_handouts.py " + sid)
        else:
            n_pages = _pages(pdf)
            odd = (n_pages or 0) % 2
            rep.add(WARN if odd and "board" not in s.name else OK,
                    f"{pdf.name} ({n_pages} pages)",
                    "odd page count duplexes onto a wasted sheet" if odd and "board" not in s.name else "")

    if srcs and not any("-answers" in s.name for s in srcs):
        rep.add(WARN, "answer sheet", "no handouts/%s-*-answers.md — students get nothing back" % sid)

    # the copies that actually go to the printer live outside the repo
    printdir = ROOT.parent / "2026" / "handouts-to-print"
    for s in srcs:
        if "-answers" in s.name:
            continue
        copy = printdir / f"{s.stem}-PRINT-THIS.pdf"
        src_pdf = s.with_suffix(".pdf")
        if not copy.exists():
            rep.add(WARN, f"{copy.name}", "not staged for printing yet")
        elif src_pdf.exists() and copy.stat().st_mtime < src_pdf.stat().st_mtime:
            rep.add(FAIL, f"{copy.name} is STALE",
                    f"cp {src_pdf.relative_to(ROOT.parent)} {copy.relative_to(ROOT.parent)}")


def _pages(pdf):
    try:
        return sum(1 for _ in __import__("re").finditer(
            rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    except Exception:
        return None


# --------------------------------------------------------------- readings ---
def check_readings(n, rep):
    ok, out = run(["tools/build_readings.py"])
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

    dist = ROOT / "private" / "build" / tag / "dist" / "autograder"
    zips = sorted(dist.glob("*.zip")) if dist.is_dir() else []
    rep.add(OK if zips else FAIL, f"{tag} autograder zip",
            zips[-1].relative_to(ROOT) if zips else
            f"run: python tools/build_problem_sets.py {tag}")
    if zips:
        _check_zip(zips[-1], tag, rep)


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
    check_repo(rep)

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
