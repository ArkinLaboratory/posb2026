<!--
title: Session 3 — Board notes
subtitle: Every line to write, in order. Thirty-seven minutes of board across eight segments.
session: 3
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written* — the half of the session with the highest load on the room and
no other artefact.

**Thirty-seven minutes across eight segments,** all before minute 74.

**Conventions.** **ASK** — put it to the room before writing the next line, and
the answer to expect. **CHECK** — do it out loud; doing them is the habit being
taught. **IF ASKED** — the question that always comes. **CUT** — drop this first
if you are behind, decided now rather than at minute 70.

<div class="rule"></div>

## The board plan

Dwinelle 219 is blackboard across the front with the projection screen coming
down in the **centre**, leaving a **left wing** and a **right wing**. That is
two working surfaces, not one, and the session is designed around it.

**LEFT WING — the ledger. Written once, never wiped.** Three things, and the
session breaks if any of them is erased:

1. **The matrix**, from segment 4 — $S_{ij}$, the 3 × 2 table with its labels,
   and $\dot{\mathbf{x}} = \mathbf{S}\mathbf{v}$ beneath it. Everything from
   26 to 37 min points back at it; segment 5 is unteachable without it.
2. **The cascade reaction list**, from segment 5 — $\varnothing \to m$,
   $m \to \varnothing$, $m \to m + p$, $p \to \varnothing$. The ConcepTest at
   33 is about its third reaction, the pause at 37 asks for its **S**, and the
   laptops at 51 use it. It must survive from 26 min to 59.
3. **$m^* = \alpha/\gamma_m$, $p^* = k_p\alpha/\gamma_m\gamma_p$, 20 and
   1600**, from segment 6. Segments 7 and 8 both point at them.

**RIGHT WING — the workings. Wiped between segments:** the collision dots, the
Damköhler arithmetic, the integrating factor, the nondimensionalisation. The
one exception is the three longhand derivatives from segment 3 — **wipe those
only once the matrix is on the left wing**, because segment 4 is the act of
watching them reappear as $\mathbf{S}\mathbf{v}$.

The screen is down all session, so what is projected is central and what you
write is peripheral: the lit rectangle wins by default, and when you want the
room looking at the board you have to say so. Check from the back row before
class that the outer third of each wing reads, and keep the matrix inboard
rather than at the far edge.

Running board time is in each heading. More than three minutes behind at the
37-minute mark: take the first CUT.

<div class="rule"></div>

## 1 · 8–13 min — Where mass action comes from

**Board 1 of 8 · 5 min · cumulative 5**

Draw a box. Put two dots labelled A and three labelled B in it.

> **ASK:** *How many distinct A–B pairs can meet?*
> Expect a beat, then "six." Write **2 × 3 = 6**.

Add one more A.

> **ASK:** *Now?* — "nine." Write **3 × 3 = 9**.

Now write:

$$\text{encounters per second} \;\propto\; [\mathrm{A}]\,[\mathrm{B}]$$

Say: the proportionality is *counting pairs*. Nothing chemical has happened yet.

Then the rate law:

$$v \;=\; k\,[\mathrm{A}][\mathrm{B}]$$

> Say explicitly what $k$ absorbs: how often an encounter has enough energy, the
> right orientation, a catalyst present, the solvent, the temperature. **Every
> assumption in this model is hiding in that one letter.**

Then the coefficient point. Write the dimer:

$$\mathrm{P} + \mathrm{P} \rightarrow \mathrm{P}_2 \qquad v = k[\mathrm{P}]^2$$

> Say: the stoichiometric coefficient enters the **flux as a power** and the
> **balance as a multiplier**. Same number, two different jobs. Confusing them is
> exercise E4 and it is the single most common algebra error in the course.

> **IF ASKED** *"why not $2[\mathrm{P}]$?"* — because you are counting pairs of
> P, and the number of pairs among $n$ objects goes as $n^2$, not $2n$. Go back
> to the dots.

**CUT:** the dimer paragraph — repeated in segment 5 and in E4. At five minutes
rather than six, expect to take it.

<div class="rule"></div>

## 2 · 13–17 min — Is mass action allowed in an *E. coli*?

**Board 2 of 8 · 4 min · cumulative 9**

Three columns on the board. Head them **well mixed**, **dilute**, **many**.

### Well mixed — do this one live

$$\tau_{\text{mix}} \;\sim\; \frac{L^2}{2D} \;=\; \frac{(1\ \mu\mathrm{m})^2}{2 \times 7.7\ \mu\mathrm{m^2\,s^{-1}}} \;\approx\; 0.065\ \mathrm{s}$$

$$\tau_{\text{rxn}} \;\sim\; \frac{1}{k_{\text{on}} C} \;=\; \frac{1}{10^{8}\ \mathrm{M^{-1}s^{-1}} \times 10^{-9}\ \mathrm{M}} \;\approx\; 10\ \mathrm{s}$$

$$\mathrm{Da} \;=\; \frac{\tau_{\text{mix}}}{\tau_{\text{rxn}}} \;\approx\; 0.007$$

> Both numbers came from Tuesday. Say that.
>
> **Verdict: passes, by three orders of magnitude.** A molecule crosses the cell
> hundreds of times before it reacts, so there is no gradient to speak of.

> **IF ASKED** *"is $10^8$ right?"* — that is diffusion-limited, the fastest
> possible. A typical protein–protein association is $10^5$–$10^6$, which makes
> $\tau_{\text{rxn}}$ **longer** and Da **smaller**. The conclusion is robust in
> the direction that matters.

### Dilute — one line, no derivation

20% protein by weight. Excluded volume raises the activity of a large complex
above its concentration; reported shifts run to about an order of magnitude for
large complexes. **Verdict: bends.** $k$ absorbs it — which is fine right up
until you drop an *in vitro* $k$ into a model of a cell without saying so.

*(Mark this one as a range, not a measurement. It is the claim on this slide
with the shortest shelf life.)*

### Many — the one that fails

$$1\ \mathrm{nM} \approx 1\ \text{molecule per cell} \quad\Longrightarrow\quad N = 1, \qquad \frac{1}{\sqrt{N}} = 1$$

> **Verdict: fails outright.** Not approximately — the quantity the ODE
> integrates does not describe any single cell.

**Land this:** the three answers disagree, and not in the way anyone guesses.
The spatial assumption — the one that *feels* shakiest in a crowded cell — is
the one that passes most comfortably. What fails is counting, which is exactly
what Session 2 said would fail.

> Then the honest statement of the next ten weeks, in one sentence:
> *we are going to integrate the mean of a process whose fluctuations are of
> order one, and it works because we mostly ask whether a design can work at
> all.* Session 12 is where the mean stops being enough.

<div class="rule"></div>

## 3 · 17–21 min — The long way

**Board 3 of 8 · 4 min · cumulative 13**

Write the reaction, then the three derivatives — **and write them, do not show
the slide**. The rhetorical move in segment 4 depends on the room having *felt*
the repetition.

$$\mathrm{A} + \mathrm{B} \underset{k_r}{\overset{k_f}{\rightleftharpoons}} \mathrm{C}$$

$$\frac{d[\mathrm{A}]}{dt} = -k_f[\mathrm{A}][\mathrm{B}] + k_r[\mathrm{C}]$$

$$\frac{d[\mathrm{B}]}{dt} = -k_f[\mathrm{A}][\mathrm{B}] + k_r[\mathrm{C}]$$

> **ASK** before writing the third line: *what is* $d[\mathrm{C}]/dt$? They will
> get it. **That is the point** — they already know the content, and what is
> coming is only bookkeeping.

$$\frac{d[\mathrm{C}]}{dt} = +k_f[\mathrm{A}][\mathrm{B}] - k_r[\mathrm{C}]$$

Circle the two distinct fluxes. Say: **two fluxes, six terms, every term is one
of those two with a sign.** Then: thirty species and forty reactions is where
this course is by November — 1200 potential terms, each an opportunity for a
sign error you will not find.

<div class="rule"></div>

## 4 · 21–26 min — Two fluxes, one matrix

**Board 4 of 8 · 5 min · cumulative 18**

$$v_1 = k_f[\mathrm{A}][\mathrm{B}], \qquad v_2 = k_r[\mathrm{C}]$$

Draw the empty table. **Take the entries from the room, one row at a time.**

| | $v_1$ | $v_2$ |
|---|---|---|
| A | $-1$ | $+1$ |
| B | $-1$ | $+1$ |
| C | $+1$ | $-1$ |

> **ASK** for the A row. Then the B row — **they will notice it is identical**,
> and that is worth naming out loud rather than passing over. Then C.

Define it properly:

$$S_{ij} = \text{net molecules of species } i \text{ produced by reaction } j$$

$$\frac{d\mathbf{x}}{dt} = \mathbf{S}\,\mathbf{v}(\mathbf{x})$$

> **Now multiply it out, row by row, out loud.** Row A gives
> $-v_1 + v_2$. Substitute the fluxes and the first equation from segment 3
> reappears on the board next to it. **That moment is the session.** Do not
> rush it and do not narrate over it.

Then the split, in two sentences: $\mathbf{S}$ is **structure** — a constant
integer matrix off the reaction list, knowing nothing about rate constants,
concentrations or time. $\mathbf{v}$ is **kinetics** — every parameter and all
of the biology.

<div class="rule"></div>

## 5 · 26–33 min — Both null spaces

**Board 5 of 8 · 7 min · cumulative 25 · the longest, and the one to protect**

### Left first

$$\mathbf{w}^{\mathsf{T}}\mathbf{S} = \mathbf{0} \quad\Longrightarrow\quad \frac{d}{dt}\left(\mathbf{w}^{\mathsf{T}}\mathbf{x}\right) = \mathbf{w}^{\mathsf{T}}\mathbf{S}\mathbf{v} = 0 \quad \text{for any } \mathbf{v}$$

> Three symbols, and it is the whole theorem. Say "for **any** v" twice — the
> result does not care about the kinetics at all.

> **ASK:** *find me a $\mathbf{w}$.* Give them thirty seconds. Expect
> $(1,0,1)$ and $(0,1,1)$.

$$[\mathrm{A}] + [\mathrm{C}] \quad\text{and}\quad [\mathrm{B}] + [\mathrm{C}] \quad\text{are conserved}$$

Note the rank: the two columns of $\mathbf{S}$ are negatives of each other, so
$\operatorname{rank}\mathbf{S} = 1$. Forward and reverse are not independent
reactions. Hence

$$\dim(\text{left null}) = n - \operatorname{rank}\mathbf{S} = 3 - 1 = 2 \;\checkmark$$

### Right next — this half is new to almost everyone

$$\mathbf{S}\mathbf{v} = \mathbf{0}, \quad \mathbf{v} \neq \mathbf{0}$$

> Say the question in words first: **which patterns of reaction rates leave
> every concentration unchanged?**

For $\mathrm{A} + \mathrm{B} \rightleftharpoons \mathrm{C}$: $-v_1 + v_2 = 0$,
so $v_1 = v_2$. One flux mode, and
$\dim = r - \operatorname{rank}\mathbf{S} = 2 - 1 = 1$.

### Then the cascade, as the contrast

$$\varnothing \xrightarrow{\alpha} m \qquad m \xrightarrow{\gamma_m} \varnothing \qquad m \xrightarrow{k_p} m + p \qquad p \xrightarrow{\gamma_p} \varnothing$$

$$\mathbf{S} = \begin{pmatrix} +1 & -1 & 0 & 0 \\ 0 & 0 & +1 & -1 \end{pmatrix}, \qquad \operatorname{rank} = 2$$

$$\dim(\text{left null}) = 2 - 2 = 0, \qquad \dim(\text{right null}) = 4 - 2 = 2$$

> **ASK before you say it:** *no conservation laws at all — what does that mean
> physically?* Answer: it is an **open system**. Matter is synthesised from
> nothing and degraded to nothing, so nothing can be conserved. That is not a
> defect in the model, it is the model being about a cell.
>
> The two flux modes: transcription balancing mRNA decay, and translation
> balancing protein decay. **The two independent balances, read straight off
> the matrix without solving anything.**

**Close the segment with one sentence and do not elaborate:**

> *Flux balance analysis is the right null space, plus bounds on $\mathbf{v}$,
> plus an objective. That is all it is. Session 20.*

> **IF ASKED** *"how do you find these in practice?"* — `scipy.linalg.null_space`
> on $\mathbf{S}$ and on $\mathbf{S}^{\mathsf{T}}$. One line each. Do not open a
> laptop here.

**CUT:** the cascade contrast. Keep left, right, and the FBA sentence.

*Then ConcepTest 1 at 33–37 and the pause at 37–39: the vote asks for the
mRNA's stoichiometry in m → m + p, the pause asks for the cascade's **S**,
where that is the third column. The adjacency is the point — do not overrun.*

<div class="rule"></div>

## 6 · 59–63 min — The steady state, without a computer

**Board 6 of 8 · 4 min · cumulative 29**

$$\frac{dm}{dt} = \alpha - \gamma_m m = 0 \quad\Longrightarrow\quad m^* = \frac{\alpha}{\gamma_m}$$

> The move worth naming: **a cascade solves top-down.** $m^*$ does not contain
> $p$, so solve it alone and substitute. First appearance of a structure they
> will use constantly.

$$\frac{dp}{dt} = k_p m^* - \gamma_p p = 0 \quad\Longrightarrow\quad p^* = \frac{k_p \alpha}{\gamma_m \gamma_p}$$

Numbers: $\alpha = 10$, $\gamma_m = 0.5$, $k_p = 4$, $\gamma_p = 0.05$ give
$m^* = 20$ and $p^* = 1600$.

> **IF ASKED / IF OFFERED** *"$p^*$ doesn't depend on the initial conditions at
> all"* — correct, and it is Session 8's territory: one globally stable fixed
> point. Say the phrase, move on.

<div class="rule"></div>

## 7 · 63–67 min — Integrate it exactly

**Board 7 of 8 · 4 min · cumulative 33**

The only closed-form integration in the course. Do every line.

$$m(t) = m^*\left(1 - e^{-\gamma_m t}\right)$$

$$\frac{dp}{dt} + \gamma_p p = k_p m(t)$$

Multiply by the integrating factor $e^{\gamma_p t}$:

$$\frac{d}{dt}\left[p\,e^{\gamma_p t}\right] = k_p m(t)\, e^{\gamma_p t}$$

> Say: **this is the move**, and it comes back in Session 5 for response time
> and Session 11 for the delayed oscillator.

Integrate and rearrange:

$$p(t) = p^*\left[1 - \frac{\gamma_m e^{-\gamma_p t} - \gamma_p e^{-\gamma_m t}}{\gamma_m - \gamma_p}\right]$$

> **CHECK 1, out loud:** at $t = 0$ the bracket is
> $(\gamma_m - \gamma_p)/(\gamma_m - \gamma_p) = 1$, so $p(0) = 0$. ✓
>
> **CHECK 2:** as $t \to \infty$ both exponentials die and $p \to p^*$. ✓
>
> Ten seconds each, and they are the habit being taught.

**Two exponentials, not one.** The protein does not simply relax at $\gamma_p$;
it also carries the mRNA's rise.

> **IF ASKED** *"what if $\gamma_m = \gamma_p$?"* — somebody always asks. It is a
> **removable singularity**; the limit exists,
> $p = p^*\left[1 - (1 + \gamma t)e^{-\gamma t}\right]$, and physically it is the
> critically damped case: the two relaxation modes have collided. Comes back as
> repeated eigenvalues in Session 8. **If nobody asks, say it anyway.**

<div class="rule"></div>

## 8 · 70–74 min — Four parameters become one

**Board 8 of 8 · 4 min · cumulative 37**

$$\tau = \gamma_p t, \qquad \mu = \frac{m}{m^*}, \qquad \pi = \frac{p}{p^*}$$

Derive both, two lines each — do not display them.

$$\frac{dm}{dt} = \alpha - \gamma_m m \;\Big/\, m^* \;\Longrightarrow\; \frac{d\mu}{dt} = \gamma_m(1 - \mu) \;\xrightarrow{\ \tau = \gamma_p t\ }\; \frac{d\mu}{d\tau} = \frac{1}{\epsilon}(1-\mu)$$

$$\frac{d\pi}{d\tau} = \mu - \pi, \qquad \boxed{\;\epsilon = \frac{\gamma_p}{\gamma_m}\;}$$

**Land the parameter count, plainly:** you started with four parameters and you
now have one. Two cascades with wildly different rate constants and the same
$\epsilon$ give the *same curve* after rescaling — so **no experiment measuring
the shape alone can tell them apart.** That is a real and slightly unwelcome
result; let the 247 half sit with it.

Then the punchline, and hand straight to the slide:

$$\epsilon \to 0 \;\Longrightarrow\; \mu = 1 \text{ instantly} \;=\; \textbf{the quasi-steady-state approximation}$$

Ours is $\gamma_p/\gamma_m = 0.05/0.5 = 0.1$.

> **IF ASKED** whether this has a name — Buckingham Pi, without the ceremony.
> Say so only if someone raises it; do not introduce it.

<div class="rule"></div>

## If you are running late

Take them in this order. Each is chosen so nothing downstream breaks.

1. **The dimer paragraph in segment 1** (30 s). Repeated in segment 5 and E4.
2. **The cascade contrast in segment 5** (2 min). Keep left null, right null and
   the FBA sentence — those three are what Session 20 needs.
3. **CHECK 2 in segment 7** (20 s). Keep CHECK 1; one sanity check taught
   properly beats two done at speed.
4. **The degeneracy discussion in segment 7** (30 s) — *only* if nobody asked.

Do **not** cut segment 8. It is what makes Session 4 a derivation rather than a
recipe, and it is four minutes.
