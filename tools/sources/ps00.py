"""PS0 — environment check. Ungraded."""
from .common import md, code, header, SETUP

REL = "problem-sets/ps00-environment/ps00.ipynb"
TITLE = "PS0 — Environment Check"
SUBTITLE = "Ungraded · ten minutes · proves your setup works"
DATE = "due Wednesday, September 2, 2026, 11:59pm"


CELLS = [
    header(TITLE, SUBTITLE, DATE, REL),

    md("""This is not really a problem set. It exists to prove that your computing
environment works, so that nothing about the tooling is a surprise in week 3.

It should take **ten minutes**. If it takes longer, something is wrong and I
want to know — post on the bCourses forum, or bring it to the Tuesday
discussion hour on September 1, which is before this is due.

**Submit to Gradescope** (linked from bCourses) by **Wednesday, September 2**.

The deadline sits deliberately *after* the Tuesday discussion hour on
September 1. If any of this fights you, bring it there and we will sort it out
together — that is what the hour is for in week one. It also sits before
Session 3, which is where the notebooks really start."""),

    md("""---
## 0. Setup

Run the cell below. It should print a table of version numbers.

You will run a cell like this at the top of **every** notebook in this course.
On DataHub it costs nothing. On Colab it clones the course repository, which
is necessary because Colab opens a notebook by itself, without the supporting
code that lives next to it."""),
    code(SETUP),

    md("""---
## 1. Does the numerical stack work?

The single most important function in this course is
`scipy.integrate.solve_ivp`. It integrates a system of ordinary differential
equations forward in time. We will use it in almost every notebook from here
to December.

Here is the simplest possible test: exponential decay,

$$\\frac{dy}{dt} = -k y, \\qquad y(0) = y_0$$

which you already know has the solution $y(t) = y_0 e^{-kt}$. So we can check
the numerics against the truth."""),

    code('''\
from scipy.integrate import solve_ivp

k, y0 = 0.5, 1.0

sol = solve_ivp(lambda t, y: -k * y, [0, 10], [y0], dense_output=True)

t = np.linspace(0, 10, 200)
y_numeric = sol.sol(t)[0]
y_exact = y0 * np.exp(-k * t)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(t, y_numeric, lw=3, alpha=0.5, label="solve_ivp")
ax.plot(t, y_exact, "k--", lw=1.5, label="exact")
ax.set_xlabel("time")
ax.set_ylabel("y")
ax.set_title("dy/dt = -0.5 y")
ax.legend()
plt.show()

print(f"max absolute error: {np.max(np.abs(y_numeric - y_exact)):.2e}")'''),

    md("""**What you should see:** two curves lying on top of each other, and an
error around $10^{-7}$ or smaller.

If the plot rendered, your environment works and you are done with the hard
part."""),

    md("""---
## 2. Can you write a function?

No Python experience is assumed in this course, but you do need to be able to
write a function and a loop. Here is the level of fluency the course expects —
if this is comfortable, you are fine.

**Q2.1** Write a function `half_life(k)` that returns the time at which
$y$ has fallen to half its initial value, for the decay $dy/dt = -ky$.

You should be able to do this analytically; there is no need to simulate
anything. Replace `...` with your answer."""),

    code('''\
def half_life(k):
    """Time for exponential decay at rate k to fall to half the initial value."""
    ...


# quick self-check
_a = half_life(0.5)
print("correct" if _a is not None and np.isclose(_a, np.log(2) / 0.5)
      else "not yet — replace ... with your answer")'''),

    md("""**Q2.2** Write a function `steady_state(alpha, gamma)` returning the
steady-state value of $x$ for

$$\\frac{dx}{dt} = \\alpha - \\gamma x$$

This is the single most-used result in the whole course. You will see it again
in Session 5 and on every problem set after that."""),

    code('''\
def steady_state(alpha, gamma):
    """Steady state of dx/dt = alpha - gamma*x."""
    ...


_b = steady_state(10.0, 2.0)
print("correct" if _b is not None and np.isclose(_b, 5.0)
      else "not yet — replace ... with your answer")'''),

    md("""---
## 3. Submit

1. `Kernel → Restart Kernel and Run All Cells`
2. Confirm it runs top to bottom with no errors
3. Submit this `.ipynb` to **Gradescope** (linked from bCourses)

Get in the habit of step 1 now. From PS1 onward, a notebook that only runs
because of leftover state from cells you executed in a different order will
lose points — and it is the most annoying possible way to lose points on
work you actually understood."""),
]
