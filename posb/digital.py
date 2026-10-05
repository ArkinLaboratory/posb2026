"""
posb.digital — transfer curves, gain, thresholds and noise margins.

Introduced in Session 13. You find the unity-gain points of a transfer curve
by hand in class first; this is the same arithmetic made reusable.

Gain here is the LOG-LOG slope,

    G(x) = d ln y / d ln x ,

the fractional change in output per fractional change in input. Electronics can
use dV_out/dV_in because both sides are volts. In a cell the input and the
output are different molecules, so a linear slope changes with the units you
happen to pick; a log slope does not. It is also the quantity Daniel et al.
(Nature 2013, p. 623) call sensitivity. For a chain of identical gates measured
in the same units the two definitions pick out the same restoring region.

The leaky repressor used throughout:

    y(x) = y_min + (y_max - y_min) / (1 + (x/K)^n)

Its gain magnitude is g(x) * (y - y_min)/y with g = n u^n/(1 + u^n), u = x/K --
session 11's loop gain, discounted by the leak. Two consequences fall out:

  * |G| > 1 somewhere only if n > 1. A non-cooperative repressor cannot restore
    a degraded signal, which is the toggle's requirement again.
  * the leak pulls |G| back below 1 at high input, so there are two unity-gain
    points: the input thresholds x_IL and x_IH.

Scaling the output (an RBS change) multiplies y_min and y_max together and
leaves G -- and so both input thresholds -- unchanged. The RBS moves a gate's
output levels without moving its input thresholds. That is what makes signal
matching a tuning problem rather than a redesign.

Plain NumPy and SciPy. Read the source.
"""

import numpy as np
from scipy.optimize import brentq

__all__ = [
    "Repressor",
    "loglinear_range_hill",
]


class Repressor:
    """A leaky Hill repressor gate: input x, output y, both in absolute units."""

    def __init__(self, y_min, y_max, K, n, name=None):
        if not (0 < y_min < y_max):
            raise ValueError("need 0 < y_min < y_max")
        self.y_min, self.y_max, self.K, self.n = float(y_min), float(y_max), float(K), float(n)
        self.name = name or "gate"

    # -- the curve and its slope -------------------------------------------
    def __call__(self, x):
        u = np.asarray(x, dtype=float) / self.K
        return self.y_min + (self.y_max - self.y_min) / (1.0 + u ** self.n)

    def gain(self, x):
        """Log-log slope d ln y / d ln x (negative for a repressor)."""
        u = np.asarray(x, dtype=float) / self.K
        un = u ** self.n
        dy = -(self.y_max - self.y_min) * self.n * un / (1.0 + un) ** 2
        return dy / self(x)

    def scaled(self, factor, name=None):
        """The same promoter with the output multiplied by `factor` (an RBS change)."""
        return Repressor(self.y_min * factor, self.y_max * factor, self.K, self.n,
                         name or f"{self.name} x{factor:g}")

    # -- thresholds -----------------------------------------------------------
    def peak_gain(self):
        """(x, |G|) at the steepest point, located on a fine log grid then refined."""
        xs = self.K * np.logspace(-6, 6, 24001)
        g = np.abs(self.gain(xs))
        i = int(np.argmax(g))
        return xs[i], g[i]

    def thresholds(self):
        """Input thresholds (x_IL, x_IH): the two points where |G| = 1.

        Raises ValueError if |G| never exceeds 1 -- such a gate has no
        restoring region and no digital interpretation at all.
        """
        xp, gp = self.peak_gain()
        if gp <= 1.0:
            raise ValueError(f"{self.name}: peak |gain| = {gp:.3f} <= 1; "
                             "no restoring region (n too small or leak too large)")
        f = lambda x: abs(self.gain(x)) - 1.0
        x_il = brentq(f, self.K * 1e-8, xp)
        x_ih = brentq(f, xp, self.K * 1e8)
        return x_il, x_ih

    def output_levels(self):
        """(y_OL, y_OH): the output at the worst-case valid inputs.

        y_OH is the output when the input is as high as still counts as LOW
        (x_IL); y_OL the output when the input is as low as still counts as HIGH
        (x_IH). A repressor inverts, so a low input gives the high output.
        """
        x_il, x_ih = self.thresholds()
        return float(self(x_ih)), float(self(x_il))

    def __repr__(self):
        return (f"Repressor({self.name}: y_min={self.y_min:g}, y_max={self.y_max:g}, "
                f"K={self.K:g}, n={self.n:g})")


def noise_margins(sender, receiver):
    """Noise margins, in decades, when `sender`'s output drives `receiver`'s input.

        NM_low  = log10( x_IL(receiver) / y_OL(sender) )
        NM_high = log10( y_OH(sender)   / x_IH(receiver) )

    Both must be positive for the pair to be signal-matched: the sender's
    worst-case low output must read as LOW, and its worst-case high output as
    HIGH. A margin is how many decades of noise that reading survives.
    """
    x_il, x_ih = receiver.thresholds()
    y_ol, y_oh = sender.output_levels()
    return float(np.log10(x_il / y_ol)), float(np.log10(y_oh / x_ih))


def rbs_window(sender, receiver):
    """The range of output scale factors on `sender` that make the pair match.

    Returns (lo, hi): multiply the sender's output by any factor in [lo, hi]
    and both noise margins are >= 0. Empty (lo > hi) means no RBS can fix it.
    """
    x_il, x_ih = receiver.thresholds()
    y_ol, y_oh = sender.output_levels()
    return x_ih / y_oh, x_il / y_ol


def loglinear_range_hill(n, frac=0.75):
    """Fold-range of input over which a Hill function is logarithmic.

    For y = u^n/(1 + u^n) on a log axis the slope is n y (1 - y), largest at
    y = 1/2. It stays within `frac` of that maximum while y(1 - y) >= frac/4,
    i.e. between the two roots y_lo, y_hi, and the input range is

        (y_hi/(1 - y_hi) * (1 - y_lo)/y_lo) ** (1/n).

    At frac = 0.75: y in [1/4, 3/4], so the range is 9**(1/n) -- ninefold at
    n = 1, threefold at n = 2. Cooperativity buys gain and spends range.
    """
    d = np.sqrt(1.0 - frac)
    y_lo, y_hi = 0.5 * (1 - d), 0.5 * (1 + d)
    return float((y_hi / (1 - y_hi) * (1 - y_lo) / y_lo) ** (1.0 / n))


__all__ += ["noise_margins", "rbs_window"]
