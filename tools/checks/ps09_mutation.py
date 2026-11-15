"""Perturb every keyed variable and confirm some test catches it.

A test that passes against the solution and ALSO passes against a wrong answer
grades nothing. This perturbs each keyed variable by 1% -- ten times the set's
own rel 1e-3 tolerance -- and reports any that no test notices.

PHI_CELL is expected to be undetected: Q9(d) says the hidden tests check the
student's arithmetic against whatever they set, never against a value of ours.
It is the student's own defended choice and is marked in Q10b, by hand.

    PYTHONPATH="$PWD" python3 tools/checks/ps09_mutation.py
"""
import importlib.util
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path("tools").resolve()))
from sources.common import SETUP, grad                      # noqa: E402
import nbformat as nbf                                      # noqa: E402

# The variables a STUDENT sets. Stem constants (K_I, T_0, D_A ...) are given
# data, not answers, so perturbing them tests nothing.
ANSWERS = [
    "T50", "Q_100", "GAIN_HALVE_S", "GAIN_MU_OVER_100", "FOLD",
    "S_COMPETITION", "S_GROWTH",
    "REQUIRED_FV", "ESCAPERS", "RETENTION", "DOSE_MAX",
    "A_PLATE", "A_REACTOR", "OUT_PLATE", "OUT_REACTOR", "S_NEEDED",
    "A_PEAK", "G_PEAK", "A_LO", "A_HI", "WIDTH",
    "ELL_A", "X_LIT", "T_ARRIVE", "GAMMA_TARGET",
    "P_HIV_HOM", "P_VEC_HOM", "INFECTIOUS", "VEC_SHARE_INF",
    "R0_PATIENT", "R0T", "P_MIN", "P_MIN_N400_T0V0", "P_MIN_N400_LAMK",
    "Y_POS", "MARGIN", "CUT_ZERO_FP", "PHI95_ZERO",
    "N_DOSE", "PHI_CELL", "N_WRONG", "N_WRONG_BOUND",
]

# Nothing should be ungraded. PHI_CELL is never checked against a value of
# OURS -- Q9(d) promises that -- but its product anchor binds it to the
# student's own N_WRONG, so a perturbation of it is still caught.
EXPECTED_UNGRADED = set()


def main():
    spec = importlib.util.spec_from_file_location(
        "ps09", "private/sources/ps09.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cells = m.build(lambda t: nbf.v4.new_markdown_cell(t),
                    lambda t: nbf.v4.new_code_cell(t),
                    lambda t: nbf.v4.new_raw_cell(t), SETUP, grad)

    base, tests = {}, []
    exec("import numpy as np\nimport matplotlib\nmatplotlib.use('Agg')\n"
         "import matplotlib.pyplot as plt\nimport posb\n", base)
    for c in cells:
        if c["cell_type"] != "code":
            continue
        src = c["source"]
        if src.lstrip().startswith("# ---"):
            continue
        if src.startswith('"""'):
            tests.append((re.search(r"name: (\S+)", src).group(1),
                          src.split('""" # END TEST CONFIG\n', 1)[1]))
        else:
            exec(src.replace("# BEGIN SOLUTION\n", "")
                    .replace("# END SOLUTION\n", ""), base)

    keys = [k for k in ANSWERS if isinstance(base.get(k), float)]
    absent = [k for k in ANSWERS if k not in base]
    if absent:
        print(f"  FAIL  these answer variables are never bound by the "
              f"solutions: {absent}")
        return 1

    undetected = []
    for k in keys:
        ns = dict(base)
        ns[k] = float(base[k]) * 1.01
        caught = 0
        for _n, body in tests:
            try:
                exec(body, dict(ns))
            except Exception:
                caught += 1
        if caught == 0:
            undetected.append(k)
        print(f"  {k:<20} +1%  ->  {caught} test(s)"
              + ("   UNDETECTED" if caught == 0 else ""))

    surprises = set(undetected) - EXPECTED_UNGRADED
    missing = EXPECTED_UNGRADED - set(undetected)
    print(f"\n{len(keys) - len(undetected)}/{len(keys)} keyed variables graded")
    if surprises:
        print(f"  FAIL  ungraded and not expected to be: {sorted(surprises)}")
    if missing:
        print(f"  NOTE  now graded though listed as expected-ungraded: "
              f"{sorted(missing)} -- update EXPECTED_UNGRADED")
    return 1 if surprises else 0


if __name__ == "__main__":
    sys.exit(main())
