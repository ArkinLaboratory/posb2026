# Session 9 — Bistability and the toggle switch

[← all sessions](../README.md) · **Thursday, September 24, 2026**

> **Re-cut 18 September.** The first build repeated everything session 8 now
> derives — nullclines, fixed points, the Jacobian, *a*<sub>c</sub>, the scaling,
> the wedge. What is left is the thing Tuesday cannot do: turn one knob on the
> device that was built and watch a stable state die.

## The one thing to remember

> **A threshold is a saddle-node. Memory is a state that outlives its signal.**

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | Nullcline; the saddle test; when QSSA fails |
| 5–8 | Goals as questions | Why 40 µM, all at once, and no way back; what you can change; why it fails at 40 h |
| 8–12 | Why memory | Combinational vs sequential; λ did it first |
| 12–16 | The artifact | Fig. 1, Fig. 3; GFP sits with cI, so *high* is cI on |
| 16–26 | **Argue**, groups | Where in the parts is the cooperativity; what the six RBS variants were searching for; what breaks it |
| 26–32 | Sorted | Mutual repression · cooperativity on at least one arm · inside the wedge · slow removal |
| 32–35 | Tuesday in three lines | Box 1; crossings; g₁g₂ > 1; the wedge. Nothing new is needed |
| 35–45 | **Run**, five steps, picture | IPTG stretches one nullcline; low state and saddle annihilate at s<sub>c</sub> = 5.4 = **39 µM**; no way back |
| 45–48 | Fig. 5a beside ours | The data jump at 40 µM. Points 3a/3b: bimodality near the fold |
| 48–55 | Engineerability | α easy, removal moderate, cooperativity hard, symmetry fragile |
| 55–60 | **ConcepTest** | Switch faster? *(B — tags; removal sets the time)* |
| 60–65 | Bistable ≠ useful | Fig. 4 (22 h), Fig. 6 (3–4 h to begin and done by 6 going up; 35 min down) |
| 65–77 | **Faded set**, two halves | [Four problems](../../handouts/s09-faded-toggle.md): n = 4 and n = 1 at α = 2; item 4 is the saddle-node by construction |
| 77–80 | It fails | pTog at 2/31/40 h — ⚠ provenance still open |
| 80 | Window, and next | Session 23 preview; session 11 is the other exit from the τ–Δ plane |

## The result this session exists to produce

pTAK117 with the Fig. 5 IPTG term, *u* → *u*/(1 + [IPTG]/K)<sup>η</sup> in d*v*/d*t*
only. Raising IPTG stretches the *v*-nullcline; the *u*-nullcline does not move.
The low state (LacI on) and the saddle meet and annihilate at

**s<sub>c</sub> = 5.41, i.e. [IPTG]<sub>c</sub> = 39 µM** (K = 2.9618 × 10⁻⁵ M, η = 2.0015, from the legend)

which is where the red circles in Fig. 5a jump. Remove the IPTG and the high
state still exists, so the cell stays: hysteresis, and the reason the device
needs two inducers. `figures/s09_bistability.py::iptg_threshold` computes it by
bisection on the number of fixed points; `fig_hysteresis` is Fig. 5a's
theoretical curve recomputed.

## Coverage

T21 (faded set: n = 4, n = 1), T22 (the bifurcation diagram, hysteresis),
T23 (the saddle-node; what destroys bistability — the failure surface and
the faded set's item 4).

## Built

| | |
|---|---|
| Figures | `s09_fold_p1..p4`, `s09_hysteresis`, plus the retained `s09_separatrix`, `s09_nullclines`, `s09_bifurcation` at legible sizes |
| Handout | [s09-faded-toggle](../../handouts/s09-faded-toggle.md) + [answers](../../handouts/s09-faded-toggle-answers.md) |
| Board notes | [s09-board-notes](../../board-notes/s09-board-notes.md) |

## Forward pointer, added 26 September

This session assumes cooperativity — *n* > 1 on at least one arm — and the
engineerability row calls it hard. Where a real *n* comes from is **session 18**,
where sharpness gets built rather than assumed: zero-order ultrasensitivity,
multi-step, and a toggle whose parts are phosphorylation sites instead of
promoters (Mishra et al., *Science* 2021, now `preview_in: [s09]` in
`readings.yaml`). Nine sessions is a long wait for an answer to a question this
session raises, and the gap is deliberate — Part I has no room for the
derivation — so both ends say so out loud rather than leaving it a hole.

## Open

- **Provenance of the 40-hour pTog panels** (`toggle_longevity_2025deck`). Not
  Gardner 2000. Only Adam or Ron Weiss can close this; the deck prints an
  ATTRIBUTION NEEDED tag until it is.
- Badges are placeholders; the run sheet is Adam's.
