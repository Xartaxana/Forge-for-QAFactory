# t-042 — critic on PLAN: PC2-6 «briefs over the ceiling — cure the brief, not the ceiling»

Spec under review: `docs/tasks/specs/t-042-pc2-6-briefs-over-ceiling.md` (whole, with «Answers to the forks (Lead, 12.11.2026)»).
Source: `plans/piles/package-ci/findings/20261111-kanon-krasnyj-brief-pack-brify-vyshe-potolka-6-kb.md`.
Reviewer: critic (opus). Read-only; no tests run (non-goal); the step-M measurement is not repeated.

**VERDICT: ACCEPT WITH FIXES** — 6 blocking findings (spec text, no change of direction), 14 non-blocking.
The direction (K1 + O-c, file list and waiver last, an over-ceiling line, no ceiling raise) is sound and consistent with
AR-24/AR-21/AR-20/FR-8; the blockers are positional invariants, a stop condition and a class left half-fixed, all of which
a Sonnet builder would otherwise have to invent or would get wrong.

`bp` = `ai-packages/qa-factory/scripts/brief_pack.py`, `tbp` = `ai-packages/qa-factory/scripts/tests/test_brief_pack.py`.

---

## Answers 1-7

### 1. Facts by trail — mostly TRUE; two imprecisions, one partly unverifiable

- `minimal` drops this stage's waivers: TRUE. `bp:1703` `shown` = gate+warning+override+halt+answer; `bp:1704` `minimal` = gate+warning+halt+answer (no `override_lines`); `bp:1708-1709` appends `- N waiver(s) of <stage> are in the side file ...`.
- Decisions pointer twice at level 1: TRUE. `bp:4317-4318` (`omitted`, when `full and dec_level < 2`) and `bp:4328` (words section at `dec_level == 1`).
- Files loop pops case-file lines before named inputs: TRUE. `files` = `plan_files` (`bp:4245`) + `file_lines(names)` with masks/view (`bp:4209-4224`) + «critic findings: none yet» (`bp:4212`) + cases (`bp:4229-4232`) + window tests (`bp:4234-4235`) + source material (`bp:4236`); the loop pops from the end skipping doors and, while anything else is left, the window test file (`bp:4419-4422`). Pop order today: source material → «... and N more case files» → cases last-first → «none yet» → named inputs last-first.
- `over_ceiling` has no reader outside tests: TRUE for consumers (grep `over_ceiling` case-insensitive over the package: only `bp`, `CHANGELOG.md:139`, `tbp:771/2427/2448`, `test_brief_pack_s5_plan.py:447-514`, `test_brief_pack_sd_head.py`, `test_case_id_form_texts.py:215`; positive control: the same grep finds `bp:4427`). Imprecise: `main --json` DOES print it (`bp:4495-4496`); no caller uses `--json` (grep `brief_pack.build(|"brief: |budget_bytes` outside tests: only `bp` itself). Non-blocking N3.
- `story_step._brief` returns the last stdout line of `main`: IMPRECISE. It returns the last line of `stdout + stderr` concatenated (`story_step.py:152` `(done.stdout + done.stderr).strip()`, `:453`). Any stderr line printed during `build` (`bp:3115, 3169, 3249, 3271, 3344, 3760, 3889, 4039` — helper failures) lands AFTER the stdout line and becomes the note; the §3 stdout note is then not delivered. Non-blocking N2 (pre-existing class; `story_step.py` is outside owns).
- §1.4 «level 1 ADDS `- every decision in full: <path>` (`bp:4328`)» in the short-words fixture: INACCURATE. The fixture (`tbp:88-91`) has an S1 waiver, so `others = 1` and level 2 already carries `- every decision in full: <decisions>` (`bp:1705-1707`). By line length: level 2 = gate, warning, waiver (~71), pointer (~97), others line (~62); old level 1 = gate, warning, count line (~108), pointer `bp:4328` (~97), omitted line (~102). Net level 1 − level 2 ≈ +77 B — the conclusion (level 1 is longer) holds, the mechanism stated does not. After K1 + O-c: level 1 = gate, warning, waiver (~71), omitted (~102) ≈ 57 B SHORTER than level 2 — so O-d saves 0 on this fixture (N1).
- The five checks of A1 vs CI run 43110913721: CONSISTENT, partly visible. `ci-out/c2/package-full-shard-2/selftest-shard-2-of-2.txt:41-44`: `test_brief_pack: 873/878 ok` (5 fails) and three FAIL lines printed — «the case files are listed with sizes» (`tbp:2876`), «and the S5 waiver» (`tbp:2899`), «K6 ... the S5 waiver» (`tbp:2206`). The selftest summary prints only three; `tbp:770` and `tbp:2244` are not visible in this artifact. The count (5) and the labels match the finding (`finding:7-11`, from run 43092267661). N14.
- Line refs checked on the carrier: `bp:54, 55, 59-60, 1693, 1704, 1708-1709, 4229-4232, 4317-4320, 4328, 4376-4377, 4379-4386, 4395, 4405-4426, 4427-4448, 4449-4450, 4459-4462, 4473, 4498-4502`; `test_brief_pack_s5_plan.py:441`; `test_case_id_form_texts.py:215`; `story_step.py:449-453, 1190-1192, 1225-1226` — all as stated. `test-layers.json` `keep_fail_at_entry` is now at `:5357-5360` (drift from the uncommitted working-tree edit; harmless).

### 2. The trim order — rung 7 keeps the stated invariant; O-d is safe but must be the class fix

- With K1 (`minimal` = gate + warning + override + halt + answer), a waiver of this stage is in the brief at every built level: level 2 via `shown` (`bp:1703`, cut at 400 with `...` when long, the line stays), level 1 via the new `minimal`; level 0 is rendered only by the `over_ceiling` probe (`bp:4329-4330, 4430`) and never shipped. No other path in `build` drops it: the walk brief (`bp:4299-4301`) and first look still render the words section (`bp:4322-4330` is unconditional); the SLICE note loop re-renders with the same `chosen` (`bp:4444`). The stated unreachable state («a waiver of this stage absent while anything else could be cut») becomes unreachable outright. KEPT.
- Sibling in the same artifact (rule 14, surface «person's words at level 1»): the gate, warnings, halts and journal answers keep a 240-char line; the QUESTION answers do not — their `minimal` is «the id and the letter, no words» (`bp:1603`, `bp:1621` `"{qid} answered in the person's own words"`, `bp:1634`). §2 rung 7 claims «every answer keep[s] their own line, each cut at DECISION_CHARS_MIN» — false for free-text question answers. Blocking B5 (fix the text, and fix or queue the sibling).
- O-d and the closed vocabulary: today «words at level 1» is appended only when `chosen[1] == 1` (`bp:4431`) and `bp:4415` hard-wires `chosen = (0, 1, False, -1)`. If the last resort runs at level 2, the reason would silently become «doors only» — which `test_case_id_form_texts.py:215` (accepts only `== ["words at level 1"]`) and K7 (`test_brief_pack_s5_plan.py:509-512`, where «doors only» turns an overflow GREEN) read differently. The spec states the wanted outcome but not the code: `bp:4431` must become `chosen[1] >= 1` and `bp:4415` must take the chosen words level. Otherwise O-d can flip a red K7 verdict to green by renaming the reason. Folded into B3.
- O-d and the bisection at `tbp:2943`: the predicate «`- every decision in full - read` absent» is monotone in the ceiling iff the level choice is ceiling-independent — it is (both renders at the same fixed parameters; popping files shifts both by the same bytes). It tips inside 512..65536 iff level 1 is strictly shorter in the 10 KB fixture: gate 400 → 240 chars (−160), the `bp:1707` pointer and the others line gone (−~159), omitted line added (+~102) → ≈ −217 B. SAFE; M printing both numbers is the right proof.
- The class O-d addresses is systematic after K1, not a fixture accident: when every words line is ≤ 240 chars, no line is truncated and there is no other-stage decision, level 2 has NO pointer (`bp:1705` false) and level 1 = level 2 + the omitted pointer (+ the `## Not in the brief` heading when it opens it). Rung 7 then strictly ADDS ~100 B and buys an extra popped file line. The Lead's answer applies O-d only «when M shows a saving» on the S5 test fixtures — that fixes the instance, not the class. Blocking B3.

### 3. The over-ceiling line — sound idea, the computation order is not specified

- Placement «first line of `## Not in the brief`» keeps W3 (`tbp:2362`, the words heading stays the first `## `) and the by-range note at `top[2]` (`tbp:2447`; the note goes in at `parts = head[:2] + [note, ""]`, `bp:4321`). KEPT.
- BUT the order of computation is unstated (rule 11 (ii), positional). `over_ceiling`'s budget reasons are computed at `bp:4427-4434`; the SLICE check measures `text` at `bp:4437`; the note loop RE-RENDERS via `render(...)` (`bp:4444`). (a) If the line is inserted by string edit after the note loop, `huge["bytes"]` includes the line but the note's printed size does not → W8 (`tbp:2446-2447`) red. (b) If inserted before the loop but not passed into `render`, the loop's re-render drops it → the 30 KB brief has no over line (adversarial input (e) fails). (c) «subtracted in `budget_of`, the way `form_cost` is» is not implementable as written: `form_cost` is a constant subtracted from EVERY text, while `budget_of` is also called on every ladder attempt where the line is absent; a builder who instead detects the line by searching the text lets a person's warning containing the same words reduce the budget (a person's text then changes the trim). Blocking B1.
- Can the line change the predicate that prints it? Not if the predicate is computed on the render without the line (B1 states that). It can legitimately push `bytes` past `SLICE_BYTES` (30,000) and add «over SLICE_BYTES» — correct direction (real size).
- `DOORS_ONLY_BRIEF_MAX`: with F5 «outside», `budget_bytes` is unchanged by the line, so K7 cannot move because of it. K1/O-c can move the plan critic's level-1 bytes (O-c by −~97 B, K1 by ±waiver length); the spec's STOP on red K7 is right. N13.
- Adversarial inputs: (a) AT 6144 → no line, +1 → line: correct (`>` at `bp:4395/4428`). (b) multi-byte: correct (`measured_bytes` encodes UTF-8, `bp:3586`). (c) partly wrong wording: only the plugin root is tokenised (`bp:3582-3585`); the PROJECT checkout path (the `Branch check:` line, `tbp:2858`) is not, so a long checkout raises the budget and may itself trigger the line — safe direction, but the text should say so (N6). (d) correct (`bp:4423-4424`). (e) correct only under B1's order; `over_ceiling` stays `["words at level 1", "over SLICE_BYTES"]` because the reasons are computed before the line.

### 4. Edges — mostly decided correctly; three missing or mis-stated

- Correct as decided: no waivers (`bp:1708` guards the count line), only other stages' waivers (`bp:1710-1711`, `tbp:2900, 2919-2921`), a waiver over 240 chars (`bp:1693`, `_short`), zero input files (`bp:4341`, `bp:4423`), only doors, under-ceiling briefs (all four changes act at rung ≥ 7 or when over), the 10 KB fixtures (see 2), `DOORS_ONLY_BRIEF_MAX` STOP, PC2-1 (`s5_ceiling` present at `tbp:2315`).
- «ten waivers» / «a waiver list so long the brief is over at every level»: covered — rung 8 then §3; past 30 KB the by-range note. Correct.
- MISSING: K1 changes the level-1 brief of EVERY stage and role with a waiver of its stage, stage `"*"` included (`bp:1692` `entry.get("stage") in (stage, "*")`), not only the S5 automator and code critic. Such a brief that reaches level 1 now carries N lines of ≤ 242 chars instead of one ~108-char count line and may pop more file lines — the intended trade (the direction), but undeclared in §4, the changelog and A2's witness scope. N10.
- MISSING: question answers lose their words at level 1 (see 2) — B5.
- MISSING: `--output` / `--dry-run` — the over line says «here whole or one named file away», but with `--output` no side file is written (`bp:4458`, W5 `tbp:2410-2411`). N12.
- MISSING: the stderr displacement of the stdout note (see 1) — N2.

### 5. Forks as answered

- F1 (a): right against FR-8/AR-24 and the direction; `tbp:2432` is the only pin of the count line (grep `waiver\(s\) of|every decision in full` over the package: `bp:1707, 1709, 4318, 4328`, `tbp:2432, 2434, 2942-2948`). But the answer is not folded into §5 (B4).
- F2 left to the measurement: fine.
- F3 (a): defensible (the case files are the scope), but as written it needs the positional invariant (B6), and with anything still popped it moves the loss onto named inputs that `tbp:2877-2879` read (B2). Also it moves the critic's per-dispatch findings path (`bp:4188-4192`, FR-15; mitigated by the form skeleton per the comment at `bp:4190`) and the snapshot masks (`bp:4213-4219`, «the last to be trimmed») earlier in pop order unless B6's text keeps them — the masks are the person's exclusions (FR-8).
- F4 (a): acceptable against AR-14/P27. On «must the owner be told»: the carrier says the direction is the LEAD's (`finding:15` «направление выбрано, Lead 11.11.2026»; `finding:34` «Решение владельца нужно: нет»), not the owner's, so no owner notice is owed by rule. But «hands the finding half to the conductor» is not true in effect: no conductor rule turns a `note:` line into a run finding; the half is DROPPED by Lead decision. Say so and record it in the finding/batch «Ход» so the batch close does not read item 3 as unmet (N7). The data is not lost (the line is in the brief file on disk, readable by a measurer — FR-55).
- F5 outside: right against AR-20 (K7 untouched).
- F7 (a): fine; PC2-1's core is in `tbp:2300-2325`.

### 6. Architecture

- AR-24, AR-21, AR-20, AR-22, AR-12, AR-10: right set, each kept under the fixes (AR-22's conductor half is conditional — N2). Add a «not touched» line for AR-17 (the over case is not a state with no move; the conductor learns via a note, not the seam) — N11. AR-27 n/a (not a story finding, F4).
- AR-29 / P27: nothing judges a role — the line reports a byte fact, O-d is a byte comparison, K1 is a carry rule. KEPT.

### 7. Executability for a Sonnet builder

- E, M, W: executable (`tbp:501 expectation_lines`, `tbp:2773 main` exist; `s5_ceiling` model at `tbp:2315-2325`).
- Selection rule: the stop condition is too weak (B2) and O-d is gated on the wrong evidence (B3). On STOP, the fate of the already-applied edits is unsaid (N9).
- Owns by function: `decisions`, `build` (incl. nested `render`), `main` cover K1/O-c/O-d/F3/§3. A module-level constant for the line text would fall outside owns (N11). The `tbp` owns conflict with the Lead's A5 answer (B4).
- Left to invent: the over-line computation order (B1), the F3 categorisation and render-order preservation (B6), the `bp:4415/4431` edits (B3).
- Step P: a real proof for its sample IF deterministic; the change is structurally confined (dec_level 1, rung 8, over), so a sample + reading suffices. Weaknesses: no determinism control (two BEFORE runs) and no negative control (a deliberately altered brief shows a differing hash); a naive F3 (reordering the appends at `bp:4229-4236`) changes EVERY brief's file list and P would only then catch it after the fact (N8, B6).

---

## Blocking findings (each with the exact spec text to change)

**B1 — §3 item 2 (computation order of the over line; W8 and input (e)).** Replace §3 item 2 with:
«2. The line is OUTSIDE the budget (fork F5). Order inside `build`, after the last-resort loop: (i) compute the budget reasons of `over_ceiling` (`bp:4427-4434`) and `budget_bytes = budget_of(text)` on the render WITHOUT the line — this number is the one returned; (ii) if a budget reason exists, re-render with the line as a new `render()` argument (like `note`), the line first in `## Not in the brief`, the section opened when absent; (iii) only then the SLICE check (`bp:4437`) and the by-range note loop (`bp:4440-4447`), which passes the same line argument on every re-render. `budget_of` is never applied to the text with the line, and the line is never found by searching the text. The line is NOT appended to `omitted` (that list is «one line per thing taken out»).»

**B2 — §1.4 selection rule (stop condition) and A1.** Replace «if every build in the M table is within the ceiling with no case line and no S5 waiver lost, stop there» with:
«if every build of the M table (`tbp:769, 2202, 2239, 2855, 2933`) keeps the S5 waiver inline AND has NO `input file(s) - read` line in `omitted` (nothing popped at all), stop there. A build that still pops any file line is NOT covered, whatever F3 keeps: with F3 (a) the named inputs are popped before the case files, and `tbp:2877-2879` (the test-plan slice and bundle lines, green today) read them.»

**B3 — O-d is the class fix; name the code.** Replace the selection rule's «Else add O-d if M shows it saves > 0 for a failing build; re-run M» and the F2 answer's «(when M shows a saving) O-d» with:
«O-d is applied ALWAYS with K1 (with K1, any brief whose words lines are all ≤ 240 chars, none truncated and no other-stage decision is strictly LONGER at level 1 by the `bp:4317-4318` pointer, so rung 7 would buy a popped file line). Code: rung 7 is taken only when `budget_of(level-1 render) < budget_of(level-2 render)` at `(0, ·, False, -1)`; `sides_needed` is the one of the render actually kept; `bp:4415` sets `chosen` to the kept words level; `bp:4431` `chosen[1] == 1` becomes `chosen[1] >= 1`, so «words at level 1» (= the words at their shortest kept form) is still named and `test_case_id_form_texts.py:215` and K7 read the same reason.»

**B4 — fold the Lead's answers into §5 (owns are normative).** In the §5 block replace the `tbp` owns line with:
«`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py` (ONLY the N4 W6 block, `n4_scenario`, `tbp:2423-2440`: line 2432's expectation → the S5 waiver line inline; ONE added `check_in` that the first line of `## Not in the brief` of `battery` starts with `f"- the brief stays over its {brief_pack.BRIEF_MAX_BYTES} B budget after every cut ("` and names `words at level 1`)»;
in non-goals replace «no edit of any expectation in test_brief_pack.py except F1(a)» with «… except the two W6 edits above»; in A2 replace «The one exception is `tbp:2432` if and only if the Lead answered F1 with (a)» with «The exceptions: `tbp:2432` (new expectation: the S5 waiver line inline) and the one added W6 check»; in A5 delete «No new test is written for it … only on the Lead's word (it would change `tbp`)» and write «guarded by the one W6 check of the owns line; its expected text is built from `brief_pack.BRIEF_MAX_BYTES` (A3: no numeric literal)».

**B5 — §2 rung 7: the question-answer sibling (class completeness, rules 5/14).** Replace «every open halt and every answer keep their own line, each cut at `DECISION_CHARS_MIN`» with:
«every open halt and every JOURNAL answer keep their own line, each cut at `DECISION_CHARS_MIN`; a QUESTION answer keeps its line in the existing minimal form — the id and the reading letter, a free-text answer WITHOUT its words (`bp:1603, 1621, 1634`), whole in `<ID>-decisions.md`»,
and add to «Noticed, not widened»: «queued: the person's free-text question answers lose their words at level 1 (`question_answer_lines` minimal, `bp:1621`) — the same FR-8 class as the waiver; owner of the node: Lead of `package-ci` (a finding file + a row in the next untaken batch, D-0044)». (Or include it in K1 — the Lead's call; either way the remainder is named.)

**B6 — §2 rung 8 / F3: positional invariant.** Replace rung 8's text with:
«8. Input-file lines. The ORDER IN WHICH THEY ARE RENDERED in `## Read these files` does not change (an under-ceiling brief stays byte-identical, step P); only the POP PRIORITY changes, first popped to last: (1) source material lines (`bp:4236`); (2) the other non-door lines of `files` that are not case lines, not the window test file and not the snapshot line with its masks/view block (`bp:4213-4224`), popped from the end — incl. the «critic findings: none yet» line and the code-critic's per-dispatch findings line (`bp:4192`); (3) the snapshot masks/view block, from its end; (4) the case lines — the `cases[:8]` lines and the «... and N more case files» line (`bp:4229-4232`), «... and N more» first, then last case first; (5) the window test file (`bp:4235`). Doors never. A line's category is decided when `files` is built (e.g. a parallel list of tags), never by re-parsing its text. `trimmed_files` keeps the lines in their RENDERED order (insert at the original position, the invariant of the comment at `bp:4303`), so `<ID>-files.md` lists them as the brief did.»

## Non-blocking findings

- N1 — §1.4 bullet «Words level 1 is NOT always shorter»: replace «ADDS `- every decision in full: <path>` (`bp:4328`) AND a second pointer» with «carries the `bp:4328` pointer where level 2 already carried `bp:1707` (the fixture has an S1 waiver, so `others` = 1), ADDS the `## Not in the brief` pointer (`bp:4317-4318`)»; and note: after K1 + O-c level 1 is ~57 B shorter on this fixture, so O-d saves 0 there.
- N2 — §3 item 3 / AR-22 row: add «Edge: `_brief` returns the last line of stdout+stderr (`story_step.py:152, 453`); a helper failure printed to stderr during `build` (`bp:3115` …) displaces the note. Queued (story_step outside owns): `_brief` reads the line starting `brief: `.» with an owner.
- N3 — §1 AR-22 row: «`main` prints no `over_ceiling`» → «`main`'s line (non-`--json`) prints no `over_ceiling`; `--json` prints it, and no caller uses `--json`».
- N4 — §3 item 3: fix the position: «inside the parentheses, right after the `against the ceiling` clause, before `, side files:`»; note `test_story_step_materialize.py:247`'s regex then does not normalise an over brief (none in that fixture today).
- N5 — §3 item 1: «`<reasons>` = the entries of `over_ceiling` among `words at level 1`, `doors only`, in that order» (excluding `sd head`, `over SLICE_BYTES`), or state otherwise.
- N6 — §3 (c): «only the plugin root is tokenised; the project checkout path (the `Branch check:` line) counts in the budget, so a long checkout can itself trigger the line — the safe direction».
- N7 — F4 answer: replace «is the conductor's move on the note» with «is dropped by Lead decision (AR-14, P27); the over line stays in the brief file for any measurer» and record it in the finding/batch «Ход».
- N8 — Step P: add «run the BEFORE snapshot twice (identical hashes = the determinism control) and once with one fixture deliberately altered (a differing hash = the negative control); both outputs in the report».
- N9 — Selection rule: on STOP, «leave K1, O-c, O-d, F3 and §3 in the tree uncommitted, report the M table; the Lead decides».
- N10 — §4: add row «K1 at other stages/roles (stage `*` waivers included, `bp:1692`): a level-1 brief now carries each waiver line; it may pop more file lines — by the direction; the changelog fragment says so».
- N11 — §1 «Not touched»: add AR-17; §5 owns: the line text lives inside `build` (or name a module constant in owns).
- N12 — §3 line text under `--output`/`--dry-run` (side files not written, `bp:4458`): append «(side files not written in this run)» as `bp:4241` does, or reword.
- N13 — `DOORS_ONLY_BRIEF_MAX`: if K7's measured doors-only size FALLS (O-c), report the new number; tightening the ratchet is the Lead's call (AR-20).
- N14 — A1: note that run 43110913721's artifact shows 3 of the 5 FAIL lines (selftest truncation); `tbp:770`/`2244` rest on the count and on run 43092267661.

## Duplication and consistency / code quality (critic-diff-brief items 6-7, plan form)

- Duplication: the plan REMOVES one (the doubled decisions pointer, O-c). Risk of a new one: a second category scheme for file lines (B6 says one tag list built with `files`). None other found: grepped `every decision in full|waiver\(s\) of` and `over_ceiling` over the package.
- Code quality: the over line as a `render()` argument mirrors `note` (B1) — one rendering road. The `bp:4415` hard-wire is replaced, not duplicated (B3).

## One action, one road (item 12, P31)

- None found that blocks: K1 applies to every stage/role alike (N10 makes it explicit); the over line is produced for every role by the same predicate; O-d (under B3) applies to every brief. No exclusion of a language, project or case.

## Class completeness (SIBLING_MAP)

- No SIBLING_MAP axis names the brief trim order (grep `brief_pack|ceiling|budget` in `docs/SIBLING_MAP.md`: hits are other axes; `DOORS_ONLY_BRIEF_MAX` sits under the ratchet axis 18 by AR-20). In-artifact sweep of «person's words dropped at level 1»: gate — kept (cut); warnings — kept; halts — kept; journal answers — kept; waivers — fixed by K1; question answers — NOT kept (B5: fix or queue). «A words rung that costs bytes»: B3 makes it class-wide.

## What I did not check

- No test or M run (non-goal); byte figures above are by line length, not measured.
- `tbp:770` and `tbp:2244` as red in run 43110913721 (not printed in the artifact).
- Whether the plan critic's K7 fixture holds a waiver (K1's effect on K7 unmeasured).
- `scenario_walk.py --witness-for brief_pack.py` output (the DoD's witness list) — not executed.
- Other roles' tests that read a squeezed brief's file lines (`test_brief_pack_roles.py`, `_manual.py`, etc.) beyond the grep for `minimal`/`every decision in full`/`waiver(s) of`.
- `source_material()` contents per role and whether any S5 role has a ticket snapshot in its names.

## Trail

Read: the spec whole; the finding whole; `bp:1600-1735, 3570-3599, 4180-4508`; `story_step.py:143-153, 436-461, 1160-1239`; `tbp:77-126, 730-789, 2150-2254, 2290-2475, 2840-2984`; `test_brief_pack_s5_plan.py:425-516`; `test_case_id_form_texts.py:190-219`; `ci-out/c2/package-full-shard-2/selftest-shard-2-of-2.txt:38-52`; `tools/critic_verdict.schema.json`; `architecture.md` AR-20 block; `test-layers.json` `keep_fail_at_entry`.
Greps (case-insensitive where content-negative, positive control noted): `over_ceiling` over the package (control: hits `bp:4427`); `waiver\(s\) of|every decision in full` over the package; `minimal` over tests; `decisions\(` over scripts; `sys.stderr|warnings.warn` in `bp`; `against the ceiling|B, side files|note: brief: ` and the size pattern over tests (control: hits `test_story_run_s6_w1_frozen.py:29`); `brief_pack.build(|"brief: |budget_bytes|against the ceiling` outside tests; `^FAIL` and `FAIL.*(brief|waiver|case files|10 KB)` in `ci-out/c2`; `brief_pack|ceiling|budget` in `docs/SIBLING_MAP.md`.
Needed beyond the manifest: `story_step.py:143-153` (`_run`), `test_story_step_materialize.py:247`, `test_story_run_s6_w1_frozen.py`, `docs/SIBLING_MAP.md`.

The decision to accept the plan and to apply these fixes is the Lead's (rule 6): this verdict is an input.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 sec.3 item 2: the over line's computation order is unstated - it must be a render() argument added after the budget reasons and BEFORE the SLICE check and the by-range note loop (else tbp:2447 W8 red or the line lost in the 30 KB brief); budget_bytes computed on the render without the line, never by searching text; not in omitted",
    "B2 sec.1.4 selection rule: stop condition 'no case line lost' is too weak - with F3(a) named inputs read by tbp:2877-2879 are popped instead; the condition must be 'no input file(s) line in omitted' for the five builds",
    "B3 O-d gated on fixture savings fixes the instance: after K1 any brief with short, untruncated words and no other-stage decision is strictly longer at level 1 by the bp:4317-4318 pointer; apply O-d always and name the bp:4415 and bp:4431 (chosen[1] >= 1) edits so the over_ceiling reason stays 'words at level 1'",
    "B4 sec.5 owns/A2/A5 contradict the Lead's answers (tbp owns only line 2432 vs the added W6 check_in); fold the answers into the header and build the check text from brief_pack.BRIEF_MAX_BYTES",
    "B5 sec.2 rung 7 claims every answer keeps a 240-char line; question answers keep only id and letter, free-text words dropped (bp:1603, 1621, 1634) - the FR-8 sibling of the waiver is neither fixed nor queued",
    "B6 sec.2 rung 8 / F3: positional invariant missing - rendered file order must stay (step P), only pop priority changes; categories tagged when files is built; trimmed_files keeps rendered order; masks block and case-file 'and N more' line placed explicitly"
  ],
  "class_completeness": "No SIBLING_MAP axis covers the brief trim order; DOORS_ONLY_BRIEF_MAX is under ratchet axis 18 (AR-20). In-artifact sweep of person's words at level 1: gate, warnings, halts, journal answers kept; waivers fixed by K1; question answers not kept (B5, fix or queue). The 'words rung that costs bytes' class is made class-wide by B3. K1 reaches every stage and role with waivers including stage '*' (N10).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-042-pc2-6-briefs-over-ceiling.md",
      "plans/piles/package-ci/findings/20261111-kanon-krasnyj-brief-pack-brify-vyshe-potolka-6-kb.md",
      "ai-packages/qa-factory/scripts/brief_pack.py:1600-1735,3570-3599,4180-4508",
      "ai-packages/qa-factory/scripts/story_step.py:143-153,436-461,1160-1239",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py:77-126,730-789,2150-2254,2290-2475,2840-2984",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py:425-516",
      "ai-packages/qa-factory/scripts/tests/test_case_id_form_texts.py:190-219",
      "ci-out/c2/package-full-shard-2/selftest-shard-2-of-2.txt:38-52",
      "ai-packages/qa-factory/design/architecture.md AR-20",
      "tools/critic_verdict.schema.json",
      "docs/SIBLING_MAP.md (grep)"
    ],
    "reruns": [
      {
        "command": "Grep over_ceiling -i over ai-packages/qa-factory",
        "result": "only brief_pack.py, CHANGELOG.md:139 and tests; no non-test consumer"
      },
      {
        "command": "Grep ^FAIL in ci-out/c2 selftest shards",
        "result": "test_brief_pack 873/878 ok; three FAIL lines printed (2876, 2899, 2206); 770 and 2244 not visible"
      },
      {
        "command": "Grep waiver(s) of|every decision in full over the package",
        "result": "bp:1707,1709,4318,4328; tbp:2432,2434,2942-2948 only"
      }
    ]
  },
  "fixes": [
    "B1: replace sec.3 item 2 with the stated computation order (render argument, before the SLICE check and note loop, budget on the render without the line, not in omitted)",
    "B2: selection rule stop condition = S5 waiver inline AND no input file(s) line in omitted for tbp:769,2202,2239,2855,2933",
    "B3: O-d always with K1; name bp:4415 kept words level, bp:4431 chosen[1] >= 1, sides_needed of the kept render",
    "B4: sec.5 owns, non-goals, A2, A5 rewritten to the Lead's answers; the W6 check text built from brief_pack.BRIEF_MAX_BYTES",
    "B5: rung 7 text corrected for question answers and the sibling queued with an owner (or included in K1)",
    "B6: rung 8 rewritten as pop priority over an unchanged rendered order, with tagged categories and rendered-order trimmed_files"
  ]
}
```
