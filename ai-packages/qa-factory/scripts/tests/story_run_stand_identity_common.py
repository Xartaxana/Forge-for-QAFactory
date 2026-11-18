#!/usr/bin/env python3
"""The stand's BUILD question (t-300 N1b): `Driver.build_check`, the variants of its text, the closed answers and the
`take_answer` branch, by the driver in this process with `claude` replaced by the stub.

Two rigs. The FAKE one registers a probe script named `runtime_probe.py` that prints the record a test put in
`records.json` (so every shape of record the real ladder can print is reachable without docker) and logs the argv it was
run with. The REAL one registers the package's own `runtime_probe.py` over a git checkout with two commits and NO
container, so the ladder runs for real (the registry, a person's word, a `command` row) and a person's answer changes
what the next probe reads - the pair driver <-> probe is exercised end to end.

Keys: K35 the question and its texts (every variant obeys references/human-questions.md), K36 the answers, K37 the
positions and the flag, K38 the `confirm` variant, K39 what is a line and not a question, K40 one question per profile,
K44 a labelled stand asks nothing; plus the edges of the node spec (per window, per dispatch scope, `--task-root`, the
closed forms at and beyond their limits, a commit that is not the story's, a stand the config no longer has).

Mutations this file kills (each by this file alone, run on a scratch copy of the package):
  the question is asked although the record is `matched` (M8) | a free-text answer is read by code as a form (M9) |
  the driver shows the script line to the person (M10)

Run: each part alone, python -B scripts/tests/test_story_run_stand_identity_<k35_k36|t366_k37|k38_edges|ep1>.py
"""
# Shared helpers of test_story_run_stand_identity.py, split by tools/test_split.py (TD-11c).
import contextlib
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from story_run_common import d2_answer, d2_driver, d2_enter, d2_seed, s0_journal, s0_state


HEAD = "e" * 6 + "0" * 34


OLD = "a1b2c3" + "0" * 34


NOWHERE = "9" * 40


TS = "2026-10-03T09:00:00+00:00"


LABEL = "org.opencontainers.image.revision"


DIGEST = "image:sha256:" + "b" * 64


PY = Path(sys.executable).as_posix()


FAKE_PROBE = r'''
import json, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent
args = sys.argv[1:]
profile = args[args.index("--profile") + 1]
with (here / "calls.jsonl").open("a", encoding="utf-8") as handle:
    handle.write(json.dumps({"profile": profile, "argv": args}) + "\n")
mode = json.loads((here / "records.json").read_text(encoding="utf-8")).get(profile)
if mode == "__fail__":
    sys.exit(3)
if mode == "__nojson__":
    print("this is not json")
    sys.exit(0)
if mode == "__hang__":
    time.sleep(60)
print(json.dumps(mode))
'''


WRAPPED_PROBE = r'''
import contextlib, io, json, sys
sys.path.insert(0, r"@SCRIPTS@")
import runtime_probe as R
out = io.StringIO()
with contextlib.redirect_stdout(out):
    code = R.main()
record = json.loads(out.getvalue())
record["container"] = record.get("container") or "ui-c"
print(json.dumps(record))
sys.exit(code)
'''


_PLAN: dict = {}


def use_plan(rows: dict) -> None:
    """The plan's rows as `gate_preflight.plan_rows_of` reads them: {case: (profile, disposition)}. The real keying of a row to
    a profile (`s5_profiles`, N1a's K32) runs; only the reading of work/test-plan.json is replaced."""
    import gate_preflight
    _PLAN.clear()
    _PLAN.update(rows)

    def rows_of(task_root, dispositions):
        return [(case, {"execution_profile_id": profile, "disposition": disposition})
                for case, (profile, disposition) in _PLAN.items() if disposition in dispositions]
    gate_preflight.plan_rows_of = rows_of


class Rig:
    """A seeded project (S0 done, controller initialised, stand `localhost` CONFIRMED) with profiles, a registered probe per
    profile and a checkout; the driver is built after the config is final (a Driver reads it once)."""

    def __init__(self, profiles=("api", "e2e-ui"), real=False, foreign=False, timeout=30, task="QA-9", host=False):
        """`real`: the package's own probe. Since EP1-28 a probe that names no container asks the `no_container` question, so
        the REAL rig runs the probe through a thin wrapper that only puts a container NAME in the record (the ladder is the real
        one, docker is not asked): the `how` question and its label / file / command answers stay what these tests are about.
        `host=True`: no wrapper, the plain probe with no container (the application runs on the host)."""
        self.task, self.real, self.profiles = task, real, profiles
        self.root, self.task_root, self.env = d2_seed(task, environment="localhost", pending=False, stands=("localhost",))
        self.config_path = self.root / "qa-factory" / "config.json"
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        cfg["environments"] = [{"name": "localhost", "base_url": "http://localhost:8080", "frontend_url": "http://localhost:5173"}]
        cfg["profiles"] = [{"profile_id": p, "capabilities": [p]} for p in profiles]
        cfg["implementation_repos"] = [{"repo_id": f"repo-{p}", "local_path": "ui", "execution_profile_id": p} for p in profiles]
        self.fake = self.root / "fake-probe"
        probes = {}
        if real:
            self.git_checkout()
            head = ["{python}", "{plugin_root}/scripts/runtime_probe.py"]
            if not host:
                wrapper = self.root / "wrapped-probe"
                wrapper.mkdir()
                (wrapper / "runtime_probe.py").write_text(WRAPPED_PROBE.replace("@SCRIPTS@", str(harness.SCRIPTS)), encoding="utf-8")
                head = [sys.executable, str(wrapper / "runtime_probe.py")]
            for p in profiles:
                probes[p] = {"argv": [*head, "--profile", p, "--environment", "localhost",
                                      "--checkout", "ui", "--app-root", "/app"], "cwd": ".", "timeout_s": 60}
        else:
            self.fake.mkdir()
            self.script = self.fake / ("probe_check.py" if foreign else "runtime_probe.py")
            self.script.write_text(FAKE_PROBE, encoding="utf-8")
            self.records()
            for p in profiles:
                probes[p] = {"argv": [sys.executable, str(self.script), "--profile", p, "--environment", "localhost"], "cwd": ".",
                             "timeout_s": timeout}
        cfg.setdefault("execution", {})["runtime_probes"] = probes
        self.config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        self.cfg = cfg

    def git_checkout(self) -> None:
        ui = self.root / "ui"
        ui.mkdir()

        def git(*args):
            return subprocess.run(["git", "-c", "user.email=t@example.invalid", "-c", "user.name=t", *args], cwd=str(ui),
                                  capture_output=True, text=True, check=True).stdout.strip()
        git("init", "-q")
        git("commit", "--allow-empty", "-q", "-m", "one")
        self.old = git("rev-parse", "HEAD")
        git("commit", "--allow-empty", "-q", "-m", "two")
        self.head = git("rev-parse", "HEAD")
        self.git = git

    def records(self, **by_profile) -> None:
        (self.fake / "records.json").write_text(json.dumps(by_profile), encoding="utf-8")

    def calls(self) -> list:
        path = self.fake / "calls.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []

    def driver(self, **kw):
        return d2_driver(self.root, self.env, self.task, **kw)

    def command_script(self, sha: str) -> list:
        """A registry `command` that prints `sha` - a way a person would give; python itself reads nothing from docker."""
        path = self.root / f"sha-{sha[:6]}.py"
        path.write_text(f"print('{sha}')\n", encoding="utf-8")
        return [sys.executable, str(path)]

    def registry(self) -> Path:
        return self.root / "qa-factory" / "records" / "stand-identity.json"

    def rows(self) -> list:
        return json.loads(self.registry().read_text(encoding="utf-8"))["rows"] if self.registry().is_file() else []

    def confirmations(self) -> list:
        path = self.task_root / "state" / "stand-confirmations.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.is_file() else []

    def put_row(self, method: str, profile: str = None, **extra) -> None:
        import stand_identity as SI
        SI.append_row(self.root, SI.make_row(self.cfg, "localhost", profile or self.profiles[0], method, words="my own words", **extra))

    def sha(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "absent"

    def done(self) -> None:
        harness.cleanup(self.root)


def record(profile, result, **extra) -> dict:
    out = {"profile_id": profile, "timestamp": TS, "environment_id": "localhost", "expected_source_revision": HEAD,
           "observed_runtime_identity": "", "evidence_refs": [], "provenance": {"technical_verification": False},
           "result": result, "comparisons": [], "container": "ui-c", "checkout": "ui"}
    out.update(extra)
    return out


def matched(profile, kind="oci_label", linkage="exact") -> dict:
    return record(profile, "matched", observed_runtime_identity=DIGEST, observed_without_evidence=True,
                  provenance={"technical_verification": True, "source_linkage": linkage, "identity_kind": kind,
                              "deployed_source_revision": HEAD, "verified_source_revisions": [HEAD]})


def unknown(profile, asks="how", **extra) -> dict:
    base = dict(error="which build the stand runs could not be read: no container is named for this profile",
                tried=[{"method": "docker", "outcome": "no container is named for this profile"}], remedy="label the image")
    if asks:
        base["asks_person"] = asks
    base.update(extra)
    return record(profile, "unknown", **base)


def mismatched(profile, **extra) -> dict:
    base = dict(build_sha=OLD, observed_runtime_identity=DIGEST, observed_without_evidence=True,
                provenance={"technical_verification": True, "source_linkage": "exact", "identity_kind": "oci_label",
                            "deployed_source_revision": OLD, "verified_source_revisions": [HEAD]})
    base.update(extra)
    return record(profile, "mismatched", **base)


def sources_mismatched(profile, files) -> dict:
    return record(profile, "mismatched", differing_files=files, observed_runtime_identity="verified_content:abc",
                  provenance={"technical_verification": True, "source_linkage": "verified_content",
                              "deployed_source_revision": "content_mismatch", "verified_source_revisions": [HEAD]})


def run_entry(rig, words=None, stage="S5", built=None, **kw):
    """One driver process: an answer taken first when `words` is given, then one entry into the stage. `built` is a driver
    already made (the 4-tuple of `d2_driver`). (exit code, stdout, roles started, the driver)."""
    if words is None:
        reset_question(rig)         # an entry with no answer is a NEW process with no question the person has not answered
    if built is None:
        extra = dict(kw)
        if words is not None:
            extra["answer"] = d2_answer(rig.root, words)
        built = rig.driver(**extra)
    driver, started = built[0], built[1]
    if stage == "S6":
        driver_stub(driver)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = d2_enter(driver, stage)
    return code, out.getvalue(), started, driver


def reset_question(rig) -> None:
    """The state of a driver process that starts with no question open: the open question, its file and its flag are gone
    (the person answered it, or this is the first run). Everything else of the story is as it was."""
    path = rig.task_root / "state" / "driver-state.json"
    if path.is_file():
        state = json.loads(path.read_text(encoding="utf-8"))
        state["asked"] = {}
        state.pop("build_question", None)
        state.pop("stand_question", None)
        path.write_text(json.dumps(state), encoding="utf-8")
    question = rig.task_root / "state" / "driver-question.md"
    if question.is_file():
        question.unlink()


def asked(rig) -> dict:
    return s0_state(rig.task_root).get("asked") or {}


def flag(rig) -> dict:
    return s0_state(rig.task_root).get("build_question") or {}


def journal_answers(rig) -> list:
    return [str(e.get("notes")) for e in s0_journal(rig.root) if e.get("event") == "human_answer"]


def line_broken(text: str) -> list:
    """The shape rules of references/human-questions.md for one printed line (a status is not a whole question)."""
    import human_text
    return [p["rule"] for p in human_text.problems(text) if p["rule"] not in ("filler", "too_short", "no_how_to_answer")]


def driver_stub(driver) -> None:
    """S6 reads the stand's freshness through the registered probe too (R4); this file is about the build question, so the
    freshness read is replaced for the entry that follows."""
    driver.s6_freshness = lambda cases: {"decided": False, "why": "stub", "stand": [], "run": {}, "passed": 0, "failed": 0}
