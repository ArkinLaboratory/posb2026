#!/usr/bin/env python3
"""Check that docs/course-map.md agrees with course.yaml.

Two copies of the calendar exist on purpose: one a table a human reads, one a
file a build reads. Two copies of anything drift. This is the thing that makes
the drift loud instead of silent -- if a date moves in the prose and not in the
data, the reading tracker keeps computing assignments against the old calendar
and nobody finds out until a class period is wasted.

    python tools/check_schedule.py
"""
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "docs" / "course-map.md"
COURSE = ROOT / "course.yaml"

ROW = re.compile(
    r"^\|\s*(\d+|—)\s*\|\s*\*{0,2}([A-Z][a-z]{2}) ([A-Z][a-z]{2}) (\d+)\*{0,2}\s*\|",
    re.M)
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
WEEKDAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def main():
    course = yaml.safe_load(COURSE.read_text())
    year = course["last_class_day"].year
    want = {s["n"]: s["date"] for s in course["sessions"]}
    holidays = {h["date"] for h in course.get("no_class", [])}

    rows = ROW.findall(MAP.read_text())
    if len(rows) < len(want):
        sys.exit(f"course-map.md: parsed {len(rows)} dated rows but course.yaml "
                 f"has {len(want)} sessions. Has the table format changed?")

    errors = []
    seen = set()
    for n, dow, mon, day in rows:
        d = date(year, MONTHS[mon], int(day))
        if WEEKDAY[d.weekday()] != dow:
            errors.append(f"course-map.md: {dow} {mon} {day} {year} is actually "
                          f"a {WEEKDAY[d.weekday()]}")
        if n == "—":
            if d not in holidays:
                errors.append(f"course-map.md: {mon} {day} is marked as no class "
                              f"but course.yaml does not list it in no_class")
            continue
        n = int(n)
        seen.add(n)
        if n not in want:
            errors.append(f"course-map.md: session {n} is not in course.yaml")
        elif want[n] != d:
            errors.append(f"session {n}: course-map.md says {d}, "
                          f"course.yaml says {want[n]}")

    for n in sorted(set(want) - seen):
        errors.append(f"session {n} is in course.yaml but not in course-map.md")

    # every teaching day is a class day
    for s in course["sessions"]:
        if WEEKDAY[s["date"].weekday()] not in ("Tue", "Thu"):
            errors.append(f"session {s['n']} falls on a "
                          f"{WEEKDAY[s['date'].weekday()]}; the course meets TuTh")
        if s["date"] in holidays:
            errors.append(f"session {s['n']} is scheduled on a no-class day")

    if errors:
        print("schedule FAILED:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {len(want)} sessions, course.yaml and docs/course-map.md agree")


if __name__ == "__main__":
    main()
