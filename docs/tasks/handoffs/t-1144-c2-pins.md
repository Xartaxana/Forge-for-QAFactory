# t-1144 C2 hand-off (builder)

Branch nobriefs-c2. All transformations of card C2 done, with ONE expected red (below).

## Per transformation (real lines)
- 7 documents git rm: critic-diff-brief, builder-rules, 0.9 brief-common, 0.9 critic-brief, test-diet-brief, test-diet-fold-brief, docs/retro/README.md: done.
- tools/tests/test_role_carriers_one_owner.py: constants CRITIC/TESTING/TESTING_RUN (+ CRIT_21, CRIT_Q6 helpers); OWNER_KEYS per card; POINTERS rows re-pointed or removed per card (the :91 self-reference and all RULES/BRIEF-carrier rows removed; the old RULES->RUNBOOK_7 row became ("docs/TESTING.md", RUNBOOK §7) per card :90); 4 K-TESTPTR rows + designer rule 24 Q13 (d) row; test_negative_control_real_key_in_a_copy deleted; K-REG/K-NOBRIEF block appended at the end (main_documents, forbidden_hits, strip_allowed, scan, MAIN, test_register_sees_the_main_documents, test_no_main_document_names_a_deleted_file, test_deleted_files_stay_untracked, test_no_brief_file_at_the_top_of_docs_tasks, test_forbidden_hits with 14 adversarial rows of section 8). CRLF line endings kept.
- tools/test_handoff_rule_anchors.py: BRIEF, RULES, K3, K_BRIEF removed; test_critic_rule_23_what_comes_back added; test_builder_rules_p11 and the pointer-copy negative control deleted; docstring lines 5-9 updated.
- install_parity_anchors.json:22; test_quarantine.py:51 (FORGE_CARRIERS, STAGED); test_test_quarantine.py:389, 413, 841, 1489, 1613; test_split.py:1843; owns_readers.py:26, :55 (card listed :26, :55; the diff also shows :22 only as part of a hunk header context, no change there); dispatch_gate.py:1870 (STAGED); test_language_sites.py:4: done.

## Expected red (not a defect of C2)
test_no_main_document_names_a_deleted_file[docs/RUNBOOK.md]: docs/RUNBOOK.md:399 (section 9.8) still says "(builder-rules п. 13)". Owned by t-1122 K-DOC (spec E13, precondition P1); C1 does not edit 9.8; RUNBOOK is not in my owns. This is K-NOBRIEF working as designed (E2 window); the wave-1 merge waits for K-DOC.

## Witness (DoD command, from worktree root)
python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_install_parity.py tools/test_test_quarantine.py tools/test_owns_readers.py tools/test_language_sites.py -q

    FAILED tools/tests/test_role_carriers_one_owner.py::test_no_main_document_names_a_deleted_file[docs/RUNBOOK.md]
    1 failed, 780 passed, 2 skipped in 288.70s (0:04:48)
    (assertion detail: hits (399, 'builder-rules'))

## E4 script (full) and output
Script: C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/e4.py (source below).

```python
import json
import pathlib
import subprocess
import sys

W = pathlib.Path("C:/QAFactory/forge-repo/.claude/worktrees/nobriefs-c2")
sys.path.insert(0, str(W / "ai-packages/qa-factory/scripts"))
import selftest  # noqa: E402

OLD = ("plans/builder-rules.md", ".gitlab-ci.yml", "docs/SIBLING_MAP.md", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md")
NEW = ("docs/TESTING.md", ".gitlab-ci.yml", "docs/SIBLING_MAP.md", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md")


def old_text(rel):
    r = subprocess.run(["git", "-C", str(W), "show", "HEAD~1:" + rel], capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""


old = selftest.gate_named_files(extra_texts=[old_text(r) for r in OLD])
new = selftest.gate_named_files(extra_texts=[(W / r).read_text(encoding="utf-8", errors="replace") for r in NEW if (W / r).is_file()])
left = old - (new | {"test_arch_check.py"})
only_new = new - old
layers = json.loads((W / "ai-packages/qa-factory/scripts/tests/test-layers.json").read_text(encoding="utf-8"))
row = layers["keep"]["test_arch_check.py"] if "keep" in layers else None
print("old:", len(old), "new:", len(new))
print("old - (new | test_arch_check.py):", sorted(left))
print("only in new:", sorted(only_new))
print("test_arch_check.py in old:", "test_arch_check.py" in old, "in new:", "test_arch_check.py" in new)
print("test_arch_check.py keep layer:", row and row.get("layer"))
ok = not left and row is not None and row.get("layer") == "data_join"
print("E4:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
```

Output:

    old: 235 new: 234
    old - (new | test_arch_check.py): []
    only in new: []
    test_arch_check.py in old: True in new: False
    test_arch_check.py keep layer: data_join
    E4: PASS

Old texts = HEAD~1 (pre-L-a) blobs of the four old carriers; new = worktree. No name appears only in the new set.

## Files left staged, uncommitted (mechanism paths)
tools/test_quarantine.py, tools/dispatch_gate.py

## Analogs noticed
- docs/RUNBOOK.md:399 as above (the only MAIN hit).
- The ALLOWED sentence of builder.md ends at "FR-57."; sentence end in `strip_allowed` = a period followed by whitespace or end (the sentence holds "TESTING.md"). The per-line scan is mine; the spec says "through its final period".

## Needed beyond the manifest
docs/SIBLING_MAP.md axis 31 table, .claude/agents/builder.md rule 11 text, docs/TESTING.md headings, test-layers.json keep row, critic.md headings (Q6/Q7/Q12/Q13, rules 21-23).
