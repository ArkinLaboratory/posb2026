"""The reading-assignment rule, tested.

A checker nobody has watched fail is not a checker. Each test here is a way the
rule gets broken in practice while the file still looks fine.
"""
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.build_readings import (check_load, load, previous_teaching_session,
                                  resolve)


SESSIONS = {
    1: {"n": 1, "date": date(2026, 8, 27)},
    2: {"n": 2, "date": date(2026, 9, 1)},
    3: {"n": 3, "date": date(2026, 9, 3)},
    15: {"n": 15, "date": date(2026, 10, 15), "kind": "exam"},
    16: {"n": 16, "date": date(2026, 10, 20)},
}


def paper(**kw):
    base = {"key": "x", "doi": "10.0/x", "pages": 4, "short": "X et al., 2000",
            "focus": "Figure 2.", "required": True}
    base.update(kw)
    return base


def spec(readings, **limits):
    return {"limits": limits, "readings": readings}


def test_default_assignment_is_the_previous_meeting():
    rows, errors = resolve(spec({"s03": [paper()]}), SESSIONS)
    assert not errors
    assert rows[0]["assign"] == 2 and rows[0]["discuss"] == 3


def test_the_midterm_never_carries_an_assignment():
    # s16 follows the exam, so the default must skip back to s14 -- handing a
    # paper out at the end of a midterm is not a thing that happens.
    assert previous_teaching_session(16, SESSIONS) == 3
    rows, errors = resolve(spec({"s16": [paper()]}), SESSIONS)
    assert any("days between assignment" in e for e in errors), errors


def test_first_session_cannot_assign_backwards():
    _, errors = resolve(spec({"s01": [paper()]}), SESSIONS)
    assert any("no earlier meeting" in e for e in errors), errors


def test_explicit_override_must_precede_the_discussion():
    _, errors = resolve(spec({"s02": [paper(assign_in="s03")]}), SESSIONS)
    assert any("assignment must come first" in e for e in errors), errors


def test_assigning_into_the_exam_is_rejected():
    _, errors = resolve(spec({"s16": [paper(assign_in="s15")]}), SESSIONS)
    assert any("midterm" in e for e in errors), errors


def test_a_reading_must_be_findable_and_specific():
    _, errors = resolve(spec({"s03": [{"key": "y"}]}), SESSIONS)
    assert any("doi or a url" in e for e in errors), errors
    assert any("`focus`" in e for e in errors), errors
    assert any("`short`" in e for e in errors), errors


def test_notice_that_is_too_long_is_an_error_not_a_courtesy():
    _, errors = resolve(spec({"s16": [paper(assign_in="s01")]},
                             max_days_notice=14), SESSIONS)
    assert any("will not remember" in e for e in errors), errors


def test_load_cap_counts_only_required_papers():
    s = spec({"s03": [paper(key="a"), paper(key="b", required=False)]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12)
    rows, errors = resolve(s, SESSIONS)
    assert not errors
    assert not check_load(rows, s)

    s = spec({"s03": [paper(key="a"), paper(key="b")]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12)
    rows, _ = resolve(s, SESSIONS)
    assert any("required papers" in e for e in check_load(rows, s))


def test_page_budget():
    s = spec({"s03": [paper(pages=40)]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12)
    rows, _ = resolve(s, SESSIONS)
    assert any("required pages" in e for e in check_load(rows, s))


def test_the_real_files_are_valid():
    _, sessions, s = load()
    rows, errors = resolve(s, sessions)
    assert not errors + check_load(rows, s)


def test_override_needs_a_reason():
    s = spec({"s03": [paper(key="a"), paper(key="b")]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12,
             overrides={"s02": {"max_required_per_assignment": 2}})
    rows, _ = resolve(s, SESSIONS)
    errors = check_load(rows, s)
    assert not any("required papers" in e for e in errors), errors   # lifted
    assert any("needs a `reason`" in e for e in errors), errors


def test_override_still_enforces_the_page_budget():
    s = spec({"s03": [paper(key="a", pages=8), paper(key="b", pages=8)]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12,
             overrides={"s02": {"max_required_per_assignment": 2,
                                "reason": "two complementary papers"}})
    rows, _ = resolve(s, SESSIONS)
    assert any("required pages" in e for e in check_load(rows, s))


def test_override_applies_only_to_the_session_named():
    # The whole point: s02 may assign two, s01 may not.
    s = spec({"s02": [paper(key="a"), paper(key="b")],
              "s03": [paper(key="c"), paper(key="d")]},
             max_required_per_assignment=1, max_required_pages_per_assignment=12,
             overrides={"s02": {"max_required_per_assignment": 2,
                                "reason": "two complementary papers"}})
    rows, _ = resolve(s, SESSIONS)
    errors = check_load(rows, s)
    assert any(e.startswith("s01 assigns 2") for e in errors), errors
    assert not any(e.startswith("s02 assigns 2") for e in errors), errors


def test_a_dead_override_is_reported():
    s = spec({"s03": [paper()]},
             overrides={"s16": {"max_required_per_assignment": 2,
                                "reason": "stale"}})
    rows, _ = resolve(s, SESSIONS)
    assert any("does nothing" in e for e in check_load(rows, s))
