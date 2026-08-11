#!/usr/bin/env python3
"""Pre-flight check for nbgitpuller distribution links.

Reproduces the checks nbgitpuller itself performs, so three of the four real
failure modes can be caught without a browser:

  * repo not public          -> students see "Problem accessing HEAD branch"
  * branch does not exist    -> students see "Branch: X -- not found in repo"
  * notebook path is wrong   -> pull SUCCEEDS, then JupyterLab says
                                "Could not find path", which students read as
                                "the assignment is missing"

The fourth -- whether the urlpath app prefix renders -- needs one interactive
click. See docs/instructor-setup.md.

IMPORTANT: run this with no GitHub credentials in the environment. Berkeley
DataHub mounts a GitHub App credential helper, so a *private* repo can clone
fine for you and fail for all your students. Unauthenticated is the only
honest test.

Usage:
    python tools/check_links.py                 # check every link it can derive
    python tools/check_links.py <url> [<url>]   # check specific pasted links
"""
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = "https://datahub.berkeley.edu"
REPO = "https://github.com/ArkinLaboratory/posb2026"
BRANCH = "main"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def ok(msg):
    print(f"  {GREEN}PASS{RESET}  {msg}")


def bad(msg, detail=""):
    print(f"  {RED}FAIL{RESET}  {msg}")
    if detail:
        print(f"        {DIM}{detail}{RESET}")


def warn(msg):
    print(f"  {YELLOW}WARN{RESET}  {msg}")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def check_repo_public(repo):
    r = run(["git", "ls-remote", "--heads", "--", repo])
    if r.returncode == 0:
        ok(f"repo is reachable without credentials: {repo}")
        return True
    bad("repo is not reachable unauthenticated -- it may be private",
        "Students will see: Problem accessing HEAD branch")
    return False


def check_branch(repo, branch):
    r = run(["git", "ls-remote", "--heads", "--", repo])
    if r.returncode != 0:
        return False
    if f"refs/heads/{branch}" in r.stdout:
        ok(f"branch exists: {branch}")
        return True
    found = [ln.split("refs/heads/")[-1] for ln in r.stdout.strip().splitlines()]
    bad(f"branch '{branch}' does not exist",
        f"Students will see: Branch: {branch} -- not found in repo. "
        f"Branches present: {', '.join(found)}")
    return False


def check_file(repo, branch, path):
    owner_repo = repo.removeprefix("https://github.com/").removesuffix(".git")
    raw = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{path}"
    try:
        req = urllib.request.Request(raw, method="HEAD")
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status == 200:
                ok(f"file exists on {branch}: {path}")
                return True
    except Exception:
        pass
    bad(f"file not found on {branch}: {path}",
        "Pull will SUCCEED, then JupyterLab shows 'Could not find path'")
    return False


def check_urlpath(urlpath, repo, path):
    """The urlpath must be <app>/<repo-folder>/<path-in-repo>."""
    folder = repo.rstrip("/").split("/")[-1].removesuffix(".git")
    expected_lab = f"lab/tree/{folder}/{path}"
    expected_nb = f"tree/{folder}/{path}"
    if urlpath in (expected_lab, expected_nb):
        ok(f"urlpath includes the clone folder '{folder}'")
        return True
    if f"/{folder}/" not in f"/{urlpath}":
        bad("urlpath is missing the repository folder name -- the most common mistake",
            f"expected: {expected_lab}\n        got:      {urlpath}")
    else:
        warn(f"urlpath differs from the canonical form\n        expected: "
             f"{expected_lab}\n        got:      {urlpath}")
    return False


def check_link(url):
    print(f"\n{url}")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    repo = q.get("repo", [None])[0]
    branch = q.get("branch", [None])[0]
    urlpath = q.get("urlpath", [None])[0]

    if not repo:
        bad("no repo= parameter")
        return False
    if branch is None:
        warn("no branch= parameter. nbgitpuller >=1.1 resolves the default "
             "branch, so this works -- but be explicit.")
        branch = "HEAD"
    if branch == "master":
        warn("branch=master. The Berkeley link-generator extension pre-fills "
             "this and it is wrong for repos whose default branch is 'main'.")

    results = [check_repo_public(repo)]
    if branch != "HEAD":
        results.append(check_branch(repo, branch))
    if urlpath:
        folder = repo.rstrip("/").split("/")[-1].removesuffix(".git")
        after = urlpath.split(f"{folder}/", 1)
        if len(after) == 2 and after[1].endswith(".ipynb"):
            results.append(check_file(repo, branch if branch != "HEAD" else "main",
                                      after[1]))
        results.append(check_urlpath(urlpath, repo,
                                     after[1] if len(after) == 2 else ""))
    else:
        warn("no urlpath= -- students land in the file browser, not the notebook")
    return all(results)


def derive_links():
    """Build the canonical link for every committed notebook."""
    folder = REPO.rstrip("/").split("/")[-1]
    links = []
    for d in ("sessions", "problem-sets"):
        for nb in sorted((ROOT / d).rglob("*.ipynb")):
            if ".ipynb_checkpoints" in str(nb):
                continue
            rel = nb.relative_to(ROOT).as_posix()
            urlpath = f"lab/tree/{folder}/{rel}"
            links.append(
                f"{HUB}/hub/user-redirect/git-pull"
                f"?repo={urllib.parse.quote(REPO, safe='')}"
                f"&urlpath={urllib.parse.quote(urlpath, safe='')}"
                f"&branch={BRANCH}"
            )
    return links


def main():
    links = sys.argv[1:] or derive_links()
    if not sys.argv[1:]:
        print(f"{DIM}No links given; checking the canonical link for every "
              f"committed notebook.{RESET}")
    results = [check_link(u) for u in links]
    print()
    if all(results):
        print(f"{GREEN}All {len(results)} link(s) passed the offline checks.{RESET}")
        print(f"{DIM}Still do one interactive test: in a DataHub terminal run\n"
              f"  rm -rf ~/posb2026\n"
              f"then click a link. Incognito does NOT test this -- you land in "
              f"the same home directory.{RESET}")
    else:
        print(f"{RED}{results.count(False)} of {len(results)} link(s) failed.{RESET}")
        sys.exit(1)

    print("\nLinks (paste into bCourses):")
    for u in links:
        print(f"  {u}")


if __name__ == "__main__":
    main()
