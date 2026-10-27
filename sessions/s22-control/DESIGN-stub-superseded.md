# Session 22 — Robustness and control: rejecting the disturbance instead of modelling it

**Tuesday 10 November 2026.** Part II, seventh session. Required reading: Aoki,
Lillacci, Gupta, Baumschlager, Schweingruber & Khammash, *Nature* 570 533–537
(2019) — **held** as of 26 October (ETH Research Collection, published version;
author list verified off page 1).

**Status: DESIGN STUB, written 26 October ahead of its build week.** It exists
now because **PS8 posts 5 November and assesses this session**, and without the
three moves below PS8's control questions would be written against a guess.
The deck is not this week's work.

---

## 1 · Why this is rung 4, and what that means for its shape

Rungs 1–3 (see `sessions/s20-metabolic/DESIGN.md` §1) each found a coupling and
dealt with it on its own terms: measure the burden, compute the fluxes, insulate
the interface. **Each cure is specific to its disturbance.** Session 22's claim
is that you can stop doing that:

> **An integrator does not need to know what the disturbance is.**

That is the arc's turn from diagnosis-and-patch to structural guarantee, and it
is why this session comes after three sessions of patches rather than before
them. The room should feel it as a release.

## 2 · The three moves

1. **Integral feedback gives exact adaptation.** If the controller integrates
   the error, the only steady state is zero error — independent of the plant's
   parameters. Derived, not asserted.
2. **Two molecules that annihilate each other are an integrator.** Aoki's
   antithetic motif: Z₁ produced at a constant reference rate, Z₂ produced in
   proportion to the output, Z₁ + Z₂ → ∅. Then d(Z₁ − Z₂)/dt depends only on the
   reference and the output, so the output is pinned by the *ratio of two rate
   constants* and by nothing else in the circuit. **That one sentence is the
   session** — `readings.yaml` says so and it is right.
3. **Dilution breaks it, and that is the argument.** The integrator is exact only
   if Z₁ and Z₂ are lost *only* by annihilation. In a growing cell they dilute,
   the integrator leaks, and adaptation stops being perfect. `readings.yaml`'s
   focus note sets this up explicitly: *"ask what dilution does to it — that is
   the session's argument."* **This is also the session's link back to S19**,
   where growth rate was the thing the circuit changed; here growth rate is the
   thing that degrades the circuit's guarantee.

## 3 · What PS8 can assess, which is the reason this stub exists

The three techniques assigned to this session are integral feedback → exact
adaptation (HAND), simulating an antithetic controller (AUTO), and quantifying
disturbance rejection (AUTO). All three are writable against §2 as it stands:

- the derivation that zero error is the only fixed point;
- a simulation of the antithetic motif under a step disturbance, with and
  without dilution of the controller species;
- a disturbance-rejection number — the ratio of output deviation with and
  without the controller — which is also the quantity that degrades as the
  dilution rate rises.

**The leak is the item that ties PS8 together**, because it is the only question
on the set where the host's economy (rung 1) and the controller (rung 4) appear
in the same calculation.

## 4 · Open for the build week

- Whether the derivation is done on a general plant or on a specific one the
  room already owns. A circuit from Part I would make it concrete and would
  carry the arc better than an abstract plant.
- The Aoki student copy: the held PDF is 22 pages (ETH cover, the Letter at
  pp. 2–6, Methods pp. 7–9, SI after). `readings.yaml` records `pages: 5`, which
  is true of the Letter only — so the student copy is pp. 2–6 and the full file
  is the instructor copy, unless Adam wants the whole thing handed out.
- `posb` support for the antithetic model and the leaky integrator.
