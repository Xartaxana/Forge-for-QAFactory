"""Prepare a project copy for one calibration run of the experiment.

    python experiments/measurers/prepare_copy.py --name <run> --judge on
    python experiments/measurers/prepare_copy.py --name <run> --judge none
    python experiments/measurers/prepare_copy.py --name <run> --remove
    python experiments/measurers/prepare_copy.py --name <run> --base <commit>   # a copy at that commit, not at the live HEAD

The live checkout, the copy prefix, the toolchain proof and the installed plugin come from the runs table
(QA_RUNS_TABLE, experiments/measurers/paths.py): without one this script makes no copy.

Creates a git worktree of the test repository (the table's live_repo) as a sibling of the live checkout,
at the live HEAD or at `--base <commit>` (a comparison run: HEAD carried 1508 lines of an earlier run's tests, so the
base had to be moved by hand), so the config's relative `../..` paths resolve the same, copies the live project's qa-factory
config/strategy/readiness into it (no story artifacts), removes `artifacts/<--ticket>` from the COPY (HEAD
tracks the earlier run of the same story, and a story with a pipeline.json skips S0 - so the driver would never
read `--skip-sources`; the live checkout is never touched), sets `judge.provider` and
`pipeline.stop_after: null`, disables the installed qa-factory plugin for that copy (the branch
plugin is loaded with `--plugin-dir`), installs the copy's toolchain (`poetry install`), PROVES it
(`import <toolchain module>`, then `pytest --collect-only` on one existing test file) and exits non-zero with the
stderr quoted when either proof fails, then prints the command to start the story.
"""
import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import paths

sys.path.insert(0, str(paths.SCRIPTS))
import runtime_paths as RP  # noqa: E402 - where the factory's files live, in either layout (t-232)

LIVE_REPO = paths.LIVE_REPO          # the table's live_repo under BASE, or None: then main refuses
PLUGIN = str(paths.PACKAGE)
TICKET_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*-\d+$")


STDERR_QUOTE = 2000


class ToolchainNotReady(RuntimeError):
    """The copy's environment is not one a story can run in; the message quotes what failed."""


def add_worktree(live_repo: Path, copy: Path, base: str | None = None, run=subprocess.run) -> str:
    """The copy's worktree, at `base` (a commit, tag or branch of the live repository) or, with none, at the
    live HEAD as it always was. Returns the commit the copy stands at.

    F-cmp2-5: HEAD of the live branch carried 1508 lines of e2e tests of an earlier run of the story, and the
    base of the copy was moved by hand to the re-onboarding commit. INVARIANT: a copy never silently stands at a
    commit other than the one asked for - a `--base` that is not a commit of the live repository is refused
    BEFORE anything is created, and an existing copy at another commit is refused, not reused (reusing it is
    how a run starts on the wrong base). Without `--base` an existing copy is reused as it is."""
    ref = "HEAD" if base is None else str(base).strip()
    if not ref or ref.startswith("-"):
        raise ValueError(f"--base {base!r} is not a commit: give a commit hash, a tag or a branch of {live_repo}")
    wanted = run(["git", "-C", str(live_repo), "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                 capture_output=True, text=True)
    sha = (wanted.stdout or "").strip()
    if wanted.returncode != 0 or not sha:
        raise ValueError(f"--base {ref!r} is not a commit of {live_repo}: give a commit hash, a tag or a branch "
                         "that `git rev-parse` resolves there")
    if not Path(copy).exists():
        run(["git", "-C", str(live_repo), "worktree", "add", "--detach", str(copy), sha], check=True)
        return sha
    at = run(["git", "-C", str(copy), "rev-parse", "HEAD"], capture_output=True, text=True)
    stands = (at.stdout or "").strip()
    if base is not None and stands != sha:
        raise ValueError(f"the copy {copy} already stands at {stands[:10] or 'an unreadable commit'}, not at "
                         f"--base {ref} ({sha[:10]}): remove it (`--name <name> --remove`) and run again")
    return stands or sha


def _quote(text: str) -> str:
    """The tail of what a failed command printed - the end is where a traceback names its cause."""
    text = (text or "").strip()
    return text if len(text) <= STDERR_QUOTE else "..." + text[-STDERR_QUOTE:]


def prepare_toolchain(project: Path, run=subprocess.run, proof_import=None, tests_dir=None) -> str:
    """`poetry install` in the copy's test-harness, then PROVE it: the SDK imports, and one existing test file
    collects. Raises ToolchainNotReady, quoting stderr, on the first step that fails; returns a line to print.

    F-cmp2-19: `poetry install` exited 0 and the SDK module (a path dependency outside the repository) was
    still not importable in the copy's environment - the gate-A packet then carried "the tests do not collect"
    to a person. An exit code of the install is not proof of an environment; the two commands below are.
    A copy with no test file to collect is refused too: a toolchain nobody could try is unverified, not ready.
    `proof_import` (the module to import) and `tests_dir` (the folder of existing tests, relative to the project)
    default to the `toolchain` of the runs table; with neither given nor named there the toolchain cannot be proved
    and is refused, never reported ready."""
    chain = paths.TABLE.get("toolchain") or {}
    proof_import = proof_import or chain.get("import")
    tests_dir = tests_dir or chain.get("tests")
    if not proof_import or not tests_dir:
        raise ToolchainNotReady("no toolchain proof in the runs table (QA_RUNS_TABLE, key toolchain: import, tests): "
                                "the toolchain would be installed but unverified")
    project = Path(project)
    tests = project / tests_dir
    found = sorted(tests.rglob("test_*.py")) if tests.is_dir() else []
    sample = found[0].relative_to(project).as_posix() if found else ""
    steps = [("poetry install", ["poetry", "install"]),
             (f"import {proof_import}", ["poetry", "run", "python", "-c", f"import {proof_import}"])]
    if sample:
        steps.append((f"pytest --collect-only on {sample}",
                      ["poetry", "run", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", sample]))
    for label, command in steps:
        try:
            done = run(command, cwd=str(project), capture_output=True, text=True)
        except OSError as exc:
            raise ToolchainNotReady(f"`{label}` could not start: {exc}. Is poetry installed and on PATH?") from exc
        if done.returncode != 0:
            said = _quote(done.stderr) or _quote(done.stdout) or "(nothing printed)"
            raise ToolchainNotReady(f"`{label}` failed (exit {done.returncode}) in {project}:\n{said}")
    if not sample:
        raise ToolchainNotReady(f"no test_*.py under {tests}: nothing to collect, so the toolchain of {project} is "
                                "installed but unverified")
    return f"toolchain ready: the SDK imports and {sample} collects"


def remove_story_artifacts(copy: Path, ticket: str, live_repo: Path | None = None) -> str:
    """Remove `test-harness/qa-factory/artifacts/<ticket>` from the COPY and say so (t-172 C1, B-231).

    The copy is `git worktree add --detach HEAD`, and the live repository's HEAD TRACKS the artifacts of
    an earlier run of the story (pipeline.json included). A story with a pipeline.json skips S0, so a list of sources not
    to read (`--skip-sources`) would never be read and the old manifest citing the excluded merge request
    would stay in work/. A comparison run must start from no story at all.

    INVARIANT: only a path inside the copy is ever removed. The live checkout is the copy's parent's
    sibling and is never touched: the target is resolved and refused unless it lies under the copy and
    not under the live repository. Returns the line to print; nothing tracked or present is one line too."""
    live_repo = live_repo or LIVE_REPO
    if live_repo is None:
        raise ValueError("no live repository: name live_repo in the runs table (QA_RUNS_TABLE) or pass live_repo")
    if not TICKET_RE.match(str(ticket or "")):
        return (f"no ticket given (--ticket {ticket!r}): nothing removed from the copy; a story that already "
                "has artifacts in it skips S0 and never reads a list of sources not to read")
    copy_root, live_root = Path(copy).resolve(), Path(live_repo).resolve()
    if copy_root == live_root or live_root in copy_root.parents:
        raise ValueError(f"{copy_root} is the live checkout or inside it: refusing to remove anything from it")
    target = (copy_root / "test-harness" / "qa-factory" / "artifacts" / ticket).resolve()
    if copy_root not in target.parents or live_root in target.parents or target == live_root:
        raise ValueError(f"{target} is not inside the copy {copy_root}: refusing to remove it")
    if not target.exists():
        return f"artifacts/{ticket} is not in the copy: nothing removed"
    files = sum(1 for p in target.rglob("*") if p.is_file())

    def force(func, path, _info):
        # tracked files of a worktree are read-only on Windows after a git checkout
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if sys.version_info >= (3, 12):
        shutil.rmtree(target, onexc=force)
    else:
        shutil.rmtree(target, onerror=force)
    return (f"removed artifacts/{ticket} from the copy ({files} files of an earlier run of the story): the story "
            "starts from S0 and reads its list of sources not to read")


def copy_factory_files(live_project: Path, copy_project: Path) -> list:
    """Copy the live project's factory files into the copy: the config, the shared records at the top of
    `qa-factory/` (obligations, backlog), the strategy documents and the readiness report. Returns the
    names copied, relative to `qa-factory/` as they stand in the COPY.

    The layout is asked of `runtime_paths`, never spelled here (FR-37, t-232): the live project may keep
    `readiness.json` beside the config (an older factory) or in `state/` (the two-folder layout), and
    the copy gets it where this package's readiness.py writes it. Nothing else of `state/` or `records/`
    is copied: a comparison run starts without the live project's journal, ledger or receipts."""
    src, dst = RP.home_dir(live_project), RP.home_dir(copy_project)
    dst.mkdir(parents=True, exist_ok=True)
    done = []
    for name in ("config.json", "obligations.md", "factory-backlog.md"):
        if (src / name).is_file():
            shutil.copy2(src / name, dst / name)
            done.append(name)
    report = RP.readiness(live_project)
    if report.is_file():
        target = RP.readiness_write(copy_project)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(report, target)
        done.append(target.relative_to(dst).as_posix())
    if (src / "strategy").is_dir():
        shutil.copytree(src / "strategy", dst / "strategy", dirs_exist_ok=True)
        done.append("strategy/")
    return done


def start_lines(project, plugin, ticket, name, runs=None) -> list:
    """The lines that tell a person how to start a story in the copy: PowerShell, `Start-Process -WorkingDirectory`
    (docs/RUNBOOK.md 9.3), never `cd <project>`. A shell whose cwd is inside the project fires the hooks of the live
    session on everything it runs (builder-rules 10), and a driver started from the tool's own shell dies with it
    (the 02.10 rehearsal's process died at 05:38 and its log held nothing: PYTHONUNBUFFERED is set for that reason,
    B-178, FR-43). The driver's output goes to `<runs>/<name>-1.log` / `.err` (default: this experiment's `runs/`),
    `-PassThru` prints the pid the start line of the notebook needs. The interactive session is the same form
    without the redirects. The default `<runs>` is `runs_dir` of the runs table, else `<BASE>/runs` - never this
    folder, which travels with the repository and must not collect run logs."""
    runs = Path(runs) if runs else (paths.table_path("runs_dir") or paths.BASE / "runs")
    log, err = runs / f"{name}-1.log", runs / f"{name}-1.err"
    scripts = f"{plugin}/scripts/story_run.py"
    driver = ",".join(f'"{x}"' for x in (scripts, "--task", ticket, "--env", "localhost", "--model", "sonnet",
                                         "--no-trace", "--plugin-dir", plugin))
    return ["  start (PowerShell; the working folder is set by Start-Process, never by `cd`):",
            '  $env:PYTHONUNBUFFERED = "1"',
            f'  Start-Process -FilePath python -WorkingDirectory "{project}" `',
            f"    -ArgumentList {driver} `",
            f'    -RedirectStandardOutput "{log}" `',
            f'    -RedirectStandardError "{err}" -PassThru',
            "  or, an interactive session in the same folder:",
            '  $env:CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS = "0"',
            f'  Start-Process -FilePath claude -WorkingDirectory "{project}" '
            f'-ArgumentList "--plugin-dir","{plugin}","--model","sonnet"']


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--name", required=True, help="suffix of the copy: <copy_prefix><name> of the runs table")
    ap.add_argument("--judge", choices=["on", "shadow", "none"], default="none")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--ticket", default="<TICKET>")
    ap.add_argument("--base", default=None,
                    help="commit, tag or branch of the live repository the copy is made at (default: its HEAD)")
    ap.add_argument("--plugin", default=PLUGIN,
                    help="plugin root loaded with --plugin-dir (default: this repository's package)")
    a = ap.parse_args()
    try:                              # after parsing, so `--help` works with no config (F-14)
        paths.require_base()          # this script writes under BASE
    except paths.BaseNotSet as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    if LIVE_REPO is None:
        sys.stderr.write("no live repository: set live_repo in the runs table (QA_RUNS_TABLE)\n")
        return 2
    try:
        copy = LIVE_REPO.parent / paths.copy_folder(a.name, {})
    except ValueError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    if a.remove:
        subprocess.run(["git", "-C", str(LIVE_REPO), "worktree", "remove", "--force", str(copy)], check=False)
        print("removed", copy)
        return 0
    try:
        print(f"copy {copy} stands at {add_worktree(LIVE_REPO, copy, a.base)}")
    except ValueError as exc:
        print(f"copy NOT made: {exc}", file=sys.stderr)
        return 2
    dst = RP.home_dir(copy / "test-harness")
    copy_factory_files(LIVE_REPO / "test-harness", copy / "test-harness")
    (dst / "artifacts").mkdir(exist_ok=True)
    (dst / "state").mkdir(exist_ok=True)
    print(remove_story_artifacts(copy, a.ticket))
    cfg_path = dst / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8-sig"))
    cfg["judge"] = ({"provider": "none"} if a.judge == "none" else
                    {"provider": "typesafe", "mode": a.judge, "api_key_env": "TYPESAFE_API_KEY"})
    cfg["pipeline"] = {"stop_after": None}
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    installed = paths.TABLE.get("installed_plugins") or []     # every id the copy must not load beside --plugin-dir
    if installed:
        local = copy / "test-harness" / ".claude"
        local.mkdir(exist_ok=True)
        (local / "settings.local.json").write_text(json.dumps(
            {"enabledPlugins": {plugin_id: False for plugin_id in installed}}, indent=2) + "\n", encoding="utf-8")
    else:
        print("no installed plugin named in the runs table: nothing disabled")
    project = copy / "test-harness"
    try:
        print(prepare_toolchain(project))
    except ToolchainNotReady as exc:
        print(f"copy NOT ready: {exc}\n  fix the environment in {project}, then run this again "
              "(the copy is reused as it is)", file=sys.stderr)
        return 3
    print(f"copy ready: {project}\n  judge: {cfg['judge']}")
    for line in start_lines(project, a.plugin, a.ticket, a.name):
        print(line)
    print(f"  then: /qa-factory:qa-story {a.ticket}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
