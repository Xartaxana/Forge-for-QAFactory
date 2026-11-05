"""TQ1-2 (K3): the actor-control rule. Part D is the document witness (keys quoted from the node's DoD before the run,
with a negative control); part T is TC-014 (TP1 MR !719): the mutation "the token is invalid" leaves a test written by
the old rule green and turns a test written by the new rule red.

No pytest, no network, no stand: a temporary git repository, `red_sandbox.prepare`, and a tiny runner.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import PLUGIN_ROOT, check, check_eq, cleanup, finish, temp_dir, temp_project, use_project  # noqa: E402

ROOT = temp_project("qa-factory-actor-control-")
use_project(ROOT)

import red_sandbox as RS  # noqa: E402
import validate_artifacts as V  # noqa: E402

# --- part D: the wording reached the five places that carry it --------------------------------------------------------------
# Keys are quoted verbatim from the DoD of the node; whitespace runs are folded (a sentence may wrap).
D_KEYS = {
    "references/code-review-rubric.md": [
        "the SAME credentials doing an allowed call", "# oracle_unknown: Q<n>", "expectation_unconfirmed",
        "# broad_status: range per R-<n>|Q<n>", "on one mixed Then that same Then", "Verify each marker's R/Q states the range"],
    "agents/qa-case-designer.md": [
        "A permission refusal is two Thens", "allowed call by the SAME account", "`unknown` with its question"],
    "agents/qa-case-critic.md": ["no allowed call by the SAME account", "without the reason code a source names"],
    "references/test-code-patterns.md": [
        "the SAME credentials make an allowed call", "# oracle_unknown: Q<n>", "expectation_unconfirmed",
        "# broad_status: range per R-<n>|Q<n>", "(on one mixed Then, that same Then)", "# broad_status: not a status"],
    "references/slices/qa-automator/test-code-patterns.md": ["the SAME credentials make an allowed call", "expectation_unconfirmed"],
}


def folded(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def missing(text: str, keys: list) -> list:
    """The keys that the (folded) text does not hold; [] when all are there."""
    body = folded(text)
    return [key for key in keys if key not in body]


def read(rel: str) -> str:
    return (PLUGIN_ROOT / rel).read_text(encoding="utf-8")


for rel, keys in D_KEYS.items():
    check_eq(f"D: {rel} holds every key", missing(read(rel), keys), [])

check_eq("D5: the catalog entry is automator-only - the code critic gets the rule from the rubric, not a second copy (A25 weight)",
         missing(read("references/slices/qa-code-critic/test-code-patterns.md"), ["the SAME credentials make an allowed call"]),
         ["the SAME credentials make an allowed call"])
code = json.loads(read("references/judgments.d/code.json"))
narrow = next(j for j in code["judgments"] if j["id"] == "code_narrow_negative")
check_eq("D2: criteria.false names a refusal with no allowed call by the same credentials",
         missing(narrow["criteria"]["false"], ["no allowed call by the same credentials"]), [])
check_eq("D2: criteria.true asks for the allowed call made with the same credentials",
         missing(narrow["criteria"]["true"], ["made with the same credentials"]), [])
check("D2: a range never passes the judge (the calibration line says so)", "A range never passes here" in narrow["calibration"])

designer, critic = folded(read("agents/qa-case-designer.md")), folded(read("agents/qa-case-critic.md"))
# D3 (spec t-1765 X1, register outcome "dropped" - for the critic): the old order `blocked_by_env` < sentence < `Each compound
# obligation` was a step order of the retired role-file procedure. The rule itself ("two Thens") is pinned by D_KEYS above; here
# the sentence only has to stand in the charter's "Where bugs hide" section (the new carrier), before "## Techniques".
check("D3: the designer's sentence stands in the charter section `Where bugs hide at this stage` (order pin dropped)",
      designer.index("## Where bugs hide at this stage") < designer.index("allowed call by the SAME account") < designer.index("## Techniques"))
check("D4: the critic's sentence stands after `however well the steps read.` and before `Across those dimensions`",
      critic.index("however well the steps read.") < critic.index("no allowed call by the SAME account") < critic.index("Across those dimensions"))
rubric = folded(read("references/code-review-rubric.md"))
check("D1: the rubric sentence is in dimension 2 (before dimension 3)",
      rubric.index("the SAME credentials doing an allowed call") < rubric.index("3. **Waits and stability**"))

# D-neg: the same check on a text with one key cut out reports it missing (the check can fail).
cut = read("references/code-review-rubric.md").replace("the SAME credentials doing an allowed call", "an allowed call")
check_eq("D-neg: a rubric without the key reports it missing",
         missing(cut, D_KEYS["references/code-review-rubric.md"]), ["the SAME credentials doing an allowed call"])

# --- part T: TC-014 ----------------------------------------------------------------------------------------------------------------
PRODUCT = '''\
VALID = {"tok-readonly", "tok-admin"}


def call(token, method, path):
    if token not in VALID:
        return 401
    if method == "GET":
        return 200
    if method == "POST" and path.endswith("/validate"):
        return 403
    return 404
'''
ACCOUNTS = 'READONLY_TOKEN = "tok-readonly"\nADMIN_TOKEN = "tok-admin"\n'
MUTATED_ACCOUNTS = 'READONLY_TOKEN = "tok-expired"\nADMIN_TOKEN = "tok-admin"\n'
HEAD = "from accounts import ADMIN_TOKEN, READONLY_TOKEN\nfrom product import call\n\n\n"
REFUSAL = 'status = call(READONLY_TOKEN, "POST", "/v1/workflows/w1/validate")\n    assert 400 <= status < 500  # oracle_unknown: Q4\n'
CONTROL = 'assert call({token}, "GET", "/v1/workflows/w1") == 200\n    '
TESTS = {
    "test_old_rule.py": HEAD + "def test_refused_TC_014():\n    " + REFUSAL,
    "test_new_rule.py": HEAD + "def test_refused_TC_014():\n    " + CONTROL.format(token="READONLY_TOKEN") + REFUSAL,
    "test_new_rule_fixture.py": HEAD + 'def readonly_session():\n    assert call(READONLY_TOKEN, "GET", "/v1/workflows/w1") == 200\n'
                                      "    return READONLY_TOKEN\n\n\ndef test_refused_TC_014():\n    readonly_session()\n    " + REFUSAL,
    "test_other_account.py": HEAD + "def test_refused_TC_014():\n    " + CONTROL.format(token="ADMIN_TOKEN") + REFUSAL,
}
RUNNER = '''\
import importlib
import sys

module = importlib.import_module(sys.argv[1])
failed = 0
for name in sorted(vars(module)):
    if name.startswith("test_") and callable(getattr(module, name)):
        try:
            getattr(module, name)()
            print("PASS", name)
        except AssertionError:
            failed += 1
            print("FAIL", name)
sys.exit(1 if failed else 0)
'''


def run(cwd: Path, module: str) -> int:
    done = subprocess.run([sys.executable, "-B", "run.py", module], cwd=str(cwd), capture_output=True, text=True, timeout=60,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return done.returncode


repo = temp_dir("qa-actor-control-repo-")
sandbox_root = temp_dir("qa-actor-control-sbx-")
try:
    subprocess.run(["git", "init", "-q"], cwd=str(repo), capture_output=True, timeout=60)
    (repo / "product.py").write_text(PRODUCT, encoding="utf-8")
    (repo / "accounts.py").write_text(ACCOUNTS, encoding="utf-8")
    (repo / "run.py").write_text(RUNNER, encoding="utf-8")
    for name, body in TESTS.items():
        (repo / name).write_text(body, encoding="utf-8")
    check_eq("T0: on the unmutated repository all four modules pass",
             [run(repo, name[:-3]) for name in TESTS], [0, 0, 0, 0])

    control_line = next(i for i, line in enumerate(TESTS["test_new_rule.py"].splitlines(), start=1) if "== 200" in line)
    request = {"mutations": [{
        "path": "accounts.py", "before_sha256": RS.digest(repo / "accounts.py"), "replacement_utf8": MUTATED_ACCOUNTS,
        "instance_id": "TC-014", "expected_location": f"test_new_rule.py:{control_line}", "expected_reason": "assert 401 == 200"}]}
    receipt = RS.prepare(repo, sandbox_root / "sbx", request)
    sandbox = Path(receipt["sandbox"])
    check_eq("T-prepare: the sandbox is prepared with the token mutated", receipt["status"], "prepared")
    check("T-prepare: the sandbox holds the mutated bytes", "tok-expired" in (sandbox / "accounts.py").read_text(encoding="utf-8"))
    check_eq("T1: the test written by the old rule SURVIVES the dead token (4xx is 4xx)", run(sandbox, "test_old_rule"), 0)
    check_eq("T2: the test with the allowed call by the same credentials FAILS", run(sandbox, "test_new_rule"), 1)
    check_eq("T3: ... and so does the one whose control lives in a fixture function", run(sandbox, "test_new_rule_fixture"), 1)
    check_eq("T4: a control by ANOTHER account does not catch the mutation (hence the SAME)", run(sandbox, "test_other_account"), 0)

    # T5 (cut by X7-2): `check_test_code` is gone; a broad status line is the code critic's to judge (rubric CRR 2), not a refusal.
    check_eq("T5: the validator has no test-code check any more", hasattr(V, "check_test_code"), False)
finally:
    cleanup(repo)
    cleanup(sandbox_root)
    cleanup(ROOT)

finish("test_actor_control_rule")
