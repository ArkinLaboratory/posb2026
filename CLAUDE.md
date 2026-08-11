# Working notes for Claude

How to work in this repository without producing stale artifacts. Read this
first in any new session.

## Where the authoritative copy lives

There are three copies and they drift:

| | |
|---|---|
| `~/Documents/PoSB/posb2026` on Adam's Mac | **authoritative.** This is what gets taught from. |
| `github.com/ArkinLaboratory/posb2026` | the published copy; only as current as the last push |
| Claude's sandbox clone | scratch. A separate filesystem, not a view of either of the above. |

**Claude cannot see or write Adam's disk directly.** The sandbox has its own
filesystem; files reach the Mac only through an explicit copy step. This has
already caused one wasted round trip — a deck source was updated while the built
`.pptx` on the Mac stayed two hours old, and the session was reviewed from the
stale file.

## The rules that follow from that

**1. Start a session by re-syncing.** Ask Adam to push, then:

```
git fetch origin && git reset --hard origin/main
```

Never assume the sandbox clone is current. Its commit hashes will not match the
Mac's even when the content does.

**2. Ship artifacts, not just sources.** Anything generated — `.pptx`, `.pdf`,
figures under `figures/build/` — must be built and copied to the Mac in the same
turn as the source that produced it. A source file the instructor has to build
himself is not a delivery.

**3. Never run git in Adam's repositories.** Reads through the file bridge are
fine. Anything that takes a lock is not: the bridge cannot delete files, so a
stranded `index.lock` blocks his next commit and only he can clear it.

**4. Verify by rendering, not by reasoning.** These decks and handouts are
generated, so "it should look right" is not evidence. Convert to PDF, rasterise,
and look at the pixels. Several layout bugs — stretched figures, boxes hanging
off the slide, captions floating in empty space — were invisible in the source
and obvious in the render.

## Building

```
python tools/build_figures.py [s01]        # figures/build/*.png
python tools/build_decks.py [s01] [--pdf]  # private/build/decks/
python tools/build_handouts.py [--check]   # handouts/*.pdf, committed
python tools/build_readings.py [--check]   # docs/readings.md
python tools/check_schedule.py             # course.yaml vs docs/course-map.md
python -m pytest tests/ -q
```

`private/` is a second, private repository mounted inside this one and ignored
by it. Copyrighted paper figures live in `private/paper-figures/`; the deck
build embeds them if present and draws a labelled slot if not, so the public
build never carries them.

## House rules for the material

- **Nothing is assessed that was not demonstrated first.** The coverage matrix
  is the contract.
- **Do the mathematics.** Derive rather than assert, wherever it fits.
- **Nothing in `posb` is abstracted away before it has been built by hand.**
- **A paper discussed in class is assigned at the end of the previous class.**
  `readings.yaml` enforces this; see [for-instructors](docs/for-instructors.md).
- **Say when something is not known.** Speaker notes carry the provenance
  problems — an uncited figure, a claim with a shelf life — rather than hiding
  them.

## Critique before shipping

Adam wants the hole found, not the compliment. Before delivering, state what is
weakest about the thing just built, and what evidence would settle it. Several
of the better decisions in this repository came from a correction he made to a
draft; the drafts got better when they arrived with their own objections
attached.
