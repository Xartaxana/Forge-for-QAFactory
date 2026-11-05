"""prepare_copy: a run copy starts with NO story of the ticket (t-172 C1, B-231), at the commit asked for
(F-cmp2-5), in an environment that is PROVED, not assumed (F-cmp2-19).

    python -B experiments/measurers/test_prepare_copy.py
    python -m pytest experiments/measurers/test_prepare_copy.py -q

the live repository's HEAD TRACKS artifacts/PROJ-1 (pipeline.json included), so a copy made with
`git worktree add HEAD` already holds a story: `story_run` skips S0 for it, never reads `--skip-sources`, and
the old manifest that cites the excluded merge request stays in work/. The removal runs inside the COPY only.

Everything here happens in throwaway repositories under the OS temp folder: a stand-in "live" checkout with
the story tracked, and a real `git worktree` of it as the copy. Poetry is never run: the toolchain step takes
its subprocess runner as an argument and the tests hand it a stub. Nothing touches a real checkout.

Each `test_*` below is one group of checks; run as a script they all run and the exit code is the sum, run by
pytest each is one test (the script style this file had before called `sys.exit` at import, which pytest
reports as an internal error).
"""
import contextlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_copy  # noqa: E402

prepare_copy.paths.COPY_PREFIX = "copy-"      # the copy prefix of a synthetic runs table: main() names copies by it

TICKET = "PROJ-1"
fails = 0
total = 0


def check(name, ok, detail=""):
    global fails, total
    total += 1
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" - {detail}"))
    fails += 0 if ok else 1
    return ok


def git(repo, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env, timeout=60)
    assert done.returncode == 0, (args, done.stderr)
    return done.stdout.strip()


def force_rmtree(path):
    def force(func, target, _info):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=force)
    else:
        shutil.rmtree(path, onerror=force)


def remove_worktrees(live, *copies):
    for copy in copies:
        try:
            git(live, "worktree", "remove", "--force", str(copy))
        except Exception:
            pass


def test_prepare_copy_removes_story():
    start = fails
    base = Path(tempfile.mkdtemp(prefix="qa-prepare-copy-"))
    try:
        live = base / "live-repo"
        live.mkdir()
        git(live, "init", "-q")
        harness = live / "test-harness" / "qa-factory"
        for ticket in (TICKET, "PROJ-2"):
            for name in ("pipeline.json", "work/context-manifest.json", "work/source-inventory.json"):
                target = harness / "artifacts" / ticket / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('{"ticket": "%s"}' % ticket, encoding="utf-8")
        (harness / "config.json").write_text("{}", encoding="utf-8")
        git(live, "add", "-A")
        git(live, "commit", "-q", "-m", "tracks the earlier run of the story")
        copy = base / "copy-sample"
        git(live, "worktree", "add", "--detach", str(copy), "HEAD")
        tracked = git(copy, "ls-files", "--", f"test-harness/qa-factory/artifacts/{TICKET}").splitlines()
        check("the fixture: the copy HOLDS the story (tracked, pipeline.json included)",
              any(line.endswith("pipeline.json") for line in tracked) and len(tracked) == 3, str(tracked))
        # the tracked files of a worktree can be read-only on Windows: the removal must not stop there
        os.chmod(copy / "test-harness" / "qa-factory" / "artifacts" / TICKET / "pipeline.json", stat.S_IREAD)

        line = prepare_copy.remove_story_artifacts(copy, TICKET, live_repo=live)
        print("prepare_copy printed: " + line)
        check("prepare_copy_removes_story: artifacts/<T> is gone from the COPY",
              not (copy / "test-harness" / "qa-factory" / "artifacts" / TICKET).exists())
        check("and it says so, with the number of files", line.startswith(f"removed artifacts/{TICKET} from the copy (3 files"), line)
        check("the other story of the copy is untouched",
              (copy / "test-harness" / "qa-factory" / "artifacts" / "PROJ-2" / "pipeline.json").is_file())
        check("the LIVE checkout is never touched (every file of both stories is still there, byte for byte)",
              all((harness / "artifacts" / t / n).read_text(encoding="utf-8") == '{"ticket": "%s"}' % t
                  for t in (TICKET, "PROJ-2") for n in ("pipeline.json", "work/context-manifest.json", "work/source-inventory.json")))
        check("and git sees the copy's removal as the copy's own uncommitted change, not the live repo's",
              git(live, "status", "--porcelain") == "" and "artifacts/" + TICKET in git(copy, "status", "--porcelain"))

        # nothing tracked / present for the ticket: nothing removed, one line
        again = prepare_copy.remove_story_artifacts(copy, TICKET, live_repo=live)
        check("a second call: nothing to remove, ONE line, no error", again == f"artifacts/{TICKET} is not in the copy: nothing removed", again)
        none = prepare_copy.remove_story_artifacts(copy, "PROJ-99999", live_repo=live)
        check("a ticket the copy does not hold: nothing removed, one line", "nothing removed" in none and "\n" not in none, none)

        # edges: the ticket that is not a ticket, and the path that leaves the copy
        for label, ticket in (("the placeholder of the usage line", "<TICKET>"), ("empty", ""), ("a path", "../copy-sample"),
                              ("a path with a slash", "PROJ-1/work"), ("dots", "..")):
            got = prepare_copy.remove_story_artifacts(copy, ticket, live_repo=live)
            check(f"a ticket that is {label}: nothing removed, one line, the live checkout and the copy stand",
                  "nothing removed" in got and "\n" not in got and (live / "test-harness").is_dir() and (copy / "test-harness").is_dir(), got)

        for label, bad_copy in (("the live checkout itself", live), ("a folder inside the live checkout", live / "test-harness")):
            try:
                prepare_copy.remove_story_artifacts(bad_copy, TICKET, live_repo=live)
                refused = False
            except ValueError:
                refused = True
            check(f"INVARIANT: given {label} as the copy it refuses, and the live story is intact", refused
                  and (harness / "artifacts" / TICKET / "pipeline.json").is_file())

        # a leftover, UNTRACKED story of an earlier run in a reused copy goes too (the copy starts from no story at all)
        leftover = copy / "test-harness" / "qa-factory" / "artifacts" / TICKET / "work"
        leftover.mkdir(parents=True)
        (leftover / "earlier-run.json").write_text("{}", encoding="utf-8")
        got = prepare_copy.remove_story_artifacts(copy, TICKET, live_repo=live)
        check("a leftover of an earlier run in a reused copy is removed too", "removed artifacts/" in got and not leftover.exists(), got)
    finally:
        remove_worktrees(base / "live-repo", base / "copy-sample")
        force_rmtree(base)
    assert fails == start, "see the FAIL lines above"


def _two_commit_repo(base):
    """A live checkout whose HEAD (B) carries what an earlier run left (`old-run-tests.py`) and whose
    first commit (A) is the clean re-onboarding commit - the shape of a comparison run (HEAD vs the re-onboarding commit)."""
    live = base / "live-repo"
    live.mkdir()
    git(live, "init", "-q")
    harness = live / "test-harness" / "qa-factory"
    harness.mkdir(parents=True)
    (harness / "config.json").write_text("{}", encoding="utf-8")
    git(live, "add", "-A")
    git(live, "commit", "-q", "-m", "re-onboarding")
    clean = git(live, "rev-parse", "HEAD")
    git(live, "tag", "clean-base")
    (live / "test-harness" / "old-run-tests.py").write_text("def test_old():\n    pass\n" * 50, encoding="utf-8")
    git(live, "add", "-A")
    git(live, "commit", "-q", "-m", "tests of an earlier run")
    return live, clean, git(live, "rev-parse", "HEAD")


def test_prepare_copy_base():
    start = fails
    base = Path(tempfile.mkdtemp(prefix="qa-prepare-copy-base-"))
    try:
        live, clean, head = _two_commit_repo(base)
        old = Path("test-harness") / "old-run-tests.py"

        at_head = base / "copy-head"
        got = prepare_copy.add_worktree(live, at_head)
        check("prepare_copy_base: with no --base the copy is at the live HEAD, as it always was",
              got == head and git(at_head, "rev-parse", "HEAD") == head and (at_head / old).is_file(), got)

        at_base = base / "copy-base"
        got = prepare_copy.add_worktree(live, at_base, clean)
        check("--base <commit>: the copy stands at that commit, not at the live HEAD",
              got == clean and git(at_base, "rev-parse", "HEAD") == clean, got)
        check("and what the later commit added is NOT in it (the comparison-run shape: 1508 lines of an older run)",
              not (at_base / old).exists())
        check("the live checkout is untouched: still on its own HEAD, no change",
              git(live, "rev-parse", "HEAD") == head and git(live, "status", "--porcelain") == "")

        by_tag, by_short = base / "copy-tag", base / "copy-short"
        check("a tag is a base", prepare_copy.add_worktree(live, by_tag, "clean-base") == clean)
        check("and so is an abbreviated hash", prepare_copy.add_worktree(live, by_short, clean[:8]) == clean)

        # edges: a base that is not a commit is refused BEFORE anything is created
        for label, bad in (("a name nothing resolves", "no-such-commit"), ("empty", ""), ("only spaces", "  "),
                           ("an option", "--help"), ("a ref with a path in it", "HEAD:test-harness/old-run-tests.py")):
            target = base / "copy-bad"
            try:
                prepare_copy.add_worktree(live, target, bad)
                refused = ""
            except ValueError as exc:
                refused = str(exc)
            check(f"--base that is {label}: refused with a message naming it, nothing created",
                  "is not a commit" in refused and not target.exists(), refused)

        # a copy that already exists
        try:
            prepare_copy.add_worktree(live, at_head, clean)
            refused = ""
        except ValueError as exc:
            refused = str(exc)
        check("INVARIANT: an existing copy at ANOTHER commit than --base is refused, never silently reused",
              "already stands at" in refused and "--remove" in refused and git(at_head, "rev-parse", "HEAD") == head, refused)
        check("an existing copy at the --base commit is reused",
              prepare_copy.add_worktree(live, at_base, clean) == clean)
        check("an existing copy with no --base is reused as it is, wherever it stands",
              prepare_copy.add_worktree(live, at_base) == clean)

        # end to end through main(): the usage line `--base <commit>`
        saved = (prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, prepare_copy.paths.BASE, sys.argv)
        prepare_copy.LIVE_REPO = live
        prepare_copy.paths.BASE = base          # in-process: main() needs a runs base, and this machine may have none set
        prepare_copy.prepare_toolchain = lambda project: "toolchain ready (stub)"
        sys.argv = ["prepare_copy.py", "--name", "viamain", "--base", clean]
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = prepare_copy.main()
            via_main = base / "copy-viamain"
            check("main --base <commit>: exit 0, the copy is at that commit and says where",
                  code == 0 and git(via_main, "rev-parse", "HEAD") == clean and clean in out.getvalue(),
                  f"{code} {out.getvalue()[:300]} {err.getvalue()[:300]}")
            sys.argv = ["prepare_copy.py", "--name", "viabad", "--base", "no-such-commit"]
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = prepare_copy.main()
            check("main --base that is not a commit: non-zero, the message on stderr, no copy made",
                  code != 0 and "is not a commit" in err.getvalue() and not (base / "copy-viabad").exists(),
                  f"{code} {err.getvalue()[:300]}")
        finally:
            prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, prepare_copy.paths.BASE, sys.argv = saved
    finally:
        remove_worktrees(base / "live-repo", *(base / n for n in (
            "copy-head", "copy-base", "copy-tag", "copy-short", "copy-viamain")))
        force_rmtree(base)
    assert fails == start, "see the FAIL lines above"


class Done:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def stub_runner(script):
    """A `subprocess.run` that never starts anything: `script` maps a fragment of the command line to the
    answer; every command is recorded as (command, cwd)."""
    calls = []

    def run(command, **kwargs):
        calls.append((list(command), kwargs.get("cwd")))
        line = " ".join(command)
        for fragment, answer in script.items():
            if fragment in line:
                if isinstance(answer, Exception):
                    raise answer
                return answer
        return Done()
    run.calls = calls
    return run


def test_prepare_copy_toolchain():
    start = fails
    base = Path(tempfile.mkdtemp(prefix="qa-prepare-toolchain-"))
    try:
        project = base / "test-harness"
        for rel in ("activity/test_activity_events_access.py", "test_zeta.py"):
            target = project / "suite" / "tests" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("def test_x():\n    pass\n", encoding="utf-8")
        sample = "suite/tests/activity/test_activity_events_access.py"
        proof = dict(proof_import="pkg", tests_dir="suite/tests")     # what the runs table's `toolchain` names

        run = stub_runner({})
        line = prepare_copy.prepare_toolchain(project, run=run, **proof)
        commands = [" ".join(c) for c, _ in run.calls]
        check("prepare_copy_toolchain: install, then the SDK import, then a collect-only of ONE existing test file",
              commands == ["poetry install", "poetry run python -c import pkg",
                           f"poetry run pytest --collect-only -q -p no:cacheprovider {sample}"], str(commands))
        check("every command runs in the copy's test-harness", all(cwd == str(project) for _, cwd in run.calls),
              str(run.calls))
        check("and the line it returns says what was proved", "ready" in line and sample in line, line)

        # F-cmp2-19: the install exits 0, the SDK is not importable
        sdk = "ModuleNotFoundError: No module named 'pkg'"
        run = stub_runner({"import pkg": Done(1, "", f"Traceback (most recent call last):\n{sdk}")})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("install exit 0 but `import pkg` fails: it FAILS, quoting the stderr",
              sdk in raised and "import pkg" in raised and "exit 1" in raised, raised)
        check("and the collection is not tried on an environment that cannot import the SDK",
              not any("--collect-only" in " ".join(c) for c, _ in run.calls), str(run.calls))

        run = stub_runner({"--collect-only": Done(2, "", "ERROR collecting x: conftest.py ImportError")})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("the SDK imports but the test file does not collect: it FAILS, quoting the stderr",
              "conftest.py ImportError" in raised and "collect-only" in raised and sample in raised, raised)

        run = stub_runner({"--collect-only": Done(2, "E   ImportError: stdout only", "")})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("pytest says its reason on stdout and stderr is empty: the stdout is quoted instead",
              "stdout only" in raised, raised)

        run = stub_runner({"poetry install": Done(1, "", "SolverProblemError")})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("a failed install fails at once, and nothing after it is tried",
              "SolverProblemError" in raised and len(run.calls) == 1, f"{raised} {len(run.calls)}")

        long_err = "HEAD-NOISE " + "x" * 5000 + " the-cause-at-the-end"
        run = stub_runner({"import pkg": Done(1, "", long_err)})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("a long stderr is cut to its END (where the cause is), and the cut is marked",
              "the-cause-at-the-end" in raised and "HEAD-NOISE" not in raised and "..." in raised
              and len(raised) < prepare_copy.STDERR_QUOTE + 400, str(len(raised)))

        run = stub_runner({"poetry": FileNotFoundError(2, "No such file or directory: 'poetry'")})
        try:
            prepare_copy.prepare_toolchain(project, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("poetry not installed: it fails with a message that says so, not a traceback",
              "could not start" in raised and "poetry" in raised, raised)

        empty = base / "empty-harness"
        empty.mkdir()
        run = stub_runner({})
        try:
            prepare_copy.prepare_toolchain(empty, run=run, **proof)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("no test file to collect: refused as unverified, never reported ready",
              "nothing to collect" in raised and "unverified" in raised, raised)

        # end to end through main(): a failed proof is a non-zero exit with the stderr in front of the person
        live, clean, _head = _two_commit_repo(base)
        saved = (prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, prepare_copy.paths.BASE, sys.argv)
        prepare_copy.LIVE_REPO = live
        prepare_copy.paths.BASE = base          # in-process, as in the --base group: no config or env var needed

        def failing(_project):
            raise prepare_copy.ToolchainNotReady(f"`import pkg` failed (exit 1) in x:\n{sdk}")
        prepare_copy.prepare_toolchain = failing
        sys.argv = ["prepare_copy.py", "--name", "toolchainfail"]
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = prepare_copy.main()
        finally:
            prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, prepare_copy.paths.BASE, sys.argv = saved
            remove_worktrees(live, base / "copy-toolchainfail")
        check("main: a toolchain that is not ready exits NON-ZERO and quotes the stderr",
              code != 0 and sdk in err.getvalue() and "NOT ready" in err.getvalue(), f"{code} {err.getvalue()[:300]}")
        check("and does not print the line that tells the person to start the story",
              "/qa-factory:qa-story" not in out.getvalue(), out.getvalue()[:300])
    finally:
        force_rmtree(base)
    assert fails == start, "see the FAIL lines above"


def test_prepare_copy_installed_plugins():
    """`installed_plugins` of the runs table: every id is written `false` into the copy's settings.local.json; an
    empty list, an empty table or no key disables nothing and says so (the branch main() takes after the config)."""
    start = fails
    base = Path(tempfile.mkdtemp(prefix="qa-prepare-plugins-"))
    p = prepare_copy.paths
    try:
        live, _clean, _head = _two_commit_repo(base)
        saved = (prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, p.BASE, p.TABLE, sys.argv)
        prepare_copy.LIVE_REPO, p.BASE = live, base
        prepare_copy.prepare_toolchain = lambda project: "toolchain ready (stub)"
        try:
            for name, table, want in (("twoids", {"installed_plugins": ["a@one", "a@two"]}, {"a@one": False, "a@two": False}),
                                      ("emptylist", {"installed_plugins": []}, None),
                                      ("nokey", {}, None)):
                p.TABLE = table
                sys.argv = ["prepare_copy.py", "--name", name]
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = prepare_copy.main()
                local = base / ("copy-" + name) / "test-harness" / ".claude" / "settings.local.json"
                if want is None:
                    check(f"installed_plugins {table}: exit 0, nothing disabled, no settings.local.json written",
                          code == 0 and "nothing disabled" in out.getvalue() and not local.exists(),
                          f"{code} {out.getvalue()[:200]} {err.getvalue()[:200]}")
                else:
                    written = json.loads(local.read_text(encoding="utf-8")) if local.is_file() else None
                    check(f"installed_plugins {table}: every id is written false into settings.local.json",
                          code == 0 and written == {"enabledPlugins": want} and "nothing disabled" not in out.getvalue(),
                          f"{code} {written} {err.getvalue()[:200]}")
        finally:
            prepare_copy.LIVE_REPO, prepare_copy.prepare_toolchain, p.BASE, p.TABLE, sys.argv = saved
    finally:
        remove_worktrees(base / "live-repo", *(base / ("copy-" + n) for n in ("twoids", "emptylist", "nokey")))
        force_rmtree(base)
    assert fails == start, "see the FAIL lines above"


if __name__ == "__main__":
    for group in (test_prepare_copy_removes_story, test_prepare_copy_base, test_prepare_copy_toolchain,
                  test_prepare_copy_installed_plugins):
        try:
            group()
        except AssertionError:
            pass  # its FAIL lines are printed and counted; the other groups still run
    print(f"=== test_prepare_copy: {total - fails}/{total} ok ===")
    sys.exit(1 if fails else 0)
