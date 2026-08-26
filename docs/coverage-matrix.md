# Coverage Matrix

[← back to README](../README.md) · See also [Syllabus](syllabus.md) · [Course Map](course-map.md)

**Purpose.** The syllabus states: *"Nothing is assessed that was not demonstrated first."* This is the audit that keeps that promise. Every technique the course assesses appears here with the session that works it and the instrument that tests it.

**How to use it.** Before releasing any problem set, check that every problem maps to a row whose *Demonstrated* session has already happened. Before finalizing any lecture, check that its worked example actually produces the technique its row claims.

**Grading column.** `AUTO` = otter-grader can check it (returns a number, array, or function output). `HAND` = requires a human reading a derivation, plot, or argument. `MIX` = a computational part plus an interpretive part.

---

## Part I — Design Principles

| # | Technique | Demonstrated | Assessed | Grading |
|---|---|---|---|---|
| T0a | Read a specification and enumerate what must be known and built | S1 (Aug 27) | Project proposal | HAND |
| T0b | Name the four requirement classes — sense, compute, actuate, **survive** | S1 | Project, Final | HAND |
| T1 | Order-of-magnitude estimation: molecule counts from concentration and cell volume | S2 (Sep 1) | PS1 | AUTO |
| T2 | Diffusion timescale, *t* ~ *L*²/2*D* | S2 | PS1, Final | AUTO |
| T3 | Comparing process timescales (diffusion vs. transcription vs. division) | S2 | PS1 | HAND |
| T4 | Write mass-action rate laws from a reaction list | S3 (Sep 3) | PS1, Mid | HAND |
| T5 | Construct the stoichiometric matrix **S**; assemble d**X**/d*t* = **S·v** | S3 | PS1, Mid, PS7 | MIX |
| T6 | Numerical integration with `solve_ivp` | S3 | PS1 and every set after | AUTO |
| T7 | Quasi-steady-state approximation; **derive Michaelis–Menten** | S4 (Sep 8) | PS1, Mid | HAND |
| T8 | **Derive the Hill function** from cooperative equilibrium binding | S4 | PS1, Mid | HAND |
| T9 | Identify where QSSA fails — compare full vs. reduced numerically | S4 | PS1 | AUTO |
| T10 | Response time; *t*₁⁄₂ = ln2/(γ+μ) | S5 (Sep 10) | PS2, Mid | AUTO |
| T11 | Dilution vs. degradation; effect of degradation tags on circuit speed | S5 | PS2 | MIX |
| T12 | Steady-state expression level from production/removal balance | S5 | PS2 | AUTO |
| T13 | Promoter occupancy from statistical thermodynamics (partition function) | S6 (Sep 15) | PS2, Mid | HAND |
| T14 | **Derive** activator, repressor, and AND-like regulation functions | S6 | PS2, Mid | HAND |
| T15 | **Derive** the negative-autoregulation speed-up | S7 (Sep 17) | PS3, Mid | HAND |
| T16 | Positive autoregulation → graphical bistability condition | S7 | PS3 | MIX |
| T17 | Variance reduction under NAR (scaling argument) | S7 | PS3 | HAND |
| T18 | Compute and plot nullclines for a 2-D system | S8 (Sep 22) | PS3, Mid | MIX |
| T19 | Find fixed points — analytically and by numerical root-finding | S8 | PS3, PS4, Mid | AUTO |
| T20 | Jacobian, eigenvalues, linear stability classification | S8 | PS3, PS4, Mid | AUTO |
| T21 | Toggle-switch fixed points for *n* = 4 and *n* = 1 | S9 (Sep 24) | PS4, Mid | AUTO |
| T22 | Bifurcation diagram; hysteresis loop | S9 | PS4, Mid | AUTO |
| T23 | Identify a saddle-node bifurcation and say what destroys bistability | S9 | PS4 | HAND |
| T24 | FFL sign logic: coherent vs. incoherent classification | S10 (Sep 29) | PS5, Mid | HAND |
| T25 | FFL timing/delay table **with a stated delay convention** | S10 | PS5, Mid | AUTO |
| T26 | IFFL adaptation: compute pulse amplitude and adaptation error numerically | S10 | PS5 | AUTO |
| T27 | Construct the repressilator model | S11 (Oct 1) | PS5 | MIX |
| T28 | **State and apply the oscillation criterion** | S11 | PS5, Mid | HAND |
| T29 | Locate the Hopf boundary numerically by parameter sweep | S11 | PS5 | AUTO |
| T30 | Delay as a driver of oscillation | S11 | PS5 | HAND |
| T31 | Set up a chemical master equation | S12 (Oct 6) | PS6, Final | HAND |
| T32 | **Write a Gillespie SSA from scratch** | S12 | PS6, Final | AUTO |
| T33 | Compute CV and Fano factor from trajectories | S12 | PS6, Final | AUTO |
| T34 | Intrinsic vs. extrinsic noise decomposition (two-colour logic) | S12 | PS6 | HAND |
| T35 | Bursting: burst size and frequency from parameters | S12 | PS6 | AUTO |
| T36 | Transfer curve and gain, d*out*/d*in* | S13 (Oct 8) | PS6, Mid | AUTO |
| T37 | Threshold and noise-margin computation | S13 | PS6, Mid | AUTO |
| T38 | **Numeric signal matching between two measured gates** | S13 | PS6, Mid | AUTO |

## Part II — Engineering Design

| # | Technique | Demonstrated | Assessed | Grading |
|---|---|---|---|---|
| T39 | Truth table → biological circuit mapping | S16 (Oct 20) | PS6 | HAND |
| T40 | Hazard identification; complete timing table | S16 | PS6, Final | AUTO |
| T41 | Cascade delay estimation | S16 | PS6 | AUTO |
| T42 | Compose parts in code (the compositor abstraction) | S17 (Oct 22) | PS6 | AUTO |
| T43 | Quantify context dependence of a part | S17 | PS6 | HAND |
| T44 | **Golden Gate overhang and primer design** | S17 | PS6 | MIX |
| T45 | Compare gate families on orthogonality, speed, and load | S18 (Oct 27) | PS7 | MIX |
| T46 | CRISPRi repression model | S18 | PS7 | MIX |
| T47 | Recombinase state model / memory element | S18 | PS7 | HAND |
| T48 | Build and simulate a shared-resource model | S19 (Oct 29) | PS7, Final | AUTO |
| T49 | Couple burden to growth rate | S19 | PS7, Final | MIX |
| T50 | Apply bacterial growth laws | S19 | PS7 | HAND |
| T51 | Build **S** for a metabolic network | S20 (Nov 3) | PS7 | MIX |
| T52 | **Solve FBA as a linear program** (`scipy.optimize.linprog`) | S20 | PS7, Final | AUTO |
| T53 | Knockout prediction and flux coupling | S20 | PS7, Final | AUTO |
| T54 | Objective-function choice and its consequences | S20 | PS7 | HAND |
| T55 | **Derive the retroactivity term** | S21 (Nov 5) | PS8, Final | HAND |
| T56 | Quantify load effect on an upstream module | S21 | PS8, Final | AUTO |
| T57 | Insulation via timescale separation (load driver) | S21 | PS8 | MIX |
| T58 | Integral feedback → exact adaptation | S22 (Nov 10) | PS8, Final | HAND |
| T59 | Simulate an antithetic integral controller | S22 | PS8, Final | AUTO |
| T60 | Quantify disturbance rejection | S22 | PS8 | AUTO |
| T61 | Mutation–selection model; **time to circuit failure** | S23 (Nov 12) | PS8, Final | AUTO |
| T62 | Estimate fitness cost from growth data | S23 | PS8 | MIX |
| T63 | Retention time and containment requirement | S23 | PS8 | AUTO |
| T64 | Sender/receiver model construction | S24 (Nov 17) | PS9, Final | MIX |
| T65 | Band-detect / patterning analysis | S24 | PS9 | AUTO |
| T66 | Diffusion length scale in a community (reuses T2) | S24 | PS9 | AUTO |
| T67 | **Binomial genome-partitioning calculation** | S25 (Nov 19) | PS9, Final | AUTO |
| T68 | Minimal gene set reasoning | S25 | PS9 | HAND |
| T69 | **Design a multi-input classifier to a false-positive budget** | S26 (Nov 24) | PS9, Final | AUTO |
| T70 | Sensitivity/specificity trade-off reasoning | S26 | PS9 | HAND |
| T71 | Design–filter–validate arithmetic (hit rate) | S27 (Dec 1) | **Final only** | AUTO |
| T72 | Compare generative design vs. directed evolution yield | S27 | **Final only** | HAND |
| T73 | Compute *R*₀ for a therapeutic interfering particle | S28 (Dec 3) | **Final only** | AUTO |
| T74 | Why similarity-based screening fails on generated sequences | S28 | **Final only** | HAND |

---

## Gaps and decisions this exposes

### 1. The Gillespie gap — needs a decision before PS5 is written

Session 12 (noise, Gillespie) falls on **Tuesday Oct 6**. PS5 is due **Thursday Oct 8** and covers sessions 10–11. PS6 is not released until **Oct 20**, after the midterm.

So in the naive schedule, students write a Gillespie simulator on Oct 6, are examined on it Oct 15, and do not practise it on a graded set until after the exam. This is precisely the PS4/PS5 failure pattern from 2024–25, reappearing in the new calendar.

**Recommended fix:** the S12 notebook ships with a **self-checking, ungraded Gillespie exercise** — otter public tests that students run themselves, no submission. PS6 then assesses it properly (T32, T33, T35 are all AUTO, so this costs the reader nothing). The midterm scope document states explicitly that stochastic simulation is examinable *conceptually* — master equation setup, CV reasoning, when noise matters — but that a from-scratch implementation will not be required under exam conditions.

**Alternative:** move noise to session 11 and oscillators to session 12, so PS5 can cover it. This costs the clean "dynamics → digital abstraction → midterm" ramp into Part II, which is the pedagogical hinge of the whole course. I do not recommend it.

### 2. Sessions 27–28 are assessed only on the final

PS9 is due **Dec 3**; session 27 is **Dec 1** and session 28 is **Dec 3** itself. There is no way to assess them on a problem set. So PS9 covers sessions 24–26 only, and T71–T74 are final-exam-only.

This is defensible — closing sessions on frontier material and governance — but it means those four techniques get **zero formative practice**. Either accept that and weight them lightly on the final, or move one earlier. Flagged, not fixed.

### 3. PS8 spans two weeks

Out Nov 5, due Nov 19, covering sessions 21–23. This is the longest window and the heaviest conceptual load (retroactivity, control, evolutionary stability — the three sessions with no existing deck). Consider splitting into two shorter sets if authoring allows.

### 4. Grading load, computed

| | Count |
|---|---|
| AUTO techniques | 38 |
| HAND techniques | 24 |
| MIX techniques | 12 |

Roughly **half the assessed techniques are autogradable.** With 35 students × 9 sets, that is a real reduction, but the reader still handles ~24 derivation-type techniques across the term. Budget for it.

Note the asymmetry: Part I is derivation-heavy (14 HAND of 38 techniques), Part II is computation-heavy. The reader's load is front-weighted, peaking around PS2–PS3 where five of the eleven techniques are pure derivations.

---

## Audit: the 2024–25 failures, closed

These were assessed in prior years with no demonstrating lecture. Each now has one.

| Previously assessed with no lecture | Prior instrument | Now demonstrated |
|---|---|---|
| Fixed points and stability | PS4 Q4–Q5, 20 pts | **S8** (T19, T20) |
| Retroactivity / impedance | PS5 Q1, 20 pts | **S21** (T55, T56) |
| Oscillation criteria | PS4 Q6 | **S11** (T28) |
| FFL timing tables | PS4 Q1–Q3 | **S10** (T25) |
| Signal matching with numbers | PS3 Q4–Q5 | **S13** (T38) |
| Hill function derivation | PS1, PS2 | **S4** (T8) |
| Golden Gate primer design | PS1 Q13 | **S17** (T44) |

---

## What this implies for the build

**Notebooks required, in delivery order.** Sessions 3, 4, 5, 8, 9, 10, 11, 12, 13 in Part I; 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28 in Part II. Sessions 1, 2, 6, 7, 14, 15 need no notebook — S2, S6, and S7 are board work.

**Critical path.** The `posb` package must support, in this order: `solve_ivp` wrapping and **S**-matrix assembly (S3) → root-finding and Jacobian utilities (S8) → parameter sweeps (S11) → a Gillespie implementation students write themselves and then import (S12) → `linprog` wrapping for FBA (S20) → delay-differential support (S11, optional).

**Highest-risk authoring.** T55–T63 (sessions 21–23) — retroactivity, antithetic control, evolutionary stability. No existing deck, no existing notebook, no existing problem. Three sessions, twelve techniques, due Nov 5. This is the single largest block of net-new work in the course and it should be started before the semester begins, not in October.
