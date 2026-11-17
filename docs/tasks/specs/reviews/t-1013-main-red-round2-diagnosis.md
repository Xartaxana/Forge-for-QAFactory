# t-1013 — main red, round 2: diagnosis of R1–R9 (canon run 44013914849 at 26d4b9ac)

critic (opus), 17.11.2026. This is a diagnosis done BEFORE any fix (CLAUDE.md rule 3). I edited nothing in the repo and wrote no journal lines; this file is the only write.
Read from: the root checkout at 5751426c (= origin/main; 26d4b9ac plus one docs commit 5751426c that touches no file named below).

## Summary table

| Row | Cause commit (K1) | Hidden before? | Direction (K2) | Fix kind (K3) | Node (K4) |
|---|---|---|---|---|---|
| R1, R2 | ccb4a82f (t-850, 16.11 22:30): `run_allowed` and both test rows were born together. The test passes a `Path` for cwd, and `_decide_command` silently swaps any cwd that is not a `str` for `os.getcwd()` | Red in plain sight in forge-check 43987289826 (00:28Z) and 43991546078 (01:01Z). Then hidden behind the red `lint_ratchet --check` step from 43995181538 (01:23Z) to 44010947813. Round 1 did not look at forge-check (t-986 line 8) | Both sides have a defect. The test passes only when the PROCESS cwd is a dirty tree, so it is always green on the developer's dirty root and always red on the clean CI checkout. The product, on a doubt-refusing road, measures a tree other than the one it was given | product hardening (recommended) + test isolation; **fork F1** | N1 (Lead mechanism commit) |
| R3, R4 | 92781363 (t-905, FG7-5 `--node-cost`), import at forge_metrics.py:1721, merged in 254eaae7; e9204bde adds a second import at :1229. Both are function-level `import usage_report`, and the AST closure counts them | Same history as R1/R2: visible at 00:28Z, then hidden by lint_ratchet | The product is consistent with its own net rule ("the list is TAKEN FROM the closure"). The net is missing one row | **fork F2**; recommend a new `MECHANISM_PREFIXES` row | N2 (Lead mechanism commit) |
| R5 | 86ce4caf (t-965, T4a), guard_pre_tool.py:1187-1189: the values refusal now goes through `refusal("guard_pre_tool:PT-handoff-values", …)`, so `block` prints `expected:` / `door:` / `check:` lines | No: it came with wave A (merge 71d36190) | Product right (told-before-work T4a: "the stderr is the old text, then `expected:`/`door:` of the row and `check: <id>` last", test_detector_verdict.py:1791-1793). Pin stale | pin follows | N3 |
| R6 | 2d84d1f1 (T5r, t-970): the row-fields finding is built by `_sited(... DV.refusal("s5_precheck:row_fields", …))`, which adds `told` as the LAST key (s5_precheck.py:294-301) | No: wave A | Product right (the `_sited` docstring, T5r: "plus `told` as its LAST key"). Pin stale | pin follows | N3 |
| R7 | dce58459 (t-1004, cluster E): `gate_brief.MAX_LINES` 40 → 41, merged in 5eefb31e | No: round-1 fix | Product right: a named raise (AR-20) at gate_brief.py:65 "raised by the Lead 17.11.2026 on the owner's word about size limits". The test comment at test_gate_brief_and_retro.py:2126 itself says "the cap grows by them" | pin follows | N3 |
| R8 | c5b7bb6c (t-993, K5/real) added `qa-case-critic` to the producers of `handoff_check:findings_tooling` (stage-joints.json:5392-5396), and also to the census row `handoff_check.py::check_findings`. 26d4b9ac then regenerated the case-critic slice and raised its pin 18795 → 18830 | No: wave A | **Product wrong (the data is wrong). K10p's view is right**, see §R8. The census row is over-wide, and that row is what forced the K5 widening | data fix in one node: census + row + slice + pin back down | N4 |
| R9 | 86ce4caf (t-965, T4a) test only: `T4A_OLD['plugin read'] = 'c8455f9f8ed26987'` (test_detector_verdict.py:1758) was captured on Windows over the text `…(<PLUGIN>\scripts\hooklib.py)…`. The provocation at :1683 uses `str(Path)`, so the separator depends on the OS | No: wave A. Green on Windows (t-985 handoff: `test_detector_verdict 745/745`) and red on Linux | Product right (`PLUGIN_READ_MSG` is unchanged since 9ac00f09). **Test defect: an OS-dependent pin** | test fix (pin follows the OS-free form) | N3 |

## Evidence per row

### R1, R2: `tools/test_hygiene_gate.py` `run_allowed` rows

- **What the row asserts.** Row `git-checkout-on-a-dirty-tree` (test_hygiene_gate.py:573): `run_allowed("git checkout -- .", world["repo"])` is `False`, because `repo` is a dirty git repo (fixture :39-58, :66). The parity test (:631-637) says the same thing for `git reset --hard` in `repo`: whatever `decide()` denies, `run_allowed` must refuse too.
- **What the code does.**
  - The test passes `world[cwd_key]`, which is a `pathlib.Path` (fixture :66-69).
  - `run_allowed` (hygiene_gate.py:1567) forwards it unchanged as `_decide_command("Bash", cmd, {"cwd": cwd})`.
  - `_decide_command` (hygiene_gate.py:1502-1504) runs `cwd = payload.get("cwd"); if not isinstance(cwd, str) or not cwd: cwd = os.getcwd()`. So the rollback is measured on the pytest PROCESS cwd, not on `repo`.
  - `decide()`, by contrast, is fed `str(cwd)` (test :86). That is why the parity test's `decide` half passes and its `run_allowed` half fails.
- **CI vs local, measured.**
  - CI forge-check log 133807200585: `AssertionError: ('git-checkout-on-a-dirty-tree', [])` and `assert True is False` at :636. The CI checkout is clean, so the rollback is "allowed".
  - Local: `python -B -m pytest tools/test_hygiene_gate.py -q -k run_allowed` gives `29 passed`. The root checkout is dirty (git status: `M docs/OWNER_PRINCIPLES_INDEX.md`, `M logs/journal/dev1.jsonl`, …), so the swapped-in cwd happens to be dirty and the row passes by accident.
- **The one production caller** is journal_write.py:626 `hygiene_gate.run_allowed(cmd, str(root))`. It passes a `str`, so production is not affected today. The test still proves nothing about its own `repo` world.
- **K1.** `git log -S"def run_allowed"` and `git log -S"world[cwd_key]"` both return only ccb4a82f.
  - First red seen: run 43987289826, job 133718632040, `FAILED tools/test_hygiene_gate.py::test_run_allowed_battery[git-checkout-on-a-dirty-tree]`, `4 failed, 9502 passed`.
  - Hidden from 01:23Z: jobs 133745404670, 133757037859, 133769511773, 133779552165, 133784427772, 133786867728, 133792731082, 133794897895 and 133797541305 all end at `Run python tools/lint_ratchet.py --check` with exit 1, so pytest never ran.
- **K2.** The `run_allowed` docstring says the call judges "may the command … be RUN … from `cwd`" and "the ERROR DIRECTION is … REFUSES on doubt". Measuring a different tree is not refusing on doubt: with a clean process cwd it can falsely allow a rollback of a dirty `cwd`. The product hardening is the right direction. The test also needs its process cwd pinned, so its verdict stops depending on the developer's tree.

### R3, R4: the mechanism-net closure reaches `tools/usage_report.py`

- **The chain.** `.githooks/pre-commit:66` and `.githooks/pre-merge-commit:17` run `tools/forge_metrics.py`, which is in the net (mechanism_gate.py:257).
  - forge_metrics.py:1229 (`node_costs`, blame e9204bde) has a function-level `import usage_report`.
  - forge_metrics.py:1721 (the `--node-cost` branch, blame 92781363) has another, commented "lazy: only this mode prices (I-2)".
  - `_ast_tool_imports` (test_mechanism_gate.py:963-987) walks the whole tree with `ast.walk`, so nested imports count.
  - usage_report.py imports only `transcripts` (usage_report.py:187), which is already in the net (mechanism_gate.py:276). So the gap is exactly one module.
- **CI evidence.** Log 133807200585: `reaches modules outside the MECHANISM_PREFIXES net: ['tools/usage_report.py']` and `assert ['tools/usage_report.py'] == []`.
- **Side finding (not blocking).** The `_ast_tool_imports` docstring says "top-level `import X`", but the code walks every level. The docstring is wrong; the code is the conservative (right) direction.
- **K1.** 92781363 was committed 17.11 00:24 (local time). The t-905 handoff, line 7, names its DoD as `pytest tools/test_forge_metrics.py`; the closure judge `tools/test_mechanism_gate.py` was not in the DoD. The first red was 43987289826 (00:28Z), after which the row was hidden as for R1.
- **The two consequences are in fork F2.**

### R5: K3 of `test_guard_dispatch_budget_and_logs.py`

- I ran the one function in-process (`test_the_guard_parses_once_reads_the_form_once_and_prints_the_one_functions_text`):
  - GOT = the expected text plus `\n  expected: A Write of \`<ID>.values.yaml\` lands only when …\n  door: rewrite the file with the kept lines …\n  check: guard_pre_tool:PT-handoff-values`, then TRAPPED.
  - EXP = the bare text (test :895-899 builds `direct` without the row's lines).
- **Source.** guard_pre_tool.py:1187-1189 (blame 86ce4caf) wraps the text in `refusal(...)`. hooklib.py:984-999 `block` → `detector_verdict.spoken` prints the row's lines (detector_verdict.py:179-191). The test lines are from 9ac00f09.
- **Why the witness missed it.** The file IS mapped (`test-layers.json` keep row `test_guard_dispatch_budget_and_logs.py` covers `guard_pre_tool.py`, so `--witness-for scripts/guard_pre_tool.py` names it). But it is slow-listed in `scripts/slow_tests.json`, which means it is "judged by the batch canon". No canon was run on `wave-a/integrate` before merge 71d36190: `ci_read.py pipelines --n 90` shows no canon on that branch.

### R6: `(c)` of `test_s5_precheck.py`

- test_s5_precheck.py:5007 (blame 82c00a00, 13.11) compares `[k for k in found if k != "subjects"]` to the six plain keys.
- Since 2d84d1f1 the row-fields finding is `_sited("manifest", "", DV.refusal("s5_precheck:row_fields", message), …)`, at s5_precheck.py around :3859 (`sed -n 3830,3880` line 30). `_sited` appends `told` last (:294-301; docstring "plus `told` as its LAST key").
- CI: `got [..., 'level', 'told']`.
- The file is mapped (`keep` covers `s5_precheck.py`) but slow-listed: same process cause as R5.

### R7: D8 of `test_gate_brief_and_retro.py`

- The cut length, the trailer number and the sha256 all follow from the cut moving one line (gate_brief.py:4069 `cap = (MAX_LINES + 2 …`).
- dce58459's diff touches only gate_brief.py. Its message says "selftest keeps a case AT the cap and one beyond"; that refers to gate_brief's own `--selftest`, not this file.
- The file is mapped (covers `gate_brief.py`) but slow-listed.
- The t-1004 witness was `gate_brief.py --selftest`, and 5eefb31e merged before any canon.

### R8: K10p vs K5/real on `handoff_check:findings_tooling`

**Which view is right: K10p's.** Four pieces of evidence:

1. **The carrier's own documentation.** stage-joints.json `note`: "for every check the factory makes of a role, **what produces the thing it demands** and where the role is told it". The row demands "A finding whose cause is `tooling` is repeated in `tooling_findings`", with the door "add it to `tooling_findings`".
2. **Can qa-case-critic write a contract where this check can fire? No.**
   - The refusal fires only when `finding.cause == "tooling"` and the id is not in `tooling_findings` (handoff_check.py:1868-1878).
   - `handoffs/s4-case-critic-to-designer.yaml:88-101` declares `findings[]` with no `cause` key and has no `tooling_findings` key. `grep -rln tooling_findings handoffs/` returns only `s5-critic-to-automator.yaml`.
   - On the values road (how a role without Bash fills its form), a path the contract lacks is refused: `` `{path}` is not a field of `{contract}` `` (handoff_check.py:2687). So a case critic can neither trigger the check nor use its door: the told line names a door it cannot use (FR-2, FR-11, AR-9, AR-10).
   - The t-993 builder's evidence ("runs when `doc.data["findings"]` is a list (:1858)") shows the unit is REACHED. It does not show the check can be MET.
3. **The spec's own rule for K5 conflicts.** docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md §(e), lines 134-139: "Widening the row would tell 10 roles a false sentence … so the per-row census narrowing stays truth-keeping". The rule is to narrow the census, never to widen the row with a false sentence. t-993 did the opposite: it widened the census row (`check_findings` → [case-critic, code-critic]) and then widened the told row to satisfy K5 (handoff t-993 §"Rows added").
4. **K10p's definition is older and stated.** test_contract_slices.py `test_k10p_k2` docstring (442ae9de, 14.11): "a requirement row is told to the roles whose contract a check of that row can judge". Its predicate for this row is `"findings[].cause" in HO.spec(c)` (:1063-1064), which yields only qa-code-critic.

**The two tests do not define "roles" for the same thing.**
- K5/real (test_stage_joints.py:868) asserts `row roles ⊇ census roles of the unit`.
- K10p asserts `row roles == writers of contracts the check can judge`.

They agree whenever the census row is truthful. The defect is the census row `check_findings`, not either test.

**The ONE fix (node N4), all in one package commit:**
- census `handoff_check.py::check_findings` roles → `["qa-code-critic"]`, with a `note`;
- row `handoff_check:findings_tooling` producers roles → `["qa-code-critic"]`;
- the qa-case-critic slice regenerated (removes `references/slices/qa-case-critic/handoff-keys.md:89`);
- the `role-load.json` `process_ratchet_tokens` pin for qa-case-critic lowered back to its measured value (expected 18795, the pre-26d4b9ac value);
- the census `ratchet.blocking_per_role` qa-case-critic lowered if C3 demands it (currently 158 after 0aab0f06).

**Must 26d4b9ac be reverted?** Its slice line and its pin raise, yes: both exist only because of the false row. Do this by the edits above, not by `git revert` (the commit also carries snapshots, reviews and journal lines).

**The sibling row wave A changed the same way (`validate_artifacts:check_cell_counts` + qa-test-strategist).** Adding the strategist is TRUE (validate_artifacts.py:1853 `check_plan_v0` calls `check_cell_counts`; artifact-writers.json:63 `test-plan.md` → qa-test-strategist), so it must not be reverted. But the change is incomplete in two ways:
- (a) **The strategist is told nowhere.** The row's `stages` stays `["S2","S4"]`. The slice generator keeps only the rows for the role's stages (contract_slices.py:673-676 → `stage_joints.rows_for(role, ids, …)`), and the strategist is S3 (stages.json:94-100). Measured: `grep -l check_cell_counts references/slices/*/*.md` finds only `qa-case-designer` and `qa-requirements-tester`; none of the strategist's five slice files has it. So AR-10 is not achieved for the strategist even though the row names it.
- (b) **The row still names qa-case-designer**, which reaches no call of `check_cell_counts`. The only callers are validate_artifacts.py:588 (`check_register`, tester) and :1853 (`check_plan_v0`, strategist). So the designer is told a false sentence (the t-993 builder reported this as a sibling and left it). This is **fork F3**.

**Outside the keys, for the Lead.** 0aab0f06 also set the census `validate_artifacts.py::check_requirements_review` → `["qa-requirements-tester"]`, although the t-993 builder had left that unit unchanged with an open question ("is the tester the writer, or should the artifact get an owner in artifact-writers.json first?"). The note says "finding queued". The Lead should confirm the question was decided by somebody entitled to decide it, rather than settled at integration.

### R9: `t4a plugin read`

I computed the digest of `PLUGIN_READ_MSG.format(tool="Read", path=p)` (the message is unchanged since 9ac00f09: `git log -S"PLUGIN_READ_MSG"` returns only the initial import), rstripped and sha256'd as `t4a_digest` does:
- `p = "<PLUGIN>\scripts\hooklib.py"` gives **c8455f9f8ed26987**, which is the pin.
- `p = "<PLUGIN>/scripts/hooklib.py"` gives **577c1db84a62bfdb**, which is exactly CI's value.

The normaliser in `t4a_provoke_in` (test :1661-1663) replaces only the root prefix, so the separators after it keep the OS form. Local in-process run of `tbw_t4a_sites()`: `PASS t4a plugin read … the problem text is the old one` on Windows. CI (Linux): FAIL.

The other 46 T4A rows pass on both OSes: their texts carry no path after the normalised root.

## K3: exact fixes

**N3-a, R5** (`scripts/tests/test_guard_dispatch_budget_and_logs.py:895-899`). Old:
- `direct = ("PRE-TOOL GUARD: these handover values leave the form not ready; nothing was written.\n" + H.refusal_text(form, report.contract, report.problems, report.role, kept=report.kept))`
- `check_eq("K3: the block is the one function's text, byte for byte (and the guard's own closing line)", text, (direct + "\n" + hooklib.TRAPPED).strip())`

New:
- `import detector_verdict as DV`
- `direct = DV.spoken(DV.refusal("guard_pre_tool:PT-handoff-values", "PRE-TOOL GUARD: these handover values leave the form not ready; nothing was written.\n" + H.refusal_text(form, report.contract, report.problems, report.role, kept=report.kept)))`
- `check_in("K3: the row's id closes the block before TRAPPED (T4a, t-965)", "\n  check: guard_pre_tool:PT-handoff-values", text)`. This is an independent requirement line, so the expectation is not only the product's own output (P20).
- `check_eq("K3: the block is the one function's text with the row's lines, byte for byte (and the guard's own closing line)", text, (direct.rstrip() + "\n" + hooklib.TRAPPED).strip())`

Pin follows.

**N3-b, R6** (`scripts/tests/test_s5_precheck.py:5007`). Old: `[k for k in found if k != "subjects"]`. New:
- `check_eq("(c) the finding's other keys are the six it always had", [k for k in found if k not in ("subjects", "told")], list(plain))`
- `check_eq("(c) ... and `told` stands last, naming its row (T5r, 2d84d1f1)", (list(found)[-1], [t.get("check") for t in found["told"]]), ("told", ["s5_precheck:row_fields"]))`

Pin follows.

**N3-c, R7** (`scripts/tests/test_gate_brief_and_retro.py`):
- :2126: `84` → `85`, and append to the comment `; dce58459 (t-1004): MAX_LINES 40 -> 41 by name, the cut grows by one`.
- :2128: `"_(brief truncated at 84 lines; …)_"` → `"_(brief truncated at 85 lines; …)_"`.
- :2130: `"45da4c8b3fe58fd9dcb28dce38e33ad293a1f1a5b67f8fbacecdd35028088042"` → `"072de46f5465ec6d88f0ffe125eda25632ecbea7c4723a0d6962a1ad4330224a"`, with `(was 45da4c8b..., dce58459)` prepended to the trailing comment.

The new sha is code output, so the builder confirms it once in-process. The cut at dce58459 vs at dce58459^ should differ by exactly one body line plus the trailer number (a `difflib` of the two renders), and that diff goes in the report as the witness.

Pin follows.

**N3-d, R9** (`scripts/tests/test_detector_verdict.py`):
- :1683: `ev("Read", str(hooklib.PLUGIN_ROOT / "scripts" / "hooklib.py"), role="qa-scout")` → `ev("Read", (hooklib.PLUGIN_ROOT / "scripts" / "hooklib.py").as_posix(), role="qa-scout")`.
- :1758: `'plugin read': 'c8455f9f8ed26987',` → `'plugin read': '577c1db84a62bfdb',   # the POSIX spelling on every OS (was c8455f9f..., the Windows spelling); PLUGIN_READ_MSG unchanged since 9ac00f09`.

The witness is `tbw_t4a_sites()` in-process on Windows: green. That proves `plugin_read_check` still refuses a forward-slash `C:/…` path, through `_native_path` → `RP.contained`; on Linux the value is already proven by CI.

Test fix.

**N4, R8** (package data). Edits:
- `references/stage-joints.json`: row `handoff_check:findings_tooling` `producers[0].roles` `["qa-case-critic","qa-code-critic"]` → `["qa-code-critic"]`.
- `scripts/tests/fixtures/judgment-census.json`: row `handoff_check.py::check_findings` `roles` → `["qa-code-critic"]`, plus `"note": "the refusal needs findings[].cause; only s5-critic-to-automator declares it (and tooling_findings); s4-case-critic-to-designer declares neither and the values road refuses both paths as not a field (handoff_check.py:2687)"`. Then lower `ratchet.blocking_per_role` for qa-case-critic only if `test_judgment_census.py` C3 says so.
- Run `python -B scripts/contract_slices.py --write` (removes the case-critic line).
- `references/role-load.json`: `"qa-case-critic": 18830` → the measured value printed by `scripts/tests/test_audit_rules.py` (expected 18795).

Product (data) fix. Plus **fork F3** for the `check_cell_counts` row.

**N1, R1/R2** (fork F1, recommended option a). In `tools/hygiene_gate.py` `run_allowed`, before `_decide_command`:
- `if isinstance(cwd, os.PathLike): cwd = os.fspath(cwd)`
- `if not isinstance(cwd, str) or not cwd: return False, ["the working directory is not a path, so the gate cannot measure a rollback there; refused"]`

In `tools/test_hygiene_gate.py`, add `monkeypatch.chdir(world["clean"])` as the first line of `test_run_allowed_battery` and of `test_run_allowed_keeps_the_refusal_classes_of_the_live_gate` (add the `monkeypatch` parameter). The process cwd is then a CLEAN tree on every machine, so a swap back to `os.getcwd()` would turn the rows red locally as well.

Product fix + test isolation.

**N2, R3/R4** (fork F2, recommended option a). In `tools/mechanism_gate.py` `MECHANISM_PREFIXES`, after the `tools/transcripts.py` line (:276), add:
- `"tools/usage_report.py",        # imported (lazily, --node-cost only) by tools/forge_metrics.py (t-905); the closure counts it`

Optionally correct the `_ast_tool_imports` docstring in test_mechanism_gate.py:964 ("top-level" → "every `import` in the module, nested ones included").

Product fix (the net).

## K4: clusters

Four independent nodes; their owns do not overlap.

- **N1, tools hygiene** (R1, R2). owns: `tools/hygiene_gate.py`, `tools/test_hygiene_gate.py`.
  - A **Lead mechanism commit**: `tools/hygiene_gate.py` is in the net (mechanism_gate.py:239).
  - Builder content goes on a neighbouring filename (enforcement-file review rule: it is a live hook) or as a diff; the Lead places it.
  - Witness: `python -m pytest tools/test_hygiene_gate.py -q -k run_allowed`.
- **N2, the mechanism net** (R3, R4). owns: `tools/mechanism_gate.py` (+ the docstring in `tools/test_mechanism_gate.py`). A **Lead mechanism commit**: axis block + `tier: opus`.
  - Witness: `python -m pytest tools/test_mechanism_gate.py -q -k "closure"`.
  - N1 and N2 can be one Lead commit.
- **N3, package pins** (R5, R6, R7, R9). owns: `scripts/tests/test_guard_dispatch_budget_and_logs.py`, `scripts/tests/test_s5_precheck.py`, `scripts/tests/test_gate_brief_and_retro.py`, `scripts/tests/test_detector_verdict.py`. Tests only, one builder, no mechanism commit.
  - Package commit lines: `architecture: none -- test pins follow named changes (T4a t-965, T5r, dce58459) and one OS-free provocation`; `judgment: none`.
  - Witness: the four functions in-process: `test_the_guard_parses_once_…`, the FV1-30b-style function holding line 5007, the D8 golden function, and `tbw_t4a_sites`. Three of the four files are slow-listed, so the builder does not run the whole files; the canon judges them.
- **N4, told rows and census** (R8 + fork F3). owns: `references/stage-joints.json`, `scripts/tests/fixtures/judgment-census.json`, `references/slices/qa-case-critic/**`, `references/slices/qa-case-designer/**` and `references/slices/qa-test-strategist/**` (F3), `references/role-load.json`. Package data, one builder.
  - Lines: `architecture: AR-10 -- a told row reaches only roles that can meet it; AR-22 -- census and rows paired; AR-20 -- pins lowered (and any strategist raise named)`.
  - Witness: `scripts/tests/test_contract_slices.py` (fast), `scripts/tests/test_stage_joints.py` K5 (243 s on CI: slow, so canon), `scripts/tests/test_judgment_census.py`, `scripts/tests/test_audit_rules.py`.
  - Not a mechanism path.

## Forks for the Lead

- **F1 (R1/R2).**
  - (a) Product: `run_allowed` coerces PathLike and refuses a non-path cwd; the test pins its process cwd. Consequence: a Lead mechanism commit (hygiene_gate.py is a live hook); the doubt-refusing road can no longer measure the wrong tree; the test becomes machine-independent.
  - (b) Test only: pass `str(world[cwd_key])` and `str(world["repo"])`. Consequence: no mechanism commit, but the latent wrong-tree measurement stays in the product, and the test stays green by accident for any future Path caller.
  - **Recommend (a).**
- **F2 (R3/R4).**
  - (a) Add `tools/usage_report.py` to `MECHANISM_PREFIXES`. Consequence: a 1-line Lead mechanism commit. usage_report.py (the money-accounting reader, P18) becomes a mechanism path, so each edit needs an axis block and `tier: opus`. The friction is low: one edit since 9ac00f09. It follows the list's own rule ("TAKEN FROM the closure").
  - (b) Move `node_costs` and the `--node-cost` mode out of forge_metrics.py into a module outside the hook closure, as hop_metrics is (test_mechanism_gate.py:1678 pins hop_metrics as outside). Consequence: a ~300-line move in a mechanism file (still a Lead commit), a CLI change for `--node-cost`, and the spec/doc pointers to it must follow; any import back from forge_metrics re-creates the edge.
  - (c) Make the closure ignore function-level imports. That weakens the detector, so **rejected**.
  - **Recommend (a).**
- **F3 (the `check_cell_counts` sibling).**
  - (a) roles `[qa-requirements-tester, qa-test-strategist]`, stages `["S2","S3"]`. Consequence: the designer's slice loses a false line (its pin may go down); the strategist's slice gains the line (≈ +30 process tokens against pin 17581; a raise, if needed, is named per axis 18 by the Lead).
  - (b) Only drop the designer. Truthful, no growth, but the strategist stays untold.
  - (c) Leave it. Green tests, but a false telling to the designer and an untold strategist.
  - **Recommend (a).** Spec §(e) truth-keeping; AR-10.

## K5: class completeness and process cause

**Sibling map (targeted lookup):**
- R8, F3: axis 32 (census ↔ gates ↔ charters). The census change must travel with its rows and slices, and t-993 widened rows instead of narrowing the census. Also axis 18: the 26d4b9ac raise was named (good), but it was a raise caused by a false row, so it must come back down with N4.
- R7: axis 18. The raise is named at the constant; the D8 golden in the same package is a direct consumer of the cap, and dce58459 did not touch it.
- R5, R9: axis 17. `test_detector_verdict.py` is the axis's detector; the T4a rows are its consumers.
  - The other pinned refusal texts of guard_pre_tool (the T4A_OLD table) pass on CI.
  - Both shards ran fully (213/215, 177/180, no timeouts), so the canon itself is the completeness proof: no other byte pin of a T4a/T5r-wrapped text is red.
- R1/R2: axis 11 (shell-command recognizers). `run_allowed` and `decide` share `_decide_command`. The parity test exists, but its two halves feed different cwd types. No other `run_allowed(…, Path)` call: the only non-test caller is journal_write.py:626, which passes a `str`.
- R3/R4: no map axis. The rule lives in mechanism_gate.py:282 ("the list is TAKEN FROM the closure test").

**The process cause shared with round 1: the witness skipped the judging file.** For each row:
- **R5, R6, R7.** The map rows EXIST: `--witness-for` names the files through keep `covers` (scenario_walk.py:913-916 matches `guard_pre_tool.py`, `s5_precheck.py`, `gate_brief.py`). But all three are in `scripts/slow_tests.json`, so builders legitimately left them to "the canon of the batch" (t-985 handoff line 75 says so).
  - The canon of `wave-a/integrate` was never run before merge 71d36190, and t-1004 merged in 5eefb31e before any canon. The first canon after both is 44013914849.
  - So the cause is **merge before the batch canon**, not a missing row.
- **R8.** **Missing rows.** `--witness-for references/stage-joints.json` prints only `test_selftest_slow_tests.py`.
  - The keep rows of `test_contract_slices.py`, `test_stage_joints.py` and `test_detector_verdict.py` do not list `references/stage-joints.json`.
  - No keep row lists `scripts/tests/fixtures/judgment-census.json`; test_stage_joints covers `tests/test_judgment_census.py`, not the fixture.
  - Add `references/stage-joints.json` to the `covers` of those three, and `scripts/tests/fixtures/judgment-census.json` to the `covers` of `test_judgment_census.py` and `test_stage_joints.py`. This is a `test-layers.json` edit and can ride N4.
- **R9.** **Missing row plus an OS gap.** The keep row of `test_detector_verdict.py` does not cover `guard_pre_tool.py` or `host_adapter.py`, although `tbw_t4a_sites` provokes both. Even if it did, a Windows-only witness was green (t-985: 745/745). The class is byte pins over path-bearing text pinned on one OS.
- **R1–R4.** No `--witness-for` exists for `tools/` (CLAUDE.md rule 4: the DoD names the judging test).
  - t-905's DoD named only `test_forge_metrics.py` (handoff line 7). The cross-cutting judge `test_mechanism_gate.py` (closure) applies to ANY import change in a module of the net, and nothing makes a DoD name it.
  - R1/R2's judge ran, but its verdict depended on the developer's dirty tree.
  - All four were visible on forge-check at 00:28Z, merged on, then masked by lint_ratchet; round 1 excluded forge-check.
  - The proposed node, owner the Lead: a DoD line rule for `tools/`: "an import change in a `MECHANISM_PREFIXES` module → `pytest tools/test_mechanism_gate.py -k closure`".

## K6: anything else in run 44013914849

- **package-fast (job 133807395675)** is red on exactly R8 and R9: `FAIL K10p/narrowed-by-contract/handoff_check:findings_tooling …` and `FAIL t4a plugin read …`, `=== qa-factory selftest (fast): 219/221 ok ===`. `--contracts` is 3/3 and test_audit_rules is 375/375. Nothing else.
- **Shard artifacts.**
  - Shard 1: only two FAIL lines (R5, R6), `213/215 ok`, ending normally. test_stage_joints PASSES (243.6 s, no timeout any more), so K5/real, including `check_requirements_review`, is green.
  - Shard 2: only three FAIL files (R7, R8, R9), `177/180 ok`. test_judgment_census PASSES.
  - install-smoke: success.
- **Not verified, hidden by R1–R4.** In forge-check, the steps after `python -m pytest tools/ -q` never ran in this run:
  - `python -B experiments/measurers/test_measurers.py`;
  - `scoreboard.py norms --check --against <base>` (forge-check.yml:97-108).

  I could not find a run since 14.11 where they executed (every forge-check since 43987289826 stopped at pytest or lint). Their state is **unknown**: name them as the next possible red after N1 and N2 land.

## Verdict

**NEEDS WORK.** main is red on 9 rows, grouped into 4 nodes. The verdict is an input; accepting the nodes and opening them is the Lead's decision.

- **Blocking: all nine rows.**
- **Product or data defects:**
  - R8: false told row + census, and the 26d4b9ac pin and slice that followed from it;
  - R1/R2: `run_allowed` measures the wrong tree for a non-`str` cwd, and the test is masked by the developer's dirty tree;
  - R3/R4: the net is missing `usage_report.py`.
- **Pin follows:** R5, R6, R7.
- **Test defect (OS-dependent pin):** R9.

**Standing questions for this diagnosis:**
- **Duplication and consistency.** Two tests define the same row's roles from two sources. They agree only while the census is true, which is what N4 restores.
- **Code quality.** The `_ast_tool_imports` docstring contradicts its code. Silent cwd substitution in a refuse-on-doubt road.
- **One road.** None: no exclusion of a language, project or case.
- **Tests.** N3 is pins only; N4 is data. No volume growth expected.

## Trail

**Read:**
- tools/test_hygiene_gate.py:1-90 and :545-637;
- tools/hygiene_gate.py:1490-1602;
- tools/journal_write.py:626 (grep);
- tools/mechanism_gate.py:215-292;
- tools/test_mechanism_gate.py:963-987, :1030-1041, :1650-1683;
- tools/forge_metrics.py:1008-1010, :1215-1235, :1712-1725;
- tools/usage_report.py imports;
- .githooks/pre-commit:66 and pre-merge-commit:17;
- .github/workflows/forge-check.yml:96-108;
- scripts/guard_pre_tool.py:505-575 and :1178-1190;
- scripts/hooklib.py:984-1000;
- scripts/detector_verdict.py:149-191 and :213-223;
- scripts/s5_precheck.py:290-310 and :3817-3860;
- scripts/handoff_check.py:1850-1885 and :2670-2690;
- scripts/contract_slices.py:620-690;
- scripts/gate_brief.py:65 and :4069;
- scripts/tests/test_guard_dispatch_budget_and_logs.py:1-60 and :848-900;
- scripts/tests/test_s5_precheck.py:4668-4675 and :4977-5007;
- scripts/tests/test_gate_brief_and_retro.py:2118-2135;
- scripts/tests/test_contract_slices.py:1042-1076;
- scripts/tests/test_stage_joints.py:820-875;
- scripts/tests/test_detector_verdict.py:1606-1690 and :1741-1811;
- scripts/tests/scenario_walk.py:900-921;
- scripts/tests/test-layers.json keep rows (6 files);
- scripts/slow_tests.json (grep);
- references/stage-joints.json (header + 2 rows);
- references/stages.json:92-100;
- references/artifact-writers.json:60-70;
- handoffs/s4-case-critic-to-designer.yaml:85-105 and s5-critic-to-automator.yaml (grep);
- references/slices/*/handoff-keys*.md (grep);
- scripts/tests/fixtures/judgment-census.json (about + rows);
- docs/tasks/handoffs/t-993-k5-real.md, t-985 (lines 7, 26, 75-90), t-981, t-905 (line 7), t-850-B0-r3 (line 20);
- docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md:38, :130-139, :344-350;
- docs/tasks/specs/reviews/t-986-main-red-canon-diagnosis.md (lines 8, 29, 47, 53);
- docs/tasks/compact-snapshots/2026-11-17-0530-narrative.md:36-42;
- docs/SIBLING_MAP.md axes 17, 18, 32 (+ heading list).

**Git:**
- `log -25 origin/main`;
- `show --stat` of e47e086c, c5b7bb6c, 0aab0f06, dce58459, 26d4b9ac;
- blame on every pin line named above;
- `log -S` for run_allowed, PLUGIN_READ_MSG, told, narrowed-by-contract;
- ancestry checks of 92781363, ccb4a82f, 2d84d1f1, 86ce4caf.

**CI:**
- `ci_read.py pipelines --n 90`;
- jobs of 44013914849, 44010947813, 44014057685 and 6 older runs;
- forge-check logs 133807200585, 133807745056, 133797541305, 133718632040, 133733232842 and 7 lint-stopped jobs;
- both shard artifacts (FAIL / tail / line-kind counts);
- package-fast log 133807395675.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "R8: handoff_check:findings_tooling told to qa-case-critic, whose contract declares neither findings[].cause nor tooling_findings (s4-case-critic-to-designer.yaml:88-101; handoff_check.py:2687 refuses both paths); census check_findings over-wide since c5b7bb6c; 26d4b9ac slice line and pin 18795->18830 follow from it",
    "R1/R2: run_allowed forwards a Path cwd, _decide_command (hygiene_gate.py:1503) swaps it for os.getcwd(); green locally only because the root checkout is dirty, red on clean CI; born ccb4a82f",
    "R3/R4: forge_metrics.py:1229/:1721 import usage_report (92781363, e9204bde); usage_report.py not in MECHANISM_PREFIXES",
    "R5/R6/R7: pins stale after intended changes T4a 86ce4caf, T5r 2d84d1f1, named cap raise dce58459",
    "R9: T4A_OLD plugin read pinned on Windows over a backslash path; CI Linux digest 577c1db84a62bfdb is the same text with forward slashes"
  ],
  "fixes": [
    "N1 (Lead mechanism commit, fork F1 a): run_allowed coerces os.PathLike via os.fspath and refuses a non-path cwd; test_hygiene_gate run_allowed tests monkeypatch.chdir(world clean)",
    "N2 (Lead mechanism commit, fork F2 a): add tools/usage_report.py to MECHANISM_PREFIXES; fix the _ast_tool_imports docstring",
    "N3 (builder, tests only): R5 expected text built through DV.spoken(DV.refusal(guard_pre_tool:PT-handoff-values, ...)) plus a check_in on the check line; R6 exclude told and assert told last naming s5_precheck:row_fields; R7 84->85, trailer 85, sha 072de46f...; R9 provoke with as_posix() and pin 577c1db84a62bfdb",
    "N4 (builder, package data): census check_findings and row findings_tooling roles -> [qa-code-critic]; contract_slices.py --write; role-load qa-case-critic pin back to measured (expected 18795); fork F3 a for check_cell_counts (roles tester+strategist, stages S2,S3); add covers rows for references/stage-joints.json and the census fixture in test-layers.json"
  ],
  "class_completeness": "Axis 32: t-993 widened rows instead of narrowing the census (spec 20261114 t1r-pages section e says narrow); sibling check_cell_counts row is incomplete (strategist untold because stages lack S3; designer told falsely) - fork F3. Axis 18: dce58459 raise left its D8 golden consumer stale; 26d4b9ac raise must come back down. Axis 17: canon complete (both shards ran fully) so no other T4a/T5r byte pin is red. Axis 11: run_allowed is the only Path-fed caller. Process: R5-R7 mapped but slow-listed and merged before the batch canon; R8 and R9 have missing covers rows in test-layers.json; R3/R4 had no DoD line naming test_mechanism_gate closure; forge-check steps after pytest (test_measurers, scoreboard norms) unverified.",
  "trail": {
    "read": [
      "tools/test_hygiene_gate.py",
      "tools/hygiene_gate.py",
      "tools/mechanism_gate.py",
      "tools/test_mechanism_gate.py",
      "tools/forge_metrics.py",
      "tools/usage_report.py",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py",
      "ai-packages/qa-factory/scripts/hooklib.py",
      "ai-packages/qa-factory/scripts/detector_verdict.py",
      "ai-packages/qa-factory/scripts/s5_precheck.py",
      "ai-packages/qa-factory/scripts/handoff_check.py",
      "ai-packages/qa-factory/scripts/contract_slices.py",
      "ai-packages/qa-factory/scripts/gate_brief.py",
      "ai-packages/qa-factory/scripts/tests/test_guard_dispatch_budget_and_logs.py",
      "ai-packages/qa-factory/scripts/tests/test_s5_precheck.py",
      "ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py",
      "ai-packages/qa-factory/scripts/tests/test_contract_slices.py",
      "ai-packages/qa-factory/scripts/tests/test_stage_joints.py",
      "ai-packages/qa-factory/scripts/tests/test_detector_verdict.py",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/slow_tests.json",
      "ai-packages/qa-factory/references/stage-joints.json",
      "ai-packages/qa-factory/references/stages.json",
      "ai-packages/qa-factory/references/artifact-writers.json",
      "ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "docs/tasks/handoffs/t-993-k5-real.md",
      "docs/tasks/handoffs/t-985-wave-a-fix-round.md",
      "docs/tasks/handoffs/t-905-fg7-5-node-cost.md",
      "docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md",
      "docs/tasks/specs/reviews/t-986-main-red-canon-diagnosis.md",
      "docs/SIBLING_MAP.md"
    ],
    "reruns": [
      {"command": "python -B -m pytest tools/test_hygiene_gate.py -q -k run_allowed (root checkout, dirty tree)", "result": "29 passed, 251 deselected - green locally, red on clean CI: the Path cwd falls back to os.getcwd()"},
      {"command": "in-process test_the_guard_parses_once_reads_the_form_once_and_prints_the_one_functions_text (test_guard_dispatch_budget_and_logs.py)", "result": "FAIL K3; GOT carries expected/door/check: guard_pre_tool:PT-handoff-values lines that EXP lacks"},
      {"command": "in-process tbw_t4a_sites (test_detector_verdict.py) on Windows", "result": "PASS t4a plugin read ... the problem text is the old one (CI Linux: FAIL)"},
      {"command": "sha256 of PLUGIN_READ_MSG.format(Read, <PLUGIN>\\scripts\\hooklib.py) vs <PLUGIN>/scripts/hooklib.py, first 16 hex", "result": "c8455f9f8ed26987 (pin) vs 577c1db84a62bfdb (CI got)"},
      {"command": "ci_read.py log 133718632040 / 133733232842 (forge-check 00:28Z, 01:01Z)", "result": "same 4 failed (R1-R4), 9502 passed - visible before lint_ratchet masked them"},
      {"command": "ci_read.py log 133807395675 (package-fast)", "result": "only K10p findings_tooling and t4a plugin read FAIL; 219/221"},
      {"command": "ci_read.py artifact 44013914849 shards 1 and 2", "result": "213/215 and 177/180; FAIL lines only R5,R6 and R7,R8,R9; no timeouts"},
      {"command": "grep -l check_cell_counts references/slices/*/*.md", "result": "qa-case-designer and qa-requirements-tester only - strategist untold"}
    ]
  }
}
```
