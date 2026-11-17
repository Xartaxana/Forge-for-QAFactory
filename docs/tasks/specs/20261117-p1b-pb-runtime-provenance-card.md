# P-b card (DRAFT, designer t-1072): the code critic's `probes.runtime_provenance` gets a producer on the critic's road

Status: DRAFT for Lead acceptance, then a plan critic (PROJECT.md "Как принимается изменение пакета" item 6: the change alters the
meaning of a deriver's source). It is not a dispatch until accepted. Forks F1-F5 are below. The numbered items are written for
the RECOMMENDED options (F1-B, F2-b, F3-b, F4-a, F5-a), so a builder can execute the card as written until the Lead decides
otherwise (PROJECT.md "Командная работа" item 11).

Source: critic diagnosis `docs/tasks/specs/reviews/t-1070-p1b-main-s5-residue-diagnosis.md` (K3, K4 "Node P-b", standing lines,
trail). Sibling card P-a (t-1071, `_review_receipt`) touches the same file.

---

## 0. Facts read this round (file:line). Every load-bearing claim of the card rests on one of these

| # | Fact | Carrier (read this round) |
|---|---|---|
| A1 | `window_runtime_record(task_root, dispatch)` reads only `work/run-blocks/` through `run_history.read_run_blocks`. Any unreadable block gives a named unknown (`:541-543`). It keeps blocks whose `dispatch_id` (stripped) equals the dispatch and whose `runtime_provenance` is a non-empty dict (`:544-550`). None of them: `(None, "no run block of dispatch ... carries a runtime_provenance record ...")` (`:551-554`). Otherwise it takes the newest such block, `evidence_refs[0]` (`:555-562`), and resolves it inside the story by the tail rule (`:563-580`). | `ai-packages/qa-factory/scripts/handoff_check.py:522-580` |
| A2 | `_RECORD_PRODUCER = "the record is written by runtime_probe.py when run_suite runs this dispatch's tests"` ends every no-path reason (`:535,540,543,554,562,579`). | `handoff_check.py:522` |
| A3 | `_runtime_provenance(art, doc)` takes the dispatch from `_form_dispatch(art, doc)` and returns `(path, why)` or `(None, "", why)`. | `handoff_check.py:583-586` |
| A4 | The three callers: `DERIVERS["artifacts.runtime_provenance"]` (s5-automator-to-critic), `["probes.runtime_provenance"]` (s5-critic-to-automator), `["runtime.provenance"]` (s5-automator-to-runner). All three map to `_runtime_provenance`. Today the automator and runner forms get their run block's record. The critic gets `(None, "", "no run block of dispatch S5-qa-code-critic-1 ...")` (diagnosis `:42`). | `handoff_check.py:644-651`; diagnosis `:42` |
| A5 | `--fix` fills a blank field from `DERIVERS.get(generic) or _by_path(...)`. A third element extends the blank refusal as ` Code could not fill it: <why>`. | `handoff_check.py:1650-1677` |
| A6 | `build_run_block` returns None for `purpose == "red_probe"`, so a probe writes no run block. The block's `runtime_provenance` is a copy of the REQUEST's `runtime_provenance`. | `ai-packages/qa-factory/scripts/run_suite.py:470-473`, `:582` |
| A7 | `probe_by_code` builds its request with `execution_request.build_mine_request(..., purpose="red_probe", dispatch_id="" if s6_close else dispatch, probe=probe_runtime)` (`:2939-2942`). It sets `idempotency_key = "{dispatch}:red_probe:probe-{iid}:{mutation}:{fp12}"` plus `:again-N` (`:2956-2961`). The request is written to `work/probe-requests/probe-<IID>.json` (invert road, `:4674-4676`) or to `work/probe-requests/probe-walk-<IID>-<n>.json` (the walk, `:6168-6169`). Both names are REUSED: a later probe of the same instance overwrites the file. | `ai-packages/qa-factory/scripts/probe_by_code.py:2917-2965,4674-4677,6168-6169` |
| A8 | A red probe's `runtime_provenance` is COPIED from the precedent request (the newest job of the profile, `:3398-3399`) with only `timestamp=now` replaced. It is not re-observed: "A red probe runs in a sandbox by definition and keeps copying (its own gate is the launch check)" (`:2843-2850`). | `ai-packages/qa-factory/scripts/execution_request.py:2837-2876,3395-3399` |
| A9 | At launch, `run_suite --request` re-probes the stand when `runtime_required`. It refuses a moved `profile_id` / `observed_runtime_identity` / `expected_source_revision` BEFORE any job exists (`:2904-2922`). It then sets `request["runtime_probe_before"] = observed` (`:2923`). The job is begun later, `store.begin(request)` (`:2989`). So `runtime_probe_before` is persisted in the job and is the observation taken at THIS run's launch. | `run_suite.py:2878-2923,2966-2995` |
| A10 | `JobStore`: one file per idempotency key under `<task_root>/state/execution-jobs/<sha256(key)>.json`. A job holds `{job_id, idempotency_key, request_digest, status: "persisted", created_at, request}` (`:450-453`). `update` adds `updated_at` (`:474-477`). A finished run writes `status="completed", execution_status, summary, run_block` (`run_suite.py:2412-2416`). `jobs()` returns every readable job oldest first, sorted by `(updated_at or created_at, file mtime_ns)`. It SKIPS unreadable files silently ("a lookup ..., never the idempotency decision itself", `:500-518`). | `execution_request.py:404-518`; `run_suite.py:2412-2416` |
| A11 | `red_sandbox.py --probe` runs `run_suite.py --mine ... --purpose red_probe --dispatch <dispatch>` (`:1257-1262`). That request goes to `work/requests/mine-*.json` (`execution_request.write_mine_request`, `:3924-3934`), NOT to `work/probe-requests/`. `red_sandbox` already reads the job store as "the request the runner was launched with" (`:1001-1007`). | `ai-packages/qa-factory/scripts/red_sandbox.py:998-1009,1250-1264`; `execution_request.py:3924-3934` |
| A12 | `runtime_probe.write_record` is the one writer of `evidence/runtime-provenance-<profile>-<stamp>[_NN].json`. It sets `record["evidence_refs"] = [<absolute posix path>]`, which is why the tail resolver of A1 exists. | `ai-packages/qa-factory/scripts/runtime_probe.py:1562-1596` |
| A13 | MEASURED, kept world `C:\Users\i_mas\AppData\Local\Temp\qa-story-run-s0-tqwkmqn_\qa-factory\artifacts\DRY-1` (read with Read/Grep this round). See the list below the table. | the two job files under `state/execution-jobs/`; `work/probe-requests/probe-walk-test_the_case-1.json:4,6,55,60`; Glob of `evidence/runtime-provenance-*.json` |
| A14 | The contract says: "# The stand the probes ran on: the record of this review's own probe run." / `runtime_provenance: <path of the runtime_provenance record this review probed against>`. | `ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml:53-55` |
| A15 | The critic's charter does not mention `runtime_provenance`: case-insensitive grep `window_record|provenance` over `agents/` gives one hit, `agents/qa-code-critic.md:69` (`window_record`), the positive control. `brief_pack.py` and `tests/dry_stub.py` never mention `runtime_provenance`: 0 hits each, with positive controls `probe_by_code` (7 hits in brief_pack.py) and `window_record` (37 in dry_stub.py). | greps this round |
| A16 | The census makes a unit from a function name matching `UNIT_NAME_RE = ^(check_|rule_|judge|judged_|_?validate|_?refuse)|^_?(check|run)$|(_check|_errors|_problems)$`, from a judge call, or from a refusal site (`:218-259`). `window_runtime_record` and `_runtime_provenance` have no census row; their P1B-9 C3 commit had `judgment: none` (report `docs/tasks/specs/reports/20261114-p1b9-c3-report.md:92-94`). | `ai-packages/qa-factory/scripts/tests/test_judgment_census.py:77,218-259`; `scripts/tests/fixtures/judgment-census.json:471-481` (handoff_check rows: none for derivers) |
| A17 | `test_handoff.py` is a KEEP row: layer `data_join`, covers `handoff_check.py`. Today's C3 table is `the_runtime_record_is_the_windows_own` (`:266-402`), and its no-path rows assert `"runtime_probe.py" in got[2]` (`:396-400`). The blank-field function is `:405-430`. `main()` calls both (`:2653-2654`). | `scripts/tests/test-layers.json:2299-2322`; `test_handoff.py:257-430,2615-2674` |
| A18 | `test_field_producers.py` checks that all three provenance paths are in `DERIVERS` (`:161-162`) and that `DERIVERS["runtime.provenance"] is DERIVERS["artifacts.runtime_provenance"]` (`:165-167`). It does NOT pin `probes.runtime_provenance` to the same function. Keep row, `data_join` (`test-layers.json:1687-1689`). | `scripts/tests/test_field_producers.py:158-167` |
| A19 | `known_red.json` holds one row, `main/S5` (`node: FV3-20`, a "stub gap" label with 3 findings), and pin `known_red: 1` (equality both ways, `_about`). | `scripts/tests/fixtures/driver-exits/known_red.json:1-12` |
| A20 | Cart-1's 8 recorded jobs (2026-10-31) are all `status: completed` and each carries `request.runtime_probe_before`. None is `purpose: red_probe`: no match for `"purpose": "red_probe"` with the same spacing that matched `"status": "`. | Grep over `scripts/tests/fixtures/stories/cart-1/state/execution-jobs/` |

A13, as measured in the kept world:

- Job `44bcd10c384267c69a56`: `status: completed`, `request.dispatch_id: S5-qa-code-critic-1`, `purpose: red_probe`, `runtime_required: true`, `built_by.tool: probe_by_code.py`, `updated_at: 2026-11-17T07:53:03+00:00`, `run_block: null`.
- Its `request.runtime_provenance.evidence_refs[0]` = `.../DRY-1/evidence/runtime-provenance-dry-pytest-20261117T075205Z.json`, with `timestamp 07:52:56`. That file was written in the AUTOMATOR's window: it is the same file that job `66bd1d15b5fe5da442d7` (`S5-qa-automator-1`, `purpose: initial`) and its run block name.
- Its `request.runtime_probe_before.evidence_refs[0]` = `.../evidence/runtime-provenance-dry-pytest-20261117T075258Z.json` (`timestamp 07:52:58`): the record written at THIS probe's launch.
- Both files exist.
- The probe request file has `dispatch_id: S5-qa-code-critic-1` (`:4`), `purpose: red_probe` (`:6`), `runtime_provenance.timestamp` (`:55`) and evidence `...075205Z.json` (`:60`). It has NO `runtime_probe_before`: the same Grep pattern matched `:141` of the job file.

What A13 means: the probe REQUEST file carries the automator's record, not one this probe took. Only the job carries the record of the probe's own launch. This decides F1 and F3.

---

## 1. Package spec §1 (designer rule 1; CLAUDE.md rule 10 "a change to the package"; P27, AR-29)

### 1.1 AR-n touched and how each is kept (the change check goes into the DoD as C-n)

| AR | How the card keeps it | Change check (DoD) |
|---|---|---|
| AR-13 one reader per fact | `window_runtime_record` stays THE reader of "the record of a dispatch's run". The probe branch lives inside it, behind `probe_run=True`. The job list is read only through `execution_request.JobStore(...).jobs()`. The story tail rule (`:563-576`) is EXTRACTED into one helper `_story_record(root, ref)`, called by both branches, so there is no second copy. | C1: `grep -n "_story_record(" ai-packages/qa-factory/scripts/handoff_check.py` shows 1 `def` and exactly 2 call sites. The text `parts[::-1].index(root.name)` occurs once in the file. |
| AR-22 every field read has a producer | `s5-critic-to-automator:probes.runtime_provenance` gets the producer that the critic's road reaches: run_suite's completed `red_probe` job of the dispatch (A9, A10, A13). | C2: test row P1 ("dry-world shape") is red before the change and green after it. |
| AR-25 every recorded state has a way out | The critic's blank field gets a code move. When code cannot fill it, the refusal names a door the critic holds (probe_by_code / red_sandbox --probe, `brief_pack.py:238-258`, diagnosis `:71`). | C3: every no-path reason on the probe road contains `probe_by_code.py` (table assertion). |
| AR-28 an unknown never becomes a pass | Unreadable run blocks keep today's named unknown and never reach the probe branch. Unreadable job files give a named unknown (F5-a), never "no record" read silently. | C4: rows P4, P18. |
| AR-9 a refusal names a door its receiver can use | The critic's reasons end with `_PROBE_RECORD_PRODUCER`. The automator's and runner's reasons keep `_RECORD_PRODUCER` byte for byte. | C5: row P21 (automator reason byte-identical to `probe_run=False`). |
| AR-19 stage twins change together | S5 automator and critic: the twin difference is a DATA row (the `DERIVERS` key binds `probes.runtime_provenance` to a probe-scoped deriver). The automator/runner paths are unchanged (F2-b). | C5 (same row). |
| AR-4 not tied to one machine | The record path from another machine resolves by the existing tail rule, now shared. | row P15. |
| AR-29 code judges data | The new branch is a join (dispatch id, purpose, job status, field presence, file presence). It refuses nothing itself: the blank refusal stays `handoff_check:field.blank`. | C6: `test_judgment_census.py` green with no census edit (A16: new names avoid `UNIT_NAME_RE` and call no `refusal(`). |
| AR-20 shrink-only ratchets | No ratchet is raised. `role-load.json` is untouched, because no role-read text changes (§5). | C6 (same run) + no diff in `references/role-load.json`. |

Not touched: AR-1/2/3/5/6 (no variety, no host), AR-7/8/10/11/12 (no role text, no tool list), AR-14 (nothing new is written: `--fix` writes the form as before), AR-15/16/17/18, AR-21/23/24/26/27.

### 1.2 Checks added or changed: owner and census class (P27, AR-29)

| Check | Added / changed | Owner | Census class | Census row |
|---|---|---|---|---|
| `window_runtime_record(..., probe_run=True)` probe branch (`_probe_run_record`) | added (a deriver branch, refuses nothing) | data (code) | none: not a census unit (A16) | none. If `test_judgment_census.py` C1 asks for a row, the builder STOPS and reports. No row is added without the Lead (AR-20). |
| `_probe_runtime_provenance` (deriver bound to `probes.runtime_provenance`) | added | data (code) | none | none |
| the blank refusal `handoff_check:field.blank` | text extended only (its `Code could not fill it:` tail) | data (code) | existing rows `run`/`refuse` (shape, data) unchanged | unchanged |

Commit lines: the builder writes the `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py` accepts (the gate is the only carrier of the grammar; it is not copied here). Content to carry:

- architecture: AR-13, AR-22, AR-25, AR-28, with the "how kept" clauses of 1.1 in one sentence each.
- judgment: `none` WITH its ` -- <why>`. Why: the probe branch of `window_runtime_record` joins data (dispatch id, purpose, job status, record presence, file presence), refuses nothing itself, and the census asked for no row.

### 1.3 Joint and census rows

- `references/stage-joints.json`: no row changes. No joint is added. The only hit for `runtime_provenance` is the request requirement at `:3243`, unrelated.
- `scripts/tests/fixtures/driver-exits/s5.json`, `gates.json`: no change. `handoff_check:field.blank` (`gates.json:268`) already exists, and the code of the refusal is unchanged.
- `known_red.json` row `main/S5`: see F4. Once P-a and P-b have both merged, the expected outcome is that the main pass goes past S5 or stops at its next stop. Either way the row's text and node are stale, and the pin's equality makes the canon red until the row is edited. The builder does not run the slow main pass (`plans/builder-rules.md` 7b).
- `scripts/tests/fixtures/form-rounds.json:94` (`derive: s5-critic-to-automator:probes.runtime_provenance`, reason "evidence/runtime-provenance-*.json is not in the world"): unchanged. That world has no job store with a red probe (Not established N4).
- `references/null-outcomes.json:178` (`tool_field`, `default: false`, inventory I12): unchanged. Its conditions `no_runtime_record` / `no_run_in_dispatch` are `reserved` (`null_outcomes.py:164-165`), not wired.

---

## 2. Header-ready manifest (for `python -B tools/dispatch_new.py`; R11-f)

given:
- this card (whole);
- `C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1070-p1b-main-s5-residue-diagnosis.md` (K3, K4 P-b);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole) and `C:/QAFactory/forge-repo/plans/builder-rules.md` (PROJECT.md package item 1);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py` (`:515-651`, `:1636-1678`);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (`:404-518`, JobStore);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py` (`:2878-2995`, `:2395-2416`);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py` (`:257-430`, `:2615-2674`);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1/state/execution-jobs/0c897bbbb87dc97d606971a7101075fa9aea0e6042203d2cf652c35aa94b37a4.json` (a real job's shape);
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/p1b-9-c3-own-run-record.md` (the fragment form).

owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/p1b-pb-probe-run-record.md

non-goals:
- `_review_receipt`, `_form_dispatch`, `Artifacts.__init__` (`handoff_check.py:74-177`): P-a's (t-1071). Not one byte there.
- `run_suite.py`: no run block for `red_probe`. The alternative is NOT taken (brief).
- `execution_request.py`: `JobStore` is not changed (F5-c is not taken).
- `probe_by_code.py`, `red_sandbox.py`, the contract `handoffs/s5-critic-to-automator.yaml`, `agents/qa-code-critic.md`, `references/slices/qa-code-critic/handoff-keys.md`, `references/role-load.json`.
- `known_red.json` (F4-a: the coordinator's), `form-rounds.json`, `null-outcomes.json`, `stage-joints.json`.
- comparing a role-typed value against the deriver (FV2-76); extracting the resolver for `driver_dispatch.walk_run_values` (FV2-67).
- running the main pass, CI, mutations.

handoff: `C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261117-p1b-pb-report.md`. The report form is `.claude/agents/builder.md` rule 7, its content builder-rules item 11. It carries the FR pass (A, C, D, E, G; B "no text a person reads changed except the refusal tail, FR-1/FR-2 lines"), the witness verbatim, and the C1 grep output.

edges: E1-E21 of §4 (each with its invariant).

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/tests/test_handoff.py`. Plus the `test:` lines:
- `python -B ai-packages/qa-factory/scripts/tests/test_handoff.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_field_producers.py`
- `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`
- `python -B ai-packages/qa-factory/scripts/selftest.py --lang`

The last one is needed because the new test row uses a `\u00fc` escape, and the source must stay ASCII (FR-30). Each `test:` line is dropped when the file is in `SLOW_TESTS`: the Lead confirms (N1). Acceptance is items 1-6 below and C1-C6.

siblings:
- FV2-76 (`plans/piles/live-run-fvf/batch-2-live-run-fvf.md:103`, typed value vs `window_runtime_record`): its table must include the critic path once this card has merged. The Lead adds a pointer row.
- FV2-67 (`:94`, "the tail resolver EXTRACTED from window_runtime_record"): this card performs that extraction (`_story_record`). FV2-67 then imports it, and its node text is updated by the Lead.
- P-a t-1071 (same file, disjoint lines).
- FV2-78 (`:105`): superseded by P-a (Lead to mark).
- SIBLING_MAP axes 5 (S5 twins: automator/critic, kept via F2-b), 24/25 (n/a: no run row or freshness read), 32 (judgment: none, §1.2), 34 (one road: F1-B covers both probe tools; F2-b is a data-row difference), 38 (dry census: no joint added), 18 (no ratchet raised).

designer: (the accepted path of this draft, or a skip/resubmission line, as the Lead decides).

Preconditions:
1. Dispatched only AFTER P-a (t-1071) is merged into `main`. The builder's branch starts from an `origin/main` that contains P-a.
2. The builder's edits stay out of `handoff_check.py` `:74-177` (anchor by function names; line numbers shift after P-a).
3. Lead decisions on F1-F5 are written into the dispatch. Without them, the recommended options apply.

---

## 3. Numbered items (for a weaker model; each names file, function, behaviour and its test row)

### Item 1: extract the story resolver (no behaviour change)

File `ai-packages/qa-factory/scripts/handoff_check.py`. Add a module-level function directly above `window_runtime_record`:

```python
def _story_record(task_root, ref) -> str:
    """The story-relative path `ref` names when it is a file of THIS story, else "" (the tail after the LAST part that is the
    story folder, so a record written on another machine still resolves, AR-4; never a path outside the story). Never raises."""
```

Its body is today's `:563-576`, moved without a change in logic:

1. strip `ref`;
2. `root = Path(task_root)`; `parts = PurePosixPath(ref.replace("\\", "/")).parts`;
3. the tail after the last `root.name`, else `ref`;
4. `rel = _story_relative(candidate)`;
5. `is_file` under `try/except OSError`;
6. return `rel` if `is_file` else `""`.

In `window_runtime_record`, replace `:563-579` with `rel = _story_record(task_root, ref)`. When `rel` is empty, return today's reason with today's text. The reason prints the stripped ref (`{ref}`), exactly as today: keep `ref = ref.strip()` before the call.

Test: every existing C3 row (`test_handoff.py:296-394`) stays green unchanged. That is the no-regression witness of the extraction.

### Item 2: the probe branch inside the one reader

1. Signature: `def window_runtime_record(task_root, dispatch, *, probe_run: bool = False) -> tuple:`.
2. Add the constant next to `_RECORD_PRODUCER` (exact text):

```python
_PROBE_RECORD_PRODUCER = ("the record is the stand reading run_suite takes when it launches this review's own probe: "
                          "probe_by_code.py --dispatch <this dispatch> (or red_sandbox.py --probe) runs the probe through "
                          "run_suite, which keeps the completed run under state/execution-jobs/")
```

3. At the top of the function: `producer = _PROBE_RECORD_PRODUCER if probe_run else _RECORD_PRODUCER`. Replace every `{_RECORD_PRODUCER}` in the function's reasons with `{producer}`. With `probe_run=False` every string stays byte-identical (C5).
4. POSITION. The probe branch replaces ONLY the `if not own:` return (`:551-554`), as follows:

```python
if not own:
    if not probe_run:
        return None, (<today's text, byte-identical, ending with {producer}>)
    return _probe_run_record(task_root, dispatch, producer)
```

   The blocks `:533-543` (no dispatch, run blocks unreadable) stay ABOVE it, unchanged. The `own` branch (`:555-580`) stays BELOW it, unchanged.

   The invariant this position keeps:
   - a probe job never outranks the dispatch's own run block, whether that block yields a path or a named reason;
   - an unreadable run block is never hidden by a probe job;
   - a form with no dispatch never reaches the job store;
   - with `probe_run=False` the function is byte-identical to today in every world.

5. Update the docstring: one sentence on `probe_run` ("the probe road: when no run block of the dispatch carries a record, the record of the dispatch's newest completed red_probe run, `runtime_probe_before`, read from run_suite's job store"), and the invariant above.

### Item 3: `_probe_run_record(task_root, dispatch, producer) -> tuple`

A new module-level function. The name avoids `UNIT_NAME_RE` (A16), and the function calls no `refusal(`. It never raises. Steps, in this order:

1. `folder = Path(task_root) / "state" / "execution-jobs"`. In `try:`, do a lazy `import execution_request as ER`, then `files = len(list(folder.glob("*.json"))) if folder.is_dir() else 0`, then `jobs = ER.JobStore(folder).jobs()`. `except Exception as exc:` return `(None, f"the execution jobs under state/execution-jobs/ could not be read ({type(exc).__name__}); {producer}")` (J1).
2. `bad = max(0, files - len(jobs))`. If `bad`: return `(None, f"{bad} execution job(s) under state/execution-jobs/ could not be read, and one of them may be this review's probe run; {producer}")` (J2, F5-a).
3. `own = [j for j in jobs if <all of>]`:
   - `j.get("status") == "completed"`;
   - `isinstance(j["request"], dict)`;
   - `str(j["request"].get("dispatch_id") or "").strip() == dispatch`;
   - `j["request"].get("purpose") == "red_probe"`;
   - `isinstance(j["request"].get("runtime_probe_before"), dict) and j["request"]["runtime_probe_before"]`.

   `jobs()` already guarantees that `request` is a dict.
4. If `own` is empty: return `(None, f"no run block and no completed red_probe run of dispatch {dispatch} (work/run-blocks/, state/execution-jobs/) carries a runtime_provenance record: this review ran no probe through run_suite, or every probe was refused before it started; {producer}")` (J3).
5. `newest = own[-1]` (the order of `JobStore.jobs()`: `updated_at`/`created_at`, then mtime_ns, A10). `job = str(newest.get("job_id") or "<unknown job>")`. `refs = newest["request"]["runtime_probe_before"].get("evidence_refs")`. `ref = refs[0] if isinstance(refs, list) and refs else None`. If `not isinstance(ref, str) or not ref.strip()`: return `(None, f"the newest probe run of dispatch {dispatch} (execution job {job}) carries a stand reading with no evidence_refs: the probe wrote no file for it (a rehearsal or a failed write); {producer}")` (J4).
6. `ref = ref.strip()`; `rel = _story_record(task_root, ref)`. If empty: return `(None, f"the probe run of dispatch {dispatch} (execution job {job}) names {ref}, which is not a file of this story; {producer}")` (J5).
7. Return `(rel, f"the stand reading of red_probe run {job} (dispatch {dispatch}, state/execution-jobs/)")`.

### Item 4: the deriver of the probe field (a data row, F2-b)

Below `_runtime_provenance`, add:

```python
def _probe_runtime_provenance(art, doc, row=None):
    """`probes.runtime_provenance`: the record of THIS review's own probe run (`window_runtime_record(..., probe_run=True)`)."""
    path, why = window_runtime_record(art.root, _form_dispatch(art, doc), probe_run=True)
    return (path, why) if path else (None, "", why)
```

In `DERIVERS`, change only `"probes.runtime_provenance": _runtime_provenance` to `_probe_runtime_provenance`. Add a one-line comment saying why the key differs: "the critic's field names the probe's run, not the window's run (A14)". `artifacts.runtime_provenance` and `runtime.provenance` keep `_runtime_provenance` (A18: the identity pin still holds).

### Item 5: tests (`ai-packages/qa-factory/scripts/tests/test_handoff.py`, keep row; no new test file)

(a) A helper next to `_run_block`:

```python
_probe_job(task, name, dispatch, *, purpose="red_probe", status="completed", before=<dict|None|any>,
           provenance=None, updated="2026-01-02T00:00:00+00:00")
```

It writes `task/state/execution-jobs/<name>.json` holding `{"job_id": name, "idempotency_key": name, "status": status, "created_at": updated, "updated_at": updated, "request": {"dispatch_id": dispatch, "purpose": purpose, "runtime_provenance": provenance, "runtime_probe_before": before}}`. When `before` is the sentinel "absent", the `runtime_probe_before` key is omitted.

(b) ONE table function `the_probe_record_is_the_reviews_own()`, registered in `main()` right after `the_runtime_record_is_the_windows_own()`. Its rows are `(case, got, expected_path_tuple, said)`. Assertions:
- the path, as in `:397`;
- for no-path rows: `len(got) == 3 and said in got[2] and "probe_by_code.py" in got[2]`.

`C = "S5-qa-code-critic-1"`, `A = "S5-qa-automator-1"`. `derive(task)` is `H._probe_runtime_provenance(H.Artifacts(task, dispatch=C), handoff.parse("header:\n  dispatch: ''\n"))`. The rows are P1-P21 of §4 (each edge maps to its row).

(c) Extend `the_blank_provenance_field_says_why_code_could_not_fill_it` with ONE variant on the critic form. Use `handoff.template("s5-critic-to-automator")`, `H.check(..., H.Artifacts(task, dispatch=C), fix=True, ...)`:
- (c1) with a P1-shaped job: `probes.runtime_provenance` is not among the problems, and `out.get("probes.runtime_provenance") == "evidence/runtime-provenance-api-b.json"`;
- (c2) with no job: one `blank` problem whose text contains `Code could not fill it:`, `S5-qa-code-critic-1` and `probe_by_code.py`.

(d) "The test can fail" (builder-rules 7b): row P1 and (c1) are red on the tree before item 2. The report quotes that one red line.

### Item 6: changelog fragment

Create `ai-packages/qa-factory/changelog.d/p1b-pb-probe-run-record.md`: one bullet in the form of `p1b-9-c3-own-run-record.md`, ASCII only. Content: "the code critic's `probes.runtime_provenance` is filled by `handoff_check --fix` from the stand reading run_suite takes when it launches the review's own red probe (`runtime_probe_before` of the dispatch's newest completed `red_probe` job under `state/execution-jobs/`); a run block of the dispatch still decides first; the automator's and runner's fields are unchanged; a field code cannot fill says why and names `probe_by_code.py` (P-b)".

---

## 4. Edges, each with its invariant, and the test row that holds it

| Edge | Behaviour | Invariant it protects | Row |
|---|---|---|---|
| E1 no dispatch | `(None, "the form names no dispatch, so its own run cannot be found; <probe producer>")` (today's line, producer swapped on the probe road) | no record without the form's own dispatch | P20 |
| E2 run blocks unreadable (`bad`) | today's named reason, probe producer; the job store is not read | an unreadable block that may be this dispatch's is never hidden by a job | P4 |
| E3 the dispatch HAS an own run block with a record | today's answer verbatim. If it is a path, path and source are byte-identical to `probe_run=False`. If it is a named reason (refs empty, file missing), that reason, and the jobs are not consulted | a probe job NEVER outranks a dispatch's own run block | P2, P3 |
| E4 no `state/execution-jobs/` folder | J3 | absence is "no probe run": blank, never a pass, never a guess | P5 |
| E5 only another dispatch's jobs (the automator's ordinary job; another critic dispatch's red probe; an S6-close stand-in) | J3 | never another dispatch's record | P6 |
| E6 a job of this dispatch with `purpose` other than `red_probe` | not counted; J3 if nothing else | only a PROBE run answers the probe field from the job store (a test run of the dispatch writes a run block, E3) | P7 |
| E7 `status` ∈ {persisted, running, incomplete} or absent | not counted | a run that did not finish is never named | P8 (3 rows) |
| E8 a completed red_probe job with `runtime_probe_before` absent / `{}` / a string / a list | not counted; J3 if nothing else | a record not taken at THIS probe's launch is never named (A9: only a launched, checked run carries it) | P9 (4 rows) |
| E9 several qualifying jobs | the last of `JobStore.jobs()`: newest `updated_at`/`created_at`, a same-second tie broken by file mtime_ns. An exact tie of both takes glob order, either answer is one of this review's own completed probe runs | the newest decides. Whichever wins, it is never a run of another review | P10, P11 |
| E10 newest qualifying job: `evidence_refs` empty / not a list / first not a string / blank, while an OLDER job has a good ref | J4; the older job is NOT used | the same rule as the run-block road (`:557-562`): nothing older stands in for the newest, nothing guessed | P12, P13 |
| E11 the ref names a missing file / `../X/...` / an absolute path of another story / a placeholder | J5 | never a file outside this story (`_story_relative`) | P14 (3 rows) |
| E12 the ref is absolute from another machine (`C:/elsewhere/.../artifacts/QA-1/evidence/b.json`), file present here | resolved by the tail | AR-4 | P15 |
| E13 a job file that is malformed JSON, starts with a UTF-8 BOM (`jobs()` reads `utf-8`), is a JSON list, or is a dict without `request` | J2 (count of `*.json` greater than readable jobs) | FR-59 / AR-28: an unknown is named, never read as "no record" | P18 (4 rows) |
| E14 the import of `execution_request`, the glob or `jobs()` raises | J1 | never raises (the deriver's contract, `:531`) | covered by the `except` path. Whether to add a row by monkeypatching `ER.JobStore` is the builder's choice, NOT required |
| E15 TEMPORAL, before the change (stories in flight) | Forms with a typed value are untouched: `--fix` fills blanks only (`:1642`). Blank critic fields in a story whose jobs carry `runtime_probe_before` (present at least since cart-1, 2026-10-31, A20) are filled at the next `--fix`. Jobs without it fall under E8 | a story in flight is never given a record its probe did not take; a typed value is not this card's (FV2-76) | P9 + (c1) |
| E15 TEMPORAL, after the change | The change creates NO artifact (no new file, flag or config): the job store and the evidence files exist today (A10, A12). The only new file is the changelog fragment, which no code reads | n/a: no two-world artifact | n/a |
| E16 POSITIONAL | item 2.4 | see item 2.4 | P2, P3, P4, P20 |
| E17 the automator's / runner's paths, even when their dispatch HAS a completed red_probe job (`run_suite --mine --purpose red_probe` is open, `MINE_PURPOSES`, `execution_request.py:571`) | never reach the branch; result and reason byte-identical to today | the window's run record is never replaced by a probe's (the field meanings differ, F2) | P21 |
| E18 conflicting requirement pair: the brief's "newest red_probe REQUEST under work/probe-requests" vs. the brief's own invariant "a record this review did not probe against = never" | resolved for the invariant: the request file names the automator's record (A13) | see F1/F3 | P1 |
| E19 magnitude: `evidence_refs` with 10,000 entries | the first is taken | no limit is introduced, so there are no AT/BEYOND rows (CLAUDE.md rule 11) | P17 |
| E20 encoding: a non-ASCII ref (`runtime-provenance-api-\u00fc.json`, written with the escape in the test source), file present | resolved | a path is compared as text, never re-encoded | P16 |
| E21 adversarial: a role-forged `work/probe-requests/*.json` naming any file | never read (not a source under F1-B) | a role's hand-written request is no evidence of a run | P19b: a forged request with no job gives J3 |

Rows not tied to one edge:
- P1: the dry-world shape. The critic job's `runtime_provenance.evidence_refs` names file `a` (the automator's) and its `runtime_probe_before.evidence_refs` names file `b`. The answer is `b`.
- P19: `dispatch_id` with surrounding spaces matches (the same `strip()` as `:547`).

### 4.1 The direction of the permitted error (designer rule 1; PROJECT.md package item 6 (c))

The reused function is `window_runtime_record`, together with the job store read through `JobStore.jobs()`, an adviser-class lookup (A10: "never the idempotency decision"). It moves into a more load-bearing role: filling a REQUIRED field of the exit gate.

- The permitted error: a BLANK field when a record exists. That is today's behaviour, and it costs one more `--fix` round or a typed value. Examples:
  - an exact tie;
  - the newest job's refs are empty while an older job's are good (E10);
  - a corrupt job beside a good one (E13);
  - the request file says more than the job.
- Never permitted: naming a record this review did not probe against.

Adversarial inputs that must stay on the safe side, each a row:

| Input | Rows |
|---|---|
| another dispatch's job or run block | P6 |
| the automator's file carried in the critic request's `runtime_provenance` (A13) | P1 |
| a request that was written but never launched (refused at the stand check, A9, so no job exists) | P19b |
| a job that did not finish | P8 |
| a job without a launch reading | P9 |
| a ref outside the story | P14 |
| a forged request file | P19b |
| an S6-close stand-in dispatch | P6 |
| the automator's own red probe job reaching the automator's field | P21 |

A forged JOB file under `state/execution-jobs/` has the same exposure as a forged run block on today's road (`work/run-blocks/`). The road is not widened (N5).

---

## 5. Does the field's meaning change, and which texts change (FR-37, AR-10)

- The contract meaning (A14) does not change. It already says "the record of this review's own probe run". The card makes the code read exactly that: the reading taken at the probe's launch (F3-b). The contract, the charter (A15), the critic slice `references/slices/qa-code-critic/handoff-keys.md:32` and the placeholder hint stay byte-identical. So the `qa-code-critic` role load (`role-load.json:17,31,40`, at its ceiling) does not move.
- What does change is the meaning of the DERIVER's source for one field. Before, it read "a run block of the dispatch" only. After, it reads "a run block of the dispatch, else the launch reading of its newest completed probe run". This is why the plan critic is owed (PROJECT.md package item 6). Item 6 (a), the premise measured on real data, is A13.
- A person or role reads one changed text: the blank refusal's tail on the critic form (`_PROBE_RECORD_PRODUCER`, FR-1/FR-2). It names only paths the code writes: `state/execution-jobs/`, written by `run_suite.py` (A10; FR-37). It is printed by `handoff_check` at run time and is not a role-load layer.

---

## 6. Readers of every touched file (designer rule 7)

Command: Grep `handoff_check|window_runtime_record|_RECORD_PRODUCER|test_handoff\.py`, plus `changelog\.d` for settings.json, over `tools/`, `.githooks/`, `.claude/agents/`, `.claude/settings.json`.

| Where | Hits | Reader | Verdict |
|---|---|---|---|
| `tools/` | 2 files | `tools/lint-baseline.json:235` (`test_handoff.py`, class `HandReaderInput`, args `RR-plan-row`, count 1) | unchanged, unless the new rows trip `HandReaderInput` (N3) |
| `tools/` (same grep) | | `tools/test_dod_gate.py:1208,1254` | unchanged: false positives, test names about dispatch handoff files (read `:1250-1261`) |
| `.githooks/` | 0 | positive control: the same grep finds hits in `tools/` | none |
| `.claude/agents/` | 0 | positive control: `handoff` gives 8 hits in 3 files | none |
| `.claude/settings.json` | 0 | positive control: `hooks` gives 16 hits | none |

Inside the package, for the changed names:

| Reader | Verdict |
|---|---|
| `window_runtime_record`: package-wide grep, the only callers are in `handoff_check.py:585` (`_runtime_provenance`) and, after this card, `_probe_runtime_provenance` | changes in this card |
| `DERIVERS` readers: `handoff_init.py:271` (reads `{section}[].version` only) | unchanged |
| `DERIVERS` readers: `test_field_producers.py:81,161-167` (membership + the automator/runner identity) | unchanged. Holds per A18; DoD `test:` line |
| `DERIVERS` readers: `test_handoff.py` | changes in this card |
| `handoff_check.py` is imported by 59 package files (Grep `import handoff_check|from handoff_check import|handoff_check as`) | none import `window_runtime_record`, `_runtime_provenance` or `_RECORD_PRODUCER`. The signature change is keyword-only with a default: unchanged |
| a new lazy import edge `handoff_check -> execution_request` (inside a function) | any import-graph ratchet: N2 |
| `changelog.d/p1b-pb-probe-run-record.md` (new) | read by the release step only (`docs/RUNBOOK.md` §4.1): unchanged |

Parallel streams that meet here:
- P-a (same file, `:74-177`): sequential by precondition 1;
- FV2-76 and FV2-67 (same file / same function): not in work (status `ожидает`, batch-2 `:94,:103`). Their node texts get the pointer rows named in `siblings:`.

---

## 7. Sweep inside `handoff_check.py`: derivers whose input may not exist on the road of the role whose contract lists the field

Read this round: `DERIVERS` `:644-674`, `LIST_DERIVERS` `:639-642`, `BY_PATH` `:682-687`, and the bodies `:140-198, 329-475, 491-519, 583-636`. "Walked" means I have a positive fact that the input is produced on that role's road. "Scout" means not established within this budget.

| Entry | Input | Verdict |
|---|---|---|
| `artifacts.runtime_provenance` (s5-automator-to-critic) | the automator's run blocks | walked: holds (kept world: run block of `S5-qa-automator-1` with a record, A13) |
| `probes.runtime_provenance` | | THIS card |
| `runtime.provenance` (s5-automator-to-runner) | the automator's run blocks | walked: holds (same fact) |
| `artifacts.run_witness`, `run.witness`, `rounds[].verify.witness` | manifest `runs[]` / `run_witness` / `run-report.witness` | scout: does `run.witness` on s6-runner-to-analyst have `runs[]` on the runner's road (null-outcomes row `no_run_in_dispatch`, `null-outcomes.json:208`)? |
| `review.findings_file` | `_form_dispatch` + the critic's own findings file | walked: holds (`:180-198`) |
| `review.receipt_ref` | | P-a |
| `review.rollcall` | the case critic's roll-call rows | scout (`form-rounds.json:90-91` declares it absent from the form world only) |
| `artifacts.probes` (also `LIST_DERIVERS`) on s5-automator-to-critic | `work/probes/*.json` | SCOUT, possibly the same class as this card: the automator's form lists probe records, but the probe tools are the critic's (`brief_pack.py:238-258`). Does the automator's road write any? `form-rounds.json:92` declares them absent from the form world |
| `artifacts.tests` | manifest `tests[].file` | walked: holds (kept world `work/automation-manifest.json`) |
| `implementation.diff.*` (3) | `work/impl-diff*.txt` via `diff_pass` | walked: holds (kept world `work/impl-diff.txt`) |
| `implementation.source` | pipeline / context-manifest | walked: holds (kept world `work/context-manifest.json`) |
| `run.totals`, `run.window_totals`, `run.execution_status` | `work/run-report.json` | scout for the S6 runner road (the kept world has one at S5, which is no proof for S6) |
| `delivery.ready`, `delivery.blocked_by` | `work/ledger.json` | scout (S8) |
| `size.computed` | `work/sizing.json` | walked: holds (kept world) |
| `scope[].case_version` | `state/story-case-links.json` | scout (not listed in the kept world's `work/`; it lives under `state/`, not globbed) |
| `scope[].material_collected` | `work/source-inventory.json` | walked: holds (kept world) |
| `inputs_read[].version` | sha of a named path | walked: holds (pure function of the row) |
| `grounding.*` (5, `:1030`), `blast_radius` | grounding tables | scout (`form-rounds.json:80-89`) |
| `BY_PATH` (4: `_requirements_of`, `_plan_row_of` on the S4 designer contracts) | the case file | walked: FV2-1 accepted 1d1206b (batch-2 `:28`) |

Scout question for the Lead (one dispatch): "For every `DERIVERS`/`LIST_DERIVERS`/`BY_PATH` entry of `ai-packages/qa-factory/scripts/handoff_check.py` marked scout in §7 of `docs/tasks/specs/20261117-p1b-pb-runtime-provenance-card.md`, name the role whose contract lists the field and whether that role's road (its brief card in `brief_pack.py`, its charter) writes the deriver's input. Answer per entry: produced by <tool>, or not produced, with file:line. First priority: `artifacts.probes` on s5-automator-to-critic."

---

## 8. Forks returned (the Lead decides; the owner is away, so the recommended option is executable until the owner's word)

**F1: the source of "the probe run of this dispatch".**
- (A) The brief's literal source: the newest `red_probe` request file under `work/probe-requests/`.
  - Facts against it:
    - (i) it proves no launch: the file is written BEFORE `run_suite` and survives a refused run (A7, A9);
    - (ii) its only time field is the copied `runtime_provenance.timestamp`, and its names are reused and overwritten (A7);
    - (iii) it misses `red_sandbox.py --probe`, whose request goes to `work/requests/` (A11). That is a second road for the same action (P31, axis 34);
    - (iv) it carries the automator's record, not the probe's (A13).
- (B) run_suite's job store, `state/execution-jobs/`, read through `JobStore.jobs()`. Each job is the launched request plus `status` and timestamps. It covers both probe tools and is written only for a run that passed the launch check.
- (C) Join (A) to (B) by `idempotency_key`. This keeps (A)'s file as the candidate list but inherits (A)'s overwrite and red_sandbox gaps.
- **Recommended: B.** Cost: one lazy import of `execution_request` in `handoff_check`. The Lead's direction "the probe request of this dispatch" is kept in substance: the job's `request` IS that request, as launched.

**F2: the scope of the fallback.**
- (a) The brief's literal scope: inside `window_runtime_record` for all three callers. An automator or runner dispatch with no run block but with its own red probe job (`run_suite --mine --purpose red_probe` is open to it, `execution_request.py:571`) would then get the probe's stand reading in a field that means the window's run.
- (b) Only `probes.runtime_provenance`, through `probe_run=True` and a separate deriver bound by its `DERIVERS` key (a data row, a legal difference under designer rule 6 / AR-1). The automator and runner stay byte-identical in every world.
- **Recommended: b.** Cost: one deriver function and one keyword.

**F3: which record inside the probe job.**
- (a) The brief's literal record: `request.runtime_provenance.evidence_refs[0]`. On a red probe this is the PRECEDENT copy (A8). In the kept world it is the automator's file `...075205Z.json` (A13). Its identity was verified equal at launch, but the file was written for another dispatch's run.
- (b) `request.runtime_probe_before.evidence_refs[0]`: the reading `run_suite` took at THIS probe's launch (A9). In the kept world it is `...075258Z.json`, which exists. It is present only on a run that passed the launch check.
- **Recommended: b.** It matches the contract's words (A14) and is the only option on the safe side of 4.1. For the automator the two records are the same file (its job's `runtime_probe_before` and `runtime_provenance` both name `...075205Z.json`, A13), so (b) is the analog of the run-block road, not a new meaning.

**F4: the `known_red.json` row `main/S5` after the fix.**
- (a) The builder does not touch it. After P-a and P-b both merge, the coordinator runs ONE main pass with the world kept (as t-1070 did: 393.5 s < 800 s, diagnosis `:20-23`). In the same merge it either removes the row and sets pin 0 (the pass went past S5 and nothing else is red), or relabels it with the measured next stop: a new row id, `node`, `raised_by` naming the product finding.
- (b) The builder edits the row blind (to "removed"). The canon goes red if the pass stops at S5/S6 for another reason.
- (c) Merge and let the canon go red, then fix the label (a `defect_found` that is known in advance).
- **Recommended: a.** Cost: one main pass, about 7 minutes, by the coordinator. The label text must not be guessed (FR-41).

**F5: unreadable job files.**
- (a) Name them (J2), using the count of `*.json` files minus the readable jobs. This mirrors `bad` on the run-block road (`:541-543`).
- (b) Accept `JobStore.jobs()`'s silent skip. The error still stays on the safe side, an older own probe or blank, but an unknown is read as absence (FR-59).
- (c) Add a `bad` return to `JobStore.jobs()`. This touches `execution_request.py`, a file with many readers that is outside this card.
- **Recommended: a.** Cost: one glob. A corrupt job of ANOTHER dispatch also blocks the critic's derivation, exactly as a corrupt run block does today.

## 9. Small choices closed by the designer (no design weight; listed so the critic can reopen any)

1. The helper names `_story_record`, `_probe_run_record` and `_probe_runtime_provenance` avoid `UNIT_NAME_RE` and call no `refusal(` (A16), so no census unit is created.
2. The glob count is taken BEFORE `jobs()`. A job landing in between makes the difference negative, and `max(0, ...)` gives 0. A file landing after the glob is simply not seen: an older answer or blank, the safe side.
3. `runtime_required` is not checked separately. The presence of `runtime_probe_before` implies the launch check ran (A9).
4. `execution_status` is not filtered: `inconclusive` and `failed` (an intended failure) both count. This mirrors the run-block road, which writes blocks for both. The reading is the stand at launch either way.
5. Order and tie-break are those of the existing reader (`JobStore.jobs()`). No second ordering rule is invented. The tie-break uses mtime_ns only inside that reader, after the `updated_at`/`created_at` fields; mtime is not the primary order.
6. On the probe road, the reasons of the run-block branch (no dispatch, unreadable blocks, own block refs empty or missing) also end with `_PROBE_RECORD_PRODUCER` (FR-2: the critic's door). The path and source on that branch stay byte-identical.
7. A missing `job_id` is printed as `<unknown job>`.
8. The changelog fragment is ASCII and in the house form.

## 10. Not established (no shell; the Lead runs these)

- N1: whether `test_handoff.py`, `test_field_producers.py` or `test_judgment_census.py` is in `SLOW_TESTS`, and what `--witness-for` prints for the two owns. Command: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/tests/test_handoff.py`, and `grep -n "SLOW_TESTS" -A40 ai-packages/qa-factory/scripts/selftest.py` (or wherever `SLOW_TESTS` lives: `grep -rn "SLOW_TESTS *=" ai-packages/qa-factory/scripts`).
- N2: whether any ratchet counts import edges of `handoff_check.py` (the rule-7 "ratchet on importers"). Command: `grep -rn "handoff_check" tools/*.json ai-packages/qa-factory/scripts/tests/fixtures/*.json`.
- N3: whether the new rows trip the `HandReaderInput` lint (`tools/lint-baseline.json:235`). The row writes job JSON by hand, as `_run_block` already writes run blocks. Command: the lint ratchet the canon runs (`python -B tools/lint_ratchet.py --check` or its CI job). The canon judges it.
- N4: that the form world behind `form-rounds.json:94` holds no red-probe job, so the row stays true. The canon judges it.
- N5: whether the guard refuses a role's write under `state/execution-jobs/` (the same question as for `work/run-blocks/` today). Command: `grep -n "state/" ai-packages/qa-factory/references/artifact-writers.json ai-packages/qa-factory/scripts/guard_pre_tool.py | head`.
- N6: the step-0 premise was measured by the designer by reading the kept world (A13), not by running code. An in-process confirmation for the plan critic or Lead, read-only and after the builder's diff:

  ```
  ( cd C:/QAFactory/forge-repo/ai-packages/qa-factory && python -B -c "import sys; sys.path.insert(0,'scripts'); import handoff_check as H; t=r'C:\Users\i_mas\AppData\Local\Temp\qa-story-run-s0-tqwkmqn_\qa-factory\artifacts\DRY-1'; print(H.window_runtime_record(t,'S5-qa-code-critic-1',probe_run=True)); print(H.window_runtime_record(t,'S5-qa-code-critic-1')); print(H.window_runtime_record(t,'S5-qa-automator-1'))" )
  ```

  Expected:
  - `('evidence/runtime-provenance-dry-pytest-20261117T075258Z.json', 'the stand reading of red_probe run 44bcd10c384267c69a56 ...')`;
  - today's critic text, byte-identical;
  - `('evidence/runtime-provenance-dry-pytest-20261117T075205Z.json', 'the runtime_provenance of run block ...')`.

  The kept world is a temp folder: if it is gone, re-create it with the t-1070 scratch runner (diagnosis `:13`).
- N7: the next stop of the main pass after P-a and P-b (F4-a).

## 11. Noticed analogs and contradictions in the brief (reported, scope not widened)

- The brief's direction (`work/probe-requests`, `runtime_provenance.evidence_refs[0]`) contradicts its own error-direction line (item 4) on measured data: A13, see F1/F3.
- The brief lists three callers that "get" something today. In fact the automator and runner get their own run block's record, and the critic gets the named "no run block" reason (A4).
- FV2-67's planned extraction of the tail resolver is done here as `_story_record`, and FV2-76's comparison table should gain the critic path. Both are in `siblings:`.
- `artifacts.probes` on the automator's form may be the same class of gap as this card (§7, scout first priority).

## Reading trail (this round)

- the diagnosis t-1070 (whole);
- `handoff_check.py:1-200,200-480,480-720,1636-1685`;
- `run_suite.py:455-625,2395-2420,2878-3006` and the grep `runtime_provenance|evidence_refs`, `runtime_probe|write_text|atomic_json|json.dump`, `store.begin|status=`;
- `probe_by_code.py:1-40,2910-2980,4640-4709,6120-6209` and the greps `probe-requests`, `evidence_refs`, `build_request|run_request|"red_probe"`;
- `execution_request.py:400-540,2830-2919,3221-3280,3370-3419,3895-3934` and the greps `runtime_provenance|dispatch_id|purpose|runtime_observed`, `created_at`, `precedent`;
- `runtime_probe.py:1560-1599`;
- `red_sandbox.py:995-1009,1250-1264` and the grep `red_probe|build_mine_request|run_suite`;
- `handoffs/s5-critic-to-automator.yaml` (whole);
- the greps over `agents/`, `brief_pack.py`, `tests/dry_stub.py` with positive controls;
- `references/role-load.json:1-46`;
- `judgment-census.json` grep `handoff_check`;
- `test_judgment_census.py:77,218-277` and the grep `def |ast.`;
- `test-layers.json:2295-2329,1687-1689,2802-2804,3400-3402`;
- `test_handoff.py:170-440` and the greps `window_runtime_record|...`, `main`;
- `test_field_producers.py:70-180`;
- `form-rounds.json:80-104`;
- `null-outcomes.json:170-184`;
- `null_outcomes.py` grep `no_runtime_record`;
- `stage-joints.json` grep;
- `driver-exits/known_red.json` (whole), `s5.json` grep, `gates.json` grep `handoff`;
- `plans/builder-rules.md:36-71`;
- `plans/piles/live-run-fvf/batch-2-live-run-fvf.md:1-30,94-105`;
- `docs/SIBLING_MAP.md` headings, axes 24, 25, 34;
- `changelog.d/p1b-9-c3-own-run-record.md`;
- `tools/lint-baseline.json:228-242`, `tools/test_dod_gate.py:1250-1261`;
- `.claude/settings.json` and `.claude/agents/` greps with controls;
- cart-1 jobs (grep and `0c897bbb...json:1-60`);
- the kept world: Glob of `state/execution-jobs/*.json`, `work/**/*`, `evidence/runtime-provenance-*.json`; Grep and Read of job `230891e4...json:1-171`; Grep of job `3cfdedf7...json`; Grep of `work/probe-requests/probe-walk-test_the_case-1.json`.

## Lead decisions on the forks (17.11.2026, Fable; owner asleep: by recommendation, until the owner's word; draft accepted t-1072)

F1 = B (run_suite's job store `state/execution-jobs/` through `JobStore.jobs()`); F2 = b (the fallback only for
`probes.runtime_provenance`); F3 = b (`request.runtime_probe_before.evidence_refs[0]`); F4 = a (the coordinator runs one
main pass after P-a and P-b merge and relabels `known_red.json` `main/S5` by what it shows); F5 = a (unreadable job files
are named as an unknown). Spot check of A13 by the Lead in the kept dry world: job `230891e480ca` (`red_probe`, completed,
dispatch `S5-qa-code-critic-1`) carries `runtime_probe_before` = `...075258Z.json` and `runtime_provenance` =
`...075205Z.json` (the automator's); job `3cfdedf79422` (`initial`, `S5-qa-automator-1`) carries `...075205Z.json` in both.
The direction itself (a fallback source for the critic's window) stays a question to the owner in the morning report.

## Fix round after the plan critic t-1075 (BINDING; overrides the text above where they differ). Lead, 17.11.2026

Verdict: `docs/tasks/specs/reviews/t-1075-p1b-pb-plan.md` (accept with fixes, 0 blocking). Every FIX and NOTE is taken.

- **F-1 = (a).** New edge E22 + a test row: every completed own `red_probe` job has `runtime_required: false` (so no
  `runtime_probe_before`). Outcome: the field stays blank with a DISTINCT reason J6: "the probe runs of dispatch <X> ran
  with no stand to read (`runtime_required: false`), so run_suite took no stand reading; the field has no record by code".
  J6 names no door that re-runs the probe. The reserved null outcome `no_runtime_record` (`null_outcomes.py`,
  `null-outcomes.json` row `s5-critic-to-automator:probes.runtime_provenance`) is the eventual home: NOT wired here, queued.
  §9.3 is withdrawn: `runtime_required` is read, to tell J6 from J3b.
- **F-2.** New edge E23 + a test row: the dispatch owns no job because every probe was answered by an earlier probe's
  receipt (`proof_level.already_probed`, a repair round). Outcome: blank (never another dispatch's record), reason J3a.
  Whether a repair-round review should carry the earlier probe run's record is a MEANING question for the owner (morning
  report); until her word the value is blank.
- **F-3.** J3 splits. J3a (no own `red_probe` job at all): "... no probe of this review ran through run_suite (none was
  launched, every one was refused before it started, or every one was answered by an earlier probe's receipt, which
  belongs to another dispatch); ..." — it promises no door that `already_probed` closes. J3b (own `red_probe` jobs exist,
  none completed with a stand reading): names the count and the newest job's status. Rows P8/P9 assert J3b. Joins only,
  no census unit.
- **F-4 (replaces the F4 = a line).** The builder does not touch `known_red.json` or any group ledger. The coordinator:
  merges `origin/main` (with P-a) INTO the P-b branch; on that branch runs the main pass and starts the canon's dry-only
  door (`python tools/ci_read.py start --ref <branch> --var dry_only=true`); relabels `known_red.json` and any group
  ledger from what both show as a coordinator commit ON THE P-b BRANCH; only then `wave.py merge`.
- **F-5.** Queued, not fixed here: a finding in `live-run-fvf` — "the run block's `runtime_provenance` is the request's
  (possibly copied) record, not `runtime_probe_before`; one road for the three provenance fields = the launch reading of
  the dispatch's newest completed job" (SIBLING_MAP axis 5). The builder adds it to its report's `siblings` line only.
- **F-6.** Wording everywhere (§4.1, E8, docstrings, reasons): "the record the launch reading cites", never "the record
  written at this launch" (a project's own probe may cite one file for every launch).
- **Notes.** N-1: the `PurePosixPath` import moves into `_story_record`. N-3: §1.1's AR-13 row gains one line naming that
  J2's glob count restates JobStore's layout and may drift. N-4: tests construct `Artifacts` with the constructor as P-a
  leaves it (read the merged signature). N-5: row P11 asserts MEMBERSHIP in the set of own jobs' records, never one
  winner (FR-58). N-2, N-6: no change.
