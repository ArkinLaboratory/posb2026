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
         "s04_modeling_ii", "s05_expression", "s08_phase_plane",
         "s09_bistability"]
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
    long_total = 0
    glyph_total = 0
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
            # min/slide EXCLUDES intermediate step slides, so a session with
            # more derivation runs shows a worse rate by construction and the
            # number reads like trouble when it is not. Session 8 was reported
            # at 8.0 min/slide and read as over-dense; its four runs are at
            # 1.6-2.5 min/step, inside session 5's own range. For a deck with
            # step runs, min/step is the metric that governs and it now prints
            # beside the other one instead of only when it fails.
            runs = [r for r in rows if r.get("steps")]
            if runs:
                worst = max(runs, key=lambda r: r["per_step"])
                print(f"          {len(runs)} derivation run(s), "
                      f"{min(r['per_step'] for r in runs):.1f}"
                      f"-{worst['per_step']:.1f} min/step "
                      f"(cap {sm['max_min_per_step']:.1f}) "
                      f"-- this, not min/slide, is the rate a run is judged on")
            # theme.py computes this; nothing printed it, so the ceiling was
            # a rule the build knew about and never mentioned. `.get` because
            # the field arrived in a parallel session and an older theme.py
            # would otherwise KeyError every deck build.
            # A glyph Calibri does not carry draws as an empty box in
            # PowerPoint and as nothing at all through LibreOffice's PDF
            # export. Session 4 shipped with every K_M, E_tot and V_max
            # invisible on the projector and the build said it was fine.
            bad = sm.get("bad_glyphs") or []
            if bad:
                glyph_total += len(bad)
                seen = {}
                for ch, fix, ctx in bad:
                    seen.setdefault((ch, fix), ctx)
                print(f"  !! {len(bad)} character(s) with no glyph in "
                      f"Calibri/Cambria -- these render as blanks:")
                for (ch, fix), ctx in seen.items():
                    print(f"     U+{ord(ch):04X}  use {fix:<8} in: {ctx}")

            sparse = sm.get("sparse") or []
            if sparse:
                cap = sm.get("max_min_per_step", "?")
                print(f"  !! {len(sparse)} derivation run(s) with too few steps "
                      f"for the time -- past {cap} min on one step the reveal "
                      f"has stopped pacing anything:")
                for r in sparse:
                    print(f"     {r['badge']:<12} {r['minutes']} min over "
                          f"{r['steps']} step(s) = {r['per_step']:.1f} min/step "
                          f" {r['label'][:34]}")

            long_blocks = sm.get("long") or []
            if long_blocks:
                long_total += len(long_blocks)
                cap = sm.get("max_activity", "?")
                print(f"  !! {len(long_blocks)} block(s) of student work longer "
                      f"than {cap} min -- past that the fast half has finished "
                      f"and the slow half has stalled:")
                for r in long_blocks:
                    print(f"     {r['badge']:<12} {r['minutes']} min  "
                          f"{r['label'][:44]}")
                print(f"     -> split it and put the answers in between; "
                      f"anything that will not fit belongs on the problem set")
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
        # Behind --audit, not --check. Across the seven built decks this flags
        # 25 segments and 24 of them are correctly classified: "Built one line
        # at a time", "The answers", a figure walk-through -- all genuinely me
        # talking. Printing it every build would be noise, and a check that
        # cries wolf is a check nobody reads. But the ONE it caught was real,
        # and it had already changed a design decision, so the audit stays
        # available and should be run whenever a session's headers change.
        if "--audit" in sys.argv and getattr(deck, "unclassified", None):
            print(f"  !! {len(deck.unclassified)} segment(s) whose header matches "
                  f"neither the student-activity nor the board word list, so the "
                  f"minutes were counted as ME TALKING:")
            for badge, label, mins in deck.unclassified:
                print(f"     {badge:<14} {mins:>3} min   {label}")
            print("     -> if the room is working, add a word from "
                  "Deck.ACTIVITY_WORDS to the header. The pacing percentage "
                  "above is wrong until this list is empty.")
        if deck.loose_slots:
            print(f"  {len(deck.loose_slots)} slot(s) much larger than the "
                  f"figure -- the image shrinks and floats:")
            for key, fill, box, got in deck.loose_slots:
                print(f"    {key:<24} fills {fill:.0%} of {box[0]}x{box[1]}in "
                      f"-> renders {got[0]}x{got[1]}in")

    # NOTE: long_total is reported above but deliberately NOT part of the
    # strict exit yet. Session 2's handout set is labelled as one twenty-four
    # minute block -- the two-block plan lives in its speaker notes, not in its
    # segment headers -- so making this fail --check would fail CI on a known,
    # dated deferral rather than on a surprise. Relabel s02 after 1 September
    # and then add `or long_total` here, which is the point of counting it.
    if strict and (missing_total or unassigned or thin_total or glyph_total):
        sys.exit(f"\n--check: {missing_total} paper figure(s) missing, "
                 f"{unassigned} reading(s) never handed out, "
                 f"{thin_total} under-slided segment(s), "
                 f"{glyph_total} missing glyph(s)"
                 + (f"  [and {long_total} over-long student block(s), "
                    f"not yet strict]" if long_total else ""))
    print(f"\nDone. Decks in {OUT.relative_to(ROOT)}/ (gitignored).")


if __name__ == "__main__":
    main()
