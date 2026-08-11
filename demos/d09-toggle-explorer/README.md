# Demo 9 — The Toggle Explorer

[← all demos](../README.md) · for **Session 9**

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/demos/d09-toggle-explorer/d09_toggle_explorer.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/demos/d09-toggle-explorer/d09_toggle_explorer.ipynb)

Sliders for α₁, α₂ and *n*, with live nullclines, fixed points, and stability
classification. Filled circles are stable states; the open red circle is the
saddle.

## The sequence that works in lecture

1. **n = 2, raise α.** The second stable state appears as you cross α = 2.
   Do it slowly enough that they see the nullclines bend into a third crossing.
2. **n = 1, raise α as far as it goes.** Nothing happens. Try again. Ask what
   would have to be true for it to work.
3. **Break the symmetry.** n = 2, α₁ = 6, walk α₂ down. The bistable window
   collapses abruptly rather than gracefully — which is why growth rate and
   burden knock a real toggle out of usefulness.

Step 2 is the point of the demo. The analytic reason is
`toggle_alpha_critical(n) = ∞` for *n* ≤ 1, and the derivation is the worked
example in Session 9.
