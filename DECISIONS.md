# Decisions Log

One line per decision — the operative statement, not the discussion
that led to it. Only what the project's FUTURE work needs to know goes
here: a lasting rule, a binding, a boundary. A temporary decision — a
one-time plan, a schedule, a "confirm next session" note, the state of
a branch — goes to CURRENT_CONTEXT.md or the backlog, not here (the
owner, 06.10.2026). A new decision is appended at the end, in the order
it was made; a line is never edited or renumbered — with one move
allowed: a line that has stopped being operative is MOVED whole to
docs/DECISIONS_ARCHIVE.md with the date and the reason, and an
over-long line is trimmed here to its operative statement with its full
text kept there; a number is never reused. Archived so far: D-0004,
D-0005, D-0006, D-0011, D-0015, D-0024 (06.10.2026); trimmed: D-0019,
D-0021, D-0022, D-0023 (06.10.2026); D-0039, D-0040, D-0043, D-0044,
D-0046, D-0033, D-0035, D-0036, D-0037, D-0041, D-0042 (19.10.2026, boot diet);
D-0022, D-0023, D-0035, D-0036, D-0038, D-0040, D-0041, D-0042, D-0044, D-0057,
D-0059, D-0061, D-0062 (11.11.2026, boot diet).

This log is read by EVERY session, so it keeps only what every session needs (the owner,
11.11.2026). A decision that belongs to one node, spec, batch or day, or whose rule text lives in
CLAUDE.md, PROJECT.md or a role file, is written into that carrier and, if it needs a number, into
docs/DECISIONS_ARCHIVE.md — not here. Moved out whole on this ground (11.11.2026): D-0001, D-0008,
D-0009, D-0016, D-0021, D-0022, D-0025, D-0027, D-0035, D-0036, D-0038, D-0040, D-0041, D-0042,
D-0044, D-0048, D-0051…D-0062; part 2, decisions about the factory's own behaviour: D-0010, D-0012, D-0013, D-0014, D-0017, D-0018, D-0019, D-0020, D-0023, D-0026, D-0028, D-0029, D-0030, D-0031, D-0032, D-0034. A D-number cited anywhere and absent below resolves in the archive.

Format: `- D-NNNN — <operative statement, one line>.`

- D-0002 — Scout is bound to claude-sonnet-5-5, not the kit's Haiku default: the owner uses no Haiku anywhere; the Tiers line of the policy block is adapted accordingly (host adaptation 1 in CLAUDE.md).
- D-0003 — Bindings: lead claude-fable-5-1, critic and designer claude-opus-5-5, builder and scout claude-sonnet-5-5; judge stays as shipped (deferred, subscription contour).
- D-0007 — The installed qa-factory plugin is disabled in this repository (enabledPlugins in .claude/settings.json): its pre-tool guard is written for qa-* roles and blocked the operator's own work on 29.09.2026 (a repository configuration change, then a decision text that merely named one); it stays enabled in the target projects where stories run.
- D-0033 — The clone ratchet is a merge gate: `tools/dup_ratchet.py --check` against `tools/dup-baseline.json` (only shrinks) runs in `forge-check` on every push and MR; a new clone group or a new copy in one is red with a door (remove the copy, or `--update` on the Lead's word); every builder's witness carries `--check` and the critic reads it as the mechanical layer of the diff gate (`docs/tasks/critic-diff-brief.md`; the owner, 06.10.2026: «поддерживать порядок» after the 0.8.1 clean-up; B-417, B-309). Detector: the `forge-check` job, `tools/test_dup_ratchet.py`. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0037 — Exams are deferred (the owner's word 09.10.2026, verbatim in `docs/DECISIONS_ARCHIVE.md`): `.claude/agents/critic.md` gains rule 18 (B-419) WITHOUT the exam its rule 10 demands — this line is the recorded pass of that gate (P13); every exam and calibration debt is forge batch 3 `plans/piles/forge/batch-3-exam-debts.md` (inventory `docs/tasks/specs/reports/t-600-exam-debts.md`), priority П3; the weekly calibration runs after forge batch 4 closes. Until a scout pass exists, scout digests stay under the strict form R1 b. Detector: calibration check 14(a) reads this decision as the pass; check 5/13 for the overdue line.
- D-0039 — An unforeseen state calls the conductor; the run never stalls and never promises what it will not do (the owner, 09.10.2026). The conductor offers the person every way to continue with its price and consequences, executes the choice through the existing commands (dispatch only through the controller, never editing artifacts) and writes a finding; free-form answers are read by the conductor, code reads only closed options. Carrier: PROJECT.md P22. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0043 — The factory never asks a person about what it has itself established as unreachable, and never re-asks per instance after a recorded class decision (the owner, 13.10.2026). Unreachable by the factory's own probe is a recorded gap named in the report; a question remains only where the person can give a road; one class decision covers every instance until the end of the run. Carrier: PROJECT.md P5; refined by D-0047. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0046 — A critic verdict with fixes is a rejected attempt, and the fix round is attempt n+1 of the SAME task (the owner, 16.10.2026): `rejected` with `basis: critic` the turn the verdict is accepted; the fix round is a fresh worker carrying only the diff and the verdict, `delegated` under the same `task_id` with `attempt: n+1`; the merge's `accepted` closes the id, no re-review of a fix round (D-0035 b). D-0045 stays reserved for R11-h. Full text: `docs/DECISIONS_ARCHIVE.md`.

## D-0047 — D-0043 refined: a standing decision is applied WITHOUT a new question but SAID OUT LOUD; the report names an unreachable source only where it changes what is left to the person, with the provenance of the decision (16.10.2026)

The decision is the heading above; carrier: PROJECT.md P5. The owner's words and the mechanism: `docs/DECISIONS_ARCHIVE.md` (D-0047).
- D-0049 — The GROUNDING step returns to the factory (the owner, 19.10.2026): the implementation is checked against the REQUIREMENTS before any test is written, by the role that writes the test plan, together with the blast radius, which is a required output; refactoring thresholds are data (over 30 % of the change: told to the person and added to the plan and regression; over 50 %: a stop and a question). Carriers: PROJECT.md P23, pile `grounding`. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0050 — A ticket without acceptance criteria does not stop S0 (the owner, 19.10.2026): AC are one source of requirements among others, read from every ticket of the task where they exist; no AC is a report line, never a question; the stop stays only for a READ FAILURE, named as the factory's own defect (FR-46). Carrier: PROJECT.md P23. Full text: `docs/DECISIONS_ARCHIVE.md`.
- D-0063 — One action, one road (the owner's words 06.11.2026, PROJECT.md P31; spec t-2065): designer rule 6, critic rule 19 + brief question 12, the ratchet `tools/language_sites.py`, axis 34, calibration check 42. `.claude/agents/critic.md` gains a duty WITHOUT the exam its rule 10 demands, because `PROCESS/CRITIC_EXAM.md` does not exist and exams stand deferred by D-0037; this line is the recorded pass; the debt joins `plans/piles/forge/batch-3-exam-debts.md`. Detector: calibration checks 14(a) and 42. Tier: fable.
- D-0064 — This repository, `Xartaxana/Forge-for-QAFactory`, is the only place the QA Factory is developed; releases go to `Xartaxana/QAFactory` (marketplace `qafactory`) as a copy of ai-packages/qa-factory/ (the move to GitHub, 05.11.2026; replaces D-0001, whose names were of the old host).
