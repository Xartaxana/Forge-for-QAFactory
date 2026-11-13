# t-223 — critic: OH3-6 + OH3-12 (t-207) and RC1-10 (t-209), one pass on one topic (texts a role or a person reads)

Reviewer: critic (Opus). Date: 2026-11-13. Diffs: `origin/main...origin/wip/oh3-6` (5114711) and `origin/main...origin/wip/rc1-10` (8394e08).
Spec/DoD: node rows OH3-6, OH3-12 (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:29,31`) and their findings
`findings/20261022-doctor-daet-cheloveku-komandy-skriptov.md`, `findings/20261022-doktor-rasskazyvaet-cheloveku-o-svoej-kuhne.md`; RC1-10
(`batch-2-onboarding-roles-forge-p3.md:46`) and `findings/20261023-karty-rolej-ostatki-help-otkazy-mimo-role-cli-i-runtime-provenance.md`.

## Verdicts

- **OH3-6 + OH3-12: NEEDS WORK (fit_with_fixes).** Fixes O1, O2 and O3 below. None blocks the merge on its own, but O1 must be fixed before
  merge: the new eval teaches the wrong person to ask and a write the skill forbids.
- **RC1-10: NEEDS WORK (fit_with_fixes).** Fixes R1, R2 and R3 come before merge. R4 is a queue line. R5 and R6 are minor.

Acceptance rests with the Lead (rule 6). This verdict is an input to it.

## OH3-6 + OH3-12 — findings

**O1 (fix before merge) — eval 16 asks the person the wrong question and has the doctor write outside its declared writes.**
Eval 16 (`skills/qa-doctor/evals/evals.json`, id 16) has a remedy with `remedy.owner: user` whose step is `tracker_write.py --record confirmed|no
--words <its answer>`. It expects the doctor to "ask the person one closed question ... then run the recording itself". I checked the producer:
- `readiness.py:846-852`: the `--record` step is emitted only under `owner: "orchestrator"` (status unknown). Its `need` is "one question to the
  **tracker agent**, which no script can ask". The `owner: "user"` branch (`:839-845`) carries `r.get("alternatives")`, not `--record`. So the
  eval's premise is a state the producer never emits.
- The answer being recorded belongs to the tracker channel, not the person. `tracker_write.py:30` shows the example `--words "the assistant answered:
  it can create issues"`. Asking the person first skips a route the factory can take itself. That breaks FR-50/P5 and the skill's own "Routes the
  factory can take itself come first".
- `tracker_write.py:39`: `--record` appends a `tracker_write_answer` line to the carried log `records/onboarding-approvals.jsonl`. The doctor's
  bold write list (`SKILL.md:39-41`) does not include that log. Neither does "Its only repairs are ..." (`SKILL.md:312`).

The new bullet (`SKILL.md:279-281`, "A decision is one closed question ..., then you run it") has no bound. Read with eval 16, it extends the
doctor's writes to any script a remedy names. It also overrides `remedy.autorun: false`: step 2b runs only `autorun: true` probes.
Fix:
- (a) Rebuild eval 16 on a person-owned remedy that is really emitted, for example `readiness.py:301-307` `ticket-read-route`. Its steps name
  `/qa-factory:qa-onboarding` and `waiver.py --stage S1 ... --decision "<your words>"`. Expected: the skill is named, and the waiver becomes one
  closed question that the doctor records only if waiver is within its writes. Otherwise it names the owning skill.
- (b) Bound the bullet: "you run it" covers only a script within the writes listed above or a read-only probe. Anything else: name the skill that
  owns it.

**O2 (fix before merge, cheap) — the new bullet duplicates the one before it (brief item 6).**
- `SKILL.md:278` says: "The person gets a skill, a closed question or an action of their own - never a factory script ... Run such a step yourself,
  or name the skill that owns it."
- `SKILL.md:279`, the new bullet, says: "The role runs the script; the person answers or acts ... a step only they can do is an action in words."

These are two adjacent rules on one duty. Merge them into one bullet; that bullet carries the bound from O1(b). The file is at 18999/19000 bytes
(`selftest.py:341` `SKILL_MD_MAX_BYTES = 19_000`), and OF1-4 is queued on the same file (`batch-1...md:70`). The merge buys back the headroom that
the cuts spent.

**O3 (queue lines owed) — the class root and the siblings named in the findings are neither fixed nor queued.**
- Both findings name the siblings: onboarding and `qa-story` texts that hand a person `*.py`, on the "text to a person" axis.
- The producer still writes script lines into person-owned steps: `readiness.py:301-307` (`waiver.py ...`, `references/jira-direct-access.md`).
  Its docstring contract at `readiness.py:96` still says "steps ordered, each executable as written".
- The doctor now has to translate them at render time. That is a render-side patch of a producer-side defect (FR-32 root cause, AR-16 one form).

No row for these exists in the pile; I grepped `plans/piles/` for OH3-6/OH3-12. Return as Остатки lines for the Lead:
- `readiness.py remedy.steps (owner: user) carry script lines and paths; docstring :96 "executable as written" | перенос: findings/<new> |
  обоснование: producer side of OH3-6, out of owns | подтвердил: —`
- `qa-onboarding / qa-story person texts handing *.py (siblings named in the OH3-6 and OH3-12 findings) | перенос: findings/<new> |
  обоснование: same class, other skills | подтвердил: —`

**O4 (no action) — the cuts lost no mandatory rule.** Every role-rules anchor holds:
- `test_role_rules.py` on the branch: `role-rules: 447 rows, 534 carriers checked, 0 finding(s)`, 57/57.
- `selftest --limits --lang` is 4/4 on the branch.

Each removed sentence, and where its rule survives:

| Removed sentence | Where it survives / verdict |
|---|---|
| "interrupted continuations" | → "continuations"; superset, fine |
| "do not re-judge it" | "use its summary verbatim" (`:45`) |
| "Run once and wait" | "seven steps ... each one Bash call" and "`status: running` means wait" |
| "Two probes are not full parity" | only as readiness `live parity:` printed verbatim (`readiness.py:1177`); acceptable |
| "Doctor never runs" | → "Never runs" |
| "never re-open a `pipeline.json`" | "It never edits a `pipeline.json` by hand" (`:41`) and the Read/Glob/Grep ban (`:45`) |
| "is never the next action" (factory row) | next-action row 5a ("NOT an action ... next row") |
| "a bare command that will stop and ask for a token is not a step" | evals.json:140 asserts it; SKILL keeps "says where to get it, with the minimal rights" |
| "`/qa-factory:qa-story` is row 9 only" | table row 9 plus "first row that applies, stop" |

OH3-12 item (1) (`injection: unverified` goes to the tail) is done at `SKILL.md:282`. Item (2) (working tree) was already covered on main by
"No working tree, `git status` or own writes". Item (3) is covered by eval 17. Eval 17 has no explicit `git status`-retelling assertion; that is
minor and not a finding (a missing pin is not a finding).

**O5 (process) — no witness or FR walk was attached for OH3-6.** The builder's report is "at the agent" (rule 7). I did my own walk and re-ran the
two checks above.
- A: FR-1/2 n/a, no refusal text changed. FR-50 is broken by eval 16 (O1).
- B: FR-6 applies. Person text goes through the closed-question form (`references/human-questions.md` is cited). Holds, except O1.
- C: FR-38 n/a. FR-15 n/a. FR-56: no new tool.

The FR walk lines should still be attached to the acceptance event.

**Standing questions, OH3-6:**
- DUPLICATION AND CONSISTENCY: O2. I grepped SKILL.md for "script" and "closed question"; the other bullets don't overlap.
- CODE QUALITY: none found. Text and evals only; evals.json parses; LF endings kept, the same as main (0 CR lines in old and new).
- ONE ROAD (item 12): none found. I read the diff for language, project or host branches; the Codex/Claude hook-file line is a rewording, with no
  new exclusion.
- JUDGMENT (item 11): none. No census or role-load rows. The new bullet is report-form procedure, not craft; the size is at the cap (O2).
- ARCHITECTURE: AR-16 is named and kept, except O1. AR-14 (one writer) is touched by O1 (the approvals log) and not named.
- Ratchets: none in the diff.

## RC1-10 — findings

**R1 (fix before merge) — same class, same owned function, not fixed and not named: `critic_rollcall.py --task-root` with no value.**
The run is in the trail. `python -B scripts/critic_rollcall.py --task-root` prints:
`critic_rollcall.py: this is a defect in critic_rollcall.py, not something you wrote wrong: IndexError: list index out of range`, exit 2.
- Cause: `critic_rollcall.py:1121` reads `args[index + 1]` unguarded. The `--store` sibling 12 lines below is already guarded.
- Also, `--apply-fixes` without `--task-root` (`:1143`) prints `{"error": "--apply-fixes requires --task-root"}` with no card, exit 1.

Both are argument refusals that bypass `role_cli.refuse`, which is the node's class. They sit in `main()`, which this diff edits. The builder's
sibling list misses them. Fix: refuse both through `role_cli.refuse("critic_rollcall.py --store" | "critic_rollcall.py", ...)`, as the `--store`
branch does. Add one table row each.

**R2 (fix before merge) — `external_writes.py:1397` main parser stays plain `argparse` in an owned file the node names.**
- The node names "отказы разбора аргументов (... `external_writes --record`)". The diff moves only the two semantic refusals in `record_result`.
- The script's argparse errors (bad `--phase`, an unknown flag on a `--record` call) still print bare usage with no card. So does `:1420`
  ("a ticket id is required").
- The builder listed both as siblings not fixed. They sit in the file's own `main()` and the change is one constructor
  (`RefusingParser(command=command_from_argv("external_writes.py"), ...)`). The sweep-the-artifact rule says fix them now, not queue.

**R3 (fix before merge, test) — the no-card rows pin a real registry gap as desired behaviour.**
- `test_role_commands.py:851` uses `manual_evidence.py validate` as the "card is missing" case.
- `validate` is a role-facing command with an `--input` file: `references/manual-evidence.md:122` says `manual_evidence.py validate --task-root
  <T> --input <record.json> checks a rec...`.
- The registry has no `manual_evidence.py validate` key; I listed the registry keys, see the trail.

So the test now passes because the card is missing. `role_cli.py`'s docstring promises the opposite: "the test names the gap". Adding the card
later turns this row red for the wrong reason.

Fix:
- (a) The no-card row uses a command that is unregistered by design. For example, construct `RefusingParser(command="no_such_command.py")`
  in-process and call `parse_args([])`.
- (b) Add the `manual_evidence.py validate` card to `references/role-commands.json` (in owns) with its example, or return it as an Остатки line.

The `artifact_producer.py validate` row has the same shape. That subcommand is not referenced by any agent or skill I grepped, so it is lower risk,
but use the same synthetic row.

**R4 (queue lines owed) — the builder named these siblings without a pile line.** I verified each line on the branch:
- `case_versions.py:661`, `execution_fingerprint.py:893`, `manifest_put.py:2796`, `red_sandbox.py:2236`: plain `argparse.ArgumentParser`.
- `grounding_section.py:145`: plain `argparse.ArgumentParser` with an epilog.

My own scan found the same set. These scripts have registry cards and still use plain `argparse.ArgumentParser`: `case_versions`,
`execution_fingerprint`, `external_writes`, `manifest_put`, `red_sandbox`; `critic_rollcall` only in `print_help`, which is legitimate. Return as
one Остатки line: `carded scripts on plain argparse (case_versions:661, execution_fingerprint:893, manifest_put:2796, red_sandbox:2236,
grounding_section:145) | узел: <RC1-n in an untaken batch>`. A bare list in a report is refused by `piles.py check` (д).

**R5 (minor, queue) — the `critic_rollcall.py --help` usage line misstates the call.** It prints `usage: critic_rollcall.py [-h]`, which is the
first line of the help; the real shapes are only in the docstring (lines 25-26 of the output). Pass `usage=` from the docstring forms, or
`argparse.SUPPRESS`. The test checks only the prefix `usage: critic_rollcall.py`.

**R6 (minor) — a text pin in the test.** `check_not_in(... "interpreter identity", card(command))`, and the number-word list `"all six"`, pin wording
(brief item 5). The positive junction checks (every key `build()` asks for and every `validate_runtime_provenance` field appears in the card) are the
real value. Drop the negative literal.

**Semantics checked (rule 13, empirical where cheap):**
- The `runtime_provenance` card was read against `profile_contract.validate_runtime_provenance:667-730` and `execution_fingerprint.build:108-128`.
  The required fields, the `not_applicable` exemption, the non-empty `evidence_refs` for `matched`, and the `matched` linkage/technical rule all
  match.
- `person_confirmed` also needs `person_confirmation{words, at}`, `technical_verification` false and `identity_kind`. The card is silent on these,
  but it says the record is the one "the runner wrote, read whole" (copied, not composed). Acceptable, not a finding.
- The `external_writes` refusals keep exit 1 and move from stdout/stderr to stderr. No reader depends on the old text: a grep for
  `external-id is required|needs --remote-revision|reconcile unknown` outside tests finds only the producer. The one caller is the conductor
  (`references/conductor-actions.json:12`).
- Inside `record_result`, refusals now exit 2, 1 and 1. The first one was already 2 on main. Recorded as an observation, not a finding.
- No-card message (`role_cli.py:109`), checked for FR-1/FR-2. It says what is missing, and its door (`--help`) is usable by the role; the role's
  `--help` works on every `RefusingParser` and on `critic_rollcall`. Holds.

**Standing questions, RC1-10:**
- DUPLICATION AND CONSISTENCY: the diff reuses `role_cli.refuse`, `RefusingParser`, `command_from_argv` and `epilog`, so it adds no second
  implementation. I grepped `def refuse|class .*Parser\(argparse` in the package; the existing survivor is `role_cli.py:102`.
- Consistency gap: a missing card is announced on usage errors but stays silent in `refuse()`. The builder chose this and stated it in a code
  comment; acceptable.
- CODE QUALITY: R5 is a misleading usage line. New functions are under 60 lines (`argument_refusal_table` is 94 lines of table and loops, at
  `test_role_commands.py:814-906`, test code; a queue-level note). No dead branches. The `return 1` comments are truthful.
- ONE ROAD: none found. No language, runner or project branch in the diff; I read every hunk.
- JUDGMENT: none. No census rows, no `blocks_override`, no scan-constant edits.
- ARCHITECTURE: AR-9 and AR-13 are named. AR-9 is not fully kept: R1 and R2 are argument refusals still without the card.
- Ratchets: none in the diff.
- Tests: `test_role_commands.py` has a `keep` row in `test-layers.json`. The table tests run through the real door (subprocess of the script) and
  catch the node's defect class, except R3.

## Class-wide completeness (SIBLING_MAP)

- **The "one question for every stop / person text" class.** Axis 5 (stage twins, `references/human-questions.md` carrier) and axis 31 (role
  carriers). The doctor side is done; the producer (readiness remedy steps) and the onboarding/qa-story siblings are not queued (O3).
- **The role_cli refusal survivor** (AR-15, axis 17 detector-shape neighbours). The owned files have residuals (R1, R2); the other files need a
  queue line (R4).
- Axis 18 (ratchets): no rows. Axis 34 (one road): none found.

## Spot-checks of claims

- "SKILL.md trimmed to 18999 bytes": `wc -c` gives 18999 for the new file and 18995 for main. **Holds.**
- "test_role_commands 860/860": my re-run on the branch gives `=== test_role_commands: 860/860 ok ===`, exit 0. **Holds.**
- "selftest --limits --lang 4/4" (RC1-10): not re-run. I re-ran it on OH3-6 instead: 4/4.
- Builder's negative "siblings not fixed = list": **partially false.** The list is complete for plain-argparse parsers, but it misses
  `critic_rollcall.py:1121` and `:1143` (R1). Positive control: the same grep shape (`argparse.ArgumentParser(`) found all six of the builder's
  lines.
- "No consumers of the dropped `REJECT:` prefix": verified by my grep. The positive control is the producer lines 884/890 found by the same pattern.

## Trail

Files read:
- Both diffs in full.
- `docs/tasks/critic-diff-brief.md`.
- Node rows `batch-1...md:29,31,70` and `batch-2...md:46`, and the three findings.
- On the branch, new and old `skills/qa-doctor/SKILL.md` (whole: header, steps 2/2b, report template, printing rules, never-does).
- `design/role-rules.json` doctor rows.
- `scripts/readiness.py:90-100, 290-310, 640-660, 835-855, 1177`.
- `scripts/tracker_write.py:1-45`.
- `scripts/role_cli.py:1-140`.
- `scripts/critic_rollcall.py` `main()`.
- `scripts/external_writes.py:858-895, 1180-1200, 1390-1425`.
- `scripts/profile_contract.py:667-730, 812, 830-855`.
- `scripts/execution_fingerprint.py:108-128`.
- `references/role-commands.json` keys.
- `scripts/tests/test-layers.json` row for `test_role_commands`.
- `docs/SIBLING_MAP.md` axis headings.
- `tools/critic_verdict.schema.json`.

Commands (verbatim results). Worktrees are under the scratchpad, `wt-oh3` (5114711) and `wt-rc1` (8394e08):
- `python -B scripts/tests/test_role_rules.py` (wt-oh3): `role-rules: 447 rows, 534 carriers checked, 0 finding(s)` / `=== role rules: 57/57 ok ===`
- `python -B scripts/selftest.py --limits --lang` (wt-oh3): `=== qa-factory selftest: 4/4 ok ===`
- anchor script over `role-rules.json` × new SKILL.md: 5 doctor carriers. One case-only miss (`no third bucket` vs "No third bucket"), the same on
  main; the matcher is case-insensitive per E-6, and the test passes.
- `python -B scripts/tests/test_role_commands.py` (wt-rc1): `=== test_role_commands: 860/860 ok ===`, EXIT=0, 2m22s.
- `python -B scripts/critic_rollcall.py --task-root` (wt-rc1): `...this is a defect in critic_rollcall.py ... IndexError: list index out of range`, EXIT=2
- `python -B scripts/critic_rollcall.py --apply-fixes` (wt-rc1): `{"error": "--apply-fixes requires --task-root"}`, EXIT=1
- `python -B scripts/critic_rollcall.py --help` (wt-rc1): first line `usage: critic_rollcall.py [-h]`, EXIT=0
- registry keys (wt-rc1): `manual_evidence.py prepare|write-block|export|build|rejudge`, `artifact_producer.py publish|validate-batch`,
  `critic_rollcall.py --store`, `external_writes.py --record`, `plan_row.py`, `execution_fingerprint.py`. There is no `manual_evidence.py validate`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "OH3-6: the doctor side is done; the producer side (readiness.py remedy.steps owner user carry script lines, docstring :96) and the onboarding/qa-story siblings named by both findings are neither fixed nor queued (O3). RC1-10: residuals in owned files (critic_rollcall --task-root/--apply-fixes R1, external_writes main parser R2) must be fixed now; the remaining carded scripts on plain argparse need one Ostatki line (R4). Axis 18 and axis 34: none.",
  "fixes": [
    "O1 OH3-6: rebuild eval 16 on a person-owned remedy readiness really emits (readiness.py:301-307), not tracker_write --record (an orchestrator-owned tracker-agent question that writes records/onboarding-approvals.jsonl); bound the new bullet SKILL.md:279 so the doctor runs only scripts within its declared writes or read-only probes, else names the owning skill",
    "O2 OH3-6: merge SKILL.md:279-281 into the bullet at :278 (duplicate duty; buys back bytes at 18999/19000 with OF1-4 queued on the file)",
    "O3 OH3-6: return Ostatki lines for readiness.py remedy.steps script lines (producer, docstring :96) and the onboarding/qa-story person-text siblings",
    "R1 RC1-10: critic_rollcall.py:1121 --task-root without value (IndexError reported as factory defect) and :1143 --apply-fixes without --task-root (bare JSON) refuse through role_cli.refuse; add table rows",
    "R2 RC1-10: external_writes.py:1397 main parser to RefusingParser(command=command_from_argv('external_writes.py')) and :1420 through refuse",
    "R3 RC1-10: no-card test rows use a synthetic unregistered command, not manual_evidence.py validate (role-facing per references/manual-evidence.md:122); add that card or return it as an Ostatki line",
    "R4 RC1-10: one Ostatki line with a node for case_versions:661, execution_fingerprint:893, manifest_put:2796, red_sandbox:2236, grounding_section:145",
    "R5/R6 minor: critic_rollcall --help usage line [-h] misstates the call; drop the negative text pin 'interpreter identity' in the test"
  ],
  "trail": {
    "read": [
      "git diff origin/main...origin/wip/oh3-6",
      "git diff origin/main...origin/wip/rc1-10",
      "docs/tasks/critic-diff-brief.md",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:29,31,70",
      "plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:46",
      "plans/piles/onboarding-forge/findings/20261022-doctor-daet-cheloveku-komandy-skriptov.md",
      "plans/piles/onboarding-forge/findings/20261022-doktor-rasskazyvaet-cheloveku-o-svoej-kuhne.md",
      "plans/piles/onboarding-forge/findings/20261023-karty-rolej-ostatki-help-otkazy-mimo-role-cli-i-runtime-provenance.md",
      "ai-packages/qa-factory/skills/qa-doctor/SKILL.md (old and new)",
      "ai-packages/qa-factory/design/role-rules.json",
      "ai-packages/qa-factory/scripts/readiness.py:90-100,290-310,640-660,835-855,1177",
      "ai-packages/qa-factory/scripts/tracker_write.py:1-45",
      "ai-packages/qa-factory/scripts/role_cli.py:1-140",
      "ai-packages/qa-factory/scripts/critic_rollcall.py main()",
      "ai-packages/qa-factory/scripts/external_writes.py:858-895,1180-1200,1390-1425",
      "ai-packages/qa-factory/scripts/profile_contract.py:667-730,812,830-855",
      "ai-packages/qa-factory/scripts/execution_fingerprint.py:108-128",
      "ai-packages/qa-factory/references/role-commands.json",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "docs/SIBLING_MAP.md axis headings",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_role_rules.py (wt-oh3, 5114711)", "result": "role-rules: 447 rows, 534 carriers checked, 0 finding(s); 57/57 ok"},
      {"command": "python -B scripts/selftest.py --limits --lang (wt-oh3)", "result": "4/4 ok"},
      {"command": "python -B scripts/tests/test_role_commands.py (wt-rc1, 8394e08)", "result": "860/860 ok, EXIT=0"},
      {"command": "python -B scripts/critic_rollcall.py --task-root (wt-rc1)", "result": "defect in critic_rollcall.py: IndexError: list index out of range, EXIT=2"},
      {"command": "python -B scripts/critic_rollcall.py --apply-fixes (wt-rc1)", "result": "{\"error\": \"--apply-fixes requires --task-root\"}, EXIT=1"},
      {"command": "python -B scripts/critic_rollcall.py --help (wt-rc1)", "result": "usage: critic_rollcall.py [-h] ... EXIT=0"}
    ]
  }
}
```
