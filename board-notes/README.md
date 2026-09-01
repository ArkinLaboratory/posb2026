# Board notes

One PDF per session that has board work, for the instructor, printed and
carried into the room.

**Why these exist.** Session 3 spends nearly forty minutes at a board. That is
the right call — a derivation appearing one line at a time is worth more than
the same derivation revealed on a slide — but a board segment has no artefact.
The slide deck records what is projected and records nothing about what gets
written, so the part of the lecture with the highest cognitive load for the
room is the part with no script. These are the script.

**What is in one.** Every line to write, in the order to write it, with:

- the exact algebra, so nothing is reconstructed live;
- `ASK:` — the question to put to the room before writing the next line, and
  the answer to expect;
- `CHECK:` — the sanity check to do out loud, because doing them is the habit
  being taught;
- `IF ASKED:` — the question that always comes, and the answer;
- `CUT:` — what to drop if you are running late, chosen in advance rather than
  at minute 70.

Timings match the deck's segment badges exactly. If a badge moves, this file
moves with it — and so does `handouts/s03-board-sheet.md`, the students' version
of the same eight segments with the algebra left blank. Three files carry those
timings; changing one and not the others is the obvious way this goes wrong.

```
python tools/build_handouts.py s03-board    # this folder, to PDF
```

Same pipeline as `handouts/`: Markdown with LaTeX in, MathJax rendered at build
time, PDF out. The PDFs are committed.
