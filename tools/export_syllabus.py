#!/usr/bin/env python3
"""Export docs/syllabus.md to a form that survives being pasted into bCourses.

    python tools/export_syllabus.py                    # writes to the default Dropbox path
    python tools/export_syllabus.py --out DIR
    python tools/export_syllabus.py --check            # report link problems, write nothing

## Why this exists

The syllabus is written for the repository, where relative links work. Pasted
into Canvas, `[Coverage Matrix](coverage-matrix.md)` resolves against the Canvas
page URL and 404s -- silently, for every student, on the one document they are
most likely to actually click through.

Three things therefore happen on export:

1. **The repository navigation header is removed.** "back to README" is chrome
   for someone browsing GitHub; it is noise on a course page.
2. **Relative links become absolute GitHub URLs.** Anything still pointing at a
   file in this repository is rewritten to `blob/main/...`.
3. **Untracked targets are reported.** A file that exists on your disk but is
   not committed will 404 on GitHub for everyone but you. That is the failure
   this script is loudest about, because it is invisible from your machine.

The exported files carry a DO-NOT-EDIT banner. **`docs/syllabus.md` is the
source of truth**; editing an export means the next run destroys your change,
and a syllabus that disagrees with the repository is how the 8:00-versus-8:10
error survived for weeks.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "syllabus.md"
BLOB = "https://github.com/ArkinLaboratory/posb2026/blob/main/"
# Sibling of the repository, so this survives the whole tree being moved.
# posb2026/ and 2026/ live side by side under the project root.
DEFAULT_OUT = ROOT.parent / "2026" / "bcourses"

NAV = re.compile(r"^\*\*Fall 2026\*\*[^\n]*\n(?:[^\n]*\n)*?(?=\n)", re.M)
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def tracked_files():
    out = subprocess.run(["git", "--no-optional-locks", "ls-files"],
                         cwd=ROOT, capture_output=True, text=True)
    return set(out.stdout.split())


def convert(text, tracked, problems):
    def sub(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http", "#", "mailto:")):
            return m.group(0)
        path, _, frag = target.partition("#")
        if not path:
            return m.group(0)
        resolved = (SRC.parent / path).resolve()
        try:
            rel = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            problems.append(f"points outside the repository: {target}")
            return label
        if not resolved.exists():
            problems.append(f"target does not exist: {target}")
            return label
        if rel not in tracked:
            problems.append(f"UNTRACKED, will 404 on GitHub until committed: {rel}")
        return f"[{label}]({BLOB}{rel}{'#' + frag if frag else ''})"
    return LINK.sub(sub, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    text = SRC.read_text()
    before = len(text)
    text = NAV.sub("", text, count=1)
    stripped = before != len(text)

    problems = []
    text = convert(text, tracked_files(), problems)

    for p in problems:
        print(f"  ! {p}")
    if args.check:
        print(f"{len(problems)} problem(s). Nothing written.")
        return 1 if problems else 0

    banner_md = ("<!-- GENERATED EXPORT - DO NOT EDIT.\n"
                 "     Source of truth: docs/syllabus.md in the posb2026 repository.\n"
                 "     Regenerate with: python tools/export_syllabus.py -->\n\n")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "syllabus.md").write_text(banner_md + text)

    try:
        import markdown
    except ImportError:
        print("markdown not installed; wrote .md only (pip install markdown)")
        return 0
    body = markdown.markdown(text, extensions=["extra", "sane_lists", "toc"])
    (args.out / "syllabus.html").write_text(banner_md.replace("<!--", "<!--", 1) + body)

    print(f"wrote {args.out}/syllabus.md and syllabus.html"
          f"{' (nav header stripped)' if stripped else ' (WARNING: no nav header found to strip)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
