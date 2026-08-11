# Deck Triage — the Fall 2025 material

[← back to README](../README.md) · See also [Status and Roadmap](roadmap.md)

A file-by-file verdict on the twenty-one Fall 2025 decks: what survives, what
merges into what, and what is cut. Produced by extracting all 962 pages,
normalising the text, and comparing every page against every page of every
earlier deck at a 0.90 similarity threshold.

**Method is reproducible.** Page text via `pdftotext -layout`, lowercased and
stripped to letters, compared with `difflib.SequenceMatcher`. Pages under 40
characters (title cards, image-only slides) are counted as novel rather than
guessed at, so the duplication figures below are a **lower bound**.

---

## 1. The headline number

> **309 of 962 pages — 32% — repeat a page from an earlier deck.**

That is not sloppiness. It is the ordinary consequence of continuing a topic
across sessions: you re-show where you left off, then add. But it means the
distinct content is **653 pages, not 962**, and six decks are almost entirely
recapitulation.

| Deck | Pages | Novel | % new | Repeats |
|---|---:|---:|---:|---|
| L01 Berkeley Only | 26 | 26 | 100% | — |
| **L02 Cellular Physics** | 16 | 6 | **38%** | L01 ×10 |
| L03 Modeling Biology I | 35 | 32 | 91% | L02 ×3 |
| L04 Top Down Design | 68 | 51 | 75% | L03 ×17 |
| **L06 Top Down + Cell Growth** | 50 | 23 | **46%** | L04 ×25 |
| **L07 Top Down + Cell Growth** | 41 | 9 | **22%** | L04 ×17, L06 ×13 |
| L08 Cell Growth + DNA Assembly | 62 | 48 | 77% | L06 ×13 |
| L09 Parts & Compositors I | 41 | 41 | 100% | — |
| L10 Parts & Compositors II | 70 | 49 | 70% | L09 ×21 |
| **L12 Parts III + Logic I** | 45 | 3 | **7%** | L10 ×41 |
| L13 Logic Cascades + Therapies | 57 | 52 | 91% | L03 ×3 |
| **L14 Logic Therapies** | 43 | 4 | **9%** | L13 ×39 |
| L15 Therapies + Logic Synthesis | 41 | 24 | 59% | L13 ×17 |
| **L16 Logic Synthesis** | 30 | 2 | **7%** | L15 ×20, L13 ×8 |
| L17 Gate Minimization II | 28 | 27 | 96% | L15 ×1 |
| L18 Gate Minimization III | 55 | 47 | 85% | L17 ×6 |
| **L19 Circuit Synthesis + FFL** | 39 | 4 | **10%** | L18 ×33 |
| L20 Sequential Dynamics | 23 | 21 | 91% | L18 ×2 |
| L21 Latches II + Oscillators | 71 | 63 | 89% | L20 ×8 |
| L24 Protein Circuits and more | 82 | 82 | 100% | — |
| L25 Epidemics | 39 | 39 | 100% | — |

**Six decks — L02, L06, L07, L12, L14, L16, L19 — are under 50% new material.**
Between them they occupy seven class periods and contribute about 51 pages of
content that is not already somewhere else.

Fourteen decks also repeat pages **within themselves**; L04 has 8 such pages and
L24 has 7.

---

## 2. Where the 2025 material lands in the 2026 calendar

| 2025 deck | Verdict | Goes to |
|---|---|---|
| L01 Berkeley Only | **REWRITE** — the framing is 2016-era | S1 |
| L02 Cellular Physics | **MERGE** — its 6 novel pages | S2 |
| L03 Modeling Biology I | **KEEP** — strongest deck in the set | S3 |
| L04 Top Down Design | **SPLIT** — abstraction hierarchy → S1; parts framing → S16 | S1, S16 |
| L06, L07 | **DIE** — 32 novel pages between them, on growth processes | S19 |
| L08 Cell Growth + DNA Assembly | **SPLIT** — assembly → S17; growth/burden → S19 | S17, S19 |
| L09 Parts & Compositors I | **KEEP** | S16 |
| L10 Parts & Compositors II | **MERGE into S16** with L09 | S16 |
| L12 Parts III + Logic I | **DIE** — 3 novel pages | S13 |
| L13 Logic Cascades + Therapies | **SPLIT** — cascades/transfer functions → S13; therapy → S26 | S13, S26 |
| L14 Logic Therapies | **DIE** — 4 novel pages | S26 |
| L15 Therapies + Logic Synthesis | **SPLIT** | S26, S16 |
| L16 Logic Synthesis | **DIE** — 2 novel pages | — |
| L17 Gate Minimization II | **CUT ENTIRELY** — Karnaugh maps | — |
| L18 Gate Minimization III | **CUT ENTIRELY** — except the Cello material → S16 | S16 |
| L19 Circuit Synthesis + FFL | **DIE** — 4 novel pages, feedforward → S10 | S10 |
| L20 *(titled "Feedforward and Feedback")* | **SPLIT** — pp. 1–10 motifs → S10; pp. 11–23 toggle → S9 | S9, S10 |
| L21 Latches II + Oscillators | **SPLIT** — toggle → S9; oscillators → S11 | S9, S11 |
| L24 Protein Circuits | **KEEP** — 82 novel pages | S18 |
| L25 Epidemics | **KEEP** — DIPs/TIPs → biosecurity | S28 |

### What this recovers

Cutting the gate-minimisation block (L17, L18 minus Cello) and the six
recapitulation decks removes roughly **five class periods** of content that
either duplicates earlier material or teaches Karnaugh maps. That is the budget
that pays for sessions 20–23.

---

## 3. The sessions with no source material at all

This is the more consequential half of the triage. **Thirteen of twenty-eight
sessions have no 2025 deck to build from:**

| Session | Topic | Why there is nothing |
|---|---|---|
| **S4** | QSSA, Michaelis–Menten, Hill | Hill appears in L03 as 3 title-only slides; MM is used, never derived |
| **S5** | Expression dynamics, response time | — |
| **S6** | Promoter occupancy from statistical thermodynamics | — |
| **S7** | Autoregulation | asserted from Alon, never derived |
| **S8** | **Phase plane, fixed points, stability** | the sharpest gap: assessed for 20 points, one slide of symbol definitions |
| **S12** | Noise, master equation, Gillespie | "stochastic" appears once in L03 |
| **S20** | Metabolic engineering, FBA | new for 2026 |
| **S21** | **Retroactivity, insulation** | assessed for 20 points; "impedance" appears 3× in 962 pages, always as the phrase "Impedance matching" in a bullet list |
| **S22** | Antithetic / integral control | new |
| **S23** | Evolutionary stability, containment | new |
| **S24** | Communities, quorum sensing | 4 passing mentions of "quorum", no treatment |
| **S25** | Minimal and synthetic cells | new |
| **S27** | AI / generative design | new |

A keyword census across all 962 pages:

| term | hits | | term | hits |
|---|---:|---|---|---:|
| nullcline | **0** | | retroactivity | **0** |
| Jacobian | **0** | | flux balance | **0** |
| eigenvalue | **0** | | antithetic | **0** |
| bifurcation | **0** | | minimal cell | **0** |
| Gillespie | **0** | | impedance | 3 |
| master equation | 2 | | quorum | 4 |
| Hill function | 1 | | Karnaugh | 5 |

The three non-zero terms in the left column are the tell. "Impedance" appears
three times across 962 pages, never with a definition or a calculation.
"Master equation" twice, "Hill function" once — for concepts that carry
problem-set points.

The diagnosis said the course assessed techniques it never taught. This is that
claim in its strongest form: **the vocabulary is absent from the corpus.**

---

## 4. What to do, in order

**Reuse is concentrated and shallow.** Only four decks survive largely intact —
L03, L09, L20, L24 — plus L25 and parts of L08, L13, L21. Everything else is
either a fragment or a cut.

1. **S3** — L03 is the strongest deck in the set. Light edit: convert MATLAB
   references to the notebook, add the worked example.
2. **S1, S2** — L01 rewritten for 2026, absorbing L02's 6 novel pages and L04's
   abstraction hierarchy.
3. **S16, S17** — L09 + L10 merged, with the Cello material from L18. L08's
   assembly pages to S17.
4. **S9, S11** — L20 + L21 split. The S9 deck already exists, built new.
5. **S18, S26, S28** — L24, L13/L14/L15's therapy pages, L25.

**A correction to the row above.** The file called *Sequential Dynamics* is
titled **"Feedforward and Feedback"** on its own first page, and it splits
cleanly: **pp. 1–10** are the pulse generator recap and four coherent/incoherent
feed-forward motif slides, which belong to **S10**; **pp. 11–23** are the toggle,
which belong to **S9**. The earlier verdict sent the whole deck to S9 and would
have lost the only feedforward material in the corpus.

**None of the four motif slides carries a citation.** Neither does the "Toggle
longevity" slide (p. 21), which is the source of the 40-hour failure claim — see
[`decks/paper_figures.yaml`](../decks/paper_figures.yaml). The one Alon
reference in all 962 pages is a credit line on the *autoregulation* slide in
L10 and L12, which is S7 material.
6. **Everything in §3 is written from nothing.** Thirteen sessions.

The honest summary: **the 2025 decks provide usable material for about eight of
the twenty-eight sessions.** The triage is worth doing because it cuts the
authoring problem from twenty-eight to roughly twenty, and because it tells you
exactly which twenty — but it does not make this a small job.

Prioritise by date. S4 is needed 8 September and PS1 already assesses its
content; S8 is needed 22 September and is the single largest pedagogical gap in
the old course.
