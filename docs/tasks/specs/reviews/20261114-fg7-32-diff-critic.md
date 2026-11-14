# t-750 — code critic, FG7-32 (order-known door), uncommitted diff in worktree fg7-32

Reviewed: `git -C C:/QAFactory/forge-repo/.claude/worktrees/fg7-32 diff` (tools/journal_validator.py +112/-6,
tools/test_journal_validator.py +63, PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md +9). DoD: the 8 inline items of the
t-750 dispatch. One pass, no code edited, no CI.

**Verdict line: NEEDS WORK (fit_with_fixes) — 1 blocking finding (B1), closed by a small fix round; 3 fixes this round, 2 queue lines.**

## Headline

B1 — a REGRESSION on the real journal. The real root journal `logs/journal/dev1.jsonl` (179 uncommitted lines over
HEAD = origin/main `ef0bdf4`) passes the PRE-diff validator with 0 violations. The diff makes it fail with 2
refusals. Neither refusal is an order defect: both are lines whose notes MENTION the token's form in prose
(`order-known:<ts>`): the t-746 dispatch_skipped and delegated lines at 1817 and 1818, the dispatch of this very
node. The cause is `ORDER_KNOWN_RE = (?<!\w)order-known:(\S*)` (journal_validator.py:368). It accepts any
non-blank run as a ts. The "names no line" branch (journal_validator.py:465) then REFUSES it. The door that refusal
names ("copy the ts exactly, put the token on a LATER line") cannot fix a prose mention, so it breaks FR-2 and
AR-9. That is the exact class the finding exists to remove: a refusal with no usable door. The comment at
journal_validator.py:367 says this is "the same parse as `closes:`". That is false: `journal_keys.CLOSES_RE`
(journal_keys.py:83) is shape-gated (`closes:(t-\d+)…`), so a prose `closes:<task-id>` is never a token.

## Key 1 — DoD items 1-8

| # | Status |
|---|---|
| 1 token form, several per notes, bare-run parse | built, but the parse is wider than the neighbour's (B1): `closes:` reads a value of its shape only, while this reads any `\S*`. Trailing punctuation (`order-known:<ts>,`) is read into the value and refused as "names no line" (probe J). That direction is safe, and it matches `replaces_worker:` |
| 2 three declarable defects, new lines only, later line, no self, earlier does not count, HEAD unjudged | built as written. Marks sit at exactly three sites: 9a novelty (l.1110), 9c/d repeat (l.1200), rule 10 monotone (l.1232). Declaration needs `q > fi` (strictly later). HEAD tokens can never declare, because marks are new lines and the carrier must be later. Probes A-E |
| 3 declared drops, undeclared refuses with line/ts/task_id/defect/expected/exact token, one refusal per line | built. The door is APPENDED to the original text, so the original reason stays (probes A1/B1/C1). "One refusal per line": a line with BOTH an id and a ts defect gets two texts, one per defect. That is acceptable: each text names its defect |
| 4 names-no-line refuses / clean line WARN / shared ts covers both | built. The WARN wording for a token naming a HEAD line ("carries no order defect", probe D) states something unverified: HEAD lines are never judged. Fix F3 |
| 5 empty token → WARN, notes non-string → base check | built (table row edge5). But only the EMPTY value is treated as not-a-token. A non-ts value is refused (B1) |
| 6 another file never declares | built: tokens are collected from head+new of THIS file only, and the seed is excluded (row edge6) |
| 7 count printed in the summary; one calibration check | built DIFFERENTLY, and the difference is wrong. DoD: "count of declaring TOKENS". Built: the count of declared DEFECTS (`declared += 1` per mark, l.448). One token over a line with two defects prints `2 declared` (probe F). One token over two lines sharing a ts prints 2 (table row edge4-two-lines). The summary text says "defective lines", and 13(m) says "the number of tokens": three different quantities under one name. Fix F2 |
| 8 nothing else declarable; closes/replaces_worker/id_band/merge unchanged | built for the defect set: reopen-closed, fabricated replaces_worker, orphan accepted, future ts, typed fields and by/basis all stay refused (probes G, H, I). `--merge-parent`: the door also reaches the merge TAIL, because `decide_merge` calls `validate_new_lines` (l.1863). That is the one-road behaviour (P31), and right. But the count is not printed in merge or `--all` mode (queue Q1) |

## Key 2 — direction of error

- No pass beyond the three defects. Marks are tied to violation INDICES. Only the order texts are dropped, and every
  other violation of the same line survives:
  - probe H: id defect + missing `worker_ref` + token → still refused on `worker_ref`;
  - probe G: future ts, unknown `by`, missing witness → all still refused; a token naming the future-ts line is a WARN;
  - probe I: reopen-closed + token → still refused.
  - append-only (`check_append_only` runs before), id_band placement (`_band_place_text`, not marked) and
    cross-clone novelty (the merge-mode embed checks) are all unmarked.
- ONE token CAN silence several ORDER defects: the id and ts defects of one line (probe F), and every new line that
  shares the ts and stands before the token. This is DoD 4 as written. It is not wider than the three defects.
- The same-commit token makes the gate a no-op for ordering BY DESIGN. HEAD lines are never judged, so every judged
  line is new. In practice the door only ever applies to new lines, including one written a second ago. That is
  the informed pass of FR-4, wider than the finding's wording ("old lines of the same writer"). It was decided by
  the Lead in DoD 2, not invented by the builder. Its detector is the count. The validator's summary line goes to
  stderr only and persists nowhere, so the REAL weekly carrier is the grep over `logs/journal/*.jsonl` that 13(m)
  also names. B1 pollutes that grep with prose mentions. Fix F2 says the grep is the carrier.

## Key 3 — empirics (worktree validator, `decide_with_warnings`, HEAD = one line t-001 @08:00, now 23:00)

Script: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\t750\probe.py`.
Outputs, abridged; the door suffix is verbatim once:

```
=== A1 id out of order undeclared: code=1
  V: line 2 ... task_id novelty violated -- got t-005; the next new id is t-002 ... (rules 9a, 9e) -- ORDER DEFECT (task id issued out of order) on the journal line with ts '2026-07-10T09:00:00', task_id 't-005': if the line is already written and cannot be edited, declare it -- expected: a LATER line of this same file whose notes carry the token `order-known:2026-07-10T09:00:00`; append a new line with that token in its notes, then commit again (rule 19)
=== A2 id out of order declared: code=0
  W: order-known: 1 declared (...)
=== B1 ts not monotone undeclared: code=1   (rule 10 text + ORDER DEFECT (ts not monotone ...) `order-known:2026-07-10T07:00:00`)
=== B2 ts not monotone declared: code=0   W: order-known: 1 declared
=== C1 dup delegated undeclared: code=1   (9c text + ORDER DEFECT (repeated delegated ...) `order-known:2026-07-10T10:00:00`)
=== C2 dup delegated declared: code=0   W: order-known: 1 declared
=== D token naming a HEAD line: code=0
  W: line 2: WARN `order-known:2026-07-10T08:00:00` names a line that carries no order defect -- nothing was declared
=== E self-declaring line: code=1
  V: ... ORDER DEFECT (task id issued out of order) ... `order-known:2026-07-10T09:00:00` ...
  V: line 2: `order-known:2026-07-10T09:00:00` names no line -- no line of this journal that stands before line 2 has the ts ...
=== F two defects (id + ts) one token: code=0
  W: order-known: 2 declared (...)
=== G order defect + future ts + bad by, one token: code=1
  V: line 3 ... 'witness' is required ...
  V: line 3 ... by='claude-opus' is not a known tier ...
  V: line 3 ... ts '2026-07-10T23:30:00' is later than now+10min ...
  V: lines 4, 5 ... later than now+10min ...
  W: line 4: WARN `order-known:2026-07-10T23:30:00` names a line that carries no order defect
  W: order-known: 1 declared
=== H order defect + missing worker_ref, one token: code=1
  V: line 2 ... 'worker_ref' is required ...
  W: order-known: 1 declared
=== I reopen closed task + token: code=1
  V: ... 'witness' is required ...;  V: ... delegated on a CLOSED task 't-001' ...
  W: line 4: WARN `order-known:...09:00:00` names a line that carries no order defect
=== J token with trailing comma: code=1   V: ...ORDER DEFECT...;  V: line 3: `order-known:2026-07-10T09:00:00,` names no line ...
=== K `xorder-known:` (prefix in a word): code=1   (only the undeclared defect; not read as a token — the boundary works)
=== L ts cascade: line 3 at 08:30 after 09:00 blamed (pre-existing rule-10 behaviour, not this diff)
```

Control re-run of the mechanical layer:
`( cd C:/QAFactory/forge-repo/.claude/worktrees/fg7-32 && python -m pytest tools/test_journal_validator.py -q -k order_known )`
→ `15 passed, 158 deselected in 0.46s`. This matches the report's 15 table rows. The 494-pass 4-file run was not
re-run (69 s; it is consistent with the diff: the door is appended, so no existing text changes).

## Key 4 — refusal text (FR-1 / FR-2 / AR-9)

- The order-defect suffix names: the line (through the original `line N event= task_id=` tag and the ts/task_id
  again), the defect, what was expected, and the exact token. The original reason stays first.
- It is true for all three defects, with one nuance on the ts defect: rule 10 blames the line AFTER a forward jump,
  not the jumped line (probe L). The declared line is the one rule 10 flags, so the token the text gives does clear
  it. The text is true.
- The "names no line" text is FALSE as a door when the value is not a ts at all (B1).
- The HEAD-line WARN text claims "carries no order defect" about a line that was never judged (F3).

## Key 5 — journal_echo

- `journal_echo.py:2372` calls `decide(disk_text, head_text, ...)` and gets the violations only.
- At the write moment of a defective line it warns WITH the door text. That is the right moment: the writer learns
  the exact token.
- Once the token line is on disk, the defect is dropped and the echo goes silent. That is right: a declared defect
  is not a defect to repeat.
- Empty-token WARNs and the count do not reach the echo. That is harmless: the ignored token leaves the defect a
  violation, which the echo does show.
- Side effect of B1: the two prose-mention lines in the live dev1 journal will be echoed as violations on EVERY
  journal write until they are committed. They cannot be committed at all.

## Key 6 — the real case (dev1.jsonl, READ ONLY, copy in the scratchpad)

- Checks first:
  - `git merge-base --is-ancestor ef0bdf4 HEAD` → yes.
  - `cmp HEAD:dev1 == origin/main:dev1` → equal.
  - HEAD has 1648 lines and the working file 1827: **179** new lines, not "several hundred" (the dispatch's
    figure is not borne out).
  - No `continues` field, so seed = None.
- Run: `_developer_file_result("logs/journal/dev1.jsonl", cur, head, None, now, slug="dev1", known_labels={"main","dev1"})`.
  That is the same function `_check_developer_files` calls per staged file in the pre-commit gate (deviation: the
  pure path, not a temp git repo; the git reads are only `get_staged_text` / `get_head_text`, replaced by the two
  texts).
- Script: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\t750\real.py`.

```
NEW validator:  violations: 2 warnings: 0
  2 token names no line
  * line 1817: `order-known:<ts>)` names no line -- ... has the ts '<ts>)' ...
  * line 1818: `order-known:<ts>` names no line -- ... has the ts '<ts>' ...
OLD validator (git show HEAD:tools/journal_validator.py + journal_keys.py, same call):
  OLD validator violations: 0 warnings: 0
```

- Order refusals: **0**, of any of the three kinds. No other refusal kind either. Today nothing blocks committing
  the root journal except what this diff adds.
- The finding's premise ("the gate refuses because of OLD lines") does not hold under the current code. The
  builder's own probe (report §"Earlier finding") agrees: HEAD lines are never judged, and `ef0bdf4` already
  committed the 13-14.11 lines.
- For the Lead: the door is still useful for NEW defective lines that cannot be rewritten in good faith. But no
  journal in the repo needs it right now. The owner question in the finding ("how dev1 is committed before the
  door") is answered by measurement: it commits as is with the HEAD validator.

## Key 7 — tests and the calibration text

- Tests: ONE parameterised table (15 rows), and the ids name the case (`id-not-declared`,
  `edge4-token-on-the-defective-line-itself-does-not-count`, ...). Every refusal row asserts `order-known:<ts>` in
  the text. This conforms to docs/TESTING.md (a table of cases, no test per line).
- Missing rows:
  - (a) a non-ts token value: the real-data case of B1;
  - (b) one token over a line with two defects: the count semantics of F2;
  - (c) a line with an order defect AND a non-order defect plus a token stays refused. This pins the direction of
    error from key 2.
  - Add them in the fix round (F1/F2).
- Calibration 13(m): placed as the last letter of check 13, after (l), in English.
- Wording defects of 13(m):
  - it calls the stderr summary line a weekly source, but the line is not persisted;
  - it counts "tokens" while the summary counts defects (F2).
- Rewrite the first sentence so the persisted grep is THE carrier and the summary is the at-commit echo of the
  same number.

## Key 8 — DUPLICATION AND CONSISTENCY / CODE QUALITY

DUPLICATION AND CONSISTENCY: one finding.
- The token reader is a third regex beside `REPLACES_WORKER_RE` (journal_validator.py:357, `\S+`) and
  `journal_keys.CLOSES_RE` (journal_keys.py:83, shape-gated). It is not a copy of either: it is a new rule and a
  LOOSER one than the `closes:` reader it claims to mirror (l.367 comment). That looseness is B1.
- Where it lives: `closes:` and the node reader live in `journal_keys.py` (axis 1's token readers). `replaces_worker:`
  lives in the validator, which is precedent for keeping this one there. Moving it is not required while the
  validator is its only code reader (13(m) reads by grep): queue Q2, only if a code reader ever appears.
- Grepped: `order-known` case-insensitive over the worktree → hits only in journal_validator.py (15),
  test_journal_validator.py (11), the protocol (4) and the report (6). That is also the positive control: the same
  call finds the known sites. There is no second reader.

CODE QUALITY: two minor findings.
- (i) The mark tuple carries `tag` (6th field), and `_resolve_order_known` never reads it (unpacked as `tag`, then
  unused): dead data. Drop it with F2.
- (ii) `_mark` binds to `len(violations) - 1`, a positional coupling: it is correct only because each call sits
  right after its `append`. It holds at all three sites (traced l.1109-1110, l.1193-1200, l.1223-1232). A comment
  saying "call right after the append" is enough.
- `_resolve_order_known` is ~45 lines with ≤3 nesting levels; no function is over the cap.
- The clone ratchet was not run here: it is CI's deterministic layer.

## Key 9 — SIBLING_MAP axis 1 and rule 10

The same commit should carry a sentence in the `CLAUDE.md` "Routing log" section. Today the policy says
"Old events are never rewritten", and the SHAPES `delegated` row says a repeat "is legitimate only as" the three
reasons. The gate now has a fourth state (declared), which the policy does not name. Proposed, after the
`closes:<task-id>` sentence:

> An already written order defect (id out of order, non-monotone `ts`, repeated `delegated`) is declared, never
> rewritten: a bare `order-known:<ts>` (that line's exact `ts`) in the `notes` of a LATER line of the same file (validator rule 19; check 13(m)).

Then `python tools/agents_md.py` to regenerate AGENTS.md (pre-commit runs `agents_md.py --check`).

Other sites, judged:
- the session-start hook (`session_context.py`): n/a. It reconciles open dispatches through `closes:` and never
  reads order.
- `journal_keys.py where`: n/a. It prints the next id, and the novelty text already points to it.
- the role files: n/a. No role but Lead writes the journal.

Axis lines that are NOT n/a (rule 10 (b)):
- axis 1: covered by the CLAUDE.md sentence + AGENTS.md regeneration (fix F4);
- axis 17 (detector verdict shape): covered. The door is appended to the same violation strings, with one output
  shape and one reader;
- axis 34 (one road): covered for the declaration. The door works alike in the commit gate, the echo and the merge
  tail. Queued for the COUNT, which prints only in the commit path (Q1).

Rule 10 (c) detector: check 13(m), the grep. (d) on the path: pre-commit `journal_validator.py` and the echo.
The package AR/FR gates do not apply: tools/ is outside the package. JUDGMENT (Q11): none moved. The token is a
shape-and-join data check. ONE ROAD (item 12): no exclusion found.

## Blocking finding

B1 — tools/journal_validator.py:368 (`order-known:(\S*)`) with :465: a prose mention of the token form is
refused as "names no line". Measured on the real dev1 journal: 0 → 2 refusals that no appended line can clear.

## Fixes this round

- F1. Read a token value as a ts only when it matches `TS_RE`. A non-empty value that does not match (`<ts>`,
  `<ts>)`, a malformed ts) gets the empty-token treatment: a WARN, ignored. This keeps the direction of error: an
  ignored token never declares, so the defect it meant stays refused. Fix the l.367 comment ("the same parse as
  `closes:`" → "shape-gated like `closes:`"). Add table rows: `<ts>` in prose → WARN with code 0; a ts-shaped typo →
  still "names no line".
- F2. Make the count one quantity. Either count TOKENS that declared at least one defect (DoD 7 as written) or count
  distinct declared LINES. Make the summary text and 13(m) say the same word. 13(m): the persisted grep over
  `logs/journal/*.jsonl` is the carrier, and the summary is its at-commit echo. Add the table row "one token, a line
  with two defects" asserting the chosen count. Drop the unused `tag` from the mark tuple, and add the
  "call right after append" comment.
- F3. The WARN for a token naming only HEAD lines: "names a line already in HEAD; HEAD lines are not judged, so
  nothing was declared" instead of "carries no order defect". Add a direction row: order defect + `worker_ref`
  missing + token → still refused.
- F4 (Lead, at commit). The CLAUDE.md "Routing log" sentence above, regenerated AGENTS.md, and the axis block with
  the three non-n/a lines.

## Queue lines (proposed; the Lead opens the nodes)

- Q1. Print the `order-known: N declared` count in the merge (`decide_merge`) and CI `--all` paths too (axis 34, the
  count only). Owner: forge pile.
- Q2. If a code reader of the token appears (calibration_counts), move `ORDER_KNOWN_RE` beside `CLOSES_RE` into
  journal_keys.py as the one reader. Until then, keep it.

Decision on acceptance and on the commit belongs to the Lead (rule 6).

## Trail

Read:
- the diff (3 files);
- tools/journal_validator.py: l.255-275, 355-480, 1009-1250, 1290-1312, 1396-1414, 1810-1866, 2230-2360, 2463-2480;
- tools/journal_keys.py: l.76-83 and 153-164;
- tools/journal_echo.py (grep `decide` → l.2372);
- .githooks/pre-commit;
- the finding;
- the builder report;
- docs/SIBLING_MAP.md axis 1 and the axis list;
- docs/tasks/critic-diff-brief.md items 6-12;
- PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md check 13 (h)-(m);
- CLAUDE.md "Routing log" (worktree);
- tools/critic_verdict.schema.json.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "tools/journal_validator.py:368 and :465 -- ORDER_KNOWN_RE reads any non-blank run as a ts, so a prose mention order-known:<ts> in notes is refused as names no line with a door that cannot clear it; the real dev1 journal goes from 0 (HEAD validator) to 2 refusals (lines 1817, 1818)."
  ],
  "fixes": [
    "F1: judge a token value only when it matches TS_RE; a non-ts value is a WARN and ignored like an empty one; fix the l.367 comment; table rows for prose <ts> (code 0, WARN) and a ts-shaped typo (still refused).",
    "F2: one quantity for the count (tokens per DoD 7, or distinct lines), the same word in the summary and in check 13(m); 13(m) names the persisted grep as the carrier; table row one-token-two-defects; drop the unused tag from the mark tuple; comment that _mark is called right after its append.",
    "F3: WARN wording for a token naming only HEAD lines (not judged, not 'no order defect'); table row order defect + missing worker_ref + token stays refused.",
    "F4 (Lead at commit): CLAUDE.md Routing log sentence naming the door, AGENTS.md regenerated, axis block with axis 1 / 17 / 34 lines."
  ],
  "class_completeness": "Axis 1: CLAUDE.md Routing log and AGENTS.md must carry the door in the same commit (F4); session_context, journal_keys where and role files n/a. Axis 17 covered (door appended to the same violation strings). Axis 34 covered for the declaration (commit gate, echo, merge tail alike); the count only in the commit path, queued Q1. Token reader placement beside CLOSES_RE queued Q2 only if a code reader appears.",
  "trail": {
    "read": [
      "git diff of worktree fg7-32 (3 files)",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/tools/journal_validator.py",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/tools/journal_keys.py",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/tools/journal_echo.py",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/.githooks/pre-commit",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/plans/piles/forge/findings/20261114-zhurnal-starye-stroki-s-defektami-poryadka-bez-dveri.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/docs/tasks/specs/reports/20261114-fg7-32-report.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/fg7-32/CLAUDE.md",
      "C:/QAFactory/forge-repo/docs/SIBLING_MAP.md",
      "C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md",
      "C:/QAFactory/forge-repo/logs/journal/dev1.jsonl (copy only)"
    ],
    "reruns": [
      {
        "command": "( cd C:/QAFactory/forge-repo/.claude/worktrees/fg7-32 && python -m pytest tools/test_journal_validator.py -q -k order_known )",
        "result": "15 passed, 158 deselected in 0.46s"
      },
      {
        "command": "python -B scratchpad/t750/probe.py (probes A1-M against the worktree validator)",
        "result": "undeclared x3 refused with door; declared x3 code 0; HEAD-line token WARN; self-declaring refused; one token two defects -> '2 declared'; non-order defects stay refused (G,H,I); trailing comma refused"
      },
      {
        "command": "python -B scratchpad/t750/real.py (dev1.jsonl copy vs origin/main ef0bdf4 via _developer_file_result)",
        "result": "new validator: 2 violations, both 'names no line' on prose order-known:<ts> (lines 1817, 1818); 0 order defects"
      },
      {
        "command": "same call with git show HEAD:tools/journal_validator.py (pre-diff)",
        "result": "OLD validator violations: 0 warnings: 0"
      }
    ]
  }
}
```
