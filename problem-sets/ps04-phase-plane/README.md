# PS4 — The Phase Plane, Bistability, and the Toggle Switch

[← all problem sets](../README.md) · **Out Sep 24 · Due Oct 1** · 42 points (BioE 247: 48)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps04-phase-plane/ps04.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps04-phase-plane/ps04.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Two sessions, one object. Session 8 drew the phase plane and found where a
two-gene circuit can sit still and whether it stays there; session 9 turned one
knob on the device Gardner built and watched a state die.

Two of these questions are the items the session 8 handout said would be here.
They are the same items.

| | |
|---|---|
| **Q1** | Nullclines, the diagonal root by `brentq`, every crossing by `fixed_points` — and why the drawing comes first. |
| **Q2** | The Jacobian, analytically, anywhere in the plane; every crossing classified from its eigenvalues. |
| **Q3** | *n* = 4 and *n* = 1: the count of stable states against *a*, and the stronger result the handout proved. |
| **Q4** | pIKE105: the bistable band in α₂ at pTAK117's α₁, the bifurcation diagram, the two saddle-nodes, and what an RBS swap moves. |
| **Q5** | One ssrA tag: the criterion becomes g₁g₂ > δ₂, the point drops down the α₂ axis, and the RBS pays it back. |
| **Q6** | *BioE 247* — the IPTG threshold from the Fig. 5 legend's own parameters, the one-sided sweep, and what the model cannot say about a bimodal culture. |

### Before you start

The notation is the paper's — α₁, α₂, β, γ — and `posb.toggle_model(alpha1,
alpha2, n, m)` calls the cooperativities `n` (on *u*) and `m` (on *v*), so
γ = `n` and β = `m`. Every fixed-point count here uses
`stability_report(model, grid=(1e-3, 300, 9))`; pTAK117's states reach *u* = 156
and the default guess grid does not.

**Q5b asks you to build a `posb.Model` from four `Reaction`s.** Read the source
of `posb.toggle_model`; it is twelve lines and the pattern is session 3's.

### Collaboration

Encouraged. Discuss, argue, work at a whiteboard, then write your own solution
and your own code. Record who you worked with in the first cell. If you used an
LLM, say so and say what for — the conditions are that you can explain anything
you submit and that the code you submit runs.
