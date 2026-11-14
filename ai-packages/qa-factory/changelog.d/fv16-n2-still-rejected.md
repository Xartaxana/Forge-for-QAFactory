- the rows the S4 case critic still rejects now travel to the S5 automator (`scripts/critic_rollcall.py`, `scripts/s5_plan.py`,
  `scripts/brief_pack.py`, FV1-6 N2): a reviewed roll-call row whose word is not an approving one (`reject`, `partial`, an unknown word,
  an empty cell) becomes a remark `CR-<case>` (`CR-global` for a row that names no case) with `still_rejected: true`, the critic's note
  whole, and the case it would be answered against in `plan_remarks`; the latest accepted round that lists a case decides, a case
  no longer in the story is named as removed, `CC-n` ids of the concerns do not move, and the brief head counts the still-rejected
  remarks apart; `critic_rollcall.rejected_rows` is the one predicate and `critic_rollcall.current_rejected` reads the newest round of a
  findings file
