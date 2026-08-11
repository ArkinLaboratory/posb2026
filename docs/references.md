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
