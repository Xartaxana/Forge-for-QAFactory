# t-578 / EP1-41a report: surfaces table, reader, web lock

Branch `r0108/t-578` from 93731262. Commit order: (1) `a43289f8` the web pin and its comparison test, on the untouched code, 28 files, written by `test_surfaces.py --write-pin` and re-compared on a second run; (2) the next commit: `surfaces.json`, `surfaces.py`, `readiness.py` (only `compute`), `manual-capture-steps.json` (`table_free`, one note sentence), qa-doctor step 2, p1-discovery, tests, changelog fragment, this report. No line of `surfaces.py` existed at (1).

## Darker table (t-544 section 5)

Darker HEAD at reading: `aaa44653c1d108b2e4889a30d4b3de6276b47e93` (`git ls-remote https://github.com/Xartaxana/Darker-than-a-dark-test-factory HEAD`). Base: `https://raw.githubusercontent.com/Xartaxana/Darker-than-a-dark-test-factory/aaa44653c1d108b2e4889a30d4b3de6276b47e93/`. Downloaded with `curl.exe -fsSL` into a new directory of the OS temp (outside the tree), files only read (Read tool), never run or imported, nothing copied into the repository. Negative control: `scripts/no-such-file-xyz.py` gave `curl: (22) ... 404`, no file created, 0 reads.

| N | Address at the sha | Read | What it showed | Data row changed |
|---|---|---|---|---|
| [1] | `.claude/settings.json` 58-100 | read | allowed forms `adb devices` (58), `adb shell uiautomator dump*` (60), `adb exec-out screencap*` (63), `adb logcat*` (64), `adb shell am start -W -n ...` (59), the Appium `/status` call (69, 85) | none. `logcat -d -t {tail}` flags are not shown (only the prefix `adb logcat*`): stay general knowledge |
| [2] | `scripts/doctor.py` 89-138 | read | serial from `adb devices` rows whose second field is `device`; explicit `AO3_DEVICE`/`ANDROID_SERIAL` (our key name is data), 2+ devices without it is a warning, never the first | none (rule for 41b code; table `devices.argv` confirmed) |
| [3] | `scripts/doctor.py` 305-463 | read | `adb -s <serial> shell dumpsys package <pkg>`, `versionCode=(\S+)` inside the package block; `adb shell pm path` (a `/base.apk` line of `package:` lines) and `adb shell sha256sum <path>` (first 64-hex token). `versionName=` is not read by Darker. The live output was never captured there either (its own comment: "NO DEVICE") | `android.installed_build.code_re` `versionCode=(\d+)` -> `versionCode=(\S+)`. `version_re` stays general knowledge |
| [4] | `scripts/doctor.py` 466-641 | read | named checks, ok / fail / warn, a reason on every branch, "n/a" outcomes that say why | none (41b texts) |
| [5] | `scripts/tasks.ps1` 926-985, and 989-1063 for the session (moved on, found by name `Test-AppiumHealthy`) | read | `GET {url}/status`, `value.ready -eq $true`, `/status` at the base path `/`; deep: `POST /session` with `alwaysMatch` caps `platformName Android`, `appium:automationName UiAutomator2`, `appium:deviceName`, `appium:udid`, `appium:newCommandTimeout 30`; `DELETE /session/<id>`; timeout 120 s with one retry after 15 s | `drivers.appium.session_timeout_s` 60 -> 120. Not changed, flagged: Darker's health session uses `newCommandTimeout 30` and no `noReset`; our shared `session_defaults` (`noReset true`, 300) are for a hands session. 41b decides whether the deep probe needs its own defaults |
| [6] | `scripts/tasks.ps1` 1346-1358 (`Get-Device`), and 906-924 (`Get-DeviceSerials`) | read | the wrapper prints `DEVICE: <serial>` / `NO DEVICE`; the tool inside is `adb devices`, skip line 1, rows matching `\sdevice$`. The header text is skipped by position, not matched | none. `header_re`, `other_row_re` stay general knowledge. The wrapper's words are not contract |
| [7] | `framework/core/reporting.py` 15-50 | read | failure evidence is a screenshot (`get_screenshot_as_png`), the context, `page_source`, and `adb.logcat_dump(dest)`; the driver is reached through a client, no W3C path literal; the logcat flags live in `adb.py`, outside the reading list | none. W3C paths and logcat flags stay general knowledge |
| [8] | `framework/core/a11y_tree.py` whole | read | `page_source` XML attributes `content-desc`, `text`, `resource-id`, `class`, `clickable`, `displayed`, `bounds` | none in 41a. For 41d: the Android half of `page_words` (`text`, `content-desc`) is confirmed; `label` stays an iOS guess. Darker's hands are `adb`, not a W3C session: Ф-1 stands, W3C paths labelled general knowledge |

## Per item

- Table, reader, lock: DONE. `references/surfaces.json` (t-511 section 2 with t-524 9.1 edits; no language, runner or `note` about them), `scripts/surfaces.py` (`TABLE_PATH`, `rows`, `row_of`, `stand_rows`, `declared_surfaces`, `unsupported`, `stand_for`, `stand_of_profile`), `readiness.compute` `surfaces` key, `capture_surfaces.{ui,http}.table_free`.
- qa-doctor step 2 and p1-discovery (signal row, summary line, text per t-544 6.1 items 3 and 4): DONE. SKILL.md 18992 bytes (cap 19000); I shortened two neighbouring sentences of step 2 to make room.
- `row_for_profile`: NOT DONE, question below.

## Answers

AR-1: closed variety is the table; `grep -E 'android|ios' surfaces.py` 0, `grep -ciE 'read_test_adapters|framework_adapter|pytest|typescript|kotlin|java'` 0 in both files, positive control `grep -c native`: 1 (py), 3 (json). AR-2: roles judge what an unknown capability word is (it reads the table and publishes nothing); `declared_surfaces` ran on a `gradlew test` profile and on a broken table and reported, never halted. AR-3: no new top-level config key; `table_free` is a data flag. AR-10: p1 summary names the test language before S5. AR-13: the table has one reader; free words come through `manual_capture.spec()`. AR-20: pin changes only by Lead's word.

FR pass: A: no refusal text added (`ValueError`s name file, expectation and door, FR-1). B: `words` are plain sentences, `human_text` not run on them (not run: unchecked). C: `declared_surfaces` shape documented in the docstring. D: unknown never `ok` (table error is `unknown`, FR-59). E, F: not touched. G: English (`--lang` pass), FR-33 open: nothing ran on a device.

## Mutation (named, not run)

A language list in `unsupported` (e.g. a set of runner names added to its result) -> `test_surfaces.py` line "a native profile whose command and tests are in any language: no language word". `row_of` returns the web row for a typo -> same file ("a surface the table lacks is refused"). `declared_surfaces` always reads the table -> "web+api: ... table was not read".

## Deviations, findings, questions

1. Added data field `words_only_alone: true` on the `cli` row to say "only if no other arm" as data (spec states the rule, not the field).
2. Unknown capability word: the table is read, nothing is published (spec silent). A word like `mobile` would pass in silence: question for Lead, a design decision.
3. `row_for_profile(cfg, profile)`: named in owns, defined nowhere in my text: left unimplemented. Question: what does it return?
4. Negative control covers `ui`, `http`, `_blocked`, `readiness.compute` (three configs) and `s5_profiles` (broken table, `surfaces.rows` read 0 times, output equal to the pin). `Driver.stand_login_problem` and `env_probe.probe` are not exercised: neither imports `surfaces` today; their controls belong to 41c/41f.
5. The pin has no `fixtures` for `http` with a login-user failure: those `_blocked` branches are reached only through `ui`.
6. Class siblings seen: `capture_surfaces` and `surfaces.json` are two tables of one fact (queued in t-524 section 12); the 41e `artifact` argv and `session_defaults` meet the Darker notes above.

## Witness

```
python -B ai-packages/qa-factory/scripts/tests/test_surfaces.py   -> === test_surfaces: 80/80 ok ===
python -B ai-packages/qa-factory/scripts/tests/test_readiness.py  -> === test_readiness: 209/209 ok ===
python tools/dup_ratchet.py --check  -> scripts: 12 groups, 10 known, 0 new, 0 grown, 2 carried, 3 shrunk/gone (3 diverged)
                                        tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
python tools/lint_ratchet.py --check -> no finding in my files (one unused import fixed; the others listed belong to other files)
python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang -> PASS limits ...; === qa-factory selftest: 3/3 ok ===
```

Needed beyond the manifest: `scripts/manual_capture.py` (`spec`), `scripts/tests/fixtures/manual-evidence/scaffold.py`, `test_manual_capture.py` (fake helpers), `harness.py`, `role-commands.json`, t-524 sections 9.4 (`stand_of_profile` rule) and 9.3. Needed from integration: none.
