# TD-5 critic-on-plan (t-2257) — spec `docs/tasks/specs/td-5-role-rules-register.md`

**Verdict: ACCEPT WITH FIXES — 3 blocking findings (B1–B3), 7 non-blocking (R1–R7).**
The design (one data register, one reader, an anchor that must stand exactly once, data-only check) is sound and I checked it
holds today: all 12 anchors written out in §4.2/§4.3 stand exactly once in their carriers. Three things must be fixed before a
builder gets it. (1) The matcher strips HTML comments, but the requirements-register template keeps its whole guidance inside
comments. (2) Several pinned rules are left out or wrongly sorted into a "dropped" kind. (3) §4.4 is a set of directions, not
rows: a Sonnet builder would have to guess. Accepting the spec, and deciding the fixes, is the Lead's call.

All line numbers refer to the worktree `D:/ws1/wt-test-diet` at HEAD 4d3e6b7bb. Package paths are relative to
`ai-packages/qa-factory/`.

## Blocking

### B1 — Stripping HTML comments (§3.2, E-12) turns every template row red. The template's guidance to the role IS its comments.
- Evidence: I ran the spec's matcher (strip `<!--.*?-->` non-greedy, fold whitespace, casefold) on the keys of
  `test_detection_role_texts.py:33-43`. All 9 keys of `references/templates/requirements-register.md` count **0 outside
  comments and 1 with comments**: "never a reading `from: code` that drops the norm", "the norms hold (default)…",
  "`invariant:`/`bug:candidate-defect`…", "departs from it is an expected red…", "IS a requirement: the norm is its oracle",
  "one `open_questions` row per fork…", "unknown: <why>", "ONE confirmation question", "none derived, no such question".
  The file's guidance blocks run as comments, e.g. lines 29-66 (`<!-- A \`|\` inside a cell … -->`), with "ONE
  confirmation question" on line 62.
- Nothing strips comments before delivery. `scripts/brief_pack.py:93` hands the role the template path, and the role reads
  the file raw. Searching the non-test `scripts/*.py` for comment stripping finds only `branch_accounting.py:65` (its own
  parse) and `validate_artifacts.py:1884` (the factory-summary block). So "a commented-out rule is a removed rule" (E-12,
  §3.3 "Only in a comment") is false for templates. §4.4 still asks for rows on "template t-1692 B1-B3, F5 (b) and its edge".
- Failure scenario: TD-5.1 adds those rows → `role_rules.py --check` reports 8 "only inside an HTML comment" findings →
  DoD "`--check` clean" can't be met. The builder either drops the rows (8 rules lost: the template twin of K1-5/K1-6, B1,
  B2 ×2, B3, F5 (b) and its edge) or edits the template (a non-goal).
- Fix in the spec: (a) §3.2/§2.4: comments are NOT stripped in `references/templates/*`, because a template's comments are
  its delivered guidance. Simplest alternative: strip only the marker comments the package itself writes (`<!-- kind: … -->`,
  `<!-- roles: … -->`, `<!-- gen… -->`, `<!-- /gen -->`) and count every other comment. (b) Narrow E-12 to the files where
  stripping applies, and add an edge row "anchor inside a template comment → counts". (c) §7.1 non-goals/DoD: say what the
  builder does with a key that does not hold today. Recommended: the row is NOT added, it goes under `red before:` with
  the old pin's output, and the Lead decides. Today "goes to `red before:`, not repaired" (§7.1 non-goals) contradicts DoD 1
  ("rows of §4.4") and the shipped case `findings(PLUGIN_ROOT) == []` (§3.5).

### B2 — Completeness: rules a pin guards today that the spec leaves unguarded or does not account for (the owner's word 10.11.2026)
1. **`test_mixed_then_texts.py` K3a** (`:46`, automator, "move independent Thens before the red one"; present, count 1).
   It is neither in §4.4's "become rows" list ("K1a, K1b, K2, K3b, K3-ref?, K4, …") nor in its dropped list. Worse, §4.1
   and §8 F8 call the owner-word sub-keys "K2a/K2b/K3a", and the file's docstring (`:11`) does too, while the code names
   that sub-key `K3a-sub` (`:71`). A builder reading "drop K3a (F8)" deletes the guard of a live duty: the owner's 28.10
   rule, HF5-16. Fix: add K3a to the rows of §4.4, and rename every F8 mention to "K3a-sub".
2. **`test_blocked_by_env_texts.py` (8): the three handoff lines** (`:61`, `:112-118`). §4.4 drops them as "form of the
   handoff". They are critic duties in a delivered carrier (`handoffs/s5-automator-to-critic.yaml:114-117`): "the critic
   checks the list is complete…", and on `remedy`, "the critic checks it names an exact fix and carries no credential
   value", which is a safety duty. The old pin is their only guard. They can become rows: §3.2 searches YAML comments, and
   "the list is complete" and "carries no credential value" each count 1. Fix: rows for `instance_ids` and `remedy` (the
   `detail` line restates the slice key, so merge it).
3. **`test_blocked_by_env_texts.py` (7): the charter pointer.** `:104-107` (`count("A blocked row that ran red") != 1` →
   finding, so 0 is red too) is the only guard of the critic's pointer at `agents/qa-code-critic.md:37`. §4.4 drops it as
   "pointer count = 1 (form / F3)". Yet for `test_recommended_rule` the spec keeps the conductor's pointer as a twin carrier
   (§4.4 last row). Same class, opposite verdict. The anchor counts exactly 1 in the critic file. Fix: a twin row, rubric
   heading (`references/code-review-rubric.md:83`) + critic pointer.
4. **`test_scout_conflict_rule.py:35`, "s1.md keeps the halt digest"** (the halt stays for an UNRESOLVED conflict). §4.4
   neither keeps nor drops it. The anchor `it is no halt` guards only the settled half of `skills/qa-story/phases/s1.md:377`.
   No product script reads "requirement/code conflict": `git grep -l -i "requirement/code conflict" -- scripts/*.py hooks
   references` finds only tests and `references/halts.md`; the same-shape control on `unresolved_facts` finds
   `context_bundle.py` and `source_inventory.py`. Fix: a row in s1, anchor "Halt only on an unresolved conflict" (count 1).
5. **`test_case_role_twins.py` K14-phase** (`:66`). §4.4 drops it as a "single token". But
   `skills/qa-story/phases/s7.md:239` states the rule ("A row with `field_absent` is judged by its `shape_ref` instead"),
   the s7 twin of K14 (analyst). §4.1's own single-identifier row says "if none does, widen … and make it a row". Fix: K14
   becomes a twin row (analyst + s7), with s7 anchor "judged by its `shape_ref`" (count 1). Also remove the §4.1↔§4.4
   contradiction for K6 `oracle_field_absent`: no product script reads it (`git grep -l oracle_field_absent -- scripts/*.py
   hooks` → only the pin; the same shape for `field_absent` finds `manifest_from_tests.py`). Dropping K6 is fine only
   because K5 holds the same rule, so the spec should say that, not "single token".

### B3 — Buildability: §4.4 makes the builder decide (PROJECT.md «Командная работа» p. 11: a node is written for a weaker model)
§7.1 DoD 1 demands "the rows of §4.4", but §4.4 holds directions, not rows. These places force a guess:
- "K3-ref?" and "dropped unless the builder finds it is the only carrier" (mixed_then);
- "a second scout row if a unique 2-6 words exist" (scout). They do exist: "with both quotes" counts 1;
- "merge B-K2b/B-K2c/B-K9b/N3c/N3d/E21b of s7 by rule" (s7_control). These are at least four different rules (no repair
  for `ASSERT_STRICTER`; never `CASE_DEFECT` …; never skips the control experiment; evidence under `evidence/`). Read as
  "one row", three lose their guard;
- "widen `cannot-tell`", "widen `manual-evidence`", "`t_after + tolerance` widened if fewer". Measured: "cannot tell"
  counts 2 in both case charters and "from the requirements" counts 3 in the designer, so K1 needs new words in both;
- non-unique keys the builder must re-word: s4 "start S5 in this window unless …" ×2, s8 "go on to S9 in this window" ×2,
  s7 "under `evidence/`" ×2 (all outside comments);
- every row's `rule` text and `source`. §5.2 makes `rule` the critic's only yardstick when an anchor moves, so writing it
  is judgment, not transcription;
- the B1 conflict (a key that doesn't hold → row or no row).
Fix: the designer, or the Lead, completes §4.4 as a row table in the §4.3 form (id, rule, source, carriers + counted
anchor) for all ten files. Most counts are already in this review's trail. The builder then copies rows verbatim, runs
`--check`, and anything that doesn't count 1 goes under `doubt:`. That also makes DoD 1 checkable by the critic of TD-5.1.

## Non-blocking

- **R1 — stale text.** §2.1 says TESTING.md, test-diet.md and builder-rules 7d "name `references/role-rules.json` today".
  Commit cac99e83d already moved them: `docs/TESTING.md:70` and `docs/tasks/test-diet.md:22` say `design/role-rules.json`.
  F1–F8 are decided, yet §1.1/§1.2/§2.1/§7.1 still say "fork F2", "if F5-c", "under F1-B …", and the status line says
  "DRAFT … NOT decided". §4.3 cites s7 "line 145" for "Nobody comments out"; it is line 148. Fix: write the decisions in and
  delete the F1-B branches.
- **R2 — F8 reworded on the facts (see Q3).** §8 F8 still says "the Lead keeps the open owner question" and "I did not read
  its status line". Replace with: FA-10 answered 28.10.2026 (HF5-16, `plans/piles/hotfix-12586/batch-5-…md:61`, accepted
  818bba85c); its meaning stands in other words at `skills/qa-story/phases/s7.md:148`; FA-11 took the soft-assert road
  (batch 6, `plans/piles/hotfix-12586/README.md:35`), so K3a-sub is an option nobody took. Drop the flag.
- **R3 — row deletion and register emptying stay code-blind (E-19, E-3).** The code can see this half of E-19 as data, with
  no judgment: an id present in `HEAD:<REG>` and missing from the staged `<REG>` must have a `role-rules: retire <id> --`
  line in the commit message. That is a join, the `architecture_gate.py` pattern, AR-29-clean, and it also catches
  `rows: []`. Proposal only: whether to add it is the Lead's call (promotion after a leak, CLAUDE.md rule 10 (d)). At
  minimum, E-19 should name the commit-msg gate as the possible future detector.
- **R4 — `<why>`/`<reason>` in the §3.3 refusals.** `hooklib.read_json` (`scripts/hooklib.py:694`) returns only `default`,
  with no reason. State how the reader gets one (an `is_file()` / size probe before `read_json`), or drop `<why>` from the
  register-level text.
- **R5 — K-R1-1a partial edit.** `s7.md:255-256` is one sentence ("read first: the case's triage row (…) and the case
  file's Self-probe notes"). The row's single anchor "Self-probe notes" lets someone delete the triage-row half silently,
  the very case the spec gives as the reason R3-2d gets its own row. "the case's triage row" counts 1. Fix: a second row
  (§4.1 item 4 allows only one anchor per carrier per rule), or say why the loss is accepted.
- **R6 — B-K13 (`design/state-exits.md`) is dropped by the carrier-home rule.** That is correct under FR-44: no role reads
  `design/`. Name it in the TD-5.1 "known losses" list next to the F3 losses so the drop is visible.
- **R7 — the driver golden.** `experiments/driver-golden/MANIFEST.json:1394` hashes `scripts/tests/test_blocked_by_env_texts.py`
  (`package_files`, read by `scripts/tests/driver_golden.py:130-132` provenance). It already disagrees with many files (11
  of the 12 pins are not in it), so TD-5.1 breaks nothing new. Mention it so nobody adds it to the cleanup list by mistake.

## Answers

### Q1 — Completeness, per file
"Rules pinned" counts PRESENT keys after the pin's own `X7_3_RETIRED` filter that state a duty or ban (absence, count,
position, cap, eval and negative-control keys are listed separately as intended drops).

| Pin file | Rules pinned (keys) | Rows proposed by the spec | Rules left unguarded / unaccounted |
|---|---|---|---|
| blocked_by_env_texts | 14 KEYS (`:39-59`) + charter pointer (`:104-107`) + 3 handoff critic duties (`:112-118`) | "KEYS rows" (`last_run.reason` token folds into (5)) | **pointer** (B2.3); **handoff `instance_ids`/`remedy` duties** incl. "no credential value" (B2.2). Intended drops: charter absence ×2 (F3) |
| case_role_twins | 19 keys (`:32-68`) | K4→case-focus-twin, K4b, K5, K7, K8, K9, K9b-d, K10, K11, K13, K14 | **K14-phase s7:239 rule** (B2.5). K6/K8b/K12×3 drops OK (K5/K8 hold the rule; `field_absent` read by `manifest_from_tests.py`) |
| case_roles_twin_rules | 3 keys × 2 files (`:17-18`) | case-focus-twin | none ("whole" rightly dropped) |
| critic_lines_hf2 | 7 keys + D14a in 2 slices (`:19-31`) | D13a…D15b, D14a with 3 carriers | none (D13a/D14c/D15b are 7–8 words: trim) |
| detection_role_texts | 24 keys (`:20-59`) | all except K1-9 | **8 template rules** red under comment stripping (B1). Intended drops: 5 ABSENT (F3), K1-9 token |
| gate_continuation_texts | 8 PRESENT (`:35-44`) | all; s4/s8 "never pipe" twin | none (2 keys count 2: re-word, B3). Intended: 7 ABSENT, SKILL_CAP, evals 14/18-20 |
| mixed_then_texts | 15 KEYS + K5 in 2 slices (`:41-64`) | K1a, K1b, K2, K3b, K3-ref?, K4, K5a, K5e, K6, K7 | **K3a** (B2.1). Intended: K5b/c/d tokens, dim-8 safe side (F3, listed), K2a/K2b/K3a-sub (F8) |
| recommended_rule | 5 (`:28-32`) | twin row + 3 sub-rule rows | none. Intended: position after item 6, byte caps, stages.json control |
| red_then_texts | 10 PRESENT after filter (`:32-55`) | 8 rows (§4.3) | K-R1-1a only partially (R5). Intended: K-R3-5 ABSENT, K-R1-5 regex (positive sentence kept) |
| s7_control_experiment_texts | 25 PRESENT after filter (`:48-106,112-114`) | "PRESENT rows", merges unclear | B-K13 (`design/`, by policy, R6); risk of loss through "merge by rule" (B3). Intended: 12 ABSENT, 3 COUNT, 2 positions, RUBRIC_CAP, eval 21 |
| scout_conflict_rule | 4 words × 2 files, s1 halt digest, scout When-to-ask sentence (`:16,35,40-41`) | scout+s1 twin; When-to-ask "if unique" | **s1 halt on unresolved conflict** (B2.4). When-to-ask: anchor exists ("with both quotes" = 1). Intended: ABSENT scout halt line, conflict-passage filter |
| time_fork_rule | 9 keys (`:23-33`) | K1 twin, K2, K3, F2 twin | none (K1 needs new words: counts 2/3, B3). `cannot-tell` is read by `guard_pre_tool.py:2220` |

Dropped keys that were the ONLY guard of a real rule: blocked_by_env pointer count (B2.3) and the handoff `the critic
checks` lines (B2.2). Every other intended drop is either an absence/count/position key whose rule has a positive row, or a
token a script reads.

### Q2 — Anchors (16 sampled; spec matcher: utf-8-sig, `<!--…-->` stripped in .md, whitespace folded, casefold)
All of §4.2 and §4.3 count exactly 1: case-focus-twin (designer:32, critic:64); red-then-read-row-first (s7, "Self-probe
notes"); red-then-no-s5-rework (s7, conductor); person-words-by-file; red-then-price-first (s7 "report writer run again",
conductor "say so first"); red-never-commented-out (s7:148); independent-then-copy-only; diagnostic-run-not-verdict;
reorder-reviewed-by-code-critic. §4.4 named anchors: "Triangulate a conflict" 1 (`agents/qa-scout.md:61`), "it is no
halt" 1 (`s1.md:377`), "Recommend an option only after" 1 (conductor). The spec says "A conflict nothing settles" is NOT
usable, and it counts 2 (scout:83, :85), so the spec is right. Misses: none among written-out anchors. Duplicates the
builder will meet: see B3. Over 6 words, needs trimming: human-questions KEY (7 words) and most §4.4 old keys (5–26
words).

### Q3 — F8 (a)
Right. The current texts carry none of K2a/K2b/K3a-sub (counts 0 in rubric/automator). The owner's FA-10 answer, "the
red-by-bug Then goes last, no commenting when reordering is possible" (HF5-16 row, batch-5 `:61`), stands in other words at
`s7.md:148` ("Nobody comments out the red"), which the row `red-never-commented-out` guards. K2b and K3a-sub are the
options the owner did not take: FA-10 (b), and FA-11 (a) before the soft-assert road of batch 6. Their absence is an
F3-class absence, already accepted. The "absent until the owner speaks" mechanism (`test_mixed_then_texts.py:30-32,107-116`)
is stale. No role text depends on the flag. The only rule-like remnant is the dim-8 safe side (dim 8 must not name
`contradicts_requirement`; it doesn't today, `references/code-review-rubric.md` dimension 8). The spec already lists it as
an F3 known loss. Fix the F8 text (R2).

### Q4 — Design
- Defeat paths: carrier renamed → E-8 red (good); anchor re-pointed to an unrelated phrase and row deleted with the rule →
  E-19, code-blind by design; deleting a row is detectable as data (R3); emptying the register → E-3 passes green with a
  "nothing guarded" line, only the critic sees it (R3 closes it); anchor matching an unrelated sentence → prevented at
  creation by exactly-once, but a 2-word floor allows generic anchors ("say so first"), so the `rule` field + critic must
  carry it (§5.2, stated); a rule held only in a template comment → false red (B1, the wrong direction for a template).
- Edges stated: missing carrier E-8 ✓; empty anchor = 0 words < 2 → E-4 ✓ (say "empty" explicitly); duplicate ids E-5 ✓;
  carrier outside the package E-7 (absolute, `..`, backslash, outside homes) ✓; duplicate JSON keys named as a blind spot ✓;
  unreadable register E-1/E-2 ✓. Missing: what happens to a key that does not hold today (B1 (c)).
- AR-29: yes, a data check, a join between two developer-authored package files. The census classes shape/xref are right;
  `word-list` (ceiling 0, `judgment-census.json:4`) is correctly ruled out. The reader returns strings and raises nothing,
  so `refusal_registry.sites` gives it no blocking unit and `blocking_per_role` is not touched (my reading of
  `test_judgment_census.py:202-212`, not run).

### Q5 — Architecture and rules
- AR-1 ✓ (closed list → one data file). AR-14 ✓ (one writer, the developer's diff; F7 sequential waves avoid two
  concurrent writers). AR-20 ✓ (no ratchet under F1-A). FR-13 ✓. FR-30 ✓: `selftest.py --lang` covers "any Cyrillic
  character anywhere in the package" (`scripts/selftest.py:11`), so `design/*.json` too.
- FR-44 / `design/`: right. Nothing loads it at run time. `release_fingerprint.py:17` keeps `design/` outside the
  fingerprint for exactly that reason. A test reading `design/` has precedent (`manifest_put.py:130`: `design/state-exits.md`
  is walked by `test_state_exits.py`). `cmd_homes` (`selftest.py:924-932`) checks only `design/*.md`, so it doesn't
  interfere. `design/` ships with the release copy (the whole directory), so the shipped case of `test_role_rules.py` runs
  in the release CI.
- Registries (wave-1 lesson). The spec §4.5 names only `plans/features.json`, and that is correct:
  - `plans/features.json`: 9 of 12 (lines 375 gate_continuation, 414 recommended, 440 detection, 517 mixed_then, 724
    s7_control, 725 red_then, 1129 critic_lines_hf2, 1133 scout_conflict, 1136 time_fork). NOT listed: blocked_by_env,
    case_role_twins, case_roles_twin_rules.
  - `fixtures/driver-layers.json`, `references/gate-registry.json`, `references/stage-joints.json`, `scripts/selftest.py`
    (`CONTRACT_TESTS`/`TEST_TIMEOUTS`), `.gitlab-ci.yml`, `scripts/slow_tests.json`, `.github/`: none of the 12. Same-shape
    controls found other test names in each (counts 3/1/2/1/2 for driver-layers/gate-registry/stage-joints/CI/slow_tests;
    selftest: `test_(infra_failure|red_sandbox_probe)` → 3).
  - Outside the list: `CHANGELOG.md` (history, not edited, as the spec says) and `experiments/driver-golden/MANIFEST.json`
    (R7). Repo-wide, the names also appear in docs/plans history files (handoffs, reviews, specs), which are not registries.
  - The spec's DoD 3 grep (`-- ai-packages/qa-factory/scripts plans/features.json`) is the right shape.

### Q6 — Buildability
TD-5.1's reader, test and wiring parts are buildable: file, functions `load`/`findings`, CLI, refusal texts, the edge
table, census rows. The migration part is not (B3). The B1 conflict (a key that doesn't hold) and the §4.1↔§4.4
contradictions (B2.5) are further guesses. TD-5.2 (scout) is well specified. TD-5.3 depends on the inventory, which is
fine. Smaller guesses: `<why>` in refusals (R4); "`cmd_limits` only, if F5-c" (decided, R1).

## Trail
- Read whole: the spec; the 12 pin files; `docs/TESTING.md:55-89`; `docs/tasks/test-diet.md:15-93`.
- Read in part: `scripts/selftest.py:884-938` (cmd_homes); `scripts/hooklib.py:694-708` (read_json);
  `references/templates/requirements-register.md` (comment boundaries by grep, lines 9-188); `handoffs/s5-automator-to-critic.yaml:111-117`;
  `s7.md:147-256` (by grep); `s1.md:34,375-442` (by grep); `agents/qa-scout.md:61,83,85`; `agents/qa-code-critic.md:37`;
  rubric dimension 8; `plans/piles/hotfix-12586/batch-5-…md:61`; `README.md:35`; `judgment-census.json:3-4`;
  `test_judgment_census.py` (grep of block/ratchet lines); `driver-golden-rules.json:70-92`; `release_fingerprint.py:17`.
- Runs (read-only Python on stdin, the spec's matcher): (1) the 12 written-out anchors of §4.2/§4.3 + 4 §4.4 anchors + 9 old
  keys; (2) every key of all 12 pins, extracted by AST, counted with and without comments (output: the template keys
  "n=0 (incl comments 1)", the duplicates s4/s8/s7 ×2, K2a/K2b/K3a-sub 0, K3a 1); (3) candidate anchors for B2/B3
  ("carries no credential value" 1, "the list is complete" 1, "A blocked row that ran red" critic 1, "judged by its
  `shape_ref`" 1, "the case's triage row" 1, "Halt only on an unresolved conflict" 1, "cannot tell" 2/2, "from the
  requirements" 3/1, "with both quotes" 1). No test file or suite was run.
- Searches with a positive control of the same shape:
  - the 12 names in the registries: `git grep -n -i -E "test_(scout_conflict_rule|…|case_roles_twin_rules)"`, then the same
    form with other names: `test_(judgment_census|audit_rules|stage_joints_12586|check_delivery)` and
    `test_(infra_failure|red_sandbox_probe)` for selftest;
  - repo-wide `git grep -l -i -E` of the same pattern;
  - "requirement/code conflict" in product code (control: `unresolved_facts` → found);
  - `oracle_field_absent` (control: `field_absent` → `manifest_from_tests.py`);
  - `manual-evidence`, `cannot-tell` readers;
  - comment stripping in non-test scripts (`re.sub(.*<!--|<!--.*?-->`) → branch_accounting/validate_artifacts found;
  - the template's delivery (`brief_pack.py:93`);
  - FA-10/FA-11 in plans;
  - selftest `--lang` scope (Grep tool, case-insensitive).
- Needed beyond the manifest: `scripts/brief_pack.py`, `scripts/hooklib.py`, `scripts/selftest.py`,
  `scripts/release_fingerprint.py`, `scripts/tests/test_judgment_census.py`, `fixtures/judgment-census.json`,
  `fixtures/driver-golden-rules.json`, `experiments/driver-golden/MANIFEST.json`, `plans/piles/hotfix-12586/*`,
  `plans/features.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: section 3.2/E-12 strips HTML comments, but references/templates/requirements-register.md carries its role guidance inside comments; all 9 template keys of test_detection_role_texts count 0 outside comments, so the section 4.4 template rows turn red or get dropped; also state what happens to a key that does not hold today",
    "B2: unguarded or unaccounted pinned rules: mixed_then K3a (name clash with the F8 K3a-sub), blocked_by_env handoff critic duties (instance_ids, remedy carries no credential value), blocked_by_env charter pointer (count==1 was its only guard), scout_conflict s1 halt on an unresolved conflict, case_role_twins K14-phase s7:239 rule",
    "B3: section 4.4 gives directions, not rows (K3-ref?, if unique, merge by rule, widen, non-unique keys, rule/source text); complete it as a row table in the 4.3 form"
  ],
  "fixes": [
    "Do not strip comments in references/templates/* (or strip only package marker comments); narrow E-12; add an edge row for a template comment",
    "State that a key failing today is not added as a row and goes under red before: for the Lead",
    "Add rows: mixed_then K3a; handoff instance_ids and remedy duties; critic pointer twin with the rubric heading; s1 'Halt only on an unresolved conflict'; K14 twin analyst + s7 'judged by its shape_ref'; rename F8 mentions to K3a-sub",
    "Write the section 4.4 rows for all ten files with counted anchors (counts in the review trail)",
    "R1-R7: stale fork text and line numbers, F8 rewording on the FA-10/FA-11 facts, proposed retire-line commit-msg data gate, reason source for refusals, K-R1-1a second row, list B-K13 as a known loss, driver-golden note"
  ],
  "class_completeness": "The class is 'a pinned role rule that the migration drops'. Swept across all 12 pin files by enumeration (Q1 table, a verdict per file); found in 4 files (B2). The sibling surfaces 'comment-stripping vs delivered comment text' and 'single-token drop vs the section 4.1 widen rule' were walked across every carrier the 12 pins name: only the template carries keys in comments; K6 and K14-phase are the token cases. Forge analogs (install_parity_anchors.json etc.) are queued by the spec to TD-8; a SIBLING_MAP axis for the package role register is queued to the Lead (spec 7.4).",
  "trail": {
    "read": [
      "docs/tasks/specs/td-5-role-rules-register.md",
      "the 12 pin files under ai-packages/qa-factory/scripts/tests/",
      "docs/TESTING.md:55-89",
      "docs/tasks/test-diet.md:15-93",
      "scripts/selftest.py:884-938",
      "scripts/hooklib.py:694-708",
      "references/templates/requirements-register.md comment lines",
      "handoffs/s5-automator-to-critic.yaml:111-117",
      "plans/piles/hotfix-12586/batch-5-run-12586-manual-red-then-bugs.md:61",
      "scripts/tests/fixtures/judgment-census.json:3-4"
    ],
    "reruns": [
      {"command": "python -B - (stdin, spec matcher) over the 12 section 4.2/4.3 anchors and 4 section 4.4 anchors", "result": "all 1; 'A conflict nothing settles' 2"},
      {"command": "python -B - (stdin, AST extraction) counting every key of the 12 pins with and without HTML comments", "result": "9 template keys n=0 outside comments, 1 with; s4/s8/s7 duplicates x2; K2a/K2b/K3a-sub 0; K3a 1"},
      {"command": "python -B - (stdin) candidate anchors for the B2 rows", "result": "each counts 1"},
      {"command": "git grep -n -i -E test_(the 12 names) over the 7 registries plus .github, with same-shape positive controls", "result": "only plans/features.json, 9 of 12; controls found names in every registry"}
    ]
  }
}
```
