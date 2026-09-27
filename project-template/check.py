"""Run the same mechanical checks the autograder runs. Science is not checked.

    python check.py

Exit code 0 means the package passes. Anything else prints what failed.
"""
import csv
import math
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT_S = 600            # ten minutes, one CPU
README_SECTIONS = [
    "What this reproduces",
    "How to run",
    "Contents",
    "Parameters and provenance",
    "Methods note: AI use",
    "FAIR self-assessment",
]
failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL  " + msg)


def ok(msg):
    print("ok    " + msg)


# 1. README has its sections, and each has something under it.
readme = (HERE / "README.md").read_text() if (HERE / "README.md").exists() else ""
headings = [line.lstrip("#").strip() for line in readme.splitlines()
            if line.startswith("## ")]
for sec in README_SECTIONS:
    if sec not in headings:
        fail(f"README.md has no '## {sec}' section")
if "TODO" in readme:
    fail("README.md still contains TODO")
if not failures:
    ok("README.md has all six sections")

# 2. Every parameter has a value, units and a source.
n_before = len(failures)
with open(HERE / "parameters.csv", newline="") as f:
    rows = list(csv.DictReader(f))
for col in ["symbol", "value", "units", "source"]:
    if rows and col not in rows[0]:
        fail(f"parameters.csv has no '{col}' column")
for r in rows:
    try:
        float(r["value"])
    except (ValueError, TypeError):
        fail(f"parameter {r.get('symbol')!r}: value {r.get('value')!r} is not a number")
    for col in ["units", "source"]:
        if not (r.get(col) or "").strip():
            fail(f"parameter {r.get('symbol')!r} has no {col}")
if len(failures) == n_before:
    n_assumed = sum(r["source"].strip().lower() == "assumption" for r in rows)
    ok(f"parameters.csv: {len(rows)} parameters, {n_assumed} labeled assumption")

# 3. run.py runs inside the limit.
expected = [l.strip() for l in (HERE / "outputs.txt").read_text().splitlines()
            if l.strip() and not l.startswith("#")]
t0 = time.time()
try:
    r = subprocess.run([sys.executable, "run.py"], cwd=HERE, timeout=LIMIT_S,
                       capture_output=True, text=True)
    dt = time.time() - t0
    if r.returncode != 0:
        fail(f"run.py exited {r.returncode}:\n{r.stderr[-2000:]}")
    else:
        ok(f"run.py finished in {dt:.1f} s (limit {LIMIT_S} s)")
except subprocess.TimeoutExpired:
    fail(f"run.py did not finish in {LIMIT_S} s")

# 4. It made what it said it would.
# An output left over from an earlier run does not count: it must be new.
missing = [n for n in expected
           if not (HERE / "outputs" / n).exists()
           or (HERE / "outputs" / n).stat().st_mtime < t0 - 1]
for n in missing:
    fail(f"outputs/{n} is listed in outputs.txt but this run of run.py did not write it")
if expected and not missing:
    ok(f"all {len(expected)} declared outputs created")

print()
print("PASS" if not failures else f"{len(failures)} problem(s)")
sys.exit(0 if not failures else 1)
