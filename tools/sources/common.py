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
