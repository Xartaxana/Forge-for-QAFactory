# Spec: dispatch completeness gate (B-201) - consolidated revision 3

History: draft by designer t-090; critic-on-plan REJECT (measured: revision 1 blocks 41 of 41 real builder
prompts); Lead's revision 2; critic t-092 ACCEPT WITH CHANGES (five changes). This text folds all of it into one
body; nothing outside this file is part of the spec.

## The decision the gate rests on

The gate enforces a NEW FORM of a writing dispatch; it is not a check of the old habit. Measured by the critic on
the 87 real dispatch prompts of this project with the definitions below: 40 of 41 old builder prompts are blocked
(by design: they predate the form), the one written in the form (t-091) passes unchanged, 0 of 46 non-builder
dispatches are swept in. The form goes into CLAUDE.md rule 11 text by Lead in the same commit that places the
live hook, or before it - never after.

The form: header lines `given:`, `owns:` (absolute paths; a path with spaces in backticks), `non-goals:`,
`handoff:`, `edges:`, `DoD:` (the verification command in backticks).

## Facts (verified by the critic against the code)

1. `tools/dispatch_gate.py` `decide()` :570-606 runs, on `subagent_type == "builder"`, a DoD-word check (:583) and
   a given/owns check that fires only after a write signal: the phrase list `WRITE_INDICATORS_RE` (:287) or an
   owns line with an absolute path or a glob (:342). t-083 attempt 1 passed both.
2. `tools/owns_gate.py:1369` and `tools/critic_snapshot.py:393` call `decide()` and unpack a 2-tuple.
3. `is_path_like_token` lives in `dispatch_gate.py` :330 (glob branch :342); `owns_gate` imports it (:535) and
   wraps it (:761). `owns_gate.extract_owns_paths` returns `[]` for repo-relative paths, and also returns relative
   globs and prose containing a glob as if they were paths.

## Definitions

- Header line: a line outside a fenced or blockquote region matching (case-insensitive)
  `^[ \t]*(?:[-*•][ \t]+)?(?:\*\*|#{1,6}[ \t]+)?KEY\b[^\n:]{0,160}:`. No numbered-list prefix: `3. Edge: ...` and
  `6. Owns overlap: ...` are not headers. Quoted regions are decided by `dispatch_gate._is_quoted`; an
  unterminated fence counts as prose. A line starting with a backtick is not a header.
- KEY groups (one constant, in code): given `given|дано`; owns `owns`; non-goals `non-goals?`; handoff
  `hand-?off`; edges `edges?|edge behaviou?r`; dod `dod|witness|verification`.
- Section: a header line plus the lines after it up to the next header or skip line, or the end of the prompt.
- Command: an inline-code span, or a line inside a fence, holding 2 or more whitespace-separated tokens.
- Owned paths of a prompt: `owns_gate.extract_owns_paths(<owns section text only>)`, then filtered to ABSOLUTE
  tokens (after stripping backticks/quotes: a drive letter, a leading `/`, or `/c/...`); a glob is kept only
  inside an absolute token.
- Skip line: outside quotes, case-insensitive, leading whitespace and one bullet allowed:
  `manifest-skip:[ \t]*ITEMS[ \t]*(--|—)[ \t]*REASON`; ITEMS is a comma list from `given, owns, non-goals,
  handoff, edges, dod` (all six at once is legal); REASON has at least one non-space character.

## Requirements

1. Pure module `tools/dispatch_manifest.py`: `check(payload) -> (exit_code, message, note)`. No I/O of any kind:
   it returns or raises.
2. Checked: `subagent_type.strip().lower() == "builder"` always; any other type only if its prompt has an owns
   section with at least one owned path (as defined above). Everything else returns `(0, "", "")`.
3. A checked dispatch passes when it has given, non-goals, handoff and edges sections each with a non-blank body
   (the header's tail after the colon counts), a dod section containing a command, and at least one owned path.
4. `owns_gate` is imported lazily inside the function; an import failure raises.
5. Missing items covered by a valid skip line are waived; the pass returns note = SKIP NOTE.
6. A malformed skip line (unknown item, empty reason) returns exit 2 with SKIP REFUSED.
7. Degraded quote detection (`md_regions` reports a degraded read, e.g. more than 200 inline spans on one line,
   `md_regions.py` about :174): the payload counts as not completely read - the module returns
   `(0, "", UNCHECKED NOTE)`. Invariant: exit 2 only from a complete read; quoted text never counts.
8. Wiring (piece B): `decide()` keeps its 2-tuple `(exit_code, message)` - it calls `dispatch_manifest.check` in
   place of the old checks 1-2 and drops the note; the label check stays last. `main()` calls
   `dispatch_manifest.check` for the note and adds it to the additionalContext parts. An unreadable payload, or
   any exception from the check, gives exit 0 AND an UNCHECKED NOTE in additionalContext (visible to the
   coordinator), plus the same text on stderr. `main()` guards the payload with `isinstance`.
9. `tools/warn_layers.json` registers two literals with carrier `tools/dispatch_manifest.py`: `MANIFEST-SKIP:`
   and `MANIFEST-UNCHECKED:`.
10. Existing tests: only those that pinned the old check-1/check-2 behaviour may change (in `.next` twins); where
    the premise was "a passing dispatch" the premise stays and the fixture gets a full manifest. Every changed
    test is reported old -> new. The builder lists every warning layer of `dispatch_gate.py` the new `decide()`
    makes unreachable (known candidates: `_region_aware_is_write`, `write_quoted_warn`, the dod/manifest-quoted
    layers); they are not removed.

## Texts (verbatim)

- INCOMPLETE (exit 2):
  `DISPATCH INCOMPLETE (CLAUDE.md rule 11): this {kind} dispatch does not go out. Missing: {items}. Expected, each as its own line outside code fences and quotes, starting with its name and a colon: given: (files/data the worker gets; a pointer to a persisted spec is allowed), owns: (the absolute paths the worker may write, never by pointer; on the owns line itself or on the lines right under it, with no blank line and no heading marks; a path with spaces in backticks), non-goals:, handoff:, edges: (the behavior at each limit, empty input and conflicting pair, or 'edges: none -- <why>'), DoD: (with the exact verification command in backticks, two words or more). To send it anyway on purpose, add a line: manifest-skip: <item>[, <item>] -- <reason>`
  `{kind}` is `builder` or `writing`; `{items}` in the fixed order given, owns, non-goals, handoff, edges, DoD,
  each with `(no line)`, `(empty)`, `(no absolute path could be read)` [owns] or `(no command in backticks)` [DoD].
- SKIP REFUSED (exit 2):
  `MANIFEST-SKIP REFUSED: '{line}' -- {why}. Expected: manifest-skip: <item>[, <item>] -- <reason>; items: given, owns, non-goals, handoff, edges, dod; the reason is not empty.`
  `{why}` is `unknown item '<x>'` or `no reason after --`.
- SKIP NOTE: `MANIFEST-SKIP: dispatch sent without {items} on purpose: "{reason}" -- the line stays in the prompt as the record.`
- UNCHECKED NOTE: `MANIFEST-UNCHECKED: this dispatch was not checked for completeness ({what}) -- it went out; check given, owns, non-goals, handoff, edges and DoD by eye.`
  `{what}` is `quoted regions could not be read reliably`, `payload unreadable: <detail>` or `check failed: <ExcType>`.

## Edges, with the invariant each protects

- Never lock the session: empty stdin, a TTY, malformed JSON, a non-dict payload or `tool_input`, a stdin timeout,
  an internal exception, a failed `owns_gate` import, a degraded read - all exit 0 with the UNCHECKED NOTE.
- An empty builder dispatch never goes out: a prompt that is absent, None, a non-string or "" gives exit 2 with
  all six items.
- Quoted text never counts: a manifest inside a fence or blockquote is not a manifest. The owns section is sliced
  before `owns_gate` sees it.
- Pointers: `given: docs/tasks/x.md` passes (R11-m); `owns: see docs/tasks/x.md` fails.
- Header limit: 0-160 characters between the key and the colon is a header; 161 is not.
- Command limit: 1 token is not a command; 2 tokens is. Named limit: any 2-token code span in the DoD section
  counts, a JSON example included.
- Owns continuation (inherited): 40 lines pass, 41 is unreadable -> exit 2.
- No new length cap; a 1,000,000-character prompt and an owns line with 5,000 `()` groups each finish under 5 s.
- Non-ASCII: `ДАНО:` counts as given; any other Cyrillic header counts as missing (false block, the safe side).
- Conflicts: a present section beats a skip naming it; a skip on a present item is ignored; duplicate sections
  are satisfied if any one qualifies.
- SendMessage resumes are not in the matcher: not checked (queued).
- Error directions of the reused `extract_owns_paths` in its new role: `[]` = false block (allowed): relative
  paths, `~/` paths, UNC paths, a relative glob on the owns line hiding an absolute path on the next line, owns in
  a fence, bare roots, `**bold**`, a 41-line continuation. A non-owns token returned as a path = false pass:
  closed for relative globs and prose by the absolute filter. NAMED OPEN LIMITS (tests pin the current behaviour):
  an absolute path merely mentioned in the owns section counts; a bullet path with spaces and no backticks
  (`- C:/AI Runway Bootcamp/x.py`) is cut to `C:/AI` and passes - the rule text requires backticks there;
  a prose line such as "Given the above, ...:" counts as a given header; a deliberate degraded read (201 inline
  spans on one line) lets a dispatch out - with the UNCHECKED NOTE.

Added after the critic's review of piece A (t-093, 30.09):
- A skip line that has text but no `--` / `—` separator (`manifest-skip: given because pointer`, an en dash) is
  refused with `no reason after --`, decided BEFORE the items are looked at.
- Named false blocks, pinned by tests, whose refusal now says the expected form: `## Owns:` followed by bullets,
  and `owns:` + a blank line + bullets -> `owns (no absolute path could be read)` (the reused reader stops at a
  heading mark and at a blank line); `DoD: \`pytest\` green` -> `DoD (no command in backticks)` (one token).
- The named open limit "a prose line counts as a header" holds for EVERY key, not only given (`Edge cases are
  listed...:`, `Handoff to the critic happens later:`); a second degraded route is named: more than 10,000 lines
  each holding an inline span come back UNCHECKED.
- Queued, not part of this task (backlog): the gate and the owns registry can read the same prompt differently
  (an earlier prose line with "owns:", a stray unterminated fence before the manifest) - the registry should
  read the same section slice as the gate.

## Tests

Fixtures are files in the repo, `tools/fixtures/dispatch_manifest/` (tests never read the home directory): the
verbatim first user message of each transcript under
`C:\Users\dev1\.claude\projects\D--ws-yml-text-factory\175a6154-a62a-4690-90f8-b64f3d7f5b2d\subagents\`,
copied once by the builder:
- K1 `agent-a35ade67180757a93.jsonl` (t-083 attempt 1, builder) -> exit 2; missing includes given, owns, non-goals, handoff, edges.
- K2 `agent-a32b719dd53980b69.jsonl` (t-087) and K3 `agent-a60e943cb56899a70.jsonl` (t-085) -> exit 2, owns among the missing.
- K4 `agent-a89f4d6fd4aaa51ba.jsonl` (scout t-088) -> exit 0, not checked.
- K5 = K1 plus a valid skip line naming its missing items -> exit 0, note starts with `MANIFEST-SKIP:`.
- K6 unknown skip item -> SKIP REFUSED; empty reason -> SKIP REFUSED.
- K7 `agent-acf314aa2bbc7eb77.jsonl` (t-091, builder, written in the form) -> exit 0 unchanged, empty note.
- K8 the critic prompt `agent-a10adbb*.jsonl` (line "6. Owns overlap: ...") -> exit 0, not checked.
Battery: every edge above, each limit at and beyond it; Cyrillic as ensure_ascii escapes and as raw UTF-8 bytes;
`Builder ` (capital, trailing space) is checked; `general-purpose` with no owns header -> exit 0; a
monkeypatched exception inside the check propagates out of `check` (piece A) and becomes exit 0 + UNCHECKED NOTE
in `main()` (piece B); degraded read at 200 spans (checked) and 201 (UNCHECKED NOTE).
Mutation (piece A): drop the quoted-region filter -> `tools/test_dispatch_manifest.py` goes red; restore by byte
copy, show the hash before and after.

## Piece A (one dispatch, a finished piece)

Owns: `tools/dispatch_manifest.py`, `tools/test_dispatch_manifest.py`, `tools/fixtures/dispatch_manifest/`.
Requirements 1-7, the texts, the edges, K1-K8 at module level, the battery, the mutation.
Witness: `python -m pytest tools/test_dispatch_manifest.py -q`.

## Piece B (after A is accepted)

Owns: `tools/dispatch_gate.py.next`, `tools/test_dispatch_gate.py.next`, `tools/test_dispatch_gate_md.py.next`
(its :179-187 and :215-227 pin the old behaviour), `tools/test_owns_gate.py.next` and
`tools/test_critic_snapshot.py.next` (only if needed), `tools/warn_layers.json`, a scratch directory.
Requirements 8-10. Witness, on a scratch copy of `tools/` and `.claude/agents/` with the `.next` files in place:
`python -m pytest <scratch>/tools/test_dispatch_gate.py <scratch>/tools/test_dispatch_gate_md.py <scratch>/tools/test_dispatch_manifest.py <scratch>/tools/test_owns_gate.py <scratch>/tools/test_owns_gate_md.py <scratch>/tools/test_owns_gate_retry.py <scratch>/tools/test_critic_snapshot.py <scratch>/tools/test_warn_messages.py <scratch>/tools/test_warn_density.py -q`
plus subprocess runs of `dispatch_gate.py` and `owns_gate.py` on a full-manifest payload (import cycle), and the
sha256 of the live `tools/dispatch_gate.py` before and after - identical.

## Non-goals (both pieces)

No edits to the live `dispatch_gate.py`, `owns_gate.py`, `md_regions.py`, `.claude/settings.json`, CLAUDE.md,
`PROCESS/`, `.claude/agents/`, the existing WARN layers or `WRITE_INDICATORS_RE`. No fix of `owns_gate`'s own
blindness to relative paths. No git state changes.

## Handoff (each piece)

At most 500 words: the witness verbatim; for B the diff `.next` vs live with line refs and changed tests old ->
new; the mutation result (A); unreachable layers (B); analogs noticed; anything needed beyond the manifest.

## Integration (Lead)

Rule 11 text with the form; byte-copy each `.next` over its live file and remove the `.next` files; rerun the
piece B witness in place; calibration protocol check 13(d) line; one commit with the axis block.

## Rule 10

- (a) Cost: six header lines on every builder dispatch, absolute owns paths, the command in backticks; a false
  block is one coordinator round trip; latency = one module import plus the lazy `owns_gate` import, to be
  measured with `experiments/dev-speed/hook_latency.py` at integration.
- (b) axis 1: queued to Lead at integration (rule 11 text; `designer.md` already says absolute). axis 2: n/a, no
  exam discipline touched. axis 3: n/a, `tools/` is not released. axis 4: covered - B-201 closes with a hash.
  axis 5: n/a, package-internal. axis 6: n/a. axis 7: n/a.
- (c) Detector: `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 13(d) - a `rejected` with `failure_class=spec` for
  a missing manifest after the landing date is a leak; MANIFEST-SKIP and MANIFEST-UNCHECKED density under check 11
  via `warn_layers.json`.
- (d) What stops the skip: the PreToolUse `Task|Agent` hook on the execution path; known holes - SendMessage
  resumes, non-builder types with no absolute owns path, a deliberate degraded read (visible by its note).
