# t-400 SL-4 (D) handover

State: change STAGED in C:\QAFactory\forge-repo\.claude\worktrees\fg8-1, not committed.

## git diff --cached --stat
```
 tools/piles.py               | 110 +++++++++++++++++++++++++++++++++++++------
 tools/test_collect_intake.py |   3 ++
 tools/test_piles_form.py     | 106 +++++++++++++++++++++++++++++++++++------
 tools/test_piles_take.py     |  24 ++++++++++
 4 files changed, 213 insertions(+), 30 deletions(-)
```

## Witness (verbatim)
```
( cd <wt> && python -m pytest tools/test_piles_form.py tools/test_piles_take.py tools/test_collect_intake.py tools/test_piles.py -q )
336 passed in 84.23s (0:01:24)

( cd <wt> && python tools/piles.py check --all )
(б) overlap: ok (10 active batches; 45 pair(s) of one developer not compared (dev1: github-move/3 + onboarding-forge/1, dev1: github-move/3 + onboarding-forge/2, dev1: github-move/3 + onboarding-forge/3, ...; inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two parallel sessions of one developer are no longer blocked by (б)))
(в) frozen: ok (10 taken batch(es) on origin/main; ...)
(г) backlog: ok ...
(д) form: ok (33 piles, 100 batches)
(е) findings: ok ... (WARN baseline line, not blocking)
piles check: ok

python tools/lint_ratchet.py --check
lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
```

Key (probe P1): `git clone --shared` of the worktree HEAD into the scratchpad, `git reset -q` to rebuild the index, then
`python -B <wt>/tools/piles.py --repo <clone> take <slug> <N> --who dev1 --today 2026-11-13`:
```
OLD (HEAD piles.py):
piles take: github-move/3 and forge/7 both write:  ~ changelog.d/ -- add the line "очередь: ...
piles take: driver-hosts/1 and github-move/3 both write: changelog.d/ ~ , docs/tasks/specs/reports/ ~ , experiments/ ~  ... -- add the line ...
piles take: onboarding-forge/1 and collect/4 both write: scripts/story_run.py -- add the line ...
NEW (staged piles.py), --who dev1:
piles take: forge/7 taken by dev1 (13.11.2026). Next:
piles take: driver-hosts/1 taken by dev1 (13.11.2026). Next:
piles take: collect/4 taken by dev1 (13.11.2026). Next:
NEW, forge 7 --who Ira (unreadable taker, today's rule):
piles take: github-move/3 and forge/7 both write: ai-packages/qa-factory/ (the whole package) ~ changelog.d/, ... (refused)
```
(The empty name `" ~ changelog.d/"` is now `ai-packages/qa-factory/ (the whole package)`.)

## changed: per owned file
- tools/piles.py: `+import journal_keys`; `+PACKAGE_ROOT`, `_norm_token` (root with/without slash -> PACKAGE_ROOT), `+package_tops`,
  `+shown_token`, `parse_zone` (bare root stays an unreadable part), `tokens_overlap` (`*, tops=None`, empty token overlaps nothing,
  PACKAGE_ROOT rule), `writers_of` and `fn_lists_of` (blank span dropped), `+developer_vocabulary`, `+dev_of`, `+same_developer`,
  `_pair_overlap` (new arg `tops=None`; prints `shown_token`), `check_overlap` (skip same-developer pair, ok note), `_overlap_refusal`
  (new args `who=None, vocab=None`), `cmd_take` (passes who/vocab, WARNING). Old call signatures still work (test_piles.py unchanged).
- tools/test_piles_form.py: `test_check_b_token_overlap_rules` (4th column `tops`, 6 new rows + one extra: root without slash),
  `+vocab_for`, `+test_dev_of`, `+dev_batches`, `+test_check_b_pair_by_developer`, `+PKG_TOPS`.
- tools/test_piles_take.py: `+test_take_by_developer`.
- tools/test_collect_intake.py: `test_a_card_zone_is_read_by_parse_zone_only` (bare package root, with and without slash).
- tools/piles_testkit.py: unchanged (not needed). tools/collect_intake.py: unchanged (pinned, D.6 (v)).

## Rows of section 5.4
- `test_dev_of` ids: dev10, dev1-old, two-slugs-handover, cyrillic-name, owner-and-lead, dash, empty, case-folded-with-date,
  lead-and-opus-are-not-slugs, journal-named-lead, real-github-move-3, real-onboarding-forge-1, empty-vocab,
  untracked-journal-not-slug, tracked-journal-is-slug, git-fails-empty-vocab.
- `test_check_b_pair_by_developer`: same-developer, different-developer (whole-package cell, asserts "(the whole package)"),
  waiting-node-other-developer, two-clones-one-slug.
- `test_take_by_developer`: take-passes-own-overlaps, take-refused-other-developer, take-warns-who-differs-from-clone,
  take-no-warning-without-dev-config.
- `test_check_b_token_overlap_rules` new rows: the 5 named, plus `ai-packages/qa-factory` without slash.
- `test_collect_intake.py::test_a_card_zone_is_read_by_parse_zone_only`: the package-root row.
- Status-time overlap test deletion: nothing to delete here (belongs to SL-3's tree; not present in this worktree).

## Deviations, small choices (flag for acceptance)
- D.2 ok note lists at most 3 pairs then `...` (the spec's "..." read as an elision); the count N is complete. Each entry is
  `<slug>: a/1 + b/2`.
- `dev_of` tokenises with `SLUG_RE.findall` literally as the spec says.
- The D.3 WARNING is printed after the "Next" lines and after the off-main WARNING.
- `_overlap_refusal` / `_pair_overlap` keep working with the old positional args (new args are optional).
- `test_dev_of` is a single table with a `kind` column (literal vocab, untracked, git-fails via monkeypatch of `piles.git`).

## Analogs noticed (not widened)
1. `dev_of` literal tokenising: `dev1ира` (slug glued to Cyrillic) yields token `dev1` -> slug dev1 (a wrong "same" from adversarial
   text). Closing it needs a boundary rule (lookarounds) -- a design choice, not made.
2. `tokens_overlap` PACKAGE_ROOT rule by first segment: a bare basename token (`x.py`) or a glob with a glob first segment
   (`**/x.py`) against the whole package gives False when `tops` is known (first segment not a top). The spec's rule literally;
   the existing bare-basename branch would call these overlapping against package files. Safe side would be True. Question for Lead.
3. `hod_ignored` normalises hod-list tokens without the blank filter (`_norm_token("  ")` -> "" would show as ignored): cosmetic.
4. `collect_intake.py:877` calls `_norm_token` on resolved file paths only; it is pinned by the new row. A resolved path equal to the
   package root cannot occur.
5. The 45 skipped pairs listing for the real tree is long in the ok line; SL-2/SL-3 may want a count-only form.

## Addendum after the Lead's answers (both applied)
- `tokens_overlap`: the whole package also overlaps a bare basename and a glob-first-segment token (safe side). New rows:
  `story_run.py` (True), `**/x.py` (True), `tools/*.py` (False) vs the whole package.
- `dev_of`: runs of `[\w-]+` after casefold, each must fullmatch SLUG_RE and be in vocab. New test_dev_of ids: dev1-cyrillic-glued,
  dev12-digit-glued, xdev1-letter-glued, dev1-comma, dev1-parens. Analog 1 and 2 above are closed; no spec-table conflict found.
- Witness (one run after the last edit): `python -m pytest tools/test_piles_form.py tools/test_piles_take.py tools/test_collect_intake.py
  tools/test_piles.py -q` -> `344 passed in 53.83s`; `check --all` -> `piles check: ok` with the (б) one-developer note;
  `lint_ratchet --check` -> `36 findings, 36 in the baseline, 0 new, 0 stale`.
- Diff stat: piles.py 112, test_collect_intake.py 3, test_piles_form.py 115, test_piles_take.py 24; 224 insertions, 30 deletions.
- Draft commit message: no axis line changed; read its body as "whole package also overlaps an unresolvable token".

## Draft commit message
```
piles: batches of one developer do not block each other; the package-root token is not empty (SL-4, t-400)

(б) check and `take` skip a pair whose takers read as one developer (slugs = logs/journal/<slug>.jsonl in the git index, matched as
a whole token in `взял:`); an unreadable taker is "different" as before. `take` prints a writer-side WARNING when --who reads as a
developer other than the clone's dev.config slug. `_norm_token` maps the package root to PACKAGE_ROOT instead of "", `tokens_overlap`
gets `tops=` and treats an empty token as overlapping nothing, the refusal prints "(the whole package)", `parse_zone` still reports
the bare root as an unreadable part.

axis 1 (Policy <-> role): n/a (PROJECT.md item 3 clause lands in SL-5b).
axis 2 (Per-tier exam instruments): n/a.
axis 3 (Factory package <->): n/a (package).
axis 4 (Factory rules <->): n/a.
axis 5 (Stage twins inside): n/a (package).
axis 6 (Measurement tools <->): n/a (forge_metrics does not read zones).
axis 7 (Per-test identity <->): n/a (package).
axis 8 (Where the story): n/a (package).
axis 9 (is this a): n/a.
axis 10 (git-top readers): n/a (`git ls-files` runs with the root the tool already holds).
axis 11 (shell-command recognizers): n/a.
axis 12 (carriers of the): covered (readers of `_norm_token` / `parse_zone` / `tokens_overlap`: (б), `take`, collect_intake pinned, test_piles_form table; SIBLING_MAP row added in SL-5b).
axis 13 (the dispatch text): covered (inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two parallel sessions of one developer are no longer blocked by (б); `dispatch_manifest` unchanged) (t-367 B2).
axis 14 (readers of agent): n/a.
axis 15 (console stream setup): n/a.
axis 16 (one JSON reader): n/a (package).
axis 17 (detector verdict shape): n/a (package).
axis 18 (in-tree shrink-only ratchets): n/a (no ratchet).
axis 19 (one reader of): n/a (package).
axis 20 (host receipt names): n/a (package).
axis 21 (readers of the): n/a.
axis 22 (a host's return): n/a (package).
axis 23 (fields of a): n/a (package).
axis 24 (the record of): n/a (package).
axis 25 (freshness of a): n/a (package).
axis 26 (the word stand): n/a (package).
axis 27 (the profile of): n/a (package).
axis 28 (the render site): n/a (package).
axis 29 (append-only jsonl writers): n/a (reads journal names, appends nothing).
axis 30 (the commands of): n/a (package).
axis 31 (Role carriers): n/a.
axis 32 (Where judgment lives): n/a (forge tools).
axis 33 (which dispatch am): n/a.
axis 34 (One road for): covered (one computation of "same developer" from the git index for the commit, `take` and CI; the exception by case rests on the owner's quoted word 13.11.2026, its reading pending Q-O1; dev.config read only by the writer-side WARNING).
axis 35 (Sides of a): n/a (package).
axis 36 (The row written): n/a (package).

Four questions: (a) cost: fewer false reds and doors between one developer's batches; one git call per run; (c) detector:
calibration check 33 (b'') (spec 6.2); (d) skip: commit-msg `check`, CI `check --base`, `take` on the execution path.

tier: <model>

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
```

## Needed beyond the manifest
tools/journal_keys.py (journal_names, developer_slug, JournalFile fields), tools/conftest.py (fixtures), tools/gitcmd.py (via git helper),
spec lines 1157-1177 (L-1, read only).
