# t-154 — critic gate on OF3-1 node a (builder t-148, commit e61efb8, branch wip/of3-1a)

Critic (Opus), 12.11.2026. Spec: `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` (node a = items 1, 2, 3a, 4, the `covers` edits).
Diff read with `git -C .claude/worktrees/of3-1a show e61efb8` (10 files, +506/-55).

## Verdict

**FIX ROUND** (accept with fixes; no blocker). The catalogue, the derived `KEYS`, the damage branch, the removal of the dead keys and R1
match the spec, and the control re-runs reproduce the witness. Two must-findings remain. F1: `value()` on a registry row always reads
`unknown` with an empty problem (this is builder question Q1; it is a spec defect, and the Lead picks the fix). F2: two rows have
`needed_by: []`, which contradicts §2. One of them (`dod`) has a reader the builder missed. The other (`format_changed`) has no reader
at all, so it needs an owner node. The minors can go into the same fix round.
Acceptance stays with the coordinator (Opus coordinator, builder diff: this verdict is the critic input the matrix needs).

## Findings

1. **must** — `scripts/project_knowledge.py:328`, `:346`. `value(root, key, environment="", cfg=None)` delegates a registry row to
   `state(root, key, environment, "", cfg)`. `state()` with element `""` gives `_form(key, "") == ""`, so `_latest` returns None and
   the result is `unknown`. `_account_state` with element `""` finds no candidate and also returns `unknown`. The `problem` field is
   only the registry's load problem: `""` on a healthy registry.
   Concrete case: a registry that holds `product.roles` element `auditor` in state `known`. `PK.value(root, "product.roles")` returns
   `{"value": None, "state": "unknown", "source": "", "problem": ""}`. That is a silent unknown that does not name what it could not
   establish (FR-41/FR-59). Separately, a `known` registry fact would still carry `value: None`, because `state()['row']` is dropped.
   The test `test_project_knowledge.py:895` pins the always-unknown outcome as the expected behaviour.
   Fix (my recommendation for Q1): add a trailing keyword `element=""` to `value()` and pass it to `state()`. A registry row with
   `element == ""` returns `unknown` with the problem "a registry fact is per element: name the element". A found row puts its stored
   `value` into `value`. Rewrite the :895 test as two rows: a known element, and the empty-element problem.
   Why this is safe: the signature change has no caller yet. The grep for `PK.value(` / `project_knowledge.value(` outside tests is
   empty; its positive control, `PK.state(`, does find callers. The direction stays toward unknown.
   Whose decision: the spec's §3 signature cannot do what §3 asks for. That is a dispatcher-side spec defect, so the Lead chooses.
   Keeping the current signature is acceptable only if the empty-element problem text is added.

2. **must (coordinator/Lead)** — `references/config-keys.json:751` (`format_changed`) and `:754` (`dod`) carry `needed_by: []`. §2
   says the field is "non-empty". By the spec's own R3 (node f), both rows will turn red, and R3's door says "add the reader, or move
   the key to `removed`".
   - `dod`: "no reader found" is only partly true. The key has `absent_means: required` and `project_fact: true` (config-keys.json
     :194-197). `readiness.py` reads it generically through the keys table: `_optional_top_keys` at readiness.py:907-913 excludes it,
     so it is a required key. `config_contract.not_filled` (:1624) also reads it, via `project_fact`. These readers check presence by
     table, not by name. Moving `dod` to `removed` would be wrong.
   - `format_changed`: a case-insensitive grep over the whole package (`*.py`, `*.md`, `*.json`) finds no reader. The only hits are
     the onboarding phases that WRITE it and two tests. Its positive control, the same call for `format_all|records_policy`, does find
     its hits. So `format_changed` is produced and never read (AR-22). The p2-interview text still calls it "the only formatting a
     role may run", but no role brief carries it. This is the same class as the `format_all` key the owner removed.
   Fix: in the fix round, give `dod` the reader entries `readiness.py:_optional_top_keys` and `config_contract.py:not_filled`. The
   coordinator files a finding for `format_changed` with an owner question (remove it like `format_all`, or wire it into the S5/S8
   brief) and gives it a node line before node f. Node f's spec must also say how R3 counts a presence-only reader that reads by
   table (data-driven): R2's AST scan by name cannot back one. Without that, R3 is red on `dod` by construction.

3. **minor** — `scripts/project_knowledge.py:234` `_stand_roles` vs `:291` `_stand_card`: the same module now has two rules for "the
   stand named N". `_stand_roles` compares `str(e.get("name") or "") == environment`; `_stand_card` compares
   `entry.get("name") == name`.
   Concrete case: `environments: [{"name": 5, "credentials_by_role": {...}, "safe_to_break": "x"}]` with stand `"5"`.
   `state(ACCOUNTS_KEY, "5", ...)` finds the stand. `value("environments[].safe_to_break", "5")` reads "no stand is named 5". This is
   one action by two roads (P31, AR-13). The `needed_by` of `environments[].name` already names both functions.
   Fix: make `_stand_roles` take the stand from `_stand_card(environment, cfg)["entry"]`, or queue it explicitly to N-r1 with that
   pointer. Both directions lean toward unknown, so this is not a blocker.

4. **minor** — `scripts/tests/test_config_migration.py:378`: R1 re-implements the note predicate inline (`not k.endswith("_note")`).
   The same file already has it as `value_keys()` (:59), and the package has `config_contract._is_note` (:1572), which also counts a
   bare `note` key. No top-level `note` key exists today, so the output is correct now.
   Fix: iterate `value_keys()` (or filter with `C._is_note`) inside `knowledge_gaps`.

5. **minor** — `scripts/project_knowledge.py:503`: when the damage came from `config_keys()`, the sentence says the door twice:
   `...damaged (references/config-keys.json of the plugin is unreadable (...); the plugin install is damaged - reinstall the plugin);
   reinstall the plugin; nothing was recorded`. The text is the one §3 prescribes, so it fits the spec, but it reads poorly.
   Fix: optional. Either leave it as specified, or strip a trailing "- reinstall the plugin" from `CATALOGUE_PROBLEM` before
   wrapping it.

6. **minor** — code quality: `_read_catalogue()` re-reads and re-parses `config-keys.json` (about 800 lines) on every `rows()` and
   `value()` call (`:58`, used at `:84` and `:336`), while `KEYS` is a snapshot taken at import (`:101`). There is no hot caller yet,
   so this is not a defect today. Two snapshots of one table, though, can disagree within one process.
   Fix: queue it. When the first loop caller of `value()` arrives (phase 2), read the table once per call site or cache it per process.

7. **minor** — the witness's scope is incomplete. `scenario_walk.py --witness-for` over node a's owns also prints
   `test_scenario_cart_1.py`, `test_scenario_local_1_0108.py`, `test_scenario_local_1_arm_b.py` (slow, `slow_tests.json:118-120`) and
   `test_story_run_monorepo.py` (slow by name). The report's "not run (slow)" line does not list them. Not running them is legitimate
   (they are judged by CI), but they should be named.
   Fix: add the four names to the report's "not run (slow)" line. In the BATCH CANON, read these files' rows.

## Builder deviations judged

- **`_note` template keys get no catalogue row**: accept. A note is factory text with its own `notes` table and rule, not a project
  fact. §2's "one row per top-level template key" is read sensibly as fact keys. The predicate duplication is F4.
- **`format_note` / `records_policy_note` removed from `notes` with no `removed` rows**: accept for this node. Spec item 4 says "follow
  the existing note rule". In an old config, `migration_plan` keeps them as `kept: not a template key` (config_contract.py:1919-1921).
  There is a precedent with the same outcome: `execution_note` and `pre_commit_note` (test_config_migration.py:334-337).
- **An empty `knowledge` object treated as "no section"**: accept. This is the safe direction. An empty section would otherwise give
  `KEYS == {}` with no `CATALOGUE_PROBLEM`, which is exactly the false cause "not a project-knowledge key (the keys: )" that t-142 X-2
  set out to remove.
- **`needed_by: []` for `format_changed` and `dod`**: this contradicts §2's "non-empty". See F2: `dod` is a reader miss, and
  `format_changed` is a real dead key that needs an owner node before f.

## Builder questions

- **Q1** (`value()` and `element`): add a trailing `element=""` keyword and return the row's value. A registry row with an empty
  element reads `unknown` with an explicit problem (F1). Do not keep the signature as it is unless the explicit problem is added. The
  choice belongs to the Lead.
- **Q2** (`removed` rows for stale `format_note` / `records_policy_note`): no, not in this node. A `removed` row pops the note
  unconditionally, including a note text the person edited. Today `settle_note` would move such a text into `answers_legacy`; with a
  `removed` row it would appear only as `was` in the plan. That is a weaker carrier for a person's words (AR-24). The class (a
  retired key's companion note: `execution_note`, `pre_commit_note`, and now these two) needs ONE migration rule: retire a note only
  when its text is in the retired note's `note_history`. That is a change to `config_contract.migration_plan`, outside a's owns.
  Proposed node for the Lead: `config_contract.py` `migration_plan` + a `test_config_migration.py` row; after node f, with OF1-2
  (`config_contract.py`).

## Standing questions (critic-diff-brief)

1. **Fit to the spec**: items 1, 2, 3a and 4 and the `covers` edits are implemented as written, except F1 (§3's registry delegation
   cannot work) and F2 (§2's non-empty `needed_by`). Error direction: `value()` and `environment()` never raise and lean toward
   unknown. All 15 adversarial ids are present, and a stored `""` is `known`. Order (1) no row → (2) registry → (3) config is kept.
   The positional invariant holds: the damage branch sits only on the not-in-`KEYS` branch (:500-503).
2. **The builder's own decisions**: safe direction, judged above. Also: a stored `None` reads `unknown`. §3 is silent on that, and
   `unknown` is the safe side.
3. **Seams**: `report_facts` and `test_gate_role_accounts` are untouched, and the derived `KEYS` matches the literal (the test asserts
   equality, and I re-ran it). The `test-layers.json` edits are `covers` lines only, matching the spec list, and `test_brief_pack`
   already covers `brief_pack.py`. `config_contract.py` is not edited.
4. **Class-wide completeness**: see the class note below.
5. **Tests**: the rows are behaviour rows in existing keep files. The damaged state is an input (patch plus reload), not a source
   mutation. The byte-equal plan row has a negative control, which is a repo-wide practice in test_config_migration and not new here.
   One finding: `test_project_knowledge.py:895` pins the F1 defect as expected. There is no new test file.
6. **DUPLICATION AND CONSISTENCY**: F3 (`_stand_roles` / `_stand_card`) and F4 (the note predicate). `_read` reuses
   `read_config_file` and `rows` reuses `config_keys`. Grepped: `def _stand|def stand_name|environments.*name ==` in project_knowledge
   and stand_gaps; `endswith("_note")|_is_note` in the package. `stand_gaps.stand_name` stays the chooser of "the" stand, as §3 says.
   The clone-ratchet output was not attached. Its baseline is not touched, so CI reads it.
7. **CODE QUALITY**: `value()` runs :328-378 (about 51 lines, 3 levels of nesting), under the cap. There are no dead branches. One
   name shadows a function: the parameter `environment` inside `value()` shadows the module function `environment()`. It is harmless,
   because `_stand_card` is used instead. F6 covers repeated reads whose result nobody needs to recompute.
8. **Hygiene**: `selftest --limits --lang` 4/4 ok in the witness. The new package text is English.
9. **IN-TREE RATCHETS**: none raised. Grepped the diff for `OUTSIDE_WALKS`, `judgment-census`, `dup-baseline` and `KEPT`: no hits.
10. **ARCHITECTURE**: AR-1, AR-3, AR-9, AR-13, AR-22, AR-28 and AR-29 are named, with how each is kept. The rest of the spec's §1 (AR-4,
    AR-14, AR-15, AR-20) belongs to nodes b-f. AR-22 has two gaps: `dod` (a reader miss) and `format_changed` (a produced field with no
    reader), both F2. Producer/reader walk for the removed keys: no reader remains (grep below), and the writers (p2, p4, template) are
    removed in the same commit.
11. **JUDGMENT**: none moved. R1 is set equality of names. There is no census row and no role text, apart from the removal of an ask
    and one optional-key sentence.
12. **ONE ROAD**: F3 is the only two-road instance, and it is a fix of this round or an N-r1 pointer. There is no language, project or
    case exclusion. Grepped the diff for language and runner names: none.

## Class-wide completeness (spec §1 AR rows, SIBLING_MAP)

- Axis 16 (one JSON reader): `project_knowledge._config` is folded through `read_config_file`. The other config readers are nodes b
  and N-r4, already queued.
- Axis 35 (`contract.registry_sides`): it keeps working through the derived `KEYS`. The fold is N-r3, already queued.
- Axis 8 (`artifact_root`): node a only adds the row. The sites are nodes c and d, already queued.
- Axis 34 (P31): F3 is the open sibling inside this artifact.
- The OH3-35 class (a template key nobody reads): `format_changed` is a new, unqueued sibling. It needs an owner node (F2). The note
  companions are a class of their own (Q2), with a proposed node.

## FR walk (checked; the builder's report text was not attached, so this walk is my own)

- A, FR-1: the refusal is byte-equal on a healthy catalogue (test row, re-run) and names the cause and the door on a damaged one.
- B, FR-6: the p2/p4 asks are removed, and the one optional-key sentence is placed where item 4 says.
- C, FR-13: the closed `KEYS` literal is now data rows. FR-14: `value` and `environment` have new output shapes, documented in their
  docstrings.
- D, FR-59 and F, FR-41: these lean toward unknown, except F1's empty problem.
- G, FR-30: lang 4/4. FR-32: tests are present.
- E, FR-37: no path text changed.

## Spot-checks (negatives with positive controls)

- **"config_contract.py needed no edit"**: holds. The file is not in the diff. A case-insensitive `knowledge` grep over
  config_contract.py and readiness.py is empty. The control, `written_by` in the same call shape, hits onboard_apply.py:973.
  `migration_plan` is byte-equal with the section present (R1 row, re-run).
- **"no scripts/ reader of format_all / records_policy / default_environment"**: holds. A case-insensitive grep over the whole package
  (`*.py`, `*.md`, `*.json`) leaves only config-keys.json, config-projection.json:32, fixtures, tests and the changelog fragment. The
  `stand_lease.py` / `walk_session.py` hits are the unrelated constant `DEFAULT_ENVIRONMENT = "default"`. Positive control: the same
  call finds `format_changed` in tests.
- **"`needed_by` filled from grep"**: sampled four entries (`app_card.py:_test_data` :235, `contract.py:registry_sides` :5711,
  `judge_code.py:test_data_for_judge` :208, `stand_health.py:settings` :118); all exist. Missed: `dod` (F2).
- **Template ↔ catalogue**: every non-note template key has a row. The registry rows appear in today's `KEYS` order. Only
  `format_changed` and `dod` have an empty `needed_by`.

## Trail

Read: the spec t-129 whole; critic-diff-brief.md; the full diff of e61efb8; project_knowledge.py:100-300 in the worktree;
config_contract.py:1326-1338, :1800-1830, :1880-1940, the import block; test_config_migration.py:320-340, :870-885; config-keys.json
`removed` and `knowledge` (via python); templates/config.json keys; readiness.py:880-915; app_card.py:235; slow_tests.json:118-120;
tools/critic_verdict.schema.json.
Re-runs (cheap control of the attached witness):
- `python -B -m pytest .../tests/test_project_knowledge.py -q` → `85 passed in 8.03s` (witness 85 passed)
- `python -B .../tests/test_config_migration.py` → `=== test_config_migration: 617/617 ok ===` (witness identical)
- `python -B .../tests/scenario_walk.py --witness-for <node a owns>` → lists the three scenario files and test_story_run_monorepo
  besides the builder's set (F7)
Not run: slow files (test_brief_pack, test_install_retire, test_reinstall_equals_fresh, the scenarios), which are judged by CI.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axes 16, 35 and 8 for node a: covered or queued to nodes b-d, N-r3 and N-r4 as the spec says. Open: format_changed is an unqueued sibling of the OH3-35 dead-key class (needs an owner node before f). Retired-key companion notes (execution_note, pre_commit_note, format_note, records_policy_note) need one migration rule (a proposed node). _stand_roles vs _stand_card is a two-road sibling inside the artifact (fix now or N-r1).",
  "fixes": [
    "F1 must: project_knowledge.py:328/:346 value() gets a trailing element keyword passed to state(); a registry row with an empty element returns unknown with an explicit problem; a found row returns its value; rewrite test_project_knowledge.py:895 (Lead picks, spec defect)",
    "F2 must: config-keys.json:754 dod needed_by gets readiness.py:_optional_top_keys and config_contract.py:not_filled; a finding plus an owner node for format_changed (:751, produced with no reader); node f's spec states how R3 counts readers that read by table",
    "F3 minor: project_knowledge.py:234 _stand_roles takes the stand through _stand_card (or an explicit N-r1 pointer)",
    "F4 minor: test_config_migration.py:378 knowledge_gaps reuses value_keys() or C._is_note",
    "F5 minor: project_knowledge.py:503 doubled door text (optional)",
    "F6 minor: queue a per-process read of the catalogue for the first loop caller of value()",
    "F7 minor: the report names the three scenario files and test_story_run_monorepo as not run (slow)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md",
      "docs/tasks/critic-diff-brief.md",
      "git show e61efb8 (full diff)",
      "ai-packages/qa-factory/scripts/project_knowledge.py:100-300 (worktree)",
      "ai-packages/qa-factory/scripts/config_contract.py:1326-1338,1800-1830,1880-1940",
      "ai-packages/qa-factory/scripts/tests/test_config_migration.py:320-340,870-885",
      "ai-packages/qa-factory/references/config-keys.json (removed, knowledge)",
      "ai-packages/qa-factory/scripts/readiness.py:880-915",
      "ai-packages/qa-factory/scripts/slow_tests.json:118-120",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -m pytest ai-packages/qa-factory/scripts/tests/test_project_knowledge.py -q (worktree)", "result": "85 passed in 8.03s"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_config_migration.py (worktree)", "result": "=== test_config_migration: 617/617 ok ==="},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <node a owns> (worktree)", "result": "also lists test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_story_run_monorepo (slow, not in the report)"}
    ]
  }
}
```
