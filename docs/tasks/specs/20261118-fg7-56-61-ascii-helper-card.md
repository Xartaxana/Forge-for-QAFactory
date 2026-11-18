# FG7-56 + FG7-61 -- one ASCII line helper for tools/ (design card, draft)

task: t-1384 | node: forge/7/FG7-56 (+ FG7-61, one class) | feature: F19 | designer draft, 18.11.2026
Status: DRAFT. Forks F1..F11 are returned with a recommendation; the Lead decides. Nothing below is closed that carries design weight.

## 1. Scope, invariant, architecture lines

Goal: the ASCII sanitizers of tools/ hook and report lines collapse to ONE stdlib helper `tools/ascii_line.py`
(home named by FG7-61); every copy that is the class calls it; every copy left out is named with its reason.

THE INVARIANT (FG7-61): every hook line and report line stays byte for byte what it is today. That means, for each
member: same character set out, same cap per call site, same order of steps, same None / non-str reading. Section 6
says how acceptance proves it.

- AR lines: the spec does not touch `ai-packages/qa-factory/`, so the AR-n block of designer rule 1 does not apply.
  AR-15 ("one survivor, wired everywhere"; change check: "grep for the problem, not the helper, and list every site.
  A site that cannot call the survivor is named on its axis. A new survivor gets an axis in the same commit") is the
  node's rationale, quoted from `ai-packages/qa-factory/design/architecture.md:214-219`. Section 3 is that grep; F10 is
  the axis question.
- Checks added or altered: none (no gate, no refusal). One parameterised test is added (section 7).
- variety: none -- one tools/ helper over behaviours that already exist; no language, project or case reaches it.
- One road (rule 6): every member reaches the helper the same way (F2 is the one place a per-file road is proposed,
  and it is returned as a fork).

## 2. The copy table (bodies read 18.11.2026)

Steps are listed in the order the body runs them. "ctrl" = the class `[\x00-\x1f\x7f]` (includes `\t \n \r`).
"?" = one `?` per code point (`str.encode("ascii","replace")`; lone surrogates and C1 `\x80-\x9f` included).
No copy appends a cut marker except hygiene_gate::_clip.

| # | file::symbol (line) | None | non-str | strip | ctrl | non-ASCII | cap (default) | marker | proposed |
|---|---|---|---|---|---|---|---|---|---|
| 1 | coordinator_rules::_ascii (37) | "None" | str() | yes, BEFORE ctrl | removed | "?" | head, 200 | none | IN, replace profile |
| 2 | session_context::_ascii_sanitize (1064) | "None" | str() | yes, before ctrl | removed | "?" | head, 80 | none | IN, replace profile |
| 3 | tier_echo::_ascii_sanitize (141) | "None" | str() | yes, before ctrl | removed | "?" | head, 80 | none | IN, replace profile |
| 4 | journal_echo::_ascii_sanitize (487) | "None" | str() | yes, before ctrl | removed | "?" | head, MAX_MESSAGE_LEN (500 per module docstring :108) | none | IN, replace profile |
| 5 | journal_echo::_raw_sanitize (471) | "None" | str() | yes, before ctrl | removed | KEPT | head, MAX_MESSAGE_LEN | none | F5 (recommend IN, keep profile) |
| 6 | wait_reaper::ascii_clip (59) | "" | str() | NO | each -> " " (127 too) | "?" | head, n (no default) | none | F3 (recommend IN, reaper profile) |
| 7 | crap_report::ascii_text (589) | "None" | str() | no | KEPT raw | `\xNN` `\uNNNN` `\UNNNNNNNN` (backslashreplace) | none | none | F4 (recommend IN, escape profile) |
| 8 | wiring_check::_ascii_safe (261) | "None" | str() | no | KEPT raw | backslashreplace | none | none | F4 (recommend IN, escape profile) |
| 9 | escape_check::_ascii_safe (322) | "None" (via ascii()) | ascii(): a repr | no | ASCII str: raw; else repr-escaped (`\n` -> `\\n`) | ASCII str: identity; non-ASCII str: QUOTED repr, backslashes doubled | none | none | F7 (recommend OUT) |
| 10 | session_context::_ascii_content_line (2124) | TypeError | TypeError | no | removed EXCEPT `\t` | transliteration table, then "?"; returns (line, translit, unmapped) | none | none | F8 (recommend OUT) |
| 11 | hygiene_gate::_clip (1910) | TypeError | TypeError | no | kept | kept: stdout is UTF-8 by design (`_reconfigure_stdout_utf8` :2048-2050, `json.dumps(..., ensure_ascii=False)` :2140) | TAIL, SHOWN_TARGET_CHARS=40 (:129) | "..." prefix | OUT (not the class: no ASCII step) |
| 12 | source_split::_ascii (837) | -- | -- | -- | -- | a plan CHECK: refuses R9 when `not piece.isascii()`, returns None | -- | -- | OUT (non-goal; not a sanitizer) |

Rows 1-4 are the same body (strip -> ctrl removed -> "?" -> head cut) and differ only in the default cap. Row 5 is
that body minus the encode step. Row 6 is that body with three switches (None -> "", no strip, ctrl -> " "). Rows 7-8
are one body (`str(v).encode("ascii","backslashreplace").decode("ascii")`) with no strip, no ctrl, no cap.

Ordering facts the survivor must keep (they change bytes if moved):
- strip runs BEFORE ctrl removal: `"\x00 a"` -> `" a"` (a leading space survives); `str.strip()` also removes
  `\x1c-\x1f`, `\x85`, `\xa0`, `\u3000` at the edges BEFORE they would become "?" -- in the middle `\xa0` -> "?".
- the cut runs LAST, after replacement; replacement is 1:1 per code point for "?" and for removal-free paths, so the
  cut counts output characters.

## 3. AR-15 change check: every site of the PROBLEM (not of the helper)

Inline sites found by `Grep "split\(\)\)\[:\d+\]|\.encode\(["']ascii["'], *["'](replace|backslashreplace|ignore)["']\)"`
over `tools/[!t]*.py` plus the def grep (section 9). None of them is a named member; each is returned in F9:
- journal_echo.py:273 and tier_echo.py:108 (`_transcripts_off_line`), permission_audit.py:129: `" ".join(str(exc).split())[:40]`
  then "?" -- whitespace COLLAPSED to one space, other ctrl (`\x00-\x08`) kept, cap 40. A "comment-named copy" class with
  agent_budget.py:72 and dispatch_gate.py:351 (those two do no ASCII step). permission_audit is "a kit file, installed
  alone" (permission_audit.py:112, :127) -- it cannot import a sibling helper.
- test_quarantine.py:82 `_say`: a whole-output CLI writer, "?" only, no strip, no ctrl, no cap (multi-line by design).
- ci_read_common.py:38 `sanitize` (allowlist `[A-Za-z0-9 _./:()=,'\[\]-]`, else "?") and :47 `sanitize_own` (non-printable
  -> "?", printable non-ASCII KEPT): a different contract (remote-text allowlist), OUT.

## 4. The survivor

Home: `tools/ascii_line.py` (absent today: Lead's fact `Grep def ... tools/*.py`, 18.11; my Glob agreed). Stdlib only
(`re`), a leaf: imports nothing from tools/.

```
def clip(value, max_len, *, errors="replace", control="", strip=True, none=None) -> str
```

Steps, in this order (the order of rows 1-6):
1. `text = none if (value is None and none is not None) else str(value)`
2. `if strip: text = text.strip()`
3. `if control is not None: text = CTRL_RE.sub(control, text)` with `CTRL_RE = re.compile(r"[\x00-\x1f\x7f]")`
4. `if errors is not None: text = text.encode("ascii", errors).decode("ascii")`
5. `return text if max_len is None else text[:max_len]`

Argument checks (run first, on every call, whatever the input):
- `errors` must be one of `"replace"`, `"backslashreplace"`, `None` -> else `ValueError` (invariant: a mistyped handler
  cannot hide until the first non-ASCII value reaches a hook).
- `max_len` must be `None` or an int >= 0 -> else `ValueError` (invariant: a negative cap never silently becomes a
  TAIL cut by Python slicing). No call site passes a negative or a non-int (section 5 caps are literals or positive
  module constants -- `estimate`: the constants' values were not all read; the builder reads each and lists it).
- `max_len` has NO default: every call names its cap or `None` (invariant: a hook line never loses its cap silently;
  a call that forgets it is a TypeError the tests see, not an uncapped line).

Profiles (keyword sets; the defaults ARE the replace profile):

| profile | members | keywords |
|---|---|---|
| replace | rows 1-4 | (defaults) |
| keep | row 5 (F5) | `errors=None` |
| reaper | row 6 (F3) | `control=" ", strip=False, none=""` |
| escape | rows 7-8 (F4) | `max_len=None, errors="backslashreplace", control=None, strip=False` |

## 5. Call sites per file (Grep of the call form, 18.11.2026; "calls (lines)")

| file | symbol | calls (lines) | default-cap calls that must gain an explicit cap |
|---|---|---|---|
| tools/session_context.py | _ascii_sanitize | 43 (42) | 11 calls on 10 lines: 653, 654, 655, 1118, 1139, 1140, 1149, 1158, 1196 (x2), 1197 -> cap 80 |
| tools/session_context.py | _ascii_content_line | 1 (1) | out (F8) |
| tools/wait_reaper.py | ascii_clip | 19 (17) | none (n is required today) |
| tools/crap_report.py | ascii_text | 13 (9) | none (uncapped) |
| tools/wiring_check.py | _ascii_safe | 13 (13) | none (uncapped) |
| tools/escape_check.py | _ascii_safe | 32 (23) | out (F7) |
| tools/tier_echo.py | _ascii_sanitize | 2 (2) | 2: 219, 226 -> cap 80 |
| tools/journal_echo.py | _ascii_sanitize / _raw_sanitize | 1 (1) / 1 (1) | none (:896 passes PEER_NOTE_MAX to both) |
| tools/coordinator_rules.py | _ascii | 1 (1) | none (:74 passes 160) |
| tools/hygiene_gate.py | _clip | 1 (1) | out |

Test files that name a member directly (readers, section 8): test_session_context.py 5 lines (858-867),
test_journal_echo.py 8 (358-401), test_journal_echo_r3.py 6 (591-719, `_raw_sanitize`), test_wiring_check.py 6
(1169, 1173, 1262, 1282, 1396, 1397). No other module calls a member across modules (Grep
`\w+\.(ascii_clip|ascii_text|_ascii_safe|_ascii_sanitize|_ascii|_clip|_raw_sanitize|_ascii_content_line)\b`: only test
files and a journal_echo docstring; positive control: the same call found the test_wiring_check lines).

## 6. How acceptance proves "byte for byte"

TESTING.md «Что не пишется» bans a committed «Как раньше» test ("a helper behaves like the code it replaced"). So the
old-vs-new proof is an ACCEPTANCE WITNESS, not a test (conflicting-pair edge E11):
- W1 equivalence run (scratch script, FULL source and output in the builder's report, never committed): for each IN
  member, extract the OLD function body from `git -C <worktree> show origin/main:tools/<file>` by AST name, exec it with
  `re` in scope, and compare `old(x, cap)` with the NEW binding the file now uses, over the battery
  {`""`, `"   "`, `"abc"`, `" a b "`, `"\x00 a"`, `"a\nb\r\nc\td"`, `"\x7f"`, `"\x1b[31mred"`, `"\x85x\xa0"`, `"\xa0a\xa0"`,
  `"café"`, `"дом"` (as `\u` escapes in the script), `"\U0001F600"`, `"\ud800"`, `"a"*1000`, `"x"*79/80/81`, `None`, `5`,
  `ValueError("é\nboom")`, `b"by"`, `["é"]`} x caps {0, 1, 20, 40, 60, 80, 100, 120, 150, 160, 200, 240, 300, 500}
  (rows 7-8: uncapped). Output: one line per member `<file>::<symbol> mismatches=0 cases=N`.
  NEGATIVE CONTROL in the same run: the reaper binding with `control=""` must report mismatches > 0.
- W2 call-site caps: every default-cap call of section 5 carries the OLD default (80) explicitly; the critic reads the
  13 lines in the diff; the per-file call count after the change equals the section 5 count.
- W3 the hook-level tests that already pin these lines stay green (DoD run 2).

## 7. Builder card (one node: FG7-56 and FG7-61 land together)

given: this card; the bodies at section 2 lines; `docs/TESTING.md` («Бюджет», «Что не пишется»); `tools/mechanism_gate.py::MECHANISM_PREFIXES`
owns:
C:/QAFactory/forge-repo/tools/ascii_line.py
C:/QAFactory/forge-repo/tools/test_ascii_line.py
C:/QAFactory/forge-repo/tools/crap_report.py
C:/QAFactory/forge-repo/tools/coordinator_rules.py
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/journal_echo.py
C:/QAFactory/forge-repo/tools/tier_echo.py
C:/QAFactory/forge-repo/tools/wiring_check.py
C:/QAFactory/forge-repo/tools/wait_reaper.py
C:/QAFactory/forge-repo/tools/mechanism_gate.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/tools/install_parity_anchors.json
(the last two only per F10 / F11; test_session_context.py, test_journal_echo.py, test_journal_echo_r3.py,
test_wiring_check.py join owns only if F6 = (a))
non-goals: escape_check.py, hygiene_gate.py, source_split.py, ci_read_common.py, permission_audit.py, test_quarantine.py
unless a fork moves them in; no change to any hook line's text; no new axis heading unless F10 = (b); no `.githooks/` edit.
handoff: the branch with commits A and B (below), the report with W1 source + output, W2 list, the DoD run tail.
edges: E1-E12 (section 7.1)
DoD: `python -m pytest tools/test_ascii_line.py -q` ; `python -m pytest tools/test_session_context.py tools/test_journal_echo.py tools/test_journal_echo_r3.py tools/test_tier_echo.py tools/test_wiring_check.py tools/test_wait_reaper.py tools/test_crap_report.py -q -k "ascii or sanitiz or adversarial"` ; `python -m pytest tools/test_mechanism_gate.py -q -k "transitive_import_closure or every_live_settings_hook_command"`
siblings: docs/SIBLING_MAP.md axis 15 (console stream setup: "a chain link keeps its own copy" -- the precedent F1 weighs), axis 34 (one road); FG7-62 edits tools/session_context.py too (sequence the two, do not run in parallel); FG7-60 (one loader) -- unrelated files.

Acceptance criteria:
1. `tools/ascii_line.py` holds `clip` exactly as section 4 (signature, step order, argument checks); stdlib only.
2. Every IN member's body is gone; each file reaches `clip` by the road F2 / F6 decide; docstrings that say "a copy,
   not an import" (journal_echo.py:103-108, :488-492; tier_echo.py:142-145; session_context.py:2116-2119, :2127) are
   corrected in the same commit.
3. `MECHANISM_PREFIXES` gains `"tools/ascii_line.py",  # imported by <the chain members>` in commit B (the closure test
   `test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` turns red without it).
4. W1 reports mismatches=0 for every IN member and >0 for its negative control; W2 holds.
5. The local `ascii_line` in `session_context.layer_a_lines` (:2319-2324) is renamed (closed choice C3).

test: (one parameterised test in tools/test_ascii_line.py, rows written top-down until test lines reach code lines;
the rest reported as `tests not written: <row> -- over budget`)
- test: replace profile -- `"a\nINJECTED"` -> one line, ctrl removed, non-ASCII/emoji/lone surrogate -> one "?" each, strip-before-ctrl (`"\x00 a"` -> `" a"`), cap AT (unchanged) and BEYOND (head cut), `""`/whitespace -> `""`, None -> "None", an exception object -> its str
- test: reaper profile -- None -> "", ctrl and `\x7f` -> " ", no strip, non-ASCII -> "?", cap AT/BEYOND
- test: escape profile -- ASCII identity, `\xe9` -> `\\xe9`, Cyrillic -> `\\u04..`, emoji -> `\\U0001f600`, ctrl kept, no cap
- test: argument refusals -- errors="ignore" and max_len=-1 each raise ValueError on an ASCII input
- test: magnitude -- a 1,000,000-character input with cap 80 returns 80 characters; with None returns all of it
- test: keep profile (only if F5 = IN) -- non-ASCII kept, ctrl removed, cap

Commit split (mechanism files: coordinator_rules.py :229, session_context.py :228, journal_echo.py :246, tier_echo.py
:269, wiring_check.py :275, wait_reaper.py :284, mechanism_gate.py :225, docs/SIBLING_MAP.md :220 -- all in
`MECHANISM_PREFIXES`; crap_report.py and install_parity_anchors.json are NOT):
- Commit A (builder): tools/ascii_line.py, tools/test_ascii_line.py, tools/crap_report.py (+ install_parity_anchors.json
  per F11). No chain file imports the helper yet, so the closure test stays green at A.
- Commit B (mechanism, the Lead commits with the axis block, per the brief): the six chain files, the
  MECHANISM_PREFIXES row, the SIBLING_MAP row (F10). The builder leaves B's edits uncommitted in its worktree and lists
  them with `git -C <worktree> diff --stat`; B carries importers and the prefix row together, so no commit has an
  importer without the row.

### 7.1 Edges (behaviour + the invariant it protects)

- E1 limit: cap AT -> unchanged; BEYOND -> first `max_len` chars; `None` -> no cut; `0` -> `""`. Invariant: a capped
  call never returns more than `max_len` characters; an uncapped call never cuts.
- E2 cut marker: none is added by any profile. Invariant: no member's line gains bytes ("..." stays hygiene_gate's own).
- E3 non-ASCII: replace -> one "?" per code point (C1, surrogates, astral included); escape -> backslash form; keep ->
  unchanged. Invariant: in the replace/reaper/escape profiles no output character is above `\x7f`.
- E4 control: removed / " " / kept per profile; `\t \n \r` are in the class. Invariant: replace, keep and reaper
  outputs never contain `\n` or `\r` -- no injected second hook line.
- E5 None: "None" by default; `none=""` in the reaper profile. Invariant: no member changes how it prints None.
- E6 non-str: `str(value)`; a `__str__` that raises propagates. Invariant: the helper never turns an exception into a
  fake line (callers' own boundaries stay the only fail-open).
- E7 order: strip -> ctrl -> encode -> cut. Invariant: section 2 ordering facts hold for every row.
- E8 empty / whitespace-only -> `""` (replace, keep); reaper keeps whitespace as is.
- E9 argument checks (section 4). Invariant: they refuse only inputs no call site passes (W2 lists the caps).
- E10 TEMPORAL: today `tools/ascii_line.py` is absent and no file imports it; commit A creates it; commit B makes the
  chain import it and adds its MECHANISM_PREFIXES row in the same commit. The world where a chain file runs WITHOUT the
  helper (a host install, a partial copy) is F2's question. Invariant: no commit leaves an importer outside the net.
- E11 conflicting pair: "byte for byte" vs TESTING «Как раньше» -> W1 is an uncommitted witness, not a test. Pair
  "byte for byte" vs E9 -> E9 refuses only never-passed values.
- E12 POSITIONAL / name: a function that calls the helper must not bind the name `ascii_line` locally (it would
  shadow the module: UnboundLocalError). Invariant: `layer_a_lines` keeps working after the rename (C3).

## 8. Readers of every touched file (designer rule 7)

The `owns_readers` block was NOT attached to the brief. `estimate, not verified` -- the Lead runs:
`python -B tools/owns_readers.py --paths tools/ascii_line.py tools/session_context.py tools/journal_echo.py tools/tier_echo.py tools/coordinator_rules.py tools/wiring_check.py tools/wait_reaper.py tools/crap_report.py tools/mechanism_gate.py docs/SIBLING_MAP.md tools/install_parity_anchors.json --names _ascii_sanitize _raw_sanitize _ascii ascii_clip ascii_text _ascii_safe MECHANISM_PREFIXES clip`
and the plan critic answers its lines (Q13 (d)). My hand grep, with commands in section 9:

| touched file | reader | answer |
|---|---|---|
| tools/ascii_line.py (new) | the IN members; tools/test_ascii_line.py | changes in this stream |
| tools/ascii_line.py | test_mechanism_gate.py closure test (AST import walk) | changes in this stream (prefix row, commit B) |
| tools/ascii_line.py | install_parity_anchors.json: hosts carry tools/session_context.py (:540) and tools/wiring_check.py (:547) | F11 |
| tools/ascii_line.py | dup/lint ratchets that scan all tools/*.py | estimate: unchanged (copies are 4-5 statements, absent from tools/dup-baseline.json -- Grep of the eight file names there found only other functions) |
| session_context.py `_ascii_sanitize` | test_session_context.py 858-867 | unchanged under F6 (b); changes in this stream under F6 (a) |
| journal_echo.py `_ascii_sanitize`, `_raw_sanitize` | test_journal_echo.py 358-401; test_journal_echo_r3.py 591-719 | same as above |
| wiring_check.py `_ascii_safe` | test_wiring_check.py 1169-1397 (6 lines) | same as above |
| tier_echo.py `_ascii_sanitize` | journal_echo.py docstring :488 only | changes in this stream (docstring) |
| wait_reaper.py `ascii_clip`; crap_report.py `ascii_text`; coordinator_rules.py `_ascii` | no cross-module reader found | unchanged |
| wait_reaper.py, coordinator_rules.py, wiring_check.py (as modules) | session_context.py lazy imports inside try (:257, :271, :1484, :1919, :1946) | unchanged road; their new import of ascii_line runs inside those try blocks |
| tools/mechanism_gate.py `MECHANISM_PREFIXES` | test_mechanism_gate.py (:931, :1041) and other readers of the list | estimate: unchanged except the closure test; count via owns_readers |
| docs/SIBLING_MAP.md | mechanism_gate axis-block reader (reads `## Axis N` headings) | unchanged under F10 (a) (a table row, no heading); every future mechanism commit changes under F10 (b) |
| tools/session_context.py | FG7-62 (BOOT BUDGET, same file) | sequence, not parallel; line text unchanged so the boot byte count is unchanged |

## 9. Forks (decisions for the Lead)

- F1 shared leaf vs kept copies. (a) chain files import `tools/ascii_line.py` (the node FG7-61 names it; precedent: tier_echo
  imports `tier_ladder`, "a leaf: stdlib only", tier_echo.py:129). (b) keep copies under a census like axis 15 ("a chain
  link keeps its own copy", SIBLING_MAP.md:362-366; journal_echo.py:103-108 states hook self-containment). Recommend (a):
  one body, the node's word; cost: one more mechanism file whose break reaches six hooks.
- F2 the world without the helper (E10) in fail-open hooks. session_context.py:132-142 makes import-time fail-open "a hard
  constraint" (N4: a failed import binds a stub that raises when called, caught by main()'s one boundary). (a) one plain
  sibling-form import everywhere (`try: from tools import ascii_line` / `except ImportError: import ascii_line`, the
  tier_ladder road); a missing helper = a traceback at SessionStart. (b) the same form, wrapped in session_context only in
  its N4 deferral (the whole context degrades to its one failure line); journal_echo and tier_echo stay plain (journal_echo
  already imports journal_validator and tier_echo plainly, :254-255); the lazily imported members need nothing (session_context's try covers
  them). (c) a fallback body when the import fails: a second copy -- not recommended. Recommend (b): it keeps each hook's
  stated failure contract; the per-file difference is the file's own written contract, which the Lead may rule a rule-6 case.
- F3 wait_reaper::ascii_clip (ctrl -> " ", no strip, None -> ""): (a) IN via the reaper profile (recommended; W1 proves bytes);
  (b) OUT, named on the axis. Converging its behaviour to the replace profile is not an option: it changes WAITS lines.
- F4 escape family (crap_report::ascii_text, wiring_check::_ascii_safe): (a) IN via `errors="backslashreplace"`
  (recommended; identical bodies today); (b) OUT -- they keep control characters and have no cap, so they are "ASCII text",
  not "a line".
- F5 journal_echo::_raw_sanitize (no ASCII step; the JSON channel): (a) IN with `errors=None` (recommended: :896 already
  branches on `ascii_only` between the two, one pipeline); (b) OUT -- a function in a module named ascii_line returning
  non-ASCII reads wrong.
- F6 how call sites reach `clip`. (a) every call site calls `ascii_line.clip(x, cap, <profile>)`; old names vanish; the
  4 test files' direct references move into the table (owns widen to them). (b) each file keeps its old NAME as a
  keyword-only binding `name = functools.partial(ascii_line.clip, <profile keywords>)`; only the 13 default-cap calls are
  edited; tests keep working. Recommend (b): smallest diff on hook lines, the profile sits on one line per file for the
  critic; cost: eight names stay for one action (no bodies). (b) needs a module-level import (ties to F2).
- F7 escape_check::_ascii_safe: (a) OUT (recommended): its contract is a quoted repr of a Python value (`ascii()`), raw for
  ASCII strings, pinned in its docstring (:323-331); the stdlib builtin is already the shared body. (b) IN with a fourth
  `errors="repr"` mode.
- F8 session_context::_ascii_content_line: (a) OUT (recommended): transliteration table, counts, keeps `\t`, never cuts,
  returns a tuple -- a boot-file renderer. (b) let it call `clip(s, None, strip=False, control=None)` for its final encode.
- F9 inline analogs (section 3). (a) OUT of this node, one finding for the "transcripts off" comment-named class
  (journal_echo:273, tier_echo:108, permission_audit:129, agent_budget:72, dispatch_gate:351 -- permission_audit cannot
  import, two have no ASCII step; NUL survives the collapse) and test_quarantine._say listed as a writer, not a line.
  (b) a `collapse=True` switch and the two in-owns sites join now (rule 2: "fixed by the card" when in reach). Recommend (a):
  a different body (collapse, not strip) and a class that spans five files, three outside this card.
- F10 the axis (AR-15: "a new survivor gets an axis in the same commit"). (a) a row in axis 15 (console stream setup,
  same problem: a non-UTF-8 console) -- recommended, no heading change; (b) a new axis 39 -- every later mechanism commit
  must answer it; (c) none.
- F11 kit hosts: hosts carry session_context.py and wiring_check.py (install_parity_anchors.json:538-551, `kind: path`);
  with F1 (a) they need tools/ascii_line.py too. (a) add a `path` row for tools/ascii_line.py (recommended); (b) nothing.
  Question: no kit builder writes `toolkit/` in this repo (Grep `["']toolkit/` over tools/scripts found only
  install_parity.py) -- who ships the kit is unknown to me.

## 10. Small choices closed by the designer

- C1 function name `clip`, module `ascii_line` (FG7-61's home); `max_len` positional without default (section 4 reason).
- C2 argument checks: `errors` limited to three values, `max_len` None or int >= 0.
- C3 rename the local `ascii_line` in `session_context.layer_a_lines` (e.g. `safe_line`).
- C4 hygiene_gate::_clip OUT: no ASCII step, UTF-8 output by design (row 11 evidence). The Lead may override.
- C5 test home: a new `tools/test_ascii_line.py` (one table, pure function, well under 10 s); TESTING.md «Файлы»: no
  existing table is about this helper; the critic judges it (rule 22, Q5). Forge tests carry no `keep` row.
- C6 the finding's line numbers are stale (session_context:1020 -> 1064 today); the copy count is 11 defs in 10 files
  plus `_raw_sanitize`, as section 2.

## 11. Reading trail (all measured by me on 18.11.2026 unless marked)

- Lead's fact: `Grep def (_?ascii|ascii_clip|_clip)` -> 11 defs in 10 files; mine (`^\s*def (_?ascii\w*|ascii_clip|_clip)\b`, -i,
  tools/*.py) -> the same 11 (coordinator_rules:37, crap_report:589, escape_check:322, hygiene_gate:1910, journal_echo:487,
  source_split:837, session_context:1064 and :2124, wiring_check:261, wait_reaper:59, tier_echo:141).
- Wider def grep `^\s*def \w*(sanitiz|ascii|clip)\w*\(` -i over tools/.githooks/.claude non-test files -> adds
  journal_echo:471 `_raw_sanitize`, ci_read_common:38/:47, judge_calib_sanitize:132 (pairs, unrelated). `.githooks/` holds
  only shell scripts (Glob: pre-push, pre-merge-commit, commit-msg, post-merge, pre-commit).
- Bodies read: each row of section 2 at its line; hygiene_gate :129, :2048-2050, :2140; journal_echo :100-115, :466-496;
  tier_echo :100-150; session_context :120-180, :1055-1076, :2110-2145, :1344-1352; ci_read_common :20-59;
  test_quarantine :76-85; permission_audit :124-131; source_split :837-840.
- Call counts: `Grep \b(<symbol>)\(` per file, content mode, lines counted by hand, def and docstring lines removed
  (session_context: 44 lines - def :1064 - docstring :2719 = 42; escape_check: 25 - def - docstring :10 = 23;
  wiring_check: 15 - def - docstring :170 = 13).
- Mechanism list: tools/mechanism_gate.py:216-296 read whole. Closure test names: test_mechanism_gate.py:931, :1041.
- Inline analogs: section 3 command, glob `[!t]*.py` (tier_echo:108 and test_quarantine:82 found by the first encode grep
  over all tools/*.py).
- Registries: `_ascii_sanitize|ascii_clip|_ascii_safe|ascii_text` over tools/*.json, tools/*.yaml, design/*.json,
  docs/*.md, scripts/*.json -> 0; positive control with `|session_context` added -> 10 hits in 4 files.
- `ascii_line` -i over tools/ -> only local variables (session_context:2319-2324, two test files); tools/ascii_line.py absent.
- Test files present: test_crap_report, test_tier_echo, test_wait_reaper, test_mechanism_gate; test_coordinator_rules.py
  absent (same Glob found the four).
- TESTING.md read :165-244; SIBLING_MAP axis 15 :355-366; architecture.md AR-15 :214-219.
- Not measured (estimates): MAX_MESSAGE_LEN value (500 from the docstring), the values of the cap constants named in
  section 4, the owns_readers block, whether the replace handler maps a lone surrogate to one "?" (W1 measures it).

## Lead decisions (18.11, Lead 501cb4e0; designer t-1384 accepted)

- F1 (a) one leaf `tools/ascii_line.py`; F2 (b) plain sibling-form import, wrapped only inside session_context's N4
  deferral (each hook keeps its written failure contract); F3 (a) wait_reaper IN via the reaper profile; F4 (a) the escape
  family IN via `errors="backslashreplace"`; F5 (a) `_raw_sanitize` IN with `errors=None`; F6 (b) each file keeps its old
  name as a `functools.partial` binding (tests untouched); F7 (a) escape_check OUT; F8 (a) `_ascii_content_line` OUT;
  F9 (a) the inline "transcripts off" collapse class goes to a finding, not this node; F10 (a) a row in axis 15;
  F11 (a) a `path` row for tools/ascii_line.py in install_parity_anchors.json (who ships the kit stays an open question,
  not this node's). All on the designer's recommendation; "решила сама".
- Commit split as section 7: commit A by the builder; commit B (six chain files, MECHANISM_PREFIXES row, SIBLING_MAP
  row) staged by the builder, committed by the Lead with the axis block.
