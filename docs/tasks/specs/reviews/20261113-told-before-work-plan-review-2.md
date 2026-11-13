# Critic RE-PASS on plan: "told before the work" mechanism spec after the fix round (13.11.2026)

Under review: `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md`, its "Fix round 13.11" table and the sections that
table names. Against: the first verdict `reviews/20261113-told-before-work-plan-review.md` (B1-B6, N1-N14, K9), the Lead decisions
in plan §16 (`20261113-plan-fabrika-ne-huzhe-agenta.md:494-`), and F12/F13/F14 = (a). Package facts come ONLY from the read-main
worktree `.claude/worktrees/read-main/ai-packages/qa-factory/` (written `pkg:` below). This is a plan: no code exists. The
mechanical layer is fact checks by Read/Grep/sed and one measuring script (trail at the end). I did not re-review what the first
pass found fit.

## Verdict in short

The B1 decision is right. The key page is the one carrier the role gets WHOLE with no action of its own. I verified this on the
hook road and on the driver road, in both slice modes once F12 (a) lands, and on Codex too. It has one renderer (`told_text`) and
one reader of rows (`load_rows`/`row_for`/`rows_for`). Role-rules is joined by id and hand prose is not a K2 leg. B2-B6 are fixed
as asked, with two small residues.

Four findings still block, each with a small fix:
- the dispatch-kind section drop (`kinds.drop_sections`) can still cut the new page section;
- the page has no size decision: there is no split rule when K8 goes red, and the Codex 100000-character total ceiling is not
  named, though the automator is already close to it;
- dispatch-only row groups that exclude each other are resolved only through the brief, which is the very road the survivor rule
  rejects;
- T4 and T5 have no drafted requirement sentences. This is the N9 class, fixed for T7a, T7b-f and T9 but not for these two.

---

## R1 — THE SURVIVOR (B1)

### Delivery, road by road (fact checks)

| Road | Carrier on read-main | Page reaches the role before work? |
|---|---|---|
| First dispatch, hook (Claude Code `Task`/`Agent`) | `pkg:scripts/inject_context.py:606-747`: `dispatch` → `collect_blocks(role, imap, event, dispatch_kind(last))` `:676`; the blocks are appended to `ti["prompt"]` `:732` (the user prompt of the subagent) | yes, whole (`:256-286`) |
| First dispatch, driver (`claude -p --agent`) | `pkg:scripts/driver_dispatch.py:213-281` `system_file` → the same `collect_blocks` `:235`; passed as `--append-system-prompt-file` (`pkg:scripts/driver_runner.py:570-571`); call site `driver_dispatch.py:706-707` | yes, whole, as the appended system prompt |
| Rework / repair dispatch (a new dispatch) | same two roads; `kind = dispatch_kind(record)` (`inject_context.py:137-151`) → `delivered_text` drops the sections named by `inject-map.json` `kinds.<kind>.<role>.drop_sections` (`:164-196`, `:279`). The "never cut" set is `common` + `COMMON_LAYER_SUBJECTS` (`:172`, `:226`) | **yes today, but only by data**: the kinds table drops nothing from `handoff-keys.md` today (`inject-map.json:7-18`: one repair row, two `execution-lifecycle.md` headings). Nothing stops a future row dropping `## What code will check of you` for a repair, and F12 (a) explicitly leaves the "kinds drop rules unchanged" (§9 F12). **Blocking finding B1** |
| Resumed role, hook road (`SendMessage`) | `inject_context.py:621-625`: no re-injection, "the agent already carries its injected context"; the first injection went into the user prompt, so it stays in the transcript | yes (it carries the first dispatch's page) |
| Resumed role, driver road, Codex | `driver_runner.py:611-639` `host_prompt`: a fresh session gets the rule layer inside the FIRST stdin message; a resume gets "the prompt alone: the thread already holds its role". The layer is in the thread's history | yes |
| Resumed role, driver road, Claude | every role resume calls `run_claude(..., resume=sid)` with NO `system_file` (`driver_dispatch.py:546-547, 575-576, 1035, 2078-2079`; `driver_machine.py:548`), and `claude_cmd` passes `--append-system-prompt-file` only when given (`driver_runner.py:570-571`) and drops `--agent` on resume (`:568`). The page lived in the appended system prompt of the first call | **estimate, not verified**: whether `claude -p --resume` re-applies an earlier call's appended system prompt is a host property no carrier states. If it does not, every role resume (resume_structured, resume_repair, handoff resumes, the person's-answer resume) runs without the page. These are exactly the moments when the role is told it broke a check. Non-blocking N1: one experiment in T0 (CLAUDE.md pt.6a) |
| Codex hook road (native packet) | `inject_context.py:718-731` → `native_context.stage` (`pkg:scripts/native_context.py:173-206`) → `deliver` at SubagentStart (`:209-263`) | yes, whole, with two inherited roads: (1) `len(context) > 100000` → `ValueError` → the role is refused (`native_context.py:174-175`), see R2; (2) an ambiguous child (several pending packets, or none matching) gets NO context at all (`:232-244`), said to the person |
| `on_demand` mode | `inject_context.py:245-255`: every `plugin:references/slices/` entry except `COMMON_LAYER_SUBJECTS` is replaced by the `index.md` path list. F12 (a) adds `KEYS_NAME` to a new `INLINE_SUBJECTS` used by `named_instead` | yes after F12 (a). `catalogue()` already never lists the key page: `targets()` skips it (`contract_slices.py:69-70, 618-622`). A sibling of the same set is not moved: the on_demand weight report (`contract_slices.py:739-752`) still counts the key page as "named instead", so the printed saving overstates by the page's bytes. N2 |
| Hook fail-open | `inject_context.py:526-551` main: any crash after the receipt ALLOWS the dispatch with a `hook_signal` (owner's residual F-9/F-11); docstring `:30-32`: a host without `updatedInput` degrades to no injection | no page in these cases. Inherited by every injected rule, owner-accepted, signalled. Name it in §3 as a known road (N3) |

The roads by which a role starts work WITHOUT the page, as the DoD asks:
1. a future `kinds` row that drops the section (B1);
2. the Codex total over 100000 characters, where the role is refused rather than started (R2/B2);
3. the Codex ambiguous child;
4. the hook fail-open crash and a host without `updatedInput`;
5. (resume, not start) the Claude driver resume, unverified.

Roads 3 and 4 are inherited and owner-accepted. Roads 1 and 2 are new exposure created by putting the requirement text on the page.

### Architecture (AR-13/14/15, P31)

- One carrier: the page (§2.0, §2.6). The brief keeps no copy of a requirement: T3 removes `ahead_card`/the ahead section
  (`pkg:scripts/brief_pack.py:4344, 4425-4426`).
- Two leftover hand texts in the brief are not named:
  - `FIRST_LOOK_AHEAD` (`brief_pack.py:3849`) disappears with the ahead section. It is not in `ahead-cards.json`, so
    `### Not yet in rows` will not carry it, and `hand_cards` (12) does not count it.
  - `FIRST_LOOK_DOD` (`:3847`, put into the form `:3688`) states what `first_look.py put` refuses.

  Both are requirement texts of one check with no row (N4).
- One renderer: `told_text` serves the page, the refusal and C11 (I-S). The window code file renders `REQUIRED_ROW_FIELDS` through
  the same function (`brief_pack.py:2391`, made a call in T3) and is declared "not a told leg" (axis 28 line). It is a second
  delivery with no second text, so it is acceptable.
- One reader of rows: `load_rows`. But `selftest.py:722` still reads `references/stage-joints.json` directly
  (`_json_carrier(...).get("joints")`), and E6 keeps it. The AR-13 change check in §1.1 ("Grep `stage-joints\.json` over
  `scripts/*.py` minus tests → only `stage_joints.py`") will therefore fail. It also hits the prose at `contract_slices.py:440, 550`
  and `retro_numbers.py:1229, 1290`. Either T1 moves `selftest.py:722` onto `load_rows`, or the check names the exception and
  greps code reads (`_json_of|_json_carrier|read_json|json.load` + the name) (N5).
- The role-rules join by id (K7) is fit. Hand prose is never a K2 leg (K2 text, §1.2). The exception is the 9 legacy legs: 4 of
  them are `agents/<role>.md` hand prose and stay as told legs while counted in `legacy_legs`. F13 (a) says "re-legged later by the
  nodes that own their checks" without naming the nodes. Per rule 19 a residual leaves with an owner, so map each of the 9 legs to
  its node (N6).
- The page renderer gains `requirement_section`, and `_keys_outputs` moves onto `load_rows` (B6). That keeps one generator. Fit.

Verdict R1: **sound choice, verified on every road. One blocking hole (B1, the kinds drop) and one unverified resume road (N1).**

## R2 — SIZE

Facts:
- `MAX_BLOCK_CHARS = 26000` per injected file (`inject_context.py:45`). An over-size file RAISES, and the dispatch is refused on
  the hook (`:267-277, 680-685`) and on the driver (`driver_dispatch.py:236-241`).
- The Codex native packet refuses a whole context over 100000 characters (`native_context.py:174-175`): role block + every slice
  + project files + packet.
- Today's key pages measure 3460-6626 bytes (`wc -c references/slices/*/handoff-keys.md`; max qa-test-strategist 6626).

What the spec decides:
- K8 makes a page over `MAX_BLOCK_CHARS` red at dev time (`contract_slices.keys_findings`, §1.2, E12).
- The page is plugin-generated and project-independent, so a dev-time check is exact for this one ceiling. That honours «потолок —
  фордж» for `MAX_BLOCK_CHARS`.

What the spec does NOT decide (**blocking finding B2**):
1. **What happens when K8 goes red.** There is no split rule. The builder of, say, T7a-7 adds the doc-scribe rows, K8 goes red,
   and the node must invent a road: raise the constant, split the page, or drop rows. Each road has an architectural consequence.
   A second page needs an `inject-map.json` entry and a K2 leg rule. A raised constant is a run ceiling moved by a node. A weaker
   model must not choose. T0 M5 measures only "the would-be automator page section (rows of T4+T5)", not the end state of any
   role. The doc-scribe gets 11 T7a-7 rows plus T4's `*` rows. The automator gets T4 + T5 + T7a-5 + T9.
2. **The Codex 100000 ceiling is not named** (§0.10 lists four ceilings, not this one). It is project-dependent: `project:` files
   are up to 26000 each, so a dev-time check cannot close it. My measurement (script in the trail) of plugin-injected characters
   per role today: qa-automator 46913 + agent file 11084 + `project:…/framework-rules.md` (up to 26000) + the packet. That is
   about 84000 before the packet and before any requirement row. qa-code-critic: 46227 + 12146 + the same project file. A page
   that grows by several KB can push a role with a large project file over 100000 at run time on Codex, and the role is then
   refused (`refuse_native_stage`). That is the case the owner's word forbids, and the spec does not decide it.

Smallest fix:
- **Split rule.** When a page reaches 80 % of `MAX_BLOCK_CHARS`, the requirement section moves to a second generated page
  `references/slices/<role>/handoff-checks.md`. It gets its own `inject-map.json` entry, written by `contract_slices --write`, and
  joins INLINE_SUBJECTS and the never-cut set of B1. K2 accepts either generated page of the role. K8 warns at 80 % and is red at
  100 %, naming the split. Or the Lead picks another split. The point is that the spec decides it.
- **T0 M5.** Measure the projected END-STATE page for every role. The source is the universe's role join, at about 120 B a row
  as a stated estimate.
- **Codex ceiling.** Name it in §0.10. Measure today's worst total per role in T0, from `role_load` plus the largest `project:`
  file the stand has. Decide its owner: either a K8 sibling (plugin part of the total over `100000 − 26000 × project entries`
  is red at dev time), or a pointer to the node that removes the in-run ceilings (amendment B4), named in E12.

## R3 — DISPATCH-DEPENDENT ROWS (F14 (a))

- Do they reach the role before the work? Yes. Every group is on the page under its heading (§2.6), and the page is injected
  whole (R1).
- Is over-inclusion honestly the safe side? Only for ADDITIVE groups (`plan`, `manual`, `walk`: extra rules that do not hold
  this time). It is not for groups that EXCLUDE each other:
  - `first_look` vs `not_first_look`: the spec created `not_first_look` precisely because the first look REPLACES the runner's
    card (`brief_pack.py:4344`). The first-look handoff "is not a run report" (`:4342-4343`).
  - `plan` vs a window dispatch: §5.2 `controller:s5_plan_accept` says "a plan dispatch never closes S5: accepted without
    `--complete`", while a window has its own completion.
  
  A runner that cannot tell it is in a first look reads both groups. It may write the run-report fields, or skip them, the wrong
  way round.
- The ONLY resolver the spec gives is the brief line ("the rules code applies to this dispatch: the sections <names>…", §2.6).
  The brief reaches the role as a path it must open (§0.5; `pkg:scripts/story_step.py:295-300`), which is exactly the road the
  survivor rule rejects. A resumed role is not even given the brief line (`:294-295`).
- The injected packet carries only some of the facts: `purpose` (first look) and `execution_kind` are in `PACKET_DISPATCH_KEYS`
  (`inject_context.py:569-571`), but as raw tokens, never named as the page's headings. `walk` (a walk record on disk,
  `brief_pack.py:4262-4265`) and the S5 plan kind are not projected under those names.

**Blocking finding B3.** For exclusive groups the told leg depends on an action of the role. Smallest fix: put the group line
where the role gets it with no action, and keep one computation.
- `story_step._prompt` (`story_step.py:250-304`) already builds the prompt beside the brief. It takes the group names from the same
  `rows_for(role, stages, dispatch_facts)` call `brief_pack.build` makes (returned with the brief, so there is no second reader of
  the dispatch kind; AR-13 is kept, and F14 (b)'s objection does not apply).
- It also prints them on the resumed prompt.
- The page heading of an exclusive group says which other group it replaces ("### Only in a first look (replaces "Not in a first
  look")").
- A T3 row: for each of the five dispatch fixtures, the PROMPT names the groups.

## R4 — B2-B6

| Finding | Fixed as asked? | Evidence | Residue |
|---|---|---|---|
| B2 cross-process text | yes | §2.0 Text; §2.4: form-1 producers byte-identical, expected/door only via `block`/`deny`/`refuse`; I-R `match_known(spoken(r)) == match_known(str(r))` + no `REPAIR_MARKER`/`PERSON_MARKER` in filled text + `parse`/`split_overridden` equality; T2 (e) runs through `parse` on printed text; E9, E10, T5/T6/T9 "byte-identical" rows. N0 invariant restated in §7 | none |
| B3 controller | yes | §0.4 is true to the code: `controller.py:7465, 7513` `_s3_completion_gate` raises "S3 structured test plan invalid: …"; `driver_dispatch.py:36` `STRUCTURED_RE`, `:89` → `resume_structured`; `REPAIR_MARKER` at `controller.py:6456-6459, 6853-6855`; `RESUMABLE_HEADS` `driver_machine.py:38-39`, `:551-559`; census rows `:171, 181, 182, 190, 195` are all `["conductor"]`. Units are in the universe with rows (§5.2), relabelled in T9 (a), raise named (E17), Q1 rewritten | **N7: T0 M7 cannot find the units it is meant to find.** M7 = "AST: a literal head matching `STRUCTURED_RE`". But `STRUCTURED_RE = r"story_step: refused - S\d structured .* invalid"`, and its prefix `story_step: refused - ` is added by story_step, never written in `controller.py`. No controller literal matches, so M7 under-detects: the wrong error direction for a list that decides the universe. Match the controller-side part `S\d structured .* invalid` (case-insensitive, as `driver_machine.py:444` does). Positive control: `_s3_completion_gate` `:7513`. Negative control: `_decision_problems` `:3203` ("structured test plan invalid", Gate A, conductor road, no `S\d` head) |
| B4 scanner | yes on substance | §2.5: no list-name filter; `sys.exit(<str>)`, `SystemExit(<str>)`, `sys.stderr.write` in WIDE_TRANSPORTS; K6 `untold` defined test-side (§1.2); walk error defined (N4) | N8a: "appends inside a unit the census marks blocking": `sites(raises=spec)` is a package function, and the census is test-only (FR-44), so the spec must say the TEST passes the census's blocking (file, function) set into the spec. Without that set every append in the package counts (834 + 539 + …), and the baseline becomes noise. N8b: §0.9 says "inherited verbatim", but it drops the census header's parenthetical "(a call, a subscript, or `mod.B` where `mod` comes from a from-import of a module)" (`judgment-census.json:3`). Copy it whole, or point T0 at the header as the one carrier |
| B5 stringifying transports | yes | §2.4 `run_guarded` passes a Record whole; `RECORD_SINKS`; `sourced` only through a Record-aware sink; join/str downgrades to `tagged`; T2 (f)(h) rows per sink; `refuse` keeps `stream=` (T2 (g)) | none |
| B6 second reader | yes for `contract_slices` | T1 owns `_keys_outputs`; T1 (i) asserts pages byte-identical; §0.8 lists every reader | `selftest.py:722` stays a direct reader, so the AR-13 change check fails as written (N5, R1) |

## R5 — N1-N14, five spot checks

| N | Check | Verdict |
|---|---|---|
| N3 (E12 corrected) | §0.10 now names `FINDINGS_MAX_BYTES` (`detector_verdict.py:63`), `BRIEF_MAX_BYTES` + ladder + over-budget line, `MAX_BLOCK_CHARS`, `process_ratchet_tokens`; E12 points to FV1-4 / amendment B4; form-1 lines unchanged so findings do not grow | fit, except the native 100000 ceiling is missing (B2) |
| N9 (T7a cut, §5.1) | **names**: all 49 functions of §5.1 exist, each defined exactly once, and `validate_artifacts.py` has exactly 49 `def check_` (count by grep). 0 name mismatches, so the "from memory" worry is unfounded for names. **Sentences**: six bodies sampled against their drafts. `check_run_report_head` (`:1633`) fit. `check_cell_counts` (`:249`) fit. `check_report_coverage` (`:1084`) fit. `check_understanding` (`:1933`) **under-states**: the draft says "stays within its line limit", but the body also refuses a missing `UNDERSTANDING_SECTIONS` section and requirement ids listed in no "What we verify / What we do not verify" line. `check_manifest_invariants` (`:2215`) **mis-states**: the draft says "written only through `manifest_put.py`, never by hand", a procedure; the body refuses duplicate instance ids, a case in both lists and a repeated repair. `check_context_manifest_v0` (`:2350`) **under-states**: the draft says "lists only what the ticket names", but the body refuses a non-object entry, a `kind` outside `RELATED_KINDS` and an entry with no `source` | fit on names. 3 of 6 sentences under-state, so expect question returns. The clause "the builder verifies each sentence… returns a mismatch as a question" covers it. Better: the designer re-reads every body before dispatch, as the spec already asks for T7b-f (N9b) |
| N12 | T3 (i) removes `CARD_MAX_BYTES` and its check (`test_ahead_cards.py:52, 249`) outright; §2.0 F8 | fit. The same name in `app_card.py:41` and `story_step.py:3157` is a different constant, out of scope |
| N10 | §2.3 import rule, T1 (h) subprocess row asserting the heavy modules are not loaded; `stage_joints.py:33-36` module imports today are `ast, re, sys, Path` | fit |
| N13 | K1 skips `unlabelled`/`unknown`; T1 (b) row; §7 C11/G1 | fit |

## R6 — NODES

- **Owns.** Disjoint or queued: T1 → T3 on `contract_slices.py`; T2/T4 on disjoint functions of `hooklib`/`stage_guard`; T3/T4 on
  `inject_context.py` (T4 relabel only); data merges in the stated queue (§7); census T4 → T9. Fit, with one gap: **T3 (j) "the
  walker accepts `{"page": true}`"** and E6 "T3 enables `page`" need an edit to `stage_joints._told_leg`, which T1 owns. T3 owns
  only `test_stage_joints.py`. Say either "T1 implements the page leg, gated on `contract_slices.requirement_section` existing",
  or add `stage_joints.py (_told_leg)` to T3's owns, queued after T1 (N9).
- **Executable by a weaker model.** T0, T1, T2, T3, T6, T7a-1..7, T9 name file, function, behaviour and test per point.
  T7a-8 and T7b-f defer the sentences to a designer follow-up. Fit.
- **Blocking finding B4: T4 and T5 carry no requirement sentences and no "designer drafts first" clause.**
  - T4 (price rank 1, first to run) gives rows `stages: ["*"]`, `roles: ["*"]`, `when: ["shell"]`, but no `requirement` text
    and no `requirement_from` carrier for the guard refusals. A24 entries carry `refuses` (what is refused, e.g. `PT-direct-test-run`
    `refusal_registry.py`), not what is expected.
  - T5's s5_precheck families, `execution_request:<field>` and 15 `manifest_put` functions are the same.
  
  This is the N9 class: requirement sentences are designer-grade writing (J1 judges them). It is fixed for T7a (§5.1), T7b-f
  ("drafted by the designer in a follow-up draft per node") and T9 (§5.2), but not for T4 and T5. Sweep-the-artifact-first misses
  two neighbours. Smallest fix: the same clause in T4 and T5 (a designer draft §5.3/§5.4 before dispatch, sourced from A24
  `refuses`/`override` and the family code), or draft them now.
- **Designer pass owed by size.** T3 is the largest node: 10 owned files, 10 test points, and the brief_pack queue. It must land as
  one commit only to avoid a world with the requirement in NEITHER carrier. A world with it in both is over-telling and harmless.
  The spec may allow T3a (page section + case-critic page + K8 + F12) → T3b (brief section removal + brief line) to shrink the
  node. Optional (N10). No node needs a designer pass for size beyond B4.

## R7 — Owner questions §10

- **Q1** is true to the code:
  - the role-resumed controller refusals and their two roads are verified (R4/B3);
  - "отказ в запуске роли ещё до её старта" is the `Task`/`Agent`/`SendMessage` hook (`inject_context.py:609-619`);
  - "у дирижёра нет брифа и страницы ключей" holds: the conductor is not a role of `inject-map.json` `roles`.
  
  One caveat follows from N1: "роль видит её на своей странице ключей до работы" is true for the first dispatch. It is unverified
  for the driver's Claude resume, which is exactly where these refusals arrive. Keep Q1, and fix N1 before claiming it to the owner
  for resumes.
- **Q2**: the order T4 → T5 → T6 → T7 → T9 matches §5 and "сотни" is labelled as awaiting T0's number. But "примерно пятнадцать
  узлов билдеров подряд" is wrong on both counts. The builder nodes are T0, T1, T2, T3, T4, T5, T6, T7a-1…8, T7b-f (5) and T9:
  **21**. Many run in parallel (T4/T5/T6, T7b-f), so not "подряд". Restate: "около двадцати узлов, часть параллельно" (N11).

## Duplication and consistency (rule 18)

Found:
- the AR-13 claim vs `selftest.py:722` (N5);
- `INLINE_SUBJECTS` moved for `named_instead` but not for its two siblings, the never-cut set (B1) and the on_demand weight
  report (N2);
- the N9 sentence-drafting fix applied to T7a, T7b-f and T9 but not T4 and T5 (B4);
- `FIRST_LOOK_AHEAD`/`FIRST_LOOK_DOD` hand texts left in the brief (N4).

Grepped: `COMMON_LAYER_SUBJECTS|named_instead|on_demand|slices_mode` over `pkg:scripts` (control: the definition
`contract_slices.py:68`); `stage-joints|stage_joints` over `pkg:scripts/*.py` (control `contract_slices.py:490`);
`CARD_MAX_BYTES` (control `test_ahead_cards.py:52`); `100000|native_context|codex|resume` case-insensitive over the spec (0 hits for
`100000`; control `resume` → 9).

## Code quality (rule 18)

No code under review. Design quality:
- clean split of carrier, renderer and reader;
- I-S and I-R are testable invariants;
- one smell: the page's size has no owner of its growth (B2), and growth is a quantity no row author sees.

## One action, one road (rule 19, P31)

- One road to tell "what code checks": the page. No road is excluded by language or project name.
- The `on_demand` mode no longer forks the road after F12 (a).
- Open: the dispatch-group resolver forks by "did the role open the brief" (B3). This is a fix in this round, not a residual.

---

## Blocking findings

**B1 — the dispatch-kind section drop can remove the requirement section.**
- Where: §2.0, §9 F12 (a) ("kinds drop rules unchanged"), T3 owns `inject_context.collect_blocks` only.
- Why: `delivered_text` cuts any heading `inject-map.json` `kinds.<repair|rework>.<role>.drop_sections` lists for a non-common
  `plugin:` entry (`inject_context.py:164-196`), and `map_problems` accepts such a row (`:199-239`). A data edit can therefore make
  rework/repair dispatches start without `## What code will check of you`. K2 checks only that the page is listed. The owner asked
  for a mechanism later fixes cannot break.
- Smallest fix: `_dropped_headings` and `map_problems` treat `INLINE_SUBJECTS` like `COMMON_LAYER_SUBJECTS` ("never cut"), or at
  least refuse the requirement-section headings. Add a T3 row: a fixture kinds row dropping the section → `map_problems` names it
  and `delivered_text` keeps it.

**B2 — the page's size has no decision.**
- Where: §0.10, E12, K8, T0 M5.
- Why:
  - K8 red at dev time has no next move, so a weaker builder must choose between splitting, raising a run ceiling or dropping rows.
  - M5 measures only the automator's T4+T5 share.
  - The Codex native context refuses a role over 100000 characters (`native_context.py:174-175`). The automator is already about
    84000 with a full-size project file (measured, trail), and that ceiling is project-dependent and unnamed. A growing page can
    block a role at run time.
- Smallest fix:
  - a split rule (second generated page, its inject-map entry, K2 accepting either, K8 warning at 80 %), or another decided road;
  - M5 measures the end state for every role;
  - name the 100000 ceiling: a dev-time sibling check of the plugin share against `100000 − 26000 × project entries`, or a
    dependency on the node that removes in-run ceilings.

**B3 — exclusive dispatch groups are resolved only through the brief.**
- Where: §2.6, F14 (a).
- Why: `first_look`/`not_first_look` and plan/window rows contradict each other. The role learns which group holds only from the
  brief line, a path it must open (`story_step.py:295-300`; not given on resume, `:294-295`). That contradicts the survivor rule
  for those rows.
- Smallest fix: the group line goes into the dispatch prompt built by `story_step._prompt`, from the same `rows_for` result
  `brief_pack.build` computes (no second reader). The exclusive headings name what they replace. Add a T3 row per dispatch fixture.

**B4 — T4 and T5 carry no requirement sentences and no designer-draft clause (N9 class incomplete).**
- Where: §5 T4, T5.
- Why: guard, s5_precheck, execution_request and manifest_put rows need requirement sentences J1 judges. T7a, T7b-f and T9 got
  drafts or a draft-first clause. T4, which runs first, did not. PROJECT.md «Командная работа» item 11.
- Smallest fix: draft §5.3 (T4) and §5.4 (T5) now, or give T4/T5 the T7b-f clause.

## Non-blocking findings (fix in the same round)

- N1 — Claude driver resume passes no `system_file` (`driver_runner.py:568-571`; resume call sites listed in R1). Whether
  `--resume` keeps the earlier appended system prompt is an unmeasured host property (estimate, not verified). Add T0 M9, one
  experiment: a resumed `claude -p` asked to quote a line of its appended page. If it is lost, pass `system_file` on role resumes
  (the driver owner's node), or record it as an inherited road.
- N2 — the on_demand weight report (`contract_slices.py:739-752`) uses `COMMON_LAYER_SUBJECTS`. Move it to `INLINE_SUBJECTS` with
  `named_instead`.
- N3 — name the inherited no-context roads in §3: hook fail-open (`inject_context.py:526-551`), no `updatedInput` (`:30-32`),
  Codex ambiguous child (`native_context.py:232-244`).
- N4 — `FIRST_LOOK_AHEAD` (`brief_pack.py:3849`) and `FIRST_LOOK_DOD` (`:3847`) state `first_look.py put`'s check in hand text.
  Give that check a `when: first_look` row in T3 and say what happens to both constants.
- N5 — the AR-13 change check fails on `selftest.py:722` and on prose hits. Move that read onto `load_rows` (T1 owns that line),
  or narrow the grep to code reads.
- N6 — F13 (a): map each of the 9 legacy legs to its owning node (rule 19: a residual leaves with an owner).
- N7 — T0 M7: match `S\d structured .* invalid` on controller literals, case-insensitive, with positive control `:7513` and
  negative control `:3203`.
- N8 — (a) say the test passes the census blocking-unit set into `raise_family(wide=True)`; (b) copy the census blind-spot list
  whole (the parenthetical of `judgment-census.json:3`).
- N9 — T3 (j) needs `stage_joints._told_leg`, owned by T1: put the gated page leg in T1, or add it to T3's owns after T1.
- N9b — §5.1 sentences: 3 of 6 sampled under-state their function (R5). The designer should re-read the bodies before T7a goes out.
- N10 — optional: allow T3a/T3b.
- N11 — Q2: "около двадцати узлов (21), часть параллельно", not "пятнадцать подряд".

## Verdict

`fit after fixes`: **4 blocking findings** (B1-B4) and 11 non-blocking. The survivor decision itself is architecturally sound and
verified. B1-B4 do not change the architecture: each is a decision or a clause inside the chosen design, so the Lead can check the
fix round against this file without a third critic pass. Acceptance belongs to the Lead.

## Trail

Read (read-main `pkg:` unless noted):
- the first verdict (whole);
- the spec (whole: `:1-505`);
- plan §16 (`:494-534`);
- `scripts/inject_context.py:30-330, 412-442, 526-551, 569-604, 606-752`;
- `references/inject-map.json:1-20` + Grep `kinds|handoff-keys|drop_sections|qa-case-critic`;
- `scripts/native_context.py:173-264` + Grep `^def|MAX|len(`;
- `scripts/driver_dispatch.py:30-40, 205-281, 540-580, 690-719, 1030-1040, 2075-2085`;
- `scripts/driver_runner.py:550-639, 773-830`;
- `scripts/driver_machine.py:36-40, 444, 544-560`;
- `scripts/story_step.py:250-319`;
- `scripts/contract_slices.py:60-70, 250-262, 600-630, 736-756` + Grep `COMMON_LAYER_SUBJECTS`;
- `scripts/brief_pack.py:1998-2016, 2380-2400, 3847-3849, 4120-4130, 4258-4268, 4326-4346` + Grep `_row_field_lines|FIRST_LOOK_`;
- `scripts/controller.py:3190-3215` + Grep the five unit `def`s, `REPAIR_MARKER`, `structured test plan invalid`;
- `scripts/tests/fixtures/judgment-census.json:1-5` + controller rows;
- `scripts/validate_artifacts.py`: `check_understanding :1933`, `check_manifest_invariants :2215`, `check_context_manifest_v0
  :2350`, `check_report_coverage :1084`, `check_run_report_head :1633`, `check_cell_counts :249` (about 22 lines each);
- `scripts/refusal_registry.py` Grep REGISTRY ids + `PT-direct-test-run` entry;
- `scripts/stage_joints.py` import/`def` list;
- Grep `stage-joints|stage_joints` over `scripts/*.py`;
- Grep `CARD_MAX_BYTES`;
- `scripts/tests/test-layers.json` Grep `test_slices_on_demand` (in `quarantine`, `:9760` > `:7046`).

Not read: `codex_roles.py`, `role_load.py` bodies, `handoff_check.py`, `planning_contract.py`; the Claude host's resume
semantics (N1, unverified).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 kinds drop_sections can cut the new requirement section of the key page on repair/rework dispatches: delivered_text inject_context.py:164-196 never-cut set is only common + COMMON_LAYER_SUBJECTS (:172, :226); F12 (a) leaves kinds rules unchanged; K2 checks only that the page is listed",
    "B2 page size undecided: no split rule when K8 is red; T0 M5 measures only the automator T4+T5 share; the Codex native ceiling of 100000 chars (native_context.py:174-175) is unnamed, project-dependent, automator already near 84000 with a full project file (measured)",
    "B3 exclusive dispatch groups (first_look vs not_first_look, plan vs window) are resolved only by the brief line, a path the role must open (story_step.py:295-300, absent on resume :294-295), contradicting the survivor rule",
    "B4 T4 and T5 carry no requirement sentences and no designer-draft clause; the N9 class was fixed for T7a, T7b-f and T9 only (PROJECT.md teamwork item 11)"
  ],
  "class_completeness": "Class: a told carrier that can fail to reach the role, or a fix applied to some members of a set. Swept inside the spec: INLINE_SUBJECTS siblings (named_instead, the never-cut set, the on_demand weight report), the readers of stage-joints.json (contract_slices moved, selftest.py:722 left), designer-drafted sentences per node (T7a, T7b-f, T9 done; T4, T5 missing), the brief's hand requirement texts (ahead card removed; FIRST_LOOK_AHEAD and FIRST_LOOK_DOD left). Map axes 8 (hook and driver twins, both verified) and 28 (render sites) were walked. Each gap is a blocking or non-blocking finding in this round; no residual is passed on.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/20261113-told-before-work-plan-review.md",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md:1-505",
      "docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:494-534",
      "read-main pkg scripts/inject_context.py:30-330,412-442,526-551,569-752",
      "read-main pkg references/inject-map.json:1-20 + Grep",
      "read-main pkg scripts/native_context.py:173-264",
      "read-main pkg scripts/driver_dispatch.py:30-40,205-281,540-580,690-719,1030-1040,2075-2085",
      "read-main pkg scripts/driver_runner.py:550-639,773-830",
      "read-main pkg scripts/driver_machine.py:36-40,444,544-560",
      "read-main pkg scripts/story_step.py:250-319",
      "read-main pkg scripts/contract_slices.py:60-70,250-262,600-630,736-756",
      "read-main pkg scripts/brief_pack.py:1998-2016,2380-2400,3847-3849,4120-4130,4258-4268,4326-4346",
      "read-main pkg scripts/controller.py:3190-3215 + Grep unit defs",
      "read-main pkg scripts/tests/fixtures/judgment-census.json:1-5 + controller rows",
      "read-main pkg scripts/validate_artifacts.py six function bodies",
      "read-main pkg scripts/refusal_registry.py PT-direct-test-run entry",
      "read-main pkg scripts/stage_joints.py imports and def list"
    ],
    "reruns": [
      {"command": "wc -c references/slices/*/handoff-keys.md", "result": "3460..6626 bytes per page, max qa-test-strategist 6626"},
      {"command": "python -I script summing plugin: entries of inject-map.json per role plus agents/<role>.md", "result": "qa-automator 46913 + agent 11084 + 1 project file; qa-code-critic 46227 + 12146 + 1 project file; others 20119..42596"},
      {"command": "grep -c ^def <name>( for all 49 names of spec 5.1 in validate_artifacts.py; grep -c ^def check_", "result": "all 49 found once each; file has exactly 49 def check_"},
      {"command": "Grep stage-joints|stage_joints over scripts/*.py except stage_joints.py", "result": "code reads at contract_slices.py:490 and selftest.py:722; prose at contract_slices.py:440,550 and retro_numbers.py:1229,1290; retro_numbers.py:1236 via stage_joints.threshold"},
      {"command": "Grep COMMON_LAYER_SUBJECTS|named_instead|on_demand|slices_mode over scripts", "result": "inject_context.py:172,226,250-251 and contract_slices.py:68,622,695-696,745-752; test_slices_on_demand.py is quarantined"},
      {"command": "grep STRUCTURED_RE and the controller literals", "result": "STRUCTURED_RE carries the prefix story_step: refused - which no controller literal has; :7513 S3 structured test plan invalid; :3203 structured test plan invalid in _decision_problems (Gate A)"},
      {"command": "Grep -i 100000|native_context|codex|resume over the spec", "result": "100000 absent; native_context only in the T4 completeness line and the NOT-read list"}
    ]
  },
  "fixes": [
    "B1: _dropped_headings and map_problems never cut INLINE_SUBJECTS (or the requirement headings); a T3 row with a fixture kinds row",
    "B2: a split rule for the page (second generated page, inject-map entry, K2 accepts either, K8 warns at 80 percent); T0 M5 measures the end state for every role; name the Codex 100000 ceiling with a dev-time sibling check or a dependency",
    "B3: put the dispatch-group line into the story_step prompt, computed from the same rows_for result as the brief; exclusive headings name what they replace; a T3 row per fixture",
    "B4: designer drafts of the T4 and T5 row sentences (5.3 and 5.4), or the T7b-f draft-first clause on both",
    "N1-N11 as listed in this file"
  ]
}
```
