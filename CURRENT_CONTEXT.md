# Current Context

## Maintenance Rule

This file holds LIVE state only: the state of `main`. A batch's progress lives in the «Ход» section of its file.
This file is read on every boot — keep it short.

## Current Milestone

The forge has moved to GitHub: this repository is `Xartaxana/Forge-for-QAFactory` (private); released versions of the
package go to `Xartaxana/QAFactory` (public, marketplace `qafactory`). History before the move is not carried: the old
repository's history and run data are kept in a bundle outside GitHub (decisions O2, O3).

## Current Task

Release 0.11.0 is out in `QAFactory` (tag `v0.11.0`, 12.11.2026). The comparison run LR2-1 (factory vs free agent) is
being run by a separate Opus operator session since 12.11 17:38 (its `lead_degraded` window in the journal and the
uncommitted `experiments/mybooks/factory-vs-free-agent/` paths are that session's). Unfinished plan phases stand as
nodes: `onboarding-forge/3` (knowledge plan, phases 1-6), `package-ci/4` (TD-11, TD-15), `roles-context/2`,
`thinking-roles/5`. Open dispatch t-073 = node PC4-1: handed in, waits for the owner's word. `main` carries FG7-8 part B (the words commit / stash / go on), which is
NOT in 0.11.0; read the canon on `main` first (`docs/tasks/compact-snapshots/2026-11-12-1315-lead.md`, top section).

The journal starts anew in this repository (`journal_created`); task ids continue from the highest t-NNNN of the old journal (the history bundle), and the first `journal_created` of the new repository carries the field `continues_from: t-NNNN`.

Host quirks of the agent tools (worktrees, hand-backs, merges): `docs/RUNBOOK.md` §12.
