#!/usr/bin/env python3
"""Did everything actually arrive on this machine?

THE PROBLEM. Files reach the teaching Mac one at a time, through a copy step,
from a sandbox that cannot see the Mac's filesystem. Nothing in that path is
transactional. A delivery of twenty files can land nineteen, and the twentieth
is missing in a way that looks exactly like "not written yet" -- no error, no
warning, and the next thing you notice is a build that fails or, worse, one
that succeeds against a stale file.

`tools/manifest.py` answers "is this ARTIFACT older than its sources?". This
file answers the question one level up: "is this WORKING COPY the one that was
just handed to me?"

HOW IT WORKS. Two commands, one small JSON file between them.

    (sandbox)   python tools/handoff.py --emit
                    -> writes docs/handoff.json: a sha256 for every tracked
                       file, plus any built decks present

    (your Mac)  python tools/handoff.py --check
                    -> compares this disk against that list and tells you
                       exactly what is missing, what differs, and what is
                       newer here than there

The check is deliberately dumb and content-based. It does not talk to GitHub,
does not need credentials, does not care about mtimes -- which is the point,
because the copy restamps every mtime and the repos have three different commit
histories.

READING THE OUTPUT.

    MISSING     the file never arrived. This is the failure this tool exists
                to catch. Ask for it again.
    EDITED      an AUTHORED file whose contents are not what was sent. Either
                you changed it (fine -- you will know) or an older copy is
                sitting on top of a newer one (not fine).
    REBUILT     a GENERATED file that differs. Expected as soon as you run a
                build: matplotlib and LibreOffice do not produce byte-identical
                output on two machines. Not a problem, and not something this
                tool can adjudicate -- `--verify` is the authority there.
    EXTRA       here and not in the handoff. Usually your own work.
    OK          byte-identical.

Exit status is 1 if anything is MISSING or EDITED. REBUILT does not fail.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "docs" / "handoff.json"

# Built decks are gitignored (they may embed copyrighted figures) but they are
# the thing you teach from, so a handoff that ignores them checks the wrong
# half of the problem.
ALSO = ["private/build/decks"]

# Paths whose contents are PRODUCED by a command rather than written by a
# person. A difference here after you have run a build locally is expected and
# uninteresting -- matplotlib and LibreOffice do not produce byte-identical
# output on two machines, so a rebuilt PNG or .pptx will always differ from the
# one that was sent even when nothing about the course changed.
#
# The authority for those files is `build_decks.py --verify` / `build_figures.py
# --verify`, which compare an artifact against ITS OWN sources on THIS disk.
# What --check is uniquely good for is the other column: an AUTHORED file that
# differs means somebody edited it, and that is always worth knowing.
GENERATED = ("figures/build/", "private/build/", "handouts/")

GREEN, RED, YELLOW, DIM, RESET = ("\033[32m", "\033[31m", "\033[33m",
                                  "\033[2m", "\033[0m")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked():
    """Every file git knows about, plus the built decks. Sorted, relative."""
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True)
    files = [l for l in out.stdout.splitlines() if l.strip()] if out.returncode == 0 else []
    for extra in ALSO:
        d = ROOT / extra
        if d.is_dir():
            files += [str(f.relative_to(ROOT)) for f in sorted(d.rglob("*"))
                      if f.is_file()]
    # The handoff file cannot contain its own hash -- it is written after the
    # list is computed, so its entry would be one version stale for ever.
    return sorted(set(files) - {"docs/handoff.json"})


def emit():
    files = {}
    for rel in tracked():
        p = ROOT / rel
        if p.is_file():
            files[rel] = digest(p)
    HANDOFF.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF.write_text(json.dumps(
        {"note": "sha256 of every file in this handoff; "
                 "run `python tools/handoff.py --check` to compare",
         "count": len(files), "files": files}, indent=1) + "\n")
    print(f"wrote {HANDOFF.relative_to(ROOT)}  ({len(files)} files)")
    return 0


def check(verbose=False):
    if not HANDOFF.is_file():
        sys.exit(f"no {HANDOFF.relative_to(ROOT)} on this machine. That file is "
                 f"part of the handoff too -- ask for it.")
    body = json.loads(HANDOFF.read_text())
    expected = body["files"]

    missing, differs, rebuilt, ok = [], [], [], 0
    for rel, want in sorted(expected.items()):
        p = ROOT / rel
        if not p.is_file():
            missing.append(rel)
        elif digest(p) != want:
            (rebuilt if rel.startswith(GENERATED) else differs).append(rel)
        else:
            ok += 1

    here = set(tracked())
    extra = sorted(here - set(expected))

    print(f"\nChecked {len(expected)} files against "
          f"{HANDOFF.relative_to(ROOT)}\n")
    print(f"  {GREEN}{ok:>4} OK{RESET}       byte-identical")
    if missing:
        print(f"  {RED}{len(missing):>4} MISSING{RESET}  never arrived here")
        for rel in missing[:40]:
            print(f"        {rel}")
        if len(missing) > 40:
            print(f"        ... and {len(missing) - 40} more")
    if differs:
        print(f"  {YELLOW}{len(differs):>4} EDITED{RESET}   authored file, and "
              f"not the version that was sent")
        for rel in differs[:40]:
            print(f"        {rel}")
        if len(differs) > 40:
            print(f"        ... and {len(differs) - 40} more")
    if rebuilt:
        print(f"  {DIM}{len(rebuilt):>4} REBUILT{RESET}  generated file that "
              f"differs — normal if you have run a build since{RESET}")
        if verbose:
            for rel in rebuilt[:40]:
                print(f"        {rel}")
        print(f"        {DIM}check these with `build_decks.py --verify` and "
              f"`build_figures.py --verify`{RESET}")
    if extra:
        print(f"  {DIM}{len(extra):>4} EXTRA{RESET}    here and not in the "
              f"handoff (usually yours){RESET}")
        if verbose:
            for rel in extra[:40]:
                print(f"        {rel}")

    if missing or differs:
        print(f"\n{RED}Not a clean handoff.{RESET} MISSING means ask for the "
              f"file again — it never arrived. EDITED means either you changed "
              f"it, which you would know, or an older copy landed on top of a "
              f"newer one.")
        return 1
    print(f"\n{GREEN}Everything in the handoff is on this disk, "
          f"byte for byte.{RESET}")
    return 0


if __name__ == "__main__":
    if "--emit" in sys.argv:
        sys.exit(emit())
    sys.exit(check(verbose="-v" in sys.argv))
