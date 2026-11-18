# t-1439 code review: FG7-14 cards A, B, C and FG7-81 card A

critic, 18.11.2026. Spec: `docs/tasks/specs/20261118-fg7-14-dispatch-label-role-card.md` (sections 0-5, 9, 11) and
`docs/tasks/specs/20261118-fg7-81-named-by-pointer-check-card.md` (sections 2-4, 8, 11). Each branch diffed against
origin/main (eb1c3e51) with `git -C <worktree> diff origin/main...HEAD`.

## Verdict

- **FG7-14 card A (91a60282): NEEDS WORK.** Two fixes, neither blocks the merge (findings 1 and 2).
- **FG7-14 card B (3fc1d24c): ACCEPT.** It stays world-agnostic: 145 passed before A, and the same files pass in the
  merged world. One fix to the record only (finding 4).
- **FG7-14 card C (72270bdf): ACCEPT.** It stays world-agnostic: 126 passed before A, and the same files pass in the
  merged world. One fix to the record only (finding 4).
- **FG7-81 card A (f5f42106): NEEDS WORK.** One fix that does not block the merge (finding 3).
- **Hook paths and dispatches that break when A lands: none found in code.** No live tool, probe or rule text still
  writes a tier-form label (see Spot-checks). The only thing that changes is the Lead's own typed label: from that
  merge on it must be `<subagent_type>: ...` (COORDINATOR.md rule 7 as edited in 91a60282).
- Nothing blocks the merge. Merging stays the Lead's decision (rule 6).

## Findings

**1. FG7-14 A: the resolver table repeats the hook's rows, and one row checks a live role file. Fix before merge (does not block).**
`tools/test_dispatch_gate.py:3322-3334` (`test_role_bound_model_rows`). Five rows test a behaviour that
`tools/test_journal_hooks.py` already tests through the hook:
- `scout_default`, `critic_config` and `designer_role_file`: the same as `test_d0016_...` rows :168, :169 and :172;
- `builder_no_model`: the same as NOT_RECORDED `coordination_role_without_model` (:119);
- `no_role_file`: the same as `role_without_binding` (:118).

This is a Q5(e) duplicate. The `designer_role_file` row has a second problem: it reads the live
`.claude/agents/designer.md` and expects `claude-opus-5-5`. That is a check on a measured constant (Q5(b)/(f)): the
expected value comes from repo data, not from the spec.
- Proof on a scratch copy: I set `model:` in designer.md to `claude-sonnet-5-5`. The product is correct, but
  `test_role_bound_model_rows[designer_role_file]` failed at `:3334` (`1 failed, 8 passed`). The byte copy was then
  restored, and the hashes match (c508e396 = c508e396).
- Fix: cut the five rows. Keep `none`, `int` and `blank` (the never-raises contract, which the hook door cannot reach)
  and `test_role_bound_model_filename_beats_name_field`.

**2. FG7-14 A: the resolver reads the config a second way. Fix before merge (does not block). It needs a file
outside card A's `owns`, so the Lead widens the owns or records the deviation.**
`tools/dispatch_gate.py:1102`: `if "lead" not in tier_ladder.bindings(config_text)[0]:` re-derives the private
"defaulted" flag of `tier_ladder._effective`. This goes against:
- the card's own § 2 AR-13 line: «bindings are read only through `tier_ladder.effective_bindings`»;
- the ladder home's own docstring (`tools/tier_ladder.py:122`): «EVERY reader goes through this one function».

It also parses the YAML twice on every hook call. The handoff names this deviation honestly. Today the two are
equivalent. The failure scenario: the ladder changes when it defaults (any edit to `_effective`). The hook's
`; model by default bindings` line then silently stops matching what was written.
- Fix: in `tools/tier_ladder.py` (outside A's owns, a non-goal of card A), expose the flag with the bindings, for
  example a public twin of `_effective`. `role_bound_model` then makes one call.
- An analog already on main: `tools/savings_report.py:133` calls `tier_ladder.bindings` directly. Name it in the
  same convergence.

**3. FG7-81 A: the line-number form check catches only a trailing `:<digits>`. Fix before merge (does not block).**
`ai-packages/qa-factory/scripts/selftest.py:794`, `re.search(r":\d+$", rel)`. Card 2.1 says «No `:<digits>`», and
E12 says «no forge entry keeps a line number after A». The probe below is a pure function on the real tree (no
corruption needed, hygiene 7(d)). It printed:
- `design/state-exits.md:57` -> PROBLEM;
- `design/state-exits.md:57-60`, `:L57`, `#L57` and `:57 ` (trailing space) -> OUTSIDE (note only, exit 0).

So a line pointer in range form gets in as an "outside, the forge checks it" entry. Card B (not yet built) would
later refuse it as «in neither». Until then the error runs toward a pass, against 2.2's direction of error. Card B is
not this card's guard.
- Fix: refuse any `:` left in `rel` after the `::` split. The drive form is already refused, and no package path holds
  a colon. Add one `x.md:3-4` variant to the "a line number" row of `layers_cli_cases`.

**4. FG7-14 B and C: the last commit on each branch comes after the handoff's witness. A record fix, not a code change.**
- Card B: 3fc1d24c (registry-entry labels, the answer to B's question).
- Card C: 72270bdf (`subagent_type: builder` added to the two `test_dispatch_cut.py` payloads, the answer to C's
  question).

Both handoffs still end on the question, and C's says «NOT DONE». Their witnesses (145, 126) were taken before these
commits (rule 7). I re-ran both on the final HEADs. The numbers are the same, and the files are green in the merged
world (Trail). Fix: one addendum line in each handoff, quoting the answer and the re-run.

## Seam and class notes

- **E6 (TEMPORAL).** The gate and the hook change in the one commit 91a60282, together with the Lead's D6 edits:
  - COORDINATOR.md rule 7 matches the text of § 9 word for word;
  - AGENTS.md was regenerated (rule 7 mirror, hooks row, byte header);
  - the pile row's owns changed CLAUDE.md -> COORDINATOR.md.

  origin/main has not touched AGENTS.md, COORDINATOR.md or any of A's files since the base 7d15b636: only
  `tools/conftest.py` and `tools/under_test.py`, and they add no tier labels.
- **B and C are world-agnostic.** Their files pass before A (145 and 126) and after it (271 = 145 + 126, run against A's
  `dispatch_gate.py` with B's and C's files laid over it).
- **Leftover tier-word labels in A's world:** 23 in `test_dispatch_gate.py`, all `role_type_warn` rows. That layer no
  longer reads the description, so they serve as "a known role stays silent under any label" rows, which is correct
  behaviour.
- **Class (SIBLING_MAP axes 1, 13, 34).** `role_bound_model` is the one reader of a role's model. `tier_echo` was left
  unchanged by Lead decision F6 (a). `journal_echo` reads the journal's `model` (M11).
- **Q12 one road:** none found that blocks. Check 3 runs the same for every role. The split between the config and the
  role file is keyed by the data row `tier_ladder.COORDINATION_FUNCTIONS`. Harness built-ins get a door line and no
  record, which is Lead decision F2 (a) (card § 11, quoted from its carrier).
- **FG7-81 card B** is the declared follow-up for the forge side (E12).

## Standing questions

- **Q1 fit.**
  - A: D1-D4 are implemented as written, and so are F1-F7. Check 3 is still last: the 4 tests named under Q5(a) cover
    this.
  - FG7-81: 2.1-2.3 as written, except finding 3.
  - B and C: fixtures only.
- **Q2, the builders' own decisions:** they are all in the safe direction:
  - `agents_dir=None` read at call time;
  - a no-role-file WARN with no label;
  - FG7-81 refusing a backslash and a drive.
- **Q3 seams:** additive. The Lead edits ride A as § 11 says.
- **Q4 class:** see the notes above. One analog outside owns is named: finding 2, `savings_report.py:133`.
- **Q5 tests.**
  - (a) Killing power holds. A mutant that always returns the no-subagent_type text was killed by 4 tests
    (`..._handoff_refusal_keeps_the_label_check_behind_it`, `test_echo_json_blocks_bad_label`,
    `..._label_check_still_runs` x2). For FG7-81, the six rows hit E2, E1, E9 and E3.
  - (b) Expected values: finding 1 (designer).
  - (c) Every door has a row.
  - (d) The deleted and rewritten rows are listed in A's handoff. The main() guard test was restored with a new
    trigger.
  - (e) Duplicates: finding 1.
  - (f) Budget: new test lines are about 70 against about 109 product lines, so it is within budget. The fixture
    rewrites are edits.
  - (g) No new test file.
- **Q6 duplication:** A, finding 2. FG7-81 does not reuse `selftest._carrier_text` (:690), and that is correct here:
  `_carrier_text` folds a missing file and an unreadable file into `""`, while 2.2 needs "missing -> outside" kept
  apart from "unreadable -> problem".
- **Q7 code quality:**
  - `named_by_problems` is about 35 lines with 3 levels of nesting;
  - `_label_refusal` is 8 lines;
  - the dead names were removed (`_FAMILY_NAMES`, `_model_family`, `LABEL_MODEL_PREFIX_RE`, `_LABEL_LEADING_TOKEN_RE`,
    `label_model_family`, `ROLE_TYPE_WARN_MISMATCH`). A grep finds none left outside C's docstring, which C rewrites.
- **Q8 hygiene (FG7-81):**
  - CRLF kept: test-layers.json 11954 of 11954 lines, selftest.py 1544 of 1544;
  - 0 Cyrillic lines added.
- **Q9 ratchets.** FG7-81 adds one census row (`selftest.py::named_by_problems`, class xref, not blocking). The class
  ceilings cover word-list, meaning-proxy, meaning and safety only, so no ceiling is raised. C3 is the canon's to judge,
  and I did not run it. The dup and lint ratchets (`tools/dup-baseline.json` names `role_type_warn`, and its lines
  shift) are the forge-check job's. That result was not attached, so it is requested from the Lead's merge pipeline.
  I did not run them.
- **Q10.** A names AR-13, AR-29 and AR-1 in the card. Finding 2 is the AR-13 change check.
  `VARIETY: none -- forge tools`. FG7-81 is package tooling for test-layers data only, with no project-facing value.
- **Q11 judgment:** none. No class was lowered, no `blocks_override` was added, and no scan constant was edited.
- **Q12:** see above.

## Spot-checks

These are claims I checked myself, each negative with a positive control.

**FG7-14:**
- **Live emitters of tier-form labels.** The grep `"description"\s*:\s*f?"(sonnet|opus|haiku|fable|claude)[ :-]` over
  tools/, .claude, .githooks and scripts, excluding test_*, found only `usage_report.py:1106` (an argparse
  description, unrelated). The control `"description"\s*:\s*f?"(builder)[ :-]` found `hook_liveness_probe.py:598, 670,
  704`.
- **Rule docs.** The case-insensitive grep `\b(sonnet|opus|haiku|fable): ` over the root *.md files, PROCESS/*.md,
  .claude/agents/*.md and RUNBOOK found 0. The control `\b(builder|critic): ` found 4 in COORDINATOR.md.
- **Deleted names.** A grep for them over tools, scripts and .githooks finds only C's docstring lines
  `test_critic_snapshot.py:356, 358`, and C removes them.
- **No reader parses a tier from the journal's `notes`.** The grep finds no tool that does.
- **Package twin.** The hits for `dispatch label` in the package are unrelated text (driver_dispatch.py:2634,
  driver_s0.py:532).

**FG7-81:**
- **The narrow call on the real tree** prints `0 46`, which matches the handoff.
- **test-layers.json, compared as data:**
  - outside `named_by`, only two `why` texts differ, as the Lead's answer says;
  - 161 rows were re-pointed, and the `data_join` row lost its `named_by`;
  - the carrier set did not change in any row;
  - 0 `:N` entries remain;
  - the 6 `::symbol` entries are `NO_CARD`, `CENSUS_EXEMPT`, `refusal_every_action_has_a_move`, `EXCEPTIONS`,
    `KNOWN_IGNORING` and `COMMANDS`.
- **origin/main drift since 845650e1:** it touches none of the named_by carriers or the edited files.
- **Forge readers.** Nothing in the forge parses `named_by` entries, so a `::symbol` breaks nothing in
  `test_quarantine`. Its only reads are at :1525, :1698 (shim rows).

## Trail

Read:
- the FG7-14 card, sections 0-11;
- the FG7-81 card, sections 2-4, 8 and 11;
- the four handoffs;
- the full diffs of all four branches;
- the commit message of 91a60282;
- `tools/tier_ladder.py:20-140`;
- `tools/journal_validator.py:862-880`;
- `tools/dispatch_gate.py:1735-1750`;
- `tools/test_dispatch_gate.py:480-560, 1836-1860, 3300-3350`;
- `selftest.py:690-715, 750-840`;
- `test_judgment_census.py:218-232, 386-416`.

Commands, output verbatim (tails):
- In A's worktree, `python -B -m pytest -p no:cacheprovider tools/test_dispatch_gate.py -q` -> `376 passed in 38.79s`.
- In B's worktree, `python -B -m pytest -p no:cacheprovider tools/test_owns_gate.py tools/test_owns_gate_retry.py
  tools/test_owns_gate_md.py -q` -> `145 passed in 9.76s`.
- In C's worktree, `python -B -m pytest -p no:cacheprovider tools/test_dispatch_gate_md.py tools/test_critic_snapshot.py
  tools/test_dispatch_cut.py -q` -> `126 passed in 15.93s`.
- In the merged scratch world (A's HEAD archive with B's and C's files laid over it), the six B and C files ->
  `271 passed in 24.29s`.
- The scratch mutant at `dispatch_gate.py:881` (always `BLOCK_MESSAGE_NO_SUBAGENT_TYPE`) -> `4 failed, 372 passed`.
  Restored, sha 901b193d = 901b193d.
- Scratch: designer.md set to `model: claude-sonnet-5-5`, `-k role_bound_model` -> `1 failed, 8 passed`. Restored, sha
  c508e396 = c508e396.
- In FG7-81's worktree, `python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py` ->
  `=== test_selftest_shard: 101/101 ok ===`.
- The `named_by_problems` probe (finding 3) is quoted there. On the real tree it printed `real tree: 0 46`.
- All worktrees had a clean `git status --short` after the runs.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "FG7-14: role_bound_model is the one reader of a role's model; tier_echo unchanged by Lead F6 (a); journal_echo reads the journal model; no live tool, probe or rule text emits a tier-form label after A (grep with positive control). One analog outside owns: tools/savings_report.py:133 also calls tier_ladder.bindings directly (finding 2). FG7-81: forge side is card B (E12); no forge reader parses named_by entries.",
  "fixes": [
    "1 (FG7-14 A, does not block): tools/test_dispatch_gate.py:3322-3334 cut rows scout_default, critic_config, builder_no_model, designer_role_file, no_role_file (duplicates of test_journal_hooks.py:118, :119, :168, :169, :172; designer row pins live .claude/agents/designer.md)",
    "2 (FG7-14 A, does not block, needs tools/tier_ladder.py outside owns): tools/dispatch_gate.py:1102 re-derives the private defaulted flag via a second tier_ladder.bindings call; expose the flag from the ladder and make one call",
    "3 (FG7-81 A, does not block): ai-packages/qa-factory/scripts/selftest.py:794 refuse any ':' left in rel (x.md:57-60, :L57 now pass as outside); add an x.md:3-4 variant to the 'a line number' row",
    "4 (FG7-14 B and C, record only): add a handoff addendum for 3fc1d24c and 72270bdf with the Lead answer and the re-run witness (145 / 126 before, 271 after)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-fg7-14-dispatch-label-role-card.md sections 0-11",
      "docs/tasks/specs/20261118-fg7-81-named-by-pointer-check-card.md sections 2-4, 8, 11",
      "four handoffs t-1426, t-1427, t-1428, t-1432",
      "git diff origin/main...HEAD of all four worktrees",
      "tools/tier_ladder.py:20-140",
      "tools/journal_validator.py:862-880",
      "tools/test_dispatch_gate.py:480-560, 1836-1860, 3300-3350",
      "ai-packages/qa-factory/scripts/selftest.py:690-715, 750-840",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:218-232, 386-416"
    ],
    "reruns": [
      {"command": "A worktree: python -B -m pytest -p no:cacheprovider tools/test_dispatch_gate.py -q", "result": "376 passed in 38.79s"},
      {"command": "B worktree: pytest test_owns_gate.py test_owns_gate_retry.py test_owns_gate_md.py -q", "result": "145 passed in 9.76s"},
      {"command": "C worktree: pytest test_dispatch_gate_md.py test_critic_snapshot.py test_dispatch_cut.py -q", "result": "126 passed in 15.93s"},
      {"command": "scratch merged world main+A+B+C: the six B/C files", "result": "271 passed in 24.29s"},
      {"command": "scratch mutant dispatch_gate.py:881 always BLOCK_MESSAGE_NO_SUBAGENT_TYPE", "result": "4 failed, 372 passed; restored sha equal"},
      {"command": "scratch designer.md model changed, -k role_bound_model", "result": "1 failed (designer_role_file), 8 passed; restored sha equal"},
      {"command": "FG7-81 worktree: python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py", "result": "=== test_selftest_shard: 101/101 ok ==="},
      {"command": "named_by_problems probe on line-pointer forms and the real tree", "result": "':57' PROBLEM; ':57-60', ':L57', '#L57', ':57 ' OUTSIDE; real tree 0 46"}
    ]
  }
}
```
