# Critic on plan — T1r-sites (t-739), draft `20261114-told-before-work-t1r-sites-spec.md` with §6a

Critic: Opus, one pass, no code edited. Read base: worktree `tbw-t1r` at 7ed7f10 + the running fix round's uncommitted edits
(`git status`: only `stage_joints.py`, `contract_slices.py`, `stage-joints.json`, `judgment-census.json` and two test files dirty;
`execution_request.py`, `run_suite.py`, `red_sandbox.py`, `detector_verdict.py` are clean, so their line numbers below are stable).

**Verdict: fit_with_fixes — NOT dispatchable as written.** Three blocking findings; each closes with a binding amendment below
(B1 also needs one Lead choice, with a recommendation). The approach (literal sites through `refusal()`, an additive `told` key,
two sequential nodes, markers only on proved rows) is sound. The headline is not: as drafted, qa-code-critic, the only role the node
is meant to bring under H, gets its ER/RS rows taken off its page while the roads it actually uses print no `told`. So those rows
would be told nowhere.

---

## Blocking findings

### B1. The transport covers `run_suite.py`'s own printers only. Code-critic's and the analyst's roads drop `told`, so their call-told rows are told nowhere (AR-10, FR-38, P31, rule 15)

- **Surface:** the printers that hand an ER/RS refusal to a role session. The draft (§1 AR-18, §4.1 P-5, S13, E8) treats
  `red_sandbox.py` and `execution_scheduler.py` as "readers of the JSON lines, untouched". They are not passive readers. They are
  the printers the role sees:
  - `red_sandbox.py:1249-1284` `_run_mine` runs `run_suite.py --mine --purpose red_probe --sandbox-root …` as a subprocess.
    `:1687-1692` (probe) and `:2174-2177` (diagnostic) turn a refusal into a note that keeps only `status`, `error` and `hint`.
    `told` is dropped. `red_sandbox.py:1384` also calls `ER.fresh_evidence` in-process.
  - `probe_by_code.py:2929` calls `build_mine_request(...)` in-process (`purpose="red_probe"`, `s6_close=`). The `MineRefusal`
    never passes through `run_suite.py`.
  - `import_test_receipt.py:260` calls `validate_request(...)` in-process: the 10 request-file rows, automator road.
  - `execution_scheduler.py:271` calls `validate_request` in-process. `run_suite.py:2822-2824` prints `invalid_schedule` with
    `str(exc)`, and `execution_scheduler.py:527-528` keeps only `error` of a child's `run_refused`.
- **Who uses which road** (agents files): qa-code-critic uses "`probe_by_code.py` and `red_sandbox.py --probe`"
  (`agents/qa-code-critic.md:68`). Its only direct `run_suite.py` call is `--request --detail` (`:69`), and that hits
  `run_suite:detail_target`, an automator-only row. qa-failure-analyst uses `run_suite.py --request` plus `red_sandbox.py
  --diagnostic` (`qa-failure-analyst.md:73`). qa-automator uses `run_suite.py --mine` plus `import_test_receipt.py`
  (`qa-automator.md:68`).
- **Failure scenario:** after S-2, `execution_request:sandbox` (producers: code-critic and analyst only; the refusal is reachable
  only with `--sandbox-root`, i.e. through `red_sandbox`) is call-told and gone from both pages. The code-critic runs
  `red_sandbox.py --probe` with a profile `cwd` outside the project. It reads `baseline run: run_suite.py refused it
  (mine_refused): the run directory … is outside the project root …`, with no `expected:` and no row sentence. So the requirement
  is on no page and in no refusal the role reads. The same holds for all 14 ER rows and for `run_suite:begin` for code-critic.
  This is the defect the draft names itself in Q1.2 ("counted told at the call and told NOWHERE"), reproduced one hop further out.
- **Why no gate catches it:** `call_told` (`stage_joints.py:751-766`) ANDs "every producer entry of THIS role carries the marker"
  with `_is_sited(check, real_sited())`, a GLOBAL literal anywhere in the package. The second condition holds on one carrier (the
  `run_suite` printer road) while the first is about a role whose road is a different carrier. That is a pair detector not
  scoped to its own carrier (critic rule 15). F-4's proof row `T1rs/told/<id>` provokes the refusal only through `run_suite.py`
  (§4.1 test table), so it proves the automator/runner road and nothing for code-critic or the analyst.
- **P31:** one road (the call road) reaches the automator and the runner, but the shared mechanism does not reach code-critic or
  the analyst. That is an exception for those roles with no data row and no owner's word (critic rule 19, axis 34).
- **Effect on §3:** with the roads as they are, none of code-critic's 16 ER/RS rows may leave its page. Its U stays 74,327, or
  +5,927 over H. **The node then brings no STOP role under H.**

**Binding amendment B1 (Lead chooses (a) or (b); recommend (a)):**
> "(a) S-1 owns every printer that hands a relabelled ER/RS refusal to a role session, and each adds the same `told` projection
> through `detector_verdict.told_fields`. The minimum set: `red_sandbox.py` (`_run_mine` callers' refusal notes at the probe and
> diagnostic branches: append `spoken`-form `expected:`/`door:` lines of each `told` entry after the note, or carry `told` in
> the result object), `probe_by_code.py` (the handler of a `MineRefusal`/`RequestError` from `build_mine_request`),
> `import_test_receipt.py` (the handler of `validate_request`'s `RequestError`), `run_suite.py` `invalid_schedule` and
> `execution_scheduler._group_row`'s `run_refused` branch (carry `told`). P-7 adds: the grep of every `except` that catches
> `RequestError`/`MineRefusal`/`Exception` around `validate_request`, `build_mine_request`, `fresh_evidence` and
> `JobStore.*` in `scripts/*.py`, each with 'carries told' or the reason it reaches no role (e.g. `driver_stage_s6.py:543`,
> code). `T1rs/told/<id>` gains a column `road` (`run_suite`, `red_sandbox`, `probe_by_code`, `import_test_receipt`,
> `schedule`). S-2's call marker on a producer entry for role R is set only when the row is proved on EVERY road R uses (the
> road list per role is a data constant in the test, read from the agents files' tool lines). An unproved road splits the
> producer entry and keeps the page for that role. (b) Leave S-1's printers as drafted, and S-2 marks only the roles whose
> roads are all `run_suite.py` (automator for the `--mine` and RS rows, runner). Code-critic and analyst keep every ER/RS row
> on the page, and §3's headline becomes 'no STOP role closed; automator −≈7.2K'."
> 
> Plus, in either case: "§1, E8 and S13 drop 'readers, untouched' for `red_sandbox.py` / `execution_scheduler.py`. They are
> printers to a role (AR-18: one output shape per refusal on every road)."

Cost of (a): about 4 more owned files. `probe_by_code.py` and `red_sandbox.py` are large and appear in many pile files (see
"needed beyond the manifest"), so the Lead's overlap check must run per function (D-0048).

### B2. S-1's DoD skips the one file that holds all of S-1's acceptance rows. S-2's DoD runs a slow file. The witness rule is internally inconsistent

- `slow_tests.json:5` sets `slow_over_s: 10`. `:36` lists `test_execution_request.py: 20.9` and `:125` lists
  `test_stage_joints.py: 67.6`.
- S-1's DoD and command 1 (spec §4.1 lines 237, 308) say "every non-slow file it lists, each alone; a slow … file … judged by the
  batch canon". Yet every S-1 test row (`T1rs/told/*`, `error-bytes`, `one-json-line`, `no-launch`, `unreadable-row`; line 300ff)
  lives in `test_execution_request.py`. So the S-1 witness would carry none of S-1's acceptance keys ("every `T1rs/*` row green",
  line 313). S-2 then pins `T1rs/marked-iff-tested` (F-4) to an S-1 list that no local run produced.
- S-2's DoD (line 340) runs `test_stage_joints.py` "ONCE, last". But PROJECT.md «Как принимается изменение пакета» p. 2 says a
  slow file (`SLOW_TESTS`) "локально не запускается и не ждётся". The two nodes take opposite readings of one rule, and
  PROJECT.md p. 2 itself pairs "до минуты каждый" with SLOW_TESTS, which a 20.9 s file falls under.

**Binding amendment B2:**
> "S-1 DoD: `python -B ai-packages/qa-factory/scripts/tests/test_execution_request.py` is run ONCE as this node's own narrow
> witness (the owned module's test file, under a minute; named here because F-4 makes its result the input of S-2), its verbatim
> summary in the report. S-2 DoD: `test_stage_joints.py` is NOT run locally; it is named 'judged by the batch canon', and S-2's
> own rows go to the fast `test_contract_slices.py` where they are data joints." If the Lead reads PROJECT.md p. 2 as forbidding
> any SLOW_TESTS file locally, then: "the `T1rs/told` joint rows move to an in-process table in `test_detector_verdict.py` (fast,
> keep), calling `validate_request` / `build_mine_request` / the road printers directly". Either way, ONE reading for both nodes.

### B3. `run_suite:recover` sited inside `JobStore.read` prints the recover sentence on calls that are not `--recover` (E6 broken by its own site table)

- The site table (line 284) maps `run_suite:recover` to `JobStore.read 403` ("corrupt persisted job for idempotency key").
  `JobStore.read` is a shared helper (`execution_request.py:396-403`). Its callers are `begin` (`:413`, `:434`), `recover`
  (`:452`), `last_run_of` (`:496`, the `--detail` road) and `run_suite.main:2884` (the `--request` lookup of an existing key).
- **Failure scenario:** an automator runs `run_suite.py --request r.json` and the job file under its key is corrupt. It gets
  `invalid_request` with `told[0].expected` = "`--recover <KEY> --task <T>` names the idempotency key of a job recorded…". That is
  the sentence of a command it did not call. This breaks the draft's own E6 invariant: "a refusal never prints a sentence that is
  not its own".

**Binding amendment B3:**
> "`JobStore.read`'s corrupt-file raise stays a bare string. The id is attached at the CALLER: `recover` wraps it as
> `run_suite:recover`; `begin` (both reads) and the `run_suite.main` existing-key lookup wrap it as `run_suite:begin` (its door
> already names `--recover` for an unreadable claim); `last_run_of` leaves it bare (E6). Rule for the builder: a site inside a
> helper with more than one caller gets no literal id; the id goes on each caller."

Class walk (rule 14, surface "an id literal placed in a shared helper"): `_command_from_profile` (profile_command) and `_profile_for`
(profile) are called by `build_mine_request` and by `probe_by_code` through it. Both callers ask the same requirement, so they are
not affected. `reference_target_problem` is wrapped at its two callers in the draft already, which is correct. `sandbox_run_directory`
has one caller (`:3452`), so it is not affected. `_place_rows` is called twice from one function with the same requirement, so it is
not affected.

---

## Answers per key

### 1. FACTS (§0)

| fact | verdict | trail |
|---|---|---|
| S1-S4 "sited" | true as written | `stage_joints.py:291-342` (`check_ids` pre-filter `:304-306`, `sited_ids :336-337`, `_is_sited :340-342`), `call_told :751-766`, `_call_leg :769-786` |
| S5 pre-filter | true | `:304-306` |
| S6/S7 no literal ids | not re-run; consistent with the T1r-pages witness `unsited 150` (report §10) and with `call_told_families` having no effect (report §3) | — |
| S10 `refusal()` / `spoken()` | true; `Record` is a `str` subclass, so `"; ".join` of Records and `str(exc)` stay byte-identical | `detector_verdict.py:94-191` |
| S11 `validate_request` collects then joins | true | grep: 49 `errors.append` lines 126-352, raise 355 |
| S12 printers | true, with additions: `run_suite.py:2972` (`invalid_request` from `store.begin` inside the launch path) is in no list, and `:2823` `invalid_schedule` is missing too (B1) | grep `"status": "(invalid_request|mine_refused|run_refused|invalid_recovery)"` |
| S13 one reader | **false**: `red_sandbox.py` reads the line AND re-prints a reduced form to the role (B1); `execution_scheduler._child_answer` is a second reader (`:388-408`, `:527-530`) | reads |
| S14 "every refusal before … the stand lease" | **false in letter**: the race-path `run_suite:begin` refusals (`execution_request.py:436, 438`, and `:417` on a race) fire at `run_suite.py:2970-2972`, INSIDE `with hold_stand(...)` (`:2967`), which may first wait up to `run.stand_wait_s` (default 1800 s, `:1484`). The lease is released on exit, so nothing irreversible happens. Separately, the `--mine` road writes the request file (`run_suite.py:2073`) BEFORE `validate_request` (`:2885`), so a validate refusal of a mine-built request leaves that file behind. "No row spends a run" stays true | reads |
| S15 `--template request` | true | `run_suite.py:14, 2529-2539, 2745` |
| S16 data | true: wording "{n} checks of your commands are told …", ratchet `unsited 150` | python read of `stage-joints.json` |
| S17 producers | true for all 31 rows (code-critic: 13 `--mine` + `sandbox`, plus `recover` and `begin`; runner: 13 + `recover`, `begin`, `reparse`; analyst: 14 + `begin`) | python read, list in the trail |
| S18 K10 baseline | true | `role_load.py:302-343` |

### 2. ARITHMETIC (§3)

- **code-critic:** 74,327 − 6,017 (ER, 14 rows) − 773 (RS, 2 rows) + 345 (index lines, est.) = **67,882**, which is 518 B under 68,400.
  Re-derived from report §2/§3 and identical to the draft.
- **automator:** the five kept rows measure, as requirement+door bytes plus the ≈ 42 B per-row overhead the report's 8,170 chars
  imply over 23 rows, about 372 + 311 + 496 + 663 + 373 ≈ **2,215 B**, not 2,363. That gives ER leaving ≈ 5,955 and
  U' ≈ 84,240 − 5,955 − 1,443 + 345 − 400 ≈ **76,787**, about 8,387 over H. Immaterial: STOP stays.
- **Is 518 B real?** It is above the character-vs-byte error (< 50 B per role, report §2) and the index-wording estimate (about
  ±30 B). It is below the page cost of every single code-critic ER row except the smallest. Per-row page cost ≈ requirement+door
  + ≈ 43 B, range 311-663 B. So the margin holds only if ALL 16 rows leave.
- **The single row that tips it (F-4):** `execution_request:profile` (≈ 663 B) or `execution_request:sandbox` (≈ 560 B), alone.
  `sandbox` is the likeliest unproved row: the draft did not read `sandbox_run_directory` (U-2), and its only road is
  `red_sandbox --sandbox-root`. `mine_call` (≈ 500), `case_entries` (≈ 496) or `stand.probe` (≈ 490) each tip it with any second
  unproved row. With B1 unresolved, all 16 rows are unproved on code-critic's roads, so U stays 74,327.

### 3. FR-38 / AR-10 direction (F-3) — and the `MineRefusal` order the draft could not establish

The order in `build_mine_request` (its own comment, `execution_request.py:3465-3469`) is: refusals that need no process, then the
stand probe (`_observe_stand`, `:3475`, about 11 s), then the collect (about 100 s unless the memo hits), then readers of the collect.

| sites | position | cost of a refused call |
|---|---|---|
| `mine_call` 3224/3227/3314/3444/3457, `scope` 3296/1012, `active_dispatch`, `case_entries`, `profile`, `profile_command` 1826/1837/3433, `no_test` 3331/3472, `sandbox` via `sandbox_run_directory` (`:3452`), `place_rows` (first call `:3474`) | before the probe | about 1 s |
| `stand.probe` 2859 | before the probe (no probe to run) | about 1 s |
| `stand` 2825/2869, `stand.reference` 2875 | after a read-only probe | about 11 s |
| `no_test` **3497**, `selector_args` **3583**, `sandbox` **3602**, `window_first` **3659** | AFTER the probe AND the collect | up to about 2 min |
| `run_suite:begin` race 436/438 | inside the stand lease (wait up to 1800 s, B-S14 above) | a lease wait |

Nothing in this table is irreversible. No launch, no idempotency key spent, no budget unit (the `--mine` road answers the budget
while building), no stand mutation, and no persistent collect output: the memo goes only into a request that is never written on
refusal. The draft's F-3 column "seconds" is wrong for the four post-collect sites. The recommendation stands: every row is
acceptable as "learned at the refused call" under the owner's pages F-2, with these qualifications:
- the 5 manifest-row rows stay on the automator's page, which is correct (they judge its finished work);
- `window_first` costs a collect each time a role does not know it. It is call-told for all four roles. That is acceptable (the
  memo makes the repeat cheap; it is an efficiency answer, not a judgment of work), but it is the costliest call-told row and the
  live-runs detector (§7 (c)) should count it first.

Binding amendment (non-blocking): "F-3 table, column 'cost': the four `--mine` rows `no_test` (post-collect branch),
`selector_args`, `sandbox` (clone file), `window_first` refuse after the stand probe and the collect (about 2 min, nothing written,
nothing launched); `run_suite:begin`'s race sites refuse inside the stand lease (released on exit). S14 is corrected to say so."

### 4. TRANSPORT (F-2 (a))

- **Does an extra key break a reader?** No reader breaks. `red_sandbox._run_mine` keys on `error` / `execution_status`
  (`:1282`, `:1687`). `execution_scheduler._child_answer` keys on `status` and keeps `error` (`:527-528`). `stdout_tail` keeps the
  raw last line whole (`:539`, `lines()` `:462-468`). Tests match `error`/`status`.
- **Is `told` dropped?** Yes: by red_sandbox (both branches), probe_by_code (in-process), import_test_receipt (in-process),
  execution_scheduler `invalid_schedule` and the `run_refused` row. → **B1**.
- **Does the role see `told` on the run_suite road?** Yes. The role runs `run_suite.py` through its shell tool and reads stdout and
  stderr whole. `invalid_request` is on stderr, `mine_refused` / `run_the_window_first` / `executor_unavailable` on stdout.
- **AR-18:** one shape per refusal holds only if every road carries the same projection (B1 (a)).
- **Mechanism conflict (non-blocking, binding):** the mechanism spec's decision "Text" (`20261113-…-mechanism-spec.md:92-93`) says
  "expected and door are printed only by in-process transports to the role (`hooklib.block`, `stage_guard.deny`,
  `role_cli.refuse`)", and its row B2 (`:709`) says "expected/door only from `block`/`deny`/`refuse`". F-2 (a) adds a fourth
  transport on a cross-process JSON line. That changes a decided meaning (PROJECT.md p. 6). Amendment: "F-8's edit of the
  mechanism spec also amends the 'Text' decision (:92-93) and row B2 (:709): the `told` key built by `detector_verdict.told_fields`
  is the fourth transport, for the JSON refusals of `run_suite.py` and the road printers of B1; `error` stays byte-identical."
- **Person question (AR-16):** `told` beside `question` in the `executor_unavailable` object (`run_suite.py:1567-1571`) leaves the
  question text untouched. `halts.md:28` reads only the question. OK.

### 5. ONE ROAD (P31, brief item 12)

After the plan as written, a requirement reaches a role by:
- (i) a page row (output judges, and the automator's 5 manifest-row rows);
- (ii) the index line plus the refusal's `told`, on the `run_suite.py` road;
- (iii) nothing, on the red_sandbox / probe_by_code / import_test_receipt / schedule roads (B1);
- `--help` card: not established for `run_suite.py` (no role_cli row was checked for it). Not load-bearing, because the request
  rows' before-work door is `--template request`, named in the index line (S-2 P-2);
- brief: carries no copy (mechanism :88-90).

Told by two roads: the automator's 5 manifest-row rows (page, plus the refusal's `told` once sited). Acceptable: one rule (a sited
refusal always prints its row), and the page is the before-work carrier. E9's transitional double telling is acceptable too.
Told by none: B1. The skill road (`skills/qa-story/phases/s5.md:144,190`) is conductor text, not a role carrier, and stays as is.

### 6. EDGES (§5)

Covered: zero sited rows (E1), a row for some roles (E2), a partly call-told index line (E3), several checks at once (E7), an empty
door (P-1 "key left out when empty"), an unreadable row (E5). Missing:
- **E-road** (B1): a refusal reaching a role through a printer that drops `told`. Invariant: a row is call-told for role R only when
  proved on every road R uses.
- **E-helper** (B3): an id literal inside a multi-caller helper.
- **E-unknown-id:** a literal `refusal("execution_request:typo", …)` sites a non-row id (`_is_sited` true for nothing, `refusal()`
  prints the factory-defect sentence). Amendment: "S-1 acceptance adds: no `execution_request:` / `run_suite:` literal outside the
  31 row ids (P-7 grep, both directions)."
- **E-unmapped site:** `run_suite.py:2902` `RequestError("runtime probe does not match requested profile/source/runtime: …")` is in
  neither the site table nor the E6 list, and P-7's grep enumerates only `validate_request` appends. Amendment: "P-7 enumerates every
  `raise RequestError|MineRefusal|WindowFirst|_sandbox_refusal` and `errors.append(` in `execution_request.py`, and every `raise` and
  JSON refusal print in `run_suite.py`, each with its id or its E6 reason; `:2902` is decided by name (it fits `execution_request:stand`
  'runs this story's build', or E6)."
- **E-index wording per road:** P-2's "your `run_suite.py` calls" is false for a role whose roads are red_sandbox / probe_by_code
  (FR-37). Under B1 (a): "checks of your test-run calls (`run_suite.py`, `red_sandbox.py`, `probe_by_code.py`) are told in the refusal
  …". Count the bytes against the margin.

### 7. P27 / AR-29

No judgment moves into code. Sites write a literal and markers are data. `told_fields` is a renderer, not a census unit (builder
confirms with `test_judgment_census.py`, already in the DoD). Census classes in §1 are acceptable. Under B1 (a), the added road
handlers are renderers too. The road-per-role test constant is data read from the agents' tool lines (AR-1); it is not a judgment.

### 8. TESTS vs docs/TESTING.md

- Right: one parameterised data-joint table `T1rs/told/<id>` (code site ↔ data row), and the S-2 index-line / partial-family joints
  in `test_contract_slices.py`.
- Against TESTING.md «Чего больше нет»: `T1rs/told-fields/*`, six rows on an internal helper (a "мини-батарея на внутреннюю
  функцию"); `T1rs/no-launch/<channel>` ×6, asserting S14, which this node does not change; and `error-bytes` / `one-json-line`
  per channel as separate receipts. Amendment: "fold `error-bytes` and `one-json-line` into the `T1rs/told/<id>` row (one row asserts
  `error` unchanged, one `{` line, the `told` entry); drop `T1rs/told-fields/*` and `T1rs/no-launch/*`; keep `T1rs/unreadable-row` as
  one row of the same table." `T1rs/listed-zero-sited` re-tests `_call_leg` behaviour T1r-pages already owns. Keep it only if no
  `t1rp` row covers "marker on unsited row → red", otherwise drop it. `T1rs/marked-iff-tested` is a pinned list: acceptable as the F-4
  joint, if the list constant is regenerated from the S-1 report, not hand-typed.
- Slow files: B2.
- Witness lawfulness: no CI and no mutations asked of either builder (non-goals list them). Good.

### 9. FEASIBILITY and CUT

- **Site count, re-measured:** 113 raise/append lines in `execution_request.py` (grep), minus about 22 E6 = about 91 relabels; plus
  `run_suite.py` 8 `reparse` raises, 4 RS refusers, the `:2877` reference print and about 8 printers. That is about 110, close to the
  draft's 120. The wrapping is mechanical and weak-model-safe. The cost is in the 31 provokers inside a 3,000-line slow test file,
  plus B1's road printers.
- **Recommendation:** cut S-1 by file into **S-1a** and **S-1b**, sequential or parallel with function-disjoint test owns (D-0048):
  - **S-1a:** `execution_request.py` sites, `RequestError.records`, and in-process joint rows asserting `exc.records`/`args[0]` carry
    the id and `told_text`.
  - **S-1b:** `detector_verdict.told_fields`, `run_suite.py` sites and printers, and B1's road printers, with road rows.
  
  This keeps each worker well under the 250K WARN that T1r-pages passed.
- **Collisions:** none with the running fix round, because S-1 reads `stage_joints.py`, `contract_slices.py` and `stage-joints.json`
  and does not own them. S-2 owns `stage-joints.json`, which F-6 already gates on the fix round's acceptance. None with FV1-23 / F7-RC
  either: `driver_stage_plan.py`, `source_inventory.py` and `ticket_adapter.py` are not in any owns of this draft. Under B1 (a),
  `red_sandbox.py` and `probe_by_code.py` join the owns. They appear in many pile files (grep over `plans/piles` lists 137 files naming
  one of the four scripts), so the Lead must check the in-work batches by function before dispatch. The draft's F-6 "needed beyond the
  manifest" (T5/T5b status) stands.

### 10. F-8 — does absorbing T5 (ER+RS) and T5b leave a requirement without a node?

- Covered: T5's `validate_request`, the four `run_suite.py` refusers, the `invalid_*` prints and "notes stay notes" (the draft keeps
  `MINE (note)`). T5's line "a test row per family 'the automator's page names it'" is superseded by the `T1rs/index-line` and
  partial-family rows. That is acceptable for the call-told rows, and the five manifest rows still satisfy the old line.
- Left without a node: T5b names `s6_close_from_state`'s `MineRefusal` sites (mechanism `:397`). The draft leaves all of them, plus
  `build_mine_request` 3234-3259, bare under E6, because no row exists. After F-8 nothing owns the decision "row or no row" for them.
  Amendment: "S-1's report classifies each E6 site: (code) a caller's misuse no role can meet (e.g. `s6_close` flags passed by
  `probe_by_code` itself), with no row needed; or (role) a requirement a role can meet, with a proposed row queued to T1r-cards with
  a pointer. The Lead's mechanism-table edit (F-8) names that queue."

### 11. §6a Lead decisions

- **F-1 (a):** order creates no rework. N-door and the prose pass are additive renderer and charter edits, and S-2's A22 and
  inject-map changes are cheap regenerations that a later lever lowers again. But F-1's premise, "code-critic to green", is false
  under B1. Amendment: "§6a F-1 is re-taken after B1's choice: with (a) the node closes code-critic by an edge (S-2's measure
  decides), with (b) it closes no role, and the morning report says so." With (b), deciding N-door first gives code-critic its
  measured 1,502 B, which still does not close its 5,927 gap. Neither order closes code-critic without B1 (a).
- **F-2 (a):** right shape. It needs the mechanism "Text"/B2 amendment (key 4).
- **F-3 (a):** right recommendation, wrong cost column (key 3).
- **F-4 (a):** right. It must be proved per road (B1).
- **F-5 (a):** right. A further cut is recommended (key 9).
- **F-6 (a), F-7 (a):** right.
- **F-8 (a):** right, with the E6 classification and the mechanism-text edit.
- No decision conflicts with FR / AR / P beyond the above.

### 12. Class completeness by SIBLING_MAP (axes touched)

| axis | verdict |
|---|---|
| 5 (stage twins) | the draft says "covered"; agreed, one rule across S5/S6/S7 |
| 12 (work-plan carriers) | queued (F-8 edit), agreed; add the E6 queue (key 10) |
| 16 (JSON reader) | the draft says "n/a — no file read added". **Disagree in spirit:** the readers of the refusal JSON line (`red_sandbox._run_mine`, `execution_scheduler._last_json_object`) are axis-16-adjacent twins that parse one line each their own way. Not a blocker; note it for the B1 (a) builder: do not add a third parser, reuse what exists |
| 17 (detector verdict shape) | the draft says "covered"; partially: the Record projection has one builder, but its consumers on other roads drop it (B1) |
| 18 (ratchets) | covered: `unsited` and A22 rows lowered and named. Under B1 (b) code-critic's and the analyst's A22 rows do not fall; P-6 must not lower them by assumption (the "a rise = STOP" guard holds) |
| 34 (one road) | **not covered** as drafted (B1); covered after B1 (a) |
| 37 (T10 "transports" row) | the note is right; under B1 (a) the road printers join it |

All other axes: n/a as the draft says (checked against the map headings; no policy file, release step, shell recognizer, story
resolver or profile reader logic changes).

---

## Proposed nodes (owner: the Lead opens them; rule 6)

- **PN-1 (Lead, stage_joints):** make `call_told` road-aware, so the rule 15 class gets a code guard and not only a test. A data key
  per role listing its run roads, and a site counted for role R only on a road R uses. Open it only if B1 recurs after (a) (promotion
  by evidence, rule 10 (d)).
- **PN-2 (Lead → T1r-cards):** rows or "code-only" labels for the E6 sites (key 10).
- **PN-3 (live-runs):** §7 (c)'s refusal count per ER/RS id per run, with `window_first` and the post-collect rows first.

## Needed beyond the manifest

Read beyond the given: `red_sandbox.py:1225-1314, 1675-1704, 2160-2189`; `probe_by_code.py:2915-2944`;
`import_test_receipt.py:252-265`; `execution_scheduler.py:386-470, 515-543`; `agents/qa-*.md` tool lines; `slow_tests.json`;
`plans/builder-rules.md` 7b (read-main); `docs/TESTING.md:1-70`. Not established: the in-work status of pile batches owning
`red_sandbox.py` / `probe_by_code.py` / `execution_request.py` / `run_suite.py` by function (a scout or the Lead's `piles.py check`).

## Trail

- Draft whole (1-556). T1r-pages report whole. My earlier pages verdict (grep `N5|B2|B3|transport|red_sandbox`). Mechanism spec
  `:88-97`, `:396-397`, `:584-586`, `:709`, grep `T5b?` and `s6_close`. SIBLING_MAP headings, axes 17, 18, 34. TESTING.md 1-70.
  builder-rules 7b (`read-main`).
- Worktree code: `execution_request.py` 380-543, 2600-2880, 3400-3680, grep of every raise/append (113 lines);
  `run_suite.py` 2010-2109, 2815-2980, 3085-3114, grep of printers and raises, `hold_stand` 1464-1490, `refuse_missing_executor`
  1552-1572, `executor_gap` 1642-1664; `stage_joints.py` 288-345, 720-790; `detector_verdict.py` 94-193; `role_load.py` grep
  `native_headroom`; `red_sandbox.py`, `probe_by_code.py`, `import_test_receipt.py`, `execution_scheduler.py` as above.
- Searches with positive controls. `except (MineRefusal|RequestError)` over `scripts/*.py` found `run_suite.py:2081, 2835, 2971, 3106`
  and the test files; the control is that the same pattern found the known `run_suite.py:2081`. `fresh_evidence\(|build_mine_request\(|validate_request\(`
  over non-test scripts found 7 callers; the control is that the known `run_suite.py:2053` hit. Case-insensitive grep of the status
  words over the package listed 23 files; the control is that `run_suite.py` is in the list.
- Re-runs (mechanical, read-only): a python read of `stage-joints.json` giving the 31 rows' requirement+door bytes and producer roles,
  `call_index_wording.execution_request` and `told_ratchet`. Output: e.g. `execution_request:sandbox 517 ['code-critic', 'failure-analyst']`,
  `execution_request:profile 620 [all four]`, `{'hand_cards': 12, 'legacy_legs': 0, 'unsited': 150}`. Also `git -C … status --short`:
  the four scripts under review are clean.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the told transport covers only run_suite.py printers while qa-code-critic (agents/qa-code-critic.md:68) and qa-failure-analyst reach the same refusals through red_sandbox.py (_run_mine notes keep status/error/hint only, red_sandbox.py:1687-1692, 2174-2177), probe_by_code.py:2929 (in-process build_mine_request), and the automator through import_test_receipt.py:260; call_told's global _is_sited (stage_joints.py:766) cannot see this, so S-2 would take code-critic's 16 ER/RS rows off its page and tell them nowhere, and the node closes no STOP role.",
    "B2: S-1's DoD runs only non-slow files (spec line 237/308) but every T1rs acceptance row lives in test_execution_request.py, which slow_tests.json:36 lists at 20.9 s over slow_over_s 10, while S-2's DoD runs the slow test_stage_joints.py (spec line 340) against PROJECT.md p.2; the witness carries none of S-1's keys and F-4's proof list is unsupported.",
    "B3: siting run_suite:recover inside JobStore.read (execution_request.py:403, site table line 284) prints the --recover sentence on begin, --request (run_suite.py:2884) and --detail calls that share the helper, breaking the draft's own E6 invariant."
  ],
  "class_completeness": "Axes touched: 5 covered; 12 queued (F-8) plus the E6 queue; 16 note for the road readers; 17 partial until B1; 18 covered, with A22 not lowered by assumption under B1 (b); 34 not covered as drafted (B1), covered after B1 (a); 37 note for T10. Rule 14 walk of 'id literal in a shared helper': only JobStore.read is affected (B3). Rule 15: call_told pairs a per-role marker with a global site, so a road-scoped proof (B1) or PN-1 is required.",
  "fixes": [
    "B1 (a, recommended): S-1 owns and adds told_fields projection to the refusal printers of red_sandbox.py (probe and diagnostic notes), probe_by_code.py (build_mine_request handler), import_test_receipt.py (validate_request handler), run_suite.py invalid_schedule and execution_scheduler run_refused; T1rs/told rows gain a road column; S-2 marks role R only when proved on every road R uses; or (b) mark only automator/runner and restate the headline as no STOP role closed.",
    "B2: S-1 DoD runs test_execution_request.py once as its own narrow witness; S-2 does not run test_stage_joints.py locally (judged by the batch canon); one reading of PROJECT.md p.2 for both nodes.",
    "B3: JobStore.read's corrupt-file raise stays bare; ids attached at the callers (recover -> run_suite:recover; begin and run_suite.main:2884 -> run_suite:begin; last_run_of bare).",
    "S14 and the F-3 cost column corrected: begin race sites refuse inside hold_stand (run_suite.py:2967-2972); no_test 3497, selector_args 3583, sandbox 3602, window_first 3659 refuse after the probe and the collect (about 2 min); the --mine road writes the request file (run_suite.py:2073) before validate_request (2885).",
    "P-7 enumerates every raise/append in execution_request.py and every raise/JSON print in run_suite.py with id or E6 reason (run_suite.py:2902 decided by name); acceptance adds no ER/RS literal outside the 31 ids.",
    "F-8 also amends mechanism spec Text decision :92-93 and row B2 :709 to name the told key as the fourth transport.",
    "Index wording names the roads the role uses, not only run_suite.py.",
    "Tests: fold error-bytes and one-json-line into T1rs/told/<id>; drop T1rs/told-fields/* and T1rs/no-launch/* (TESTING.md mini-battery and receipt rows); keep unreadable-row as a table row.",
    "S-1 report classifies each E6 site code-only vs role-meetable; role-meetable ones queued to T1r-cards.",
    "Cut S-1 into S-1a (execution_request.py sites and records) and S-1b (told_fields, run_suite.py, road printers), function-disjoint test owns.",
    "Section 6a F-1 re-taken after B1's choice; automator figures restated (kept rows about 2,215 B, U' about 76,787)."
  ],
  "trail": {
    "read": [
      "C:/QAFactory/forge-repo/docs/tasks/specs/20261114-told-before-work-t1r-sites-spec.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/tbw-t1r/docs/tasks/specs/reports/20261114-t1r-pages-report.md",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reviews/20261114-tbw-t1r-pages-plan-critic.md",
      "C:/QAFactory/forge-repo/docs/tasks/specs/20261113-told-before-work-mechanism-spec.md",
      "C:/QAFactory/forge-repo/docs/SIBLING_MAP.md",
      "C:/QAFactory/forge-repo/docs/TESTING.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/read-main/plans/builder-rules.md",
      "W/scripts/execution_request.py",
      "W/scripts/run_suite.py",
      "W/scripts/stage_joints.py",
      "W/scripts/detector_verdict.py",
      "W/scripts/red_sandbox.py",
      "W/scripts/probe_by_code.py",
      "W/scripts/import_test_receipt.py",
      "W/scripts/execution_scheduler.py",
      "W/scripts/role_load.py",
      "W/scripts/slow_tests.json",
      "W/references/stage-joints.json",
      "W/agents/qa-code-critic.md, qa-automator.md, qa-failure-analyst.md, qa-runner.md"
    ],
    "reruns": [
      {
        "command": "python -B (read-only) load W/references/stage-joints.json; print requirement+door bytes and producer roles of the 31 ER/RS rows, call_index_wording.execution_request, told_ratchet",
        "result": "31 rows; sandbox 517 [code-critic, failure-analyst]; profile 620 [automator, code-critic, failure-analyst, runner]; code-critic ER sum 5,426 B; wording '{n} checks of your commands are told in the refusal of the call, with what they expect and the door.'; told_ratchet {hand_cards 12, legacy_legs 0, unsited 150}"
      },
      {
        "command": "git -C .claude/worktrees/tbw-t1r status --short; log --oneline -1",
        "result": "HEAD 7ed7f10; dirty only stage-joints.json, contract_slices.py, stage_joints.py, judgment-census.json, test_contract_slices.py, test_stage_joints.py (the fix round); execution_request.py, run_suite.py, red_sandbox.py, detector_verdict.py clean"
      },
      {
        "command": "grep -nE raise/append sites in execution_request.py; raises and JSON refusal prints in run_suite.py",
        "result": "113 lines in execution_request.py; run_suite.py raise at 2902 and print at 2972 / 2823 absent from the draft's lists"
      }
    ]
  }
}
```
