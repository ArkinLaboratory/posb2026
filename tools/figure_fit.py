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

ROOT = Path(__file__).resolve().parent.parent

# Stems placed at more than one band, filled in by `_placements`. A figure
# shared between decks is measured against the TIGHTEST of its bands; this
# records the disagreement so it can be reported rather than silently
# resolved. See the note at the assignment site.
MULTI_BAND = {}


def _dpi():
    """The dpi savefig will actually write at.

    `rcParams["savefig.dpi"]` defaults to the STRING "figure", meaning "use the
    figure's own dpi". `float()` on it raises, and the two places in this file
    that need a dpi had wrapped that in a try/except -- so the exception was
    swallowed and the check silently measured nothing while reporting clean.
    That is the §5.7 failure this file exists to catch, committed here.
    """
    import matplotlib as _mpl
    for key in ("savefig.dpi", "figure.dpi"):
        v = _mpl.rcParams.get(key, None)
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return 100.0

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
    # MEASURE THE PNG ON DISK. Reconstructing the placed size from the figure
    # object has been wrong in both directions and neither error is visible in
    # the output:
    #
    #   * savefig.bbox="tight" adds pad_inches per side, so measuring the bare
    #     tight bbox is OPTIMISTIC -- it passes a figure whose type lands under
    #     the floor.
    #   * adding rcParams' pad back is wrong whenever a generator passes its own
    #     pad_inches. `_save(..., fixed=True)` in the session-25 module writes
    #     with pad_inches=0, so this function was crediting those panels with
    #     0.2 in they do not have: about 4% PESSIMISTIC, which invents
    #     type-floor violations and sends a builder padding figures that were
    #     already correct.
    #   * get_tightbbox is taken after this function's own tight_layout() call,
    #     which is a SECOND pass for a generator that already ran one -- and
    #     tight_layout is not idempotent on an aspect-equal axes, so the
    #     geometry measured was never the geometry saved.
    #
    # The file that the deck embeds is the only thing that settles it. Fall back
    # to the reconstruction only when the PNG is not on disk yet.
    import matplotlib as _mpl
    _png = (ROOT / "figures" / "build" / f"{stem}.png") if stem else None
    _w = _h = None
    if _png is not None and _png.exists():
        try:
            from PIL import Image
            with Image.open(_png) as _im:
                _px_w, _px_h = _im.size
            _d = _dpi()
            if _d and _px_w and _px_h:
                _w, _h = _px_w / _d, _px_h / _d
        except Exception:
            _w = _h = None
    if _w is None:
        tb = fig.get_tightbbox(r)
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
            boxes.append(("legend", legend.get_window_extent(r), "content"))
            sized += [(t.get_text(), t.get_fontsize())
                      for t in legend.get_texts()]
        # THE AXES TITLE IS A COLLISION TARGET, not just frame.
        # `frame` was excluded from `boxes` wholesale, so a label that grew
        # UPWARD into the axes title was invisible here. That is not
        # hypothetical: on 8 November an agent added "(digitized)" to a tag on
        # s25_design_space, the tag grew into the panel's own title, and
        # "above our band past 0.35" printed through "oscillatory" on the
        # rendered page with this gate reporting clean. It was found by
        # rendering the deck, which is the thing the gate exists to save.
        # deck-bar D5d item 2, one level down.
        #
        # THE AXIS LABELS AND THE TICK LABELS ARE TARGETS TOO, as of
        # 9 November. The note that stood here said they were a known
        # remaining gap; two independent agents then walked into it on the
        # same day. One moved a legend outside the axes to dodge a collision
        # and it **printed straight through the x-label**, with this gate
        # reporting zero -- found only by reading the PNG at page size. The
        # other hit a title sitting on a y-tick (deck-bar D5d item 1).
        #
        # Both were invisible for the same reason: `frame` was excluded from
        # `boxes` wholesale and tick labels were never in it at all, so the
        # standard remedy for a crowded panel -- move the text to the edge --
        # relocated it into the one region nothing checked.
        #
        # On the rotation worry that kept the y-label out: `get_window_extent`
        # returns the axis-aligned box of the ROTATED text, which is larger
        # than the ink, so including it is conservative rather than wrong. A
        # false positive here costs a look; a false negative ships.
        collidable = tuple(frame)
        for a in list(ax.texts) + list(frame):
            s = a.get_text()
            if not s.strip():
                continue
            sized.append((s, a.get_fontsize()))
            if a not in frame or a in collidable:
                kind = ("title" if a is ax.title
                        else "frame" if a in frame else "content")
                boxes.append((s.replace("\n", " | ")[:44],
                              _label_box(a, r), kind))
        # Tick labels: only the ones MATPLOTLIB ACTUALLY DRAWS, and
        # `get_visible()` is not that predicate. This block used it and was
        # wrong in two independent ways, both measured 9 November within
        # hours of the block being written:
        #
        # 1. A locator emits ticks beyond the view limits. matplotlib builds
        #    real `Text` artists for them, with real bounding boxes, and
        #    filters them out at DRAW time in `Axis._update_ticks()` without
        #    ever touching `visible`. Verified: with ylim (-0.52, 0.10) the
        #    tick at loc -0.60 reports `get_visible() == True`.
        # 2. `ax.axis("off")` sets `ax.axison = False`, which short-circuits
        #    drawing and clears no artist's flag at all. Verified: every tick
        #    label on such an axes still reports `get_visible() == True`.
        #
        # The cost was not theoretical. Seven of the eleven findings this
        # block produced on its first run were phantoms, and the four
        # largest -- reported as 32 to 79 px of overlap -- were ticks that
        # paint ZERO pixels. An agent proved it by rendering each figure
        # twice, once with the tick's visibility forced off, and diffing:
        # phantoms changed 0 pixels, real ticks changed 265 to 3872. Chasing
        # them would have meant cutting NUMBERS.md 20.3's sourced wording
        # out of a panel title to clear a collision with a label that does
        # not exist -- deck-bar D5b, designing to the metric, caused by the
        # metric being wrong.
        #
        # `_update_ticks()` is matplotlib's own draw-time predicate and is
        # exact, but private; view-interval plus `axison` reproduces it for
        # every case in this repo.
        for which, axis in (("x", ax.xaxis), ("y", ax.yaxis)):
            if not ax.axison:
                continue
            lo, hi = sorted(axis.get_view_interval())
            for t, loc in zip(axis.get_ticklabels(), axis.get_ticklocs()):
                if not t.get_visible() or not t.get_text().strip():
                    continue
                if not (lo <= loc <= hi):
                    continue
                boxes.append((f"{which}-tick {t.get_text()[:16]!r}",
                              _label_box(t, r), "frame"))

        if scale is None and sized:
            problems.append(
                f"ax{ai}: placement unknown -- no deck call for {stem!r} could "
                f"be read, so the type floor was NOT checked here")
        for s, pt in (sized if scale is not None else []):
            if pt * scale < FLOOR - 0.5:
                problems.append(
                    f"ax{ai}: {pt * scale:.1f} pt on the slide (floor "
                    f"{FLOOR}) -- {s.replace(chr(10), ' | ')[:50]!r}")

        # WHICH PAIRS ARE WORTH COMPARING, and this is the whole difficulty
        # of including the frame. Adding axis labels and tick labels as
        # targets on 9 November produced 190 findings across week 13, and
        # every one sampled was an axis label sitting beside its own ticks --
        # which is not a defect, it is matplotlib's layout doing its job.
        #
        # The distinction that holds: matplotlib GUARANTEES clearance between
        # an axis label and its own tick labels, and between adjacent ticks.
        # It guarantees NOTHING about a title fitting the axes width, so a
        # long title really can overhang and strike a tick (seen on
        # s25_genotypes), and it guarantees nothing about where a human puts
        # a data label or a relocated legend (a legend moved outside the axes
        # printed through the x-label, with this gate reporting zero).
        #
        # So: content is checked against everything, a title is checked
        # against the frame, and frame-against-frame is skipped.
        def _worth(ka, kb):
            kinds = {ka, kb}
            if "content" in kinds:
                return True
            return "title" in kinds and "frame" in kinds

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (na, a, ka), (nb, b, kb) = boxes[i], boxes[j]
                if not _worth(ka, kb):
                    continue
                if (a.x0 < b.x1 + GAP and b.x0 < a.x1 + GAP
                        and a.y0 < b.y1 + GAP and b.y0 < a.y1 + GAP):
                    # SAY HOW CLOSE. "touches" covers everything from a 9 px
                    # near-miss to 40 px of overprint, and those want
                    # different fixes -- the first is a judgement about
                    # whether GAP's margin for cross-machine font swings is
                    # being eaten, the second is ink on ink. Reporting one
                    # number lets a reader triage instead of rendering all
                    # of them. Negative = overlapping, positive = clear.
                    dx = max(b.x0 - a.x1, a.x0 - b.x1)
                    dy = max(b.y0 - a.y1, a.y0 - b.y1)
                    sep = max(dx, dy)
                    how = (f"overlaps by {-sep:.0f} px" if sep < 0
                           else f"clears by only {sep:.0f} px (gap {GAP})")
                    problems.append(f"ax{ai}: {na!r} {how} against {nb!r}")

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
        # Frame boxes (axis labels, tick labels) sit OUTSIDE the data area by
        # construction, so they are targets for other text but not candidates
        # for sitting on a curve. Checking them here would report a y-tick
        # against a curve that starts at the spine.
        for name, bb, _kind in [b for b in boxes if b[2] != "frame"]:
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

            # CONTOURS AND SCATTER ARE NOT `ax.lines`. A nullcline drawn by
            # ax.contour is a LineCollection and a scatter is a PathCollection,
            # so neither is in ax.lines and the loop above cannot see either.
            # Session 24's phase plane shipped a label plate erasing ~50 px of
            # the Cdot1 = 0 nullcline -- and the branch was a contour, so this
            # check scored it clean. A human had to find it by magnifying the
            # PNG. Sample the collections too, densified to about one point per
            # pixel so the count is comparable to the line count above.
            for col in getattr(ax, "collections", []):
                try:
                    if col.get_zorder() is not None and col.get_zorder() <= 1:
                        continue
                    pts = []
                    if hasattr(col, "get_segments"):
                        for sg in col.get_segments():
                            sg = np.asarray(sg, dtype=float)
                            if len(sg) < 2:
                                continue
                            d = ax.transData.transform(sg)
                            for k in range(len(d) - 1):
                                p0, p1 = d[k], d[k + 1]
                                n = int(max(abs(p1[0] - p0[0]),
                                            abs(p1[1] - p0[1]))) + 1
                                pts.append(np.linspace(p0, p1, max(n, 2)))
                    if hasattr(col, "get_offsets"):
                        off = np.asarray(col.get_offsets(), dtype=float)
                        if off.ndim == 2 and off.size:
                            pts.append(ax.transData.transform(off))
                    if not pts:
                        continue
                    cink = np.vstack(pts)
                    cnpx = int(((cink[:, 0] > bb.x0) & (cink[:, 0] < bb.x1)
                                & (cink[:, 1] > bb.y0)
                                & (cink[:, 1] < bb.y1)).sum())
                except Exception:
                    continue                 # never let this crash the gate
                if cnpx > LINE_PX:
                    problems.append(
                        f"ax{ai}: {name!r} sits on {cnpx:.0f} px of a contour "
                        f"or scatter ({type(col).__name__})")

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
    # derivation_fig panels are merged in LAST, with setdefault, so an explicit
    # image()/image_centered() call for the same stem wins. A panel placed both
    # ways (session 25's urn_6 is in the series AND on a slide of its own) lands
    # in two different boxes and this records only the explicit one -- check the
    # other by hand.
    _deriv = {}
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
            if fn == "derivation_fig":
                # theme.derivation_fig puts every panel in its `figs` list into
                # one fixed column -- self.image(s, current, FX, 1.66, 5.4,
                # 4.95) -- and the deck never names that box. Without this
                # branch every derivation panel reported "placement unknown"
                # and its TYPE FLOOR WAS NEVER CHECKED: on week 13 that was 12
                # of 20 figures in session 25 and 8 of 19 in session 24, i.e.
                # more than half of both, silently skipped behind a summary
                # line that looked clean.
                _figs = node.args[4] if len(node.args) >= 5 else None
                for kw in node.keywords:
                    if kw.arg == "figs":
                        _figs = kw.value
                if _figs is not None:
                    for c in ast.walk(_figs):
                        if isinstance(c, ast.Constant) \
                                and isinstance(c.value, str) \
                                and c.value.endswith(".png"):
                            _deriv.setdefault(
                                os.path.basename(c.value)[:-4], (5.4, 4.95))
                continue
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
                # KEEP THE TIGHTEST BAND, AND RECORD THE CONFLICT.
                # This was `out[stem] = band`, i.e. last writer wins -- and
                # the writer is whichever deck the parser happened to read
                # last. Two of session 24's PNGs are re-used by session 25 at
                # band=4.14 against session 24's own 4.40, so the shared
                # figure answered to a band NOT VISIBLE FROM ITS OWN DECK'S
                # CALL. An agent sized `s24_qss_no_hopf` against the 4.40 it
                # could see, and the result projected 20pt type at 19.5pt on
                # session 25's slide -- under the floor, in a different
                # session, with this gate reporting clean. Found 8 November.
                #
                # A figure placed in two boxes has to satisfy the smaller of
                # them, so the tightest band is the honest one to measure
                # against. Area is the proxy: the two cases that matter here
                # share a width and differ in height.
                prev = out.get(stem)
                if prev is None or (band[0] * band[1]) < (prev[0] * prev[1]):
                    out[stem] = band
                if prev is not None and tuple(prev) != tuple(band):
                    MULTI_BAND.setdefault(stem, set()).add(tuple(prev))
                    MULTI_BAND[stem].add(tuple(band))
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
    for _k, _v in _deriv.items():
        out.setdefault(_k, _v)
    return out


def series_consistency(stems):
    """A derivation series must not change size between its own stages.

    THE FLOOR IS NOT THE ONLY THING PLACEMENT CAN BREAK. `audit` checks that a
    figure's text clears 20 pt after placement, and a panel can clear it at
    every stage while the PICTURE jumps -- which is what `derivation_fig` exists
    to prevent ("the drawing grows as the algebra does").

    Session 25 shipped exactly that: `s25_urn_1..5` and `s25_chain_1..4` go into
    `derivation_fig`'s 5.4 x 4.95 box at scale 1.135, while `s25_urn_6` and
    `s25_chain_5` were placed on slides of their own at 4.98 x 4.52, scale
    1.047. Same PNG, adjacent slides, same role -- the urn shrank 7.8% on the
    slide that strikes the heterozygote out, and the chain on the slide that
    carries 1 - 1/R0. Every stage cleared the floor, so nothing complained.

    Groups stems by family (the stem with any trailing _<digits> removed) and
    reports a family whose placement scales differ by more than 2%.
    """
    import re
    from collections import defaultdict
    global _PLACED
    if _PLACED is None:
        try:
            _PLACED = _placements()
        except Exception:
            _PLACED = {}
    fam = defaultdict(list)
    unreadable = []          # never silently skip: a skip that reads as a pass
                             # is the defect this whole module is about
    for st in stems:
        placed = _PLACED.get(st)
        png = ROOT / "figures" / "build" / f"{st}.png"
        if placed is None or not png.exists():
            continue
        try:
            from PIL import Image
            with Image.open(png) as im:
                pw, ph = im.size
            w, h = pw / _dpi(), ph / _dpi()
            mw, band = placed
            fam[re.sub(r"_\d+$", "", st)].append((st, min(mw, band * (w / h)) / w))
        except Exception as exc:
            unreadable.append(f"{st}: could not measure -- {exc}")
    out = []
    for name, items in sorted(fam.items()):
        if len(items) < 2:
            continue
        lo = min(items, key=lambda t: t[1])
        hi = max(items, key=lambda t: t[1])
        if hi[1] - lo[1] > 0.02 * lo[1]:
            out.append(
                f"{name}_*: the series changes size between stages -- "
                f"{lo[0]} at {lo[1]:.3f} against {hi[0]} at {hi[1]:.3f} "
                f"({100 * (hi[1] / lo[1] - 1):.1f}% jump). A derivation picture "
                f"must not resize as the algebra advances.")
    return out + unreadable


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

    # -v is a FLAG, not a module. Leaving it in the list made a clean run end
    # with "-v: could not audit -- No module named 'figures.-v'", which is a
    # gate printing an error on a pass -- and that is how people stop reading
    # gate output at all.
    mods = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not mods:
        mods = sorted(p.stem for p in Path("figures").glob("*.py")
                      if p.stem not in ("style", "__init__"))
    worst = []
    crashed = []
    for m in mods:
        try:
            res = audit_module(m)
        except Exception as exc:
            # A CRASH IS NOT A PASS. This printed one line and `continue`d,
            # so the run still ended "worst first: none" -- and on 9 November
            # that is exactly what happened: a three-tuple change broke an
            # unpack, every module failed to audit, and the summary line
            # said none. A gate that crashes to clean ranks with the defect
            # it was meant to catch (deck-gauntlet 5.7), and this file has
            # now committed that failure twice in one day. So it is counted,
            # it is carried into `worst`, and it sets the exit status.
            print(f"  !! {m}: COULD NOT AUDIT -- {exc}")
            print(f"     This is a FAILURE, not a pass: nothing in {m} was "
                  f"checked.")
            worst.append((10 ** 6, m))
            crashed.append(m)
            continue
        # Series consistency is a PLACEMENT defect across figures, so it
        # cannot be found by auditing one figure at a time -- which is why a
        # derivation picture shrank 8% at the payoff step with every stage
        # clearing the type floor and the gate reporting zero.
        series = series_consistency([name for name, _, _ in res])
        n = sum(len(p) for _, _, p in res) + len(series)
        scales = [s for _, s, _ in res if s is not None]
        unknown = sum(1 for _, s, _ in res if s is None)
        if n:
            worst.append((n, m))
        shown = (f"min placement scale {min(scales):.3f}" if scales
                 else "no placement readable")
        if unknown:
            shown += f"  ({unknown} unplaced)"
        print(f"{m:24s} {len(res):2d} figure(s)  {shown}  {n:3d} problem(s)")
        for pr in series:
            print(f"    {pr}")          # always shown, never behind -v
        # A figure placed in two different boxes is measured against the
        # tighter one. Say so unconditionally: the whole point is that the
        # binding box is NOT visible from the deck being worked on.
        for stem, bands in sorted(MULTI_BAND.items()):
            if any(stem == name for name, _, _ in res):
                shown_b = ", ".join(f"{w:g}x{h:g}" for w, h in sorted(bands))
                print(f"    !! {stem} is placed at {len(bands)} different "
                      f"bands ({shown_b}); measured against the tightest")
        if "-v" in sys.argv:
            for name, scale, probs in res:
                for pr in probs:
                    print(f"    {name}: {pr}")
    print("\nworst first:", ", ".join(f"{m} ({n})" for n, m in
                                      sorted(worst, reverse=True)[:10]) or "none")
