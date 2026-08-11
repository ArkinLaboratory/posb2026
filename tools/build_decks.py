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
    unassigned = 0
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
        # The rule from readings.yaml, enforced where it actually gets broken:
        # a deck that ends without handing out the next session's paper.
        if deck.session is not None:
            due = deck.assigned_here()
            if due and not deck.assignment_rendered:
                unassigned += len(due)
                print(f"  !! session {deck.session} must assign "
                      f"{len(due)} paper(s) for session {deck.session + 1} "
                      f"({', '.join(r.get('key', '?') for r in due)}) "
                      f"but this deck never calls d.assignment()")
            elif due:
                print(f"  assigns {len(due)} reading(s) for "
                      f"session {deck.session + 1}")
            if deck.assignment_overflow:
                _, at, over = deck.assignment_overflow
                unassigned += 1
                print(f"  !! the assignment box was placed at y={at} but is "
                      f"{over}in too tall for the slide; it has been moved up "
                      f"and probably now overlaps. Reflow that slide.")
        if deck.loose_slots:
            print(f"  {len(deck.loose_slots)} slot(s) much larger than the "
                  f"figure -- the image shrinks and floats:")
            for key, fill, box, got in deck.loose_slots:
                print(f"    {key:<24} fills {fill:.0%} of {box[0]}x{box[1]}in "
                      f"-> renders {got[0]}x{got[1]}in")

    if strict and (missing_total or unassigned):
        sys.exit(f"\n--check: {missing_total} paper figure(s) missing, "
                 f"{unassigned} reading(s) never handed out")
    print(f"\nDone. Decks in {OUT.relative_to(ROOT)}/ (gitignored).")


if __name__ == "__main__":
    main()
