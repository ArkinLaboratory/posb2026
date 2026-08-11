#!/usr/bin/env python3
"""Render handouts/*.md into print-ready HTML in handouts/build/.

    python tools/build_handouts.py            # all
    python tools/build_handouts.py s01        # matching only

Why HTML and not PDF: the handouts have to print on a departmental printer the
morning of class, from whatever machine is to hand, with no toolchain. A
self-contained HTML file with an @page rule opens anywhere and prints from the
browser. Adding LaTeX or weasyprint to the critical path of "it is 7am and I
need forty copies" is a bad trade.

Front matter is an HTML comment at the top of the file so the source still
renders as ordinary Markdown on GitHub:

    <!--
    title: Session 1 -- Diagnostic
    subtitle: Ungraded. Eight minutes.
    session: 1
    -->

Three CSS hooks, and no more: `<div class="rule"></div>` is a ruled writing line,
`<span class="blank"></span>` an inline blank, `<div class="eq">` a display
equation. Write equations in Unicode -- there is deliberately no LaTeX here. A
handout printed at 7am cannot depend on a MathJax CDN, and silently printing
`$\alpha$` at a class is worse than not having the symbol, so the builder
refuses to render a file containing dollar-delimited math.
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "handouts"
OUT = SRC / "build"

FRONT = re.compile(r"\A<!--(.*?)-->", re.S)

CSS = """
@page { size: letter; margin: 0.7in 0.75in 0.6in 0.75in; }
* { box-sizing: border-box; }
body { font: 11.5pt/1.45 Calibri, "Segoe UI", system-ui, sans-serif;
       color: #23423F; margin: 0 auto; max-width: 7.0in; padding: 0.4in 0; }
h1 { font: bold 20pt/1.2 Cambria, Georgia, serif; color: #0B3A3F;
     margin: 0 0 0.10in; }
h2 { font: bold 14pt/1.25 Cambria, Georgia, serif; color: #0E4F57;
     margin: 0.26in 0 0.08in; page-break-after: avoid; }
h3 { font: bold 12pt/1.3 Cambria, Georgia, serif; color: #0E4F57;
     margin: 0.20in 0 0.06in; page-break-after: avoid; }
p { margin: 0.06in 0; }
hr { border: 0; border-top: 1px solid #D3DEDA; margin: 0.20in 0; }
blockquote { margin: 0.10in 0; padding: 0.09in 0.16in; border-left: 3px solid #4FD1C5;
             background: #E8F4F0; font-style: italic; }
code, pre { font-family: "Cascadia Mono", Consolas, monospace; font-size: 10pt; }
pre { background: #F4F8F7; border: 1px solid #D3DEDA; border-radius: 4px;
      padding: 0.10in 0.14in; overflow: visible; white-space: pre-wrap; }
table { border-collapse: collapse; width: 100%; margin: 0.10in 0; font-size: 10.5pt; }
td, th { border: 1px solid #D3DEDA; padding: 0.05in 0.07in; text-align: left; }
.rule { border-bottom: 1px solid #A8C8D8; height: 0.30in; margin-top: 0.06in; }
.blank { display: inline-block; width: 0.8in; border-bottom: 1px solid #A8C8D8;
         height: 1em; vertical-align: baseline; }
.eq { font: 13pt/1.4 Cambria, Georgia, serif; color: #0B3A3F; text-align: center;
      margin: 0.12in 0; }
.masthead { border-bottom: 2px solid #0E4F57; padding-bottom: 0.08in;
            margin-bottom: 0.18in; }
.masthead .course { font-size: 9.5pt; letter-spacing: 0.06em;
                    text-transform: uppercase; color: #6E8B87; font-weight: bold; }
.sub { color: #6E8B87; font-style: italic; margin: 0.02in 0 0; }
.foot { margin-top: 0.30in; padding-top: 0.08in; border-top: 1px solid #D3DEDA;
        font-size: 8.5pt; color: #6E8B87; }
@media print { body { padding: 0; max-width: none; } .noprint { display: none; } }
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head><body>
<div class="masthead">
  <div class="course">Principles of Synthetic Biology &middot; BioE 147 / 247 &middot; {term}</div>
  <p class="sub">{subtitle}</p>
</div>
{body}
<div class="foot">{foot}</div>
</body></html>
"""


def front_matter(text):
    """Pull the leading HTML comment off, parse `key: value` lines from it."""
    m = FRONT.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    return meta, text[m.end():]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sources = sorted(p for p in SRC.glob("*.md")
                     if not args or any(a in p.name for a in args))
    if not sources:
        sys.exit(f"no handout matches {args}. available: "
                 f"{[p.name for p in sorted(SRC.glob('*.md'))]}")

    from tools.schedule import course, session_date
    term = course()["term"]

    OUT.mkdir(parents=True, exist_ok=True)
    for src in sources:
        meta, text = front_matter(src.read_text())
        # LaTeX would print as raw source. Fail loudly rather than at 7am.
        stray = re.search(r"\$\$?[^$\n]+\$\$?", text)
        if stray:
            sys.exit(f"{src.name}: contains LaTeX math ({stray.group(0)!r}). "
                     f"These handouts render without a math engine -- write it "
                     f"in Unicode, and use <div class=\"eq\"> for a display "
                     f"equation.")
        body = markdown.markdown(
            text, extensions=["tables", "fenced_code", "md_in_html"])

        foot = f"Principles of Synthetic Biology &middot; {term}"
        if meta.get("session"):
            n = int(meta["session"])
            d = session_date(n).strftime("%A %d %B %Y").replace(" 0", " ")
            foot = f"Session {n} &middot; {d} &middot; ungraded unless stated"

        html = PAGE.format(
            title=meta.get("title", src.stem),
            subtitle=meta.get("subtitle", ""),
            term=term, css=CSS, body=body, foot=foot)
        dst = OUT / f"{src.stem}.html"
        dst.write_text(html)
        print(f"  {src.name:<28} -> {dst.relative_to(ROOT)}")

    print(f"\nOpen in a browser and print. Letter, portrait, no scaling.")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
