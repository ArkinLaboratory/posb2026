# For Instructors

[← back to README](../README.md)

This material is [CC BY 4.0](../LICENSE) (content) and
[BSD 3-Clause](../LICENSE-CODE) (code). Use it, adapt it, teach from it,
including commercially, with attribution. If you run a course from it I would like to hear about it —
[open an issue](https://github.com/ArkinLaboratory/posb2026/issues) or email.

---

## The one thing worth stealing

Not the lectures. The **coverage matrix**.

It is a table with four columns: *technique*, *the session that demonstrates
it*, *the instrument that assesses it*, and *whether a machine can grade it*.
This course has 74 rows. The rule it enforces is:

> Nothing is assessed that was not demonstrated first.

That sounds like a platitude until you build the table for an existing course.
When it was built for the previous version of this one, it found that a
20-point problem on retroactivity was supported by exactly two occurrences of
the phrase "impedance matching" in nineteen lecture decks, both in bullet
lists. It found that the criterion for oscillation was assessed and never once
stated. It found that Boolean minimisation was demonstrated eight times and
barely assessed.

Then — and this is the part that convinced me it is worth the effort — when the
matrix was rebuilt against the *new*, corrected calendar, it immediately caught
the same class of failure recurring: stochastic simulation scheduled for
October 6, examined October 15, with no graded practice in between. Caught in
August rather than by thirty students in October.

The matrix transfers to any quantitative course in any subject. Building one
for a course you already teach takes an afternoon and is uncomfortable.

---

## Adapting the material

### The whole course

Fork the repository. The pieces you will need to change:

1. **`tools/sources/common.py`** — `REPO_URL` and `REPO_DIR`, which propagate
   to every Colab badge, clone command, and DataHub link.
2. **`docs/course-map.md`** — dates, room, assessment weights.
3. **The DataHub links** are Berkeley-specific. If your institution runs a
   JupyterHub, substitute its hostname; the
   [nbgitpuller](https://nbgitpuller.readthedocs.io/) URL format is otherwise
   identical. If it does not, the Colab badges work anywhere.

Then `python tools/build_notebooks.py && python tools/execute_notebooks.py`.

### Individual pieces

Sessions in Part II are largely independent and can be lifted into an existing
course. The ones least covered elsewhere, and therefore most worth taking:

- **Session 19–20** — resource competition, burden, and constraint-based design
- **Session 21** — retroactivity and insulation
- **Session 22** — antithetic integral control
- **Session 23** — evolutionary stability and time-to-circuit-failure

`posb` is independently useful. `pip install` is not set up (deliberately — it
is course material, not a library), but the package is two files and vendors
cleanly.

### A note on licensing course code

If you are at a university or national laboratory, check your own institution's
software-release rules before publishing, even for a free licence. Several
require disclosure to a technology-transfer office *prior to* external
distribution regardless of whether money changes hands, and the requirement
usually turns on how and why the code was written rather than on which GitHub
account it sits in. Course scaffolding written for teaching is normally clear of
this; research code repackaged for teaching often is not.

---

## How the repository works

### Notebooks are build artifacts

The Python modules in `tools/sources/` are the source of truth. Each defines
`CELLS`, a list built from `md()` and `code()` helpers, plus the notebook's
title and path.

```bash
python tools/build_notebooks.py           # regenerate every .ipynb
python tools/build_notebooks.py --check   # fail if any is stale (used in CI)
python -m pytest tests/ -q                # unit tests for posb
python tools/execute_notebooks.py         # execute every notebook, fail on error
python tools/execute_notebooks.py --html out/   # also render to HTML
```

**Do not hand-edit a `.ipynb`.** Two reasons. First, executed notebooks churn
`execution_count` and `outputs` on nearly every cell, so diffs become useless.
Second, and much worse, is the interaction with distribution — see below.

### The nbgitpuller trap

If you distribute with [nbgitpuller](https://nbgitpuller.readthedocs.io/), know
its merge rule: on a conflicting line, **the student's version always wins**.

A student who has *executed* a notebook has modified `execution_count` and
`outputs` on nearly every cell. So if you fix a bug in one of those cells and
push, **the fix silently does not reach anyone who already ran the notebook.**
They will keep working from the broken version and you will not find out until
they submit.

Two rules follow:

1. **Ship each assignment as a new folder.** Never patch a notebook students
   have already run.
2. **Keep reusable logic in `.py` modules**, which students rarely edit, so
   merges stay clean. Keep notebooks thin.

Also: nbgitpuller's `branch` parameter defaults to `master`. Set it explicitly
to `main` or students get an unhelpful failure.

### Problem sets and the public-repo problem

This repository is public, so **problem-set masters cannot live in it** — they
contain solutions. The split:

```
private/sources/psNN.py            master source, SOLUTIONS, gitignored
    -> private/build/psNN/psNN.ipynb           master notebook
    -> otter assign
         -> problem-sets/psNN-*/psNN.ipynb     student version, COMMITTED
         -> private/build/psNN/dist/autograder/*.zip   upload to Gradescope
```

```bash
python tools/build_problem_sets.py        # all sets
python tools/build_problem_sets.py ps01   # one
```

Keep `private/` somewhere you back up — a private GitHub repo works well. It is
the source of truth for every problem set and is not recoverable from the public
repository.

### Otter Assign format, as verified against otter-grader 7.0.0

These cost several hours to establish empirically, so they are written down.

1. **Solution cells must sit between `# BEGIN SOLUTION` / `# END SOLUTION`
   *block* cells** (fenced ```` ```otter ```` markdown cells), exactly like
   `# BEGIN TESTS`. Inline `# BEGIN SOLUTION` comments **alone strip nothing** —
   they only take effect inside a cell already tagged by a block. Get this wrong
   and Otter silently publishes the answer key to students; `assign` reports no
   error.
2. **The two mechanisms compose.** A block-tagged code cell containing inline
   markers keeps the function signature and docstring and replaces only the
   marked body with `...`.
3. **Every cell object must be distinct.** Notebook cells are mutable dicts. If
   a helper returns a shared `# END QUESTION` cell reused at twenty indices,
   they are aliases, Otter's tagging applies to all occurrences at once, and
   only the first solution block gets stripped. `build_problem_sets.py` now
   fails the build on aliased cells rather than letting this through.
4. **Visible tests are embedded verbatim in the student notebook.** So visible
   tests must check *properties* — shapes, conservation laws, scaling,
   monotonicity, internal consistency — and hidden tests check *exact values*.
   A visible test that asserts the answer hands over the answer.
5. **Question points must equal the sum of that question's test points.**

### Why we pass `--no-run-tests`

Otter's assign-time validator evaluates tests in a namespace that does not match
the notebook's own. Observed with 7.0.0: a test calling a function that closes
over a variable assigned in a `NO PROMPT` solution cell sees that variable as
`Ellipsis`, while the identical test passes when the notebook actually runs.

So the builder skips that validator and instead **executes the solution notebook
and requires every `grader.check` to report all cases passing**. That is a
stricter gate, because it runs in the namespace students will actually have. It
immediately caught a wrong reference value in PS1 that the built-in validator
had masked behind an unrelated failure.

### Continuous integration

`.github/workflows/ci.yml` runs on every push: unit tests, a staleness check
that fails if any notebook differs from its source module, and a full execution
of every notebook. Free for public repositories.

The execution step is the one that matters. Unit tests cover `posb`; only
execution covers the thing students actually open.

### Pinning to the version floor

CI installs the **minimum** supported versions rather than the latest, because
the binding constraint is whichever student environment is oldest. Here that is
Google Colab (NumPy 2.0, SciPy 1.16) rather than Berkeley DataHub (NumPy 2.4,
SciPy 1.17).

Testing against the newest libraries tells you nothing about whether your
students can run the code. Test against the floor.

---

## Notes on the pedagogy

Fuller treatment in [Design Notes](design-notes.md). Three things that are
cheap to adopt and that made a disproportionate difference:

**Build the abstraction in front of them.** Session 3 solves the same network
three times — by hand, as a matrix, then with the package — and `assert`s that
all three agree to 10⁻⁹. Fifteen minutes of class time. Students end up able to
debug the tooling instead of treating it as an oracle, and the assertion makes
the claim "this is bookkeeping, not approximation" checkable rather than
asserted.

**Predict before you simulate.** Every worked example computes the expected
steady state on paper first, then plots the simulation against it. A simulation
you cannot check independently is not evidence of anything, and this habit is
the difference between students who catch their own modelling errors and
students who do not.

**Look for a conservation law and check it.** The cheapest possible test of a
model, and it catches sign errors instantly.

---

## Known limitations

- **`Model.rhs` is ~4 µs per call**, which is fine for `solve_ivp` and too slow
  for large stochastic ensembles. See
  [Package Reference § Performance](posb-reference.md#performance).
- **`method="LSODA"` is the default** in `Model.simulate`, which auto-switches
  between stiff and non-stiff solvers. Convenient, and the one genuine black
  box in the package. Documented rather than removed.
- **Roughly half the assessed techniques are not autogradable.** Derivations
  need a human. Plan reader time accordingly, and resist the temptation to make
  every problem numerically checkable — that reintroduces the defect this
  rebuild was meant to fix.
