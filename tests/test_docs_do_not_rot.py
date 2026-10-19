"""Checklist lines that assert a path are the lines nobody re-derives.

Week 9 found three of them wrong at once, and one had been publishing every
handout answer key to a public GitHub repo:

  * Phase 3 said `git add handouts/ board-notes/`, and `handouts/` matched
    `*-answers.md`.
  * Section 5.1 said to upload the deck from `private/build/decks/`, which is
    overwritten without asking, instead of `private/taught/`, which is the
    copy that was approved and hand-edited.
  * Section 5.2 said readings must be proxy links, while six weeks of actual
    practice uploaded the PDFs.

Prose corrections were written for all three. Prose is what rotted in the
first place, so the two that a machine can check are checked here instead.
The third -- whether readings may be uploaded -- is a judgement Adam made on
18 October and is recorded in the checklist; there is nothing to assert.
"""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKLIST = ROOT / "docs" / "session-release-checklist.md"


def _doc_paths():
    docs = sorted((ROOT / "docs").glob("*.md"))
    extra = [ROOT / "AGENTS.md"]
    return [p for p in docs + extra if p.is_file()]


def test_no_doc_tells_you_to_git_add_a_private_path():
    """`private/` is a separate repository and this one gitignores it.

    A `git add` naming a private path either fails or, worse, succeeds for a
    path that only looks private. The one exception is the block that runs
    after `cd private`, where the paths are relative to that repo.
    """
    offenders = []
    for p in _doc_paths():
        lines = p.read_text(encoding="utf-8").split("\n")
        in_private = False
        for i, ln in enumerate(lines, 1):
            if re.search(r"\bcd\s+private\b", ln):
                in_private = True
            elif ln.startswith("```") and in_private:
                in_private = False
            if in_private:
                continue
            if "git add" in ln and re.search(r"(^|[\s`'\"])private/", ln):
                offenders.append(f"{p.relative_to(ROOT)}:{i}: {ln.strip()}")
    assert offenders == [], (
        "these tell you to add a private path to the PUBLIC repo:\n  "
        + "\n  ".join(offenders))


def test_the_public_add_list_cannot_reach_an_answer_sheet():
    """Whatever Phase 3 adds, none of it may glob up an answer sheet.

    This is the check that would have caught the 18 October exposure. It reads
    the actual `git add` lines out of the checklist and resolves them.
    """
    text = CHECKLIST.read_text(encoding="utf-8")
    block = text.split("Then the **private** repo", 1)[0]
    targets = []
    for ln in block.split("\n"):
        if "git add" in ln:
            targets += [t for t in ln.replace("git add", "").replace("\\", "").split()
                        if not t.startswith("-")]
    assert targets, "no git add line found in Phase 3 -- has it been rewritten?"
    leaked = []
    for t in targets:
        for f in ROOT.glob(t.rstrip("/") + "/**/*" if t.endswith("/") else t):
            name = f.name.lower()
            if "answers." in name or "board-notes" in str(f.relative_to(ROOT)):
                leaked.append(str(f.relative_to(ROOT)))
    assert leaked == [], (
        "Phase 3's add list reaches material with answers in it:\n  "
        + "\n  ".join(sorted(set(leaked))[:12]))


def test_the_checklist_uploads_the_approved_deck_not_the_build():
    """`private/taught/` is the approval record; `private/build/decks/` is
    regenerated without asking and is wrong the moment a typo is fixed at the
    lectern."""
    text = CHECKLIST.read_text(encoding="utf-8")
    assert "from\n`private/taught/`" in text or "`private/taught/`" in text, \
        "5.1 no longer names private/taught/ as the upload source"
    instruction = text.split("### 5.1", 1)[1].split("### 5.2", 1)[0]
    body = "\n".join(ln for ln in instruction.split("\n")
                     if not ln.lstrip().startswith(">"))
    # Naming the build directory is fine where it is being ruled out; the
    # instruction reads "from `private/taught/`, never from
    # `private/build/decks/`". It is only a defect when it is the source.
    for m in re.finditer(r"private/build/decks", body):
        before = body[max(0, m.start() - 60):m.start()].lower()
        assert "never" in before or "not" in before, (
            "5.1 names the build directory as an upload source again; it is "
            "regenerated without asking, so the module would go stale the "
            "moment a typo is fixed at the lectern")


@pytest.mark.parametrize("folder", ["handouts", "board-notes"])
def test_the_build_reads_private_material_from_private(folder):
    """build_handouts must point at private/, or the move silently undoes."""
    src = (ROOT / "tools" / "build_handouts.py").read_text(encoding="utf-8")
    assert f'"private" / "{folder}"' in src, (
        f"build_handouts no longer reads {folder} from private/")
