# Course Map

[← back to README](../README.md)

All 28 sessions, Fall 2026. **TuTh 8:00–9:29, Dwinelle 219.**
Instruction begins Aug 26; classes end Dec 4; no class Thu Nov 26.

Each session is roughly **45 minutes of concept + 30 minutes of a worked
example** — a problem actually being solved, using the technique the next
problem set demands. The worked example column is not decoration; it is the
contract. See [Design Notes](design-notes.md) for why the course is built this
way.

**Status key:** ✅ notebook published · 📝 board work, no notebook · ⬜ in preparation

---

## Part I — Design principles

*What can a circuit do, and why is it built that way?*

| # | Date | Topic | Worked example | |
|---|---|---|---|---|
| 1 | Thu Aug 27 | What synthetic biology is in 2026; the specification problem | Diagnostic; three specifications to argue about | [📝](../sessions/s01-specification/) |
| 2 | Tue Sep 1 | The cell as a physical substrate: crowding, copy number, timescales | Faded set: four estimates, from copy number to a search-time paradox | [📝](../sessions/s02-substrate/) |
| 3 | Thu Sep 3 | **Modeling I:** mass action, stoichiometry, d**x**/d*t* = **S·v** | Build and integrate a system three ways; prove they agree | [✅](../sessions/s03-modeling-i/) |
| 4 | Tue Sep 8 | **Modeling II:** timescale separation, quasi-steady state and its limits | Derive Michaelis–Menten; derive Hill from cooperative binding | ⬜ |
| 5 | Thu Sep 10 | Gene expression dynamics; response time; dilution vs. degradation | Response-time calculation; effect of degradation tags | ⬜ |
| 6 | Tue Sep 15 | Promoter occupancy from statistical thermodynamics | Derive activator, repressor, and AND-like rate laws | 📝 |
| 7 | Thu Sep 17 | Autoregulation: negative (speed, variance) and positive (bistability) | Derive the negative-autoregulation speed-up | 📝 |
| 8 | Tue Sep 22 | **The phase plane:** nullclines, fixed points, Jacobian, linear stability | Complete two-dimensional stability analysis | ⬜ |
| 9 | Thu Sep 24 | Bistability and the toggle switch: bifurcation, hysteresis, failure | Fixed points for *n* = 4 and *n* = 1 | ⬜ |
| 10 | Tue Sep 29 | Feedforward loops: persistence detection, pulse generation, adaptation | FFL timing analysis; numerical IFFL adaptation | ⬜ |
| 11 | Thu Oct 1 | Oscillators: repressilator, delayed negative feedback | State and apply the oscillation criterion; find the Hopf boundary | ⬜ |
| 12 | Tue Oct 6 | Noise: intrinsic vs. extrinsic, CV, bursting, the master equation | Write a Gillespie simulator from scratch | ⬜ |
| 13 | Thu Oct 8 | **The digital abstraction:** transfer curves, gain, noise margins | Numeric signal matching between two measured gates | ⬜ |
| 14 | Tue Oct 13 | Review and worked problems | Open problem session | 📝 |
| 15 | **Thu Oct 15** | **Midterm** — sessions 1–13 | | |

## Part II — Engineering design

*Now build one that survives in a real host.*

| # | Date | Topic | Worked example | |
|---|---|---|---|---|
| 16 | Tue Oct 20 | Combinational logic in cells; hazards; why design automation plateaued | Hazard timing table, end to end | ⬜ |
| 17 | Thu Oct 22 | Building it physically: parts, compositors, context, DNA assembly | Compose a two-part system; design Golden Gate overhangs | ⬜ |
| 18 | Tue Oct 27 | Implementation layers: CRISPRi/a, recombinase memory, protein circuits | Compare gate families on orthogonality, speed, load | ⬜ |
| 19 | Thu Oct 29 | Resource sharing, cellular economy, growth laws, burden | Shared-resource simulation | ⬜ |
| 20 | Tue Nov 3 | **Metabolic engineering and constraint-based design** | FBA as a linear program on the same **S** from session 3 | ⬜ |
| 21 | Thu Nov 5 | Retroactivity, impedance, insulation, load drivers | Retroactivity calculation for a loaded module | ⬜ |
| 22 | Tue Nov 10 | Robustness and control: integral feedback, antithetic control | Simulate an antithetic controller; quantify what it costs | ⬜ |
| 23 | Thu Nov 12 | Evolutionary failure: mutation, burden, circuit loss; containment | Time-to-circuit-failure from mutation rate and fitness cost | ⬜ |
| 24 | Tue Nov 17 | Communities: quorum sensing, patterning, division of labour | Sender/receiver band-detection analysis | ⬜ |
| 25 | Thu Nov 19 | Minimal and synthetic cells: top-down and bottom-up | Binomial genome partitioning: why most daughters are incomplete | ⬜ |
| 26 | Tue Nov 24 | Therapeutic circuits: logic-gated cell therapies, synNotch, delivery | Multi-input classifier to a false-positive budget | ⬜ |
| — | Thu Nov 26 | *Thanksgiving — no class* | | |
| 27 | Tue Dec 1 | Machine learning as the specification layer; genome language models | Design–filter–validate arithmetic: what beats directed evolution? | ⬜ |
| 28 | Thu Dec 3 | Biosecurity and governance as technical problems; what limits the field | Why similarity-based screening fails on generated sequences | ⬜ |

---

## Problem sets

Nine sets, roughly weekly, **2–4 problems each** — a weekly check that you can
execute the week's technique, not a weekend-consuming exercise.

| Set | Out | Due | Covers | |
|---|---|---|---|---|
| PS0 | Aug 27 | Sep 1 | Environment check — *ungraded* | [✅](../problem-sets/ps00-environment/) |
| PS1 | Sep 3 | Sep 10 | Mass action, timescale separation, Michaelis–Menten, Hill | [✅](../problem-sets/ps01-modeling/) |
| PS2 | Sep 10 | Sep 17 | Expression dynamics, response time, promoter occupancy | ⬜ |
| PS3 | Sep 17 | Sep 24 | Autoregulation, phase plane, stability | ⬜ |
| PS4 | Sep 24 | Oct 1 | Bistability, the toggle, hysteresis | ⬜ |
| PS5 | Oct 1 | Oct 8 | Feedforward loops, oscillation criteria | ⬜ |
| PS6 | Oct 20 | Oct 29 | Stochastic simulation, digital abstraction, hazards, assembly | ⬜ |
| PS7 | Oct 29 | Nov 5 | Implementation layers, resource competition, burden, FBA | ⬜ |
| PS8 | Nov 5 | Nov 19 | Retroactivity, feedback control, evolutionary stability | ⬜ |
| PS9 | Nov 19 | Dec 3 | Communities, minimal cells, therapeutic design | ⬜ |

## Assessment

| Component | Weight |
|---|---|
| Problem sets (9, lowest two dropped) | 30% |
| Midterm — Thu Oct 15 | 15% |
| Final exam — in person, finals week | 25% |
| Term project — staged from week 5 | 30% |

---

## Working through this outside Berkeley

The material is designed to stand alone. A reasonable self-study path:

**Foundations (sessions 3–5).** Do these in order and do the exercises. If
d**x**/d*t* = **S·v** and the quasi-steady-state approximation are comfortable,
everything else is reachable.

**Dynamics (sessions 8–12).** The analytical core. Phase-plane analysis
(session 8) is the single highest-leverage technique in the course — it is what
lets you look at a two-species circuit and say what it does without simulating
it.

**Then pick your interest.** Part II sessions are largely independent of one
another. Sessions 19–23 (burden, metabolism, retroactivity, control, evolution)
are the ones least covered by other courses and textbooks, and are where this
course differs most from its neighbours.

For the first half, [Biological Circuit
Design](https://biocircuits.github.io) (Elowitz & Bois) is an excellent
parallel treatment with a different framing. Read both.
