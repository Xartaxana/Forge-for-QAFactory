# t-288 — diff critic, topic t-231 Parts A and B (OF1-1)

Branches: `origin/wip/t231-a` 456039c (Part A), `origin/wip/t231-b` 18eabee (Part B). Spec:
`docs/tasks/specs/t-231-env-sources-of1-1-of4-12.md` §0-§3 (A :145-168, B :170-189), §5, §6, §9.
Critic: opus, 13.11.2026.

## Verdict

- **Part A: fit_with_fixes.** Two blocking findings (F1: a sample-name regression against main; F2: a URL path leaks through the
  "host"), one fix-before-merge on the test (F3), two small items (F6, F7).
- **Part B: fit_with_fixes.** No blocking finding. Two wording fixes (F4, F5) to make in this round.
- **Ratchet raise `blocking_per_role.conductor` 474 -> 475: ACCEPTED** (reason in Q1). The spec §1 text must be fixed.

This is input to acceptance. Accepting the work and amending the spec are decisions for the coordinator / Lead tier.

## Q1. Ratchet raise (AR-20, brief item 9/11)

Row by row: `ratchet.blocking_per_role.conductor` 474 -> 475. The cause is the new census row `env_probe.py::_env_file_names`
(`shape`, `data`, roles `["conductor"]`, judgment-census.json:256).

Why the raise cannot be avoided (traced in `scripts/tests/test_judgment_census.py`):
- u3 (:22, :234-235): a body with `raise ValueError` is a unit. b1 (:262-264): a refusal site inside the unit sets `blocks = True`.
  So every u3 unit blocks, always.
- C2 (:320-322): `roles` must be a non-empty list. C3 (:349-354): every role of a blocking row adds 1 to `per_role`.
- So any row that A-2 requires adds +1 to some role. Spec §1 / §6.5 said "`shape` carries no ceiling, so no ratchet moves". That
  reasoning only covers the class ceilings (`CLASS_CEILING_KEYS`). It missed `blocking_per_role`. The error is in the spec, not the
  builder.

The no-raise alternatives, each ruled out:
- (a) `blocks_override: false` + note: this raises `blocks_overrides` 10 -> 11 instead. It is also a false label, because the unit
  does refuse work when the package is damaged (brief item 11 names this as "the other cheap way").
- (b) Raising a non-`ValueError` (RuntimeError, a custom class) so `refusal_registry.sites()` does not see it: this exploits the
  blind spot the census docstring (:32-37) explicitly forbids.
- (c) No raise / a built-in list: this breaks A-2 ("no silent classification without the table") and AR-1. (d) Let `table[...]` crash
  unnamed: this breaks FR-1.
- (e) Reuse a shared loader that already has a row: there is none. Grep `reinstall the plugin|package copy is damaged` over `scripts/*.py`
  found 15 per-module package-table loaders, each raising on its own (install_paths.py:232, proof_level.py:92, onboarding_notes.py:94,
  config_contract.py:1334, …). The diff follows the standing pattern. That convergence class predates this diff and is not this diff's to fix.
- Roles `["conductor"]` is accurate: the only callers of the loader are `project_inventory` (onboarding p1/p2b, run by the session) and,
  after Part C, `gate_preflight`. `agents/qa-scout.md:71` uses `env_probe.py`, but its `probe` path never reaches `env_file_kind` in Part A.

**Spec §1 fix (one line, census-table row 1, last cell):** "`shape` carries no class ceiling, but a u3 unit always blocks (b1), so
`blocking_per_role.conductor` rises 474 -> 475 — a named AR-20 raise (critic t-288)". The same correction goes in §6.5 and in the A DoD (4)
clause "and no ceiling raised" -> "and only `blocking_per_role.conductor` +1, named".

## Findings

**F1 (blocks) — the sample-name surface regresses against main: a dash/underscore-joined marker is now "env".**
`env_probe.py:159` splits the name only on `.`, and `:166` tests whether a part EQUALS a marker. On main the regex was
`(?i)(example|sample|template|dist)$` on the whole name. Probe output (`probe1.py`, trail):
```
'.env.dev-example'    old(is_env, example)= (True, True) new= 'env'
'.env.qa_sample'      old(is_env, example)= (True, True) new= 'env'
'.env.local-template' old(is_env, example)= (True, True) new= 'env'
'.env.docker-dist'    old(is_env, example)= (True, True) new= 'env'
```
Failure scenario: a repository whose only env file is `.env.docker-example`.
- Main marks it `example: true`, keeps `account_pairs` / `frontend_candidates` empty, and never treats it as the stand's.
- The branch makes it the chosen file, with `env_file_is_sample: false` and account pairs proposed. Its address rows go out with
  `sample: false`, so Part B's p2 rule then PROPOSES the sample's address as the stand's.

That is exactly OF1-1, reopened. It breaks A-1's own invariant ("a sample is never classified env — the marker errs toward sample").
The spec letter ("splits `name` on `.`") conflicts with that invariant here, and the builder followed the letter.
Neighbouring classes walked on this surface:
- case (`.env.EXAMPLE` ok);
- nesting (`.env.example.local` ok);
- bare form (`env.example` ok);
- non-ASCII (ok, "env");
- empty name (ok);
- separator: **fails**.

Fix:
- `env_probe.py:159-166`: keep the dot `parts` for the bare-form check (reach unchanged). For the marker test, use tokens split on the
  table's separators: `tokens = [t for t in re.split("[" + re.escape("".join(table["marker_separators"])) + "]+", text.lower()) if t]`
  and `return "sample" if markers.intersection(tokens) else "env"`.
- `references/env-file-names.json`: add `"marker_separators": [".", "-", "_"]` (closed variety stays a data row, AR-1), and make the
  loader (`_NAME_LIST_KEYS`, `env_probe.py:125`) require it.
- `test_manual_capture.py:3170`: add rows `.env.dev-example`, `.env.qa_sample`, `.env.local-template`, `.env.docker-dist` -> "sample".
- The Lead amends A-1's letter (one clause: "split on the table's separators for markers").

**F2 (blocks) — a URL path or encoded path reaches the output through the "host" (question 4).**
`project_inventory.py:451-453` builds `address` from `env_probe.origin()`. Python's `urlsplit` keeps a backslash, `%2F` or `;` inside
`hostname`, while browsers and WHATWG parsers treat `\` as a path separator. Probe (`.env` with these lines) gave:
```
"address": "http://hooks.slack.com\\services\\t0\\b0\\secretback", "has_path": false
"address": "http://host%2fservices%2fsecretpct",                   "has_path": false
"address": "http://host;secretsemi",                               "has_path": false
secretback True   secretpct True   secretsemi True    (substring present in json.dumps(discovery) + render_access)
```
- The token leaks, lower-cased, and `has_path` falsely says there is no path.
- Spec A-6's named residual is "a secret placed in a hostname". These are not hostnames; they are path material the parser did not
  split. This breaks A-6's invariant "no part of an address beyond its origin".
- Neighbouring classes walked: userinfo (`u:p@`, ok); query/fragment (ok); IPv6 (ok); bad port (ok, no row); case (the host is
  lower-cased: a mixed-case token still leaks partly).

Fix:
- `project_inventory.py`, after `scheme, host, port = parts` (:451), add:
  `if not re.fullmatch(r"[a-z0-9.-]+|[0-9a-f:.]+", host): continue`. This means no row and no count, the same treatment as
  `origin() == ()`. `origin` itself stays untouched (A non-goal).
- Add three `url_rows` to the test (`\`, `%2F`, `;`), each expecting `[]` with the token absent from json + render.

**F3 (fix before merge) — the A-2 test deletes the live package table (FR-31, hygiene pt. 7(d)).**
- `test_manual_capture.py:3280-3300` unlinks and then rewrites `references/env-file-names.json` in the package tree.
- `selftest.py:911/934` runs test files in a `ThreadPoolExecutor`. Any concurrent file that reaches `project_inventory` /
  `env_file_kind` during that window gets the `ValueError`: a load-only flake.
- The loader reads the module global at call time (`env_probe.py:135`), so the point can be proven on a copy.

Fix: set `env_probe.ENV_FILE_NAMES_PATH = <tmpdir>/absent.json`, then to a tmp file holding `{"exact": 1}`, and restore the attribute
in `finally`. Drop the unlink/byte-copy block. The live file is then never touched.

**F4 (Part B, fix this round) — p1 says the wrong thing in one sentence.**
`p1-discovery.md:149` reads "The env file is shown to the person with the file it came from." That is circular, and it is not B-2's
rule. Replace it with: "Every env value shown to the person names the file it came from."

**F5 (Part B, fix this round) — the producer/reader join through the render (AR-22/AR-21).**
- p1:47 runs `--access` (the render). The new paragraph p1:145-157 and p2:149-157 speak only in JSON field names (`sample: true`,
  `has_path`, `env_file_is_sample`). The render prints these as the prefix `sample `, ` (has a path, not shown)` and
  `only a sample:` (A-8).
- Field names checked, and they match A exactly: `env_file_addresses` {key, address, has_path, path, sample}, `env_file_addresses_more`,
  `env_file_is_sample`, `example`.
- The gap is only the mode. Fix: at p1:146 say "(`--access --json`; in the plain render, the line `http address origins in env files:`
  with a sample's row prefixed `sample` and `(has a path, not shown)` for `has_path`)". This follows the existing convention at p1:115/:125.

**F6 (Part B, fix this round) — p3 wording.** `p3-summary-gate.md:72` "One more line rule:" reads as one more line to PRESENT. Replace
it with "Rule for env values in this section:". The anchor `never shown as the stand's` stays.

**F7 (Part A, queue-level, may ride F1's round) — the loader accepts an empty `sample_markers`.**
`env_probe.py:142-143` accepts `[]` lists, so a damaged table with `"sample_markers": []` silently classifies every sample "env". That
is the silent classification A-2 forbids. Fix: require a non-empty `sample_markers` and `exact`/`prefixes`/`suffixes` not all empty.

## Per-question answers

**Q2 Part A edges.**
- A-1: all 22 spec rows pass; F1 is outside the spec rows.
- A-2: correct apart from F3/F7. The message names the file, the keys and the door. The loader goes through `hooklib.read_json` (axis 16).
- A-3: the regex and `_is_env_file`'s expression are gone; `_is_env_file` now delegates (used by `_walk` :250).
- A-4: sort `(example, path)` is unchanged (:301).
- A-5: normalisation is equivalent to §6.10 (`declared` is stripped at :466, then `PurePosixPath(...replace("\\","/"))` at :468).
  Declared sample -> chosen, flag true, pairs/candidates/same-origin empty (test rows present). Absolute / `..` match no row. No
  case-folding.
- A-6: origin only, `has_path` from `urlsplit(value.strip()).path.strip("/")`, cap 10 with the cut taking the LAST rows (real files are
  first), unreadable -> no rows. **300/301 on the origin string: correct reading.** A-6 defines `address` as "the ORIGIN only", and the
  rule says "an address longer than 300", so the field is what is measured. It also bounds what is printed. Apart from F2's bad hosts,
  only a >290-char host reaches it.
- A-7: shape verified by test row and by reading :520-524.
- A-8: both first-line forms and `where` (:615-617, :640) and the origins line (:665-672) are byte-for-byte as spec A-8. The
  non-sample branch is byte-equal to main (diff read).

**Q3 Part B (B-1..B-6).**
- B-1: grep of p1 (`\.env|env file|env\.example|sample`, case-insensitive; positive control: it hits the new law at :146) — no line
  left that sends the role into an env file or sample for a value. :44/:45/:46 are rewritten as specified. :168 is the env_file choice
  (names).
- B-2/B-3: present in p1:149-157 and p2:148-157. A sample is never proposed even when it is the only address; two non-sample files ->
  the person picks.
- No new question: the base-path ask lives inside the existing stand question (B-3 says so).
- B-4: the anchors exist verbatim (test_role_rules 57/57 rerun).
- B-5: empty outcomes stated. B-6: p3 line present inside «What was found» (wording: F6).

**Q4 Secret leakage.**
- Routes checked: secret-looking NAMES (filtered by `http_address_keys` -> `SECRET_NAME`, test row `API_KEY_URL`); userinfo
  (urlsplit `hostname` drops it — probe `C_URL` ok); path/query/fragment (dropped); the render (prints only row fields).
- `has_path` is a bool. No other value leaves `env_file_address_rows`; `account_pairs`/candidates are unchanged.
- Leak found: F2 only.

**Q5 Class-wide completeness / duplication / quality.**
- CLASS (SIBLING_MAP): axis 37 is not in the map yet. That is the named, queued deviation of spec §1 AR-15 / §2a, and not a finding here.
- Grep for env-file NAME tests over `scripts/*.py` (`startswith("\.env|endswith("\.env|== "\.env"|"\.env\*"|"\*\.env"|env\\\.`, -i):
  hits only `gate_preflight.py:5179` (Part C, queued by spec) and `guard_secrets.py:22` (kept, §2a). These two known sites are the
  positive control. No unqueued sibling.
- Axis 16: the loader uses `read_json`, ok. Axis 5: untouched.
- DUPLICATION AND CONSISTENCY: none blocking.
  - The origin->string formatting (:452-453) is new, but no formatter exists. Grep `scheme\}://\{|'\[' \+` found `env_probe.py:463`,
    `device_stand.py:266`, `manual_capture.py:2695` — all use `netloc` or the path, and so are not reusable for an origin-only form.
  - `env_file_address_rows` re-parses each env file already parsed by `env_file_keys` (t-230's function, not owned): a second read
    with no second parser. Acceptable.
  - The per-module package-table loader pattern: pre-existing class (Q1(e)).
- CODE QUALITY:
  - New functions are all under 60 lines and nested at most 3 levels.
  - `_walk` and `scan_sources` both call `env_file_kind` per file, and each call stats the table twice (`env_probe.py:135-136`). This
    is redundant I/O — queue, not blocking. Suggestion: one `stat()` per call.
  - No dead branches. Names are truthful.
  - Test lines (150) exceed product lines (~110). This is justified by the A-1/A-6 adversarial tables the DoD itself requires.
- ONE ROAD (P31, item 12): none found. The diff branches on no language, project or framework (diff read in full; the only
  conditionals are sample / non-sample and the IPv6 bracket).
- JUDGMENT (item 11): the one census row added is `shape`/`data`, correctly classed (it judges the form of a package file). No
  `blocks_override`, no edit to the scan constants. Part B adds a judgment rule for the role (which address is the stand's) and no code
  detector (FR-12 kept).
- What the role still decides (AR-2): which found address is the stand's, its full base path when `has_path`, and that a sample's
  address is never it. Stated in B's text.

## Mechanical-layer consistency

- Witness numbers ↔ diff: 70 new A-* rows is plausible. Counted from the table: 22 name rows + about 48 check_* calls, consistent.
- The census `21 passed` was rerun and matches. test_role_rules 57/57 was rerun and matches.
- The AR-1 grep was rerun: after the change, all hits are comments, the `example` field and `SKIP_DIRS` "dist" (a directory name, :144).
  The control on main finds the regex at :267 (the spec said :275 — line drift only).
- Not rerun: test_manual_capture (it writes to the package table, F3) and the slow files. They are accepted as attached.

## Trail

Read:
- the spec (§0-§10, :1-578);
- docs/tasks/critic-diff-brief.md (whole);
- SIBLING_MAP (grep env/axis 16);
- both full diffs;
- test_judgment_census.py :1-80, :200-274, :315-354;
- hooklib.read_json :751-768;
- env_probe.origin :851-862 and http_address_keys :548-557, SECRET_NAME :93;
- project_inventory grep `_is_env_file|declared|sort|MAX_FILES`;
- p1/p2/p3/p2b greps (worktree t231-b).

Commands:
- `git fetch -q origin`; `git diff --stat` / `git diff refs/remotes/origin/main...refs/remotes/origin/wip/t231-{a,b}`.
- `python -m pytest <A>/scripts/tests/test_judgment_census.py -q -p no:cacheprovider` -> `21 passed in 22.63s`.
- `python -B <B>/scripts/tests/test_role_rules.py` -> `=== role rules: 57/57 ok ===`.
- `python -B <scratchpad>/probe1.py <A>/scripts` -> the output quoted in F1 and F2. The scratchpad is
  `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\probe1.py`, read-only on
  the worktree.
- AR-1 grep after the change, and the same grep on `origin/main:project_inventory.py` (control).
- Env-file name-test grep (control: gate_preflight/guard_secrets).
- Formatter grep.
- `reinstall the plugin` loader grep.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: env_probe.py:159-166 splits only on '.', so .env.dev-example / .env.qa_sample / .env.local-template / .env.docker-dist (samples on main) become 'env' and can be chosen as the stand's file - OF1-1 reopened",
    "F2: project_inventory.py:451-453 builds address from a urlsplit hostname that keeps backslash, %2F and ';' - a URL path token leaks (lower-cased) into json and render with has_path false"
  ],
  "fixes": [
    "F1: marker tokens split on a new table key marker_separators ['.','-','_'] (loader requires it); bare-form check keeps dot parts; add 4 test rows -> sample; Lead amends A-1 letter",
    "F2: after origin(), skip the row unless host fullmatches [a-z0-9.-]+ or [0-9a-f:.]+ (no row, not counted); 3 test rows (backslash, %2F, ;) with the token absent",
    "F3: A-2 test redirects env_probe.ENV_FILE_NAMES_PATH to tmp files instead of unlinking the live package table (FR-31, hygiene 7d)",
    "F4: p1-discovery.md:149 -> 'Every env value shown to the person names the file it came from.'",
    "F5: p1-discovery.md:146 names the mode (--access --json) and the render forms (prefix sample, '(has a path, not shown)')",
    "F6: p3-summary-gate.md:72 'One more line rule:' -> 'Rule for env values in this section:'",
    "F7: loader requires non-empty sample_markers and a non-empty env-file rule",
    "Spec: section 1 census row, 6.5 and A DoD (4): shape has no class ceiling but a u3 unit always blocks; blocking_per_role.conductor 474 -> 475 is a named AR-20 raise (accepted by critic t-288)"
  ],
  "class_completeness": "Env-file name sites: gate_preflight.py:5179 queued to Part C, guard_secrets.py:22 kept (spec 2a); no other name test in scripts (grep with those two as positive control). Axis 37 absent from SIBLING_MAP by the named AR-15 deviation (queued to full Lead). F1 and F2 neighbouring classes walked (case, nesting, bare, non-ASCII, empty; userinfo, query, IPv6, port).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-231-env-sources-of1-1-of4-12.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (grep)",
      "git diff origin/main...origin/wip/t231-a",
      "git diff origin/main...origin/wip/t231-b",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py",
      "ai-packages/qa-factory/scripts/hooklib.py read_json",
      "ai-packages/qa-factory/scripts/env_probe.py origin, http_address_keys, loader",
      "ai-packages/qa-factory/scripts/project_inventory.py",
      "ai-packages/qa-factory/skills/qa-onboarding/phases/p1,p2,p3,p2b (grep)"
    ],
    "reruns": [
      {"command": "python -m pytest t231-a/.../test_judgment_census.py -q", "result": "21 passed in 22.63s"},
      {"command": "python -B t231-b/.../test_role_rules.py", "result": "=== role rules: 57/57 ok ==="},
      {"command": "python -B scratchpad/probe1.py t231-a/scripts", "result": "4 dash/underscore samples now 'env'; backslash, %2F, ';' tokens present in output"},
      {"command": "grep -n -i -E 'example|sample|template|dist' project_inventory.py (branch and origin/main)", "result": "no file-name test after; control finds regex at main :267"}
    ]
  }
}
```
