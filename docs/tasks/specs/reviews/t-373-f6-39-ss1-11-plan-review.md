# t-373 — critic on the plan t-365 (F6-39 node A, SS1-11 node B)

critic: opus | 13.11.2026 | read tree: `.claude/worktrees/read-main` (HEAD `9a7f72a`) | spec: `docs/tasks/specs/t-365-f6-39-ss1-11-specs.md` (read whole)

**Verdict per node:**
- **Node A (F6-39): fit_with_fixes.** No blocker. Five spec edits: A-1 to A-5.
- **Node B (SS1-11): fit_with_fixes, with three BLOCKING spec edits (B-1, B-2, B-3) to make before any builder dispatch.** Six more fixes: B-4 to B-9.
- **The Lead's fork decisions:** all of F-A1..F-A5, F-B1, F-B2 and F-B4 hold, with the corrections below. The Lead's choice of F-B3 (b) is right, but part of its reasoning is wrong. The AR-20 ratchet argument is false (see key 4/7).

Accepting this verdict, and opening any node it proposes, is the coordinator's decision (rule 6).

---

## Key 1 — Facts by trail

### Node A (each checked at file:line in read-main)

| Claim | Check | Result |
|---|---|---|
| point 1: nothing deletes an archive ref | `grep -n "update-ref\|for-each-ref\|\"-d\"" tools/worktree_sweep.py` → only `:496` `update-ref ref head`; positive control = the same grep finds `:496` | TRUE: not done |
| point 2: two resolvers | `worktree_sweep.repo_context` `:262-283` (`rev-parse --git-dir --git-common-dir`); `wiring_check._main_checkout_githooks` `:338-365` (`rev-parse --git-common-dir` via `_run_git` `:270`) | TRUE: not done |
| point 3: gitcmd docstring is stale | `gitcmd.py:1-19` lists 9 callers and "NOT callers yet … dup_ratchet … wait for F2-11". `grep -il "import gitcmd" tools/*.py` (minus tests) → 14 modules, `dup_ratchet.py:68` among them. SIBLING_MAP axis 10 row `:260` says "nine callers" | TRUE: not done |
| point 4: no HEAD re-read before remove | `apply_one` `:582-613`: `archive_head(... wt.head)` `:586`, `remove_traces` `:592`, `worktree remove` `:593`; no read in between | TRUE: not done |
| point 5: three porcelain parsers | case-insensitive Grep `porcelain=v1\|--porcelain.*-z` over `tools/*.py` → `worktree_sweep.parse_status:171`, `compact_snapshot.parse_porcelain_z:171`, `hygiene_gate._parse_status:1454`. The three bodies are the same in meaning (skip a record under 4 chars, consume the origin on R/C) | TRUE: not done |
| point 6: the summary counts unpruned copies | `sweep` `:741-744` does `rep.done += 1` on PRUNABLE; `prune_registrations` `:675-681` returns True after a FAILED prune; the branch loop `:772` runs on `pruned` | TRUE: not done |
| hygiene_gate guarded import | `hygiene_gate.py:59-62` `try: import gitcmd / except Exception: gitcmd = None` (copy alone in a folder, permission_audit); `_measure_rollback` `:1477` `getattr(gitcmd, "git", None)` | TRUE. The spec's F-A4 cost line holds, but see A-1 |
| `worktree_sweep.py` goes live only at the merge into main | `.githooks/post-merge:4-6` exits in a linked worktree (`gd != common`); `post_merge` `:1224` second guard `repo.linked` | TRUE |

"None of the six points is done": **confirmed** for all six (table above).

### Node B

| Claim | Check | Result |
|---|---|---|
| the registry writer, revoke, guard and catalogue exist for accounts and sides | `project_knowledge.record` `:559-583`, `revoke` `:586-592`, verbs `cmd_side` `:806-841`, `main` subparsers `:870-902`. Guard regex `(?:account\|role\|revoke\|side)(?![\w-])` (`guard_pre_tool.py:1765`; the spec says `:1772`, line drift). Catalogue rows `config-keys.json:706-710` | TRUE |
| KEYS derived from `store: registry` + `scope` + `compare` | `_derive_keys` `:85-101` | TRUE |
| `record_problems` treats every non-side element as a role | `:535-545` (`_unsafe_role`, `CC.reserved_role`, `_form`); the person-words door `:553` names `role` | TRUE |
| no package code reads `files_filter`/`wait_for_indexing`/`timeout(900)` | `grep -rilE` over the package minus `scripts/tests/` → empty. Positive control: the same pattern without the filter → `scripts/tests/fixtures/investigation-14857/...` | TRUE |
| SS1-11 is absorbed by OF3-3 | `batch-3-…md:29` "Поглощает: … SS1-11 — onboarding-forge/2"; `project-knowledge-plan.md:244-246` | TRUE |
| "the producer `project_knowledge.py lesson` is called by the conductor or driver" (spec §2.1 AR-22) | `grep -i "project_knowledge\.py (side\|role\|account\|revoke)"` → the conductor learns these verbs ONLY from rows of `references/conductor-actions.json:26-29` (and `s4.md:184-188`). The spec adds no such row for `lesson`, and no driver code calls it | **FALSE. Blocker B-1** |
| "S5 brief builder function is not located" (F-B3) | located, see key 4 | answered |
| role-load raise for a TOOLING entry (B2-3, AR-11/AR-20, B2 owns `role-load.json`) | `role_load.static_load` `:504-523` counts the brief as `_layer("brief", _brief_ceiling(...))` = `brief_pack.BRIEF_MAX_BYTES` (`:455-463`, `:520`), a fixed ceiling. No TOOLING row and no head line is measured. `process_ratchet_tokens` covers the `agents/*.md` text only (`role-load.json` note) | **FALSE: no ratchet moves under (a) or (b)**. Fix B-5 |

Real data for F-A1 (read-only, root clone): `git for-each-ref refs/worktree-sweep/` gives 28 refs. Of these, 20 are reachable from `origin/main` and 8 are not; all are 0-1 days old. Merge commits on `origin/main` since 01.10: 125 of 593. So reachability-based expiry does catch most archives here. Patch-equal or unmerged archives stay, as stated.

---

## Key 2 — Node A safety (live hooks)

**Which parse error is safe.** In `hygiene_gate`, a non-empty entry list refuses the rollback (`:1513`). Any exception inside `_measure_rollback` becomes a `marker` (`:1516-1517`). The marker is only a NOTE, and the rollback passes (`_decide_command` `:1541-1544`). So the safe wrong parse is **more entries, never fewer, and never a raise**. In `worktree_sweep`, more entries means KEEP the copy, which is also safe. The spec states the error direction only for `main_checkout` (§1.1 last edge), not for `parse_status_z`. That function is about to gate two destructive decisions → fix A-2.

**Guarded import in `wiring_check` (F-A5 a).** The direction is right: a failed import narrows check (1) to `<root>/.githooks`, which errs toward refusing. `enforcement_probe` then fail-closes a chain commit from a worktree. But the spec's form leaves two crash roads:

1. **A-1 (fix).** A1-3 writes `except ImportError`. A broken `gitcmd.py` (a SyntaxError, or an exception raised at import) is not an ImportError, so `wiring_check` dies at import. `wiring_check` is the observer of `enforcement_probe` (`enforcement_probe.py:256-272`): every commit that touches chain files is then refused with a traceback. Its sibling uses `except Exception` for exactly this reason (`hygiene_gate.py:61`).
2. The same fix covers a `gitcmd` that has no `main_checkout`: an old copy, or a host's own unrelated `gitcmd.py` (wiring_check "is meant to run against ANY host repo", docstring `:8-10`). Calling it raises AttributeError outside any try.

Exact edit to A1-3: `try: import gitcmd` / `except Exception: gitcmd = None`; in `_main_checkout_githooks`, `resolve = getattr(gitcmd, "main_checkout", None)`; if None → `(None, "tools/gitcmd.py is not importable or has no main_checkout")`. Add a test row: a module object with no `main_checkout` → only `<root>/.githooks` accepted.

**`hygiene_gate` under F-A4 (a).** The call `gitcmd.parse_status_z(out)` sits at `:1500`, inside the `try` → a missing function becomes a marker, not a crash. But a marker is fail-open for this gate. Keep the parser pure and total (A-2), and the risk stays theoretical: both files land in one merge.

**Is a self-activating file placed live before review?** No step does it. The builder edits in a worktree; the live hooks run `python tools/...` from the main checkout. One gap: the spec never says WHEN A1 reaches main. Fix A-3: "A1 is not merged into main before the code critic of the topic (A1+A2) accepts; A2 merges A1's branch into its own worktree, not via main."

**`main_checkout` "never raises".** It calls an injected runner. `worktree_sweep.Git.__call__` (`:87-89`) does not catch, and the tests inject raising runners (`test_worktree_sweep.py:812-819`). Fix A-4: say that an exception from the runner is caught and returned as code `"git"` with its type name; stderr is bytes from `gitcmd.git`, decoded with `as_text`.

---

## Key 3 — Node A archive expiry: can it delete the only copy of unmerged work?

| Case | Walk | Result |
|---|---|---|
| archived commit not on origin/main (unmerged, or only on local main from the background run, which judges by `main`, `:52`) | `merge-base --is-ancestor sha origin/main` rc 1 → kept silently | safe |
| on origin/main, main later rewritten | the ref is deleted while the commit is reachable on the PUSHED main. Afterwards a force-push removes it from origin/main. The commit then survives locally only in the reflog of `refs/remotes/origin/main` and until gc | residual. **The claimed grace does not exist:** age is the commit's committer date, so a commit made 60 days ago and merged today expires on the first run after the merge (zero grace). Reachability is the only guard. Fix A-5 (text) |
| patch-equal, different hash (rebase or squash merge; the sweep deletes such branches, `merged_verdict` "patch-equal" `:775`) | is-ancestor rc 1 → kept forever | safe (space only; 8 of 28 live refs today) |
| a ref with no commit date (tag or tree object) | `%(committerdate:unix)` is empty → kept | safe |
| ref moved between list and delete | `update-ref -d ref sha` old-value guard | safe |
| stale local `origin/main` (no fetch) | judged on a lagging ref → fewer expire | safe direction |

Conclusion: the rule cannot delete the only copy of unmerged work. The only residual is a rewritten main, and the docstring must name it honestly instead of the "grace" claim.

---

## Key 4 — Node B principles; AR-n named with "how kept"

| Principle / AR | Spec's claim | True? |
|---|---|---|
| P2 / AR-1 | the subject is free words, no list in code | TRUE (project names stay data, key-1 grep) |
| P27 / AR-29 / AR-7 | code stores and shows, never applies | TRUE for the readers. `wait_s` is read only for display `(at least N s)`; no code uses it as a timeout (§4). So using it is not a judgment by code. The number is the CONDUCTOR's reading of the person's words, stored under `source: person` next to the words; that is acceptable because the words are whole beside it. Recommendation (non-blocking, the Lead decides): drop `wait_s` entirely. It duplicates the words, has no consumer, and takes six edges (E31-E32) plus a value branch with it |
| AR-3 | no row = no lesson; template untouched | TRUE |
| AR-14 | one writer `record`, the verb closed to roles | TRUE |
| AR-13 | one reader `lessons` | TRUE; quality note B-9 |
| AR-22 | producer called by conductor or driver | **FALSE → B-1** |
| AR-24 | words stored whole | **FALSE for this key → B-2.** `record` `:575` returns the held row when `state` and `value` are equal and never compares the words. For accounts and sides the payload is `value`. For a lesson the payload IS the words, and `value` is `{"wait_s": null}` in the usual case. A person's corrected lesson under the same subject is answered "already recorded" and the new words are dropped |
| AR-25 | revoke exits a lesson; state-exits needs no row | partly. The exit exists, but **E44 is false**: `revoke` takes back ONE row (`:586`). Under E37 an older live row of the same subject exists, so revoking the newest row resurfaces the older words. The `known` row of `design/state-exits.md:161` names the account/role producers only (sides are missing there too, pre-existing) → B-4 |
| AR-11 / AR-20 | the automator load grows; the role-load row is raised by name | **FALSE premise → B-5** (the brief is counted at its ceiling) |
| AR-28 / FR-59 | an unreadable registry is a note | TRUE |
| AR-9 | refusals name the door | TRUE |
| AR-15 / P31 | one road: same registry, writer, revoke | TRUE inside the registry. But an existing road for the same fact is not addressed: S9 `knowledge_fold` kind `stand_quirk` (`handoffs/s9-retro-to-project.yaml:60-64`) writes stand quirks into project documents, and plan phase 6.1 (`project-knowledge-plan.md:271`) moves `stand_quirk` into the fact store → B-6 |
| P9 | plain words in the note | mostly. "Acting on what you taught" claims an action that code does not perform. Better: "What you taught about <stand> (the roles read it): …". `cmd_revoke`'s printed sentence (`:799-800`, "it is asked again where it is needed; an account value…") is wrong for a lesson (and for a side) → B-7 |
| FR-7 | — | n/a: a note, not a question; nothing is re-asked |

---

## Key 5 — Node B and OF3-3

- **A data row, or a second road?** Building on the registry gives OF3-3 a data row (one catalogue row and one verb on the same writer). That holds only if (i) OF3-2's seam absorbs `lesson` the way it absorbs `account`/`role`/`side`, and (ii) OF3-6 phase 6.1 writes `stand_quirk` INTO `environments.stand_lessons` and not into a new key (B-6).
- **Is "a finding plus an `очередь:` line" legal?** The order line is already there: `batch-3-…md:11` reads `очередь: onboarding-forge/2 → onboarding-forge/3`. A second one adds nothing. An `очередь:` line is an ORDER between batches, not a message carrier, so it cannot tell OF3-3 that SS1-11 landed as a key.
- Under «Командная работа» п. 2, the finding goes into `findings/` and gets, in the same move: a row in an **UNTAKEN** batch of the pile (`batch-5-ostatki-hf8-4-i-oh3-42.md`, status "ожидает"; batch 3 is taken and frozen) and a row in the README «Содержание» table.
- A note in batch 3 «Ход» (an editable section) pointing to the finding is legal. So is a «Ход» line in batch 2 recording the Lead's F-B2 (a) decision: the SS1-11 row text says "записывается в конфиг проекта" (`batch-2-…md:39`), and the node's text is frozen. Fix B-8 gives the exact carriers.

---

## Key 6 — Edges and both worlds

| Edge | Spec | Verdict |
|---|---|---|
| project with no lessons, no registry file | E39/E45: no note, no line | OK |
| lesson with empty words | E36: `_words` refuses; `record_problems` `:550` | OK |
| `wait_s` absent / 0 / negative / huge / non-number | E31/E32 | OK. Add to E31: `int()` also accepts `" 7"`, `"+7"`, `"1_0"` and Unicode digits, and raises ValueError on more than 4300 digits (the same refusal branch). Either refuse with `^[0-9]+$` before `int()` or state that they are accepted. A hand-edited registry row whose `value.wait_s` is a string or float must not break `lessons`: show the words without the wait. That reader-side edge is missing (B-3) |
| two lessons for one operation | E37 | **wrong for same `wait_s` + new words (B-2)**; different subjects compared exactly ("Indexing" vs "indexing") are two lessons, both shown. State that |
| revoked lesson | E44 | **wrong when an older row exists (B-4)** |
| old registry written before the key | E39 both worlds | OK (`_usable` skips an unknown key, `:182`) |
| person's words: magnitude | no size limit (person_words `:35`, by design); display cut at 200, at most 10 lines | OK |
| nesting | n/a (flat text) | — |
| encoding | BOM tolerated; whitespace collapsed for display | add: control characters (ESC, etc.) are not whitespace and reach the gate packet. Strip C0 controls in the DISPLAY only, never in the store (B-3) |
| empty / broken file | `_words` door | OK |

---

## Key 7 — Feasibility and cut

- **A1, A2**: executable by Sonnet as written, after A-1..A-5. The cut is ordered (A2 merges A1's branch).
  - With F-A4 (a) taken, A1's manifest must list `tools/hygiene_gate.py` in `owns`, remove it from `non-goals`, and add `python -m pytest tools/test_hygiene_gate.py -q` to the DoD. The spec keeps them conditional, and the dispatch manifest needs them inline. That edit is part of A-3.
  - `test_wiring_check.py:196-210`'s fake prints ONE line. `main_checkout` needs two (git dir, common dir), so the fake must print both, or E2 turns the test red. Name it in A1's test bullet (part of A-4).
- **B1**: blocked by B-1, B-2 and B-3. B1's knowledge-test file is not named: name `scripts/tests/test_project_knowledge.py` and `scripts/tests/test_guard_project_knowledge.py` (it exists and holds the `side` door rows `:32-36`).
- **B2**: rewrite B2-3 for F-B3 (b) (see below). Drop `role-load.json` from owns.
- **Ownership overlaps**:
  - `gate_preflight.py` is a hot file and is also owned by **OH1-5 of the same batch 2** (`batch-2-…md:31`). The spec names EP1-33 for the guard but not OH1-5. State B2's functions (`check_stand_lessons` plus the one tuple entry in `run` `:6044-6051`) and the order or merge rule against OH1-5 (п. 3).
  - EP1-33 vs `human_word_check`: the functions are disjoint, OK.
  - B1 and B2 both own the census fixture, sequentially: OK.
- **Weakest part**: B1. The verb has no caller, the dedup loses words, and the revoke semantics are wrong. Then F-B3.
- **Ratchets each part moves**:
  - A1/A2: none in the package.
  - B1: none. `human_word_check` keeps its census row (safety, `judgment-census.json:370`); the shape check stays inside the `record_problems` unit. Name the new branch so it does NOT match `UNIT_NAME_RE` (`test_judgment_census.py:61`: no `_problems`/`_check`/`_errors` suffix), as `_side_value_faults` does.
  - B2: **one new census row, for certain** (not "if asked"): `check_stand_lessons` matches `check_`. Row: `{"file": "gate_preflight.py", "function": "check_stand_lessons", "class": "shape", "roles": ["conductor"], "owner": "data"}`. Expected: `blocking_per_role.conductor` stays 476 because the check never calls `add`. If the test counts it as blocking, that is a defect of the check, not a raise to name.
  - role-load: none (B-5).

**F-B3, the brief location asked for.** The S5 automator brief is built by `brief_pack.build` (`scripts/brief_pack.py:4086`).
- The automator-only head lines are assembled at `:4179-4183`: `if stage == "S5" and role in SIDES_ROLES: head += side_lines(pipeline)`, which is `[]` for a story with nothing to tell, so the brief is byte-identical. `:4196` adds `test_timeout_line` for S5/S7. The head is never shrunk.
- So (b) is implementable there with **no new road**: one function `stand_lesson_lines(project, stand)` built on `PK.lessons`, returning `- Stand lessons: …` lines or `[]`. It is called (1) from `manual_stand_lines` (B2-2) and (2) in the S5 head next to `side_lines`, with `stand = str(pipeline.get("environment") or "")`, the same source `build` passes to `manual_stand_lines` (`:4318-4320`). The manual runner and the automator then read one fact through one function (axis 5).
- (b) is right, but for the cost reasons only: zero bytes when there are no lessons, and no extra tool call for the automator (under (a), one tool call costs more than the 40-token line). It is NOT right for the ratchet reason: no ratchet moves either way (B-5).
- Optional, for the Lead: hand the same lines to `qa-code-critic` (it is in `SIDES_ROLES`, and P17 has it judge the automator's waits). Recommended: yes, for parity with `side_lines`.

Exact replacement for B2-3: "`brief_pack.stand_lesson_lines(project, stand)` → `["- Stand lessons: " + line for line in PK.lessons(project, stand)["lines"]]`, or one `could not be read (<problem>)` line, or `[]`. Called in `manual_stand_lines` (before `_case_actor_lines`) and in `build` inside the `stage == "S5" and role in SIDES_ROLES` block after `side_lines(pipeline)`. No TOOLING entry, no role-load change. Test: a row in the brief test's head table: no lessons → head byte-identical; one lesson → the line present for automator and code critic, absent for S4 roles."

---

## Key 8 — Tests, duplication, code quality, class completeness

- **Tests (docs/TESTING.md)**: one parameterised test per behaviour, rows in existing files, no new file. OK for all four parts. Add the rows named in A-1, A-4, B-2, B-3, B-4 and B-5.
- **DUPLICATION AND CONSISTENCY**: Node A removes 3 parser copies and 2 resolvers into `gitcmd` (checked by Grep, key 1). In Node B the formatting has one home (`PK.lessons` lines), with two call sites after the F-B3 rewrite. Remaining inconsistency: the `PT-human-word` `refuses` text in `scripts/refusal_registry.py:728-732` lists neither the `project_knowledge.py` verbs nor `side`, and now `lesson` (pre-existing sibling). Add it to B1 or queue it (B-7).
- **CODE QUALITY**: `lessons` calls `state()` per subject, and `state()` calls `load()` again (`:278`), so N subjects mean N+1 registry reads per gate and per brief. Load once and use `_latest` directly (B-9, non-blocking).
- **Class completeness (SIBLING_MAP)**:
  - axis 10: the Lead updates the row in A1's commit, as the spec says. Also name `main_checkout`/`parse_status_z` as survivors there (§5).
  - axis 5: two brief readers through one function, after the B2-3 rewrite.
  - axis 11: `human_word_check` reads command words; the `lessons` lookahead is correct (`lesson(?![\w-])` does not match `lessons`). Test both.
  - axis 18 / 32: the census row is added in the diff that adds the unit.
  - axis 34 (one road): `stand_quirk` (B-6).
  - axis 35 (sides): the registry sibling. Its state-exits and refusal-registry gaps are pre-existing; queue them with B-4/B-7.
- **ONE ACTION, ONE ROAD (P31)**: no language/project/case exclusion was found. The one second-road risk is `knowledge_fold stand_quirk`, which B-6 routes to the same key.

---

## Findings with exact spec edits

### Blocking (node B, before dispatch)

**B-1 — the producer has no caller (AR-22, FR-11, FR-15).** Surface: the conductor's action table.
- Spec edit to §2.2: add `references/conductor-actions.json` to B1 owns, plus one row after the `side` row (`:28`): `{"says": "the person teaches how the stand behaves (an operation that takes long, how to narrow it), meant for the next runs too", "run": "project_knowledge.py lesson --task <T> --subject \"<a few words>\" [--stand <name>] [--wait-s <seconds>] --words-file <file holding their words>; a story that leaves no trace refuses it"}`.
- Extend the revoke row (`:29`) "about a role or an account" → "about a role, an account, a side or a stand lesson".
- Add B1 to the witness: `scripts/tests/test_conductor_doors.py` (its `MOVE_KEYS` check, `:198`).

**B-2 — a corrected lesson is dropped (AR-24).** Surface: `record`'s dedup.
- Spec edit to B1-2: "In `record`, for `key == LESSONS_KEY` the existing row is returned only when `state`, `value` AND `provenance.words` (stripped) are equal; other keys unchanged."
- Rewrite E37: "same subject, same `wait_s`, same words → already recorded; different words or `wait_s` → a new row, the newest shown."
- Test row: same subject and wait, new words → a new PK id, `lessons` shows the new words.

**B-3 — reader-side and display edges missing.**
- Spec edit to B1-2 `lessons`: "a row whose `value` is not `{"wait_s": int 1..86400 | null}` (a hand edit) is shown with its words and without the wait, never dropped and never raised; the display strips C0 control characters and DEL (the store keeps them)."
- Add to E31 the `int()` forms (refuse anything not matching `^[0-9]+$`).
- Test rows for both.

### Fixes (non-blocking, same round)

- **A-1** Guarded import: `except Exception` plus `getattr(gitcmd, "main_checkout", None)` in A1-3, and a test row (key 2).
- **A-2** Add to §1.1 edges: "`parse_status_z` gates a refusal (hygiene_gate) and a deletion (worktree_sweep): it may err only toward MORE entries; it never raises on any bytes/str input (a raise in hygiene_gate is a marker, so the rollback passes) and never drops a record of 4+ characters."
- **A-3** State that A1 does not reach main before the topic critic. Move `tools/hygiene_gate.py` into A1 owns (F-A4 a taken), out of non-goals, and add `tools/test_hygiene_gate.py` to the A1 DoD.
- **A-4** `main_checkout` catches a runner exception (code `"git"`) and decodes stderr bytes. The wiring fakes print two lines.
- **A-5** Docstring and F-A1 text: replace "N is only a grace period against a rewritten main" with "N counts from the commit's committer date, not from the merge; reachability from origin/main is the only guard; a later rewrite of main is the accepted residual".
- **B-4** Rewrite E44: "revoking the newest row of a subject shows the previous live row again; to remove a lesson, revoke every live row of the subject (`show` lists them)". Add `lesson` to the producer cell of `design/state-exits.md:161` (sides alongside, or queue them), with a test row.
- **B-5** Drop `role-load.json` from B2 owns and the `role_load.py --all` before/after from the handoff. Rewrite the AR-11 line: "no start-load ratchet moves: the brief is counted at `BRIEF_MAX_BYTES` (`role_load.py:520`)". Replace B2-3 with the F-B3 (b) text in key 7.
- **B-6** The OF3 finding (B-8) also names OF3-6 phase 6.1: "`stand_quirk` lands as an `environments.stand_lessons` row (one key), not a new key."
- **B-7** Text: the gate note wording (key 4 P9); a `cmd_revoke` sentence that fits a lesson; the `PT-human-word` `refuses` text in `refusal_registry.py` names the `project_knowledge.py` verbs. Either add these to B1 owns or queue them with a pointer.
- **B-8** Replace F-B1's "a finding plus an `очередь:` line" with: a finding file in `plans/piles/onboarding-forge/findings/`, a row in `batch-5-ostatki-hf8-4-i-oh3-42.md` (untaken), a README «Содержание» row, a «Ход» line in batch 3 pointing at it, and a «Ход» line in batch 2 recording F-B2 (a) against the node's "конфиг" wording. Also name the OH1-5 `gate_preflight.py` overlap (key 7).
- **B-9** `lessons` loads the registry once (key 8).

### Lead's forks

| Fork | Review |
|---|---|
| F-A1 (a) | right; correct the grace claim (A-5) |
| F-A2 (a) | right; SessionStart already prints FAILED (`session_context.py:1790-1792` per spec) |
| F-A3 (a) | right |
| F-A4 (a) | right; manifest edit (A-3) and error direction (A-2) |
| F-A5 (a) | right in direction; wrong exception class (A-1) |
| F-B1 (a) | right, with B-1, B-6 and B-8 |
| F-B2 (a) | right, with B-2 (the words are the payload) |
| F-B3 (b) | right; the ratchet half of the reasoning is false (B-5); implementation text in key 7 |
| F-B4 | right, with `conductor-actions.json` added (B-1) and OH1-5 named |

Request to the coordinator (not done here, rule 3): run `python tools/piles.py check --all` to confirm that no batch "в работе" outside onboarding-forge owns `tools/hygiene_gate.py`, `tools/wiring_check.py` or `scripts/gate_preflight.py`.

## Trail

Read (read-main):
- the spec, whole
- `tools/worktree_sweep.py` 40-110, 165-190, 250-300, 480-525, 560-792, 1213-1245
- `tools/gitcmd.py` whole
- `tools/wiring_check.py` 1-40, 196-410
- `tools/hygiene_gate.py` 50-70, 1440-1560
- `tools/compact_snapshot.py` 165-190
- `tools/enforcement_probe.py` 50-70, 256-276
- `tools/test_worktree_sweep.py` 208-222, 636-690, 808-880
- `tools/test_wiring_check.py` 150-215
- `.githooks/post-merge`
- `docs/SIBLING_MAP.md` headings and 255-262
- `scripts/project_knowledge.py` 80-210, 265-300, 380-410, 470-600, 685-730, 760-915
- `scripts/guard_pre_tool.py` 1718-1785
- `scripts/brief_pack.py` 853-875, 2682-2726, 3140-3215, 4170-4200, 4225-4330
- `scripts/gate_preflight.py` 1664-1680, 5106-5125, 6035-6060
- `scripts/role_load.py` 500-535
- `references/role-load.json` 1-40
- `references/config-keys.json` 700-790
- `references/conductor-actions.json` 20-32
- `design/state-exits.md` 161-163
- `scripts/refusal_registry.py` 725-740
- `scripts/tests/fixtures/judgment-census.json` (head, rows 331/339/370/654)
- `scripts/tests/test_judgment_census.py` (`UNIT_NAME_RE`)
- `scripts/tests/test_config_migration.py` 385-410
- `scripts/tests/test_guard_project_knowledge.py` 1-36
- `handoffs/s9-retro-to-project.yaml` 50-80
- the batch-2 SS1-11/F6-39/EP1-33 rows and owns column; batch-3 header and the OF3-3 "Поглощает" line
- `project-knowledge-plan.md` 240-275
- the SS1-11 finding, whole

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 node B: the producer verb `project_knowledge.py lesson` has no caller - no row in references/conductor-actions.json (the only place the conductor learns registry verbs, rows 26-29); AR-22 claim false. Edit: add the row and extend the revoke row; conductor-actions.json into B1 owns; test_conductor_doors.py into the witness",
    "B-2 node B: record() dedups on state+value only (project_knowledge.py:575); for a lesson the words are the payload, so a corrected lesson with the same wait_s is answered already recorded and the new words are lost (AR-24). Edit: for LESSONS_KEY also compare provenance.words; rewrite E37; add a test row",
    "B-3 node B: missing reader/display edges - a hand-edited row with a malformed value must show words without the wait and never raise; display strips control characters; --wait-s refuses non [0-9]+ forms that int() accepts. Edit B1-2 lessons and E31; add test rows"
  ],
  "fixes": [
    "A-1 wiring_check guarded import: except Exception plus getattr(gitcmd, main_checkout, None); test row for a gitcmd with no main_checkout",
    "A-2 state the error direction of parse_status_z: more entries, never a raise, never a dropped record (a raise in hygiene_gate is a marker and the rollback passes)",
    "A-3 A1 is not merged into main before the topic critic; hygiene_gate.py into A1 owns and test_hygiene_gate.py into the A1 DoD (F-A4 a taken)",
    "A-4 main_checkout catches runner exceptions as code git and decodes stderr bytes; the wiring fakes print two lines",
    "A-5 replace the grace-period claim: age is the committer date, reachability from origin/main is the only guard, a rewritten main is the residual",
    "B-4 E44 is false (revoke takes one row; an older live row resurfaces): rewrite the edge and add lesson to the producer cell of design/state-exits.md:161",
    "B-5 no role-load ratchet moves (the brief is counted at BRIEF_MAX_BYTES, role_load.py:520): drop role-load.json from B2 owns; replace B2-3 with stand_lesson_lines called in manual_stand_lines and in the S5 head next to side_lines (brief_pack.py:4179-4183)",
    "B-6 the OF3 finding also names OF3-6 phase 6.1: stand_quirk lands as an environments.stand_lessons row",
    "B-7 text: the gate note without Acting on; a cmd_revoke sentence fit for a lesson; the PT-human-word refuses text names the project_knowledge verbs (fix or queue with a pointer)",
    "B-8 replace the order line with: a finding plus a row in untaken batch 5, a README row, Hod lines in batch 3 and batch 2; name the OH1-5 gate_preflight.py overlap",
    "B-9 lessons loads the registry once instead of once per subject"
  ],
  "class_completeness": "Node A: axis 10 covered by the Lead's row update; the third parser (hygiene_gate) is included via F-A4. Node B: axis 5 covered after the B2-3 rewrite (one function, two briefs); axis 11 lookahead correct; axis 18/32 census row in the same diff; axis 34 second road knowledge_fold stand_quirk routed by B-6; axis 35 sides siblings in state-exits and refusal_registry are pre-existing gaps, queued with B-4/B-7.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-365-f6-39-ss1-11-specs.md",
      "tools/worktree_sweep.py",
      "tools/gitcmd.py",
      "tools/wiring_check.py",
      "tools/hygiene_gate.py",
      "tools/compact_snapshot.py",
      "tools/enforcement_probe.py",
      "tools/test_worktree_sweep.py",
      "tools/test_wiring_check.py",
      ".githooks/post-merge",
      "docs/SIBLING_MAP.md",
      "ai-packages/qa-factory/scripts/project_knowledge.py",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/role_load.py",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/references/config-keys.json",
      "ai-packages/qa-factory/references/conductor-actions.json",
      "ai-packages/qa-factory/design/state-exits.md",
      "ai-packages/qa-factory/scripts/refusal_registry.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py",
      "ai-packages/qa-factory/scripts/tests/test_config_migration.py",
      "ai-packages/qa-factory/scripts/tests/test_guard_project_knowledge.py",
      "ai-packages/qa-factory/handoffs/s9-retro-to-project.yaml",
      "plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md",
      "plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md",
      "plans/project-knowledge-plan.md",
      "plans/piles/onboarding-forge/findings/20261030-nauchennoe-o-stende-ne-sohranyaetsya-na-sleduyushchij-progon.md"
    ],
    "reruns": [
      {"command": "grep -n update-ref|for-each-ref tools/worktree_sweep.py (read-main)", "result": "only :496 update-ref ref head - no delete of archive refs (point 1 not done)"},
      {"command": "grep -il import gitcmd tools/*.py minus tests (read-main)", "result": "14 modules incl. dup_ratchet.py:68 - gitcmd docstring stale"},
      {"command": "Grep -i porcelain=v1|--porcelain.*-z over tools/*.py", "result": "3 parsers: worktree_sweep:171, compact_snapshot:171, hygiene_gate:1454"},
      {"command": "grep -rilE files_filter|wait_for_indexing|timeout(900) package minus scripts/tests, control without filter", "result": "empty; control finds fixtures/investigation-14857 files"},
      {"command": "git -C root for-each-ref refs/worktree-sweep/ with merge-base --is-ancestor origin/main and age", "result": "28 refs: 20 reachable, 8 not; ages 0-1 d"},
      {"command": "git -C root rev-list --merges --count --since=2026-10-01 origin/main --", "result": "125 merges of 593 commits"},
      {"command": "Grep -i project_knowledge.py (side|role|account|revoke) over the package", "result": "conductor learns verbs only from references/conductor-actions.json rows 26-29 and s4.md; no lesson row in the plan"},
      {"command": "grep TOOLING|BRIEF_MAX_BYTES scripts/role_load.py", "result": "brief counted as ceiling layer at :520; TOOLING not measured - no ratchet moves"}
    ]
  }
}
```
