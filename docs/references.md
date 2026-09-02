# References

[← back to README](../README.md)

There is **no required textbook** for this course. Readings are primary
literature, posted on bCourses, and short — typically one paper per week with a
specific figure to focus on.

**The schedule of those readings is [Readings](readings.md)**, generated from
`readings.yaml`. The rule there is fixed: a paper discussed in class is assigned
at the end of the previous class, never on the day.

The books below are recommended companions. All three are either free online or
widely available.

---

## Recommended texts

### Elowitz & Bois, *Biological Circuit Design*

Free and online at **[biocircuits.github.io](https://biocircuits.github.io)**.
The course materials for Caltech's BE 150, and the closest neighbour to the
first half of this course. Every narrative chapter is paired with a numbered,
executable technical appendix that regenerates that chapter's figures from
scratch, in the same NumPy/SciPy stack used here.

If a lecture in sessions 3–13 does not land, read the corresponding chapter
there. It is a second voice on the same material with a different framing, not
a substitute for the course.

```bibtex
@misc{elowitz_bois_biocircuits,
  author       = {Elowitz, Michael B. and Bois, Justin S.},
  title        = {Biological Circuit Design},
  howpublished = {\url{https://biocircuits.github.io}},
  note         = {Course materials for Caltech BE 150}
}
```

**The course itself is a separate resource** —
[be150.caltech.edu/2022](http://be150.caltech.edu/2022/) — carrying the lecture
schedule, homework and tutorials that the book does not. Twenty-three lectures,
with guest sessions from Uri Alon.

The numbered technical appendices are the part worth mining, because they are
executable and they land on this course's thinnest material: **TA 10b** (linear
stability analysis) and **TA 11a** (stability diagrams by numerical
eigenvalues) for session 8, **TA 17a** (Gillespie) for session 12, **TA 2a-2b**
for session 5.

Two cautions. Its spine is design principles of natural circuits; ours is
specification to parts to composition to engineering, so its *ordering* is not
transferable even where its derivations are. And this repository is public under
CC BY 4.0 -- credit their figures and code in speaker notes rather than
redistributing them. Deriving our own is the house rule anyway.

### Alon, *An Introduction to Systems Biology*

The standard reference for network motifs. Directly relevant to sessions 7
(autoregulation) and 10 (feedforward loops).

```bibtex
@book{alon2019introduction,
  title     = {An Introduction to Systems Biology: Design Principles of Biological Circuits},
  author    = {Alon, Uri},
  edition   = {2nd},
  year      = {2019},
  publisher = {CRC Press},
  isbn      = {9781439837177}
}
```

### Del Vecchio & Murray, *Biomolecular Feedback Systems*

Free online at
**[cds.caltech.edu/~murray/BFSwiki](https://www.cds.caltech.edu/~murray/BFSwiki/)**.
The reference for retroactivity, insulation, and feedback control — sessions
21 and 22, which are the parts of this course least covered by other textbooks.

```bibtex
@book{delvecchio2014biomolecular,
  title     = {Biomolecular Feedback Systems},
  author    = {Del Vecchio, Domitilla and Murray, Richard M.},
  year      = {2014},
  publisher = {Princeton University Press}
}
```

---

## Session readings

Primary literature for each session is posted on bCourses. Full citations will
be collected here as the term progresses.

<!--
Maintenance note: keep BibTeX entries here verified against the publisher
record, not reconstructed from memory. A fabricated ISBN or year propagates
into every student bibliography that copies from this file.
-->

---

## Citing this course

See [CITATION.cff](../CITATION.cff), or:

```bibtex
@misc{arkin2026posb,
  author       = {Arkin, Adam P.},
  title        = {Principles of Synthetic Biology: course materials for
                  {UC} {B}erkeley {B}io{E} 147/247},
  year         = {2026},
  howpublished = {\url{https://github.com/ArkinLaboratory/posb2026}},
  note         = {Licensed CC BY 4.0 (content) and BSD-3-Clause (code)}
}
```


---

## Sources used in the sessions

Papers the lectures argue from or take numbers from, beyond the assigned
readings in [Readings](readings.md).

### Session 2 — the cell as a physical substrate

**Elowitz, M. B., Surette, M. G., Wolf, P. E., Stock, J. B. & Leibler, S.**
Protein mobility in the cytoplasm of *Escherichia coli*.
*J. Bacteriol.* **181**, 197–203 (1999).
[doi:10.1128/jb.181.1.197-203.1999](https://doi.org/10.1128/jb.181.1.197-203.1999)

> Where *D* = 7.7 ± 2.5 µm²/s comes from — a measurement, in a living cell, of
> a number the course uses all term. About 11× slower than the same protein in
> water, and that factor is the crowding.

**Valverde-Mendez, D., Sunol, A. M., Bratton, B. P., Delarue, M., Hofmann, J. L.,
Sheehan, J. P., Gitai, Z., Holt, L. J., Shaevitz, J. W. & Zia, R. N.**
Macromolecular interactions and geometrical confinement determine the 3D
diffusion of ribosome-sized particles in live *Escherichia coli* cells.
*PNAS* **122**(4), e2406340121 (2025).
[doi:10.1073/pnas.2406340121](https://doi.org/10.1073/pnas.2406340121)

> Two results the session depends on. Effective viscosity is not a property of
> the cytoplasm but of the cytoplasm *and the probe*: ~100 cP for a
> ribosome-sized particle against ~12 cP for GFP. And the apparent subdiffusion
> in tracking data (α ≈ 0.75 for large particles, 0.45 for 20 nm) is produced
> by geometric confinement — nucleoid and cell wall — not by the medium being
> exotic; their higher-resolution simulations recover α > 0.84.
>
> [Demo 2](../demos/d02-crowding/) reproduces both, from scratch, in about
> thirty lines.

**Lee, H., Popodi, E., Tang, H. & Foster, P. L.** Rate and molecular spectrum of
spontaneous mutations in *Escherichia coli* determined by whole-genome
sequencing. *PNAS* **109**, E2774–E2783 (2012).
[doi:10.1073/pnas.1210309109](https://doi.org/10.1073/pnas.1210309109)

> ~1 × 10⁻³ mutations per genome per generation, or ~2 × 10⁻¹⁰ per bp. Session
> 23 computes time-to-circuit-failure from this.
