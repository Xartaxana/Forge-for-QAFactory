"""Focused external receipt import and semantic red-proof checks."""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok)); print(("PASS " if ok else "FAIL ") + name); return bool(ok)


def check_eq(name, got, expected):
    return check(name, got == expected)


def finish(label):
    bad = len(RESULTS) - sum(RESULTS); print(f"=== {label}: {sum(RESULTS)}/{len(RESULTS)} ok ===")
    raise SystemExit(1 if bad else 0)
from execution_fingerprint import file_hash  # noqa: E402
from import_test_receipt import (ImportError, _copy_evidence, import_receipt, receipt_digest,
                                 validate_import_block)  # noqa: E402
from red_sandbox import verify  # noqa: E402

# Outside the package: a local-directory marketplace copies whatever lies in it.
ROOT = Path(tempfile.mkdtemp(prefix="qa-receipt-import-"))


def request() -> dict:
    return {"task": "IMP-1", "revision": "r1", "dispatch_id": "d1", "profile_id": "local",
        "purpose": "initial", "selected_instance_ids": ["i1"], "current_scope_instance_ids": ["i1"],
        "input_fingerprint": "f" * 64, "fingerprint_files": [{"path": str(ROOT / "test.py"),
        "sha256": file_hash(ROOT / "test.py"), "kind": "test_files"}],
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


def signed_receipt(req: dict) -> dict:
    from import_test_receipt import _binding
    value = {"schema_version": 1, "producer": {"kind": "ci", "id": "pipeline", "system": "CI",
        "run_id": "42", "adapter_id": "ci-json", "adapter_version": "1"},
        "binding": _binding(req), "reporter": "pytest", "execution_status": "passed",
        "started_at": "2026-09-17T10:00:00Z", "ended_at": "2026-09-17T10:01:00Z",
        "evidence": [{"path": "report.xml", "sha256": file_hash(ROOT / "report.xml")}],
        "results": [{"test_id": "suite::one", "status": "passed", "reason": ""}]}
    value["receipt_sha256"] = receipt_digest(value)
    return value


def rejects(req, receipt) -> bool:
    try:
        import_receipt(req, receipt, ROOT, ROOT / "out")
        return False
    except (ImportError, ValueError):
        return True


def main():
    shutil.rmtree(ROOT, ignore_errors=True); ROOT.mkdir(); (ROOT / "test.py").write_text("# test\n")
    (ROOT / "report.xml").write_text("<testsuite/>")
    config = {"profiles": [{"profile_id": "local", "adapter_id": "ci-json", "adapter_version": "1",
        "extensions": {"external_receipts": {"enabled": True, "producer_id": "pipeline", "system": "CI"}}}]}
    (ROOT / "qa-factory").mkdir()
    (ROOT / "qa-factory/config.json").write_text(json.dumps(config))
    try:
        req = request(); receipt = signed_receipt(req)
        first = import_receipt(req, receipt, ROOT, ROOT / "out")
        second = import_receipt(req, receipt, ROOT, ROOT / "out")
        check_eq("exact external receipt imports once", first["status"], "imported")
        check_eq("same receipt import is idempotent", second["status"], "reused")
        block = json.loads(Path(first["run_block"]).read_text())
        check_eq("instance parameters survive normal block pipeline", block["results"][0]["parameters"], {"region": "eu"})
        check_eq("durable imported block validates", validate_import_block(ROOT, block), [])
        changed_block = copy.deepcopy(block)
        changed_block["results"][0]["status"] = "failed"
        check("reader rejects a result row changed after receipt import",
              "import block execution payload does not match its receipt"
              in validate_import_block(ROOT, changed_block))
        changed_evidence = copy.deepcopy(block)
        changed_evidence["import_provenance"]["evidence"][0]["sha256"] = "0" * 64
        evidence_errors = validate_import_block(ROOT, changed_evidence)
        check("reader rejects durable evidence mapping changed after import",
              "durable evidence does not exactly match receipt evidence" in evidence_errors)
        durable = ROOT / block["import_provenance"]["evidence"][0]["path"]
        check("reporter evidence is copied away from mutable source", durable.is_file() and durable != ROOT / "report.xml")
        check("durable hierarchy uses compact collision-checked filesystem keys",
              len(durable.parent.parent.name) == 22 and len(durable.stem) == 22
              and block["import_provenance"]["receipt_sha256"] == receipt["receipt_sha256"])
        # Exercise atomic copying at a long clean-export-like parent using the production
        # compact target shape; the deliberately overlong legacy shape is compared below.
        long_parent = ROOT / "out" / ("p" * 70)
        long_target = long_parent / (("h-" + "a" * 20) + ".xml")
        long_source = ROOT / "long-report.xml"
        long_source.write_text("<testsuite/>")
        long_hash = file_hash(long_source)
        _copy_evidence(long_source, long_target, long_hash)
        check("atomic temp naming does not extend a long hash target",
              long_target.is_file() and not any(p.name.startswith(".h-" + "a" * 20)
                                                for p in long_parent.iterdir()))
        clean_prefix = Path("C:/Users/user/AppData/Local/Temp/qa-factory-release-12345678"
                            "/ai-packages/qa-factory/.receipt-import-test/out")
        legacy_target = clean_prefix / "imports" / ("a" * 64) / "evidence" / (("b" * 64) + ".xml")
        compact_target = clean_prefix / "imports" / ("i-" + "a" * 20) / "e" / (("h-" + "b" * 20) + ".xml")
        check("compact durable layout fits where clean-export legacy layout was too long",
              len(str(legacy_target)) > len(str(compact_target)) + 80
              and len(str(compact_target)) < 240)
        (ROOT / "report.xml").unlink()
        third = import_receipt(req, receipt, ROOT, ROOT / "out")
        check_eq("durable exact import reuses after source retention ends", third["status"], "reused")
        (ROOT / "report.xml").write_text("<testsuite/>")
        tampered = copy.deepcopy(receipt); tampered["results"][0]["status"] = "failed"
        check("tampered signed receipt is rejected", rejects(req, tampered))
        wrong_scope = copy.deepcopy(receipt); wrong_scope["binding"]["selected_instance_ids"] = ["other"]
        wrong_scope["receipt_sha256"] = receipt_digest(wrong_scope)
        check("signed but wrong approved scope is rejected", rejects(req, wrong_scope))
        claim = copy.deepcopy(receipt); claim["execution_status"] = "green"
        claim["receipt_sha256"] = receipt_digest(claim)
        check("claimed CI green is not a machine result", rejects(req, claim))
        unknown = copy.deepcopy(receipt); unknown["producer"]["adapter_id"] = "unknown"
        unknown["receipt_sha256"] = receipt_digest(unknown)
        check("unknown adapter cannot manufacture green", rejects(req, unknown))
        inconsistent = copy.deepcopy(receipt); inconsistent["execution_status"] = "failed"
        inconsistent["receipt_sha256"] = receipt_digest(inconsistent)
        check("failed execution with only passed rows is rejected", rejects(req, inconsistent))
        malformed_time = copy.deepcopy(receipt); malformed_time["ended_at"] = "not-a-time"
        malformed_time["receipt_sha256"] = receipt_digest(malformed_time)
        check("malformed timestamps are rejected", rejects(req, malformed_time))
        durable.write_text("tampered")
        check("reader detects tampered durable reporter evidence", bool(validate_import_block(ROOT, block)))
        author = ROOT / "author.py"; author.write_text("assert actual == expected\n")
        base = {"repo": str(ROOT), "original_hashes": {"author.py": hashlib.sha256(author.read_bytes()).hexdigest()},
            "targets": [{"instance_id": "i1", "obligation_id": "REQ-1", "defect_location": "src/app.py:8",
            "assertion_id": "assert-total", "expected_location": "author.py:1", "expected_reason": "total differs"}]}
        setup = [{"instance_id": "i1", "status": "failed", "failure_kind": "setup", "obligation_id": "REQ-1",
            "defect_location": "src/app.py:8", "assertion_id": "assert-total", "location": "author.py:1",
            "reason": "total differs", "semantic_verdict": "intended_failure"}]
        check_eq("wrong-red setup failure remains incomplete", verify(base, setup)["status"], "incomplete")
        wrong_binding = copy.deepcopy(setup); wrong_binding[0]["failure_kind"] = "assertion"; wrong_binding[0]["assertion_id"] = "mock-called"
        check_eq("wrong assertion identity remains incomplete", verify(base, wrong_binding)["status"], "incomplete")
    finally: shutil.rmtree(ROOT, ignore_errors=True)
    finish("test_import_test_receipt")


if __name__ == "__main__": main()
