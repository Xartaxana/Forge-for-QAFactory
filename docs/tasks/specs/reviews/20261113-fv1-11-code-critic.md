# FV1-11 code review (critic, one pass) - S0 keeps a first-line title without a question

Diff: `git -C .claude/worktrees/fv111 diff be2c988..a9e4a82` (3e8a085 + fix round a9e4a82). All file:line below are in the
fv111 worktree (`ai-packages/qa-factory/` unless a path says otherwise).

## Verdict

**ACCEPT WITH FIXES (fit_with_fixes)** - no blocking finding in the code's behaviour. The DoD's behaviour holds; four
fixes are needed before merge (F1-F3 fix before merge, F4-F5 queue or fix). The decision to accept is the Lead's.

## Findings

**F1 (fix before merge) - the record line does not say WHICH line was taken as the title, and gate A has no other place
that shows it.** `scripts/driver_s0.py:1163-1164` (`s0_pass_phrase`) gives
`S0: the ticket-title check: title taken from the first line (kept without asking)`. The title itself is only in the
pass's `witness` (`driver_s0.py:1572`), which goes into the local-calibration finding, not to a person. Gate A shows
`pipeline.warnings[:5]` (`scripts/gate_brief.py:3267-3272`), and `gate_brief.py` does not read the ticket snapshot or
its title (Grep -i `ticket-snapshot|snapshot.{0,30}title` on gate_brief.py found nothing; positive control: the same
tool on the same file finds `get("title")` at :1902/:2672). Before this change the person saw the quoted title inside
the question. Now the person learns that a title was taken but not what it is, so a greeting, a URL or a cut paragraph
taken as the title (Q3) cannot be caught at gate A. Both commits' `judgment:` line ("the person still corrects the title
at gate A") depends on the person seeing the title, and right now they cannot. Fix: put the quoted title in the
phrase, for example
`S0: the ticket-title check: title taken from the first line (kept without asking): "<s0_quote(title)>"`, inside
`S0_LINE_LIMIT` (180, gate_brief cuts at 180). Take the title from the stored pass (add a `title` key to the record
`s0_record_pass` writes, or read the witness tail) so that `s0_rest` (:2404) and `skip_sources_late` (:2208) still use
one phrase. The K-F2 pin at `scripts/tests/test_story_run_s0.py:1895` and the unit row at :1937 change with it.

**F2 (fix before merge) - a reference text still promises the removed question.**
`references/templates/ticket-snapshot.md:34-36`: "...takes its FIRST non-empty line as the title ... and the person is
asked once whether that will do (`go on` keeps it; or add a `# ` title line and answer `retry`)". `phases/s0.md` and
`references/adapters-read.md` point readers to this template (Grep `templates/ticket-snapshot\.md`). The fix report says
"No hit remains in design/, skills/, references/", which is true only for the literal `ticket_title`. The dispatch also
asked for a grep of the question's wording, and that grep finds this line. Fix: "...kept without asking; the story
record carries the line and gate A shows it". Lines 38-40 of the same paragraph ("A text with no criteria ... the person
is asked") are older than D-0050 and also stale. They are outside this node's class, so they go to «Остатки», not into
this fix.

**F3 (fix before merge) - code comments in files this diff edits still describe the question.**
- `scripts/ticket_adapter.py:105-106` (module docstring): "...says so in `provenance.title_from` (`first_line`) and
  the driver asks the person once."
- `scripts/ticket_adapter.py:468-469` (`split_body` docstring): "...and the driver asks the person once".
  The diff fixed the comment at :686-688 in the same file and missed these two (sweep-the-artifact-first).
- `scripts/driver_s0.py:1212-1215` (block comment above the REST ticket section): "a title the reader took from the
  first line and a criteria section the reader lost ... are the person's questions (F2, F5)".
Each is an annotation that is now false (brief item 7). Fix: one clause each, "kept without a question, recorded".

**F4 (non-blocking; queue or fix) - the taken-title line can land below gate A's five.** `driver_s0.py:2404` appends
the pass lines after the readiness `WARN` lines (:2385), the stand line (:2396) and the `data_cleanup` lines (:2400).
The lines inserted at the front (experiment :2418, criteria :2414, implementation source :2409, sides :2423) push it
down further. Gate A shows the first five (`gate_brief.py:3271`), so with three front lines and two readiness WARN lines
the title line is sixth and no person sees it. How often readiness prints 2 or more WARN lines is an estimate, not
measured. A `go on` line had the same position before, but the person had already answered that question. The taken
title has no other carrier to a person. Fix: insert the factory-taken line right after the criteria line, the way the
SS1-13 line is placed. Otherwise «Остатки»: `the taken-title line of S0 can fall past gate A's five warnings | узел: <id>`.

**F5 (queue) - the sentinel string is compared in three places.** `driver_s0.py:1163`, `:1180`, `:1198` each branch on
`words == self.S0_TAKEN_WORDS`. The person's words cannot equal the sentinel: the `go on` door stores the raw words only
after they normalise to `go on` (`:782`, `:795`). So this is not a bug, just three copies of one decision. `:1180` could
reuse `s0_pass_phrase` for both branches if the print may carry the quoted words. Severity: queue.

No other findings. Not findings: the K3 pin row removal (Q5), the price row removal (Q2), the e2e `retry` block
removal (Q4).

## Answers to the dispatch questions

**1. The unreachability proof - right.** In `s0_criteria` (:1560-1573) `problems` is the literal one-item list (:1561).
`s0_record_pass` is the only writer of `s0_passes` (Grep -i `s0_passes` over scripts: the writer is at :1154 only; the
other hits are reads, the cleanup at :2445 and tests). Its two callers are :1572 (same constant) and `s0_read_word` :795
(`ask["problems"]` of a stored ask, which the old raise built from the same constant). So `s0_passed` (:1175 subset
test) is always True after :1567-1572. Paths walked:
- resume: the pass is in `driver-state.json`. On re-entry :1567 skips the write and :1573 re-reads it.
- retry of S0: the same.
- local-key story: `s0_local_file` (:876-881) gives the same file path, so the same branch runs. A local text whose
  first line equals the key goes to `ticket_no_title`, as the DoD asks.
- paste door: the paste is written to `driver-tmp/ticket-<T>.md` (:840-844) and read by the same adapter.
The criteria gap is a separate path after the branch (:1588-1590), and the TITLE-PLUS-OTHER-PROBLEM row
(test_story_run_s0.py:1924) proves it still stops. One residual is not a defect: when a later paste gives a different
first-line title, the stored pass keeps the old witness. The finding is filed once anyway (idempotency key, :1200).

**2. Stored question - every answer still handled; removing the rows starves no reader.** `s0_read_word` (:761-861) is
generic over the stored `s0_ask`. Each answer of an older stored `s0.ticket_title` question:
- `stop`: `s0_again` with the stored text (:785-790).
- `retry`: nothing to drop, the step runs again (:791-793). If the file still has no `# ` line, the title is now taken
  silently.
- `go on`: `s0_record_pass` with the same shape as before (:794-795). Not byte-identical, because the code moved into
  the shared writer, but the same behaviour. The DoD's one-writer requirement asks for that.
- paste: :836-847.
- any other words: the `unread` seam with the stored text and doors (:848-860). The seam (`driver_conductor.py:852`)
  takes no question key.
The price is rendered into `s0_ask.text` when the question is raised (`s0_stop` :733-737), and `no_move.load_question_prices`
is called by key only when a question is raised. So no reader looks up `s0.ticket_title` on resume. A stored block with
no answer is cleared on entry (:778), and the title is then taken. FR-40/AR-25 hold. The doors census: the K15 row and
its raise site left together, and the stored-question block (`test_conductor_doors.py:770-779`) replaces them.

**3. P22/FR-48/FR-3.** The record reaches a person only through gate A's warnings (`driver_s0.py:2404` ->
`pipeline.json` -> `gate_brief.py:3271`), plus the S0 stdout print (:1180-1181) and a local-calibration finding
(:1195-1203). It can be lost in two ways: it does not name the title (F1), and it can fall past the five (F4). A first
line that is not a title (a greeting, a URL, a 2,000-character paragraph cut at 200 by `ticket_adapter.split_body`
:493-494) is accepted with no check. That is what the node is meant to do (the finding's "Что сделать": take the first
line, stop only on empty text), and a code check on whether a line "looks like a title" would be judgment in code (P27,
FR-12). The remaining gap is the person's visibility, which F1 and F4 close. No new node is needed beyond F4 if F1 is
fixed now.

**4. Removed e2e block and changed rows - justified.** The K-F2 `retry` block exercised "live question, add a `# ` line,
`retry`". That path no longer exists, because no live question is raised. `retry` on a STORED question is covered at
unit level twice: `test_conductor_doors.py:771-779` and `test_story_run_s0.py:1947-1953`. Both check that no pass is
recorded and no block is left. The changed K-F2 rows (:1877-1897) now pin the new e2e behaviour: no title stop, readiness
first, the record line once, the finding once. The wiki rows (:2286, :2332-2335) drop the `go on` step that no longer
exists and keep the snapshot checks. The removed question-text checks in `t287_texts_name_the_file_read` checked text
that no longer exists. The new unit rows would catch the node's defect: FIRST-LINE-TITLE expects `("line", None)`, and
the old code raises `ticket_title`.

**5. K3 pin row and marker - right.** The removed sentence (`phases/s0.md:79-80` before the change) described a question
to a person. The marker `person-owned: access` classifies who owns a question, and the new sentence ("kept without
asking") puts no question to anyone, so a marker there would be false. K3 ties the marker count to the row count, so
22 -> 21 follows. Control re-run green (trail). This is a test constant, not an axis-18 ratchet.

**6. Role text.** `design/driver.md:169` and `phases/s0.md:79-80, 506` now match the code. The table row's "gate A shows
it" is true only within F1/F4. Remaining promises of the live question: `references/templates/ticket-snapshot.md:34-36`
(F2), and code comments `ticket_adapter.py:105-106, 468-469` and `driver_s0.py:1212-1215` (F3). Search: Grep -i
`ticket_title|asks the person once|title the reader took|could not find a title|that line will do as the title` over the
package. Positive control: it finds `driver_s0.py:54/1567`. No hit in agents/, skills/ (except the lines changed),
design/ or references/. A second Grep -i `title.{0,60}first (non-empty )?line|first (non-empty )?line.{0,60}title` over
`*.md` found the template; `CHANGELOG.md:3520` is history.

**7. Analogs (axis 5 and the class "a check stops though a reading was found").** The first report names
`s0_criteria_gap`, `readiness` and `flags`. None of them belongs to the class. `ticket_incomplete` stops because the
reader read nothing from a section (I4). Readiness stops because something required is missing. `flags` stops because
of two sources where the choice is the person's. Walked: all 14 `s0_stop` sites of `driver_s0.py` (:911 key_form,
:961 no_change, :1038 deliverable, :1262 ticket_auth, :1358/:1475 ticket_read, :1577 ticket_no_title, :1692
ticket_incomplete, :2049/:2080/:2168 source_list, :2239 flags, :2309 stand, :2371 readiness). None of them stops after
the code found an acceptable reading. No node is needed. Axis 5 twin "skill phase <-> driver" (SIBLING_MAP.md:128): both
sides changed together. Twin "one question for every stop" (:123): the raise is inside `s0_stop`, so A27's baseline is
untouched.

**8. DUPLICATION AND CONSISTENCY.** The diff removes duplication. `s0_record_pass` (:1151-1158) is now the one writer of
`s0_passes`: the inline dict at `s0_read_word` became a call to it. `s0_pass_phrase` (:1160-1165) replaces two inline
copies of the record line (old :2208-2209 and :2405-2406). The remaining copy of the decision is F5. No second
implementation was found: Grep -i `s0_passes` over scripts shows one writer; Grep -i `passed by the person's word` over
the package (fixtures excluded) shows no other reader parsing S0 pass lines. The clone ratchet (`forge-check`) output was
not attached: batch level, read at the PR.
**CODE QUALITY.** The new functions are 8 and 6 lines; `s0_criteria` got shorter. No dead branch is left: the
unreachable raise was deleted in a9e4a82. The test function name `s0_title_question` (test_story_run_s0.py:1876) now
names a question that is not asked. That is cosmetic, not a finding. The false comments are F3.
**Ratchets (question 9).** No in-tree ratchet row was added or raised. `question-prices.json` lost one row (a data key,
not a ratchet). The K3 SITES count went 22 -> 21 (a pin list). `role-load.json`, `judgment-census.json` and
`dup-baseline.json` are untouched (diff stat).
**JUDGMENT (q11).** No census row was changed. The code records the adapter's existing reading and judges no wording.
`judgment: none` holds once F1 lets the person see the title.
**ARCHITECTURE (q10).** AR-9 and AR-25 are named in the commits and hold. AR-14 (one writer) is also touched, kept
(improved) and not named; that is minor. The a9e4a82 line "keeps its handler and its rows" is inaccurate, because the
price row was removed in that same commit. The handler keeping the state is what AR-25 needs, so this is not a finding.
**ONE ROAD (q12).** None found. The diff adds no language, project or runner branch. The wiki/markdown wording at
:1568-1571 is the existing `provenance.markup` reading and is used only for the witness. Searched: the diff hunks.
**Hygiene.** The changed files are English; selftest --lang 2/2 was attached.

## Spot-checks

- Lead's re-run of test_conductor_doors 219/219: consistent with the diff (the K15 raise row was removed and 2 stored
  rows were added). Not re-run.
- Builder claim "no hit remains in references/": partly false (F2).
- Builder claim "the K15 census requires a raise site per row": consistent with `test_conductor_doors.py:670` docstring
  ("`awaiting`: data rows whose ...") and the removed raise.

## Trail

- Read: `docs/tasks/critic-diff-brief.md`; the full package diff; `driver_s0.py` :720-861, :1140-1220, :1540-1710,
  :2180-2282, :2290-2315, :2370-2430; `gate_brief.py` :3250-3285; `ticket_adapter.py` :97-113, :457-500, :572-600;
  `references/templates/ticket-snapshot.md` :28-41; `driver_conductor.py:852-864`; both reports; the finding;
  `tools/critic_verdict.schema.json`; `docs/SIBLING_MAP.md` axis 5 (:111-150), axis 34 heading.
- Greps (case-insensitive where stated): listed in Q6, Q8 and F1; the `s0_stop` site list (Q7); `title_from` in
  `ticket_adapter.py`; `question-prices` over scripts; `local-tickets` in tests; the commits' `architecture:` and
  `judgment:` lines.
- Control re-run: `( cd .claude/worktrees/fv111/ai-packages/qa-factory && python -B scripts/tests/test_conductor_investigates_first.py )`
  -> `=== test_conductor_investigates_first: 33/33 ok ===`.
- Not run (forbidden here): test_story_run_s0.py (the builder's scratch 53/53 is its stand-in; CI judges the file).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 5 twin skill-phase<->driver: both sides changed (s0.md, driver_s0.py). Twin one-question-for-every-stop: the raise lives in s0_stop, A27 untouched. Same-artifact sweep incomplete: ticket_adapter.py:105-106 and :468-469 and driver_s0.py:1212-1215 still describe the question (F3); references/templates/ticket-snapshot.md:34-36 still promises it (F2). The class 'S0 check stops though a reading was found': all 14 s0_stop sites walked, no other member, no node.",
  "fixes": [
    "F1 driver_s0.py:1160-1165 (+ s0_record_pass :1151-1158): the factory-taken record line quotes the taken title within S0_LINE_LIMIT (180) so gate A shows WHICH line was taken; update the pins test_story_run_s0.py:1895 and :1937 - fix before merge",
    "F2 references/templates/ticket-snapshot.md:34-36: drop 'the person is asked once ... go on ... retry'; say the first line is kept without asking and recorded for gate A - fix before merge",
    "F3 ticket_adapter.py:105-106, ticket_adapter.py:468-469, driver_s0.py:1212-1215: comments still say the driver asks the person; correct them - fix before merge",
    "F4 driver_s0.py:2404: the taken-title line can fall below gate A's first five (gate_brief.py:3271); insert it right after the criteria line, or queue a node in Ostatki - non-blocking",
    "F5 driver_s0.py:1163/1180/1198: the S0_TAKEN_WORDS sentinel is compared in three places; fold into s0_pass_phrase - queue"
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/fv111 diff be2c988..a9e4a82 (package part, whole)",
      "ai-packages/qa-factory/scripts/driver_s0.py:720-861,1140-1220,1540-1710,2180-2282,2290-2315,2370-2430",
      "ai-packages/qa-factory/scripts/gate_brief.py:3250-3285",
      "ai-packages/qa-factory/scripts/ticket_adapter.py:97-113,457-500,572-600",
      "ai-packages/qa-factory/references/templates/ticket-snapshot.md:28-41",
      "ai-packages/qa-factory/scripts/driver_conductor.py:852-864",
      "docs/tasks/specs/reports/20261113-fv1-11-report.md",
      "docs/tasks/specs/reports/20261113-fv1-11-fix-report.md",
      "plans/piles/live-run-fvf/findings/20261112-s0-ostanovka-na-tikete-bez-zagolovka.md",
      "docs/SIBLING_MAP.md:111-150",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "( cd .claude/worktrees/fv111/ai-packages/qa-factory && python -B scripts/tests/test_conductor_investigates_first.py )",
        "result": "=== test_conductor_investigates_first: 33/33 ok ==="
      }
    ]
  }
}
```
