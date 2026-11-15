"""Recompute every keyed constant in the PS9 master from the library.

`ps-bar.md` section J rule 7: never type a key from a displayed value. On
15 November a key was typed out from NumPy's `array(0.03115402)` display and
came out as 0.031154020551492653 -- right to seven figures, invented after
that. It was 1.4e-7 from the true value, so every test passed and the review
that read the item saw nothing.

This script is the mechanical check. Run it before the build.

    PYTHONPATH="$PWD" python3 tools/checks/ps09_constants.py
"""
import math
import pathlib
import re
import sys

from posb.evolution import (time_to_failure, broken_fraction,
                            fitness_cost_from_competition,
                            fitness_cost_from_growth,
                            containment_requirement, escapers_per_dose,
                            retention_time)
from posb.communities import (sender_receiver, basu_params, band_peak,
                              band_edges, penetration_depth, diffusion_time)
from posb.populations import (diploid_packaging, infectious_fraction,
                              basic_R0, therapeutic_R0, P_min)
import posb.classifiers as cf
from scipy.optimize import brentq

TOL = 1e-3          # the set's own tolerance -- a key must sit inside it
SIGFIGS = 4


def sf(x, n=SIGFIGS):
    return float(f"%.{n}g" % x)


def truth():
    """Recompute every keyed quantity. Returns {key_literal: true_value}."""
    out = {}

    # ---- Q1-Q3, session 23 -------------------------------------------------
    s, mu = 0.02, 1.0e-4
    t50 = float(time_to_failure(0.5, s, mu))
    tgt = float(time_to_failure(0.5, s / 2, mu))
    out["T50"] = t50
    out["Q_100"] = float(broken_fraction(100.0, s, mu))
    out["GAIN_HALVE_S"] = tgt - t50
    out["GAIN_MU_OVER_100"] = float(time_to_failure(0.5, s, mu / 100)) - t50
    out["FOLD"] = float(brentq(
        lambda F: float(time_to_failure(0.5, s, mu / F)) - tgt, 1.0, 1.0e6))

    out["S_COMPETITION"] = float(fitness_cost_from_competition(
        [0, 10, 20, 30, 40, 50],
        [1.000, 0.842, 0.690, 0.588, 0.481, 0.409]))
    out["S_GROWTH"] = float(fitness_cost_from_growth(
        [0, 1, 2, 3, 4, 5, 6],
        [0.0100, 0.0320, 0.103, 0.329, 1.05, 3.37, 10.8],
        [0.0100, 0.0332, 0.110, 0.366, 1.22, 4.03, 13.4]))

    fv = 10 ** -8.6
    out["REQUIRED_FV"] = float(containment_requirement(5.0e10))
    out["ESCAPERS"] = float(escapers_per_dose(5.0e10, fv))
    out["RETENTION"] = float(retention_time(out["REQUIRED_FV"], k=3, mu1=2.0e-4))
    out["DOSE_MAX"] = 1.0 / fv

    # ---- Q4-Q6, session 24 -------------------------------------------------
    kI, gA, D, th, n_ = 0.030, 0.025, 0.010, 5.0, 2.0
    out["A_PLATE"] = kI * 4.0 / gA
    out["A_REACTOR"] = kI * 4.0 / (gA + D)
    out["OUT_PLATE"] = float(sender_receiver(
        out["A_PLATE"], 4.0, k_I=kI, gamma_A=gA, D=0.0,
        alpha=1.0, theta=th, n=n_)[1])
    out["OUT_REACTOR"] = float(sender_receiver(
        out["A_REACTOR"], 4.0, k_I=kI, gamma_A=gA, D=D,
        alpha=1.0, theta=th, n=n_)[1])
    out["S_NEEDED"] = (gA + D) * th / kI

    p = basu_params("BD2")
    p["beta_C"] = 0.020
    a_pk, g_pk = band_peak(p)
    a_lo, a_hi = band_edges(p, frac=0.5)
    out["A_PEAK"] = float(a_pk) * 1000.0
    out["G_PEAK"] = float(g_pk)
    out["A_LO"] = float(a_lo) * 1000.0
    out["A_HI"] = float(a_hi) * 1000.0
    out["WIDTH"] = out["A_HI"] / out["A_LO"]

    DA, gS = 0.0144, 0.055
    L = math.log(400.0 / 1.5)
    out["ELL_A"] = float(penetration_depth(DA, gS))
    out["X_LIT"] = out["ELL_A"] * L
    out["T_ARRIVE"] = float(diffusion_time(out["X_LIT"], DA)) / 60.0
    out["GAMMA_TARGET"] = DA / (6.0 / L) ** 2

    # ---- Q7-Q8, session 25 -------------------------------------------------
    hiv, _het, vec = diploid_packaging(6.0)
    out["P_HIV_HOM"] = float(hiv)
    out["P_VEC_HOM"] = float(vec)
    out["INFECTIOUS"] = float(infectious_fraction(6.0))
    out["VEC_SHARE_INF"] = out["P_VEC_HOM"] / out["INFECTIOUS"]

    d_, T0, nB, cC = 0.02, 800.0, 200.0, 30.0
    V0 = 8.0e4 / 1000.0
    r0 = float(basic_R0(d_ * T0 + cC * V0 / nB, cC / (nB * T0), nB, cC, d_))
    out["R0_PATIENT"] = r0
    out["R0T"] = float(therapeutic_R0(3.6, 0.25, r0))
    out["P_MIN"] = float(P_min(0.25, r0))
    n4 = 400.0
    out["P_MIN_N400_T0V0"] = float(P_min(0.25, float(basic_R0(
        d_ * T0 + cC * V0 / n4, cC / (n4 * T0), n4, cC, d_))))
    out["P_MIN_N400_LAMK"] = float(P_min(0.25, float(basic_R0(
        d_ * T0 + cC * V0 / nB, cC / (nB * T0), n4, cC, d_))))

    # ---- Q9, session 26 ----------------------------------------------------
    lines = ["DAOY", "HEK293", "HeLa", "MCF-7", "SH-SY5Y", "SKBR3", "T47D"]
    markers = ["P21", "P17-30a", "T141", "T142-3p", "T146a"]
    sense = {"P21": "high", "P17-30a": "high", "T141": "absent",
             "T142-3p": "absent", "T146a": "absent"}
    table = [[0.420, 0.429, 0.961, 0.697, 0.417],
             [0.010, 0.078, 1.106, 0.993, 1.230],
             [0.933, 0.717, 0.894, 0.849, 0.854],
             [0.931, 0.405, 0.106, 1.019, 1.033],
             [0.090, 0.242, 1.072, 0.963, 1.063],
             [0.525, 0.755, 0.544, 0.817, 0.938],
             [0.560, 0.690, 0.789, 0.994, 0.970]]
    raw = {ln: dict(zip(markers, row)) for ln, row in zip(lines, table)}
    norm = cf.normalize_responses(raw, markers)
    matrix = [[norm[ln][m] for m in markers] for ln in lines]
    levels = cf.marker_levels_from_sensor_outputs(matrix, lines, markers, sense)
    o = cf.classifier_output(levels, markers, sense)
    out["Y_POS"] = float(o["HeLa"])
    out["MARGIN"] = out["Y_POS"] / max(float(o[ln]) for ln in lines
                                       if ln != "HeLa")
    out["PHI95_ZERO"] = float(cf.fp_rate_upper_bound(0, 6))
    return out


# What the master actually keys. Each entry is the literal as it appears in a
# hidden test, paired with the name of the quantity it is meant to be.
KEYED = {
    "T50": "264.1", "Q_100": "0.03115",
    "GAIN_HALVE_S": "193.8", "GAIN_MU_OVER_100": "231.1", "FOLD": "47.50",
    "S_COMPETITION": "0.01803", "S_GROWTH": "0.03022",
    "REQUIRED_FV": "2.0e-11", "ESCAPERS": "125.6",
    "RETENTION": "1.357", "DOSE_MAX": "3.981e8",
    "A_PLATE": "4.8", "A_REACTOR": "3.429",
    "OUT_PLATE": "0.4796", "OUT_REACTOR": "0.3198", "S_NEEDED": "5.833",
    "A_PEAK": "5.405", "G_PEAK": "11.10",
    "A_LO": "3.827", "A_HI": "8.364", "WIDTH": "2.186",
    "ELL_A": "0.5117", "X_LIT": "2.858", "T_ARRIVE": "4.728",
    "GAMMA_TARGET": "0.01248",
    "P_HIV_HOM": "0.02041", "P_VEC_HOM": "0.7347",
    "INFECTIOUS": "0.7551", "VEC_SHARE_INF": "0.9730",
    "R0_PATIENT": "1.75", "R0T": "1.389", "P_MIN": "3.055",
    "P_MIN_N400_T0V0": "3.830", "P_MIN_N400_LAMK": "2.366",
    "Y_POS": "0.4441", "MARGIN": "1.475", "PHI95_ZERO": "0.3930",
}


def main():
    src = pathlib.Path("private/sources/ps09.py").read_text()
    true = truth()
    bad = []

    for name, lit in sorted(KEYED.items()):
        want = true[name]
        got = float(lit)
        if abs(got - want) / abs(want) >= TOL:
            bad.append(f"{name}: key {lit} is {abs(got-want)/abs(want):.2e} "
                       f"from the computed {want!r} -- OUTSIDE the set's own "
                       f"tolerance of {TOL}")
            continue
        if lit not in src:
            bad.append(f"{name}: key {lit} is not present in the master")
            continue
        # The key must be the 4-significant-figure rounding, or the exact
        # value. "Exact" allows float noise in the LIBRARY's own arithmetic:
        # R0_PATIENT is exactly 1.9375 by closed form, and basic_R0 returns
        # 1.9375000000000002.
        if got != sf(want) and abs(got - want) > 1e-12 * abs(want):
            bad.append(f"{name}: key {lit} is neither the {SIGFIGS}-figure "
                       f"rounding ({sf(want)!r}) nor the exact value "
                       f"({want!r})")

    # Any long float literal in the BUILD BODY that is not an accounted key.
    # The module docstring is excluded: it narrates the 15 November
    # fabrication incident and quotes the bad value on purpose.
    body = src[src.index("def build("):]
    longs = set(re.findall(r"(?<![\w.])(\d+\.\d{6,})(?![\w])", body))
    allowed = {"0.666667", "0.833333"}        # exact rationals written out
    stray = longs - allowed
    if stray:
        bad.append(f"unaccounted literals with 6+ decimals (section J rule 2 "
                   f"wants 4 significant figures): {sorted(stray)}")

    for line in bad:
        print("  FAIL  " + line)
    print(f"\n{len(KEYED)} keys checked against a live recomputation; "
          f"{len(bad)} problem(s).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
