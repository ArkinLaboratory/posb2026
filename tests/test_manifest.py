"""The staleness check, checked.

This is the one piece of tooling in the repository whose failure mode is
silence: if it wrongly says "up to date", nothing anywhere else notices, and the
consequence is a lecture given from the wrong file. So the tests here are mostly
about the negative cases -- that it does NOT say up to date when it should not.
"""
import json

import pytest

from tools import manifest


@pytest.fixture
def art(tmp_path, monkeypatch):
    """An artifact, a dependency, and a manifest tying them together."""
    monkeypatch.setattr(manifest, "ROOT", tmp_path)
    dep = tmp_path / "source.py"
    dep.write_text("x = 1\n")
    a = tmp_path / "deck.pptx"
    a.write_bytes(b"built from x = 1")
    manifest.write(a, [dep])
    return a, dep


def test_fresh_build_is_ok(art):
    a, _ = art
    assert manifest.verify(a) == ("ok", [])


def test_changed_dependency_is_stale(art):
    a, dep = art
    dep.write_text("x = 2\n")
    status, detail = manifest.verify(a)
    assert status == "stale"
    assert detail == [("source.py", "changed")]


def test_deleted_dependency_is_stale(art):
    a, dep = art
    dep.unlink()
    assert manifest.verify(a) == ("stale", [("source.py", "removed")])


def test_dependency_that_did_not_exist_at_build_time_is_stale(tmp_path,
                                                             monkeypatch):
    """A paper figure appearing later changes the deck, so it must count.

    The tempting implementation drops missing inputs from the manifest, which
    makes 'the figure arrived' indistinguishable from 'nothing happened' -- and
    the deck still shows the dashed placeholder.
    """
    monkeypatch.setattr(manifest, "ROOT", tmp_path)
    a = tmp_path / "deck.pptx"
    a.write_bytes(b"deck with a placeholder")
    absent = tmp_path / "paper-figure.png"
    manifest.write(a, [absent])
    assert manifest.verify(a) == ("ok", [])

    absent.write_bytes(b"the real figure, at last")
    assert manifest.verify(a) == ("stale", [("paper-figure.png", "added")])


def test_hand_edited_artifact_is_reported(art):
    """Someone opened the .pptx, fixed a typo, saved it. The next rebuild will
    throw that away, so it is worth saying out loud rather than at 8:05 am."""
    a, _ = art
    a.write_bytes(b"built from x = 1, then edited in PowerPoint")
    assert manifest.verify(a)[0] == "tampered"


def test_missing_artifact_is_not_a_failure(tmp_path, monkeypatch):
    """CI never builds decks. A machine that has not built one is not stale."""
    monkeypatch.setattr(manifest, "ROOT", tmp_path)
    assert manifest.verify(tmp_path / "never-built.pptx") == ("absent", [])
    assert "absent" not in manifest.FAIL


def test_artifact_without_a_manifest_fails(tmp_path, monkeypatch):
    """The exact shape of the bug: a built deck copied to the teaching machine
    on its own. It cannot be checked, so it must not pass."""
    monkeypatch.setattr(manifest, "ROOT", tmp_path)
    orphan = tmp_path / "copied-here-alone.pptx"
    orphan.write_bytes(b"?")
    assert manifest.verify(orphan) == ("unmanifest", [])
    assert "unmanifest" in manifest.FAIL


def test_manifest_paths_are_repository_relative(art):
    """Absolute paths would make a manifest useless the moment it is copied
    from the sandbox to the Mac, which is the only journey it ever makes."""
    a, _ = art
    body = json.loads((a.parent / (a.name + manifest.SUFFIX)).read_text())
    assert list(body["deps"]) == ["source.py"]
    assert not any(k.startswith("/") for k in body["deps"])


def test_mtime_alone_does_not_change_the_verdict(art):
    """Content hashes, not timestamps -- because the file bridge restamps
    everything it copies, so on the teaching machine every source looks newer
    than the artifact built from it."""
    a, dep = art
    import os
    os.utime(dep, (0, 0))
    assert manifest.verify(a) == ("ok", [])
    os.utime(dep, None)
    assert manifest.verify(a) == ("ok", [])


def test_every_status_has_a_label():
    for s in ("ok", "absent", "unmanifest", "stale", "tampered"):
        assert s in manifest.LABEL
