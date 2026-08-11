# Contributing

Errors, unclear explanations, broken links, and confusing notation are all
worth reporting. [Open an issue](https://github.com/ArkinLaboratory/posb2026/issues).

**Students in the course: this counts.** Finding a real error in the material
is a genuine contribution and you will be credited in the repository. Do not
assume someone else has already reported it.

## Useful issue reports

- Which notebook or document, and where in it
- What you expected, and what happened
- The full error text if there is one
- Which environment: DataHub, Colab, or local

## Pull requests

**Do not edit `.ipynb` files directly.** They are build artifacts, generated
from the Python modules in `tools/sources/`. Edit the source module, then:

```bash
python tools/build_notebooks.py
python -m pytest tests/ -q
python tools/execute_notebooks.py
```

All three must pass. CI runs the same checks on every push.

For prose fixes in `docs/`, edit the markdown directly.

## Scope

This is course material with a specific pedagogical design -- see
[Design Notes](docs/design-notes.md). Contributions that fit that design are
welcome; ones that add convenience abstractions to `posb` generally are not,
because the package is deliberately small. If in doubt, open an issue before
writing code.
