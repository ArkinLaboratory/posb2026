#!/usr/bin/env python3
"""Generate every course notebook from its source module.

The Python modules in tools/sources/ are the SOURCE OF TRUTH. The .ipynb files
are build artifacts. Never hand-edit a .ipynb: executed notebooks churn
`execution_count` and `outputs` on every cell, which fights nbgitpuller's
merge rule and silently strands your fixes on students who have already run
the notebook.

Usage:
    python tools/build_notebooks.py
    python tools/build_notebooks.py --check    # fail if anything is stale
"""
import argparse
import importlib
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# Every notebook in the course. Add a line here when you add one.
NOTEBOOKS = [
    "sources.ps00",
    "sources.d02",
    "sources.s03",
    "sources.d09",
]

METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python",
                   "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
    "colab": {"provenance": []},
}


def build(module_name):
    mod = importlib.import_module(module_name)
    nb = nbf.v4.new_notebook()
    nb.cells = mod.CELLS
    nb.metadata = METADATA

    # Deterministic cell IDs. nbformat assigns random ones by default, which
    # would make every rebuild produce a different file -- churning git
    # history and, worse, guaranteeing nbgitpuller merge conflicts against
    # students' executed copies. Stable IDs mean a rebuild with no content
    # change is a genuine no-op.
    for i, cell in enumerate(nb.cells):
        cell["id"] = f"c{i:03d}"

    return Path(ROOT / mod.REL), nb, mod.TITLE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any notebook on disk differs from source")
    args = ap.parse_args()

    stale = []
    for name in NOTEBOOKS:
        path, nb, title = build(name)
        new = nbf.writes(nb)
        if args.check:
            old = path.read_text() if path.exists() else ""
            status = "OK   " if old == new else "STALE"
            if old != new:
                stale.append(path)
            print(f"{status} {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new)
            print(f"wrote {str(path.relative_to(ROOT)):<50} {len(nb.cells):>3} cells  — {title}")

    if stale:
        print(f"\n{len(stale)} notebook(s) out of date. Run: python tools/build_notebooks.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
