#!/usr/bin/env python3
"""Does the artifact on this machine match the sources on this machine?

THE BUG THIS EXISTS TO CATCH. A deck source is edited, the figure it embeds is
regenerated, both are copied to the teaching machine -- and the built `.pptx`
sitting in `private/build/decks/` is not rebuilt. The instructor opens the deck,
sees the old slide, and there is nothing anywhere that says so. It has happened
twice. Both times the source was right, the build was right, and the file being
looked at was two hours old.

Nothing in the repository could detect that, because the repository does not
know what the artifact was made from.

    build_decks.py --check    "is every paper figure present?"
    build_readings.py --check "is every paper handed out first?"
    (nothing)                 "is the deck you are about to teach from
                               the one your sources would produce?"

So the build now writes a sidecar next to every artifact it produces:

    PoSB_Session02_Substrate.pptx
    PoSB_Session02_Substrate.pptx.deps.json

listing every input the build actually read -- deck module, theme, course.yaml,
readings.yaml, every figure, every movie, every poster frame -- each with a
content hash. `--verify` recomputes those hashes and says what changed.

WHY HASHES AND NOT MTIMES. Mtimes do not survive the trip. Files reach the
teaching machine through a copy, which stamps them with the time of the copy,
so on that machine the sources are *newer* than an artifact built from them
even when they are identical -- and an artifact copied after its sources looks
fresh even when it is stale. Mtime comparison gives a false alarm and a false
all-clear on the one machine where the answer matters. Content hashes travel.

WHAT IT DELIBERATELY DOES NOT DO. It does not rebuild. A checker that fixes the
thing it is checking cannot report on it, and the interesting question here is
"what is on disk right now", asked before class rather than after.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUFFIX = ".deps.json"


def digest(path):
    """sha256 of a file, or None if it is not there."""
    p = Path(path)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    """Repository-relative POSIX path, so a manifest is machine-independent."""
    p = Path(path).resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def write(artifact, deps, extra=None):
    """Record what `artifact` was built from. Returns the manifest path.

    `deps` is any iterable of paths. Missing ones are recorded with a null
    hash rather than dropped -- "this input did not exist at build time" is
    itself a fact worth keeping, because a paper figure appearing later
    changes the deck and should count as a reason to rebuild.
    """
    artifact = Path(artifact)
    entries = {}
    for d in deps:
        entries[rel(d)] = digest(d)
    body = {
        "artifact": artifact.name,
        "artifact_sha256": digest(artifact),
        "artifact_bytes": artifact.stat().st_size if artifact.is_file() else None,
        "deps": dict(sorted(entries.items())),
    }
    if extra:
        body.update(extra)
    path = artifact.with_name(artifact.name + SUFFIX)
    path.write_text(json.dumps(body, indent=2) + "\n")
    return path


def verify(artifact):
    """Compare an artifact and its recorded inputs against what is on disk.

    Returns (status, detail):

        "ok"          the artifact is present and every input still hashes to
                      what it hashed to when the artifact was built
        "absent"      no artifact here. Not an error -- CI never builds decks,
                      and a machine that has not built one is not stale.
        "unmanifest"  an artifact with no sidecar. Cannot be checked, and the
                      likely cause is that it was copied here without one.
        "stale"       inputs have changed since this was built. detail lists
                      them: (path, "changed" | "added" | "removed")
        "tampered"    the artifact itself no longer hashes to what the build
                      wrote, i.e. something edited it by hand afterwards.
                      These decks are generated; a hand edit is a change that
                      the next rebuild will silently destroy.
    """
    artifact = Path(artifact)
    man = artifact.with_name(artifact.name + SUFFIX)
    if not artifact.is_file():
        return "absent", []
    if not man.is_file():
        return "unmanifest", []
    body = json.loads(man.read_text())

    changed = []
    for path, was in body.get("deps", {}).items():
        now = digest(ROOT / path)
        if was == now:
            continue
        changed.append((path, "added" if was is None else
                        "removed" if now is None else "changed"))
    if changed:
        return "stale", sorted(changed)

    recorded = body.get("artifact_sha256")
    if recorded and digest(artifact) != recorded:
        return "tampered", []
    return "ok", []


# The two words the whole thing exists to print.
LABEL = {
    "ok": "up to date",
    "absent": "not built on this machine",
    "unmanifest": "NO MANIFEST -- cannot tell; rebuild it",
    "stale": "STALE -- built before these inputs changed",
    "tampered": "EDITED BY HAND after the build -- a rebuild will discard that",
}
FAIL = ("stale", "unmanifest", "tampered")


def report(name, artifact, indent="  "):
    """Print one line, plus the reasons if there are any. Returns True if bad."""
    status, detail = verify(artifact)
    print(f"{indent}{name:<34} {LABEL[status]}")
    for path, how in detail:
        print(f"{indent}   {how:<8} {path}")
    return status in FAIL
