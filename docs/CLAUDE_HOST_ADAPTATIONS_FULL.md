# CLAUDE.md host adaptations — the full text

The host section of `CLAUDE.md` lists the project's adaptations of the supervised-delegation policy. On
2026-10-19 (the boot diet, the owner's word) adaptations 5, 6 and 7 were trimmed there to pointers and their full
text moved here. Since F6-33 (21.10.2026; one owner per aspect, `docs/SIBLING_MAP.md` axis 31) the rule text of adaptation 5 is
`docs/tasks/critic-diff-brief.md` and of adaptation 6 is `CLAUDE.md` host adaptation 6 itself; this file keeps for them only
the reason. Adaptation 7 is kept verbatim as it stood at commit `16238d26`; it and its trimmed line in `CLAUDE.md` are a
trimmed ↔ full pair: a change to one side is checked against the other (skill `boot-diet`, step 4).

## Adaptations 5-7 (5 and 6: the reason; 7: moved verbatim)

5. Rule 3, the critic gate on a diff — the rule text is `docs/tasks/critic-diff-brief.md` items 6-7 (the critic role file's
   rule 18 points there). Why: the owner's word 06.10.2026 «поддерживать порядок» after the 0.8.1 clean-up; the role file
   gained rule 18 on 09.10.2026 (B-419) without the exam its rule 10 demands — deferred by D-0037 (forge batch 3).
6. Cost gates — the rule text is `CLAUDE.md` host adaptation 6; here only why. D-0035 (the owner's word 07.10.2026): release
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
