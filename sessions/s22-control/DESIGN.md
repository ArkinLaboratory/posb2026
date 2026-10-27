# Session 22 — Robustness and control: rejecting the disturbance instead of modelling it

**Tuesday 10 November 2026.** Part II, seventh session. **PS8 is out and
assesses this session.** Required reading: Aoki, Lillacci, Gupta, Baumschlager,
Schweingruber & Khammash, *Nature* 570 533–537 (2019). PDF held.

**Status: DESIGNED, 26 October 2026.** Supersedes the 26 October stub, kept at
`DESIGN-stub-superseded.md`. Every quotation below was read off the held PDF.
The two questions the stub left open are both answered in §5.

---

## 1 · Why this is rung 4, and what that means for its shape

Rungs 1–3 each found a coupling and dealt with it on its own terms: measure the
burden (19), compute the fluxes (20), insulate the interface (21). **Each cure
is specific to its disturbance.** This session says you can stop doing that:

> **An integrator does not need to know what the disturbance is.**

That is the arc's turn from diagnosis-and-patch to structural guarantee, and it
is why this session comes after three sessions of patches. The room should feel
it as a release.

## 2 · The sentence the hour is built on, in the authors' words

> *"In this scheme, **as long as the closed dynamics are stable**, the
> steady-state value of the output is determined solely by the ratio μ/θ.
> Notably, it does not depend on the topology and parameters of the circuit
> of interest, which are usually uncertain and noisy, nor on any constant
> external perturbations that afflict the network."*
> — Aoki et al., Nature 570:533 (2019), p. 533

The stability clause is part of the sentence and was cut from every file that
quoted it until 27 October. "The controlled network" was our paraphrase
presented inside quotation marks.

Everything else is commentary. Two rate constants set the output; the circuit
being controlled does not get a vote.

## 3 · The four moves

**1. Integral feedback gives exact adaptation — derived, not asserted.**
If a controller integrates the error, the only steady state is zero error. Do
it on a *general* plant, because the generality is the result (see §5.1), then
instantiate it on session 5's object, dX/dt = k − γX, so it is concrete.

**2. Two molecules that annihilate each other are an integrator.** Z₁ made at a
constant reference rate μ, Z₂ made in proportion to the output at rate θ, and
Z₁ + Z₂ → ∅. Subtract the two equations and d(Z₁ − Z₂)/dt = μ − θX: the
annihilation rate cancels, so what is left integrates the error. The output is
pinned by μ/θ and by nothing else.

**3. THE ANNIHILATION IS SEQUESTRATION, AND THAT IS THE ARC CLOSING.** Aoki
implement Z₁ + Z₂ → ∅ with a σ factor and its anti-σ factor from *B. subtilis*
— **SigW and RsiW** — and the paper describes the mechanism in the course's own
word: *"In its natural context, RsiW stably sequesters and holds SigW
inactive."*

Session 18 named sequestration. Session 19 found it in the ribosome pool,
session 21 in the downstream operator, and the ladder's invariant has been
*a molecule held by something that is not its target is not available to do its
job*. **Here that unavailability is the mechanism of the cure.** The same
physics that was the problem on rungs 1–3 is what makes rung 4 work. This is
the single best beat in Part II and the stub did not have it.

**4. Dilution breaks it, and that is the argument.** The integrator is exact
only if Z₁ and Z₂ are lost *only* by annihilation. The paper says so itself:
the ideal analysis assumed *"negligible degradation of controller proteins Z₁
and Z₂,"* and *"in living cells, these assumptions are not satisfied because
all genes have a limited production capacity and, in the case of fast-growing
cells, dilution."*

In a growing cell they dilute, the integrator leaks, and adaptation stops being
perfect. **This is the link back to rung 1**: in session 19 the growth rate was
the thing the circuit changed; here it is the thing that degrades the circuit's
guarantee.

## 4 · What they actually built, and the measurement that settles it

Not GFP. **Growth rate**, in *E. coli* — which is session 19's variable, and
closes the arc on the same quantity it opened on.

- `sfgfp` is replaced by **metE**, the last step of cobalamin-independent
  methionine biosynthesis, in a **ΔmetE** host grown in methionine-free medium.
  So the cell's growth rate is the controlled output.
- The **open-loop** control is the same circuit with the anti-σ module
  (P_BAD–rsiW) deleted. One module out, feedback gone, everything else
  identical. That is the right control and it is worth saying why.
- **The perturbation is temperature**: 37 °C against 30 °C, growth rates
  normalised to each circuit's own 37 °C rate, n = 3, two-tailed unpaired
  unequal-variance t-test.

**The result, Fig. 3d:**

| circuit | P |
|---|---|
| closed loop | **0.2261** |
| open loop | **7.769 × 10⁻⁵** |

The controlled strain's growth rate is statistically indistinguishable across a
seven-degree temperature change; the uncontrolled one is not, by three and a
half orders of
magnitude.

**Teach this as a pair of p-values, and teach what a large P does and does not
mean.** P = 0.2261 is a failure to detect a difference, not proof of its
absence — and that is exactly the distinction PS8 Q3d(ii) asks about with
Mishra's n = 3, on the same set. The two should be said in the same
words.

## 5 · The stub's two open questions, answered

**5.1 — General plant or a specific one?** **Both, in that order.** The
universality is the result, not a framing: Box 1 proves that *every* controller
achieving robust perfect adaptation must embed an antithetic motif. Deriving on
a specific plant would throw that away. So: derive on an arbitrary plant, land
μ/θ, and *then* instantiate on dX/dt = k − γX so the room can see it move.
PS8 Q4 is written against the general form.

**5.2 — The Aoki student copy.** The held PDF is 22 pages: ETH cover p. 1, the
Letter pp. 2–6, Methods pp. 7–9, SI after. `readings.yaml` records `pages: 5`,
which is the Letter and is the right assignment. The focus note should send
them to **Fig. 1c** (the motif), **Fig. 3a–b** (closed and open loop) and
**Fig. 3d** (the temperature result) — and should say the controller regulates
*growth rate*, because that is what makes it land after session 19.

## 6 · Segments

1. **frame** — three patches, each tailored. What would it take to stop?
2. **build** — integral feedback on a general plant; zero error is the only
   fixed point. Board.
3. **release** — instantiate on k − γX: where does the output sit, and which
   parameters is it allowed to depend on?
4. **debrief** — μ/θ, and nothing else. The plant does not get a vote.
5. **build** — the antithetic motif; subtract the two equations.
6. **debrief** — the annihilation is sequestration (§3.3). Collect the ladder.
7. **build** — Aoki's circuit: SigW/RsiW, metE, ΔmetE, and the open-loop
   control that deletes one module.
8. **release** — the two p-values. What does P = 0.2261 license you to say?
9. **debrief** — robustness measured, and what a large P is not.
10. **build** — dilution. The integrator leaks, and rung 1 is why.
11. **close** — the design ledger, and what Part II has been about.

## 7 · What is still needed for the build

- `posb/control.py`: the antithetic model, the step-disturbance simulation, the
  adaptation error against dilution rate. PS8 Q4 has students write the ODEs
  themselves, so the module is for the figures, not for them.
- Figures: the motif; closed vs open loop under a step; adaptation error
  against δ; a redraw of Fig. 3d as two normalised distributions with their
  p-values.
- `NUMBERS.md` with every value and its KIND, before any slide is built.
- Handout (home guide + answers), board notes.
- **Cross-deck vocabulary grep before building.** "integral feedback",
  "antithetic", "set point", "adaptation", "sigma factor", "anti-sigma" — none
  of these has been used in sessions 1–21 and the grep must say so explicitly.
- The PS8 contract: Q4 and Q5 are released on 5 November against §3 and §5.1.
  **This design may not move under them.** Anything learned in the build that
  contradicts §3 has to be reconciled with a set already in students' hands.
