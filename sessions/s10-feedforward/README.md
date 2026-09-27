# Session 10 — Feedforward loops

[← all sessions](../README.md) · **Tuesday, September 29, 2026**

> Continues from session 9. The toggle held a state; a feedforward loop does
> something with **time** — it delays, it accelerates, or it turns a step into
> a pulse. Same three-node idea, three different jobs, and which job you get is
> decided by three signs.

## The one thing to remember

> **A feedforward loop is a two-path race. Whether the paths agree (coherent) or
> fight (incoherent) sets whether the circuit waits or pulses — and it only does
> it in one direction.**

## The artifact this is built on

Basu, Mehreja, Thiberge, Chen & Weiss, *PNAS* 2004 — the pulse generator. A
real incoherent type-1 FFL: LuxR·AHL activates GFP and also activates CI, and CI
represses the GFP promoter. Signal on → GFP rises, then CI catches up and shuts
it → a pulse. It reads the *rate* of the signal, which is how receiver cells on
a plate tell near senders from far ones. Assigned at the end of session 9 with
Mangan & Alon 2003 (the eight-type map). Artifact first, abstraction after — the
same shape as session 9.

## What happens

| | | |
|---|---|---|
| carry | **Session 9, unfinished** | The 40-hour failure surface and the parameter window — session 9's slides 21–22, not reached Thursday |
| 0–5 | **Retrieval**, notes closed | Nullcline; the saddle test; and *what makes the toggle hold* — carry the "removal sets the timescale" idea forward |
| 5–8 | Goals as questions | Why does one circuit ignore a flicker, another turn a step into a pulse, and can a three-gene circuit be *faster* than a one-gene one? |
| 8–14 | **The artifact** | Basu Fig. 1: point at the incoherence — the signal drives the output and its own delayed brake. Fig. 3: a pulse, and it depends on the *rate* |
| 14–24 | **Argue**, groups | Which arm is fast, which slow; what happens to the pulse if you swap them; what a slow ramp does and why that lets a cell measure distance |
| 24–28 | Sorted | Two paths, one delayed; agree → delay; fight → pulse. The delay is the second path's build time |
| 28–30 | The map, in one line | Three signs, eight wirings (Mangan Table 1/2). We build the two that matter |
| 30–42 | **Run**, the delay, one line at a time | C1-AND: Z waits for Y to cross K_yz. t_D = ln[Y_max/(Y_max−K_yz)]. Off-step: no wait. Short ON pulse: rejected |
| 42–48 | The incoherent one | I1 with basal Y: Z overshoots then adapts. **Peak, final, adaptation error = final/peak**, read off the curve (this is the PS5 item) |
| 48–52 | Coherent vs incoherent, the whole table | Which is a persistence detector, which is a pulser; the speed row; the AND↔OR sign flip in one sentence |
| 52–58 | **Response acceleration**, then **engineerability** | The same I1 circuit reaches half its steady state 6.3× faster than the matched one-gene design — Mangan & Alon's other headline result, and goal 3 from the opening. Then: what sets the delay (Y's lifetime, K_yz), what sets the pulse height (β_z vs the repression), and which of those is an RBS you can swap |
| 58–63 | **ConcepTest** | You want the pulse *taller and later*. Which knob? |
| 63–71 | **Worked set**, faded | [Four items](../../handouts/s10-feedforward.md): classify by sign, fill a delay table with the convention stated, compute one adaptation error, design one |
| 71–78 | Second half of the set | Reach the design item: pick a wiring for a stated job |
| 78–80 | Forward link | A toggle holds, an FFL times a single event — what keeps time *forever*? Session 11, the repressilator |

## The result this session exists to produce

Two, and they are the two coverage rows that are AUTO-graded on PS5, so the
handout has to state them as procedures:

**The delay (T24, T25).** The delay convention, stated on the slide and on the
handout because the matrix requires it: *response time is the time for Z to reach
50% of its steady state; the FFL is compared to a simple-regulation design with
the same steady-state Z; delay = t½(FFL) − t½(simple), reported with the sign of
the Sx step.* For C1-AND, on-step,

**t_D = α_y⁻¹ · ln[(Y_max − Y_min)/(Y_max − K_yz)]**

verified against the numerics in `figures/s10_feedforward.py` (H≫1 limit: 0.69
analytic vs 0.75 measured at K_yz = 0.5; the on-step delays, the off-step does
not — *sign-sensitive*).

**The adaptation error (T26).** For the incoherent type-1 with basal Y, Z rises
to a **peak**, then relaxes to a nonzero **final** level. The number a designer
cares about is how completely it forgets:

**adaptation error = Z_final / Z_peak**

read off the trajectory numerically — 0.62 for the handout's parameters. This is
the AUTO item on PS5, so the notebook computes peak, final and the ratio.

## Coverage

T24 (coherent vs incoherent classification by the two-path sign rule),
T25 (delay/timing table with the convention *written down*),
T26 (IFFL adaptation: peak, final and adaptation error, numerically).

All three are assessed on **PS5**, out Thursday 1 October.

## Reading handed out at the end of this session

Session 11's paper — Potvin-Trottier et al., *Nature* 2016 (the repressilator
with its noise sources removed one at a time). Assigned here per the readings
rule; discussed Thursday.

## Built

| | |
|---|---|
| Figures | `s10_c1_p1..p5` (the delay reveal), `s10_iffl_adaptation`, `s10_pulse_generator` — all from `posb.core` |
| Deck | `decks/s10_feedforward.py` |
| Handout | [s10-feedforward](../../handouts/s10-feedforward.md) + answers |
| Board notes | `board-notes/s10-board-notes.md` |

## Paper figures (slots; images stay out of the public repo)

`basu2004_fig1`, `basu2004_fig3`, `mangan2003_coherent_table`,
`mangan2003_incoherent_table` in `decks/paper_figures.yaml`. The Mangan tables
are reproduced legibly by pages 6–9 of the 2025 Lecture 20 rendering; crop those
to `private/paper-figures/` before delivering.

## Open

- **Carryover from session 9, confirmed 26 September.** Session 9 was delivered
  through its slide 20 (the second half of the faded set) and then its slide 23,
  the forward link — so the reading went out in the room on schedule. Its slides
  21 (the 40-hour failure surface) and 22 (the parameter window) were not
  reached and are carried at the front of this session.
- Badges are placeholders; the run sheet is Adam's.
