"""
posb — a small toolkit for BioE 147/247, Principles of Synthetic Biology.

Design rule for this package: **nothing is abstracted away before it has been
built by hand in class.** Every module below names the session that introduces
it. If you are using something from here, you have already written the
un-abstracted version yourself.

Currently available
-------------------
core       Session 3.  Reaction, Model, Trajectory. Builds S and integrates
                       dx/dt = S @ v.

Coming later in the term
------------------------
analysis   Session 8.  Nullclines, fixed points, Jacobian, linear stability.
stochastic Session 12. Gillespie SSA — you write your own first.
fba        Session 20. Flux balance analysis as a linear program.

Everything here is plain NumPy and SciPy. There is no hidden solver, no
symbolic engine, and no simulation framework. Read the source.
"""

from .core import Reaction, Model, Trajectory

__version__ = "0.1.0"
__all__ = ["Reaction", "Model", "Trajectory"]


def check_environment(verbose=True):
    """Report the running environment. Used by PS0 and by every notebook.

    Returns a dict so it can be tested; prints a table when verbose.
    """
    import sys
    import numpy
    import scipy
    import matplotlib

    info = {
        "python": ".".join(str(v) for v in sys.version_info[:3]),
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
        "posb": __version__,
    }
    try:
        import sympy
        info["sympy"] = sympy.__version__
    except ImportError:
        info["sympy"] = "not installed"

    # Where are we running?
    if "google.colab" in sys.modules:
        info["platform"] = "Google Colab"
    elif "JUPYTERHUB_USER" in __import__("os").environ:
        info["platform"] = "Berkeley DataHub"
    else:
        info["platform"] = "local or other"

    if verbose:
        width = max(len(k) for k in info)
        for k, v in info.items():
            print(f"{k:<{width}}  {v}")

    return info
