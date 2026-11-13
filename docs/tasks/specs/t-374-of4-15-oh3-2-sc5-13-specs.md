# t-374 — draft specs of three package nodes: OF4-15, OH3-2, SC5-13

Designer draft (t-374). Read on `.claude/worktrees/read-main` (origin/main). The Lead accepts it; forks are in §4 and
are not decided here. Each node in §1–§3 can go into a builder dispatch once the Lead has picked its forks. Package
text is English (FR-30). Line numbers are origin/main as read on 2026-11-13. Node A is built on top of `wip/tq1-28`
(94d3515). Lines there may be shifted: the builder finds each site by the OLD TEXT quoted here, not by its number.

---

## 1. Node A — onboarding-forge/4/OF4-15: the bug path in role-facing text is the one `publish` accepts

### 1.1 Facts checked (file:line)

- The source of truth. `scripts/artifact_producer.py:229-236` `publish(root, kind, data, relative, ...)`: `root` is the
  task root (`--task-root`), `target = root / relative`, allowed when under `root/'work'` or, for `kind == 'bug'`, under
  `root/'bugs'`; otherwise `ValueError('author artifact must be under task/work, outside evidence receipts')`. A bug is
  accepted ONLY at `<task root>/bugs/BUG-<id>.md` (`:243-248`, the name starts with `BUG-`, `.md`, stem == front-matter id).
- OH5-9 is on main. `agents/qa-bug-reporter.md:57` reads "`<task root>/bugs/BUG-n.md` comes first (`publish` takes only `bugs/`,
  `work/`), never overwritten." and `scripts/brief_pack.py:297` reads "`--path bugs/BUG-<id>.md`". Its test,
  `scripts/tests/test_brief_pack_roles.py:306-325`, is QUARANTINED (`test-layers.json:7149`), so it guards nothing in the canon.
- The four stale sites, verbatim:
  - S1 `references/common-rules.md:111`:
    `` | proposals and artifacts: `bug_file`, `case_file`, artifact paths | the **state directory**, `<project>/qa-factory/` — `bugs/BUG-1.md` is `<project>/qa-factory/bugs/BUG-1.md` | ``
    The same line is in 10 generated slices, `references/slices/<role>/common-rules.md`: qa-automator :90,
    qa-bug-reporter :85, qa-case-designer :48, qa-code-critic :103, qa-doc-scribe :85, qa-failure-analyst :103,
    qa-retro-analyst :85, qa-runner :103, qa-scout :61, qa-test-strategist :48. qa-requirements-tester and qa-case-critic
    do not carry it: the section marker at `common-rules.md:103` lists the 10 roles.
  - S2 `references/external-writes.md:43-44`: "... writes the artifact to its **first-class local home** — a bug always gets `qa-factory/bugs/BUG-n.md` regardless of channel, ..."
  - S3 `references/templates/test-report.md:35`: "TS-n — a plan row; BUG-n — a bug file in `qa-factory/bugs/`."
  - S4 `scripts/driver_stage_s8s9.py:274-275`: `"below and file exactly what the person's own words order there — a local "` / `"proposal under qa-factory/bugs, grounded in the register and the report, "`.
- **One reader disagrees with publish (load-bearing, not in the finding).** `scripts/external_writes.py:649-656`
  `process_bug_proposal`: `bug_path = state_dir() / bug_file_rel`, where `hooklib.state_dir()` is `<project>/qa-factory`
  (`hooklib.py:169-172`). It refuses with "bug_file not found" when the file is not there. `:900-903` (`--record`)
  writes the external id into `state_dir() / rel` too. So a proposal's `bug_file` is read in the STATE-DIRECTORY frame,
  and row S1 describes that frame correctly. A bug published to `<task root>/bugs/` is not found by the tracker
  executor today. `delivery_summary.py:94-99` reads `bug_file` against the task root first, then its parent. Two
  readers of one field use two frames (AR-13). This is fork F-A1.
- The project home is real in code. `scripts/bug_records.py:10-18` reads: "The canonical home of a bug file is the PROJECT's
  `qa-factory/bugs/` (owner, 30.09: bugs are not pushed with the tests)". It reads both homes, and lists a
  story-folder-only record under `outside_home` (`:22-24`). `references/install-paths.json:40` carries
  `qa-factory/bugs/**` (class `carried`, reader `bug_records.py`). DECISIONS.md holds no entry on the bug home (grep
  `qa-factory/bugs|bug home|bugs/`, case-insensitive, 0 hits; positive control `D-00\d\d` = 23 hits). The owner's word
  of 30.09 stands only in that code docstring. This is the owner question (§4.0).
- Load of the texts. `references/inject-map.json:95-100`: qa-bug-reporter gets its common-rules slice AND
  `references/external-writes.md`. No role is injected with `references/templates/test-report.md`, and role_load counts
  only the charter, the inject entries and handoff forms (`role_load.py:419-449`). The driver text is dispatch text,
  not static load. No `<!-- kind: craft -->` marker sits in any of these files (grep over `references/`: only
  tester-manifesto, explore-charter, charter-form, role-load.json), so every changed byte is PROCESS.
- The process ratchet is shrink-only with slack 0 in BOTH directions. `role_load.py:259-282`: a load above its row is
  red, and a load BELOW its row is red too ("lower to N"). Tokens are `ceil(bytes/4)` (`role_load.py:132-134`). Rows on
  main (`references/role-load.json:24-37`): scout 13971, test-strategist 15392, case-designer 12079, automator 18685,
  code-critic 17593, runner 14417, failure-analyst 16322, bug-reporter 13914, doc-scribe 16943, retro-analyst 13198. On
  wip/tq1-28: automator 18687, code-critic 17596 (brief).
- A role-text pin as its own test is forbidden. `docs/TESTING.md:93`: the guard is the registry
  `design/role-rules.json` (read by `scripts/role_rules.py`, keep row `test_role_rules.py`, `test-layers.json:4512`).
  Carriers must have a suffix `.md/.yaml/.yml/.json` (`role_rules.py:43,121`). Anchors are 2-6 words, at most 80 chars,
  and appear exactly once (`:49,173,234`). The rule text is at most 300 chars.

### 1.2 Changes (numbered; the text is exact)

Under F-A1 (§4) the Lead picks (a) or (b) BEFORE dispatch. Items marked [a] or [b] go in only under that option.
Unmarked items go in under both.

A-1 `references/common-rules.md:111`, replace the whole row:
 - [a] `` | proposals and artifacts: `case_file`, artifact paths | the **state directory**, `<project>/qa-factory/`; `bug_file` and `publish` paths: the **task root** | ``
 - [b] `` | proposals and artifacts: `bug_file`, `case_file`, artifact paths | the **state directory**, `<project>/qa-factory/`; a `publish` path: the **task root** | ``
 The line after it (`:114-115`, "`journal_path` carries the `qa-factory/` prefix and `bug_file` does not ...") stays as it is. It is true under both options.

A-2 [a only] `references/external-writes.md:44`: replace `` `qa-factory/bugs/BUG-n.md` `` with `` `<task root>/bugs/BUG-n.md` ``.
 Nothing else in the sentence changes. Under [b] S2 is NOT edited, because the executor still reads the state directory (§4 F-A1).

A-3 `references/templates/test-report.md:35`: the new line is
 `TS-n — a plan row; BUG-n — a bug file in the story's `bugs/` folder.`

A-4 `scripts/driver_stage_s8s9.py:275`: replace the one string literal with two:
 `"bug file at bugs/BUG-<n>.md under the task root (the folder publish takes), "`
 `"grounded in the register and the report, "`
 (`:274` keeps "... — a local " and `:276-277` keep "submitted nowhere. ...".)

A-5 `python -B scripts/contract_slices.py --write` from the package root of the worktree. Then `--check` must be green.
 Exactly the 10 slice files of §1.1 change, and no other file under `references/slices/` changes.

A-6 `design/role-rules.json`: append ONE row (the registry replaces the quarantined OH5-9 pin and guards the new texts):
 `{"id": "bug-file-home-task-root", "rule": "A bug file is written to the story's own bugs/ folder (<task root>/bugs/BUG-n.md), the folder artifact_producer.py publish accepts; the project's qa-factory/bugs/ is only a place bug_records.py reads.", "source": "OF4-15 (finding 20261112-put-baga-v-references-ne-tot-chto-prinimaet-publish); OH5-9 (B-315)", "carriers": [...]}`
 with these carriers:
 - `{"file": "agents/qa-bug-reporter.md", "anchor": "`<task root>/bugs/BUG-n.md` comes first"}`
 - `{"file": "references/templates/test-report.md", "anchor": "a bug file in the story's"}`
 - [a] `{"file": "references/common-rules.md", "anchor": "`publish` paths: the **task root**"}` and `{"file": "references/external-writes.md", "anchor": "a bug always gets `<task root>/bugs/BUG-n.md`"}`
 - [b] `{"file": "references/common-rules.md", "anchor": "a `publish` path: the **task root**"}`

A-7 `references/role-load.json` `process_ratchet_tokens`: set each of the 10 roles of §1.1 to its value measured by
 `python -B scripts/role_load.py --all --json` (`process_tokens`) after A-1..A-5. Expected bytes: A-1 is −21 bytes per
 slice under [a] (179 → 158) and −23 under [b] (179 → 156); A-2 is +1 byte for qa-bug-reporter. That makes each row
 −5 or −6 tokens (ceil effects), and qa-bug-reporter −5 under [a] (net −20 B) or −6 under [b]. qa-requirements-tester
 and qa-case-critic do not move. A row that would have to RISE: stop, change nothing in role-load.json, and report it
 (§1.4 E-A3). Do not touch `ratchet_tokens` (slack 1000; a shrink of 6 tokens stays inside it).

A-8 [a only] `scripts/external_writes.py` `process_bug_proposal` (`:653-656`) and `--record` (`:900-903`). A bug's
 `bug_file` is read from the task root:
 - `bug_path = artifacts_dir(ticket) / bug_file_rel` (`hooklib.artifacts_dir`, already imported at `:117`).
 - If `bug_path` is not inside `artifacts_dir(ticket)`, checked with `runtime_paths.contained` (the one containment
   predicate, SIBLING_MAP axis 8): `status.append(("REJECT", path.name, "bug_file must be a path inside the story folder, such as bugs/BUG-1.md; got <value>"))`.
 - If it is absent there AND `state_dir() / bug_file_rel` exists (a story filed before this release): read that file
   (builder-rules 9, no refusal for an in-flight story), and add one status line
   `("NOTE", path.name, "bug_file read from the project's qa-factory/bugs/ (an older home); the story's bugs/ has no such file")`.
 - If it is absent from both: the existing REJECT "bug_file not found: <rel>" is unchanged.
 - `--record` uses the same resolution, through ONE helper `_bug_file_path(ticket, rel) -> Path | None` that both call sites use.
 The case path (`case_file`, `:779`) stays on `state_dir()`.

A-9 Changelog fragment `changelog.d/of4-15-bug-path.md`, one line in the shape of `changelog.d/oh5-9-publish-path.md`,
 naming the shared rules, the report template and the S8 dispatch text, plus the executor under [a].

A-10 [F-A3, if the Lead takes it] `scripts/form_selftest.py:245`: the same new text as A-3, with ` - ` in place of ` — ` (the sample keeps its ASCII dashes).

### 1.3 Architecture, owners, census

- AR-13 (one reader per fact): under [a] the three readers of a bug's location (publish, external_writes,
  delivery_summary) use one frame, the task root. Under [b] the text stops claiming a frame that publish refuses, and
  the executor split stays as the open F-A1 residual node. Change check: the text names exactly the frame of the code
  that reads it.
- AR-22 (every field read has a producer): `bug_file`'s producer is the role, told by A-1/A-2. Its reader is
  external_writes, and they agree under [a].
- AR-19 (stage twins change together): the source and its 10 slices change in one commit (A-5, `contract_slices --check`).
- AR-20 (shrink-only ratchets): 10 rows go down, none goes up (A-7).
- AR-8 (a role is handed its paths): the S8 dispatch names the folder publish takes (A-4).
- Checks added or changed, with owner and census class:
  - the role-rules row (A-6): owner data, class xref. `role_rules._carrier_problems` already has census row `xref/data`
    (`judgment-census.json:707`). No new census row.
  - [a] the containment REJECT in `process_bug_proposal`: owner data, class shape. It appends a status and raises
    nothing, so it is not a census unit. The builder confirms with `test_judgment_census.py` if the witness prints it.
- FR walk for the builder report: A (FR-1: the new REJECT names what it expected and a door, `bugs/BUG-1.md`),
  B (no text a person reads: the report notation is read by a person, plain words, no path inside the plugin), C
  (FR-11, FR-15), D (FR-37 is the rule this node closes), E (FR-37), G (FR-30, FR-32, FR-54).

### 1.4 Edges, with the invariant each protects

- E-A1 qa-requirements-tester and qa-case-critic. Their slices must stay byte-identical. Invariant: a slice changes
  only when its source section reaches that role.
- E-A2 wip/tq1-28 regenerated two `test-code-patterns.md` slices. A-5 must not change them. Invariant: this node's
  slice diff is exactly the 10 common-rules slices.
- E-A3 a process row would have to rise (a ceil effect on a slice another branch changed): stop and report the role,
  the old row and the measured value. Invariant: no process row rises without a named verdict (AR-20, axis 18).
- E-A4 [a] a proposal written before this release whose bug lives only in `<project>/qa-factory/bugs/`: it is read
  there, with a NOTE. Invariant: a bug file that exists in one of the two homes bug_records reads is never "not found",
  and a file outside both homes is never read.
- E-A5 [a] hostile `bug_file`: `../../x.md`, `C:/x.md`, `/etc/x.md`, `bugs/../../../x.md`, an empty string (that stays the
  existing "missing 'bug_file'"), a value with backslashes `bugs\\BUG-1.md`. The first four are REJECTed by containment.
  Backslashes resolve inside on Windows and are accepted. Invariant: the executor never reads a file outside the story
  folder, nor outside the project's `qa-factory/bugs/` on the fallback. Error direction: when containment cannot decide
  (an OSError while resolving), refuse.
- E-A6 [a] custom `artifact_root` (stories under `qa-factory/stories/`): `artifacts_dir(ticket)` resolves it.
  Invariant: no literal `artifacts/` in the new code.
- E-A7 the dispatch text grows by about 30 bytes inside `extra`. It is not a static load and has no cap of its own;
  `run_role` passes it whole. No cut.
- E-A8 under [b], S2 still says `qa-factory/bugs/` while the charter says the task root (the status quo since OH5-9).
  This is the named residual of F-A1(b), not a silent gap.

### 1.5 Tests (docs/TESTING.md)

- No new test file. The guard of the texts is the registry row A-6, checked by the keep test `test_role_rules.py`.
  Before A-1..A-3 the anchors are absent, so the row is red. That is the row "that failed before the fix".
- `test_contract_slices.py` (keep, table) covers the regeneration.
- `test_role_load.py` / audit A22 covers A-7. Note that `test_audit_rules.py` and `test_role_load.py` were red when the
  quarantine cohort entered (`test-layers.json:6984-6991`). A red that is not this node's is a report line, not a fix.
- The driver text (A-4) gets no test: a `.py` carrier is refused by the registry (`role_rules.py:121`), and a source
  pin is forbidden (`TESTING.md:94`). The critic reads it.
- [a] `test_external_writes.py` (keep, table), with variant rows of ONE parameterised case "where a bug proposal's
  bug_file is read":
  - the file at the task root → no REJECT;
  - the file only in the project home → NOTE and no REJECT;
  - the file in neither → "bug_file not found";
  - `../../x.md` → REJECT "inside the story folder";
  - `C:/x.md` → the same REJECT.

### 1.6 owns, witness, siblings

- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\common-rules.md`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\` (the 10 `common-rules.md` files only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\templates\test-report.md`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s8s9.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of4-15-bug-path.md`;
  [a] plus `...\references\external-writes.md`, `...\scripts\external_writes.py`, `...\scripts\tests\test_external_writes.py`;
  [F-A3] plus `...\scripts\form_selftest.py`.
  `scripts/contract_slices.py` is RUN, not edited. The batch row names it under «Пишет в»; the Lead may strike it.
  (In the builder's worktree: the same relative paths.)
- witness:
  `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owned path, the 10 slice files named one by one>`;
  then run every file it prints, plus `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`,
  `python -B ai-packages/qa-factory/scripts/role_load.py --all` (the table goes into the report),
  `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` (external-writes.md is an unmarked reference
  under the 12,000 B cap, `selftest.py:387-392`).
- ratchets: process_ratchet_tokens (10 rows down, A-7); the judgment census unchanged; the clone ratchet ([a], one
  helper instead of two copies).
- siblings by SIBLING_MAP:
  - axis 8 (where the story is on disk): the bug's home is a story location; [a] reads it through `artifacts_dir` and
    `contained`. Covered.
  - axis 5 (stage twins): the charter (:57), card (brief_pack:297) and S8 dispatch (A-4) say one thing. Covered.
  - axis 13 (dispatch text): A-4. Covered.
  - axis 18 (ratchets): A-7 rows down. Covered.
  - axis 34 (one road): two homes are two roads until the owner answers (§4.0). Queued as the owner question.
  - Analogs reported, not widened: F-A2 (`project:bugs/` keys), F-A3 (`form_selftest.py:245`),
    `design/factory-rules-debt.md:29` (the FR-37 debt row about gate A's wording: no `qa-factory/bugs` is left in
    `gate_brief.py` by grep; whether the row is stale is the Lead's to judge), `judge_results.py:274` (a comment) and
    `metrics_projection.py:481,514` (reads only the project home): under the owner's answer.
- Sweep inside the artifacts (rule 9):
  - common-rules.md table rows :110 and :112: n/a, other frames.
  - external-writes.md :49 (`"bug_file": "bugs/BUG-n.md"`): right in the new frame under [a], unchanged under [b].
  - `external_writes.py:46` docstring: the same, n/a.
  - test-report.md other notation entries: n/a.
  - driver_stage_s8s9.py :269-270 (the experiment line): n/a, no path.

---

## 2. Node B — onboarding-forge/2/OH3-2: `[DEFERRED: application repo paths]` gets its `add`

### 2.1 Facts checked, and the recommendation with its evidence

- The marker: `skills/qa-onboarding/phases/p4-generate.md:364-367`: "Nobody could give a local path → `code_repos: []`
  **plus** a `[DEFERRED: application repo paths]` marker in `project-profile.md` and its `factory-backlog.md` row;
  never `app_root: "."` left standing ...". The text names a row, but no command writes it.
- How the other markers of P4 work: each one has a row command, and both live in **step 8**.
  - `risk areas not named`: P4:598-609, a doc ref, `story_count 3`, resolve with `--marker-file`/`--marker-text`.
  - `impact scale not set`: P4:611-619, a pointer ref, `manual`, resolve with `--field-values` and `--marker-text`.
  - Step 8's general rule (P4:584-596): every deferred answer gets **both** traces, a marker AND a `DD-n` row with the
    question verbatim. Its own example question is this topic: "batch 1: where are the application repositories
    checked out locally?" (P4:591).
- What OH3-24 did to `add` on this page (on main):
  - An ANSWERED question ("a key stays") is now a doc-ref bookkeeping row (P4:299-301, with `--essence`; test
    `test_project_decisions_doc_ref_form.py:107-118`).
  - `add`/`resolve` refusals are one line, exit 2 (`project_decisions.py:869`), and every refusal comes before the
    first write (`:488`).
  - A deferral, an UNanswered question, stays a pointer row whose `resolve` writes the config value
    (`project_decisions.py:460-472`).
  - "Nobody could give a local path" is an unanswered question, so it is a pointer row.
- The audit requires the row even if the marker went away. `scripts/audit_factory.py:766-769` REQUIRED_FACTS
  "application repositories (interview topic 1)": when `code_repos` AND `protected_app_paths` are empty, `:808-817`
  demands an open DD row whose cells hold "application repo" (or app_repo/code_repos/...), else A13 is red.
- **Recommendation: a pair in the registry (option 1).** Dropping the marker (option 2) is inconsistent:
  - A13 still demands a DD row for the same hole (audit_factory.py:766-817), so the row needs a command anyway.
  - Step 8 demands both traces (P4:584-588).
  - P4:178-185 forbids `add-finding` when a question WAS asked.
- Already done:
  - The `add` without `--essence` (the batch row's "with `add` without `--essence` on P4:251") is fixed: the site is
    now P4:299-301 and carries `--essence` and a doc ref (OH3-24 Q-d, test_project_decisions_doc_ref_form.py:107-118).
  - Q-e (a collector check of `--essence`) is OH3-24's, not this node's.
- `scripts/tests/test_onboarding_markers.py:38-40` `EXCEPTIONS = {"application repo paths": "finding ... (OH3-2)"}`.
  K2-2 (`:106-111`) goes red as soon as the marker is paired and the row is still there. So the row goes in the same commit.
- The collector `ADD_COMMAND` (`:45`) wants, within ONE backtick span, `project_decisions.py ... add --field-ref ... --essence "<E>"`.
  A13 pairs by the first 40 chars of the marker's essence inside the row's essence cell (`audit_factory.py:897-906`).
  So the essence must start with "application repo paths".
- `project_decisions.py:885-888`: `add` requires `--field-ref` (repeatable), `--essence`, `--asked`; `--trigger-type`
  is one of manual|capability_verified|story_count|date (`:404`). `upsert` reuses an open row with the same set of
  refs (`:421-423`), so a re-onboarding writes no second row.

### 2.2 Changes

B-1 `p4-generate.md:365-366`: replace "marker in `project-profile.md` and its `factory-backlog.md` row;" with
 "marker in `project-profile.md` and its `factory-backlog.md` row (step 8);".

B-2 `p4-generate.md`, step 8: add a new paragraph right after the impact-scale paragraph (after the line ending
 `--marker-text "[DEFERRED: impact scale not set]"`.` at :619), before `## 8b.`:

 ```
 A deferred application repo path is ONE row too, and it exists only when topic 1 was asked and nobody could give a
 local path (step 1): `project_decisions.py --root . add --field-ref /code_repos --field-ref /app_root
 --field-ref /protected_app_paths --essence "application repo paths not given: config.json, strategy/project-profile.md"
 --asked "batch <id>: <the question as it was put>" --trigger-type story_count --trigger-value 1` (it comes due at the
 first story, which reads its change in the application code). Its later resolution gives the exact values of all three
 keys in `--field-values` (an object keyed by the three pointers; tests and application in one repository is
 `{"/code_repos": [], "/app_root": ".", "/protected_app_paths": ["src"]}`) and names
 `qa-factory/strategy/project-profile.md` as `--marker-file` with `--marker-text "[DEFERRED: application repo paths]"`.
 ```
 The trigger values in this text follow F-B1's recommendation. Under F-B1(b) the text reads `--trigger-type manual`,
 and the parenthesis becomes "(it is `manual`: A13 already names the empty keys on every audit)".

B-3 `scripts/tests/test_onboarding_markers.py:38-40`: the table becomes empty, and the comment above it stays:
 `EXCEPTIONS = {}`.

B-4 Changelog fragment `changelog.d/oh3-2-app-repo-paths-row.md`, one line: onboarding now writes the deferred-decision
 row for application repository paths nobody could give, so the audit pairs the marker.

### 2.3 Architecture, owners, census

- AR-22 (every field produced has a reader): the marker the phase writes now has the row its reader A13 pairs.
- AR-28 (an unknown never becomes a pass): the hole stays an open row with a trigger, never a silent `[]`.
- AR-23 (empty outcome declared): `code_repos: []` + marker + row is the declared empty outcome.
- AR-20 (shrink-only ratchets): `EXCEPTIONS` shrinks 1 → 0.
- Checks: no check is added or changed. A13 (`a13_deferred_decisions`, xref, owner data) and K2-1/K2-2 are unchanged;
  only their input changes. No census row.
- FR walk: C (FR-11: the tool the text names produces the field; FR-38), E (FR-23: a recordable null outcome),
  B (n/a: no text to a person changes; the `--asked` cell carries the person's question verbatim, as before).

### 2.4 Edges

- E-B1 re-onboarding over an open row with the same three refs: `upsert` returns the existing row (PD:421-423).
  Invariant: one hole, one open row.
- E-B2 a later answer "tests and application in one repository": the resolution still gives all three values
  (`code_repos: []`, `app_root: "."`, `protected_app_paths: [...]`). Invariant: `resolve` refuses while a pointer has
  no value (PD:464-466), so no key is left half-written.
- E-B3 a re-onboarding where the person now gives the path: P4:358-364 writes the keys, and the open row is closed by
  `resolve`, not left open. Invariant: A13 has no live marker without an open row, and no open row is left without its hole.
  `resolve` refuses while a marker remains unnamed (PD:480-483).
- E-B4 topic 1 never asked: no marker and no row (P4:595-596 "go back and ask"). Invariant: no deferral without a question.
- E-B5 the essence must stay free of `"` and backticks: the collector reads it up to the next `"` (`ADD_COMMAND`).

### 2.5 Tests

- No new row. The proof is K2-1 of `test_onboarding_markers.py` (keep, detector) once the exception row is gone. It
  fails on today's text (the marker is unpaired) and passes after B-2. K2-2 has nothing left to iterate.

### 2.6 owns, witness, siblings

- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_onboarding_markers.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh3-2-app-repo-paths-row.md`.
- witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/skills/qa-onboarding/phases/p4-generate.md ai-packages/qa-factory/scripts/tests/test_onboarding_markers.py`,
  then every file it prints, at least `python -B ai-packages/qa-factory/scripts/tests/test_onboarding_markers.py`.
- ratchets: `EXCEPTIONS` 1 → 0 (axis 18 member by its own comment, `:36-37`). No process-token ratchet (P4 is not a
  role's load). The judgment census is unchanged.
- siblings:
  - axis 5 (stage twins): the three P4 deferral paragraphs, risk areas / impact scale / app repo paths, now share one
    shape. Covered.
  - axis 18: covered.
  - axis 21 (markdown table cells): n/a, no table reader touched.
  - axis 34 (one road): every P4 marker now reaches A13 by the same road. Covered.
- Sweep of p4-generate.md for markers: `risk areas not named` has its paragraph (applied before), `impact scale not
  set` has its paragraph (applied before), and the two template markers `[DEFERRED: …]` (:137, :309, :356, :586) are
  slots, not concrete markers (`concrete_markers`, test :52-55). Not applicable.

---

## 3. Node C — onboarding-forge/2/SC5-13: readiness prints receipts so far, and NOTE for an unasked unknown

### 3.1 Facts checked: what is done and what is not

- The finding's items (`findings/20261031-preduprezhdeniya-s0-host-hooks-unknown-visyat-do-konca.md:24-29`):
  1. print_summary;
  2. `--require` NOTE, and WARN with a move for a requested capability;
  3. the conductor does not copy NOTE lines.
- Item 1 is NOT done. `scripts/readiness.py:1338-1339` still prints `missing: {', '.join(host['missing'])}` at every state.
  grep `receipts so far` in readiness.py, driver_s0.py and host_capabilities.py: 0 hits (case-insensitive). The positive
  control in the same call hit `note` lines in host_capabilities.py.
- Item 2 is NOT done. `readiness.py:1393-1426` prints `WARN` only for `wanted` names that are not ok, and nothing for an
  unasked capability. `did not ask` has 0 hits.
- Item 3: the CODE path is done by construction.
  - `driver_s0.py:2362` `wanted` never holds `vcs_api`/`host_hooks`.
  - `:2373` reads the lines after the JSON record.
  - `:2389` keeps only lines starting with `WARN`, so a `NOTE` line is never copied.
  - The CONDUCTOR path is not done: `skills/qa-story/phases/s0.md:262-264` tells the conductor to record "`unknown` ...
    as the script's own line (`vcs_api: unknown - ...`)", and `:288-289` keeps "a `vcs_api`, `host_hooks` or
    `base_slice` line whose status is `unknown`: it is recorded and not shown at gate A".
  - The gate A filter `gate_brief.py:2246` matches only the prefixes `S0 ` / `WARN `. A recorded `NOTE vcs_api: ...`
    line would therefore be SHOWN at gate A. That is a regression to avoid (F-C2).
- OH5-3 (ff6c771) and OH3-6 touched nothing of the above. The host line and the `--require` block read as quoted.
- Data shape: `host_capabilities.inspect` (`host_capabilities.py:70-124`) returns `observed` (any receipt script),
  `missing` (expected − observed), `mechanisms` (one key per expected script, `invocation: observed|unverified`, 10
  today), `story_ready`, `live_parity`. `readiness.json` keeps the whole dict (`readiness.py:1248`). Only the printed
  line changes (AR-21).
- `vcs_api` is `unknown` without `--probe-vcs` and without receipts (`readiness.py:1253-1256`). `host_hooks` is
  `unknown` until `hooks_proved` (`:1262-1275`).

### 3.2 Changes

C-1 `scripts/readiness.py`: add, right above `print_summary`:

 ```python
 def _receipts_part(host: dict) -> str:
     """The receipts part of the `host_integration` line (SC5-13). Until the live probe passed (`story_ready`), a missing
     hook receipt is a call that has not happened yet, so the line counts what arrived instead of listing what has not;
     once the probe passed, a missing receipt is news and is named. Counted from `mechanisms` (one entry per expected
     script), never from `observed`, which may hold a receipt of a script that is not expected."""
     if host.get('story_ready') is True:
         missing = host.get('missing') or []
         return 'missing: ' + (', '.join(missing) if missing else 'none')
     mechanisms = host.get('mechanisms')
     if not isinstance(mechanisms, dict) or not mechanisms:
         return 'receipts so far: unknown'
     seen = sum(1 for m in mechanisms.values() if isinstance(m, dict) and m.get('invocation') == 'observed')
     return f'receipts so far: {seen} of {len(mechanisms)} expected scripts (they accumulate as the story runs)'
 ```
 Then replace `:1338-1339` with:
 ```python
     host = data.get('host_integration')
     if host:
         print(f"  host_integration  {host['status']}  {_receipts_part(host)}; live parity: {host['live_parity']}")
 ```

C-2 `scripts/readiness.py` `main`, inside `if args.require:`, right AFTER the `if stop_line: print(f"WARN {stop_line}")`
 lines and BEFORE `if blockers:`:
 ```python
         asked = set(wanted)
         for name in CAPABILITIES:
             entry = (data.get("capabilities") or {}).get(name) or {}
             if name not in asked and entry.get("status", UNKNOWN) == UNKNOWN:
                 print(f"NOTE {name}: unknown; this story did not ask for it")
 ```
 The WARN line for a REQUESTED capability stays exactly as it is (`:1402`, `:1417-1418`). F-C1 explains why the
 finding's "WARN with the move" is not specified.

C-3 [F-C2, recommended] `skills/qa-story/phases/s0.md`:
 - `:262-264`: replace "`unknown` goes into `warnings[]` as the script's own line (`vcs_api: unknown - ...`) and is NOT
   said to the person: it is not established, gate A does not show it, and the report names it." with
   "`unknown` is the line `NOTE vcs_api: unknown; this story did not ask for it`: it is not established, it is NOT said
   to the person and NOT recorded (`state/readiness.json` keeps it)."
 - `:288-289`: replace "the other exception is a `vcs_api`, `host_hooks` or `base_slice` line whose status is `unknown`:
   it is recorded and not shown at gate A." with "the other exception is a `base_slice` line whose status is `unknown`:
   it is recorded and not shown at gate A; a `NOTE` line (`unknown`, and the story did not ask for it) is not recorded at all."
 - `:411` stays as it is. The gate A filter still covers lines that older stories recorded (builder-rules 9).

C-4 Changelog fragment `changelog.d/sc5-13-readiness-receipts-note.md`, one line: readiness counts hook receipts so far
 instead of listing missing ones until the live probe passes, and names an unknown capability a story did not ask for
 as a NOTE, not a warning.

### 3.3 Architecture, owners, census

- AR-28 (an unknown never becomes a pass): NOTE never changes the exit code and never says ok. "receipts so far:
  unknown" when the count cannot be read, never 0.
- AR-12 (friction): no per-story noise for the conductor and the person.
- AR-21 (what a stage gathers travels whole): readiness.json is unchanged, only the printed line changes.
- AR-22 (every field produced has a reader): the NOTE line's reader is the conductor by s0.md's text. Its code reader,
  driver_s0:2389, ignores it by its WARN-only rule, which is stated.
- AR-17/AR-18 (one output shape, one reader): no new detector shape; `WARN` keeps its one reader.
- P31 (one road): the conductor path records what the driver path records (C-3).
- Checks: none added. The `--require` block is in `main` and has no census row (`judgment-census.json:660-675` lists
  readiness check units, and `main` is not one). NOTE is output, not a refusal. Owner: data. Census class: n/a, no unit.
- FR walk:
  - A (FR-4: an informed pass stays one, the exit code is unchanged);
  - B (FR-6: a text a person reads. The WARN lines that reach gate A are unchanged; NOTE never reaches a person (C-3);
    the summary is a machine channel to the conductor, `human-questions.md:9-11`);
  - F (FR-41: unknown is printed as unknown);
  - E (n/a).

### 3.4 Edges

- E-C1 `host_integration` absent: no line (unchanged).
- E-C2 `story_ready` True and `missing` empty: "missing: none" (the old text printed "missing: ;").
- E-C3 `mechanisms` absent, empty or not a dict: "receipts so far: unknown". Invariant: an unreadable count is never printed as a number.
- E-C4 `observed` holds a receipt of a script outside the expected set: not counted. Invariant: N ≤ M always.
- E-C5 `story_ready` False because the probe FAILED, not because it was never run: the count line is printed too. The
  failure is told by the `host_hooks` capability line and its note (`host_capabilities.py:113-117`), not by this list.
- E-C6 no `--require`, or `--require ""`: no NOTE line, because no story asked anything. Invariant: NOTE exists only
  against a stated ask list.
- E-C7 `--require` naming every capability: no NOTE. Duplicated names: the set removes them. An unknown name exits 1
  before any NOTE (unchanged, `:1395-1398`).
- E-C8 a capability entry absent from `data["capabilities"]`: read as `unknown`. It gets a NOTE if not asked; if asked,
  the existing WARN line "None" is unchanged.
- E-C9 an unasked capability that is `missing` or `not_configured`: no NOTE, no WARN (unchanged; the finding scopes
  `unknown` only).
- E-C10 `--require ... --json`: the NOTE lines come after the JSON record. `driver_s0.json_record` returns them in
  `after` and `:2389` drops them. Invariant: the driver's `pipeline.warnings` is byte-identical before and after this
  change for the same project.
- E-C11 conflicting pair: the finding's "WARN with the move" against FR-6. Forked (F-C1).
- E-C12 conflicting pair: "NOTE not copied" against s0.md's "record unknown vcs_api". Resolved by C-3 under F-C2.
  Invariant: a NOTE line never reaches gate A.

### 3.5 Tests (keep file `test_readiness.py`, inside its `main()` flow)

- T-C1, ONE parameterised case "the host_integration line". Each row calls `readiness.print_summary(data)` with a
  synthetic `data = {"host_integration": {...}}` under `contextlib.redirect_stdout` and reads the line starting with
  `  host_integration`. Rows (id → expect in / expect not in):
  - fresh: `story_ready` False, 10 unverified mechanisms → "receipts so far: 0 of 10 expected scripts" / "missing:";
  - partial: 3 of 10 observed → "receipts so far: 3 of 10";
  - ready-missing: `story_ready` True, `missing` ["exit_gate.py"] → "missing: exit_gate.py";
  - ready-complete: True, `[]` → "missing: none";
  - no-mechanisms: False, key absent → "receipts so far: unknown";
  - stray-receipt: an `observed` key outside `mechanisms` → the count is unchanged.
  - Plus one real-path row: `cli(root)` on the test's project → the line has
    `f"receipts so far: 0 of {len(host_capabilities.inspect(root)['mechanisms'])}"` and no "missing:". The count is read
    from the code, never pinned as 10 (TESTING.md:95).
- T-C2, ONE parameterised case "an unasked unknown is a NOTE". Rows through `cli(root, ...)`:
  - `--require vcs_api` → "WARN vcs_api: unknown", no "NOTE vcs_api", exit 0;
  - `--require test_repo` → "NOTE vcs_api: unknown; this story did not ask for it" and
    "NOTE host_hooks: unknown; this story did not ask for it", no "WARN vcs_api", exit 0;
  - no `--require` → no line starting with "NOTE ";
  - `--require test_repo --json` → "NOTE vcs_api" after the record, exit 0.
- Both fail before C-1/C-2 (the old line and no NOTE).

### 3.6 owns, witness, siblings

- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\readiness.py` (`print_summary`, new `_receipts_part`,
  `main` `--require` block),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_readiness.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\sc5-13-readiness-receipts-note.md`;
  [F-C2] plus `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s0.md`.
- witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/readiness.py ai-packages/qa-factory/scripts/tests/test_readiness.py [ai-packages/qa-factory/skills/qa-story/phases/s0.md]`,
  then every printed file, at least `python -B ai-packages/qa-factory/scripts/tests/test_readiness.py`.
- ratchets: none moves. s0.md is not a role load, there is no census unit, and the clone ratchet gets one small helper.
- siblings:
  - axis 17 (the detector verdict shape): n/a. A readiness line is not a detector finding, and the `WARN` prefix keeps
    its readers (driver_s0:2389, gate_brief:2243/2246).
  - axis 34 (one road): conductor and driver record the same lines. Covered by C-3.
  - axis 5 (stage twins): `qa-doctor/SKILL.md:245` ("`vcs_api`/`host_hooks` are never the next action unless an open
    story needs them") is the same decision for another entry. n/a, the doctor reads readiness.json, not the
    `--require` output.
  - axis 18: n/a.
- Sweep of print_summary: the other lines (capabilities, execution_profile, telemetry, runtime_paths,
  orchestrator_context) do not print a list of things not yet happened. n/a.

---

## 4. Forks and the one owner question (decisions are the Lead's)

### 4.0 The owner question (OF4-15), in plain words

Владельцу: «Где живут баги истории: в папке самой истории (`<папка истории>/bugs/`, туда их сейчас кладёт публикация),
а общая папка проекта `qa-factory/bugs/` — только старое место, где читатели ещё ищут, или настоящий дом багов — общая
папка проекта (ваше слово от 30.09, записанное в `bug_records.py`), а папка истории — рабочая копия?»

If she answers "the project folder": the four texts go back to naming `qa-factory/bugs/`, and the code changes
instead. `publish` (artifact_producer.py:232-234) and the reporter's charter and card from OH5-9 then write into the
project folder. That is a code node with a critic. This node's A-1..A-4 and A-6 would be reverted, and F-A1(a) would
not be built.

### 4.1 Forks

- **F-A1 (OF4-15): the tracker executor reads `bug_file` from the state directory.**
  `external_writes.py:653,901` read it there. Changing S1/S2 alone makes the text say a frame that one reader does not use.
  - (a) Recommended. A-8 goes into this node. The executor reads the task root first and falls back to the project
    home with a NOTE. The node becomes builder → critic.
    - Cost: about 25 lines of code, one helper, 5 variant rows, and 3 more owned files.
    - Gain: one frame for all three readers (AR-13); the jira channel finds a published bug.
  - (b) Text-only now. Node A changes S1 (the [b] wording, true for today's code), S3, S4, and does not touch S2 or the
    executor. A new node with owns `external_writes.py` + `test_external_writes.py` is opened in the pile after the
    owner answers.
    - Cost: until then, external-writes.md and the charter contradict each other (the status quo), and the tracker
      channel cannot find a bug published at the task root.
  - (c) The finding's literal option: text-only on all four sites, the executor untouched. Not recommended: the text
    would tell the role a frame the jira executor refuses ("bug_file not found").
- **F-A2 (OF4-15): an analog the finding did not name.** The handoff key `project:bugs/`: `references/stages.json:286,360`
  (the reporter's witness artifact), `references/artifact-writers.json:268`, `references/slices/qa-bug-reporter/handoff-keys.md:7,13`,
  `skills/qa-story/phases/s8.md:5`, `scripts/brief_pack.py:104`, and the generated digest at `agents/qa-bug-reporter.md:62`.
  These name the project root as the reporter's output, while publish writes to the task root.
  - Recommended: a new finding in onboarding-forge, opened after the owner's answer, not in this node.
    - Cost: none now. Reason: these files are a contract with readers (exit_gate:733, driver_runner:1046,
      guard_pre_tool:1033), and changing them is a code node.
  - Alternative: widen this node. Cost: about 7 more files and a critic on code.
- **F-A3 (OF4-15): `scripts/form_selftest.py:245`** holds the same notation line in a self-test sample.
  - Recommended: include it (A-10). Cost: one line, one more owned file.
  - Alternative: leave it. Cost: a stale sample in the package.
- **F-B1 (OH3-2): the trigger of the new row.**
  - (a) Recommended: `story_count 1`. Every story reads its change in the application code, so the hole is due at once,
    like risk areas' `story_count 3`.
  - (b) `manual`, like the impact scale. A13's REQUIRED_FACTS does not keep the hole loud once the row exists
    (audit_factory.py:811), so a manual row could stay forgotten.
  - Cost of either: one token in the text.
- **F-C1 (SC5-13): the finding's "for a requested capability: WARN as now AND the move (the probe command from `remedy`)".**
  A requested non-ok WARN line goes into `pipeline.warnings` and is shown at gate A, cut to 180 chars
  (`readiness.py:1413-1415`). A script command in it would put a script name in front of a person (FR-6,
  `human-questions.md:46-47`).
  - (a) Recommended: the WARN line stays unchanged. The move already lives in `readiness.json` `remedy.steps/verify`,
    which the conductor reads (s0.md:279-281). Cost: none.
  - (b) Append "; next: <remedy.verify>". Cost: an FR-6 violation at gate A, plus a gate_brief translation that does not exist.
- **F-C2 (SC5-13): s0.md is in owns, beyond the batch row's «Пишет в».** The finding's item 3 asks for it.
  - Recommended: include C-3. Without it, the conductor path can record a `NOTE vcs_api ...` line that gate A then shows
    (`gate_brief.py:2246` matches only `S0 `/`WARN `), which is worse than today.
    - Cost: two sentences of a phase text.
    - What changes: conductor-path stories stop carrying `vcs_api/host_hooks: unknown` lines in `warnings`, which is
      exactly what driver-path stories already do (`driver_s0.py:2362,2389`).
  - Alternative: keep owns as the row says. Cost: two roads (P31) and the regression above.

### 4.2 Small choices closed by the designer

- Node A tests through the role-rules registry, not a new pin (TESTING.md:93). The anchors are listed in A-6.
- "missing: none" in place of an empty list (E-C2).
- The receipt count comes from `mechanisms`, not `observed` (E-C4).
- Each NOTE line names one capability, so many unknowns give many short lines, not one cut line.
- One changelog fragment per node, in the shape of `changelog.d/oh5-9-publish-path.md`.
- Node B carries three refs (`/code_repos`, `/app_root`, `/protected_app_paths`), because P4:358-364 writes the three
  keys together, and `resolve` then refuses a half answer (E-B2).
- The new P4 paragraph goes in step 8, beside its two siblings, and step 1 points to it (B-1).
- In A-4 the S8 dispatch names the relative `bugs/BUG-<n>.md` (the card's `--path` form), not an absolute path.

---

## 5. Reading trail

Read (origin/main, `.claude/worktrees/read-main`):
- the two node findings and the SC5-13 finding (`findings/20261031-...visyat-do-konca.md`);
- batch-2 rows :29-39 and batch-4 rows :40-49;
- `references/common-rules.md:100-119`;
- `references/external-writes.md:35-52`;
- `references/templates/test-report.md:25-44`;
- `scripts/driver_stage_s8s9.py:260-289`;
- `scripts/artifact_producer.py:220-259`;
- `agents/qa-bug-reporter.md:45-71`;
- `scripts/tests/test_brief_pack_roles.py:295-334`;
- `scripts/external_writes.py:624-660, 880-907`;
- `scripts/hooklib.py:169-172` (and grep for `artifacts_dir`);
- `scripts/delivery_summary.py:85-104`;
- `scripts/bug_records.py:1-30`;
- `references/role-load.json` (whole);
- `scripts/role_load.py:255-286, 419-453`;
- `references/inject-map.json:90-119`;
- `design/role-rules.json:1-4`;
- `scripts/role_rules.py` (grep);
- `scripts/form_selftest.py:225-254`;
- `scripts/report_facts.py:4355-4389`;
- `scripts/selftest.py:354-401`;
- `skills/qa-onboarding/phases/p4-generate.md:40-91, 130-141, 172-187, 290-375, 395-434, 580-624`;
- `scripts/tests/test_onboarding_markers.py` (whole);
- `scripts/project_decisions.py:267-306, 400-493` (and grep of the argparse block);
- `scripts/audit_factory.py:766-830, 897-936`;
- `scripts/tests/test_project_decisions_doc_ref_form.py:100-124`;
- `scripts/readiness.py:1240-1431` (and grep);
- `scripts/host_capabilities.py:53-125`;
- `scripts/driver_s0.py:2340-2409`;
- `scripts/gate_brief.py:2236-2265`;
- `skills/qa-story/phases/s0.md:245-304, 404-412`;
- `references/human-questions.md:1-64`;
- `docs/TESTING.md:36-115`;
- `plans/builder-rules.md` 7b (grep);
- `docs/SIBLING_MAP.md` axes 8, 17, 18, 31, 34 and the axis list;
- `scripts/tests/test-layers.json` (rows of the named tests, the quarantine head, cohorts);
- `scripts/tests/fixtures/judgment-census.json:1-25` and grep.

Negative claims and their controls:
- `qa-factory/bugs` in DECISIONS.md: 0 hits; control `D-00\d\d` = 23.
- `receipts so far|did not ask` in readiness/driver_s0/host_capabilities: 0 hits, case-insensitive; the same call hit `note` lines.
- `comes first|task root>/bugs` in role-rules.json: 0 hits, case-insensitive; control `still in focus` = 1.
- `project:bugs` in contract_slices.py: 0 hits; control `project:|digest` hits :40, :299.

Needed beyond the manifest: `scripts/external_writes.py`, `scripts/delivery_summary.py`, `scripts/bug_records.py`,
`scripts/host_capabilities.py`, `scripts/driver_s0.py`, `scripts/gate_brief.py`, `skills/qa-story/phases/s0.md`,
`scripts/audit_factory.py`, `scripts/role_rules.py`, `design/role-rules.json`.
