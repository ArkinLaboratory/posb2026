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
    python tools/build_decks.py --verify  # build nothing; is what is on disk
                                          # older than the sources that made it?

The build also measures PACING: minutes of exposition per slide, per segment,
excluding the stretches where the students are working and the slide is static
on purpose. A segment where you talk for eight minutes with nothing on the
screen changing is invisible in the source and obvious in the ratio, and it is
the difference between a short lecture and an improvised one.

And every build now writes a sidecar recording exactly which files it read, so

    python tools/build_decks.py --verify

can answer the question nothing else here could: is the .pptx you are about to
teach from the one your current sources would produce? Run it before class. It
does not build anything -- see tools/manifest.py for why that is the point.
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import manifest                                  # noqa: E402

DECKS = ["s01_specification", "s02_substrate", "s03_modeling_i",
         "s04_modeling_ii", "s09_bistability"]
OUT = ROOT / "private" / "build" / "decks"

# Inputs every deck depends on regardless of what it happens to draw. The
# per-deck figures, movies and poster frames are not listed here: the Deck
# records those as it reads them (theme.Deck._used), because a hand-maintained
# list of what a slide embeds is exactly the kind of thing that goes out of
# date without anyone noticing -- which is the bug this whole file addresses.
COMMON = ["decks/theme.py", "course.yaml", "readings.yaml",
          "decks/paper_figures.yaml", "decks/paper_movies.yaml",
          "tools/schedule.py"]


def deps_for(name, deck):
    return [ROOT / f"decks/{name}.py"] + [ROOT / c for c in COMMON] + deck.assets


def verify():
    """Report on what is on disk. Builds nothing. Returns the number of
    artifacts that cannot be trusted."""
    print("Checking built decks against the sources on this machine.\n"
          "(No build is run. 'not built on this machine' is not a problem.)\n")
    bad = 0
    for name in DECKS:
        mod = importlib.import_module(f"decks.{name}")
        for suffix in (".pptx", ".pdf"):
            bad += manifest.report(mod.FILENAME + suffix,
                                   OUT / f"{mod.FILENAME}{suffix}")
    if bad:
        print(f"\n{bad} artifact(s) you should not teach from. Rebuild:\n"
              f"    python tools/build_decks.py --pdf")
    else:
        print("\nEverything present is current.")
    return bad


def to_pdf(pptx):
    """Convert a built deck to PDF with LibreOffice, if it is installed.

    Worth having for two reasons. A PDF is the thing to post to bCourses after
    class, and it is the only way to check what a deck actually looks like
    without opening PowerPoint -- which matters because these decks are
    generated, so "looks right" is a thing you verify rather than assume.
    """
    import shutil
    import subprocess
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sys.exit("--pdf needs LibreOffice. On macOS: brew install --cask libreoffice")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                    "--outdir", str(pptx.parent), str(pptx)],
                   check=True, capture_output=True)
    return pptx.with_suffix(".pdf")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--check" in sys.argv
    want_pdf = "--pdf" in sys.argv

    if "--verify" in sys.argv:
        sys.exit(1 if verify() else 0)

    names = [d for d in DECKS if not args or any(a in d for a in args)]
    if not names:
        sys.exit(f"no deck matches {args}. available: {DECKS}")

    missing_total = 0
    unassigned = 0
    thin_total = 0
    for name in names:
        mod = importlib.import_module(f"decks.{name}")
        deck = mod.build()
        path = deck.save(OUT / f"{mod.FILENAME}.pptx")
        n_slides = len(deck.prs.slides)
        print(f"\n{name}  ->  {path.relative_to(ROOT)}  ({n_slides} slides)")
        deps = deps_for(name, deck)
        manifest.write(path, deps, extra={"deck": name, "slides": n_slides})
        if want_pdf:
            pdf = to_pdf(path)
            manifest.write(pdf, deps, extra={"deck": name, "from": path.name})
            print(f"  also  {pdf.name}")
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
        if deck.segments:
            rows, sm = deck.pacing()
            board = (f";  {sm['board_min']} min at the board"
                     if sm.get("board_min") else "")
            print(f"  pacing: {sm['exposition_min']} min exposition over "
                  f"{sm['exposition_slides']} slides = "
                  f"{sm['min_per_slide']:.1f} min/slide;  "
                  f"{sm['activity_min']} min students working "
                  f"({sm['activity_frac']:.0%}){board}")
            if sm["thin"]:
                thin_total += len(sm["thin"])
                print(f"  !! {len(sm['thin'])} segment(s) with too few slides "
                      f"for the time -- you would be improvising:")
                for r in sm["thin"]:
                    print(f"     {r['badge']:<12} {r['slides']} slide(s) for "
                          f"{r['minutes']} min  ({r['per_slide']:.1f} "
                          f"min/slide)  {r['label'][:38]}")
        if deck.missing_movies:
            missing_total += len(deck.missing_movies)
            print(f"  {len(deck.missing_movies)} movie(s) shown as slots:")
            for key, ref in deck.missing_movies:
                print(f"    {key:<26} {ref}")
            print(f"  -> save these as private/paper-movies/<key>.mp4")
        if deck.unattributed_figures:
            print(f"  !! {len(deck.unattributed_figures)} figure(s) marked "
                  f"ATTRIBUTION NEEDED on the slide:")
            for n in deck.unattributed_figures:
                print(f"     {n}")
        if deck.loose_slots:
            print(f"  {len(deck.loose_slots)} slot(s) much larger than the "
                  f"figure -- the image shrinks and floats:")
            for key, fill, box, got in deck.loose_slots:
                print(f"    {key:<24} fills {fill:.0%} of {box[0]}x{box[1]}in "
                      f"-> renders {got[0]}x{got[1]}in")

    if strict and (missing_total or unassigned or thin_total):
        sys.exit(f"\n--check: {missing_total} paper figure(s) missing, "
                 f"{unassigned} reading(s) never handed out, "
                 f"{thin_total} under-slided segment(s)")
    print(f"\nDone. Decks in {OUT.relative_to(ROOT)}/ (gitignored).")


if __name__ == "__main__":
    main()
