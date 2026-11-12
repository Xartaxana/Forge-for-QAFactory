# t-181 — why a recorded `go on` at the S5 exit_limit never lets the exit gate through

critic (opus), read-only diagnosis, 2026-11-12. Run package: `C:\QAFactory\exp-fvf\pkg-fix1\qa-factory\scripts\` (= "R").
Live artifacts: `...\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1\` (= "A"). Nothing in the run copy or the
live tree was changed. Probes ran in-process against COPIES in the scratch dir (`pipeline.copy.json`, `standing.copy.json`).

## Verdict on the three hypotheses

| # | hypothesis | outcome |
|---|---|---|
| 1 | the exit gate never consults `stage_overrides` for this finding class | **CONFIRMED, made precise**: the gate DOES read the words, but the class is *refused to every word at its source*. The gate's own judge classes the record `refused`, and no word passes it, `*` included. This is the design as written, not a lookup miss (verified, below) |
| 2 | matching fails because of how lines are split/normalised | **KILLED as the cause**: every one of the 15 recorded `go on` rows names the gate record whole under `names_whole` (15/15, verified). The record is never shown to the matcher. (The split causes a separate hazard: finding S2) |
| 3 | the exit_limit branch re-asks on the second refusal whatever the passes say | **TRUE BUT A CONSEQUENCE**: the ladder re-asks because the gate still blocks. The passes are already folded into the gate's result. The driver defect is upstream of the re-ask: it OFFERS `go on` for a record no word can pass, and says "recorded" over 15 rows that act nowhere (finding R2) |

## Root cause (trail)

R1. **The source refuses every word for this finding** (verified by reading and by a probe).
- `R\s5_precheck.py:3824`: `check_row_fields` emits the finding with family `"manifest"` and tag `row-fields-missing`. Its docstring (3797-3798) says: "Family `manifest`, outside PASSABLE: no recorded word, `*` included, and no judge pass lifts it - it is a repair the author makes with one command (FR-4)".
- `R\s5_precheck.py:82`: `PASSABLE = {"environment", "obligations"}`. `:101`: `WORD_PASSABLE_TAGS` does not hold `row-fields-missing`. So `_passable` returns False (3914-3917) and `refusal_cause` returns `"family"` (3931-3932).
- `R\s5_precheck.py:4660-4663`: `report` prints `WORDS_REFUSED_AT_SOURCE: manifest:-:row-fields-missing family` above a header that carries `(words judged at source)`. `passed_by_word` (3974-3976) returns a non-passable finding untouched: the source never even looks at the words.
- `R\detector_verdict.py:321-322` sets `words="source"`, and `_tag_lines` ties the refusal tag to the finding. `R\exit_gate.py:434-436` (`detector_records`) builds the Record with `refused="family"`.
- `R\exit_gate.py:1748-1749` (`word_class`): a record with `refused` set is `"refused"`. `:1783-1785` (`judge_words`): a `refused` record goes to `blocking` with no matcher call. That is why 15 valid rows, and even a `*`, change nothing.

Probe (in-process, R on sys.path, copies of the live pipeline and standing lines; the finding rebuilt from the standing lines, and the round trip checked):
```
passable? False | refusal_cause: 'family'
parsed words: source | refused: ['family'] | marker: repair
record == standing joined: True
refusal_parts(record) == standing lines: True
word_class: refused
LIVE overrides -> blocking 1 passed 0
LIVE + '*' -> blocking 1 passed 0
each go-on row names the record whole: 15/15
same text as a words=gate record -> blocking 0 passed 1
```
The last line is the control: the SAME text as a non-refused record is passed by the live rows. Matching works, and the refusal class alone blocks.

R2. **The driver offers a `go on` it cannot carry out, and reports success** (verified by reading, and by the live question).
- `R\driver_dispatch.py:3685-3749` (`exit_limit_facts`): `go on` is withheld for one reason only, an incomplete handover form (`absent["go on"]`, 3705-3708). There is no reading of whether the lines come from a record the gate refuses to every word. So the offer `(c) go on — the step closes as it is ...` (`A\state\driver-question.md`) promises what cannot happen (FR-10, P22 "promised and did not do", FR-2: a door the party cannot use).
- `R\driver_dispatch.py:3833-3842` (`_exit_go_on`): one `waiver.py` row per line. `waiver.py` accepts each row (it checks only form). Nothing re-asks the gate whether the rows passed anything. `:3793` prints "the person's answer `go on` is recorded" (`factory-23.log:4`). This is the TP1-15045 class that `waiver.recheck_stage_block` (`R\waiver.py:225-232`) exists for: "a silent OK over a standing block".
- `R\driver_dispatch.py:534-541` (`handoff_ladder`): on the next handover the set is the same, its key is in the resume record, and `exit_limit` asks the same question (`factory-23.log:9`). `_exit_go_on` drops duplicate rows (3839), so a second `go on` writes nothing and changes nothing. The question loops for as long as the person keeps answering `go on`. That is inferred from code; the log shows two rounds.

R3. **Below R1/R2: the repair the finding names does not exist for this project's language, while the door that does exist is denied by the text** (verified by reading and by a probe). This is the substance of `plans/piles/live-run-fvf/findings/20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md`, confirmed here.
- `R\s5_precheck.py:3764,3771-3773`: `obligation_refs` has `filled_by="marker"` (`R\window_record.py:187-188`), so the fix text says "written by the marker, not by hand ... put `qa(obligations=[...])` on the test and run `manifest_from_tests.py`".
- `R\manifest_from_tests.py:1341-1388` (`language_rows`): for a non-Python file no obligation field is written, and the note says "this language has no marker". The 10 failing rows are all `tests/api/cart/*.spec.ts` (`A\work\automation-manifest.json`, verified).
- The check itself accepts a hand-written value: `WR._obligation_refs_problem({"obligation_refs":[{"obligation_id":"OB-1"}]}, plan)` returns `''`, while absent refs return `'missing'` (probe, verified). The TS rows of TC-006 in the same manifest carry exactly that: `[{'obligation_id': 'OB-6'}]`, no hash (verified). `manifest_put.obligation_hash_problems` (`R\manifest_put.py:592-622`) refuses only a SENT hash it cannot vouch for; leaving the hash out "is the door".
- So the role WAS able to repair this, but the refusal told it not to. It concluded it was impossible ("needs a person's waiver", `A\state\driver-question-details.md`) and handed the repair to the person, who can only answer with a word that the source refuses.

## Why the t-180 fix did not help (verified)
t-180 (`_exit_go_on` 3837-3838) records the part of each line before ` — fix: `. That fixed the `<placeholder>` refusal by `waiver.py`, and the rows were written. But the rows were never the obstacle once written. The record is `refused`, so their content is never read (R1).

## Secondary findings

S1. **The line split makes the go-on rows over-broad** (the matching is verified, the hazard is inferred). Surface: the waiver block built from `waiver.refusal_parts` (`R\waiver.py:432-446`, split at `"; "`), used by `refusal_lines` (`R\driver_core.py:617-633`). The one multi-item finding became 15 rows such as `cart unchanged: obligation_refs (missing)` and `TC-001 Then 4 the cart never exceeds stock`. Under `names_whole` each such row passes ANY later S5 `words="gate"` record whose text contains that phrase. That is a pass the person never saw (FR-4). Neighbouring classes walked:
- magnitude: 15 rows for one finding. No cap, harmless in itself.
- nesting: the inner `; ` of the finding's own list (message and fix) is indistinguishable from the controller's join. That is the cause.
- encoding: the em dash ` — fix: ` partition is exact and safe (t-180).
- empty: `refusal_parts` drops empties, fine.

The row for the first line carries the `s5_precheck.py: ` prefix, which the source's text (`passed_by_word` 3979, no script prefix) never contains. So even a passable version of this finding (route B below) is not passed by these rows (probe: tag made passable in-process, live rows, finding kept = 1; an extra row `manifest:-:row-fields-missing` gives finding kept = 0).

S2. The S5 precheck says in its own output "These are repairs, not questions: nothing here goes to the person". Yet the exit_limit seam sends it to the person with `round / fresh / go on / stop`. This is FR-3/FR-48/P22, already item 3 of the live-run-fvf finding. Not new; noted for completeness.

## Proposed minimal fix (a proposal: the decision is the Lead's)

The question asks for "a recorded `go on` closes the step". Under the check's written design (R1, docstring 3797-3798: no word lifts it) **that is not achievable without changing the meaning of the check**. And while the repair exists (R3), the right outcome is that the role repairs it, not that the person waives it. So I propose route A (the minimum, keeps every documented meaning) and set route B out as a fork.

**Route A (recommended; main AND run copy):**

A1. *Source text names the door that exists*: `s5_precheck._row_fields_text` (`R\s5_precheck.py:3752-3781`). For `obligation_refs` on a row whose file has no marker reader (the same split `manifest_from_tests` makes: Python `TestFile` vs `LanguageFile`, `R\manifest_from_tests.py:1629`), name the fragment door: `{"tests":[{"instance_id":"<id>","obligation_refs":[{"obligation_id":"<plan obligation id>"}]}]}` through `manifest_put.py --task <T> --fragment <file>`, hash left out ("the code builds it").
- The twin render site, axis 28: `manifest_from_tests._row_form` (`:1721`, which today gives null slots only to `filled_by=="automator"` fields) changes in the same commit, or the role sees two answers.
- This is a P31 one-road decision. Either the fragment door is named for EVERY language (it works everywhere: `_obligation_refs_problem` reads only `obligation_id`), with the marker as the Python convenience, or the TS marker reader comes later. Pick one. This fork is the designer's and the Lead's, and needs a census row (see class completeness).
- Edges:
  - a Python row keeps the marker text, unless the uniform-door option is chosen;
  - a row whose file cannot be classified gets the fragment door (it works for both);
  - the hash is never asked of the role (`obligation_hash_problems` refuses a sent hash it cannot vouch for).

A2. *The driver does not offer what it cannot do*: `exit_limit_facts` (`R\driver_dispatch.py:3705`, beside the form rule). When any line that reached the seam comes from a record with `exit_gate.word_class(record) == "refused"`, put `go on` in `absent` with one truthful sentence: "the check refuses every word for N of these lines; only <role> can repair them". Then `round`/`fresh` stay.
- Data path: `handoff_ladder` still holds the `DV.Record` objects (`errors`, line 535) before `refusal_lines` flattens them to strings. Pass a count (`refused=`) into `exit_limit`, then `exit_limit_facts`.
- Edges:
  - form lines (plain `str`) read as `named` and are unaffected;
  - the `refusal`/`structured`/`session_gone` roads carry strings without attributes, so the count is 0 and behaviour is as today; A3 covers them;
  - an all-refused set with `round` and `fresh` both absent (no session, stage closed) leaves only `stop`. That is a dead end (FR-57) and must go to the conductor (`no_move`, P22), never to a person-only `stop`. State this in the spec.

A3. *A recorded pass is verified, never trusted* (the class guard, covering every road): at the end of `_exit_go_on`, re-run `self.exit_errors(role, digest, dispatch)` (`role` and the digest are in `rec`/`saved_result`). If any of `rec["lines"]` still blocks (`refusal_lines` over the result shares lines with `rec["lines"]`), do NOT print "recorded". Instead raise `held_question` with "your word was recorded but the check does not accept a word for: <lines>; only the role can repair them", and file the finding. This is the `waiver.recheck_stage_block` precedent (TP1-15045).
- Edges:
  - the gate raising (`gate_unreadable`) propagates as today;
  - with the S1 adapter rows (3819-3830) already written, the hold says what was written;
  - the rows stay for the sweep (`revoke_passes_of_dead`). They harm nothing, but see S1.

**Route B (only by the Lead's and possibly the owner's decision; a meaning change, PROJECT.md "package change" item 6: critic on plan before code):** make `row-fields-missing` word-passable so `go on` closes the step with the gap carried to gate B. It needs ALL of the following, or it still fails (probe above):
- (i) add the tag to `WORD_PASSABLE_TAGS`, which drops the `family` refusal line;
- (ii) the driver's block for a labelled S5P record must be its id (`manifest:-:row-fields-missing`), not the split line fragments. `tag_words` (3967-3971) shows a word to the source only if its `match` holds the tag, and the source text has no `s5_precheck.py: ` prefix;
- (iii) confirm that the window record / `acceptance.validate_window` does not then refuse the same missing field. The finding text says "the S5 window record or the test run will refuse" (inferred, not measured).

Route B contradicts the check's own docstring, and while R3's repair door exists it waives work the role can do. Not recommended as the minimal fix.

**Live run now (no code; operator/owner choice):** answer `round` with words telling the automator to send the `obligation_refs` fragment exactly as the TC-006/007 rows already carry it. The check accepts that (verified). Per the live-run-fvf finding, this counts as operator help in the comparison. `go on` will NOT work in the run copy as it stands, whatever is written (verified).

**Where it belongs:** main and the run copy.
- The relevant code is the same: `exit_gate.py`, `waiver.py`, `manifest_from_tests.py`, `window_record.py`, `driver_core.py` are byte-identical between R and main (`cmp`). The main `s5_precheck.py` differs, but it carries the same `PASSABLE` line (82) and the same `by_marker` split (3764). Main `driver_dispatch.py:3707` has the same single `go on` absent rule.
- The t-180 partition is on its branch only. A1-A3 do not depend on it.

## Duplication and consistency (rule 18)
- Found: the "which door fills `obligation_refs`" decision lives in two render sites keyed on `filled_by` (`s5_precheck._row_fields_text` 3763-3773 and `manifest_from_tests._row_form` 1721/1780). Both are wrong the same way for non-Python rows. Fix them together (axis 28).
- `exit_limit_facts` has a single ad-hoc `absent["go on"]` rule. A2 should be a second row of the same structure, not a parallel branch.
- grepped: `absent\["go on"\]` in R and main `driver_dispatch.py`, `filled_by != "automator"` in both `s5_precheck.py`.

## Code quality (rule 18)
- `_exit_go_on` writes and declares success with no read-back (R2). This is a quality defect of the "write then trust" kind that the package already names (`recheck_stage_block` docstring).
- The `check_row_fields` docstring cites FR-4 for a check no word can pass. FR-4 says a check stops a silent pass, never an informed one. That is coherent only while a repair always exists (FR-5/FR-57), and for TS rows the named one does not (R3).

## One action, one road (rule 19, P31)
- **Blocks:** filling `obligation_refs` has a marker road for Python and NO named road for TypeScript. The text even denies the hand road the check accepts. This exclusion has no data row (`references/detectors.json` `marker_read` is not read for obligations) and no owner's word.
- The census `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` has row 82 (Then bindings, same `language_rows`) but no row for `obligation_refs` (case-insensitive grep "obligation" on the census: only line 60 and other rows, none for this field).
- Proposed node, owner the Lead of `live-run-fvf` / `thinking-roles` TR2-16: add the census row and fix it by A1 (uniform fragment door or a TS marker reader).

## Class completeness (SIBLING_MAP)
- axis 23/28 (row fields carrier / render sites): A1 must touch both render sites, plus `window_record.py:787` refusal words if they name the marker. Not done, a proposal.
- axis 34 (one road): census row missing, proposed above.
- axis 17 (detector verdict shape): the `refused` class is honoured by the gate. The DRIVER is a consumer of that shape that ignores it (A2/A3). A2/A3 close it for the exit_limit seam. Other `go on` writers named in `pass_block`'s docstring (`take_seam_answer`, `_answer_code_close`, `_answer_repair_limit`) are the same class: they write a row with no read-back. They are outside this diff's scope; queue them with A3 as one mechanism (a shared "write pass, then verify" helper in `pass_block`) rather than three copies. Request to the coordinator: a scout to confirm whether those three can receive refused-at-source lines.

## Claims ledger
Verified (probe or direct read): R1 entirely; the 15/15 match; the control; R2 offer and "recorded" print (`factory-23.log:2-9`); the dedup (3839); R3 TS files, no marker for TS, hand refs accepted, TC-006 rows hand-written; t-180 not the obstacle; R/main identity per `cmp`; route B needing (i)+(ii) (probe).
Inferred: the endless re-ask loop (code path, two rounds observed); S1 cross-pass hazard (predicate behaviour, no live instance); route B (iii) window/acceptance refusal; the three other `pass_block` callers sharing the defect.

## Trail
Read: R\driver_dispatch.py 280-610, 3582-3858; R\driver_core.py 60-70, 610-633; R\waiver.py 195-232, 432-457; R\contract.py 120-171; R\exit_gate.py 424-447, 1685-1843; R\detector_verdict.py 55-121, 281-334; R\s5_precheck.py 82, 101, 3740-3825, 3881-4000, 4650-4685; R\manifest_from_tests.py 1-60, 1338-1397; R\window_record.py 160-240; R\manifest_put.py 588-622; A\pipeline.json (copy), A\state\driver-question.md, driver-question-details.md, standing-refusal.json (copy), A\work\automation-manifest.json; runs\factory-23.log; docs\SIBLING_MAP.md axes 28, 34 and the headings; t-2046 census (grep); plans\piles\live-run-fvf\findings\20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md.
Not read: factory-22.log beyond a grep (the attempt before t-180, superseded); the controller's own S5 close path.

```json
{
  "verdict": "blocker",
  "blockers": [
    "R1: s5_precheck row-fields-missing is family manifest, outside PASSABLE and WORD_PASSABLE_TAGS; report prints WORDS_REFUSED_AT_SOURCE family; exit_gate.word_class returns refused and judge_words blocks with no matcher call, so no stage_overrides row, star included, can pass it (probe: live rows blocking 1, with star blocking 1, same text as words=gate passed 1)",
    "R2: driver_dispatch.exit_limit_facts offers go on (the step closes as it is) for a refused-at-source record, and _exit_go_on writes rows and prints recorded with no read-back of the gate; the ladder then re-asks the same question and dedup makes a repeated go on inert (loop)",
    "R3: the finding's fix names a marker door that does not exist for TypeScript rows (manifest_from_tests.language_rows writes no obligation fields) and denies the hand fragment door the check itself accepts (_obligation_refs_problem returns empty for hand refs; TC-006 TS rows carry them) - P31 language exclusion with no data row"
  ],
  "class_completeness": "axis 28: both render sites of obligation_refs door (s5_precheck._row_fields_text, manifest_from_tests._row_form) must change together; axis 34: t-2046 census lacks an obligation_refs row - proposed node; axis 17: the driver ignores the refused class - A2/A3 close the exit_limit seam, the other pass_block callers (take_seam_answer, _answer_code_close, _answer_repair_limit) share write-without-read-back and are queued as one helper in pass_block, scout requested to confirm reachability",
  "trail": {
    "read": [
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/driver_dispatch.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/driver_core.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/waiver.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/contract.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/exit_gate.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/detector_verdict.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/s5_precheck.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/manifest_from_tests.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/window_record.py",
      "C:/QAFactory/exp-fvf/pkg-fix1/qa-factory/scripts/manifest_put.py",
      "LOCAL-1/pipeline.json (copy)",
      "LOCAL-1/state/driver-question.md",
      "LOCAL-1/state/driver-question-details.md",
      "LOCAL-1/state/standing-refusal.json (copy)",
      "LOCAL-1/work/automation-manifest.json",
      "experiments/mybooks/factory-vs-free-agent/runs/factory-23.log",
      "docs/SIBLING_MAP.md",
      "plans/piles/live-run-fvf/findings/20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md"
    ],
    "reruns": [
      {
        "command": "python -B heredoc: rebuild S5P output for the row-fields finding from standing lines, DV.parse, exit_gate.detector_records, word_class, judge_words over the copied live stage_overrides",
        "result": "passable False, cause family, words source, word_class refused; live overrides blocking 1 passed 0; plus star blocking 1 passed 0; 15/15 rows names_whole the record; same text as words=gate record passed 1"
      },
      {
        "command": "python -B heredoc: window_record._obligation_refs_problem with hand refs vs absent",
        "result": "hand refs without hash -> empty (accepted); absent -> missing"
      },
      {
        "command": "python -B heredoc: in-process WORD_PASSABLE_TAGS plus row-fields-missing, s5_precheck.passed_by_word over a scratch copy of the pipeline",
        "result": "live rows: finding kept 1 (first row has script prefix, others lack the tag); with an extra id-only row: kept 0"
      },
      {
        "command": "cmp main vs run copy for exit_gate, waiver, manifest_from_tests, window_record, driver_core, s5_precheck, contract",
        "result": "identical except s5_precheck and contract; PASSABLE and by_marker lines identical in main; main driver_dispatch has the same single go-on absent rule at 3707"
      }
    ]
  },
  "fixes": [
    "A1: s5_precheck._row_fields_text and manifest_from_tests._row_form name the manifest_put fragment door for obligation_refs (hash left out) where no marker reader exists, or uniformly - P31 fork to designer/Lead",
    "A2: exit_limit_facts withholds go on when any reaching record has exit_gate.word_class refused, counted in handoff_ladder before refusal_lines flattens; all-refused with no round/fresh goes to the conductor",
    "A3: _exit_go_on re-runs exit_errors after writing rows and holds the question truthfully when the lines still block, instead of printing recorded"
  ]
}
```
