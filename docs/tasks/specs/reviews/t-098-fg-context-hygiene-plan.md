# t-098 — critic on the PLAN `docs/tasks/specs/fg-context-and-hygiene.md` (designer draft t-095 + Lead acceptance section)

Reviewer: critic (Opus), read-only, 12.11.2026. Experiments A0/B0/C0/D0 not run (per the dispatch). The "Lead acceptance"
section is read as winning over the text below it.

**Verdict: NEEDS WORK (fit_with_fixes): 6 blocking findings (B1-B6) to settle in the spec before any builder dispatch, plus 14 fixes (F1-F14).**
The plan is sound in shape (A/B/D/E3 can be built as written once the fixes land). Two nodes cannot be built as written:
**C1** (the payload classifier it promotes to a gate refuses pure reads and calculations, see B1) and **E1** (the item
count and the `siblings:` body cannot work with the existing section extents, see B3). **A0.1** is not a builder task
(F10).

The decision to accept the plan, and every policy change here, belongs to the Lead (rule 6). The findings below are input to it.

---

## Blocking findings

### B1. C1 / M3: `_classify_pyc_payload` cannot move from advice to gate as it stands. It refuses pure reads and calculations, and a reading role has no door (surface: the python payload classifier)

Evidence. `tools/hygiene_gate.py:795-806,1011-1033`: the M lists were built for a WARN TEXT and lean toward M on purpose. The
docstring says so: "an unresolvable base ... is NOT excluded -> "M" (the conservative default)", :954-956. Under a gate that
lean points toward REFUSAL. That breaks the spec's own error direction ("A REFUSAL requires certainty", §4) and its
invariant "a read or calculation is never refused". It also breaks the owner's word 7 ("не лечить чтение через `python -c`").
Control run (a pure function, read-only, see Trail R1):

| payload (all pure, stdout only) | `_classify_single_payload` |
|---|---|
| `print('a/b'.replace('/','-'))` | **M** (`replace` is in `_PATH_MUTATING_METHOD_NAMES`, :796, matched by attribute name alone, :1011) |
| `import json,sys; json.dump({'a':1}, sys.stdout)` | **M** (`_DUMP_QUALIFIED`, :803, whatever the target) |
| `import sys; sys.stdout.buffer.write(b'x')` | **M** (base `sys.stdout.buffer` is not in `_STDIO_DOTTED`, :806, :1031) |
| `import io; b=io.StringIO(); b.write('x'); print(b.getvalue())` | **M** |
| `import csv,sys; w=csv.writer(sys.stdout); w.writerow([1])` | **M** |
| `open(r'C:/Users/x/scratchpad/f.txt','w').write('x')` | **M** (the target lies outside the tree; M1 would pass the same write as a redirect) |
| `print(open('a').read())` | P (control) |

`str.replace` is one of the commonest calls in a calculation one-liner. The spec handles only the `json.dump` row, and calls
refusing it "acceptable" (§4 "Awkward inputs"). That contradicts the invariant two paragraphs above it.

Door. The mutation door says "Edit/Write or a named, committed script; write scratch output outside the tree". It cannot be
used by the parties most often refused:
(a) A critic, designer or scout cannot Write a script at all: `tools/handoff_gate.py` refuses every Write except the handoff
file. Witnessed in this session: my Write of a scratch probe script was refused with "HANDOFF GATE: this critic worker may
write only the one report file". For these roles `python -c` and heredoc are the ONLY way to calculate, so a false M is a
dead end, which breaks P15 and FR-57.
(b) "write scratch output outside the tree" is exactly what the refused `open(scratch,'w')` does.
The current opaque text names the usable door "a named script (python <path>, including under scratchpad)",
`hygiene_gate.py:787-792`. The new text drops it.

Fix (this round, in the spec):
1. Define a gate-grade subset of M that refuses only on certainty. It is the free `open(<literal path>, <literal w/a/x/+>)`,
   `Path(<literal>).write_text/write_bytes`, and `json.dump`/`pickle.dump` whose file argument is such an `open`, each with
   the literal target resolved the way M1 resolves a redirect: inside the tree -> refuse, outside -> pass.
2. Every other current M (attribute-name matches such as `replace`/`rename`/`write`, `csv.writer`, stdio-rooted chains,
   unresolvable targets) becomes U, which gets F-C2's one WARN.
3. State that the subset lives in a constant next to the advisory lists. Do not re-label the advisory lists: the audit
   still measures with them.
4. Restore "including under scratchpad" in the door, and add for reading roles: "or Edit/Write the handoff file".

The edge row "`python -c "open(p,'w')"` with `p` outside the tree -> refuse" becomes "`p` a variable -> U (WARN)", or it
stays a refusal with a door the refused role can use. Either is legal; the spec must pick one.

### B2. C1, journal class: "unchanged minus F10" does not make the Lead's two rows pass, and leaves a pair detector that cross-matches (surface: the journal write detector; rule 15)

Evidence. `_is_journal_bypass` (`hygiene_gate.py:524-547`) fires when ONE statement carries the target (`logs/*.jsonl`
substring, :488-491) and ANY write form (:506-521). The two conditions are not tied to the same object:
- `>` anywhere in the quote-masked statement counts: `2>/dev/null`, `> /dev/null`, `2>&1`;
- `echo` or `tee` as a bare word counts even when it is an argument: `PRINTF_ECHO_RE` runs on the UNMASKED text, :516.

Control run (R1):
- `grep x logs/journal/dev1.jsonl 2>/dev/null` -> `journal: True`. This is the Lead's acceptance row, line 15 of the spec.
- `grep -c "echo" logs/journal/dev1.jsonl` -> `journal: True`.
- `ls logs/journal/dev1.jsonl 2>&1` -> `journal: True` (F10).

Live evidence: my first read-only probe in this session was a `python - <<'PY'` heredoc whose body held a journal path in a
string and a `>` in another string on the same line. It was DENIED as a journal write.

The acceptance section says both of the Lead's rows "must pass". §4 gives the journal class no mechanism to make that true:
F10's fix is only named.

Fix: redefine the journal class as "an M1/M2/M3 write whose RESOLVED target is a journal file". That is one classifier with
a target filter, not a second write-form detector, which also answers question 6 on duplication. Keep the existing
asymmetry ("always refuse") only for a resolved journal target. Add the three rows above plus the heredoc-body row to C1's
table as must-pass rows.

### B3. E1: with the existing section extents, the item count is almost always 0 and `siblings:` bodies are almost never empty (surface: the dispatch cut)

Evidence. `dispatch_manifest.section_cut` ends a section at the NEXT header or at the END of the text:
`end = events[k + 1][0] if k + 1 < len(events) else n`, `tools/dispatch_manifest.py:300`. The body is every line up to
there, :301. So "items outside every manifest section" (§6) counts only numbered lines ABOVE the first header. Every
numbered line after the first header belongs to some section (given, DoD, edges...) and is excluded. That covers the
standard layout, where header lines are followed by the spec body, and also this very dispatch, whose Q1-Q7 sit after
`given:`. With F-E3 decided as "owns + items", the item half of the threshold is structurally dead. The test row
"3 numbered items only in DoD (no check)" shows the draft assumed bounded sections.

The same extent breaks the `siblings:` grammar:
- an empty `siblings:` followed by any prose has a non-empty body and passes;
- `siblings: none` followed by more text is a "free item" and passes;
so "`none` without a reason / an empty body -> missing" fires only when another header follows at once.

The existing loop already has the right extent: `_section_paths` reads "the header tail and the lines under it up to the
FIRST BLANK LINE", `dispatch_manifest.py:547-558`.

Fix: name the extent in E1. For the siblings form AND for "outside the sections", a section is its header tail plus its
continuation up to the first blank line (the `_section_paths` rule, one definition). Then decide explicitly whether
numbered acceptance criteria inside `DoD:` count. CLAUDE.md rule 11 puts "named acceptance criteria" in the DoD, and rule 2
counts "numbered items" of the spec. As written, excluding the DoD exempts exactly the items rule 2 means. Add test rows:
spec body after the header block (counted), `siblings:` empty then prose (refused), `siblings: none` then prose (refused).

### B4. C1: the `rollback` signal does I/O, but `_collect_signals` is the audit's replay function (surface: the hygiene signal set; AR-22)

Evidence. `permission_audit.classify_hygiene` replays EVERY window command through `hygiene_gate._collect_signals`
(`tools/permission_audit.py:454-479`, "a single source of truth"). C1 adds `rollback` to `_collect_signals`' keys (§4 C1),
and the rollback class is defined as "when `git status --porcelain -- <paths>` (run by the hook, timeout 5 s) is non-empty".
If the key carries the dirty-state verdict, a calibration replay over thousands of historical commands runs `git status`
against TODAY's tree. That gives wrong counts (the paths' state then is not their state now) and costs up to 5 s per call.
M1's "root = nearest ancestor holding `.git`, found by path walk" has the same time-shift on deleted worktrees.

Fix: `_collect_signals` stays pure and carries the FORM (`rollback_form`: a checkout/restore/reset/clean shape with its
pathspec). The dirty-state check runs only in `decide()`. Check 27 (c)'s new "gate's own refusals of dirty paths, counted"
reads the gate's verdict from the transcript, as §8 already says for 27 (a). State it in C1 and add a test row: audit
replay of a checkout command performs no subprocess call.

### B5. C, one road (P31, rule 19): F-C3 "content writes only" contradicts M3's payload classes, and scratch writes take two roads

Evidence.
- F-C3, decided: `rm`, `mv`, `cp`, `Remove-Item`, `New-Item` are NOT mutation (they pass).
- M3 refuses class M, which includes `os.remove`, `os.rename`, `os.mkdir`, `shutil.*` and Path `unlink`/`rename`/`mkdir`
  (`hygiene_gate.py:795-802,1014-1019`).
So `rm docs/a.md` passes and `python -c "import os; os.remove('docs/a.md')"` is refused: two roads for one action, with no
data row and no word of the owner. Likewise `echo x > <scratchpad>/f` passes (M1, target outside the tree) while
`python -c "open('<scratchpad>/f','w')"` is refused (M3 resolves no target).

Fix: M3's refusing subset holds only the content-write classes that M1/M2 refuse. File-level operations follow F-C3 in
every syntax. Targets are resolved the same way for M1 and M3 (see B1).

### B6. C1, rollback refusal: wrong repository, uncovered shapes, false refusals from untracked files, and a door that does the harm (surface: the rollback recognizer)

Evidence and scenarios. The spec says "the status runs in the payload cwd", §4 "Rollback edges".
- **Wrong repository.** `git -C <other tree> restore f`, which is exactly the shape the cd door recommends, would have its
  status taken in the WRONG repository. An empty status there means the command passes while it discards the other tree's
  changes. `GIT_STATEMENT_RE` already knows `-C <dir>` repetitions (`hygiene_gate.py:387-390`). The recognizer must also
  skip `-c k=v` and `--no-pager` before the subcommand, and run the status in the `-C` directory.
- **Uncovered shapes.** `git checkout HEAD f.py` (rev + path, NO `--`) overwrites `f.py` and is not in the list
  ("`git checkout [<rev>] -- <paths>`, `git checkout .`"). `git checkout -f`, `git switch --discard-changes` and
  `git stash drop` are the same harm. F-C5 took `reset --hard` and `clean -f` only. The flag forms of clean (`-fd`, `-xdf`,
  `-fX`) are unstated. `git clean -x` deletes IGNORED files, which `git status --porcelain` does not list without
  `--ignored`, so `tools/dev.config.yaml`-class untracked config would vanish with a "clean" status.
- **False refusals.** `git status --porcelain -- docs/` lists `??` untracked files, and this clone carries several right now
  (`docs/tasks/compact-snapshots/*.md`, gitStatus). So `git checkout -- docs/` with every tracked file clean is refused,
  although checkout never touches untracked files. That is a refusal without harm, against the error direction. Use
  `--untracked-files=no` for checkout/restore, and the untracked plus ignored view for clean.
- **The door does the harm.** "`git stash push -- <paths>` (recoverable)" removes another session's uncommitted changes from
  ITS working tree mid-work. Worktrees share the stash ref of the main clone. The door therefore commits the very harm the
  refusal names, only reversibly. P15 needs a door that does not do the refused harm. Suggested door: "your own edit: undo
  it with Edit/Write; a byte copy you took: restore from it; changes that are not yours: leave them and tell the Lead".

Fix: state each shape above as a row, with the status run in the `-C` directory and the untracked policy per subcommand.
Settle the door text.

---

## Fixes (non-blocking, settle in the same fix round)

- **F1 (Q1, F16 false as stated; D0, D1 and the §5 goal change).** `hygiene_gate` class (a) refuses `cd <root> && <anything>`,
  compound git included. Control run (R1): `cd C:/QAFactory/forge-repo && git grep -n x` -> `cd_to_repo_root: True` ->
  deny with `MSG_CD_PREFIX` (`hygiene_gate.py:394-399,1172-1173`). "Root" is decided by the BASENAME of the folder holding
  the running copy (`_REPO_ROOT_NAME = Path(__file__).resolve().parents[1].name`, :624-634), and hook commands are
  cwd-relative (`.claude/settings.json:38`). So a worker whose cwd is its worktree runs the worktree's copy, and
  `cd <its worktree> && git grep` is refused. This is a strong candidate for t-084's "worktree guard"
  (`t-084-td11c-NC.md:79`). The §11 search (`worktree`, and `git|deny|block` in `tools/claude-mods`) could not find it.
  Consequences:
  (a) Add hygiene_gate class (a) to D0 as the first candidate.
  (b) If confirmed, D1 collapses into C1's cd row.
  (c) §5's goal "after C, a compound read is allowed" is false for a cd-prefixed compound. C1 refuses `cd <dir> && <read>`
      at ANY target. The goal must read "names its door (the Bash subshell / `git -C`)". The brief's §D sentence ("после C
      составная команда чтения внутри своего дерева отказом быть не должна вовсе") is the Lead's, not the owner's word 5.
      The Lead should note the narrowing to the owner as "решила сама".
- **F2 (Q2, harms that pass the cd class).** `pushd docs && ls` -> no signal (R1). `pushd`/`popd` are Bash builtins and
  PowerShell aliases of Push-/Pop-Location, and are not in §4's list. Also `eval "cd x"` (a quoted cd that DOES persist),
  `{ cd x; }`, and `if ...; then cd x; fi` (`cd` after `then`/`do`/`{`, which is not a statement start under a `;&|\n`
  splitter, :476). Name these rows or name the limit.
- **F3 (Q2, harms that pass the mutation class).** Each passes as specified:
  - `python -B -c "open('docs/a.md','w').write('x')"` and `python3 -c ...` -> `pyc_payload: U` (R1): `PY_DASH_C_RE` is
    `\bpython\s+-c\b` (:273, :761), so `-B` (this repo's own canonical form) or `python3` gives only F-C2's WARN. M3 names
    python3/py but not the regex widening; state it.
  - `cp <scratch> docs/a.md`, `Copy-Item`, `New-Item docs/a.md -Value x -Force` (F-C3 excludes them, so invariant (2)
    "never edited by an ad-hoc command" is NOT what C keeps; restate the invariant as "content writes by redirect, in-place
    editor or interpreter payload").
  - `python C:/scratch/fix.py` (an uncommitted script).
  - `awk -i inplace`.
  - `[IO.File]::WriteAllText('docs\a.md','x')`.
  - A redirect from a worktree into the MAIN clone (`> C:\QAFactory\forge-repo\docs\a.md`): §4 resolves the root from "the
    payload cwd's repository", so another tree's file passes. Resolve the root from the TARGET's own path.
  The journal class has the same hole: `cp <x> logs/journal/dev1.jsonl` passes (no write form).
  List the accepted residuals by name in C1 and check 27 (a).
- **F4 (Q2, C2 leaves the old motive in place).**
  - CLAUDE.md hygiene point 6 ("valid only after a positive check using the canonical form (point 1)") stays "unchanged",
    while C2 drops point 1's canonical form. The pointer dangles, and so do `.claude/agents/critic.md:66`,
    `builder.md:61` and `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:123`, which say "canonical form". Either keep point 1
    defining "the canonical (correctly invoked) form" or rewrite point 6 in C2. Rule 6 forbids editing the role files
    outside B1's rule 7/16 ownership without adding them to an owns list.
  - `docs/SIBLING_MAP.md:528` says `tools/hygiene_gate.py | command hygiene 3-4`; after C it is 3, 4, 5, 7. The brief names
    SIBLING_MAP among the carriers that change together, and C owns none of it.
  - `.claude/skills/permission-audit/SKILL.md` steps 3-5 (:69-90, allowlist curation for prompts) keep the prompt motive
    in an auto-mode deployment. Name them: kept (F12 allow rows exist) or queued.
- **F5 (Q4, A1's snapshot identity).**
  (a) PROJECT.md names the hand-written narrative `docs/tasks/compact-snapshots/<дата>-manual.md` (:273), the hook's own
      name family. The Lead's committed narrative `2026-11-12-1210-manual.md` (commit 97fae62) MATCHES A1's hook regex
      `^\d{4}-\d{2}-\d{2}-\d{4}-(manual|auto|unknown)\.md$`. So the name cannot tell hook from hand-written, and A1.4's
      REMINDER "the newest `*-manual.md` narrative" would point at hook files too.
  (b) `write_unique` writes `<stem>-2.md` within the same minute (`compact_snapshot.py:546-547`), which the regex misses,
      and `--source` takes any value (:678-681).
  (c) Two compactions within `STALE_MIN` with the second PreCompact failed show the first snapshot as fresh. That breaks
      the invariant "a snapshot measured before an earlier compaction never counts as this compaction's".
  Fix: identify by content, not name. The hook writes `session_id` and the trigger into the snapshot it already writes,
  and SessionStart (whose payload carries `session_id`) matches it. Hand-written files take a distinct name (for example
  `<date>-narrative.md`), and PROJECT.md:273 changes in the same commit (axis 31).
- **F6 (Q4, the pointer path through the parent folder).** p4:64 records the snapshot-less compaction under the transcript
  project "C--QAFactory dir", meaning the session was OPENED in the parent. `C:\QAFactory\.claude` does not exist (R2,
  positive control on the clone's `.claude` with the same command). So in such a session the clone's
  `.claude/settings.json` hooks (PreCompact and SessionStart) are not loaded at all, unless the operator's user settings
  hold them (private, not checked). F6-36 (absolute hook commands) does not register hooks for a session rooted in another
  folder, so F-A2's "wait for F6-36" rests on a cause A0.2 does not test.
  - Add to A0.2: read the transcript slug of 646c4aac.
  - State in §2 that on this path NO forge hook can keep the invariant: it is a named open limit with check 32 as detector,
    not a gap F6-36 closes.
  - For A3's "no PostCompact" outcome, note that `agent_budget.py` runs PreToolUse on every tool and measures context
    (`settings.json:17-22`, `agent_budget.py:266-279`). A sharp context drop is a host-independent compaction signal on
    which the pointer can be injected. Name it as A3's fallback, so the invariant has a carrier in both A0 outcomes.
- **F7 (Q4, A3 sequencing).** `autoCompactWindow: 350000` is live now (`settings.json:3`), and A3 waits for F6-36
  (`onboarding-forge/1`, status `ожидает`, batch-1:3). Until both land, an auto compaction may leave no pointer. Say so in
  §2 and in check 32's text, rather than claiming the invariant.
- **F8 (Q5, landing order).**
  (a) `tools/test_warn_messages.py` pins `MSG_CD_PREFIX` and `MSG_CD_NON_ROOT_WARN` by name (:174-188), so C1 WILL edit
      it ("only if" is wrong). It also loads `dispatch_gate` messages (:96), so E2's new NOTE texts must be checked there.
      Add it to E2's DoD.
  (b) Check 11's "declared population" for Command hygiene is data in `tools/warn_layers.json:196-209`, which E2 owns
      (wave 2), but §7 lands it with C1+C2 (wave 1+2). Give the row to C1 or order it.
  (c) Check 28's text names the `dod_gate` substring "COMPLETE final report" (`PROCESS/...:838`), which B2 removes, and
      the 25-line cap, which B1 changes. Land check 28's edit with whichever of B1/B2 merges first, or merge B1+B2
      together.
  (d) FG7-23 (same batch-7) edits the protocol's hook snapshot (check 19) and SIBLING_MAP paths, and FG7-29 owns
      `hop_metrics`. Add "очередь:" lines, or name them in §7 as concurrent writers of shared carriers.
- **F9 (Q5, four-question blocks).** The axis blocks use ranges ("19-30 n/a", "5-10 n/a", "15-30 n/a", "16-28 n/a") and
  bare "n/a" without a why. `tools/mechanism_gate.py` counts a literal `axis N:` for every axis of the 36 in
  `docs/SIBLING_MAP.md` (:24-31, :384-387). The commit messages must carry one line per axis with a reason; the spec should
  say so, so the builder or the Lead does not copy the ranges. Detectors (c) and skip stops (d) are present for A, B, C, D,
  E1/E2 and E3 (checks 32, 28, 27, 27 (a), 1 (c)/11/15, 24).
- **F10 (feasibility, A0.1).** A builder subagent cannot open a "throwaway session" and drive it past a context window. It
  has no interactive session and no way to observe PreCompact or SessionStart of another session. Route A0.1 to the
  operator or the Lead (as C0.2 already is), or specify a headless procedure and its cost.
- **F11 (Q3/Q7, E1 grammar edges).**
  - State `siblings: none — <why>` with an em dash (manifest-skip accepts `--|—`, `dispatch_manifest.py:121`), as well as
    `none.` and `none (<why>)`.
  - Writing out "Neighbours:"/"Siblings ...:" as a header (§6 named limit) also means such a prose line now CUTS the
    preceding section (sections end at the next header, :300). Add a test row showing the owns list is not truncated.
  - `SKIP_REFUSED_TEMPLATE` (:83-85) and `UNCHECKED_NOTE_TEMPLATE` (:91-93) hard-code the six items. Derive both from
    `KEY_GROUPS` with the two new keys (AR-1), not only `INCOMPLETE_TEMPLATE`.
  - The pointer form (R11-m: the spec lives one hop away in a file) gives `items_count = 0` by construction. Name it as a
    limit; check 1 (c) still reads the diff.
- **F12 (Q4/Q7, B2 edges).**
  - Compare handoff paths case-insensitively and slash-normalized on Windows, and say how a worktree copy of the path is
    treated.
  - Filter candidates by `HANDOFF_DIRS` as `handoff_gate` does (one reader), so a builder's handoff line mentioning a
    non-report absolute path is not "missing".
  - Name the state key of "once per agent", separate from `consecutive_blocks`, which resets on a passing stop (`dod_gate.py:265-268`).
  - The check must also run for an agent with NO edits. That is the critic who never wrote, and today `evaluate` returns
    "no-edits" before anything else (:222-223), while `main` skips saving when the track did not exist (:430).
- **F13 (Q7, E2).** Importing `scenario_walk` into the `dispatch_gate` hook process also imports `harness`, which inserts
  package paths at the head of `sys.path` and sets `os.environ` keys (`scenario_walk.py:30-33`, `harness.py:23,33`).
  Lazy imports of forge modules inside the same process (`dispatch_manifest._import_siblings`) then resolve against a
  polluted path. No basename collision between `scripts/*.py` and `tools/*.py` was found today (comm of the two basename
  lists; unverified, no positive control). State "subprocess, or import after the forge modules", and count the import
  time inside the 2 s budget. Also state how `.github/workflows/*.yml` in `carriers.json` is expanded (a glob in a file
  list).
- **F14 (Q2, C doors per shell).** For PowerShell, which has no subshell door, name the door for a command that truly needs
  a working directory (for example `Start-Process -WorkingDirectory`, or the tool's `--root`). Otherwise the PowerShell
  user of the cd refusal has only `git -C` and `python -B`.

---

## Answers Q1-Q7

**Q1 (facts).** Checked in the carrier:
- F1 true (`session_context.py:2218-2241,2309-2312`).
- F3 true (`settings.json:10-114`, every hook `python tools/<x>.py`; F6-36 `ожидает`, batch-1:3,52).
- F4: the Lead's correction is true (`settings.json:3`).
- F5 true (`compact_snapshot.py:73-78`; PROJECT.md:273).
- F6 true (`agent_budget.py:111-112,266-272`). Sibling found: PROJECT.md:273 says the warning "повторяется каждые ~100K",
  while `MAIN_STEP = 50000`. A2 should align one of them.
- F7 true (`builder.md:72-79`; `test_handoff_rule_anchors.py:23-44`; `dod_gate.py:119-126`).
- F9 true (`hygiene_gate.py:272,678,1169-1191`).
- F10 true and WIDER: `2>/dev/null`, a quoted `"echo"`, and a heredoc body also trip it (B2).
- F11 true (`permission_audit.py:174-179,454-479`).
- F13 true (`dispatch_manifest.py:100-107,128`, skip items :85).
- F14 true by grep (`scenario_walk.py:887,920`).
- F15 true (`test_quarantine.py:51-52,1340,2194`).
- F17 true (`critic.md:66-67,74`, `builder.md:61`, `designer.md:43`).
- F18: `tools/dispatch_manifest.py` IS a mechanism path (`mechanism_gate.py:270`), which closes §10's last item. The noted
  analog is confirmed: `mechanism_gate.py:233` lists `tools/critic_snapshot.py` as a "PreToolUse Task|Agent hook", which
  `settings.json` does not carry. That is a stale carrier, to be queued (it belongs with FG7-23).
- **F16 is false as stated** ("no PreToolUse hook refuses compound git"). See F1. It changes D0, D1 and §5's goal.
- **F2's cause is mis-attributed.** See F6. It changes A0.2, F-A2 and §2's invariant scope.
- F8 and F12: not verified by me; the spec marks them unverified, which is correct.

**Q2 (C).**
- Harms that pass: cd via `pushd`/`eval`/after `then` (F2); mutation via `python -B -c`, `cp`, an uncommitted script,
  `awk -i inplace`, .NET writes, and cross-tree targets (F3); journal via `cp` (F3); rollback via `git -C`, rev+path
  without `--`, `checkout -f`, `clean -x` (B6).
- Reads and calculations refused: `str.replace`, `json.dump(..., sys.stdout)`, `sys.stdout.buffer.write`, StringIO,
  `csv.writer(sys.stdout)` (B1); `grep ... journal 2>/dev/null`, `grep "echo" journal`, a heredoc read mentioning a journal
  path (B2). Not a read but harmless: `git checkout -- docs/` refused because of untracked files (B6).
- Error direction for `_classify_pyc_payload`: WRONG as specified (B1).
- Doors: the mutation door is unusable for reading roles and self-contradictory for scratch writes (B1); the rollback door
  does the harm (B6); the cd door is fine in Bash, thin in PowerShell (F14).
- C2 residue: point 6's pointer, two role files, protocol :123, SIBLING_MAP:528, skill steps 3-5 (F4).

**Q3 (E).**
- Can a dispatch with no siblings line pass? Yes: an empty `siblings:` followed by prose, or `none` followed by prose (B3);
  a prose "Siblings/Neighbours ...:" line (named limit); a degraded cut (existing, named).
- Can a well-formed line be refused? `none — why` with an em dash or `none (why)`, per the grammar as written (F11).
- Threshold vs rule 2: owns >= 3 matches "touches 3 or more files". The item half is dead (B3), and excluding the DoD
  contradicts rule 11's numbered acceptance criteria (B3). Resubmission (`designer: resubmission <task_id>`) matches rule
  2's continuation, at the cost of an extra line. Re-badging and decomposed parts cannot be seen by the gate: calibration
  1 (d) reads them, and per-dispatch counting matches "judged on its own".
- Note: a small-work batch (rule 8) touching 3+ files is over the threshold. Rule 2 already says so; the gate makes it
  visible. Not a defect.
- P27: kept. The gate checks presence and form and prints the carriers as a NOTE; sufficiency stays with the critic and
  Lead. The `designer:` path is stat-ed, not judged.

**Q4 (A, B).**
- The pointer invariant is NOT kept on three listed paths:
  - a session rooted in the parent folder (F6);
  - auto compaction until A0/A3 and F6-36 (F7);
  - two compactions inside `STALE_MIN`, or a hand-written file named like the hook's (F5).
- On the plain manual path from the clone root it is kept, by the existing line plus A1.
- B2's one-block rule loops nothing (once, plus the shared safety valve). It cannot lose a report: on a refused Write the
  message rule sends the whole report. But as specified it never runs for a no-edit agent, which is the main case, and it
  can misfire on a non-report handoff path (F12).

**Q5 (order).**
- No two nodes of one wave own the same file by the owns lists.
- Hidden overlaps: `test_warn_messages.py` (C1 and E2), `warn_layers.json` (C1's population, owned by E2), check 28 (B1 and
  B2), FG7-23/FG7-29 in the same batch (F8).
- Missing dependency: none blocking beyond F8.
- Four-question blocks: detectors and skip stops present. The axis enumeration is by ranges, which the gate rejects (F9).

**Q6 (forks).**
- F-E4 (refusal) is consistent with the owner's "да" and the recorded direction "требует строку" (`calibration-20261112.md:80-84`).
  Note that the Lead's citation of word 4 is about hygiene, not dispatch; word 6 is the right basis.
- F-E3 is consistent with the direction "число нумерованных пунктов и путей owns", but is unbuildable as specified (B3).
- **F-C3 is wrong in combination with M3** (B5, one road).
- **F-C5 is incomplete and its door is wrong** (B6).
- **F-A2 rests on an unverified cause** (F6).
- F-A1, F-B1..B4, F-C1, F-C2, F-C4, F-C6, F-D1, F-E1, F-E2, F-E5 and F-E6: no conflict with the owner's words 1-7 or the
  C2 word found.
- Owner's call? None of the forks is a product risk. One process-risk item the Lead should mention to the owner as
  "решила сама": the narrowing of the brief's §D sentence (F1 (c)), because a cd-prefixed compound read stays refused,
  with a door.

**Q7 (silent edges).**
- A1: name regex vs `-N` suffix, free `--source`, hand-written names, `STALE_MIN` across two compactions (F5).
- B1: 2,000 chars vs 3+N lines when both bind; N when the spec is a pointer; the form puts N items on one line, so "3 + N
  lines" never binds as drawn.
- B2: path normalization, the HANDOFF_DIRS filter, the once-key, no-edit agents (F12).
- C1: root from cwd vs target; `git -C`; global git options; untracked policy; rev+path without `--`; clean flags (B6, F3).
- E1: section extent; none variants; template lists (B3, F11).
- E2: import side effects, glob expansion, time budget counting the import (F13).
- E3: stated adequately (the 90 s budget does not refuse; a missing script refuses with `--no-verify` named).

## Standing questions

- **DUPLICATION AND CONSISTENCY:**
  - The journal class keeps a second shell-write detector beside the new M1-M3 (B2; one classifier with a target filter
    fixes it).
  - A1 re-states `compact_snapshot`'s file-name format as a regex in `session_context` (one writer and one reader of the
    name should share a function or constant in `compact_snapshot.py`, or use content identity per F5).
  - The three carrier lists are queued (F-E2, accepted as queued with an axis-13 note).
  - `hop_metrics._manifest_lines` is queued to FG7-29.
  - Grepped: `COMPLETE final report`, `canonical form|allowlist|point 3`, `hygiene`, `FORGE_CARRIERS`.
- **CODE QUALITY:** I/O inside the audit's pure replay function (B4). The rest is plan level; no other finding.
- **ONE ROAD (rule 19):**
  - `rm` vs `os.remove`, and redirect vs `open()` to the scratchpad: B5, a fix of this round.
  - Bash subshell vs PowerShell: a capability difference, stated in the spec, legitimate.
  - `node -e`/`ruby -e` as data rows `payload_classifier: none`: legitimate.

## Class completeness (SIBLING_MAP)

- Axis 11 (shell-command recognizers) is where every recognizer added here lives: cd statement starts, rollback with `git -C`,
  the redirect target, the journal target. F-C4 decides own masks plus queued convergence. Acceptable, provided the queue
  line is written on axis 11 in the same commit.
- Axis 13: the new keys plus the section extent (B3) touch every reader of the cut: `owns_gate` and `handoff_gate` via
  `SECTION_STOP_RE`, and `hop_metrics` queued.
- Axis 14: B2 reads the worker file through `transcripts` (kept).
- Axis 31: PROJECT.md:273, the snapshot name, changes with A1 (F5); SIBLING_MAP:528 changes with C (F4).
- Axis 34: B5.

## Trail

Read:
- the spec (1-327);
- the brief (1-73);
- `calibration-20261112.md` (33-89); `-p4.md` (19, 53-64, 106);
- `.claude/settings.json` (1-176);
- `tools/hygiene_gate.py` (380-679, 695-1214, grep of defs);
- `tools/dispatch_manifest.py` (30-139, 140-309, 546-587, 600-698);
- `tools/dod_gate.py` (1-452);
- `tools/session_context.py` (2210-2319);
- `tools/compact_snapshot.py` (70-79, 540-589, grep);
- `tools/permission_audit.py` (170-179, 454-479);
- `tools/agent_budget.py` (grep);
- `tools/handoff_gate.py` (grep);
- `tools/mechanism_gate.py` (grep, 211-274);
- `tools/test_handoff_rule_anchors.py` (1-60);
- `tools/test_warn_messages.py` (66-96, grep);
- `tools/warn_layers.json` (grep, 195-209);
- `tools/test_quarantine.py` (grep);
- `tools/journal_echo.py` (grep WITNESS ECHO);
- `scenario_walk.py` (grep); `harness.py` (grep);
- `.claude/agents/builder.md` (64-85); `critic.md` and `designer.md` (grep);
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (36-60, 777-863, headings grep);
- `docs/SIBLING_MAP.md` (axis headings, 150, 215, 528 grep);
- `t-084-td11c-NC.md` (grep :79);
- batch-7 (41-48); onboarding-forge batch-1 (3, 52);
- PROJECT.md (:273).

Control runs:
- **R1:** `python -B - <<'PY' ...` importing `tools/hygiene_gate.py` and calling `_classify_single_payload` and
  `_collect_signals` on the rows quoted in B1, B2, F1, F2 and F3. Results are verbatim in those findings. A first attempt
  whose body held a literal journal path was denied by the live gate as a journal write; that denial is B2's live evidence.
- **R2:** `ls -d C:/QAFactory/.claude C:/QAFactory/forge-repo/.claude` gives "cannot access 'C:/QAFactory/.claude'" and
  `C:/QAFactory/forge-repo/.claude`. The second path is the positive control, same command.
- **R3:** `ls -la docs/tasks/compact-snapshots/` (F5 names and mtimes); `git log -3 -- docs/tasks/compact-snapshots` (97fae62
  carries the 12:10 snapshot).

Negative-claim searches:
- `COMPLETE final report` (-i, whole repo): main tree = the protocol, `dod_gate.py`, the t-744 spec and this spec. The
  positive control is the same call finding `dod_gate.py`.
- `permission request|allowlist match|canonical form|point 3\b|hygiene point 3|breaks the allowlist` (-i) over role files,
  skills, PROCESS, the brief, builder-rules, SIBLING_MAP, TESTING, PROJECT, RUNBOOK. The hits are listed in F4; the same
  call found SKILL.md:60, which is the positive control.
- comm of package and tools basenames: empty (unverified, no positive control).

Not verified: F8, F12, the host's behaviour on `PostCompact` and auto compaction, whether a worker's hooks run the
worktree copy of `hygiene_gate` (F1 is a strong candidate, not proof), and the operator's user settings (private).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 C1/M3: _classify_pyc_payload promoted to a gate refuses pure reads/calculations (str.replace, json.dump to sys.stdout, sys.stdout.buffer.write, StringIO, csv.writer(sys.stdout) all classify M, R1); reading roles have no door (handoff_gate refuses script Writes); define a certain-only refusing subset with resolved literal targets, the rest U",
    "B2 C1 journal class: unchanged pair detector still refuses grep ... 2>/dev/null (the Lead's must-pass row), grep \"echo\" on a journal, heredoc reads; redefine as M1-M3 with a resolved journal target",
    "B3 E1: sections run to the next header or EOF (dispatch_manifest.py:300), so items outside sections are near zero and empty/none siblings bodies pass; define the extent as header tail + continuation to first blank line and decide whether DoD acceptance criteria count",
    "B4 C1: the rollback key in _collect_signals would run git status during permission_audit replay of historical commands; keep the signal pure (form), do the dirty check only in decide()",
    "B5 C one road: F-C3 passes rm/mv/cp while M3 refuses os.remove/shutil, and M1 passes scratch redirects while M3 refuses open() to scratch; align the M3 refusing subset with M1/M2 and F-C3",
    "B6 C1 rollback: status in payload cwd misses git -C; rev+path without --, checkout -f, clean -x uncovered; untracked ?? causes false refusals; the git stash door removes another session's changes"
  ],
  "fixes": [
    "F1 F16 false: hygiene_gate class (a) refuses cd <root> && git grep (R1); add to D0, D1 may collapse into C1, restate the section 5 goal",
    "F2 cd class: pushd/popd, eval, cd after then/do/{",
    "F3 mutation residuals: python -B -c and python3 -c are U, cp/New-Item, uncommitted scripts, awk -i inplace, .NET writes, cross-tree targets (resolve the root from the target), cp into the journal; restate invariant 2",
    "F4 C2 residue: hygiene point 6 pointer to the canonical form, critic.md:66, builder.md:61, PROCESS:123, SIBLING_MAP:528, skill steps 3-5",
    "F5 A1 snapshot identity: hand-written names match the hook regex (2026-11-12-1210-manual.md), -N suffix, free --source, two compactions within STALE_MIN; match by session_id content and rename narratives with PROJECT.md:273",
    "F6 F2 cause: the 646c4aac session was rooted in C:\\QAFactory, which has no .claude (R2); F6-36 does not fix it; add to A0.2, name the limit, agent_budget context drop as the A3 fallback",
    "F7 the auto window is live before A3 and F6-36: state the gap in section 2 and check 32",
    "F8 order: test_warn_messages is certainly edited by C1 and is a reader for E2; the warn_layers hygiene row; check 28 lands with B1 and B2; FG7-23/FG7-29 concurrency",
    "F9 axis blocks must be one line per axis with a reason (mechanism_gate counts a literal axis N:), no ranges",
    "F10 A0.1 is not buildable by a builder subagent: route it to the operator or Lead or specify headless",
    "F11 E1 grammar: em dash and none variants, prose header cutting sections, derive the skip/unchecked templates from KEY_GROUPS, the pointer-spec limit",
    "F12 B2: path normalization, HANDOFF_DIRS filter, a once-key separate from consecutive_blocks, run for no-edit agents",
    "F13 E2: scenario_walk/harness import pollutes sys.path and os.environ in the hook process; subprocess or ordering; count import time in 2 s; glob expansion in carriers.json",
    "F14 the PowerShell door for commands that need a working directory"
  ],
  "class_completeness": "Axis 11: every new recognizer (cd starts, rollback with git -C, redirect and journal targets) sits on it; own masks plus a queued convergence line per F-C4 is acceptable if written on axis 11 in the same commit. Axis 13: new keys and the section extent touch owns_gate, handoff_gate, dispatch_gate (hop_metrics queued FG7-29). Axis 14 kept for B2. Axis 31: PROJECT.md:273 snapshot name with A1, SIBLING_MAP:528 with C. Axis 34: B5 open.",
  "trail": {
    "read": [
      "docs/tasks/specs/fg-context-and-hygiene.md",
      "docs/tasks/specs/fg-context-and-hygiene-lead-brief.md",
      "docs/tasks/specs/reports/calibration-20261112.md",
      "docs/tasks/specs/reports/calibration-20261112-p4.md",
      ".claude/settings.json",
      "tools/hygiene_gate.py",
      "tools/dispatch_manifest.py",
      "tools/dod_gate.py",
      "tools/session_context.py",
      "tools/compact_snapshot.py",
      "tools/permission_audit.py",
      "tools/agent_budget.py",
      "tools/handoff_gate.py",
      "tools/mechanism_gate.py",
      "tools/test_handoff_rule_anchors.py",
      "tools/test_warn_messages.py",
      "tools/warn_layers.json",
      "tools/test_quarantine.py",
      "tools/journal_echo.py",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/harness.py",
      ".claude/agents/builder.md",
      ".claude/agents/critic.md",
      ".claude/agents/designer.md",
      ".claude/skills/permission-audit/SKILL.md",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "docs/SIBLING_MAP.md",
      "docs/tasks/specs/reports/t-084-td11c-NC.md",
      "plans/piles/forge/batch-7-vhodyashchie-4.md",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md",
      "PROJECT.md"
    ],
    "reruns": [
      {
        "command": "python -B heredoc: hygiene_gate._classify_single_payload on 7 payloads and _collect_signals on 10 commands",
        "result": "replace/json.dump(stdout)/stdout.buffer.write/StringIO/csv.writer(stdout)/open(scratch,w) -> M; print(open(a).read()) -> P; python -B -c and python3 -c -> pyc_payload U only; ls journal 2>&1, grep journal 2>/dev/null, grep \"echo\" journal -> journal True; cd forge-repo && git grep -> cd_to_repo_root True; pushd docs && ls and true && cd docs -> no signal"
      },
      {
        "command": "ls -d C:/QAFactory/.claude C:/QAFactory/forge-repo/.claude",
        "result": "cannot access C:/QAFactory/.claude; C:/QAFactory/forge-repo/.claude exists (positive control)"
      },
      {
        "command": "ls -la docs/tasks/compact-snapshots/ and git log -3 -- docs/tasks/compact-snapshots",
        "result": "2026-11-12-1210-manual.md (hand-written, commit 97fae62) matches the hook name pattern; td-11 narratives do not"
      }
    ]
  }
}
```
