"""Session 3 — Modeling Biology I."""
from .common import md, code, header, SETUP

REL = "sessions/s03-modeling-i/s03_modeling_i.ipynb"
TITLE = "Session 3 — Modeling Biology I"
SUBTITLE = r"Mass action, stoichiometry, and $\dot{\mathbf{x}} = \mathbf{S}\mathbf{v}$"
DATE = "Thursday, September 3, 2026"


CELLS = [
    header(TITLE, SUBTITLE, DATE, REL),

    md("""Today has two jobs.

The first is the **science**: every deterministic model in this course is built
the same way. You write down a list of reactions, you turn each reaction into a
rate, and you assemble those rates into a system of differential equations.
That assembly step has a compact form — $\\dot{\\mathbf{x}} = \\mathbf{S}\\mathbf{v}$ —
and once you see it, you will never write an ODE system by hand again.

The second is **tooling**: this is the notebook where the course's Python setup
gets introduced. Everything else this term builds on it.

### The rule for this package

> **Nothing in `posb` is used before you have built it by hand.**

So we are going to do today's problem twice. First the long way, writing every
derivative out explicitly. Then the short way, with the stoichiometric matrix.
Then we will check *numerically* that the two give identical answers — because
an abstraction you have not verified is just a place for bugs to hide."""),

    md("""---
## 0. Setup"""),
    code(SETUP),

    md("""---
## 1. The long way

Consider the simplest interesting reaction network — a reversible binding
event:

$$\\mathrm{A} + \\mathrm{B} \\;\\underset{k_r}{\\overset{k_f}{\\rightleftharpoons}}\\; \\mathrm{C}$$

**Mass action** says the rate of a reaction is proportional to the product of
its reactant concentrations, each raised to its stoichiometric coefficient. So
the forward reaction proceeds at $k_f[\\mathrm{A}][\\mathrm{B}]$ and the reverse
at $k_r[\\mathrm{C}]$.

Now write the derivative of each species. A is consumed by the forward
reaction and produced by the reverse:

$$\\frac{d[\\mathrm{A}]}{dt} = -k_f[\\mathrm{A}][\\mathrm{B}] + k_r[\\mathrm{C}]$$
$$\\frac{d[\\mathrm{B}]}{dt} = -k_f[\\mathrm{A}][\\mathrm{B}] + k_r[\\mathrm{C}]$$
$$\\frac{d[\\mathrm{C}]}{dt} = +k_f[\\mathrm{A}][\\mathrm{B}] - k_r[\\mathrm{C}]$$

Note how repetitive that is. The same two flux terms appear in all three
equations, with different signs. **That redundancy is the thing the
stoichiometric matrix removes.** Hold onto that observation.

Let us integrate it directly."""),

    code('''\
kf, kr = 1.0, 0.2

def rhs_by_hand(t, x):
    """Right-hand side, written out species by species."""
    A, B, C = x
    forward = kf * A * B
    reverse = kr * C
    return [
        -forward + reverse,   # dA/dt
        -forward + reverse,   # dB/dt
        +forward - reverse,   # dC/dt
    ]

x0 = [1.0, 1.5, 0.0]
t_eval = np.linspace(0, 15, 400)

sol_hand = solve_ivp(rhs_by_hand, [0, 15], x0, t_eval=t_eval,
                     method="LSODA", rtol=1e-8, atol=1e-10)

fig, ax = plt.subplots(figsize=(6.5, 4))
for row, name in zip(sol_hand.y, ["A", "B", "C"]):
    ax.plot(sol_hand.t, row, lw=2, label=name)
ax.set_xlabel("time")
ax.set_ylabel("concentration")
ax.set_title("A + B $\\\\rightleftharpoons$ C, written out by hand")
ax.legend()
plt.show()'''),

    md("""**Sanity check before going further.** Two quantities should be
conserved here: $[\\mathrm{A}] + [\\mathrm{C}]$ and $[\\mathrm{B}] + [\\mathrm{C}]$,
because every A that disappears becomes a C. If your integration does not
conserve them, the model is wrong or the tolerances are too loose.

**Always look for a conservation law and check it.** It is the cheapest
possible test of a model, and it catches sign errors immediately."""),

    code('''\
A, B, C = sol_hand.y
print(f"A + C  varies by {np.ptp(A + C):.2e}")
print(f"B + C  varies by {np.ptp(B + C):.2e}")

# and the equilibrium constant should come out right
print(f"\\nAt the end:  C/(A*B) = {C[-1]/(A[-1]*B[-1]):.6f}"
      f"   kf/kr = {kf/kr:.6f}")'''),

    md("""---
## 2. The short way: the stoichiometric matrix

Look again at the three derivatives. There are only **two distinct fluxes**:

$$v_1 = k_f[\\mathrm{A}][\\mathrm{B}], \\qquad v_2 = k_r[\\mathrm{C}]$$

and every derivative is a signed sum of those two. Collect the signs into a
matrix. Let $S_{ij}$ be the *net* number of molecules of species $i$ produced
by reaction $j$:

|   | $v_1$ (forward) | $v_2$ (reverse) |
|---|---|---|
| A | $-1$ | $+1$ |
| B | $-1$ | $+1$ |
| C | $+1$ | $-1$ |

Then the entire system is one matrix product:

$$\\frac{d\\mathbf{x}}{dt} = \\mathbf{S}\\,\\mathbf{v}(\\mathbf{x})$$

This is not a notational trick. It is a genuine separation of concerns:

- $\\mathbf{S}$ is **structure** — what the network is. It is a constant
  integer matrix, it comes straight from the reaction list, and it does not
  depend on rate constants, concentrations, or time.
- $\\mathbf{v}(\\mathbf{x})$ is **kinetics** — how fast each reaction runs right
  now. This is where all the biology and all the parameters live.

Keep that split in mind. In **Session 20** we will take exactly this same
$\\mathbf{S}$, throw away the kinetics entirely, and ask a completely different
question of it — *what flux distributions are consistent with steady state?* —
which is flux balance analysis. Same matrix, different question."""),

    code('''\
S = np.array([
    [-1, +1],   # A
    [-1, +1],   # B
    [+1, -1],   # C
])

def fluxes(x):
    A, B, C = x
    return np.array([kf * A * B,    # v1, forward
                     kr * C])       # v2, reverse

def rhs_matrix(t, x):
    return S @ fluxes(x)

sol_matrix = solve_ivp(rhs_matrix, [0, 15], x0, t_eval=t_eval,
                       method="LSODA", rtol=1e-8, atol=1e-10)

# THE POINT OF THIS CELL: are they the same?
diff = np.max(np.abs(sol_matrix.y - sol_hand.y))
print(f"max difference between the two formulations: {diff:.3e}")
assert diff < 1e-9, "These should be identical to numerical precision!"
print("Identical. The matrix form is bookkeeping, not approximation.")'''),

    md("""---
## 3. The shorter way: `posb.Model`

Building $\\mathbf{S}$ by hand is fine for three species and two reactions. It
is miserable and error-prone for thirty species and forty reactions, which is
roughly where we will be by November.

So `posb` does that bookkeeping. You give it a reaction list; it constructs
$\\mathbf{S}$ and evaluates $\\mathbf{S}\\mathbf{v}$.

**Nothing else.** Open `posb/core.py` and read `_build_S` — it is nine lines,
and it does precisely what you just did by hand."""),

    code('''\
from posb import Reaction, Model

model = Model(
    [
        Reaction({"A": 1, "B": 1}, {"C": 1}, k=kf, name="forward"),
        Reaction({"C": 1}, {"A": 1, "B": 1}, k=kr, name="reverse"),
    ],
    species=["A", "B", "C"],     # fixes the row order of S
)

print(model.summary())'''),

    code('''\
# Same initial conditions, same time span — and check against the hand version.
traj = model.simulate({"A": 1.0, "B": 1.5, "C": 0.0}, (0, 15), n_points=400)

diff = np.max(np.abs(traj.y - sol_hand.y))
print(f"max difference from the hand-written version: {diff:.3e}")
assert diff < 1e-9
print("Identical again.")

fig, ax = plt.subplots(figsize=(6.5, 4))
for name in ["A", "B", "C"]:
    ax.plot(traj.t, traj[name], lw=2, label=name)
ax.set_xlabel("time"); ax.set_ylabel("concentration")
ax.set_title("Same system, three lines of specification")
ax.legend(); plt.show()'''),

    md("""Note what `Model` gives you beyond brevity:

- `traj["A"]` — access by name, so you cannot silently mix up row order
- `model.S` — the matrix is right there to inspect
- `model.summary()` — prints the network, useful when a model gets big
- errors that name the species you got wrong

That last one matters more than it sounds. Most of the debugging time in this
kind of work goes to index bookkeeping, not to science."""),

    md("""---
## 4. Worked example: a gene expression cascade

Now the real thing — the model underneath most of this course.

A gene is transcribed to mRNA at constant rate $\\alpha$. mRNA is degraded at
rate $\\gamma_m$. Each mRNA is translated to protein at rate $k_p$. Protein is
removed at rate $\\gamma_p$ (degradation **and** dilution by growth — we will
take that apart properly in Session 5).

As reactions:

$$\\varnothing \\xrightarrow{\\alpha} m \\qquad
m \\xrightarrow{\\gamma_m} \\varnothing \\qquad
m \\xrightarrow{k_p} m + p \\qquad
p \\xrightarrow{\\gamma_p} \\varnothing$$

Note the third one carefully: **translation does not consume the mRNA.** The
mRNA appears on both sides, so its net stoichiometry is zero. This is exactly
the catalyst pattern, and getting it wrong is the single most common modeling
error in the first two weeks of this course.

Before running anything, work out the steady state on paper. Set both
derivatives to zero:

$$m^* = \\frac{\\alpha}{\\gamma_m}, \\qquad p^* = \\frac{k_p m^*}{\\gamma_p}
= \\frac{k_p \\alpha}{\\gamma_m \\gamma_p}$$

**Always predict before you simulate.** If the simulation disagrees with your
prediction, one of them is wrong, and you want to find out which — a
simulation you cannot check is not evidence of anything."""),

    code('''\
params = {
    "alpha":   10.0,   # transcription,  molecules / min
    "gamma_m":  0.5,   # mRNA turnover,  1 / min   (half-life ~1.4 min)
    "k_p":      4.0,   # translation,    1 / min
    "gamma_p":  0.05,  # protein removal,1 / min   (half-life ~14 min)
}

cascade = Model(
    [
        Reaction({},           {"mRNA": 1},                   k="alpha",   name="transcription"),
        Reaction({"mRNA": 1},  {},                            k="gamma_m", name="mRNA decay"),
        Reaction({"mRNA": 1},  {"mRNA": 1, "protein": 1},     k="k_p",     name="translation"),
        Reaction({"protein": 1}, {},                          k="gamma_p", name="protein decay"),
    ],
    params=params,
    species=["mRNA", "protein"],
)

print(cascade.summary())
print("\\nNote the zero in the mRNA row under v2 — translation is catalytic.")'''),

    code('''\
# Prediction first.
m_star = params["alpha"] / params["gamma_m"]
p_star = params["k_p"] * m_star / params["gamma_p"]
print(f"predicted   mRNA* = {m_star:8.3f}   protein* = {p_star:8.3f}")

traj = cascade.simulate({"mRNA": 0.0, "protein": 0.0}, (0, 200), n_points=800)
final = traj.final()
print(f"simulated   mRNA* = {final['mRNA']:8.3f}   protein* = {final['protein']:8.3f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(traj.t, traj["mRNA"], lw=2, color="C1")
axes[0].axhline(m_star, ls="--", c="k", lw=1, label="predicted $m^*$")
axes[0].set_title("mRNA"); axes[0].legend()

axes[1].plot(traj.t, traj["protein"], lw=2, color="C0")
axes[1].axhline(p_star, ls="--", c="k", lw=1, label="predicted $p^*$")
axes[1].set_title("protein"); axes[1].legend()

for ax in axes:
    ax.set_xlabel("time (min)"); ax.set_ylabel("molecules")
plt.tight_layout(); plt.show()'''),

    md("""### Read the picture

The two species reach steady state on visibly **different timescales**. mRNA is
there within a few minutes; protein takes an hour.

That is not an accident of the numbers I picked — it is the generic situation in
bacteria, where mRNA half-lives are minutes and proteins are effectively stable
and removed mainly by dilution. The separation is roughly tenfold here and can
be much larger in real systems.

This observation is the entire foundation of **Session 4**. When one variable
equilibrates much faster than another, you can often set its derivative to zero
and eliminate it — the quasi-steady-state approximation. That is where
Michaelis–Menten comes from, and where the Hill function comes from, and both
are on PS1.

So look at the two timescales in this plot and ask: *could I have replaced the
mRNA equation with an algebraic relation and gotten the protein curve right?*"""),

    md("""---
## 5. Exercises

These are the technique PS1 will assess. Do them now, while the notebook is
open.

**E1.** Change `alpha` to 20 and predict, **before running**, what happens to
$m^*$ and $p^*$. Then check. Now change `gamma_p` to 0.1 and do the same.
State in one sentence which parameters set the protein steady state and which
set only how fast it gets there.

**E2.** Add a second protein $q$ that is produced from the same mRNA at rate
$k_q = 1.0$ and degraded at $\\gamma_q = 0.2$. Write the reactions, predict
$q^*$, simulate, and confirm.

**E3.** Build $\\mathbf{S}$ by hand for the cascade — write out the $2 \\times 4$
integer array yourself — and check it against `cascade.S` with
`np.array_equal`. Do this before looking at `model.summary()` output.

**E4.** *(247 only)* The dimer $\\mathrm{P} + \\mathrm{P} \\rightleftharpoons
\\mathrm{P}_2$ has stoichiometry 2 on one side. Write the reaction, build the
model, and verify that $[\\mathrm{P}] + 2[\\mathrm{P}_2]$ is conserved. Explain
in one sentence why the factor of 2 appears in the conservation law but the
mass-action flux uses $[\\mathrm{P}]^2$."""),

    code('''\
# E1 — your work here
'''),

    code('''\
# E2 — your work here
'''),

    code('''\
# E3 — your work here
S_by_hand = np.array([
    # fill in: rows are [mRNA, protein], columns are the four reactions
])
# print(np.array_equal(S_by_hand, cascade.S))
'''),

    # E4 is the 247-only item and was the one exercise with no cell to work in.
    # More than half the room is in 247; an exercise with nowhere to answer it
    # reads as an exercise that was not meant seriously.
    code('''\
# E4 — 247 only. P + P <-> P2, and the factor of two.
'''),

    md("""---
## What to take away

1. Every deterministic model in this course is $\\dot{\\mathbf{x}} =
   \\mathbf{S}\\mathbf{v}(\\mathbf{x})$. Structure and kinetics are separable, and
   we will exploit that separation again in Session 20.
2. A species on both sides of a reaction has **zero** net stoichiometry.
   Translation is catalytic in the mRNA.
3. Predict the steady state on paper before you simulate. Check conservation
   laws. A simulation you cannot check independently is not evidence.
4. Widely separated timescales are the norm in gene expression, and they are
   an opportunity — that is Session 4.

**Next:** Session 4, Tuesday September 8 — quasi-steady state, and deriving
Michaelis–Menten and the Hill function rather than asserting them.
**PS1 goes out today and is due Thursday September 10.**"""),
]
