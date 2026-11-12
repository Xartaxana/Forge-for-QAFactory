# t-093: small-work batch, findings of the calibration of 12.11.2026 filed into piles (builder, documents only, no commit)

## Table: finding file -> pile -> batch -> node -> owner decision

Files are under `plans/piles/<pile>/findings/`, all named `20261112-<slug>.md`.

| # | Calibration item | finding file (slug) | pile | batch | node | owner decision |
|---|---|---|---|---|---|---|
| 1 | 1 dispatcher spec defects | spec-dispatchera-ne-nesyot-sosednij-klass | forge | 7 | FG7-18 | yes (recommended: WARN `neighbors:`) |
| 2 | 2 narrowed witness | suzhennyj-svidetel-molchit-v-pyati-iz-shesti-pozdnih-defektov | forge | 7 | FG7-19 | yes (part II only) |
| 3 | 3 designer threshold | porog-dizajnera-propuskaetsya-molcha | forge | 7 | FG7-20 | yes (recommended: WARN by owns >= 3) |
| 4 | 4 repeat self-execution | povtornoe-samoispolnenie-odnogo-klassa-v-sessii | forge | 7 | FG7-21 | no |
| 5 | 5 journal | zhurnal-priemka-pered-sdachej-canon-ne-v-witness-basis-rejected | forge | 7 | FG7-22 | no (Lead fork: basis on `rejected`) |
| 6 | 6 stale navigation | navigatsiya-ustarela-ukazateli-perezhili-svoi-obekty | forge | 7 | FG7-23 | no (D-0045 is Lead's) |
| 7 | 7 permissions | net-razdela-permissions-v-settings-json | forge | 7 | FG7-24 | yes (recommended: yes, narrow rows) |
| 8 | 8 Lead context | kontekst-lida-bez-szhatiya-i-kompakt-bez-snimka | forge | 7 | FG7-25 | no |
| 9 | 9 ratchet raises | podyomy-hrapovikov-bez-imeni-v-verdikte-ar-20 | forge | 7 | FG7-26 | no |
| 10 | 10 ONE ROAD | verdikty-kritika-bez-one-road-i-kodovyj-sloj-ne-podklyuchen | forge | 7 | FG7-27 | no |
| 11 | 11 feature attribution | privyazka-k-fichham-ostatok-posle-a8a9fb4 | forge | 7 | FG7-28 | no |
| 12 | 12 exchange form | obmen-skauta-8k-tokenov-pri-celi-2k | forge | 7 | FG7-29 | no |
| 13 | 13 craft sections | razdely-masterstva-nesut-stroki-procedury-p27 | roles-context | 2 | RC2-3 | no (fork 3 is Lead's) |
| B1 | nightly red | nochnoj-prohod-krasnyj-probe-by-code-languages-300-s | package-ci | 3 | PC3-2 | no (owner word 12.11 already given) |
| B2 | carrier survives the cut | nositel-perezhivaet-rezku-bez-izmenenij-source-split-carriers-i-named-by | forge | 7 | FG7-30 | no |

B3 (edit, not a finding): `plans/features.json`, see below. Forge batch 7 now has 30 node rows (17 before, FG7-18..FG7-30 added: 13), i.e. well over size S; still one batch as the edge says, the Lead re-cuts later.

## Per-item decisions

- Pile for item 13: `roles-context` (card "Роли, тексты и контекст", zone `agents/qa-*.md`, untaken batch 2). `thinking-roles` also touches the runner role (four untaken batches) but leads behaviour of the walk, not the charter text; I judged one pile fits better and did NOT fall back to `forge`. Said in the finding. Question 3 below.
- Existing findings (greps by key words over `plans/piles/*/findings`, DECISIONS.md and the archive; the same grep shape found known samples, e.g. `witness-for`, `features.json`, `BATCH CANON`, `AR-20`, `snapshot`): no item is a pure duplicate, but four overlap a class and are linked in "Связи" of the new finding:
  - item 6 <-> `onboarding-forge/findings/20261014-kalibrovka-1-slepye-detektory-i-ustarevshaya-navigaciya.md` (F6-10, still open in `onboarding-forge`/1: dead SIBLING_MAP paths, stale CURRENT_CONTEXT). Same class "pointer outlives its object", but different instances; filed. The checker of map paths stays F6-10's job, FG7-23 only fixes instances and waits for it.
  - item 4 <-> same finding, point 3 (repeat key of six words is blind). Different class (rule broken, no marker at all); filed, six-word key not touched.
  - item 12 <-> `forge/findings/20261013-format-obmena-mezhdu-rolyami.md` (F5-2, closed): it adopted the form; the calibration measures the target (2K) still missed. Filed as a residual measure.
  - item 8 <-> `onboarding-forge/findings/20261023-hooki-sessii-privyazany-k-cwd-...` (F6-36): same probable root of the PreCompact silence; the node starts with an experiment and defers the fix there if confirmed.
  - items 2, 9, 10, 5 link their siblings (`20261111-svidetel-...`, F6-45, `20261106-odna-doroga-...`, FG7-16).
- Old test files with NO feature attribution: none. All six old files had one (F05: test_controller_rework.py; F06: test_no_move_seam.py, test_infra_failure.py, and test_story_run_loop_b/_freshness via glob `test_story_run*.py`; F12: test_handoff_values.py via glob `test_handoff*.py`). Nothing is left unattributed by this rule.
- B3 result (the part files of freshness, loop_b and handoff_values were ALREADY matched by existing globs `test_story_run*.py` and `test_handoff*.py`; the six commons and the parts of controller_rework, no_move_seam, infra_failure were not). Added globs: F05 `test_controller_rework_*.py` + `controller_rework_common.py` (explicit `test_controller_rework_scope.py` row kept as it was); F06 `test_no_move_seam_*.py`, `no_move_seam_common.py`, `test_infra_failure_*.py`, `infra_failure_common.py`, `story_run_*_common.py`; F12 `handoff_values_common.py`.
- Facts I could not verify from the evidence parts (marked in the finding text): the four extra files at 260-288 s in B1 (named neither in the record nor in `slow_tests.json` as such: "проверить"); run ids 43178152997 / 43157607270 are quoted from the dispatch (the 209.2 s is confirmed in `ai-packages/qa-factory/scripts/slow_tests.json:81`); `F19` root-repo block in `features.json` (finding 11, "проверить"); the PreCompact cwd hypothesis (finding 8, stays an experiment).

## DoD runs (verbatim)

```
$ python tools/piles.py check --all
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (2 active batches)
(в) frozen: ok (2 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main ca44194
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (32 piles, 88 batches)
(е) findings: ok (913 findings read, 0 dated from 2026-10-13 on are orphans, 167 older are the baseline)
(е) findings: WARN: 167 finding(s) dated before 2026-10-13 or undated (74) are named in no batch file of their pile (the baseline the calibration reads; not blocking), ...
piles check: ok

$ python tools/piles.py board
piles board: wrote plans/PILES.md: 32 piles, 88 batches, 432 ids
piles board: WARNING: untracked file(s) under plans/piles feed plans/PILES.md: <the 15 new finding files> -- `git add` them, or the next committer's `board --check` goes stale

$ python tools/piles.py board --check
piles board: up to date (32 piles, 88 batches, 432 ids)
(the same untracked-files WARNING; not an error)

$ python -m pytest tools/test_pile_cards_contents.py -q
131 passed in 1.63s

$ python tools/forge_metrics.py --check --base origin/main
forge_metrics --check: ok (base ca44194): new rows 0 (all attributed), new findings 15 (all attributed), new package files 0 (all classified), new journal events needing a feature 0 (all carry one)
```

B3 witness: `python tools/forge_metrics.py --window 2026-11-12` before the edit: "package files on disk matching no feature: 20" (6 commons + 13 parts + test_manifest_projection.py), "files in window commits matching no feature: 19"; after: "package files on disk matching no feature: 1 (test_manifest_projection.py, not mine)", "files in window commits matching no feature: 0", "Overlaps: 0"; `plans/features.json` parses as JSON.

`git status --porcelain` at the end:

```
 M plans/PILES.md
 M plans/features.json
 M plans/piles/forge/README.md
 M plans/piles/forge/batch-7-vhodyashchie-4.md
 M plans/piles/package-ci/README.md
 M plans/piles/package-ci/batch-3-khrapovik-doors-only.md
 M plans/piles/roles-context/README.md
 M plans/piles/roles-context/batch-2-slova-cheloveka-v-brife.md
?? 15 new findings under plans/piles/{forge,package-ci,roles-context}/findings/ (+ this report)
```

## Questions for the Lead

1. Items 4-6, 8-12 and 13 carry directions the record only implies (the record chose a direction for none of them except items 1-3's "promote?" and 7); each finding writes the most conservative reading of the record as "Что именно менять" and marks function/flag names as "проверить по коду" where I did not read the code. Please confirm or replace: FG7-21 (`calibration_counts` table, marker `repeat:`), FG7-22 point 2 (`basis` on `rejected`) and 3 (canon carrier), FG7-26 (new data file `tools/ratchet-files.json`), FG7-27 point 3, FG7-28 (feature for `live-runs`, recommendation F15).
2. FG7-23 and D-0045: the number is absent from every decisions carrier; I did not write a line for it (fork left in the finding).
3. Pile for item 13: `roles-context` chosen over `thinking-roles` (both fit in part). Move if you disagree.
4. Pile `forge` batch 7 now has 30 nodes (size S per its header); re-cut at your discretion. Three of its nodes (FG7-18, FG7-20, FG7-27 with FG7-21) share `tools/dispatch_manifest.py` / `tools/calibration_counts.py`: ordering is stated in "Зависит от".
5. `test_manifest_projection.py` remains unattributed (owned by finding 11's node).

## Needed beyond the manifest

`plans/piles/roles-context/{README.md,batch-2-*.md}`, `plans/piles/thinking-roles/README.md` (pile choice), `plans/piles/onboarding-forge/batch-1-*.md` and `findings/20261014-kalibrovka-1-*.md` (overlap), `tools/test_pile_cards_contents.py`, `tools/source-split-carriers.json`, `ai-packages/qa-factory/scripts/tests/test-layers.json` (named_by lines), `ai-packages/qa-factory/design/state-exits.md` (lines 118-121), `ai-packages/qa-factory/agents/qa-runner.md` and `qa-case-critic.md`, `ai-packages/qa-factory/scripts/slow_tests.json`, `tools/language_sites.py` (docstring), `docs/tasks/specs/td-11c-test-split.md` and `td-11d-world-per-file.md`.

## Same-class neighbours noticed (not widened)

- `plans/piles/forge/README.md` "Пачки" row 7 says size S while the batch has 30 nodes (the card size column is the Lead's to re-cut).
- Other findings in `forge` that name `20261014-kalibrovka-1-*` as `onboarding-forge` pile files but are listed in the `forge` card (F6-36, F6-10): card rows and files live in different piles; not touched.
