"""Session 6 figures — promoter occupancy from a partition function.

Four figures, and every number in them is derived here and checked against a
published value rather than transcribed from one:

  * the states-and-weights ladder for simple activation, in our own notation,
    which is the object derivation 1 builds;
  * fold-change against activator concentration, showing that K_A is the
    midpoint and f is the plateau -- the two things you can read off a log-log
    plot without knowing a single binding energy;
  * lambda P_RM with and without the helper operator O_R1: SAME plateau,
    steeper transition. This is the session's design ledger in one picture --
    cooperativity buys sharpness, not amplitude;
  * sensitivity against the affinity ratio, which turns that into a design
    rule with an optimum in it.

VALIDATION (the reason these are safe to project). The regulation factors are
derived from the states, not copied from Bintu's Table 1, which is a figure in
the PDF and cannot be read as text. The derived forms then reproduce ALL FOUR
sensitivities listed in the legend of their Figure 2b:

    K_R2/K_R1      paper     derived here
    0 or infinity   .54        0.537
    10^3            .66        0.66
    10^-1           .84        0.845
    25              .93        0.933

Four independent numbers across the whole range of the parameter, so the
algebra is theirs. See sessions/s06-promoter-occupancy/README.md.

    python tools/build_figures.py s06
"""
import numpy as np
import matplotlib.patches as mpatches

from figures.style import use, AMBER, CYAN, INK, MUTED, RED, RULE, TEAL

# The deck palette has a body-text colour; figures/style.py does not export
# one, so alias it here rather than inventing a second grey.
BODY = "#23423F"

plt = use()
OUT = "figures/build"

# Bintu et al. 2005 (applications), Figure 2 legend, verbatim: "These plots are
# generated using f ~ 11 [46] and w ~ 100 [47] as extracted from in vitro
# biochemical studies", with K_R2/K_R1 ~ 25 called the realistic parameter.
# Their [46] is Hawley & McClure, J Mol Biol 157:493 (1982); their [47] is
# Koblan & Ackers, Biochemistry 31:57 (1992).
F_LAMBDA = 11.0
OMEGA_BINTU = 100.0
RATIO_LAMBDA = 25.0

# Ackers, Johnson & Shea 1982, Table 3: dG_12 = -1.99 +/- 0.06 kcal/mol at
# 37 C, 0.2 M KCl. That is w = 25.2, NOT the 100 Bintu use -- different assays,
# and the discrepancy is on the answer sheet rather than hidden. Both give the
# same qualitative result; the slope differs in the second decimal place.
RT_37 = 1.9872e-3 * 310.15               # kcal/mol
OMEGA_ACKERS = float(np.exp(1.99 / RT_37))

N_NS = 5e6      # Bintu et al. 2005 (models), Figure 1 legend


def f_simple(a, f):
    """Fold-change for one activator site that recruits RNAP.

    a = [A]/K_A. Weak-promoter limit, so fold-change IS the regulation factor.
    States: empty (1), A bound (a), and each with RNAP; the activator-bound
    state transcribes f times faster.
    """
    return (1 + f * a) / (1 + a)


def f_helper(a, f, omega, ratio):
    """Activator site plus a helper site, one TF species, cooperativity omega.

    a = [A]/K_A with K_A = K_R2; the helper occupancy is h = [A]/K_H, so
    h = ratio * a with ratio = K_R2/K_R1. Only the activator-bound states
    transcribe faster: the helper's whole job is to recruit.
    """
    h = ratio * a
    return (1 + f * a + h + f * omega * a * h) / (1 + a + h + omega * a * h)


def _max_slope(fn, lo=-30, hi=30, n=400001, **kw):
    """Maximum log-log slope, which is what Bintu call the sensitivity s."""
    la = np.linspace(lo, hi, n)
    s = np.gradient(np.log(fn(np.exp(la), **kw)), la)
    return s.max(), np.exp(la[s.argmax()])


def fig_states_weights():
    """The four states of a simple activated promoter, with their weights.

    Drawn rather than plotted, because the object of derivation 1 IS this
    ladder: every state the promoter can be in, each with a Boltzmann weight,
    and the regulation function falls out of the ratio of two sums.
    """
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    ax.set_axis_off()

    rows = [("empty", None, None, "1", "0", MUTED),
            ("activator only", "A", None, "a", "0", TEAL),
            ("RNAP only", None, "P", "p", "1", CYAN),
            ("both, and they touch", "A", "P", "a p f", "f", AMBER)]

    for i, (name, act, pol, w, rate, c) in enumerate(rows):
        y = 3.35 - i * 0.92
        ax.add_patch(mpatches.FancyBboxPatch(
            (0.30, y - 0.20), 3.05, 0.42, boxstyle="round,pad=0.03",
            facecolor="#EEF3F1", edgecolor=RULE, lw=1.6, zorder=1))
        # operator, then promoter, left to right along the DNA
        for x, lab, on in ((1.05, "O", act), (2.55, "P", pol)):
            ax.add_patch(mpatches.Rectangle((x - 0.36, y - 0.11), 0.72, 0.22,
                         facecolor="#FFFFFF", edgecolor=MUTED, lw=1.5,
                         zorder=2))
            ax.text(x, y, lab, ha="center", va="center", fontsize=13,
                    color=MUTED, zorder=3)
            if on:
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x - 0.32, y + 0.13), 0.64, 0.30,
                    boxstyle="round,pad=0.04", facecolor=c, edgecolor="none",
                    zorder=4))
                ax.text(x, y + 0.28, on, ha="center", va="center",
                        fontsize=14, color="white", fontweight="bold",
                        zorder=5)
        if act and pol:
            ax.plot([1.42, 2.18], [y + 0.28, y + 0.28], color=AMBER, lw=3.4,
                    zorder=3)
            ax.text(1.80, y + 0.52, r"$\varepsilon_{ap}$", ha="center",
                    fontsize=13, color=AMBER)

        ax.text(3.65, y, name, ha="left", va="center", fontsize=14, color=INK)
        ax.text(7.35, y, w, ha="center", va="center", fontsize=17, color=c,
                fontweight="bold")
        ax.text(8.75, y, rate, ha="center", va="center", fontsize=17,
                color=INK if rate != "0" else MUTED)

    for x, lab in ((7.35, "weight"), (8.75, "transcribes")):
        ax.text(x, 3.95, lab, ha="center", fontsize=13.5, color=MUTED,
                style="italic")

    ax.text(0.30, -0.40,
            r"$p_{\rm bound}\ \propto\ \dfrac{p + apf}{1 + a + p + apf}"
            r"\qquad\longrightarrow\qquad"
            r"\text{fold-change} = \dfrac{1 + fa}{1 + a}$",
            fontsize=17, color=INK, va="center")
    ax.text(0.30, -1.05,
            "the second form is the weak-promoter limit: p is small, so it "
            "drops out of the denominator\nand the unknown reservoir goes "
            "with it. That is why fold-change is the measurable thing.",
            fontsize=13, color=MUTED, style="italic", va="center")
    ax.text(0.30, 4.55,
            r"$a = [A]/K_A$,   $p = P/N_{\rm NS}\,e^{-\Delta\varepsilon_{p}/k_BT}$,"
            r"   $f = e^{-\varepsilon_{ap}/k_BT}$",
            fontsize=14.5, color=INK, va="center")
    ax.set_xlim(0, 10.1)
    ax.set_ylim(-1.5, 4.9)
    fig.tight_layout(pad=0.2)
    fig.savefig(f"{OUT}/s06_states_weights.png")
    plt.close(fig)


def fig_fold_change():
    """Fold-change against activator concentration for a single site.

    The point of the figure is that the two model parameters are the two
    things you can see: the plateau is f and the midpoint is K_A. No binding
    energy has to be known to read either one off.
    """
    a = np.logspace(-3, 3, 600)
    fig, ax = plt.subplots(figsize=(9.4, 5.5))
    for f, c in ((100.0, TEAL), (11.0, CYAN), (3.0, AMBER)):
        s, _ = _max_slope(f_simple, f=f)
        ax.loglog(a, f_simple(a, f), color=c, lw=3.0,
                  label=f"f = {f:g}   (slope s = {s:.2f})")
        ax.axhline(f, color=c, lw=1.2, ls=":", alpha=0.7)
    ax.axvline(1.0, color=RULE, lw=1.6, ls="--")
    # Annotations in AXES coordinates. Placed in data coordinates they landed
    # outside the axes once the limits changed -- the failure AGENTS.md rule 5
    # exists to catch, and it was invisible in the source.
    ax.text(0.52, 0.045, "$[A] = K_A$ — half-activation", fontsize=13,
            color=INK, transform=ax.transAxes)
    ax.text(0.02, 0.95, "plateau is f — the whole dynamic range you get",
            fontsize=13, color=MUTED, style="italic", transform=ax.transAxes)
    ax.set_xlabel("$[A] / K_A$")
    ax.set_ylabel("fold-change")
    ax.set_ylim(0.6, 320)
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.10))
    fig.tight_layout()
    fig.savefig(f"{OUT}/s06_fold_change.png")
    plt.close(fig)


def fig_cooperativity():
    """lambda P_RM with and without the helper operator O_R1.

    THE session figure. Both curves saturate at the same f; the one with the
    helper is nearly twice as steep. Two requirements, two knobs -- which is
    the opposite of session 5's result and is the reason the two ledgers are
    read side by side.
    """
    a = np.logspace(-5, 3, 900)
    fig, ax = plt.subplots(figsize=(9.6, 5.6))

    s_no, _ = _max_slope(f_simple, f=F_LAMBDA)
    ax.loglog(a, f_simple(a, F_LAMBDA), color=MUTED, lw=2.6,
              label=f"$O_{{R}}1$ deleted — one site      s = {s_no:.2f}")

    s_yes, _ = _max_slope(f_helper, f=F_LAMBDA, omega=OMEGA_BINTU,
                          ratio=RATIO_LAMBDA)
    ax.loglog(a, f_helper(a, F_LAMBDA, OMEGA_BINTU, RATIO_LAMBDA),
              color=TEAL, lw=3.4,
              label=f"with helper, $K_{{R2}}/K_{{R1}}$ = 25   s = {s_yes:.2f}")

    s_ack, _ = _max_slope(f_helper, f=F_LAMBDA, omega=OMEGA_ACKERS,
                          ratio=RATIO_LAMBDA)
    ax.loglog(a, f_helper(a, F_LAMBDA, OMEGA_ACKERS, RATIO_LAMBDA),
              color=CYAN, lw=2.4, ls="--",
              label=f"same, with $\\omega$ = {OMEGA_ACKERS:.0f} (Ackers 1982, superseded)"
                    f"   s = {s_ack:.2f}")

    ax.axhline(F_LAMBDA, color=AMBER, lw=1.6, ls=":")
    ax.text(1.2e-5, F_LAMBDA * 1.25,
            "every curve saturates at the same f ≈ 11", fontsize=13.5,
            color=AMBER)
    ax.set_xlabel("$[cI_2] / K_{R2}$")
    ax.set_ylabel("fold-change")
    ax.set_ylim(0.7, 30)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s06_cooperativity.png")
    plt.close(fig)


def fig_sensitivity_ratio():
    """Sensitivity against the affinity ratio: the design rule, with a peak.

    A helper site only helps if it is tighter than the activator site, and
    making it much tighter is worse than making it slightly tighter. Bintu's
    rule of thumb is K_R2/K_R1 ~ f; the computed optimum here is nearer
    sqrt(f), and the curve is flat enough between them that both are fine.
    That flatness is itself the engineering point.
    """
    ratios = np.logspace(-1, 3, 260)
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    for om, c, lab in ((OMEGA_BINTU, TEAL, r"$\omega$ = 100  (Koblan & Ackers 1992, 37 °C)"),
                       (OMEGA_ACKERS, CYAN,
                        rf"$\omega$ = {OMEGA_ACKERS:.0f}  (Ackers 1982, superseded)")):
        s = np.array([_max_slope(f_helper, f=F_LAMBDA, omega=om, ratio=r)[0]
                      for r in ratios])
        ax.semilogx(ratios, s, color=c, lw=3.0, label=lab)
        i = s.argmax()
        ax.plot([ratios[i]], [s[i]], "o", color=c, ms=9, zorder=5)

    s_one, _ = _max_slope(f_simple, f=F_LAMBDA)
    # Drawn across the right half only: a full-width rule at this height
    # runs straight through the legend, whichever corner the legend is in.
    ax.axhline(s_one, xmin=0.34, color=MUTED, lw=1.6, ls="--")
    ax.text(9.0e2, s_one + 0.016, "one site alone", fontsize=13, color=MUTED,
            ha="right")
    ax.axhline(1.0, color=RED, lw=1.4, ls=":")
    ax.text(1.2e-1, 1.012, "s = 1 — the ceiling for this architecture, and the "
            "floor for bistability", fontsize=13, color=RED)
    ax.axvline(RATIO_LAMBDA, color=RULE, lw=1.6, ls="--")
    ax.text(RATIO_LAMBDA * 1.2, 0.60, "$\\lambda$ $O_R$", fontsize=13.5,
            color=INK)
    ax.set_xlabel("$K_{R2} / K_{R1}$    (how much tighter the helper site is)")
    ax.set_ylabel("sensitivity  s")
    ax.set_ylim(0.45, 1.08)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s06_sensitivity_ratio.png")
    plt.close(fig)


def _dna(ax, x0, x1, y, h=0.26, c="#E3EAE7"):
    ax.add_patch(mpatches.Rectangle((x0, y - h / 2), x1 - x0, h,
                 facecolor=c, edgecolor=MUTED, lw=1.4, zorder=1))


def fig_promoter_anatomy():
    """What a promoter IS, before anybody is asked to model one.

    Added 11 September after Adam's review: the session introduced operator,
    core promoter, RNAP, recruitment and the closed-to-open transition as
    vocabulary and never once showed the object. Sessions 1-5 never show it
    either -- "closed complex" and "-35" appear ZERO times in decks 1 through 5
    -- so session 6 is the first time in this course that a promoter is a piece
    of DNA rather than a symbol, and it has to be drawn before it is counted.
    """
    fig, ax = plt.subplots(figsize=(10.0, 5.2))
    ax.set_axis_off()

    y = 2.35
    _dna(ax, 0.4, 9.6, y)

    # the core promoter: the two hexamers RNAP reads
    for x0, x1, lab, sub in ((2.55, 3.35, "−35", "TTGACA"),
                             (4.45, 5.25, "−10", "TATAAT")):
        ax.add_patch(mpatches.Rectangle((x0, y - 0.13), x1 - x0, 0.26,
                     facecolor=CYAN, edgecolor=INK, lw=1.5, zorder=2))
        ax.text((x0 + x1) / 2, y + 0.30, lab, ha="center", fontsize=14.5,
                color=INK, fontweight="bold")
        ax.text((x0 + x1) / 2, y - 0.42, sub, ha="center", fontsize=11.5,
                color=MUTED, family="monospace")

    # start site
    ax.annotate("", xy=(6.9, y + 0.95), xytext=(5.95, y + 0.95),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))
    ax.plot([5.95, 5.95], [y + 0.14, y + 0.95], color=INK, lw=2.2)
    ax.text(6.45, y + 1.12, "+1  transcription starts here", ha="center",
            fontsize=12.5, color=INK)

    # an operator, drawn where it actually sits for a simple repressor
    ax.add_patch(mpatches.Rectangle((5.05, y - 0.13), 1.0, 0.26,
                 facecolor=AMBER, edgecolor=INK, lw=1.5, alpha=0.55, zorder=3))
    ax.text(5.55, y - 0.82, "operator (overlapping)", ha="center",
            fontsize=11.5, color=AMBER)
    ax.add_patch(mpatches.Rectangle((0.70, y - 0.13), 1.0, 0.26,
                 facecolor=TEAL, edgecolor=INK, lw=1.5, alpha=0.55, zorder=3))
    ax.text(1.20, y - 0.50, "operator (adjacent)", ha="center", fontsize=11.5,
            color=TEAL)

    ax.text(0.4, y + 0.95, "DNA", fontsize=12.5, color=MUTED)

    ax.text(0.4, 4.30,
            "The core promoter is where RNA polymerase binds: two hexamers, "
            "35 and 10 bases upstream of the start.\nHow well they match the "
            "consensus is what ‘promoter strength’ means.",
            fontsize=13, color=BODY, va="top")

    # One string per line. Two-part lines with a bold lead-in need text
    # measurement to place the second half, and guessing an x offset is how
    # the first version of this figure overlapped itself twice.
    ax.text(0.4, 1.34, "An OPERATOR is just a binding site for something "
            "else, and where it sits decides the mechanism.",
            fontsize=12.5, color=INK, fontweight="bold")
    for i, (txt, c) in enumerate([
            ("Over the core promoter — a bound protein excludes RNAP. "
             "Repression by occlusion, and no state has both bound.", AMBER),
            ("Beside it — the bound protein and RNAP can touch, and that "
             "contact is the only place activation can come from.", TEAL)]):
        ax.text(0.4, 0.92 - i * 0.40, txt, fontsize=12, color=c)

    ax.set_xlim(0, 10.0); ax.set_ylim(0.25, 4.55)
    fig.tight_layout(pad=0.3)
    fig.savefig(f"{OUT}/s06_promoter_anatomy.png")
    plt.close(fig)


def fig_two_mechanisms():
    """Recruitment versus the closed-to-open transition.

    The session used both phrases and drew neither, then at minute 70 asked
    the room to accept that an activator can repress -- which is ENTIRELY a
    claim about these two levers. Without this picture that segment is an
    assertion; with it, it is a consequence.
    """
    fig, ax = plt.subplots(figsize=(10.2, 5.0))
    ax.set_axis_off()

    for col, (title, sub, c) in enumerate([
            ("1 · RECRUITMENT", "change how OFTEN polymerase is there", TEAL),
            ("2 · ISOMERISATION", "change how often it FIRES once it is there",
             AMBER)]):
        x0 = 0.3 + col * 5.15
        ax.add_patch(mpatches.FancyBboxPatch((x0, 0.25), 4.65, 4.35,
                     boxstyle="round,pad=0.06", facecolor="#F2F6F4",
                     edgecolor=c, lw=2.0))
        ax.text(x0 + 0.25, 4.25, title, fontsize=14, color=c,
                fontweight="bold")
        ax.text(x0 + 0.25, 3.95, sub, fontsize=12, color=BODY, style="italic")

    # --- left: recruitment ---
    for row, (lab, bound) in enumerate([("without activator", False),
                                        ("with activator", True)]):
        y = 3.05 - row * 1.35
        _dna(ax, 0.55, 4.65, y, h=0.22)
        ax.add_patch(mpatches.Rectangle((2.55, y - 0.11), 1.15, 0.22,
                     facecolor=CYAN, edgecolor=MUTED, lw=1.2, zorder=2))
        if bound:
            ax.add_patch(mpatches.FancyBboxPatch((1.30, y + 0.14), 0.85, 0.34,
                         boxstyle="round,pad=0.03", facecolor=TEAL,
                         edgecolor="none", zorder=4))
            ax.text(1.72, y + 0.31, "A", ha="center", va="center",
                    fontsize=12, color="white", fontweight="bold", zorder=5)
            ax.add_patch(mpatches.Ellipse((3.12, y + 0.33), 1.05, 0.40,
                         facecolor="#8FC7A9", edgecolor=INK, lw=1.3, zorder=4))
            ax.text(3.12, y + 0.33, "RNAP", ha="center", va="center",
                    fontsize=9.5, color=INK, zorder=5)
            ax.plot([2.15, 2.60], [y + 0.31, y + 0.33], color=AMBER, lw=3.0,
                    zorder=3)
            ax.text(2.38, y + 0.62, r"$\varepsilon_{ap}$", ha="center",
                    fontsize=12, color=AMBER)
        ax.text(0.55, y - 0.42, lab, fontsize=11, color=MUTED)
    ax.text(0.55, 0.58, "RNAP is bound MORE OF THE TIME.\nThe rate it fires "
            "at is unchanged.", fontsize=12, color=INK, va="bottom")

    # --- right: isomerisation ---
    for row, (lab, fires) in enumerate([("closed complex", False),
                                        ("open complex", True)]):
        y = 3.05 - row * 1.35
        _dna(ax, 5.70, 9.80, y, h=0.22)
        ax.add_patch(mpatches.Rectangle((7.35, y - 0.11), 1.15, 0.22,
                     facecolor=CYAN, edgecolor=MUTED, lw=1.2, zorder=2))
        ax.add_patch(mpatches.Ellipse((7.92, y + 0.33), 1.05, 0.40,
                     facecolor="#8FC7A9", edgecolor=INK, lw=1.3, zorder=4))
        ax.text(7.92, y + 0.33, "RNAP", ha="center", va="center", fontsize=9.5,
                color=INK, zorder=5)
        if fires:
            # melted bubble + departing transcript
            ax.add_patch(mpatches.Ellipse((7.92, y), 0.55, 0.30,
                         facecolor="white", edgecolor=AMBER, lw=2.0, zorder=3))
            ax.annotate("", xy=(9.35, y + 0.62), xytext=(8.45, y + 0.62),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.4))
            ax.text(8.90, y + 0.80, "transcript", fontsize=10.5, color=AMBER,
                    ha="center")
        ax.text(5.70, y - 0.42, lab, fontsize=11, color=MUTED)
    ax.annotate("", xy=(6.15, 1.98), xytext=(6.15, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.2))
    ax.text(6.30, 2.26, "melts", fontsize=11.5, color=AMBER, va="center")
    ax.text(5.70, 1.05, "the rate it fires at is $k$", fontsize=11.5,
            color=AMBER)
    ax.text(5.70, 0.50, "RNAP is bound just as often.\nIt converts to the "
            "firing state more often.", fontsize=12, color=INK, va="bottom")

    ax.set_xlim(0, 10.2); ax.set_ylim(0, 4.75)
    fig.tight_layout(pad=0.3)
    fig.savefig(f"{OUT}/s06_two_mechanisms.png")
    plt.close(fig)


FIGURES = [fig_promoter_anatomy, fig_two_mechanisms, fig_states_weights, fig_fold_change, fig_cooperativity,
           fig_sensitivity_ratio]
