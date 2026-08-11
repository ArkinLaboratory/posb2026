#!/usr/bin/env python3
"""Render handouts/*.md to print-ready PDF, with real mathematics.

    python tools/build_handouts.py            # all
    python tools/build_handouts.py s01        # matching only
    python tools/build_handouts.py --check    # CI: fail if any PDF is stale

**The PDFs are committed.** That is a deliberate exception to this repository's
rule that build artifacts are not tracked, and the reason is the failure mode
this tool exists to prevent: it is 7am, class is at 8, and you need forty
copies. At that moment you must be able to open a file and press print, with no
Python, no browser automation and no network. Everything else here -- the
Markdown source, the toolchain below -- exists to produce that file well in
advance.

## How the maths works

LaTeX in, SVG out, rendered at BUILD time by MathJax inside headless Chromium.
The PDF therefore contains vector glyphs and no font or script dependency at
all. Nothing is rendered while you are standing at the printer.

Markdown and LaTeX fight over the same characters -- `_` is a subscript in one
and emphasis in the other, `*` and `\\` likewise -- so math spans are lifted out
before the Markdown processor runs and put back afterwards. Without that,
`$x_1$` silently becomes `$x<em>1$`.

## Front matter

An HTML comment, so the source still renders as ordinary Markdown on GitHub:

    <!--
    title: Session 1 -- Diagnostic
    subtitle: Ungraded. Eight minutes.
    session: 1
    -->

## Layout hooks

`<div class="rule"></div>` a ruled writing line; `<span class="blank"></span>`
an inline blank; `<div class="pagebreak"></div>` forces a new page; and
`<div class="q" markdown="1"> ... </div>` keeps a question and its answer lines
on the same sheet, which is the difference between a handout and an annoyance.

## Requirements

playwright with Chromium, and one 2 MB MathJax download cached in
tools/.cache/ on first run. Both are instructor-side only; students never build
a handout.
"""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "handouts"
CACHE = ROOT / "tools" / ".cache"
MATHJAX = CACHE / "mathjax-tex-svg-3.2.2.js"
MATHJAX_URL = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"

FRONT = re.compile(r"\A<!--(.*?)-->", re.S)

# Display first, so $$..$$ is never eaten as two inline spans.
MATH = re.compile(r"(\$\$.+?\$\$|\\\[.+?\\\]|(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$))",
                  re.S)

CSS = """
@page { size: letter; margin: 0.7in 0.75in 0.6in 0.75in; }
* { box-sizing: border-box; }
body { font: 11.5pt/1.45 "Calibri", "Carlito", "Segoe UI", system-ui, sans-serif;
       color: #23423F; margin: 0; }
h1 { font: bold 20pt/1.2 "Cambria", "Caladea", Georgia, serif; color: #0B3A3F;
     margin: 0 0 0.10in; }
h2 { font: bold 14pt/1.25 "Cambria", "Caladea", Georgia, serif; color: #0E4F57;
     margin: 0.26in 0 0.08in; page-break-after: avoid; }
h3 { font: bold 12pt/1.3 "Cambria", "Caladea", Georgia, serif; color: #0E4F57;
     margin: 0.20in 0 0.06in; page-break-after: avoid; }
p { margin: 0.06in 0; orphans: 2; widows: 2; }
hr { border: 0; border-top: 1px solid #D3DEDA; margin: 0.20in 0; }
blockquote { margin: 0.10in 0; padding: 0.09in 0.16in;
             border-left: 3px solid #4FD1C5; background: #E8F4F0;
             font-style: italic; page-break-inside: avoid; }
code, pre { font-family: "Cascadia Mono", "DejaVu Sans Mono", Consolas, monospace;
            font-size: 9.5pt; }
pre { background: #F4F8F7; border: 1px solid #D3DEDA; border-radius: 4px;
      padding: 0.08in 0.12in; line-height: 1.3; white-space: pre-wrap;
      page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; margin: 0.10in 0;
        font-size: 10.5pt; page-break-inside: avoid; }
td, th { border: 1px solid #D3DEDA; padding: 0.05in 0.07in; text-align: left; }
th { background: #F4F8F7; font-size: 9.5pt; letter-spacing: 0.03em;
     text-transform: uppercase; color: #0E4F57; white-space: nowrap; }
.rule { border-bottom: 1px solid #A8C8D8; height: 0.28in; margin-top: 0.05in; }
.blank { display: inline-block; width: 0.8in; border-bottom: 1px solid #A8C8D8;
         height: 1em; vertical-align: baseline; }
.pagebreak { page-break-after: always; }
/* Wrap a question in <div class="q" markdown="1"> ... </div> to stop the
   printer splitting its prompt from its answer lines. */
.q { page-break-inside: avoid; }
.masthead { border-bottom: 2px solid #0E4F57; padding-bottom: 0.08in;
            margin-bottom: 0.18in; }
.masthead .course { font-size: 9.5pt; letter-spacing: 0.06em;
                    text-transform: uppercase; color: #6E8B87; font-weight: bold; }
.sub { color: #6E8B87; font-style: italic; margin: 0.02in 0 0; }
mjx-container[display] { margin: 0.13in 0 !important; }
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<script>window.MathJax = {{
  tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']],
         displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'local' }},
  startup: {{ pageReady: () => MathJax.startup.defaultPageReady()
                .then(() => {{ window.__posbMathDone = true; }}) }}
}};</script>
<script>{mathjax}</script>
<style>{css}</style>
</head><body>
<div class="masthead">
  <div class="course">Principles of Synthetic Biology &middot; BioE 147 / 247 &middot; {term}</div>
  <p class="sub">{subtitle}</p>
</div>
{body}
</body></html>
"""


def front_matter(text):
    m = FRONT.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    return meta, text[m.end():]


def render_markdown(text):
    """Markdown, with LaTeX spans held out of its reach.

    Markdown would treat `_`, `*` and `\\` inside math as its own syntax. So the
    math is replaced by inert placeholders, Markdown runs, and the original
    strings go back verbatim for MathJax to find.
    """
    spans = []

    def stash(m):
        spans.append(m.group(0))
        return f"@@MATH{len(spans) - 1}@@"

    html = markdown.markdown(MATH.sub(stash, text),
                             extensions=["tables", "fenced_code", "md_in_html"])
    for i, s in enumerate(spans):
        html = html.replace(f"@@MATH{i}@@", s)
    return html


def mathjax():
    """The MathJax bundle, fetched once and cached. Never at print time."""
    if MATHJAX.exists():
        return MATHJAX.read_text(encoding="utf-8")
    CACHE.mkdir(parents=True, exist_ok=True)
    print(f"  fetching MathJax once -> {MATHJAX.relative_to(ROOT)}")
    try:
        with urllib.request.urlopen(MATHJAX_URL, timeout=60) as r:
            data = r.read()
    except Exception as e:
        sys.exit(f"could not fetch MathJax ({e}). This is a one-time download; "
                 f"run once with network, and every later build is offline.")
    MATHJAX.write_bytes(data)
    return data.decode("utf-8")


def build_pdf(html, dst):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright is not installed. It is instructor-only:\n"
                 "    pip install playwright && playwright install chromium")
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.set_content(html, wait_until="networkidle")
        # MathJax v3 typesets asynchronously. Wait for the flag its own
        # pageReady promise sets -- polling the internal state machine is
        # version-fragile and silently times out when it changes.
        page.wait_for_function("() => window.__posbMathDone === true",
                               timeout=60000)
        page.pdf(path=str(dst), format="Letter", print_background=True,
                 margin={"top": "0.7in", "bottom": "0.6in",
                         "left": "0.75in", "right": "0.75in"})
        b.close()


def main():
    check = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    # README.md documents the folder; it is not a handout.
    available = sorted(p for p in SRC.glob("*.md") if p.stem.lower() != "readme")
    sources = [p for p in available if not args or any(a in p.name for a in args)]
    if not sources:
        sys.exit(f"no handout matches {args}. available: "
                 f"{[p.name for p in available]}")

    from tools.schedule import course, session_date
    term = course()["term"]
    # --check compares a hash of the page with the MathJax bundle removed, so
    # it needs neither the 2 MB download nor a browser. That is what makes it
    # cheap enough to run in CI.
    js = "" if check else mathjax()

    stale = []
    for src in sources:
        meta, text = front_matter(src.read_text())
        sub = meta.get("subtitle", "")
        if meta.get("session"):
            n = int(meta["session"])
            d = session_date(n).strftime("%A %d %B %Y").replace(" 0", " ")
            sub = f"Session {n} &middot; {d}" + (f" &middot; {sub}" if sub else "")

        html = PAGE.format(title=meta.get("title", src.stem), subtitle=sub,
                           term=term, css=CSS, mathjax=js,
                           body=render_markdown(text))
        dst = SRC / f"{src.stem}.pdf"

        # A PDF carries a creation date, so it is never byte-identical between
        # runs. Stamp the source hash into a sidecar and compare that instead.
        stamp = SRC / ".build" / f"{src.stem}.sha"
        digest = hashlib.sha256(
            (html.replace(js, "")).encode("utf-8")).hexdigest()

        if check:
            if not dst.exists() or not stamp.exists() \
                    or stamp.read_text().strip() != digest:
                stale.append(src.name)
            continue

        build_pdf(html, dst)
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(digest + "\n")
        print(f"  {src.name:<28} -> {dst.relative_to(ROOT)}")

    if check:
        if stale:
            sys.exit(f"--check: {len(stale)} handout(s) stale: "
                     f"{', '.join(stale)}. Run `python tools/build_handouts.py`.")
        print(f"OK: {len(sources)} handout(s) up to date")
        return

    print("\nPDFs are committed. Print them; do not rebuild on the morning.")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
