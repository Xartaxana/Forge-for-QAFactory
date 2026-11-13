# t-327: critic-on-plan, t-322 OH8-4 (role-read texts get the package root through `runtime_paths.script_command`)

Spec: `docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md` (rev 1 + §7a, every fork decided as recommended). Everything was read in `.claude/worktrees/read-main` (origin/main). This verdict is an input to acceptance: the Lead decides.

## Verdict: fit_with_fixes. 2 fixes block the builder start (B1, B2), 4 are small spec edits (B3-B6), 3 are notes (N1-N3)

### B1 (blocks Part 2): the D3 marker cannot match `ON_CARD_RE`, so Part 2's own DoD fails
`test_ahead_cards.py:166`: ``ON_CARD_RE = r"`([A-Za-z0-9_]+\.py)[^`]*`\s*(?:\([^)]*on your card...``. It needs the script name inside backticks.
§3.2 D3 gives the new value `ticket_adapter: "ticket_adapter.py (on your card)"`, which has no backticks. The data join therefore finds
only `("qa-requirements-tester", "branch_accounting.py")`, and DoD (4) `found == DATA_CARD_SCRIPTS` goes red. The builder would have to guess a fix.
**Fix:** D3 value ``"`ticket_adapter.py` (on your card)"``, with the same spelling in §3.2 and §7 F2. The parser keeps backticks inside a YAML
double-quoted string, and E19 still holds (old forms fill the plain `text` field).

### B2 (blocks Part 1 row C7): C7's reader column is wrong. By §1.1's own line the site belongs to OH8-5
§3.1 C7 says the reader of `stage_done.current_code_diff_refusal` (`stage_done.py:209`, checked) is "qa-scout (Bash)". The repo says otherwise:
- the scout's card `brief_pack.TOOLING["qa-scout"]` (:185-198) has no `stage_done.py`;
- `agents/qa-scout.md` mentions `implementation_source` only as a dispatch input (:86);
- the CONDUCTOR runs it: `skills/qa-story/phases/s1.md:35` ("record it by code: `stage_done.py --task ...`") and `:334`;
- the DRIVER runs it: `driver_machine.py:928` (`implementation_source=diff` through `self.py("stage_done.py", ..., check=True)`).

No role reads C7. Under §1.1 ("conductor-read when NO role reads it"), a literal with no role reader goes to OH8-5, which
runs its host experiment first. **Fix (Lead picks; recommendation (a)):**
- (a) drop C7 and its row C7-E4 from Part 1 and hand `stage_done.py:209` to OH8-5 next to `story_step.py:1034/:1101`. Move the
  missing-script row (E5) to C6 or C8: `C6-E4`, a root lacking `scripts/runtime_probe.py`, gives the gap text and no `python ` path;
- (b) keep C7 and add a clause to §1.1: "a text a PERSON may read (driver mode prints the refusal) moves here whatever OH8-5 finds,
  because a person's shell never holds the variable". Then check `:1034/:1101` against the same clause in the same edit. Without that
  check, the line has two roads (P31).

### B3: sites C11-C13 have no test row, and C11 carries the one real breakage named in E2
DoD (2) has rows C1-C10 only. C11 (`run_role`, `driver_dispatch.py:697`, checked: `python {self.scripts}/<name>.py` UNQUOTED) is every
driver-mode role prompt. C12 is at `:2491` and C13 at `story_step.py:618/:734` (both checked). Without a row, putting the hand spelling back stays green.
**Fix:**
- add a row `C13b` through `run_mode_refusal(task, switch)`, a pure function;
- add a row `C13a` through `_s5_plan_init` with `SP.init` raising `PlanUnreadable`;
- add a row `C12` through `s1_reference_window` with `self.py` stubbed;
- for C11, either a row through `run_role` with `run_claude` stubbed to capture `full_prompt`, or a NAMED exemption ("C11: judged by
  the one-off AR-13 grep in the report; run_role cannot be driven cheaply"). C11 also gets the E2 assertion: a root with a space
  yields one double-quoted word.

### B4: no §5 edge row for C11 `must_exist=False` (asked in key 5)
§8 says it in passing. **Fix:** add E23: "C11 names the placeholder `<name>.py`, which never exists, so the existence check is off. A copy
whose `scripts/` is missing is not detected HERE: the card head has the same form (OH5-2 N4), and the conductor's qa-doctor owns the gap.
Invariant: the prompt and the card head spell the root one way."

### B5: the merge mechanics of the shared `test_ahead_cards.py` (key 4)
The two lists of owned functions are disjoint. Two shared regions are still left unassigned:
- the module import header (:29-49): Part 1 needs six heavy modules, Part 2 needs `env_probe` and `runtime_paths` (`handoff` is already
  imported at :46);
- the gap between the end of `charter_card_join` (:191), which Part 2 extends, and `def main` (:194), where a new function naturally lands.

**Fix:**
- every new import goes INSIDE its owning function (lazy), and the header is owned by neither part;
- `role_text_roots` goes directly before the `if __name__` block, not between `charter_card_join` and `main`;
- say "ONE code critic after both parts converge (R13-g; D-0048: the later part merges, resolves, and the critic comes after the merge)".

The merge order is otherwise free: the parts have no semantic dependency, and E16 keeps Part 2's expander, reader and tokens in one commit.

### B6: F4 does not say why the existing token family is not reused (P31, key 3)
`runtime_paths.py:357-361` already defines `{plugin_root}` and others, and they sit in Part 2's `given`. A builder will ask why a second
token grammar is added to the same module. **Fix:** one sentence in F4: "`PLUGIN_TOKEN` is a stored-path hint. `_resolve_text` resolves it in
leading position only, to a bare path, with no `python`, no quoting and no gap text. `{script:<name>}` is a command spelling resolved
through `script_command`. These are two actions, each with one road."

### N1 (note): the neighbouring class in the same functions, bare `handoff_help.py`
C9 `story_step.py:280` and C10 `handoff_check.py:2852` tell a Bash role "run handoff_help.py --file ...". The name is bare, with no path,
it is not on any card (Grep `handoff_help` -i over `brief_pack.py`: none; the same Grep over `scripts/*.py` finds 20+ hits), and it has no marker.
Sweep-the-artifact asks for a verdict per neighbour. Proposed: "n/a: the card head names the root pattern". Sweeping it would also break
the keep pin `test_handoff_values_refusal.py:81` (`"handoff_help.py --file"`). Otherwise add it to R1 with `guard_pre_tool.py:2256`.

### N2 (note): OH8-5's carrier does not name what §1.1 hands to it
The batch-8 OH8-5 row's "Пишет в" names `skills/**`, `common-rules.md`, `source_exclusions.py`, `config_contract.py`, `run_headless` and
`evals.json`. It does not name `story_step.py` (:1034/:1101), and `stage_done.py` would join if B2 (a) is taken. The OH5-2e finding carries
these sites only by pointer to the t-254 §2 census (which does list them). The batch file is frozen. **Proposal (Lead):** a line in the
batch-8 "Остатки", or in the OH5-2e finding, naming those sites and the hot-file queue they need.

### N3 (note): no detector for the class itself
After this node, `driver_dispatch`, `driver_stage_s7`, `execution_request` and `handoff_check` hold no literal, and neither does
`stage_done` if C7 stays. Only the named rows guard them. `refusal_registry._host_root_lines` (:1125) scans `SCANNED` only. Proposed
residual R4: widen that one scanner's file list once OH8-5 clears `story_step.py`, rather than adding a second AST scanner in a test (AR-15).
Also stale: the quarantined `test_package_generation.py:490-494` (P4/P5) still pins the literal in `agents/*.md`, which contradicts keep
`test_ahead_cards.py:190`. Report it when that file leaves quarantine.

## Answers per key
1. **Facts by trail.** Rows checked at their lines: C1 :3868, C2 :3910, C3 :3951, C4 :700, C5 :1040, C6 :2751 (drift confirmed),
   C7 :209, C8 :651, C9 :276, C10 :2836 (drift confirmed), C11 :697, C12 :2491, C13 :618/:734. All match. Readers: C1-C3 and C9/C10 hold;
   C6 holds (`run_suite --mine` raises the S5 `MineRefusal`, automator); C8 holds (strategist reads the file); C7 is wrong (B2).
   Census: Grep `claude_plugin_root` -i over the package gives **402 in 72 files**, which reproduces §2 (positive controls in the same call:
   hooks.json 19, codex.json 28).
   - Role-read literal missed: none found. The remaining `scripts/*.py` hits are legitimate per t-254 §2 :379 or are comments:
     delivery_verdict, regression_scope, refusal_registry, install_smoke, driver_core, session_env, brief_pack.
   - `judge.md`, `handoffs.md` and `common-rules.md` are no role's `plugin:` door: the Grep -i `plugin:(references/)?(common-rules|handoffs|judge|human-text|stand-answers)`
     finds only the slice headers. Positive control: `plugin:references/templates/requirements-register` finds `brief_pack.py:94`.
   - The slices are clean (`test_ahead_cards.py:190`).
   - Same-file hand spellings: grep over the six owned files finds exactly C9-C13.
2. **The role/conductor line.** Correct for every carrier except C7 (B2). N2 is the hand-over gap.
3. **One road.**
   - F2: the card marker is one road with OH5-2's charter join. The data join reads its roles from `ROLE_FILES` and `to_role`, so no
     list is copied.
   - F3/F4: `env_probe.stand_answers` is the only code reader. The Grep `stand-answers|stand_answers` -i finds the other modules only through
     it; the tests read raw only in quarantined `test_stand_health.py:754`.
   - `fill`'s `_Words`/format_map leaves an unexpanded `{script:...}` unchanged: the format-spec error is caught (:327-330), so even a
     broken expansion is visible, never wrong.
   - No second road is left, given the B6 sentence.
4. **The cut.** The parts' file sets are disjoint. The test file needs B5. Merge order is free, with one critic after convergence.
5. **Edges.** Temporal: E11 and E16 are sound. The old reader never meets a token because the expander, the reader and the tokens land in
   one commit; quarantined `test_login_body_fields.py:422` reads through the reader. `--plugin-dir`: E1 is sound (`driver_core.py:416`, :501;
   the R sites run from `self.scripts` = X in a driver run). C11 `must_exist`: B4. Mutations: Part 1 rows are discriminating (the `$` root
   forces single quotes) but miss C11-C13 (B3). Part 2 has T-rows plus the vacuity guard plus a reader row, and is complete once B1 is fixed.
6. **Fix before the builders start:** B1 and B2. B3-B6 are edits to the same spec in the same move.

P31 (rule 19): no exclusion of a language, project or case. One open two-road risk remains, the §1.1 line against C7 (B2). Duplication (rule 18, applied to the plan): the
only second road the plan could introduce is the token family (B6). Code quality: n/a for a plan gate.
Class completeness: SIBLING_MAP has no plugin-root axis. Axes stop at 36, and axis 37 is queued to the Lead (t-254 F7). In-artifact sweep: C11-C13 are
covered; the bare-name neighbour is N1. Outside the node: R1 (named, its own node), N2, N3.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: D3 new value lacks backticks, so ON_CARD_RE (test_ahead_cards.py:166) cannot match it and DoD (4) DATA_CARD_SCRIPTS equality fails",
    "B2: C7 reader is not qa-scout (scout card has no stage_done.py; s1.md:35/:334 conductor, driver_machine.py:928 driver run it); by spec section 1.1 a literal with no role reader belongs to OH8-5"
  ],
  "fixes": [
    "B1: D3 value becomes a backticked ticket_adapter.py followed by (on your card), in 3.2 and F2",
    "B2: correct the C7 reader; (a) move stage_done.py:209 to OH8-5 and move the missing-script row to C6 or C8, or (b) add a person-reader clause to 1.1 and re-check story_step.py:1034/:1101 under it",
    "B3: add rows C12, C13a (_s5_plan_init), C13b (run_mode_refusal); C11 a run_role row with run_claude stubbed or a named exemption, plus the space-root assertion",
    "B4: add edge E23 for C11 must_exist=False (placeholder never exists; same form as card head)",
    "B5: lazy imports inside owning functions; role_text_roots placed before the __main__ block; one code critic after convergence",
    "B6: F4 states why PLUGIN_TOKEN family (runtime_paths.py:357-361) is not reused"
  ],
  "class_completeness": "No plugin-root axis in SIBLING_MAP (stops at 36; axis 37 queued to Lead). In-file hand spellings C9-C13 all covered; bare handoff_help.py neighbours in C9/C10 need a verdict (N1); OH8-5 carrier does not name story_step.py:1034/:1101 (N2); no static class detector beyond rows (N3, widen refusal_registry._host_root_lines later).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md",
      "read-main ai-packages/qa-factory/scripts/runtime_paths.py (whole)",
      "read-main driver_dispatch.py 594-730, 2486-2494, 3860-3875, 3945-3965",
      "read-main driver_stage_s7.py 1030-1050; execution_request.py 2738-2766; stage_done.py 194-212, 615-660",
      "read-main story_step.py 268-282, 612-622, 722-737, 1026-1037, 1094-1104; handoff_check.py 2810-2856",
      "read-main driver_core.py 405-420; driver_machine.py 915-930; delivery_verdict.py 268-320; refusal_registry.py 1110-1150",
      "read-main env_probe.py 221-263, 320-332; brief_pack.py 84-97, 180-215; test_ahead_cards.py 1-50, 130-200, tail",
      "read-main references/stand-answers.json 108-118; templates/requirements-register.md 108-116, 176-183; handoffs/s0-setup-to-scout.yaml 50-70",
      "read-main test_stand_access.py 561-608; test_package_generation.py 480-500; test-layers.json keep/quarantine sections",
      "read-main plans/piles/onboarding-hooks/batch-8 header and rows OH8-4/OH8-5; findings OH5-2e",
      "docs/tasks/specs/t-254-oh5-2-plugin-root-given.md census line 71 and 379",
      "read-main docs/SIBLING_MAP.md axis headings",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "Grep -i claude_plugin_root over read-main ai-packages/qa-factory, count", "result": "402 occurrences in 72 files; hooks.json 19, codex.json 28 (matches spec section 2)"},
      {"command": "Grep -i plugin:(references/)?(common-rules|handoffs|judge|human-text|stand-answers) excluding tests", "result": "only slice header comments; positive control plugin:references/templates/requirements-register -> brief_pack.py:94"},
      {"command": "Grep -i stand-answers|stand_answers over the package", "result": "code reads only through env_probe.stand_answers; raw read only in quarantined test_stand_health.py:754"},
      {"command": "grep hand spellings (HERE.as_posix, self.scripts) over the six owned files", "result": "exactly driver_dispatch 697, 2491; story_step 276, 618, 734; handoff_check 2836"}
    ]
  }
}
```
