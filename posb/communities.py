"""Communities -- session 24's object, and the wire that left the cell.

THE CHANGE OF OBJECT. For twenty-three sessions every connection in a circuit
has been a molecule inside one cell. The moment the signal leaves, the
connection acquires A LENGTH SCALE AND A DELAY, and both become design
parameters that belong to the medium rather than to the plasmid. Two
quantities in this module are nothing but that statement: `diffusion_time`,
which is how long the signal takes, and `penetration_depth`, which is how far
it gets before it decays.

WHAT IS HERE, AND WHOSE IT IS. Three groups of functions, with three different
provenances, and the difference matters more here than in any other module in
this package:

  * `band_detect_response`, `band_edges`, `basu_params` are BASU'S MODEL,
    equations (1)-(4) as printed in Basu, Gerchman, Collins, Arnold & Weiss,
    *Nature* 434:1130-1134 (2005), p.1134, with their printed BD2 parameter
    set. Nothing here is fitted and nothing is ours.

  * `predator_prey_model`, `pp_qss_model`, `pp_steady_states`, `pp_jacobian`,
    `pp_hopf_D` and the IPTG rules are THE BIOMODELS DEPOSIT'S model,
    BIOMD0000000296, transcribed in NUMBERS.md sec 20 -- NOT the equations of
    Balagadde's text, which prints none. The deposit is four-dimensional
    because THE SIGNALS ARE STATE VARIABLES, and that is where the oscillation
    lives: `pp_qss_model` is the same circuit with the signals eliminated and
    it cannot oscillate at any parameter values. A slide using these equations
    says which provenance it is using.

  * `sender_receiver` and `dol_criterion` are a minimal pair written with the
    room, and Tsoi's printed criterion evaluated with a burden form the caller
    chooses. Neither carries a parameter either paper supplies.

WHAT NO PAPER IN THIS SESSION SUPPLIES. A diffusion coefficient that can
legitimately be put with Basu's decay constant. `penetration_depth` therefore
has no default D, and the reasons are written out there because they are the
session's engineering lesson rather than an inconvenience.

Everything is plain NumPy, plus `scipy.optimize` for the two root-finds. There
is no ODE solver anywhere in this module and there is none in its tests: every
quantity below is a closed form or a root of one, and an integrator used to
check a closed form mostly measures the integrator.
"""
import numpy as np

__all__ = [
    "diffusion_time", "penetration_depth",
    "KARIG_D_3OC12HSL", "KARIG_D_C4HSL", "BASU_XI",
    "BASU_BD2", "basu_params", "band_detect_response", "band_peak",
    "band_edges",
    "sender_receiver",
    "PP_PARAMS", "PP_INITIAL", "PP_IPTG", "iptg_assignment_rules", "pp_params",
    "predator_prey_model", "pp_qss_signals", "pp_qss_model",
    "pp_steady_states", "pp_jacobian", "pp_oscillatory_focus",
    "pp_leading_real_part", "pp_hopf_D",
    "burden_form", "dol_criterion",
]

# --- the diffusion numbers, with their provenance ---------------------------
# Karig, Martini, Lu, DeLateur, Goldenfeld & Weiss, PNAS 115:6572-6577 (2018),
# main text p.6573. BOTH ARE ESTIMATES, obtained by fitting a fluorescence wave
# profile over time, and both are EFFECTIVE CELL-TO-CELL coefficients through a
# bacterial lawn rather than free-solution values. The measured ratio is
# 21.6 +/- 10 where free solution (Wilke-Chang) predicts about 1.5, so the
# ratio is a property of cells and not of the molecules. And the slow one is
# 3OC12HSL, which is NEITHER of Basu's signals (Basu's inducer is 3OC6HSL).
KARIG_D_3OC12HSL = 83.0        # um^2/s
KARIG_D_C4HSL = 1810.0         # um^2/s

# Basu p.1134 prints this as "AHL intercellular diffusion", units mm^2/min.
# IT IS NOT A DIFFUSION COEFFICIENT. Their equation (5) is a bare discrete
# Laplacian, sum(six neighbors) - 6A, with no grid spacing, so the coefficient
# in that equation must have units of min^-1 and the only self-consistent
# reading is xi = D/dx^2 with a lattice spacing dx the paper never states.
# Kept here so that the arithmetic in the session can be run against it and
# seen to fail, and named so that nobody reaches for it by accident.
BASU_XI = 0.001                # mm^2/min AS PRINTED; see the warning above


def diffusion_time(L, D):
    """t ~ L^2 / (2D). Session 2's convention, and the course's.

    THE CONVENTION IS L^2/2D AND NOT L^2/6D, and session 2 states the
    convention before it states the number -- its closing slide ("The habit
    this course wants") makes that the first of four habits: "L^2/2D or
    L^2/6D? Say which. A factor of three is nothing; an unstated convention is
    an argument you cannot settle afterwards." A factor of three is nothing
    next to the factor of 400 that comes from squaring the distance.

    This function exists so that session 24 and session 2 cannot drift apart.
    It is deliberately a one-liner: there is nothing to abstract, and the
    whole content is the choice of denominator.

    L and D carry no units here and must be consistent -- L^2 over D. Session 2
    works in um and um^2/s; session 24 works in mm and mm^2/min. Mixing them is
    the error this signature cannot catch, which is why D has no default: the
    one in session 2's figure module is GFP in E. coli cytoplasm and is not an
    AHL coefficient in agar.

    WHICH DIRECTION IT IS WRONG IN. Session 2 measured that too: for anything
    large it is optimistic by more than an order of magnitude, because the
    effective viscosity depends on the size of the probe.
    """
    L = np.asarray(L, float)
    D = np.asarray(D, float)
    if np.any(L < 0.0):
        raise ValueError("L is a distance and cannot be negative")
    if np.any(D <= 0.0):
        raise ValueError("D must be > 0; at D = 0 nothing ever arrives, which "
                         "is a statement to make and not a number to return")
    return L ** 2 / (2.0 * D)


def penetration_depth(D, gamma):
    """lambda = sqrt(D / gamma). How far a decaying signal gets, at steady state.

    This is the length scale that replaces L^2/2D once decay matters. A signal
    spreading from a source and decaying first-order settles to an exponential
    profile with e-folding length sqrt(D/gamma), so gamma is the knob: Basu
    hand the physics over on p.1134, where gamma_A sets the steepness of the
    gradient and is pH-sensitive. You change it by changing the medium.

    D HAS NO DEFAULT, AND THAT IS THE POINT OF THE FUNCTION. There are two
    candidate numbers in this session's folder and neither one may be put with
    Basu's gamma_A = 0.01 min^-1:

      1. Basu print xi = 0.001 mm^2/min for AHL, and it is not a diffusion
         coefficient. Their equation (5) is a discrete Laplacian with no grid
         spacing, so xi is really D/dx^2 with dx never stated. Substituted as a
         D it puts their own 10 mm ring at L^2/2xi = 833 hours against a
         36-hour experiment -- one to two orders of magnitude too small for the
         figures it generated. The session runs that arithmetic as a reductio,
         not as a design number.

      2. Karig's 83 um^2/s is a sourced, measured-and-fitted coefficient, but
         it is 3OC12HSL -- a different signaling molecule from either of
         Basu's -- measured as an effective cell-to-cell coefficient through a
         different bacterial lawn.

    So the lesson is the formula and the sourcing requirement, not a number:
    DO NOT TAKE A DIFFUSION COEFFICIENT FROM A PAPER WITHOUT CHECKING ITS
    UNITS AGAINST THE PAPER'S OWN GEOMETRY. If you have a D with a stated
    medium and a citation, pass it; this function will not guess one for you.

    Units are yours to keep consistent: D in length^2/time with gamma in
    1/time returns a length. D in mm^2/min with gamma in min^-1 returns mm.
    """
    D = np.asarray(D, float)
    gamma = np.asarray(gamma, float)
    if np.any(D <= 0.0):
        raise ValueError("D must be > 0 to have a penetration depth")
    if np.any(gamma <= 0.0):
        raise ValueError("gamma must be > 0; with no decay there is no "
                         "penetration depth -- the steady-state profile is "
                         "set by the geometry instead, and L^2/2D is the tool")
    return np.sqrt(D / gamma)


# ===========================================================================
# BASU'S BAND DETECTOR, in the liquid-phase limit
# ===========================================================================
# The printed BD2 set, Basu p.1134, where the text says these parameters
# approximate the behavior of BD2. MODELLED in NUMBERS.md's sense -- a chosen
# parameter set, not a fit to any data reported in that paper, and no source is
# cited for any entry. Concentrations in uM, rates in min^-1.
BASU_BD2 = {
    "alpha_G": 2.0,        # uM/min, GFP synthesis
    "alpha_L1": 1.0,       # uM/min, LacI synthesis, CI-repressible route
    "alpha_L2": 1.0,       # uM/min, LacI synthesis, LuxR-AHL-activated route
    "alpha_C": 1.0,        # uM/min, CI synthesis
    "beta_L": 0.8,         # uM, repression coefficient, LacI on GFP
    "beta_C": 0.008,       # uM, repression coefficient, CI on LacI
    "gamma_G": 0.0692,     # 1/min, LVA-tagged: ln2/0.0692 = 10.0 min
    "gamma_C": 0.0692,     # 1/min
    "gamma_L": 0.0231,     # 1/min, untagged: ln2/0.0231 = 30.0 min
    "gamma_R": 0.0231,     # 1/min
    "theta_R": 0.01,       # uM, LuxR/AHL activation coefficient
    "eta1": 2.0,           # cooperativity, LacI on GFP
    "eta2": 2.0,           # cooperativity, CI on LacI
    "eta3": 1.0,           # LuxR-AHL complex on its promoters -- NOT
                           # cooperative; the cooperativity is all in eq. (4)
    "rho_R": 0.5,          # uM^-3/min, LuxR/AHL dimerization
    "gamma_A": 0.01,       # 1/min, AHL decay: ln2/0.01 = 69.3 min
    "LuxR": 0.5,           # uM, fixed
}


def basu_params(variant="BD2"):
    """A fresh copy of Basu's printed parameters for BD1, BD2 or BD3.

    The variants are the paper's own, p.1134, and each is a change to the BD2
    set and nothing else:

      BD1   rho_R increased TENFOLD. The hypersensitive LuxR-G2F mutant is
            represented in the model by the dimerization constant alone --
            nothing else moves. Since A enters only through
            R = rho_R [LuxR]^2 A^2 / gamma_R, a tenfold rho_R shifts the whole
            dose-response to lower AHL by exactly sqrt(10) and changes its
            shape not at all.
      BD2   as printed.
      BD3   alpha_G, alpha_L2 and [LuxR] HALVED. Halving [LuxR] moves the
            response by a factor of two the other way (R goes as [LuxR]^2);
            halving alpha_G scales the output and so cannot move an edge
            defined as a fraction of the peak; halving alpha_L2 does change
            the shape, so BD3's shift is not a pure rescaling.

    Returns a dict, so mutating it cannot reach `BASU_BD2`.
    """
    p = dict(BASU_BD2)
    if variant == "BD2":
        return p
    if variant == "BD1":
        p["rho_R"] = 10.0 * BASU_BD2["rho_R"]
        return p
    if variant == "BD3":
        p["alpha_G"] = 0.5 * BASU_BD2["alpha_G"]
        p["alpha_L2"] = 0.5 * BASU_BD2["alpha_L2"]
        p["LuxR"] = 0.5 * BASU_BD2["LuxR"]
        return p
    raise ValueError(f"variant must be 'BD1', 'BD2' or 'BD3'; got {variant!r}. "
                     f"HD1 and HD3 are the high-detect strains and are the "
                     f"same changes applied to a circuit that also drops "
                     f"equation (3) -- not this function.")


def _required(params, keys):
    missing = [k for k in keys if k not in params]
    if missing:
        raise ValueError(f"params is missing {missing}. Start from "
                         f"posb.communities.basu_params('BD2') and change what "
                         f"you mean to change.")


def band_detect_response(AHL, params):
    """Steady-state GFP of Basu's band detector, in the LIQUID-PHASE LIMIT.

    T65. The liquid-phase limit is the paper's own: "liquid-phase simulations
    omit equation (5) entirely" (p.1134). Dropping the discrete Laplacian
    leaves AHL as an imposed constant rather than a state variable, and
    equations (1)-(4) then have an algebraic steady state that composes in one
    direction with no solving at all:

        R = rho_R [LuxR]^2 A^2 / gamma_R                           from (4)
        a = R^eta3 / (theta_R^eta3 + R^eta3)        the shared activation
        C = (alpha_C / gamma_C) a                                  from (3)
        L = [ alpha_L1 / (1 + (C/beta_C)^eta2) + alpha_L2 a ] / gamma_L  (2)
        G = (alpha_G / gamma_G) / (1 + (L/beta_L)^eta1)             from (1)

    WHY IT IS NON-MONOTONE, which is the whole circuit. L has two production
    terms and they move in opposite directions with A. At low A both repressors
    are basal, the CI-repressible route runs at full rate, L is high and GFP is
    off. At high A, CI has shut that route off but the LuxR-AHL-activated route
    has replaced it, L is high again and GFP is off again. In between, CI has
    silenced wild-type LacI while LacI_M1 is still below the threshold that
    would silence GFP -- and GFP is on. The parameter that makes the window
    exist is beta_C << beta_L: 0.008 uM against 0.8 uM in BD2, a factor of 100.
    THE HUNDREDFOLD IS BD2'S VALUE AND NOT A REQUIREMENT -- Basu's own Figs. 4b
    and 4c form rings at ratios of 28.6 and 3.3.

    WHERE THE MODEL SIMPLIFIES THE BIOLOGY, stated because the prose and the
    model do not say the same thing. There are five species, so LacI and
    LacI_M1 are LUMPED into the single variable L with one repression
    coefficient beta_L. The model cannot express "CI represses better than
    LacI_M1" as a property of two repressors; it expresses it as
    beta_C << beta_L.

    AHL is in uM and may be an array. Returns GFP in uM.
    """
    _required(params, ("rho_R", "LuxR", "gamma_R", "theta_R", "eta1", "eta2",
                       "eta3", "alpha_C", "gamma_C", "alpha_L1", "alpha_L2",
                       "beta_C", "beta_L", "gamma_L", "alpha_G", "gamma_G"))
    A = np.asarray(AHL, float)
    if np.any(A < 0.0):
        raise ValueError("AHL is a concentration and cannot be negative")
    p = params
    R = p["rho_R"] * p["LuxR"] ** 2 * A ** 2 / p["gamma_R"]
    # The activation is shared by equations (2) and (3): the same R drives CI
    # and the LacI_M1 route, with the same theta_R and the same eta3. That is
    # why the band is a competition between two terms and not two thresholds.
    Re = R ** p["eta3"]
    a = Re / (p["theta_R"] ** p["eta3"] + Re)
    C = p["alpha_C"] * a / p["gamma_C"]
    L = (p["alpha_L1"] / (1.0 + (C / p["beta_C"]) ** p["eta2"])
         + p["alpha_L2"] * a) / p["gamma_L"]
    return (p["alpha_G"] / p["gamma_G"]) / (1.0 + (L / p["beta_L"]) ** p["eta1"])


def _band_center(params):
    """The AHL at which the LuxR-AHL activation is half-maximal.

    R = theta_R when rho_R [LuxR]^2 A^2 / gamma_R = theta_R, so
    A_c = sqrt(theta_R gamma_R / (rho_R [LuxR]^2)). Everything interesting
    happens within a few decades of this, for any parameter set, which is how
    the searches below pick a window instead of hard-coding one.
    """
    p = params
    return float(np.sqrt(p["theta_R"] * p["gamma_R"]
                         / (p["rho_R"] * p["LuxR"] ** 2)))


def band_peak(params, decades=5.0, points=4001):
    """The AHL at the band's maximum, and the GFP there. Returns (A_peak, G_peak).

    Located rather than sampled: a log grid spanning `decades` either side of
    `_band_center` brackets the maximum, and a bounded scalar minimization of
    -G refines it. The grid is deliberately fine (about 400 points per decade
    by default) because THE RESPONSE IS NON-MONOTONE AND A COARSE GRID
    STRADDLES ITS EXTREMA: on the BD2 set a one-point-per-decade sweep reports
    a peak nearly six times too low and reports the band as still rising.
    """
    from scipy.optimize import minimize_scalar
    c = np.log10(_band_center(params))
    lg = np.linspace(c - decades, c + decades, int(points))
    G = band_detect_response(10.0 ** lg, params)
    i = int(np.argmax(G))
    if i == 0 or i == len(lg) - 1:
        raise ValueError(
            f"the maximum is at the edge of the search window "
            f"[1e{lg[0]:.2f}, 1e{lg[-1]:.2f}] uM, so this response has no "
            f"interior peak in it -- widen `decades` or check the parameters")
    r = minimize_scalar(lambda x: -float(band_detect_response(10.0 ** x,
                                                              params)),
                        bounds=(lg[i - 1], lg[i + 1]), method="bounded",
                        options={"xatol": 1e-12})
    return 10.0 ** float(r.x), float(-r.fun)


def band_edges(params, frac=0.5, decades=5.0, points=4001):
    """The low and high AHL edges of the band. SOLVED, not read off a plot.

    T65. An edge needs a definition, and this one is the paper's: Basu locate a
    ring by the first coordinate whose fluorescence exceeds 50 % of the maximum
    steady-state fluorescence (p.1134, the "shift begin" criterion). So an edge
    here is where the response crosses `frac` of its own peak, and `frac`
    defaults to 0.5 for that reason. Pass another fraction and you are asking a
    different question, which is fine as long as the slide says which.

    Both edges come from `scipy.optimize.brentq` on G(A) - frac*G_peak, in
    log10 A, bracketed by the peak on one side and the flat tail on the other.
    Returns (A_low, A_high) in uM, and A_low < A_peak < A_high always.

    The band is narrow on the BD2 set: the half-maximum edges sit a factor of
    2.65 apart. That is a property of the printed parameters in the
    liquid-phase limit and not of the measured strains, whose dose-response
    Basu show in Fig. 2d.
    """
    from scipy.optimize import brentq
    frac = float(frac)
    if not 0.0 < frac < 1.0:
        raise ValueError(f"frac is a fraction of the peak and must lie "
                         f"strictly in (0,1); got {frac}")
    A_peak, G_peak = band_peak(params, decades=decades, points=points)
    target = frac * G_peak
    x_peak = np.log10(A_peak)
    c = np.log10(_band_center(params))
    lo_bound, hi_bound = c - decades, c + decades

    def f(x):
        return float(band_detect_response(10.0 ** x, params)) - target

    if f(lo_bound) >= 0.0 or f(hi_bound) >= 0.0:
        raise ValueError(
            f"the response does not fall below {frac:g} of its peak inside "
            f"[1e{lo_bound:.2f}, 1e{hi_bound:.2f}] uM, so this band has no "
            f"edge at that fraction -- widen `decades`, or the parameters do "
            f"not give a band")
    lo = brentq(f, lo_bound, x_peak, xtol=1e-14, rtol=8.9e-16)
    hi = brentq(f, x_peak, hi_bound, xtol=1e-14, rtol=8.9e-16)
    return 10.0 ** lo, 10.0 ** hi


# ===========================================================================
# THE MINIMAL SENDER/RECEIVER PAIR
# ===========================================================================
def sender_receiver(A, S, k_I, gamma_A, D=0.0, alpha=1.0, theta=1.0, n=1.0):
    """The pair the session writes with the room. Returns (dA_dt, output).

    T64, and it is on PS9 and on the final.

        sender:    dA/dt = k_I S - gamma_A A   (- D A in a reactor)
        receiver:  output = alpha A^n / (theta^n + A^n)

    S is the sender density (or the synthase level -- whatever k_I is per unit
    of), A the signal concentration, gamma_A its decay, D the dilution rate of
    the vessel, which is zero on a plate and nonzero in a chemostat.

    k_I IS A REQUIRED ARGUMENT WITH NO DEFAULT, AND THAT IS DELIBERATE.
    NEITHER PAPER PRINTS A SENDER SYNTHESIS RATE. Basu's model is
    receiver-only -- equations (1)-(4) take AHL as an input -- and their
    Methods tune the senders to put a ring at 7 mm without printing the value
    they tuned to. Balagadde's equations are in a supplement this repository
    does not hold, and the main text prints none. So the session supplies k_I
    itself and says that it is doing so, out loud, on the slide: k_I is a
    PROMOTER CHOICE, and that is the one design knob this half of the model
    has.

    THE STEADY STATE IS ONE LINE, which is why there is no solver here:

        A* = k_I S / (gamma_A + D)

    so the signal a receiver sees is set by the ratio of a promoter to a pump,
    and the reactor's dilution competes directly with the molecule's own decay.

    THE RECEIVER'S THETA IS NOT SESSION 10'S 47 nM. That slide reports a
    SATURATION level -- above about 47 nM the output stops growing -- and a
    saturation is not a threshold. `theta` here is the half-maximal point of
    the Hill form and defaults to 1.0 only because there is nothing to default
    it to; pass the number you mean and name where it came from.
    """
    A = np.asarray(A, float)
    S = np.asarray(S, float)
    k_I = float(k_I)
    gamma_A = float(gamma_A)
    D = float(D)
    if np.any(A < 0.0):
        raise ValueError("A is a concentration and cannot be negative")
    if np.any(S < 0.0):
        raise ValueError("S is a density and cannot be negative")
    if k_I < 0.0:
        raise ValueError(f"k_I is a synthesis rate and must be >= 0; got {k_I}")
    if gamma_A < 0.0 or D < 0.0:
        raise ValueError(f"gamma_A and D are removal rates and must be >= 0; "
                         f"got {gamma_A}, {D}")
    if gamma_A + D <= 0.0:
        raise ValueError("gamma_A + D must be > 0; with neither decay nor "
                         "dilution the signal accumulates without bound and "
                         "there is no steady state to talk about")
    theta = float(theta)
    if theta <= 0.0:
        raise ValueError(f"theta must be > 0; got {theta}")
    dA_dt = k_I * S - (gamma_A + D) * A
    An = A ** n
    output = alpha * An / (theta ** n + An)
    return dA_dt, output


# ===========================================================================
# THE PREDATOR-PREY PAIR -- THE DEPOSITED MODEL, FOUR STATES
# ===========================================================================
# WHOSE MODEL THIS IS, AND IT IS NOT THE PAPER'S TEXT. Balagadde, Tsoi, You &
# Lin print no equations: their main text names "equations S14-S17" and the
# supplement is not in this repository. What IS available is the BioModels
# deposit BIOMD0000000296, read through the JWS Online curation, which states
# it was obtained from BioModels and curated by reproducing the paper's
# figures. NUMBERS.md sec 20 is the transcription and is the specification for
# everything below. A slide using these equations says it is using the
# DEPOSITED model, because that is a different provenance from the paper's
# text and the two cannot be cited as one.
#
# THE SIGNALS ARE STATE VARIABLES. That is the finding, and it is what makes
# the system oscillate -- see `pp_qss_model`. Reactions as deposited:
#
#   J0  predator growth   kc1 * C1 * (1 - (C1 + C2)/Cm)
#   J1  predator death    (D + d1 * K1/(K1 + A2^2)) * C1
#   J2  prey growth       kc2 * C2 * (1 - (C1 + C2)/Cm)
#   J3  prey death        (D + d2 * A1^2/(K2 + A1^2)) * C2
#   J4  3OC12HSL synth    kA1 * C1
#   J5  3OC12HSL removal  (dAA1 + D) * A1
#   J6  3OC6HSL synth     kA2 * C2
#   J7  3OC6HSL removal   (dAA2 + D) * A2
#
# Read the two death terms as the circuit: A2 is the PREY's signal and it
# RESCUES the predator, so the predator's death falls as A2 rises --
# K1/(K1 + A2^2). A1 is the PREDATOR's signal and it KILLS the prey, so the
# prey's death rises with it -- A1^2/(K2 + A1^2). Both are squared, i.e. both
# dose-responses are cooperative, and the halves sit at sqrt(K1) and sqrt(K2).
# Note that dilution D appears four times: on both populations and on both
# signals, and in the signal terms it competes directly with abiotic decay.
PP_PARAMS = {
    "kc1": 0.8,        # 1/h, predator growth
    "kc2": 0.4,        # 1/h, prey growth
    "Cm": 100.0,       # shared carrying capacity
    "d1": 1.0,         # 1/h, predator death AT IPTG = 5 -- an assignment rule
    "d2": 0.3,         # 1/h, prey death
    "K1": 10.0,        # (signal)^2, prey signal rescuing the predator
    "K2": 10.0,        # (signal)^2, predator signal killing the prey
    "kA1": 0.1,        # predator's 3OC12HSL synthesis, per cell
    "kA2": 0.035,      # prey's 3OC6HSL synthesis AT IPTG = 5 -- assignment rule
    "dAA1": 0.017,     # 1/h, abiotic decay of 3OC12HSL
    "dAA2": 0.11,      # 1/h, abiotic decay of 3OC6HSL
    "D": 0.1125,       # 1/h, dilution
}

# The deposit's initial condition, kept because a trajectory figure needs one
# and inventing a different one would make the figure unreproducible.
PP_INITIAL = (20.0, 20.0, 0.1, 0.1)      # C1, C2, A1, A2
PP_IPTG = 5.0                            # the deposit's own IPTG

_PP_KEYS = ("kc1", "kc2", "Cm", "d1", "d2", "K1", "K2", "kA1", "kA2",
            "dAA1", "dAA2", "D")


def iptg_assignment_rules(iptg):
    """The deposit's two assignment rules. Returns (kA2, d1).

        kA2 = 0.02 + 0.03 * IPTG^2 / (5^2 + IPTG^2)
        d1  = 0.5  +        IPTG^2 / (5^2 + IPTG^2)

    IPTG ENTERS THE MODEL NOWHERE ELSE. It tunes the prey's signal synthesis
    and the predator's death rate, and nothing else -- which is exactly why the
    paper's own experimental route across the Hopf is IPTG rather than
    dilution, and it settles what the session's review asked about Box 1B being
    spanned by strain parameters. It is also why IPTG is not a clean knob and
    the authors say so: one chemical moves one parameter in each population.

    At the deposit's IPTG = 5 both Hill terms are exactly one half, so
    kA2 = 0.035 and d1 = 1.0. At IPTG = 0 they are 0.02 and 0.5, and d1 = 0.5
    is BELOW kc1 = 0.8 -- so uninduced, the predator can live without the prey,
    and `pp_steady_states` returns a predator-only state that does not exist at
    IPTG = 5. That switch is the circuit, in one parameter.
    """
    iptg = np.asarray(iptg, float)
    if np.any(iptg < 0.0):
        raise ValueError("IPTG is a concentration and cannot be negative")
    h = iptg ** 2 / (5.0 ** 2 + iptg ** 2)
    return 0.02 + 0.03 * h, 0.5 + h


def pp_params(iptg=PP_IPTG, **overrides):
    """The deposited parameter set with kA2 and d1 set by the IPTG rules.

    A fresh dict, so mutating it cannot reach `PP_PARAMS`. Pass `iptg` to sweep
    the paper's own knob; pass any other parameter by keyword to override it.
    """
    p = dict(PP_PARAMS)
    kA2, d1 = iptg_assignment_rules(iptg)
    p["kA2"] = float(kA2)
    p["d1"] = float(d1)
    for k, v in overrides.items():
        if k not in _PP_KEYS:
            raise ValueError(f"{k!r} is not a parameter of this model; "
                             f"expected one of {_PP_KEYS}")
        p[k] = float(v)
    return p


def predator_prey_model(c, params):
    """dc/dt for the deposited four-state model. State is (C1, C2, A1, A2).

    C1 predator, C2 prey, A1 the predator's 3OC12HSL, A2 the prey's 3OC6HSL:

        dC1/dt = kc1 C1 (1 - (C1+C2)/Cm) - (D + d1 K1/(K1 + A2^2)) C1
        dC2/dt = kc2 C2 (1 - (C1+C2)/Cm) - (D + d2 A1^2/(K2 + A1^2)) C2
        dA1/dt = kA1 C1 - (dAA1 + D) A1
        dA2/dt = kA2 C2 - (dAA2 + D) A2

    FOUR STATES, NOT TWO, AND THAT IS THE WHOLE POINT. Each population's
    signal has its own synthesis and its own removal, so a population's effect
    on the other arrives LATE -- the signal has to accumulate first, on a clock
    set by dAA + D. That lag is where the oscillation lives. Eliminate it and
    it goes: `pp_qss_model` is the same circuit with the signals at
    quasi-steady state, and it cannot oscillate at any parameter values.

    Accepts an array whose last axis is the four states, so a grid of states
    can be passed at once.
    """
    _required(params, _PP_KEYS)
    c = np.asarray(c, float)
    if c.shape[-1] != 4:
        raise ValueError(
            f"state is (C1, C2, A1, A2) -- four entries, because the signals "
            f"are state variables in the deposited model; got shape {c.shape}. "
            f"For the two-state reduction use pp_qss_model.")
    if np.any(c < 0.0):
        raise ValueError("a density and a concentration cannot be negative")
    p = params
    C1, C2, A1, A2 = c[..., 0], c[..., 1], c[..., 2], c[..., 3]
    L = 1.0 - (C1 + C2) / p["Cm"]
    m1 = p["D"] + p["d1"] * p["K1"] / (p["K1"] + A2 ** 2)
    m2 = p["D"] + p["d2"] * A1 ** 2 / (p["K2"] + A1 ** 2)
    return np.stack([p["kc1"] * C1 * L - m1 * C1,
                     p["kc2"] * C2 * L - m2 * C2,
                     p["kA1"] * C1 - (p["dAA1"] + p["D"]) * A1,
                     p["kA2"] * C2 - (p["dAA2"] + p["D"]) * A2], axis=-1)


def pp_qss_signals(c, params):
    """The two signals at quasi-steady state. Returns (A1, A2).

        A1 = kA1 C1 / (dAA1 + D)        A2 = kA2 C2 / (dAA2 + D)

    Set dA1/dt = dA2/dt = 0 in the deposited model and this is what is left:
    each signal becomes a multiple of the population that makes it, with the
    constant of proportionality set by how fast the vessel and the medium
    between them clear it. Session 4's QSSA, applied to a molecule outside the
    cell instead of inside one.
    """
    _required(params, _PP_KEYS)
    c = np.asarray(c, float)
    if c.shape[-1] < 2:
        raise ValueError(f"need at least (C1, C2); got shape {c.shape}")
    p = params
    C1, C2 = c[..., 0], c[..., 1]
    return (p["kA1"] * C1 / (p["dAA1"] + p["D"]),
            p["kA2"] * C2 / (p["dAA2"] + p["D"]))


def pp_qss_model(c, params):
    """dc/dt for the two-state reduction. State is (C1, C2).

    The deposited model with the signals at quasi-steady state substituted
    back in, which is the move the session makes with the room:

        a1 = kA1/(dAA1 + D),  a2 = kA2/(dAA2 + D)
        dC1/dt = kc1 C1 (1 - T/Cm) - (D + d1 K1/(K1 + (a2 C2)^2)) C1
        dC2/dt = kc2 C2 (1 - T/Cm) - (D + d2 (a1 C1)^2/(K2 + (a1 C1)^2)) C2

    THIS MODEL CANNOT OSCILLATE, AT ANY PARAMETER VALUES, and the proof is two
    lines. At an interior fixed point both per-capita rates vanish, so the
    growth term cancels the death term on each diagonal and all that is left
    of each is the logistic self-limitation:

        tr J = -(kc1 C1 + kc2 C2) / Cm

    exactly. Every quantity in it is positive, so the trace is strictly
    negative at every interior fixed point of every parameter set, and a 2x2
    system whose trace cannot reach zero has no Hopf bifurcation. The cross
    terms do not enter the trace at all -- they are off the diagonal, and they
    only ever set the determinant.

    SO THE OSCILLATION LIVES IN THE SIGNAL DYNAMICS, which is the session's
    result and is the same lesson as session 11's repressilator in a new
    substrate: what makes a loop oscillate is the lag around it. Here the lag
    is the time a population's signal takes to accumulate, on the clock
    dAA + D, and the QSSA is precisely the approximation that throws it away.
    Note that the FIXED POINTS do not move -- `pp_steady_states` serves both
    models, because substituting the quasi-steady-state signals is exact AT a
    fixed point. Only the stability changes.
    """
    _required(params, _PP_KEYS)
    c = np.asarray(c, float)
    if c.shape[-1] != 2:
        raise ValueError(f"state is (C1, C2) -- two entries; got shape "
                         f"{c.shape}. For the four-state deposited model use "
                         f"predator_prey_model.")
    if np.any(c < 0.0):
        raise ValueError("a population density cannot be negative")
    p = params
    C1, C2 = c[..., 0], c[..., 1]
    A1, A2 = pp_qss_signals(c, p)
    L = 1.0 - (C1 + C2) / p["Cm"]
    m1 = p["D"] + p["d1"] * p["K1"] / (p["K1"] + A2 ** 2)
    m2 = p["D"] + p["d2"] * A1 ** 2 / (p["K2"] + A1 ** 2)
    return np.stack([p["kc1"] * C1 * L - m1 * C1,
                     p["kc2"] * C2 * L - m2 * C2], axis=-1)


def pp_jacobian(state, params):
    """The Jacobian, analytic. 4x4 for a four-state point, 2x2 for a two-state one.

    Which model you get is decided by the length of `state`, because that is
    the only thing that distinguishes them: four entries is the deposited
    system, two is the quasi-steady-state reduction. Both are differentiated by
    hand rather than by finite difference, because move 4 is the room writing
    this matrix down.

    With T = C1 + C2, L = 1 - T/Cm and the two death rates

        m1 = D + d1 K1/(K1 + A2^2)      m2 = D + d2 A1^2/(K2 + A1^2)

    the derivatives of the death rates with respect to the signals are

        dm1/dA2 = -2 d1 K1 A2 / (K1 + A2^2)^2       (rescue: negative)
        dm2/dA1 = +2 d2 K2 A1 / (K2 + A1^2)^2       (killing: positive)

    and the four-state matrix is

        [ kc1 L - kc1 C1/Cm - m1,  -kc1 C1/Cm,   0,          -C1 dm1/dA2 ]
        [ -kc2 C2/Cm,  kc2 L - kc2 C2/Cm - m2,  -C2 dm2/dA1,  0          ]
        [ kA1,          0,         -(dAA1 + D),  0                       ]
        [ 0,            kA2,        0,          -(dAA2 + D)              ]

    The two structural zeros in the top rows are worth saying out loud: the
    predator does not respond to its own signal and the prey does not respond
    to its own either. Every interaction in this community goes through the
    bottom two rows, which is the statement that the wire is outside the cell.

    The 2x2 is the same top-left block with the signal columns folded in
    through dA1/dC1 = a1 and dA2/dC2 = a2.
    """
    _required(params, _PP_KEYS)
    st = np.asarray(state, float)
    if st.ndim != 1 or st.shape[0] not in (2, 4):
        raise ValueError(
            f"state must be (C1, C2, A1, A2) for the deposited model or "
            f"(C1, C2) for the quasi-steady-state reduction; got shape "
            f"{st.shape}")
    if np.any(st < 0.0):
        raise ValueError("a density and a concentration cannot be negative")
    p = params
    full = st.shape[0] == 4
    C1, C2 = float(st[0]), float(st[1])
    if full:
        A1, A2 = float(st[2]), float(st[3])
    else:
        a1, a2 = pp_qss_signals(st, p)
        A1, A2 = float(a1), float(a2)
    L = 1.0 - (C1 + C2) / p["Cm"]
    m1 = p["D"] + p["d1"] * p["K1"] / (p["K1"] + A2 ** 2)
    m2 = p["D"] + p["d2"] * A1 ** 2 / (p["K2"] + A1 ** 2)
    dm1_dA2 = -2.0 * p["d1"] * p["K1"] * A2 / (p["K1"] + A2 ** 2) ** 2
    dm2_dA1 = 2.0 * p["d2"] * p["K2"] * A1 / (p["K2"] + A1 ** 2) ** 2
    j00 = p["kc1"] * L - p["kc1"] * C1 / p["Cm"] - m1
    j11 = p["kc2"] * L - p["kc2"] * C2 / p["Cm"] - m2
    if full:
        return np.array([
            [j00, -p["kc1"] * C1 / p["Cm"], 0.0, -C1 * dm1_dA2],
            [-p["kc2"] * C2 / p["Cm"], j11, -C2 * dm2_dA1, 0.0],
            [p["kA1"], 0.0, -(p["dAA1"] + p["D"]), 0.0],
            [0.0, p["kA2"], 0.0, -(p["dAA2"] + p["D"])]])
    slope1 = p["kA1"] / (p["dAA1"] + p["D"])      # dA1/dC1
    slope2 = p["kA2"] / (p["dAA2"] + p["D"])      # dA2/dC2
    return np.array([
        [j00, -p["kc1"] * C1 / p["Cm"] - C1 * dm1_dA2 * slope2],
        [-p["kc2"] * C2 / p["Cm"] - C2 * dm2_dA1 * slope1, j11]])


def pp_steady_states(params, grid=4001):
    """Every fixed point of the deposited model. Returns a dict of (m,4) arrays.

    Keys, each an array of shape (m, 4) in (C1, C2, A1, A2) with m possibly
    zero:

        'washout'          always [[0, 0, 0, 0]]
        'prey_only'        when D < kc2
        'predator_only'    when D + d1 < kc1
        'coexistence'      the interior points, by the reduction below

    IT SERVES BOTH MODELS. Substituting the quasi-steady-state signals is
    EXACT at a fixed point, so the (C1, C2) of every state here is also a fixed
    point of `pp_qss_model` and the (A1, A2) are what `pp_qss_signals` returns
    for it. Only the stability differs between the two models, which is why the
    session can put the same phase portrait under both.

    THE BOUNDARY STATES ARE CLOSED FORMS. At C1 = 0 the predator's signal is
    absent, so the prey's death term is exactly D and C2 = Cm(1 - D/kc2). At
    C2 = 0 the prey's signal is absent, so K1/(K1 + 0) = 1 and the predator
    carries its FULL death rate: C1 = Cm(1 - (D + d1)/kc1). At the deposit's
    IPTG = 5, d1 = 1.0 exceeds kc1 = 0.8 and there is no predator-only state at
    any dilution rate -- the predator needs the prey's signal to survive, which
    is the circuit. Drop IPTG below about 2.4 and the state appears.

    THE INTERIOR STATES ARE ONE SCALAR ROOT-FIND, not a 4-D solve. Let
    g = 1 - T/Cm be the shared logistic factor. Both populations' per-capita
    rates vanish at an interior point, so

        kc1 g - D = d1 K1/(K1 + A2^2)   ->  A2^2 = K1 (d1/(kc1 g - D) - 1)
        kc2 g - D = d2 A1^2/(K2 + A1^2) ->  A1^2 = K2 (kc2 g - D)/(d2 - (kc2 g - D))

    which gives both signals as explicit functions of the single unknown g, on
    the bounded interval where both brackets are positive. The signal equations
    then give the populations, C1 = A1 (dAA1 + D)/kA1 and
    C2 = A2 (dAA2 + D)/kA2, and the interior points are where those add up to
    the Cm(1 - g) that g itself asserts. A sign change on a bounded interval,
    so bisection and nothing more. Note that this needs no relation between
    kc1 and kc2: g is a factor of both growth terms.

    `grid` is how finely the bracketing scan samples g, and it matters. At the
    deposit's parameters there is a NARROW FOLD just below the dilution rate
    where coexistence is lost -- three interior points for D between about
    0.1755 and 0.1764, two of them within 0.6 of each other in C1 -- and the
    default scan finds all three at D = 0.176 but misses one at D = 0.1762.
    Raise `grid` when working near a fold; the residuals tell you which roots
    are real.
    """
    from scipy.optimize import brentq
    _required(params, _PP_KEYS)
    p = params
    for key in ("Cm", "K1", "K2", "kA1", "kA2"):
        if p[key] <= 0.0:
            raise ValueError(f"{key} must be > 0; got {p[key]}")
    if p["D"] < 0.0:
        raise ValueError(f"D is a dilution rate and must be >= 0; got {p['D']}")
    if p["dAA1"] + p["D"] <= 0.0 or p["dAA2"] + p["D"] <= 0.0:
        raise ValueError("each signal needs some removal: dAA + D must be > 0")
    D, Cm = p["D"], p["Cm"]
    s1 = p["kA1"] / (p["dAA1"] + D)
    s2 = p["kA2"] / (p["dAA2"] + D)

    out = {"washout": np.zeros((1, 4))}
    if D < p["kc2"]:
        C2 = Cm * (1.0 - D / p["kc2"])
        out["prey_only"] = np.array([[0.0, C2, 0.0, s2 * C2]])
    else:
        out["prey_only"] = np.zeros((0, 4))
    if D + p["d1"] < p["kc1"]:
        C1 = Cm * (1.0 - (D + p["d1"]) / p["kc1"])
        out["predator_only"] = np.array([[C1, 0.0, s1 * C1, 0.0]])
    else:
        out["predator_only"] = np.zeros((0, 4))

    g_lo = max(D / p["kc1"], D / p["kc2"], 0.0)
    g_hi = min((D + p["d1"]) / p["kc1"], (D + p["d2"]) / p["kc2"], 1.0)

    def _state(g):
        u1 = p["kc1"] * g - D
        u2 = p["kc2"] * g - D
        if not (0.0 < u1 < p["d1"] and 0.0 < u2 < p["d2"]):
            return None
        A2 = np.sqrt(p["K1"] * (p["d1"] / u1 - 1.0))
        A1 = np.sqrt(p["K2"] * u2 / (p["d2"] - u2))
        return A1 / s1, A2 / s2, A1, A2

    def mismatch(g):
        st = _state(g)
        if st is None:
            return np.nan
        return st[0] + st[1] - Cm * (1.0 - g)

    roots = []
    if g_hi > g_lo:
        gs = np.linspace(g_lo, g_hi, int(grid))
        vals = np.array([mismatch(g) for g in gs])
        for i in range(len(gs) - 1):
            a, b = vals[i], vals[i + 1]
            if np.isfinite(a) and np.isfinite(b) and a * b < 0.0:
                g = brentq(mismatch, gs[i], gs[i + 1], xtol=1e-16,
                           rtol=8.9e-16)
                st = _state(g)
                if st is not None and st[0] > 0.0 and st[1] > 0.0:
                    roots.append(list(st))
    out["coexistence"] = np.array(roots) if roots else np.zeros((0, 4))
    return out


def pp_oscillatory_focus(params, grid=4001):
    """The interior fixed point whose LEADING eigenvalue pair is complex.

    A Hopf is a complex pair crossing the imaginary axis, so an interior point
    whose leading eigenvalue is real cannot carry one and is not a candidate.
    At low dilution the deposited model has a second interior point, close to
    prey domination, whose leading eigenvalue is real and positive -- a saddle.
    Tracking it instead of the focus would return a dilution rate that is not a
    bifurcation at all, which is what this selection exists to prevent.

    Returns the state as a 4-vector, or None when there is no such point, or
    when there is more than one and the choice would be a guess.
    """
    hits = []
    for st in pp_steady_states(params, grid=grid)["coexistence"]:
        ev = np.linalg.eigvals(pp_jacobian(st, params))
        lead = ev[int(np.argmax(ev.real))]
        if abs(lead.imag) > 1e-6 * (1.0 + float(np.max(np.abs(ev)))):
            hits.append(st)
    return hits[0] if len(hits) == 1 else None


def pp_leading_real_part(params, model="full", grid=4001):
    """The largest real part in the spectrum at the oscillatory focus.

    `model` is "full" for the deposited four-state system or "qss" for the
    two-state reduction; the fixed point is the same either way and only the
    Jacobian changes. Returns NaN when there is no single focus to evaluate at,
    so that a sweep can pass over a fold rather than stopping on it.
    """
    if model not in ("full", "qss"):
        raise ValueError(f"model must be 'full' or 'qss'; got {model!r}")
    st = pp_oscillatory_focus(params, grid=grid)
    if st is None:
        return np.nan
    J = pp_jacobian(st if model == "full" else st[:2], params)
    return float(np.max(np.linalg.eigvals(J).real))


def pp_hopf_D(params, D_lo=0.0, D_hi=None, which="first", model="full",
              grid=401, state_grid=4001):
    """The dilution rate or rates at which the focus changes stability.

    Move 4's result. The leading real part at the oscillatory focus is scanned
    across D, every sign change is bisected, and `which` picks what comes back:
    "first" (default) the lowest crossing, "last" the highest, "all" a 1-D
    array of all of them.

    THE DEPOSITED MODEL HAS TWO, and they bound the oscillatory region in D
    rather than marking the single edge the design expected. Between them the
    interior focus is unstable; outside them it is stable; a little above the
    upper one coexistence is lost altogether.

    WITH model="qss" THERE ARE NONE, and that is not a search failure -- see
    `pp_qss_model`. The trace of the 2x2 is -(kc1 C1 + kc2 C2)/Cm at every
    interior fixed point, so it cannot reach zero and the raised error says so.

    What this does NOT return is a period, an amplitude, or the width of the
    oscillatory region as a quantity to compare against a figure. The width is
    a property of the deposited parameters and reading it against a
    digitization of the paper's Fig. 3C would be comparing a model to a
    one-significant-figure estimate off a rendered page.
    """
    from scipy.optimize import brentq
    if which not in ("first", "last", "all"):
        raise ValueError(f"which must be 'first', 'last' or 'all'; "
                         f"got {which!r}")
    if D_hi is None:
        # Above the slower growth rate nothing persists, so the whole interior
        # branch is inside this bracket by construction.
        D_hi = float(min(params["kc1"], params["kc2"]))
    if not 0.0 <= D_lo < D_hi:
        raise ValueError(f"need 0 <= D_lo < D_hi; got {D_lo}, {D_hi}")

    def lead(D):
        q = dict(params)
        q["D"] = float(D)
        return pp_leading_real_part(q, model=model, grid=state_grid)

    def lead_strict(D):
        v = lead(D)
        if not np.isfinite(v):
            raise ValueError(
                f"no single oscillatory focus at D = {D:g}, inside a bracket "
                f"whose ends have one -- there is a fold in here. Narrow the "
                f"bracket, or raise state_grid, and look at "
                f"pp_steady_states(...) across it.")
        return v

    Ds = np.linspace(D_lo, D_hi, int(grid))
    vals = np.array([lead(D) for D in Ds])
    found = []
    for i in range(len(Ds) - 1):
        a, b = vals[i], vals[i + 1]
        if np.isfinite(a) and np.isfinite(b) and a * b < 0.0:
            found.append(float(brentq(lead_strict, Ds[i], Ds[i + 1],
                                      xtol=1e-13, rtol=8.9e-16)))
    if not found:
        raise ValueError(
            f"no stability crossing in D on [{D_lo:g}, {D_hi:g}] for "
            f"model={model!r}. With model='qss' that is exact rather than a "
            f"search failure: the trace of the reduced 2x2 is "
            f"-(kc1 C1 + kc2 C2)/Cm at every interior fixed point, which is "
            f"strictly negative, so there is no Hopf at any dilution rate.")
    if which == "all":
        return np.array(found)
    return found[0] if which == "first" else found[-1]


# ===========================================================================
# DIVISION OF LABOR -- TSOI'S CRITERION, WITH THE BURDEN FORM AS AN ARGUMENT
# ===========================================================================
def burden_form(name, n=2.0):
    """A growth multiplier f(B) in [0,1] for a relative burden B. Returns a callable.

    The three forms Tsoi, Zhang, Wu, Lee & You draw on one pair of axes in
    their Fig. 2D:

        'linear'        f(B) = 1 - B, floored at zero
        'exponential'   f(B) = exp(-B)
        'hill'          f(B) = 1 / (1 + B^n)      -- the paper's Eqs. (11)-(13)

    The ORDERING of the three is a fact about the functions and not about the
    paper: f_hill(B) >= f_exp(B) >= f_lin(B) for every B >= 0, with equality
    only at B = 0, where all three are exactly 1. So at the same burden the
    Hill form leaves the host growing fastest and the linear form slowest, and
    the burden at which division of labor starts to win is highest for Hill and
    lowest for linear. Their Fig. 2D shows exactly that ordering and reads
    about 20, 36 and 78 off it.

    WHAT THAT FACTOR OF ABOUT FIVE IS NOT. Fig. 2D's own caption says the
    parameters were CHOSEN so that the Hill form reduces growth least and the
    linear form most. So the spread is the spread of a chosen example, not a
    property of the functional form, and the three numbers above are a
    one-significant-figure digitization of a rendered figure. The ordering
    survives that; the numbers do not, and nothing in this module reproduces
    them.
    """
    if callable(name):
        return name
    if name == "linear":
        return lambda B: np.maximum(0.0, 1.0 - np.asarray(B, float))
    if name == "exponential":
        return lambda B: np.exp(-np.asarray(B, float))
    if name == "hill":
        nn = float(n)
        if nn <= 0.0:
            raise ValueError(f"the Hill coefficient must be > 0; got {nn}")
        return lambda B: 1.0 / (1.0 + np.asarray(B, float) ** nn)
    raise ValueError(f"burden form must be 'linear', 'exponential', 'hill' or "
                     f"a callable B -> multiplier; got {name!r}")


def dol_criterion(beta_e1, gamma_e2, burden="hill", n=2.0,
                  mu_max=1.0, delta_v=0.1, rho=1.0,
                  eta=1.0, delta_me=0.0, alpha2_e2=1.0,
                  alpha1_e1=1.0, G=1.0, G1=1.0, G2=1.0,
                  rho1=None, rho2=None):
    """Does splitting the pathway across two strains raise the yield? Returns a dict.

    Tsoi's criterion, evaluated. The paper is entirely analysis -- there is no
    experiment in it anywhere -- so everything here is MODELLED, and the
    session states the criterion rather than deriving it.

    WHAT IS COMPUTED. Steady-state densities from their growth equations
    (8)-(10), v = rho (1 - delta_v/mu) when mu > delta_v and zero otherwise,
    with the burden entering through the growth rate:

        mu  = mu_max G  f(beta_e1 + gamma_e2)        the single cell carries both
        mu1 = mu_max G1 f(beta_e1)                   DOL-1 carries only E1
        mu2 = mu_max G2 f(gamma_e2)                  DOL-2 carries only E2

    THAT SPLIT IS THE WHOLE MECHANISM: the single cell's burden is the SUM and
    each DOL population's is one term, so splitting always helps growth. What
    it costs is in the denominators of their Eqs. (14) and (15), the
    steady-state product per cell, which this function evaluates directly:

        p_SC  = alpha1_e1 (delta_me + eta v) / (delta_me + delta_me eta/alpha2_e2 + eta v)
        p_DOL = alpha1_e1 eta v1            / (delta_me + delta_me eta/alpha2_e2 + eta v2)

    DOL is favored when the TOTAL yield is higher, p_DOL v2 > p_SC v, which is
    what `dol_favored` reports. Their Eq. (16) rewrites that as

        v1 v2 / (v^2 + eps v)  >  theta_I,      eps = delta_me/eta

    with theta_I the ratio of those two denominators -- the left side "the net
    gain in biomass by utilizing DOL", the right side "the reduced per-cell
    productivity of DOL", in their words. Both forms are returned, and they
    agree in sign wherever v > 0; the yield comparison is the definition and
    the ratio is the rewriting, so when v = 0 the yield comparison is still
    meaningful and the ratio is not.

    BURDEN IS PER ENZYME, NOT PER PATHWAY. `beta_e1` and `gamma_e2` are each
    one enzyme's burden, and the single cell carries their SUM while each split
    population carries one of them. Passing a pathway total here, rather than
    the per-enzyme value, halves the burden the model sees and can reverse
    `dol_favored`. Anything built on this function -- a slide, a guide item, a
    rubric -- has to say which of the two its numbers are.

    EPSILON DOES NOT DETERMINE THE ANSWER, so pass `eta` and `delta_me` and do
    not reason from their ratio. `theta_I` depends on the two SEPARATELY. Over
    the family of (eta, delta_me) pairs that all give eps = 0.5, with the
    defaults otherwise and a Hill burden at n = 2, the burden at which DOL
    starts to win runs from 1.3413 to 1.3663.

    A SPURIOUS ROOT, FOR ANYONE LOCATING THE BORDER NUMERICALLY. The yield
    margin `yield_dol - yield_sc` is identically ZERO once both populations are
    dead, which at the defaults happens above beta_e1 = gamma_e2 = 3.0: the
    single cell dies at 1.5 because it carries both enzymes, and each split
    population dies at 3.0 carrying one. So a bisection over any bracket that
    contains 3.0 returns 3.0 rather than the crossing you wanted -- `brentq`
    over [0.3, 3.0] returns exactly 3.0. BRACKET BELOW THE EXTINCTION POINT,
    or scan the margin first and bracket a sign change you have actually seen.

    THE ASSUMPTION THAT DOES THE MOST WORK AND IS EASIEST TO MISS:
    rho1 = rho2 = rho/2 by default, which is theirs. THE TWO DOL POPULATIONS
    SPLIT THE SINGLE-CELL CARRYING CAPACITY. So the "gain in biomass" is not a
    gain in total capacity -- it is a gain in how much of a HALVED capacity
    each population can occupy once the burden is split. At zero burden that
    is a straight loss: v1 v2/v^2 = 1/4 against theta_I = 1/2, and the single
    cell wins. Division of labor has to earn its way out of a factor of four.

    delta_me defaults to 0, which is their eps = 0 regime (delta_me << eta,
    the assumption behind Eq. 17). `burden` takes a name or a callable, so the
    functional form is the caller's choice and not this module's.
    """
    f = burden_form(burden, n=n)
    if mu_max <= 0.0 or delta_v < 0.0 or rho <= 0.0:
        raise ValueError(f"need mu_max > 0, delta_v >= 0, rho > 0; got "
                         f"{mu_max}, {delta_v}, {rho}")
    if eta <= 0.0 or delta_me < 0.0 or alpha2_e2 <= 0.0:
        raise ValueError(f"need eta > 0, delta_me >= 0, alpha2_e2 > 0; got "
                         f"{eta}, {delta_me}, {alpha2_e2}")
    if min(beta_e1, gamma_e2) < 0.0:
        raise ValueError("a burden is non-negative")
    r1 = 0.5 * rho if rho1 is None else float(rho1)
    r2 = 0.5 * rho if rho2 is None else float(rho2)

    mu = mu_max * G * float(f(beta_e1 + gamma_e2))
    mu1 = mu_max * G1 * float(f(beta_e1))
    mu2 = mu_max * G2 * float(f(gamma_e2))

    def density(m, cap):
        # v = cap (1 - delta_v/mu), and a population whose growth rate cannot
        # cover its own turnover does not persist. Returning 0.0 rather than a
        # negative density is the whole content of the `else`.
        if m <= delta_v:
            return 0.0
        return cap * (1.0 - delta_v / m)

    v = density(mu, rho)
    v1 = density(mu1, r1)
    v2 = density(mu2, r2)

    eps = delta_me / eta
    base = delta_me + delta_me * eta / alpha2_e2
    den_sc = base + eta * v
    den_dol = base + eta * v2
    theta_I = np.inf if den_sc == 0.0 else den_dol / den_sc

    p_sc = 0.0 if den_sc == 0.0 else alpha1_e1 * (delta_me + eta * v) / den_sc
    p_dol = 0.0 if den_dol == 0.0 else alpha1_e1 * eta * v1 / den_dol
    yield_sc = p_sc * v
    yield_dol = p_dol * v2

    lhs = np.inf if v == 0.0 else v1 * v2 / (v ** 2 + eps * v)

    return {
        "mu": mu, "mu1": mu1, "mu2": mu2,
        "v": v, "v1": v1, "v2": v2,
        "eps": eps, "theta_I": float(theta_I), "lhs": float(lhs),
        "p_sc": p_sc, "p_dol": p_dol,
        "yield_sc": yield_sc, "yield_dol": yield_dol,
        "dol_favored": bool(yield_dol > yield_sc),
    }
