# t-367: critic review of the PLAN t-356 (piles.py slimming)

Under review: `docs/tasks/specs/t-356-piles-slimming-spec.md` (802 lines, read in full). Code read on
`.claude/worktrees/read-main` at **9a7f72a**. The spec says a234cc6, but the commit message is the same, so the tree is
taken as equivalent and every line number below was re-read on 9a7f72a. Plan gate: no diff exists yet. Keys 1-9 of the
dispatch are answered in order.

**Verdict: NEEDS WORK (fit_with_fixes). 4 blocking findings, 9 non-blocking fixes.** Every blocking finding carries its
exact spec edit. Whether to accept the plan is the Lead's call. The owner-facing questions (B1, B2) belong to the owner,
and this review does not decide them.

---

## Key 1. FACTS BY TRAIL (14 load-bearing claims checked)

| # | Spec claim | Carrier read | Result |
|---|---|---|---|
| 1 | pre-commit:38-40 runs `board --check --if-staged`, pre-merge-commit:19-20 runs `board --check` | `.githooks/pre-commit`, `.githooks/pre-merge-commit` (cat, grep -n) | confirmed |
| 2 | forge-check.yml:81 has the `board --check` step; :85 has `check --all --base "$BASE"` | `.github/workflows/forge-check.yml:81,85` | confirmed |
| 3 | settings.json:139,158, .gitattributes:21, mechanism_gate.py:254, test_workflows.py:154-155 | grep -n | confirmed |
| 4 | `_norm_token` turns `ai-packages/qa-factory/` into "", and `tokens_overlap` matches "" against the empty basename of a folder token | piles.py:1322-1324, 1383-1400; traced by hand | confirmed. Also: "" matches ONLY folder tokens, so a whole-package node does NOT collide with a literal file token today (a false green). The spec's fix (iii) closes that too |
| 5 | The empty token comes from GM3-2 (github-move/3:30), not from `нет` or an empty cell | github-move/batch-3 row 30: the cell holds `` `ai-packages/qa-factory/` ``, status **сдано** | confirmed. Probe below: `writers_of` of github-move/3 holds "" |
| 6 | `take` is refused by waiting-node zones of onboarding-forge/1 and by github-move/3's empty token | probe P1 (below): `_overlap_refusal` run read-only over every waiting batch | confirmed and WORSE than the brief: **21 of 22 waiting batches with nodes are refused** (the brief says 5). Only release-next/2 passes, and all its nodes are принято |
| 7 | (а) a9 and (д)'s unreadable-finding red carry the wildcard `CARDS_AND_FINDINGS` | piles.py:1169, 1201-1203, 1313, 2041 | confirmed |
| 8 | `load_tree` walks folders on disk (untracked piles are read) | piles.py:853-864 | confirmed |
| 9 | (в) masks the header статус, the node/proof Статус cells and the card Статус | piles.py:1676-1690 (`_frozen_lines`), 1731-1741 (`_compare_card`) | confirmed |
| 10 | (г) compares rows and the lock only, so a BACKLOG header-prose edit passes | piles.py:1803-1825 (`_g_after_freeze`) | confirmed |
| 11 | `apply_changes` puts the board in the rollback set | piles.py:3032 (`... + [board]`) | confirmed |
| 12 | Measured friction: 588 commits, 140 with a skip, 260 lines, ~240 live-run-fvf | P2 (below) | confirmed (591 / 141 / 264 / 245; a few commits newer) |
| 13 | NEGATIVE: `DECISIONS.md` has no board hit | `grep -c -i "PILES\.md\|board" DECISIONS.md` = 0. Positive control, same form: `grep -c -i "D-00"` = 23 | confirmed |
| 14 | NEGATIVE: nothing else reads the board (§2 inventory) | P3: `git grep -n -i -E "PILES\.md\|piles\.py board\|piles board\|board --check\|BOARD_REL\|board-check"` over the tracked tree (history paths excluded). Control: the same call finds `tools/piles.py` / `.githooks/pre-commit:40` | confirmed apart from the misses in Key 3. `docs/RUNBOOK.md`, `BOOT.md`, `.claude/agents`, `.claude/skills`: 0 hits for `piles.py`; control `PROJECT.md:7` |
| 15 | `disk_journal_files` gives the developer vocabulary, "tracked, so the same in CI and on every clone" (D.1, D.4, F-D2) | journal_keys.py:533-538 | **WRONG**: it lists the folder ON DISK (`os.scandir`), not the git index. See B4 |
| 16 | The inside-one-developer guard is "the dispatch gate's owns overlap" (D.2 ok line, axis 13) | owns_gate.py:300-330, 930-996 | **inaccurate**: it is `tools/owns_gate.py`, it only WARNs, and it covers live dispatch records only, not taken batches. See B2 |

Every claim the verdict below rests on was re-checked here. No claim was taken from the spec on faith.

## Key 2. OWNER'S WORDS

- **Word 2 (board out of PROJECT.md and the script): served exactly.** The extra removals (hooks, CI, settings,
  .gitattributes, cards, SIBLING_MAP, protocol, README) are the board's readers, which must change with their producer.
  They are not widenings. The B-id table of contents and the count line go with it. F-1 keeps the one number someone
  still needs. That is a technical choice.
- **Word 1 («мешает закрывать узлы … Может его переписать?»): served by a reading of it, not by the owner's own text.**
  SL-2 (scope) and SL-3 (status) are the Lead's reading of «мешает закрывать узлы». The measured friction supports that
  reading. Two points are not in the owner's words:
  - the question «переписать?» is answered with "slim it", and the spec records no owner reply to that;
  - SL-2 changes WHAT BLOCKS A COMMIT for both developers, which is the team agreement of D-0036 / D-0044.
  Neither blocks the plan. Both belong in the owner-facing plan of PROJECT.md «новая идея» step 4, one line each, before
  builders start (fix N1).
- **Word 3: NOT served exactly, in two opposite directions.** These are B1 and B2.
  - **B1 (narrowed): F-D1's recommendation contradicts the owner.** The owner's sentence was about exactly the mechanism F-D1
    asks about. The quote the spec itself gives (§1 lines 14-16): «the script counts a batch's zone by all unaccepted nodes, so
    one waiting node with a zone like scripts/tests/ blocks the take of any other batch» → «это надо исправить» → «Это верно
    для двух разработчиков и не верно внутри одной сессии». The owner calls the waiting-node block RIGHT between two
    developers. That is F-D1 option (3) between different developers. The spec recommends (1), which removes it.
    Worse, (1) makes `take` empty:
    - at take, EVERY node of the batch being taken is «ожидает» (probe P1: the node-status column of all 21 refused batches
      is `['ожидает']`, or a mix with принято);
    - under (1) the batch being taken therefore has no zone, so `take` can never refuse anything, between any two people;
    - the cost line of F-D1 ("a collision is found later") hides this.
  - **B2 (widened): "same developer" is wider than the owner's "одной сессии".** The spec turns «внутри одной сессии» into
    "the same developer slug in `взял:`": every session, every clone and every day of dev1.
    - The journal shows dev1 working from several sessions in parallel (compact snapshots named `…-manual`, `…-lead`,
      `…-narrative` on the same day).
    - CLAUDE.md rule 4 names parallel SESSIONS of one repo as the same hazard as parallel workers.
    - The guard the spec names for inside one developer (D.2 ok line) is `owns_gate`'s WARN over live dispatch records
      (owns_gate.py:993 «OWNS OVERLAP (warn)»). It is not a gate over taken batches, and it does not see a batch taken
      yesterday by another session.
    - The widening may be what the owner meant ("developer" vs "session" is a fair reading of «двух разработчиков»). But
      choosing it is interpreting intent (CLAUDE.md 11a), so it is the owner's call.
- Kept but not asked for: the `release` refused alias stays while `board` becomes a usage error (see Key 9). That is a
  technical choice.

## Key 3. SAFETY OF REMOVAL: readers the spec misses

The spec's inventory (§2) is nearly complete. Misses found by P3 and the import scan P4:

1. `.github/workflows/nightly.yml:12`: a comment «board-check is not ported: it mirrors piles to GitLab issues». History of
   the GitLab job, not a reader. Reword or leave, but list it (fix N7).
2. `tools/test_workflows.py:8`: the docstring «without `board-check`». The same history class. Same treatment.
3. **`tools/collect_intake.py:846,877` reads `piles.parse_zone` and `piles._norm_token`.** SL-4 changes `_norm_token`
   (fix (i)), so this is a reader of the changed producer on axis 12 («ONE zone reader `piles.parse_zone`»).
   - Today a zone part `` `ai-packages/qa-factory/` `` normalises to "", and `parse_zone` reports it as an error, "cannot be
     read".
   - After SL-4 (i) the same part becomes `ai-packages/qa-factory/**`, a pattern in the UN-normalised space. It silently
     matches no package-relative path (collect_intake normalises the paths it matches, :877).
   - So an error that is reported today becomes a silent miss.
   - No card holds such a zone today (grep over `plans/piles/*/README.md`: 0), so the defect is latent.
   - This is part of B3: the producer and its readers change together.
4. **`tools/test_piles_form.py:58-73`** (`test_check_b_token_overlap_rules`) calls `tokens_overlap(a, b)` with two
   arguments. SL-4 (iii) changes the signature to `(a, b, tops)`, but the file is not in SL-4's owns. This is part of B3.

Every other reader the dispatch names was checked, with no further miss: hooks, CI, tests, backlog_tree (it reads
`load_tree`, not the file; test_backlog_tree untouched), RUNBOOK (0), PROJECT.md / AGENTS.md (listed), skills (0, control
`next-task` found by its own name), compact_snapshot (`leftovers_unowned`, kept), forge_metrics (`load_tree`, kept),
hook_liveness_probe cases 14/15 (`check`, not board).

## Key 4. THE ZONE RULE

- **Where the identity comes from:**
  - The taker's free text in `взял:` is the only identity read. `take --who` accepts any 1-40 characters and nothing
    checks them against the clone's `tools/dev.config.yaml`.
  - Vocabulary in a hook: `logs/journal/*` on the clone's DISK.
  - Vocabulary in CI: the files of the checkout.
  - These differ when a clone holds an untracked journal file, for example a new developer whose `journal_created` line is
    not committed yet. Then the commit reads "same" and CI reads "different": green at the commit, red in CI. That is the
    two-roads class (P31) that F-D2 says it avoids.
  - The error direction there is the safe one, but the spec's claim "tracked, so identical in CI" is false (B4).
- **Absent identity:** an unreadable or foreign `взял:`, no journal folder, or a new slug all read None, which means
  "different", which means today's rule. That is correct.
- **Two clones sharing one slug: wrong direction.** Two people who both configure `dev1`:
  - read as one developer, so protection is lost between two real people;
  - nothing detects it. Check 33(e) catches two FILES with one slug after casefold, but two clones writing one file merge
    by union, silently.
  - A taker typing someone else's slug (`--who dev2` from dev1's clone) is the same class.
  - The spec's adversarial table covers none of this.
- **Does the two-developer protection survive?**
  - With D.1 as written and F-D1 (3): yes, in every case where the slugs differ.
  - With F-D1 (1): no. `take` stops protecting anything (B1).
- **Error direction:** the safe wrong answer is "different" (a false red has doors: `очередь:`, function lists,
  `piles-skip: б`). The unsafe one is "same" (a silent green between two people, no door needed, nothing logged). The spec
  states this direction correctly for `dev_of`. It does not cover the two false-"same" sources above (B4).

## Key 5. THE FORKS

| Fork | Recommendation right? | Cost | Who decides |
|---|---|---|---|
| F-1 (next free B-id) | (a) is right in kind. Defect: SL-1 deletes `_open_sets` and `toc_lines`, but `_count_line` needs `ids`, `open_ids` and `live` from them (piles.py:985-1062), so "moved unchanged" is impossible as written | about 15 lines, plus KEEPING `_open_sets` and the id computation (fix N2) | technical: the Lead |
| F-2 (CI step) | (a) is right. (c) is not: its premise "the audit line is what check 33 (a) reads" is false. Check 33(a) runs `check --all` on origin/main ITSELF (protocol :982-985) and never reads a CI log. A `|| true` step has no reader and is a second road for the same audit | (a): nothing; (c): one unread step plus one more pin | technical: the Lead. Recommend (a), and name 33(a) as the audit (fix N3) |
| F-3 (a9 carrier) | (a) is right: it keeps "a red the commit creates blocks that commit". A git grep runs only when a9 reds exist | one `git grep -l <id> <rev> -- plans/piles` per a9 red | technical: the Lead |
| F-D1 (waiting zones between developers) | **wrong**: answered by the owner's word 3 as (3), and (1) makes take empty (B1) | (3): today's refusals stay between developers only; (1): take never refuses | **the owner** (already spoken; a reversal goes back to the owner) |
| F-D2 (identity source) | (a) is right in kind (one computation everywhere), but build it from the git INDEX / tree, not the disk (B4) | as spec | technical: the Lead |

## Key 6. CHECKS ON TOUCHED PILES ONLY: does narrowing open a hole?

- **Yes, one class is missed by the spec's invariant B.3** ("a red this commit CREATES always has a carrier in a pile it
  touches or in BACKLOG").
  - (б)'s function-list verdicts read CODE files: `defined_names` reads the `.py` in the working tree (piles.py:1450-1468,
    used at :1515). A code commit that renames or removes a function named in a batch's `функции:` list creates a (б) red
    ("undefined"), and it touches no pile.
  - Today the commit-msg hook already skips that commit (`_relevant`, piles.py:2233). But CI's `check --all --base` (:85)
    judges every push and catches it.
  - Under F-2 (a) it is caught by nobody until weekly check 33(a).
  - So B.3 is false for this class, and §4 B does not list it (B3 part c).
- **Second, smaller sibling (same surface, "what the check reads"):** the check reads the WORKING TREE, not the index.
  - B.2 handles one instance: untracked piles.
  - The neighbour stays open: another session's UNSTAGED edits to a tracked file of a TOUCHED pile are judged as if they
    were part of the commit, either way.
  - The problem exists today too, but SL-2 is the node that owns "what a commit is judged on", so it should name it
    (fix N4).
- **Is the non-blocking audit read by someone?**
  - B.5's "N red(s) in piles this commit does not touch" line is printed to the committer, who need not act.
  - The CI `|| true` line of F-2 (c) is read by nobody.
  - The real reader is calibration check 33(a), which is weekly and shows as overdue in the Boot Report after 7 days.
  - That is acceptable only if the spec names 33(a) as THE reader and drops the CI line (fix N3).
- **Neighbour classes walked (surface: "the carrier set of a red"):**
  - deleted pile: covered, B.3 (е) and the `deleted-pile-move-line` row;
  - renamed batch: covered;
  - BACKLOG-only commit: covered;
  - (в) against a moving origin/main: no new hole, because drift on main is already on main;
  - the time-dependent FINDINGS_FROM: static, so no hole;
  - code-dependent (б) lists: the hole above.

## Key 7. FEASIBILITY AND CUT

- **SL-1 cannot be committed by its builder as specified (B3 part a).**
  - Hooks run from the in-tree `.githooks` (`core.hooksPath = C:\QAFactory\forge-repo\.githooks`, read).
  - SL-1's owns include `plans/PILES.md (delete)`. Staging that deletion makes `board_triggers` true (piles.py:1096-1097
    lists `BOARD_REL`), so the unchanged pre-commit runs `piles.py board --check --if-staged` against the builder's new
    piles.py, which has no `board`. The result is an argparse invalid choice, exit 1, and `set -e` refuses the commit.
  - The builder must not place hook files (CLAUDE.md rule 2), so it cannot get around this.
- **The merge procedure is unstated.** A clean `git merge` auto-commits and runs `pre-merge-commit`, still with
  `board --check`, which fails the same way. The Lead must conclude with `git merge --no-commit` → place hooks / CI /
  settings → `git rm plans/PILES.md` → `git commit` (pre-commit then runs the NEW hook from the working tree). The spec
  should also say which branch this is: batch work goes on `pile/forge/batch-8` with one PR into main (PROJECT.md
  «Командная работа» p.1), so "main between nodes" means the batch branch.
- **SL-4 tests reach into SL-3** (B3 part b): §5.4 assigns `test_node_status_to_v_rabote_runs_overlap` to SL-4, but the
  `status` command is created by SL-3, which runs two nodes later. The overlap check at `status --set "в работе"` (F-D1
  (1)) is in no node's Behaviour or edges (SL-3's edges 1-11 have no overlap edge). If B1 is fixed as recommended, this
  goes away.
- **Owns not disjoint where they should be:**
  - SL-4 needs `tools/test_piles_form.py` (the (б) tests and `test_check_b_only_active_batches_and_unfinished_nodes_count`
    live there, not in test_piles.py's "(б) section"), and it is missing from SL-4's owns.
  - SL-2 owns test_piles_form.py too. They run in a queue, so the overlap is fine, but both must list it.
- **The weakest node is SL-2.** It carries a false invariant (Key 6), the largest semantic change, and nine files. SL-1 is
  mechanical. SL-3 is well edged. SL-4 is small once B1, B2 and B4 are settled.
- **Ready-to-paste batch 8:**
  - FG8-2's «Пишет в» lists `dev_of` without the `+`, while the spec's own SL-4 writes `+dev_of`, and it omits
    `+developer_vocabulary` and `+same_developer`. Under D-0048 grammar a bare name that does not exist yet is "undefined",
    a red as soon as another batch lists functions on piles.py (`_item_verdict`, piles.py around 1490).
  - The preamble says «designer → builder → critic — кодовый узел», but every row says `builder → critic`.
  - Fix N5.
- **Executable by Sonnet with nothing to invent:** SL-1 yes after B3(a). SL-3 yes. SL-6 yes. SL-2 and SL-4 only after
  B1-B4.

## Key 8. MECHANISM QUESTIONS (CLAUDE.md rule 10)

- The spec ships ONE axis block (§6.7) "for SL-5", but five commits carry mechanisms: SL-5a with SL-1, SL-4 (a gate's duty),
  SL-2 (a gate's scope), SL-3 (a new status writer) and SL-5b.
  - Rule 10(b) wants a block per mechanism, or one block whose lines close each mechanism BY NAME. The §6.7 lines do not
    name the mechanism, and axis 13 speaks only for SL-4.
  - (c) Detectors: SL-2 has the new (b′). SL-1 has `test_backlog_tree.py`. **SL-4 has none**: nothing would ever see a
    false "same" hiding a cross-developer overlap. A cheap one is a check-33 line that compares the slugs in `взял:` of
    the pairs skipped as one developer's (printed by the D.2 ok line) against the journal of the claimed slug (fix N6).
    SL-3's detector (33(d) «card row Статус ahead of its batch file») is not named.
  - (d) What stops it being skipped: named for SL-2 only (commit-msg, CI).
  - (a) Cost: answered.
  - Fix N6.
- The axis answers themselves were spot-checked against the 36 headings of docs/SIBLING_MAP.md (read). Axis 12 is covered
  but misses collect_intake (Key 3). Axis 13 cites the wrong guard (Key 2, B2). Axis 34: see Key 9.

## Key 9. DUPLICATION, CODE QUALITY, ONE ROAD, CLASS-WIDE COMPLETENESS

- **DUPLICATION AND CONSISTENCY: three findings.**
  1. §5.4 adds a new `test_package_root_token` table beside the existing parametrized table
     `test_check_b_token_overlap_rules` (test_piles_form.py:58-73). That is two tables for one behaviour (docs/TESTING.md:
     one parametrized test per behaviour). The rows go into the existing table (B3).
  2. SL-3 edge 3 defines a node status order (ожидает < в работе < сдано < принято, отклонено final) next to the existing
     `STATUS_ORDER` (piles.py:108), which (в) already uses for "only forward". Extend the one table with `отклонено`. Do
     not write a second order (fix N8).
  3. SL-4 (iii) `tops` ("first segment is an entry of the package dir on disk") resembles
     `dispatch_manifest.path_candidates`' "first segment is a top-level entry of the root" (axis 13). They are different
     roots, so not a clone. Note only.
- **CODE QUALITY: none blocking.** The spec removes about 210 lines of board code and adds small, single-purpose functions.
  SL-3's `cmd_status` with 11 edges risks exceeding 60 lines. The spec should say "one refusal helper per edge class", or
  the critic of SL-3 will flag it (note).
- **ONE ROAD (P31, item 12):**
  - (a) The same-developer exception from (б) is an exception by case. It is legitimate only on the owner's quoted word,
    and the word quoted is «одной сессии», not "one developer" (B2). Until the owner confirms, the exception is wider than
    its carrier.
  - (b) F-2 (c) runs the audit by two roads in CI (blocking range plus `|| true` whole tree). Drop (c) (fix N3).
  - (c) The retired subcommands take two roads: `release` stays a refused alias that names the new road (piles.py:3217
    comment), while `board` becomes a bare argparse usage error. One road: make `board` a refused alias like `release`,
    naming the «Бэклог» pane and `backlog_tree.py`. Or retire both the same way and say so (fix N9).
  - Searched: the spec text for "unchanged" / "not supported" / non-goals (none exclude a language or project); piles.py
    COMMANDS (:3216-3218).
- **CLASS-WIDE COMPLETENESS (axis 12, the map):**
  - producer `piles.py` → readers `backlog_tree`, `compact_snapshot`, `forge_metrics`: covered.
  - `collect_intake` (parse_zone / _norm_token): MISSED (B3).
  - `test_piles_form`: MISSED (B3).
  - hook_liveness_probe 14/15: covered.
  - The axis-12 «Queued» Q8 item (`_incoming`): struck by the spec, correct.
  - The untracked-file class at the `take` surface: `cmd_take` uses the strict `load_tree(root)` (piles.py:2479), so a
    foreign session's untracked broken or active batch can still make `take` CannotRun or refuse. B.2 fixes `check` only.
    Queue it or fix it in SL-2 (fix N4).

---

## Blocking findings, each with its exact spec edit

**B1. F-D1 recommends against the owner's word, and option (1) makes `take` empty.**
Evidence: Key 2, Key 4, probe P1 (every batch being taken has only «ожидает» nodes).
Spec edits:
- §1 line 37-38, replace «Whether a waiting node holds a zone (F-D1) is intent: the owner decides it.» with «Between
  DIFFERENT developers a waiting node holds its zone, as today: the owner's word 13.11.2026 («Это верно для двух
  разработчиков»), F-D1 (3).»
- §7 F-D1: mark «Decided by the owner: (3) between different developers». Keep (1) only as «to reopen it, ask the owner;
  cost: `take` never refuses, because every node of a batch being taken is «ожидает»».
- §3 SL-4 D.5: «`writers_of` is unchanged.»
- §5.4: delete the two «Where F-D1 (1) is accepted» tests.
- §8 note on FG8-6: drop the clause «Under F-D1 (1) it holds nothing while waiting».

**B2. "Same developer" widens the owner's «внутри одной сессии» without the owner's word.**
Evidence: Key 2, owns_gate.py:300-330 / 930-996 (a WARN over live dispatch records).
Spec edits:
- §1 D: append «Reading: "session" is taken as "developer slug" (every session and clone of dev1). This is wider than the
  word; QUESTION TO THE OWNER, with a recommendation: (a) one developer = one slug (recommended: no session identity exists
  in `взял:`); (b) narrower: none available without a session id in `взял:`. The node runs on (a) until the answer
  (PROJECT.md «Командная работа» p. 11).»
- §3 SL-4 D.2 ok-line text: replace «the dispatch gate's owns overlap judges inside one developer's work» with «inside one
  developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two parallel sessions of one
  developer are no longer blocked by (б)».
- §6.7 axis 13: the same correction.

**B3. Producer, readers and order: four defects in the cut.**
- (a) SL-1 cannot be committed by its builder. Edit §3 SL-1 owns: remove `…\plans\PILES.md (delete)` and `…\.gitattributes`.
  Move both into SL-5a. Edit «Temporal edge» to «The Lead integrates SL-1 by `git merge --no-commit --no-ff <node branch>`,
  places the hook / CI / settings content, runs `git rm plans/PILES.md`, edits `.gitattributes`, then `git commit`
  (pre-commit then runs the NEW hook). A plain merge auto-commits through the OLD pre-merge-commit and is refused (exit 1).»
  Name the branch the nodes integrate into (`pile/forge/batch-8`).
- (b) SL-4 tests point at SL-3. With B1 fixed, delete `test_node_status_to_v_rabote_runs_overlap` from §5.4. Without B1,
  move the status-time overlap check and its test into SL-3's Behaviour, edges and §5.3.
- (c) The B.3 invariant is false for (б) function-list reds created by code commits. Edit §3 SL-2 B.3 and §4 B, adding one
  bullet: «(б) function-list verdicts read the named `.py` (`defined_names`). A code commit that removes a listed name
  creates a red with no pile path. Carrier = (b1.path, b2.path, the `.py`). In a commit, the check runs when a staged path
  is a `.py` named in an active batch's function list (extend `_relevant`). In CI `--base`, the range's paths are carriers
  too.» (Or the Lead accepts the hole explicitly with check 33(a) as its named detector. Then say so in §4 B.)
- (d) Readers of `_norm_token` / `tokens_overlap` missing from SL-4. Edit §3 SL-4 owns: add `tools/test_piles_form.py` and
  `tools/collect_intake.py (no change expected; pinned)`. Add to D.6: «(v) `parse_zone` keeps reporting the package root as
  an unreadable zone part (or maps it to every package path): never a pattern in the un-normalised space.
  `tools/test_collect_intake.py::test_a_card_zone_is_read_by_parse_zone_only` gains the row
  `` `ai-packages/qa-factory/` ``.» Make `tops` a keyword argument. §5.4: move the `test_package_root_token` rows into
  `test_check_b_token_overlap_rules`.

**B4. The identity vocabulary is not what the spec says, and the unsafe "same" cases are unnamed.**
Evidence: journal_keys.py:533-538 (`os.scandir`), Key 4.
Spec edits:
- §3 SL-4 D.1: replace «`journal_keys.disk_journal_files(root)`: tracked, so the same in CI and on every clone» with «the
  slugs of `git ls-files -z logs/journal` passed through `journal_keys.journal_names` (the index: in a commit the staged
  tree, in CI the checkout). An untracked journal file is not a slug until it is committed.»
- Add to the adversarial list two false-"same" rows and their accepted risk:
  - «two people configured with one slug: read as one developer (accepted; detector: N6)»;
  - «`--who <another's slug>`: read as that developer».
- §3 SL-4 D.3: add «`take` prints a WARNING when `dev_of(--who)` differs from the clone's `journal_keys.developer_slug`»
  (a writer-side guard. It reads dev.config only at the writer, so the check side stays one road).
- §7 F-D2 (a): the same wording fix.

## Non-blocking fixes

- N1. The owner-facing plan (PROJECT.md new-idea step 4) carries one line each: "slim, not rewrite" (word 1's question),
  and "a commit is blocked only by reds of the piles it touches" (a team-agreement change).
- N2. F-1 (a): SL-1 keeps `_open_sets` and the `ids` computation for `summary`, so §2.1 / SL-1's removal list drops
  `_open_sets`, and `toc_lines` is split.
- N3. F-2: recommend (a). Delete «The audit line is what check 33 (a) reads» and option (c). §6.2: check 33(a) is the named
  reader of untouched-pile reds.
- N4. SL-2 B.2: one line: «the check reads the working tree; unstaged edits of a touched pile are judged as part of the
  commit (pre-existing)». Queue the strict `load_tree` in `cmd_take` (the untracked-foreign-batch sibling) as a node or a
  finding.
- N5. §8: FG8-2's cell becomes `tools/piles.py (+dev_of, +developer_vocabulary, +same_developer, check_overlap, …)`.
  Reconcile the «Исполнитель» preamble with the rows.
- N6. §6.7: one axis block per mechanism commit (SL-5a/SL-1, SL-4, SL-2, SL-3, SL-5b), or lines that name the mechanism.
  The (c) detector for SL-4 is a check-33 line: the pairs printed by the D.2 ok line, with each claimed slug's journal
  showing that clone's work on both batches. SL-3's detector is named 33(d).
- N7. §2.1: list `nightly.yml:12` and `test_workflows.py:8` (history comments about the GitLab `board-check`), with a
  verdict.
- N8. SL-3 edge 3: extend `STATUS_ORDER` with `отклонено`; no second order table.
- N9. `board`: a refused alias like `release` (names the «Бэклог» pane / `backlog_tree.py`), or retire both alike.
- §6.1 (6) (the PROJECT.md item 3 clause on one developer's batches) must be MANDATORY, not optional. Without it item 3
  states a rule the code no longer enforces.

## Trail

Read in full: the spec under review. On read-main (9a7f72a):
- `tools/piles.py`: 100-110, 195-215, 853-907, 985-1122, 1165-1215, 1305-1415, 1450-1468, 1490-1530, 1554-1610, 1670-1745,
  1800-1830, 2031-2044, 2177-2350, 2440-2510, 3026-3053, 3180-3225;
- `tools/journal_keys.py`: 440-575;
- `tools/owns_gate.py`: 300-330, 930-1000;
- `.githooks/pre-commit`, `pre-merge-commit`, `commit-msg` (whole);
- `.github/workflows/forge-check.yml`: 60-106;
- `tools/test_piles_form.py`: 50-75;
- `tools/hook_liveness_probe.py`: 941-1000, 1363-1385;
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: 970-1025, 1078-1088;
- `docs/SIBLING_MAP.md`: headings, axis 1, axes 12-13;
- `PROJECT.md`: 276-302;
- `plans/BACKLOG.md`: 5-8, 22-26;
- `plans/piles/_template/finding.md`: 11-14;
- the GM3-2 row of github-move/batch-3;
- `tools/critic_verdict.schema.json`;
- `docs/tasks/critic-diff-brief.md`: items 1-12.

Commands, all read-only, with results:
- P0 `git -C <read-main> log --oneline -1` → `9a7f72a journal: t-346/t-349 accepted, t-353 delegated; …`
- P0b `python -B tools/piles.py check --all` (subshell in read-main) → exit 0: «(б) overlap: ok (10 active batches)»,
  «(е) … 152 older are the baseline», «piles check: ok».
- P1 a read-only scratch script (scratchpad/probe.py: `load_tree(tolerant=True)`, `_overlap_refusal` per waiting batch,
  `writers_of` of active batches) → 21 of 22 waiting batches REFUSED (by github-move/3 or onboarding-forge/1), release-next/2
  PASS. All 10 active batches are dev1's. Empty token only in github-move/3.
- P2 `git log --since=2026-10-08` piles-skip count → «commits with skip 141 skip lines 264 mentioning live-run-fvf 245» of
  591 commits.
- P3 `git grep -n -i -E "PILES\.md|piles\.py board|piles board|board --check|BOARD_REL|board-check"` (history paths
  excluded) → the list in Key 3. Control: hits in `.githooks/pre-commit:40` and `tools/piles.py`.
- P4 `git grep -n -i "piles"` over `tools/*.py` (import and call sites) → collect_intake (parse_zone, _norm_token),
  compact_snapshot, forge_metrics, canon_clock, backlog_tree, test_piles_form (tokens_overlap).
- P5 `grep -c -i "PILES\.md|board" DECISIONS.md` → 0; control `grep -c -i "D-00"` → 23.
- P6 `git -C <read-main> config core.hooksPath` → `C:\QAFactory\forge-repo\.githooks`.
- P7 `git grep -c -i "piles.py" -- PROJECT.md docs/RUNBOOK.md BOOT.md .claude/agents .claude/skills` → `PROJECT.md:7` only.
- P8 the `взял:` values of non-closed, non-waiting batches → all dev1 (`dev1, 05.11.2026`; `dev1 (Opus coord), 12.11.2026`
  ×6; `… 13.11.2026`; `Lead dev1 (Opus), 13.11.2026`).
- P9 grep of card zones for the package root → 0.

Not done: the spec's PROJECT.md byte counts (the Lead measures them, as the spec says). No tree was modified (scratch
script in the scratchpad only).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: F-D1 recommends option (1) against the owner's word 3 (waiting-node zones are right between two developers), and (1) makes take empty because every node of a batch being taken is ozhidaet (probe P1); edit section 1, F-D1, D.5 and section 5.4 to decide (3) between different developers",
    "B2: same developer (slug) widens the owner's word one session; the named inside-developer guard is owns_gate WARN over live dispatches only; add the reading as a question to the owner with recommendation (a), correct the D.2 ok line and axis 13",
    "B3: the cut. (a) the SL-1 builder cannot commit the PILES.md deletion through the unchanged pre-commit (board_triggers lists BOARD_REL, so argparse exits 1), so move the delete and .gitattributes into SL-5a and state the merge --no-commit procedure; (b) SL-4 tests reach the SL-3 status command; (c) the B.3 invariant is false for function-list reds that code commits create (defined_names reads the .py); (d) the readers of _norm_token and tokens_overlap (collect_intake parse_zone, test_piles_form) are missing from SL-4's owns",
    "B4: the developer vocabulary comes from os.scandir on disk, not the tracked files, so CI and the commit can differ; the false-same cases (two clones with one slug, --who naming another person's slug) are unnamed; build the slugs from git ls-files and add a writer-side WARNING in take"
  ],
  "fixes": [
    "N1: the owner-facing plan names slim-not-rewrite and the change of what blocks a commit",
    "N2: F-1 (a) needs _open_sets and the id computation kept; fix the SL-1 removal list",
    "N3: F-2 recommend (a); the claim that check 33 (a) reads the CI audit line is false; drop (c)",
    "N4: SL-2 names the working-tree-versus-index reading; queue the strict load_tree in cmd_take (the untracked sibling)",
    "N5: FG8-2 cell needs +dev_of, +developer_vocabulary, +same_developer; reconcile the executor preamble of batch 8",
    "N6: one axis block per mechanism commit; a registered detector for SL-4 (check 33 line) and SL-3 (33 d)",
    "N7: list nightly.yml:12 and test_workflows.py:8 history comments with a verdict",
    "N8: SL-3 extends STATUS_ORDER with otkloneno instead of a second order table",
    "N9: board as a refused alias like release, or retire both alike; make PROJECT.md edit (6) mandatory"
  ],
  "class_completeness": "Axis 12 walked: producer piles.py to readers backlog_tree, compact_snapshot, forge_metrics, hook_liveness_probe 14/15 covered; collect_intake (parse_zone, _norm_token) and test_piles_form (tokens_overlap) missed (B3 d); the untracked-file class is fixed for check but not for take (N4); the code-dependent function-list red class is outside the B.3 invariant (B3 c). Axis 13 cites the wrong guard (B2). Axis 34: the same-developer exception rests on a widened reading of the quoted word (B2); F-2 (c) is a second road (N3); board vs release alias (N9).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-356-piles-slimming-spec.md (whole)",
      "read-main tools/piles.py 100-110, 195-215, 853-907, 985-1122, 1165-1215, 1305-1415, 1450-1530, 1554-1610, 1670-1745, 1800-1830, 2031-2044, 2177-2350, 2440-2510, 3026-3053, 3180-3225",
      "read-main tools/journal_keys.py 440-575",
      "read-main tools/owns_gate.py 300-330, 930-1000",
      "read-main .githooks/pre-commit, pre-merge-commit, commit-msg",
      "read-main .github/workflows/forge-check.yml 60-106",
      "read-main tools/test_piles_form.py 50-75",
      "read-main tools/hook_liveness_probe.py 941-1000, 1363-1385",
      "read-main PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 970-1025, 1078-1088",
      "read-main docs/SIBLING_MAP.md headings, axis 1, axes 12-13",
      "read-main PROJECT.md 276-302; plans/BACKLOG.md 5-8, 22-26; plans/piles/_template/finding.md 11-14; github-move batch-3 row 30",
      "tools/critic_verdict.schema.json; docs/tasks/critic-diff-brief.md items 1-12"
    ],
    "reruns": [
      {"command": "python -B tools/piles.py check --all (subshell in read-main 9a7f72a)", "result": "exit 0; (b) overlap ok (10 active batches); piles check: ok"},
      {"command": "scratchpad probe.py: _overlap_refusal over every waiting batch (read-only)", "result": "21 of 22 waiting batches refused (github-move/3 or onboarding-forge/1); only release-next/2 passes; all active batches dev1; empty token only in github-move/3"},
      {"command": "git log --since=2026-10-08 piles-skip count", "result": "591 commits, 141 with skip, 264 lines, 245 mention live-run-fvf"},
      {"command": "git grep -n -i -E board/PILES.md pattern over the tracked tree (history excluded), control in .githooks/pre-commit:40", "result": "inventory confirmed; misses nightly.yml:12 and test_workflows.py:8 (comments)"},
      {"command": "grep -c -i board/PILES.md DECISIONS.md; control grep -c D-00", "result": "0; control 23"},
      {"command": "git config core.hooksPath (read-main)", "result": "C:/QAFactory/forge-repo/.githooks (in-tree)"}
    ]
  }
}
```
