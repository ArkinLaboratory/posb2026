"""The three gates that were prose in a document until something executed them.

Each of these cost a term's worth of damage once:

  * GATE 1. M3's bCourses assignment was copied from M1 and M2 and inherited
    `allowed_extensions: ["pdf"]`. M3 is the first milestone whose deliverable
    includes a code package, and its own Canvas description said so. Four
    students emailed their packages overnight because they could not upload
    them, and the identical defect was waiting on the graded final project.
  * GATE 2. "M3 in Week 12 (due Thu 12 Nov)" was a blockquote in
    docs/session-release-checklist.md. M3's platform state went unexamined
    until two days after its due date.
  * GATE 3. The midterm shipped 25 scored rows into 60 minutes -- 2.4 min/row
    against a declared 3-minute floor -- while a human pilot's per-item timing
    table, in the repository, totalled 58:45 of the 60-minute budget. The row
    count was never checked against it. Class average 45.65%.

What is tested here is the arithmetic and the parsing, not the prose. The
parses are tested against the REAL documents, because a parser tested only
against its own fixtures is how a check starts matching nothing.
"""
import datetime
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import exam_budget as eb              # noqa: E402
from tools import graded_items as gi             # noqa: E402
from tools import preflight                      # noqa: E402

DOT = "·"


# ============================================================ the syllabus ===
def test_syllabus_milestone_table_parses_the_real_file():
    ms = gi.milestones()
    ids = [m.ident for m in ms]
    assert ids == ["M1", "M2", "M3", "M4", "FINAL"], ids
    assert all(m.due is not None for m in ms)
    assert all(m.line for m in ms)


def test_the_two_package_deliverables_are_the_ones_the_syllabus_says():
    """M3 reads '4-5 pp + package'; the Final reads 'under 10 pp + package'.

    Read off the Length column, never a list kept here -- a list here is the
    hardcoding the gate exists to replace.
    """
    pkg = {m.ident for m in gi.milestones() if m.needs_package}
    assert pkg == {"M3", "FINAL"}, pkg


def test_problem_set_table_parses_and_ps0_is_ungraded():
    ps = gi.problem_sets()
    assert [p.ident for p in ps] == [f"PS{i}" for i in range(10)]
    assert ps[0].ident == "PS0" and ps[0].graded is False
    assert all(p.graded for p in ps[1:])
    assert not any(p.needs_package for p in ps)


def test_both_exam_dates_come_off_the_weight_table():
    ex = {e.ident: e.due for e in gi.exams()}
    assert ex["MIDTERM"] == datetime.date(2026, 10, 15)
    assert ex["FINAL-EXAM"] == datetime.date(2026, 12, 16)


def test_every_graded_due_date_falls_on_the_weekday_the_syllabus_claims():
    """course.yaml carries no graded dates, but it does carry the term.

    A 'Thu Nov 12' that is not a Thursday is a typo students read first.
    """
    bad = [(i.ident, i.weekday_claimed, i.due) for i in gi.all_graded()
           if not i.weekday_ok]
    assert bad == []


def test_all_graded_is_in_date_order():
    items = gi.all_graded()
    dues = [i.due for i in items]
    assert dues == sorted(dues)
    assert len(items) == 17, [i.ident for i in items]


@pytest.mark.parametrize("doc, why", [
    ("# nothing here\n\nsome prose.\n", "no table at all"),
    ("| Milestone | Due | Length | Becomes |\n"
     "| M1 | Thu Oct 8 | 1 p | - |\n", "no separator row"),
    ("| Milestone | Due | Length | Becomes |\n|---|---|---|---|\n",
     "header and separator with no body"),
])
def test_a_missing_or_moved_table_raises_instead_of_matching_nothing(doc, why):
    with pytest.raises(gi.SyllabusParseError):
        gi.milestones(doc)


def test_a_renamed_first_column_raises_rather_than_returning_zero_rows():
    doc = ("| Milestone | Due | Length | Becomes |\n|---|---|---|---|\n"
           "| **Stage one** | Thu Oct 8 | 1 p | - |\n")
    with pytest.raises(gi.SyllabusParseError):
        gi.milestones(doc)


# ===================================================== gate 1, the package ===
def _entry(**kw):
    e = {"id": 1, "name": "x", "published": True,
         "submission_types": ["online_upload"], "allowed_extensions": ["pdf"],
         "points_possible": 10}
    e.update(kw)
    return e


def test_pdf_only_is_true_only_for_an_upload_assignment_refusing_all_but_pdf():
    assert gi.pdf_only(_entry()) is True
    assert gi.pdf_only(_entry(allowed_extensions=["pdf", "zip"])) is False
    assert gi.pdf_only(_entry(allowed_extensions=[])) is False
    assert gi.pdf_only(_entry(allowed_extensions=None)) is False
    # Canvas keeps a stale extension list on assignments that take no uploads.
    # Reading it there would invent a defect.
    assert gi.pdf_only(_entry(submission_types=["online_text_entry"])) is False
    assert gi.pdf_only(_entry(allowed_extensions=[".PDF"])) is True


def _manifest(entries, read_at="2026-11-14T00:00:00Z"):
    return {"course_id": 1557313, "read_at": read_at, "assignments": entries}


def _run(check, monkeypatch, tmp_path, manifest):
    """Run one gate against a manifest on disk, and return its report rows."""
    p = tmp_path / "platform-manifest.json"
    if manifest is not None:
        p.write_text(json.dumps(manifest))
    monkeypatch.setattr(gi, "MANIFEST", p)
    rep = preflight.Report()
    check(rep)
    return rep


def _row(rep, needle):
    hits = [r for r in rep.rows if needle in r[1]]
    assert hits, f"no report row mentioning {needle!r} in {[r[1] for r in rep.rows]}"
    return hits[0]


def _full(ids, **over):
    """A manifest entry per milestone, accepting a package where one is asked."""
    out = []
    for n, ident in enumerate(ids, start=100):
        pkg = ident in ("M3", "FINAL")
        out.append(_entry(id=n, name=f"Milestone {ident}", item=ident,
                          allowed_extensions=["pdf", "zip"] if pkg else ["pdf"],
                          **over))
    return out


MILESTONE_IDS = ["M1", "M2", "M3", "M4", "FINAL"]


def test_gate1_fails_when_a_package_deliverable_is_pdf_only(monkeypatch, tmp_path):
    """The M3 defect, reproduced. This is the test that had to exist in October."""
    entries = _full(MILESTONE_IDS)
    m3 = [e for e in entries if e["item"] == "M3"][0]
    m3["allowed_extensions"] = ["pdf"]
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(entries))
    status, what, detail = _row(rep, "M3 asks for a package")
    assert status == preflight.FAIL
    assert "+ package" in detail            # quotes the syllabus side
    assert "'pdf'" in detail or '"pdf"' in detail  # quotes the platform side
    assert rep.blocking


def test_gate1_passes_when_the_package_deliverables_accept_one(monkeypatch,
                                                               tmp_path):
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(_full(MILESTONE_IDS)))
    assert _row(rep, "M3 accepts a package")[0] == preflight.OK
    assert _row(rep, "FINAL accepts a package")[0] == preflight.OK
    assert not rep.blocking


def test_gate1_fails_when_a_milestone_has_no_manifest_entry(monkeypatch,
                                                            tmp_path):
    entries = [e for e in _full(MILESTONE_IDS) if e["item"] != "M3"]
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(entries))
    assert _row(rep, "M3 has no entry")[0] == preflight.FAIL
    assert rep.blocking


def test_gate1_warns_and_does_not_block_when_nothing_has_been_imported(
        monkeypatch, tmp_path):
    """The absent manifest IS the finding. Silence would re-create the defect."""
    rep = _run(preflight.check_platform, monkeypatch, tmp_path, None)
    status, what, detail = _row(rep, "never been imported")
    assert status == preflight.WARN
    assert not rep.blocking
    assert "import_platform_manifest" in detail


def test_gate1_warns_when_the_read_is_older_than_the_staleness_window(
        monkeypatch, tmp_path):
    old = (datetime.datetime.now(datetime.timezone.utc)
           - datetime.timedelta(days=gi.STALE_DAYS + 3)).isoformat()
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(_full(MILESTONE_IDS), read_at=old))
    status, what, detail = _row(rep, "platform manifest read")
    assert status == preflight.WARN
    assert "stopped checking" in detail
    assert not rep.blocking          # stale is a warning, not a block


def test_a_fresh_read_does_not_warn(monkeypatch, tmp_path):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(_full(MILESTONE_IDS), read_at=now))
    assert _row(rep, "platform manifest read")[0] == preflight.OK


def test_gate1_warns_on_an_unpublished_deliverable(monkeypatch, tmp_path):
    rep = _run(preflight.check_platform, monkeypatch, tmp_path,
               _manifest(_full(MILESTONE_IDS, published=False)))
    assert _row(rep, "UNPUBLISHED")[0] == preflight.WARN


def test_a_per_entry_read_at_wins_over_the_file_level_one():
    man = _manifest([_entry(item="M3", read_at="2026-01-02T03:04:05Z")],
                    read_at="2026-11-14T00:00:00Z")
    got = gi.entry_read_at(man["assignments"][0], man)
    assert got.year == 2026 and got.month == 1 and got.day == 2


def test_an_entry_is_matched_by_name_when_it_carries_no_item_field():
    man = _manifest([_entry(id=9, name="Project Milestone M3 — "
                                       "Preliminary Results")])
    m3 = [m for m in gi.milestones() if m.ident == "M3"][0]
    assert gi.match_entry(m3, man)["id"] == 9


def test_the_final_proposal_is_not_matched_to_the_final_exam():
    man = _manifest([_entry(id=7, name="Final exam"),
                     _entry(id=8, name="Final proposal and package")])
    fin = [m for m in gi.milestones() if m.ident == "FINAL"][0]
    assert gi.match_entry(fin, man)["id"] == 8


# ===================================================== gate 2, the horizon ===
def test_gate2_prints_a_row_on_every_run_and_never_blocks(monkeypatch,
                                                          tmp_path):
    rep = _run(preflight.check_graded_soon, monkeypatch, tmp_path, None)
    assert rep.rows, "gate 2 printed nothing; its whole purpose is attention"
    assert not rep.blocking


def test_gate2_flags_an_item_whose_manifest_read_predates_its_creation(
        monkeypatch, tmp_path):
    """The M3 shape: the assignment was created after the last platform read,
    so the entry on file cannot be describing it."""
    soon = [i for i in gi.all_graded() if i.graded and i.due
            and datetime.date.today() <= i.due
            <= datetime.date.today() + datetime.timedelta(days=14)]
    if not soon:
        pytest.skip("nothing graded is due inside the horizon today")
    target = soon[0]
    man = _manifest([_entry(id=5, name=f"{target.ident} thing",
                            item=target.ident,
                            read_at="2026-01-01T00:00:00Z",
                            created_at="2026-06-01T00:00:00Z")])
    rep = _run(preflight.check_graded_soon, monkeypatch, tmp_path, man)
    hits = [r for r in rep.rows if "due within" in r[1]]
    assert hits and hits[0][0] == preflight.WARN
    assert "predates" in hits[0][2]
    assert not rep.blocking


# ======================================================== gate 3, the rows ===
def _rubric(n_rows, pts=4):
    return "\n\n".join(
        f"## A{i} {DOT} a row about something {DOT} {pts} pts\n\n"
        f"Correct: the answer.\n\n- **{pts}** — right\n- **0** — not"
        for i in range(1, n_rows + 1))


def _timing(seconds_each, n):
    rows = "\n".join(f"| A{i} | {seconds_each // 60}:{seconds_each % 60:02d} |"
                     for i in range(1, n + 1))
    return f"# pilot\n\n| item | time |\n|---|---|\n{rows}\n"


def _exam(tmp_path, rows, pilot_total_s=None, date="2026-12-16",
          item_time=120, n_pilot_rows=None, **cfg):
    d = tmp_path / "examdir"
    (d / "reviews").mkdir(parents=True, exist_ok=True)
    (d / "exam.md").write_text("# paper\n")
    (d / "rubric.md").write_text(_rubric(rows))
    conf = {"item_time_minutes": item_time, "date": date}
    conf.update(cfg)
    (d / "budget.json").write_text(json.dumps(conf))
    if pilot_total_s is not None:
        n = n_pilot_rows or rows
        (d / "reviews" / "human-pilot.md").write_text(
            _timing(pilot_total_s // n, n))
    return d


FUTURE = datetime.date(2026, 12, 1)       # before the 16 December sitting


def _sev(res, needle):
    hits = [f for f in res["findings"] if needle in f[1]]
    assert hits, f"nothing about {needle!r} in {[f[1] for f in res['findings']]}"
    return hits[0]


def test_row_count_reproduces_the_midterms_known_25_rows_and_100_points():
    """Cross-checked against private/midterm/marking_sheet.py's SCORED list.

    That file names its 25 labels by hand. This counts any row heading that
    declares points, and must agree -- including skipping the four block
    headings B1, B2, B3 and C1, which declare none.
    """
    rubric = ROOT / "private" / "midterm" / "rubric.md"
    if not rubric.is_file():
        pytest.skip("private/midterm is not present")
    rows = eb.scored_rows(rubric)
    assert len(rows) == 25
    assert sum(p for _, p in rows) == 100
    labels = [lab for lab, _ in rows]
    assert "B1" not in labels and "C1" not in labels
    sys.path.insert(0, str(ROOT / "private" / "midterm"))
    import marking_sheet                                   # noqa: E402
    assert labels == marking_sheet.SCORED


def test_the_real_human_pilot_table_parses_to_its_own_declared_total():
    """Josh's table, by hand, at quarter-minute resolution: 15 items, 58:45."""
    f = ROOT / "private" / "midterm" / "reviews" / "human-pilot-2026-10-12.md"
    if not f.is_file():
        pytest.skip("the human pilot write-up is not present")
    tables = eb.parse_timing_tables(f.read_text(encoding="utf-8"))
    assert len(tables) == 1, "expected exactly one timing table"
    t = tables[0]
    assert len(t["items"]) == 15
    assert sum(t["items"].values()) == 58 * 60 + 45
    assert t["declared_total"] == 58 * 60 + 45
    assert t["items"]["A7"] == 7 * 60 + 30     # bolded in the source
    assert t["items"]["C1"] == 8 * 60 + 30
    assert t["items"]["A3.1"] == 90            # a sub-numbered row


def test_the_midterms_own_arithmetic_is_reproduced_and_does_not_block():
    """25 rows, 2.40 min/row, a pilot at 98% of budget -- and WARN, not FAIL.

    The exam was sat on 15 October. It cannot be fixed, and a permanent FAIL on
    it would train a reader to discount this whole report -- which is what
    preflight's own docstring warns about.
    """
    d = ROOT / "private" / "midterm"
    if not (d / "budget.json").is_file():
        pytest.skip("private/midterm is not present")
    res = eb.assess(d, today=datetime.date(2026, 11, 14))
    assert res["past"] is True
    assert res["rows"] == 25
    assert res["pilots"][0]["total"] == 58 * 60 + 45
    assert round(res["pilots"][0]["fraction"], 3) == 0.979
    assert {f[0] for f in res["findings"]} == {"warn"}
    assert "2.40 min/row" in _sev(res, "min/row")[1]


def test_exam_budget_passes_with_margin_printed(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=90 * 60)      # 75% of 120 min
    res = eb.assess(d, today=FUTURE)
    assert _sev(res, "scored rows")[0] == "pass"
    assert _sev(res, "min/row")[0] == "pass"
    sev, what, detail = _sev(res, "pilot total")
    assert sev == "pass"
    assert "75%" in what
    assert "margin 30:00" in detail          # the margin prints on a pass too


def test_exam_budget_warns_inside_the_85_percent_band(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=108 * 60)     # 90% of 120 min
    res = eb.assess(d, today=FUTURE)
    sev, what, detail = _sev(res, "pilot total")
    assert sev == "warn"
    assert "90%" in what and "85%" in what
    assert "cutting scored skills" in detail


def test_the_85_percent_band_is_exclusive_at_its_edge(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=102 * 60)     # exactly 85%
    res = eb.assess(d, today=FUTURE)
    assert _sev(res, "pilot total")[0] == "pass"


def test_exam_budget_fails_when_a_pilot_total_exceeds_the_budget(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=126 * 60)     # 105% of 120 min
    res = eb.assess(d, today=FUTURE)
    sev, what, detail = _sev(res, "EXCEEDS")
    assert sev == "fail"
    assert "margin -6:00" in detail
    assert "not redundancy" in detail


def test_a_past_exam_reports_the_same_overrun_without_blocking(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=126 * 60, date="2026-10-15")
    res = eb.assess(d, today=FUTURE)
    assert res["past"] is True
    assert _sev(res, "EXCEEDS")[0] == "warn"


def test_too_many_rows_fails_against_the_derived_cap(tmp_path):
    """The cap is minutes over minutes-per-row, never a row count typed in.

    120 minutes at 4.5 min/row is 26 rows. The rule is stated as a rate
    because a row count and a duration can each look defensible while their
    ratio does not.
    """
    d = _exam(tmp_path, rows=30, pilot_total_s=60 * 60)
    res = eb.assess(d, today=FUTURE)
    assert res["config"]["rows_cap"] == 26
    assert res["config"]["rows_cap_derived"] is True
    sev, what, detail = _sev(res, "scored rows")
    assert sev == "fail"
    assert "4 over" in what


def test_an_explicit_rows_cap_overrides_the_derivation(tmp_path):
    d = _exam(tmp_path, rows=30, pilot_total_s=60 * 60, rows_cap=30)
    res = eb.assess(d, today=FUTURE)
    assert res["config"]["rows_cap"] == 30
    assert res["config"]["rows_cap_derived"] is False
    assert _sev(res, "scored rows")[0] == "pass"


def test_the_minutes_per_row_floor_fails_below_three_minutes(tmp_path):
    d = _exam(tmp_path, rows=26, pilot_total_s=60 * 60, item_time=60)
    res = eb.assess(d, today=FUTURE)
    sev, what, detail = _sev(res, "min/row")
    assert sev == "fail"
    assert "2.31 min/row" in what
    assert "+" in detail or "-" in detail          # the margin is printed


def test_the_budget_and_the_cap_are_per_exam_not_the_midterms_numbers(tmp_path):
    d = _exam(tmp_path, rows=26, pilot_total_s=100 * 60, item_time=120,
              target_minutes_per_row=4.0, floor_minutes_per_row=2.0,
              warn_fraction=0.9)
    res = eb.assess(d, today=FUTURE)
    assert res["config"]["rows_cap"] == 30
    assert _sev(res, "scored rows")[0] == "pass"
    assert _sev(res, "pilot total")[0] == "pass"      # 83% under a 90% band


def test_an_exam_with_no_pilot_table_warns_and_says_what_shape_to_ask_for(
        tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=None)
    res = eb.assess(d, today=FUTURE)
    sev, what, detail = _sev(res, "no pilot timing table")
    assert sev == "warn"
    assert "quarter-minute" in detail
    assert "human-pilot-2026-10-12" in detail


def test_a_timing_table_whose_own_total_disagrees_is_reported(tmp_path):
    d = _exam(tmp_path, rows=10, pilot_total_s=60 * 60)
    f = d / "reviews" / "human-pilot.md"
    f.write_text(f.read_text() + "| **TOTAL** | 90:00 |\n")
    res = eb.assess(d, today=FUTURE)
    assert _sev(res, "does not add up")[0] == "warn"


def test_a_missing_budget_json_is_an_error_not_a_silent_pass(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=60 * 60)
    (d / "budget.json").unlink()
    with pytest.raises(eb.ExamConfigError):
        eb.assess(d, today=FUTURE)


def test_a_misspelled_config_key_is_refused(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=60 * 60)
    (d / "budget.json").write_text(json.dumps(
        {"item_time_minutes": 120, "warn_fracton": 0.85}))
    with pytest.raises(eb.ExamConfigError):
        eb.assess(d, today=FUTURE)


def test_item_time_minutes_has_no_default(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=60 * 60)
    (d / "budget.json").write_text(json.dumps({"date": "2026-12-16"}))
    with pytest.raises(eb.ExamConfigError):
        eb.assess(d, today=FUTURE)


def test_no_exam_directory_is_silence_not_a_crash(tmp_path):
    """private/final/ does not exist yet. The gate must not invent a failure."""
    assert eb.exam_dirs(tmp_path) == []
    rep = preflight.Report()
    preflight.check_exam_budget(rep)          # against the real repo
    assert not rep.blocking                   # the midterm is past; nothing blocks


def test_an_exam_directory_is_discovered_by_its_paper(tmp_path):
    d = _exam(tmp_path, rows=20, pilot_total_s=60 * 60)
    assert [n for n, _ in eb.exam_dirs(tmp_path)] == [d.name]


def test_mmss_formats_a_negative_margin():
    assert eb.mmss(-360) == "-6:00"
    assert eb.mmss(58 * 60 + 45) == "58:45"


# ============================================================== the wiring ===
def test_all_three_gates_run_on_every_invocation():
    """They are repo-wide and cheap -- file reads, no subprocess.

    A gate you have to remember a flag for is a gate that is not on when it
    matters, which is how all three of these came to be needed.
    """
    import inspect
    src = inspect.getsource(preflight.main)
    for fn in ("check_platform", "check_graded_soon", "check_exam_budget"):
        assert fn in src, f"{fn} is not dispatched from main()"
