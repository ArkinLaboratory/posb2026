"""Shared pieces for every notebook: the setup cell and cell constructors.

The setup cell is duplicated into every notebook rather than imported, because
a notebook must work when Colab opens it *alone*, with nothing else present.
That constraint is the reason for the git clone.
"""

import nbformat as nbf

REPO_URL = "https://github.com/ArkinLaboratory/posb2026"
REPO_DIR = "posb2026"

# ---------------------------------------------------------------------------
# The setup cell.
#
# It has to satisfy three environments:
#   DataHub  — the repo is already on disk; find its root by walking up
#   Colab    — only this one .ipynb exists; clone the repo, then add to path
#   local    — same as DataHub
#
# Walking up until we find a directory containing `posb/` makes it independent
# of how deeply the notebook is nested, so moving a notebook between folders
# does not silently break it.
# ---------------------------------------------------------------------------
SETUP = f'''\
# ---------------------------------------------------------------------------
# SETUP — run this cell first, every time.
#
# DataHub / local : finds the repository root and puts it on the import path.
# Google Colab    : clones the repository first, because Colab opens this
#                   notebook on its own, without the posb package beside it.
# ---------------------------------------------------------------------------
import os
import sys

if "google.colab" in sys.modules:
    if not os.path.exists("{REPO_DIR}"):
        !git clone -q {REPO_URL}.git
    sys.path.insert(0, os.path.abspath("{REPO_DIR}"))
else:
    _d = os.getcwd()
    while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "posb")):
        _d = os.path.dirname(_d)
    sys.path.insert(0, _d)

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import posb
from posb import Reaction, Model

posb.check_environment()
'''


def md(s):
    return nbf.v4.new_markdown_cell(s)


def code(s):
    return nbf.v4.new_code_cell(s)


def colab_badge(rel_path):
    """Markdown badge that opens `rel_path` in Colab."""
    url = f"https://colab.research.google.com/github/ArkinLaboratory/{REPO_DIR}/blob/main/{rel_path}"
    return (f"[![Open In Colab]"
            f"(https://colab.research.google.com/assets/colab-badge.svg)]({url})")


def datahub_link(rel_path):
    """nbgitpuller URL that pulls the repo and opens `rel_path` on DataHub."""
    return (
        "https://datahub.berkeley.edu/hub/user-redirect/git-pull"
        f"?repo={REPO_URL}"
        "&branch=main"
        f"&urlpath=lab/tree/{REPO_DIR}/{rel_path}"
    )


def header(title, subtitle, date_line, rel_path):
    """Standard first cell: title, launch links, then the prose."""
    return md(
        f"# {title}\n"
        f"## {subtitle}\n\n"
        f"**BioE 147/247 · Principles of Synthetic Biology · {date_line}**\n\n"
        f"[Open in DataHub]({datahub_link(rel_path)}) · "
        f"{colab_badge(rel_path)}\n\n"
        "---\n"
    )


# ---------------------------------------------------------------------------
# The 147/247 split, written once.
#
# Every problem set carries one extra question. It is REQUIRED for BioE 247 and
# EXTRA CREDIT for BioE 147. Those are two different denominators, which is why
# it is also two Gradescope assignments -- see docs/course-site-runbook.md.
#
# This lives here, and is injected into every master, because PS1 shipped with
# the opposite policy printed inside it -- "students in 147 may attempt this
# for no credit" -- and a student had pulled that notebook before anyone
# noticed. A policy stated in nine separate files is a policy that will be
# wrong in at least one of them.
# ---------------------------------------------------------------------------
class grad:
    """The standard 147/247 language for problem-set masters."""

    @staticmethod
    def points_line(core, extra, n):
        """The points fragment of a problem-set header."""
        return (f"**{core} points** · **Question {n}** is required for "
                f"**BioE 247** ({core + extra} total) and is extra credit "
                f"for **BioE 147** (up to +{extra})")

    @staticmethod
    def question_header(n, core, extra):
        """The heading block that opens the extra question."""
        return f"""---
## Question {n} — required for BioE 247, extra credit for BioE 147

**BioE 247** — part of the assignment, worth {extra} of your {core + extra}
points.

**BioE 147** — optional, worth up to {extra} points of extra credit on top of
{core}. You do not need it for full marks. It is not a harder version of the
same thing; it removes an assumption the earlier questions made, which is
where most of the interest is."""
