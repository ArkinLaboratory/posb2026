#!/usr/bin/env python3
"""Import the bCourses assignment state to disk, so a local gate can check it.

    # In a session that HAS browser access and is signed in to bCourses:
    #   fetch /api/v1/courses/1557313/assignments?per_page=100
    #   save the response body to a file, then:
    python tools/import_platform_manifest.py canvas-assignments.json
    pbpaste | python tools/import_platform_manifest.py -        # or paste it

THIS SCRIPT DOES NOT TALK TO CANVAS, AND MUST NOT LEARN HOW.
`tools/preflight.py` runs on a laptop with no Canvas credentials and no
network, and that is the property worth keeping: a gate that needs a token is a
gate that gets skipped at 7am. So the platform state is imported by whatever
can reach it -- a browser session, curl with a token, a human with Save As --
and this script's only job is to reduce that blob to the fields the gate reads
and stamp it with the UTC time it was read.

There is no browser automation here on purpose. Nothing in this repository
should hold a Canvas token or drive a logged-in session unattended.

WHAT COMES OUT
`private/platform-manifest.json`: a JSON object with a file-level `read_at` and
one entry per assignment carrying id, name, due_at, published,
submission_types, allowed_extensions, points_possible, created_at, updated_at
and its own `read_at`. The `item` field is this script's guess at which
syllabus graded item the assignment is -- M3, FINAL, PS8 -- printed on import
so a human can correct it. The gate prefers that field over name matching,
because a rename on bCourses should not silently un-check an assignment.

It lives under private/ because private/ is a separate, non-public repository:
the file carries no secrets, but it does carry the course's internal Canvas
ids, and nothing is gained by publishing them.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "private" / "platform-manifest.json"
COURSE_ID = 1557313
ENDPOINT = f"/api/v1/courses/{COURSE_ID}/assignments?per_page=100"

KEEP = ["id", "name", "due_at", "published", "submission_types",
        "allowed_extensions", "points_possible", "created_at", "updated_at",
        "html_url"]


def reduce_blob(blob, read_at):
    """Canvas's assignment list -> the manifest's `assignments`."""
    if isinstance(blob, dict):
        rows = blob.get("assignments") or blob.get("data") or []
    else:
        rows = blob
    if not isinstance(rows, list):
        raise SystemExit("expected a JSON array of assignments, or an object "
                         "with an 'assignments' key")
    out = []
    for a in rows:
        if not isinstance(a, dict):
            continue
        e = {k: a.get(k) for k in KEEP}
        e["read_at"] = read_at
        out.append(e)
    if not out:
        raise SystemExit("the blob contained no assignments -- check that you "
                         f"saved the body of GET {ENDPOINT}")
    return out


def guess_items(entries):
    """Stamp each entry with the syllabus item it appears to be.

    Uses the gate's own matcher, so the guess and the check cannot disagree
    about what counts as a match.
    """
    from tools import graded_items as gi
    matched = {}
    fake = {"assignments": entries}
    for item in gi.all_graded():
        e = gi.match_entry(item, fake)
        if e is not None and not e.get("item"):
            e["item"] = item.ident
            matched[item.ident] = e.get("name")
    return matched


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", help="path to the saved JSON body, or - for stdin")
    ap.add_argument("--read-at", default=None,
                    help="UTC timestamp of the read (default: now). Set this "
                         "if the blob was captured earlier than this import.")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()

    text = sys.stdin.read() if a.source == "-" else \
        Path(a.source).read_text(encoding="utf-8")
    blob = json.loads(text)

    read_at = a.read_at or datetime.datetime.now(
        datetime.timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z")

    entries = reduce_blob(blob, read_at)
    matched = guess_items(entries)

    manifest = {
        "course_id": COURSE_ID,
        "source": f"GET {ENDPOINT}",
        "read_at": read_at,
        "imported_by": "tools/import_platform_manifest.py",
        "assignments": entries,
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n",
                   encoding="utf-8")

    print(f"wrote {out} — {len(entries)} assignment(s), read_at {read_at}")
    print("\nmatched to syllabus items:")
    for ident, name in sorted(matched.items()):
        print(f"  {ident:<11} {name}")
    unmatched = [e["name"] for e in entries if not e.get("item")]
    if unmatched:
        print("\nnot matched to any syllabus graded item (fine for anything "
              "that is not one; add an \"item\" field by hand if it is):")
        for n in unmatched:
            print(f"  — {n}")
    print("\nNow run: python tools/preflight.py")


if __name__ == "__main__":
    main()
