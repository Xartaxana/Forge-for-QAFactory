# FV1-3 code critic (diff gate, one pass for the topic)

Diff: `wip/fv1-3` `819a31f...a540636` (+ fix round `c69ce79`: the line-98 needle of `test_story_run_loop_b_answers.py`, Lead's decision,
not a finding). Spec: `docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md` rev. 2. Builder report:
`.claude/worktrees/fv1-3/docs/tasks/specs/reports/20261113-fv1-3-report.md`. Lines below are on the worktree at `c69ce79`.

**VERDICT: fit_with_fixes. 0 blockers, 3 fixes for this node's fix round, 1 report correction, 6 queue lines.**
This verdict is input to acceptance. The acceptance decision belongs to the Lead.

## Findings

### Fixes for this node's fix round (none blocks the merge on its own)

**F1. A seam that stops, or a crash after the save, re-asks the threshold question with no FR-7 "answered before" block. The spec's E13(c) claim does not hold.**
`driver_dispatch.py:1792-1798` (`take_question_answer`) saves state and calls the seam. The answer's audit row in
`state/driver-answers.jsonl` is written only at the end of `take_answer` (`driver_machine.py:3592` `record_answer_row`) or by the
Refusal funnel (`:2018` `settle_unread_answer`, which runs only for a Refusal). `ask()` finds an earlier answer only through
`already_answered`, `driver_dialog.py:381-392`, which reads only `driver-answers.jsonl` by `question_sha`.
Concrete state: a free answer at an S2 stop, then the conductor answers `stop` (`Stop(EXIT_GAVE_UP)`) or the process dies after
`save_state()`. On disk: `asked` = the threshold question, `pending_words` filed, no row. A rerun with no `--answer` reaches the new
guard (`driver_machine.py:1442-1452`), which re-raises the same body. `ask()` finds no row, so the person gets the identical
question with no "You have answered this exact question before" block. That breaks FR-7, and it contradicts spec E13(c), which says the block quotes their words.
Fix direction (code, not spec; in owns): in `take_question_answer`, right before `self.save_state()` at :1794, add `self.answer_file();
self.record_answer_row("", dispatch)`. The row is written once per answer (`held["row"]`, `driver_conductor.py:240-242`), so the
end-of-`take_answer` call becomes a no-op. Add one assertion to the `seam-raises` row: one `driver-answers.jsonl` row for this answer.
Sibling outside owns: queue line Q3.

**F2. The print-back calls a question that is new to the register "open again".**
`driver_dispatch.py:1856-1859` compares `after` with `before.get(qid)`. Concrete input: `before` = {Q1..Q7}, and during the seam the
register gains Q8 (status `open`; any writer, e.g. a rewrite of `requirements-readiness.json` by a command the conductor may run).
The output is "S2: recorded by the assistant from your own words — Q8: open again". The person is told something that never
happened (P9/FR-10). The spec (§3.1 step 5) does not cover a new id, and the builder's choice errs toward a false statement.
Fix: `if qid not in before: continue` (or a separate "new question" word). A test row is optional: the spec names no such edge.

**F3. K9 not met as written. The commit's `architecture:` line leaves out AR-14, AR-19, AR-22 and AR-29.**
Commit `a540636`'s line reads `AR-13, AR-15, AR-17, AR-20, AR-24, AR-25, AR-28`. Spec K9 lists AR-14, AR-19, AR-22 and AR-29 as well.
AR-22 is really touched: `question_pass_lines` gets a second producer after the seam (`:1797-1798`). The report's prose names all of
them, so nothing is starved; the gap is only the gate line the commit carries (brief Q10). Fix: the fix-round commit carries the full
K9 line.

### Report correction (not a code defect)

**R1.** The report's FR-G line says "the em dash in the print-back is written `\u2014`". It is not: `driver_dispatch.py:1860` holds a
literal U+2014. A byte grep counts 17 occurrences in the file now and 16 at `819a31f`. This is harmless: the file already used literal
em dashes, and `--lang` checks for Cyrillic. But the claim is false and should be corrected (rule 12: a load-bearing-looking claim I
could not reproduce).

### Optional (builder's choice, no finding)
After the seam returns, the conductor's plan lines (`:1797-1798`) are only in memory until `take_answer` saves at `:3626`. A crash in
that short window loses them for good, because `apply_recorded_answers` writes once per record. One `self.save_state()` after the
extend closes it.

## Answers to the dispatch

**1. K1-K8 and edges.**
- K1: met. Rows `all-tokens` (0 calls), `token-word-inside-free-text` and `mixed` (1). The words file is whole in `another-language`, `words-at-6000` and `words-beyond-6001`.
- K2: met. `fv1_3_the_real_s4_answer` holds the 18 lines verbatim (LF; the CRLF on disk is noted in the report). It checks the register record, the shown hash, the order `apply, conductor, apply`, the print-back, `question_stop.shown`, `--show` and the absence of the judge. Before the change this scenario fails at "called once".
- K3: met. One function covers all 16 ids. `no-judge-on-register`, `halt-road-shares-member` and `rerun-other-dispatch` are loops inside the same function, not table rows. That is acceptable: each label names the row.
- K4: met (`fv1_3_rerun_with_no_answer`).
- K5: met, at diff lines `:92`, `:108`, `:139` and `:326`. The report notes that the `:326` check covers 2 of the 3 labels.
- K6: met by reading (answer 5).
- K7: met after `c69ce79`. The 106/106 is the builder's; I did not re-run it.
- K8: met per the witness (`test_audit_rules` 375/375, `test_driver_layers` 283/283). The A27 swap is named; no census row moved.
- E1, E1b, E2, E3, E4, E5, E7, E9, E10, E11, E16 and E18: met, each by the row of the same name.
- E6: n/a, pinned elsewhere.
- E8: met by the limit rows and `fv1_3_the_real_pack_size`.
- E12: met (report line).
- E13(a), E13(b), E13(d), E14, E15 and E17: met by reading.
- E13(c): **not met** (F1).

**2. The order and the rerun path.** I walked each case:
- (a) The seam returns. `take_answer` clears `asked` and saves.
- (b) The seam raises a Person. `_run_guarded` calls `ask()`, which overwrites `asked` with the seam question (kind `questions`, `offered`). `pending_words`, `stop.answered` and `stop.resume` are already on disk from :1794. The rerun guard fires (`asked.dispatch == dispatch`, file present, words filed). `held_question("")` rebuilds `offered`/`options` (`driver_dialog.py:620-622`), and the role is not resumed. K4 proves this.
- (c) The seam raises Stop, or the process crashes after the save. `asked` = the threshold question, and the guard arm `kind == "questions"` re-asks it. The FR-7 block is missing: F1.
- (d) A crash before the save. The register and journal hold the code records, and the state does not. The rerun re-asks. On the re-answer, `record_answers` skips the same answer (H6b, `question_register.py:1004-1006`) and `apply` writes once per record, so nothing is applied twice. This window existed before the change, and wider.

`pending_words` and `stop["answered"]` are set in the same block and saved together (:1789-1794), so they cannot disagree on disk.
Side effect of (d): ids skipped as "same answer" are left out of `recorded`, so the conductor is told "recorded by code: nothing" for
them. It is safe but imprecise: queue line Q5.

**3. Code reading free words.** None. The member reads only `record_answers`' dict (shape: tokens, unread, unknown ids) and the
register's `(status, reading, at)` (data). `judged_reply` is called only when `recorded is None` (:1821), which keeps today's
behaviour on S1 review and on a halt with no register. The guard reads only state fields. There is no phrase list and no regex on meaning, so P22, FR-12,
AR-17 and AR-24 are kept.

How the 6000 limit works:
- The words go whole through `answer_file()` (`driver_conductor.py:864`).
- The prompt copy is cut at `NO_MOVE_WORDS_IN_PROMPT`, and the cut says so out loud: "(cut; the whole answer is in <file>)" (`:322-323`, untouched).
- The rows at 6000 and 6001 prove the file is byte-whole.
- `qtext[:6000]` cuts only question text after every instruction, and the conductor is told "the question text below may be cut" with the `--show` command (:1839-1840). `fv1_3_the_real_pack_size` proves both instructions stand before character 6000 of the refusal text.

**4. One survivor (AR-15).** Yes. The halt road's inline text (`-198..-219` of the diff) is moved, not copied. `_unread_halt_or_review` now calls
the member (:3822). A case-insensitive grep over `scripts/*.py` for `recorded by code -`, `Not read, still open` and `that --show prints`
finds them only in the member and in the new test (positive control: the grep finds `driver_dispatch.py:1828`). The print-back exists
once (:1860). DUPLICATION AND CONSISTENCY: no new duplicate. The pattern "instructions + MOVES_RULE + OWN_TOKEN_RULE + `## The question`
+ qtext[:6000]" is older than this diff and sits at `driver_machine.py:3963`, `:3991`, `driver_stage_build.py:522` and `driver_conductor.py:879/892`
(queue line Q4, not this node). The two `question_pass_lines` extends (:1788, :1798) are trivial twins.
CODE QUALITY: the member runs `:1800-1862` (63 lines including a 9-line docstring and a local `snapshot()`), at most 3 nesting levels, no dead
branch. `nouns.get(kind, 'a halt')` puts a default on a closed three-key vocabulary with exactly three callers, which is acceptable. The issues found are F2 (a label that lies) and the optional save.

**5. The two slow files.** `test_story_run_s0.py:1135` and `test_story_run_s6.py:921` set `driver.unread = lambda *a, **k: "continue"`.
The stub is correct by reading, for these reasons:
- Both direct calls hand over non-all-token words: a fenced `Q1: a`, a case line, and the unknown `Q77`. The member now reaches `unread`, which would otherwise call the real conductor.
- The member ignores the return value of `unread`.
- The assertions judge only what `record_question_words` prints. That output is unchanged, and the print-back adds only "the assistant recorded nothing..." / "could not be read back", which none of the `check_not_in` needles match.
- The new `save_state()` is safe: `_write_json` creates parent directories (`driver_core.py:319`).

The stub hides no behaviour the tests pinned before: those tests never looked at the conductor. These two files were not run, by
design; CI on the batch branch judges them.

**6. Class-wide (map, not scan).** All free-word roads in `take_answer` reach the ONE seam `unread`. A grep of `self.unread(` over
`driver_*.py` finds 30 sites, each through `no_move`. The question stop and the halt road now share the member (axis 34 covered). The
differences are queue lines, not findings:
- Gate A/B: register card lines take `_unread_kept_gate` (`driver_machine.py:4032`). That road has no "recorded by code / --by conductor" instruction and no print-back of the conductor's records, which may be a second road for the same action (P31). A scout should confirm it (Q2).
- S0 closed stops: `_keep_s0_words`, then `s0_read_word`, then the seam with `doors` (`driver_s0.py:852`). They are closed-token questions, not register words, so n/a.
- The seam's second answer (F-12) and `after_close`: already queued by the spec.
- The halt road's resumed role is never told plan lines: Q1.

**7. Standing questions.** Q10 ARCHITECTURE: AR-13, AR-14, AR-15, AR-17, AR-19, AR-20, AR-22, AR-24, AR-25, AR-28 and AR-29 are kept by
reading. The A27 row is swapped by name with the sum unchanged (`audit_factory.py:1687`). There is no new conductor call site, and the
only added `self.unread(` is at :1845. The only gap is the gate line (F3). Q11 JUDGMENT: there is no new check that judges meaning. The
hand-over predicate is token shape, the guard is the presence of two state halves, and the print-back is a data diff. No census row,
scan constant, `blocks_override` or craft marker is touched, so `judgment: none` holds. Q12 ONE ROAD (P31): none found. The diff has
no branch on a language, project or runner name (grep of the diff for language names: only the test's `chr()` Cyrillic). `s1_review`
without MOVES_RULE is older than this diff and named in the code.

## Queue lines (for «Остатки» of the pile; the Lead places them, D-0044)
- Q1: halt road (`record_halt_words` `driver_dispatch.py:1920` and the member's after-seam apply via `_unread_halt_or_review`) discards `plan_lines`, so the resumed halt role is not told what code/the conductor changed in the plan (H36 sibling) | перенос: findings/<new> live-run-fvf | обоснование: older than FV1-3 for code tokens, spec-decided for the conductor's | подтвердил: —
- Q2: gate A/B register card lines go to the conductor through `_unread_kept_gate` without the register instruction and print-back the question stop now has: one road? (P31, axis 34) | перенос: findings/<new> live-run-fvf (scout first) | обоснование: outside FV1-3 owns | подтвердил: —
- Q3: any answer branch whose seam raises Stop (halt road `_unread_halt_or_review` and others) writes no `driver-answers.jsonl` row, so the rerun re-ask lacks the FR-7 block | перенос: findings/<new> live-run-fvf | обоснование: class wider than the node; FV1-3's own instance is F1 | подтвердил: —
- Q4: one builder for the conductor prompt tail (instructions, MOVES_RULE, OWN_TOKEN_RULE, `## The question`, qtext cut), sites listed in answer 4 | перенос: findings/<new> | обоснование: older than this diff, dup class | подтвердил: —
- Q5: `record_answers` leaves ids skipped as the same answer (H6b) out of `recorded`, so a re-answer tells the conductor "recorded by code: nothing" for ids already recorded (`question_register.py:1004-1006`) | перенос: findings/<new> (FV1-13 owns token reading) | обоснование: non-goal of FV1-3 | подтвердил: —
- Q6: F-12 (seam second answer) and `after_close` free words: already queued by the spec §4 siblings; named here for completeness.

## Trail
- Read: spec rev. 2 §1-§4 (lines 1-457); the critic-diff brief (whole); the builder report (whole); the diff `819a31f...a540636` (all 661 lines);
  `git show --stat c69ce79`; commit message `a540636`; `driver_dispatch.py:1590-1800`, `:1800-1862`, `:1866-1954`; `driver_machine.py:1439-1452`,
  `:1844-1883`, `:3353-3392`, `:3520-3629`, `:3646-3663`, `:2443-2455`, `:4058-4083`; `driver_dialog.py:249-392`, `:600-648`;
  `driver_conductor.py:235-260`, `:305-326`, `:852-870`; `driver_core.py:313-325`, `:611-616`; `question_register.py:976-1023`;
  `test_story_run_s0.py:1120-1149`; `test_story_run_s6.py:904-937`; `SIBLING_MAP.md` axis 34 and rows 137/155; `tools/critic_verdict.schema.json`.
- Greps: `self.unread(` over `driver_*.py` (30 hits); `record_answer_row(` / `already_answered` (writers and reader of driver-answers.jsonl);
  `settle_unread_answer()` (one caller, the Refusal funnel); case-insensitive `MOVES_RULE|OWN_TOKEN_RULE|PRE_FILLED|recorded by code -|qtext\[:6000\]|Not read, still open|that --show prints`
  over `scripts/*.py` (positive control: hits `driver_dispatch.py:1828`); byte grep for U+2014 in `driver_dispatch.py` (17 now, 16 at 819a31f).
- Control re-run (cheap, non-slow): `( cd .../fv1-3/ai-packages/qa-factory/scripts/tests && python -B test_story_run_loop_b_threshold.py )`, last
  line `=== test_story_run_loop_b_threshold: 198/198 ok ===`, matching the witness. No slow file was run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 driver_dispatch.py:1792-1794 take_question_answer: write the answer's driver-answers.jsonl row (answer_file + record_answer_row('', dispatch)) before save_state, so a seam Stop or a crash re-ask carries the FR-7 answered-before block (spec E13(c)); one assertion in the seam-raises row",
    "F2 driver_dispatch.py:1856-1859: the print-back labels an id absent from before as 'open again'; skip new ids or word them as new",
    "F3 commit architecture line omits AR-14, AR-19, AR-22, AR-29 that K9 lists (AR-22 touched by the second question_pass_lines producer); the fix-round commit carries the full K9 line",
    "R1 report: the em dash at driver_dispatch.py:1860 is a literal U+2014, not an escape; correct the FR-G line"
  ],
  "class_completeness": "Axis 34: question stop and halt road share register_words_to_conductor (covered); every free-word road reaches the one seam unread. Queued: Q1 halt-road plan lines not told (H36 sibling), Q2 gate A/B register card lines via _unread_kept_gate (P31 check, scout), Q3 seam-Stop branches write no driver-answers row (FR-7), Q4 prompt-tail builder dup, Q5 record_answers omits H6b-skipped ids, Q6 F-12 and after_close already queued by the spec.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md (1-457)",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/fv1-3/docs/tasks/specs/reports/20261113-fv1-3-report.md",
      "git diff 819a31f...a540636 (661 lines); git show --stat c69ce79; commit message a540636",
      "scripts/driver_dispatch.py 1590-1954",
      "scripts/driver_machine.py 1439-1452, 1844-1883, 2443-2455, 3353-3392, 3520-3663, 4058-4083",
      "scripts/driver_dialog.py 249-392, 600-648",
      "scripts/driver_conductor.py 235-260, 305-326, 852-870",
      "scripts/driver_core.py 313-325, 611-616",
      "scripts/question_register.py 976-1023",
      "scripts/tests/test_story_run_s0.py 1120-1149; scripts/tests/test_story_run_s6.py 904-937",
      "docs/SIBLING_MAP.md axis 34, rows 137 and 155",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "( cd C:/QAFactory/forge-repo/.claude/worktrees/fv1-3/ai-packages/qa-factory/scripts/tests && python -B test_story_run_loop_b_threshold.py )",
        "result": "=== test_story_run_loop_b_threshold: 198/198 ok === (matches the builder witness)"
      }
    ]
  }
}
```
