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
data       Session 5.  Synthetic decay and induction timecourses, generated
                       from the model with Andersen's half-lives. Seeded.
analysis   Session 8.  Nullclines, fixed points, Jacobian, linear stability,
                       and the toggle bifurcation condition.
           Session 11. The repressilator, the loop gain, parameter sweeps and
                       the Hopf boundary.
stochastic Session 12. Gillespie SSA, time-weighted averages, Fano and CV,
                       and the birth-death, bursting and autoregulation
                       models. You write your own SSA first.
digital    Session 13. Transfer curves, log gain, unity-gain thresholds,
                       noise margins and the RBS window for signal matching.
logic      Session 16. Truth tables, NOR networks, synchronous timing
                       tables, hazards, and cascade delay in lifetimes.
assembly   Session 17. Golden Gate junctions: the 120 usable overhang
                       identities, distinguishability measured against the
                       reverse complement, a clash proxy, and the published
                       standard sets with their MEASURED fidelity.
protein    Session 18. Covalent modification cycles: the steady state as a
                       quadratic, the two exact results, and zero-order
                       ultrasensitivity -- an apparent Hill coefficient with no
                       cooperative binding anywhere in the model.
resources  Session 19. Competition for a shared translational pool: the
                       partition function again, the apparent repression it
                       manufactures between unconnected genes, and the isocost
                       line.
retroactivity
           Session 21. What a downstream load costs the module driving it:
                       the retroactivity term, the exact steady states of the
                       conservative and diluted models, and the result that
                       both costs are set by sites-per-molecule and NOT by the
                       affinity -- so weakening the operator buys nothing.

fba        Session 20. Flux balance analysis as a linear program: session 3's
                       stoichiometric matrix with the rate column thrown away.
                       S @ v = 0 plus bounds plus an imported objective -- and
                       the two limitations that come with the shape of the
                       problem, vertex solutions and alternate optima, both
                       checkable rather than asserted.

control    Session 22. Antithetic integral feedback: the set point as a ratio
                       of two controller parameters, the plant's parameters
                       absent from it, and the two limits where that stops
                       being true -- actuator saturation and a leaking
                       integrator.

evolution  Session 23. The first module whose state variable is a fraction of
                       a POPULATION and whose clock is GENERATIONS. Session
                       19's burden read a second way, as a selection
                       coefficient; the exact failure time; and why an onset
                       in a stability curve counts the lesions escape needs.

communities
           Session 24. The wire outside the cell. Diffusion time and
                       penetration depth, Basu's band detector read as a
                       feed-forward loop in SPACE, and the two-strain
                       predator-prey chemostat -- including the result that
                       the signal-free 2-state reduction has tr J < 0 for
                       EVERY parameter value and so cannot oscillate. The
                       Hopf is a property of the signals, not of the cells.

populations
           Session 25. What happens when the construct has to spread on its
                       own. Diploid packaging as two draws from an urn,
                       heterozygote waste, the vector's own reproductive
                       ratio, and the result that making the payload more
                       potent lowers the ratio that carries it.

classifiers
           Session 26. The population as the thing being CLASSIFIED. A
                       classifier as a threshold on a product of continuous
                       sensor responses rather than a Boolean circuit -- so
                       the error rates move with the threshold and a budget
                       for them is possible at all. The marker senses carried
                       explicitly, because a reversed NOT term is silent; and
                       a per-cell error rate times a treated population
                       against a budget of one wrong cell, which is session
                       23's escapers-per-dose arithmetic with the sign of the
                       intent reversed.

Everything here is plain NumPy and SciPy. There is no hidden solver, no
symbolic engine, and no simulation framework. Read the source.
"""

from . import (data, stochastic, digital, logic, protein, resources,
               retroactivity, fba, control, evolution, communities,
               populations, classifiers)
from .core import Reaction, Model, Trajectory
from .analysis import (
    nullcline, fixed_points, jacobian, classify, stability_report,
    toggle_model, toggle_alpha_critical,
    repressilator_model, repressilator_alpha_critical, loop_gain,
    sweep, leading_real_part, hopf_boundary,
)

__version__ = "0.3.0"
__all__ = [
    "Reaction", "Model", "Trajectory",
    "nullcline", "fixed_points", "jacobian", "classify", "stability_report",
    "toggle_model", "toggle_alpha_critical",
]


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
