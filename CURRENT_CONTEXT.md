# Current Context

## Maintenance Rule

This file holds LIVE state only: the state of `main`. A batch's progress lives in the «Ход» section of its file.
This file is read on every boot — keep it short.

## Current Milestone

The forge has moved to GitHub: this repository is `Xartaxana/Forge-for-QAFactory` (private); released versions of the
package go to `Xartaxana/QAFactory` (public, marketplace `qafactory`). History before the move is not carried: the old
repository's history and run data are kept in a bundle outside GitHub (decisions O2, O3).

## Current Task

Finish the move: pile `github-move` (`plans/PILES.md`) — the first runs of `forge-check`, `nightly` and `canon` on GitHub,
the first release PR in `QAFactory`, the live run on the MyBooks stand (`docs/RUNBOOK.md` §11), and the transfer of the
experiment branch with the same tools.

The journal starts anew in this repository (`journal_created`); task ids continue from the highest t-NNNN of the old journal (the history bundle), and the first `journal_created` of the new repository carries the field `continues_from: t-NNNN`.

Host quirks of the agent tools (worktrees, hand-backs, merges): `docs/RUNBOOK.md` §12.
