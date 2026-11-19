- an S5 window whose last round is an accepted critic with `unresolved: tests_in_repair` is open, and `stage_S5` records its owed author
  round as `route` from that critic's own route, once per window and in window order; a driver that died between the send-back and the
  author's rework no longer loses the round or meets the "every window is accepted" refusal (FV3-35b2, E12)
