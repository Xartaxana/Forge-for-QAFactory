# t-943 — critic on PLAN, second pass: «Всё в кучках» r2 (fix round t-926) + the new §8 (W3)

Reviewer: critic (Opus). Object: `docs/tasks/specs/20261117-everything-in-piles-spec.md` (DRAFT r2, 1013 lines), its fix
table, and §8 / streams K, K2 / fork F21. Prior verdict: `docs/tasks/specs/reviews/t-920-everything-in-piles-plan.md`.
Nothing edited except this file; no test set run (plan gate). This verdict is an INPUT to the Lead's acceptance, not the
acceptance (critic rule 6). Repo state read: HEAD = origin/main = `e2e3b30b`.

**Verdict: GO WITH FIXES — NEEDS WORK. Six blocking findings (R1-R6); the rest are fixes in this spec (F-a … F-n) or
lines for another file (named). Re-pass of the critic: owed only on R5 (it changes the shape of §8); the rest the Lead
checks against this list.**

---

## (1) The fix table, checked by trail

| t-920 | closed by | checked against code | state |
|---|---|---|---|
| B1 | §2.3: `remarks` in the verdict, `status --set принято --verdict`, wave forwards it, back-reference in (д) | `tools/critic_verdict.schema.json`: required `[verdict, blockers, class_completeness, trail]`, `additionalProperties: true` (python json load); `critic_verdict_check.py` stdlib-only, `check_text` at :172, not called by any hook/tool (grep `-i critic_verdict_check\|validate_verdict` over tools/.githooks/.github/.claude/PROCESS → the tool, its test, docs, `settings.json` allow, `critic.md`) — P31 confirmed; `piles.py cmd_status` :3335-3365 and `_status_node_row/_status_node_cell` :3267-3297 have no batch-status test — P29 confirmed; `wave.py record_node` :251-266 runs `piles.py status … --set принято` inside the temp worktree after the merge — P30 confirmed | **closed in design, but with two holes: R1 (hand edit), R2 (circular import); and F-a (a `blocker` verdict passes)** |
| B2 | §2.4: flow gate at ADD time in (д), counter by `(slug,id)`, SessionStart line, F20 container close | `.githooks/commit-msg:40` runs `piles.py check --msg-file` (doors readable there); forge-check `:84` `check --base`, `fetch-depth: 0` (:45) so E16's shallow-clone case does not arise in CI | **the brake fires on the wrong road — R3** |
| B3 | §2.2 row-by-row to the owner's list; 5.5 red-CI; keys reduced; F18/F19 to the owner | §2.2 rows 1-7 vs the owner's section (spec :974-986): one-to-one; 5.5 quotes PROJECT «Как принимается» п. 2 clause | closed (K5 below: F18 is answerable from the files) |
| B4 | E20 cutover by pickaxe; (в) mask; E9 identity | `_frozen_lines` :1644-1677: header row and node-table rows compared cell by cell, only the `Статус` column masked, «Ход»/«Остатки» skipped — dropping two more named columns is a local change, as stated | closed |
| B5 | §5.14 instance (OWNER key, 5 K-PTR rows, RETIRED list); class → §8 | `tools/tests/test_role_carriers_one_owner.py` :1-30 (K-OWN/K-PTR, scans all tracked text files minus EXCLUDED), :107 (`k in t` substring) | instance closed; §8 judged below (R4-R6) |

N spot-checks (three): **N1** `plans/builder-rules.md:10` is п. 1 «File ownership» — confirmed. **N2** WEEKLY `перенос:` at
:1026 and :1095 (check 39) — confirmed (grep). **N7** `docs/SIBLING_MAP.md:655-661` today names CURRENT_CONTEXT.md's "Lead
Queue" section, not `lead-queue.md`; P16 describes what the architect-tier spec will make of it — consistent, but P16's
wording ««Lead Queue» → `lead-queue.md`» should say "(after architect-tier stream F)" (F-n, trivial).

### R1 (BLOCKER) — the B1 gate has a sanctioned bypass: the hand edit of the Статус cell

`piles.py:3225` `HAND_EDIT = "edit the cell by hand (a taken batch allows it: (в) masks every Статус cell)"` is the door the
status writer itself names; in an untaken batch nothing is frozen at all. (д) `_node_reds` (:1846) checks only that the cell
starts with a known word; the evidence rule (`--hash`/`--task`) lives only in `_status_evidence` (:3254-3263; grep of
`принято` over piles.py shows no write-time check of a cell that moved to `принято`). So `wave.py merge <branch> --task t-N`
WITHOUT `--node`, then a hand edit `| … | принято: abc1234 |` commits with no verdict, no `verdict: none` line, nothing for
calibration (iii) to count. The spec's own guarantee (§2.3 "no node is accepted … unless someone says why in the record")
does not hold, and it is two roads for one action (P31): the gated `status` road and the ungated hand road.
Expected fix (§2.3 part 2, §4 (д) row, A2): move the judgment to the one place both roads pass — (д) at commit-msg: a node
row whose `Статус` first word becomes `принято` against the base requires a message line `verdict: <path>` or
`verdict: none -- <why>` (the same line wave/`status` already print), and the `чужой-код`-inside-`Пишет в` join runs there
on the named file; `status --verdict` stays as the convenient writer of that line. Edge to state: a range in CI reads the
line through `range_messages` (:2330), like `piles-skip:`.

### R2 (BLOCKER) — A2 + C create a circular import between `piles.py` and `critic_verdict_check.py`

§2.3 part 1: `critic_verdict_check` reads `remark_dispositions` "through `piles.node_vocab`, the one reader"; part 2:
`piles._verdict_problem` "extracts the verdict through `critic_verdict_check.check_text`". Scenario: `python -B
tools/piles.py status … --verdict r.md` runs piles as `__main__`; `import critic_verdict_check` executes its top, which
does `from piles import node_vocab` → a SECOND copy of the 3482-line `piles.py` loads as module `piles`, whose top again
imports `critic_verdict_check` — now partially initialised (stopped before `check_text` is defined) → `ImportError` (with a
`from … import` form) or a half module (with a plain import used at call time, fragile by order). It also breaks the
checker's stated design: `critic_verdict_check.py` is stdlib-only by intent ("a shared module across hooks/tools is
deliberately not introduced", its stdin helper comment). Expected fix: the vocabulary reader lives in a small leaf module
(e.g. `tools/piles_vocab.py`, `node_vocab()` only, stdlib only) imported by `piles.py` (re-exported), `collect_intake.py`
and `critic_verdict_check.py`; name it in A1's owns. Also after A2 `critic_verdict_check.py` (and the leaf) are imported by
a mechanism file — add both to `MECHANISM_PREFIXES` with `piles-vocab.json` in H (the list keeps "live wiring closure"
entries such as `md_table.py`, `gitcmd.py`); P20's "NOT a mechanism path" for it becomes stale at A2.

### R3 (BLOCKER) — the flow brake reds the road PROJECT п. 2 prescribes for every finding

§2.4 gate: "for every batch file not «закрыта» that gains a NEW node row … when `opened > closed` for that batch over the
window INCLUDING this commit → red unless `приток:`". An untaken batch closes nothing by design (nodes are accepted after
`take`), so for every untaken intake batch `closed = 0` and the first added row makes `opened ≥ 1 > 0`: every finding
filed the prescribed way (5.1: "тем же ходом … получает УЗЕЛ … в НЕвзятой пачке"), every `collect_intake` row (B), and every
M1/E-k migration commit (~152 rows `Откуда: миграция`) goes red and needs `приток:`. The informed pass becomes the road
(FR-4 inverted, P15 friction), and its count in calibration (ii) is noise. Expected fix: judge only batches that are being
WORKED — `closed > 0` in the window, or a header in FROZEN (taken) — i.e. the forge/7 case and the taken case; exempt rows
`Откуда: миграция` explicitly; state the edge "untaken batch that only receives intake → not judged, printed in summary".
Re-check F13 against this scope.

---

## (2) §8 — keys K1-K6

### K1 — can a service file still contradict a main file after K lands? Remaining roads

| road | open after K? | named in the spec? |
|---|---|---|
| a. edit an EXISTING unmarked block in place (count unchanged) into a restatement that contradicts | open: the census counts blocks, not their content; the baseline starts at today's count (§8.5), grandfathering every existing paraphrase | partly («semantic drift no code sees», §8.6 sample of 5) — the in-place road itself is not named |
| b. **`see:` laundering**: unit (a) exempts any block that "carries a `see:` marker" — a paragraph restating a rule plus one `see:` line leaves the census; K2's "turned into a pointer" can be done by adding a marker only | open | **not named** — F-b |
| c. re-stamp without reading (`stamp` is one command) | open by design (the re-stamper judges) | named as the owner of the meaning; no detector — F-c |
| d. a main rule outside `main` (`CLAUDE.md, PROJECT.md, docs/TESTING.md, plans/builder-rules.md`): `DECISIONS.md`, `docs/SIBLING_MAP.md`, `PROCESS/*.md`, `BOOT.md`, `docs/RUNBOOK.md`, `design/factory-rules.md`, `design/architecture.md`, `delegation.config.yaml`; `docs/TEAMWORK.md` conditional | open; service files already point at such homes (`boot-diet/SKILL.md:119` → BOOT.md, `next-task/SKILL.md:66` → PROCESS/WEEKLY…, grep `see [a-z./_-]+\.md`) | only TEAMWORK — F-d |
| e. a service file outside the globs: `PROCESS/*.md` (check 39 is THE live drift instance of t-920 N2), `docs/SIBLING_MAP.md`, `plans/piles/_template/*` (5.13 edits its leftover comment), `CURRENT_CONTEXT.md`, refusal texts and dispatch templates in `tools/*.py` (the `service` list has a placeholder; the census unit is defined for markdown only) | open | package twin named; the rest not — folded into R5 |
| f. `plans/builder-rules.md` is MAIN and also restates CLAUDE.md (7b vs rule 4, 1 vs rule 11) — as main it is never counted or stamped | open | not named — F-d |

### K2 — feasibility and cost

**Section identity — R6 (BLOCKER).** §8.2's grammar: an anchor is "a literal line prefix that occurs EXACTLY ONCE as the
start of a line"; the section ends at the next heading of same/higher level or, for a list item, the next sibling item.
(i) The first instance fails it: the home «**Остатков в идеале нет вовсе**» stands MID-LINE — `PROJECT.md:333` is
`   доказательств не должно. **Остатков в идеале нет вовсе**: минорные` — and 5.3 replaces the span from that phrase, so
«**Остатков нет по правилу**» stays mid-line unless 5.3 says "on a new line"; `see: PROJECT.md#**Остатков нет по правилу**`
(§8.2's own example) is then E31 red on day one, while §5.14's K-PTR substring row (:107 `k in t`) passes — the two checks
disagree on the same pointer. (ii) Leading whitespace is not addressed (item 9's lines are indented 3 spaces). (iii) A bold
lead-in is neither a heading nor a list item: its section end is undefined (read literally it runs to the next heading —
items 10-13 of «Командная работа» — so every edit there reds the leftover stamps). (iv) `11a.`/`4a.` openers: sibling or
not is unstated (rule 11's section would include 11a). (v) boot-by-topic S1 inserts headings above CLAUDE.md rules (its
rows C1-C12 "heading per F19", sub-headings «### Rule 11 · …») and S3-2 inserts `### <n>. <bold title>` lines in
builder-rules — each new heading ENDS the list-item section above it, so stamps made before S1 change meaning after it.
Expected fix: define the grammar for heading / list item / bold lead-in (end = the next bold lead-in at line start, the
next sibling item, or a heading, whichever first), leading whitespace stripped, `\d+[a-z]?\.` as an item opener; 5.3 puts
the home on its own line; K lands after boot-by-topic S1 (§7.3 row).

**Cost per main-file edit — measured.** Commits in the last 7 days: `git -C $R log --since=2026-11-10 --format=%h -- CLAUDE.md
| wc -l` → **11**; same for PROJECT.md → **10**. Three CLAUDE.md commits, sections touched (old-side hunk lines mapped to
`#`-headings and top-level numbered items; script `sect.py` in the scratchpad, `git diff -U0 c^ c -- CLAUDE.md`):
`9f486c3d` 2 hunks → 1 heading / 2 sections (Command hygiene, item 4); `7b3f1d80` 8 hunks, +27 lines → 3 headings /
4 sections (hygiene 5, Routing log, rules 11 and 12); `63bbd5e2` 1 hunk → 1 section (rule 12). Service files referencing
those topics today (grep -liE over the 18 of P39): rule 11/DoD 7, command hygiene 7, journal_write/Routing log 3. So: with
POINTERS, 0 reds per commit (content edits never red a pointer); with STAMPED blocks, 1-4 affected sections per commit and an
upper bound of ~17 stamps for a commit like `7b3f1d80` if every reference were a carried block (estimate, not measured on
stamps — none exist). Conclusion: feasible only if K2 makes the pointer the overwhelming form and stamps rare — say so as
K2's target (F-e).

**Who pays, and is the door usable (FR-1/FR-2, P15)?** The committer of the main file. Not usable as written:
- **R4 (BLOCKER)** — `rule_stamps.py check` is placed in `.githooks/pre-commit` (§8.3), but its informed passes
  `stamp-skip:` and `rule-census-raise:` are COMMIT-MESSAGE lines. A pre-commit hook gets no message; the repo says so at
  `.githooks/commit-msg:39` ("piles-skip … this is why it runs here and not in pre-commit"). Both doors are unreachable on the
  local path. Expected fix: run it in commit-msg with `--msg-file "$1"` (as `piles.py check`), and in forge-check read the
  range's messages (as `range_messages`), or a commit that used the door locally stays red in CI.
- PROJECT.md is not a mechanism path, `.claude/agents/*` and `.claude/skills/*` are (`mechanism_gate.py` list). A builder
  editing PROJECT.md (stream D does) is refused for a stale stamp in `critic.md` — a file outside its `owns` that it may not
  commit. The refusal text must name the second door ("hand the re-stamp to the Lead: `stamp-skip: <file>:<line> -- handed to
  Lead`") (F-f).
- Every edit of `.claude/agents/critic.md` (and `scout.md`) owes the role exam BEFORE the commit (critic.md rule 10,
  scout.md :59). D's 5.11 and each K2 commit on these files carry that cost; neither DoD names it (F-f).

### K3 — architecture and principles

- AR-29 / P27 / FR-12: the hash, anchor resolution and block count are data; no part of §8 reads wording by a phrase list.
  F21 (b)/(c) (12-word verbatim spans) is shape too. §5.14's RETIRED phrase list is a list of OUR old rule texts, the same
  class as the existing K-OWN keys — acceptable, not a role's wording.
- **R5 (BLOCKER) — P31 / AR-15: §8 adds a second pointer grammar and a second checker where a survivor and a decided
  extension already exist.** Three pointer forms would coexist: (1) K-PTR rows with a prose pointer (§5.14: literal
  «PROJECT.md «Командная работа» п. 9», substring anchor); (2) boot-by-topic's `rule: <file> § <section>` /
  `правило: <файл> § <раздел>` (its K3, §4.3 resolver contract: heading text or `<x>.`/`### <x>`/`**<x>.**`), whose checker is
  node FG7-52 — "скан `test_role_carriers_one_owner.py` (K-PTR) расширяется … отдельного `tools/pointer_lint.py` нет (A1; P31,
  AR-15)" (boot-by-topic spec :690); (3) §8's `see: <file>#<anchor>` with a line-prefix anchor in a NEW tool
  `rule_stamps.py`. Different resolution rules on the same pointer (R6 (i) is the first collision). Also the scan set
  diverges: the survivor scans every tracked text file minus EXCLUDED (test :8-10, :24-27); §8's `service` is three globs —
  narrower, and if K-OWN moves onto `rule_sources.json` scopes it SHRINKS the axis-31 scan. Expected fix: ONE pointer form
  (adopt boot-by-topic's `rule:`/`правило:` grammar, or amend that spec to `see:` — the Lead picks, one road) and ONE
  resolver; K extends the survivor (the axis-31 test + FG7-52's resolver) with the stamp and census parts instead of a
  parallel `section_bounds`; `service` = the survivor's scan set minus `main` (one definition), K-OWN scope unchanged;
  merge K with FG7-52 or order FG7-52 → K with K reusing its resolver. Generated blocks: say K builds no generator; a
  projection block reuses `factory_rules_index.py`'s road by its own node.
- Clone ratchet (`dup_ratchet.py`): code scopes only (its SCOPES) — no overlap with F21 (a); (b)/(c) would be a prose
  sibling of `dup_report` — a reason more for (a).

### K4 — collisions with work in flight

- **boot-by-topic** (S1 pending: CLAUDE.md headings + TOC; S2: imports, R2; S3-2 builder-rules headings; FG7-52 pointer
  checker). §7.3 has no row ordering K/K2 against it. Needed rows: `CLAUDE.md`/`PROJECT.md`/`plans/builder-rules.md` as K's
  MAIN files: boot-by-topic S1/S2/S3 → K (R6 (v)); `test_role_carriers_one_owner.py`: D → FG7-52 → K, or K absorbs FG7-52
  (R5). The `main` row for `docs/TEAMWORK.md` (§8.1) is handled.
- **architect-tier** (B-F being built; L edits CLAUDE.md, role files, queue files): it DELETES `.claude/skills/onboarding/`
  and `next-task/` (its D6, spec :616) — by my approximation ~73 of ~353 blocks of the 18 service files (approximation script
  `census.py`: paragraphs/list items, fences and headings excluded; NOT the spec's unit) — and L rewrites role-file text.
  A census baseline written before those land gets orphan rows and rises/falls by others' commits. Fix: K's baseline is
  written after architect-tier D6 and L, and §8.4 states the rows for a NEW service file (no row → baseline 0? or written
  in the adding commit) and a DELETED/renamed one (row dropped by the same commit, never red) (F-g).
- **F7 (a) after stream L** — sound for the FILE retirement (L edits the queue files; one writer at a time). Not sound for
  the readers: architect streams C (`session_context.py` architect-queue count), A5 (`_tier_queue_note`) and F (check 49 (b))
  are being built now to read the queue files; F7 (a) later rewrites all three to read nodes. Either amend the architect-tier
  spec now so C/A5/F read through `piles` from the start, or state the rework (three readers built twice) in F7 — a line for
  `docs/tasks/specs/20261116-architect-tier-spec.md` (Lead amendment), not this spec only (F-h).
- **F12** — the order (boot-by-topic first, D edits fragments in their homes) is sound. Its recommendation "the home stays in
  PROJECT.md although a gate now refuses part of 9d" overrides the owner's criterion of boot-by-topic («what code holds may
  leave», her «да» 17.11.2026, boot-by-topic §5.1) for one fragment — an exception to an owner's rule is hers (P31). Either
  apply her criterion clause by clause (the gate-held clauses — `чужой-код` inside `Пишет в`, `приток:` — move with 9a to
  TEAMWORK; the discipline clauses — on-topic word, scope cut, red CI — stay) or put the exception to her (F-i).

### K5 — forks: who decides

- In §8 the Lead decides the `main` list ("the Lead's list"). Which files are «основные» is the meaning of her sentence
  (11a: interpreting intent); the list leaves out homes her own process treats as main (road d). Put ONE question to her
  with the recommendation (main = boot files + TESTING + TEAMWORK + design/factory-rules.md + architecture.md + SIBLING_MAP +
  PROCESS/*.md; executable on the recommendation until she answers, PROJECT п. 11) (F-d).
- F21 (census unit), F13, F17, F20 — technical, Lead's — correctly labelled.
- Returned to the owner but answerable from the files: **F18** «занятый файл» — PROJECT «Командная работа» п. 3 already rules
  it (queue line `очередь: A → B` or disjoint function lists, D-0048, "поздний узел сливает main … решает конфликт сам"), and
  her «делать сразу» for own-code remarks closes (b); the Lead can decide (a) citing both with a «решила сама» line. **F8** —
  her word is "the fate is decided after it is empty"; it should leave Phase 0's list (asking now contradicts her timing).
  **F16** — CLAUDE.md rule 4 already fixes half (a canon failure after convergence is `defect_found`, reopening forbidden);
  only "node or not" is hers — narrow the question. F1, F14, F19 — legitimately hers.

### K6 — edges and the four questions for K/K2

Named well: E30-E36 (stale, 0/2+ anchors, daily edits, missing main file, block edited without stamp, unreadable base),
CRLF/trailing spaces, block12 for edits inside the block, error directions, owners.
Silent (F-j): a service file with no baseline row / a deleted service file (above); a `see:` naming a file NOT in `main`
(red, ignored, or allowed?); a `source:` without its `<!-- /source -->`, two stamps nested or overlapping, a marker inside a
code fence (counted? ignored?); a file in both `main` and `service` (builder-rules); `--staged` vs working tree under
partial staging; leading whitespace and mid-line anchors (R6); the stamp of a section that is itself a generated block.
Four questions: (a) cost — now measured above, write it into §8.3 E33; (b) axes — left to the committer's enumeration,
legal; (c) detector — check 33 item (v); add the cheap data detector for road c: `check` prints, and calibration counts, a
re-stamp in which `source12` moved and `block12` did not (a re-stamp with the carried text untouched) (F-c); (d) what
stops skipping — pre-commit placement must become commit-msg (R4); forge-check catches `--no-verify`.

---

## Standing lines (plan gate)

- **DUPLICATION AND CONSISTENCY**: R5 (three pointer forms, two resolvers, two scan sets); R1 (two roads to `принято`).
  Grepped: `rule:|правило:|K-PTR|pointer_lint` in the boot-by-topic spec (:56, :71, :408-418, :690); POINTERS/EXCLUDED in the
  axis-31 test; `dup_ratchet.py` SCOPES (code only).
- **CODE QUALITY**: no code yet; R2 is a design-level import cycle; `rule_stamps.py` scope shrinks once R5 is applied.
- **ONE ROAD (P31)**: R1, R5; F12's exception to the owner's criterion (F-i).
- **TESTS**: rows in existing files, E15 batteries per input kind, negative control per red — consistent with
  `docs/TESTING.md`; K's rows in the axis-31 test (no new file) — right; after R5 the stamp/census rows join FG7-52's.

## Fixes (non-blocking, in this spec unless a path is named)

- F-a §2.3 part 2: refuse `--verdict` on a verdict whose `verdict` is `blocker` (pure data; door `--owner-word`/`--no-verdict`).
- F-b §8.4 unit (a): a block counts as marked by `see:` only when its prose besides the marker is at most one sentence (or
  ≤ N words, a shape limit); otherwise it is counted; state it as the anti-laundering edge.
- F-c §8.6 detector: count re-stamps with `block12` unchanged while `source12` moved; calibration item (v) reads them.
- F-d §8.1: the `main` list as one owner question with a recommendation; `builder-rules` dual role stated (main for its
  own rules, service where it restates CLAUDE.md — or the restatements become pointers in K2).
- F-e §8.5: K2's target stated — pointers by default, stamps only where the reader cannot load the main file (names the
  cases: a dispatch template, a hook refusal); the measured cost above in E33.
- F-f §8.3 refusal text: second door for a refused party who cannot touch the service file; D's and K2's DoD name the
  critic/scout exam run for `critic.md`/`scout.md` edits (critic.md rule 10).
- F-g §8.4: baseline written after architect-tier D6/L; rows for a new / deleted / renamed service file; the three
  one-off task briefs (`pre-release-0.9-*`, `test-diet-*`) — service files or history? (archive them, or exclude).
- F-h F7: state the rework of architect streams C/A5/F, or amend `docs/tasks/specs/20261116-architect-tier-spec.md` now.
- F-i F12: follow the owner's boot-by-topic criterion per clause, or ask her for the exception.
- F-j §8.3 edges listed under K6.
- F-k Phase 0: drop F8 (her timing), decide F18 by PROJECT п. 3 + «делать сразу», narrow F16.
- F-l H: `critic_verdict_check.py` and the vocab leaf module into `MECHANISM_PREFIXES` (R2).
- F-m §7.3: rows K ↔ boot-by-topic (S1/S2/S3-2, FG7-52) and K ↔ architect-tier (D6, L).
- F-n P16 wording: SIBLING_MAP's «Lead Queue» names CURRENT_CONTEXT.md today; `lead-queue.md` after architect stream F.

## Class completeness

Class of §8: "a service text drifts from its main rule". Walked: the forms (pointer / stamp / free) — laundering via `see:`
(F-b) and in-place edit (named partly); the scope (main list, service set) against the axis-31 scan set and the homes service
files already cite (R5, F-d); the anchor grammar against the real first instance and boot-by-topic's coming headings (R6);
the road (pre-commit vs commit-msg, CI range messages — R4); the doors for the refused party (F-f). Class of B1 ("a node is
accepted while an own-code remark is deferrable"): walked the writers of a node's `принято` — `status`, `wave --node`, the
hand edit (R1); the verdict values (F-a). Class of B2 (a growing batch): walked the adders of rows — intake, migration, the
Lead, collect_intake (R3). SIBLING_MAP axes not re-walked beyond the spec's 1/4/18/31/34 (the committer's enumeration).

## Trail

Read: the spec whole (1-1013); the t-920 review whole; boot-by-topic spec lines 1-75 by grep, 155-183, 400-425, 545-552,
:690 (FG7-52 row); architect-tier spec by grep (stream L, D6 :616, streams C/A5/F); `tools/piles.py` 1644-1680, 3225,
3254-3365 + grep of defs; `tools/wave.py` 1-30, 240-280 + defs; `tools/critic_verdict_check.py` 1-50, 160-196 + defs;
`tools/critic_verdict.schema.json` (python load); `.githooks/pre-commit` 1-80; `.githooks/commit-msg` grep (:32, :37, :39-40);
`.github/workflows/forge-check.yml` 40-90; `tools/tests/test_role_carriers_one_owner.py` 1-30 + defs; `tools/mechanism_gate.py`
205-290; `tools/dup_ratchet.py` 1-25; `PROJECT.md:326, 333`; `plans/builder-rules.md:10`; WEEKLY grep `перенос:`;
`docs/SIBLING_MAP.md:655-661`; `.claude/agents/*.md` grep `exam`.
Reruns / measurements: CLAUDE.md and PROJECT.md commit counts since 2026-11-10 (11, 10); `sect.py` on 9f486c3d, 7b3f1d80,
63bbd5e2; grep of topic references over the 18 service files (7/7/3); `census.py` approximation (353 blocks, onboarding 62,
next-task 11); grep `see: ` in service files → 0, positive control `see ` → 19 lines and `see <file>.md` hits.
Needed beyond the manifest: the code and config files listed above (read-only).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "R1 s2.3/s4: the B1 gate sits only in status --set принято, but HAND_EDIT (piles.py:3225) lets the Статус cell be written принято by hand with no verdict and no record; move the verdict-line requirement and the чужой-код join into (д) at commit-msg so both roads meet one check",
    "R2 s2.3: critic_verdict_check imports piles.node_vocab while piles imports critic_verdict_check.check_text - a circular import (piles run as __main__ loads a second piles that sees a half-initialised checker) and a break of the checker's stdlib-only design; put node_vocab in a leaf module imported by all three",
    "R3 s2.4: the flow brake reds every intake into an untaken batch (closed is 0 by design), every collect_intake row and every M1 migration commit; judge only batches being worked (closed>0 in window or taken) and exempt миграция",
    "R4 s8.3: rule_stamps check is placed in pre-commit but its doors stamp-skip and rule-census-raise are commit-message lines a pre-commit hook cannot read (commit-msg:39 says so); run it in commit-msg with --msg-file and read range messages in forge-check",
    "R5 s8/K3: a third pointer grammar (see: file#anchor) and a new resolver rule_stamps.py beside the K-PTR rows and boot-by-topic's rule:/правило: form whose checker FG7-52 extends the axis-31 test (no pointer_lint, P31/AR-15); one pointer form, one resolver, service = the survivor's scan set minus main",
    "R6 s8.2: the anchor grammar fails its own first instance (the home phrase is mid-line at PROJECT.md:333, indented), leaves the end of a bold lead-in section undefined and the 11a/4a openers unstated, and boot-by-topic S1/S3-2 headings will change section bounds; define the grammar, put the home on its own line, land K after S1"
  ],
  "fixes": [
    "F-a refuse --verdict on a blocker verdict",
    "F-b see: marks a block only when its prose besides the marker is one sentence; else counted",
    "F-c count re-stamps where source12 moved and block12 did not; calibration item v",
    "F-d main list as one owner question with a recommendation; builder-rules dual role stated",
    "F-e K2 target: pointers by default, stamps only where the main file cannot be loaded; measured cost into E33",
    "F-f second door in the stale-stamp refusal for a party that cannot touch the service file; critic and scout exam runs in D and K2 DoD",
    "F-g census baseline after architect-tier D6 and L; rows for new, deleted, renamed service files; decide the one-off briefs",
    "F-h F7: state the rework of architect streams C, A5, F or amend the architect-tier spec now",
    "F-i F12: apply the owner's boot-by-topic criterion per clause or ask her for the exception",
    "F-j silent s8 edges: see: to a non-main file, unclosed or nested stamps, markers in fences, file in main and service, partial staging, generated sections",
    "F-k Phase 0: drop F8, decide F18 from PROJECT p.3 and the owner's делать сразу, narrow F16 using CLAUDE.md rule 4",
    "F-l H: critic_verdict_check.py and the vocab leaf into MECHANISM_PREFIXES",
    "F-m s7.3 order rows K vs boot-by-topic S1/S2/S3-2/FG7-52 and K vs architect-tier D6/L",
    "F-n P16 wording on SIBLING_MAP Lead Queue today vs after architect stream F"
  ],
  "class_completeness": "s8 class (service text drifts from its main rule): walked forms (see: laundering F-b, in-place edit partly named), scope (main list and service set vs the axis-31 scan set, R5, F-d), anchor grammar vs the real first instance and boot-by-topic headings (R6), hook placement and CI range messages (R4), doors for the refused party (F-f). B1 class: all writers of a node принято - status, wave --node, hand edit (R1), verdict values (F-a). B2 class: all adders of rows - intake, migration, Lead, collect_intake (R3). SIBLING_MAP axes beyond the spec's 1/4/18/31/34 left to the committer's rule-10 enumeration.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-everything-in-piles-spec.md",
      "docs/tasks/specs/reviews/t-920-everything-in-piles-plan.md",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md",
      "docs/tasks/specs/20261116-architect-tier-spec.md",
      "tools/piles.py",
      "tools/wave.py",
      "tools/critic_verdict_check.py",
      "tools/critic_verdict.schema.json",
      ".githooks/pre-commit",
      ".githooks/commit-msg",
      ".github/workflows/forge-check.yml",
      "tools/tests/test_role_carriers_one_owner.py",
      "tools/mechanism_gate.py",
      "tools/dup_ratchet.py",
      "PROJECT.md",
      "plans/builder-rules.md",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "docs/SIBLING_MAP.md",
      ".claude/agents/critic.md"
    ],
    "reruns": [
      {"command": "git log --since=2026-11-10 --format=%h -- CLAUDE.md | wc -l ; same for PROJECT.md", "result": "11 and 10 commits"},
      {"command": "sect.py: git diff -U0 c^ c -- CLAUDE.md mapped to headings and numbered items for 9f486c3d 7b3f1d80 63bbd5e2", "result": "1 heading/2 sections; 3 headings/4 sections; 1 heading/1 section"},
      {"command": "grep -liE topic references over the 18 service files", "result": "rule 11 or DoD 7 files; command hygiene 7; Routing log or journal_write 3"},
      {"command": "census.py approximation of unmarked blocks in the 18 service files", "result": "353 blocks; onboarding 62, next-task 11 (deleted by architect-tier D6)"},
      {"command": "python json load of tools/critic_verdict.schema.json", "result": "required verdict blockers class_completeness trail; additionalProperties true"},
      {"command": "grep -n Остатков в идеале PROJECT.md", "result": "line 333, mid-line, indented 3 spaces"},
      {"command": "grep -i critic_verdict_check over tools .githooks .github .claude PROCESS", "result": "only the tool, its test, docs, settings allow line, critic.md - no execution path"}
    ]
  }
}
```
