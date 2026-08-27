#!/usr/bin/env python3
"""Where the course build actually stands, derived from the repository.

    python tools/status.py              # human-readable
    python tools/status.py --json       # machine-readable, for a dashboard
    python tools/status.py --md > ../2026/STATUS.md

## Why this exists

A hand-maintained status document is wrong within a week and nobody can tell by
looking at it. Everything here is *derived*: which sessions have a plan, a deck,
figures, a handout, a notebook, a demo; which problem sets exist and which have
an autograder; how many tests there are; whether the working tree is clean and
pushed; whether every documentation link resolves. None of it can drift, because
none of it is typed.

What is NOT derivable -- decisions, reasoning, what to do next -- belongs in
`2026/SESSION-LOG.md`, which is written by hand on purpose.

Run this at the START of any working session. It is the ground truth that a
conversation should be built on rather than a remembered summary.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ["plan", "deck", "figures", "handout", "notebook", "demo"]
# Two-letter codes, because deck and demo both start "de" and a colliding
# column header in a status table is worse than no header at all.
CODE = {"plan": "PL", "deck": "DK", "figures": "FG",
        "handout": "HO", "notebook": "NB", "demo": "DM"}


def git(*args, cwd=ROOT):
    """Always --no-optional-locks: a plain `git status` through the Cowork
    bridge leaves .git/index.lock behind and blocks the next real commit."""
    try:
        r = subprocess.run(["git", "--no-optional-locks", *args], cwd=cwd,
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip()
    except Exception:
        return ""


def nums(paths):
    out = set()
    for p in paths:
        m = re.search(r"[sd](\d\d)", p.name)
        if m:
            out.add(int(m.group(1)))
    return out


def collect():
    cal = yaml.safe_load((ROOT / "course.yaml").read_text())
    built = {
        "plan": nums(p for p in (ROOT / "sessions").glob("s*") if p.is_dir()),
        "deck": nums((ROOT / "decks").glob("s*.py")),
        "figures": nums((ROOT / "figures").glob("s*.py")),
        "handout": nums((ROOT / "handouts").glob("s*.md")),
        "notebook": nums((ROOT / "sessions").glob("s*/*.ipynb")),
        "demo": nums(p for p in (ROOT / "demos").glob("d*") if p.is_dir()),
    }
    today = date.today()
    sessions = []
    for s in cal["sessions"]:
        n = s["n"]
        sessions.append({
            "n": n, "date": str(s["date"]), "title": s["title"],
            "part": s.get("part", ""), "kind": s.get("kind", "session"),
            "past": s["date"] < today,
            **{a: n in built[a] for a in ASSETS},
        })

    upcoming = [s for s in sessions if not s["past"]]
    ps = sorted(p.name for p in (ROOT / "problem-sets").glob("ps*") if p.is_dir())
    graders = sorted(p.name for p in (ROOT / "private" / "build").glob("ps*")) \
        if (ROOT / "private" / "build").is_dir() else []

    tests = sum(len(re.findall(r"^def test", p.read_text(), re.M))
                for p in (ROOT / "tests").glob("test_*.py"))
    package = sum(len(p.read_text().splitlines())
                  for p in (ROOT / "posb").glob("*.py"))

    # readings.yaml is keyed by session ("s09": [...]), not a flat list.
    by_session = yaml.safe_load((ROOT / "readings.yaml").read_text()).get("readings") or {}
    read_sessions = {k for k, v in by_session.items() if v}
    n_readings = sum(len(v) for v in by_session.values() if v)

    links = subprocess.run([sys.executable, str(ROOT / "tools" / "check_doc_links.py"),
                            "--strict"], capture_output=True, text=True)

    return {
        "as_of": str(today),
        "sessions": sessions,
        "next_session": upcoming[0] if upcoming else None,
        "counts": {a: len(built[a]) for a in ASSETS},
        "total_sessions": len(sessions),
        "problem_sets": ps,
        "autograders": graders,
        "tests": tests,
        "package_lines": package,
        "readings_declared": n_readings,
        "sessions_with_readings": len(read_sessions),
        "links_ok": links.returncode == 0,
        "links_report": links.stdout.strip().splitlines()[-1] if links.stdout else "",
        "git": {
            "head": git("--no-pager", "log", "--oneline", "-1"),
            "dirty": [l for l in git("status", "--porcelain").splitlines() if l],
            "unpushed": len([l for l in git("--no-pager", "log", "--oneline",
                                            "origin/main..HEAD").splitlines() if l]),
        },
        "private_git": {
            "head": git("--no-pager", "log", "--oneline", "-1", cwd=ROOT / "private"),
            "dirty": len([l for l in git("status", "--porcelain",
                                         cwd=ROOT / "private").splitlines() if l]),
        },
    }


def human(d):
    out = []
    a = out.append
    a(f"PoSB build status — {d['as_of']}")
    a("=" * 62)
    n = d["next_session"]
    if n:
        have = [k for k in ASSETS if n[k]]
        a(f"NEXT: session {n['n']}, {n['date']} — {n['title']}")
        a(f"      has: {', '.join(have) if have else 'NOTHING YET'}")
    a("")
    c, tot = d["counts"], d["total_sessions"]
    a(f"plans {c['plan']}/{tot}   decks {c['deck']}   figures {c['figures']}   "
      f"handouts {c['handout']}   notebooks {c['notebook']}   demos {c['demo']}")
    a(f"problem sets {len(d['problem_sets'])}/10   autograders {len(d['autograders'])}   "
      f"tests {d['tests']}   posb {d['package_lines']} lines")
    a(f"readings declared {d['readings_declared']} across "
      f"{d['sessions_with_readings']} session(s)")
    a("")
    a(f"{'#':>3} {'date':<11} {'title':<44} " + " ".join(CODE[k] for k in ASSETS))
    for s in d["sessions"]:
        row = " ".join((" X" if s[k] else "  ") for k in ASSETS)
        mark = "·" if s["past"] else (">" if n and s["n"] == n["n"] else " ")
        a(f"{s['n']:>3}{mark}{s['date']:<11} {s['title'][:43]:<44} {row}")
    a("")
    g = d["git"]
    a(f"git   {g['head']}")
    a(f"      {len(g['dirty'])} uncommitted, {g['unpushed']} unpushed")
    for l in g["dirty"][:8]:
        a(f"        {l}")
    a(f"private  {d['private_git']['head']}  ({d['private_git']['dirty']} uncommitted)")
    a(f"links {'OK — every target committed' if d['links_ok'] else 'PROBLEMS: ' + d['links_report']}")
    return "\n".join(out)


def markdown(d):
    c, tot = d["counts"], d["total_sessions"]
    n = d["next_session"]
    L = [f"# Build status — {d['as_of']}", "",
         "*Generated by `tools/status.py`. Do not edit: every number here is derived",
         "from the repository, which is the only way it stays true. Decisions and",
         "reasoning live in `SESSION-LOG.md`, which is written by hand on purpose.*", ""]
    if n:
        have = [k for k in ASSETS if n[k]]
        L += [f"**Next: session {n['n']}, {n['date']} — {n['title']}**  ",
              f"Has: {', '.join(have) if have else '**nothing yet**'}", ""]
    L += ["| | |", "|---|---|",
          f"| Sessions with a plan | **{c['plan']} / {tot}** |",
          f"| Decks · figures · handouts | {c['deck']} · {c['figures']} · {c['handout']} |",
          f"| Notebooks · demos | {c['notebook']} · {c['demo']} |",
          f"| Problem sets · autograders | {len(d['problem_sets'])} / 10 · {len(d['autograders'])} |",
          f"| Tests | {d['tests']} |",
          f"| `posb` package | {d['package_lines']} lines |",
          f"| Readings declared | {d['readings_declared']} across {d['sessions_with_readings']} session(s) |",
          f"| Doc links | {'all resolve, all committed' if d['links_ok'] else '**' + d['links_report'] + '**'} |",
          f"| Repo | `{d['git']['head']}` — {len(d['git']['dirty'])} uncommitted, {d['git']['unpushed']} unpushed |",
          f"| Private repo | `{d['private_git']['head']}` — {d['private_git']['dirty']} uncommitted |",
          "", "## Sessions", "",
          "| # | Date | Session | " + " | ".join(a.title() for a in ASSETS) + " |",
          "|---|---|---|" + "---|" * len(ASSETS)]
    for s in d["sessions"]:
        cells = " | ".join("●" if s[a] else "○" for a in ASSETS)
        t = f"*{s['title']}*" if s["kind"] == "exam" else s["title"]
        L.append(f"| {s['n']} | {s['date'][5:]} | {t} | {cells} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()
    data = collect()
    print(json.dumps(data, indent=2) if args.json
          else markdown(data) if args.md else human(data))
