# Status and Roadmap

[← back to README](../README.md)

Living document. What exists, what does not, and what to do next.
**Last updated: 24 August 2026 — two days before instruction begins, three before the first lecture.**
*(Session 3 built since; the block below still stands.)*

---

## 1. The two repositories

| | Repo | Contains |
|---|---|---|
| **Public** | `ArkinLaboratory/posb2026` | Everything students and the world see. Notebooks, `posb`, docs, generated figures, deck *sources*. |
| **Private** | `ArkinLaboratory/posb2026-private` | Problem-set masters (with solutions), exam material, figures scanned from papers, assembled decks. |

The private repo is mounted as `private/` inside the working copy and is
gitignored by the public one, so the two never collide.

**Wiring it up, once:**

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026/private
git init
git remote add origin https://github.com/ArkinLaboratory/posb2026-private.git
git add -A && git commit -m "Problem set masters and paper figures"
git branch -M main && git push -u origin main
```

Thereafter it is a second `git push` whenever masters change. **Do this before
writing PS2** — `private/` currently exists only on one machine.

---

## 2. How decks work — one source, two outputs

There is **no public deck and private deck to keep in sync, and nothing is ever
edited by hand before class.**

```
decks/s09_bistability.py          ← public source, in the repo
        │
        │   python tools/build_decks.py s09
        ▼
private/build/decks/*.pptx        ← gitignored output
```

Figures resolve at build time:

| Figure kind | Where it comes from | In the built deck |
|---|---|---|
| Generated from `posb` | `figures/build/*.png`, public | always embedded |
| From a published paper | `private/paper-figures/<key>.png` | embedded **if present**, otherwise a labelled slot naming the exact figure |

So the same command produces your classroom deck on your machine and a
slot-marked deck in CI or on a fork. `decks/paper_figures.yaml` records every
expected figure with its full citation, DOI and figure number — it is the
shopping list, and it is public because a citation is not a copyright problem.

```bash
python tools/build_decks.py            # all decks
python tools/build_decks.py s09        # one
python tools/build_decks.py --check    # fail if any paper figure is missing
python tools/build_decks.py --verify   # is the built deck older than its sources?
```

Use `--check` before class: it tells you exactly which images are still slots.

**Why the assembled deck is gitignored:** it may embed copyrighted figures, and
this repo is CC BY 4.0. See [Figures, Demos, and Decks](figures-and-decks.md).

---

## 3. What exists, on 24 August

| | Status |
|---|---|
| Public repo, CI, licensing, docs, branding | done |
| `posb.core` (S3) + `posb.analysis` (S8) | done, 48 tests |
| Build pipelines: notebooks, problem sets, figures, decks, handouts, readings, links | done |
| **Staleness check** — `--verify` on decks and figures | done, in CI |
| Syllabus, coverage matrix (76 techniques), course map, deck triage | in the repo |
| **Decks: S1 (22 slides), S2 (20), S3 (21), S9 (18)** | **4 of 28** |
| Handouts: S1 diagnostic, S1 launch problem, S2 faded set | 3, PDF, committed |
| Figures: 15 generated, across 5 modules + 1 movie | done |
| Demos: D2 crowding, D9 toggle explorer | 2 |
| Notebooks: S3 only | 1 of 28 |
| PS0, PS1 + Gradescope bundle | done |
| Readings declared | **5 papers, 2 sessions (S9, S10) of 27** |
| PS2–PS9, midterm, final | not started |

---

## 4. The arithmetic, which is the actual status

**Decks exist for 27 August and 1 September. The next one needed is 3
September, and it does not exist.** S9 is built but stored — it does not defend
the front. On current stock the course runs out on the third teaching day.

Twenty-four decks remain over fourteen teaching weeks: **1.8 decks per week,
sustained, while teaching, while writing eight problem sets, a midterm and a
final.** S1 and S2 each took roughly a day at the standard they were built to —
twenty slides, generated figures, two ConcepTests, a demo, embedded movies,
speaker notes carrying provenance. That standard does not multiply by
twenty-five.

### The block that decides the semester

The deck triage found thirteen sessions with no 2025 source material. **Five of
them are consecutive, and they land in the first month:**

| | Date | In | Topic | Source material |
|---|---|---|---|---|
| S4 | Sep 8 | 15 d | QSSA, Michaelis–Menten, Hill | Hill = 3 title-only slides; MM used, never derived |
| S5 | Sep 10 | 17 d | Expression dynamics, response time | none |
| S6 | Sep 15 | 22 d | Promoter occupancy, statistical thermodynamics | none |
| S7 | Sep 17 | 24 d | Autoregulation | asserted from Alon, never derived |
| S8 | Sep 22 | 29 d | **Phase plane, fixed points, stability** | one slide of symbol definitions; assessed for 20 points |

Everything before this block is either built (S1, S2) or has a notebook (S3).
Everything after it has 2025 material to triage until S12. So the hardest
writing in Part I coincides exactly with the first month of teaching, when the
least time exists. This is the risk that ends the semester badly, and it is
visible now rather than on 6 September.

**Three fixes, none of them optional on their own:**

1. **Build S4–S8 as one block, now, not one per week.** They share machinery —
   each is *write a rate law, take a limit, analyse what survives*. One figure
   module and one notebook cover S4, S5 and S7. Written serially they are five
   days of work; written together they are closer to three, and the shared
   notation stops being re-derived.
2. **Define a second deck standard and say which sessions get which.** The S1/S2
   build — movies, demos, faded sets — is right for the sessions that carry the
   course's argument and unaffordable for all twenty-eight. A B-standard deck is
   fourteen slides, one generated figure, one ConcepTest, no demo, notes that
   still carry provenance. Name the eight A-standard sessions in advance;
   otherwise the standard is decided by whichever week is busiest.
3. **Decide now whether S6 survives as a session.** Statistical thermodynamics
   of promoter occupancy is the most compressible period in Part I — it could be
   the first twenty minutes of S7. That recovers a period to absorb slippage.
   The cost is real and must be paid explicitly: T13 is assessed in PS2 and on
   the midterm, so cutting the session means moving the assessment, not quietly
   keeping it.

### The second production line

PS2 posts **10 September** and does not exist. Then PS3 (Sep 17), PS4 (Sep 24),
PS5 (Oct 1). Four problem sets in the same twenty-two days as the five-deck
block. PS2 and PS3 assess S5–S8 — the sessions not yet written — so they cannot
be written first.

---

## 5. Overdue and imminent, in date order

| Was due | What | Who |
|---|---|---|
| **Aug 20 — passed** | Syllabus on bCourses | you |
| **Aug 25 — tomorrow** | nbgitpuller links posted and tested (`tools/check_links.py`, then one live click) | both |
| now | Push `private/` to the private repo — it holds the only copy of the PS1 master | you |
| now | Gradescope: CalNet SAML login, confirm **Create Course** appears | you |
| ~~now~~ | ~~Merge 147 + 247 into one bCourses site~~ — **done**; one site, SIS `CRS:BIOENG-147-2026-D`, carrying `BIOENG 147 LEC 001` and `BIOENG 247 LEC 001` | you |
| now | DataHub memory request — verify with `/sys/fs/cgroup/memory.max` | filed |
| **Aug 27** | **S2's reading, if it gets one.** The rule is that a paper discussed in class N is handed out at the end of class N−1, so anything S2 reads must be named on Thursday | both |
| ~~Sep 3~~ | ~~S3 deck~~ — **built 24 August** | done |
| Sep 8 | S4 deck + notebook | me |
| Sep 10 | S5 deck; **PS2 posted**; PS1 due | me |

Three syllabus items remain unresolved and one of them is a registrar
dependency: final-project date (Fri Dec 11, RRR week), the exam group, and
whether the final falls in the Dec 14–18 block.

---

## 6. Known risks

**Readings are declared for two sessions out of twenty-seven.** The mechanism
is built and enforced in CI; the content is not. A session with no declared
reading is not automatically wrong, but it is indistinguishable from one that
was forgotten — and the decision has to be made a session ahead, not the night
before. Fill these in as each deck is written.

**The five-deck block above.** Restated here because it is the top risk in the
course and everything else is downstream of it.

**Sessions 21–23 — twelve coverage-matrix techniques, no material of any kind.**
Retroactivity, antithetic control, evolutionary stability. Due 5 November. The
largest net-new block after Part I. Start before October or it collides with
the same problem in Part II that Part I is about to have.

**The Gillespie gap.** S12 is 6 October, the midterm 15 October, PS6 not
released until 20 October. Students meet the master equation and are assessed on
it with no formative practice in between. The fix — an ungraded self-checking
exercise in the S12 notebook — is designed and not built. `posb.stochastic` is
also not built, and `Model.rhs` at ~4 µs is too slow for ensembles, so the
Gillespie path must precompute stoichiometry into arrays.

**`private/` is a single point of failure** until it is pushed. It holds the only
copy of the PS1 master and every paper figure and movie.

**Sessions 27–28 get no formative practice** — they fall after the last problem
set. Accepted; weight them lightly on the final.

**Reader load is front-weighted.** Part I is derivation-heavy, so hand-grading
peaks around PS2–PS3, which is exactly where the course's value is. Do not
economise there by making every problem autogradable.

---

## 7. What is actually finished, and what that proves

Three decks, three handouts, two demos, two problem sets, eleven figures, one
notebook, 48 tests, and six checks that fail loudly: paper figures missing,
readings not handed out first, pacing too thin, the calendar disagreeing with
itself, a committed figure older than its generator, and a built deck older than
its sources.

The checks are the part worth keeping. Every one of them exists because
something went wrong first — a distorted figure, a fourteen-slide ninety-minute
lecture, a citation attached to the wrong claim, a deck taught from a
two-hour-old file. None of them would have been caught by rereading the source.
