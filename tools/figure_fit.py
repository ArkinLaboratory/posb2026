"""Legibility gate for the INSIDE of a matplotlib figure.

`tools/slide_fit.py` measures PowerPoint shapes against each other. It cannot
see inside a rendered PNG, so a deck can pass `--check` at zero fit problems
while carrying a figure whose legend is printed on top of the curve it is
explaining. Session 23 shipped exactly that: eleven slides with text colliding
with text or with plotted data, and twenty-one labels below the content floor,
all of it invisible to the existing gate.

This module checks the three things that gate cannot:

1.  TYPE FLOOR, AFTER PLACEMENT. Every piece of text inside a figure is
    content, so it must land on the slide at or above TYPE["body"]. The catch
    is "after placement": a figure whose tight bbox is taller than the band it
    is placed in gets scaled down, and 20 pt authored becomes 17 pt projected.
    So the check computes the placement scale and tests the product.

2.  TEXT ON TEXT. Two labels that merely touch read as one run of text. The
    gate uses a gap, not an intersection, for that reason.

3.  TEXT ON DATA. The expensive lesson. Making a label opaque so a curve
    cannot strike through it converts a legibility defect into an occlusion
    defect, and the occlusion defect is worse because it is silent -- the
    figure looks clean and the curve is simply gone. This check transforms
    every plotted point into display space and counts how many fall under
    each label box.

Run as a script for a report:   python tools/figure_fit.py s23_evolution
Imported by tools/build_figures.py, where failures are reported per figure.
"""
import importlib
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from figures.style import TYPE                                 # noqa: E402

FLOOR = TYPE["body"]
GAP = 10.0          # px: closer than this and two labels read as one
BAND_IN = 4.60      # image_centered's default band height
MAXW_IN = 10.2      # image_centered's default max width
COVER = 0.03        # fraction of a curve's points a label may sit on


def _label_box(artist, renderer):
    """The box that actually paints: the plate if there is one, else the ink.

    For an Annotation the ink is the TEXT, not the text plus its arrow -- see
    _text_box. An arrow pointing at a data point crosses that data by design.
    """
    patch = getattr(artist, "get_bbox_patch", lambda: None)()
    if patch is not None:
        return patch.get_window_extent(renderer)
    return _text_box(artist, renderer)


def _text_box(a, r):
    """The INK of a label, excluding an annotation's arrow.

    Annotation.get_window_extent() returns text plus arrow. An arrow that
    points at a data point necessarily crosses the curve it points at, so
    measuring the inflated box makes every annotated point a false
    "text sits on data" hit -- 105 px of phantom width on s22's 0.6193
    callout alone. Measure the text, and let the arrow do its job.
    """
    import matplotlib.text as _mtext
    if isinstance(a, _mtext.Annotation):
        try:
            return _mtext.Text.get_window_extent(a, r)
        except Exception:
            pass
    return a.get_window_extent(r)


def audit(fig, stem=None):
    """Return a list of problem strings for one drawn figure.

    `stem` is the PNG name it will be saved as; it is what lets the placement
    band be looked up from the deck that actually places it.
    """
    fig.tight_layout()
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    # theme.image_centered sizes the figure from its own aspect to FILL the
    # band, so a short wide figure is scaled UP and a tall one down. It does
    # not cap at natural size, so the scale is not min(..., 1.0) -- getting
    # that wrong is how a 16 pt legend was mistaken for a 16 pt projection
    # when it was really 18.5, and it is also how a genuinely shrunken
    # figure could be passed as fine.
    tb = fig.get_tightbbox(r)
    # savefig.bbox="tight" adds pad_inches on every side, so the PNG that is
    # actually placed is larger than the tight bbox. Measuring without the pad
    # makes the scale optimistic -- the direction that passes a figure whose
    # type lands under the floor.
    import matplotlib as _mpl
    _pad = (float(_mpl.rcParams.get("savefig.pad_inches", 0.1))
            if _mpl.rcParams.get("savefig.bbox", None) == "tight" else 0.0)
    _w, _h = tb.width + 2 * _pad, tb.height + 2 * _pad
    aspect = _w / _h
    global _PLACED
    if _PLACED is None:
        try:
            _PLACED = _placements()
        except Exception:
            _PLACED = {}
    # NO GUESSING. If no deck's placement of this figure could be read, the
    # scale is unknown and the type-floor check is skipped rather than run
    # against an assumed band. Silently falling back to image_centered's
    # defaults is what produced confident wrong verdicts for most of this
    # course: s16 and s17 place at NATURAL size (width = pixels/dpi, so scale
    # is exactly 1.000 by construction), and measuring them against a 4.60 in
    # band invented hundreds of type-floor violations that do not exist.
    # Collision checks are scale-invariant and still run.
    placed = _PLACED.get(stem)
    if placed is None:
        scale = None
    else:
        _maxw, _band = placed
        scale = min(_maxw, _band * aspect) / _w

    problems = []
    for ai, ax in enumerate(fig.axes):
        frame = (ax.xaxis.label, ax.yaxis.label, ax.title)
        boxes = []                      # (name, bbox) for things over the data
        sized = []                      # (name, pt) for the type floor
        legend = ax.get_legend()
        if legend is not None:
            boxes.append(("legend", legend.get_window_extent(r)))
            sized += [(t.get_text(), t.get_fontsize())
                      for t in legend.get_texts()]
        for a in list(ax.texts) + list(frame):
            s = a.get_text()
            if not s.strip():
                continue
            sized.append((s, a.get_fontsize()))
            if a not in frame:
                boxes.append((s.replace("\n", " | ")[:44], _label_box(a, r)))

        if scale is None and sized:
            problems.append(
                f"ax{ai}: placement unknown -- no deck call for {stem!r} could "
                f"be read, so the type floor was NOT checked here")
        for s, pt in (sized if scale is not None else []):
            if pt * scale < FLOOR - 0.5:
                problems.append(
                    f"ax{ai}: {pt * scale:.1f} pt on the slide (floor "
                    f"{FLOOR}) -- {s.replace(chr(10), ' | ')[:50]!r}")

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (na, a), (nb, b) = boxes[i], boxes[j]
                if (a.x0 < b.x1 + GAP and b.x0 < a.x1 + GAP
                        and a.y0 < b.y1 + GAP and b.y0 < a.y1 + GAP):
                    problems.append(f"ax{ai}: {na!r} touches {nb!r}")

        # 4. TEXT SPILLING ITS BOX. A schematic's labels sit inside drawn
        #    rectangles, and raising them to the floor is exactly what makes
        #    them outgrow the box. Checks 1-3 are all blind to it: the text
        #    collides with nothing, covers no plotted line, and is the right
        #    size. Session 22 shipped five labels overflowing their boxes by
        #    up to 77 px while this file reported the figure clean.
        from matplotlib.patches import Rectangle
        rects = [(p, p.get_window_extent()) for p in ax.patches
                 if isinstance(p, Rectangle)]
        for a in ax.texts:
            tb = _text_box(a, r)
            cx, cy = (tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2
            for _p, qb in rects:
                if not (qb.x0 < cx < qb.x1 and qb.y0 < cy < qb.y1):
                    continue            # label belongs to some other box
                spill = max(qb.x0 - tb.x0, 0) + max(tb.x1 - qb.x1, 0)
                if spill > 1:
                    problems.append(
                        f"ax{ai}: {a.get_text()[:34]!r} spills its box by "
                        f"{spill:.0f} px (text {tb.width:.0f}, box "
                        f"{qb.width:.0f})")

        inside = ax.get_window_extent()
        for name, bb in boxes:
            for line in ax.lines:
                # GUIDES ARE NOT DATA. This repo draws reference lines --
                # slope-one guides, set-point lines, gridline-style axhlines
                # -- at zorder 1 and its data at zorder 3 or above. A label
                # crossing a dashed grey guide is normal; crossing the curve
                # the figure is about is not. Without this the s23 stability
                # figure reports its own annotation sitting on an axhline
                # that is there to be written over.
                if line.get_zorder() is not None and line.get_zorder() <= 1:
                    continue
                ink, marks = _ink_px(ax, line, inside)
                npx = (((ink[:, 0] > bb.x0) & (ink[:, 0] < bb.x1)
                        & (ink[:, 1] > bb.y0) & (ink[:, 1] < bb.y1)).sum()
                       if len(ink) else 0)
                nmk = (((marks[:, 0] > bb.x0) & (marks[:, 0] < bb.x1)
                        & (marks[:, 1] > bb.y0) & (marks[:, 1] < bb.y1)).sum()
                       if len(marks) else 0)
                if npx > LINE_PX or nmk > 1:
                    problems.append(
                        f"ax{ai}: {name!r} sits on {npx:.0f} px of drawn line"
                        f" ({nmk} marker(s)) of {line.get_label()!r}")

        # A label striking a patch's edge FROM OUTSIDE it. The spill check
        # above only looks at labels a box contains; nothing looked at a label
        # that collides with a border it does not belong to.
        for a in ax.texts:
            if not a.get_text().strip():
                continue                        # an empty label draws nothing
            tb = _text_box(a, r)
            cx, cy = (tb.x0 + tb.x1) / 2, (tb.y0 + tb.y1) / 2
            for _p, qb in rects:
                if qb.x0 < cx < qb.x1 and qb.y0 < cy < qb.y1:
                    continue                    # the box owns this label
                ox = min(tb.x1, qb.x1) - max(tb.x0, qb.x0)
                oy = min(tb.y1, qb.y1) - max(tb.y0, qb.y0)
                if ox > 1 and oy > 1:
                    problems.append(
                        f"ax{ai}: {a.get_text()[:30]!r} overlaps a box edge "
                        f"it is not inside, by {ox:.0f}x{oy:.0f} px")
                    break
    # FIGURE-LEVEL TEXT. audit() walks fig.axes and each axes' own texts, so
    # anything attached to the FIGURE rather than to an axes -- suptitle,
    # fig.text() -- was invisible to every check, the type floor included.
    # s22, s07 and s14 all use one. Fourth blind spot of the same family as
    # the three in deck-bar D5a: the gate was silent, not clean.
    if scale is not None:
        for t in fig.texts:
            label = t.get_text()
            if not label.strip():
                continue
            if t.get_fontsize() * scale < FLOOR - 0.5:
                problems.append(
                    f"figure text: {t.get_fontsize() * scale:.1f} pt on the "
                    f"slide (floor {FLOOR}) -- {label[:46]!r}")

    return scale, problems


LINE_PX = 12        # px of drawn line a label may sit on before it is a problem


def _ink_px(ax, line, inside):
    """A line's RENDERED ink in display px, split into path and markers.

    The metric this replaces counted how many of a curve's DATA POINTS fell
    inside a label, and flagged at 3 per cent of them. That measures the
    author's sampling density, not ink: a line plotted with 18 markers running
    straight through a three-line annotation put 2 points in the box and
    cleared a threshold of "more than 2", while the same line drawn with 500
    points would have put 60 in. The instructor caught on the
    rendered slide what this file had passed. Sample the path itself, about one point per
    pixel, and the answer stops depending on how the author chose to plot.
    """
    xd, yd = line.get_data()
    xd, yd = np.asarray(xd, float), np.asarray(yd, float)
    if len(xd) < 1:
        return np.zeros((0, 2)), np.zeros((0, 2))
    # THE LINE'S OWN TRANSFORM, not transData. axhline and axvline use a
    # BLENDED transform -- one axis in data coordinates, the other in axes
    # fractions -- so an axhline's xdata is (0, 1) meaning "the full width",
    # not "from x=0 to x=1". Pushing that through transData put every
    # reference line at a position it is not drawn at, and then reported
    # labels as sitting on it.
    P = line.get_transform().transform(np.column_stack([xd, yd]))
    P = P[np.isfinite(P).all(axis=1)]
    clip = lambda A: A[(A[:, 0] >= inside.x0) & (A[:, 0] <= inside.x1)
                       & (A[:, 1] >= inside.y0) & (A[:, 1] <= inside.y1)]
    marks = (clip(P) if line.get_marker() not in (None, "None", "none", "")
             else np.zeros((0, 2)))
    if line.get_linestyle() in (None, "None", "none", " ", "") or len(P) < 2:
        return np.zeros((0, 2)), marks
    seg = np.diff(P, axis=0)
    out = []
    for i, dist in enumerate(np.hypot(seg[:, 0], seg[:, 1])):
        k = max(int(dist), 1)
        out.append(P[i] + np.linspace(0, 1, k, endpoint=False)[:, None] * seg[i])
    out.append(P[-1:])
    return clip(np.vstack(out)), marks


def _placements():
    """figure stem -> (max_w_in, band_in), read from the decks themselves.

    The band was hard-coded to image_centered's 10.2 x 4.60. Decks that place
    with d.image(..., w=W-2*M, h=5.05) -- s20 and s22 -- really get about
    11.93 x 5.05, so every figure in them was measured against a band 10 per
    cent shorter than the one it lands in. That under-reports the scale, and
    on s22 it invented 20 type-floor violations at 19.2 pt against a floor of
    20 for figures that actually project above it. Read the real call instead.
    """
    import ast, glob, os
    out = {}
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "..",
                                    "decks", "*.py")):
        try:
            tree = ast.parse(open(f).read())
        except Exception:
            continue
        helpers = {}                      # helper name -> band it places at
        _enclosing = {}
        # Calls that sit inside a for-loop whose header names PNGs literally.
        _loop_pngs = {}
        for loop in ast.walk(tree):
            if not isinstance(loop, ast.For):
                continue
            names = [os.path.basename(c.value)[:-4]
                     for c in ast.walk(loop.iter)
                     if isinstance(c, ast.Constant)
                     and isinstance(c.value, str) and c.value.endswith(".png")]
            if not names:
                continue
            for inner in ast.walk(loop):
                if isinstance(inner, ast.Call):
                    _loop_pngs.setdefault(id(inner), names)
        for fn_def in ast.walk(tree):
            if isinstance(fn_def, ast.FunctionDef):
                for inner in ast.walk(fn_def):
                    if isinstance(inner, ast.Call):
                        _enclosing.setdefault(id(inner), fn_def.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = getattr(node.func, "attr", None)
            if fn not in ("image", "image_centered"):
                continue
            stem = None
            for a in node.args:
                # FIG + "name.png", or a bare "…/name.png"
                if isinstance(a, ast.BinOp) and isinstance(a.right, ast.Constant) \
                        and isinstance(a.right.value, str) and a.right.value.endswith(".png"):
                    stem = os.path.basename(a.right.value)[:-4]
                elif isinstance(a, ast.Constant) and isinstance(a.value, str) \
                        and a.value.endswith(".png"):
                    stem = os.path.basename(a.value)[:-4]
            # No early exit on a missing stem: the call may be inside a
            # staged-run loop or a per-deck helper, and both are resolved
            # below from the band this call establishes.
            kw = {k.arg: k.value for k in node.keywords}

            # Most decks pass w and h POSITIONALLY -- d.image(s, path, x, y,
            # w, h) -- not as keywords. Reading only keywords found a real
            # placement for 25 of 249 figures and silently fell back to
            # image_centered's band for the other 224, which is the whole
            # course measured against a band most of it does not use.
            def num(v):
                """A literal, or a simple expression over the theme's own
                geometry constants: W - 2 * M and friends."""
                if v is None:
                    return None
                try:
                    return float(ast.literal_eval(v))
                except Exception:
                    pass
                try:
                    return float(eval(compile(ast.Expression(v), "<p>", "eval"),
                                      {"__builtins__": {}},
                                      {"W": 13.333, "H": 7.5, "M": 0.7}))
                except Exception:
                    return None

            if fn == "image_centered":
                band = (num(kw.get("max_w")) or MAXW_IN,
                        num(kw.get("band")) or BAND_IN)
            else:
                pos = node.args          # (s, path, x, y, w, h)
                w = num(kw.get("w")) or (num(pos[4]) if len(pos) > 4 else None)
                h = num(kw.get("h")) or (num(pos[5]) if len(pos) > 5 else None)
                band = (w, h) if (w and h) else None
            if band is None:
                continue
            if stem:
                out[stem] = band
            elif _loop_pngs.get(id(node)):
                # A staged run: for png, foot in (("x_1.png", ...), ...) with
                # d.image(s, FIG + png, ...). The names are constants in the
                # loop header even though the call sees only a variable.
                for key in _loop_pngs[id(node)]:
                    out.setdefault(key, band)
            else:
                # The placement is inside a per-deck helper -- _fig(d, s,
                # "name", top) and friends. Record the band against the
                # enclosing function so the helper's callers can be resolved
                # below; without this, every deck that wraps its placement
                # reads as "no placement found" and falls back to a band it
                # does not use.
                owner = _enclosing.get(id(node))
                if owner:
                    helpers[owner] = band

        if helpers:
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = getattr(node.func, "id", None) \
                    or getattr(node.func, "attr", None)
                if name not in helpers:
                    continue
                for a in node.args:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        key = os.path.basename(a.value)
                        key = key[:-4] if key.endswith(".png") else key
                        out.setdefault(key, helpers[name])
    return out


_PLACED = None


def audit_module(modname, write=False):
    """Audit every figure a session's figure module produces.

    Hooks Figure.savefig rather than a module's own _save helper: only some
    figure modules have one, and the ones that call savefig directly are
    exactly the ones nothing has ever checked.
    """
    from matplotlib.figure import Figure

    # Auditing runs the generators. A movie module writes its .mp4 through
    # ffmpeg rather than Figure.savefig, so running one here rewrites the
    # file and the build manifest then reports it as EDITED BY HAND. Movie
    # frames are played full-bleed anyway, so none of the placement
    # arithmetic below describes them. Refuse outright.
    if modname.endswith("_movie"):
        raise ValueError(f"{modname} is a movie module: auditing it would "
                         f"rewrite its .mp4, and frames are not placed in "
                         f"a slide band")

    mod = importlib.import_module(f"figures.{modname}")
    out = []
    real = Figure.savefig

    def hook(self, fname, *a, **kw):
        # Movie frames render to a BytesIO and are played full-bleed, not
        # placed in a slide band, so the placement arithmetic here does not
        # describe them. Only audit figures written to a real path.
        if not isinstance(fname, (str, bytes)) and not hasattr(fname, "name"):
            return real(self, fname, *a, **kw)
        name = str(fname).rsplit("/", 1)[-1].rsplit(".", 1)[0]
        out.append((name,) + audit(self, name))
        if write:
            real(self, fname, *a, **kw)

    figs = getattr(mod, "FIGURES", None)
    if figs is None:
        figs = [v for k, v in vars(mod).items()
                if k.startswith("fig_") and callable(v)]
    Figure.savefig = hook
    try:
        for fn in figs:
            fn()
    finally:
        Figure.savefig = real
    return out


if __name__ == "__main__":
    import sys

    mods = sys.argv[1:]
    if not mods:
        mods = sorted(p.stem for p in Path("figures").glob("*.py")
                      if p.stem not in ("style", "__init__"))
    worst = []
    for m in mods:
        try:
            res = audit_module(m)
        except Exception as exc:                       # a module that will not
            print(f"{m}: could not audit -- {exc}")    # import is not this
            continue                                   # tool's business
        n = sum(len(p) for _, _, p in res)
        scales = [s for _, s, _ in res if s is not None]
        unknown = sum(1 for _, s, _ in res if s is None)
        if n:
            worst.append((n, m))
        shown = (f"min placement scale {min(scales):.3f}" if scales
                 else "no placement readable")
        if unknown:
            shown += f"  ({unknown} unplaced)"
        print(f"{m:24s} {len(res):2d} figure(s)  {shown}  {n:3d} problem(s)")
        if "-v" in sys.argv:
            for name, scale, probs in res:
                for pr in probs:
                    print(f"    {name}: {pr}")
    print("\nworst first:", ", ".join(f"{m} ({n})" for n, m in
                                      sorted(worst, reverse=True)[:10]) or "none")
