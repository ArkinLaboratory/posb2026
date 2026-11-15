"""Score a DO-NOTHING submission against a problem set's generated tests.

WHY THIS EXISTS
---------------
A test that passes without the student doing the work grades nothing, and
nothing in the build said so. PS7 shipped with 19 of 23 autograded points
harvestable by transcription; ps08-PLAN.md section "what PS7 got wrong"
predicted the same shape for PS8 and was right -- the first measurement came
back 21 of 39. Both were found by a human reading test files one at a time,
which is not a process that holds.

So the claim "these points cannot be harvested" is now checked every build,
for every set, the way the missing-background guard and the unbraced-subscript
check are.

HOW
---
`private/sources/psNN_stub.py` holds the answers a student could produce from
the question text, a slide, or the degenerate empty value -- having run
nothing. It is deliberately a file in the repo rather than something inferred:
the stub IS the claim about what is free, and it should be arguable in review.

A set with no stub file is reported, not silently passed.
"""
import contextlib
import io
import pathlib
import sys
import zipfile

# The repository root, so a stub can import `posb` the way a student's notebook
# does. Added 15 November 2026: PS9's stub was the first to import the course
# library -- it evaluates the stem's own printed equations, which is what a
# student harvesting a point actually does -- and `score()` exec's the stub in
# a bare namespace under whatever sys.path the caller happened to have. Run as
# `python3 tools/build_problem_sets.py`, sys.path[0] is tools/, so the import
# raised ModuleNotFoundError and took the whole build down after the bundle had
# already been written.
ROOT = pathlib.Path(__file__).resolve().parent.parent


def _test_sources(bundle):
    """Yield (name, source) for every generated test.

    Otter leaves the tests only inside the Gradescope zip, so that is what is
    read -- and reading the shipped artefact rather than a copy is the point:
    this measures what Gradescope will actually run.
    """
    with zipfile.ZipFile(bundle) as z:
        for n in sorted(z.namelist()):
            if n.startswith("tests/") and n.endswith(".py"):
                yield n, z.read(n).decode("utf-8")


def score(bundle, stub_path):
    """Return (earned, total, rows) for the stub against every generated case."""
    ns = {}
    _added = str(ROOT) not in sys.path
    if _added:
        sys.path.insert(0, str(ROOT))
    try:
        exec(compile(pathlib.Path(stub_path).read_text(), str(stub_path),
                     "exec"), ns)
    finally:
        if _added:
            sys.path.remove(str(ROOT))
    total = earned = 0
    rows = []
    for tname, src in _test_sources(bundle):
        mod = {}
        exec(compile(src, tname, "exec"), mod)
        t = mod["test"]
        for suite in t["suites"]:
            for case in suite["cases"]:
                pts = case.get("points", 0) or 0
                total += pts
                code = "\n".join(
                    l[4:] if l.startswith((">>> ", "... ")) else l
                    for l in case["code"].splitlines())
                local = dict(ns)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(compile(code, "<case>", "exec"), local)
                    ok = True
                except Exception:
                    ok = False
                if ok:
                    earned += pts
                    # A 0-point case grades nothing BY DESIGN -- it is a
                    # diagnostic, and ps-bar section K says to set one to 0
                    # precisely when it sits on transcription. Listing it as a
                    # leak would train the reader to ignore this report.
                    if pts:
                        rows.append((t["name"],
                                     "hidden" if case.get("hidden") else
                                     "VISIBLE", pts))
    return earned, total, rows


def report(name, bundle, stub_path, cap=0.10):
    """Print the harvestable figure. Returns True if it is within `cap`."""
    stub_path = pathlib.Path(stub_path)
    if not stub_path.exists():
        print(f"  !! no do-nothing stub at {stub_path} -- nothing checks that "
              f"{name}'s autograded points require any work. Write one.")
        return False
    earned, total, rows = score(bundle, stub_path)
    frac = earned / total if total else 0.0
    if not rows:
        print(f"  do-nothing stub earns 0 of {total} autograded points")
        return True
    if frac <= cap:
        print(f"  do-nothing stub earns {earned} of {total} autograded points "
              f"({frac:.0%}, within the {cap:.0%} cap) -- from:")
        for n, kind, pts in rows:
            print(f"     {n:<6} {kind:<8} {pts} pt(s)")
        return True
    print(f"  !! a DO-NOTHING submission earns {earned} of {total} autograded "
          f"points ({frac:.0%}) -- these tests grade nothing:")
    for n, kind, pts in rows:
        print(f"     {n:<6} {kind:<8} {pts} pt(s)")
    return frac <= cap
