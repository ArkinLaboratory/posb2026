# Project package — template

Copy this folder, rename it, and replace the worked example with your own
model. Keep the six `##` headings below exactly as written; `check.py` and the
autograder look for them. Delete this paragraph and every *italic instruction*
before you submit.

## What this reproduces

*Which figures and which numbers in your proposal this package regenerates,
named the way the proposal names them (Figure 2, the value of X in section 3).*

Worked example: the response time of an untagged and an LAA-tagged reporter,
and the speed-up the tag buys — `outputs/response.png` and
`outputs/numbers.json`.

## How to run

```
python run.py      # regenerates everything in outputs/
python check.py    # the autograder's mechanical checks, run locally
```

Runs in the course environment (NumPy, SciPy, matplotlib, SymPy and `posb`,
at the versions in the course `requirements.txt`). Under ten minutes on one
CPU, no GPU, no network. *If you need anything else, ask before M3.*

## Contents

| File | What it is |
|---|---|
| `run.py` | The one entry point. Reads `parameters.csv` and `data/`, writes `outputs/` |
| `parameters.csv` | Every parameter: symbol, value, units, source, note |
| `outputs.txt` | The files `run.py` must create |
| `data/` | Input data, with its own README saying where each file came from |
| `outputs/` | Generated. Nothing in here is edited by hand |
| `check.py` | Mechanical checks. Do not edit |

## Parameters and provenance

The table is `parameters.csv`, and `run.py` reads it — so the numbers in the
table are the numbers in the model, and they cannot drift apart. Every row has
a source: a paper, with the table or figure the number comes from, or the word
`assumption`. An assumption is allowed. An unlabeled one is not.

*Below the table's pointer, one short paragraph on the parameters your result
is most sensitive to, and how far you trust each.*

## Methods note: AI use

*What you used, and for what: code, literature search, drafting. One short
paragraph. "None" is an acceptable answer.*

## FAIR self-assessment

*One short paragraph per letter, one page in all. For each of Findable,
Accessible, Interoperable and Reusable: how this package does and does not meet
it, and why. A class project is not deposited and has no persistent identifier,
so the honest answer for F and A is mostly "does not", with what it would take.
I and R are where your choices show: formats, units, the parameter table,
whether someone could change one assumption and rerun.*
