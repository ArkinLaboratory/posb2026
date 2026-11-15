#!/usr/bin/env python3
"""The graded items the repo already knows, and the platform state beside them.

WHY THIS EXISTS
On 12 November the bCourses assignment for milestone M3 was created by copying
M1 and M2, which carried `allowed_extensions: ["pdf"]`. M3 is the first
milestone that asks for a code package. Its own Canvas description read "Four
to five pages, PDF, plus the first version of your package" while its upload
settings refused anything but PDF. Nineteen students submitted write-ups; four
emailed their packages overnight because they could not upload them. The same
defect was then found waiting on the graded final project assignment, due
14 December.

Both halves of that failure were knowable without a network. The syllabus says
M3's deliverable includes a package. The platform said pdf-only. Nothing in the
repository held both facts at once, so nothing could compare them.

THE TWO HALVES
`preflight.py` runs locally with no Canvas credentials and no network, so the
platform state has to be IMPORTED TO DISK by something that can and checked
locally afterwards. `tools/import_platform_manifest.py` does the importing --
it takes a JSON blob a browser session fetched and writes
`private/platform-manifest.json`. This module does the reading and the
matching. Neither talks to Canvas.

WHAT IS AUTHORITATIVE FOR A DUE DATE
`course.yaml` is the source of truth for which session is on which day and it
carries NO graded due dates at all -- not a milestone, not a problem set, not
the exams. `docs/syllabus.md` carries all three, in three tables, and it is
also the document students are held to. So the syllabus is authoritative here,
and course.yaml is used for exactly two things: to resolve the calendar year a
bare "Thu Nov 12" means, and to cross-check that a date the syllabus claims is
a Thursday really is one. A disagreement between them is a finding, not a
tiebreak.

THE PARSE FAILS LOUDLY
A table parse that silently matches nothing is the same defect one level up: a
check that has stopped checking while still reporting green. Every entry point
here raises SyllabusParseError when a table it expects is missing or yields no
rows, and the caller is expected to surface that as a blocking failure rather
than an empty list.
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYLLABUS = ROOT / "docs" / "syllabus.md"
MANIFEST = ROOT / "private" / "platform-manifest.json"

# How old a platform read may be before it stops being evidence. Two weeks is
# one milestone-to-milestone gap in this course: anything longer and an
# assignment can have been created, copied and gone wrong entirely inside the
# window the manifest claims to describe.
STALE_DAYS = 14

_MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}
_WEEKDAYS = {d: i for i, d in enumerate(
    ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
     "sunday"])}


class SyllabusParseError(RuntimeError):
    """The syllabus did not contain a table this module requires."""


class GradedItem:
    """One graded thing with a due date, as the syllabus states it.

    `ident` is the stable handle a manifest entry is matched against: M1..M4
    for the milestones, FINAL for the graded final proposal and package, PS0..
    PS9 for the problem sets, MIDTERM and FINAL-EXAM for the two sittings.
    """

    def __init__(self, ident, kind, title, due, length="", graded=True,
                 line=None, weekday_claimed=None):
        self.ident = ident
        self.kind = kind                  # milestone | final-proposal | ps | exam
        self.title = title
        self.due = due                    # datetime.date
        self.length = length
        self.graded = graded
        self.line = line                  # 1-based line in docs/syllabus.md
        self.weekday_claimed = weekday_claimed

    @property
    def needs_package(self):
        """Does the syllabus's own Length column say a package is handed in?

        This is the whole of gate 1's left-hand side. It is read off the
        syllabus rather than kept in a list here, because a list here is the
        hardcoding the gate exists to replace.
        """
        return "package" in (self.length or "").lower()

    @property
    def weekday_ok(self):
        if self.weekday_claimed is None or self.due is None:
            return True
        return _WEEKDAYS.get(self.weekday_claimed.lower()) == self.due.weekday()

    def __repr__(self):
        return (f"GradedItem({self.ident!r}, due={self.due}, "
                f"length={self.length!r}, package={self.needs_package})")


# ------------------------------------------------------------------ dates ---
def _term_years():
    """(year for Aug-Dec, year for Jan-Jul) from course.yaml's own term bounds."""
    from tools.schedule import course
    c = course()
    first, last = c["first_instruction_day"], c["last_class_day"]
    return first.year, last.year


def _parse_date(cell):
    """'Thu Oct 8' / '**Mon Dec 14**' / 'Wednesday, December 16' -> (date, weekday).

    Returns (None, None) when the cell carries no date at all -- a dash, an
    em-dash, 'TBD'. Raises nothing: an unparseable date on a row that should
    have one is the caller's finding to report, not this function's to guess.
    """
    txt = re.sub(r"[*_`]", "", cell).strip()
    wd = re.match(r"\s*(mon|tues?|wed(?:nes)?|thur?s?|fri|sat|sun)[a-z]*\b[,.]?\s*",
                  txt, re.I)
    weekday = None
    if wd:
        stem = wd.group(1).lower()
        for full in _WEEKDAYS:
            if full.startswith(stem[:3]):
                weekday = full
                break
        txt = txt[wd.end():]
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2})", txt.strip())
    if not m:
        return None, None
    mon = m.group(1).lower()
    month = next((v for k, v in _MONTHS.items() if k.startswith(mon[:3])), None)
    if month is None:
        return None, None
    fall_year, spring_year = _term_years()
    year = fall_year if month >= 8 else spring_year
    try:
        return datetime.date(year, month, int(m.group(2))), weekday
    except ValueError:
        return None, None


# ------------------------------------------------------------------ table ---
def _table_rows(text, header_pattern, what):
    """Body rows of the first markdown table whose header matches.

    Each row comes back as a list of cell strings. Raises when the header is
    not found or the table has no body rows, because both mean this module is
    reading a document that has moved and is about to report green on nothing.
    """
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("|") and re.search(header_pattern, ln, re.I):
            start = i
            break
    if start is None:
        raise SyllabusParseError(
            f"{what}: no table header matching {header_pattern!r} in "
            f"{SYLLABUS.relative_to(ROOT)} -- the table has moved or been "
            f"renamed, and this check is reading nothing")
    if start + 1 >= len(lines) or not re.match(r"\s*\|[\s|:-]+\|?\s*$",
                                               lines[start + 1]):
        raise SyllabusParseError(
            f"{what}: the line after the header at {SYLLABUS.name}:{start+1} "
            f"is not a markdown separator row")
    out = []
    for j in range(start + 2, len(lines)):
        ln = lines[j]
        if not ln.lstrip().startswith("|"):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        out.append((j + 1, cells))
    if not out:
        raise SyllabusParseError(
            f"{what}: the table at {SYLLABUS.name}:{start+1} has no body rows")
    return out


def milestones(text=None):
    """M1-M4 and the graded final proposal, from the syllabus milestone table."""
    text = SYLLABUS.read_text(encoding="utf-8") if text is None else text
    rows = _table_rows(text, r"\|\s*Milestone\s*\|\s*Due\s*\|\s*Length\s*\|",
                       "milestone table")
    items = []
    for line, cells in rows:
        if len(cells) < 3:
            continue
        name = re.sub(r"[*_`]", "", cells[0]).strip()
        if not name or set(name) <= {"-", "—", "–"}:
            continue
        due, weekday = _parse_date(cells[1])
        m = re.match(r"(M[1-9])\b", name)
        if m:
            ident, kind = m.group(1), "milestone"
        elif "final" in name.lower():
            ident, kind = "FINAL", "final-proposal"
        else:
            continue
        items.append(GradedItem(ident, kind, name, due, cells[2],
                                line=line, weekday_claimed=weekday))
    if not items:
        raise SyllabusParseError(
            "milestone table: parsed 0 milestones -- the first column no "
            "longer looks like '**M1 · ...**' or '**Final proposal...**'")
    return items


def problem_sets(text=None):
    """PS0-PS9 from the syllabus problem-set table. PS0 comes back graded=False."""
    text = SYLLABUS.read_text(encoding="utf-8") if text is None else text
    rows = _table_rows(text, r"\|\s*Set\s*\|\s*Out\s*\|\s*Due\s*\|",
                       "problem-set table")
    items = []
    for line, cells in rows:
        if len(cells) < 3:
            continue
        ident = re.sub(r"[*_`\s]", "", cells[0]).upper()
        if not re.fullmatch(r"PS\d+", ident):
            continue                      # the '| --- | --- | --- | *Midterm*' row
        due, weekday = _parse_date(cells[2])
        covers = cells[3] if len(cells) > 3 else ""
        items.append(GradedItem(ident, "ps", ident, due, "",
                                graded="ungraded" not in covers.lower(),
                                line=line, weekday_claimed=weekday))
    if not items:
        raise SyllabusParseError("problem-set table: parsed 0 sets")
    return items


def exams(text=None):
    """The midterm and the final exam, with their dates, from the weight table.

    The dates live in the weight table's own row labels -- "Midterm --
    Thursday, October 15, in class" -- which is the only machine-readable
    statement of them in the repository. course.yaml marks session 15 as
    `kind: exam` but gives the final exam no row at all, because it is not a
    class meeting.
    """
    text = SYLLABUS.read_text(encoding="utf-8") if text is None else text
    rows = _table_rows(text, r"\|\s*Component\s*\|\s*Weight\s*\|", "weight table")
    items = []
    for line, cells in rows:
        label = re.sub(r"[*_`]", "", cells[0]).strip()
        m = re.match(r"(Midterm|Final exam)\s*[—–-]\s*(.+)", label, re.I)
        if not m:
            continue
        ident = "MIDTERM" if m.group(1).lower() == "midterm" else "FINAL-EXAM"
        due, weekday = _parse_date(m.group(2))
        items.append(GradedItem(ident, "exam", label, due, "",
                                line=line, weekday_claimed=weekday))
    if not items:
        raise SyllabusParseError("weight table: parsed no exam rows")
    return items


def all_graded(text=None):
    """Everything with a due date, in date order. Milestones, sets, exams."""
    text = SYLLABUS.read_text(encoding="utf-8") if text is None else text
    items = milestones(text) + problem_sets(text) + exams(text)
    return sorted(items, key=lambda i: (i.due or datetime.date.max, i.ident))


# --------------------------------------------------------------- manifest ---
def rel(p):
    """Path as written in the repo, whether it came in absolute or relative.

    The manifest path is monkeypatchable (the tests point it at a temp file),
    so a bare relative_to(ROOT) here would raise on a path from outside the
    repository -- turning a report line into a crash.
    """
    p = Path(p)
    try:
        return p.resolve().relative_to(ROOT)
    except ValueError:
        return p


def load_manifest(path=None):
    """The imported platform state, or None when it has never been imported."""
    p = Path(path) if path else MANIFEST
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _utc(stamp):
    if not stamp:
        return None
    s = str(stamp).strip().replace("Z", "+00:00")
    try:
        d = datetime.datetime.fromisoformat(s)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc)


def entry_read_at(entry, manifest=None):
    """When this entry was last read from the platform, UTC.

    Per-entry `read_at` wins; the file-level `read_at` is the fallback, so a
    manifest written in one pull does not need the stamp repeated on every row.
    """
    return _utc(entry.get("read_at")) or _utc((manifest or {}).get("read_at"))


def match_entry(item, manifest):
    """The manifest entry for a graded item, or None.

    Three ways, in order of how much a human had to get right:

      1. an explicit `"item": "M3"` on the entry -- set by hand or by the
         importer's own guess, and the only one that cannot be fooled by a
         rename;
      2. the assignment name carrying the identifier (`\\bM3\\b`, `PS8`,
         `Problem Set 8`);
      3. for the graded final proposal, a name with both "final" and one of
         proposal/project/package -- which is how it is actually named on
         bCourses and is distinguishable from the final EXAM only by that.

    A miss is reported by the caller as a missing entry, which is a blocking
    failure. Guessing harder here would convert a loud miss into a quiet
    mismatch, which is the defect that produced this module.
    """
    entries = (manifest or {}).get("assignments") or []
    want = item.ident.upper()
    for e in entries:
        if str(e.get("item", "")).strip().upper() == want:
            return e
    for e in entries:
        name = str(e.get("name", ""))
        if item.kind == "milestone" and re.search(rf"\b{item.ident}\b", name, re.I):
            return e
        if item.kind == "ps":
            n = item.ident[2:]
            if re.search(rf"\b(?:PS|problem\s+set)\s*0*{n}\b", name, re.I):
                return e
        if item.kind == "final-proposal":
            if (re.search(r"\bfinal\b", name, re.I)
                    and re.search(r"propos|project|package", name, re.I)
                    and not re.search(r"\bexam\b", name, re.I)):
                return e
        if item.kind == "exam":
            if want == "FINAL-EXAM" and re.search(r"final\s+exam", name, re.I):
                return e
            if want == "MIDTERM" and re.search(r"\bmidterm\b", name, re.I):
                return e
    return None


def pdf_only(entry):
    """Does this entry refuse everything but PDF?

    `allowed_extensions` is only meaningful when `online_upload` is among the
    submission types; Canvas keeps a stale list on assignments that no longer
    take uploads, and reading it there would invent a defect.
    """
    types = [str(t).lower() for t in (entry.get("submission_types") or [])]
    if "online_upload" not in types:
        return False
    ext = [str(x).lower().lstrip(".") for x in (entry.get("allowed_extensions") or [])]
    return ext == ["pdf"]
