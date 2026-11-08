#!/usr/bin/env python3
"""Digitize Rottinghaus Fig. 2e and fit the session-23 model to it.

WHY. The session's segment 4 originally claimed the mutation-selection model
was refuted by the paper's 28-day stability data. That claim rested on a
misread: 1e-8.6 is Fig. 1h (the optimized 2-gRNA switch, with antibiotics,
one timepoint), NOT the 28-day stability measurement. Fig. 2e is a DIFFERENT
STRAIN (CRISPRks) and it does not sit at a floor -- it rises from below
detection to about 1e-6.3 over 224 generations.

Digitized here by locating the red diamond markers in the extracted panel and
calibrating against the y-axis tick labels, so the numbers below are
reproducible rather than eyeballed off a slide.

Run:  python tools/extract_s23_panels.py && python tools/fit_s23_fig2e.py
"""
import pathlib
import sys

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from posb.evolution import broken_fraction          # noqa: E402

PANEL = ROOT / "private" / "paper-figures" / "rottinghaus2022_fig2e.png"
GEN_PER_DAY = np.log2(250)
FLOOR = -7.9          # below this the panel is reporting "no colonies"


def digitize():
    im = Image.open(PANEL).convert("RGB")
    a = np.array(im)
    r, g, b = (a[:, :, i].astype(int) for i in range(3))
    red = (r > 90) & (r < 190) & (g < 70) & (b < 70)
    ys, xs = np.where(red)
    order = np.argsort(xs)
    xs, ys = xs[order], ys[order]
    groups, cur = [], [0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 8:
            groups.append(cur)
            cur = []
        cur.append(i)
    groups.append(cur)
    marks = [(xs[c].mean(), ys[c].mean()) for c in groups if len(c) > 40]

    grey = np.array(im.convert("L")) < 100
    axis_x = int(np.argmax(grey.sum(axis=0)[:120]))
    strip = grey[:, max(0, axis_x - 72):axis_x - 6]
    rows = np.where(strip.any(axis=1))[0]
    gps, cur = [], [rows[0]]
    for rr in rows[1:]:
        if rr - cur[-1] > 4:
            gps.append(cur)
            cur = []
        cur.append(rr)
    gps.append(cur)
    cents = [float(np.mean(gp)) for gp in gps if len(gp) > 4]
    # the first cluster is the panel letter, not a tick; ticks are 0 .. <-8
    ticks = cents[1:10]
    y0, y8 = ticks[0], ticks[8]
    x0, x28 = marks[0][0], marks[-1][0]

    # The assay days are 1, 4, 7, 10, 14, 17, 21, 24, 28 -- Methods p.14
    # ("On day 1, single colonies were transferred...", then every 3-4 days).
    # An earlier version anchored the first marker at day 0 and linearly
    # interpolated to day 28, which put every point about a day late and
    # mis-set the origin. The markers are on known days; read them off.
    DAYS = [1, 4, 7, 10, 14, 17, 21, 24, 28]
    if len(marks) != len(DAYS):
        raise SystemExit(f"found {len(marks)} markers, expected {len(DAYS)}")
    out = []
    for (cx, cy), day in zip(marks, DAYS):
        lv = (cy - y0) * (-8.0) / (y8 - y0)
        out.append((float(day), day * GEN_PER_DAY, lv))
    return out


def main():
    series = digitize()
    print("Fig. 2e digitized (CRISPRks, 250x daily passage, LB, no antibiotics):")
    for day, gen, lv in series:
        tag = "   below detection" if lv < FLOOR else ""
        print(f"   day {day:5.1f}  {gen:6.1f} gen   log10 fraction viable {lv:6.2f}{tag}")

    pts = [(gen, lv) for _, gen, lv in series if lv >= FLOOR]
    t = np.array([p[0] for p in pts])
    y = np.array([p[1] for p in pts])
    print(f"\nfitting dq/dt = (1-q)(sq + mu) to the {len(pts)} detectable points:")
    print(f"   {'s':>8}  {'best mu':>11}  {'RMS (decades)':>14}")
    for s in (0.0, 0.005, 0.01, 0.02, 0.05, 0.10):
        best = None
        for mu in np.logspace(-16, -4, 800):
            pred = np.log10(np.maximum(broken_fraction(t, s, mu), 1e-300))
            sse = float(((pred - y) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, mu)
        print(f"   {s:>8g}  {best[1]:>11.2e}  {np.sqrt(best[0] / len(t)):>14.3f}")
    # A flat line is the null the fit has to beat, and it nearly does not.
    flat = float(np.sqrt(((y - y.mean()) ** 2).mean()))
    slope = float(np.polyfit(np.log10(t), y, 1)[0])
    print(f"\n   flat (no rise at all)      RMS = {flat:.3f}")
    print(f"   measured log-log slope of the data = {slope:.2f}")
    print("\nThe one-hit fit beats a flat line only narrowly, and the data's own")
    print("slope is below 1 while every model in this family predicts >= 1. So")
    print("this is an UPPER BOUND on the burden, not a measurement of it: what")
    print("the curve genuinely excludes is s >~ 0.02, which misses by 3x the RMS.")


if __name__ == "__main__":
    main()
