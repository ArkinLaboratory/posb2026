# Symbols — what each letter means, and where it is already taken

[← back to lecture-design](lecture-design.md)

**Seeded 8 November 2026 from week 13's collisions.** Not yet a complete
course-wide audit: it records the letters that have actually collided, the
resolutions, and the ones that are spoken for. Extend it when the next
collision turns up rather than rediscovering the same clash.

> **Why this file exists.** `deck-bar.md` §B2 asks for *one alphabet per
> quantity, deck-wide*, and §B1 says a symbol defined only in a note is not
> defined. Both were being satisfied by writing a disambiguating line in a
> slide foot — which is the thing B1 rules out. A foot note tells the room the
> collision exists; it does not remove it. So the collisions get renamed, and
> the renames get recorded here so the next session does not undo them.

---

## Spoken for — do not reuse

| symbol | means | where it is established |
|---|---|---|
| **λ** | **eigenvalue** | s08 phase plane, s11 oscillators, s14 review. **T29 is autograded on PS5**, so this one cannot move. |
| **λ** | CD4⁺ birth rate, 31 cells µl⁻¹ d⁻¹ | s25 — Weinberger's own printed symbol, Table 1. Cannot move. |
| **θ** | the antithetic set-point ratio | s22 control |
| **β_L, β_C** | Basu's two printed repression thresholds, in µM | s24 move 3 |
| **γ** | decay rate, of a signal or a protein | throughout |
| **K₁, K₂** | the Balagaddé deposit's half-saturation constants | s24 move 4, quoted |
| **P** | packaging advantage, crHIV-1 : HIV-1 intracellular ratio | s25. **T67 and T73 are autograded**, so this cannot move. |
| **D** | the inhibition knob; D = 1 is *no* inhibition | s25, Weinberger's. Autograded with T73. Cannot move. |
| **n** | burst size | s25, and s24's Hill coefficient — distinguished by context, no slide carries both |

## Resolved collisions

### λ as a length → **ℓ_A** · session 24, move 2
Penetration depth is `ℓ_A = √(D/γ_A)`. It was λ, which already means an
eigenvalue in three earlier sessions and a birth rate in the next one. λ as an
eigenvalue is assessed on PS5 and cannot move; Weinberger's λ is printed in the
paper and cannot move; so the length moves. **`\ell` appears nowhere else in
the repo**, and the `_A` subscript matches `γ_A`, so the pair reads together:
A's decay rate and A's decay length.

### bare θ → **θ_A** · session 24, move 1
The receiver's half-output concentration. s22 already uses bare θ, and session
24 also carries Tsoi's **θ_I** in move 5, so neither of session 24's two thetas
is written bare. Subscripts are parallel and self-documenting: θ_A is the A
concentration at half output, θ_I is Tsoi's **inefficiency factor**
(NUMBERS §11.5, sourced to p.2528 -- this file said "intermediate
threshold" until 8 November, which was wrong; the subscript is for
INEFFICIENCY, not intermediate).

### Tsoi's burden → **B**, and **B₁ / B₂** per enzyme · session 24, move 5
Tsoi writes it `βe₁ + γe₂`. γ is decay throughout this course, and the obvious
dodge — writing the burden as β — is **worse**, because session 24 already
carries β_L and β_C as Basu's printed thresholds in µM, and a dimensionless
burden sharing that letter would collide inside one hour instead of across the
course. So **B** for the total burden, with the
slide saying once that Tsoi writes βe₁ + γe₂. **Per enzyme versus total -- get this right or the verdict flips.** `dol_criterion` takes **per-enzyme** burdens, named `beta_e1` and `gamma_e2` in its signature, and the single cell carries their **sum**. So B1 and B2 are per enzyme, **B = B1 + B2** is the total the single cell carries, and that total is what `fig_dol`'s axes plot
(`dol_criterion(B₁, B₂, …)`) and the single cell carries the sum — a slide
quoting a total where the model was given a per-enzyme value is off by a factor
of two and **reverses the answer** -- verified: pathway A at B1 = B2 = 1.2 gives
`dol_favored = True`, and the same 1.2 misread as a pathway total gives `False`.
Every printed burden says which it is. The per-enzyme borders are 1.135146 and
1.355143; the figure's total-burden crossing is 2.27.

### Noble's homing efficiency → **h** · session 25, segment 5
Noble writes it P, which is this session's packaging advantage and is autograded
on two techniques. The gene-drive material is guide-and-final and hand-graded,
so the cheaper side moves: **h**. Noble's cropped figures still axis-label it P,
so the slide carrying a crop says once that Noble's P is our h. The invasion
boundary is `f > 1/(1+h)`.

### Noble's alleles → never a bare letter · session 25, segment 5
W, D and R are Noble's allele names and they are on his cropped figures, so
renaming them would make our slide contradict the figure beside it. The
collision only exists when **D** stands alone and could be read as the
inhibition knob. So alleles are written as **genotypes** — WW, WD, DD, DR — or
as noun phrases, "the W gamete", "the resistant allele". A genotype pair cannot
be mistaken for a scalar. **No slide in session 25 writes a bare allele letter
as if it were a quantity.**

---

## The worst trap here is not a collision — it is an ORDER

**Neither of the renames above is the most dangerous thing in this session.**
The packaging ratio is, and it is not a collision at all: it is the same ratio
written in two orders, both correct.

- `posb/populations.py` writes it **crHIV-1 : HIV-1 = P : 1**
- the figures and `NUMBERS.md` §3 write it **HIV-1 : crHIV-1 = 1 : P**

Both give `q = P/(1+P)`, which is what `diploid_packaging` computes. **Read
either one backwards and q becomes 1/(1+P), which inverts every genotype
probability in the session** — and T67, the binomial partition, is autograded.

I nearly broke the library over this: a report that the two files "disagreed"
was taken on trust and the docstrings were edited to match, which made a
correct line false. The lesson generalizes past this symbol — **a reported
inconsistency between two files needs the same verification as a reported fact,
because "these disagree" is itself a claim.**

**The rule: never state this ratio without naming which species comes first.**
Write "1 HIV-1 to P vector", or "crHIV-1 : HIV-1 = P : 1" — never a bare
"1 : P". That now holds in the library's docstrings, the figures, the deck and
the design.

### `s25_locus_1` / `s25_locus_2` print h directly, and that is deliberate
It is **our** figure, not a crop, so it uses our letter. Noble's *cropped*
figures still axis-label the same quantity P, because we do not alter published
panels, and the slide carrying a crop says so once. **Do not "restore" P to
`s25_locus_1` / `s25_locus_2` for consistency with the crops** — the inconsistency is the
honest part, and the bridge line is what reconciles it.

## CLOSED 8 November: the projector draws the script ell

Adam opened `s24-communities.pptx` in PowerPoint on the Mac and sent back
slides 23, 24 and 88. **U+2113 renders correctly** -- script ell with its
subscript, in the figure, in the step stack and in the ledger row. The
subscripted-Greek-lambda fallback below is **not needed** and is kept only as
a record of the decision. The original note follows.

### The original open risk

**It is U+2113, and it has never been rendered on the Dwinelle projector** --
this registry's own claim that `\ell` appears nowhere else in the repo is
exactly why. Two things follow.

- **Figures are safe.** matplotlib draws it from DejaVu, which carries it.
- **Deck text is unverified.** `theme.py`'s `MISSING_GLYPHS` is a **blacklist**,
  so a clean "0 missing glyphs" means U+2113 is *not in the table* -- not that
  Calibri carries it. The Linux VM the build runs on has neither Calibri nor
  Cambria, so a successful PDF export there proves the pipeline, not the font.

**To settle it:** open `s24-communities.pptx` in PowerPoint on the Mac and look
at slides 23, 24 and 88. A missing glyph renders as an empty box.

**If Calibri lacks it, the fallback is a subscripted Greek lambda** -- it
certainly renders, since the course sets Greek throughout. It is weaker than the
script ell because it reuses the eigenvalue letter, but session 24 writes its
eigenvalues as `Re` and `Im` of lambda rather than lambda-sub-1 and
lambda-sub-2, so a subscripted form stays distinguishable. Decide it once and
record it here; do not leave a deck depending on an untested glyph.

### `D` as a diffusion coefficient → **D_A** · session 24 · APPLIED 8 Nov

Applied across 16 occurrences (slides 2, 16, 19, 20-23, 25, 88, 89, 94, 96)
and five figure strings. A bare `D` now means the reactor's **dilution rate**
everywhere in session 24; the signal's diffusion coefficient is `D_A`, which
sits with `ell_A`, `gamma_A` and `theta_A`.

**The tie-breaker I first gave for this was wrong and is recorded so nobody
re-derives it.** I argued the dilution rate should keep the bare letter
because it is autograded on PS9. It is -- and so is **T66, the diffusion
length scale**, by this deck's own docstring. Both sides land on PS9, so that
rule does not discriminate here. The decision is still right, for a different
reason: **`problem-sets/` stops at `ps08`, so PS9 does not exist yet.** The
deck therefore *sets* the convention PS9 will be written against, and nothing
has to be re-keyed either way. When both sides of a collision are assessed,
ask which artefact already exists, not which is assessed.

Two things the first inventory of this collision also missed, both found only
by editing the deck: **slide 2 carries `t ~ L^2/2D`**, which is the symbol's
first appearance in the hour and is therefore where the rename bridge belongs;
and **`D = 7.7 um^2/s for GFP` on slide 16 cannot become `D_A`**, because `A`
is the AHL signal and GFP in cytoplasm is not it. That one drops the letter
and reads "at 7.7 um^2/s for GFP" -- a rename that would assert something
false is not a rename, it is a new defect.

### Tsoi's transport inefficiency → **eps_T** · session 24 · APPLIED 8 Nov

Applied on slides 78, 82 (table header) and 93, plus the release docstring.
Session 4's `eps` keeps the bare letter. **Tsoi's own panel still prints a
bare `eps`**, and published panels are not altered, so slide 78 carries a
bridge line saying the panel's `eps` is our `eps_T`.

**A related reading trap, recorded here because it is a glyph and not a
collision:** Tsoi sets `upsilon` in an italic that reads as a Latin `v`. The
quantity is **biomass** (NUMBERS §11.5: steady-state cell volume, proportional
to total biomass; §11.7 gives `upsilon_bar_DOL = sqrt(upsilon_1 upsilon_2)`,
and the panel's own annotation reads "Gain in biomass through DOL"). I called
it a *flux* when briefing the slide-78 repair, and had that not been checked
against NUMBERS it would have put a new false claim on the slide the last 25
slides of the session turn on.

## The five this file missed, found by front-to-back critics on 8 November

**Read the next section before reading these.** The first pass found five
collisions and missed at least five more, and the miss was systematic, not
unlucky.

### `D` as a diffusion coefficient → **D_A** · session 24

`D` is the **dilution rate** on slides 11, 51-71 and 87, and the **diffusion
coefficient** on 16-19, 23-25, 89 and 94-96. The two meet on **slide 88, two
rows apart**: "the medium - gamma_A ... which moves ell_A = sqrt(D/gamma_A)"
sits beside "the vessel and the plate - D, which you can still change after
the strains are built". **Slide 89 then opens CONSTRAINTS with "the
coefficient - D itself: pick a signal and inherit it."** So the closing ledger
calls D a knob and, four slides later, a thing that is set for you. Both rows
are individually correct. Read front to back they are a flat contradiction,
and it is on the ledger slides, which are what students photograph.

**The diffusion coefficient moves, to `D_A`.** It already sits among `ell_A`,
`gamma_A` and `theta_A`, so the subscript is the convention the session
already uses; it is the cheaper side (11 slides against ~23); and the dilution
rate is the course convention from session 11 and is autograded on PS9 and the
final, so by this file's own rule it is the one that stays.

**Knock-on, and the reason this one hid for so long:** slide 54's "D appears
four times" and slide 70's "D appears in four places" are *only true under a
partition nothing on any slide told the room about*. Both read as correct to
anyone already holding the distinction, which is why every reader who knew the
material passed over them. After the rename they are true as written.

**Still open: slide 101 carries a third `D`** - Weinberger's inhibition knob,
in the session 25 reading assignment, unflagged, after the other two.

### Tsoi's transport inefficiency → **eps_T** · session 24, move 5

`eps` is session 4's ratio of two clocks on slides 55 and 61, where the whole
punchline is *"eps was meant to be small. It is about 6 and about 2 - correct
algebra on a false premise."* It is then `delta_me/eta` on 78, 79, 81, 82 and
93, **with its own column in the table on slide 82**, taking values 0, 0.001
and 0.5.

A student who has just been taught *small eps licenses the reduction* reads
slide 82's eps column as a validity check and concludes Tsoi's own criterion
is marginal for pathway B. The verdict on 61 is seventeen slides fresher than
anything that would tell them otherwise.

**Tsoi's moves, to `eps_T`** - T for **transport**, not for the author, so the
subscript says what the quantity is and does not pretend to the same scheme as
`theta_I`. Session 4's keeps the bare letter: it has the prior course meaning
and it is the one the room has been carrying since September.

### `n` carries two exponents in session 24, and two burst sizes in session 25

**Session 24:** the receiver's Hill sharpness on slide 12, and Tsoi's burden
exponent on 80, 81 and 83. **Session 25:** "how many draws - session 2: n = 5,
today: n = 2" on slide 15, then "n is the burst size ... n = 200" from slide
29 onward, for the rest of the hour.

Session 25 slide 52 carefully disarms *session 12's* translational burst
against today's `n` - which is the exact slide where the within-hour collision
belonged, and it is not there. **Unresolved; both need a decision.** The cheap
move in s25 is to stop calling the two-strands-per-capsid count `n` at all
(say "two", it is a count, not a parameter).

### `lambda` is an eigenvalue and a birth rate inside session 25's own deck

The first pass recorded that s25 uses `lambda` for Weinberger's CD4+ birth
rate and renamed the *length* to `ell_A` on that basis. It did not notice that
**s25's own slide 2 prints "leading Re lambda (h^-1)" on its y-axis** - the
eigenvalue, carried in from session 24 - and **slide 31 writes "T = lambda/d =
1550/ul" with a 16pt gray aside calling lambda a birth rate.** Twenty-nine
slides apart, in one hour, with nothing said. The deck disarms two D's, two
burst sizes, Noble's P and session 23's s, and misses the one collision it
created itself.

**Unresolved.** The cheap fix is one line on slide 31 rather than a rename.

### `f` is used four times in session 25 and defined nowhere

Not a collision - an omission, recorded here because this is the file that is
supposed to catch it. `f` carries the whole of segment 5: the invasion
condition `f > 1/(1+h)`, `f = 0.877`, Noble's own `f = 0.9`, and the closing
comparison *"D is ONE quantity, f and h are TWO"*. **No slide says what it
is.** The only gloss anywhere is the crop's own 9pt axis label, "DW fitness,
f" - and the deck writes that genotype **WD** throughout, having disarmed
Noble's `P -> h` in a dedicated row on the same slide while saying nothing
about `DW -> WD`. Fitness *relative to what* is never stated either.

Meanwhile slide 68 spends a whole row disarming session 23's `s`, **and `s`
never appears again in the deck.** The deck defends a letter it does not use
and leaves undefined the letter the segment runs on.

### Also unresolved, same family

- **`rho`** - Basu's dimerization constant `rho_R` on session 24 slide 42,
  then `rho_1`, `rho_2`, `rho` with no definition on 79 and 81.
- **`theta_I`** - RESOLVED 8 November, twice over. This file glossed it
  "Tsoi's intermediate threshold", which is **wrong** -- NUMBERS §11.5 has
  "the inefficiency factor", sourced to p.2528. And the gloss was on no
  slide at all while slide 82 printed a `theta_I` column the room was asked
  to read. Both fixed: the gloss here is corrected, and session 24 slide 78
  now carries every symbol of the printed inequality in a foot. **A symbol
  settled only in this file is not settled for the room** -- bar B1.

## Why the first pass missed all five

Every collision above is **within one session**. Every collision the first
pass found was **across sessions**. That is not a coincidence - it is the
method.

The pass worked by grepping the course registry for a letter and comparing
sessions, because the obvious failure mode was a letter meaning one thing in
session 8 and another in session 24. It never read either deck front to back
asking *what does this letter mean on this slide, and did it mean something
else forty slides ago*. So it caught `lambda`-as-a-length against session 11's
eigenvalue, and missed `lambda`-as-a-birth-rate against the eigenvalue printed
on the same deck's second slide.

**The within-session collision is the worse of the two.** A student meeting a
letter twice in one hour has no gap in which to reset, no session boundary to
cue them, and in three of the five cases above the second meaning lands on a
slide that asks them to *use* the first. The cross-session cases the pass did
catch are real but softer: a week has passed, and the deck usually redraws the
earlier system anyway.

**So the registry is necessary and not sufficient.** It cannot be built by
grep alone, because the thing it needs to find is an *order* - which meaning
the room met first - and grep has no order.

## The rule this leaves

Before giving a quantity a letter, grep this file and `decks/` for it. If it is
taken, the one that moves is whichever is **not** assessed and **not** a
published symbol being quoted — in that order. Record the move here.

**And grep is only the first half.** A letter that survives the grep still has
to survive a front-to-back reading of its own deck, because the collisions
that hurt most are the ones inside a single hour, and those are invisible to a
cross-session search (see the section above). Two checks, both required:

1. **Per deck, per letter:** list every slide the letter appears on, in order,
   and say what it means on each. If the answer changes anywhere in that list,
   it is a collision even if no other session is involved.
2. **First-use check:** for every symbol on a slide, find the slide that
   defines it in **body type**. A definition in a foot, in a figure's axis
   label, or in a speaker note does not count — bar B1 — and a definition that
   arrives *after* the first slide that uses it does not count either (F2).

Both of these are things a reader does and a grep cannot. Neither is optional
now; five of the ten collisions in this file were found only by a person
reading the pages one after another.
