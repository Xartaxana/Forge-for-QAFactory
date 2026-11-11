# t-700 — GW1-3 (release-next/1, 0.10.9): gate B by the person's words; the retro is always full — DRAFT SPEC

Designer draft for the Lead. A critic on plan follows. Forks in §5 are NOT decided here.
R = `C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee`, P = `R\ai-packages\qa-factory`.

## 0. The load-bearing finding first: most of B-272 and half of B-271 are already on `main`

The brief assumes gate B still takes `waiver.py`. Reading the carriers says otherwise:

| Brief item | State in the tree (read, with line) | Delivered by |
|---|---|---|
| Gate B approval is a closed data word | `references/gate-approval-words.json:3` `"approve": {"gates": ["A", "B"]}`; one reader `gate_brief.approval_words` (`gate_brief.py:645`); the driver compares the first line, `Driver.gate_approval` (`story_run.py:15081`); unreadable list → one defect, nothing approved (`:15092-15098`) | C1-4b (CHANGELOG 0.10.0, `CHANGELOG.md:2543-2558`) |
| Stand-gap answers in words, never `waiver.py` shown | `question-vocabulary.json` `stand_gap_words` (`:21-40`); reader `gate_brief.read_stand_gap_answers` (`gate_brief.py:855`); the driver records the waiver itself (`Driver.take_stand_gap_answers`, `story_run.py:15440`); pin `test_story_run_delivery_b.py:262 b272_gate_b_card_in_words` (bans `waiver.py`, `--block`, `--decision`, `--stage` in the packet, `human_broken(text) == []`) | t-342 (CHANGELOG 0.8.0, `:4369`), t-357 |
| `deliver with known gaps` as a closed word | `question-vocabulary.json:17` `risk_word`; reader `question_register.risk_reason_of`; controller `_gate_risks` (`controller.py:8275`) | HF8-23 |
| A gate-A word used at gate B | `approve as is` has `gates: ["A"]`; pin `test_gate_open_items.py:96` "A-E15 at gate B it is not a word" | RH1-6 |
| Free words → conductor, never a pass | `Driver.record_by_code` returns False before any write unless `gate_approval` (`story_run.py:15362-15365`); `generic_prompt` for gates (`:14903-14910`) | C1-4b |
| B-271: the packet no longer offers to cut the retro | `story_run.py:12982-12984` comment; pins `test_story_run_delivery_b.py:177-182`, `test_story_run_delivery.py:836-842` (four phrases banned in the packet AND in `s8.md`) | t-342 |

What is NOT done (the real residue of this node):

1. **B-271, the road behind the sentence.** The retro can still be cut by a person's word: `stage_done.py:80` `SETTABLE["retro_mode"] = ("full", "numbers", "skip")`; `phases/s8.md:327-331` "The retro answer is one key … `retro_mode=full|numbers|skip` … written only when the person asked for them in their own words"; `references/conductor.md:28` row "The retro they asked for by name (`numbers` / `skip`) | `stage_done.py --set retro_mode=numbers|skip`" and `:53-54` (`--set retro_mode` among the person's-word commands); `Driver.generic_prompt` tells the conductor "stage_done --set for retro_mode" (`story_run.py:14911-14915`); `phases/s9.md:16, :31-43` ("unless the person said otherwise"); `agents/qa-retro-analyst.md:3` ("only when the human asked for the full retro") and `:12-14`. The owner's word (BACKLOG B-271, 02.10 18:15): "У пользователя не должно быть такого выбора. Ретро всегда полное."
2. **B-272 (3), one stale sentence on the skill road:** `phases/s8.md:118` tells the conductor to "state a `factory_defect` with the waiver command its `fix` prints" — to the person. Since t-357 a rehearsal `fix` is words (`gate_preflight.py:4992-4993`, `render` `:5003-5006`), and `s8.md:184` itself says "never show the person a script, a flag or a block id". The same placeholder sits in `handoffs/s8-scribe-to-gate-b.yaml:111` (reported, §5 F-6).

`waiver.py` and `controller.py` need NO change for either item (the node row lists them; see §1 "files the row named and this spec does not touch").

## 1. Goal, rules, invariants

Goal: (a) close every road by which a person's word shortens or skips the retro, while a person's word still passes any S9 block (P13) and is kept whole; (b) remove the one remaining instruction to show a waiver command to the person at gate B; (c) record, with evidence, that the rest of B-272 is delivered (Lead closes B-272 by references, F-1).

FR touched: FR-1, FR-2, FR-57 (the new refusal names what it expected and a door the conductor can use); FR-4 (nothing passes silently: the refusal is loud, the words are kept); FR-6, FR-8, FR-9 (the person's words about the retro reach a recorder — the remark — whole, and are carried into the report); FR-12 (NO phrase list: code never looks for "skip the retro" in words — the conductor reads words, code refuses the mode); FR-13 (the closed list of modes shrinks; it stays the stage_done contract lexicon, no new list); FR-30 (English); FR-54 (siblings by the map, §2 twin table).

AR touched (architecture.md), with the change check each demands (copied into the DoD, §4):
- **AR-19** (stage twins): skill phase `s8.md`/`s9.md` ↔ driver `Driver.stage_S9` / `Driver.generic_prompt` ↔ `references/conductor.md`; axis «Skill phase <-> driver» (`docs/SIBLING_MAP.md:127`). Check: name every twin in the report; each changes or says why not.
- **AR-22** (producer ↔ reader): the producer of `retro_mode=numbers|skip` (stage_done `--set`) is narrowed; its readers (`Driver.stage_S9` `:12901`, `report_facts.py:1912`, `s9.md`, `handoffs/vocabulary.yaml:260`, `s9-retro-to-project.yaml:44`, `gate-b-to-delivery.yaml:93-96`, `artifact-contract-json.md:55`, `artifact-contract-results.md:68`) STAY because stories recorded before 0.10.9 carry the values (builder-rules 9). Check: case-insensitive grep of `retro_mode` over `scripts/ agents/ skills/ references/ handoffs/` with a positive control; every hit listed in the report as "changed" or "kept: reads an older story's value".
- **AR-24** (a person's words reach whatever acts on them): words asking to cut the retro go to `waiver.py --remark` (one writer) and reach the report (`report_facts.py` reads `remarks`). Check: follow the answer to its command in the report.
- **AR-25** (every recorded state has a way out): no state is added or removed; `numbers`/`skip` keep their S9 branches and the `code_close.closed_story` door `full retro` (`no_move.py:383`, `story_run.py:14826-14832`). Check: `state-exits.md` needs no row (state unchanged) — one report line.
- **AR-16** (text a person reads): the gate B packet text is not changed by this node; the pins `b272_gate_b_card_in_words` and the B-271 phrase bans stay green. Check: no edit to `gate_brief.py`/`Driver.gate_text`; report line.
- AR-1: not touched (no new closed list; one existing contract tuple shrinks). Report line "AR-1: n/a — SETTABLE is the stage_done contract lexicon, narrowed, no new list".

## 2. Change list (for a builder of the weaker tier: file → function/key → behavior → test)

| # | File (absolute under P) | Function / key / lines | Behavior after | Test key (§4) |
|---|---|---|---|---|
| C1 | `scripts\stage_done.py` | `SETTABLE["retro_mode"]` (`:80`) | `("full",)`; the comment above it says why: the retro is always full (owner, 02.10.2026, B-271); `numbers`/`skip` are read only from a story an older version recorded | K3 |
| C2 | `scripts\stage_done.py` | `coerce_value` (`:88`) | Before the generic `allowed` check: when `key == "retro_mode"` and `value.strip().lower() in ("numbers", "skip")`, raise `ValueError` with EXACTLY this text (FR-1/FR-2/FR-57): `` `retro_mode` is always `full`: the retro is always the full one, and a person's word does not shorten or skip it (B-271). Keep their words as a remark - `waiver.py --task <T> --remark --stage S9 --words-file <file>` - the report carries them, and the retro runs whole. `` Everything else unchanged (`full` → `"full"`; a null word → `None`; any other value → the generic "one of: full" refusal) | K1, K2, K4 |
| C3 | `scripts\story_run.py` (HOT, D-0048) | `Driver.generic_prompt` (`:14898`), the non-gate branch string `:14911-14915` only | Drop `"stage_done --set for retro_mode and "`; the clause reads `stage_done --set for story facts`. No other byte of the function changes | K5 |
| C4 | `scripts\story_run.py` (HOT) | `Driver.stage_S9` (`:12891`), COMMENT ONLY above `:12901` | One comment line: `numbers`/`skip` are read only from a story an older version recorded (B-271, GW1-3); `stage_done` refuses them since 0.10.9. No code change | — (comment) |
| C5 | `references\conductor.md` | row `:28` and sentence `:53-54` | Row 28 becomes: `` | Words asking to skip the retro or keep only its numbers | not a mode: the retro is always full. Keep their words as a remark (`waiver.py --task <T> --remark --stage S9 --words-file <file>`) and say the retro runs whole; `stage_done --set retro_mode=numbers\|skip` is refused | ``. In `:53-54` drop `` and `--set retro_mode` `` from the list of person's-word commands (the list ends with `` `finish --ignore-handoff` ``) | K6a, K6b |
| C6 | `skills\qa-story\phases\s8.md` | paragraph `:327-331` ("The retro answer is one key") | Replaced by: `**Words about the retro are not a choice.** The retro is always the full one: words that ask to skip it or to keep only the numbers are kept as a remark (` + "`waiver.py --task <TICKET> --remark --stage S9 --words-file <file>`" + `), which the report carries; they are never recorded as a mode (` + "`stage_done.py`" + ` refuses ` + "`retro_mode=numbers|skip`" + `).` MUST NOT contain any of the four phrases the existing pins ban in s8.md: `skipped or cut`, `numbers alone`, `ilence is the full retro`, `The story ends with the retro` | K6c, K6d |
| C7 | `skills\qa-story\phases\s8.md` | `:118` | `state a ` + "`factory_defect`" + ` in the words its ` + "`fix`" + ` prints; a person's word that passes it is recorded by you, never typed by them.` (replaces "with the waiver command its `fix` prints") | K6e |
| C8 | `skills\qa-story\phases\s9.md` | `:16` last sentence; heading `:31`; paragraph `:33-37`; table "Why" cells `:42-43`; `:9` | `:16`: `` `numbers` and `skip` are never written from 0.10.9 on (the retro is always full; `stage_done` refuses them); a story an older version recorded with one of them still runs that mode. `` Heading: `## 0. The retro always runs in full`. `:33-37`: missing, unreadable or `full` = the retro runs; `numbers`/`skip` only in a story an older version recorded, run as recorded. "Why" cells: `An older version recorded the person's word for it; never written now.` Sections "`numbers`"/"`skip`" (`:63-84`) stay (they run an older story) | K6f |
| C9 | `agents\qa-retro-analyst.md` | frontmatter `description` `:3`; `:12-14` | `:3` ends `… into the project's ledgers — on every story: the retro is always the full one. Dispatched by qa-story at S9.` `:12-14`: `You run once per story, at the end — on every story: the retro is always the full one. A story an older version recorded as ` + "`numbers`" + ` or ` + "`skip`" + ` (` + "`pipeline.json.retro_mode`" + `) does not dispatch you.` | K6g |
| C10 | `scripts\tests\test_retro_always_full.py` (NEW) | keys K1-K7 | standalone script in the house style (`harness.check*`, a `main()` printing a summary, exit non-zero on a failure) | itself |
| C11 | `changelog.d\release-next-1-gw1-3.md` (NEW) | — | English, CHANGELOG voice: the retro is always full; `stage_done --set retro_mode=numbers|skip` is refused with the remark door; the conductor and the phase files no longer offer a short retro; an older story keeps its recorded mode; the gate B phase no longer tells the conductor to show a waiver command | `selftest.py --lang` |

Twins (AR-19, axis `docs/SIBLING_MAP.md:127` «Skill phase <-> driver»): s8.md ↔ `Driver.gate_text` (driver packet already says nothing of the retro — unchanged, pinned); s9.md ↔ `Driver.stage_S9` (C4 comment; behavior unchanged on purpose, F-2); conductor.md ↔ `Driver.generic_prompt` (C5 ↔ C3). Axis `:136` «Gate A card <-> gate B card»: untouched by this node (no card text changes).

Data rows and their reader: NO new data row. The only closed list touched is `stage_done.SETTABLE["retro_mode"]` (reader: `coerce_value`, same file). `gate-approval-words.json` is read, not changed (F-1).

Files the node row names and this spec does NOT touch: `scripts\waiver.py` (the remark door already exists: `waiver.py --remark`; RN1-9's class requirement lands in `waiver.py` — function to be named by RN1-9; this node touches no function there), `scripts\controller.py` (no retro text in it — grep `(?i)retro` over it reads only `RETRO_STAGE` logic, `controller.py:171-8101`; S9 `skipped` stays a readable state).

## 3. Edges and the invariant each protects

| Edge | Behavior | Invariant |
|---|---|---|
| E1 Words at gate B that are not the approval word (any language, `approved`, `I approve`, `approve, but fix X`) | unchanged: not recorded, whole answer to the conductor (`record_by_code` returns before any write) | a gate is never recorded on words that are not the data word (FR-12, FR-59); already pinned (`gate_approval` docstring; `test_gate_open_items.py:94`) |
| E2 Two words in one answer: first line `approve`, later lines `deliver with known gaps: <r>` and `<case>: accept` | unchanged: approval + risk reason + stand-gap record, each by its own reader; two `deliver with known gaps` lines with different reasons record no risk (`controller._gate_risks`) | each word has ONE reader; a conflict is never resolved by code guessing (pinned `test_gate_words_road.py` h3) |
| E2b First line `approve approve` / two approval words on the first line | not the word (whole-line equality) → conductor | equality, never containment |
| E3 A gate-A word at gate B (`approve as is`) | not a gate-B word → conductor | a word's gate set is data (`gates`), pinned A-E15 |
| E4 Data file absent/damaged, or with no gate-B row (an older or broken install) | `approval_words("B") == ()` → one defect per process, every answer to the conductor, the packet names no word | an unknown approves nothing (FR-59, AR-28); pinned `test_gate_brief_and_retro.py:2427-2451` |
| E5 `--set retro_mode=numbers` / `skip` / ` NUMBERS ` / `Skip` | refused, C2 text, exit non-zero, `pipeline.json` bytes unchanged | no road writes a short retro mode (B-271); the refusal has a door the conductor can use (FR-2) |
| E5b `--set retro_mode=full` | accepted, written | the `full retro` door of `code_close.closed_story` keeps its executor (`story_run.py:14827`, AR-25) |
| E5c `--set retro_mode=` (empty) / `none` | unchanged: `None` written; S9 reads it as `full` (`:12901`) | absent = full (s9.md:16) |
| E5d `--set retro_mode=Full` (other case) | unchanged generic refusal "`retro_mode` is one of: full — not `Full`" | the lexicon stays case-exact as today (small choice S-3) |
| E6 TEMPORAL — a story whose `pipeline.json` already holds `numbers`/`skip` (written before 0.10.9) | runs that mode as recorded (F-2 recommendation) | a person's word recorded under the rule of its time is not silently overridden (FR-8; builder-rules 9: a story in flight is not refused for an older artifact). After 0.10.9 no new such value can be born (E5) |
| E7 A person says at gate B "skip the retro" | conductor: remark (C5/C6); S9 runs full; the report carries the remark | the words are kept whole and reach the report (AR-24); they never change the mode |
| E8 CONFLICT PAIR — P13 "a person's word passes any block" vs B-271 "the retro is always full" | resolved by the owner's word: the retro mode is not a block (nothing waits on it); S9's real blocks (`code_close` `go on`, a stage refusal) still pass by a recorded word | no word path reaches `retro_mode` numbers/skip; every S9 block keeps its word door |
| E9 The S9 feedback question answered `skip` | unchanged: recorded `declined`, not a mode (`story_run.py:16279`) | the optional question stays optional; it never shortens the retro |
| E10 A text test over the doc files when a file is missing | the test FAILS naming the file (never passes on an empty read) | a key-presence check that cannot read is red (DOC-DISPATCH WITNESS (iii)) |
| E11 The new s8.md paragraph vs the existing four-phrase ban (`test_story_run_delivery.py:840`, `_b.py:179`) | C6's text avoids all four phrases; K6d asserts it in the narrow file | the existing pins stay green without being run by the builder (they are big files, 7b) |
| E12 POSITIONAL — C2's specific refusal sits BEFORE the generic `allowed` check | so the person-facing door is named for exactly `numbers`/`skip` | every other value keeps today's message; `full` is never refused |

Reused function in a more consequential role: none (`coerce_value` gains one branch in its own role).

## 4. Builder material

owns:
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\stage_done.py` (`SETTABLE`, `coerce_value`)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\story_run.py` (`Driver.generic_prompt`, `Driver.stage_S9` comment only — D-0048)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\references\conductor.md` (row 28, lines 53-54)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\skills\qa-story\phases\s8.md` (line 118, lines 327-331)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\skills\qa-story\phases\s9.md` (lines 9, 16, 31-43)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\agents\qa-retro-analyst.md` (lines 3, 12-14)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_retro_always_full.py` (new)
`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\changelog.d\release-next-1-gw1-3.md` (new)

given: this spec; `P\design\factory-rules.md` whole; `R\plans\builder-rules.md` (7b, 7c, 9, 11); `P\scripts\stage_done.py:60-112`; `P\scripts\story_run.py:12891-12926, 14897-14918`; `P\references\conductor.md:15-56`; `P\skills\qa-story\phases\s8.md:110-120, 236-245, 320-335`; `P\skills\qa-story\phases\s9.md:1-90`; `P\agents\qa-retro-analyst.md:1-20`; `P\scripts\tests\test_story_run_delivery_b.py:1-30, 145-185` (harness, `seed`, the phrase ban); `P\scripts\tests\story_run_common.py` (`seed`, `driver_for`); `P\scripts\tests\harness.py`.

non-goals: gate A; `gate_brief.py`, `Driver.gate_text`, the gate B packet (no text change; GW1-35 owns its size/flags); the retro's content rules and `retro_numbers.py`; removing the `numbers`/`skip` branches, vocabularies and forms (F-3); `waiver.py` (RN1-9); `controller.py`; `handoffs\*.yaml` and `references\artifact-contract-*.md` + `references\slices\*` (readers of the old values; RC1-14 owns slices — queued, F-3); a gate B message file (F-4); any phrase detector for "skip the retro" (FR-12).

handoff: `C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\docs\tasks\handoffs\t-NNN-gw1-3.md` (builder-rules 11: ≤ 500 words of prose; DONE/PARTIAL/NOT DONE per C1-C11; FR walk by section A-G; AR lines for AR-1/16/19/22/24/25; the AR-22 grep list; mutations with their killing key).

edges: §3 E1-E12.

DoD — acceptance keys (QUOTED VERBATIM here, before any run; the test asserts exactly these):
- K1 `stage_done.coerce_value("retro_mode", v)` raises `ValueError` for each v in `("numbers", "skip", " NUMBERS ", "Skip")`, and the message contains `always the full one` and `--remark --stage S9`.
- K2 `coerce_value("retro_mode", "full") == "full"` and `coerce_value("retro_mode", "") is None`.
- K3 `stage_done.SETTABLE["retro_mode"] == ("full",)`.
- K4 CLI on a seeded story (`story_run_common.seed`): `stage_done.py --task <T> --set retro_mode=skip` exits non-zero, `pipeline.json` bytes are identical before/after, the output contains `--remark`; CONTROL: `--set retro_mode=full` exits 0 and `pipeline.json` `retro_mode == "full"`.
- K5 `story_run.Driver.generic_prompt("waiver", "S9", "q")` does not contain `retro_mode`; CONTROL: it contains `waiver.py --block/--remark`.
- K6a `references/conductor.md` does not contain `` `stage_done.py --task <T> --set retro_mode=numbers ``; K6b it contains `Words asking to skip the retro or keep only its numbers` and does not contain `` and `--set retro_mode` record ``.
- K6c `s8.md` does not contain `retro_mode=full|numbers|skip` and contains `**Words about the retro are not a choice.**`; K6d `s8.md` contains none of `skipped or cut`, `numbers alone`, `ilence is the full retro`, `The story ends with the retro`, and still contains `` It is\n     always the full retro (`retro_mode: full`) `` (the existing pin at `test_story_run_delivery.py:842`); K6e `s8.md` does not contain `` with the waiver command its `fix` prints ``.
- K6f `s9.md` contains `## 0. The retro always runs in full` and `never written from 0.10.9 on`, and does not contain `unless the person said otherwise`.
- K6g `agents/qa-retro-analyst.md` does not contain `only when the human asked for the full retro` nor `unless the person asked in their own`; it contains `on every story: the retro is always the full one`.
- K7 NEGATIVE CONTROL of the text checker: the same helper run over the OLD conductor row 28 (a literal copy in the test) and over an s8 text holding `numbers alone` reports a failure; a missing file is a failure naming it (E10).

DoD — the EXACT verification run (builder, in the builder's worktree `<WT>`; output pasted verbatim as the witness; never `cd`):
```
python -B <WT>\ai-packages\qa-factory\scripts\tests\test_retro_always_full.py
python -B <WT>\ai-packages\qa-factory\scripts\stage_done.py --selftest
python -B <WT>\ai-packages\qa-factory\scripts\tests\test_story_run_words.py
python -B <WT>\ai-packages\qa-factory\scripts\tests\test_driver_layers.py
python -B <WT>\ai-packages\qa-factory\scripts\selftest.py --limits --lang
```
(rows 3-4: builder-rules 7c — the node writes `story_run.py`; row 5: package text and file sizes change. If a script needs the package as cwd, run it from the worktree's package folder as PROJECT.md allows and say so.) NOT run by the builder (7b, batch canon): `test_story_run_delivery.py` (`s9_report_rebuilt_last`, the four-phrase ban `:836-842`), `test_story_run_delivery_b.py` (`d3_gate_b_experiment`, `b272_gate_b_card_in_words`), `test_story_run_refusals.py` (CC13 `full retro`), `test_no_move_seam.py`, `test_gate_open_items.py`, `test_gate_brief_and_retro.py` (in `SLOW_TESTS`, `slow_tests.json:51`), `test_refusal_registry.py` (run it only if `refusal_registry.py` lists a `--set` refusal of stage_done — grep `SETTABLE`/`--set` there first; otherwise a report line).

AR change checks in the report (from §1): AR-19 twin list; AR-22 grep `retro_mode` (case-insensitive, over `scripts agents skills references handoffs`, positive control = a known hit such as `stage_done.py:80`), each hit "changed" / "kept: reads an older story's value"; AR-24 the answer → `waiver.py --remark` → `report_facts` remarks; AR-25 "no state added or removed"; AR-16 "no packet text changed"; AR-1 n/a line. Commit line: `architecture: AR-19, AR-22, AR-24, AR-25 -- <how kept>`.

Mutations (named, not run by the builder; one killing key each; run once at batch canon):
- M1 `SETTABLE["retro_mode"]` back to `("full", "numbers", "skip")` → K3 (and K1 via generic path still raises? NO — M1 alone keeps C2's branch, so K3 is the killer).
- M2 C2's branch removed → K1 (`skip` would be accepted).
- M3 C2's text without `--remark --stage S9` → K1.
- M4 `"stage_done --set for retro_mode and "` restored in `generic_prompt` → K5.
- M5 conductor.md row 28 restored → K6a.
- M6 s8.md old paragraph restored → K6c.
- M7 C2's branch moved AFTER the generic `allowed` check → K1 (the message would be the generic one, without `--remark`).
- M8 (canon only) the `numbers` branch of `Driver.stage_S9` deleted → `test_story_run_delivery.py::s9_report_rebuilt_last` (old recorded story, E6).

Changelog fragment: `P\changelog.d\release-next-1-gw1-3.md` (C11).

## 5. Forks (Lead decides; recommendation marked)

- **F-1 — Scope of B-272.** (a, RECOMMENDED) B-272 is delivered (§0 table: t-342/0.8.0, t-357, C1-4b/0.10.0, HF8-23, RH1-6); this node does only C7 and the Lead closes B-272 by those references (`piles.py close --id B-272 …`). (b) Rebuild a "gate-B section" in `gate-approval-words.json` (e.g. MR words `open the MR` / `no MR`) — not recommended: the MR choice is open variety read by the delivery conductor from the verbatim words (`story_run.py:12774`); a new closed word needs a reader, an executor and a price row, i.e. a new node.
- **F-2 — An older story already recorded `numbers`/`skip` (E6).** (a, RECOMMENDED) run it as recorded (FR-8, builder-rules 9; S9 code untouched; existing S9 tests stay green). (b) read it as `full` and print one line in the report that the earlier word was not carried out — honors "always full" literally but overrides a recorded word without asking (P13 tension).
- **F-3 — Depth of B-271.** (a, RECOMMENDED) close the producer (C1-C2) and every text that offers or instructs a short retro (C3, C5-C9); keep the branches, vocabularies, forms and contract docs that READ old values; queue a later sweep of `handoffs/vocabulary.yaml:260`, `s9-retro-to-project.yaml:44`, `gate-b-to-delivery.yaml:93-96`, `artifact-contract-json.md:55`, `artifact-contract-results.md:68` + its slice `references/slices/qa-retro-analyst/artifact-contract-results.md:10`, `design/driver.md:306` (RC1-14 owns slices). (b) Remove the modes outright (S9 branches, `retro_numbers.py --write-retro` road, `retro_mode_words`, forms, ~12 S9Stub test cases in `test_story_run_delivery.py:524-784`) — larger, collides with RC1-14 and the owner's rule 9.
- **F-4 — Gate B message file (RN1-4 twin; critic t-674 F4/E14 queued it).** (a, RECOMMENDED) QUEUE as its own node after GW1-35: a gate B message printed "whole" today means a 67 805-byte packet (`findings/20261030-gejt-b-paket-67805-b-…`, GW1-35), the Stop hook `gate_shown.py` is an enforcement file the Lead places, and the hook says gate B "has no file and no markers yet (queued)" (`gate_shown.py:29`). Note: the F4 finding file does not exist under `plans/` (glob `gate-b-message` finds only the critic review and the batch file) — the Lead files it. (b) In scope now: `gate_brief.main` writes `work/gate-b-message.md` for `--gate B`, `gate_shown.py` reads both — doubles this node and touches an enforcement file.
- **F-5 — Order with RN1-9 on shared text files.** RN1-9 owns `references/conductor.md` and `phases/s*.md` too. (a, RECOMMENDED) `очередь: GW1-3 → RN1-9` in both node rows (GW1-3 is small, lands first; RN1-9 merges main). (b) Disjoint lines (GW1-3: conductor.md row 28 + `:53-54`, s8.md `:118` + `:327-331`, s9.md `:9-43`) and the later node resolves (D-0048 form).
- **F-6 — Two stale gate-B carriers seen while sweeping (reported, not in owns).** (i) `handoffs/s8-scribe-to-gate-b.yaml:111` placeholder "with the waiver command its fix prints" (same sentence as C7); (ii) `s8.md:184-190` says the stand-gap answer "is recorded by the driver" — on the skill road no code reads `<case id>: <word>` (the only production caller of `gate_brief.read_stand_gap_answers` is `story_run.py:15767`), so the conductor must record those lines itself. RECOMMENDED: (i) add to C7 (one placeholder string, no field renamed); (ii) one sentence in s8.md now ("where no driver runs, you record each such line with the same `waiver.py` call") + queue the code convergence on axis `SIBLING_MAP.md:127`. Alternative: both queued.

## 6. Small choices closed by the designer

- S-1 The refusal lives in `coerce_value` (the one validator of `--set`), not in `Driver.stage_S9` and not in `waiver.py`.
- S-2 New narrow test file `test_retro_always_full.py` rather than keys in `test_story_run_delivery*.py` (big files the builder may not run, 7b).
- S-3 Case: the specific refusal matches `numbers`/`skip` lower-cased and stripped; the lexicon itself stays case-exact as today (E5d).
- S-4 The door is `waiver.py --remark --stage S9` (an existing writer whose `remarks` the report reads), not a new key.
- S-5 C4 is a comment, not code.

## 7. Reading trail

Read: `plans/piles/release-next/batch-1-release-0-10-9.md` (GW1-3 row `:27`, RN1-4 `:62`, RN1-9 `:71`, RC1-14 `:63`); `plans/BACKLOG.md:210-211` (B-271, B-272); `plans/piles/gates-and-words/README.md:57-68`, `batch-1-words-and-gates.md:12,15,42`; `P/references/gate-approval-words.json`; `P/references/question-vocabulary.json` (whole); `P/scripts/gate_brief.py:630-760, 4049-4090, 4305-4360`; `P/scripts/story_run.py:12740-12860, 12880-13009, 14800-14918, 15070-15149, 15339-15579`; `P/scripts/controller.py:2940-3037, 8250-8510`; `P/scripts/stage_done.py:60-123`; `P/scripts/gate_preflight.py:4979-5012`; `P/scripts/gate_shown.py` (grep); `P/skills/qa-story/phases/s8.md:100-360`; `s9.md:10-109`; `P/references/conductor.md:15-64`; `P/agents/qa-retro-analyst.md:1-16`; `P/handoffs/s8-scribe-to-gate-b.yaml:95-118`; `P/design/architecture.md:35-42, 154-233`; `R/plans/builder-rules.md:15-53`; `R/docs/SIBLING_MAP.md:120-139`; `P/scripts/tests/test_story_run_delivery_b.py:140-339`; `docs/tasks/specs/reviews/t-674-rn1-4-diff-critic.md:75-94, 160-165`; `P/CHANGELOG.md:2535-2558, 4369-4375` + version headers.
Greps (each with a positive control of the same shape): `gate-approval-words|gate_approval_words`; `skip(ped)? or (cut|trim)|…` (hits only tests and the agent file); `retro_mode` (whole package); `waiver\.py` in s8.md / gate_brief.py / gate_preflight.py; `--block|--stage S` in gate_preflight (hits `:1640, :2159` — control for "no fix text carries a command"); `read_stand_gap_answers\(` (one production caller); `(?i)retro` in controller.py and gate_brief.py (no offer text); `full retro`; `retro_mode_words` (two readers, no producer — reported below).
Negative claims and their controls: "no `test_gate_approval_words*` file exists" — the same glob found `test_story_run_words.py`, `test_driver_layers.py`; "CHANGELOG uses no B-ids" — `B-272` found in tests with the same Grep; "the F4 gate-B message finding is not filed" — the glob found 14 other files with `gate-a-message`.

Analogs noticed (reported, scope not widened):
- `pipeline.retro_mode_words` is read (`story_run.py:12903`, `report_facts.py:1913`) and has no producer anywhere in the package (AR-22).
- Driver road: `Driver.record_by_code` records gate B with `--bugs ordered` and no `--mr`, so the MR order is due even when the person wrote "no MR" under `approve`; only the delivery conductor reads the verbatim words (`story_run.py:12774`). Not verified end to end — a question for the critic on plan, not this node.
