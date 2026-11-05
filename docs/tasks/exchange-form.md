# Exchange form between roles (forge/5 F5-2, spec t-797)

Two forms that cut the Lead's context on hand-backs and briefs without weakening trail-based acceptance (CLAUDE.md rule 1; while the scout holds no
passed exam the STRICT form R1 b applies). `.claude/agents/scout.md` rule 10 teaches the digest form; `tools/digest_form.py` reads it back;
`tools/handback_extract.py` prints the reading as one tail on its stdout line. The code only REPORTS: the report file is the worker's verbatim text.

## 1. The scout digest, form v1

The scout's FINAL MESSAGE is the digest (it has no Write). The first non-empty line is the key `digest: v1 <task_id>`. No fence around the digest.
Sections, with these exact headings:

- `## Objects` (required) -- the header is exactly `| id | kind | gist | paths | status | owner | links | ev |`.
- `## Trail` (required) -- the header is exactly `| tid | op | target | pattern / range | flags | result | control |`.
- `## Forks` (optional) -- prose; when present its LAST line is the literal `this needs a decision from a tier above.` (scout.md rule 3).
- `## Not done` (optional) -- prose: what was not checked and why (no Bash and the like).

One table per section: Objects and Trail each hold ONE table, and any other pipe line in them (a second table, a row after a prose line or a `###` heading,
an indented row, a second separator-like row) is a stray row and is flagged -- a row nobody reads is a claim nobody checked. A heading with another name is
`unknown_section`. Before the key, whole-line HTML comments and closed fenced blocks are skipped (they are not a preamble); after the key, comment and fenced
lines are blanked, so a fenced example table is never read as data and a fenced `## Trail` is not a second section. An unclosed `<!--` is flagged, and so is a fence after the key that nothing closes (`fence_unclosed`;
what follows it is not read).

### Objects: one row, one claim

- `id` -- no spaces, no commas, unique: a B-id, a finding's file name, `path:line`, `path::symbol`, or `q<N><letter>` (item N of the dispatch's question).
- `kind` -- a free word (function, claim, pin, ci, analog, ...); the reader does not check it. An analog (scout.md rule 8) is `kind: analog`.
- `gist` -- at most 20 words (`str.split()`). A fact longer than that is several objects joined through `links`; the text is never cut by code.
- `paths` -- where it lives, `path:line` or `path:from-to`. `status` -- the state of the claim; `absent` marks a NEGATIVE object. `owner` -- the owner's word or `—`.
- `links` -- ids of other objects, B-ids, `file:line` of a carrier. `ev` -- the tids of the Trail rows the claim stands on, comma separated, exact case;
  `—` or empty means NO trail.

### Trail: what was run, verbatim

`op` is `read`, `grep` or `glob`. `target` is the path or glob searched. `pattern / range` is the pattern IN BACKTICKS exactly as run (an unquoted `|`
splits the cell), or the lines read. `flags` is `—` or tokens separated by spaces (`-i`, `content`, `files`, `count`, `glob=<g>`, `type=<t>`), compared as a SET.
`result` has a closed grammar:

| op | result | a zero? |
|---|---|---|
| `grep` without `count`, `glob` | `found <n>` (n >= 1, no leading zeros), optionally `; <path:line>[, ...]` -- or `absent` | `absent` |
| `grep` with `count` | `count <n>` (n >= 0) | `count 0` |
| `read` | `read <path>:<lines>` (where the facts that carry the claim lie) | never |

Anything else (`found 0`, `0`, `0 matches`, `count 01`, free text, `count` on a grep without the `count` flag) is out of grammar: such a row is neither a
zero nor a control. A ZERO row names in `control` the tid of a row with the same `op`, the same `target`, the same set of `flags`, a DIFFERENT pattern and a
NON-zero result -- a negative proves nothing without a positive control of the same call shape (scout.md rule 4). A zero `grep` without `-i` is flagged:
the Grep tool is case-sensitive.

### Flags (what the reader reports)

`n` is the 1-based number of the data row in its table (header and separator not counted). Order: Trail rows, then objects, then markup.

| flag | meaning |
|---|---|
| `zero_no_control:<tid>` | a zero row with an empty control |
| `control_unknown:<tid>` | the control names no tid of the Trail |
| `control_shape:<tid>` | the control is the row itself, has other op/target/flags, the same pattern, or is a zero or out of grammar |
| `zero_case:<tid>` | a zero `grep` without `-i` (a pattern with no letters is flagged too: the false flag is the allowed direction) |
| `bad_result:<tid>` | the result is outside the grammar of its op |
| `dup_tid:<tid>`, `tid_space:<n>` | a repeated tid (the first row is read, the later one is not); a tid with a space inside |
| `bad_row:<Objects\|Trail>:<n>` | the cell count differs from the header (an unquoted `\|`), an empty tid, or an unknown op; the row is not read further |
| `no_id:<n>`, `id_space:<n>`, `dup_id:<id>` | an object without an id; an id with a space or a comma; a repeated id (every row is still checked) |
| `gist_over:<id>` | more than 20 words |
| `no_ev:<id>`, `ev_unknown:<id>:<tid>` | an object with no trail; a tid that is not a Trail row |
| `zero_uncontrolled:<id>:<tid>` | ANY zero row among the object's `ev` has no good control |
| `absent_no_negative:<id>` | `status: absent` and no zero row among `ev` |
| `bad_header:<section>`, `no_section:<name>`, `dup_section:<name>` | the table header is not the exact one (its rows are not read) or there is no table; Objects or Trail missing; a section twice (the first is read) |
| `stray_row:<Objects\|Trail>:<n>` | a pipe line of the section that is not the read table's header, its one separator or one of its rows (a second table, a row after prose or a `###` heading, an indented row, a second separator-like row); not read. Lines blanked as a comment or a fence are not stray |
| `unknown_section:<name>` | a `## <name>` heading after the key that is none of Objects, Trail, Forks, Not done (its lines are not read) |
| `forks_no_line` | Forks does not end with the literal line |
| `key_not_first`, `key_no_task` | something precedes the key line (reading starts at the key); the key carries no task id |
| `comment_unclosed:<line>` | a `<!--` that never closes (the 1-based line of the message): a renderer hides what follows, so the text is a hidden claim |
| `trail_unbacked:<n>` | F6-14 (t-863, 16.10): `n` Trail lines that name a read or a search the worker's OWN transcript does not hold as a `Read`/`Grep`/`Glob` tool_use (a normalised one-direction substring of the path or pattern; a root target `.` takes any) — a fabricated trail; the digest is still printed, the flag is the acceptor's signal (FR-4) |
| `trail_unchecked` | F6-14: no transcript could be read for this hand-back (a gateway scout, a missing or unreadable JSONL) — the trail was NOT checked; never read as backed |
| `fence_unclosed:<line>` | a ``` / ~~~ fence after the key that nothing closes (the 1-based line of the message): every line after it is hidden and NOT read, so the text is a hidden claim. The one fence that is not flagged is the container -- the digest wrapped in a fence whole (the key inside it, `key_not_first`): its closing fence is the LAST non-blank line of the message, blank lines after it do not matter |

A name in a flag without an id (an object with no id) is `#<n>`. In `stray_row` `n` is the 1-based line number inside the section, its `## ` heading being line 1. `handback_extract` appends to its one stdout line, after `finished=`:
` digest=v1 objects=<n> trail=<n> flags=<n>[ first=<flag>]`, or ` digest=none` (no key: today's prose, extracted as prose), or ` digest=n/d` (the
reader failed to import or raised: the file and the exit code are as without it).

### Example: the t-794 report in form v1

An example, not a measurement. It is longer than the prose original because it carries back the facts the first rewrite dropped. The expected flags are
exactly `["control_shape:G8", "zero_uncontrolled:q3b:G8"]`: the control of G8 in the original is a direct read of the file (report line 37), and the form
makes that visible. Of the ten searches the original lists (nine Greps bullets, the `test_ci_layout.py` grep sits inside one of them) exactly two that carried no match count (`decide_merge` repo-wide, `B-454`/`B-426` in plans) are not carried over; the grep in
`tools/test_ci_layout.py` (G10) is, because the claim q3a stands on it.
`tools/test_digest_form.py` reads THIS block as its fixture.

```
digest: v1 t-794
## Objects
| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| q1 | function | `decide_merge` split by B-426 D9 `257c0617`; 90 lines, 45 of them docstring; depth 1, no loops | tools/journal_validator.py:1492-1581 | done | — | B-426, t-625 spec:31 | R2,R3,R4,G1 |
| q2a | claim | a list/dict `event` passes the isinstance checks (:692, :724 do not return) and reaches `in` at :733, :743 | tools/journal_validator.py:677,692,724,733,743 | open | — | B-454, t-507 handoff:124 | R4,G4 |
| q2b | claim | only `event` is confirmed as raising; `by` uses a tuple test (:624), no raise; `task_id` not traced | tools/journal_validator.py:624 | not verified | — | q2a | R4 |
| q2c | claim | the merge path reaches it via `_foreign_line_violations` :1273 → :1291, no try/except around | tools/journal_validator.py:1273,1291 | open | — | q2a | R4 |
| q2d | claim | main() :2178-2188 turns it into a traceback, exit 2: not a named refusal, `merge-accepts:` cannot clear it | tools/journal_validator.py:2178-2188 | open | — | q2c | R4,G9 |
| q2e | pin | no list/dict value of event, task_id or by among the 14 A8 fixtures or any test | tools/test_journal_validator_merge.py:630-663 | absent | — | q2a | R5,G5,G6 |
| q2f | pin | `[1,2,3]` is pinned as a non-object line violation (:632, :680) and never reaches :733 | tools/test_journal_validator_merge.py:632,680 | present | — | q2e | R5 |
| q3a | ci | forge-check runs `--all --base` with two fallbacks; test_ci_layout.py:49-55 pins the three lines | .gitlab-ci.yml:61-68 | present | — | — | R6,G10 |
| q3b | ci | `--merge-parent` is absent from CI; only the local pre-merge-commit hook runs it | .githooks/pre-merge-commit:18 | absent | decision needed | — | G8,R7 |
| an1 | analog | the unhashable class is pinned for journal_echo, not for the validator | tools/test_journal_echo_noteslen.py:329 | present | — | q2e | G7 |
| an2 | analog | the controller names the same class with a named refusal | ai-packages/qa-factory/scripts/controller.py:3013 | present | — | test_controller_rework.py:816 | G7 |
## Trail
| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| R1 | read | plans/piles/forge/findings/20261009-b-454-ostatok-ne-proveren.md | all | — | read plans/piles/forge/findings/20261009-b-454-ostatok-ne-proveren.md:all | — |
| R2 | read | plans/BACKLOG.md | 574, 587 | — | read plans/BACKLOG.md:574,587 | — |
| R3 | read | plans/piles/forge/batch-4-package-clones.md | 34, 56-58 | — | read plans/piles/forge/batch-4-package-clones.md:34,58 | — |
| R4 | read | tools/journal_validator.py | 640-760, 1176-1205, 1273-1330, 1380-1840, 2170-2191 | — | read tools/journal_validator.py:624,677,692,724,733,743,1273,1291,1492-1581,2178-2188 | — |
| R5 | read | tools/test_journal_validator_merge.py | 595-710 | — | read tools/test_journal_validator_merge.py:630-663,632,680 | — |
| R6 | read | .gitlab-ci.yml | 1-120 | — | read .gitlab-ci.yml:61-68 | — |
| R7 | read | .githooks/pre-merge-commit | all | — | read .githooks/pre-merge-commit:18 | — |
| G1 | grep | tools/ | `def decide_merge` | content | found 1; tools/journal_validator.py:1492 | — |
| G4 | grep | tools/journal_validator.py | `MODEL_REQUIRED_EVENTS|unhashable|TypeError` | content | found 7; :257, :324, :733, :879, :1095, :1187, :1263 | — |
| G5 | grep | tools/ | `unhashable|TypeError|hashable` | -i content glob=test_journal_validator*.py | absent | G5c |
| G5c | grep | tools/ | `non-?string|...` | -i content glob=test_journal_validator*.py | found 2; test_journal_validator.py:175, test_journal_validator.py:1517 | — |
| G6 | grep | tools/ | `event=\[|event=\{|"event": ?\[|"event": ?\{|task_id=\[|task_id=\{|by=\[|by=\{|"by": ?[\[{]|"task_id": ?[\[{]` | -i content glob=test_*.py | absent | G6c |
| G6c | grep | tools/ | `worker_ref=123|"event": ?"delegate"|event="delegate"` | -i content glob=test_*.py | found 2; test_journal_validator_merge.py:644, test_journal_validator.py:177 | — |
| G7 | grep | . | `unhashable|hashable` | -i content glob=*.{py,md,sh} | found 4; test_journal_echo_noteslen.py:329, controller.py:3013, test_controller_rework.py:816, t-507 handoff:124 | — |
| G8 | grep | .gitlab-ci.yml | `merge-parent|merge_parent` | -i count | count 0 | R6 |
| G9 | grep | tools/journal_validator.py | `except Exception|sys.exit(2)|return 2` | content | found 3; :1646, :2186, :2188 | — |
| G10 | grep | tools/test_ci_layout.py | `forge-check|merge-parent|journal_validator` | content | found 7; :28, :31, :49, :53, :55, :138, :350 | — |
## Forks
Whether q2a becomes a node of forge/5 or a finding; whether the `--merge-parent` half of q3b belongs in CI.
this needs a decision from a tier above.
## Not done
No Bash: no `git log` of tools/journal_validator.py, no live run of the TypeError (exit 2 inferred from :733 and main()).
```

## 2. The brief, form v1

A brief from the Lead to a role is the R11-f header lines (`given:`, `owns:`, `non-goals:`, `handoff:`, `edges:`, `DoD:`) plus at most N = 8 counted lines of
prose (a calibration target, not a gate; WARN in `dispatch_gate` only after a measured leak). The prose is every line of the WHOLE dispatch text that is not
empty, not inside a fence or a quote, not a `manifest-skip:` line and not a manifest line (a section header and the lines under it up to the first empty
line); each prose line counts with `handback_extract.count_lines`. If the cut is degraded, everything outside the manifest is prose.

- FACTS go by POINTER: `given:` names the frozen file (a hand-back report, a digest) and the digest's objects by their EXACT ids (`q2a, q2b`), never by a prefix
  (`q2 *`). A reservation of the scout (`not verified`) travels with the object id, so the brief does not restate it and cannot lose it.
- Code that changes is pointed at by `path::symbol`, not by a line range (the range drifts).
- The DoD, the edges and the non-goals stay INLINE (rule 11: a bare pointer is not a DoD). Only facts become pointers.

### Example: the t-795 dispatch, rewritten

The original carried about 12 counted prose lines and dropped the scout's reservation "only `event` confirmed"; here it arrives as the pointer to q2b.

```
Task t-795 — forge/5 F5-9 item 2. Facts by pointer: digest t-794, objects q2a, q2b, q2c, q2d, q2e, q2f (given; the q2b
reservation stands until you trace `by` and `task_id`). Worktree off 0455845b; tools/*.py are mechanism paths: stage only.
Work: (1) a non-string event/task_id/by is a final named violation on both paths, no `in` test on it; (2) three A8 fixtures
+ the same three as own lines; (3) one mutation per path; (4) the journal_echo agreement line.

given: D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-794-b-454-residue.md, D:/ws1/yml-text-factory\tools\journal_validator.py::_line_form_violations
(then the manifest lines for owns, non-goals, handoff, edges and DoD, inline, as in the original)
```
