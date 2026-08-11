# Status and Roadmap

[← back to README](../README.md)

Living document. What exists, what does not, and what to do next.
**Last updated: 11 August 2026 — 15 days before instruction begins.**

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
cd ~/Documents/PoSB/posb2026/private
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
```

Use `--check` before class: it tells you exactly which images are still slots.

**Why the assembled deck is gitignored:** it may embed copyrighted figures, and
this repo is CC BY 4.0. See [Figures, Demos, and Decks](figures-and-decks.md).

---

## 3. What exists

| | Status |
|---|---|
| Public repo, CI, licensing, 9 doc pages, branding | done |
| `posb.core` (session 3) + `posb.analysis` (session 8), 24 tests | done |
| Build pipelines: notebooks, problem sets, figures, decks, link check | done |
| Session 3 notebook | done |
| PS0, PS1 + Gradescope bundle + solutions HTML | done |
| Demo 9 (toggle explorer) | done |
| Session 9 figures (3, generated) | done |
| Session 9 deck, 18 slides | done |
| Syllabus, diagnosis, redesign plan, coverage matrix | written, **not yet in the repo** |
| **Lecture decks for the other 27 sessions** | **not started** |
| Notebooks for sessions 4–28 | not started |
| PS2–PS9, midterm, final | not started |

---

## 4. Critical path

Nothing below is optional. Dates are when the material is first needed.

| By | What | Who |
|---|---|---|
| **now** | Push `private/` to the new private repo | you |
| **now** | Gradescope: CalNet SAML login, confirm **Create Course** appears | you |
| **before publishing sites** | Merge 147 + 247 into one bCourses site | you |
| **~3 days** | DataHub memory request lands — verify with `/sys/fs/cgroup/memory.max` | filed |
| **Aug 20** | Syllabus on bCourses | you |
| **Aug 25** | nbgitpuller links posted and tested (`tools/check_links.py`, then one live click) | both |
| **Aug 27** | Session 1 deck; PS0 released | me |
| **Sep 1** | Session 2 deck | me |
| **Sep 3** | Session 3 deck (notebook exists); PS1 released | me |
| **Sep 8** | **Session 4 deck + notebook** — QSSA, Michaelis–Menten, Hill | me |
| **Sep 10** | PS1 due · Session 5 | me |
| **Sep 22** | Session 8 + `posb.analysis` notebook | me |
| **Oct 6** | Session 12 — Gillespie. `posb.stochastic` needed | me |
| **Oct 13** | Midterm scope document published | both |
| **Nov 3** | Session 20 — `posb.fba` needed | me |
| **Nov 5** | **Sessions 21–23** — retroactivity, control, evolutionary stability. No existing material at all. | me |

---

## 5. Next steps, in order

**1. Deck triage — highest value, do first.**
Nineteen Fall-2025 decks, roughly a quarter of them duplicated content. A
file-by-file verdict — survives / merges into / dies, with duplicate slides
identified by page — recovers about five periods before a single new slide is
written, and turns 27 decks-from-scratch into far fewer.

**2. Sessions 1–3 decks.** Needed August 27, 29, September 3. Sessions 1–2 map
onto 2025 L01–L02 (which are 65% duplicated of each other — see the diagnosis).

**3. Session 4: deck + notebook.** QSSA, deriving Michaelis–Menten and the Hill
function. PS1 already assesses these, so this is the first place the
"nothing is assessed that was not demonstrated" rule can break.

**4. Put the planning documents in the repo.** The syllabus, the coverage
matrix, and the diagnosis exist as files but not as repository content. The
coverage matrix especially — `for-instructors.md` calls it the one thing worth
stealing and then does not ship it.

**5. `posb.analysis` notebook for session 8**, then sessions 8–9 decks.

**6. PS2 and PS3.** Both assess techniques from sessions 5–8.

**7. `posb.stochastic`** before session 12. Note the performance constraint:
`Model.rhs` costs ~4 µs, fine for `solve_ivp` and too slow for ensembles, so
the Gillespie path must precompute stoichiometry into arrays.

**8. Sessions 21–23.** Twelve coverage-matrix techniques, no existing deck,
notebook or problem. The largest block of net-new work in the course. Due
November 5 — start before October.

---

## 6. Known risks

**The 40% of the course with no existing material.** Sessions 19–23 and 25–28
are new. They are also the course's differentiator, so they cannot be
downgraded to survey lectures — each has a quantitative worked example
specifically to prevent that.

**`private/` is a single point of failure** until it is pushed. It holds the
only copy of the PS1 master.

**The Gillespie gap.** Session 12 is October 6, the midterm October 15, and
PS6 is not released until October 20. The coverage matrix caught this. The fix —
an ungraded self-checking exercise in the S12 notebook — has to actually be
built.

**Sessions 27–28 get no formative practice.** They fall after the last problem
set. Accepted; weight them lightly on the final.

**Reader load is front-weighted.** Part I is derivation-heavy, so hand-grading
peaks around PS2–PS3, which is exactly where the course's value is. Do not
economise there by making every problem autogradable.
