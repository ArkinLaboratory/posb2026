#!/usr/bin/env python3
"""Build problem sets from private master sources via otter-grader.

WHY THIS IS SEPARATE FROM build_notebooks.py
--------------------------------------------
This repository is public. Problem-set masters contain solutions, so they live
under private/ (gitignored) and never enter git history. Only the *student*
version -- solutions stripped by Otter -- is committed to problem-sets/.

Pipeline:
    private/sources/psNN.py   (master source, has solutions)
        -> private/build/psNN/psNN.ipynb        (master notebook)
        -> otter assign
             -> problem-sets/psNN-*/psNN.ipynb  (student, COMMITTED)
             -> private/build/psNN/dist/autograder/*.zip  (upload to Gradescope)

Otter runs the tests against the solution notebook during `assign`, so a
successful build is also a correctness check on every autograded answer.

Usage:
    python tools/build_problem_sets.py           # all
    python tools/build_problem_sets.py ps01      # one
"""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "private"
sys.path.insert(0, str(ROOT / "tools"))

from sources.common import SETUP  # noqa: E402


def _load_master(name):
    """Import a master source by path.

    Loaded by file path rather than as a package because private/sources and
    tools/sources would otherwise collide on the module name.
    """
    path = PRIVATE / "sources" / f"{name}.py"
    if not path.exists():
        sys.exit(f"master source not found: {path}")
    spec = importlib.util.spec_from_file_location(f"_master_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROBLEM_SETS = ["ps01"]

METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python",
                   "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
    "colab": {"provenance": []},
}


def md(s):
    return nbf.v4.new_markdown_cell(s)


def code(s):
    return nbf.v4.new_code_cell(s)


def otter(s):
    """An Otter config block, written as a fenced markdown cell."""
    return md("```otter\n" + s + "\n```")


def build_one(name):
    if not PRIVATE.exists():
        sys.exit(f"private/ not found. Problem-set masters are not public;\n"
                 f"they are expected at {PRIVATE / 'sources'}.")

    mod = _load_master(name)
    cells = mod.build(md, code, otter, SETUP)

    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata = METADATA
    # Guard: every cell must be a distinct object. Reusing one cell object at
    # several indices aliases them, so Otter's solution tagging silently applies
    # to all occurrences and only the first block gets stripped -- which would
    # publish answers to students.
    seen = {}
    for i, cell in enumerate(nb.cells):
        if id(cell) in seen:
            sys.exit(f"{name}: cell {i} is the same object as cell {seen[id(cell)]}. "
                     f"Build helpers must return fresh cells, not shared ones.")
        seen[id(cell)] = i
        cell["id"] = f"c{i:03d}"

    workdir = PRIVATE / "build" / name
    workdir.mkdir(parents=True, exist_ok=True)
    master = workdir / f"{name}.ipynb"
    nbf.write(nb, str(master))
    print(f"master  {master.relative_to(ROOT)}  ({len(nb.cells)} cells)")

    dist = workdir / "dist"
    if dist.exists():
        shutil.rmtree(dist)

    print(f"running otter assign (this also runs the tests against solutions)...")
    # --no-run-tests: Otter's assign-time validator evaluates tests in a
    # namespace that does not match the notebook's own (observed with otter
    # 7.0.0: a test calling a function that closes over a variable assigned in
    # a `NO PROMPT` solution cell sees that variable as Ellipsis, though the
    # same test passes when the notebook actually runs). We verify below by
    # executing the solution notebook and reading every grader.check result,
    # which is a stricter check because it uses the namespace students get.
    r = subprocess.run(["otter", "assign", "--no-run-tests", str(master), str(dist)],
                       capture_output=True, text=True, cwd=str(workdir))
    if r.returncode != 0:
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
        sys.exit(f"otter assign failed for {name}")

    student_src = dist / "student" / f"{name}.ipynb"
    dest = ROOT / mod.REL_STUDENT
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(student_src, dest)
    print(f"student {dest.relative_to(ROOT)}   [COMMITTED]")

    verify_solutions(dist / "autograder" / f"{name}.ipynb",
                     html_out=workdir / f"{name}-SOLUTIONS.html")

    zips = list((dist / "autograder").glob("*.zip"))
    for z in zips:
        print(f"gradescope bundle  {z.relative_to(ROOT)}   [upload this]")
    return True


def verify_solutions(nb_path, html_out=None):
    """Execute the solution notebook and require every grader.check to pass.

    This is the real correctness gate: it runs in the same namespace students
    will have, so a passing run means the reference answers actually satisfy
    every autograded test, visible and hidden.

    If `html_out` is given, the executed notebook is also rendered to HTML --
    solutions with their outputs, plots and printed values included. That file
    is what the reader grades free-response answers against. HTML rather than
    PDF deliberately: PDF export needs a working LaTeX toolchain, HTML needs
    nothing, and the reader opens it in a browser either way.
    """
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(nb_path, as_version=4)
    nb.cells = [c for c in nb.cells if "grader.export" not in c.source]
    client = NotebookClient(nb, timeout=900, kernel_name="python3",
                            resources={"metadata": {"path": str(nb_path.parent)}},
                            allow_errors=True)
    client.execute()

    checks, failures, errors = 0, [], []
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errors.append(f"{out.get('ename')}: {out.get('evalue')}")
        if "grader.check(" in cell.source:
            checks += 1
            text = ""
            for out in cell.get("outputs", []):
                text += str(out.get("text", ""))
                text += str(out.get("data", {}).get("text/plain", ""))
            if "All test cases passed" not in text:
                failures.append(cell.source.strip().splitlines()[-1] + " -> " + text[:400])

    if errors:
        print("\nERRORS while executing the solution notebook:")
        for e in errors[:5]:
            print("   ", e)
    if failures:
        print("\nFAILING CHECKS:")
        for f in failures:
            print("   ", f)
    if errors or failures:
        sys.exit("solution notebook did not pass its own tests")

    print(f"verified  {checks} grader.check blocks pass in the real namespace")

    if html_out is not None:
        from nbconvert import HTMLExporter
        body, _ = HTMLExporter(template_name="lab").from_notebook_node(nb)
        html_out.write_text(body)
        print(f"solutions {html_out.relative_to(ROOT)}   [for the reader; NOT public]")


if __name__ == "__main__":
    targets = sys.argv[1:] or PROBLEM_SETS
    for t in targets:
        print(f"\n=== {t} ===")
        build_one(t)
    print("\nDone. Tests passed against the solution notebook.")
