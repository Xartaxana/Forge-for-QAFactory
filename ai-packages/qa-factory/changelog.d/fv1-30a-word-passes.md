- A person's recorded word now passes any passable S5 exit finding by ONE road, and every pass is recorded
  (`s5_precheck.py`, `branch_accounting.py`, `controller.py`; FV1-30a): every finding but `open-oracle-asserted-*` and
  `then-remainder-unrecorded-*` is passable, for every family alike; a word passes a finding only when it is `*`, the
  finding's tag, its whole id, or the stage-wide `changed-after-red` / `sides-undeclared` / `provisional-open-on-real`
  tag family (`obligation-id` too) - never a case id, never a part of a tag, never a phrase of the message or fix. A word
  recorded as a phrase of the line no longer passes; re-record it by the finding's tag. The result of `s5_precheck.run` carries a new
  `word_passes` field (`[]` with no word) and `word_passes(task_root, scope)` returns it without writing; an accepted S5
  completion records each pass in `state/passed-by-person.jsonl` with `word_at` (and `finding_id` when the block was cut);
  `branch_accounting` and the window gap check read the same passes, so a fact the person passed is not asked twice.
