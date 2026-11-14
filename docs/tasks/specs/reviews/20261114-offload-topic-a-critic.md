# t-854 — topic critic, coordinator-offload spec r2, topic A (A1 t-847, A2 t-848, A3 t-849)

Critic: opus (claude-opus-5-5). Spec: `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md` §2 Landing, §3.A1-A3,
§6.1, §6.2, §7 M1/M2, §9' F-A1-2, §11, §11'. The decisions below are proposals; accepting the work and any spec edit
belong to the Lead (Fable for A1's landing and spec meaning).

## Verdict

**GO WITH FIXES** — one blocking fix for A3 (classifier miscounts product modules named `test_*.py`; the A3 report's
own-diff claim is false because of it), one report correction, one consistency fix in TESTING.md that needs a Lead
spec decision, two small text fixes, one queued proposal. A1 and A2 deliver the spec texts verbatim (diffed, see trail).

## Numbered fix list

1. **A3 classifier: product modules named `test_*.py` are counted as tests (BLOCKING for A3).**
   File `tools/test_volume.py`, `classify()` (the `TEST_BASENAMES` branch). The basename rule `test_*.py` fires on
   product code: forge tools `tools/test_volume.py` (this very tool), `tools/test_quarantine.py`, `tools/test_redundancy.py`,
   `tools/test_split.py`, and package scripts `ai-packages/qa-factory/scripts/test_files.py`, `test_locations.py`,
   `test_novelty.py`, `test_path_grants.py`, `test_repo_base.py`, `test_source.py` (none has `def test_`; `test_split` and
   `test_redundancy` have a `__main__`; `test_files.py` docstring: "Is this a test file? The one leaf…"). Evidence:
   `decide()` on A3's own commit numstat (`git diff --numstat -M a98f2792~1 a98f2792`: 16 `.githooks/commit-msg.proposed`,
   70 `tools/test_test_volume.py`, 142 `tools/test_volume.py`) returns
   `(True, (212, 0), 'TEST VOLUME (WARN, …): +212 test lines vs +0 product lines …')`.
   This contradicts (a) TESTING.md's own definition (its measurement table: package tests = `scripts/tests/`, package code
   = «`.py` вне тестов»), and (b) the spec's declared error direction «unsure → product (fewer WARNs)»: every product edit
   to those ten files draws a false WARN.
   Expected behaviour: in `ai-packages/` a test is recognised by the SEGMENT rule only (`tests`/`test`/`fixtures`), never
   by basename; outside `ai-packages/` a path that is a test ONLY by basename `test_*.py` is a test iff its staged blob
   (`git show :<path>`) has a line matching `^\s*(def test_|class Test)`; blob unreadable → product. (Alternative the Lead
   may prefer: a data row of forge tool modules named `test_*`; weaker — a new tool named `test_x.py` silently goes the
   dispreferred way.) Keep `decide()` pure: pass the blob check in as an injectable predicate (default: the git read).
   Test rows (same table): `pkg_script_test_star` (`ai-packages/qa-factory/scripts/test_files.py` → product),
   `tool_named_test_star` (`tools/test_volume.py`, predicate False → product), `tools_real_test` (predicate True → test),
   `blob_unreadable` (predicate raises → product), and `pkg_tests_segment` (`…/scripts/tests/test_x.py` → test, no blob read).
   Timing: land this BEFORE B23 adds `tools/test_volume.py` to `MECHANISM_PREFIXES` (spec :484/:644) — afterwards every
   classifier fix is a Fable mechanism commit. The fix commit is still inactive: the same `axes: not a mechanism (inactive
   proposal; …)` line holds.

2. **A3 report: false load-bearing claim (rule 12 / witness).** `docs/tasks/handoffs/t-849-A3.md` says «Own diff: test
   lines +70 vs product lines +142 … no WARN owed». The tool as committed says +212 vs +0 and WARNs (fix 1). The fix-round
   report attaches the FIXED tool's verbatim output on its own commit's staged numstat (expected: no WARN, product ≥ test).

3. **TESTING.md «Бюджет / Объём» — the owner carrier lacks the `tests-over:` duty that four pointers state (consistency,
   axis 31; needs a Lead spec decision).** Builder.md rule 8, critic.md rule 20, builder-rules 7d and the how-to item 8
   all say "reason in the report AND a `tests-over:` line in the commit"; the bullet they all point to
   (`docs/TESTING.md:115-116`) still says only «Больше — билдер называет причину одной строкой отчёта, критик судит её».
   The one-owner invariant of E-A1-1 is thus inverted for the door: four carriers state a duty the owner does not.
   A2 obeyed E-A2-1 («other bullets byte-identical»), so this is a spec gap, not a builder defect. Expected text (append
   to the «Объём» bullet): «Больше — билдер называет причину одной строкой отчёта и строкой `tests-over: <причина>` в
   сообщении коммита (хук commit-msg без неё предупреждает, не отказывает); критик судит её.» E-A2-1's invariant (the
   «Время» owner question undecided) still holds — only «Объём» is touched. Test row: key-presence run (keys `tests-over:`,
   `хук commit-msg`) with a negative control. Owner of the decision: the Lead (relaxing E-A2-1).

4. **TESTING.md «Плохо:» example names a non-existent file (minor; spec verbatim text).** `test_fix_13797.py` does not
   exist; the same file at :118 names the real `test_fixes_13797`. Renaming to the real file would make a FALSE content
   claim: Grep of `ai-packages/qa-factory/scripts/tests/test_fixes_13797.py` for `agents/qa-automator.md` finds nothing.
   Expected text: «Плохо: файл по имени тикета (`test_fixes_<тикет>.py`, «Бюджет / Файлы») с проверкой «фраза стоит в
   `agents/qa-automator.md`» и копией файла без ключа, которая должна упасть.» Lead decides (verbatim spec text).

5. **WARN text points at «Бюджет», the roles at «Бюджет / Объём» (minor, optional).** `tools/test_volume.py` `WARN_TEXT`
   and critic.md rule 20 cite `docs/TESTING.md «Бюджет»`; builder.md 8 and builder-rules 7d cite «Бюджет / Объём».
   Cheap to align in the fix-1 round: `WARN_TEXT` → «Бюджет / Объём» (the row `test_gt_product` asserts only numbers and
   `tests-over:`, no row changes). critic.md 20 is a Fable-landed verbatim text — leave as is unless the Lead re-words.

6. **Proposed node (not topic-A-owned; the Lead opens it):** `docs/tasks/critic-diff-brief.md` question 5 — the
   question critic rule 20 points to — (a) says «more test lines than product lines with no reason named» without the
   `tests-over:` line, and restates the rule instead of pointing at «Бюджет / Объём» (E-A1-1 lists brief Q5 among the
   pointer carriers, but no stream owns it); (b) «a new test file with no keep row … — finding» must be scoped to the
   package, since the new «Бюджет / Файлы» exception gives forge tools of this spec a test file with no keep row. Owner:
   the Lead; executor: a builder in the next small-work batch.

Landing notes (not fixes): A1's builder.md rule 8 points at the A2 section — merge A1 after or with A2. A1's Fable commit
carries the F-A1-2 deviation line («critic.md rule 10: PROCESS/CRITIC_EXAM.md absent; exam not run; finding opened») and
the Lead opens that finding (rule 10 of this role: I also cannot meet it from here).

## Answers to the dispatch's questions

**(1) A3's `axes: not a mechanism (inactive proposal; …)` — the reason holds.** Checked: git runs only `.githooks/commit-msg`,
never `commit-msg.proposed`; `diff` of the live `commit-msg` (at a98f2792~1, which is on origin/main) vs the proposed file
= exactly two added lines (a comment and `python tools/test_volume.py "$1" || true`); the githooks coverage test
(`tools/test_mechanism_gate.py:1273-1283`) reads only the live `pre-commit` and `commit-msg`, so the branch breaks nothing.
The duty starts only when stream L places the hook, and the spec makes that commit carry M2's axis block and B23 put
`tools/test_volume.py` into `MECHANISM_PREFIXES` (spec :484, :644) — the Landing invariant «no real mechanism change carries
the skip line» is kept. Asymmetry with B1/C1/C3 (inactive too, yet carrying axis lines) is justified: their CLIs are called
by sessions directly from the day they land; `test_volume.py` has no caller until the hook. Condition: L's placing commit
must carry the M2 axis block (spec §7) — the Lead holds that.

**(2) WARN never blocks — yes; definitions — NOT the same until fix 1.** Exit 0: `main()` returns 0 always, `run()` wraps all
in `try/except Exception`, the hook adds `|| true` after `set -e` gates (E-A3-8 positional invariant holds: a refused
commit exits before the WARN line). Driven live (scratch repo, the committed tool as the commit-msg hook): a test-only
commit WARNs `+20 test lines vs +0`; a merge whose staged diff vs HEAD holds 20 test lines is silent while the hook DID run
(`HOOK-RAN` echoed) — the untested `MERGE_HEAD` path works; a commit with `tests-over: fixture` is silent. Definitions:
"test line" = added lines of tests + fixtures (TESTING.md :24 counts «тестов и фикстур»; tool: segments `tests/test/fixtures`
— same); "product line" = code AND text of the product (TESTING.md :115 «строк кода и текста продукта»; tool: everything
under `ai-packages/`, `tools/`, `gateway/`, `experiments/measurers/` — same) — EXCEPT the basename rule, which moves ten
product modules into "test" (fix 1). Unit differences, stated in the spec and acceptable: the rule counts per node diff,
the tool per commit (E-A3-9); the tool counts added lines (the WARN prints `+<t>`, so the unit is visible). The roles
(A1) restate neither definition — they point at «Бюджет / Объём» — so no third definition exists.

**(3) One owner per duty — holds for the rule, not for the door (fix 3).** The rule text (the 1:1 ratio) lives only in
TESTING.md «Объём»; builder.md 8, critic.md 20, builder-rules 7d carry a pointer with no number (verified: none of the
three restates «не больше»/a ratio; builder-rules 7d's old sentence is replaced exactly per §6.1). No contradiction with
TESTING.md: builder-rules 7d keeps «новый тестовый файл не создаётся» without the forge exception, which is right —
builder-rules is the package builders' carrier (PROJECT.md «Где что лежит») and the exception is for `tools/`; builder.md
8 names the exception («Бюджет / Файлы»). Critic rule 20 vs critic rules 18/19: separate verdict line, no overlap.
`PROCESS/CRITIC_EXAM.md` deviation (F-A1-2 (a)): absence verified by me (below); the deviation is legitimate only if the
Fable commit names it and the Lead opens the finding — the builder report carries the exact line to paste.

**(4) Duplication / quality / test volume.**
- DUPLICATION AND CONSISTENCY: no second implementation of a forge "is this a test path" or numstat-volume reader found:
  Grep `_testkit|is_test_path|def _is_test|TEST_SEGMENTS|def classify` and `def (is_test|_is_test|classify)` over
  `tools/*.py`, `experiments/measurers/*.py` → only unrelated classifiers (`forge_metrics.classify_path` = feature
  attribution, `controller-blocks-gen.classify`, `hook_liveness_probe.classify_settings_commands`, …); Grep `numstat` →
  `tools/r3_integration_check.py` only (commit-size window, add+del, a different question). The package's
  `scripts/test_files.py` answers "is this a test file" for the PROJECT UNDER TEST — a different object (spec axis 9 n/a
  reasoning holds). Consistency findings: fixes 3, 4, 5, 6.
- CODE QUALITY: all new functions under 30 lines, nesting ≤ 3; no dead branches; `new_path` handles both rename forms
  (rows `rename_added_only`, `rename_arrow`). One lying name: the tool's own name `test_volume.py` puts it in the test
  class (fix 1 cures the effect). Quoted (non-ASCII) numstat paths would fall to "excluded": n/a today — `git ls-files`
  under `tools ai-packages gateway experiments/measurers` lists 0 quoted paths.
- ONE ROAD (item 12): the merge exemption is the task's own condition; the «Бюджет / Файлы» exception for this spec's
  tools only is the owner's word quoted with its carrier (spec §11 F-T1 «Свой файл каждому … ок»; §11' F-T1-2 (a)). None blocks.
- TESTS (critic rule 20 as proposed): A3 +70 test / +142 product under the rule's definition — within 1:1, no reason owed;
  one parametrised table (19 rows) + 2 junction-like tests; would catch a door/merge/binary regression. The defect of fix 1
  was not caught because no row put a product module named `test_*` in the table — the fix adds those rows.
- A2 specifics asked: lower-case key «одна строка, которая падала до правки» vs the spec's own §6.2 text «Одна строка …»
  — a DoD-key transcription defect of the dispatcher, not of A2 (the section is byte-identical to §6.2 c). E-A2-2 «every
  number appears elsewhere» is violated literally by −1, 0, 1.5 — but those come from the spec's own verbatim text and are
  P16's example inputs, not limits; spec self-inconsistency, no fix owed by A2.

## Trail

Read: spec r2 §2 (whole incl. Landing), §3.A1-A3, §6.1, §6.2, §7 (a)-(d) whole, §9', §10, §11, §11'; `git -C <A1 wt>
diff --cached` (whole) and status; `docs/tasks/handoffs/t-847-A1.md` (whole); `git show 36a7ed89` (whole) and
`docs/TESTING.md` at 36a7ed89 :1-30, :95-161 and its headings; `git show a98f2792` (whole: tool, test, proposed hook);
`docs/tasks/handoffs/t-849-A3.md` (whole); `docs/tasks/critic-diff-brief.md` Q5, items 6, 7, 12;
`tools/test_mechanism_gate.py` :1200-1290; `tools/mechanism_gate.py` `MECHANISM_PREFIXES` net lines;
`tools/agents_md.py` (scope: frontmatter only); heads of `tools/test_redundancy.py`, `tools/test_split.py`,
`ai-packages/qa-factory/scripts/test_files.py`; `tools/critic_verdict.schema.json`.

Verbatim checks (scratch diff of extracted text, CR stripped): builder.md rule 8 = §6.1 → identical; critic.md rule 20 = §6.1
→ identical; TESTING.md new section = §6.2 c → identical except the trailing blank separator line (the diff reporting that
blank line is the positive control of the method); «Файлы» exception sentence = §6.2 a → identical; builder-rules 7d =
§6.1 text, «Бюджет:» label and the rest of the line kept; line 55 pointer present.

Spot-checked claims: A3 «own diff no WARN owed» → FALSE (fix 1/2); A3 «merge silent» (only a flag row) → TRUE, driven live;
A1 «AGENTS.md needs no regeneration» → TRUE (`agents_md.py` reads frontmatter only; `--check` up to date); A1/A2 «texts
verbatim» → TRUE.

Negative claim verified: `PROCESS/CRITIC_EXAM.md` absent — `ls PROCESS | grep -i exam` lists `DEPLOYMENT_ECONOMY_EXAM.md`,
`LEAD_RANKING_EXAM.md` (positive control: the same listing finds the existing exams); `find -ipath '*critic_exam*'` → none;
`git ls-files | grep -i critic.exam` → only `.claude/skills/critic-exam-gen/SKILL.md`. Second negative: "no tools/ test_*.py
without test functions" was NOT assumed — the loop (positive control: `grep -c "def test_" tools/test_journal_keys.py` → 72)
found the four forge tools and six package scripts of fix 1.

Re-runs: A3 `python -B -m pytest <scratch copy of a98f2792 test_test_volume.py> -q` → `21 passed in 0.27s`; A1 in the
worktree `python -B -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py
tools/test_agents_md.py -q` → `110 passed in 14.82s`; `python -B tools/agents_md.py --check` → `AGENTS.md: up to date
(120887 bytes)`; probe `decide(<a98f2792 numstat>)` → `(True, (212, 0), …)`; live hook drive in a scratch repo (test-only
commit WARN; merge silent with `HOOK-RAN`; door silent).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A3 tools/test_volume.py classify(): basename rule test_*.py counts product modules as tests (tools/test_volume.py, test_quarantine.py, test_redundancy.py, test_split.py; ai-packages/qa-factory/scripts/test_files.py, test_locations.py, test_novelty.py, test_path_grants.py, test_repo_base.py, test_source.py); decide() on A3's own commit gives (True, (212, 0)); contradicts TESTING.md's own definition and the spec's unsure-to-product direction",
    "A3 report t-849-A3.md claims own diff +70 test vs +142 product, no WARN owed; the committed tool says +212 vs +0 and WARNs"
  ],
  "fixes": [
    "1. tools/test_volume.py classify: in ai-packages/ tests by segment only; elsewhere a basename-only test_*.py is a test iff its staged blob has def test_ or class Test (injectable predicate, unreadable -> product); rows pkg_script_test_star, tool_named_test_star, tools_real_test, blob_unreadable, pkg_tests_segment; land before B23 nets the file",
    "2. A3 fix-round report: attach the fixed tool's verbatim output on its own staged numstat",
    "3. docs/TESTING.md Budget/Volume bullet: append the tests-over commit-line duty (Lead relaxes E-A2-1 for that bullet only); key-presence run with negative control",
    "4. docs/TESTING.md bad example: replace non-existent test_fix_13797.py by the pattern test_fixes_<ticket>.py (real file does not hold the described check); Lead decides, verbatim spec text",
    "5. optional: WARN_TEXT section pointer aligned to Budget/Volume",
    "6. proposed node for the Lead: critic-diff-brief Q5 gains the tests-over line and scopes the no-keep-row finding to the package"
  ],
  "class_completeness": "Class 1 (test-path classifier on basename): all ten product modules named test_*.py enumerated by a loop over git ls-files with a positive control; fix covers both trees. Class 3 (owner carrier vs pointers, axis 31): all five pointer carriers enumerated (builder.md 8, critic.md 20, builder-rules 7d, TESTING how-to 8, brief Q5); owner gap fixed by 3, Q5 queued by 6. Axis 4 (AGENTS.md): not affected, frontmatter only. Axis 2 (critic exam): F-A1-2 deviation, absence verified.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-coordinator-offload-spec-r2.md sections 2, 3.A1-A3, 6.1, 6.2, 7, 9', 10, 11, 11'",
      ".claude/worktrees/agent-a761020cc04116bed staged diff (builder.md, critic.md, plans/builder-rules.md)",
      "docs/tasks/handoffs/t-847-A1.md",
      "git show 36a7ed89 and docs/TESTING.md at 36a7ed89 lines 1-30, 95-161",
      "git show a98f2792 (tools/test_volume.py, tools/test_test_volume.py, .githooks/commit-msg.proposed)",
      "docs/tasks/handoffs/t-849-A3.md",
      "docs/tasks/critic-diff-brief.md Q5, items 6, 7, 12",
      "tools/test_mechanism_gate.py 1200-1290; tools/mechanism_gate.py MECHANISM_PREFIXES",
      "tools/agents_md.py scope; heads of tools/test_redundancy.py, tools/test_split.py, ai-packages/qa-factory/scripts/test_files.py",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -m pytest <scratch copy>/test_test_volume.py -q", "result": "21 passed in 0.27s"},
      {"command": "(worktree) python -B -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_agents_md.py -q", "result": "110 passed in 14.82s"},
      {"command": "(worktree) python -B tools/agents_md.py --check", "result": "AGENTS.md: up to date (120887 bytes)"},
      {"command": "decide(numstat of a98f2792~1..a98f2792, 'msg', False)", "result": "(True, (212, 0), TEST VOLUME WARN +212 test vs +0 product)"},
      {"command": "scratch repo with the tool as commit-msg hook: test-only commit / merge --no-ff / door commit", "result": "WARN +20 vs +0 / silent with HOOK-RAN echoed / silent"}
    ]
  }
}
```
