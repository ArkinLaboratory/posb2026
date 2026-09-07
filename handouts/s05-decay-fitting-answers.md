<!--
title: Session 5 — Getting a removal rate out of decay data: answers
subtitle: Items 1 and 2, worked. Items 3 and 4 are PS2; those solutions post to bCourses after the deadline.
session: 5
-->

# Answers — items 1 and 2

This is the key to the two items we did **in the room**. Items 3 and 4 of your
handout are **PS2 Q2 and Q5**; their worked solutions post to bCourses after the
deadline, not here.

If your slope differs from mine in the third decimal, you are fine — you read it
off a table of seven noisy points. The prose under each **▶** is the part worth
reading. The arithmetic was never the hard bit.

<div class="rule"></div>

<div class="q" markdown="1">

## 1 · LAA — the whole procedure

$$\text{slope} = \frac{2.17 - 4.62}{60 - 0} = -0.0408 \ \text{min}^{-1}
\quad\Longrightarrow\quad k = \gamma + \mu = 0.0408 \ \text{min}^{-1}$$

$$t_{1/2} = \frac{\ln 2}{k} = \frac{0.693}{0.0408} = \mathbf{17.0 \ \text{min}}$$

A least-squares fit to all seven points gives $k = 0.0406$, $t_{1/2} = 17.1$ min.
Two points and seven points agree here because the data really are exponential;
they would not agree if the model were wrong, which is the reason to look.

**▶ Why fit $\ln y$ and not $y$?**

Because the **error is proportional to the signal**, not constant. A
fluorescence measurement is a ratio — counts per cell, or counts against a
reference — so a reading of 100 carries roughly ten times the absolute
uncertainty of a reading of 10, and about the same *relative* uncertainty.
Taking logs turns proportional error into **constant** error, which is the
assumption ordinary least squares actually makes.

Fit $y$ directly and you have not merely chosen a clumsier method: you have
weighted the early, large points far more heavily than the late ones, and the
late points are where the exponential is doing its most discriminating work.
The estimate is biased, not just noisier.

*(This is also why the synthetic data carry lognormal noise rather than
Gaussian. The generator and the estimator agree about what a fluorescence
measurement is.)*

</div>

<div class="rule"></div>

<div class="q" markdown="1">

## 2 · AAV — and what the number is not

| $t$ (min) | 0 | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|---|
| $y$ | 100.4 | 68.0 | 51.7 | 35.4 | 24.4 | 17.3 | 12.4 |
| $\ln y$ | 4.61 | 4.22 | 3.95 | 3.57 | 3.19 | 2.85 | 2.52 |

$$\text{slope} = \frac{2.52 - 4.61}{60} = -0.0348 \ \text{min}^{-1}
\quad\Longrightarrow\quad
k = 0.0348 \ \text{min}^{-1}, \qquad
t_{1/2} = \frac{0.693}{0.0348} = \mathbf{19.9 \ \text{min}}$$

**▶ Is that $\gamma$ or $\gamma + \mu$?**

$\gamma + \mu$. The sentence that decides it is *"the cells keep growing
throughout"* — production is stopped, but division is not, so both removal
processes are running and what you see is their sum. **Nothing in the fit can
separate them.** The model is a single exponential either way; one number comes
out, and which quantity it is depends entirely on how the experiment was run.

**▶ Recovering Andersen's number.**

$$\gamma = k - \mu = 0.0348 - 0.0231 = 0.0117 \ \text{min}^{-1}$$

$$t_{1/2}^{\,\text{deg}} = \frac{\ln 2}{\gamma} = \frac{0.693}{0.0117}
= \mathbf{59 \ \text{min}}$$

which is Andersen's 60, to the precision seven noisy points support. The loop
closes: a published degradation half-life plus your own growth rate predicts the
decay you measure, and the measured decay minus your growth rate returns the
published half-life.

**▶ Why are Andersen's numbers transferable and yours are not?**

He measured after a **medium downshift**, which arrests growth: $\mu \to 0$, and
what is left is proteolysis alone. His numbers therefore carry **no growth rate
inside them**, so they can be added to the $\mu$ of whatever host you are using.

A half-life measured in growing cells — like the 19.9 min you just fitted —
carries *someone else's doubling time* baked in. Quote it to a colleague working
in minimal medium and it is wrong, in a direction they cannot recover, because
the paper did not tell them what to subtract.

> **The habit:** when you read a half-life, ask what was growing. Most papers do
> not say, and the two quantities differ here by a factor of three.

</div>

<div class="rule"></div>

## The one line to carry out of this

$$\text{a slope is a rate} \qquad
\text{a rate is not a half-life} \qquad
t_{1/2} = \frac{\ln 2}{\gamma + \mu}$$

Dilution sets a floor no tag can go below: in a cell dividing every 30 minutes,
an *undegradable* protein still has a 30-minute half-life. Every tag you add
buys speed by moving $\gamma$ up, and pays for it in steady-state level, which
falls as $\mu/(\gamma + \mu)$. That trade is item 3, and it is PS2 Q2.
