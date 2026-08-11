#!/usr/bin/env python3
"""Execute every notebook in the repository; fail on any error.

This is the test that matters most. Unit tests cover posb; this covers the
thing students actually run. Run it before every push.

Usage:
    python tools/execute_notebooks.py
    python tools/execute_notebooks.py --html out/   # also write rendered HTML
"""
import argparse
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ["sessions", "problem-sets"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", metavar="DIR", help="write rendered HTML here")
    args = ap.parse_args()

    def is_student_template(path):
        """Student problem sets have blanks, so grader.check() is meant to fail.

        They are verified instead by build_problem_sets.py, which executes the
        *solution* notebook and requires every check to pass.
        """
        text = path.read_text()
        return "otter" in text and "grader.check" in text

    paths = sorted(p for d in SEARCH for p in (ROOT / d).rglob("*.ipynb")
                   if ".ipynb_checkpoints" not in str(p))
    skipped = [p for p in paths if is_student_template(p)]
    paths = [p for p in paths if p not in skipped]
    for p in skipped:
        print(f"SKIP  {p.relative_to(ROOT)}  (student template; verified via its solution notebook)")
    if not paths:
        print("No notebooks found.")
        return

    failures = []
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        client = NotebookClient(
            nb, timeout=600, kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        )
        rel = path.relative_to(ROOT)
        try:
            client.execute()
            print(f"PASS  {rel}")
            if args.html:
                from nbconvert import HTMLExporter
                out = Path(args.html)
                out.mkdir(parents=True, exist_ok=True)
                body, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
                (out / f"{path.stem}.html").write_text(body)
        except CellExecutionError as exc:
            print(f"FAIL  {rel}")
            failures.append((rel, str(exc)[:2000]))

    if failures:
        print("\n" + "=" * 72)
        for rel, msg in failures:
            print(f"\n--- {rel} ---\n{msg}")
        sys.exit(1)
    print(f"\nAll {len(paths)} notebooks executed cleanly.")


if __name__ == "__main__":
    main()
