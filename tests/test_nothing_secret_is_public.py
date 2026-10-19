"""The public repo must not track anything with an answer in it.

On 18 October every handout answer key from s04 to s17 was found published
on github.com/ArkinLaboratory/posb2026, which is world-readable. The cause
was Phase 3 of the release checklist: `git add handouts/ board-notes/`, and
`handouts/` matched `*-answers.md` and `*-answers.pdf`. A note in the
checklist is not a control. This is.

Answers and board notes now live in private/, a separate repository that
this one gitignores. If a future change moves them back, or adds a new
answer file beside the student handouts, this fails.
"""
import subprocess

import pytest

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


def _tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True)
    if out.returncode != 0:
        pytest.skip("not a git work tree")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def test_no_answer_sheet_is_tracked_publicly():
    leaked = [f for f in _tracked()
              if "answers." in f.rsplit("/", 1)[-1].lower()]
    assert leaked == [], (
        "these carry answers and are tracked in the PUBLIC repo; they belong "
        "under private/:\n  " + "\n  ".join(leaked))


def test_no_board_notes_are_tracked_publicly():
    leaked = [f for f in _tracked() if f.startswith("board-notes/")]
    assert leaked == [], (
        "board notes carry expected answers and marking guidance and are "
        "tracked in the PUBLIC repo:\n  " + "\n  ".join(leaked))


def test_the_private_tree_is_ignored_by_the_public_repo():
    leaked = [f for f in _tracked() if f.startswith("private/")]
    assert leaked == [], (
        "private/ is a separate repository and must never be tracked "
        "here:\n  " + "\n  ".join(leaked))


def test_the_answers_and_board_notes_still_exist_where_the_build_expects():
    """Moving them must not quietly lose them."""
    answers = sorted((ROOT / "private" / "handouts").glob("*-answers.md"))
    boards = sorted((ROOT / "private" / "board-notes").glob("s*-board-notes.md"))
    assert len(answers) >= 13, f"only {len(answers)} answer sheets found"
    assert len(boards) >= 12, f"only {len(boards)} board notes found"
