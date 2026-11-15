#!/usr/bin/env python3
"""Verify every relative link in every Markdown file in this repository.

    python tools/check_doc_links.py            # report
    python tools/check_doc_links.py --strict   # also fail on untracked targets (CI)

Two different failures, and the second is the dangerous one.

**Broken** -- the target does not exist. Loud, and usually caught by whoever
clicks it.

**Untracked** -- the target exists on your disk but is not committed, so the
link works perfectly for you and 404s for every other human being. Nothing on
your machine will ever tell you. This is how `docs/coverage-matrix.md` came to
be linked from the public README while being invisible on GitHub, and how a
bare `build/` line in .gitignore silently untracked every generated figure the
session READMEs depend on.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Directories this check must not walk. The first five were always here;
# ".venv" and "_scratch" were added 14 November 2026 after a virtualenv
# created in the repo root put THREE third-party package READMEs into the
# BROKEN list -- mdit_py_plugins and playwright, whose own relative links
# are none of this repository's business -- and blocked a release. Both
# are already in .gitignore; this walk is a filesystem walk and never
# learned that. A broken link inside site-packages is not a broken link
# in the course.
SKIP = {".git", "_to_delete", "private", ".ipynb_checkpoints",
        "node_modules", ".venv", "venv", "_scratch"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero on untracked targets too")
    args = ap.parse_args()

    tracked = set(subprocess.run(["git", "--no-optional-locks", "ls-files"],
                                 cwd=ROOT, capture_output=True, text=True).stdout.split())
    broken, untracked = [], {}

    for md in sorted(ROOT.rglob("*.md")):
        if SKIP & set(md.relative_to(ROOT).parts):
            continue
        for m in LINK.finditer(md.read_text(errors="ignore")):
            target = m.group(1).split("#")[0]
            if not target or target.startswith(("http", "mailto:")):
                continue
            src = md.relative_to(ROOT).as_posix()
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                broken.append((src, target))
                continue
            rel = os.path.relpath(resolved, ROOT)
            if resolved.is_file() and rel not in tracked:
                untracked.setdefault(rel, []).append(src)

    for src, target in broken:
        print(f"BROKEN     {src} -> {target}")
    for rel, srcs in sorted(untracked.items()):
        print(f"UNTRACKED  {rel}  (linked from {', '.join(sorted(set(srcs)))})")

    if not broken and not untracked:
        print("OK: every relative link resolves and every target is committed")
        return 0
    print(f"\n{len(broken)} broken, {len(untracked)} untracked target(s)")
    if untracked and not args.strict:
        print("Untracked targets are usually just work you have not committed yet.")
    return 1 if broken or (untracked and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
