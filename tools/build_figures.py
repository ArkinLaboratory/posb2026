#!/usr/bin/env python3
"""Generate every course figure from posb.

Figures are committed so decks and READMEs can embed them without running
anything -- but they are BUILD ARTIFACTS. Edit the script, not the PNG.

The point of generating them rather than drawing them: the plot on the lecture
slide is produced by the same functions students call in the notebook, so a
figure can never drift from the code it claims to illustrate.

Usage:
    python tools/build_figures.py          # all
    python tools/build_figures.py s09      # one session
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MODULES = ["figures.s01_specification", "figures.s09_bistability"]


def main():
    (ROOT / "figures" / "build").mkdir(parents=True, exist_ok=True)
    want = sys.argv[1:]
    mods = [m for m in MODULES if not want or any(w in m for w in want)]
    if not mods:
        sys.exit(f"no figure module matches {want}. available: {MODULES}")

    total = 0
    for name in mods:
        mod = importlib.import_module(name)
        print(f"\n{name}")
        for fn in mod.FIGURES:
            fn()
            print(f"  {fn.__name__:<20} {fn.__doc__.splitlines()[0]}")
            total += 1
    print(f"\n{total} figure(s) written to figures/build/")


if __name__ == "__main__":
    main()
