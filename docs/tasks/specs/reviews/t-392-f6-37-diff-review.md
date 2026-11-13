# t-392 — diff gate, node forge/6/F6-37 (handoff path checked before launch), and node F6-35 (worktree base WARN)

One critic pass for the topic (R13-g): node A = F6-37 (section 1), node B = F6-35 (section 2). Each node has its own
verdict. One combined machine block closes the file.

Overall: **fit_with_fixes (NEEDS WORK).**
- Node A: 2 blocking findings, 4 non-blocking.
- Node B: fit, 0 blocking, 6 non-blocking.

Accepting either node is the Lead's call (rule 6).

---

# Section 1 — node A, F6-37

Reviewed: `git -C C:\QAFactory\forge-repo\.claude\worktrees\f6-37 diff a537391 b615e4e` (10 files, 484+/33-), by the
commit range. The working tree of that worktree carries node B's unstaged edits (`dispatch_gate.py`,
`test_dispatch_gate.py`, `RUNBOOK.md`, `plans/builder-rules.md`). So every probe and the control re-run below ran on a
CLEAN extraction of both commits (`git archive b615e4e tools` / `git archive a537391 tools` into my scratchpad), never
on that worktree. That is a deviation from "in the worktree via a subshell", for exactly that reason. Line numbers are
of b615e4e.

## Verdict (node A)

**fit_with_fixes (NEEDS WORK): 2 blocking findings, 4 non-blocking.**

The check itself is right. It held on a replay of 156 real past dispatches and on every K3 dispatch I tried. Two
problems remain, both small fixes:
- **(B1)** An exception in the cut builder turns into a FALSE `no handoff: line` refusal of every critic and designer
  dispatch. That breaks the §A.4 error direction on a live hook.
- **(B2)** Case 10 of the hook liveness probe is now refused. So
  `test_hook_liveness_probe.py::test_live_run_of_all_cases_is_ok` goes red on the CI canon, and the post-merge liveness
  probe (spec §D.2) fails.

## Blocking findings (node A)

### B1 — a raise in the cut builder becomes a false NO_LINE refusal (K2, §A.4)

How the false refusal happens:
- `tools/dispatch_gate.py:793` (`is_builder, cut = dm.cut_payload(payload)`) sits inside the completeness `try`.
- When `cut_payload` raises, `cut` stays `None`. `decide_full` then goes on (`:806`) to
  `handoff_folder_check(payload, None, dm)`.
- `:752` (`if cut is None: return 2, HANDOFF_NO_LINE…`) cannot tell this "unknown" `None` from the cheap-exit `None`
  (the prompt has no owns/handoff word).

When `section_cut` raises:
- It raises whenever `_import_siblings` fails. That function (`dispatch_manifest.py:240-250`) imports `md_regions`,
  `dispatch_gate` and `owns_gate`, and passes any failure up.
- Only the md_regions SCAN is wrapped into a degraded cut (`_scan`, `:285-292`).

The effect:
- A broken `owns_gate.py` on main, or any raise inside `section_cut`, refuses EVERY critic and designer dispatch.
- The refusal text is false, too: it says "It has no handoff: line" to a dispatch that has one.
- Before the diff, the same dispatch passed with a MANIFEST-UNCHECKED note.

Probe (b615e4e tools, `dm.section_cut` monkeypatched to raise `RuntimeError`):
```
dispatch: subagent_type critic, description "opus: x", prompt "Review.\nhandoff: C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1.md"
cut raises (good critic)  code=2 msg=HANDOFF PATH (CLAUDE.md rule 11, R11-h): this critic dispatch does not go out. It has no handoff: line. ...
                          notes=['MANIFEST-UNCHECKED: this dispatch was not checked for completeness (check failed: RuntimeError) -- i']
cut raises (builder)      code=0 (unchanged behaviour)
```

Spec root: §A.2 step 3.3 says "cut None → NO_LINE". §A.4 says "an unknown is never a launch refusal". The builder
followed step 3.3 to the letter, so the contradiction is in the spec (a positional/edge defect of the dispatcher). Test
e23 covers only a failed `handoff_gate` import, not a failed cut.

Fix:
- On `cut is None`, refuse with NO_LINE only when the prompt really lacks the word
  (`not dm._HANDOFF_WORD_RE.search(prompt)`). Do this through a small public predicate next to `cut_payload`, so the
  cheap exit keeps one reader.
- Otherwise return NOTE_UNCHECKED and pass.
- Alternative: `decide_full` skips the handoff check with a note when the completeness block raised.
- Add row e25: `section_cut` raises on a correct critic dispatch → code 0 + `HANDOFF CHECK: not checked`.

Surface: "the launch check's reading of a None cut". Neighbours walked:
- Manifest import failure: `dm` is None, so `dm.dispatch_kind` raises AttributeError, which is caught at `:806` →
  note, pass. OK.
- `tool_input` not a dict: `decide_full` returns a pass first. OK.
- A None or non-str prompt: becomes `""`, has no word → NO_LINE. This is e18 and intended.
- A non-breaking hyphen in `hand‑off:`: the cheap-exit regex and the header grammar (`dispatch_manifest.py:88`,
  `hand-?off`) agree. The write gate does not read it as a header either. Consistent.
- Magnitude (a prompt over MAX_TEXT_CHARS): degraded → NOTE (e17). OK.

### B2 — case 10 of hook_liveness_probe is now refused (K6/K9; the canon and the post-merge probe go red)

What breaks:
- `tools/hook_liveness_probe.py:877-905` (`_case_10_critic_snapshot`) sends a critic dispatch with
  `handoff: <tmp>/review.md` (`:898`). That path is NOT inside `docs/tasks/specs/reviews`.
- The case registry (`:1320-1328`) expects `expected_exit: 0` and a written snapshot.

Replay of `_case_10_critic_snapshot()["payload"]` through `decide_full`:
```
a537 case10 decide: 0
b615 case10 decide: 2 HANDOFF PATH (CLAUDE.md rule 11, R11-h): this critic dispatch does not go out. Its handoff: names C:/Users/.../hook-liveness-probe-critic-s...
```

Consequences:
- `tools/test_hook_liveness_probe.py:980` (`test_live_run_of_all_cases_is_ok`) asserts that every case is OK. It runs
  in the full `pytest tools/` canon, so the batch canon goes red.
- The same probe is the post-merge check that spec §D.2 prescribes.
- So a dispatch that passes today is wrongly refused. The error is in the fixture, not the gate, but the gate change
  and its consumer must land in one commit.
- I did not run that test myself (one control re-run was allowed). The gate verdict above is the direct cause.

Root cause:
- Spec fact A12 grepped only `tools/test_*.py`, and `hook_liveness_probe.py` is not a `test_*` file.
- The builder's DoD list did not include `test_hook_liveness_probe.py`.
- My sweep found exactly three files: `hook_liveness_probe.py`, `test_critic_snapshot.py` and `test_dispatch_gate.py`.
  It was a case-insensitive grep for `"subagent_type": "critic|designer"` over `tools/`, with a positive control of 11
  builder hits. So this is the only missed file.

Fix:
- Case 10's handoff becomes `<tmp>/docs/tasks/specs/reviews/review.md`, i.e.
  `_fwd(os.path.join(tmp, 'docs', 'tasks', 'specs', 'reviews', 'review.md'))`.
- `hook_liveness_probe.py` joins the owns. That is the Lead's call: the file is outside the node's manifest.
- Witness: `python -m pytest tools/test_hook_liveness_probe.py -q -k live_run`.

## Non-blocking findings (node A)

- **N1 (K4)** `dispatch_gate.py` HANDOFF_NO_PATH: for e6 the door "move the path into {folder}" misleads. In e6 the
  path is RELATIVE but already in the right folder, so the problem is that the path is relative, not that it is in the
  wrong folder. The Expected line does show the absolute form. Suggested door: "Door: write it as an absolute path
  inside {folder}, or add: …".
- **N2 (K7/rule 14, magnitude)** The same MANY refusal is rendered in two ways. The write gate joins ALL candidates
  with no limit (`handoff_gate.py:180`, `paths=", ".join(cands)`). The launch check now shows at most 5 + "and N more"
  (`_handoff_shown`, `dispatch_gate.py:728`). Queue: make `_gate` use the same cap. It is a sibling outside this diff
  (rule 5).
- **N3 (K7)** `dispatch_gate.py:743-745` is a third copy of the "put tools_dir on sys.path, then import" prelude (the
  others are at `:588` and `:1707`). A shared `_import_sibling(name)` would remove all three. Small; a candidate for
  the fix round.
- **N4 (K8)** RUNBOOK item 11 (b615 `docs/RUNBOOK.md:602-614`):
  - It says "a bare relative path is not read either", and it ties "the id-race detector reads it" only to the task
    id. It never says plainly that a bare path makes the detector MISS that dispatch.
  - Suggested clause: "(… not read either — the id-race detector then does not see this dispatch)".
  - Also owed by the Lead, per the builder's handoff: the spec text of §A.6 m1/m5 (+m1a/m5a) and §A.5 still shows the
    rows from before the decision.

## Keys (node A)

### K1 — fit to the spec

| item | status | evidence |
|---|---|---|
| §A.2 step 1 `cut_payload` + `_HANDOFF_WORD_RE` + `dispatch_kind` | met | diff `dispatch_manifest.py`; check_cut untouched |
| step 1b `handoff_mentions` | met | `dispatch_manifest.py:653-659`, same `_section_paths` loop |
| step 2 `handoff_candidates`, two callers | met | `handoff_gate.py:104-114`, `_gate`, `dod_gate.named_handoffs` |
| step 3 `handoff_folder_check` order 1-7 | met to the letter; 3.3 conflicts with §A.4 | B1 |
| step 4 `decide_full` position, try, docstrings | met | `dispatch_gate.py:805-812`, module docstring `:25-26` |
| step 5 table + fixtures | met | rows e1-e21 parametrized; fixtures gained handoff lines |
| step 6 `test_handoff_mentions` | met, as the Lead decided (m1 backticked, m1a and m5a added) | test diff |
| step 7 test_critic_snapshot | met | `_critic_payload`, `_blocked_critic_payload`, M2-1 control, new e24 row |
| step 8 h1 | met | `test_handoff_gate.py` h1 |
| step 9 RUNBOOK item 7 clause, item 11 | met; item 11 deviates from the §A.5 verbatim text per the Lead decision | diff |
| e1-e21 | met (rows present; control re-run green) | `_FOLDER_ROWS` |
| e22 | met | `test_handoff_folder_check_e22_…` |
| e23 | met for an import failure; the cut-raise neighbour is not covered | B1 |
| e24 | met | `test_m2_1_handoff_refused_dispatch_…` |
| m1, m1a, m2, m3, m4, m5, m5a | met | `test_handoff_mentions` |
| h1 | met | first-folder pair and dedup asserted |

### K2 — error direction (§A.4)

| path | result | test |
|---|---|---|
| degraded cut | NOTE, pass | e17 |
| `handoff_gate` import failure | NOTE, pass | e23 |
| exception inside `handoff_folder_check` | `HANDOFF CHECK: not checked: <Exc>`, pass (`:811-812`) | none directly; traced (a `dm=None` probe takes this road) |
| manifest module import failure | AttributeError, caught, note, pass | traced |
| `cut_payload`/`section_cut` raises | **REFUSAL NO_LINE: breach** | none (B1) |

WRONG_FOLDER and MANY direction: I replayed 156 past critic/designer Agent dispatches from 9 transcripts of this
project. Result: 150 pass, 6 refused. The write gate also refuses all 6:
- 4 critic paths outside reviews (`docs/tasks/specs/td-11-plan-critic.md` twice, `specs/reports/t-013…`,
  `experiments/…/blind-eval.md`);
- 1 designer dispatch with "handoff: the spec file itself" (no path → NO_PATH);
- 1 designer dispatch, t-337: its handoff is only inline in parentheses (NO_LINE). This is the very leak the node
  closes.

So the replay found no refusal of a write the write gate would accept.

### K3 — position invariant

- **(i) Still refused, same text:** a completeness refusal returns before the new check (`:801-803`; e22).
- **(ii) Newly refused:** a critic or designer dispatch with any of:
  - no `handoff:` header;
  - no absolute path;
  - a path in the wrong folder;
  - a non-`.md` path;
  - two paths.

  A dispatch with both a bad label and no handoff now shows the HANDOFF text first, and the label refusal comes on the
  second attempt. It is refused either way (`test_decide_full_handoff_refusal_keeps_the_label_check_behind_it`).
- **(iii) Never turns another refusal into a pass:** traced. A code-2 return only adds refusals. A code-0 return falls
  through to the path and label checks unchanged.
- **The requested dispatches**, run through `decide_full` at b615:
  - THIS dispatch text (critic, `handoff: …\reviews\t-392-f6-37-diff-review.md`): code 0, no note.
  - A scout with a relative handoff: 0. Not checked, since scout is not a gated kind.
  - A builder whose handoff is a reply: 0.
  - A designer with `manifest-skip: handoff -- draft returned in chat`: 0 + SKIP_NOTE.
  - A dispatch resumed by message: not affected. The hook matcher is `Task|Agent` (`.claude/settings.json:25`), and a
    resume goes through the `SendMessage` tool. The transcripts hold 244 SendMessage calls `{"to":…}` and no `resume`
    key among 615 Agent calls (the 615 is the positive control).
  - Other forms that pass: a path in a worktree's reviews folder, a backticked path, a bullet `- handoff:`, bold
    `**handoff:**`, `Hand-off:`, and a path on the next line.
  - `qa-factory:critic` and kind None: not checked.
- **Dispatches that pass today and are now wrongly refused:** B1 (cut raise) and B2 (liveness case 10).

### K4 — the door

Every refusal names three things: the problem, the expected form, and a door its receiver (the coordinator) can use.
The doors are "edit the dispatch" or "add `manifest-skip: handoff -- <reason>`". MANY's door is "keep one path". The
test asserts a door on every code-2 row. Nit: N1. B1's text is false in its own case ("no handoff: line").

### K5 — one loop, three callers

- Old `_gate` used `any(_in_folder(p, f) for f in folders)`, then `setdefault(_real(p, base), p)`.
- Old `named_handoffs` took the first matching folder, then `setdefault(_real, (p, folder))` with `break`.
- The two loops use the same membership test and the same dedup key:
  - `any` means the same as "a first match exists";
  - the dedup key does not depend on the folder;
  - both keep the first spelling (`setdefault`).
- So the old loops produced the same path set on every input. They differed only in what they stored (a path vs a
  pair), and `_gate` now takes just `p` from each pair.
- h1 pins the first-folder rule and the `..`/slash spelling. The diff leaves `test_handoff_gate.py` and
  `test_dod_gate.py` unchanged, and their old tests pass per the attached 907.

### K6 — class-wide (axis 13)

Readers of the handoff section in `tools/*.py` (grep `handoff_paths|handoff_mentions|sections["handoff"]`):
- `handoff_gate`, now through `handoff_candidates`;
- `dod_gate.named_handoffs`, the same;
- `hop_metrics.py:219` (`handoff_paths`), unchanged and still in agreement;
- the new check.

No private line scan was added. `cut.sections["handoff"]` is read once (`:765`), as an emptiness test.

Producers of critic payloads that now disagree with the readers: `hook_liveness_probe` case 10 (B2).

The SIBLING_MAP axis-13 row update (`handoff_folder_check`, `handoff_candidates`, `handoff_mentions`) is owed by the
Lead in the merge commit (spec §D.2; the commit message says so). The write gate's unbounded MANY rendering is queued
(N2).

### K7 — duplication and consistency; code quality

Duplication:
- N2: MANY is rendered twice, with different caps.
- N3: a third sys.path prelude.
- Grepped: `and %d more` and `sys.path.insert(0, tools_dir)` in `dispatch_gate.py`, `handoff_gate.py` and
  `dispatch_manifest.py`.
- The three copies of the candidate loop became one: a net clone reduction.

Code quality:
- The refusal texts are built from shared constants.
- `dispatch_kind` is the one kind reader.
- The fixture helpers in `test_dispatch_gate.py` (`_reading_dispatch`, `_critic_payload`) add a handoff line only when
  the word `handoff` is absent. A future fixture that mentions "handoff" in prose but has no header would be refused
  without warning. That is fragile, but it shows up as a red test. Not blocking.

### K8 — the Lead decision on m1/m5

Node C's check 46 takes the `t-NNN` out of `handoff_mentions` and compares it with the journal task_id. An undercount
means a scout dispatch with a bare relative path is silently left out of that comparison. That is a FALSE NEGATIVE of
a calibration count.

It never blocks and never raises a false alarm, so it is the allowed direction for a detector. But "harmless"
overstates it: it is a blind spot that only the template discipline closes. RUNBOOK item 11 states the rule (backticks,
fill the id and slug) but does not say the consequence plainly (N4).

### K9 — fixtures that gained a handoff line

Checked one by one in the diff:
- `test_description_check_applies_to_critic` and `…passes_for_critic_with_leading_token`: they still reach the label
  check. Meaning kept.
- `test_critic_without_dod_markers_not_blocked_by_check1`: kept.
- The echo-json given-path tests: kept; still a dispatch that passes.
- `test_owns_bare_word_no_longer_a_write_indicator`: the cut is still built on the owns word, as before, and check_cut
  returns 0. Kept.
- `test_decide_can_still_raise_on_a_non_string_description` and `test_main_exception_out_of_decide_…`: the line is
  NEEDED so the label regex is still reached. Kept.
- `_race_payload`: a critic gets a reviews path; other kinds keep "report". Kept.
- test_critic_snapshot: `_blocked_critic_payload` is still blocked by its label, and the M2-1 control still passes.
  Kept.
- The new e24 row asserts byte-identity, not the gate's code. It relies on the snapshot changing when it is rewritten.
  Weak but adequate.

No test lost its meaning. The one fixture that should have gained a line and did not is the liveness probe (B2).

## Trail (node A)

- Read:
  - spec t-366 §0, §A (lines 1-336), §C.7(c) (780-791) and §D (821-865);
  - the builder handoff t-387, by grep at b615e4e;
  - `docs/SIBLING_MAP.md` axis 13 (311-330);
  - the commit message of b615e4e;
  - the full code diff of the 5 source files and the 4 test files.
- Read in the b615 extraction:
  - `dispatch_gate.decide_full` (775-830) and `_load_manifest_module`;
  - `dispatch_manifest._import_siblings`, `section_cut` and `_scan`;
  - the MANY rendering in `handoff_gate`;
  - `hook_liveness_probe._case_10_critic_snapshot` and its registry entry;
  - `test_hook_liveness_probe.py:980-995`;
  - the matchers in `.claude/settings.json`.
- Probes (python on stdin, importing the b615 and a537 extractions):
  - `decide_full` over the K3 dispatch set, plus the cut-raise monkeypatch (B1);
  - case 10's payload at both commits (B2);
  - 156 past critic/designer Agent dispatches from 9 transcripts.
- Greps:
  - code that builds critic/designer payloads with `subagent_type` (3 files; positive control: 11 builder files);
  - readers of the handoff section;
  - `resume`/`SendMessage` in the gates and the transcripts.
- Control re-run, on the clean b615 extraction (not the worktree, which holds node B's unstaged edits):
  `python -m pytest tools/test_dispatch_gate.py -q -k handoff` → `48 passed, 263 deselected in 1.34s`.
- Mechanical layer attached by the dispatcher (907 / 280 / 763 passed; RUNBOOK keys + negative control True): it is
  consistent with the diff. The rows it claims exist, and my narrow re-run matches. It does not include
  `test_hook_liveness_probe.py`, which is how B2 slipped through.

---

# Section 2 — node B, F6-35 (WORKTREE BASE WARN)

Reviewed: `git -C C:\QAFactory\forge-repo\.claude\worktrees\f6-37 diff b615e4e 6081dce` (5 files, 299+/17-), by the
commit range. Probes ran on a clean `git archive 6081dce tools` extraction. Line numbers are of 6081dce.

Spec/DoD: t-366 §B whole (§B.2 steps 0-5, §B.3 error direction and limits (1)-(3), §B.4 rows); builder handoff t-394.

## Verdict (node B)

**fit: 0 blocking findings, 6 non-blocking.**

- The WARN is correct on real git. I built a temp repo with a bare origin, an ahead branch and a merged branch. Real
  `merge-base --is-ancestor` exits 1 for the ahead branch and 128 for a missing ref, so the "no origin/main" case stays
  silent.
- It never blocks: it runs after `write_verdict(payload, "allow")`, inside its own `try`.
- Node A's check order is untouched.
- The three carriers name one road.

The non-blocking items are polish or measured limits that the spec already names.

## Non-blocking findings (node B)

- **NB1 (KB6) Two `for-each-ref` calls where the spec has one.** `dispatch_gate.py:1898` reads heads+remotes, and
  `:1903` reads heads again to build `local`. So an isolation dispatch costs up to 8 git calls (2 for-each-ref, 5
  merge-base, 1 rev-parse), against "up to 6" in §B.5 (a).
  - Fix: one call with `--format=%(refname)` and derive both sets from the `refs/heads/` / `refs/remotes/` prefixes.
  - Direction is safe as it stands: if the second call fails, a local name is looked up as `refs/remotes/<name>`, git
    exits 128, and the WARN stays silent. Traced; no test covers it.
- **NB2 (KB6)** `:1925` `shown = kept` is a dead alias.
- **NB3 (KB5) The two WARN doors differ slightly.**
  - The push WARN door (`:1882`, spec text of §B.2 step 1) reads `git worktree add <path> -b <branch> main`.
  - The base WARN, RUNBOOK item 8 and builder-rules item 20 read `git -C <repo> worktree add <path> -b <branch> <base>`.
  - Same road, one missing `-C <repo>`. This is cosmetic, but by P31 the doors could share one constant.
- **NB4 (KB6) The test table is hard to read.**
  - In `test_worktree_base_warn`, `rc_other` is remapped inside the test (`other = 0 if rc_other == 1 else rc_other`).
  - Row b8 re-patches `subprocess.run` inside the shared body.
  - Row b11 ("local and remote with the same short name") cannot happen in real git: `refname:short` gives `wip/x` and
    `origin/wip/x`. The row really pins "a local name is checked by its local ref", which is still worth keeping.
  - None of this weakens an assertion.
- **NB5 (KB3) Measured false-ish WARNs, inside the named limit (1).** I replayed the 56 past `isolation: worktree`
  Agent dispatches against today's refs of the root repo. 5 warned, from 2 distinct dispatches:
  - (a) OH4-1: `Branch: pile/onboarding-hooks/batch-4 from origin/main` is the branch the builder itself CREATES
    (`-b …`).
    - It warns today only because that branch exists now, so this is a replay artifact.
    - A retry or dead-worker replacement of such a task WILL warn, though, since attempt 1's branch now exists and is
      ahead. That is right if attempt 1's commits are wanted, and noise if the branch is to be recreated.
  - (b) FG7-8: `commit 9bc6f5c on origin/held/tr2-9` is a cherry-pick source.
    - A host worktree shares the repo's refs and objects, so the worker can reach it. The WARN is a false positive.
  - Both fall under limit (1): the text names the branch, and check 45 measures fatigue.
  - Optional fix: one clause in the WARN, "(ignore if the worker is told to merge or cherry-pick it)".
  - Prose words that collide with branch names are a low risk in this repo. Of 235 short names, the only ones without
    a slash are `main`, `origin` (both excluded) and `worktree-agent-<hash>`.
- **NB6 (witness) The DOC-DISPATCH WITNESS checks only half of its keys.**
  - Its negative control removes a PRESENT key, so the ABSENT-key half (`сначала слей`) was never shown to fail when
    the key is present.
  - The rule's "one negative control" is met.
  - I confirmed absence independently: `git grep -i -E "сначала слей|merge <x> first"` at 6081dce over `*.md`, `*.py`
    and `*.yaml` (task history excluded) finds only the test's own `not in` assertion. Positive control:
    `создать worktree самому` found in `plans/builder-rules.md`.

## Keys (node B)

### KB1 — fit to the spec per row

| row | status | evidence |
|---|---|---|
| b1 ahead branch → WARN with name and origin sha | met | row b1; real-git probe "ahead branch named" warns with the full sha |
| b2 ancestor → silent | met | row b2; real-git probe "merged branch named" silent |
| b3 no isolation / `none` / Bash / tool_input None | met | `test_worktree_base_warn_b3_only_host_worktrees`; probe "no isolation (Lead's worktree)" silent |
| b4 main / origin/main / HEAD only | met | row b4 (`main,` stripped, then excluded); probe silent |
| b5 7 names → 5 + "(2 more names not checked)" | met | row b5 |
| b6 exactly 5 → no "more" | met | row b6 + explicit assert |
| b7 backticked / trailing comma | met | rows b7a, b7b |
| b8 for-each-ref fails / exit 128 / OSError | met | rows b8, b8c; `test_worktree_base_warn_b8_for_each_ref_fails` |
| b8a exit 1 → WARN, exit 0 → silent | met | rows b8a, b8b |
| b9 None / "" / 300 KB | met | rows b9a-c |
| b10 Cyrillic name | met | row b10 |
| b11 dedup, local ref first | met as "local ref first" (the same-short-name case cannot occur, NB4) | row b11 asserts one is-ancestor call on `refs/heads/wip/x` |
| b12 push WARN on qualified argv only | met | `test_worktree_base_warn_b12_…` + the three edited push tests |
| b13 fenced name silent, prose control warns | met | `test_worktree_base_warn_b13_…`; real-git probe "fenced mention" silent |
| b14 bare remote-only name silent (limit 2) | met | row b14 |
| §B.2 step 1 push WARN: qualified refs, `_isolation_dispatch`, one-road door | met | `:1864-1883` |
| step 1b `_isolation_dispatch`, one guard | met | `:1856-1861`, called by both WARNs |
| step 1c `_git_rc` | met | `:1848-1853` |
| step 2 `worktree_base_warn` order 1-5 | met; extra for-each-ref (NB1) | `:1892-1932` |
| step 3 `main()` wiring after `warn_push`, own try | met | `:2185-2188`, `warn_parts` order |
| step 4 RUNBOOK item 8 | met; verbatim spec text | diff |
| step 4a builder-rules item 20 | met; only that clause changed | diff |
| WARN text | met | real-git probe output matches the template, incl. door and `RUNBOOK §12 item 8` |

### KB2 — error direction: a WARN, never a block

| unknown | behaviour | test / proof |
|---|---|---|
| not an isolation dispatch | `""` | b3 |
| `for-each-ref` fails (non-zero or empty) | `""` | b8 (`_base_git(None)`) |
| git missing / OSError anywhere | `_git_out` → None, `_git_rc` → None → silent | b8 (`boom`), b8c |
| no `refs/remotes/origin/main` | is-ancestor exits 128 → skipped → silent | row b8 (fake 128) + REAL git: missing ref rc=128 |
| is-ancestor exit other than 0/1 | skipped | row b8 |
| more than 5 names | names 6+ are not checked; WARN only if one of the first 5 is ahead; else silent | b5 |
| quoted line (fence/blockquote) with a cut | not read | b13 |
| degraded cut or no cut | whole prompt read, quoted lines included: possibly a WARN, never a block (§B.2 step 3 says so) | traced `:1904-1908` |
| second for-each-ref fails | local names looked up as remote refs → 128 → silent | traced (NB1) |
| an exception inside the WARN | `warn_base = ""` | `main()` `:2185-2188` |
| the verdict | already written as `allow` before the WARN layers | `main()` flow (`write_verdict(payload, "allow")` precedes the warns) |

### KB3 — false WARNs on dispatches that are fine today

Real-git probe (temp repo; `wip/ahead` ahead of origin/main, `wip/merged` an ancestor, `review` a local ahead branch):

| dispatch | result |
|---|---|
| a branch already in origin/main (`wip/merged`) | silent |
| a worktree the Lead made itself (no `isolation`) | silent |
| a branch named only inside a fence | silent |
| a branch inside a path (`C:/repo/wip/ahead/x.py`) | silent |
| `origin/main..wip/ahead` (range token) | silent (one token, no match; silence direction) |
| an ahead branch mentioned in prose | WARN (limit 1) |
| an ahead branch in backticks | WARN (limit 1; b7 makes backticks a match on purpose) |
| a prose word equal to an ahead branch (`review`) | WARN (limit 1) |

History, by replay: 2 distinct false-ish WARNs over 56 dispatches (NB5). That is acceptable for a WARN, and the spec
names it as limit (1).

### KB4 — node A's order and `push_before_launch_warn`

- The diff b615e4e..6081dce has hunks only at `dispatch_gate.py:1845+` (helpers, the two WARNs) and `:2116+`
  (`main()` warn list).
- `decide_full`, `handoff_folder_check` (still at `:736`) and the module docstring are untouched. So node A's order
  (completeness → handoff folder → paths → label) holds.
- `push_before_launch_warn` keeps its invariants:
  - origin ahead or equal → silent;
  - a git error → silent.

  Both are pinned by the edited push tests, now on qualified argv. The fake answers only the qualified argv, so a
  return to the short form would fail b12.
- The base WARN comes after `warn_push` in `warn_parts`.

### KB5 — the documents say the same move as the WARN

- RUNBOOK item 8 (spec verbatim): the host cuts from origin/main; for another base, the coordinator creates the
  worktree (`git -C <repo> worktree add <path> -b <branch> <base>`) and dispatches without isolation; the gate WARNs
  (WORKTREE BASE).
- builder-rules item 20: "запушить `main` либо создать worktree самому (`git -C <repo> worktree add …`) и диспатчить
  без `isolation`".
- Base WARN door: the same command with the named branch.
- Push WARN door: push, or the same command from main.
- The retired road ("merge <sha> first" / «сначала слей») survives in no carrier (NB6 grep).
- One cosmetic difference: NB3.
- Note: item 8 no longer carries the old line "the dispatch text must carry the fallback, the branch then lives in the
  main repo". That is the spec's verbatim choice, consistent with the one road.

### KB6 — duplication and code quality

- Duplication:
  - NB1: two for-each-ref calls.
  - The `cwd = payload.get("cwd") if isinstance(...)` line is repeated in both WARNs (2 lines; tolerable).
  - NB3: the door text exists twice.
  - Grepped: `for-each-ref`, `isolation`, `worktree add` in `dispatch_gate.py`.
- The isolation guard became one function (`_isolation_dispatch`), with no copy left: this removes a duplicate.
- `_BASE_TOKEN_STRIP` is a different set from `dispatch_manifest._TOKEN_STRIP` on purpose (it also strips punctuation
  around prose tokens). That is not a clone.
- Code quality: NB2 and NB4. Nothing blocking.

## Trail (node B)

- Read:
  - spec t-366 §B (337-505) and §D.1;
  - the diff b615e4e..6081dce (all 5 files);
  - `dispatch_gate.main()` flow at 6081dce (warn wiring, `write_verdict` order);
  - builder handoff t-394 (by grep: witness `332 passed in 22.38s`, the DOC witness script and its negative control).
- Probes (python on stdin, importing the 6081dce extraction):
  - a temp git repo (bare origin, `wip/ahead`, `wip/merged`, `review`): real exit codes (ahead rc=1, missing ref
    rc=128, missing origin rc=128) and `worktree_base_warn` on 9 dispatch shapes; push WARN silent with main equal to
    origin;
  - a replay of 56 past isolation dispatches against the root repo's refs → 5 WARNs, 2 distinct dispatches.
- Greps:
  - the root repo's slashless branch names (235 refs);
  - the retired road across carriers, with a positive control.
- No pytest re-run for node B: the one allowed control run was spent on node A. The attached `332 passed` (builder) and
  `332 passed in 21.07s` (Lead) agree with the 16 parametrized rows + 5 tests the diff adds; checked for consistency,
  not re-run.

```json
{
  "verdict": "fit_with_fixes",
  "per_node": {"F6-37 (a537391..b615e4e)": "fit_with_fixes, 2 blockers", "F6-35 (b615e4e..6081dce)": "fit, 0 blockers"},
  "blockers": [
    "F6-37 B1 tools/dispatch_gate.py:752 with :793/:806 -- when cut_payload/section_cut raises (e.g. an owns_gate or md_regions import failure in dispatch_manifest._import_siblings), cut stays None and handoff_folder_check refuses every critic/designer dispatch with a FALSE 'It has no handoff: line'; probe: a correct critic dispatch, section_cut raising, gives code=2 (before the diff: pass with MANIFEST-UNCHECKED). Breaches spec A.4 / K2; spec step 3.3 conflicts with A.4.",
    "F6-37 B2 tools/hook_liveness_probe.py:898 -- case 10 sends a critic dispatch with handoff <tmp>/review.md (not in docs/tasks/specs/reviews); decide_full at a537391 gives 0, at b615e4e gives 2 WRONG_FOLDER; case expects exit 0, so test_hook_liveness_probe.py::test_live_run_of_all_cases_is_ok fails on the CI canon and the post-merge liveness probe of spec D.2 fails."
  ],
  "fixes": [
    "F6-37 B1: in handoff_folder_check, cut None means NO_LINE only when the prompt lacks the handoff word (one public predicate beside cut_payload); otherwise NOTE_UNCHECKED and pass. Add row e25: section_cut raises on a correct critic dispatch -> code 0 + HANDOFF CHECK: not checked.",
    "F6-37 B2: hook_liveness_probe case 10 handoff -> <tmp>/docs/tasks/specs/reviews/review.md; owns widened by the Lead; witness python -m pytest tools/test_hook_liveness_probe.py -q -k live_run.",
    "F6-37 N1: HANDOFF_NO_PATH door names the absolute form instead of 'move the path into folder'.",
    "F6-37 N3: one sys.path/import prelude helper in dispatch_gate (three copies now).",
    "F6-37 N4: RUNBOOK item 11 says plainly that a bare relative scout path is invisible to the id-race detector; Lead corrects spec A.6 m1/m5 (+m1a/m5a) and A.5 text.",
    "F6-35 NB1: one for-each-ref call (full refnames) instead of two; NB2: drop the dead alias shown = kept; NB3: one door constant with git -C <repo> for both WARNs; NB5 optional: WARN clause 'ignore if the worker is told to merge or cherry-pick it'."
  ],
  "class_completeness": "F6-37: axis 13 readers (handoff_gate._gate, dod_gate.named_handoffs, hop_metrics, the new check) agree; the three candidate loops became one (axis 34). Missed producer of critic payloads: hook_liveness_probe case 10 (B2; grep over tools/ finds exactly 3 builders of critic/designer payloads). Queued sibling: handoff_gate._gate MANY refusal unbounded (handoff_gate.py:180) vs the launch check's cap of 5 (N2). SIBLING_MAP axis-13 row owed by the Lead in the merge commit. F6-35: the isolation guard is one function for both WARNs; the one road is named by RUNBOOK item 8, builder-rules item 20 and both WARN doors; the retired merge-first road survives in no carrier (git grep at 6081dce with a positive control); calibration check 45 registration owed by the Lead (spec D.2).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-366-f6-37-f6-35-f6-58-specs.md (0, A, B, C.7c, D)",
      "b615e4e:docs/tasks/handoffs/t-387-f6-37.md (grep)",
      "6081dce:docs/tasks/handoffs/t-394-f6-35.md (grep)",
      "docs/SIBLING_MAP.md axis 13",
      "git diff a537391 b615e4e (all 10 files)",
      "git diff b615e4e 6081dce (all 5 files)",
      "b615e4e:tools/dispatch_gate.py decide_full, handoff_folder_check, _load_manifest_module",
      "b615e4e:tools/dispatch_manifest.py _import_siblings, section_cut, _scan",
      "b615e4e:tools/handoff_gate.py handoff_candidates, _gate",
      "b615e4e:tools/hook_liveness_probe.py case 10 and registry",
      "b615e4e:tools/test_hook_liveness_probe.py test_live_run_of_all_cases_is_ok",
      "6081dce:tools/dispatch_gate.py _git_rc, _isolation_dispatch, push_before_launch_warn, worktree_base_warn, main warn wiring",
      ".claude/settings.json matchers"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_dispatch_gate.py -q -k handoff (clean git archive of b615e4e)", "result": "48 passed, 263 deselected in 1.34s"},
      {"command": "decide_full probe: correct critic dispatch with dispatch_manifest.section_cut raising (b615e4e)", "result": "code=2 HANDOFF NO_LINE (B1)"},
      {"command": "decide_full on hook_liveness_probe._case_10_critic_snapshot payload at a537391 / b615e4e", "result": "0 / 2 WRONG_FOLDER (B2)"},
      {"command": "replay of 156 historical critic/designer Agent dispatches through handoff_folder_check", "result": "150 pass, 6 refused; all 6 also refused by the write gate"},
      {"command": "temp git repo: merge-base --is-ancestor ahead / missing origin ref / missing branch ref", "result": "rc 1 / 128 / 128"},
      {"command": "worktree_base_warn (6081dce) on 9 dispatch shapes with real git", "result": "WARN on ahead branch (prose, backticks, prose word); silent on merged, no isolation, fenced, path, range token, main/origin"},
      {"command": "replay of 56 historical isolation dispatches through worktree_base_warn against root refs", "result": "5 WARNs from 2 distinct dispatches, both inside named limit (1)"}
    ]
  }
}
```
