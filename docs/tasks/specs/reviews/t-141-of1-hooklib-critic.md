# t-141 — critic diff gate, onboarding-forge/1, stream "hooklib" (OH3-37, CD1-11)

Diff: `git -C .claude/worktrees/of-hooklib diff origin/main...wip/of-hooklib` (b898935 OH3-37, f99b9f3 CD1-11; 8 files, +152/-18).
Node rows: `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md` rows OH3-37 (line 34) and CD1-11 (line 45); finding
`plans/piles/onboarding-forge/findings/20261030-windows-260-codex-dispatch-bez-konteksta.md` §2 (the OH3-37 class).

**Verdict: NEEDS WORK (ACCEPT WITH FIXES) — 3 merge-blocking findings (B1-B3), 6 further fixes (F4-F9).**
The code changes themselves are small and correct on the paths they cover; what blocks is where the tests live, an
incomplete class on CD1-11 with false completeness claims, and a missed version bump on a money reader. The decision to
accept stays with the coordinator.

## Findings

### B1 (blocks merge) — the node tests are written into two QUARANTINED files
`scripts/tests/test-layers.json` holds both `test_cost_capture_nonfactory_summary.py` and `test_factory_dashboard_joins.py`
in its `quarantine` section (probe: `json.load(...)` → sections `['quarantine']` for both). `docs/TESTING.md` §«Карантин»
lines 63-68: a quarantined file "в каноне не запускается, не чинится и не правится". Consequences:
1. The canon never runs `BareRootTests`, `bare_root_creates_nothing` or `factory_activity_is_one_set`: neither OH3-37 nor
   CD1-11 has a pin that CI judges; the builder's red control proves a test nobody will run.
2. Neither commit message carries `quarantine-edit: <file> -- <reason>`. `tools/test_quarantine.py` `check_history`
   (lines 1690-1692) flags every commit that touches a quarantined path without that door, so `forge-check` goes red.
   Confirmed by running `python -B tools/test_quarantine.py check --root <worktree>`: "quarantine check: 3 violation(s)".
   It reports b8989353 for both files and f99b9f37 for test_cost_capture_nonfactory_summary.py, each expecting a
   `quarantine-edit:` line.
The dispatch's own non-goal ("no quarantined files") points the same way.
**Fix:** take the edits out of both quarantined files. Put the cases where the canon runs them: rows the
`scenario_walk.py --witness-for scripts/factory_dashboard.py scripts/cost_capture.py scripts/hooklib.py` output names (e.g.
a variant row on `story_root_class` / `guard_write_owners`), or a keep-layer `table` test. Redo the red control there.
Drop the source pin (`'("doctor", "onboarding", "story")' not in text`). TESTING.md lists a pin on a script's source
under «не пишется» (brief item 5).

### B2 (blocks merge) — CD1-11 class incomplete; three completeness claims are false
Two more readers still answer "is this factory activity" with their own three-word literal:
- `scripts/factory_dashboard.py:1955-1973` `_has_factory_activity`: `a.get('type') in ('doctor', 'onboarding', 'story')`.
  Its docstring says this is "the identical rule cost_capture.py uses to COMPUTE the field". After this diff that is false.
  The file is already in this diff (OH3-37), so the sweep-the-artifact rule applies.
- `scripts/metrics_projection.py:441-461` `_has_factory_activity`: same literal and same "mirrors" claim.
Failure scenario: a cost file without `has_factory_activity`, whose `by_activity` holds only a `collect` activity, counts as
NOT factory work on the dashboard and in the metrics. The same session counts as factory work once it is recaptured. One
session, two answers, which is exactly what the owner's word on CD1-11 removes.
False claims: the f99b9f3 FR walk "D - FR-17 the set is wired at every reader"; "architecture: AR-1 -- ... read by every
site"; the changelog fragment "the three places that asked ... read one set". The test assertion "one set, three readers"
checks only hooklib and cost_capture.
**Fix:** put ONE predicate in `activity_capture` (e.g. `is_factory_activity(items)`: `isinstance(a, dict)` and
`isinstance(a.get("type"), str)` and the type is in `REAL_FACTORY_TYPES`; this also closes F9). Make it the only reader in
`hooklib.session_has_factory_activity`, `cost_capture` (drop `_has_factory_type`, a second copy of the inline `any()` in
hooklib), `factory_dashboard._has_factory_activity` and `metrics_projection._has_factory_activity`. Correct the two
docstrings, the changelog and the AR line.

### B3 (blocks merge, money reader) — `READER_STAMP` not bumped
`cost_capture.py:988-991`: "READER_STAMP ... bump it with any change to what a scan or a capture writes". CD1-11 changes
what a capture writes: `has_factory_activity`, which also decides `collapse_requests` at `:2338`. The stamp stays
`capture-0.10.7`, so `_stale_kind` rule (i) (`:2577`) never fires. Every existing cost file of a collect /
environment-maintenance session keeps `has_factory_activity: false` and its collapsed ledger, while new captures say
`true`. The owner's word ("collect and environment-maintenance now count") is applied to new sessions only, and nothing says so.
**Fix:** bump `READER_STAMP` (one recapture pass over the stamped files is the documented price). If the price is not
wanted, the coordinator records a forward-only decision in the node row and in the changelog. The tier above decides
which; silence is not an option.

### F4 (fix this round) — the builder's cost_capture finding is REAL and belongs to OH3-37 itself
Reproduced (probe below): the hook-stdin form, plain and `--debounced`, on a bare root with a readable transcript creates
`qa-factory/state/cost/.writers/s1/state/events.lock`. Cause: `cost_capture.main` (`:3804-3817`) builds `cost_dir` from
`state_dir(event)` and takes the session lock (`_capture_with_wait` → `_capture_lock` → `EventStore(lock_root).lock()`)
BEFORE `_should_capture`'s `config.json` test (`:1894`). The docstring above that test (`:1885`) promises the opposite:
"the hook never creates `qa-factory/` in a project that is not onboarded".
It is reachable live: `telemetry_hook.main` (`:96-128`) computes `enabled` but runs the target script whether or not it is
set, so every Stop/PostToolUse in a project that is not onboarded yet (the onboarding session itself included) leaves the
tree behind.
Which node: OH3-37. Its owns list `scripts/cost_capture.py`, and its finding §2 asks for exactly this ("сперва прогон на
корне без config.json"). The builder measured it, so this is not a new node.
**Fix:** in `cost_capture.main`, before `_mark_started` and before the lock, return silently (exit 0) when
`not hooklib._carries_project(project_root(event))`. A hook must not exit 3: "telemetry does not stop the pipeline". Then pin
the hook-stdin form in the test moved under B1.

### F5 (fix or queue with a node id) — `install_smoke --report` left without a disposition; axis 10 row stale
The OH3-37 row names `install_smoke --report` and owns `scripts/install_smoke.py`. The diff does not touch it, and the given
materials record no decision about it. The writer here is the doctor's relative path
`--report "qa-factory/state/doctor-install-smoke-latest.json"` (`skills/qa-doctor/SKILL.md:50`) together with `atomic_json`.
`docs/SIBLING_MAP.md` axis 10 still lists OH3-37 as queued, with "cost_capture is NOT established" and "factory_dashboard by
reading, not run". Both are now outdated.
**Fix:** either refuse in `install_smoke` (a `--report` under a root with no config) or move the doctor's step order. If
neither is done now, give it a queue line with a node id and an owner. Update the axis 10 row in the same move.

### F6 (fix before merge; touches a hot file outside owns) — `SystemExit(3)` escapes a best-effort refresh
`run_suite.refresh_dashboard` (`run_suite.py:903-910`) calls `dashboard_main([])` inside `except Exception: pass`.
`require_project_at` raises `SystemExit`, which is a BaseException. Probe on a bare cwd: "SystemExit escaped best-effort
refresh: 3". Before the diff the same call returned normally (and wrote the stray tree that OH3-37 removes). At
`:2132` the call comes after the child test process is launched, so an escape would abort the runner with the job left
`running`.
`dashboard_refresh.refresh_project` is the declared "ONE chokepoint" and already returns `not_configured` without
config.json. run_suite bypasses it.
**Fix:** make `run_suite.refresh_dashboard` call `dashboard_refresh.refresh_project(project_root())`, or at minimum catch
`SystemExit`. `run_suite.py` is a hot file outside these owns, so the coordinator either extends owns
(`run_suite.py (refresh_dashboard)`) or queues it with a node id. The other in-process callers are safe:
`dashboard_refresh` checks config first; `metric_signals --ack` requires an existing metric-signals.json.

### F7 (fix or queue with a node id; ONE ROAD / duplication) — two refusal builders for one rule
`host_probe._not_a_project` (`host_probe.py:1077-1105`) still builds its own text for the same marker rule. It has the
better door: "Re-run with --root {above}" when an ancestor carries the marker. `require_project_at`'s docstring claims
"The ONE refusal every writer ... uses (AR-15)", and the b898935 AR-15 line says "one survivor". Neither is true while
host_probe keeps its copy. In practice `factory_dashboard --root <a story folder inside a project>` gets no hint about the
project above. The shared text also never names the one door the dashboard has on a bare root (`--read-only --out <file
outside the root>`) for a person who only wanted a page.
**Fix:** move the text into one hooklib builder, e.g. `not_a_project_text(root, given, extra_door="")`, carrying the
ancestor hint. `require_project_at` prints it and exits; host_probe returns it; the dashboard passes the `--read-only` door
as `extra_door`. Alternatively queue it with a node id.

### F8 (fix with B1/B2) — stale comments
`cost_capture.py:1938-1941` still says "doctor/onboarding/story type" in the `likely_factory` equivalence argument (the
argument still holds, the words do not). Test line `with mock.patch(...),                 mock.patch(...)`: a lost line
continuation, which goes away when B1 moves the test.

### F9 (folded into B2) — junk activity types
Strings, `""`, `None` and unknown words all give False (the builder's test and my probe agree). Unhashable values do not:
`{"type": []}`, `{"type": {}}` and `{"type": ["story"]}` raise `TypeError: unhashable type` (probe). Before the diff,
tuple membership returned False. `attribution_activities` keeps such entries (probe), so `_capture` would die at
`likely_factory` with "COST CAPTURE INCOMPLETE" and no cost file. Reachable only through a corrupted activity file
(`activity_capture.update` itself refuses such a type), so this is low severity, but it is a regression on the edge the
dispatch named. The `isinstance(str)` guard in the B2 predicate closes it.

## Answers to the dispatch questions

1. **Correctness / edges.** `factory_dashboard.main`: the refusal sits after argument validation and before every write (the
   recapture at `:3789`, `project_metrics(write=True)` at `:3988`, `refresh_signals(root)` at `:4026`, the page at
   `:4169`). The control re-run is green. Bare cwd, a `qa-factory/` folder without config.json, and `--root bare` from a
   project cwd are all refused with exit 3 and the tree byte-identical (the test runs a subprocess and compares trees).
   `--read-only --out` on a bare root works and writes nothing under it: metrics `write=False`, signals in a temp scratch,
   the recapture skipped. The test pins this. `require_project` delegation: same text except the em dash became " - "
   and "point --root at it" was added. The pins (`test_story_root_class.py:602` "refusing to create one") still match.
   install_smoke's dashboard steps run on a project seeded with `config.json` (`install_smoke.py` ~:115), so they are
   unaffected. CD1-11 on the two readers it touched: correct for strings, None, empty and junk entries. Unhashable types: F9.
   The class: B2.
2. **The `--out` deviation is RIGHT.** On a bare root a plain `--out` still writes `state/metrics.json`
   (`project_metrics(write=not args.read_only)`) and the signal files (`refresh_signals(root, ...)`) under
   `<root>/qa-factory/state`, whatever `--out` says. "Let `--out` pass with refresh skipped" would be a second road to
   exactly what `--read-only` already is (P31, brief item 12). Keep the refusal, and name the `--read-only` door in its text (F7).
3. **The cost_capture finding is real** (reproduced, both hook forms). It belongs to OH3-37 itself: F4, fixed in this round.
4. **Duplication / quality.** Duplication: `_has_factory_type` and hooklib's inline `any()` are one predicate in two places,
   and `factory_dashboard`/`metrics_projection` hold two more copies (B2). host_probe's refusal text is a second builder (F7).
   `dashboard_refresh.refresh_project:25` tests the marker by hand instead of with `_carries_project`; that is a skip, not
   a refusal, so not a blocker, but it belongs in F7's sweep. Code quality: no new function over 60 lines or deeper than 3
   levels. The names and annotations that lie are the "ONE refusal" docstring (F7) and the two "identical rule" docstrings
   (B2). Map siblings: `host_probe._not_a_project` (F7); `metric_signals.refresh` has a single caller, the dashboard, which is
   covered: the refusal comes before it, and the read-only path uses a scratch root. Axis 10 still has install_smoke open
   (F5), and the cost_capture hook is open (F4).
5. **AR-n / FR walk.** AR-9 kept for the dashboard (what is wrong, what was expected, the door). AR-15 claimed but not
   held (F7). AR-1 claimed "every site" but not held (B2). AR-22 is touched by CD1-11 (the producer `has_factory_activity`
   versus its fallback readers) and is not walked (B2/B3). FR spot-check of the negatives: b898935 "D n/a" is false, since
   FR-17 (the tool wired wherever the problem occurs) applies and the problem remains at the cost_capture hook and at
   install_smoke (F4/F5). f99b9f3 "D - FR-17 wired at every reader" is false (B2). "B n/a" holds for CD1-11. OH3-37 changes
   refusal text, which is a person-facing text (FR-6 applies; the text is plain-language, so it is answered by fact, not
   blocked). Judgment: none, agreed (a data-presence check and set membership).
6. **Readers of the behaviour change** (environment-maintenance and collect now count). `guard_pre_tool._in_factory_scope`
   (`:580-596`): such sessions now get the read-size limit and the turn counter. `skills/qa-collect/SKILL.md` (49 lines)
   tells the agent to read no large file (grep for read/open/KB/MB: nothing relevant), so I found no breakage. This follows
   the row as written. `cost_capture`: those sessions keep a per-request ledger instead of `collapse_requests`, so the files
   are bigger, which is intended. `dashboard_cost_groups` labels read `FACTORY_TYPES` and are unchanged. Breakage: the
   fallback readers disagree with the writer (B2), and old files are never reclassified (B3).

## Standing verdict lines
- DUPLICATION AND CONSISTENCY: findings B2 (the predicate in 4 places), F7 (two refusal builders). Grepped:
  `"doctor", ?"onboarding"|"onboarding", ?"story"|has_factory_activity` across `scripts/*.py` (excluding tests);
  `_not_a_project|refusing to create one`.
- CODE QUALITY: no long or deep new functions; lying annotations (B2, F7); stale comment (F8); source pin and a mangled
  line in the test (B1/F8).
- ONE ROAD: the `--out` / `--read-only` choice keeps one road (good); two refusal texts for one rule (F7). No exclusion of
  any language or project: grepped the diff for language/runner/project names, none.

## Trail
Read: the full diff; node rows OH3-37/CD1-11/LR1-5; finding §2; `docs/tasks/critic-diff-brief.md` (two layers, items
5-7, 12, return form); `docs/SIBLING_MAP.md` axis 10; `docs/TESTING.md` §Карантин; `factory_dashboard.py` 1955-1973,
3750-3830, 3980-4030, 4160-4175; `hooklib.py` 35-42, 54-94, 169-208, 2192-2214; `cost_capture.py` 985-991, 1885-1945,
2230-2240, 2330-2360, 2570-2610, 2800-2830, 3789-3825; `metrics_projection.py` 441-461; `host_probe.py` 1077-1130;
`dashboard_refresh.py` 1-80; `run_suite.py` 890-910 and the refresh call sites; `metric_signals.py` 355-372;
`onboard_apply.py` 1300-1310, 1455-1490; `install_smoke.py` 95-192, 565-590; `telemetry_hook.py` 89-135;
`guard_pre_tool.py` 560-596; `activity_capture.py` 53-79; `skills/qa-collect/SKILL.md`; `test-layers.json` sections;
`tools/test_quarantine.py` 1590-1640, 1667-1695, 1744-1758; the two commit messages.
Re-runs (verbatim tails):
- `python -B tests/test_factory_dashboard_joins.py` → "Ran 27 tests in 6.354s / OK". This is a quarantined file; I ran it
  only as the control of the attached witness, which deviates from the dispatch non-goal and is disclosed here.
- `python -B tests/test_cost_capture_nonfactory_summary.py` → "PASS test_cost_capture_nonfactory_summary / PASS bare root:
  cost_capture creates no qa-factory/ / PASS factory activity: one set, three readers" (quarantined; same note).
- Probe, run_suite on a bare cwd: `run_suite.refresh_dashboard()` → "SystemExit escaped best-effort refresh: 3".
- Probe, cost_capture hook stdin on a bare root, plain and `--debounced` → rc=0 both, and the tree created:
  `./qa-factory/state/cost/.writers/s1/state/events.lock`.
- Probe, `_has_factory_type` on junk: `[]`, `{}` and `['story']` → "RAISES TypeError unhashable type"; `attribution_activities`
  keeps a `['x']`-typed entry.
- `python -B tools/test_quarantine.py check --root <worktree>` (background, completed) → three lines "quarantined file ...
  was changed, deleted or renamed -- expected a line 'quarantine-edit: ...'" (b8989353 x2, f99b9f37 x1), then
  "quarantine check: 3 violation(s)".

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: node tests written into two quarantined files (test-layers.json quarantine: test_cost_capture_nonfactory_summary.py, test_factory_dashboard_joins.py) -- never run by canon; tools/test_quarantine.py check reports 3 violations (b8989353 x2, f99b9f37 x1) for missing quarantine-edit lines",
    "B2: CD1-11 class incomplete -- factory_dashboard._has_factory_activity (:1972) and metrics_projection._has_factory_activity (:460) keep the doctor/onboarding/story literal; FR-17, AR-1 and changelog completeness claims false",
    "B3: cost_capture READER_STAMP not bumped although has_factory_activity semantics changed (its own rule at :988-990); old collect/environment-maintenance cost files never reclassified"
  ],
  "fixes": [
    "1 (B1): remove the edits from both quarantined test files; place the bare-root and one-set cases in a canon-run layer (scenario variant rows named by scenario_walk --witness-for, or a keep-layer table test); redo the red control there; no source pin",
    "2 (B2): one predicate in activity_capture (dict entry, str type, member of REAL_FACTORY_TYPES) read by hooklib.session_has_factory_activity, cost_capture (drop _has_factory_type), factory_dashboard._has_factory_activity, metrics_projection._has_factory_activity; fix both docstrings, the changelog and the AR-1 line",
    "3 (B3): bump cost_capture.READER_STAMP, or record a forward-only decision of the coordinator tier in the node row and changelog",
    "4 (F4): cost_capture.main returns silently (exit 0) before _mark_started and the session lock when hooklib._carries_project(project_root(event)) is false; pin the hook-stdin form",
    "5 (F5): install_smoke --report on a root without config.json: refuse, or change the doctor step order, or queue with a node id; update SIBLING_MAP axis 10 row (dashboard done, cost_capture established)",
    "6 (F6): run_suite.refresh_dashboard must not let SystemExit(3) escape: route through dashboard_refresh.refresh_project(project_root()) or catch SystemExit; owns extension or queued node (hot file)",
    "7 (F7): one refusal-text builder in hooklib with host_probe's ancestor hint and an extra-door slot (dashboard: --read-only --out); host_probe._not_a_project uses it; or queue with a node id",
    "8 (F8): refresh the stale doctor/onboarding/story comment at cost_capture.py:1938-1941"
  ],
  "class_completeness": "Not complete. CD1-11: two more readers of the same predicate (factory_dashboard, metrics_projection) left on the literal, and no READER_STAMP bump. OH3-37 (SIBLING_MAP axis 10): factory_dashboard done; cost_capture hook path still creates qa-factory/ (reproduced); install_smoke --report not dispositioned; host_probe refusal still a second builder; run_suite.refresh_dashboard newly exposed to SystemExit; axis 10 row stale.",
  "trail": {
    "read": [
      "git diff origin/main...wip/of-hooklib (8 files)",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md rows OH3-37, CD1-11, LR1-5",
      "plans/piles/onboarding-forge/findings/20261030-windows-260-codex-dispatch-bez-konteksta.md section 2",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis 10",
      "docs/TESTING.md quarantine section",
      "ai-packages/qa-factory/scripts/factory_dashboard.py 1955-1973, 3750-4030, 4160-4175",
      "ai-packages/qa-factory/scripts/hooklib.py 35-94, 169-208, 2192-2214",
      "ai-packages/qa-factory/scripts/cost_capture.py 985-991, 1885-1945, 2230-2360, 2570-2610, 2800-2830, 3789-3825",
      "ai-packages/qa-factory/scripts/metrics_projection.py 441-461",
      "ai-packages/qa-factory/scripts/host_probe.py 1077-1130",
      "ai-packages/qa-factory/scripts/dashboard_refresh.py 1-80",
      "ai-packages/qa-factory/scripts/run_suite.py 890-910 and refresh call sites",
      "ai-packages/qa-factory/scripts/telemetry_hook.py 89-135",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py 560-596",
      "ai-packages/qa-factory/scripts/install_smoke.py 95-192, 565-590",
      "ai-packages/qa-factory/scripts/onboard_apply.py 1300-1310, 1455-1490",
      "ai-packages/qa-factory/scripts/activity_capture.py 53-79",
      "ai-packages/qa-factory/scripts/tests/test-layers.json sections",
      "tools/test_quarantine.py 1590-1640, 1667-1695, 1744-1758",
      "commit messages b898935, f99b9f3"
    ],
    "reruns": [
      {"command": "python -B tests/test_factory_dashboard_joins.py (worktree scripts dir)", "result": "Ran 27 tests in 6.354s OK"},
      {"command": "python -B tests/test_cost_capture_nonfactory_summary.py", "result": "PASS test_cost_capture_nonfactory_summary; PASS bare root: cost_capture creates no qa-factory/; PASS factory activity: one set, three readers"},
      {"command": "probe: run_suite.refresh_dashboard() in a bare cwd", "result": "SystemExit escaped best-effort refresh: 3"},
      {"command": "probe: cost_capture.py hook stdin (plain and --debounced) in a bare root with a readable transcript", "result": "rc=0; created ./qa-factory/state/cost/.writers/s1/state/events.lock in both modes"},
      {"command": "probe: cost_capture._has_factory_type with list/dict types", "result": "RAISES TypeError unhashable type; attribution_activities keeps the junk entry"},
      {"command": "python -B tools/test_quarantine.py check --root <worktree>", "result": "quarantine check: 3 violation(s) -- b8989353 (both quarantined test files), f99b9f37 (test_cost_capture_nonfactory_summary.py), each expecting a quarantine-edit line"}
    ]
  }
}
```
