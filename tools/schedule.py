"""Read course.yaml and readings.yaml. One loader, so there is one calendar.

Imported by tools/build_readings.py, tools/check_schedule.py and decks/theme.py.
Nothing here does any work beyond parsing and caching -- the rule about when a
paper is assigned lives in build_readings.py, and lives there once.
"""
from datetime import date
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COURSE_YAML = ROOT / "course.yaml"
READINGS_YAML = ROOT / "readings.yaml"


@lru_cache(maxsize=1)
def course():
    c = yaml.safe_load(COURSE_YAML.read_text())
    for s in c["sessions"]:
        if not isinstance(s["date"], date):
            raise ValueError(f"course.yaml: session {s['n']} date is not a date "
                             f"({s['date']!r}) -- write it unquoted, 2026-09-24")
    return c


@lru_cache(maxsize=1)
def sessions():
    """{session number: session dict}."""
    return {s["n"]: s for s in course()["sessions"]}


def session_date(n):
    try:
        return sessions()[n]["date"]
    except KeyError:
        raise KeyError(f"no session {n} in course.yaml") from None


@lru_cache(maxsize=1)
def readings_spec():
    return yaml.safe_load(READINGS_YAML.read_text()) or {}


def sid(n):
    return f"s{n:02d}"


def num(key):
    """'s09' -> 9. Raises on anything else, loudly."""
    if not (isinstance(key, str) and key.startswith("s") and key[1:].isdigit()):
        raise ValueError(f"session key must look like 's09', got {key!r}")
    return int(key[1:])
