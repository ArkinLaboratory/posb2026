#!/usr/bin/env python3
"""Generate every course figure from posb.

Figures are committed so decks and READMEs can embed them without running
anything -- but they are BUILD ARTIFACTS. Edit the script, not the PNG.

("Committed" was aspirational until it was checked: a bare `build/` in
.gitignore matched figures/build/ as well as the repository root, so none of
these were tracked and every figure link in the session READMEs was broken on
GitHub. The rule is now /build/.)

The point of generating them rather than drawing them: the plot on the lecture
slide is produced by the same functions students call in the notebook, so a
figure can never drift from the code it claims to illustrate.

The figures are committed, which creates the other half of the same problem the
decks have: a generator can be edited and the PNG beside it left alone, and the
stale PNG is what everything downstream embeds. So each build records which
generator produced which file, and

    python tools/build_figures.py --verify

says whether any committed figure is older than the code that claims to make
it. Unlike the deck check this one is meaningful in CI, because figures/build/
is tracked -- so "you edited the plotting code and forgot to rebuild" fails the
pull request instead of reaching a lecture.

Usage:
    python tools/build_figures.py          # all
    python tools/build_figures.py s09      # one session
    python tools/build_figures.py --verify # build nothing; is any committed
                                           # figure older than its generator?
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import manifest                                  # noqa: E402

BUILD = ROOT / "figures" / "build"
# figures/style.py is a dependency of every figure: change a colour there and
# every PNG in the repository is out of date, which is exactly the kind of
# wide, quiet staleness nobody checks by eye.
COMMON = ["figures/style.py"]

MODULES = ["figures.s01_specification", "figures.s02_substrate",
           "figures.s03_modeling_i", "figures.s04_modeling_ii",
           "figures.s09_bistability"]

# Slow to render (video encoding), so not built unless asked for by name.
SLOW = ["figures.s02_movie"]


def verify():
    """Is any committed figure older than the code that generates it?

    Builds nothing. Returns the number of figures that cannot be trusted.
    """
    print("Checking committed figures against their generators.\n")
    bad = 0
    for f in sorted(BUILD.iterdir()):
        if f.suffix == manifest.SUFFIX or f.name.endswith(".deps.json"):
            continue
        if f.is_file():
            bad += manifest.report(f.name, f)
    if bad:
        print(f"\n{bad} figure(s) do not match their source. Rebuild:\n"
              f"    python tools/build_figures.py")
    else:
        print("\nEvery committed figure matches the code that made it.")
    return bad


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    if "--verify" in sys.argv:
        sys.exit(1 if verify() else 0)

    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    mods = [m for m in MODULES if not want or any(w in m for w in want)]
    mods += [m for m in SLOW if want and any(w in m for w in want)]
    if not mods:
        sys.exit(f"no figure module matches {want}. "
                 f"available: {MODULES}, and (by name only) {SLOW}")

    total = 0
    for name in mods:
        mod = importlib.import_module(name)
        src = [ROOT / (name.replace(".", "/") + ".py")] + [ROOT / c for c in COMMON]
        print(f"\n{name}")
        for fn in mod.FIGURES:
            # Which files did this function write? Rather than ask it to
            # declare them -- a list that would drift -- watch the directory.
            before = {f: f.stat().st_mtime_ns for f in BUILD.iterdir()
                      if f.is_file()}
            fn()
            written = [f for f in BUILD.iterdir()
                       if f.is_file() and f.suffix != ".json"
                       and before.get(f) != f.stat().st_mtime_ns]
            for f in written:
                manifest.write(f, src, extra={"generator": f"{name}.{fn.__name__}"})
            print(f"  {fn.__name__:<20} {fn.__doc__.splitlines()[0]}"
                  f"   [{', '.join(f.name for f in sorted(written))}]")
            total += 1
    print(f"\n{total} figure(s) written to figures/build/")


if __name__ == "__main__":
    main()
