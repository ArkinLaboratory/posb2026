# Session 22 — every number, with its kind

**Settled 26 October 2026**, before any slide was built. Everything below comes
out of `posb/control.py` at its default `ControlParams`, or off the held Aoki
PDF. Nothing here is fitted and nothing is quoted from a slide.

**KIND** is one of **DERIVED** (algebra, exact), **COMPUTED** (integration of
our own model), or **MEASURED** (Aoki's experiment).

Reference circuit, which is also PS8 Q4's: μ = 10, θ = 2, k = 1, γ = 0.5,
η = 50, δ = 0 unless stated.

---

## 1 · The set point — DERIVED, and exact

At δ = 0, subtracting the Z₂ equation from the Z₁ equation cancels the
annihilation term:

    d(Z1 - Z2)/dt = mu - theta*X

so a steady state forces **X = μ/θ = 5**. k, γ and η do not appear.

## 2 · The plant does not get a vote — COMPUTED

The claim being checked is Aoki's: *"it does not depend on the topology and
parameters of the controlled network."* Integrating from rest:

| variation | closed-loop X_ss |
|---|---|
| reference | 5.0000000000 |
| plant gain k: 1 → 4 | 5.0000000000 |
| removal γ: 0.5 → 0.1 | 5.0000000000 |
| annihilation η: 50 → 500 | 5.0000000000 |
| all three at once | 5.0000000000 |

**This is the demonstration the hour turns on**, and it is worth doing live:
change a plant parameter on the slide and the answer does not move.

## 3 · Disturbance rejection — COMPUTED

| d | closed loop | open loop |
|---|---|---|
| 0.0 | 5.0000000000 | 5.0 |
| 0.5 | 5.0000000000 | 6.0 |
| 1.0 | 5.0000000000 | 7.0 |
| 2.0 | 5.0000000000 | 9.0 |

The open loop moves one-for-one with d/γ. The closed loop does not move at
all, so the rejection ratio is **infinite** in the ideal case — which is why
the figure plots it against the dilution rate rather than quoting a number.

## 4 · The actuator bound — DERIVED, then CONFIRMED

The controller acts only through Z₁ ≥ 0, so a steady state needs
k·Z₁ = γX − d ≥ 0, giving

    d <= gamma * mu / theta = 2.5

| d | settles? | X at t = 8000 |
|---|---|---|
| 2.0 | yes | 5.0000 |
| 2.4 | yes | 5.0000 |
| 2.6 | **no** | 5.2001 |
| 5.0 | **no** | 10.0000 |

**Past the bound there is no steady state at all** — not a saturated one. Z₁
falls to zero, the annihilation that was removing Z₂ stops, Z₂ grows without
bound, and X drifts toward d/γ. The d = 2.6 row is the one to show: it looks
converged at 5.2 and is not, which is why `settles` compares two horizons
instead of trusting one.

**This is a different failure from the leak in §5** and the deck must not
blur them: saturation is the controller running out of authority; dilution is
the integrator leaking.

## 5 · Dilution makes the integrator leak — DERIVED, then COMPUTED

At δ > 0 the subtraction leaves μ − θX = δ(Z₁ − Z₂), so

    error = (delta/theta) * (Z1 - Z2)

which is **first order in δ**. At d = 2:

| δ | error | error/δ |
|---|---|---|
| 0 | 0.00000000 | — |
| 0.001 | −0.00004999 | −0.04999 |
| 0.005 | −0.00024969 | −0.04994 |
| 0.01 | −0.00049876 | −0.04988 |
| 0.05 | −0.00246938 | −0.04939 |
| 0.1 | −0.00487992 | −0.04880 |

Fitted slope of log|error| against log δ over δ ∈ {0.0025 … 0.02}:
**0.997939**, i.e. exactly first order. This is PS8 Q5.

The error is **negative**: the leak makes the output undershoot its set point.

## 6 · Aoki's experiment — MEASURED

All read off the held PDF.

- **The annihilation is SigW / RsiW**, a σ and anti-σ pair from *B. subtilis*.
  The paper's own description of the mechanism: *"In its natural context, RsiW
  stably sequesters and holds SigW inactive."*
- **The controlled output is growth rate.** `sfgfp` replaced by **metE** — the
  last step of cobalamin-independent methionine biosynthesis — in a **ΔmetE**
  host in methionine-free medium.
- **The open-loop control deletes one module**, the anti-σ (P_BAD–rsiW).
  Everything else is identical.
- **The perturbation is temperature**, 37 °C against 30 °C, growth rates
  normalised to each circuit's own 37 °C rate, **n = 3**, two-tailed unpaired
  unequal-variance t-test (Fig. 3d).

| circuit | P |
|---|---|
| closed loop | **0.2261** |
| open loop | **7.769 × 10⁻⁵** |

**Teach the pair, and teach what the large P does not mean.** P = 0.2261 is a
failure to detect a difference at n = 3, not a demonstration that there is
none. PS8 Q3d(ii) asks exactly this about Mishra's n = 3 eight days earlier,
and the two should be said in the same words.

- The ideal analysis assumed *"negligible degradation of controller proteins Z₁
  and Z₂"*, and the paper says that in living cells this fails *"in the case of
  fast-growing cells, dilution"* — which is §5, in their words, and the link
  back to session 19.

## 7 · What is NOT claimed

- No number here is a fit to Aoki's data. Our circuit is a teaching model with
  invented parameters; their measurements are quoted as theirs and never mixed
  with ours. The session-21 failure — a number from one model quoted under
  another — is the one to avoid, and the KIND column is how.
- The rejection ratio in §3 is infinite only because our ideal model has no
  leak. Any real circuit has δ > 0, so the honest statement is §5, not §3.
