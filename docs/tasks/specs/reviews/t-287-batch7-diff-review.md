# t-287: diff critic for onboarding-hooks/7 (OH7-1, OH7-2, OH7-3/4, OH7-5), one pass for the topic (R13-g)

critic: opus (claude-opus-5-5), 13.11.2026. Spec: the rows and brief in `.claude/worktrees/oh7-5/plans/piles/onboarding-hooks/batch-7-ostatki-t-263.md`,
plus the five findings `20261113-*` the rows name. Branches are diffed against `refs/remotes/origin/main` after `fetch -q origin`.
Heads checked: oh7-1 bdfbbc6, oh7-34 2f6afa6, oh7-5 4274d7f, oh7-2 431094b; `merge-base --is-ancestor 0a0db4f` is true for all four.

## Verdicts per node (input to the Lead's acceptance; the acceptance decision is the Lead's)

| Node | Verdict | Fixes that block the merge |
|---|---|---|
| OH7-1 | fit | none (2 notes, not blocking) |
| OH7-3/4 (oh7-34) | fit_with_fixes | F34-1, F34-2, F34-3 |
| OH7-5 | fit_with_fixes | F5-1 (text defect inherited from the finding's prescribed wording, so it is a spec defect of the dispatcher) |
| OH7-2 | fit_with_fixes | F2-1, F2-2 |

## Q1: OH7-3 raises `json.JSONDecodeError`. Is that reuse, or a way around the scanner?

**It gets around the scanner, and the fix is required.** Evidence:
1. Behaviour does not depend on the type. `inject_context.dispatch` catches `except ValueError` (oh7-34 `inject_context.py:729`).
   `refuse_native_stage` (`:510-524`) chooses NAMED or INERT from two things only: `isinstance(exc, StateConflict)` and
   `native_context.launch_pending`. `launch_pending` returns True for a file that is not an object (`native_context.py:96-109`), so
   a plain `ValueError` takes exactly the same road: an INERT row and exit 2. The subclass only affects whether the scanner sees the raise.
   `REFUSAL_RAISES = ("StateConflict", "ValueError")` matches `ast.Name` only (`refusal_registry.py:872-881`), and `json.JSONDecodeError(...)`
   is an `ast.Attribute`. My own AST walk of the six SCANNED files found it as the only new raise the scanner does not see
   (`oh7-34 native_context.py 191 json.JSONDecodeError`; the same walk also lists the known `LaunchIdRowRefused` sites, which serves as the positive control).
2. The text the role sees is malformed. `JSONDecodeError(msg, '', 0)` formats itself as `msg + ": line 1 column 1 (char 0)"`. Control run:
   `'launch packet X.json is not a JSON object; relaunch the role under a unique task name: line 1 column 1 (char 0)'`.
   The refusal reports a parse position for JSON that parsed without error (FR-1: it does not say what is wrong).
3. It adds a factory-authored refusal text with a door but no A24 row, and AR-18 (one shape, one reader) is touched without being named in the commit.
   FR-57 and AR-18 apply. The rows' door is fine, and so is the reuse of the road. The type is not.

**F34-1 (blocks).** Make the change at `native_context.py:190-192`:
`raise ValueError('launch packet ' + path.name + ' is not a JSON object; relaunch the role under a unique task name')`.
Add an A24 row in the `native_context.py` block of `refusal_registry.py`, after NC-launch-pending at about :366:
`{"id": "NC-launch-packet-not-object", "file": "native_context.py", "function": "stage", "call": "launch packet ' + path.name + ' is not a JSON object",
"refuses": "a staging whose key already holds a file whose JSON is not an object (list, string, number, null)", "override": "",
"unpassable_because": "the file cannot be read as a launch, so nothing can be passed over it; the row written is inert (launch_pending is True for it); the door is a relaunch under a unique task name, named in the text",
"test": "scripts/tests/test_doctor_context.py (NativeStageRefusal: stage over an existing packet file table)"}`.
The census ref also changes: `judgment-census.json:574` (`native_context.py`/`stage`) gets `, A24:NC-launch-packet-not-object`.
Test changes: `test_doctor_context.py:485` `assertIsInstance(..., json.JSONDecodeError)` becomes `assertNotIsInstance(..., json.JSONDecodeError)` for the
'unreadable' rows, so the test catches a return of the evasion. The commit names `AR-18`.
Widening `REFUSAL_RAISES` to `ast.Attribute` would not catch this case: the scanner cannot learn from the AST that `JSONDecodeError` subclasses `ValueError`.
The rule that holds across the class is "raise the base name". F2-2 widens the scanner to subclasses defined in the scanned file.
Owns: `refusal_registry.py` and the census belong to OH7-2's owns. The Lead either widens OH7-34's owns for this fix round or puts the row
into OH7-2's fix round (F2-x), which merges after it. In both cases it goes in the same PR batch.

**F34-2 (blocks; same move).** The A24 row NC-launch-pending, `refusal_registry.py:363-365` "unpassable_because": `... a relaunch under a unique task
name is the door - the message does not say so yet` is now false, because OH7-4 added that door to the message. Change it to `... is the door, and the message names it`.
The producer and its reader move together (AR-22). Without this, the merged tree carries a stale statement (checked on the composed merge, see Q5).

**F34-3 (blocks; a neighbouring class on the same surface, the stage pre-read).** Empty or broken JSON (`''`, `{broken`) still raises a bare
`JSONDecodeError` from `json.loads`. The role reads `INJECT: Expecting value: line 1 column 1 (char 0)`, with no file name and no door. The
finding said the non-object case should take "the same road as corrupt JSON — a refusal naming the file and the door", and that road does
not exist. Proposed: put `json.loads` inside `try/except ValueError` and raise the same `ValueError('launch packet <name> cannot be read or is not a JSON
object; relaunch the role under a unique task name')`. That gives one refusal and one row for both classes (P31). The test's 'undecodable' rows then join 'unreadable'.
**This is a fork for the Lead:** the brief's non-goal "do not change the text, type and order of `native_context.stage`'s raises" can be read as covering
the implicit `json.loads` raise. If the Lead keeps that reading, F34-3 becomes a node in the next untaken batch (`узел: <id>`) rather than a fix here.
The decision belongs to the Lead.

Neighbours from finding item 2, which I checked myself: `_session_packets` (`native_context.py:62-74`) already does `except (OSError, ValueError)` + `isinstance(data, dict)`,
so it does not apply. `_said_write_failure` `data.get` (`:160`) gets `data` only from `_session_packets` (dicts), so it does not apply. `launch_pending` already treats a non-object as True, so it does not apply.
The OH7-4 tail is correct. Its prefix `A factory launch is awaiting SubagentStart` is byte-identical, the A24 key still matches (`--check` is clean on the merge), and the test checks the prefix.
Quality note (not blocking): the literal `relaunch the role under a unique task name` now appears 3 times in `native_context.py` (:191, :195, :232).
A module constant `RELAUNCH_DOOR` would keep the three doors identical. Do it in the F34 round.

## Q2: OH7-1, `_publish(binary=)`

Traced against `event_store.py:180-202` (oh7-1):
- "x" semantics: `tmp.open("xb")` keeps exclusive create. The `FileExistsError` retry loop and the rule "unlink only after a successful open" are unchanged for both modes.
- fsync and retry: the shared body runs `write -> flush -> os.fsync(fileno) -> replace_file` (the WinError 5/32 retry), and the `finally` unlinks. A binary stream has the same `fileno`, so this holds.
- atomic_text is byte-identical: the non-binary branch is the old call verbatim (`tmp.open("x", encoding="utf-8", **open_options)`), and `atomic_text` and `atomic_json` are unchanged.
- The control rerun is green (below). The test checks exact bytes (BOM, CRLF, non-UTF-8) and that no `.tmp` is left. Its spy confirms the call goes through `_publish`.
- The behaviour change accepted by the coordinator (dashboard now LF, `?` for a lone surrogate) follows from `atomic_text` and is in the changelog.
- Choosing `atomic_bytes` over `atomic_text` for the backup is correct. `atomic_text` with `errors="replace"` would corrupt non-UTF-8 bytes, and the backup must be the exact bytes.
- Note N1-1 (queue, not blocking): when `binary=True`, `**open_options` is silently ignored (`:186`). A future caller passing `newline=` with binary would lose it without any error.
  Use `assert not open_options` in the binary branch, or document it.
- Note N1-2 (fix if a round happens): the docstring `:181` says "behind `atomic_json` and `atomic_text`", and it should also name `atomic_bytes`.
- Third writer: `grep -rniE '\.tmp["'"'"']|os\.replace\(|tempfile\.(mkstemp|NamedTemporaryFile)'` over `scripts/` + `hooks/` (excluding tests)
  finds about 30 hand-rolled temp-then-replace publishers (app_card:574, baseline_contract:169, report_facts:4561/4659, ledger:1864, …). The positive
  control is `event_store.py:185`, which the same grep finds. The node's own class, a 32-hex `uuid4().hex` temp name, now has 0 hits (`grep -E 'uuid4\(\)\.hex[^\[]*\.tmp'`).
  The positive control is the same grep on `origin/main:factory_dashboard.py`, which finds :4171. The wider class (bare `os.replace` with no retry) is already queued:
  `plans/piles/package-ci/findings/20261113-golyj-os-replace-v-41-mestah-33-fajlov-bez-povtora-na-windows.md`. It is not a finding here.
- Leftover (optional in the finding, "можно сузить"): the `{8}|{32}` alternative of N8a in `driver-golden-rules.json` can now narrow to `{8}`.
  `test_driver_golden.py` is quarantined. Line for «Остатки»: `N8a: сузить {8}|{32} до {8} после OH7-1 | перенос: package-ci | обоснование: файл в карантине | подтвердил: —`.

## Q3: OH7-2, the 24 rows

Control run: on oh7-2 I ran `RR.sites()` for the two files and matched each site against `_covers`. Result: 24 sites, and each has exactly one row
(codex_roles 35/49/61; host_adapter 80, 171, 185, 240, 247-279 (8), 579-624 (9)). Prefixes are verified against the source:
CR-role-missing `codex_roles.py:49`, CR-role-mismatch `:61` (f-string unparsed to `Native {role} {key} mismatch`), HA-rewritten-input `host_adapter.py:240`,
HA-patch-not-text `:247`, HA-call-shape `:579`, HA-role-read-only `:603`, HA-connector-orchestrator `:624`. I checked the doors and catch sites in code. CR rows: `inject_context.py:669-673`
catches, writes `note_denial` and exits 2, as claimed. HA-patch-* rows: `guard_pre_tool.py:3060-3068` catches the ValueError from `mutation_events` and blocks with
`escalate("PT-patch-unchecked")`, as claimed (the row says "guard_pre_tool catches", which is accurate through `mutation_events`). The `override` of the connector rows matches the PT-external-writes convention.

**F2-1 (blocks: A24 accepts a row only with "the test that proves it", `refusal_registry.py:1128-1130`, and a citation of a test that does not
exercise the refusal turns the row back into prose).** I searched the tests tree case-insensitively. The positive control is `Native Codex role missing`, which is found in test_doctor_context.py:
- HA-role-nested-delegation cites `test_role_policy_reads.py`: `grep -n "Agent\|Task\b"` finds nothing there (the same file has 2 hits for `role_policy`).
- HA-doctor-no-tools cites `test_doctor_access.py`: no `diagnostic` hit there. The actual test is `test_codex_hooks_matchers.py:298` (`factory_diagnostic=True`).
- HA-event-not-object cites `test_hook_lifecycle.py (guard_pre_tool.py --selftest, unparsed event)`: that file does not mention `guard_pre_tool`,
  `selftest` or `unparsed`, and `hook event must be an object` appears in no test.
- HA-stdin-chars, HA-exec-tty cite `test_codex_hooks_matchers.py`: its tty cases (:252-258) exercise the CELL call-shape refusal ("drop the tty
  option", HA-call-shape), not `role_policy`'s `exec_command` tty block. No test sends `write_stdin` with `chars`.
- HA-tool-input-not-object: `tool_input must be an object` appears in no test.
- HA-patch-path/-orphan-content/-move/-move-empty/-line/-empty/-not-text cite `test_codex_host.py (mutation_events on apply_patch)`: that
  file exercises only one malformed input (`:217`, `'unknown patch'`, which is the envelope). Seven of the eight rows' raises are reached by no test.
Exact fix: extend the node's own test `test_doctor_context.py:554` with one parameterised table (TESTING.md, a table of cases) that drives each of these
sites through its public function (`normalize(...)`, `patch_operations(...)` with 8 malformed patches, `role_policy(...)` for Agent, write_stdin+chars,
exec_command+tty, factory_diagnostic). Each row asserts that the raised or blocked text starts with its registry `call`. Then repoint each row's `"test"` to that
test (and HA-doctor-no-tools also to `test_codex_hooks_matchers.py:298`). The cheaper option, only if the Lead chooses it, is to correct the citations to what actually
exercises each refusal and send the untested ones to a node. The test field must not stay false.

**F2-2 (blocks: the node's own enumeration is incomplete, and its changelog claim "every raise or block they carry now has a registry row" is
false).** `host_adapter.py:716` and `:719` `raise LaunchIdRowRefused(...)`, a `ValueError` subclass (`:703`), are invisible to `sites()`.
My AST walk above lists both. Finding item 1 required "every other ValueError of these files: a row, or an explicit 'not a dispatch refusal: why'".
LaunchIdRowRefused is a ValueError, and its callers `host_dispatch.py:258` and `agent_autobind.py:158` catch `except ValueError`. The node should close it, not leave
it to a queue line, because the file was brought into SCANNED by this node. Exact fix: in `_refusal_calls` (`refusal_registry.py:1056`) collect, once per tree,
the names of `ClassDef`s whose bases include a name in `REFUSAL_RAISES`, and treat a raise of such a name as a refusal. This is derived from the AST, not a
list in code (AR-1). Then add 2 rows, `HA-launch-id-row-unreadable` (`call`: `{target.name} cannot be read for the row`) and `HA-launch-id-row-unusable`
(`{target.name} holds no usable row`), function `launch_id_keys`, door "restore the file from the package" (owner: environment). The census row
for `host_adapter.py`/`launch_id_keys` gains a `ref` if one exists, and the C-checks of `test_judgment_census.py` decide. If the widening turns the census red
on files outside SCANNED (it uses the same `sites(files=...)`), keep the widening and add the rows it names. Do not narrow it.
The widening also closes Q1's class for the future, except the `json.*` attribute form, which F34-1 removes.

## Q4: OH7-5

- Robustness: `" ".join(text.split())` normalises line wrapping and indentation, so re-wrapping s5.md:234-235 does not break the test (the clause there is split
  across a newline, and the test passes, so normalisation is exercised). A missing s5.md makes `read_text` raise `FileNotFoundError`, and the
  script runner exits with a traceback. That is red, and it fails safely. It is acceptable.
- I searched for twins of the old text: `grep -rniE "has to live inside the application tree|test that has to live"` over the package (md/py/json, excluding changelog.d)
  finds only the two new constants. The positive control is that the same grep finds `guard_app_under_test.py:25`. No stale twin is left.
- **F5-1 (fix before merge; spec defect, the text came from the finding).** `TEST_PATH_HOW` is emitted only by `permission_pass` (`guard_app_under_test.py:195`),
  which runs only on a write into `protected_app_paths` (the application tree). The new first sentence now names "or in the test repository", and the same paragraph
  goes on "The person can open test files there for the automator … waiver.py … protected test path". s5.md:264 offers that waiver
  "for a place inside the application tree only", and for the test repository the door is a config record (`run.levels`), not a waiver. The refusal
  therefore suggests a door that does not exist for half of the case it now names (FR-2, FR-37). Exact fix: keep the shared clause (FR-37 alignment stays
  pinned) and scope the door: `"... do not write it another way: name the path in your handover and halt. Inside the application tree, the person can open test files for the automator; ..."`.
  Change `guard_app_under_test.py:27-28` and `test_protected_test_path.py:604-605` `HOW` together. The decision belongs to the Lead, since it amends the finding's wording.

## Q5: merge hazards

`git merge-tree --write-tree` gives no textual conflict for any pair: oh7-2×oh5-2a, oh7-34×oh7-2, oh7-1×oh7-2, oh7-34×oh7-5, oh7-1×oh7-34.
- `refusal_registry.py`: oh5-2a changes the guard_pre_tool rows region and its own sites. oh7-2 inserts a block before `# --- guard_pre_tool.py` (about :369) and
  changes `SCANNED` (:56). The hunks are disjoint. The insertion point is next to the guard_pre_tool header, so a rebase with context drift can still collide there.
  Resolution: keep both blocks whole, with oh7-2's block above the guard_pre_tool header.
- `judgment-census.json`: oh7-2 changes the codex_roles (:91-92) and host_adapter (:402-407) rows only, and oh5-2a does not touch the census in its diff. No overlap.
- `test_doctor_context.py`: oh7-34 adds a method at about :458 (before `test_native_packet_refusal_rows`), and oh7-2 adds one at about :554 (end of `NativeStageRefusal`). Disjoint.
- Semantic check on the composed merge (oh5-2a + oh7-2 + oh7-34 + oh7-1 + oh7-5, commit-tree objects only, archived into the scratchpad):
  `refusal_registry.py --check`: no violations. `pytest test_doctor_context.py test_judgment_census.py test_refusal_registry.py`: 55 passed, 84 subtests.
  `test_refusal_registry.py`: 333/333 ok. `test_protected_test_path.py`: 381/381 ok.
- Interaction after the fixes: F34-1 and F2-2 both edit `refusal_registry.py` and the census. **Merge order recommendation:** oh7-1 and oh7-5 first (independent),
  then oh5-2a (wave 6, already queued ahead), then oh7-2 with F2-1/F2-2, then oh7-34 with F34-1..3 last, merging main into its tree. Its NC row and census ref
  land on top of oh7-2's scanner change, and the one re-run `refusal_registry.py --check` sees both. One critic re-review covers the two fix diffs.

## Q6: class completeness, duplication, quality, the standing questions

- CLASS (SIBLING_MAP): axis 32 (census <-> scanner `sites()`): oh7-2 updated the refs, and F34-1 and F2-2 owe their refs. Axis 18 (ratchets): no ratchet row raised in
  any of the four diffs. A24 `ANCHOR_FLOOR` is untouched (`git diff` shows no change to it). Axis 9 (test-file leaf) and the "person-granted passes" row of axis 5:
  OH7-5 changes text only, and F5-1 keeps the waiver scoped to the app tree as that row says. Axis 34 (one road): see ONE ROAD below. The publishers' wider class is queued
  (package-ci finding, above). Analogs outside this batch: none beyond the queued ones.
- DUPLICATION AND CONSISTENCY: OH7-1 removes two second roads (AR-15). I found no other 32-hex publisher (grep above, with its control). OH7-34: the door literal is copied 3 times
  (quality note above). OH7-2: none found. I grepped for a second refusal scanner (`grep -rn "ast.Raise" scripts/*.py`), and the only scanner is `refusal_registry._refusal_calls`, which matches axis 32.
  OH7-5: the test copy `HOW` duplicates `TEST_PATH_HOW` by design (pre-existing), and the new check pins both to s5.md.
- CODE QUALITY: no new function over 60 lines. In oh7-34 `stage`, `path.is_file()` is evaluated twice (:188-189), which is harmless under the lock. The type name in Q1 does not match
  what happened (a "decode error" for JSON that decoded), which is F34-1. OH7-1: N1-1 and N1-2. OH7-2: 24 rows of data, consistent with the existing rows' form.
- ONE ROAD (P31): no exclusion of a language, project or case was found in the four diffs. I grepped the added lines for `python|typescript|java|pytest|language` and found none. F34-3 is about one road for
  the two unreadable-packet classes. Its residual is a fix here or a node, as the Lead decides (above).
- ARCHITECTURE: oh7-34 touches AR-18 by adding a refusal without naming it (F34-1). oh7-2 names AR-18/AR-22, and F2-1 is an AR-22-adjacent trail defect. oh7-1 names AR-14/AR-15. oh7-5 names AR-9/AR-22.
- JUDGMENT: none. All the changes are shape checks or text. No census class was lowered, no `blocks_override` was added, and no census scan constant was edited (census diff read in full).
- Hygiene: no Cyrillic and no control bytes on any added package line (python scan of the diffs).

## Mechanical layer: control reruns

- `python -B test_event_store.py` (oh7-1 worktree): `Ran 48 tests ... OK`. This matches the builder's witness.
- `python -B refusal_registry.py --check` (oh7-2 worktree): `A24 refusal registry: no violations`. This matches.
- The composed merge runs (Q5) cover oh7-34's and oh7-5's witnessed test files. The counts are consistent with the builders' figures: 381/381, and 304 + oh5-2a's rows = 333.
- `raise json.JSONDecodeError(msg,'',0)` str form: `...: line 1 column 1 (char 0)` (Q1, item 2).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F34-1 native_context.py:191 raises json.JSONDecodeError so the A24 scanner does not see a new refusal; its text gains ': line 1 column 1 (char 0)'",
    "F34-2 refusal_registry.py:365 NC-launch-pending says the message does not name the relaunch door yet; OH7-4 made that false",
    "F2-1 at least 13 of the 24 new A24 rows cite a test that does not exercise their refusal (A24 'test that proves it')",
    "F2-2 host_adapter.py:716/:719 LaunchIdRowRefused raises are invisible to sites(); changelog 'every raise has a row' is false"
  ],
  "fixes": [
    "F34-1 native_context.py:190-192 raise ValueError(same text); add A24 row NC-launch-packet-not-object; census :574 ref; test :485 assertNotIsInstance JSONDecodeError; name AR-18",
    "F34-2 refusal_registry.py:363-365 unpassable_because: the message now names the relaunch door",
    "F34-3 (Lead fork vs the brief non-goal) wrap json.loads in stage: empty/broken file gets the same named ValueError with file and door, or open a node",
    "F5-1 guard_app_under_test.py:27-28 and test_protected_test_path.py:604-605: scope the waiver sentence to the application tree (s5.md:264)",
    "F2-1 test_doctor_context.py:554 add one table driving every host_adapter/codex_roles site to its keyed text; repoint row test fields",
    "F2-2 refusal_registry._refusal_calls:1056 also match raises of ClassDefs subclassing REFUSAL_RAISES; add rows for launch_id_keys :716 and :719",
    "N1-1/N1-2 (not blocking) event_store._publish: guard open_options under binary; docstring names atomic_bytes"
  ],
  "class_completeness": "Per node. OH7-1: the 32-hex publisher class is closed (grep with a control); the wider bare os.replace class is queued in a package-ci finding. OH7-2: 24 of 26 raises have rows; the 2 LaunchIdRowRefused raises are missing (F2-2). OH7-3: the neighbours from finding item 2 (:69 and :179) are checked n/a; the empty/broken JSON neighbour on the same surface is still unnamed (F34-3). OH7-4: its registry twin is stale (F34-2). OH7-5: no stale twin of the old text (grep with a control). SIBLING_MAP axes 32/18/34/5 walked.",
  "trail": {
    "read": [
      ".claude/worktrees/oh7-5/plans/piles/onboarding-hooks/batch-7-ostatki-t-263.md",
      ".claude/worktrees/oh7-5/plans/piles/onboarding-hooks/findings/20261113-* (the five named)",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (axes 5, 32, 34 and the headings)",
      "docs/tasks/specs/t-263-oh6-3-oh6-4.md (F-C, siblings, grep)",
      "oh7-1 event_store.py:140-215, factory_dashboard.py, migrate_coverage.py diff",
      "oh7-34 native_context.py:30-240, inject_context.py:505-560 and 715-745, refusal_registry.py:340-370 and 860-915",
      "oh7-2 codex_roles.py:30-65, host_adapter.py:165-290 and 570-740, guard_pre_tool.py:3050-3070, inject_context.py:660-690, refusal_registry.py diff and 1110-1130",
      "oh7-5 guard_app_under_test.py:20-40 and 165-215, skills/qa-story/phases/s5.md:230-270, test_protected_test_path.py diff",
      "tests cited by OH7-2 rows: test_codex_host.py, test_codex_hooks_matchers.py, test_role_policy_reads.py, test_doctor_access.py, test_hook_lifecycle.py (greps)"
    ],
    "reruns": [
      {"command": "python -B test_event_store.py (oh7-1 tree)", "result": "Ran 48 tests OK"},
      {"command": "python -B refusal_registry.py --check (oh7-2 tree)", "result": "A24 refusal registry: no violations"},
      {"command": "git merge-tree --write-tree on 5 branch pairs", "result": "no conflicts"},
      {"command": "composed merge oh5-2a+oh7-2+oh7-34+oh7-1+oh7-5: refusal_registry.py --check; pytest test_doctor_context/test_judgment_census/test_refusal_registry; test_refusal_registry.py; test_protected_test_path.py", "result": "no violations; 55 passed 84 subtests; 333/333 ok; 381/381 ok"},
      {"command": "AST walk of raises in the six SCANNED files not named StateConflict/ValueError", "result": "native_context.py:191 json.JSONDecodeError; host_adapter.py:716,:719 LaunchIdRowRefused; stage_guard:131 AttributeError and inject_context:652 TypeError are internal"},
      {"command": "python: str(json.JSONDecodeError(msg,'',0))", "result": "msg + ': line 1 column 1 (char 0)'"}
    ]
  }
}
```
