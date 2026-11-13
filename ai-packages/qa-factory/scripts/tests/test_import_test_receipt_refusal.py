"""t-420: the role runs `import_test_receipt.py` by hand; whatever the input, it gets a refusal (exit 2, the named problem), never a
Python traceback with exit 1, and not a byte is written under the story. One parameterised test, one subprocess per case.
Run: python -B -m pytest scripts/tests/test_import_test_receipt_refusal.py -q"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from execution_fingerprint import file_hash  # noqa: E402
from import_test_receipt import _binding, receipt_digest  # noqa: E402

PHANTOM = "NO-SUCH-STORY"


def request(root: Path, task: str = "IMP-1") -> dict:
    return {"task": task, "revision": "r1", "dispatch_id": "d1", "profile_id": "local",
        "purpose": "initial", "selected_instance_ids": ["i1"], "current_scope_instance_ids": ["i1"],
        "input_fingerprint": "f" * 64, "fingerprint_files": [{"path": str(root / "test.py"),
        "sha256": file_hash(root / "test.py"), "kind": "test_files"}],
        "fingerprint_components": {"source_sha": "a" * 40, "test_content_sha": "b" * 64,
        "helper_sha": "h" * 64, "config_sha": "c" * 64, "toolchain_sha": "t" * 64},
        "runtime_required": False, "target_kind": "local_source", "runtime_provenance": {
        "profile_id": "local", "result": "not_applicable", "environment_id": "dev-1",
        "timestamp": "2026-09-17T10:00:00Z",
        "expected_source_revision": "src", "observed_runtime_identity": "local-tree",
        "evidence_refs": ["tree"], "provenance": {"technical_verification": True,
        "source_linkage": "exact", "deployed_source_revision": "src"}},
        "reason": "import", "remaining_budget": 0, "idempotency_key": "external-1", "freshness": "fresh",
        "command": {"argv": ["never-executed"], "cwd": ".", "scope": "selected", "reporter": "pytest",
        "selector_contract_verified": True, "selector_args": {"i1": ["node::one"]}},
        "instance_contracts": {"i1": {"report_test_id": "suite::one", "parameters": {"region": "eu"}}}}


def signed_receipt(req: dict, root: Path) -> dict:
    value = {"schema_version": 1, "producer": {"kind": "ci", "id": "pipeline", "system": "CI",
        "run_id": "42", "adapter_id": "ci-json", "adapter_version": "1"},
        "binding": _binding(req), "reporter": "pytest", "execution_status": "passed",
        "started_at": "2026-09-17T10:00:00Z", "ended_at": "2026-09-17T10:01:00Z",
        "evidence": [{"path": "report.xml", "sha256": file_hash(root / "report.xml")}],
        "results": [{"test_id": "suite::one", "status": "passed", "reason": ""}]}
    value["receipt_sha256"] = receipt_digest(value)
    return value


# case id -> (request file, receipt file, needle in stderr); "absent" is a path that does not exist
CASES = {
    "missing request file": ("absent.json", "rc.json", "absent.json"),
    "broken request JSON": ("req-broken.json", "rc.json", "Expecting"),
    "request is a JSON list": ("req-list.json", "rc.json", "'list' object has no attribute 'get'"),
    "receipt the importer refuses": ("req.json", "rc-bad.json", "receipt_sha256 does not match"),
    "story that does not exist": ("req-phantom.json", "rc.json", PHANTOM),
}


@pytest.mark.parametrize("case", list(CASES))
def test_the_cli_refuses_in_a_line_never_in_a_traceback(case, tmp_path):
    root = tmp_path
    (root / "test.py").write_text("# test\n")
    (root / "report.xml").write_text("<testsuite/>")
    config = {"profiles": [{"profile_id": "local", "adapter_id": "ci-json", "adapter_version": "1",
        "extensions": {"external_receipts": {"enabled": True, "producer_id": "pipeline", "system": "CI"}}}]}
    (root / "qa-factory").mkdir()
    (root / "qa-factory" / "config.json").write_text(json.dumps(config))
    story = root / "qa-factory" / "artifacts" / "IMP-1"
    story.mkdir(parents=True)
    req = request(root)
    receipt = signed_receipt(req, root)
    tampered = json.loads(json.dumps(receipt))
    tampered["results"][0]["status"] = "failed"
    (root / "req.json").write_text(json.dumps(req))
    (root / "req-phantom.json").write_text(json.dumps(request(root, PHANTOM)))
    (root / "req-list.json").write_text("[]")
    (root / "req-broken.json").write_text("{not json")
    (root / "rc.json").write_text(json.dumps(receipt))
    (root / "rc-bad.json").write_text(json.dumps(tampered))
    request_name, receipt_name, needle = CASES[case]
    before = sorted(p.relative_to(story).as_posix() for p in story.rglob("*"))
    done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "import_test_receipt.py"), "--request",
                           str(root / request_name), "--receipt", str(root / receipt_name), "--project-root", str(root)],
                          capture_output=True, text=True, cwd=root, encoding="utf-8",
                          env={**os.environ, "CLAUDE_PROJECT_DIR": str(root)})
    assert done.returncode == 2, done.stdout + done.stderr
    assert needle in done.stderr, done.stderr
    assert "Traceback" not in done.stdout + done.stderr
    if case == "story that does not exist":
        assert done.stderr.lstrip().startswith("import_test_receipt.py"), done.stderr
    assert sorted(p.relative_to(story).as_posix() for p in story.rglob("*")) == before
