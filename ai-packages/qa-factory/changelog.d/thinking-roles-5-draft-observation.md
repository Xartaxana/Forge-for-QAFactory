- bug draft contract (`references/artifact-contract-run.md`): one optional field `observation`, the id of the observation the draft belongs to,
  written when that observation has no pinned case; `place_answers.place_of_draft` joins such a draft to that place (after the `case`
  rule, before the `violates` rule); an empty, non-string or unmatched value reads as absent and `case` is never read as a target id (TR4-15)
