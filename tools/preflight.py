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

    # ...and whether the copy you actually present from is that build. The deck
    # is presented out of private/taught/, which is a manual `cp`. A rebuild
    # after that copy leaves the two silently different, and the one on the
    # projector is the old one.
    taught = ROOT / "private" / "taught"
    for art, ext in [(pptx, ".pptx"), (pdf, ".pdf")]:
        copies = sorted(taught.glob(f"*Session{n:02d}*{ext}")) if taught.is_dir() else []
        if not art.is_file():
            continue
        if not copies:
            rep.add(WARN, f"private/taught/ has no {ext} for session {n}",
                    "not approved for teaching yet")
            continue
        for c in copies:
            same = manifest.digest(c) == manifest.digest(art)
            rep.add(OK if same else FAIL,
                    f"{c.name} " + ("is the current build" if same
                                    else "DIFFERS from the current build"),
                    "" if same else f"cp {art.relative_to(ROOT)} {c.relative_to(ROOT)}")


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
