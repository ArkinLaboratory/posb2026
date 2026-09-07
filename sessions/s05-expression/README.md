# Session 5 — Gene expression dynamics: response time, dilution, and the floor

[← all sessions](../README.md) · **Thursday, September 10, 2026**

**The first session built to the revised standard** — [lecture-design §5b and
§5c](../../docs/lecture-design.md). Derivations live on slides as step-slide
runs; the board keeps only the ledger; every student activity is the same
rhythm. No laptops. **PS1 closes tonight; PS2 posts today.**

## The one thing to remember

> **A protein you never destroy still disappears, because the cell divides.
> Dilution is a rate, it is not optional, and it sets a floor on how fast any
> circuit in a growing cell can change its mind.**

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | Two from Tuesday, one interleaved from session 2 — the one that is today's hinge |
| 5–8 | Map + goals as questions | |
| 8–18 | **Derivation 1**, five step slides | d*p*/d*t* = α − (γ+μ)*p*, and *p\** = α/(γ+μ) |
| 18–24 | **Rhythm 1** | You double the promoter. What moves? *(answer B — and they cannot fully justify it yet, deliberately)* |
| 24–34 | **Derivation 2**, four step slides | *t*½ = ln2/(γ+μ), and α is absent from it |
| 34–40 | **Rhythm 2** | Ten-minute response, thirty-minute doubling, γ = 0. *(answer C)* |
| 40–44 | Andersen 1998 Fig 3A | [response curves](../../figures/build/s05_response_tags.png) |
| 44–48 | The four numbers, on the board | 30.0 → 23.6 → 20.0 → **17.1 min**, and 1.00 → 0.57 |
| 48–50 | **Pause** | Two minutes, individual, **nothing collected** |
| 50–58 | **Faded set, items 1–2** | Eight minutes. Getting a removal rate out of decay data |
| 58–62 | The answers | A slope is a rate; a rate is not a half-life |
| 62–66 | The trade, priced | [speed vs level](../../figures/build/s05_speed_level.png) |
| 66–71 | **Rhythm 3** — pose | Handout item 3, four minutes on paper |
| 71–76 | **Rhythm 3** — resolve | *(answer C: the specification is not purchasable)* |
| 76–80 | Consolidation, reading, forward link | Bintu 2005 for session 6 |

## The numbers, computed and not asserted

E. coli at a 30-minute doubling time, so μ = ln2/30 = 0.023 min⁻¹. Degradation
half-lives are Andersen et al. 1998 Fig 3A, measured **after a medium
downshift** — growth is arrested, so they are γ alone and can be added to our μ
rather than replacing it.

| tag | *t*½ degradation | γ + μ (min⁻¹) | *t*½ overall | *p\** vs untagged |
|---|---|---|---|---|
| no tag | — | 0.023 | 30.0 min | 1.00 |
| ASV | 110 min | 0.029 | 23.6 min | 0.79 |
| AAV | 60 min | 0.035 | 20.0 min | 0.67 |
| LVA / LAA | 40 min | 0.040 | **17.1 min** | **0.57** |

**The session lands on the last two columns.** The strongest tag in the paper
buys a factor of 1.75 in speed and costs 43% of the steady-state level, because
*t*½ = ln2/(γ+μ) and *p\** = α/(γ+μ) share a denominator. That is session 3's
ConcepTest 2 collision with measured numbers on it, and it is why session 7 goes
looking for a second knob.

## Why the derivations are on slides

Sessions 3 and 4 put 37 and 32 minutes of derivation on the blackboard, and the
derivation PS1 Q3a assesses existed nowhere a student could read it. See
[lecture-design §5b](../../docs/lecture-design.md). Each derivation here is a
run of step slides — one per step, each the previous slide plus one line, the
live line in colour and the earlier ones dimmed. It advances on the clicker at
chalk speed; the exported PDF has one page per step and the last page carries
the whole argument.

`Deck.pacing()` measures these runs in **minutes per step**, not minutes per
slide, and fails past 3 min/step. Both runs here are at 2.0 and 2.5.

## What the board still does

One thing, and it is the thing slides cannot: hold results in parallel while
other things are shown.

**Left wing, written once and never wiped:**

*p\** = α/(γ+μ)  ·  *t*½ = ln2/(γ+μ)  ·  μ = 0.023 min⁻¹

Rhythm 2 and Rhythm 3 are both unanswerable without those three lines, and they
are on screen for four minutes each an hour apart.

## Nothing is collected

The pause is individual and stays with the student. An earlier draft of session 4
had students hand in written answers for the instructor to read that evening;
that sent the feedback to the wrong person, and in a 31-student room the
instrument for finding out what people think is asking them. See
[lecture-design §5c](../../docs/lecture-design.md).

**Record the poll distribution after each of the three votes.** That is the
between-class signal the collected slips were really buying.

## What this session owes PS2

| | |
|---|---|
| **T10** response time, *t*½ = ln2/(γ+μ) | Derivation 2, faded set items 1–2 |
| **T11** dilution vs degradation; what a tag does to circuit speed | The floor segment and the four-row table |
| **T12** steady-state level from a production/removal balance | Derivation 1 |

Handout item 3 is PS2 Q2; item 4 is the 247 question.
