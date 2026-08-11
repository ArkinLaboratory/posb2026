#!/usr/bin/env python3
"""Build lecture decks.

ONE SOURCE, TWO OUTPUTS. Deck sources live in decks/ and are public. Figures
from published papers are looked up in private/paper-figures/ at build time:

    present -> embedded            (your classroom deck)
    absent  -> a labelled slot     (what CI builds, what a fork sees)

There is never a public deck and a private deck to keep in sync, and nothing is
ever edited by hand before class. Run the build; you get the right deck for
whatever is on the machine.

Output goes to private/build/decks/, which is gitignored -- an assembled deck
may contain copyrighted figures and must not be committed.

Usage:
    python tools/build_decks.py           # all decks
    python tools/build_decks.py s09       # one
    python tools/build_decks.py --check   # fail if any paper figure is missing
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DECKS = ["s09_bistability"]
OUT = ROOT / "private" / "build" / "decks"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--check" in sys.argv

    names = [d for d in DECKS if not args or any(a in d for a in args)]
    if not names:
        sys.exit(f"no deck matches {args}. available: {DECKS}")

    missing_total = 0
    for name in names:
        mod = importlib.import_module(f"decks.{name}")
        deck = mod.build()
        path = deck.save(OUT / f"{mod.FILENAME}.pptx")
        n_slides = len(deck.prs.slides)
        print(f"\n{name}  ->  {path.relative_to(ROOT)}  ({n_slides} slides)")
        if deck.missing_figures:
            missing_total += len(deck.missing_figures)
            print(f"  {len(deck.missing_figures)} paper figure(s) shown as slots:")
            for key, ref in deck.missing_figures:
                print(f"    {key:<24} {ref}")
            print(f"  -> save these as private/paper-figures/<key>.png "
                  f"to embed them")
        else:
            print("  all paper figures embedded")

    if strict and missing_total:
        sys.exit(f"\n--check: {missing_total} paper figure(s) missing")
    print(f"\nDone. Decks in {OUT.relative_to(ROOT)}/ (gitignored).")


if __name__ == "__main__":
    main()
