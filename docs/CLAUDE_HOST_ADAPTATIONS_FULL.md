# CLAUDE.md — history of its clauses

`CLAUDE.md` is the project's own text since t-013 (the owner's word 11.11.2026): it began as the supervised-delegation
policy plus a list of twelve host adaptations; the list is gone, each adaptation was folded into the rule it changed.
This file keeps the history: where each adaptation stands now, the reasons of 5 and 6, and adaptation 7 in full.
Since F6-33 (21.10.2026; one owner per aspect, `docs/SIBLING_MAP.md` axis 31) the rule text of adaptation 5 is
`docs/tasks/critic-diff-brief.md` and of adaptation 6 is `CLAUDE.md` rule 12, Cost gates; this file keeps for them only
the reason. Adaptation 7 is kept verbatim as it stood at commit `16238d26`; its pointer in `CLAUDE.md` rule 4a and this text are a
pair: a change to one side is checked against the other (skill `boot-diet`, step 4).

## Host adaptation N -> where it stands now

| host adaptation | where it stands now |
|---|---|
| 1 | Tiers (the scout line; no tier runs on Haiku) |
| 2 | rule 2 (DRAFTING), pointing to `.claude/agents/designer.md` rule 1 |
| 3 | rule 11, table row R11-f |
| 4 | Routing log: typed fields and the `feature` line |
| 5 | rule 3 (the critic gate on a diff: DUPLICATION and CODE QUALITY) |
| 6 | rule 12, Cost gates (plus the critic-on-plan clause in rule 3 and row R13-g) |
| 7 | rule 4a (a pointer to PROJECT.md «Командная работа»); full text below |
| 8 | rule 11, table row R11-h |
| 9 | rule 10 (the package paragraph: AR-n) |
| 10 | rule 10 (where judgment lives: P27 and AR-29) |
| 11 | rule 4 (the witness scope, solo or parallel) |
| 12 | rules 4 and 11 (which tests a DoD asks for; the quarantine) |

What was dropped and why: rule 13 judge text, R1-a, hygiene 2, the journal-segments clause — t-013 §2
(`docs/tasks/specs/t-013-claude-policy-rewrite.md`).

## Adaptations 5-7 (5 and 6: the reason; 7: moved verbatim)

5. Rule 3, the critic gate on a diff — the rule text is `docs/tasks/critic-diff-brief.md` items 6-7 (the critic role file's
   rule 18 points there). Why: the owner's word 06.10.2026 «поддерживать порядок» after the 0.8.1 clean-up; the role file
   gained rule 18 on 09.10.2026 (B-419) without the exam its rule 10 demands — deferred by D-0037 (forge batch 3).
6. Cost gates — the rule text is `CLAUDE.md` rule 12, Cost gates; here only why. D-0035 (the owner's word 07.10.2026): release
   0.9 cost 56% of the weekly limit, workers 86% of that — hence the context cap, the fresh fix-round worker, one critic pass
   per topic and the Lead's cadence. D-0038 (the owner's question 08.10.2026, B-468): a budget-stopped worker's remainder was
   being finished by the Lead by hand — hence the remainder goes to a fresh worker. D-0040 (10.10.2026): the cap's motive is
   token spend, not merge ease — hence reading dispatches are not counted. D-0054 (20.10.2026): many independent streams — the
   cap went from 4 to 6. The owner's word 21.10.2026 11:5x and 12:4x: the night sessions often ran 2–3 subagents in all — the
   reason for the slot exemption of designers, critics and scouts and for the full-queue clause.
7. Team work in piles and batches (DECISIONS.md D-0036, the owner's word 08.10.2026; PROJECT.md «Командная
   работа»): the work plan lives in `plans/piles/<slug>/` (a card for people, batch files for agents, findings
   one per file) with `plans/PILES.md` as the one generated table of contents; a batch has ONE taker and its file
   is frozen once taken (`tools/piles.py check` (в)); batches in work do not share written paths without a queue
   line ((б)); `plans/BACKLOG.md` is frozen — only `piles.py close` moves rows to «Закрыто» ((г); `release` is a refused alias); the journal
   is one file per developer `logs/journal/<dev>.jsonl` (the slug from `tools/dev.config.yaml`; `journal_keys`
   is the one loader, identity `<id>@<dev>`); `CURRENT_CONTEXT.md` holds the state of `main` only, a batch's
   progress lives in its «Ход». Gates on the path: `piles.py check --msg-file` in commit-msg (door
   `piles-skip: <item> -- <reason>`), `board --check` in pre-commit, pre-merge-commit and CI. Detector:
   calibration check 33.
