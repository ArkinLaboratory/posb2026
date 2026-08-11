# Getting Started

[← back to README](../README.md)

There are three ways to run this material. Pick one and stop reading the
others.

| | Who it is for | Setup cost | Work persists? |
|---|---|---|---|
| **[Berkeley DataHub](#berkeley-datahub)** | Enrolled Berkeley students | None | Yes |
| **[Google Colab](#google-colab)** | Everyone else | A Google account | In your Drive |
| **[Local install](#local-install)** | People who already have a Python setup | ~5 minutes | Yes |

---

## Berkeley DataHub

Berkeley runs a free JupyterHub for course use. You already have an account —
it authenticates through bCourses. **There is nothing to install and nothing to
configure.**

1. Click the link for the assignment on bCourses, or
   **[open the whole repository](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026)**
2. Sign in with your CalNet credentials
3. JupyterLab opens with the notebook already loaded

That is the entire process. Use the bCourses link every time rather than
downloading and re-uploading files.

### Four things that will otherwise surprise you

**Your session shuts down after about 30 minutes of inactivity.** Files on
disk survive; anything held only in memory does not. If you start a long
stochastic simulation and walk away, you will return to a dead kernel. Save
intermediate results to disk.

**Your home directory is not backed up.** Download anything you care about. At
minimum, download your completed problem sets.

**Access ends roughly nine months after you graduate.** Download your project
before then.

**There is a reset link for every assignment.** If you break a notebook beyond
repair, the reset link renames your copy with a timestamp and gives you a fresh
one. Nothing is deleted — your old version is still there.

---

## Google Colab

Every notebook in this repository carries an **Open in Colab** badge. You need
a Google account; any account works.

Click the badge, then **run the first cell**.

### Why the first cell matters

Colab opens a notebook **by itself**, without the rest of the repository. The
`posb` package is not there. That is why every notebook begins with a setup
cell that clones this repo and puts it on the import path.

If you skip that cell you will see:

```
ModuleNotFoundError: No module named 'posb'
```

which looks like a bug in the notebook and is not. Run the setup cell.

### Other Colab caveats

- **Everything is discarded when your session ends** — installed packages,
  downloaded files, all of it. The notebook itself is saved to *your* Google
  Drive if you use *File → Save a copy in Drive*.
- Colab runs slightly **older** numerical libraries than DataHub does (see
  [version floor](#version-floor)). All course code is written to work in
  both.

---

## Local install

You own your own environment. Course staff will help with the science but
cannot debug your conda installation.

```bash
git clone https://github.com/ArkinLaboratory/posb2026.git
cd posb2026
pip install -r requirements.txt
jupyter lab
```

To verify the install:

```bash
python -m pytest tests/ -q          # 13 tests on posb.core
python tools/execute_notebooks.py   # runs every notebook end to end
```

If both pass, you are set.

---

## Version floor

The two supported environments differ, and **Colab is the older one**:

| | Berkeley DataHub | Google Colab |
|---|---|---|
| Python | 3.11.0 | 3.12.13 |
| NumPy | 2.4.2 | **2.0.2** |
| SciPy | 1.17.0 | **1.16.3** |
| matplotlib | 3.10.3 | 3.10.0 |
| SymPy | 1.14.0 | 1.14.0 |

*(measured August 2026)*

Nothing in this repository uses anything newer than **NumPy 2.0 / SciPy 1.16**,
so the same code runs unmodified in both. If you write your own code that works
in one and not the other, this is usually why — watch for the NumPy 2.0
removals in particular (`arr.ptp()` and `np.float_` are gone; use `np.ptp(arr)`
and `np.float64`).

---

## What background do I need?

**Biology:** cell biology, molecular biology, genetics, and enough chemistry to
write a reaction rate.

**Mathematics:** calculus, elementary differential equations, and linear
algebra. You do not need to be fluent — you need to not be frightened. The
first four sessions rebuild what the course actually uses.

**Programming:** none assumed. You should be able to write a loop and a
function in *some* language. Session 3 is the Python onboarding and everything
after it builds on that one notebook.

If your background is light on differential equations, sessions 3–9 are the
demanding stretch. If it is light on molecular biology, sessions 17–19 are.

---

## Submitting work (enrolled students)

1. `Kernel → Restart Kernel and Run All Cells`
2. Confirm it runs top to bottom with no errors
3. Submit the `.ipynb` to **Gradescope**, linked from bCourses

Step 1 is not optional. A notebook that works only because of state left over
from cells you ran in a different order is not a working notebook, and it is
the most irritating possible way to lose points on something you actually
understood.

---

## Getting help

| | |
|---|---|
| Enrolled students | bCourses forum, or the Tuesday discussion hour after class |
| Everyone | [Open an issue](https://github.com/ArkinLaboratory/posb2026/issues) |

Prefer the forum to private email — a question one person asks is usually a
question five people have.
