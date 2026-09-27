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



IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif",
                  ".tiff"}


def image_digest(path):
    """A hash of what an image SHOWS, not of the file that carries it.

    Same reason `content_digest` exists for zips, different mechanism. A PNG
    re-encoded anywhere along the way -- a different zlib level, a stripped
    text chunk, a transfer that decodes and re-saves -- is a different file
    carrying an identical picture. This repository's figures reach the
    teaching machine over a bridge that does exactly that: verified on
    s11_sweep.png, 104847 bytes here and 110617 bytes there, byte hashes
    unrelated, decoded pixels identical to the bit. A byte comparison fires on
    every figure after every transfer, which is the cry-wolf failure this
    module was written to avoid.

    So: hash the decoded pixels, plus the size and mode so a resize or a
    colour-space change still counts. Falls back to the byte hash if Pillow is
    unavailable or the file will not decode.
    """
    p = Path(path)
    if not p.is_file():
        return None
    try:
        from PIL import Image
        with Image.open(p) as im:
            im.load()
            mode, size = im.mode, im.size
            raw = im.convert("RGBA").tobytes()
    except Exception:
        return digest(p)
    h = hashlib.sha256()
    h.update(f"{mode}:{size[0]}x{size[1]}:".encode())
    h.update(raw)
    return h.hexdigest()


def artifact_digest(path):
    """The right digest for whatever kind of artifact this is."""
    p = Path(path)
    if p.suffix.lower() in IMAGE_SUFFIXES:
        return image_digest(p)
    return digest(p)


def content_digest(path):
    """A hash of what a file MEANS, not of its bytes.

    A .pptx is a zip, and a zip records the time each member was written. So
    two builds from identical sources produce different bytes -- always. A
    byte comparison between the copy in private/taught/ and the current build
    therefore fires on every rebuild, whether or not anything changed, and a
    check that cries wolf is worse than no check: it trains you to ignore it.

    Verified rather than assumed: building s04 twice in a row gives different
    bytes and an identical content digest, with zero differing zip members.

    For a zip, this is a hash over (member name, member content) for every
    member in sorted order. For anything else it is the file's own hash.
    """
    import zipfile
    p = Path(path)
    if not p.is_file():
        return None
    try:
        z = zipfile.ZipFile(p)
        names = sorted(z.namelist())
    except (zipfile.BadZipFile, OSError):
        return digest(p)
    h = hashlib.sha256()
    for n in names:
        h.update(n.encode())
        h.update(hashlib.sha256(z.read(n)).digest())
    return h.hexdigest()



def deck_content(path):
    """What survives a PowerPoint round-trip: the words and the pictures.

    Every deck in private/taught/ has been opened and saved by PowerPoint --
    docProps says Application="Microsoft Macintosh PowerPoint", AppVersion 16,
    against the build's pristine python-pptx (AppVersion 14, "Steve Canny").
    So a taught copy never matches the build byte-for-byte, never matches it
    zip-member-for-member, and its mtime moves for reasons that have nothing to
    do with the source. All three of the obvious comparisons give a false alarm.

    What does compare cleanly is the content a round-trip preserves exactly:
    the text of every slide, in order, and the bytes of every embedded image.
    Returns (text_digest, media_digest, n_slides), or None if unreadable.

    Deliberately blind to styling. A theme change that moves a rule or adds an
    icon is not a different deck, and treating it as one is how a checker
    becomes noise.
    """
    import re
    import zipfile
    p = Path(path)
    if not p.is_file():
        return None
    try:
        z = zipfile.ZipFile(p)
    except (zipfile.BadZipFile, OSError):
        return None
    slides = sorted((n for n in z.namelist()
                     if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                    key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))
    th = hashlib.sha256()
    for n in slides:
        text = " ".join(re.findall(r"<a:t>(.*?)</a:t>", z.read(n).decode("utf-8"), re.S))
        th.update(re.sub(r"\s+", " ", text).strip().encode())
        th.update(b"\x00")
    mh = hashlib.sha256()
    for n in sorted(x for x in z.namelist() if x.startswith("ppt/media/")):
        mh.update(n.split("/")[-1].encode())
        mh.update(hashlib.sha256(z.read(n)).digest())
    return th.hexdigest(), mh.hexdigest(), len(slides)


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
        "artifact_content": artifact_digest(artifact),
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

    # Compare on CONTENT where we recorded it. For an image that means the
    # decoded pixels, which survive the transfer that re-encodes the file;
    # falling back to the byte hash only for manifests written before this
    # field existed, and only when the bytes happen to still match, so an
    # old manifest can neither raise nor silence a real alarm on its own.
    recorded_content = body.get("artifact_content")
    if recorded_content is not None:
        if artifact_digest(artifact) != recorded_content:
            return "tampered", []
        return "ok", []
    recorded = body.get("artifact_sha256")
    if recorded and digest(artifact) != recorded:
        return "legacy-bytes", []
    return "ok", []


# The two words the whole thing exists to print.
LABEL = {
    "ok": "up to date",
    "absent": "not built on this machine",
    "unmanifest": "NO MANIFEST -- cannot tell; rebuild it",
    "stale": "STALE -- built before these inputs changed",
    "tampered": "EDITED BY HAND after the build -- a rebuild will discard that",
    "legacy-bytes": "manifest predates the content hash -- rebuild to re-stamp",
}
FAIL = ("stale", "unmanifest", "tampered", "legacy-bytes")


def report(name, artifact, indent="  "):
    """Print one line, plus the reasons if there are any. Returns True if bad."""
    status, detail = verify(artifact)
    print(f"{indent}{name:<34} {LABEL[status]}")
    for path, how in detail:
        print(f"{indent}   {how:<8} {path}")
    return status in FAIL
