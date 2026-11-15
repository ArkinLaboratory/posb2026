"""Classifying one cell type out of a panel, to a budget for the mistakes --
session 26's object, PS9's T69 and T70.

THE OBJECT, AND IT IS NOT THE ONE SESSION 16 BUILT. `posb.logic` already holds
a cancer-cell classifier: `classifier_2025`, three repressors, a truth table
and a cold-start hazard. It is BOOLEAN, and a Boolean circuit has nothing to
move -- no threshold, therefore no error rate, therefore no budget. Here the
same job is done by a PRODUCT OF CONTINUOUS SENSOR RESPONSES WITH A CUT ON IT,
and the cut is the design variable. Import both modules in one notebook if you
like, but do not reason about one while holding the other: `logic` answers
"what does this circuit compute", this module answers "how often is it wrong,
and in which direction".

THE PAPER. Xie, Wroblewska, Prochazka, Weiss & Benenson, Science 333, 1307
(2011). A six-marker miRNA classifier in five sensor modules (miR-17 and
miR-30a share one), printed on p.1308 as

    miR-21 AND miR-17-30a AND NOT(miR-141) AND NOT(miR-142(3p))
           AND NOT(miR-146a)

evaluated across seven cell lines of which HeLa is the only positive. Five of
the six negatives are themselves cancer lines (SOM cell-line list), so A FALSE
POSITIVE HERE IS THE WRONG CANCER, IN A PATIENT, and not a healthy cell.

NO DATA LIVES IN THIS FILE. The 7 x 5 response matrix is DIGITIZED off Fig. 2D
and lives in `sessions/s26-therapeutics/NUMBERS.md`; the supplement's tables
are transfection recipes and contain no responses at all (NUMBERS sec 0.1).
Every function here takes the panel as an argument, so a student can pass
their own markers, their own lines and their own target cell type -- which is
the assignment, not a convenience.

WHAT A RESPONSE IS, AND READ THIS BEFORE PASSING A MATRIX. `responses[line]
[marker]` is the NORMALIZED LEVEL OF THE MARKER in that line: 1.0 means as
present as this panel ever sees it, 0.0 means absent. IT IS NOT THE SENSOR
MODULE'S OUTPUT. The two differ by exactly the inversion that the NOT terms
perform, and confusing them is the sign error this module exists to catch --
Fig. 2D plots SENSOR responses, already oriented so that HeLa reads high in
every series, so its HeLa-low columns have been inverted once already. Invert
them a second time by declaring `sense="absent"` and the circuit you score is
miR-141 AND miR-142(3p) AND miR-146a AND NOT(miR-21), which is a classifier
for everything HeLa is not. Nothing about the numbers looks wrong. Call
`sense_check` before trusting any confusion matrix.

AND THE SIGN GUARD IS TWO DIFFERENT QUESTIONS, WHICH IS WHY IT IS TWO
FUNCTIONS. "Is this matrix in the convention I declared?" is answered for the
WHOLE PANEL AT ONCE by `convention_check`, which runs NUMBERS sec 2.1's own
decisive test -- under the right reading the positive line is the maximum of
the product across every line -- and says nothing when that test passes. "How
much does each marker contribute to the positive line's lead?" is answered,
per marker and with no causal claim attached, by `marker_utility`. The two
were one check once, and conflating them made a marker's weak showing on a
seven-line panel read as evidence of a convention error, which it is not.

AND A PASSING TEST SUITE PROTECTED THAT DEFECT, WHICH IS THE PART WORTH
REMEMBERING. The suite was 937 tests green while the check fired on Xie's
own matrix in the correct convention. The test that covered it asserted
BREADTH -- that the complaint list named EVERY marker -- so it locked in the
one property the defect had and a correct diagnostic does not. A test that
pins how LOUD a diagnostic is pins its false positives too. Assert direction
and silence instead, and keep the real input in the suite: the Fig. 2D
matrix now sits in `tests/test_classifiers.py` as a checked mirror of
NUMBERS sec 2.2, because the correct input that tripped the check is the one
input no synthetic panel was ever going to supply.

THE LOGIC IS A PRODUCT, WHICH IS WHAT MAKES A BUDGET POSSIBLE.

    output(line) = prod over markers of   r            if sense is "high"
                                          (1 - r)      if sense is "absent"

with r = responses[line][marker]. Every factor lies in [0, 1], so the output
does too, and AND is multiplication rather than a gate. Each sensor degrades
the output continuously; nothing in the arithmetic ever decides anything. The
deciding is one comparison, made outside the circuit, and it is yours.

THE THRESHOLD IS THE DESIGN VARIABLE AND IT HAS NO DEFAULT. Fig. 2A's caption
prints Xie's own definition -- "input combinations that result in 20% output
relative to HeLa cells" -- so a threshold in this module is by default a
FRACTION OF THE POSITIVE LINE'S OWN OUTPUT (`relative=True`). YOU DO NOT GET A
CLASSIFIER; YOU GET A FAMILY OF THEM INDEXED BY A THRESHOLD, and `confusion`
refuses to pick one for you.

WHY RELATIVE IS NOT A COSMETIC CHOICE. Under a relative threshold, adding a
marker that separates -- one whose contribution in the positive line is at
least its contribution in every negative -- multiplies each negative's RATIO
to the positive by a factor <= 1 and leaves the positive's own ratio at
exactly 1. So it cannot create a false positive and cannot lose the positive.
Under an ABSOLUTE threshold the same addition shrinks every output including
the positive's, and the positive can drop below the cut: "adding information
made the classifier worse" becomes possible, and it is an artifact of the
convention rather than a fact about the markers. Both conventions are here;
the relative one is the paper's and is the one the monotonicity properties
hold in.

SPECIFICITY IS A POPULATION STATISTIC, AND SEVEN CELL LINES CANNOT MEASURE IT.
`confusion` counts CELL LINES, not cells. Six negative lines resolve a
per-cell false-positive rate no finer than 1/6 = 0.167, and zero false
positives among six lines is NOT a rate of zero: the exact one-sided 95% bound
is 1 - 0.05^(1/6) = 0.393 (`fp_rate_upper_bound`). A design that looks perfect
on this panel has shown that the per-cell rate is below about forty percent,
and nothing else. Then Fig. 4B puts HeLa and HEK293 IN ONE DISH and about a
third of the line the circuit is meant to spare dies anyway -- roughly double
what the per-line assays predict (DIGITIZED; pending the Fig. 4B pass in
NUMBERS). PER-LINE CHARACTERISATION DOES NOT COMPOSE, and that is the hour's
last move rather than a caveat on it.

THE T63 RHYME, WHICH IS WHY PS9 IS ONE SET. `wrong_cells_per_dose` is
`posb.evolution.escapers_per_dose` with the sign of the intent reversed. There
a per-cell escape fraction times 10^8 CFU is compared against a budget of one
survivor: a device that must not act. Here a per-cell error rate times a
treated population is compared against a budget of one wrong cell: a device
that must not act ON THE WRONG CELL. Same arithmetic, same budget of one,
opposite sign. Read `escapers_per_dose` first; the two functions are
deliberately the same shape.

WHAT THIS MODULE DELIBERATELY DOES NOT DO.

* No sensor model. There is no Hill function, no miRNA-target kinetics and no
  fit anywhere in this file -- the responses are measurements you supply. A
  mechanistic sensor model is session 13's and session 18's material and has
  not been built by hand for miRNA.
* No ROC curve and no AUC. With one positive line the sensitivity axis takes
  two values, and an area under a two-point curve is a number with no error
  bar and an unearned smell of rigour. Sweep the threshold and read the
  confusion matrices instead; that is T70.
* No per-cell rate. The thing that would actually give one is a single-cell
  distribution of output within a line, and no figure in the paper prints it.
  `wrong_cells_per_dose` therefore takes the rate as an ARGUMENT and the
  treated population as an ARGUMENT, and says so: the number is the student's
  and has to be defended.
"""
import itertools
import math

import numpy as np

__all__ = [
    "SENSES",
    "response_table", "marker_levels_from_sensor_outputs",
    "normalize_responses",
    "sensor_response", "classifier_output", "sense_check",
    "ConventionCheck", "convention_check",
    "MarkerUtility", "marker_utility",
    "Confusion", "confusion", "fp_rate_upper_bound",
    "wrong_cells_per_dose",
    "Design", "design_to_budget",
]

#: The only two senses a marker can have. There is no third one, and there is
#: no boolean spelling of these -- see `_canonical_sense`.
SENSES = ("high", "absent")

_WRONG_WORDS = ("low", "lo", "off", "not", "none", "down", "negative",
                "absent_high", "high_low")


def _canonical_sense(marker, word):
    """The one place a sense is read. Returns 'high' or 'absent'.

    'high' means the marker must be ABUNDANT in the target cell type; the
    sensor passes its level through. 'absent' means the marker must be ABSENT
    from the target cell type; the sensor is repressed by it, so it
    contributes (1 - level). Those are the AND terms and the NOT terms of
    Xie's expression, and nothing else is accepted.
    """
    if isinstance(word, (bool, np.bool_)):
        raise ValueError(
            f"sense[{marker!r}] is {word!r}. A sense is the word 'high' or "
            f"'absent', never True/False. A boolean does not record WHICH "
            f"way round it is read, so a flipped convention turns "
            f"NOT(miR-141) into miR-141 with nothing in the data to show it.")
    if not isinstance(word, str):
        raise ValueError(
            f"sense[{marker!r}] is {word!r} ({type(word).__name__}). A sense "
            f"is the string 'high' or 'absent'.")
    w = word.strip().lower()
    if w in SENSES:
        return w
    hint = ""
    if w in _WRONG_WORDS:
        hint = (f" {w!r} is ambiguous in exactly the way this module is "
                f"built to prevent: it names the MARKER level in one reading "
                f"and the SENSOR output in the other, and those are "
                f"opposite. Say 'absent' if the marker must be absent from "
                f"the target cell type.")
    raise ValueError(
        f"sense[{marker!r}] = {word!r} is not a sense. The two senses are "
        f"'high' (the marker must be ABUNDANT in the target cell type) and "
        f"'absent' (it must be ABSENT from it).{hint}")


def _canonical_senses(markers, sense):
    """Resolve a sense for every requested marker, or say which are missing."""
    try:
        missing = [m for m in markers if m not in sense]
    except TypeError:
        raise ValueError(
            f"sense must be a mapping marker -> 'high'/'absent'; got "
            f"{type(sense).__name__}")
    if missing:
        raise ValueError(
            f"no sense given for {missing}. Every marker in a classifier is "
            f"either required HIGH or required ABSENT; there is no default, "
            f"because the default would silently be one of the two.")
    return {m: _canonical_sense(m, sense[m]) for m in markers}


def _check_levels(levels, where):
    """Responses are normalized marker levels in [0, 1]."""
    a = np.asarray(levels, float)
    if np.any(~np.isfinite(a)):
        raise ValueError(f"{where}: a response must be finite; got {a}")
    if np.any((a < 0.0) | (a > 1.0)):
        raise ValueError(
            f"{where}: a response is a NORMALIZED MARKER LEVEL in [0, 1], "
            f"where 1.0 means the marker is as present as this panel ever "
            f"sees it and 0.0 means absent; got min {float(np.min(a)):.4g}, "
            f"max {float(np.max(a)):.4g}. A digitization in arbitrary "
            f"fluorescence units goes through `normalize_responses` first -- "
            f"and note that normalization is panel-relative, so adding a "
            f"cell line changes every number in the table.")
    return a


def _check_table(responses, markers, positive=None):
    """Validate a response table against the markers a call actually uses."""
    if not isinstance(responses, dict) or not responses:
        raise ValueError(
            "responses is a non-empty mapping cell_line -> {marker: level}. "
            "Build one with `response_table(matrix, cell_lines, markers)`; "
            "no panel is baked into this module.")
    lines = list(responses)
    gaps = []
    for line in lines:
        row = responses[line]
        if not isinstance(row, dict):
            raise ValueError(
                f"responses[{line!r}] is {type(row).__name__}; each row is a "
                f"mapping marker -> level")
        for m in markers:
            if m not in row:
                gaps.append((line, m))
            else:
                _check_levels(row[m], f"responses[{line!r}][{m!r}]")
    if gaps:
        raise ValueError(
            f"the response table has holes at {gaps[:8]}"
            f"{' ...' if len(gaps) > 8 else ''}. A missing response is not a "
            f"zero: a zero says the marker is absent, which is a measurement.")
    if positive is not None and positive not in responses:
        raise ValueError(
            f"the positive cell type {positive!r} is not in the panel "
            f"{lines}. The target cell type is yours to choose, but it has "
            f"to be one of the lines you measured.")
    return lines


def response_table(matrix, cell_lines, markers):
    """Build a response table from a labelled matrix. CELL LINES ARE ROWS.

    Returns {cell_line: {marker: level}}, which is what every other function
    here takes. Labels rather than indices on purpose: the Fig. 2D matrix is
    7 x 5 and the commonest way to lose an hour on it is to pass the
    transpose, or to reorder the markers and not the senses.

    `matrix[i][j]` is the normalized level of `markers[j]` in
    `cell_lines[i]`, in [0, 1].
    """
    m = np.asarray(matrix, float)
    lines = list(cell_lines)
    marks = list(markers)
    if m.ndim != 2:
        raise ValueError(f"matrix must be 2-D; got shape {m.shape}")
    if len(set(lines)) != len(lines):
        raise ValueError(f"duplicate cell line names in {lines}")
    if len(set(marks)) != len(marks):
        raise ValueError(f"duplicate marker names in {marks}")
    if m.shape != (len(lines), len(marks)):
        extra = ""
        if m.shape == (len(marks), len(lines)):
            extra = (" That is the TRANSPOSE of what you passed: this "
                     "function takes cell lines as ROWS and markers as "
                     "COLUMNS.")
        raise ValueError(
            f"matrix is {m.shape[0]} x {m.shape[1]} but you named "
            f"{len(lines)} cell lines and {len(marks)} markers.{extra}")
    _check_levels(m, "matrix")
    return {line: {mk: float(m[i, j]) for j, mk in enumerate(marks)}
            for i, line in enumerate(lines)}


def marker_levels_from_sensor_outputs(matrix, cell_lines, markers, sense):
    """A response table from a matrix of SENSOR outputs. Read this twice.

    Fig. 2D plots sensor responses, not marker levels: each series is already
    oriented so that the target line reads high, which means the HeLa-low
    sensors have had their NOT applied once by the biology before anything
    was digitized. Pass such a matrix straight to `response_table` and
    `classifier_output` applies those NOTs a second time -- the sign error
    this module exists to catch, and the one `sense_check` complains about.

    This function undoes the first application, exactly once, for the markers
    declared `absent`: level = 1 - sensor_output. The round trip is then the
    identity, which is tested.

    AND IT IS A MODELLING STEP, NOT BOOKKEEPING. `1 - r` is the inverse of
    THIS MODULE'S idealized sensor, in which a repressed module passes
    exactly the complement of its input. A real RNAi sensor has a transfer
    function with a leak, a ceiling and a slope (session 13's object), and
    inverting a measured output through the idealization moves whatever that
    transfer function does into the "level" it returns.

    The honest alternative is to keep Fig. 2D's sensor outputs as the
    quantities the product is taken over -- which is what Xie does -- and
    declare every sense `high`, because the NOT terms are then already in the
    data. That is defensible arithmetic and a worse teaching object: the
    expression on p.1308 has three NOTs in it and nothing in the code would
    show them. Pick one, say which in the problem statement, and do not mix
    them in one table.
    """
    senses = _canonical_senses(markers, sense)
    table = response_table(matrix, cell_lines, markers)
    return {ln: {m: (v if senses[m] == "high" else 1.0 - v)
                 for m, v in row.items()}
            for ln, row in table.items()}


def normalize_responses(responses, markers=None):
    """Divide each marker's column by its maximum across the panel.

    For a digitization that comes off a figure in arbitrary units. Returns a
    new table; the input is not touched.

    THE NORMALIZATION IS PANEL-RELATIVE AND THAT IS A MODELLING CHOICE, not
    bookkeeping. After it, 1.0 means "the most of this marker seen in THESE
    lines", so adding an eighth cell line can change every number in the
    table and therefore every output, every confusion matrix and every rate
    downstream. If the digitization is already on a fixed scale -- a fraction
    of a saturating control, say -- do not call this.
    """
    marks = list(markers) if markers is not None else sorted(
        {m for row in responses.values() for m in row})
    _check_table(responses, [], None)
    out = {}
    for mk in marks:
        col = [responses[line][mk] for line in responses if mk in responses[line]]
        if not col:
            raise ValueError(f"no line in the panel has marker {mk!r}")
        top = max(float(c) for c in col)
        if top <= 0.0:
            raise ValueError(
                f"marker {mk!r} is zero in every line, so there is nothing "
                f"to normalize it by. A marker no line expresses carries no "
                f"information and, with sense='high', switches the output "
                f"off everywhere.")
        for line in responses:
            if mk in responses[line]:
                out.setdefault(line, {})[mk] = float(responses[line][mk]) / top
    return out


def sensor_response(level, sense):
    """One sensor module's contribution to the product. THE NOT TERMS LIVE HERE.

    `sense='high'` returns the level; `sense='absent'` returns 1 - level.
    That single subtraction is the whole of NOT in this module, and it is a
    separate function so that it can be read, tested and got wrong in one
    visible place rather than inside a loop.

    Vectorized over `level`.
    """
    s = _canonical_sense("<marker>", sense)
    a = _check_levels(level, "level")
    return a if s == "high" else 1.0 - a


def classifier_output(responses, markers, sense):
    """The classifier's continuous output for every line in the panel. T69.

    Returns {cell_line: output}, where

        output = prod over markers of sensor_response(level, sense[marker])

    AND IS MULTIPLICATION, not a gate. Every factor is in [0, 1] so the output
    is too, and no comparison has been made yet -- this function cannot tell
    you what the circuit decides, only how much output each line gets. The
    deciding is `confusion`, and it needs a threshold you choose.

    An empty `markers` would be a product over nothing, i.e. 1.0 for every
    line, which is a classifier that fires on everything; it is refused rather
    than returned.
    """
    marks = list(markers)
    if not marks:
        raise ValueError(
            "a classifier needs at least one marker. A product over no "
            "markers is 1.0 in every line -- a circuit that fires on "
            "everything, which is not a degenerate classifier so much as no "
            "classifier at all.")
    if len(set(marks)) != len(marks):
        raise ValueError(
            f"markers repeat in {marks}. A repeated marker squares its own "
            f"contribution, which is a second sensor module against the same "
            f"miRNA and not what the expression says.")
    senses = _canonical_senses(marks, sense)
    lines = _check_table(responses, marks)
    out = {}
    for line in lines:
        p = 1.0
        for mk in marks:
            p *= float(sensor_response(responses[line][mk], senses[mk]))
        out[line] = p
    return out


def _negatives(lines, positive):
    """The negative lines, or the refusal that a one-line panel earns."""
    negatives = [ln for ln in lines if ln != positive]
    if not negatives:
        raise ValueError(
            f"the panel holds only {positive!r}, so there is nothing to "
            f"separate it from. A sense check, like a confusion matrix, "
            f"needs at least one negative line.")
    return negatives


def _top_and_margin(out, positive):
    """(lines tied at the panel maximum, positive / best negative).

    The margin is a RATIO because the threshold is relative by default: a
    negative whose output exceeds the positive's is a false positive at every
    relative threshold at or below 1.0, whatever the absolute numbers are.
    """
    top = max(out.values())
    tied = tuple(ln for ln in out if out[ln] == top)
    best = max(out[ln] for ln in out if ln != positive)
    pos = out[positive]
    if best > 0.0:
        margin = pos / best
    else:
        margin = float("inf") if pos > 0.0 else float("nan")
    return tied, best, margin


class ConventionCheck:
    """What `convention_check` found. ALWAYS TRUTHY -- read `.ok`.

    Like `Design`, this is an object rather than a bool or an empty list
    because `if convention_check(...)` reading as "the convention is fine" is
    exactly how a caught sign error gets uncaught again.

    * `ok` -- True when the declared senses make the positive line the strict
      maximum of the product across the panel. That is NUMBERS sec 2.1's
      decisive test, and when it passes this object claims nothing.
    * `margin` -- positive output / best negative output, under the declared
      senses. Greater than 1.0 exactly when `ok`.
    * `declared_top` -- the lines tied at the panel maximum under the declared
      senses. A tie is not a win: with exact zeros in a matrix every line can
      product to 0.0, and the positive "winning" a seven-way tie at zero is
      the sign error, not the absence of one.
    * `alternative` -- the name of the reading that DOES make the positive the
      strict maximum, or None. `'sensor-output'` means the declared `absent`
      senses are being applied to data that already contains them;
      `'global-polarity'` means every column reads the opposite way round.
    * `message` -- one string, or None when `ok`. Says what the arithmetic
      shows and names the remedy; it asserts a cause only when an alternative
      reading actually wins.
    """

    _FIELDS = ("ok", "positive", "markers", "margin", "declared_top",
               "declared_outputs", "alternative", "alternative_senses",
               "alternative_margin", "message")

    def __init__(self, **kw):
        missing = [f for f in self._FIELDS if f not in kw]
        if missing:
            raise TypeError(f"ConventionCheck is missing {missing}")
        extra = [k for k in kw if k not in self._FIELDS]
        if extra:
            raise TypeError(f"ConventionCheck got unexpected {extra}")
        for f in self._FIELDS:
            setattr(self, f, kw[f])

    def as_dict(self):
        return {f: getattr(self, f) for f in self._FIELDS}

    def __repr__(self):
        return (f"ConventionCheck(ok={self.ok}, margin={self.margin:.4g}, "
                f"alternative={self.alternative!r})")


def convention_check(responses, markers, sense, positive):
    """Is this matrix in the convention the senses were declared in? T69.

    ONE TEST, OVER THE WHOLE PANEL, AND IT IS THE PAPER'S OWN. NUMBERS sec
    2.1 settles the question for Fig. 2D by one multiplication per line:
    under the correct reading the product makes the positive line the
    maximum across every line in the panel. Read the same bars as marker
    levels instead -- applying the three NOT terms a second time -- and SKBR3
    wins with HeLa second. So this function asks exactly that, and asks it of
    the panel rather than of one marker at a time.

    WHEN IT SPEAKS. Only when the declared senses fail that test. If they
    pass it, there is nothing to report and `ok` is True -- which is a
    property worth stating plainly: A CORRECT CONFIGURATION CANNOT RAISE A
    CONVENTION WARNING HERE, because passing the test is the definition of
    being silent. The old per-marker version of this check had no such
    property and fired on four of the five leave-one-out subsets of a correct
    Fig. 2D configuration.

    THE TWO ALTERNATIVE READINGS, AND WHY NOT JUST ONE. When the declared
    senses fail, two other readings of the same numbers are tried:

    * `'sensor-output'` -- every marker declared `absent` is read `high`
      instead. This is the documented error exactly: feeding Fig. 2D's bars
      in as marker levels applies the NOTs twice, and un-applying them is the
      same arithmetic as `marker_levels_from_sensor_outputs` followed by the
      declared senses. It is NOT a global inversion, because a marker
      declared `high` reads the same in both conventions -- a sensor oriented
      so the target reads high IS the marker level when no NOT is involved.
      A global flip of all five senses does not catch Fig. 2D's double
      inversion at all (it makes HEK293 the winner, with HeLa sixth), so a
      check built only on global inversion would be silent on the one error
      this module exists to catch.
    * `'global-polarity'` -- every sense flipped. This catches a matrix whose
      every column is the complement of what was declared, which a global
      inversion is and the first hypothesis is not.

    NO MAGNITUDE FLOOR, AND NONE IS NEEDED. The test is a comparison of
    argmaxes, not a difference of two nearly equal small numbers, so there is
    no quantity here that a 0.018 wobble can push over a line. The floor the
    old check needed was a symptom of thresholding the wrong quantity.

    Returns a `ConventionCheck`. It decides nothing and raises nothing except
    on a panel with no negative line.
    """
    marks = list(markers)
    senses = _canonical_senses(marks, sense)
    lines = _check_table(responses, marks, positive)
    _negatives(lines, positive)

    out = classifier_output(responses, marks, senses)
    top, _best, margin = _top_and_margin(out, positive)
    base = dict(positive=positive, markers=tuple(marks), margin=margin,
                declared_top=top, declared_outputs=out)
    if top == (positive,):
        return ConventionCheck(ok=True, alternative=None,
                               alternative_senses=None,
                               alternative_margin=None, message=None, **base)

    if len(top) > 1 and positive in top:
        standing = (f"{positive!r} only TIES for the panel maximum, with "
                    f"{sorted(ln for ln in top if ln != positive)} at "
                    f"{out[positive]:.4g}")
    else:
        other = top[0]
        standing = (f"{positive!r} is not the panel maximum -- {other!r} is, "
                    f"at {out[other]:.4g} against {out[positive]:.4g}")

    hypotheses = []
    lifted = {m: ("high" if senses[m] == "absent" else senses[m])
              for m in marks}
    if lifted != senses:
        hypotheses.append(("sensor-output", lifted))
    flipped = {m: ("absent" if senses[m] == "high" else "high")
               for m in marks}
    if flipped != senses and all(flipped != h for _n, h in hypotheses):
        hypotheses.append(("global-polarity", flipped))

    for name, cand in hypotheses:
        alt = classifier_output(responses, marks, cand)
        alt_top, _b, alt_margin = _top_and_margin(alt, positive)
        if alt_top != (positive,):
            continue
        if name == "sensor-output":
            inverted = sorted(m for m in marks if senses[m] == "absent")
            why = (
                f"{standing}, but reading this matrix as SENSOR OUTPUTS does "
                f"make it the maximum, by {alt_margin:.4g}x. Fig. 2D's bars "
                f"are sensor outputs, in which the NOT terms are already "
                f"applied inside the sensors, so declaring {inverted} "
                f"{'absent'!r} applies them a second time. Convert at the "
                f"data boundary with marker_levels_from_sensor_outputs, or "
                f"keep the sensor outputs and declare every sense "
                f"{'high'!r} -- but say which in the problem statement and "
                f"do not mix them in one table (NUMBERS sec 2.1).")
        else:
            why = (
                f"{standing}, but inverting EVERY marker's sense does make "
                f"it the maximum, by {alt_margin:.4g}x. Every column of this "
                f"matrix reads in the opposite polarity to the sense it was "
                f"declared with.")
        return ConventionCheck(ok=False, alternative=name,
                               alternative_senses=cand,
                               alternative_margin=alt_margin,
                               message=why, **base)

    tried = "no other reading of these numbers" if not hypotheses else (
        "neither reading it as sensor outputs nor inverting every sense")
    why = (
        f"{standing}, and {tried} fixes that. Under a relative threshold a "
        f"line above the positive is a false positive at EVERY threshold at "
        f"or below 1.0, so no cut rescues this. This is a statement about "
        f"these markers on this panel, not a diagnosis of the convention: "
        f"the senses may be right and the marker set simply insufficient.")
    return ConventionCheck(ok=False, alternative=None,
                           alternative_senses=None, alternative_margin=None,
                           message=why, **base)


class MarkerUtility:
    """What one marker does to the positive line's lead ON THIS PANEL.

    `note` is None when the positive line IS the panel's top reader of this
    marker -- there is nothing to remark on -- and otherwise a string naming
    the line that reads higher and what dropping the marker would do to the
    margin. IT IS NOT A COMPLAINT AND IT IS NOT A CONVENTION DIAGNOSIS, and
    the string says so, because this was once a `sense_check` warning that
    blamed a weak marker on a double inversion.
    """

    _FIELDS = ("marker", "sense", "positive", "positive_contribution",
               "best_negative", "best_negative_contribution", "deficit",
               "top_reader", "panel_margin", "margin_without", "note")

    def __init__(self, **kw):
        missing = [f for f in self._FIELDS if f not in kw]
        if missing:
            raise TypeError(f"MarkerUtility is missing {missing}")
        extra = [k for k in kw if k not in self._FIELDS]
        if extra:
            raise TypeError(f"MarkerUtility got unexpected {extra}")
        for f in self._FIELDS:
            setattr(self, f, kw[f])

    def as_dict(self):
        return {f: getattr(self, f) for f in self._FIELDS}

    def __repr__(self):
        return (f"MarkerUtility(marker={self.marker!r}, "
                f"deficit={self.deficit:+.4g}, "
                f"top_reader={self.top_reader})")


def marker_utility(responses, markers, sense, positive):
    """Per marker: does the positive line read highest, and what is the
    marker worth to the margin? T69's reporting half.

    Returns one `MarkerUtility` per marker, in the order given -- a table, not
    a verdict. For each marker it reports the positive line's contribution
    under the declared sense, the negative line that contributes most, the
    deficit between them, and the panel's margin with and without this
    marker (leave-one-out, which is the quantity that actually measures how
    much a marker is worth to the positive line's lead).

    IT IS A SEPARATE FUNCTION FROM `sense_check` ON PURPOSE. `sense_check`
    returns a list of complaints whose EMPTINESS means "the panel is
    consistent with what you declared". A marker on which the positive line
    is not the top reader is a perfectly ordinary fact about a correct
    configuration -- in Xie's Fig. 2D it is true of four of the five markers
    -- so putting it in that list makes an empty list unreachable and the
    check uninformative. This is the defect this split repairs: an
    observation was being delivered down a channel whose semantics are "you
    have made a mistake".

    AND IT ASSERTS NO CAUSE. It says nothing about conventions, nothing about
    double inversion, and nothing about whether the marker should stay in the
    circuit. IT CANNOT SAY THE LATTER. A marker can discriminate poorly
    across a small panel and still be required: the panel here is seven
    adherent lines in culture, and a marker's job in the circuit may be to
    exclude cell types the panel does not contain at all. `convention_check`
    answers the convention question; this answers neither it nor the
    design question.

    NO MAGNITUDE FLOOR. Every marker gets a row and every number is printed,
    so there is nothing for a floor to suppress. A floor would be needed only
    if this function raised an alarm, and it does not.
    """
    marks = list(markers)
    senses = _canonical_senses(marks, sense)
    lines = _check_table(responses, marks, positive)
    negatives = _negatives(lines, positive)

    out = classifier_output(responses, marks, senses)
    _top, _best, panel_margin = _top_and_margin(out, positive)
    n_lines = len(lines)

    report = []
    for mk in marks:
        rest = [m for m in marks if m != mk]
        if rest:
            sub = classifier_output(responses, rest,
                                    {m: senses[m] for m in rest})
            _t, _b, without = _top_and_margin(sub, positive)
        else:
            without = None
        c_pos = float(sensor_response(responses[positive][mk], senses[mk]))
        contrib = {ln: float(sensor_response(responses[ln][mk], senses[mk]))
                   for ln in negatives}
        best_ln = max(contrib, key=contrib.get)
        deficit = c_pos - contrib[best_ln]
        top_reader = deficit > 0.0
        if top_reader:
            note = None
        else:
            tied = "ties with" if deficit == 0.0 else "reads below"
            lead = ("" if without is None else
                    f" Leaving it out moves the panel's margin over the best "
                    f"negative from {panel_margin:.4g}x to {without:.4g}x.")
            note = (
                f"{mk!r} (declared {senses[mk]!r}): {positive!r} {tied} "
                f"{best_ln!r} as this panel's top reader -- {best_ln!r} "
                f"contributes {contrib[best_ln]:.4f} against "
                f"{c_pos:.4f}, a deficit of {deficit:+.4f}.{lead} That is a "
                f"statement about these {n_lines} cell lines and nothing "
                f"else. It is not a convention diagnosis -- "
                f"convention_check answers that question for the whole panel "
                f"-- and it is not a reason to drop the marker: a marker can "
                f"discriminate poorly across a panel this small and still be "
                f"required, since its job in the circuit may be to exclude "
                f"cell types the panel does not contain.")
        report.append(MarkerUtility(
            marker=mk, sense=senses[mk], positive=positive,
            positive_contribution=c_pos, best_negative=best_ln,
            best_negative_contribution=contrib[best_ln], deficit=deficit,
            top_reader=top_reader, panel_margin=panel_margin,
            margin_without=without, note=note))
    return report


def sense_check(responses, markers, sense, positive):
    """What the panel says about the senses you declared. T69's sign guard.

    Returns a list of complaints; an empty list means the panel is consistent
    with everything you gave it. It decides nothing and raises nothing -- a
    marker CAN legitimately be declared against the data, and a list of
    complaints is an argument to answer rather than a verdict.

    Three things get said, and THE FIRST IS ABOUT THE PANEL AS A WHOLE, not
    about one marker:

    * **This matrix is not in the convention you declared.** Delegated whole
      to `convention_check`, which runs NUMBERS sec 2.1's decisive test: the
      declared senses fail to make the positive line the strict maximum of
      the product across the panel, and some other reading of the same
      numbers succeeds. THIS IS THE CHECK THAT CATCHES A RESPONSE MATRIX OF
      SENSOR OUTPUTS PASSED AS MARKER LEVELS, which inverts every NOT term
      silently. It says nothing at all when the positive line does win, so a
      correct configuration cannot raise it.
    * **This marker switches the positive line off.** Its contribution in the
      positive line is zero, so the product is zero there and the classifier
      fires on nothing. Adding such a marker cannot help, at any threshold.
    * **This marker carries no information.** Its contribution is the same in
      every line, so under a relative threshold it is exactly a no-op: it
      multiplies the positive and every negative by the same factor and
      cancels out of every ratio.

    WHAT IS NO LONGER HERE, AND WHY -- READ THIS IF YOU ARE LOOKING FOR THE
    OLD COMPLAINT. The convention complaint used to be made PER MARKER, by
    asking whether flipping that one marker's sense would move the positive
    line closer to the top of that marker's column, and then blaming any
    improvement on the NOT terms being applied twice. On Xie's own Fig. 2D,
    in the correct sensor-output convention with every sense 'high', that
    fired on T142(3p): flipping it lifts the positive line from 0.167 below
    the best negative to 0.149 below, an improvement of 0.018 that leaves
    HeLa losing that column under EITHER sense and therefore fixes nothing.
    It also fired on four of the five leave-one-out subsets of that same
    correct configuration. A gate that fires on four of five correct inputs
    carries no information, and the sentence it printed about a double
    inversion was false every one of those times.

    The per-marker quantity was not worthless -- by leave-one-out margin
    T142(3p) really is the most margin-costly of Fig. 2D's five markers, so
    the marker it named was the right one. The DETECTION was defensible and
    the EXPLANATION was not. That reporting now lives in `marker_utility`,
    which prints the numbers, attaches no cause, and is not a complaint.
    """
    marks = list(markers)
    senses = _canonical_senses(marks, sense)
    lines = _check_table(responses, marks, positive)
    negatives = _negatives(lines, positive)
    out = []
    verdict = convention_check(responses, marks, senses, positive)
    if not verdict.ok:
        out.append(verdict.message)
    for mk in marks:
        declared = senses[mk]
        c_pos = float(sensor_response(responses[positive][mk], declared))
        c_neg = [float(sensor_response(responses[ln][mk], declared))
                 for ln in negatives]
        if c_pos == 0.0:
            out.append(
                f"{mk!r} declared {declared!r} contributes 0.0 in the "
                f"positive line {positive!r}: the product is zero there, so "
                f"the classifier fires on nothing at any threshold.")
        if max(c_neg) - min(c_neg) == 0.0 and c_pos == c_neg[0]:
            out.append(
                f"{mk!r} contributes {c_pos:.4g} in every line, positive and "
                f"negative alike: under a relative threshold it cancels out "
                f"of every ratio and changes no call.")
    return out

class Confusion:
    """Four counts of CELL LINES -- not of cells. T69, and T70 reads it.

    `tp` and `fn` are counts over the one positive line, so they are 0 or 1
    and sensitivity takes two values. `fp` and `tn` are counts over the
    negative lines, six of them in Xie's panel.

    The properties are the usual ratios, and `fp_rate` is the one the session
    turns into a clinical number -- but it is a FRACTION OF CELL LINES in a
    convenience sample, not a per-cell error probability. See
    `fp_rate_upper_bound` for what six clean lines actually establish.
    """

    def __init__(self, tp, fp, tn, fn):
        self.tp, self.fp, self.tn, self.fn = int(tp), int(fp), int(tn), int(fn)

    def as_tuple(self):
        return (self.tp, self.fp, self.tn, self.fn)

    @property
    def n_negative(self):
        return self.fp + self.tn

    @property
    def n_positive(self):
        return self.tp + self.fn

    @property
    def sensitivity(self):
        """TP / (TP + FN). The fraction of positive LINES called."""
        n = self.n_positive
        return float("nan") if n == 0 else self.tp / n

    @property
    def specificity(self):
        """TN / (TN + FP)."""
        n = self.n_negative
        return float("nan") if n == 0 else self.tn / n

    @property
    def fp_rate(self):
        """FP / (FP + TN), a fraction of negative CELL LINES.

        The quantity `wrong_cells_per_dose` wants is a per-CELL rate. This is
        not it, and substituting one for the other is the move the session
        spends its last twenty minutes refusing to make.
        """
        n = self.n_negative
        return float("nan") if n == 0 else self.fp / n

    @property
    def fn_rate(self):
        n = self.n_positive
        return float("nan") if n == 0 else self.fn / n

    def __eq__(self, other):
        if isinstance(other, Confusion):
            return self.as_tuple() == other.as_tuple()
        try:
            return self.as_tuple() == tuple(int(v) for v in other)
        except (TypeError, ValueError):
            return NotImplemented

    def __hash__(self):
        return hash(self.as_tuple())

    def __repr__(self):
        return (f"Confusion(tp={self.tp}, fp={self.fp}, tn={self.tn}, "
                f"fn={self.fn})")


def confusion(responses, markers, sense, positive, threshold, relative=True):
    """TP / FP / TN / FN over the panel, at one threshold. T69.

    `threshold` HAS NO DEFAULT. The session's point is that it is a choice:
    move it and the error rates move, so a classifier is a family indexed by
    it. A default here would hand back one member of that family and hide the
    family.

    `relative=True` (the default, and Xie's own convention) reads `threshold`
    as a FRACTION OF THE POSITIVE LINE'S OUTPUT: a line is called positive
    when its output is at least `threshold * output[positive]`. Fig. 2A's
    caption prints exactly this at 0.20 -- "input combinations that result in
    20% output relative to HeLa cells" -- and dots above that contour are the
    false positives.

    `relative=False` reads `threshold` as an absolute output level in (0, 1].
    It is available because a real device has an absolute actuation
    threshold, and it is NOT the convention the properties hold in: adding a
    marker shrinks every output, the positive's included, so under an
    absolute cut more information can cost you the true positive. Under the
    relative cut it cannot. Be able to say which one a number was computed
    with.

    The comparison is `>=`, so a line sitting exactly on the threshold is
    called POSITIVE. At the boundary some convention has to be picked; this
    one makes the positive line itself a true positive at `threshold = 1.0`,
    where the only cut that is exactly its own output is its own.
    """
    marks = list(markers)
    out = classifier_output(responses, marks, sense)
    lines = _check_table(responses, marks, positive)
    negatives = [ln for ln in lines if ln != positive]
    if not negatives:
        raise ValueError(
            f"the panel holds only {positive!r}. A confusion matrix needs at "
            f"least one negative line; with none, FP and TN are counts over "
            f"an empty set and the specificity is not a number.")
    thr = float(threshold)
    if not np.isfinite(thr) or thr <= 0.0 or thr > 1.0:
        if relative:
            raise ValueError(
                f"a relative threshold is a fraction of the positive line's "
                f"own output and lies in (0, 1]; got {thr}. Above 1 nothing "
                f"clears the cut, the positive line included, which is a "
                f"statement to make rather than a classifier to score.")
        raise ValueError(
            f"an absolute threshold is an output level in (0, 1]; got {thr}. "
            f"Outputs are products of factors in [0, 1], so they cannot "
            f"exceed 1 and a cut above it calls nothing.")
    if relative:
        ref = out[positive]
        if ref <= 0.0:
            raise ValueError(
                f"the positive line {positive!r} has output 0 with these "
                f"markers, so a fraction of it is not a threshold. One of "
                f"your markers contributes zero there -- `sense_check` names "
                f"which. ADDING A MARKER THE POSITIVE LINE LACKS CANNOT "
                f"HELP: it switches the circuit off in the cell you are "
                f"trying to hit.")
        cut = thr * ref
    else:
        cut = thr
    tp = 1 if out[positive] >= cut else 0
    fp = sum(1 for ln in negatives if out[ln] >= cut)
    return Confusion(tp=tp, fp=fp, tn=len(negatives) - fp, fn=1 - tp)


def fp_rate_upper_bound(fp_lines, n_negative, confidence=0.95):
    """What a clean panel actually establishes about the per-cell rate. T70.

    The exact one-sided Clopper-Pearson upper bound on a binomial rate, given
    `fp_lines` false positives out of `n_negative` negative lines. With zero
    false positives it is 1 - (1 - confidence)^(1/n), so

        n = 6   ->  0.393
        n = 20  ->  0.139
        n = 100 ->  0.0295

    SIX CLEAN LINES BOUND THE RATE BELOW ABOUT FORTY PERCENT. That is the
    whole of what "no false positives in the panel" means, and it is why
    `design_to_budget` reports this number next to the one the student
    computed. A design that meets a budget of one wrong cell on the observed
    rate of 0/6 may miss it by five orders of magnitude on this bound, and
    nothing in the panel can tell you which.

    The bound treats the negative lines as independent draws from one
    per-cell rate, which they are not -- they are seven cell lines chosen for
    availability, each assayed in n = 3 experiments. It is therefore an
    OPTIMISTIC bound on a quantity the panel does not measure, and the honest
    reading is as an order of magnitude rather than a number.
    """
    from scipy.stats import beta
    k, n = int(fp_lines), int(n_negative)
    if n < 1:
        raise ValueError("a rate needs at least one negative line")
    if not 0 <= k <= n:
        raise ValueError(
            f"got {k} false positives out of {n} negative lines; a count "
            f"cannot exceed its denominator or fall below zero")
    c = float(confidence)
    if not 0.0 < c < 1.0:
        raise ValueError(f"confidence is a probability in (0, 1); got {c}")
    if k == n:
        return 1.0
    return float(beta.ppf(c, k + 1, n - k))


def wrong_cells_per_dose(fp_rate, treated_population):
    """Cells wrongly acted on, when `treated_population` cells are treated.

    T69, and it is `posb.evolution.escapers_per_dose` with the sign of the
    intent reversed. There: a per-cell escape fraction times 10^8 CFU against
    a budget of one survivor, for a device that must not act. Here: a
    per-cell false-positive rate times a treated population against a budget
    of one wrong cell, for a device that must not act ON THE WRONG CELL. Same
    product, same budget of one, opposite sign -- which is why PS9 opens on
    one and closes on the other.

    Both arguments are the caller's, and neither has a default. `fp_rate` is
    a PER-CELL rate and nothing in a seven-line panel measures one: the panel
    gives a fraction of cell lines, Fig. 3C gives a per-line killing fraction
    for HEK293 with an error bar that is a large part of its mean, and
    Fig. 4B -- the only measurement of the two cell types in ONE DISH -- puts
    about a third of the spared line dying anyway. The treated population is
    the student's number and has to be defended; T69's autograder checks the
    arithmetic and the direction, not the value.

    Linear in both arguments, and vectorized over both.
    """
    r = np.asarray(fp_rate, float)
    n = np.asarray(treated_population, float)
    if np.any(~np.isfinite(r)) or np.any((r < 0.0) | (r > 1.0)):
        raise ValueError(
            f"a per-cell false-positive rate is a probability in [0, 1]; got "
            f"min {float(np.min(r)):.4g}, max {float(np.max(r)):.4g}. A "
            f"fraction of misclassified CELL LINES is not this quantity, "
            f"even though it is also a number in [0, 1].")
    if np.any(~np.isfinite(n)) or np.any(n <= 0.0):
        raise ValueError(
            "a treated population is a positive number of cells; a budget on "
            "a rate only becomes a budget on an event once it is multiplied "
            "by one")
    return r * n


class Design:
    """The result of a search over marker subsets. ALWAYS TRUTHY.

    `found` is the answer; the object is not. A search that meets nothing
    returns this object with `found = False`, the best classifier it did find,
    and a `reason` that says what failed -- deliberately not an exception, and
    deliberately not an empty list or None, because `if design_to_budget(...)`
    reading as "no" is how a failed search gets mistaken for a met budget.
    """

    _FIELDS = ("found", "markers", "threshold", "relative", "fp_lines",
               "fn_lines", "n_negative", "fp_rate", "fp_rate_floor",
               "fp_rate_bound", "wrong_cells", "wrong_cells_bound", "budget",
               "population", "margin", "searched", "viable", "reason")

    def __init__(self, **kw):
        missing = [f for f in self._FIELDS if f not in kw]
        if missing:
            raise TypeError(f"Design is missing {missing}")
        extra = [k for k in kw if k not in self._FIELDS]
        if extra:
            raise TypeError(f"Design got unexpected {extra}")
        for f in self._FIELDS:
            setattr(self, f, kw[f])

    def as_dict(self):
        return {f: getattr(self, f) for f in self._FIELDS}

    def __repr__(self):
        return (f"Design(found={self.found}, markers={list(self.markers)}, "
                f"threshold={self.threshold}, fp_lines={self.fp_lines}, "
                f"wrong_cells={self.wrong_cells})")


def design_to_budget(responses, sense, positive, population, budget=1.0,
                     markers=None, thresholds=(0.1, 0.2, 0.3, 0.5),
                     relative=True, max_markers=None, max_candidates=100000):
    """Search marker subsets and thresholds for a classifier inside a budget.

    T69's closing calculation. Returns a `Design`; read `found`, then
    `reason`, then the numbers.

    WHAT IT DOES. Exhaustively: every non-empty subset of `markers` with at
    most `max_markers` members, crossed with every threshold in `thresholds`.
    For each pair it computes the confusion matrix over the panel, turns the
    false-positive count into a rate by dividing by the number of negative
    lines, multiplies by `population` to get wrong cells, and keeps the
    cheapest pair that calls the positive line AND comes in at or under
    `budget`. Ties are broken toward fewer markers, then toward the larger
    separation between the positive line and its nearest negative.

    A CANDIDATE THAT DOES NOT CALL THE POSITIVE LINE IS NEVER REPORTED AS
    FOUND. A classifier that fires on nothing has a false-positive count of
    zero and meets every budget ever written, and it treats nobody. The
    search therefore requires sensitivity 1 as well as the budget, and says
    so in `reason` when that is what ruled a subset out.

    THE BOUND, WHICH IS THE COMBINATORIAL PART. The search is
    (2^M - 1) x len(thresholds) evaluations, or sum_{k<=max_markers} C(M, k)
    x len(thresholds) when `max_markers` is set. At Xie's M = 5 sensor
    modules and four thresholds that is 124; at M = 20 it is over four
    million and this function refuses rather than runs, because an
    exhaustive search is the only kind it does. There is no greedy mode, no
    forward selection and no regularisation: with six markers the exhaustive
    answer is free, and a greedy answer would be a different object that
    happened to be cheaper. Raise `max_candidates`, or set `max_markers`, and
    be explicit about which.

    WHAT IT CANNOT DO, AND THE NUMBERS ARE IN THE RETURNED OBJECT.

    1. **It cannot measure a per-cell rate.** `fp_rate` is a fraction of
       negative CELL LINES. With six of them the finest nonzero rate the
       panel can express is `fp_rate_floor` = 1/6 = 0.167, and a reported
       zero means "below the panel's resolution", never zero.
       `fp_rate_bound` is the exact one-sided 95% bound on the per-cell rate
       given the counts -- 0.393 for a clean six-line panel -- and
       `wrong_cells_bound` is what that does to the budget. Expect those two
       numbers to disagree by orders of magnitude. That disagreement is T70.
    2. **It cannot see the mixture.** Every response in the table was
       measured in a line on its own. Fig. 4B puts two of them in one dish
       and roughly doubles the false-positive rate the per-line assays
       predict. No search over this table recovers that.
    3. **It cannot choose the population.** `population` has no default
       because it is the designer's claim about a dose of cells, and arguing
       it is the assignment.
    4. **It optimises a count of lines**, so with a small panel many subsets
       tie at zero false positives and the tie-break -- fewest markers --
       is a convention of this function and not a result. Fig. 2C's claim
       that more markers buy selectivity is about MARGIN, not about the
       count; `margin` is reported so the two can be compared.
    """
    marks = list(markers) if markers is not None else sorted(
        {m for row in responses.values() for m in row})
    if not marks:
        raise ValueError("no markers to search over")
    lines = _check_table(responses, marks, positive)
    senses = _canonical_senses(marks, sense)
    negatives = [ln for ln in lines if ln != positive]
    if not negatives:
        raise ValueError(
            f"the panel holds only {positive!r}; a false-positive budget "
            f"needs negative lines to be wrong about")
    thrs = [float(t) for t in thresholds]
    if not thrs:
        raise ValueError(
            "no thresholds to search. A classifier is a family indexed by a "
            "threshold; searching subsets at no threshold searches nothing.")
    pop = float(population)
    if not np.isfinite(pop) or pop <= 0.0:
        raise ValueError(f"a treated population is positive; got {population}")
    bud = float(budget)
    if not np.isfinite(bud) or bud < 0.0:
        raise ValueError(
            f"a budget is a non-negative number of WRONG CELLS; got {budget}. "
            f"The course's budget is one, matching session 23's one escaper "
            f"per dose.")
    m = len(marks)
    kmax = m if max_markers is None else int(max_markers)
    if kmax < 1 or kmax > m:
        raise ValueError(
            f"max_markers must lie in 1..{m}; got {max_markers}")
    n_subsets = sum(math.comb(m, k) for k in range(1, kmax + 1))
    n_cand = n_subsets * len(thrs)
    if n_cand > int(max_candidates):
        raise ValueError(
            f"this search is {n_subsets} subsets x {len(thrs)} thresholds = "
            f"{n_cand} evaluations, past max_candidates={int(max_candidates)}."
            f" The search is EXHAUSTIVE -- 2^M - 1 subsets of M markers -- so "
            f"it grows as 2^M and there is no greedy fallback here. Set "
            f"max_markers to bound the subset size, or raise max_candidates "
            f"deliberately.")

    n_neg = len(negatives)
    floor = 1.0 / n_neg
    searched = viable = 0
    best_ok = best_call = None
    for k in range(1, kmax + 1):
        for subset in itertools.combinations(marks, k):
            out = classifier_output(responses, subset, senses)
            ref = out[positive]
            for thr in thrs:
                searched += 1
                if ref <= 0.0:
                    continue        # the circuit is off in the target cell
                viable += 1
                cut = thr * ref if relative else thr
                tp = 1 if ref >= cut else 0
                fp = sum(1 for ln in negatives if out[ln] >= cut)
                rate = fp / n_neg
                wrong = rate * pop
                margin = 1.0 - max(out[ln] for ln in negatives) / ref
                rec = dict(markers=subset, threshold=thr, fp_lines=fp,
                           fn_lines=1 - tp, fp_rate=rate, wrong_cells=wrong,
                           margin=margin)
                if tp != 1:
                    continue        # calls nothing; never a design
                key = (wrong, k, -margin)
                if best_call is None or key < best_call[0]:
                    best_call = (key, rec)
                if wrong <= bud and (best_ok is None or key < best_ok[0]):
                    best_ok = (key, rec)

    def _finish(found, rec, reason):
        fp = rec["fp_lines"]
        bound = fp_rate_upper_bound(fp, n_neg)
        return Design(
            found=found, markers=tuple(rec["markers"]),
            threshold=rec["threshold"], relative=bool(relative),
            fp_lines=fp, fn_lines=rec["fn_lines"], n_negative=n_neg,
            fp_rate=rec["fp_rate"], fp_rate_floor=floor,
            fp_rate_bound=bound, wrong_cells=rec["wrong_cells"],
            wrong_cells_bound=bound * pop, budget=bud, population=pop,
            margin=rec["margin"], searched=searched, viable=viable,
            reason=reason)

    seen_fp = best_call[1]["fp_lines"] if best_call else 0
    bound = fp_rate_upper_bound(seen_fp, n_neg)
    unresolved = "" if seen_fp else (
        "a reported 0 means below that resolution, not zero, and ")
    resolution = (
        f"CANNOT, and these are not the same question: {n_neg} negative "
        f"lines resolve a per-cell rate no finer than 1/{n_neg} = "
        f"{floor:.4g}, so {unresolved}the exact one-sided 95% bound on the "
        f"per-cell rate is {bound:.4g} -- up to {bound * pop:.4g} wrong "
        f"cells in a population of {pop:.4g}. Every response was also "
        f"measured in a line on its own; Fig. 4B's mixture roughly doubles "
        f"the rate the per-line assays predict.")

    if best_ok is not None:
        rec = best_ok[1]
        return _finish(
            True, rec,
            f"{len(rec['markers'])} markers {list(rec['markers'])} at a "
            f"{'relative' if relative else 'absolute'} threshold of "
            f"{rec['threshold']:.4g} give {rec['fp_lines']}/{n_neg} "
            f"false-positive lines, i.e. {rec['wrong_cells']:.4g} wrong "
            f"cells against a budget of {bud:.4g}, while still calling "
            f"{positive!r}. Searched {searched} candidates. " + resolution)
    if best_call is None:
        rec = dict(markers=(), threshold=float("nan"), fp_lines=0,
                   fn_lines=1, fp_rate=float("nan"),
                   wrong_cells=float("nan"), margin=float("nan"))
        return _finish(
            False, rec,
            f"NO SUBSET MEETS THIS BUDGET, and none even calls {positive!r}: "
            f"of {searched} candidates ({viable} with a non-zero output in "
            f"the positive line) not one clears its own threshold in the "
            f"target cell. Either a marker in the panel contributes zero "
            f"there -- `sense_check` names which -- or the senses are "
            f"inverted. " + resolution)
    rec = best_call[1]
    return _finish(
        False, rec,
        f"NO SUBSET MEETS THIS BUDGET. Of {searched} candidates the best "
        f"classifier that calls {positive!r} is {list(rec['markers'])} at a "
        f"{'relative' if relative else 'absolute'} threshold of "
        f"{rec['threshold']:.4g}, with {rec['fp_lines']}/{n_neg} "
        f"false-positive lines -- {rec['wrong_cells']:.4g} wrong cells "
        f"against a budget of {bud:.4g}, short by a factor of "
        f"{(rec['wrong_cells'] / bud) if bud > 0 else float('inf'):.4g}. "
        f"Lower the population, widen the panel, or say that the budget "
        f"cannot be met with these markers. " + resolution)
