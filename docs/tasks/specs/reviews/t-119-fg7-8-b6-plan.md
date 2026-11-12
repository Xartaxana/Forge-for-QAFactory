# t-119 — critic on the plan: §3.7, node B6, fork F12 and the B1 consumers (`factory_origin`, `vcs_changes`)

Spec: `docs/tasks/specs/fg7-8-b-vcs-words.md` (lines 61-63, 102, 285-303, 473-475, 653-673, 687, 710). Narrow scope as
dispatched; the rest of the spec is not re-reviewed. Critic (Opus), 12.11.2026.

**Verdict line: NEEDS WORK (`fit_with_fixes`) — 4 blocking findings (B-1..B-4), 1 fact correction (F-1), 6 non-blocking
fixes (m-1..m-6).** Two of the blockers are the forbidden direction (a person's change classified "factory") with
concrete inputs; one is feasibility on the skill road; one is whether the mechanism delivers OW-2 at gate A at all and
needs the owner's reading. Every blocker carries a proposed text the Lead can write in as is. The decision to accept,
re-fork F12 or ask the owner is the Lead's (rule 6).

---

## Q1 — Facts: is F0-30 true, and would an existing carrier do?

**F0-30, hook part: TRUE.** PostToolUse `Write|Edit` in `hooks/hooks.json:66-75` runs only `validate_artifacts.py`;
the other PostToolUse entries are `cost_capture.py --debounced` (`:56-64`, async, matcher ""), `host_probe.py --hook`
(`:76-85`, Bash/PowerShell; it reads only `tool_input.command`/`cmd`, `host_probe.py:125-137`), `agent_autobind.py`
(`:86-95`). In `hooks/codex.json` PostToolUse `.*apply_patch|Write|Edit` runs `validate_artifacts.py` (`:26-35`) and
`host_probe.py --hook` (`:57-66`, commands only). Case-insensitive Grep for `file_path|tool_input` over
`telemetry_hook, telemetry_capture, host_probe, cost_capture, validate_artifacts` finds no writer of a write record
(positive control in the same call: `validate_artifacts.py:2764`, `cost_capture.py:1327` hit).

**F0-30, content part: PARTLY FALSE — finding F-1.** "`tests[].file` ... without a whole-file hash" is wrong:
`manifest_from_tests.py:309` computes `content_sha = sha256(raw bytes)` and writes it into each row's
`trace_binding.test_content_sha` (`:1380`, `:1488`); `proof_level.py:505-508` fixes the meaning ("the raw sha256 of the
test file"), `proof_level.claimed_test_sha` (`:585-592`) reads it. (The designer's Grep was of `manifest_put.py` only;
the row's binding is written by `manifest_from_tests.py`.) Consequence: F12 option (b)'s stated defect — "no hashes ...
a hand-edited factory test would read as the factory's and be hidden" (spec `:687`) — does not hold: with
`test_content_sha` a hand edit gives a mismatch → person. F12 = (a) may still be right, but on other grounds (b covers
test bodies only, bound at manifest build, and only from S5 on — and it has the same laundering defect as B-1). The
Lead re-states F12's reason with the true fact (fix text below, F-1).

A third existing carrier the spec does not name: the host transcripts. Every subagent Write/Edit, with its
`file_path` and (for Write) whole content, is in `subagents/agent-*.jsonl` (`hooklib.story_subagent_transcripts`,
`hooklib.py:2270-2295`; `cost_capture.py:1327` already reads `tool_use` `file_path`); they also separate a subagent's
writes from the orchestrator's — the thing B6 cannot do on the skill road (B-3). Their docstring calls them
"best-effort ... never a source of truth" and they are host-specific (AR-5, axis 14); error direction when missing:
person (safe). Named as an alternative for the Lead, not recommended over (a)-fixed.

**Alternatives and their error direction:**

| Alternative | Rule | Error direction | Verdict |
|---|---|---|---|
| S0 base alone (`test_repo_base`, `:214-272`, `:264`) | "not in S0 `dirty`, dirty now → factory" | the person's edit DURING the story (any path clean at S0) → **factory**: the forbidden direction. The base says when, not who. | unfit |
| `test_novelty`'s "new in this story" | built on the same S0 base (`test_novelty.py:259-279`, `:544-560`) | same as the row above | unfit |
| manifest `trace_binding.test_content_sha` (F12 b, corrected) | current sha == bound sha → factory | helpers/config unseen → person (safe); a person edit made BEFORE the binding is absorbed (B-1 class) → factory (forbidden) | same defect as (a), smaller coverage |
| window claims (`window_files.py`) | claim exists → factory | test bodies only, released at window close, no content (F0-30 holds here) | unfit |
| host transcripts | a subagent Write/Edit of the path → factory | missing transcript → person (safe); Edit content is a diff, so the same B-1 class unless the pre-image is read | possible, host-bound |
| B6 record (F12 a) as specified | last row sha == current → factory | B-1, B-2 (forbidden) | fixable |

---

## Q2 — Feasibility of B6

**B-3 (blocking): the story/role attribution exists on the driver road only, and B6 leaves the function to the
builder.** B6 says "resolved as `guard_pre_tool` resolves the story for `window_file_check` — not verified, the builder
names the function" (spec `:662-663`; §6 `:710`). What that resolution actually is:
- `window_file_check` (`guard_pre_tool.py:1557-1606`) returns at once unless `dispatch_identity.named()` is set
  (`:1580-1582`); `named()` reads the env `QA_FACTORY_DETECTOR_DISPATCH` / `QA_FACTORY_DRIVER_RUN`
  (`dispatch_identity.py:21-33`), which the DRIVER sets for the child it launches (`dispatch_identity.py:7`; axis 33
  `docs/SIBLING_MAP.md:575`). Then it maps the name to a story by globbing every controller (`_sessions_of`, `:1526-1554`,
  `DI.own`, `:1509-1515`). That works on the driver road.
- On the skill road the roles are subagents inside the person's own Claude Code session: no env name. The other
  resolver, `dispatched_role` (`:1147-1176`), finds the story from an ARTIFACTS path in `file_path` (`_STORY_RE`,
  `:1155-1158`) — a test file in the person's repository carries no story id, so it answers "". And per its docstring
  "A PreToolUse event does not name the agent that caused it — `agent_type` arrives on SubagentStop and nowhere else"
  (`:1150-1151`; `hooklib.subagent_type`, `hooklib.py:779-789`, is a SubagentStop reader). No package code reads any
  per-subagent field of a PostToolUse Write/Edit event (case-insensitive Grep `originalFile|tool_response|structuredPatch`
  over `scripts/`: only Agent-tool `tool_response.agentId` readers, `agent_autobind.py:93`, `host_dispatch.py:255`).
- So on the skill road B6 can either record nothing (OW-2 lives on one road only — P31 / axis 34, which says such a
  gap "is a fork to the Lead and the owner, never a fact", `SIBLING_MAP.md:589`) or attribute by "a running dispatch
  exists" — which also catches the orchestrator's writes (B-2).
- Codex host: `hooks/codex.json` is not in B6's owns; its PostToolUse matcher `.*apply_patch|Write|Edit`
  (`codex.json:27`) is where the sibling entry would go, and an `apply_patch` carries several files through
  `host_adapter.normalize` (`host_probe.py:126-128` reads events through it). Not named either way.

**Bash, orchestrator, test-run by-products.** "Reads as the person's" is the allowed direction for every file nobody
recorded: Bash generators/formatters (`prettier --write`, `black`, codegen), `git mv` (a rename: rule 3 → person),
`rm`/`git rm` by a role (` D` → person, and commit/stash would take the factory's deletion under the person's word),
snapshots, `test-results/`, `playwright-report/`, coverage files that the project does not ignore. None of these is
the forbidden direction. They make the question noisier and push the person list over the F10 cap (20) — then
commit/stash are not offered at all. That is a usability cost, not a blocker; the spec must SAY it (m-5). The
orchestrator is the exception: see B-2 — its writes are not by-products but possibly the person's own requests.

---

## Q3 — Error direction of `factory_origin` rules 1-3

**B-1 (blocking, forbidden direction): rule 2 compares only the bytes AFTER the last factory write, so a person's
change made before a factory Edit is laundered into "factory".** The Edit tool replaces a string inside whatever the
file holds; the row's sha then covers the person's bytes too. Concrete inputs:
1. S0: `tests/conftest.py` clean (not in `dirty`). The person adds a fixture to it during the story (uncommitted).
   S5 automator `Edit`s `conftest.py` (adds an import) → row `{path: "tests/conftest.py", sha256: S}`, S = person's
   fixture + factory's import. At the next gate A (the reapprove path, `s6.md:36-37`, or any later reader): rule 1 no,
   rule 2 sha == S → **factory**. The fixture is not shown and not taken by `commit`/`stash`.
2. The automator `Write`s `tests/test_login.py` (sha A). The person hand-edits it (sha B). S6 rework: the role `Edit`s
   it (sha C, containing the person's edit). Rule 2: C == last row → **factory**. The spec's own "a sha mismatch (a
   hand edit after the factory's write) → person" (`:294`) is defeated by the very next factory write.
3. A truncated base (`dirty_truncated`, more than `DIRTY_LIMIT = 2000` paths, `test_repo_base.py:65`, `:263-268`):
   `tests/helpers.py`, the 2001st dirty path, holds the person's pre-S0 edits; a role `Edit`s it; spec `:296-297` sends
   it to rule 2 explicitly → sha matches → **factory**. "Changes nothing in rule 1's direction" is the wrong conclusion:
   it moves the path into the unsafe rule.
Neighbouring classes walked on the same surface (the sha comparison): line endings (autocrlf) — git does not rewrite
the worktree unless the person checks out/stashes; any rewrite changes the sha → person (safe); "the person edits a
factory file and reverts to identical bytes" → factory, and the bytes are the factory's (correct, not a violation);
a role rewriting a file dirty at S0 → rule 1 person (correct when the base is not truncated); a resumed story — the
record is append-only under the task root and survives (fine); two stories in one repository — story B reads only its
own record, A's files → person (safe); a misattributed row (wrong story) still marks a factory-written file (not the
forbidden direction); rename — see m-1; Windows path case — the hook's spelling vs git's → mismatch → person (safe).
The defect class is "post-image only": it is closed only by a pre-image.

**Proposed text for §3.7 (replace rule 2 and the truncation sentence):**
> 2. A path is **factory** only when its record rows form an unbroken chain from the repository's own state: the FIRST
>    row's `before` equals the path's state at HEAD (`""` when the path is absent from HEAD; otherwise the sha256 of
>    `git show HEAD:<path>` bytes — through `gate_preflight._git`), every later row's `before` equals the previous
>    row's `sha256`, and the LAST row's `sha256` equals the working-tree bytes now. Any break → person. A row with
>    `before` missing or `"?"` (the pre-image could not be read) breaks the chain.
> A truncated S0 base (`dirty_truncated`) does not weaken this: a path dirty before S0 has a `before` that differs from
> HEAD, so the chain breaks and the path is the person's whether or not the base kept it.

**Proposed text for B6 (record format and how `before` is read):**
> Each row is `{path, before, sha256, at, role, dispatch, story, tool}`; `before` is the sha256 of the file's bytes
> immediately before this write (`""` = the file did not exist, `"?"` = could not be read). Where `before` comes from
> is MEASURED first, one probe, its output in the report: (i) the PostToolUse payload's own pre-image
> (`tool_response.originalFile` on Claude Code Edit/Write — estimate, not verified), else (ii) a PreToolUse entry of
> `factory_writes.py --before` that stores the pre-image sha keyed by `tool_use_id` in
> `<task root>/state/factory-writes.pending/` and the PostToolUse entry joins it. Neither available → `before: "?"`,
> and the row then never makes a path factory (rule 2) — B6 reports that OW-2 is not delivered on that host.

**B-2 (blocking, forbidden direction): "a write by the orchestrator in the person's chat → recorded as the factory's"
(spec `:667-668`).** On the skill road the orchestrator IS the person's Claude Code chat: a person who says "fix the
typo in `src/app.py`" during a story gets an Edit recorded as the factory's → rule 2 → **factory** → their change is
hidden and not taken by commit/stash. Concrete input: skill road, S4 running, person asks the conductor to edit
`src/app.py`; the conductor's Edit lands; at gate A the file is classified factory. On the driver road the orchestrator
is the driver (code, no Write tool) and the conductor session is again the person's chat — same.
**Proposed text for B6 (replace the edge):**
> Only a write attributed to a RUNNING ROLE DISPATCH of a story is recorded (`dispatch_identity.own` returns that
> dispatch; axis 33's direction: None allowed, another dispatch never). A write with no such dispatch — the
> orchestrator/conductor session, the person's own requests in it, a session outside a story — gets NO row: it reads
> as the person's (the allowed direction).

---

## Q4 — Architecture

**B-4 (blocking, feasibility of the goal): at the only moment the reader runs, the current story's record is (by
stage order) empty on a first pass; the plan does not say which factory files OW-2 is about.** `check_vcs` runs only
at gate A (`gate_preflight.py:5783-5791`, beside `check_s5_executor` … `check_s5_runtime_probe`: the environment of
the NEXT stage), and gate A follows S3/S4 (`skills/qa-story/README.md:15`: "S3 Plan … Then it stops: gate A"); the
tests are written in S5. S0-S4 roles write their artifacts under the factory home, which `vcs_changes` already leaves
out. So the factory's own files a person sees at a FIRST gate A are, by this reading, (a) files an EARLIER story left
in the same repository — which rule 1 (dirty at this story's S0) and the per-task record location both classify as
the person's — or (b) S0-S4 role writes outside the home (estimate: few or none; not measured). B6 delivers OW-2 for
(b) and for a REPEATED gate A (the reapprove path `s6.md:36-37`; the c7 repeat of gate A in
`tests/test_decision_classes.py:13`). If the owner meant (a) — plausibly the case that made her say it — the mechanism
as specified never fires for it. This is an interpretation of the owner's requirement: it goes to the owner
(CLAUDE.md rule 11a), not to the builder.
**Proposed text for §3.7 (a paragraph after the rules) and a question for the Lead to take to the owner:**
> When the reader runs: gate A only, before S5. On a first pass the story's own record holds only S0-S4 writes outside
> the factory folder; the factory's files a person sees then are mostly an EARLIER story's. Owner question (Lead):
> "Files the factory left in your repository from an earlier story — are they 'the factory's' (not shown, not taken by
> commit/stash) or 'yours' (you decided to keep them)?" Until her word: they stay the person's (the allowed side), and
> B6 is built as below. If she says "the factory's": the record moves to the project level
> (`qa-factory/state/factory-writes.jsonl`, `story` in every row), and rule 1 yields to an unbroken chain (rule 2) of
> an earlier story's rows — a new node, critic on the plan for that rule.

**AR-by-AR:**
- **AR-12 (friction).** One synchronous Python process per Write/Edit of EVERY session, most of them artifact writes
  under the factory home. The spec says "measured" (`:672`) without a measurement. m-3.
- **AR-13/14.** One writer (`factory_writes.record`) and one reader (`gate_preflight.factory_origin`) are named; the
  `artifact-writers.json` row is in owns (`references/artifact-writers.json` is `{artifacts: {path: {writer, why}}}`,
  read). The appender must be `hooklib.append_jsonl_line` (axis 29, `SIBLING_MAP.md:456`: "a new jsonl writer calls it
  and never re-implements the rule") — not named in B6. m-2.
- **AR-22.** Producer (B6) and reader (B1) land in separate nodes; the both-worlds statement exists (F12 note
  `:687`: no record → everyone is the person's). Acceptable.
- **AR-28.** An unreadable record/line → person (`:293`): no unknown becomes a pass. Holds, after B-1's "?" rule.
- **AR-29.** `factory_origin` compares bytes and rows — data, not meaning; census class "data" (`:170`). Holds.
- **FR-45.** The recorder is a separate script after `validate_artifacts.py`; the validator still writes nothing.
  Holds.
- **FR-53/P8.** The record lives in the task root under the factory folder, the same class as every other artifact of
  a no-trace run; it writes nothing in the person's tree. Holds.
- **P2/AR-4.** The hook's path is project-relative (`window_files.project_rel`, `window_files.py:59-74`, None outside
  the project); the rows must be top-relative (spec `:291-292`). A project in a repository subfolder needs the prefix;
  a tests root in ANOTHER repository (`other_repository`, `test_repo_base.py:236-244`) lies outside the project → no
  row → person (safe, but OW-2 absent for that layout). Unnamed. m-4.
- **AR-5 / P31.** Codex wiring and the skill road: B-3.
- **Smallest mechanism?** With B-1's pre-image it is the smallest carrier that has the right error direction; the
  corrected manifest (F-1) is smaller but covers test bodies only and has the same laundering class. Yes, with fixes.

**Owns gaps (m-6):** `hooks/codex.json` (or an explicit, owner-routed non-goal per axis 34); `host_capabilities.py:71-72`
`inspect`'s `expected` set of hook scripts (a hook not in it is never shown as verified on a host); a
`scripts/tests/test-layers.json` row if the B6 test part is new; `test_hooks_wiring.py` needs no row (it iterates every
entry, `test_hooks_wiring.py:47-55`, `:72-74` — the "one row" in owns is a no-op; keep the file in owns only if a
B6-specific assertion is added). Install smoke / release fingerprint: no owned change needed (the fingerprint is
rebuilt at release, PROJECT.md «Релиз»).

---

## Q5 — B6 as a node for a weaker model (PROJECT.md «Командная работа» p. 11)

Named: file, the two functions, hook placement, three test rows, DoD command. Left for the builder to invent: the
attribution function and its skill-road behaviour (B-3, "the builder names the function"); the pre-image (B-1); the
top-relative conversion (m-4); the appender (m-2); the cost measurement (m-3). B-3's text below closes the first.

**Proposed text for B6 (attribution, replace `:662-663`):**
> Attribution, per road: (1) driver road — `dispatch_identity.named()`; the story is the one whose controller holds
> that dispatch running (`guard_pre_tool._sessions_of`'s glob over `artifact_root(event)/*/state/controller.json` with
> `dispatch_identity.own(dispatches, name=...)`, any role and stage, not only S5 automator). (2) skill road — FIRST a
> probe, its output in the report: does a PostToolUse Write/Edit event fired inside a subagent carry the subagent's
> identity (`agent_id`/`agent_type` or a host field)? Yes → join it to the running dispatch of that role; no → no row
> on the skill road, and B6's report says "OW-2 is driver-road only on this host" — the Lead opens that as a P31 fork
> to the owner (axis 34), never as a silent non-goal. (3) Codex (`hooks/codex.json`) — the same entry on its
> `.*apply_patch|Write|Edit` matcher, events read through `host_adapter.normalize`, one row per file of a patch; or the
> Lead names Codex out of scope with the same P31 fork. Ambiguity (two candidate dispatches) → no row.

Tests per item (proposed, add to B6's "Tests"): a driver-road role Edit appends a row with `before`/`sha256`; an Edit
over a person's mid-story change appends a row whose `before` ≠ the previous row / HEAD (and `factory_origin` → person,
B1's table); a session with no running dispatch (orchestrator) → no row; a skill-road event with no subagent identity
→ no row; under the factory home / outside the project / no story → no row (as specified); a broken record directory →
exit 0, no row (as specified); a path in a subfolder project → top-relative key.

B1's `factory_origin` table (spec `:473-475`) gains: Edit over a person's mid-story change → person; truncated base +
Edit of an un-kept dirty path → person; `before: "?"` → person; chain break between two factory rows → person.

---

## Non-blocking fixes

- **m-1 rename.** Rule 3 says "a rename unless BOTH sides are factory" (`:294`), but the old side of a rename does not
  exist in the worktree, and "a deleted file (no current sha)" is person by the same rule — so "both sides factory" is
  unreachable. Write "a rename → person" (or define the old side as "absent now and recorded as the factory's own
  creation"). Text: "a rename (`R`/`C`, either side) → person."
- **m-2 appender.** B6 `record` appends through `hooklib.append_jsonl_line` (axis 29); no private appender.
- **m-3 AR-12.** Name the cost: the hook returns before any import beyond the standard library and
  `dispatch_identity` when the path is under the factory home or outside the project (the common case); a hot-path
  part in the style of `test_cost_capture_hot_path.py` K12 (`:528-546`) asserts it; synchronous (an async hook hashes
  bytes at an unknown later moment, possibly after the person's next edit).
- **m-4 path key.** The row's `path` = project-relative (`window_files.project_rel`) prefixed by the S0 base's
  `repo_prefix` (`test_repo_base.load`), never a sixth git-top reader (axis 10). `other_repository: true` → no row,
  stated as the allowed side.
- **m-5 by-products.** §3.7 states: Bash-written, test-run and formatter output reads as the person's; it can push the
  person list over the F10 cap (then only `go on`/`accept`); B6's report counts such entries on one real run's tree
  (or the stand) so the Lead sees the noise.
- **m-6 owns.** As listed under Q4.

## F-1 fact correction (for the Lead to write into §0 and §5)

> F0-30 (corrected): ... `automation-manifest.json` rows carry `trace_binding.test_content_sha`, the raw sha256 of the
> test file when `manifest_from_tests.py` built the row (`manifest_from_tests.py:309`, `:1380`, `:1488`;
> `proof_level.py:505-508`, `:585-592`); helpers are not listed; the binding exists only from S5 and is not refreshed
> by later writes. F12 (b) then reads: "the manifest binding plus the S0 base: test bodies only, from S5 on; a hand
> edit after the binding → person (safe); a person's change made before the binding is absorbed (the B-1 class)."

## Standing questions

- **DUPLICATION AND CONSISTENCY:** one risk found — a private jsonl appender (m-2, axis 29). Greps: `sha256|hashlib`
  (case-insensitive) over `scripts/*.py` for existing write-hash carriers (found `manifest_from_tests`, `window_record`,
  `test_source`, `test_repo_base`, `test_novelty`); `file_path|tool_input` over the hook scripts; `validate_artifacts`
  over the package for hook-list siblings (found `codex.json`, `host_capabilities.py:71`).
- **CODE QUALITY:** plan-level only: the node leaves five behaviours to invention (Q5); fixed by the proposed texts.
- **ONE ACTION, ONE ROAD (P31, brief item 12):** B-3 — OW-2 on the driver road only, unless the skill-road probe and the
  Codex wiring land; the exclusion has no data row and no owner word yet → a fork the Lead opens with the owner (rule 6),
  proposed text in B-3.

## Class completeness (SIBLING_MAP)

Axis 33 (dispatch_identity — B6 must read through `own`, direction None-allowed): named in B-3's text. Axis 29
(appender): m-2. Axis 10 (git-top readers): m-4. Axis 34 (one road): B-3. Axis 14 (transcript readers): only if the Lead
picks the transcript alternative. Axis 3 (package ↔ release copy): no change needed. Beyond the map: none requested.

## Trail

Read: the spec lines 1-120, 280-360, 460-490, 640-719; `hooks/hooks.json` (whole); `hooks/codex.json` (whole);
`scripts/test_repo_base.py` (whole); `scripts/guard_pre_tool.py:1140-1199`, `:1500-1620`; `scripts/dispatch_identity.py`
(Grep `named|environ|ENV`, :4-33); `scripts/hooklib.py:779-789`, `:2270-2295`; `scripts/window_files.py:59-89`;
`scripts/window_record.py:805-834`, `:1290-1319`; `scripts/manifest_from_tests.py:295-369` + Grep `test_content_sha`;
`scripts/proof_level.py:519-531`, `:585-592`, `:727-747`; `scripts/story_step.py:840-885`;
`scripts/gate_preflight.py:5776-5795` + Grep `check_vcs`; `scripts/host_probe.py:120-149`;
`scripts/host_capabilities.py:60-84`; `scripts/tests/test_hooks_wiring.py:1-110`;
`references/artifact-writers.json` (structure); `skills/qa-story/README.md:15`, `phases/s6.md:36-37` (Grep);
`docs/SIBLING_MAP.md` axes 10, 29, 33, 34. Greps (case-insensitive where content-negative): `sha256|hashlib` over
`scripts/*.py` (positive: 2313 hits); `originalFile|tool_response|structuredPatch` over `scripts/` (positive control in
the same call: `agent_autobind.py:93`); `file_path|tool_input` over the hook scripts (positive: `validate_artifacts.py:2764`);
`codex|host adapter|^## ` over SIBLING_MAP. Reruns: none (a plan review; no mechanical layer attached or owed).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 forbidden direction: factory_origin rule 2 compares only the post-write sha of the last row, so a person's change made before a factory Edit is absorbed and classified factory (inputs: person edits clean-at-S0 tests/conftest.py mid-story then the automator Edits it; factory Write, person hand-edit, factory rework Edit; truncated S0 base plus Edit of an un-kept dirty path, which spec 296-297 routes to rule 2). Fix: a pre-image chain (before field per row, chain from the HEAD state), text in the review Q3.",
    "B-2 forbidden direction: B6 edge records the orchestrator's writes in the person's chat as the factory's; on the skill road a person's own request to the conductor to edit src/app.py is then hidden from commit/stash. Fix: record only writes attributed to a running role dispatch via dispatch_identity.own; no dispatch, no row.",
    "B-3 feasibility and P31: the attribution the spec points to (window_file_check) needs dispatch_identity.named(), an env name only the driver sets (dispatch_identity.py:7,21-33); on the skill road no resolver can attribute a write outside the artifacts folder (guard_pre_tool.py:1150-1158; hooklib.subagent_type is a SubagentStop reader); hooks/codex.json is not in owns. The node leaves the function to the builder. Fix: per-road attribution text with a skill-road probe and an owner-routed P31 fork if it fails, text in the review Q5.",
    "B-4 goal feasibility: check_vcs runs only at gate A (gate_preflight.py:5783-5791), before S5 writes tests (README.md:15); on a first pass the story's own record is empty or near-empty, and an earlier story's leftover files are classified person by rule 1 and by the per-task record. Which files OW-2 means is the owner's reading (rule 11a). Fix: the timing paragraph and the owner question in the review Q4; until her word the leftovers stay the person's."
  ],
  "fixes": [
    "F-1: correct F0-30 and F12 (b): automation-manifest rows carry trace_binding.test_content_sha, the raw test-file sha256 (manifest_from_tests.py:309,1380,1488; proof_level.py:505-508,585-592); re-state why (a) beats (b).",
    "m-1: rule 3 rename clause is unreachable (the old side has no current sha); write 'a rename (R/C, either side) is the person's'.",
    "m-2: factory_writes.record appends through hooklib.append_jsonl_line (axis 29).",
    "m-3: name the AR-12 cost: early return before heavy imports for paths under the factory home or outside the project, a hot-path test part like test_cost_capture_hot_path K12, synchronous hook.",
    "m-4: row path = window_files.project_rel prefixed by the S0 base repo_prefix; other_repository gives no row, stated as the allowed side; no new git-top reader (axis 10).",
    "m-5: state in section 3.7 that Bash, formatter and test-run by-products read as the person's and can push the list over the F10 cap; B6 reports a count on one real tree.",
    "m-6: owns: hooks/codex.json (or an owner-routed P31 non-goal), host_capabilities.py inspect expected set, a test-layers row if the test part is new; the test_hooks_wiring row is a no-op (it iterates all entries)."
  ],
  "class_completeness": "Axis 33 (dispatch_identity.own, None-allowed direction) named in B-3; axis 29 (one jsonl appender) m-2; axis 10 (git-top readers) m-4; axis 34 (one road, P31) B-3 with an owner fork; axis 14 only if the transcript alternative is chosen; axis 3 no change. Defect class of B-1 named as post-image-only comparison; neighbouring classes walked: autocrlf, revert to identical bytes, S0-dirty rewrite, resume, two stories, rename, path case.",
  "trail": {
    "read": [
      "docs/tasks/specs/fg7-8-b-vcs-words.md:1-120,280-360,460-490,640-719",
      "ai-packages/qa-factory/hooks/hooks.json",
      "ai-packages/qa-factory/hooks/codex.json",
      "ai-packages/qa-factory/scripts/test_repo_base.py",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py:1140-1199,1500-1620",
      "ai-packages/qa-factory/scripts/dispatch_identity.py:4-33",
      "ai-packages/qa-factory/scripts/hooklib.py:779-789,2270-2295",
      "ai-packages/qa-factory/scripts/window_files.py:59-89",
      "ai-packages/qa-factory/scripts/window_record.py:805-834,1290-1319",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py:295-369,1380,1488",
      "ai-packages/qa-factory/scripts/proof_level.py:505-531,585-592,727-747",
      "ai-packages/qa-factory/scripts/story_step.py:840-885",
      "ai-packages/qa-factory/scripts/gate_preflight.py:5776-5795",
      "ai-packages/qa-factory/scripts/host_probe.py:120-149",
      "ai-packages/qa-factory/scripts/host_capabilities.py:60-84",
      "ai-packages/qa-factory/scripts/tests/test_hooks_wiring.py:1-110",
      "ai-packages/qa-factory/references/artifact-writers.json",
      "ai-packages/qa-factory/skills/qa-story/README.md:15",
      "ai-packages/qa-factory/skills/qa-story/phases/s6.md:36-37",
      "docs/SIBLING_MAP.md axes 10, 29, 33, 34"
    ],
    "reruns": []
  }
}
```
