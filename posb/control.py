"""Antithetic integral feedback -- session 22's object, and PS8's Q4 and Q5.

THE RESULT, in the authors' words (Aoki et al., Nature 570:533, 2019):

    "the steady-state value of the output is determined solely by the ratio
    mu/theta. Notably, it does not depend on the topology and parameters of
    the controlled network."

So the functions here are written to let you CHECK that, not to assume it:
`closed_loop_steady_state` takes the plant's parameters and you are meant to
vary them and watch the answer not move.

THE MODEL. A plant whose output X is driven by controller species Z1, with a
constant disturbance d:

    dX/dt  = k*Z1 - gamma*X + d
    dZ1/dt = mu    - eta*Z1*Z2 - delta*Z1
    dZ2/dt = theta*X - eta*Z1*Z2 - delta*Z2

Z1 carries the set point (made at a constant rate mu), Z2 senses the output
(made in proportion to X at rate theta), and the two annihilate at rate eta.
`delta` is the DILUTION rate of the controller species and is the whole of
section 3 move 4: set it to zero and the controller is an exact integrator;
make it positive and the integrator leaks.

WHY SUBTRACTING THE TWO CONTROLLER EQUATIONS IS THE WHOLE TRICK. At delta = 0,

    d(Z1 - Z2)/dt = mu - theta*X

-- the annihilation term cancels because it removes Z1 and Z2 at the same
rate. So Z1 - Z2 is the integral of the error (mu - theta*X), and a steady
state requires that error to be zero. Hence X = mu/theta, with k, gamma and
eta nowhere in it.

TWO LIMITS, AND BOTH ARE TAUGHT RATHER THAN HIDDEN.

1.  ACTUATOR SATURATION. The controller acts only through Z1 >= 0, so it can
    only push the output UP. A steady state needs k*Z1 = gamma*X - d >= 0, so
    exact adaptation holds only for

        d <= gamma * mu / theta        (`max_rejectable_disturbance`)

    Past that the loop does not saturate gracefully -- it has NO steady state
    at all: Z1 falls to zero, the annihilation that was removing Z2 stops, and
    Z2 grows without bound while X drifts toward d/gamma. `settles` reports
    this honestly rather than returning whatever the integrator happened to
    reach.

2.  DILUTION. At delta > 0, subtracting gives mu - theta*X = delta*(Z1 - Z2),
    so the error is (delta/theta)*(Z1 - Z2) and is FIRST ORDER in delta.

NOTHING HERE IS FITTED. Every number in sessions/s22-control/NUMBERS.md comes
out of these functions.

Run:  python -m pytest tests/test_control.py
"""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

__all__ = [
    "ControlParams", "simulate", "closed_loop_steady_state",
    "open_loop_steady_state", "setpoint_error", "settles",
    "max_rejectable_disturbance", "disturbance_rejection",
    "error_scaling_exponent",
]


@dataclass(frozen=True)
class ControlParams:
    """The circuit. Defaults are session 22's and PS8 Q4's reference values."""
    mu: float = 10.0        # set point encoding: Z1 production rate
    theta: float = 2.0      # output sensing: Z2 production per unit X
    k: float = 1.0          # plant gain: how hard Z1 drives X
    gamma: float = 0.5      # plant removal rate
    eta: float = 50.0       # annihilation rate constant
    delta: float = 0.0      # DILUTION of the controller species

    @property
    def set_point(self):
        """mu/theta -- what the output goes to, when the controller works."""
        return self.mu / self.theta


def _rhs(t, y, p, d):
    X, Z1, Z2 = y
    ann = p.eta * Z1 * Z2
    return [p.k * Z1 - p.gamma * X + d,
            p.mu - ann - p.delta * Z1,
            p.theta * X - ann - p.delta * Z2]


def simulate(p=ControlParams(), d=0.0, t_end=8000.0, y0=(0.0, 0.0, 0.0)):
    """Integrate from rest. Returns the solve_ivp solution.

    LSODA and tight tolerances are not optional: the annihilation term makes
    this stiff, and a loose solve reports a set point that is slightly wrong,
    which is the one thing this session cannot afford to get slightly wrong.
    """
    return solve_ivp(_rhs, [0.0, t_end], list(y0), args=(p, d),
                     rtol=1e-10, atol=1e-12, method="LSODA", dense_output=True)


def closed_loop_steady_state(p=ControlParams(), d=0.0, t_end=8000.0):
    """Output the loop settles to. Vary p.k, p.gamma, p.eta and watch it not move."""
    return float(simulate(p, d, t_end).y[0, -1])


def open_loop_steady_state(p=ControlParams(), d=0.0, z1=None):
    """The same plant with the feedback deleted -- Z1 held at a constant.

    This is Aoki's own control: their open-loop strain is the closed-loop one
    with the anti-sigma module removed, so Z1 is no longer being annihilated
    and the loop is broken. Here that is a fixed Z1, and the default is the
    value the closed loop happens to rest at with no disturbance -- so the two
    circuits agree at d = 0 and disagree everywhere else, which is the
    comparison the figure draws.
    """
    if z1 is None:
        z1 = (p.gamma * p.set_point) / p.k
    return float((p.k * z1 + d) / p.gamma)


def max_rejectable_disturbance(p=ControlParams()):
    """Largest d with a steady state: gamma*mu/theta. Past this, Z1 hits zero."""
    return p.gamma * p.set_point


def settles(p=ControlParams(), d=0.0, t_a=8000.0, t_b=16000.0, tol=1.5):
    """Does the system reach a steady state, or is Z2 still growing?

    Doubling the horizon should not roughly double anything. If Z2 does, the
    annihilation has stopped and there is no fixed point -- which is what
    happens past `max_rejectable_disturbance`, and is a different failure from
    the leak that dilution causes.
    """
    z2a = float(simulate(p, d, t_a).y[2, -1])
    z2b = float(simulate(p, d, t_b).y[2, -1])
    return bool(z2b / z2a < tol)


def setpoint_error(p=ControlParams(), d=0.0, t_end=8000.0):
    """Steady-state output minus the set point. Zero is perfect adaptation.

    NOT `adaptation_error`, and the name matters. Session 10 already defines
    "adaptation error" for the incoherent feedforward loop as final / peak --
    a dimensionless RATIO read numerically off the trajectory -- and that
    definition is autograded on PS5 (T26) and is Alon's standard one.

    This quantity is a DIFFERENCE, in units of X. Both conventions make zero
    mean "good", so a student carrying session 10's formula into session 22
    gets no warning that it is the wrong one. Hence the separate name here,
    and the explicit contrast on the slide and in PS8 Q5.
    """
    return closed_loop_steady_state(p, d, t_end) - p.set_point


def disturbance_rejection(p=ControlParams(), d=1.0):
    """Open-loop output deviation divided by closed-loop deviation.

    The factor by which closing the loop shrinks the effect of d. Infinite in
    the ideal case, which is why the figure plots it against the dilution rate
    rather than quoting one number.
    """
    base = p.set_point
    closed = abs(closed_loop_steady_state(p, d) - base)
    opened = abs(open_loop_steady_state(p, d) - open_loop_steady_state(p, 0.0))
    return float("inf") if closed < 1e-12 else opened / closed


def error_scaling_exponent(p=ControlParams(), d=2.0,
                           deltas=(0.0025, 0.005, 0.01, 0.02)):
    """Slope of log|error| against log(delta). The answer is 1."""
    errs = []
    for dl in deltas:
        q = ControlParams(p.mu, p.theta, p.k, p.gamma, p.eta, dl)
        errs.append(abs(setpoint_error(q, d)))
    return float(np.polyfit(np.log(deltas), np.log(errs), 1)[0])
