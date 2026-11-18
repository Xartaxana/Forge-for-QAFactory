# RD1-37 + RD1-38 card: the pinned site read moves into the reader, and an unread product probe gets the critic's one door

task: t-1367 | nodes: rules-debt/1/RD1-38 (fork RD24-a of critic t-1348) and rules-debt/1/RD1-37 (Lead decision F3 of
the RD1-24 card, "RD1-24b") | feature: F19 | status: DRAFT (designer). The Lead decides; forks are in §9.
Pile rows: `plans/piles/rules-debt/batch-1-phase-2.md` :65 (RD1-37), :66 (RD1-38). Base: main with RD1-24 (77326421) and
RD1-28 (2a125072) merged (Lead `facts:`).

## 0. Target on main (measured; file:symbol)

1. **Confirmation in a consumer.** `red_sandbox.py::_pinned_read` :1206-1224 (second `assertion_site` call with
   `pinned_frames`, then the guard: location == pin, kind `assertion`, `reason_matches`); `target_result` :1250-1255
   calls it only on `site_unread` + `failed` and appends `why`. In the reader only `reporters.py::pinned_frames` :413-426.
2. **Rule broken.** `docs/SIBLING_MAP.md:147`: "A new reporter or runtime enters the reader, never a consumer".
3. **Other consumer.** `probe_by_code.py::_judge_rows` :4362-4369 and `::_walk_run_once` :6207-6214 (sites judged in
   `_walk_attempt` :6315-6318): no pinned read. There the place NEVER proves (docstring :62; `judge_probe_row`
   :3249-3284 puts the site into `observed` only; `_judge_joint_rows` reads `location` only for `_earlier_check_at`
   :3378, the EP-G stop); `record["expected_reason"]` is the marker (`_new_record` :4627).
4. **Door.** `probe_by_code.py::judge_record` :7861-7910 (one writer of `judgment`, pinned
   `test_probe_marker_judgment.py:524`); `_judged_record` :7733-7762; `_judge_input` :7765-7800 (word in
   `JUDGE_VERDICTS` :196; quote <= 300, a folded substring of stored `message`/`failure_text` or a `rows[]` item;
   `fires` refused on empty texts or `rows_cut` > 0; `cannot_judge` needs `--why`); `_demand_critic_dispatch` :7834
   (record `task` + `case`); `_judge_cli` :7913; `JUDGE_DOOR` :194, one text (pinned :531-540).
5. **Product probe today.** `red_sandbox.py::probe` :1841-1863: unread -> `incomplete`, no receipt, "Record it as a
   `tooling` finding". `_write_product_records` :1538-1576: `verdict`, `dispatch_id`, `test_file_sha256` (raw sha,
   `proof_level` :781), identity, `mutated_files`; no `task`, `case`, `cause`, text or receipt material. The sandbox and
   `.qa-probe.json` (`prepare` :612-636) are removed before `probe` returns.
6. **Boundary.** `probe_by_code.py:161`: "red_sandbox never imports this module" (no `judgment_facts`, `cut_text`
   :3462, `JUDGE_DOOR` from red_sandbox); probe_by_code imports red_sandbox (:161, :4302, :6158).

## 1. Architecture (designer rule 1)

| AR | touched by | change check (in the step's DoD) |
|---|---|---|
| AR-13 | S1: one home for the pinned read (`reporters.pinned_site`); S2: one failure-text cutter in `reporters` (F6 a) | Grep `pinned_frames\(` over `scripts/*.py`: `reporters.py` only (control: the same Grep before the edit finds red_sandbox) |
| AR-14 | S3: `judgment` keeps one writer (`judge_record`); receipt files one writer (`red_sandbox`) | `test_judgment_written_only_by_probe_by_code` passes unedited |
| AR-22 | S2 produces `cause`, `judgment_facts`, `task`, `case`, `pending_receipt` (reader: the S3 door); S3 produces receipt `proved_by`/`judgment` (reader: `window_record.py:917`) | §7 names each reader |
| AR-2 | S2/S3: an unread product failure becomes the code critic's judgment, never a code verdict | the S3 row on a `.kt` world (unlike the default) ends judged, not halted |
| AR-28 | unreadable or mismatching input stays `incomplete` or is refused | §4 rows |
| AR-29 | S1 `pinned_site`: xref / data (moved). S2 `judgment_owed`: shape / data (routes only). S3 door checks: xref, shape / data; the verdict: owner judgment (code critic, read by the S5 acceptor); census row `judge_record` (xref, judgment) stays | new names miss `UNIT_NAME_RE` (`test_judgment_census.py:77`); refusals via `raise _judge_refusal(...)` in existing door functions; a unit the census still names gets a row (xref/data) |

Commit lines: the `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py` checks (the only
carrier). S1: AR-13, AR-28, AR-29; `judgment: none -- the reader move keeps a data cross-reference; no role judgment is
classified or refused`. S2: AR-2, AR-13, AR-22, AR-28, AR-29; `judgment: none -- the record only states that a judgment
is owed; code decides nothing of it`. S3: AR-2, AR-14, AR-22, AR-28, AR-29; the judgment line names the code critic's
`fires|other_failure|cannot_judge` on a product record, in the gate's form.

Variety walk (`design/architecture.md` § A):
- `axis 3: held by table|role -- references/detectors.json assertion_probes, then reporters.pinned_site, then the code
  critic's --judge --product; unknown value (a basename or other frame spelling) -> incomplete with cause judgment and
  the door named; code never answers survived for it`
- `axes 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13: n/a -- the change reads one failed report row and routes its judgment;
  it meets no product build, surface, flow, source, delivery, stand, host, people, artifact language, size, check kind
  or project age`
- F1 (c) would add `axis 3: narrows -- probe_by_code keeps no pinned read`: a fork. S3 edits the axis 3 cell (map rule).

## 2. Facts (measured by Read/Grep unless cited)

- Grep `_pinned_read|pinned_frames|pinned_site` (repo minus `.claude/worktrees`): package code `red_sandbox.py` 4,
  `reporters.py` 2; no test calls them; `pinned_site` nowhere (control: `pinned_frames` found).
- `reason_matches` (:640-656) = `reporters.assertion_reason` + `bool(wanted) and wanted == seen`.
- `test_rows_record_cause_judgment_with_facts` (:161-183) stubs `PBC.reporters.assertion_site` with a READ site: a step
  that leaves a read site untouched keeps it green.
- No SIBLING_MAP row names the judgment door (case-insensitive Grep `judge_record|cause: judgment|judgment_facts|
  assertion_site`: only `assertion_site` :147, :153, the control).
- `proved_by` outside probe_by_code: `window_record.py:914-917` only; `proof_level.py` 0 (`reached` counts by level).
- Critic slice `references/slices/qa-code-critic/execution-lifecycle.md:16`: a product probe "replaces probe_by_code.py
  for that instance"; :23-25 name no door. Source `references/execution-lifecycle.md`, written by `contract_slices.py --write`.
- Census: `UNIT_NAME_RE` (`test_judgment_census.py:77`); a function with a refusal site is a unit (u3); `judge_record`
  has a row (:811); `_judged_record` (raises via `_judge_refusal(...)`) has none.
- Canon class (`slow_tests.json`): `test_red_sandbox_reports.py` 48.1, `test_red_sandbox_probe.py` 60.5,
  `test_gate_registry.py` 19.7, `test_contract_slices.py` 26.2, `test_judgment_census.py` 96.9.
  `test_probe_marker_judgment.py` not listed (control: the same Grep found `test_red_sandbox_probe.py`); keep row
  `test-layers.json` :4015. Quarantined: `test_reporters.py` :9730, `test_probe_one_road.py` :9370.
- Running (Lead `facts:`): RD1-39 (t-1365) edits `assertion_site`'s TRX branch; RD1-33 (t-1366) cuts word-reader nodes
  incl. `request_status`/`verify`/`probe` chain and `_judged_record` :7754, `_judge_cli` :7943 (digest t-1362 f-pv04..07,
  f-pv17..42). No t-1365/t-1366 file on disk (Glob 0; control: t-1362 found): `estimate`.

## 3. The design (on the recommendations; forks mark what would change)

### S1 (RD1-38): `reporters.pinned_site`

`reporters.pinned_site(site, row, reporter, clone_root, location, expected_reason, message, *, pytest_command=True,
runtime="") -> dict` (about 25 lines; raises nothing):
(1) `site` itself unless `site_unread` and status `failed`; (2) `file, _, line = location.rpartition(":")`,
`pinned_frames(file, line)` None -> `site` itself, no clause; (3) the second `assertion_site(..., frames=pinned,
skip_frames=[], frame_path="path")`; (4) that answer only if not unread, `location` equal, kind `assertion` and
`reason_agrees(message, expected_reason)`; (5) else a copy of `site` with `reason + "; " + <clause>`, `_pinned_read`'s
three clauses word for word (`check_in` substrings). `reason_agrees` takes `reason_matches`' body; `reason_matches`
delegates (readers unchanged).
Callers, right after the first `assertion_site` answer, before anything reads the site: `target_result` (pin =
`expected_location`, `expected_reason`, `entry["reason"]`, `**hint`; `_pinned_read` deleted; signature and
`_frame_grammar`'s place unchanged, `test_run_suite_reports.py:973`); `_judge_rows` :4363 (record `expected_location`,
`expected_reason`, `failure_problem(row)` message); the walk (F1 a) in `_walk_attempt` between :6280 and :6315 (per row,
each key of `group` with a token, source order, pin = the key's `<file>:<line>` and token; first non-unread wins).
`SIBLING_MAP.md:147` names `pinned_site`.

### S2 (RD1-37 producer): the product record says a judgment is owed

- `reporters.cut_failure_text(text)` + `FAILURE_TEXT_MAX`: `probe_by_code.cut_text` body moved (F6 a);
  `probe_by_code.cut_text = reporters.cut_failure_text` and `FAILURE_TEXT_MAX` re-exported, so its readers stay.
- `red_sandbox.judgment_owed(proof, result, base_row) -> bool` (pure): True only when `proof` is invalid, carries
  `site_unread`, is no `probe_defect`, `result["status"] == "failed"`, `base_row` status is `passed` (the author's green
  or the own baseline), and the row's failure message or text is non-empty.
- `probe()` keeps `rows_of[iid] = row` while binding (no new result field) and passes `rows_of`, `baseline_results`,
  `results`, the bindings attempt and `mutated_receipt` to `_write_product_records`.
- `_write_product_records`, for every record (cheap, no world): adds `task` (`task_root.name`) and `case`
  (`placed[iid]["case"]`). Only when `judgment_owed`: `cause: "judgment"`, `judgment_facts` and `pending_receipt`.
  - `judgment_facts` = `{"file", "line"` (from `expected_location`), `"expected_location", "expected_reason",
    "status", "message", "failure_text"` (cut), `"site_unread_reason", "frame": null, "location": null,
    "product_mutation": [{"path", "sha256"}]` (the record's `mutated_files`), `"rows": [{"test_id", "status",
    "message", "failure_text"}], "rows_cut": 0}`: the keys `_judge_input` reads, plus what the critic must see.
  - `pending_receipt` = the receipt body `write_sensitivity_receipts` would write for that target (extract
    `_receipt_body(target, result, binding, measured, probe_receipt, notes)`, used by both) without `scope`, `checks`,
    `receipt_hash`, plus `obligation_id`; `null` with `pending_receipt_why` when `manifest_bindings` raised.
- `probe()`'s incomplete branch: an owed instance's note says the code critic judges it with probe_by_code's `--judge`
  and `--product` and names the record path; it never spells the `JUDGE_DOOR` text (pinned :540). Instances with no
  judgment owed keep today's `tooling` note.

### S3 (RD1-37 door): `probe_by_code.py --judge <instance> --product`

- CLI: `--product` (store_true). `JUDGE_DOOR` stays byte for byte; `JUDGE_PRODUCT_DOOR = JUDGE_DOOR + " --product"`
  (one text, derived). `judge_record(..., check="", product=False)`; without `product` the function is unchanged.
- `_product_judged_record(task_root, root, instance_id)` (name misses `UNIT_NAME_RE`): `(path, record, entry)` or a
  `_judge_refusal`: absent record; `current_test_sha(entry, root) != record["test_file_sha256"]`;
  `not proof_level._mutated_files_hold(record, entry, root)`; not `incomplete`/`judgment`/facts; judgment present.
- Then the shared `_judge_input(verdict, quote, why, facts)` and `_demand_critic_dispatch(root, record, ...)`.
- `fires`: `red_sandbox.write_critic_receipt(task_root, record, judgment) -> (ref | None, why)` (raises nothing): the
  pending body + `proved_by: "critic"`, `judgment: {quote, by, at, facts_sha}`, `assertion_location` = the pinned
  location, `failure_kind: "assertion"`, `scope`/`checks` by `_receipt_scope(test_file, location)`, `receipt_hash`;
  written by `_write_receipt_file` (extracted from `write_sensitivity_receipts`, its naming and collision rule). A
  `whole_unlisted` ref is published by `publish_product_refs(task_root, repo, targets, refs, notes)` (extracted from
  `probe()` :1876-1933; `probe()` calls it too); a `one_check` ref is held back with the existing note. The record:
  `verdict: intended_failure`, `proved_by: critic`, `cause: null`, `judgment`, `receipt_ref` or `receipt_missing`.
- `other_failure`: `verdict: survived` (F3 a), `cause: null`, `judgment`. `cannot_judge`: stays `incomplete`/`judgment`,
  `judgment` written. The record is written last (`atomic_json`), after any receipt.
- Text: `references/execution-lifecycle.md` (the passage behind slice :23-25) names `--judge ... --product`; slices
  regenerated by `contract_slices.py --write`; the `probe()` docstring and note; the axis 3 cell of
  `design/architecture.md`; `SIBLING_MAP.md:153` adds "the code critic's `--judge` judges both probe records".

## 4. Edges (rule 11; each with its invariant)

| # | input | behaviour | invariant protected |
|---|---|---|---|
| P1 | first answer is a read location, `{}` or any non-unread dict | `pinned_site` returns it unchanged (same object) | a vetted grammar's read is never re-read; `{}` stays RD1-39's subject (positional: after the grammar, only on unread) |
| P2 | status `error`/`passed`/`skipped`/`not_run` | unchanged | an error is never an assertion proof |
| P3 | location empty, `None`, no `:<line>`, line `0`/`05`/`5x` | unchanged, no clause | nothing pinned, nothing confirmed |
| P4 | text names no pinned token (no stack, library frames, empty) | unread + "not found" clause | an unread site is never a location |
| P5 | token outside the clone, ambiguous tail, names no file | unread + clause | another tree's frame never proves the clone's test |
| P6 | pin absolute, `./`-prefixed or backslashed (critic t-1348 F1) | location differs -> unread | `verify`'s exact compare is never loosened; never `survived` |
| P7 | message not agreeing; `expected_reason` empty | unread + clause | a pinned read is a full proof or nothing |
| P8 | a row whose error problem precedes its failure problem | the guard compares the CALLER's `message` (red_sandbox: `entry["reason"]`) | the reason checked is the reason the consumer's proof compares; a read whose message `verify` rejects would be `survived` |
| P9 | probe_by_code: a confirmed pin | only `observed`/facts keys and the stored `failure_kind` change; verdict, cause, `proved_by` unchanged | the place never proves in probe_by_code |
| P10 | walk: a confirmed pin | it is a key of the same run, so `_earlier_check_at` gives None | a pinned read never makes a `stop` / `not_reached` |
| P11 | Python 3.10/3.11 | no backslash inside an f-string expression | the package compiles where it promises (t-1348 B1) |
| J1 | unread + failed + text + baseline passed | record `cause: judgment`, facts, `pending_receipt` (or `null` + why), `task`, `case` | an unread failure becomes the critic's, never code's |
| J2 | unread + baseline red/skipped/absent/not_run (`verify` gives `site_unread` before `baseline_status`, :726-733) | no `cause` | a red baseline never makes a red run the mutation's doing |
| J3 | unread + failed, message and text empty | no `cause`; the tooling note stays | no proof with no evidence |
| J4 | accepted / survived / probe_defect / not_executed | no `cause`, no facts, no pending receipt | only an unread site owes a judgment |
| J5 | `manifest_bindings` raises | `pending_receipt: null` + `pending_receipt_why` | a receipt is never built from facts not measured at probe time |
| J6 | failure text over `FAILURE_TEXT_MAX`, 1 MB single line, non-ASCII, CRLF | cut head+tail by the one cutter; stored as read | a quote beyond the cut is refused; folding is the door's one rule |
| J7 | several targets | one record each; `request_status` precedence unchanged (a survivor first) | the status never contradicts a record |
| J8 | product record write fails (OSError) | the existing note; the door later refuses "no product probe record" | no judgment of a record nobody wrote |
| J9 | `diagnostic()` | writes no product record (unchanged) | a diagnostic never owes a judgment |
| D1 | `--product`, no product record | refused, names the probe call | the judgment is of a probe that ran |
| D2 | record not `incomplete`+`judgment`+facts (incl. records written before S2), or judged already | refused | a written judgment is never rewritten; only an owed record is judged |
| D3 | test bytes now differ, or a mutated product file moved / unreadable | refused | a judgment measured on other bytes never counts |
| D4 | `--verdict` outside the three words (case, empty, `fire`) | refused before anything is written | the word set stays closed |
| D5 | quote empty (fires/other_failure), over 300 chars, not a substring after folding, beyond the cut | refused | the critic quotes what is stored |
| D6 | `cannot_judge` without `--why` | refused | the person's door needs the reason |
| D7 | dispatch not the open S5 critic covering `case` (incl. record with no `task`/`case`) | refused | an author never writes a `fires` on its own test |
| D8 | `--product` with `--check`; with `--s6-close` | refused (`--s6-close` first, unchanged) | a product record has no checks; S6 has no critic |
| D9 | `fires`, pending body present, bytes hold | receipt (`proved_by: critic`, judgment inside the hash, pinned location), record `intended_failure`; `whole_unlisted` published, `one_check` held back | the critic's road ends in a counted receipt; a one-check receipt never stands for the whole test |
| D10 | `fires`, `pending_receipt: null` | record `intended_failure` + judgment + `receipt_missing` why, no receipt | no receipt without probe-time binding facts |
| D11 | `fires`, receipt name exists with other bytes | refused, nothing written | an immutable receipt is never overwritten |
| D12 | `other_failure` | `survived`, judgment, no receipt; a repeat is blocked (`already_probed` item 3) until a person's word | a survivor is the critic's word, never code's |
| D13 | `cannot_judge` | stays `incomplete`/`judgment`, judgment written | an unknown never becomes a pass |
| D14 | manifest publication fails | receipt stays, note (as `probe()`), record already `intended_failure` | a published level always has its receipt on disk |
| D15 | no `--product` | byte for byte today's door | the live door is untouched |

Temporal: S2 creates `cause`/`judgment_facts`/`pending_receipt` on product records. Before S2 no product record owes
anything and `--product` (absent before S3) does not exist; after S2 and before S3, owed records are only read by the
probe's note (the critic cannot act yet: S2 and S3 land in one wave, F7). Old records: D2. Old receipts: untouched.
Conflicting pairs: "the place never proves in probe_by_code" vs "one road for the pinned read" -> P9/P10 (the read is a
fact there). "Repeat-blocking `survived`" vs "a critic's word" -> D12 (the person's word passes, as for any survivor).

## 5. Reused functions in a more consequential role

- `pinned_site` in probe_by_code (a site read becomes a judgment FACT there). Allowed error direction: toward
  `site_unread` (nothing changes). Adversarial inputs that must stay unread or change nothing: P3-P7, a pin of a key with
  no token, a joint run whose message agrees with the token of a key other than the pinned one (each key pins its own
  token), a 1 MB line (linear read, t-1348 measured 0.07-0.17 s; no timing asserted).
- `_judge_input` and `_demand_critic_dispatch` on a product record (advice -> a door that writes a receipt). They err
  toward refusal. Adversarial: D4-D8, a quote equal to a substring of `expected_reason` but not of the stored texts
  (refused: `expected_reason` is not a quoted source), a `rows` item injected with a non-dict (skipped by `_judge_input`).
- `_mutated_files_hold` as the door's product-bytes check: errs toward "does not hold" (empty shas, unreadable file).

## 6. Builder cards (R11-f; the Lead prints the header lines with `python -B tools/dispatch_new.py`)

### S1 -- RD1-38

given: this card §0-§5 (symbols there); review `C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1348-rd1-24-rd1-28-code.md` (B1, F1, RD24-a).
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/reporters.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-38-pinned-site-reader.md
non-goals: the judgment door and product records (S2, S3); basename/other frame spellings; `assertion_site`'s existing
branches (RD1-39 owns the TRX one); any verdict word; `test_reporters.py` (quarantined).
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-rd1-38.md` (diff summary, witness verbatim, test lines
written / not written, `not run locally` lines).
edges: §4 P1-P11 inline; the positional invariant P1 and the safety rule P7/P8 quoted verbatim.
DoD:
- `pinned_site` and `reason_agrees` exist as §3 S1; `_pinned_read` is gone; `target_result`'s signature and
  `_frame_grammar`'s place unchanged; both probe_by_code sites call `pinned_site` before the site is judged;
- the AR-13 Grep of §1 gives hits in `reporters.py` only, with its control;
- `site_unread_is_incomplete`, `frames_from_the_table`, `junit_runner_that_is_not_pytest_is_incomplete` pass with only
  the P8 row added;
- `python -B -c "import ast,sys;[ast.parse(open(p,encoding='utf-8').read(),feature_version=(3,10)) for p in sys.argv[1:]]" <the three scripts>` exits 0 (P11);
- SIBLING_MAP :147 names `pinned_site`; the changelog fragment exists.
Verification run: `python -m pytest <worktree>/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py -q`
and the narrow call `python -B -c "import sys; sys.path[:0]=[r'<worktree>/ai-packages/qa-factory/scripts/tests', r'<worktree>/ai-packages/qa-factory/scripts']; import test_red_sandbox_reports as R; R.site_unread_is_incomplete(); R.frames_from_the_table(); R.junit_runner_that_is_not_pytest_is_incomplete(); R.finish('rd1-38')"`,
`python -B ai-packages/qa-factory/scripts/selftest.py --lang`, and the line `not run locally: test_red_sandbox_reports.py,
test_red_sandbox_probe.py, test_probe_by_code_records.py, canon judges`.
red-before: none -- a move with no defect line (P8 is a guard row, green before and after).
test lines (strongest first):
1. `test: scripts/tests/test_probe_marker_judgment.py::test_rows_record_cause_judgment_with_facts (variant: the real
   assertion_site with a grammar that refuses; a failed row whose text names the record's expected_location path-form
   and whose message is the token -> the stored observed carries that location; the same row with another message ->
   observed keeps site_unread) | expected from: §3 S1, §4 P7, P9; RD24-a; SIBLING_MAP :147`
2. `test: scripts/tests/test_red_sandbox_reports.py::site_unread_is_incomplete (one row P8: the error problem's message
   is the pinned one, the failure problem's is not -> unread, verify incomplete, never survived) | expected from: §4 P8`
Budget: about 30 product lines (+25 reporters, -20 +6 red_sandbox, +15 probe_by_code, map and changelog) against about
20 test lines.
siblings: SIBLING_MAP :147 (Report-row readers: the read enters the reader); :153; axis 34 (both consumers, one road).
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-37-38-probe-site-door-card.md

### S2 -- RD1-37 producer

given: this card (symbols in §0, §3 S2); S1 merged; `probe_by_code.py::judgment_facts` (the shape to mirror).
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/reporters.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-37-product-judgment-owed.md
non-goals: the door (S3); window/acceptance readers of product records (F5); any receipt written by a judgment; a
product verdict word; `red_sandbox` importing `probe_by_code` (forbidden, :161).
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-rd1-37-producer.md`.
edges: §4 J1-J9 inline; J2's precedence fact (`verify` :726-733) quoted.
DoD:
- `judgment_owed`, `cut_failure_text`, `_receipt_body` exist as §3 S2; `write_sensitivity_receipts` writes byte-identical
  receipts (the C4 receipt keys unchanged);
- the product record keys of §3 S2 appear only on J1; `task`/`case` on every record;
- the owed note names `--judge` and `--product` and holds no `--judge "<instance>"` text;
- `test_judgment_facts_shape_and_cut` passes unedited (the cutter moved, its readers kept).
Verification run: `python -m pytest <worktree>/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py -q`
and `python -B -c "import sys; sys.path[:0]=[r'<worktree>/ai-packages/qa-factory/scripts/tests', r'<worktree>/ai-packages/qa-factory/scripts']; import test_red_sandbox_reports as R; R.request_status_of_proofs(); R.junit_runner_that_is_not_pytest_is_incomplete(); R.a_baseline_that_is_not_a_pass_is_incomplete(); R.site_unread_is_incomplete(); R.finish('rd1-37a')"`,
`--lang`, and `not run locally: test_red_sandbox_reports.py, test_red_sandbox_probe.py, test_gate_registry.py, canon judges`.
red-before: none -- new behaviour, no defect line.
test lines (strongest first):
1. `test: scripts/tests/test_red_sandbox_reports.py::junit_runner_that_is_not_pytest_is_incomplete (added checks: the
   record says cause judgment, its judgment_facts message/failure_text hold the runner's text, task and case are set,
   pending_receipt is present; the answer's note names --product) | expected from: §3 S2, J1; pile row RD1-37`
2. `test: scripts/tests/test_red_sandbox_reports.py::request_status_of_proofs (rows over judgment_owed: J1 owed; J2 a
   skipped baseline beside an unread site; J3 empty texts; J4 a survivor and an accepted proof -> not owed) | expected
   from: §4 J1-J4`
Budget: about 55 product lines against about 30 test lines.
siblings: SIBLING_MAP :153 (a factory gap gives `incomplete`); axis 34 (the same owed state as probe_by_code's E15).
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-37-38-probe-site-door-card.md

### S3 -- RD1-37 door

given: this card (symbols in §0, §3 S3); S2 merged; `test_probe_marker_judgment.py::world`, `::judge_it`, `::refusal`.
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/execution-lifecycle.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/execution-lifecycle.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-37-product-judge-door.md
non-goals: a second judge or door text; `JUDGE_DOOR`'s bytes; window/acceptance readers (F5, node RD1-37c);
basename/other frame reads; `agents/qa-code-critic.md` (the slice carries the door); a new product verdict word (F3).
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-rd1-37-door.md`.
edges: §4 D1-D15 inline, with §5's adversarial list.
DoD:
- `--product` and the product branch as §3 S3; without `--product` the door is byte for byte today's (D15);
- `test_judgment_written_only_by_probe_by_code` and `test_judge_door_is_one_constant` pass unedited;
- receipts are written only by `red_sandbox._write_receipt_file`; `probe()`'s publication goes through
  `publish_product_refs` (one road for both writers);
- `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `contract_slices.py --write` leaves the
  slice equal to its source passage; the axis 3 cell and SIBLING_MAP :153 are edited; census rows added if a unit appears.
Verification run: `python -m pytest <worktree>/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py -q`
and `python -B -c "import sys; sys.path[:0]=[r'<worktree>/ai-packages/qa-factory/scripts/tests', r'<worktree>/ai-packages/qa-factory/scripts']; import test_red_sandbox_probe as P; P.no_row_language_reaches_a_counted_receipt(); P.finish('rd1-37b')"`,
`--lang`, and `not run locally: test_red_sandbox_probe.py, test_red_sandbox_reports.py, test_gate_registry.py,
test_contract_slices.py, test_judgment_census.py, canon judges`.
red-before: none -- new door.
test lines (strongest first):
1. `test: scripts/tests/test_red_sandbox_probe.py::no_row_language_reaches_a_counted_receipt (second scenario of the
   same world: the runner writes a basename frame `at tests.Calc.test_add(Calc.kt:<line>)` -> incomplete, record cause
   judgment; judge_record(..., product=True) fires with a quote of the stored text -> record intended_failure /
   proved_by critic, receipt proved_by critic with judgment.quote, whole_unlisted, reached counts it through the
   published ref) | expected from: §3 S3, D9; pile row RD1-37; F-O2`
2. `test: scripts/tests/test_probe_marker_judgment.py::test_judge_refusals_name_the_door (product rows over a
   product-record world: D1, D2, D3, D4, D5 not a substring, D8 --check; each refuses and the record bytes are
   unchanged) | expected from: §4 D1-D8`
3. `test: scripts/tests/test_probe_marker_judgment.py::test_judge_other_failure_is_wrong_location (product variant:
   other_failure -> survived, cannot_judge -> incomplete with the judgment, no receipt in either) | expected from: D12,
   D13, F3`
Budget: about 90 product lines (door 40, receipt writer and two extractions 40, CLI and texts 10) against about 70 test
lines; line 3 drops first.
siblings: axis 34 (one door for both probe tools); SIBLING_MAP :153; AR-14 (one writer of `judgment`).
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-37-38-probe-site-door-card.md

### Named residual (F5 b; not cut here: rule 6)

RD1-37c -- the window, acceptance and delivery see a product record that owes or failed a judgment.
owns: `scripts/proof_level.py` (`probe_record_state` and the three readers built on it read the product record when
the live one is absent), `scripts/window_record.py`, `scripts/tests/test_probe_readers.py`.
test: `test_probe_readers.py` (rows: product owed -> unjudged; product cannot_judge -> the person's door; a live record
present -> read as today).

## 7. Readers of every touched file (rule 7)

The `owns_readers.py` block is NOT attached. All rows below are hand Greps (`estimate` for the block). The Lead runs:
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/reporters.py ai-packages/qa-factory/scripts/red_sandbox.py ai-packages/qa-factory/scripts/probe_by_code.py ai-packages/qa-factory/references/execution-lifecycle.md ai-packages/qa-factory/design/architecture.md docs/SIBLING_MAP.md --names pinned_site reason_agrees cut_failure_text judgment_owed _write_product_records write_sensitivity_receipts judge_record`

| touched | readers (Grep, count) | answer |
|---|---|---|
| `red_sandbox._pinned_read` | `red_sandbox.py` only (4, incl. docstrings) | removed in S1 |
| `red_sandbox.reason_matches` | `window_record`, 3 test files (§2) | unchanged (delegates) |
| `red_sandbox.target_result` | `red_sandbox.py:1771`, `:2203`; 17 test calls (RD1-24 card §7) | unchanged signature; behaviour equal |
| `red_sandbox.write_sensitivity_receipts` | `red_sandbox.py` 3; `test_identity_proof_contract` 2, `test_probe_readers` 1, `test_probe_every_check` 1, `test_red_sandbox_setup` 1, `test_red_sandbox_probe` 1, `test_s5_precheck` 2 | unchanged output (S2 extracts `_receipt_body`, S3 `_write_receipt_file`) |
| product record (`work/probes/product/`) | `proof_level.py` 6 (`probe_fired`, `proof_identity`, `_mutated_files_hold`, repeat items 3-4), `driver_stage_s6.py:644`, `handoff_check.py:505-508` (names only), tests 7 files | new keys only; existing keys unchanged; S3 changes `verdict` only through the critic's word |
| `red_sandbox.py` source slice | `test_run_suite_reports.py:973` (`def bind_row`..`def _frame_grammar`) | unchanged (all edits after `_frame_grammar` or outside the span) |
| `reporters.py` (module) | 16 importers (RD1-24 card §7) | additions only; `assertion_site` untouched by this card (RD1-39 edits its TRX branch) |
| `probe_by_code.cut_text`/`FAILURE_TEXT_MAX` | `probe_by_code.py` 13, `test_probe_marker_judgment.py` 11 | unchanged names (alias) in S2 |
| `probe_by_code.judge_record`/`JUDGE_DOOR` | `window_record.py` 7, `test_code_critic_probe_rule.py` 4, `test_probe_not_proved.py` 5, `test_probe_marker_judgment.py` 23, `test_probe_every_check.py` 3 (`manual_evidence.py` 2 are `rejudge_record`, homonym) | keyword default keeps every call; `JUDGE_DOOR` bytes unchanged |
| `probe_by_code._judged_record`, `_judge_cli` | RD1-33's node set (digest f-pv17..42) | changes in S3; order with RD1-33 (F7) |
| `references/execution-lifecycle.md` | its slice, `contract_slices.py`, `test_contract_slices.py`, release fingerprint | slice regenerated in S3 |
| `design/architecture.md` axis 3 | designers, critics, the Lead; index generator reads `**AR-n` openers only | cell changes in S3 |
| `docs/SIBLING_MAP.md` :147, :153 | designer/critic/Lead | rows change in S1/S3 |
| `tools/`, `.githooks/`, `.claude/` | Grep `red_sandbox\|reporters\.py\|probe_by_code` over `tools/`: 1 file (`tools/fixtures/dispatch_manifest/K8.txt`, RD1-24 card §7) | unchanged |

## 8. Test cost (docs/TESTING.md)

S1: rows in existing tables, no world. S2: checks on one existing world + rows in one pure table. S3: ONE scenario
in the C4 world (+~13 s on `test_red_sandbox_probe.py`, 60.5 s, ceiling 600; t-1348 measured 13.3 s) + rows over
`world()` (tmp dirs, no run). No new file. External input (the report): magnitude/encoding J6, empty J3/P4, broken
pinned upstream (RD1-24 E2); limits only the existing `FAILURE_TEXT_MAX`/`JUDGE_QUOTE_MAX`, whose AT/BEYOND rows
exist. `test_probe_by_code*.py` untouched (PC4-19).

## 9. Forks (returned; not decided)

- **F1 -- what probe_by_code does with `pinned_site`** (RD1-38's "axis 34").
  (a) Both sites call it with the record's own pin (location, the marker as `expected_reason`, the row's message):
  one road. Its honest yield: a pin confirms only when the message agrees with the token, so it adds `location`/
  `frame` facts and changes no verdict (P9, P10); about 15 lines and 1 test row. (b) Call it without the reason guard
  (a fact read): more facts for the critic, but one function with two behaviours, and a None reason in red_sandbox
  would then read without the guard. (c) Do not call it; SIBLING_MAP says the pinned read is red_sandbox's proof road.
  A `narrows` line; it costs nothing in verdicts. **Rec (a)** (rule 6). Covering it costs the S1 walk hook.
- **F2 -- the shape of a critic's product receipt.** (a) The pending body + `proved_by: critic` + `judgment {quote, by,
  at, facts_sha}` inside the hash, `assertion_location` = the pin, level `catches_broken_product`. (b) The same at level
  `live` (a critic's word ranks below a mechanical product proof). (c) No receipt: `fires` only flips the record.
  **Rec (a):** the product was really broken and the test really failed, and the critic judges only which assertion
  fired, as probe_by_code's critic receipt keeps its tool's level. `reached` reads no `proved_by`, and the window shows it
  (`window_record.py:917`).
- **F3 -- the product word for `other_failure`.** (a) `survived`: the product vocabulary's survivor, with no new word,
  and the RD1-28 registry row stays as it is. It blocks a repeat until a person's word (D12). (b) A new product word
  `wrong_location`: a `probe_verdict` registry change, plus every product-word reader (RD1-33's list). **Rec (a).**
- **F4 -- how the door picks the product record.** (a) An explicit `--product` flag. (b) Auto-select: the live record
  if it owes, else the product record. (b) can write `fires` on the wrong probe when a quote stands in both texts.
  **Rec (a).**
- **F5 -- window/acceptance readers of a product record that owes or failed a judgment.** (a) None in this card. Today
  a product `incomplete` is no window state, and the probe answer and slice name the door. But the critic's slice :16
  says a product probe replaces probe_by_code for the instance, so an unjudged product probe can leave the instance
  "not probed" with no word of why (`estimate`). (b) The named node RD1-37c (§6), one road with probe_by_code's
  `probe_owes_judgment` / `cannot_judge_facts` and the person's `probe not proved` door. **Rec (b)** (rule 6). It costs
  `proof_level.py`, `window_record.py` and one reader table; the window gates read it.
- **F6 -- who produces the product facts and where the cutter lives** (`red_sandbox` may not import `probe_by_code`).
  (a) Move `cut_text` into `reporters` (`cut_failure_text`), with probe_by_code aliasing it; red_sandbox writes the facts
  keys `_judge_input` reads. (b) red_sandbox caps the text itself: a second cutter (AR-13). (c) The door builds the facts
  at judge time from raw text the record stores. The record then still needs a cap, and the critic reads uncut text
  before judging. **Rec (a).**
- **F7 -- order with RD1-39 and RD1-33.** S1 touches no word reader and no `assertion_site` branch, so it can run beside
  both. S2 and S3 edit `probe()`'s status chain area and `_judged_record`/`_judge_cli`, which RD1-33's nodes also cut.
  **Rec:** S1 now; S2 and S3 in one wave, after RD1-33's nodes on those functions merge, or before them with RD1-33
  rebasing (the Lead's call). Once RD1-39 lands, frameless TRX failures also reach J1. That is intended: one owed state.

## 10. Small choices closed

C1 `pinned_site` returns the final site dict (one-line callers). C2 the guard takes the caller's message (P8). C3 no
second location regex (`rpartition` + `pinned_frames`' line check). C4 `reason_matches` delegates to
`reporters.reason_agrees`. C5 walk pins per key in source order, keys with a token only. C6 `rows_of` stays local to
`probe()`. C7 `JUDGE_PRODUCT_DOOR` derived from `JUDGE_DOOR`; red_sandbox's note names flags only. C8 the door reuses
`current_test_sha` and `_mutated_files_hold`. C9 new names miss `UNIT_NAME_RE`; refusals via `_judge_refusal`; the receipt
writer raises nothing. C10 the door writes the record last (D11, D14). C11 one `changelog.d/` fragment per step.

## 11. Noticed, not widened

- Multi-target: accepted targets beside an unread one get no receipt (:849 needs the whole request `accepted`); after S3
  only the judged one does. Pre-existing; a fork for the Lead if wanted.
- `agents/qa-code-critic.md:78` spells the `--check` door by hand (the pin :540 scans `scripts/` only). Outside this card.

## 12. Reading trail

The RD1-24 card (whole). Critic t-1348 (whole). Pile rows :61, :65-67 (`batch-1-phase-2.md`). Digest t-1362 (whole).
`red_sandbox.py` :78-85, :600-656, :659-743, :747-788, :829-903, :1180-1263, :1505-1579, :1760-1938 + Greps (defs,
`site_unread`, `reason_matches`, `_LOCATION_RE`). `reporters.py` :300-509 + defs Grep. `probe_by_code.py` :52-121,
:3130-3430, :3481-3518, :4327-4386, :4600-4629, :6140-6216, :6270-6334, :7733-7932 + Greps (`assertion_site(`,
`JUDGE_DOOR`, `proved_by`, judge defs, imports, `cut_text`). `proof_level.py` :595-598, :764-793, :1134-1263, :1303-1324,
:1425-1484 + Greps. `test_probe_marker_judgment.py` :1-112, :505-541 + defs Grep. `test_red_sandbox_probe.py`
:1015-1089. `test_red_sandbox_reports.py` :1103-1153 + defs Grep. `test-layers.json` :1-40, keep and quarantine rows
by Grep. `slow_tests.json` :1-12 + Greps. `TESTING.md` :75-164, :213-250. `architecture.md` :33-128, :173-213,
:274-279, :316-321. `SIBLING_MAP.md` :147, :153, :588-601 + Greps. The critic slice
`execution-lifecycle.md` :15-30. `agents/qa-code-critic.md` Grep. `judgment-census.json` Grep, `test_judgment_census.py`
:60-80, :218-240. Grep counts are quoted in §2 and §7. Each negative (no `pinned_site`, no judgment row in SIBLING_MAP,
`test_probe_marker_judgment.py` not slow, no t-1365/t-1366 files) is paired with a same-shape positive control
(`pinned_frames`, `assertion_site`, `test_red_sandbox_probe.py`, t-1362). No shell: nothing was run. The owns_readers
block and the RD1-33/RD1-39 files are `estimate` (§7, §2).

## Lead decisions (18.11, Lead 501cb4e0; designer t-1367 accepted)

- F1: (a). Both probe_by_code sites call `pinned_site` with the record's own pin and its reason guard; it adds location/frame
  facts and changes no verdict. Invariant: a pin confirms only when the message agrees with the token (P9, P10).
- F2: (a). The critic's product receipt keeps level `catches_broken_product` with `proved_by: critic` and `judgment` inside the hash.
- F3: (a). `other_failure` on a product record reads `survived`; no new word, the RD1-28 row unchanged.
- F4: (a). An explicit `--product` flag; no auto-select.
- F5: (b). Residual node RD1-37c is filed in the rules-debt pile as RD1-41 (owns and test as in "Named residual").
- F6: (a). `cut_text` moves into `reporters` as `cut_failure_text`; probe_by_code aliases it; red_sandbox writes the facts keys.
- F7 (order): S1 starts only after RD1-39 merges (both write `reporters.py`). RD1-39 round 2 keeps the TRX road: a failed TRX row
  with no frame that names the pinned location inside the clone with the pinned message reads `accepted` through `_pinned_read`
  (critic t-1370 R1, row D2). S1 moves that read into `pinned_site` and keeps the D2 row green (both worlds: before S1 the road
  lives in `red_sandbox._pinned_read`; after S1 it lives in `reporters.pinned_site`, same verdicts). S2 and S3 run as one wave
  BEFORE RD1-33 S2-S4; RD1-33 rebases on them (its I2).
