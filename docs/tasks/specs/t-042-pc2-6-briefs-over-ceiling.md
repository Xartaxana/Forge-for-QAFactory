# t-042 — PC2-6: the S5 briefs over the 6 KB ceiling — cure the brief, not the ceiling (DRAFT SPEC)

Status: DRAFT by designer (opus) for the Lead of `package-ci/2`. The forks (end of file) are the Lead's; nothing in them is decided here.
Intent brief: `plans/piles/package-ci/findings/20261111-kanon-krasnyj-brief-pack-brify-vyshe-potolka-6-kb.md` (the builder does NOT need to read it;
everything it needs is below). Lead's chosen direction (11.11.2026): the BRIEF is cured, `BRIEF_MAX_BYTES` is NOT raised; the person's waiver of a
gate and the input-file list are the LAST things a trim may remove; a brief still over the ceiling after every cut SAYS so in a line.

All paths below are under `C:\QAFactory\forge-repo\`; `bp` = `ai-packages/qa-factory/scripts/brief_pack.py`, `tbp` =
`ai-packages/qa-factory/scripts/tests/test_brief_pack.py`.

---

## §1. Architecture, rules, owners (designer rule 1; host adaptations 9, 10)

### AR-n this node touches, and the change check each demands (goes into the DoD, §5)

| AR | why touched | change check (in the DoD) |
|---|---|---|
| AR-24 (a person's words reach whatever acts on them, whole) | the S5 waiver is dropped from the brief at words level 1 (`bp:1704` — `minimal` holds gate, warnings, halts, answers, NOT `override_lines`; `bp:1708-1709` puts a count line in their place) | every waiver of THIS stage keeps its own line at every words level; its whole text stays in `<ID>-decisions.md` (`bp:4459-4462`) |
| AR-21 (what a stage gathers travels whole) | the last resort pops input-file lines (`bp:4416-4426`), the case-file list first (it is appended near the end of `files`, `bp:4229-4232`) | every popped line is in `<ID>-files.md` (`bp:4449-4450`) and named in `## Not in the brief` (`bp:4319-4320`) — unchanged; the ORDER changes (§2) |
| AR-20 (shrink-only ratchets only shrink; a raise is named) | `BRIEF_MAX_BYTES = 6 * 1024` (`bp:54`) and `DOORS_ONLY_BRIEF_MAX = 6443` (`test_brief_pack_s5_plan.py:441`) | neither number changes; `git diff` of the node shows no edit of either line |
| AR-22 (every field produced has a reader) | `over_ceiling` (`bp:4427-4448`, returned `bp:4473`) has NO reader outside tests: `story_step._brief` reads only the last stdout line of `bp main` (`story_step.py:449-453`), and `main` prints no `over_ceiling` (`bp:4498-4502`) | `over_ceiling`'s budget reasons reach the role (a brief line) and the conductor (the stdout note) — §3 |
| AR-12 (friction measured; code that makes a stage dearer is a defect) | the cure must not move bytes into a role's reads without need | the brief is made smaller or keeps its size; nothing is moved into a NEW file the role must open unless the Lead picks option O-b (§1.4, fork F2) |
| AR-10 (a check's requirement reaches the role before the work) | the ahead card (`## The rules code will apply to your handoff`, `bp:4347-4348`, text in `references/ahead-cards.json:42-54`) is a candidate block by size | the ahead card is PROTECTED: never shortened or moved by this node |

Not touched (one line each): AR-1..AR-6 — no project/host/language variety is read or added; AR-7/AR-29 — no role judgment is
taken by code, the brief only reorders and reports data; AR-13/AR-14 — `bp` stays the one writer of the brief and its side files;
AR-16 — no text a PERSON reads changes (the brief is for a role, the stdout note for the conductor); AR-25/AR-28 — no new state.

### Checks this node adds or alters: owner and census class (AR-29, P27)

| check | owner it serves | census class |
|---|---|---|
| the over-ceiling predicate `budget_of(text) > BRIEF_MAX_BYTES` that prints the line (§3) | data (code): a byte count | shape; non-blocking (it reports, refuses nothing) |
| words level 1 keeping this stage's waivers (§2 rung 7) | intent (the person): the person's words reach the role | none — no check, a carry rule |
| the file-trim order (§2 rung 8) | data (code): a fixed order over lines | none — no check, an order |
| the five test checks (`tbp:770, 2206, 2244, 2876, 2899`) — expectations UNCHANGED | data (code): byte count and substring presence | tests are outside the census (`judgment-census.json:3`: units of `scripts/*.py` outside `scripts/tests/`) |

No refusal site is added, so no census row is expected; the commit's `judgment:` line says so. If `test_judgment_census.py` reports
a new unit anyway, its row is `class: shape, owner: data`.

### FR walk (PROJECT.md «Как принимается изменение пакета» п.1) — the builder repeats it as facts in the report

A — no refusal added (FR-4: the over-ceiling line turns a silent overflow into an informed one). B — no text a person reads changes.
C — FR-38 (the ahead card) protected; FR-49 every trimmed thing is in a side file; FR-8 the person's words are carried (the waiver
line). D — n/a. E — n/a. F — FR-55: the ceiling stands; FR-41: the line states a measured fact. G — FR-30 English, no Cyrillic;
FR-32 root cause + green tests.

### 1.4 What takes the bytes now — derived by reading; the builder's FIRST step measures it

Derived from `build` (`bp:4055-4475`), all at the REAL ceiling:

- The budget is `measured_bytes(text) - form_cost - sd_cost` (`bp:4379-4386`): the `## Your final message` section and the SD head
  (up to `SD_HEAD_MAX_BYTES` 1024, `bp:55`) are outside it. Everything else counts.
- Never shrunk (`bp:4307-4309`, `bp:4398-4404`): the head (title, `Scope:`, `Branch check:` ~0.4 KB per `tbp:2904`, `Read first`,
  `Case id form:`, `reviewed_dispatch_lines`, `expectation_change_lines`, `proof_required_lines`, `base_log_lines`, `side_lines`,
  `provisional_lines`, `first_look_lines`, `test_timeout_line`, `fit_target_lines` — `bp:4071-4179`), the card (`bp:4249-4270`;
  the automator's TOOLING rows `bp:223-234` and the critic's `bp:235-255` are each roughly 2-3 KB by reading), the ahead card
  (automator ~1.1 KB, critic ~0.85 KB, `references/ahead-cards.json:46,53`), the `## Rule` line (`bp:4293-4298`), the doors.
- What the ladder can take (`bp:4376-4377`): approach block (3 rungs), map head, digests, words 2 -> 1. Then files (`bp:4416-4426`).
- Words level 1 is NOT always shorter than level 2. In the short-words automator fixture (`tbp:2850`: one S5 waiver, one S1 waiver,
  gate words of 55 chars) level 1 swaps the S5 waiver line (~71 chars) for a count line (~93 chars, `bp:1709`), ADDS
  `- every decision in full: <path>` (`bp:4328`) AND a second pointer to the same file in `## Not in the brief` (`bp:4317-4318`),
  and drops only the `- 1 recorded decision(s) of other stages ...` line (`bp:1711`). By reading, level 1 there is LONGER than
  level 2 by tens of bytes: the ladder takes a rung that costs the waiver and saves nothing, then pops files.
- The level-1 render carries the decisions-file pointer TWICE (`bp:4328` in the words section, `bp:4318` in `## Not in the brief`):
  ~95 B of pure repetition in every level-1 brief. The critic's 10 KB-words brief (`tbp:766-772`) ends 41 B over (finding; CI run
  43092267661) with reason `words at level 1`.
- The case-file lines are popped FIRST of the files: `files` = plan lines, named inputs (+ masks/view), the "critic findings: none
  yet" line, case files, window test files, source material (`bp:4209-4245`); the loop pops from the end, skipping doors and, until
  nothing else is left, the window's test file (`bp:4419-4422`). Source material goes first, then the case files — the lines
  `tbp:2876` looks for.
- No per-block baseline exists in `plans/MEASUREMENTS.md` (searched case-insensitively for `brief`, `бриф`, `6 КБ`, `6144`: only
  lines 106, 146, 180-240, none a block size; positive control: the same search finds line 180). WHICH block grew after the
  experiment branch merge is not established by reading — the measurement (§5 step M) establishes it.

Options to free the bytes, in order of preference (each with the invariant it keeps):

| id | option | saves (by reading; M measures it) | invariant it keeps |
|---|---|---|---|
| O-c | level 1 carries the decisions-file pointer ONCE: drop `- every decision in full: {side}` from the words section at level 1 (`bp:4328`); `## Not in the brief` keeps `- every decision in full - read {side}` (`bp:4318`, the form `tbp:2434, 2943, 2948` read) | ~95 B, level-1 briefs only | no information leaves the brief (the same path stays one line away); briefs at level 2 byte-identical |
| O-d | a words rung that does not shrink the budget is not taken: level 1 only when `budget_of(level 1) < budget_of(level 2)`; the last resort pops files from the SMALLER of the two renders (today it is hard-wired to level 1, `bp:4415, 4426`) | tens of bytes in short-words briefs; 0 in long-words briefs | the person's words are never shortened for nothing; briefs that fit before rung 7 byte-identical; `over_ceiling` keeps its closed vocabulary — when the last resort ran at level 2 because level 2 is the shorter, the reason `words at level 1` is still the one named when the words keep the brief over (meaning: the words at their shortest kept form; `test_case_id_form_texts.py:215` accepts only that string) |
| O-a | the block M names as grown is shortened IN ITS TEXT, its data unchanged (detail that a door or side file already carries is replaced by a pointer to it) | whatever M shows | the block's data reaches the role in the brief or one named file away; no check substring of `tbp` lost; changes EVERY brief carrying that block (fork F2) |
| O-b | a NEW rung, after the digests rung and before the words rung, moves the grown block to its own side file `<ID>-<block>.md` with one `## Not in the brief` line | whatever M shows | roomy briefs byte-identical; the block is one named file away; written only when `write and output is None`, like every side file (`bp:4458-4470`) |

PROTECTED from O-a/O-b (never chosen as "the grown block" by this node): the person's words (gate, warnings, waivers, halts,
answers); the doors (`bp:4405-4414`); the card's command rows (O-a may only shorten their wording and must keep every substring
`tbp:2880-2894` checks); the ahead card (AR-10); the `Branch check:` line (`tbp:2935` reads it whole); the SD head (form, own cap);
`## Your final message` (outside the budget); `## The stand` (`bp:4342-4343`).

Selection rule (applied by the builder after step M, no judgment): apply K1 (§2) and O-c always; re-run M; if every build in the
M table is within the ceiling with no case line and no S5 waiver lost, stop there. Else add O-d if M shows it saves > 0 for a
failing build; re-run M. If still short: STOP, do not choose a block — return the M table to the Lead (a question, not a
`decomposable`): O-a vs O-b and the block are fork F2.

---

## §2. The trim order (explicit, first to last)

Each rung is taken only while `budget_of(text) > BRIEF_MAX_BYTES`. Rungs 1-5 are today's (`bp:4376-4377`) and keep their order
(they are what `tbp:2374` W4, `tbp:2384` W9 and the digests bisection `tbp:2868` read).

1. Project approach block, full -> one line (`ap_level` 2 -> 1).
2. Approach one line -> pointer line (`ap_level` 0).
3. Repository map head -> link only (`inline_map` 0).
4. Approach pointer line -> gone (`ap_level` -1).
5. Digests of earlier roles -> `<ID>-digests.md`.
6. ONLY if the Lead picks O-b (fork F2): the grown block -> its side file.
7. The person's words, level 2 -> level 1 (with O-d: only when level 1 is strictly smaller). At level 1: the gate line, every
   warning, EVERY WAIVER OF THIS STAGE, every open halt and every answer keep their own line, each cut at `DECISION_CHARS_MIN`
   (240, `bp:60`); the whole text of every decision is in `<ID>-decisions.md`; `## Not in the brief` names it once (O-c). Change in
   `decisions()` (`bp:1704-1709`): `minimal` = gate + warning + OVERRIDE + halt + answer lines (pair[1]), in that order (the order
   `shown` already uses, `bp:1703`); the count line `- N waiver(s) of <stage> are in the side file ...` goes — subject to fork F1.
8. Input-file lines, from the end of an order fixed by fork F3 (recommended: source material -> the other optional named inputs,
   incl. the "critic findings: none yet" line -> the case-file lines, last case first -> the window's test file), each popped
   line to `<ID>-files.md` (unchanged). Never popped: the doors (`bp:4405-4414`).
9. Nothing more is cut. The brief goes out over the ceiling and SAYS so (§3).

INVARIANT of the order (FR-8, AR-24, AR-21): a person's words that change what the role must do (a waiver of this stage, a gate
decision) and the input-file list stay inline until every other trimmable block has gone; the words are never removed at all, only
shortened at rung 7 with their whole text one named file away (N4, F-3: `bp:4404`); a file line is removed only at rung 8 and always
lands in `<ID>-files.md`. What must stay unreachable: a brief in which a waiver of this stage is absent while any rung 1-6 or any
non-door file line could still have been taken.

---

## §3. The over-ceiling case

Trigger: after rung 8, `budget_of(text) > BRIEF_MAX_BYTES` — the same predicate that today fills `over_ceiling` with
`words at level 1` / `doors only` (`bp:4428-4434`). NOT triggered by `sd head` or `over SLICE_BYTES` alone: those have their own
lines (the `head over cap` marker, `test_brief_pack_sd_head.py:204`; the by-range note, `bp:4437-4448`).

1. The brief: ONE line, the FIRST line of `## Not in the brief` (the section is opened when absent):
   `- the brief stays over its 6144 B budget after every cut (<reasons>): what it names is here whole or one named file away`,
   `<reasons>` = the budget reasons of `over_ceiling` joined by `, ` (`6144` printed from `BRIEF_MAX_BYTES`, never a literal).
   No byte count of the brief itself in the line (no fixed-point loop like `bp:4440-4447`).
   Placement keeps: the by-range note as line 3 (`tbp:2447` W8 `top[2]`), `## The person's words` as the first `## ` (`tbp:2362` W3).
2. The line is OUTSIDE the budget (fork F5): `budget_bytes` of a brief is the same with and without it. Implementation: the bytes the
   line (and a section heading it opened) add are subtracted in `budget_of`, the way `form_cost` is (`bp:4379, 4385-4386`).
3. The conductor: `main`'s stdout line (`bp:4499-4502`) gains `, over the 6144 B ceiling after every cut: <reasons>`. That line is
   what `story_step._brief` returns as the note (`story_step.py:453`) and `_write_dispatch_files` prints as `note: ...`
   (`story_step.py:1190-1192, 1225-1226`). A run finding beyond that: fork F4.

Who reads it: the role (it learns that nothing was dropped silently and where the rest is); the conductor (the start note — it may
choose to split the window or tell the person; P22, its judgment, not code's).

Error direction (the predicate is reused from a report into a more consequential role — the one line that says "over"): it may err
toward SAYING over, never toward silence. Because the line is computed from the final text and sits outside the budget, adding it
cannot change the predicate. Adversarial inputs that must stay on the safe side: (a) a brief exactly AT 6144 budget bytes -> no line
(`<=` passes, as `bp:4395`); one byte over -> the line; (b) multi-byte UTF-8 words (Cyrillic, emoji in a person's answer) -> counted
in bytes (`measured_bytes` encodes UTF-8, `bp:3586`), so a brief over in bytes but under in characters gets the line; (c) a long
checkout path -> the plugin root is tokenised (`bp:3582-3585`, AR-4), so the budget, not the raw size, decides — by design, and the
raw size is printed beside it on stdout; (d) zero file lines and only doors left -> the loop ends (`bp:4423-4424`) and the line is
there; (e) the 30 KB brief -> both the by-range note (line 3) and the over line; `over_ceiling` stays exactly
`["words at level 1", "over SLICE_BYTES"]` (`tbp:2448`).

---

## §4. Edges, each with the invariant it protects

| edge | behaviour | invariant |
|---|---|---|
| no waivers at all | level 1 has no waiver line and no count line (today the count line is appended only when `override_lines` is non-empty, `bp:1708`); with no decisions at all the words section is `- none recorded ...` (`bp:4323-4324`), unchanged | no line claims a waiver that does not exist; no `0 waiver(s)` line |
| only other stages' waivers | level 2: the `- N recorded decision(s) of other stages are in the side file` line (`bp:1710-1711`), unchanged; level 1: covered by the single decisions pointer | another stage's waiver never appears inline (`tbp:2900`) and is always in `<ID>-decisions.md` (`tbp:2919-2921`) |
| ten waivers of this stage | all ten keep their line at level 1, each ≤ 240 chars + the `- ` lead, whole text in the side file; rung 8 pops file lines first; if still over -> §3 line | no waiver of this stage is ever replaced by a count while the brief is built; a long brief is a cost, a lost word a defect (`bp:4402`) |
| a waiver whose text exceeds 240 chars | cut by `_short` at `DECISION_CHARS_MIN` with `...` (`bp:1093-1095, 1693`); whole in the side file | a cut word is a pointer, never the decision (`bp:1706`) |
| zero input files (`files == []`) | the section says `- the stage declares no input file` (`bp:4341`); rung 8 finds nothing (`last is None`) and ends; §3 line if over | the loop terminates; no line is invented |
| only doors left in `files` | rung 8 ends (`bp:4423-4424`); `doors only` reason; §3 line | a door is never trimmed (SC1-10, FR-2) |
| a brief already under the ceiling at rung ≤ 5 | byte-for-byte unchanged by K1, O-c, O-d, F3 and §3 (each acts only at rung ≥ 7 or when over). O-a is the one change that alters such briefs (fork F2) | proof: step P of §5 (hash snapshot before/after, every under-ceiling brief identical) |
| a brief that fits at level 2 only after O-c/O-d freed bytes | it now keeps level 2 (waivers whole, no side-file pointer) — that is the cure, not a regression | the five red checks read exactly this |
| the 10 KB-words fixtures (`tbp:766, 2252, 2932`) | still level 1 (the gate line cut 400 -> 240 saves more than level 1 adds), `sides.decisions` True (`tbp:773, 2937`) | `tbp:2943` bisects on "`- every decision in full - read` absent": the predicate must stay monotone in the ceiling and must tip inside 512..65536 (`tbp:2318` asserts it) — it does iff level 1 is strictly smaller than level 2 in that fixture; M prints both numbers to prove it |
| path length of the test run | the brief prints the task root (`tbp:2300-2302`); Windows temp paths measure LOWER than CI (`test_brief_pack_s5_plan.py:441`) | a local green is not the proof: the CI shard running `tbp` is (§5 key A6) |
| `DOORS_ONLY_BRIEF_MAX` (plan critic, `test_brief_pack_s5_plan.py:441-452, 497-498`) | K1 may change the plan critic's level-1 bytes when its fixture holds a waiver; the §3 line is outside the budget | the ratchet is not raised: if K7 turns red, STOP and report (a raise needs the Lead's named reason, AR-20) |
| PC2-1 (bisection pins, same batch) | its core is ALREADY in the tree: `s5_ceiling` / `s5_build_at` at `tbp:2300-2325`, used at `tbp:2868, 2943`; the constants `S5_DIGESTS_INLINE_CEILING` / `S5_GATE_LINE_CEILING` are absent (searched `tbp` dir; positive control: the same search finds `s5_ceiling(` at `tbp:2315`) | PC2-6 lands FIRST or independently (fork F7): it needs no pin change; the bisections absorb any byte shift as long as rungs 1-5 keep their order and the gate predicate stays monotone (row above). If F1(a) is chosen, PC2-6 edits `tbp` too, and PC2-1 (also `tbp`) merges `main` after it |

---

## §5. The builder node

```
given: this spec (C:\QAFactory\forge-repo\docs\tasks\specs\t-042-pc2-6-briefs-over-ceiling.md); ai-packages/qa-factory/scripts/brief_pack.py; ai-packages/qa-factory/scripts/tests/test_brief_pack.py; ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py; ai-packages/qa-factory/scripts/tests/test_brief_pack_sd_head.py; ai-packages/qa-factory/scripts/tests/test_case_id_form_texts.py; ai-packages/qa-factory/scripts/story_step.py (:445-455, :1168-1227, read only); ai-packages/qa-factory/references/ahead-cards.json (read only); ai-packages/qa-factory/design/factory-rules.md (whole); plans/builder-rules.md; docs/TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (decisions, build, main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\pc2-6-briefs-over-ceiling.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (ONLY line 2432, ONLY if the Lead answers F1 with (a))
non-goals: BRIEF_MAX_BYTES, SD_HEAD_MAX_BYTES, DECISION_CHARS(_MIN), DOORS_ONLY_BRIEF_MAX unchanged; no new test file, no new pin of a measured byte count; no edit of any expectation in test_brief_pack.py except F1(a); the ahead card, the doors, the Branch check line, the person's words never cut; no new writer of factory-backlog.md (F4); PC2-1's pins not touched; no change for roles/stages whose brief is under the ceiling
handoff: report per builder-rules п.11 with: the M table (before and after), the P hash diff, the witness runs verbatim, the FR walk, the option set applied, the M script source in full
edges: §4 of this spec, every row; §3 adversarial inputs (a)-(e)
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py` and `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack_s5_plan.py` plus every non-slow file printed by `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py`
```

### Steps

- **E (entry).** Before any edit, on the branch tip: run the two named test files and save their FAIL lines (both files are in
  `keep_fail_at_entry`, `test-layers.json:5347-5350`, so `test_brief_pack_s5_plan.py` may be red at entry for other reasons).
- **M (measure, read-only, FIRST).** A script in the builder's scratchpad (`brief_blocks.py`, not committed; full source in the
  report). It imports `tbp` as a module, wraps `brief_pack.build` with a spy, and runs `tbp.expectation_lines()` and `tbp.main()`
  unchanged. For every spied call with `stage == "S5"`, role in (`qa-automator`, `qa-code-critic`) and the REAL ceiling, it records
  the caller's line in `tbp` (the build of `:769`, `:2202`, `:2239`, `:2855`, `:2933`) and prints:
  1. `budget_bytes`, `over_ceiling`, `omitted`, `sides`, and the file lines trimmed (the roomy `files` minus this `files`);
  2. the same build at a 65536 ceiling (`write=False`, the current `SCRIPTS` kept): bytes per `## ` section and per head line
     (`measured_bytes(line) + 1`), largest first, each with its first 60 characters;
  3. the words section at level 2 vs level 1: `measured_bytes` of the lines `decisions(...)` returns as `shown` vs `minimal`,
     plus the level-1 additions (`bp:4318, 4328`) — this is the O-c and O-d saving;
  4. the deficit: by bisection over the ceiling (as `tbp:2315-2325`), the smallest ceiling at which the build keeps
     `'S5 block "vcs-1: uncommitted changes" -> go on'` inline AND no `input file(s) - read` line in `omitted`; deficit = that
     ceiling − 6144 (for the `:769` critic build: `budget_bytes` − 6144).
  Optionally the same table on a reference commit where `tbp` was green (a `git worktree` in the scratchpad), for the per-block
  growth; when none is known the absolute table is the evidence. Then apply the selection rule of §1.4.
- **C (code).** K1 (§2 rung 7, `decisions()`), O-c, and — per the selection rule — O-d; F3's order in rung 8; §3 (line, budget
  exemption, stdout note). One changelog fragment (`changelog.d/README.md` form), English only.
- **P (proof that under-ceiling briefs are unchanged).** The M script in `--snapshot` mode, run once BEFORE C and once AFTER, on
  the same fixtures plus one brief per role of `ROLE_FILES` (`bp:91-107`) at its usual stage in a `tbp` `seed` project: sha256 of
  each brief's markdown with the temp project root replaced by `<root>` and the plugin root by `<plugin>`. Expected: every brief
  whose BEFORE build had `budget_bytes <= 6144` and no `every decision in full - read` / `input file(s)` line in `omitted` has the
  same hash AFTER. Both outputs verbatim in the report; any differing hash is listed with its reason (only O-a may cause one, and
  only on that block's lines).
- **W (witness).** The DoD command(s) on the final state, verbatim output.

### Acceptance keys

- A1. The five checks green with expectations UNCHANGED: `tbp:770` («10 KB of gate words: the critic's brief is still within
  6 KB»), `tbp:2206` («K6 ... the S5 waiver»), `tbp:2244` («K6 ... the S5 waiver inline»), `tbp:2876` («the case files are listed
  with sizes»), `tbp:2899` («and the S5 waiver»).
- A2. No other check turns red: the FAIL lines of both files after C are a subset of the entry FAIL lines (step E), minus the five.
  The one exception is `tbp:2432` if and only if the Lead answered F1 with (a), and then its new expectation is the S5 waiver line
  inline.
- A3. `git diff` shows `BRIEF_MAX_BYTES = 6 * 1024` (`bp:54`) and `DOORS_ONLY_BRIEF_MAX = 6443` untouched; no new test file; no
  new numeric byte constant in any test.
- A4. Step P: every under-ceiling brief's hash identical (or the O-a block named as the only difference, if F2 chose O-a).
- A5. §3 demonstrated in the report by the existing over-ceiling builds (`tbp:2425` W6 battery, `tbp:2443` W8 huge): the line is
  the first line of `## Not in the brief`, and `budget_bytes` equals the value with the line removed (the M script prints both).
  No new test is written for it (docs/TESTING.md: a doc-dispatch-style witness is attached, never committed); if the Lead wants it
  guarded, it is ONE `check_in` added to the existing W6 block — only on the Lead's word (it would change `tbp`).
- A6. The CI shard that runs `tbp` is green on the branch (`tools/ci_read.py`): the local run measures lower than CI.
- A7. Commit message: `architecture: AR-24, AR-21, AR-20, AR-22, AR-12, AR-10 -- <how each is kept, one clause each>` and the
  `judgment:` line stating no census unit is added; the FR walk in the report.

---

## Forks (the Lead's)

- **F1 — `tbp:2432` pins the very behaviour being cured.** «N4 W6: ... the waivers are ONE count line» expects
  `- 1 waiver(s) of S5 are in the side file` in the over-ceiling battery brief (60 warnings). K1 (the waiver keeps its line at
  level 1) turns it red, which collides with A2 «no other check red». Options: (a) K1 as written, and the ONE expectation at
  `tbp:2432` changes to the waiver line inline (the line is the pin of the old order); (b) no K1: waivers keep going to a count
  line at level 1, and the five checks are made green only by freeing enough bytes that those briefs never reach level 1 —
  the waiver then still goes BEFORE the files in any brief that does reach level 1, against the Lead's direction; (c) K1 plus the
  count line kept beside the waiver lines (both true: the side file does hold them whole) — no test edit, ~95 B more per level-1
  brief, a redundant line. Recommendation: (a) — the direction says the waiver is last; a check that says otherwise is the defect's pin.
- **F2 — if O-c (+O-d) do not cover the deficit:** (O-a) shorten the grown block's text everywhere (the real cure, smaller brief
  for every role that gets it, FR-55; changes under-ceiling briefs, so A4 lists that block) vs (O-b) a new rung moving it to a side
  file before the words rung (roomy briefs byte-identical; one more file the role may have to open). And WHICH block: the Lead picks
  from the M table. Recommendation: O-a when the block repeats what a door/side file already carries, else O-b; the builder stops
  after M and returns the table — it does not choose.
- **F3 — the order inside the input-file list (rung 8).** Today the case files go right after source material, before the named
  inputs (`bp:4229-4236`); the test-plan slice line and the bundle line (`tbp:2877-2879`) are read too, so a mere swap can turn
  those red in a trimmed brief. Options: (a) source material -> other optional named inputs incl. the "none yet" line -> case
  files (last first) -> window test file; (b) keep today's order (the list as a whole is already the last rung). Recommendation: (a)
  — the case files are the scope the role acts on; in the test fixtures nothing is popped once the bytes are freed, so (a) is
  exercised only by real over-ceiling briefs.
- **F4 — who else reads the over-ceiling case.** (a) the brief line + the stdout note only (the conductor sees `note:` at start and
  decides, P22); (b) also a run finding through `project_decisions.add_finding` (`project_decisions.py:307`) — a second writer of
  the project's backlog from inside the brief builder (AR-14 risk) and code deciding that a long brief is a finding. Recommendation: (a).
  The intent brief (finding item 3) said «в брифе и в находке прогона»; (a) satisfies the brief half and hands the finding half to
  the conductor.
- **F5 — the over-ceiling line inside or outside the budget.** Outside keeps every `budget_bytes` and the shrink-only
  `DOORS_ONLY_BRIEF_MAX` (`test_brief_pack_s5_plan.py:441`) untouched; inside adds ~110 B to every over brief and can push K7
  over its ratchet (a raise needs a named reason, AR-20). Recommendation: outside.
- **F7 — PC2-6 vs PC2-1 order.** The batch table says PC2-6 depends on PC2-1 (`batch-2-potolki-brief-pack.md:29`), but PC2-1's core
  is already in `tbp` (§4, last row) while its status is «ожидает» (`:24`). Options: (a) PC2-6 first (P1, canon red), PC2-1 after
  (rebases; closes or narrows to what is left, e.g. the «ceiling in code +1» mutation of its finding); (b) together in one branch;
  (c) as the table says. Recommendation: (a), and the Lead checks whether PC2-1 still has work.

### Answers to the forks (Lead, 12.11.2026)

- F1: (a) — K1 as written; the ONE expectation at `tbp:2432` changes to the S5 waiver line inline. The owner's direction
  (finding, 11.11.2026) is that the waiver goes last; the count-line check pins the old order.
- F2: not decided in advance. The builder runs E and M, applies K1, O-c and (when M shows a saving) O-d, and STOPS with
  the M table if the deficit is not covered; the Lead then picks O-a or O-b and the block.
- F3: (a) — source material, other optional named inputs, case files (last first), the window's test file.
- F4: (a) — the brief line and the stdout note only; no second writer of the project's backlog (AR-14). The "run
  finding" half of the finding's item 3 is the conductor's move on the note.
- F5: outside the budget.
- F7: (a) — PC2-6 first. PC2-1 is checked by the Lead after this node lands (its core is already in `tbp`).
- Owns overlap with PC2-3 (`brief_pack.py`): PC2-3 is not dispatched until PC2-6 is committed (sequence, same Lead).
- A5: the over-ceiling line gets ONE `check_in` in the existing W6 block (`tbp`, near :2432) — the Lead's word; the
  builder's owns for `tbp` are that block only (line 2432 and the added check).
- The builder does not commit; the Lead commits (shared tree on `main`). A6 is read by the Lead on the canon run.

## Small technical choices closed by the designer

- The over line has no byte count of the brief (no fixed-point loop); it prints the ceiling from `BRIEF_MAX_BYTES`.
- The line sits first in `## Not in the brief` (keeps `tbp:2447` W8 line 3 and `tbp:2362` W3 first-heading).
- The O-b rung (if chosen) goes after the digests rung and before the words rung: rungs 1-5 keep their order, so W4/W9 and the
  digests bisection keep their meaning.
- The `over_ceiling` vocabulary is not extended; with O-d the reason `words at level 1` names "the words at their shortest kept form".
- The M/P script lives in the builder's scratchpad, not in the repo (one-off measurer; its full source in the report).
- The fragment file name `changelog.d/pc2-6-briefs-over-ceiling.md`.

## Noticed, not widened (report lines for the Lead)

- **Owns overlap:** PC2-3 also writes `scripts/brief_pack.py` (`batch-2-potolki-brief-pack.md:26`, «подписи измеренного бюджета
  "budget B"» — likely `main`'s print line, the same function §3 item 3 edits). `brief_pack.py` is not in PROJECT.md's hot-file
  list, but the two nodes need disjoint function lists or a `очередь:` line.
- The batch brief says «НЕ делать: правки кода `brief_pack.py`» (`:15`); the PC2-6 row lifts it for this node only (`:29`).
- `over_ceiling` had no reader outside tests before this node (grep of the package: only `bp`, `CHANGELOG.md:139`, and tests).
- The finding's «8 input lines, 3-4 popped; critic 11 of 12» is the builder t-035's spy figure, not re-measured here; step M re-measures it.

## Reading trail

- Finding (intent brief) whole; PC2-1 finding whole; `plans/piles/package-ci/batch-2-potolki-brief-pack.md` whole.
- `bp`: :40-319 (constants, ROLE_FILES, TOOLING), :380-459 (digest template, ahead card, case form), :630-669, :1093-1162,
  :1454-1512, :1600-1735 (answers, `decisions`), :3423-3482, :3570-3599, :4055-4504 (`build`, `render`, ladder, last resort,
  `over_ceiling`, write, `main`).
- `tbp`: :1-239, :501-530, :730-789, :2150-2475, :2773-2812, :2840-2984; grep of the five check labels.
- `test_brief_pack_s5_plan.py` :425-516; `test_brief_pack_sd_head.py` :185-225; `test_case_id_form_texts.py:215` (grep);
  `story_step.py` :440-459, :1160-1239; `references/ahead-cards.json` :40-59; `test-layers.json` :255-325, :5347-5358;
  `judgment-census.json` :1-5 and the `brief_pack.py` rows; `scenario_walk.py` :833-936; `plans/builder-rules.md` grep 7b;
  `docs/TESTING.md` grep pin rows (:93-95); `plans/MEASUREMENTS.md` greps (`brief` case-insensitive with hits = positive control;
  `бриф|6 ?КБ|6144`).
- Greps: `over_ceiling` over the package; `every decision in full|waiver\(s\) of` over the package; `S5_DIGESTS_INLINE_CEILING|
  S5_GATE_LINE_CEILING|s5_ceiling\(` over tests (positive control: `s5_ceiling(` found); `brief_pack` in `story_step.py`.
- Needed beyond the manifest: `story_step.py`, `test_brief_pack_s5_plan.py`, `test_brief_pack_sd_head.py`,
  `test_case_id_form_texts.py`, `ahead-cards.json`, `judgment-census.json`, `test-layers.json`, `scenario_walk.py`, the batch file.
