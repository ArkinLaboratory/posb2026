#!/usr/bin/env python3
"""Turn a problem set's README.md into the HTML that goes in the Canvas
assignment description.

    python tools/build_canvas_description.py ps02

WHY THIS EXISTS. The Canvas description is not fresh prose -- it *is* the
problem set's README, because a student who reads one and not the other must
not get different instructions. Converting it by hand is the step that failed
on PS1: the description shipped without the DataHub and Colab links, leaving a
student with somewhere to submit and no way to obtain the thing they were
submitting. It was reported within the hour.

The mangling has a mechanism. The DataHub URL is an nbgitpuller link -- a query
string with `?repo=...&branch=...&urlpath=...` -- and Canvas's rich-text editor
re-encodes query strings when you paste into it. Pasting through the `</>`
(raw HTML) view is the only route that survives, so this writes HTML for that
box and nothing else.

What is deliberately dropped:

  * the first line's back-link to ../README.md, which is a repository path and
    means nothing inside Canvas
  * $...$ math, which Canvas renders through MathJax only in its own equation
    editor. Rather than paste raw LaTeX -- `\\frac{dp}{dt} = \\alpha ...` reads as a
    defect to a student -- the small set of constructs these READMEs actually
    use is rewritten into Unicode and set as a code span, which needs no
    renderer at all.

Output goes to private/build/psNN/canvas-description.html (gitignored). Open
it, select all, paste into the `</>` view of the Canvas description.
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent


GREEK = {"alpha": "\u03b1", "beta": "\u03b2", "gamma": "\u03b3", "delta": "\u03b4",
         "mu": "\u03bc", "lambda": "\u03bb", "tau": "\u03c4", "sigma": "\u03c3",
         "theta": "\u03b8", "phi": "\u03c6", "rho": "\u03c1", "epsilon": "\u03b5",
         "Delta": "\u0394", "Omega": "\u03a9"}


def _plain(tex):
    """The small subset of LaTeX these READMEs use, as Unicode.

    Deliberately not a LaTeX engine. If a README grows an expression this
    cannot render, the right response is to simplify the expression -- a
    Canvas assignment description is not the place for one that needs MathJax.
    """
    t = tex.strip()
    t = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", t)
    t = re.sub(r"\\(" + "|".join(GREEK) + r")\b", lambda m: GREEK[m.group(1)], t)
    t = t.replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
    t = t.replace("\\left", "").replace("\\right", "")
    t = t.replace("\\cdot", "\u00b7").replace("\\times", "\u00d7")
    t = t.replace("\\ln", "ln").replace("\\log", "log").replace("\\exp", "exp")
    t = re.sub(r"\{([^{}]*)\}", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def build(tag):
    src = list((ROOT / "problem-sets").glob(f"{tag}-*/README.md"))
    if not src:
        sys.exit(f"no problem-sets/{tag}-*/README.md")
    text = src[0].read_text()

    # Drop the repository back-link line: "[← all problem sets](../README.md) · ..."
    # but keep everything after the first "·" on that line, which carries the
    # due date and the point total.
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if "](../README.md)" in ln:
            lines[i] = re.sub(r"^\[[^\]]*\]\(\.\./README\.md\)\s*·\s*", "", ln)
            break
    text = "\n".join(lines)

    # $$...$$ and $...$ -> Unicode inside a code span.
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: f"\n`{_plain(m.group(1))}`\n",
                  text, flags=re.S)
    text = re.sub(r"\$([^$\n]+)\$", lambda m: f"`{_plain(m.group(1))}`", text)

    html = markdown.markdown(text, extensions=["tables", "sane_lists"])

    out = ROOT / "private" / "build" / tag
    out.mkdir(parents=True, exist_ok=True)
    path = out / "canvas-description.html"
    path.write_text(html + "\n")

    # The one thing worth checking after the conversion is the one thing that
    # broke last time.
    for needle, what in [("datahub.berkeley.edu", "DataHub link"),
                         ("colab.research.google.com", "Colab link")]:
        if needle not in html:
            sys.exit(f"the {what} did not survive the conversion -- do not paste this")

    print(f"{path.relative_to(ROOT)}  ({len(html)} chars)")
    print("Both links survived. Paste into the Canvas description via the "
          "</> button, not the rich-text box.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().split("\n\n")[1].strip())
    build(sys.argv[1])
