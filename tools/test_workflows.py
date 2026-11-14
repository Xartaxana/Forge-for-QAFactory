"""The GitHub workflows judged against .gitlab-ci.yml (GM1-5, t-1888; plan t-1855 node GM1-5, critic t-1856 F-11, F-19, F-21).

Which files are judged: the live `.github/workflows/` of the repository root when `.github` exists there (after the
move), otherwise the staged drafts in `docs/migration/forge-repo/.github/workflows/`. The draft never masks a lost live
folder: `.github` present but empty or short of one of the three files is RED and names the missing files; neither
folder present is RED. `yaml.safe_load` reads the key `on` as `True`.

Every pin names the `.gitlab-ci.yml` line it mirrors (the file as of GM1-1, without `board-check`). GitHub itself is
NOT run here: "not run on GitHub" stays true until the step D3 of docs/migration/MIGRATION_PLAN.md.
There is no scrub step in any workflow (owner's word, decision FK-5) and nothing here pins one.
The test diet (t-2566) added to the GitLab file: the step `test_quarantine.py check` (here, since 13.11.2026, the nightly.yml job
quarantine-check, schedule only: it walks the whole history and outlived forge-check), the jobs quarantine-watch,
quarantine-watch-report (here: quarantine-watch.yml, a fourth file, so neither schedule starts the other's jobs) and
test-redundancy (here: a job of nightly.yml started by the inputs TEST_REDUNDANCY / REDUNDANCY_SCOPE); runner-facts, absent
from the first port, is a job of forge-check.yml.

Verification: python -m pytest tools/test_workflows.py -q
"""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE_MARKER = ".github"
LIVE_REL = ".github/workflows"
DRAFT_REL = "docs/migration/forge-repo/.github/workflows"
PACKAGE_DRAFT = ROOT / "docs" / "migration" / "qafactory-repo" / ".github" / "workflows" / "package-check.yml"
NAMES = ("forge-check.yml", "nightly.yml", "canon.yml", "quarantine-watch.yml")
QUARANTINE_CONFIG = ROOT / "plans" / "test-quarantine" / "config.json"


def live_or_draft(root, live_rel, draft_rel, marker_rel=None):
    """The world detector: `root/live_rel` when `root/marker_rel` (default: live_rel itself) exists, else `root/draft_rel`.
    The marker, not the target, decides: a live folder that exists but lost its files must fail, never fall back to the
    draft. A reader of another staged file (tools/cloud_setup.sh, docs/migration/cutover.json) may import this."""
    root = pathlib.Path(root)
    return root / live_rel if (root / (marker_rel or live_rel)).exists() else root / draft_rel


def find_workflows(root):
    """(directory, [names of the three workflows missing from it]); a directory that does not exist misses all three."""
    folder = live_or_draft(root, LIVE_REL, DRAFT_REL, LIVE_MARKER)
    return folder, [n for n in NAMES if not (folder / n).is_file()]


def workflows_dir():
    folder, missing = find_workflows(ROOT)
    if missing:
        pytest.fail(f"{folder}: missing {', '.join(missing)} (a present .github folder is never replaced by the draft)")
    return folder


def load(name, folder=None):
    yaml = pytest.importorskip("yaml")
    path = (folder or workflows_dir()) / name
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def text_of(name):
    return (workflows_dir() / name).read_text(encoding="utf-8")


def job_steps(job):
    return job["steps"]


def run_steps(job):
    return [s for s in job_steps(job) if "run" in s]


def runs(job):
    return [s["run"].strip() for s in run_steps(job)]


def all_run_strings():
    """Every run: string of every workflow judged here (the three, plus the QAFactory draft while it is in this tree)."""
    out = []
    docs = [(n, load(n)) for n in NAMES]
    if PACKAGE_DRAFT.is_file():
        docs.append((PACKAGE_DRAFT.name, load(PACKAGE_DRAFT.name, PACKAGE_DRAFT.parent)))
    for name, doc in docs:
        for job_name, job in doc["jobs"].items():
            for step in job.get("steps", []):
                if "run" in step:
                    out.append((f"{name}:{job_name}", step["run"]))
    return out


# ---------------------------------------------------------------- the world detector (F-11: both worlds, edges named)

def _mk(root, rels):
    for rel in rels:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("name: x\n", encoding="utf-8")


def test_the_live_folder_is_judged_once_github_exists(tmp_path):
    _mk(tmp_path, [f"{LIVE_REL}/{n}" for n in NAMES] + [f"{DRAFT_REL}/{n}" for n in NAMES])
    folder, missing = find_workflows(tmp_path)
    assert folder == tmp_path / LIVE_REL and missing == []


def test_the_draft_is_judged_while_github_does_not_exist(tmp_path):
    _mk(tmp_path, [f"{DRAFT_REL}/{n}" for n in NAMES])
    folder, missing = find_workflows(tmp_path)
    assert folder == tmp_path / DRAFT_REL and missing == []


def test_an_empty_github_folder_is_red_and_the_draft_does_not_mask_it(tmp_path):
    _mk(tmp_path, [f"{DRAFT_REL}/{n}" for n in NAMES])
    (tmp_path / ".github").mkdir()
    folder, missing = find_workflows(tmp_path)
    assert folder == tmp_path / LIVE_REL and missing == list(NAMES)


def test_a_live_folder_short_of_one_file_names_that_file(tmp_path):
    _mk(tmp_path, [f"{LIVE_REL}/{n}" for n in NAMES if n != "canon.yml"] + [f"{DRAFT_REL}/{n}" for n in NAMES])
    assert find_workflows(tmp_path)[1] == ["canon.yml"]


def test_neither_folder_is_red(tmp_path):
    folder, missing = find_workflows(tmp_path)
    assert folder == tmp_path / DRAFT_REL and missing == list(NAMES)


def test_the_real_tree_has_the_three_workflows_and_the_key_on_loads_as_true():
    folder = workflows_dir()                       # fails by itself, naming the missing files
    assert all((folder / n).is_file() for n in NAMES)
    for name in NAMES:
        doc = load(name)
        assert True in doc and "on" not in doc, name        # safe_load reads `on` as the boolean True (YAML 1.1)
        assert doc["jobs"], name


# ---------------------------------------------------------------- forge-check (.gitlab-ci.yml:44-113)

# One entry per run: step of the job, in order. A str must equal the run exactly; a tuple of tokens must all be inside it.
FORGE_CHECK_RUNS = [
    "pip install -q pytest pyflakes==3.2.0 pyyaml openpyxl",                       # .gitlab-ci.yml:62
    ("git config core.hooksPath .githooks", 'git config --global user.name "forge-ci"',          # :64-65, :40-42
     'git config --global user.email "forge-ci@invalid.example"', "git config --global init.defaultBranch main"),
    ("merge-base origin/main HEAD", '[ -n "$CANON_REF" ]', "$CI_MERGE_REQUEST_DIFF_BASE_SHA",    # the base ladder of :74-80
     "$CI_COMMIT_BEFORE_SHA", "0000000000000000000000000000000000000000", "base=HEAD~1", "$GITHUB_OUTPUT"),
    "python tools/lint_ratchet.py --check",                                         # :68
    "python tools/dup_ratchet.py --check",                                          # :70
    'python tools/journal_validator.py --all --base "$BASE"',                       # :73-80
    ('forge_metrics.py --check --base "$CI_MERGE_REQUEST_DIFF_BASE_SHA"',           # :82-87
     "forge_metrics.py --check --base HEAD~1 --warn"),
    "python tools/escape_check.py",                                                 # :89
    "python tools/factory_rules_index.py --check",                                  # :90
    "python tools/architecture_index.py --check",                                   # :91
    "python tools/agents_md.py --check",                                            # :92
    'python tools/piles.py check --base "$BASE"',                                   # :96-103; SL-2 (F-2 (a)): the range's piles, not --all
    'python tools/install_parity.py --check --skip-from-commit-message "$(git log -1 --format=%B $HEAD_SHA)"',   # :107, pull request
    "python tools/install_parity.py --check",                                       # :107, push and canon
    "python -m pytest tools/ -q",                                                   # :109
    "python -B experiments/measurers/test_measurers.py",                            # P1-v N8: run scoreboard tables
    ("scoreboard.py norms --check --against", "scoreboard.py norms --check"),       # P1-v N8: norms only tighten
]


def _fits(run, expected):
    return run == expected if isinstance(expected, str) else all(token in run for token in expected)


def test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere():
    """Mirrors .gitlab-ci.yml:58-109 (before_script and script of forge-check). FK-5: no scrub step in any workflow."""
    got = runs(load("forge-check.yml")["jobs"]["forge-check"])
    assert len(got) == len(FORGE_CHECK_RUNS), got
    for run, expected in zip(got, FORGE_CHECK_RUNS):
        assert _fits(run, expected), (run, expected)
    for name in NAMES:
        assert "scrub" not in text_of(name).lower(), name


def test_no_workflow_asks_for_a_pip_cache_or_exports_the_commit_message():
    """The drafts carried `cache: pip` (setup-python fails without a dependency file: an estimate, not verified) and
    CI_COMMIT_MESSAGE (the message of a push is read by `git log` where a tool needs it)."""
    for name in NAMES:
        text = text_of(name)
        assert not re.search(r"^\s*cache:\s*pip\b", text, re.M), name
        assert "CI_COMMIT_MESSAGE" not in text, name


def test_install_parity_has_two_branches_pull_request_with_the_head_message_and_push_without():
    """.gitlab-ci.yml:104-107: the door `parity-skip:` is read from the head commit message. On a pull request the checkout is
    the merge commit, so the message of the PR head is passed; the sha reaches the shell only through env:."""
    steps = {s.get("name"): s for s in run_steps(load("forge-check.yml")["jobs"]["forge-check"]) if "install_parity" in s["run"]}
    pr, push = steps["install parity (pull request)"], steps["install parity (push, canon)"]
    assert pr["if"] == "github.event_name == 'pull_request'" and push["if"] == "github.event_name != 'pull_request'"
    assert pr["env"] == {"HEAD_SHA": "${{ github.event.pull_request.head.sha }}"} and "env" not in push
    assert "--skip-from-commit-message" in pr["run"] and "${{" not in pr["run"]
    assert push["run"].strip() == "python tools/install_parity.py --check"          # no flag: the tool reads HEAD itself


def test_the_dup_gate_is_in_forge_check_and_the_report_is_in_package_full_and_never_flips_the_verdict():
    """.gitlab-ci.yml:69-70 (gate in forge-check, after lint, before the suite) and :209-211 (report in package-full)."""
    check = runs(load("forge-check.yml")["jobs"]["forge-check"])
    lint = check.index("python tools/lint_ratchet.py --check")
    gate = check.index("python tools/dup_ratchet.py --check")
    assert lint < gate < check.index("python -m pytest tools/ -q")
    assert not [r for r in check if "--report" in r]
    block = next(r for r in runs(load("nightly.yml")["jobs"]["package-full"]) if "selftest.py" in r)
    report_line = next(line for line in block.splitlines() if "dup_ratchet.py --report" in line)
    assert block.index("mkdir -p") < block.index("dup_ratchet.py --report") < block.index("cd ai-packages/qa-factory")
    assert "|| echo" in report_line and "|| rc=1" not in report_line          # a measurement, never the verdict
    assert '"$NODE_INDEX" = "1"' in report_line                                  # shard 1 only (:211)


# ---------------------------------------------------------------- the jobs around it

def test_package_fast_runs_fast_then_the_a19_audit_whose_failure_is_the_steps_exit():
    """.gitlab-ci.yml:166-177: --contracts, the audit-rules test, --fast, then audit_factory.py --agents last."""
    job = load("forge-check.yml")["jobs"]["package-fast"]
    got = runs(job)
    fast = next(i for i, r in enumerate(got) if "selftest.py --fast" in r)
    audit = next(i for i, r in enumerate(got) if "audit_factory.py --agents" in r)
    assert fast < audit == len(got) - 1
    assert any("selftest.py --contracts" in r for r in got[:fast])
    assert any("test_audit_rules.py" in r for r in got[:fast])
    assert "exit $rc" in got[audit] and "|| rc=$?" in got[audit]        # a red A19 is not masked by the echo after it
    assert job["defaults"]["run"]["working-directory"] == "ai-packages/qa-factory"


def test_crap_measure_is_schedule_only_and_never_blocking():
    """.gitlab-ci.yml:295-346: rules schedule only, allow_failure, no needs on package-full, the coverage steps in order."""
    jobs = load("nightly.yml")["jobs"]
    job = jobs["crap-measure"]
    assert job["continue-on-error"] is True and "github.event_name == 'schedule'" in job["if"]
    assert job["needs"] == "skip-if-unchanged"          # the minutes budget only, never the release job
    text = "\n".join(runs(job))
    order = ["coverage debug sys", "mkdir -p ci-out/crap/data", "coveragerc", "zz_coverage_startup.pth",
             "export COVERAGE_PROCESS_START", "scripts/selftest.py --jobs 4", "unset COVERAGE_PROCESS_START",
             "coverage combine", "coverage json", "tools/crap_report.py"]
    at = [text.find(token) for token in order]
    assert -1 not in at and at == sorted(at), dict(zip(order, at))
    assert text.count("--require-coverage") == 2
    for name in ("package-full", "install-smoke", "package-full-report"):
        assert "coverage" not in "\n".join(runs(jobs[name])).lower(), name


def test_quarantine_check_is_a_schedule_only_guard_of_nightly_and_forge_check_no_longer_runs_it():
    """Owner's word 13.11.2026: the history walk of `test_quarantine.py check` moved from forge-check to a nightly job: schedule only
    (a called run carries the caller's event), the whole history (fetch-depth 0), a guard (no continue-on-error)."""
    job = load("nightly.yml")["jobs"]["quarantine-check"]
    assert job["if"] == "github.event_name == 'schedule' && needs.skip-if-unchanged.outputs.run == 'true'"
    assert job["needs"] == "skip-if-unchanged" and "continue-on-error" not in job
    checkout = next(s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/checkout"))
    assert checkout["with"]["fetch-depth"] == 0 and checkout["with"]["ref"] == "main"
    assert runs(job) == ["python tools/test_quarantine.py check"]
    for name in ("forge-check.yml", "canon.yml"):
        assert "test_quarantine.py check" not in "\n".join(
            "\n".join(runs(j)) for j in load(name)["jobs"].values() if "steps" in j), name


def test_package_full_is_two_shards_at_once_and_install_smoke_and_the_drift_report_are_jobs_of_their_own():
    """.gitlab-ci.yml:179-276 (F6-50): parallel 2 + --shard I/N, install-smoke and package-full-report apart, a red shard hides none."""
    jobs = load("nightly.yml")["jobs"]
    full = jobs["package-full"]
    assert full["strategy"]["matrix"] == {"shard": [1, 2]} and full["strategy"]["fail-fast"] is False
    assert full["env"] == {"NODE_INDEX": "${{ matrix.shard }}", "NODE_TOTAL": "${{ strategy.job-total }}"}
    text = "\n".join(runs(full))
    assert '--shard "$NODE_INDEX/$NODE_TOTAL"' in text and "selftest-shard-$NODE_INDEX-of-$NODE_TOTAL.txt" in text
    assert "install_smoke" not in text and "--slow-tests" not in text            # both moved to jobs of their own
    smoke = jobs["install-smoke"]
    assert "needs" in smoke and smoke["needs"] == full["needs"] and "install_smoke.py" in "\n".join(runs(smoke))
    assert smoke["timeout-minutes"] == full["timeout-minutes"] == 180            # timeout: 3h on both (:195, :228)


def test_the_drift_report_reads_the_union_of_the_shards():
    """.gitlab-ci.yml:251-276: needs package-full; the shard outputs are joined; --slow-tests --from reads the join."""
    job = load("nightly.yml")["jobs"]["package-full-report"]
    assert job["needs"] == "package-full" and job["timeout-minutes"] == 10
    (run,) = runs(job)
    assert run.index("set -e") < run.index("cat ci-out/selftest-shard-*.txt > ci-out/selftest.txt")
    assert run.index("cat ci-out") < run.index('--slow-tests --from "$GITHUB_WORKSPACE/ci-out/selftest.txt"')
    download = next(s for s in job_steps(job) if str(s.get("uses", "")).startswith("actions/download-artifact"))
    assert download["with"]["pattern"] == "package-full-shard-*" and download["with"]["merge-multiple"] is True


# ---------------------------------------------------------------- the canon (.gitlab-ci.yml:278-293) and F-19

def test_the_canon_is_named_by_its_ref_and_its_clock_runs_after_a_red_job():
    """F-19 (d): `run-name: canon ${{ inputs.ref }}` (head_branch of a dispatched run is always main). .gitlab-ci.yml:278-293:
    canon-clock, last stage, `when: always`, `canon_clock.py --created-at <output of the first job> --message <head message>`."""
    doc = load("canon.yml")
    assert doc["run-name"] == "${{ inputs.spike && 'dry-spike' || 'canon' }} ${{ inputs.ref }}"   # a spike run never reads as a canon in the list
    jobs = doc["jobs"]
    assert jobs["start"]["outputs"] == {"created_at": "${{ steps.t.outputs.created_at }}"}
    assert jobs["checks"]["needs"] == "start" and jobs["full"]["needs"] == "start"
    clock = jobs["clock"]
    assert clock["if"] == "${{ always() && !inputs.spike }}" and set(clock["needs"]) == {"start", "checks", "full"}
    assert clock["env"] == {"CREATED_AT": "${{ needs.start.outputs.created_at }}"}
    (run,) = runs(clock)
    assert run == 'python tools/canon_clock.py --created-at "$CREATED_AT" --message "$(git log -1 --format=%B)"'


F19E_FORBIDDEN = re.compile(r"\$\{\{\s*(inputs\.|github\.event\.|github\.head_ref|github\.ref_name)")   # the pin and its control


def test_f19e_no_run_string_splices_a_value_a_person_controls():
    """F-19 (e): the canon's ref and a pull request's title, body or sha reach a shell through env:, never through
    a `${{ ... }}` spliced into the run: string (shell injection through a branch name)."""
    strings = all_run_strings()
    assert len(strings) >= 20, "the walk found almost no run: strings"
    for where, run in strings:
        assert not F19E_FORBIDDEN.search(run), (where, run)


def test_the_f19e_pin_can_fail():
    """The negative control of the pin above: the same expression finds a spliced input and a spliced PR title."""
    assert F19E_FORBIDDEN.search('if [ -n "${{ inputs.ref }}" ]; then x; fi')
    assert F19E_FORBIDDEN.search('echo "${{ github.event.pull_request.title }}"')
    assert not F19E_FORBIDDEN.search('echo "$CANON_REF"')


# ---------------------------------------------------------------- runner-facts (.gitlab-ci.yml runner-facts)

def test_runner_facts_is_a_probe_on_pull_request_and_push_only():
    """.gitlab-ci.yml runner-facts: rules mr + main (never the canon), allow_failure, timeout 15m, the facts and the timed
    `selftest.py --limits --lang`. A called run carries the caller's event (workflow_dispatch), so the canon skips it."""
    job = load("forge-check.yml")["jobs"]["runner-facts"]
    assert job["if"] == "github.event_name == 'pull_request' || github.event_name == 'push'"
    assert job["continue-on-error"] is True and job["timeout-minutes"] == 15
    (run,) = runs(job)
    for token in ("nproc", "docker info", "os-release", "selftest.py --limits --lang", "wall time"):
        assert token in run, token


# ---------------------------------------------------------------- the test diet: quarantine watch and test-redundancy

def _quarantine_config():
    import json
    return json.loads(QUARANTINE_CONFIG.read_text(encoding="utf-8"))


def test_the_watch_starts_by_its_cron_a_dispatch_and_a_plugin_version_push_on_the_quarantine_branch():
    """.gitlab-ci.yml quarantine-watch rules: schedule with QUARANTINE_WATCH=1 (cron of plans/test-quarantine/config.json),
    web/api with the variable, a push to the quarantine branch that changes plugin.json. The cron and the branch literal
    equal config.json (the junction tools/test_test_quarantine.py holds for the GitLab file)."""
    cfg = _quarantine_config()
    on = load("quarantine-watch.yml")[True]
    assert on["schedule"] == [{"cron": cfg["cron"]}] and cfg["cron"] == "0 3 * * 1,4"
    assert on["workflow_dispatch"]["inputs"]["ref"]["default"] == cfg["branch"]
    assert on["push"] == {"branches": [cfg["branch"]], "paths": ["ai-packages/qa-factory/.claude-plugin/plugin.json"]}
    assert set(on) == {"schedule", "workflow_dispatch", "push"}          # no pull_request, no workflow_call: never in a canon
    for name in ("quarantine-watch", "quarantine-watch-report"):
        checkout = load("quarantine-watch.yml")["jobs"][name]["steps"][0]
        assert checkout["with"]["ref"].endswith("|| '%s' }}" % cfg["branch"]), name     # a schedule watches the quarantine branch


def test_the_watch_is_two_shards_of_the_quarantined_tests_and_never_red():
    """.gitlab-ci.yml quarantine-watch: parallel 2, timeout 3h, allow_failure, `selftest.py --quarantined --jobs 4 --shard I/N
    --watch-out ci-out/quarantine-watch-I-of-N.json || true`, artifacts ci-out/ for 2 weeks."""
    job = load("quarantine-watch.yml")["jobs"]["quarantine-watch"]
    assert job["strategy"]["matrix"] == {"shard": [1, 2]} and job["strategy"]["fail-fast"] is False
    assert job["continue-on-error"] is True and job["timeout-minutes"] == 180
    run = next(r for r in runs(job) if "selftest.py" in r)
    assert ('python -B scripts/selftest.py --quarantined --jobs 4 --shard "$NODE_INDEX/$NODE_TOTAL" '
            '--watch-out "$OUT/quarantine-watch-$NODE_INDEX-of-$NODE_TOTAL.json" || true') in run
    assert 'export CI_COMMIT_SHA="$(git rev-parse HEAD)"' in run and "CI_PIPELINE_SOURCE=web" in run
    upload = next(s for s in job_steps(job) if str(s.get("uses", "")).startswith("actions/upload-artifact"))
    assert upload["with"]["path"] == "ci-out/" and upload["with"]["retention-days"] == 14 and upload["if"] == "always()"


def test_the_watch_report_joins_the_shards_after_any_shard_outcome_and_is_never_red():
    """.gitlab-ci.yml quarantine-watch-report: needs the watch, when: always, allow_failure, timeout 10m, the ci-summary
    line, the artifact ci-out/quarantine-watch.json (the one `tools/test_quarantine.py pull` reads)."""
    job = load("quarantine-watch.yml")["jobs"]["quarantine-watch-report"]
    assert set(job["needs"]) == {"start", "quarantine-watch"} and job["if"] == "always()"
    assert job["continue-on-error"] is True and job["timeout-minutes"] == 10
    run = next(r for r in runs(job) if "ci-summary" in r)
    assert ('python tools/test_quarantine.py ci-summary --from "ci-out/quarantine-watch-*.json" '
            '--out ci-out/quarantine-watch.json') in run
    download = next(s for s in job_steps(job) if str(s.get("uses", "")).startswith("actions/download-artifact"))
    assert download["with"]["pattern"] == "quarantine-watch-shard-*" and download["with"]["merge-multiple"] is True
    upload = next(s for s in job_steps(job) if str(s.get("uses", "")).startswith("actions/upload-artifact"))
    assert upload["with"] == {"name": "quarantine-watch-report", "path": "ci-out/quarantine-watch.json", "retention-days": 14}


def schedule_crosstalk(docs):
    """The violations of «the watch schedule starts only the watch, the nightly schedule never starts the watch»
    (.gitlab-ci.yml: QUARANTINE_WATCH == "1" on the watch, != "1" on package-full, install-smoke, package-full-report,
    crap-measure). `docs` maps a workflow file name to its parsed YAML. On GitHub a schedule starts every job of its own
    file, so the rule is: `--quarantined` runs only in a file whose schedules are exactly the watch cron, and that file
    runs no full-tier command."""
    out = []
    full_tier = ("install_smoke.py", "--slow-tests", "crap_report.py", "test_redundancy.py")
    for name, doc in docs.items():
        on = doc.get(True) or {}
        crons = [s.get("cron") for s in (on.get("schedule") or [])] if isinstance(on, dict) else []
        text = "\n".join(s["run"] for job in doc["jobs"].values() for s in job.get("steps", []) if "run" in s)
        watches = "--quarantined" in text
        if watches and crons != [WATCH_CRON]:
            out.append(f"{name}: runs --quarantined under schedules {crons}")
        if watches and any(t in text for t in full_tier):
            out.append(f"{name}: the watch file runs a full-tier command")
        if WATCH_CRON in crons and not watches:
            out.append(f"{name}: carries the watch cron without the watch")
    return out


WATCH_CRON = "0 3 * * 1,4"


def test_neither_schedule_starts_the_other_and_the_canon_never_runs_the_quarantine():
    """The watch is a workflow of its own (quarantine-watch.yml); nightly.yml keeps its own cron and no `--quarantined`;
    canon.yml calls forge-check.yml and nightly.yml only, so the canon never runs the quarantine rows."""
    docs = {n: load(n) for n in NAMES}
    assert schedule_crosstalk(docs) == []
    assert docs["nightly.yml"][True]["schedule"] == [{"cron": "0 1 * * *"}]
    canon_calls = {j["uses"] for j in docs["canon.yml"]["jobs"].values() if "uses" in j}
    assert canon_calls == {"./.github/workflows/forge-check.yml", "./.github/workflows/nightly.yml"}
    for name in ("forge-check.yml", "nightly.yml", "canon.yml"):
        assert "--quarantined" not in text_of(name), name


def test_the_crosstalk_pin_can_fail():
    """The negative control of the pin above: the watch moved into the nightly file, a full-tier command in the watch file,
    and the watch cron on a file without the watch are each named."""
    nightly = {True: {"schedule": [{"cron": "0 1 * * *"}]},
               "jobs": {"w": {"steps": [{"run": "python -B scripts/selftest.py --quarantined"}]}}}
    mixed = {True: {"schedule": [{"cron": WATCH_CRON}]},
             "jobs": {"w": {"steps": [{"run": "selftest.py --quarantined"}, {"run": "python -B scripts/install_smoke.py"}]}}}
    empty = {True: {"schedule": [{"cron": WATCH_CRON}]}, "jobs": {"x": {"steps": [{"run": "echo"}]}}}
    assert schedule_crosstalk({"nightly.yml": nightly}) == ["nightly.yml: runs --quarantined under schedules ['0 1 * * *']"]
    assert schedule_crosstalk({"w.yml": mixed}) == ["w.yml: the watch file runs a full-tier command"]
    assert schedule_crosstalk({"e.yml": empty}) == ["e.yml: carries the watch cron without the watch"]


REDUNDANCY_IF = ("github.event_name == 'workflow_dispatch' && "
                 "(inputs.TEST_REDUNDANCY == '1' || startsWith(inputs.ref, 'measure/'))")


def redundancy_rule_violations(job):
    """What of the test-redundancy job's start and failure keys departs from .gitlab-ci.yml (rule, no needs, 3h, allow_failure,
    the scope through env:)."""
    out = []
    if job.get("if") != REDUNDANCY_IF:
        out.append("if: %r" % job.get("if"))
    if "needs" in job:
        out.append("needs: %r (the GitLab job has needs: [])" % job["needs"])
    if job.get("continue-on-error") is not True:
        out.append("continue-on-error is not true (allow_failure)")
    if job.get("timeout-minutes") != 180:
        out.append("timeout-minutes: %r (3h)" % job.get("timeout-minutes"))
    if job.get("env") != {"REDUNDANCY_SCOPE": "${{ inputs.REDUNDANCY_SCOPE }}"}:
        out.append("env: %r" % job.get("env"))
    return out


def test_test_redundancy_runs_only_by_a_dispatch_with_the_input_or_a_measure_ref_and_is_never_red():
    """.gitlab-ci.yml test-redundancy: rules `(web || api) && (TEST_REDUNDANCY == "1" || ref =~ ^measure/)`, timeout 3h,
    allow_failure, no needs, the coverage .pth, the smoke on one file, the run (--keep-only when REDUNDANCY_SCOPE=keep)
    and the report, artifacts ci-out/redundancy/*.md and *.json for 30 days. The scope reaches the shell through env:."""
    job = load("nightly.yml")["jobs"]["test-redundancy"]
    assert redundancy_rule_violations(job) == []
    text = "\n".join(runs(job))
    order = ["coverage==7.16.2", "coverage debug sys", "mkdir -p ci-out/redundancy", "zz_coverage_startup.pth",
             '--out ci-out/redundancy-smoke --jobs 2 --only "test_adapter_forms.py" || true',
             "report --data ci-out/redundancy-smoke/data/.coverage", "head -n 14 ci-out/redundancy-smoke/test-redundancy.md",
             'if [ "$REDUNDANCY_SCOPE" = "keep" ]; then', "--jobs 4 --keep-only > ci-out/redundancy/run-log.txt 2>&1 || true",
             "tail -n 5 ci-out/redundancy/run-log.txt", "report --data ci-out/redundancy/data/.coverage",
             "sed -n '/^## A\\./,$p' ci-out/redundancy/test-redundancy.md | head -n 40 || true"]
    at = [text.find(token) for token in order]
    assert -1 not in at and at == sorted(at), dict(zip(order, at))
    upload = next(s for s in job_steps(job) if str(s.get("uses", "")).startswith("actions/upload-artifact"))
    assert upload["with"]["path"].split() == ["ci-out/redundancy/*.md", "ci-out/redundancy/*.json"]
    assert upload["with"]["retention-days"] == 30


def test_the_redundancy_inputs_reach_nightly_by_a_dispatch_and_through_the_canon():
    """The GitLab variables TEST_REDUNDANCY and REDUNDANCY_SCOPE are inputs under the same names (ci_read.py start --var):
    of nightly.yml's dispatch and call, and of canon.yml, which passes them on (an api pipeline with the variable = the
    canon plus the measurement). Empty is the default everywhere: the measurement does not run, the scope is every file."""
    nightly_on = load("nightly.yml")[True]
    for trigger in ("workflow_dispatch", "workflow_call"):
        for key in ("TEST_REDUNDANCY", "REDUNDANCY_SCOPE"):
            assert nightly_on[trigger]["inputs"][key]["default"] == "", (trigger, key)
    canon = load("canon.yml")
    for key in ("TEST_REDUNDANCY", "REDUNDANCY_SCOPE"):
        assert canon[True]["workflow_dispatch"]["inputs"][key]["default"] == "", key
        assert canon["jobs"]["full"]["with"][key] == "${{ inputs.%s }}" % key, key


def test_the_redundancy_rule_pin_can_fail():
    """The negative control: the real job with the measure/ branch dropped, opened to a schedule, chained after the
    skip job, or made blocking is each named by the same check."""
    real = load("nightly.yml")["jobs"]["test-redundancy"]
    mutants = [
        dict(real, **{"if": "github.event_name == 'workflow_dispatch' && inputs.TEST_REDUNDANCY == '1'"}),
        dict(real, **{"if": "github.event_name == 'schedule' || inputs.TEST_REDUNDANCY == '1'"}),
        dict(real, needs="skip-if-unchanged"),
        dict(real, **{"continue-on-error": False}),
    ]
    for mutant in mutants:
        assert redundancy_rule_violations(mutant), mutant.get("if")
