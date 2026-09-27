"""Session 10 figures — feedforward loops: delay, adaptation, and the pulse.

Every curve here comes out of `posb.core`, the same Model/Reaction the students
use, so the plot on the slide is the plot they can reproduce. The input X is
carried as a species with no reactions of its own: it holds whatever value the
initial condition sets, which is how a step of X is imposed — integrate the
pre-step steady state, then re-integrate with X switched.

The three things this session has to draw, and where each is verified:

  * the C1-FFL sign-sensitive DELAY (T24, T25). `c1_delay_curves` builds the
    on-step and off-step responses; the delay is measured off the curves, not
    asserted, and compared to Mangan & Alon's step-limit formula
    t_D = alpha_y^-1 log[(Ymax - Ymin)/(Ymax - Kyz)].
  * the I1-FFL ADAPTATION (T26). `iffl_adaptation` builds the pulse-with-basal
    case and reads the peak and the adaptation error off it numerically.
  * the Basu pulse generator as the artifact the abstraction comes from.
    `pulse_generator` is the same I1 topology with no basal Y, so the pulse is
    strong — Basu Fig. 3 in our own units.

Delay convention, stated once and used everywhere (this is the T25 spec, not a
style choice): response time is the time to reach 50% of the steady-state Z;
the FFL is compared to a simple-regulation design with the SAME steady-state Z
(Mangan & Alon's mathematically controlled comparison); delay is
t_1/2(FFL) - t_1/2(simple), and its sign is reported per direction of the Sx
step.

Run:  python tools/build_figures.py s10
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE
from posb.core import Reaction, Model

plt = use()
OUT = "figures/build"

H = 2                       # Hill coefficient at each regulated promoter
KXY = KXZ = 0.1             # X thresholds (Mangan Fig. 2 params)


def _act(u, K):
    u = max(u, 0.0)
    return (u / K) ** H / (1 + (u / K) ** H)


def _rep(u, K):
    u = max(u, 0.0)
    return 1.0 / (1 + (u / K) ** H)


def ffl(kind, Kyz, By=0.0, Bz=0.0, beta_z=1.0):
    """A three-gene FFL as a posb Model. X is an inert species (the input).

    kind = "C1": X->Y activation, {X,Y}->Z AND of two activations (coherent 1).
    kind = "I1": X->Y activation, Z activated by X and REPRESSED by Y (incoherent 1).
    By, Bz are basal rates; beta_z scales the Z promoter (used to match a simple
    design's steady state).
    """
    yz = _act if kind == "C1" else None
    zgate = ((lambda c: _act(c["X"], KXZ) * _act(c["Y"], Kyz)) if kind == "C1"
             else (lambda c: _act(c["X"], KXZ) * _rep(c["Y"], Kyz)))
    return Model(
        [Reaction({}, {"Y": 1}, rate=lambda c, p: By + _act(c["X"], KXY),
                  name="Y production, activated by X"),
         Reaction({"Y": 1}, {}, k=1.0, name="Y removal"),
         Reaction({}, {"Z": 1}, rate=lambda c, p, g=zgate: Bz + beta_z * g(c),
                  name="Z production, gated by X and Y"),
         Reaction({"Z": 1}, {}, k=1.0, name="Z removal")],
        species=["X", "Y", "Z"])


def simple(Kxz, Bz=0.0, beta_z=1.0):
    """Simple regulation: Z activated by X alone, no Y. The comparison design."""
    return Model(
        [Reaction({}, {"Z": 1},
                  rate=lambda c, p: Bz + beta_z * _act(c["X"], Kxz),
                  name="Z production, activated by X"),
         Reaction({"Z": 1}, {}, k=1.0, name="Z removal")],
        species=["X", "Z"])


def _step(model, x_pre, x_post, t=8.0, n=1600):
    """Steady state at X=x_pre, then the response after X switches to x_post."""
    sp = model.species
    pre = model.steady_state({s: 0.0 for s in sp} | {"X": x_pre})
    x0 = dict(pre) | {"X": x_post}
    return model.simulate(x0, (0.0, t), n_points=n)


def _t_half(t, z):
    z0, zf = z[0], z[-1]
    if abs(zf - z0) < 1e-9:
        return np.nan
    frac = (z - z0) / (zf - z0)
    i = int(np.argmax(frac >= 0.5))
    if i == 0:
        return 0.0
    return float(np.interp(0.5, frac[i - 1:i + 1], t[i - 1:i + 1]))


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# C1-FFL: the sign-sensitive delay, revealed one step at a time
# ---------------------------------------------------------------------------
KYZ_C1 = 0.5


def _c1_onstep():
    m = ffl("C1", KYZ_C1)
    tr = _step(m, 0.0, 1.0)
    # simple design matched to the same final Z
    zf = tr["Z"][-1]
    ms = simple(KXZ, beta_z=zf / _act(1.0, KXZ))
    sr = _step(ms, 0.0, 1.0)
    return tr, sr


def _draw_onstep(ax, tr, sr, show=("X", "Y", "Z", "simple")):
    if "X" in show:
        ax.plot(tr.t, np.where(tr.t >= 0, 1.0, 0.0), color=MUTED, lw=1.6,
                ls=":", label="X (input)")
    if "Y" in show:
        ax.plot(tr.t, tr["Y"], color=CYAN, lw=2.6, label="Y")
    if "simple" in show:
        ax.plot(sr.t, sr["Z"], color=RULE, lw=3.0, label="Z, simple reg.")
    if "Z" in show:
        ax.plot(tr.t, tr["Z"], color=TEAL, lw=3.0, label="Z, C1-FFL")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 6)
    ax.legend(loc="upper right")


def fig_c1_delay():
    """Five panels for derivation_fig: the delay appears, then proves sign-sensitive."""
    tr, sr = _c1_onstep()
    Kyz = KYZ_C1
    Ymax = _act(1.0, KXY)
    tD = np.log((Ymax - 0.0) / (Ymax - Kyz))
    tF, tS = _t_half(tr.t, tr["Z"]), _t_half(sr.t, sr["Z"])

    # p1: X steps on, Y builds
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _draw_onstep(ax, tr, sr, show=("X", "Y"))
    ax.axhline(Kyz, color=CYAN, lw=1.1, ls="--")
    ax.text(4.2, Kyz + 0.03, "$K_{yz}$", color=CYAN, fontsize=14)
    _save(fig, "s10_c1_p1")

    # p2: Z waits for Y to cross Kyz
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _draw_onstep(ax, tr, sr, show=("X", "Y", "Z"))
    ax.axhline(Kyz, color=CYAN, lw=1.1, ls="--")
    tcross = -np.log(1 - Kyz / Ymax)
    ax.axvline(tcross, color=MUTED, lw=1.0, ls=":")
    ax.text(tcross + 0.1, 0.05, "Y crosses $K_{yz}$", color=MUTED, fontsize=13)
    _save(fig, "s10_c1_p2")

    # p3: the delay, measured against the matched simple design
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _draw_onstep(ax, tr, sr, show=("X", "Z", "simple"))
    y = 0.5 * tr["Z"][-1]
    ax.annotate("", xy=(tF, y), xytext=(tS, y),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.2))
    ax.text((tF + tS) / 2, y + 0.04, f"delay $t_D$\n≈ {tF - tS:.2f}",
            color=RED, fontsize=14, ha="center")
    ax.text(0.97, 0.06, f"sharp-gate formula:  $t_D$ = {tD:.2f}",
            transform=ax.transAxes, ha="right", va="bottom",
            color=INK, fontsize=13,
            bbox=dict(facecolor="white", edgecolor=RULE, pad=3.0))
    _save(fig, "s10_c1_p3")

    # p4: off-step — Z falls at once, no delay
    m = ffl("C1", Kyz)
    off = _step(m, 1.0, 0.0)
    zf = off["Z"][0]
    ms = simple(KXZ, beta_z=zf / _act(1.0, KXZ))
    so = _step(ms, 1.0, 0.0)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    ax.plot(off.t, np.where(off.t >= 0, 0.0, 1.0), color=MUTED, lw=1.6, ls=":",
            label="X (input)")
    ax.plot(so.t, so["Z"], color=RULE, lw=3.0, label="Z, simple reg.")
    ax.plot(off.t, off["Z"], color=TEAL, lw=3.0, label="Z, C1-FFL")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 6)
    ax.legend(loc="upper right")
    ax.text(0.3, 0.3, "the two curves\nlie on top of each other:\nno delay OFF",
            color=INK, fontsize=13)
    _save(fig, "s10_c1_p4")

    # p5: a short ON pulse of X is rejected
    m = ffl("C1", Kyz)
    pre = m.steady_state({"X": 0.0, "Y": 0.0, "Z": 0.0})
    t1 = m.simulate(dict(pre) | {"X": 1.0}, (0.0, 0.6), n_points=200)
    mid = t1.final()
    t2 = m.simulate(dict(mid) | {"X": 0.0}, (0.6, 6.0), n_points=800)
    tt = np.concatenate([t1.t, t2.t])
    zz = np.concatenate([t1["Z"], t2["Z"]])
    yy = np.concatenate([t1["Y"], t2["Y"]])
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    ax.plot(tt, np.where((tt >= 0) & (tt < 0.6), 1.0, 0.0), color=MUTED,
            lw=1.6, ls=":", label="X: a short pulse")
    ax.plot(tt, yy, color=CYAN, lw=2.6, label="Y")
    ax.plot(tt, zz, color=TEAL, lw=3.0, label="Z, C1-FFL")
    ax.axhline(Kyz, color=CYAN, lw=1.1, ls="--")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 6)
    ax.legend(loc="upper right")
    ax.text(1.4, 0.6, "Y never reaches $K_{yz}$,\nso Z never fires",
            color=INK, fontsize=13)
    _save(fig, "s10_c1_p5")


# ---------------------------------------------------------------------------
# I1-FFL: adaptation — the pulse, its amplitude, and the adaptation error
# ---------------------------------------------------------------------------
def iffl_numbers(Kyz=0.5, By=0.4, beta_z=6.0):
    """Peak, final, and adaptation error of the I1-FFL with basal Y. Numeric."""
    m = ffl("I1", Kyz, By=By, beta_z=beta_z)
    tr = _step(m, 0.0, 1.0, t=12.0, n=4000)
    z = tr["Z"]
    peak = float(z.max())
    zf = float(z[-1])
    t_peak = float(tr.t[int(np.argmax(z))])
    return dict(peak=peak, final=zf, t_peak=t_peak,
                adaptation_error=zf / peak, traj=tr)


def _iffl_axes(d):
    """The shared I1 trajectory plot. Annotation is added by the caller."""
    tr = d["traj"]
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.plot(tr.t, np.where(tr.t >= 0, 1.0, 0.0), color=MUTED,
            lw=1.4, ls=":", label="X (input, on step at $X=1$)")
    ax.plot(tr.t, tr["Y"], color=CYAN, lw=2.4, label="Y (the repressor arm)")
    ax.plot(tr.t, tr["Z"], color=TEAL, lw=3.2, label="Z (output)")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 10)
    ax.set_ylim(-0.05, 1.62)
    ax.legend(loc="lower right", fontsize=11)
    return fig, ax


def fig_iffl_adaptation():
    """The I1-FFL overshoot-and-adapt, unannotated -- the mechanism surface.

    Deliberately carries NO numbers: the lecture surface that shows the shape
    comes before the surface that defines the adaptation error, and a figure
    with the answer printed on it collapses the two.
    """
    _save(_iffl_axes(iffl_numbers())[0], "s10_iffl_adaptation")


def fig_iffl_adaptation_marked():
    """The same curve with peak, final and adaptation error marked.

    For the answer sheet and the board notes, not the lecture surface.
    """
    d = iffl_numbers()
    tr = d["traj"]
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.plot(tr.t, np.where(tr.t >= 0, 1.0, 0.0), color=MUTED,
            lw=1.4, ls=":", label="X (input, on step at $X=1$)")
    ax.plot(tr.t, tr["Y"], color=CYAN, lw=2.4, label="Y (the repressor arm)")
    ax.plot(tr.t, tr["Z"], color=TEAL, lw=3.2, label="Z (output)")
    ax.axhline(d["peak"], color=AMBER, lw=1.0, ls="--")
    ax.axhline(d["final"], color=RED, lw=1.0, ls="--")
    ax.annotate("", xy=(d["t_peak"], d["peak"]), xytext=(d["t_peak"], d["final"]),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.0))
    ax.text(d["t_peak"] + 0.2, (d["peak"] + d["final"]) / 2,
            f"peak = {d['peak']:.2f}\nfinal = {d['final']:.2f}\n"
            f"adaptation error\n= final/peak = {d['adaptation_error']:.2f}",
            color=INK, fontsize=13, va="center")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 10)
    ax.set_ylim(-0.05, 1.62)
    ax.legend(loc="lower right", fontsize=11)
    _save(fig, "s10_iffl_adaptation_marked")


def _half_time(t, z, zf):
    """Time to reach half of the final value, by linear interpolation."""
    i = int(np.argmax(z >= 0.5 * zf))
    return float(np.interp(0.5 * zf, [z[i - 1], z[i]], [t[i - 1], t[i]]))


def iffl_acceleration():
    """The I1-FFL against the matched simple design: same steady state, faster.

    Mangan & Alon's other headline result. Returns the numbers so the deck and
    the answer sheet quote the same ones.
    """
    d = iffl_numbers()
    tr = d["traj"]
    t = np.asarray(tr.t)
    z = np.asarray(tr["Z"])
    zf = float(z[-1])
    sm = simple(KXZ, beta_z=zf / _act(1.0, KXZ))
    trs = sm.simulate({"X": 1.0, "Z": 0.0}, (0.0, float(t[-1])),
                      n_points=len(t))
    ts = np.asarray(trs.t)
    zs = np.asarray(trs["Z"])
    th_f = _half_time(t, z, zf)
    th_s = _half_time(ts, zs, float(zs[-1]))
    return dict(t=t, z=z, ts=ts, zs=zs, zf=zf, th_ffl=th_f, th_simple=th_s,
                speedup=th_s / th_f)


def fig_iffl_acceleration():
    """Response acceleration: the same I1 circuit reaches half its steady state 6x faster."""
    a = iffl_acceleration()
    zf = a["zf"]
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.plot(a["ts"], a["zs"], color=RULE, lw=3.0,
            label="simple regulation ($X \\to Z$ only)")
    ax.plot(a["t"], a["z"], color=TEAL, lw=3.2, label="the I1-FFL")
    ax.axhline(zf, color=MUTED, lw=1.0, ls=":")
    ax.axhline(0.5 * zf, color=MUTED, lw=1.0, ls="--")
    ax.text(3.95, zf + 0.025, "same steady state, by construction",
            color=MUTED, fontsize=11, va="bottom", ha="right")
    ax.text(3.95, 0.5 * zf + 0.025, "half of it", color=MUTED, fontsize=11,
            va="bottom", ha="right")
    for x, c in ((a["th_ffl"], TEAL), (a["th_simple"], RULE)):
        ax.plot([x, x], [0, 0.5 * zf], color=c, lw=1.6, ls="--")
        ax.plot([x], [0.5 * zf], "o", ms=9, color=c, zorder=6)
    ax.annotate("", xy=(a["th_ffl"], 0.13), xytext=(a["th_simple"], 0.13),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    ax.text(a["th_simple"] + 0.12, 0.115,
            f"{a['th_ffl']:.2f} against {a['th_simple']:.2f} lifetimes"
            f"   \u2014   {a['speedup']:.1f}\u00d7 faster",
            color=RED, fontsize=12.5, ha="left", va="center")
    ax.set_xlim(-0.05, 4.0)
    ax.set_ylim(0.0, 1.30)
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("Z")
    ax.legend(loc="upper right", fontsize=11)
    _save(fig, "s10_iffl_acceleration")


# ---------------------------------------------------------------------------
# Basu: the pulse generator as the artifact (I1, no basal Y -> strong pulse)
# ---------------------------------------------------------------------------
def fig_pulse_generator():
    """Basu's pulse generator in our units: strong pulse, and rate sensing."""
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6))

    # (a) a strong pulse from a step of the signal
    m = ffl("I1", 0.15, By=0.0, beta_z=8.0)
    tr = _step(m, 0.0, 1.0, t=10.0, n=3000)
    ax = axes[0]
    ax.plot(tr.t, np.where(tr.t >= 0, 1.0, 0.0), color=MUTED,
            lw=1.4, ls=":", label="AHL (step on, scaled: $X=1$)")
    ax.plot(tr.t, tr["Z"], color=TEAL, lw=3.2, label="GFP (output)")
    ax.plot(tr.t, tr["Y"], color=CYAN, lw=2.2, label="CI (delayed repressor)")
    ax.set_title("a step of signal → a pulse of output")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_xlim(-0.4, 8)
    ax.legend(loc="upper right")

    # (b) rate sensing: slower ramps to the same final level give smaller,
    # later pulses (Basu Fig. 3b, our units). Ramp X linearly over `tau`.
    #
    # The ramps span 500x deliberately. With alpha_y = alpha_z = 1 the
    # repressor arm and the output share a timescale, so the pulse height is
    # only weakly rate-sensitive: 0.2 -> 3 -> 10 lifetimes moves the peak by
    # 12%, which is invisible on a projected slide and argues the wrong answer.
    # Basu's device has a real separation (GFP reports as fast as it is made;
    # CI must also dimerize and find its operator), which is why his Fig. 3
    # shows a sharper distance dependence than this reduction does. That gap
    # is the point, and the slide says so.
    ax = axes[1]
    from scipy.integrate import solve_ivp
    T = 26.0
    tt = np.linspace(0, T, 6000)
    for tau, c in [(0.2, TEAL), (10.0, CYAN), (100.0, AMBER)]:
        pre = m.steady_state({"X": 0.0, "Y": 0.0, "Z": 0.0})

        def rhs(t, x, tau=tau):
            xx = min(t / tau, 1.0)
            st = dict(zip(m.species, x)) | {"X": xx}
            return m.rhs(t, [st[s] for s in m.species])
        sol = solve_ivp(rhs, (0, T), [pre[s] for s in m.species], t_eval=tt,
                        method="LSODA", rtol=1e-8, atol=1e-10)
        z = sol.y[m.species.index("Z")]
        ax.plot(tt, z, color=c, lw=2.8,
                label=f"ramp over {tau:g} lifetimes   (peak {z.max():.2f})")
        ax.plot(tt, np.clip(tt / tau, 0, 1), color=c, lw=1.2, ls=":")
        ax.plot([tt[int(z.argmax())]], [z.max()], "o", ms=7, color=c, zorder=6)
    ax.set_title("same final signal, different rate of rise")
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.text(0.985, 0.42, "dotted: the input ramp itself",
            transform=ax.transAxes, ha="right", va="top", fontsize=10,
            color=MUTED)
    ax.set_xlim(-0.4, T)
    ax.set_ylim(0, 1.45)
    ax.legend(loc="upper right", fontsize=10)
    _save(fig, "s10_pulse_generator")


FIGURES = [fig_c1_delay, fig_iffl_adaptation, fig_iffl_adaptation_marked,
           fig_iffl_acceleration,
           fig_pulse_generator]


if __name__ == "__main__":
    d = iffl_numbers()
    print("I1 adaptation:", {k: round(v, 3) for k, v in d.items() if k != "traj"})
