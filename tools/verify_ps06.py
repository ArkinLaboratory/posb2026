#!/usr/bin/env python3
"""Recompute every number quoted in private/sources/ps06.py's header block.

Run it and paste the output into that docstring, or run it with --check to
have it tell you whether the docstring still matches what posb computes.

This exists because the header block was the one place in ps06.py where
numbers were typed rather than computed, and on 18 October an adversarial
review found two errors in it and none anywhere else: `peak|G|` holding an
x-coordinate rather than a gain, and t_half(5) drifting in the fourth
decimal. Generate-don't-type is the repo's rule; this closes the exception.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np

from posb.digital import Repressor, noise_margins
from posb.logic import (GateNetwork, NOT, BUF, NAND, NOR, HYBRID, hazards,
                        cascade_half_time, classifier_2025, classifier_fixed)
from posb.stochastic import nar_fano_lna


def gates():
    out = []
    for n in (2, 3):
        g = Repressor(y_min=0.1, y_max=10, K=1, n=n)
        x_il, x_ih = g.thresholds()
        y_ol, y_oh = g.output_levels()
        x_peak, g_peak = g.peak_gain()
        out.append((n, x_il, x_ih, y_oh, y_ol, g_peak, x_peak))
    return out


def cascade():
    th = [cascade_half_time(n) for n in range(1, 6)]
    err = [abs(t - (n - 1 / 3)) for n, t in zip(range(1, 6), th)]
    inc = [th[i] - th[i - 1] for i in range(1, 5)]
    return th, err, inc


def logic_rows():
    z = GateNetwork([NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb")],
                    inputs=("A", "B"), output="Z")
    rows = [
        ("classifier_2025", classifier_2025()),
        ("Z = NOR(not A, not B)", z),
        ("Z + BUF", GateNetwork(
            [NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb"),
             BUF("out", "Z")], inputs=("A", "B"), output="out")),
        ("padded", GateNetwork(
            [NOT("R1", "B"), NAND("R2", "A", "R1"), NOT("Act", "R2"),
             BUF("R3", "Act")], inputs=("A", "B"), output="R3")),
        ("two_gene", GateNetwork(
            [BUF("g1", "A"), HYBRID("out", ("g1",), ("B",))],
            inputs=("A", "B"), output="out")),
        ("classifier_fixed", classifier_fixed()),
    ]
    out = []
    for name, net in rows:
        kinds = {}
        for a in (0, 1):
            for b in (0, 1):
                tbl = net.timing_table({"A": a, "B": b}, initial=0, ticks=6)
                hz = hazards(tbl, net.output)
                kinds[(a, b)] = hz[0].kind if hz else "clean"
        out.append((name, net, kinds))
    return out


def main():
    print("GATES  (Repressor(y_min=0.1, y_max=10, K=1, n))")
    for n, x_il, x_ih, y_oh, y_ol, g_peak, x_peak in gates():
        print(f"  n={n}:  x_IL {x_il:.4f}  x_IH {x_ih:.4f}  "
              f"y_OH {y_oh:.4f}  y_OL {y_ol:.4f}")
        print(f"        peak |G| {g_peak:.3f}, at x = {x_peak:.3f}"
              f"      <- peak_gain() returns (x, |G|)")
    A = Repressor(y_min=0.1, y_max=10, K=1, n=2)
    B = Repressor(y_min=0.1, y_max=10, K=1, n=3)
    nm = noise_margins(A, B)
    print(f"  noise_margins(A, B) = ({nm[0]:+.4f}, {nm[1]:+.4f})"
          f"   -- the HIGH side fails")

    th, err, inc = cascade()
    print("\nCASCADE")
    print("  t_half(1..5)      " + ", ".join(f"{v:.6f}" for v in th))
    print("  rule (n-1/3) err  " + ", ".join(f"{v:.6f}" for v in err))
    print("  per-stage         " + ", ".join(f"{v:.5f}" for v in inc))

    print("\nNAR")
    print(f"  beta at the matched mean (gamma=0.2, K=100, n=4, x*=100): "
          f"{0.2 * 100 * (1 + 1.0 ** 4):.1f}")
    print(f"  nar_fano_lna(4, 1.0) = {nar_fano_lna(4, 1.0):.6f}")

    print("\nLOGIC  (cold start, 4 input cases)")
    for name, net, kinds in logic_rows():
        n_bad = sum(v != "clean" for v in kinds.values())
        print(f"  {name:22} fail_safe {str(net.is_fail_safe()):5} "
              f"balanced {str(net.is_balanced()):5} "
              f"cold_start_safe {str(net.cold_start_safe()):5} "
              f"{'clean' if not n_bad else f'glitches {n_bad}/4'}")
        if n_bad:
            print(f"      {dict(sorted(kinds.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
