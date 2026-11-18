# Decisions Log

One line per decision — the operative statement, not the discussion. This log is read by EVERY session, so it keeps only
what every session needs (the owner, 06.10 and 11.11.2026): a lasting rule, a binding, a boundary. A temporary decision
(a one-time plan, a schedule, a "confirm next session" note, a branch's state) goes to CURRENT_CONTEXT.md or the
backlog; a decision that belongs to one node, spec, batch or day, or whose rule text lives in CLAUDE.md, COORDINATOR.md,
PROJECT.md or a role file, is written into that carrier and, if it needs a number, into docs/DECISIONS_ARCHIVE.md. A new
decision is appended at the end, in the order it was made; a line is never edited or renumbered, with one move allowed:
a line that has stopped being operative is MOVED whole to docs/DECISIONS_ARCHIVE.md with the date and the reason, and an
over-long line is trimmed here to its operative statement with its full text kept there; a number is never reused. A
D-number cited anywhere and absent below resolves in the archive.

Format: `- D-NNNN — <operative statement, one line>.`

- D-0033 — The clone ratchet is a merge gate: `tools/dup_ratchet.py --check` against `tools/dup-baseline.json` (only shrinks) runs in `forge-check` on every push and MR; a new clone group or a new copy in one is red with a door (remove the copy, or `--update` on the Lead's word). Detector: the `forge-check` job, `tools/test_dup_ratchet.py`. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0037 — Exams are deferred (the owner's word 09.10.2026, verbatim in `docs/DECISIONS_ARCHIVE.md`): `.claude/agents/critic.md` gains rule 18 (B-419) WITHOUT the exam its rule 10 demands — this line is the recorded pass of that gate (P13); every exam and calibration debt is forge batch 3 `plans/piles/forge/batch-3-exam-debts.md`. Until a scout pass exists, scout digests stay under the strict form R1 b. Detector: calibration check 14(a) reads this decision as the pass; check 5/13 for the overdue line.
- D-0046 — A critic verdict with fixes is a rejected attempt, and the fix round is attempt n+1 of the SAME task (the owner, 16.10.2026): `rejected` with `basis: critic` the turn the verdict is accepted; the fix round is a fresh worker carrying only the diff and the verdict, `delegated` under the same `task_id` with `attempt: n+1`; the merge's `accepted` closes the id, no re-review of a fix round (D-0035 b). D-0045 stays reserved for R11-h. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0063 — One action, one road (the owner's words 06.11.2026, PROJECT.md P31): designer rule 6, critic rule 19 + brief question 12, the ratchet `tools/language_sites.py`, axis 34, calibration check 42. `.claude/agents/critic.md` gains a duty WITHOUT the exam its rule 10 demands; this line is the recorded pass. Detector: calibration checks 14(a) and 42. Tier: fable.
- D-0067 — The ladder (the owner, 16–17.11.2026; spec docs/tasks/specs/20261116-architect-tier-spec.md): Lead is bound to claude-opus-5-5, a new function `architect` above Lead to claude-fable-5-1 (`delegation.config.yaml`; ranks and the one reader: `tools/tier_ladder.py`); the rules are COORDINATOR.md § Tiers, rule 6 and § Role ≠ tier. The Lead exam for the Opus candidate is deferred to FG7-54 by the owner's word: the informed pass of `exam.on_failure`. Full text: `docs/DECISIONS_ARCHIVE.md`.
