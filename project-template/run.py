"""Regenerate every figure and number in the proposal into outputs/.

Worked example: how much faster does an LAA-tagged reporter reach steady state
than an untagged one?  dx/dt = alpha - (mu + k_deg) x, with mu = ln2 / t_double
and k_deg = ln2 / t_half. Response time t_1/2 = ln2 / (mu + k_deg).

Replace the model; keep the shape: read parameters.csv, compute, write outputs/.
"""
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")          # no display in the autograder
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def load_parameters(path=HERE / "parameters.csv"):
    """The numbers in the table are the numbers in the model."""
    with open(path, newline="") as f:
        return {row["symbol"]: float(row["value"]) for row in csv.DictReader(f)}


def removal_rate(p, t_half):
    mu = np.log(2) / p["t_double"]
    k_deg = np.log(2) / t_half          # ln2 / inf is 0.0: untagged
    return mu + k_deg


def main():
    OUT.mkdir(exist_ok=True)
    p = load_parameters()
    t = np.linspace(0, 150, 301)
    numbers = {}
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for label, key in [("untagged", "t_half_none"), ("LAA tag", "t_half_LAA")]:
        gamma = removal_rate(p, p[key])
        x_ss = p["alpha"] / gamma
        numbers[label] = {"x_ss_nM": round(x_ss, 3),
                          "t_response_min": round(np.log(2) / gamma, 3)}
        ax.plot(t, 1 - np.exp(-gamma * t), label=label)
    numbers["speedup"] = round(numbers["untagged"]["t_response_min"]
                               / numbers["LAA tag"]["t_response_min"], 3)
    ax.axhline(0.5, color="0.6", lw=0.8, ls="--")
    ax.set_xlabel("time after induction (min)")
    ax.set_ylabel("x / x_ss")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "response.png", dpi=150)
    (OUT / "numbers.json").write_text(json.dumps(numbers, indent=2) + "\n")
    print(json.dumps(numbers, indent=2))


if __name__ == "__main__":
    main()
