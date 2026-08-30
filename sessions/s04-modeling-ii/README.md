# Session 4 — Modeling Biology II: timescale separation

[← all sessions](../README.md) · **Tuesday, September 8, 2026**

No notebook. This is board work and one short paper exercise — the computing is
in [PS1](../../problem-sets/ps01-modeling/), which is due Thursday. **This
session hands out the reading for session 5** (see below).

## The one thing to remember

> **You are not allowed to delete a differential equation. You are allowed to
> delete a *small parameter*, and then you have to say how small.**

Michaelis–Menten and the Hill function are both what you get when you do that
honestly. Everything in this session is one of those two derivations, or the
error bar that comes with it.

## What happens

| | | |
|---|---|---|
| 0–8 | **Retrieval**, notes closed | Two from Thursday, one interleaved from session 2 |
| 5–8 | Map + goals as questions | |
| 8–14 | The small parameter, at the board | ε from session 3, and what ε → 0 actually *claims* |
| 14–26 | **Michaelis–Menten**, derived | Four named steps: QSSA on [ES], enzyme conservation, eliminate [E], the rate |
| 26–30 | The real validity condition | E<sub>tot</sub> ≪ K<sub>M</sub> + S₀ — and *not* E ≪ S |
| 30–34 | Where that group comes from | Two clocks, at the board |
| 34–38 | **ConcepTest 1** | You double E<sub>tot</sub>. What happens to K<sub>M</sub>? |
| 38–42 | The two regimes | [regimes](../../figures/build/s04_qssa_regimes.png) |
| 42–46 | The error is one ratio | [slope 1, four decades](../../figures/build/s04_qssa_error.png) |
| 46–48 | **The pause** | Two minutes. Say nothing. Then hand out the paper. |
| 48–58 | **Faded set, items 1–2 only** | Ten minutes. [PDF](../../handouts/s04-regulation-functions.pdf) · [source](../../handouts/s04-regulation-functions.md) |
| 58–62 | The answers | And the one that is not K<sub>d</sub> |
| 62–67 | Sensitivity | [Hill family](../../figures/build/s04_hill_family.png) — 81<sup>1/n</sup> |
| 67–72 | Independent sites | [two sites give n = 1](../../figures/build/s04_independent_sites.png) |
| 72–76 | **ConcepTest 2** | A fit gives n = 1.9. How many binding sites? |
| 76–80 | Consolidation + forward link | Assign the reading. To response time |

**Ten minutes of paper work, not twenty-four.** Items 3 and 4 of the handout are
on PS1 rather than in the room: they are the same technique with the scaffolding
gone, they take longer than ten minutes, and a single long block is where a room
diffuses and the switch back costs more than the work gained. Item 1 is fully
worked, which is what the coverage rule requires — *demonstrated*, not
*completed*.

## Why the concept is at the board and the procedure is on paper

Per [Lecture Design §2](../../docs/lecture-design.md): *generation for concepts,
faded worked examples for procedures.* Deriving Michaelis–Menten is a
**concept** — the move being taught is "eliminate the fast variable", and it is
worth watching someone do it once, slowly, with every assumption named aloud.
Deriving a regulation function from an equilibrium is a **procedure**: the same
four steps every time, which is exactly what fades well.

## The validity condition, which is the point of the session

PS1 Q3a asks students to state what the QSSA assumes — *"not merely 'ES is at
steady state,' but what must be true of the concentrations."* The answer this
session has to deliver is

$$E_{\text{tot}} \;\ll\; K_M + S_0$$

and **not** the textbook $E \ll S$. The two agree when $S_0 \gg K_M$ and part
company otherwise, and the difference is not pedantry: at $S_0 \ll K_M$ the
approximation survives enzyme concentrations comparable with the substrate,
which is the regime a lot of intracellular enzymes actually sit in. Segel's
scaling argument is the source; the session states the condition and shows it
holding numerically rather than deriving the perturbation theory.

[`s04_qssa_error.png`](../../figures/build/s04_qssa_error.png) is the evidence:
the relative error tracks $E_{\text{tot}}/(K_M + S_0)$ on a straight line of
slope one across four decades. That is what makes it a condition you can check
before you trust a model, rather than a slogan.

## What each figure is for

| Figure | The claim it makes checkable |
|---|---|
| [`s04_qssa_regimes`](../../figures/build/s04_qssa_regimes.png) | Same enzyme, same reduction, same clock — only the **concentration** changed, and the reduction went from exact to wrong by 15% of the substrate |
| [`s04_qssa_error`](../../figures/build/s04_qssa_error.png) | The error is set by **one dimensionless group**, not by a species. Slope one, four decades |
| [`s04_hill_family`](../../figures/build/s04_hill_family.png) | Same half-point, four sensitivities. $x_{90}/x_{10} = 81^{1/n}$ is the whole content of $n$ |
| [`s04_independent_sites`](../../figures/build/s04_independent_sites.png) | Two **independent** sites give a Hill function with **n = 1**, not 2 |

Enzyme parameters are PS1 Q3's exactly — $k_1 = 1$, $k_{-1} = 1$, $k_2 = 0.1$,
$S_0 = 1$, $E_0 \in \{0.001, 1.0\}$ — so the figure on the slide is the
numerical experiment they are asked to reproduce, not a cousin of it.

## Coverage

Demonstrates **T7** (QSSA; derive Michaelis–Menten), **T8** (derive the Hill
function from cooperative equilibrium binding), **T9** (identify where the QSSA
fails; compare full vs. reduced numerically). All three are assessed in **PS1**,
which is already out, and in the midterm. See the
[Coverage Matrix](../../docs/coverage-matrix.md).

**Note on PS1 Q5.** That question asks the 247 cohort (19 students) to write a partition
function over four states — the technique of session 6, which is a week later.
Item 4 of this session's handout is the same object, and item 1 demonstrates the
method on the two-state case, so the coverage rule holds. Without it the first
problem set would assess something that had not been taught.

## Reading

**Handed out at the end of this session, for session 5:** Andersen et al.,
*New unstable variants of green fluorescent protein*, Appl. Environ. Microbiol.
**64**(6), 2240–2246 (1998). Seven pages, and Figure 3A is the one that matters.
See [readings](../../docs/readings.md).

## Next

Session 5 — gene expression dynamics and response time: how fast a circuit can
change its mind, and why dilution sets the floor.
