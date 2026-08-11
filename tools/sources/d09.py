"""Demo 9 — the toggle explorer. A classroom demo, not an assignment."""
from .common import md, code, header, SETUP

REL = "demos/d09-toggle-explorer/d09_toggle_explorer.ipynb"
TITLE = "Demo 9 — The Toggle Explorer"
SUBTITLE = "Turn the knobs in front of the room and watch bistability appear and vanish"
DATE = "for Session 9"

CELLS = [
    header(TITLE, SUBTITLE, DATE, REL),

    md("""This is a **classroom demo**. There is nothing to submit and nothing is
graded. It exists to be projected and driven live during lecture, and to be
played with afterwards.

It is deliberately short. One cell builds the model, one cell gives you sliders.

**In lecture, the sequence that works:** set *n* = 2 and raise α until the
second state appears — then set *n* = 1 and try to make it happen at any α at
all. The second half is the point."""),

    md("## Setup"),
    code(SETUP),

    md("""---
## The model

The Gardner–Cantor–Collins toggle, scaled so only three parameters remain:

$$\\frac{du}{dt} = \\frac{\\alpha_1}{1 + v^{\\,m}} - u
\\qquad
\\frac{dv}{dt} = \\frac{\\alpha_2}{1 + u^{\\,n}} - v$$

`posb.toggle_model` builds exactly this. Look at it before you use it —
`posb/analysis.py` is short."""),

    code('''from posb import toggle_model, stability_report, nullcline, toggle_alpha_critical

m = toggle_model(alpha1=3.0, alpha2=3.0, n=2)
print(m.summary())'''),

    code('''for f in stability_report(m, grid=(1e-3, 20, 9)):
    p = f["point"]
    print(f"u = {p['u']:6.3f}   v = {p['v']:6.3f}   {f['type']}")'''),

    md("""---
## The explorer

Drag the sliders. Filled circles are stable states; the open red circle is the
saddle.

Watch two things:

1. **What happens to the number of intersections as you raise α.**
2. **What happens when you drag *n* below 1** — and whether *any* α rescues it."""),

    code('''import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider


def explore(alpha1=3.0, alpha2=3.0, n=2.0):
    model = toggle_model(alpha1, alpha2, n=n)
    grid = np.linspace(0.001, 5.0, 300)

    u_of_v = nullcline(model, "u", "v", grid)
    v_of_u = nullcline(model, "v", "u", grid)

    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot(u_of_v, grid, lw=2.2, color="#0E4F57", label="du/dt = 0")
    ax.plot(grid, v_of_u, lw=2.2, color="#4FD1C5", label="dv/dt = 0")

    report = stability_report(model, grid=(1e-3, 30, 9))
    n_stable = 0
    for f in report:
        p, kind = f["point"], f["type"]
        if kind.startswith("stable"):
            ax.plot(p["u"], p["v"], "o", ms=10, color="#0B3A3F", zorder=5)
            n_stable += 1
        else:
            ax.plot(p["u"], p["v"], "o", ms=10, mfc="white",
                    mec="#B3261E", mew=2.2, zorder=5)

    ac = toggle_alpha_critical(n)
    note = ("bistable" if n_stable > 1 else "monostable")
    thr = ("no alpha can work" if np.isinf(ac) else f"alpha_c = {ac:.2f}")

    ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.set_aspect("equal")
    ax.set_xlabel("u"); ax.set_ylabel("v")
    ax.set_title(f"{n_stable} stable state(s) - {note}\\n{thr}", fontsize=12)
    ax.legend(loc="upper right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


interact(explore,
         alpha1=FloatSlider(value=3.0, min=0.5, max=12.0, step=0.1, description="alpha 1"),
         alpha2=FloatSlider(value=3.0, min=0.5, max=12.0, step=0.1, description="alpha 2"),
         n=FloatSlider(value=2.0, min=0.5, max=4.0, step=0.05, description="n"));'''),

    md("""---
## Two things to try in front of the room

**1. Break the symmetry.** Hold *n* = 2 and α₁ = 6, then walk α₂ down from 6.
The bistable window does not shrink gracefully — one state swallows the other
fairly abruptly. That is why a toggle drifts out of usefulness when growth rate
or burden unbalances the two arms.

**2. Find the boundary yourself.** Set *n* = 3 and lower α until the second
state disappears. Compare where it happened to `toggle_alpha_critical(3)`."""),

    code('''for n in (1.0, 1.5, 2.0, 3.0, 4.0):
    ac = toggle_alpha_critical(n)
    print(f"n = {n:<4}  alpha_c = {'no value works' if np.isinf(ac) else f'{ac:8.4f}'}")'''),

    md("""---
## Why this is the whole lecture in one widget

The parameter you most want to change is *n*, because it is the one that
decides whether bistability is possible at all — and it is the one you can
least control in a laboratory. Cooperativity is set by how a repressor
oligomerises and how its operators are arranged. You choose it by choosing a
protein, not by turning a knob.

Gardner and colleagues did not tune cooperativity. They **chose repressors that
already dimerise**.

**Next:** the derivation of that boundary is the worked example in Session 9,
and it takes about ten lines."""),
]
