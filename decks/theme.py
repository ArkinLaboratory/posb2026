"""Deck theme and layout helpers, keyed to the course logo.

Why python-pptx and not pptxgenjs: this repository is a Python toolchain and
the instructor is a Python programmer. A deck you can read and modify beats a
deck someone else can generate, and macOS does not ship Node.

Every deck is a Python module that calls these helpers. The helpers enforce the
things that are actually load-bearing -- consistent signalling, dark slides as
mode boundaries, extracted terms rather than prose -- so a new deck is short and
cannot drift from the house style. See docs/lecture-design.md for why the
structure is what it is.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent

# --- palette, sampled from the course logo ---------------------------------
TEAL = RGBColor(0x0E, 0x4F, 0x57)
GREEN = RGBColor(0x1A, 0x4D, 0x33)
MINT = RGBColor(0xA5, 0xD6, 0xA7)
CYAN = RGBColor(0x4F, 0xD1, 0xC5)
SILVER = RGBColor(0xA8, 0xC8, 0xD8)
INK = RGBColor(0x0B, 0x3A, 0x3F)
BODY = RGBColor(0x23, 0x42, 0x3F)
MUTED = RGBColor(0x6E, 0x8B, 0x87)
AMBER = RGBColor(0xD9, 0x8E, 0x32)
RED = RGBColor(0xB3, 0x26, 0x1E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0xD3, 0xDE, 0xDA)
WASH = RGBColor(0xE8, 0xF4, 0xF0)

HEAD, TEXT = "Cambria", "Calibri"
W, H, M = 13.333, 7.5, 0.7          # slide size and margin, inches


class Deck:
    """A lecture deck. Every method returns self or a slide, so decks read
    top to bottom like the lecture does."""

    def __init__(self, title, subtitle="", meta=""):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W)
        self.prs.slide_height = Inches(H)
        self.title_text = title
        self.subtitle = subtitle
        self.meta = meta
        self.missing_figures = []

    # -- slide construction --------------------------------------------------
    def _slide(self, dark):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])   # blank
        bg = ROOT / "decks" / ("bg_dark.png" if dark else "bg_light.png")
        if bg.exists():
            pic = s.shapes.add_picture(str(bg), 0, 0,
                                       width=Inches(W), height=Inches(H))
            s.shapes._spTree.remove(pic._element)
            s.shapes._spTree.insert(2, pic._element)
        s._posb_dark = dark
        return s

    def dark(self):
        return self._slide(True)

    def light(self):
        return self._slide(False)

    # -- text ----------------------------------------------------------------
    def text(self, s, txt, x, y, w, h, size=14, font=None, bold=False,
             italic=False, color=None, align="l", valign=None, spacing=None,
             space_pt=0):
        box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        if valign:
            tf.vertical_anchor = {"m": MSO_ANCHOR.MIDDLE,
                                  "t": MSO_ANCHOR.TOP}[valign]
        for i, line in enumerate(str(txt).split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                           "r": PP_ALIGN.RIGHT}[align]
            if spacing:
                p.line_spacing = spacing
            if space_pt:
                p.space_after = Pt(space_pt)
            r = p.add_run()
            r.text = line
            f = r.font
            f.name = font or TEXT
            f.size = Pt(size)
            f.bold = bold
            f.italic = italic
            f.color.rgb = color or BODY
        return box

    def shape(self, s, kind, x, y, w, h, fill=None, line=None, lw=1.5):
        shp = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid()
            shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line
            shp.line.width = Pt(lw)
        shp.shadow.inherit = False
        if shp.has_text_frame:
            shp.text_frame.text = ""
        return shp

    def image(self, s, path, x, y, w=None, h=None):
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        s.shapes.add_picture(str(p), Inches(x), Inches(y),
                             Inches(w) if w else None, Inches(h) if h else None)

    # -- repeating layout elements ------------------------------------------
    def header(self, s, badge, label):
        """Time badge + segment label. Same look every time: this is signalling,
        and signalling is one of the few interventions that helps novices and
        experts equally."""
        dark = s._posb_dark
        self.shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, M, 0.42, 1.62, 0.34,
                   fill=CYAN if dark else TEAL, line=None)
        self.text(s, badge, M, 0.47, 1.62, 0.3, size=11, bold=True,
                  color=INK if dark else WHITE, align="c")
        self.text(s, label.upper(), M + 1.8, 0.47, 9.5, 0.3, size=11, bold=True,
                  color=MINT if dark else MUTED)

    def title(self, s, txt, y=0.95, size=32):
        self.text(s, txt, M, y, W - 2 * M, 0.95, size=size, font=HEAD,
                  bold=True, color=WHITE if s._posb_dark else INK)

    def foot(self, s, txt, y=6.45):
        self.text(s, txt, M, y, W - 2 * M, 0.4, size=11.5, italic=True,
                  color=SILVER if s._posb_dark else MUTED)

    def notes(self, s, txt):
        s.notes_slide.notes_text_frame.text = txt

    # -- the paper-figure slot ----------------------------------------------
    def paper_figure(self, s, key, x, y, w, h, ref, caption):
        """Embed a figure from a published paper -- if it is available locally.

        Copyrighted figures cannot live in this public CC BY repository. So the
        image is looked up in `private/paper-figures/<key>.png`, which is
        gitignored:

          * present  -> the real figure is embedded (your classroom deck)
          * absent   -> a labelled slot is drawn naming the exact figure
                        (what CI builds, and what a fork sees)

        Same source, same command, two outputs. Nothing is ever edited by hand.
        """
        img = ROOT / "private" / "paper-figures" / f"{key}.png"
        if img.exists():
            self.image(s, img, x, y, w, h)
            self.text(s, ref, x, y + h + 0.04, w, 0.25, size=9,
                      italic=True, color=MUTED if not s._posb_dark else SILVER,
                      align="c")
            return True

        self.missing_figures.append((key, ref))
        box = self.shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h,
                         fill=CARD, line=AMBER, lw=2)
        box.line.dash_style = 4      # dashed
        self.text(s, "FIGURE FROM THE PAPER", x, y + h / 2 - 0.55, w, 0.3,
                  size=9.5, bold=True, color=AMBER, align="c")
        self.text(s, ref, x, y + h / 2 - 0.22, w, 0.35, size=14, font=HEAD,
                  bold=True, color=INK, align="c")
        self.text(s, caption, x + 0.2, y + h / 2 + 0.14, w - 0.4, 0.6,
                  size=11.5, italic=True, color=MUTED, align="c")
        return False

    # -- output --------------------------------------------------------------
    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(path))
        return path
