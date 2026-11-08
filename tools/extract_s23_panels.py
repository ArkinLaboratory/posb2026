#!/usr/bin/env python3
"""Regenerate session 23's Rottinghaus panels from the PDF.

WHY THIS EXISTS. `decks/paper_figures.yaml` can declare a crop of a parent
image, which keeps a panel regenerable. That covers most panels here. It does
NOT cover Fig. 3a, whose legend is wider than its plot and runs underneath
panel b's label, so no single rectangle isolates it -- the plot and the legend
are cropped separately and stacked. A hand-made PNG for that would be exactly
the untracked artifact the manifest exists to avoid, so the recipe lives here.

The images are gitignored and must stay so: this repository is public and
CC BY, and the figures are copyrighted. Showing them in a lecture you deliver
is ordinary educational use; redistributing them under CC BY is not.

Run:  python tools/extract_s23_panels.py
"""
import pathlib
import subprocess
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "private" / "readings" / (
    "Session 23 - rottinghaus-2022-crispr-kill-switches.pdf")
OUT = ROOT / "private" / "paper-figures"
DPI = 300
SCALE = DPI // 150   # boxes below were measured on a 150 dpi render

# page -> (key of the whole figure, box on the rendered page)
PARENTS = {
    3:  ("rottinghaus2022_fig1", (245, 100, 1015, 995)),
    5:  ("rottinghaus2022_fig2", (125, 100, 1145, 1100)),
    7:  ("rottinghaus2022_fig3", (130, 100, 1110, 1430)),
    13: ("rottinghaus2022_fig6", (232, 98, 1020, 1115)),
}

# simple panels: key -> (parent key, box in PARENT coordinates)
PANELS = {
    "rottinghaus2022_fig1a": ("rottinghaus2022_fig1", (5, 0, 375, 292)),
    "rottinghaus2022_fig1d": ("rottinghaus2022_fig1", (271, 298, 437, 578)),
    "rottinghaus2022_fig1f": ("rottinghaus2022_fig1", (1, 592, 269, 895)),
    "rottinghaus2022_fig1g": ("rottinghaus2022_fig1", (271, 592, 439, 895)),
    # Widened 2 November. The old box cut the right-hand end of the x-axis
    # -- the "28" tick printed half a glyph -- and clipped the panel letter.
    # Panel e carries no y-axis label in the paper itself, so the slide's
    # foot line has to supply the quantity; do not go looking for one here.
    "rottinghaus2022_fig2e": ("rottinghaus2022_fig2", (262, 597, 490, 946)),
    "rottinghaus2022_fig2g": ("rottinghaus2022_fig2", (753, 600, 1015, 955)),
    # The SCHEMATIC half of panel c only -- the bar chart under it is a
    # different claim and session 23 never makes it. This is the only
    # picture of the architecture the redundancy segment argues about:
    # four genome-integrated Ptet-cas9 cassettes, three Ptet-gRNA
    # cassettes, tetR, and the infA complement.
    "rottinghaus2022_fig2c_map": ("rottinghaus2022_fig2",
                                  # 227, not 220: at 220 the "X4" under the
                                  # cas9 arrow -- the whole point of the
                                  # panel -- was cut in half.
                                  (683, 5, 1020, 227)),
    "rottinghaus2022_fig3c": ("rottinghaus2022_fig3", (655, 2, 945, 325)),
    "rottinghaus2022_fig6a": ("rottinghaus2022_fig6", (0, 0, 788, 574)),
    "rottinghaus2022_fig6c": ("rottinghaus2022_fig6", (8, 924, 683, 1017)),
}

# Fig. 3a only: plot and legend stacked, because panel b's label sits in the
# rectangle that would otherwise hold the right-hand legend column.
STACKED = {
    "rottinghaus2022_fig3a": ("rottinghaus2022_fig3",
                              (8, 20, 402, 221),     # plot
                              (20, 221, 437, 330)),  # legend
}


def _s(box):
    """Scale a box measured at 150 dpi to the render DPI."""
    return tuple(v * SCALE for v in box)


def main():
    if not PDF.exists():
        sys.exit(f"reading not found: {PDF}\n"
                 f"It is gitignored; restore it before running this.")
    OUT.mkdir(parents=True, exist_ok=True)
    pages = OUT / "_pages"
    pages.mkdir(exist_ok=True)

    for page, (key, box) in PARENTS.items():
        stem = pages / f"p{page}"
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI),
                        "-f", str(page), "-l", str(page), str(PDF), str(stem)],
                       check=True)
        rendered = next(pages.glob(f"p{page}-*.png"))
        Image.open(rendered).crop(_s(box)).save(OUT / f"{key}.png")
        print(f"  {key}.png   (page {page} at {DPI} dpi, {box})")

    for key, (parent_key, box) in PANELS.items():
        parent = Image.open(OUT / f"{parent_key}.png")
        parent.crop(_s(box)).save(OUT / f"{key}.png")
        print(f"  {key}.png   ({parent_key} {box})")

    for key, (parent_key, plot_box, leg_box) in STACKED.items():
        parent = Image.open(OUT / f"{parent_key}.png")
        plot, leg = parent.crop(_s(plot_box)), parent.crop(_s(leg_box))
        w = max(plot.width, leg.width)
        out = Image.new("RGB", (w, plot.height + leg.height), "white")
        out.paste(plot, (0, 0))
        out.paste(leg, (0, plot.height))
        out.save(OUT / f"{key}.png")
        print(f"  {key}.png   ({parent_key} plot {plot_box} + legend {leg_box})")

    for f in pages.glob("*.png"):
        f.rename(OUT / "_pages" / f.name)
    print(f"\n{len(PARENTS) + len(PANELS) + len(STACKED)} image(s) in "
          f"{OUT.relative_to(ROOT)}/ (gitignored)")


if __name__ == "__main__":
    main()
