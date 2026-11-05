"""test_case_role_twins.py - the role texts of node B (t-1675 / t-1679), key presence.

The keys are the phrases the spec t-1675 named BEFORE the run (doc-witness property i); each must stand VERBATIM
(raw text, no whitespace folding) in the file named. K15 and the driver road (N7) are cut by the Lead (t-1677), so
there is no key for them. A NEGATIVE control proves the helper can fail (property iii).

MERGE t-1696: the critic-charter keys of 7d (the focus Then) are gone here: 7d is main's RN1-7 rule, pinned by
test_case_roles_twin_rules.py. D5-B (t-1701, Q-1): 7e (the Then's field exists: K5-K8b) and 7f (one behaviour, one case: K9)
are back in the charter, paid for by cuts of unpinned restatements under the unchanged CHARTER_MAX_BYTES (test_case_merges.py).

Runnable on its own: `python -B scripts/tests/test_case_role_twins.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, check, finish  # noqa: E402

CRITIC = "agents/qa-case-critic.md"
DESIGNER = "agents/qa-case-designer.md"
SLICE_DESIGNER = "references/slices/qa-case-designer/artifact-contract.md"
AUTOMATOR = "agents/qa-automator.md"
CODE_CRITIC = "agents/qa-code-critic.md"
ANALYST = "agents/qa-failure-analyst.md"
CONTRACT = "references/artifact-contract-automation.md"
SLICES = [
    "references/slices/qa-automator/artifact-contract-automation.md",
    "references/slices/qa-code-critic/artifact-contract-automation.md",
]

KEYS = {
    "n1_focus_twin": [
        ("K4", DESIGNER, "its Then is the value kept whole and the field still in focus"),
        ("K4b", SLICE_DESIGNER, "Its `then_oracles` ref is the field's own requirement R, never `unknown`"),
    ],
    "n2_oracle_field": [
        ("K5", CRITIC, "A Then whose value is read from an API response names the field, and you find that field "
                       "in the response shape"),
        ("K6", CRITIC, "oracle_field_absent"),
        ("K7", CRITIC, "the requirement's one expected red, not a case defect"),
        ("K8", CRITIC, "a shape you could not read is a concern marked unverified, never a pass"),
        ("K8b", CRITIC, "unverified: no response shape"),
    ],
    "n3_one_behaviour": [
        ("K9", CRITIC, "a Then whose then_oracles ref is an R-n outside this case's covers, while another case "
                       "covers that R-n, is a finding \"repeats R-n of TC-x\""),
        ("K9b", CRITIC, "Several inputs of ONE requirement in one parametrised case are no repeat"),     # X5-1 (P16)
        ("K9c", CRITIC, "\"one behaviour per case\" is a unit-level rule, not an API/e2e one"),            # X5-1 (P16)
        ("K9d", CRITIC, "how many tests the automator writes for it is its call (P17), never yours"),    # X5-1 (P17)
        ("K10", SLICE_DESIGNER, "A case asserts only its own requirements: a Then whose oracle is an R-n outside covers "
                          "belongs to that R-n's case"),
    ],
    "n4_field_absent_carriers": [
        ("K11", AUTOMATOR, "carries field_absent {then, field, read_from, shape_ref}"),
        ("K12", CONTRACT, "field_absent"),
        ("K12-slice-automator", SLICES[0], "field_absent"),
        ("K12-slice-code-critic", SLICES[1], "field_absent"),
    ],
    "n5_code_critic": [
        ("K13", CODE_CRITIC, "a red whose value was never received names the field in the response shape; "
                             "a field_absent row is accepted red, never called a product bug"),
    ],
    "n6_analyst_and_phase": [
        ("K14", ANALYST, "a field_absent row is judged by its shape_ref, not by the control experiment"),
        ("K14-phase", "skills/qa-story/phases/s7.md", "field_absent"),
    ],
}


def key_present(rel: str, key: str) -> bool:
    """True when `key` stands verbatim in the package file `rel`; prints one line saying which."""
    found = key in (PLUGIN_ROOT / rel).read_text(encoding="utf-8")
    print(f"  key {'present' if found else 'ABSENT '} in {rel}: {key!r}")
    return found


def main() -> None:
    for case, keys in KEYS.items():
        for item, rel, key in keys:
            check(f"{case} {item}: {key!r} stands in {rel}", key_present(rel, key))
    check("negative control: 'zzz-not-in-any-file' is reported ABSENT by the same helper",
          not key_present(CRITIC, "zzz-not-in-any-file"))
    finish("case role twins node B (key presence + negative control)")


if __name__ == "__main__":
    main()
