# Coordinator offload: journal by code, safe for parallel sessions; test volume in the roles (r2, t-845 = fix round of t-842)

status: DRAFT r2 by designer (t-845) for Lead acceptance; r1 (`20261114-coordinator-offload-spec.md`) is left untouched.
This file is SELF-CONTAINED: a builder dispatch points here, not at r1. §0 and §11 are carried from r1 verbatim. Forks
decided in §11 stay decided; NEW forks raised by this round are in §9' and are RETURNED, not decided — every node is
executable by the recommendation until the Lead answers (PROJECT.md «Командная работа» п. 11).
scope: forge tooling only. `ai-packages/qa-factory/` is not edited, so no AR-n of `design/architecture.md` applies
(`architecture: none -- forge tooling` on every commit of this spec). One forge file imports a package script (F-B1-3 (a):
`hooklib.append_jsonl_line`) — that is a READ of the package, named on axis 3 (§7), not a package change. CLAUDE.md rule 10
(four questions, axis enumeration) applies: §7.

## 0'. Verdict items -> how closed -> where in r2

Verdict: `docs/tasks/specs/reviews/20261114-coordinator-offload-plan-critic.md` (t-844, GO WITH FIXES). X-n = defects this
round found itself while closing the verdict (designer rule 3: reported, closed in the text, listed so the Lead sees them).

| Item | How closed | Where in r2 |
|---|---|---|
| BL-1 9a' refuses reserved/pre-issued ids landing out of order | rule 9a'' = "never seen (full id) + at most `ID_JUMP_MAX` above the letter's max"; the writer adds the machine-local check "issued by this clone's counter"; new rows: reserved lower id after a higher one is legal; `next --n 3` used in reverse order is legal | §3.B0 item 2, E-B0-3/4/8; §3.B1 E-B1-13; §3.B5 D4 |
| BL-2 `accept --run` inside the journal lock | POSITIONAL invariant: `--run` executes and `--witness-file` is read BEFORE the lock; the lock covers read → validate → append → counter only; row "30 s run in A while B's hook writes" | §3.B1 "Order of one write", E-B1-14 |
| BL-3 `shell=True` = cmd.exe on Windows vs a Bash-judging gate | the run uses exactly the shell that was judged: `[bash, "-c", cmd]`, bash resolved and capability-probed; no bash → `--run` refused with the door `--witness-file`; the cmd.exe single-quote rows added; the alternative (shlex, metacharacters refused) is fork F-B1-4 | §3.B1 E-B1-8/9; §9' F-B1-4 |
| BL-4 C3 root refresh impossible after wave 1; `branch -d` before refresh | steps reordered: journal commit (W') → root refresh by the byte-copy dance under the `journal` lock → branch deletion last (`-d` when refreshed, else ancestor check + guarded `update-ref -d`); rows "two waves in a row", "hook append during the dance" | §3.C3 steps 8-10, E-C3-9..14 |
| BL-5 `returned` lost for a delegating session in a second worktree | an open-dispatch index `<common>/forge-journal/open/<agent_id>` written with `delegated`; fallback scan of every copy listed by `git worktree list --porcelain`; step 0 measures the stop's `cwd`; a pruned marker prints a WARN read by check 48(c); row "linked worktree, background launch" | §3.B23 step 0 (d), item 2-3, E-B23-10 |
| BL-6 A1/B0/B23 paths are mechanism paths; the tier gate refuses builder commits | landing protocol: a builder of a mechanism-path stream hands over a STAGED, UNCOMMITTED worktree + patch; a Fable session commits it with the §7 axis lines and its `tier:` line (fork F-LAND-1 for the alternative); A3 is a mechanism path too (X-3); C2 uses the skip line in its DoD; cost line moved | §2 "Landing", §4, §5; §9' F-LAND-1 |
| S-1 wrong model reader | `dispatch_gate.label_model_family(description)` exposed over `_LABEL_LEADING_TOKEN_RE` + `_model_family`; no family → no write + door | §3.B23 item 1, E-B23-3 |
| S-2 msvcrt mandatory lock hides the pid text | lock one byte at offset 4096; holder text in bytes 0-63, written after acquiring, never truncated; row "holder text readable while locked" | §3.B5 D1, E-B1-3 |
| S-3 `--git-common-dir` relative to cwd | `git -C <dir> rev-parse --path-format=absolute --git-common-dir`; a relative answer (old git) is resolved against `<dir>`, never the repo root; row "--repo at a subdirectory" | §3.B5 D1, E-B1-15 |
| S-4 B0 owns incomplete | B0 owns `test_journal_validator_merge.py`, `test_piles_take.py`, `test_piles_close_gate.py`, `test_transcripts.py` | §2 B0 row, §3.B0 tests |
| S-5 leftovers of the retired road | `compact_snapshot` next-id/band lines and the validator NOVELTY text name the writer | §3.B0 item 3 |
| S-6 critic.md rule 10 exam duty | `PROCESS/CRITIC_EXAM.md` is absent on disk (checked, §10'); A1's DoD names the duty and the deviation; fork F-A1-2; axis 2 line corrected | §3.A1 E-A1-3, §7 axis 2, §9' F-A1-2 |
| S-7 the F-B4-1 (a) gate has no owner | B23 owns it as the third entry `journal_hooks.py pre-edit` (WARN phase); switch node B23-S named with trigger and owner | §3.B23 item 7, §2 B23-S row |
| S-8 F-T1 (a) needs a carrier | the owner's word goes into TESTING.md «Бюджет / Файлы» by stream A2 (E-A2-1 relaxed to that one bullet); the scope of the exception is fork F-T1-2 | §3.A2, §6.2, §9' F-T1-2 |
| S-9 C1 in the same wave as B0 | C1 moves to wave 2, based on B0's branch tip | §2, §5 |
| S-10 B1 base branch | B1 (and C1) branch from B0's committed branch tip; B0's merge is held until B1 is accepted; two rejects of B1 → F-ORD-1 (b) | §2 "Landing", §5 |
| S-11 letter refusal too wide | refused only when ISSUING a brand-new id | §3.B1 E-B1-2 |
| S-12 dod_track classifies writer calls | B1: stdout never echoes witness or notes text; B23 owns `dod_track.py`: a `tools/journal_write.py` call is never a verification run; row in `test_dod_track.py` | §3.B1 E-B1-16; §3.B23 item 8 |
| S-13 transitive import closure | the prefix list is taken from the closure test; the launch-id reader moves to `transcripts.py` so hop_metrics' import tree stays out of live hooks; axis 3 line rewritten | §3.B23 items 1, 5; §7 axis 3 |
| S-14 C3 journal copy without the lock | every read of the root journal in C3 is under `machine_lock("journal")` | §3.C3 steps 8-9 |
| N-1 leading zeros | canonical form for NEW ids (`t-001`..`t-999`, then no leading zero); reading stays permissive and string-keyed | §3.B0 item 1, E-B0-1 |
| N-2 first id of a new letter | `t-001a` stated | §3.B0 item 2 |
| N-3 «123А» vs `t-123a` | listed as «решила сама» for the owner | §8 item 11 |
| N-4 amend | stated: the WARN measures the delta against the amended HEAD (per commit) | §3.A3 E-A3-9 |
| N-5 the builder text restates the rule; builder-rules 7d unowned | builder.md holds a duty sentence + pointer only; A1 owns `plans/builder-rules.md` 7d and turns it into the same pointer | §3.A1, §6.1 |
| X-1 B1 (wave 2) called `hygiene_gate.run_allowed`, which r1 gave to B23 (wave 3) | `run_allowed` and the door text move to B0 (wave 1) | §2 B0 row, §3.B0 item 9 |
| X-2 the launch `tool_response` is a DICT with an `agentId` field (async: `status: "async_launched"`; `negative_lint.py:203-219`), not only text; a later second PostToolUse for the same agent is described there | one reader `transcripts.launch_agent_id(obj)`: field first, text regex second; post-agent is idempotent per worker_ref; step 0 measures both | §3.B23 step 0 (e), item 1, E-B23-12 |
| X-3 `.githooks/commit-msg.proposed` matches the `.githooks/` directory prefix (`mechanism_gate._matches`) | A3's commit carries the skip line with its reason (inactive proposal) | §2 Landing, §3.A3 |
| X-4 `piles.py` `TASK_RE = t-\d{1,6}` and its tests use `t-1`; done regexes `t-\d+` fullmatch refuse a letter | piles reads through the one grammar; test rows rewritten to 3-digit ids; done cells accept the letter | §3.B0 item 1, E-B0-9 |
| X-5 deleting a branch checked out in a worktree (`update-ref -d` would orphan that worktree's HEAD) | the worktree is removed first when clean, else the branch is kept and printed | §3.C3 step 10, E-C3-12 |
| X-6 F-C3-1 was reversed to (b) in §11 but r1 §3.C3 still refused on red and carried `--despite-red` | C3 prints the last known state, never waits, never refuses; the flag is gone | §3.C3 step 4 |
| X-7 F-B1-2 (a) needs callable echo collectors; `journal_echo` (B0) has only private `_collect_*` | B0 exposes `journal_echo.echo_for_lines(...)`; the witness echo is skipped for `witness_by: run` | §3.B0 item 10 |
| X-8 a scan of every worktree copy per stop is costly (dozens of worktrees here) | the open-dispatch index makes the normal path O(1); the scan reads tails only | §3.B23 item 2 |
| X-9 `hygiene_gate.decide` fails OPEN on exceptions; reused as the only check before `--run` | `run_allowed` fails CLOSED (exception or WARN-class result → refuse) | §3.B0 item 9, E-B1-9 |

## 0. The owner's words (14.11.2026, verbatim)

1. «Координатор тратит много ходов для того что бы вести журнал. Нельзя это как-то оптимизировать? Например создать
   скрипт который будет автоматически вести лог начала и конца диспачей? И вообще как уменьшить количество ходов
   координатора не связанных с тем что может делать только ИИ»
2. «все эти пункты реализовать, но убедится что они будут работать если разрабатывают две параллельные сессии на одном
   компьютере»
3. On the hygiene rule «журнал пишется только через Edit/Write»: «это было правило для экономии токенов модели, так как
   сейчас писать будет код то экономия только больше. Я своим словом разрешаю»
4. On id collisions between parallel sessions: «придумать что-то что решить эту проблему. Например пусть добавляют буквы.
   Номер 123 и 123А»
5. New event `returned` for the end of a dispatch: «ок».
6. Test volume: «Перенести правило в роль билдера и критика, в роли билдера дать ссылку на файл тестинг. Убедиться что в
   файле тестинг есть объяснение как делать эффективные тесты на нашем проекте. Поставить варн хук на случай если строк
   тестов больше чем строк кода билдера». WARN placement (Lead's brief): a commit-msg hook.

Carrier of the words: the Lead's intent brief of t-842 (journal line `logs/journal/dev1.jsonl:2065`, notes). The words are
quoted from the brief; whether they were said in a session with the owner is the Lead's to confirm (PROJECT.md «Командная
работа» п. 6).

## 1. Corrections to the brief (facts read in the carriers; designer rule 3)

K1-K10 are carried from r1 (accepted as facts in §11); K11-K17 are new in r2.

| # | Brief said / implied | The carrier says | Consequence |
|---|---|---|---|
| K1 | `dispatch_gate.py` "only reminds" that `dispatch_skipped` is owed | the reminder is `DESIGNER_SKIP_NOTE_TEMPLATE` in `tools/dispatch_manifest.py:155-157`; dispatch_gate calls the manifest | B23 reads the skip reason through the manifest's cut (one reader, axis 13) |
| K2 | hygiene_gate must be taught a legal road | the journal is refused only as a LITERAL write target (`_add_target` :1282-1291, `_dotnet` :1369-1374, `_decide_command` :1509-1519); `python -B tools/journal_write.py ...` names no such target and already passes (hygiene pt.4a) | the CODE change is the door text (`MSG_JOURNAL_BLOCK` :82-85) and `run_allowed()` (B0 item 9); the rule TEXT changes are Lead's |
| K3 | the writer's lines get the echo checks | `journal_echo.py` triggers ONLY on `tool_input.file_path` (:499-508, :2351-2352) | F-B1-2 (a) decided; X-7 |
| K4 | a letter suffix only needs the validator | `journal_keys.CLOSES_RE` reads `closes:t-123a` as closes `t-123` (critic re-ran it); `REF_RE`, `ID_NUM_RE`, `BAND_RE`, validator `TASK_ID_RE = ^t-(\d{3,})$` (:355, `\d` also matches fullwidth digits) refuse or misread a letter; pinned fallback copies in `session_context`, `calibration_counts` | B0 owns every reader (census by Grep, critic's wider Grep found no other) |
| K5 | a shared counter is enough | rule 9a: a new id is EXACTLY the file's next id (`BandState.may_issue`, journal_keys.py:337-347); worktree copies would see gaps | rule 9a'' (§3.B0 item 2) |
| K6 | builder.md lacks the volume rule | `plans/builder-rules.md` 7d (:57-58) and `docs/tasks/critic-diff-brief.md` Q5 (:41-42) already carry it; the rule's owner is TESTING.md «Бюджет / Объём» (:115-116) | F-A1-1 (b) decided; N-5 |
| K7 | a SubagentStop hook can write `returned` beside dod_gate | dod_gate may BLOCK the stop (exit 2); sibling hooks cannot see that | F-B3-1 (a) decided |
| K8 | hook files are edited by builders | `.claude/settings.json` and `.githooks/commit-msg` are self-activating: builders write `.proposed` neighbours, the Lead places | B23/A3 DoDs |
| K9 | worker_ref of the launch equals SubagentStop `agent_id` | an ESTIMATE; foreground order too | B23 step 0 |
| K10 | category values | builder→`implementation`, critic→`review`, scout→`recon`, designer→`spec` (dev1.jsonl:2053-2065) | `AGENT_ROWS` |
| K11 | (r1) only stream L needs Fable | `mechanism_gate.MECHANISM_PREFIXES` (:211-275) names `.claude/agents/`, `.githooks/` (a DIRECTORY prefix: `_matches` :370-375 is `startswith` for a `/`-ending prefix, so `.githooks/commit-msg.proposed` is a hit), journal_validator, journal_keys, session_context, journal_echo, compact_snapshot, forge_metrics, piles, dispatch_manifest, dispatch_gate, dod_gate, dod_track, hygiene_gate, mechanism_gate, transcripts, ci_read, ci_read_common; `.claude/settings.json` is an EXACT-file prefix, so `.claude/settings.json.proposed` is not a hit. `decide_full` (:939-968) requires a `tier:` line passing the lead binding (`delegation.config.yaml` roles.lead = `claude-fable-5-1`); a skip line `axes: not a mechanism (...)` bypasses both the axis and the tier check; a MERGE is exempt | §2 Landing (BL-6) |
| K12 | (r1) the model is read with `LABEL_MODEL_PREFIX_RE` | that regex is `^\S+[ :-]`, deliberately not a tier list (dispatch_gate.py:1034-1041); the tier reader is `_LABEL_LEADING_TOKEN_RE` (:1041) + `_model_family` (:1047-1057), both private | S-1 fix; B23 owns dispatch_gate for the public wrapper |
| K13 | (r1) the launch id is a text `agentId: <id>` | that is the TRANSCRIPT tool_result text hop_metrics reads (:89, :345); the PostToolUse `tool_response` of an async launch is a dict (`isAsync`, `status: "async_launched"`, `agentId`, `description`, `resolvedModel`, `prompt`) per `negative_lint.py:203-219`, which also says the worker's final result "arrives as a SEPARATE, later PostToolUse event" (a source-deployment observation, not measured here) | X-2; step 0 (e)/(f) |
| K14 | (r1) importing hop_metrics' regex into a live hook is free | hop_metrics imports dispatch_manifest, handback_extract, journal_keys, journal_validator, streams, transcripts (:69-74); the closure test (`test_mechanism_gate.py:1372-1383`) would demand `handback_extract`, `streams`, `hop_metrics` in the net | the reader moves to `transcripts.py` (already in the net) |
| K15 | (r1) piles reads ids like the journal | `piles.py:3223 TASK_RE = t-\d{1,6}`; `LEFTOVER_DONE_RE` (:2687) and `PROOF_DONE_RE` (:3002) are `t-\d+` used with `fullmatch` (:2832); `test_piles_take.py:336-392` uses `t-1`, `t-2`, `t-9` and the message "1-6 digits" | X-4 |
| K16 | (r1) `run_allowed` can just reuse the gate | `hygiene_gate.decide` "fails open VISIBLY" on any exception (:1560-1563) | X-9: the wrapper fails closed |
| K17 | (r1) dod_track only sees real test runs | `VERIFICATION_COMMAND_RE = pytest|python\s+-m\s+pytest|python\s+.*test` (dod_track.py:127-128) matches any `python ... journal_write.py accept --run "...pytest..."`; outcome = rc field when present, else text (passed/ok vs failed/error), default red (:44-52, :275-294) | S-12 |

## 2. Streams, owned paths, order, landing

Each stream is one builder dispatch. Owned paths do not overlap inside a wave (a test file owned by streams of DIFFERENT
waves is legal: the later stream branches after the earlier merges or from its tip). Every builder works in its own
worktree; nothing is live until merged and, for hook files, placed by the Lead.

All paths below are under `C:\QAFactory\forge-repo\`.

| Stream | Owns | Depends on | Wave | Lands by |
|---|---|---|---|---|
| A1 | `.claude\agents\builder.md`, `.claude\agents\critic.md`, `plans\builder-rules.md` (item 7d only) | — | 1 | Fable commit (mechanism path) |
| A2 | `docs\TESTING.md` | — | 1 | builder commit |
| A3 | `tools\test_volume.py` (new), `tools\test_test_volume.py` (new, F-T1), `.githooks\commit-msg.proposed` (new) | — | 1 | builder commit with the skip line (X-3) |
| B0 | `tools\journal_validator.py`, `tools\journal_keys.py`, `tools\session_context.py`, `tools\journal_echo.py`, `tools\compact_snapshot.py`, `tools\calibration_counts.py`, `tools\piles.py` (only `TASK_RE`, `LEFTOVER_DONE_RE`, `PROOF_DONE_RE`), `tools\dispatch_manifest.py` (id regex, `designer_skip_reason`, the header lines of F-B2-1 (a)), `tools\forge_metrics.py` (event kind), `tools\hygiene_gate.py` (door text + `run_allowed`), and tests `tools\test_journal_validator.py`, `tools\test_journal_validator_merge.py`, `tools\test_journal_keys.py`, `tools\test_session_context.py`, `tools\test_journal_echo.py`, `tools\test_calibration_counts.py`, `tools\test_compact_snapshot.py`, `tools\test_dispatch_manifest.py`, `tools\test_forge_metrics.py`, `tools\test_hygiene_gate.py`, `tools\test_transcripts.py` (peer_note rows only), `tools\test_piles_take.py` (task-id rows only), `tools\test_piles_close_gate.py` (done-cell rows only) | — | 1 | Fable commit on its branch; merge HELD until B1 is accepted |
| C2 | `tools\ci_read.py`, `tools\ci_read_common.py`, `tools\test_ci_read.py` | — | 1 | builder commit with `axes: not a mechanism (a read-only CLI subcommand)` |
| B1 | `tools\journal_lock.py` (new), `tools\journal_write.py` (new), `logs\journal-letters.json` (new), `tools\test_journal_write.py` (new, F-T1; covers journal_lock too) | B0 (branch from B0's committed tip) | 2 | builder commit; merged right after B0 (F-ORD-1 (a)) |
| C1 | `tools\dispatch_new.py` (new), `tools\test_dispatch_new.py` (new, F-T1) | B0's header grammar (branch from B0's tip) | 2 | builder commit; merged after B0 |
| B23 | `tools\journal_hooks.py` (new), `tools\test_journal_hooks.py` (new, F-T1), `tools\dod_gate.py`, `tools\dod_track.py`, `tools\dispatch_gate.py` (`label_model_family` only), `tools\transcripts.py` (`launch_agent_id` only), `tools\hop_metrics.py` (import of the launch reader only), `tools\mechanism_gate.py` (`MECHANISM_PREFIXES`), `tools\hook_liveness_probe.py`, `.claude\settings.json.proposed` (new), tests `tools\test_dod_gate.py`, `tools\test_dod_track.py`, `tools\test_dispatch_gate.py`, `tools\test_transcripts.py` (launch reader rows), `tools\test_hop_metrics.py`, `tools\test_mechanism_gate.py`, `tools\test_hook_liveness_probe.py` | B1 | 3 | Fable commit (mechanism paths) |
| C3 | `tools\wave.py` (new), `tools\test_wave.py` (new, F-T1) | B1 (`journal_lock`) | 3 | builder commit |
| L | rule texts: `CLAUDE.md`, `PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md`, `docs\SIBLING_MAP.md`, `DECISIONS.md` entry, PROJECT.md «Командная работа» п. 1/12 and `docs\RUNBOOK.md` §7 (F-C3-2 (a)); placement of `.claude\settings.json` and `.githooks\commit-msg` | B23, A3 | after wave 3 merges | Fable session |
| B23-S | the switch of `journal_hooks.JOURNAL_EDIT_MODE` from `"warn"` to `"refuse"` (one data constant) + its test row | B23 live; trigger: calibration check 48 (a) shows one full window with zero by-hand journal lines | later | owner of the trigger: the Lead; executor: a builder (Fable commit: mechanism path) |

`AGENTS.md` is generated (`tools/agents_md.py`; pre-commit `--check`; SIBLING_MAP axis 4): every stream that changes an agent
file, `CLAUDE.md` or `.claude/settings.json` regenerates it on its branch; a merge conflict on it is resolved by
regenerating, never by hand. No stream owns it.

### Landing (BL-6, K11; fork F-LAND-1 holds the alternative)

- A mechanism-path stream (A1, B0, B23, B23-S) is landed by a Fable session: the builder does NOT commit. Its handoff
  names the worktree, carries `git -C <wt> diff --cached --stat` and a patch file
  `docs/tasks/handoffs/<task>-<stream>.patch`, and the witness run on the staged tree. The Fable session (after critic and
  acceptance) commits on the stream's branch with the §7 axis lines of that stream's mechanisms and its own `tier:` line,
  then merges (a merge is exempt from the gate). Invariant: no commit ever carries a `tier:` line naming a model that did
  not make it; no real mechanism change carries the skip line.
- A3 touches `.githooks/commit-msg.proposed` (a directory-prefix hit) but makes nothing live: its commit carries
  `axes: not a mechanism (inactive proposal; the Lead places .githooks/commit-msg in stream L, whose commit carries M2's
  axis block)`. The critic of topic A judges whether that reason holds.
- C2 commits with `axes: not a mechanism (a read-only CLI subcommand)`.
- B1, C1, C3 touch no prefixed path at their time (B23 adds their files to the net later); their commits carry the axis
  lines of §7 for M3/M7/M6 (rule 10 (b) is owed for a mechanism whatever the gate sees).
- B0 then B1 (S-10, F-ORD-1 (a)): the Fable session commits B0 on its branch and pushes it, without merging. B1 and C1
  branch from that tip. After B1 is accepted, B0 and B1 merge back to back (B0 first) in one session before any session
  issues the next id; C1 merges after B0. If B1 is rejected twice, F-ORD-1 (b) applies: B0 gets a one-line follow-up that
  keeps new bands legal (WARN) and merges alone.

Wave 1 = A1, A2, A3, B0, C2 (five writers). Wave 2 = B1, C1. Wave 3 = B23, C3. Critic: one pass per topic (A, B, C);
topic B touches the journal schema → critic mandatory (rule 3).

## 3. Behaviour per stream

### A1 — the volume rule in the builder and critic roles (F-A1-1 (b))

Behaviour (texts in §6.1):
- `builder.md` gains rule 8: tests are written by `docs/TESTING.md` (link, and its how-to section of A2); the volume duty
  as ONE sentence pointing at «Бюджет / Объём» with no restated number, plus the report line and the commit-message line
  `tests-over: <reason>` (A3's door).
- `critic.md` gains rule 20: tests are a standing question with its own verdict line, pointing at
  `docs/tasks/critic-diff-brief.md` question 5.
- `plans/builder-rules.md` 7d: its volume sentence («строк теста в диффе не больше строк продукта (больше — причина строкой
  отчёта)») becomes the same pointer: «объём тестов — `docs/TESTING.md` «Бюджет / Объём»; больше — причина строкой отчёта и
  строкой `tests-over:` в сообщении коммита». No other line of builder-rules changes.

Edges:
- E-A1-1 (owner's «перенести» vs axis 31 «one owner per aspect»): decided (b). Invariant: exactly ONE carrier (TESTING.md
  «Бюджет / Объём») holds the rule text; builder.md, critic.md, builder-rules 7d, brief Q5 hold a duty sentence + a pointer
  that names the section, never a restated number.
- E-A1-2 numbering: rules are appended (builder 8, critic 20); nothing is renumbered (`tools/test_handoff_rule_anchors.py`,
  `tools/tests/test_role_carriers_one_owner.py`, `tools/install_parity_anchors.json` pin by anchor). Invariant: every
  existing anchor is still found.
- E-A1-3 critic.md rule 10 (S-6): editing critic.md requires the exam in `PROCESS/CRITIC_EXAM.md` before the commit and a
  Runs-log line in the same commit. That file does not exist (Glob `PROCESS/*EXAM*` → `DEPLOYMENT_ECONOMY_EXAM.md`,
  `LEAD_RANKING_EXAM.md`). By F-A1-2's recommendation: the builder's report states the absence with that Glob as the trail;
  the Fable commit names the deviation in its message («critic.md rule 10: PROCESS/CRITIC_EXAM.md absent; exam not run;
  finding opened»); the Lead opens the finding (the critic's queue line). Invariant: the duty is never passed silently —
  either the exam ran or the commit names why not.

Tests: no new test. Witness: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_agents_md.py -q`
and `python -B tools/agents_md.py --check`, plus the DOC-DISPATCH key-presence run (keys quoted verbatim from the DoD
before the run, script attached in full, one negative control). Keys: `docs/TESTING.md`, `tests-over:`,
`critic-diff-brief.md question 5`, `«Бюджет / Объём»`.

### A2 — the how-to section and the F-T1 carrier in docs/TESTING.md

Behaviour:
1. A new section «### Как писать эффективный тест на нашем проекте» (text §6.2), after «### Бюджет» and before «### Когда
   тест покраснел». It gathers what the file already says; it adds no rule.
2. The carrier of the owner's F-T1 word (S-8): the bullet «**Файлы**» of «### Бюджет» (TESTING.md:117-123) gains ONE
   sentence (§6.2, by F-T1-2's recommendation), and the line «Чего больше нет: … нового тестового файла на новый скрипт»
   (:55) gains the pointer «(исключение — «Бюджет / Файлы»)».

Edges:
- E-A2-1 (relaxed for S-8): the diff touches, inside «### Бюджет», ONLY the «Файлы» bullet by appending that one sentence;
  the «Время» bullet (:124-125, open finding
  `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`) and the other bullets are
  byte-identical. Invariant: the pending owner question is not decided by this diff.
- E-A2-2: the section adds no number not already in the file (10 s, 60 s, ratio 1:1). Invariant: every number in the
  section appears elsewhere in TESTING.md.
- E-A2-3: forge tools tests — the section says where a tools case goes (the tool's own test file, a row); forge tests have
  no `keep` row (`test-layers.json` is the package's carrier).

Witness: DOC-DISPATCH key-presence run (keys: `### Как писать эффективный тест на нашем проекте`, `variants.json`,
`одна строка, которая падала до правки`, `20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`,
`слово владельца 14.11.2026`, `исключение — «Бюджет / Файлы»`), and `git diff --stat` showing only TESTING.md; negative
control mandatory.

### A3 — the test-volume WARN on commit

Behaviour: `tools/test_volume.py <msg-file>` reads the STAGED diff (`git diff --cached --numstat -M`), sums ADDED lines per
class, and prints ONE WARN line to stderr when `test_added > product_added` and the message carries no `tests-over:` line
with a non-empty reason. It ALWAYS exits 0. `.githooks/commit-msg.proposed` = the current hook plus, as its LAST line,
`python tools/test_volume.py "$1" || true`.

Classifier (data row `CLASSES` in the tool, first match wins; paths as git prints them, `/`):
1. excluded: `docs/**`, `plans/**`, `logs/**`, `kb/**`, `**/changelog.d/**`, `.claude/**`, `.githooks/**`, `experiments/**`
   except `experiments/measurers/**`, root files (`*.md`, `*.yaml`, `.gitattributes`, …);
2. test: a path with a segment `tests`, `test` or `fixtures`, or a basename `test_*.py`, `*_test.py`, `conftest.py`,
   `*_testkit.py`;
3. product: `ai-packages/**`, `tools/**`, `gateway/**`, `experiments/measurers/**` (code AND text);
4. anything else: excluded.
Error direction (a WARN): unsure → product (fewer WARNs; the leak shows in check 33's ratio).

Edges (the message file and the staged diff come from outside):
- E-A3-1 merge: `MERGE_HEAD` in the git dir → silent. Cherry-pick / revert not exempt (door). Invariant: a merge never
  WARNs; a non-merge test-heavy commit without a reason always WARNs.
- E-A3-2 binary (`-\t-\t`) skipped; a rename counts its added lines only.
- E-A3-3 `tests-over:` = a line starting with it (case-insensitive, leading spaces allowed), reason = the rest stripped;
  empty → WARN says "reason empty"; lines starting `#` ignored. Invariant: a commented-out door never silences the WARN.
- E-A3-4 `test == product` → no WARN; both zero → silent; product 0 and test > 0 → WARN.
- E-A3-5 message file absent / unreadable / not UTF-8 → `errors="replace"`; absent → as no door.
- E-A3-6 git missing / not a repo / numstat fails → `test_volume: not measured -- <reason>`, exit 0. Invariant: the tool
  never changes the hook's exit code (`|| true` and an outer try/except).
- E-A3-7 magnitude: a 50,000-line fixture → counted as test; the WARN prints the three numbers and the door.
- E-A3-8 POSITIONAL: last line of commit-msg, after the refusing gates. Invariant: a refused commit prints no volume WARN
  first, and a refusal is never masked (`set -e` stays).
- E-A3-9 `--amend` (N-4): the index is compared with the HEAD being amended, so only the delta of the amend is measured;
  the WARN is per commit, not per builder diff (a builder committing tests separately draws a WARN; the door covers it).
  Stated, not engineered around.
WARN text: `TEST VOLUME (WARN, the commit goes on): +<t> test lines vs +<p> product lines in this commit; name the reason in a line "tests-over: <reason>" of the message and in your report (docs/TESTING.md «Бюджет»).`

Tests: one parametrised table over (numstat text, message text, merge flag) → (warned, numbers): equal, test>product,
door present, door empty, door commented, merge, binary, rename, excluded only, git failure. Witness:
`python -m pytest tools/test_test_volume.py -q`.

### B0 — journal schema: the id with a letter, rule 9a'', bands retired, `returned`, the shared readers

Behaviour:
1. ONE id grammar in `journal_keys` (N-1, X-4):
   - READ grammar `ID_RE = ^t-([0-9]{3,9})([a-z]{0,2})\Z` (ASCII classes, `\Z`); `parse_id(s) -> (num_text, letter) |
     None`. Task identity stays the STRING (`journal_keys.task_key` = `(label, id)`), never a normalised number, so a
     legacy non-canonical spelling never merges with another id.
   - ISSUE grammar `is_canonical(id)`: number `001`..`999` zero-padded to 3, or 4-9 digits with no leading zero; number ≥ 1.
   - `REF_RE`, `CLOSES_RE`, `ID_NUM_RE` rebuilt on the read grammar; `CLOSES_RE` ends with `(?![A-Za-z0-9])` before the
     optional `@label`. The validator's `TASK_ID_RE` imports it; `session_context` / `calibration_counts` fallback copies
     are updated and stay pinned equal; `dispatch_manifest` `resubmission t-<id>`, `compact_snapshot`, `journal_echo` read
     through it.
   - `piles.py`: `TASK_RE` = the read grammar (fullmatch); `LEFTOVER_DONE_RE` / `PROOF_DONE_RE` use the read grammar for
     their `t-` branch. Refusal text: "expected a task id t-NNN (3-9 digits, optional lower-case letter)".
2. Rule 9a'' (validator; BL-1): a brand-new id (a novelty-issuing event) is legal when (i) the full id, letter included,
   was NEVER SEEN in the logical journal (seed + file), (ii) it is canonical, and (iii) its number is at most
   `ID_JUMP_MAX = 1000` above the max number already seen WITH THE SAME LETTER (no prior id of that letter: at most 1000,
   so the first id of a new letter is `t-001a` from the counter; N-2). Gaps and out-of-order numbers are legal. A seen id
   is judged by 9b-9d (repeats, keyed by the full id; `t-123` and `t-123a` are two tasks).
3. Bands retired for NEW lines, and every leftover of the retired road names the writer (S-5):
   - a new line carrying `id_band` → violation `band_retired` naming `python -B tools/journal_write.py next`; old lines'
     bands still feed `BandState.top` (TEMPORAL, read-only);
   - `journal_keys.py where` prints the max per letter and "ids are issued by `python -B tools/journal_write.py next`";
   - the validator's NOVELTY refusal (`_novelty_text`, journal_validator.py:1283-1304) loses its band advice and names
     the writer: "got <id>; <id> was already used / is not canonical / jumps more than 1000 -- take an id from python -B
     tools/journal_write.py next";
   - `compact_snapshot.next_free_id` and `band_lines_of` (:307-331, and their print site :539-547) print
     "next id: from python -B tools/journal_write.py next (the clone counter)" and no band lines.
4. `returned`: in `EVENTS`; required `task_id`, `worker_ref`, `model`; the task must have an open `delegated` with the SAME
   `worker_ref` earlier in the logical journal; at most one `returned` per (task, worker_ref); not novelty-issuing.
   Optional fields accepted on any event: `via` (`hook` | `cli`), `session` (≤ 16 chars `[A-Za-z0-9-]`), `witness_by`
   (`run` | `file` | `text`, on `accepted`).
5. Open-dispatch reconciliation (`session_context.open_dispatches`, the session-handoff reader): `returned` NEVER closes a
   task; `delegated` + a later matching `returned` shows `RESULT PENDING: t-NNN agent=X returned <ts>` (same 3-line cut);
   without it `OPEN DISPATCH`.
6. `forge_metrics`, `calibration_counts`, `compact_snapshot` learn the event kind (axis 6).
7. `journal_keys.peer_note` (read by session_context, journal_echo; tested in test_transcripts too) no longer tells anyone
   to open a band: "ids come from the clone counter; nothing to do".
8. `dispatch_manifest.designer_skip_reason(cut) -> str | None` from the ONE cut; the header grammar of F-B2-1 (a): lines
   `task: t-NNN`, `node: <slug>/<N>/<id>`, `feature: Fnn`, read by `dispatch_manifest.header_ids(cut) -> dict`, with the
   fallback "the first `Task t-NNN` in the first 200 characters of the prompt".
9. `hygiene_gate.py` (X-1, X-9): `MSG_JOURNAL_BLOCK` names the door ("the journal is written by `python -B
   tools/journal_write.py <event> …` (the hooks write delegated/returned themselves); reading it with grep, cat or tail is
   fine"); `run_allowed(cmd, cwd) -> (ok: bool, reasons: list[str])` over `_decide_command("Bash", cmd, {"cwd": cwd})`.
   Error direction: REFUSE on doubt — ok is True only for the gate's plain allow; a deny, a WARN-class answer (an
   unresolvable payload), an exception, a NUL byte or a command over the gate's own size cap → ok False with the reason.
   The refusal classes of the live gate are unchanged.
10. `journal_echo.echo_for_lines(new_lines, base_lines, *, payload=None) -> str` (X-7): the existing collectors (tier
    MISMATCH, notes length, escalation, R3, ts drift, witness) over given lines, the same text `main()` builds; the
    witness segment is skipped for an `accepted` line with `witness_by: run`. `main()` calls it (one assembly).

Edges:
- E-B0-1 adversarial ids: `t-123A`, `t-123а` (Cyrillic), `t-１２３` (fullwidth), `t-123abc`, `t-12`, `t-1234567890` → not
  ids (form violation on a new line; `closes:` drops them); `t-0123`, `t-000`, `t-0001` → readable as strings, refused as a
  NEW id (not canonical). Invariant: no non-ASCII, upper-case or non-canonical id is ever ISSUED, and no token closes an
  id other than the one it spells.
- E-B0-2 `closes:t-123a` closes exactly `t-123a`; `closes:t-123` never closes `t-123a`; `closes:t-123ab@codex` resolves by
  label. Invariant: K4's false close is unreachable.
- E-B0-3 jump AT 1000 legal, 1001 refused; a gap of 1 legal. Invariant: a typo far above the sequence is refused.
- E-B0-4 an id issued twice in one file (the 13.11 race) is a SEEN id: its second line is judged as a repeat (9b-9d), so a
  second `delegated` of another agent on that open task passes only as a critic entry. Invariant: removing "exactly max+1"
  never lets a reused id pass as NEW. Residual (stated): a hand-typed reserved id of another session could pass as a
  critic entry; the counter makes it unreachable without a typo; detector check 46.
- E-B0-5 TEMPORAL: old journals (bare ids, bands, `<id>@<label>`) validate as today (old lines are never judged); the
  first new line after the switch with a gap is legal. Both worlds on one fixture.
- E-B0-6 `returned` without a matching open `delegated` (wrong worker_ref, closed task, no task) → violation naming the
  door `journal_write.py returned --task … --worker …`. Invariant: a `returned` never opens, reopens or closes a task.
- E-B0-7 merge mode (`--merge-parent`): two worktree copies with interleaved ids (t-900 here, t-901 there) merge with no
  NOVELTY violation; the same id in both copies with different content stays today's collision refusal.
- E-B0-8 (BL-1) out of order: t-901 written, then t-900 (never seen) → legal; `next --n 3` gives t-900..t-902 and t-902,
  t-900, t-901 are written in that order → all legal.
- E-B0-9 (X-4) piles: `--task t-415` and `t-123a` accepted; `t-1`, `T-1`, `t-1|x`, empty, `t-1234567890` refused with the
  new text; `сделано: t-123a` accepted; existing rows with `t-1`/`t-2`/`t-9` are rewritten to `t-001`/`t-002`/`t-009`
  (the cells they assert change accordingly); the "1-6 digits" magnitude row becomes the 10-digit row.
- E-B0-10 `run_allowed` battery (rows of `test_hygiene_gate.py`): every row of E-B1-9 → refused; `python -m pytest
  tools/test_x.py -q` → allowed; an exception injected into `_decide_command` → refused.

Tests: rows in the existing tables of each owned test file (no new file): grammar (E-B0-1/2/9), 9a'' (E-B0-3/4/5/8),
`returned` (E-B0-6), open-dispatch (RESULT PENDING), merge (E-B0-7), band rows changed to the retired answers, peer_note
text, `run_allowed` (E-B0-10), `echo_for_lines` equals `main()`'s text on one sample. Witness:
`python -m pytest tools/test_journal_validator.py tools/test_journal_validator_merge.py tools/test_journal_keys.py tools/test_session_context.py tools/test_journal_echo.py tools/test_calibration_counts.py tools/test_compact_snapshot.py tools/test_dispatch_manifest.py tools/test_forge_metrics.py tools/test_hygiene_gate.py tools/test_transcripts.py tools/test_piles_take.py tools/test_piles_close_gate.py -q`.

### B5 — parallel sessions on one machine (design; implemented in B0 + B1)

| Writers | Share | Today | After |
|---|---|---|---|
| two sessions, same worktree | one file | max+1 race (13.11) → bands by discipline | the machine lock + the clone counter |
| two sessions, two worktrees of one clone | the git common dir; two file copies | ids meet at the merge | the clone counter (one per common dir) |
| two clones, different developer slugs | nothing | file label `<id>@<label>` | unchanged: the file label is the READ key |
| two clones, the SAME developer slug | the file name | collision at the union merge | the clone LETTER |

D1 lock (S-2, S-3): `journal_lock.machine_lock(name, timeout)` — a lock file `<common>/forge-journal/<name>.lock`, where
`<common>` = the output of `git -C <dir> rev-parse --path-format=absolute --git-common-dir` (`<dir>` = `--repo` or cwd); if
the answer is relative (a git without `--path-format`), it is resolved against `<dir>` — never against the repo root.
The file is opened `O_RDWR|O_CREAT` and never truncated. Windows: seek to offset 4096 and `msvcrt.locking(fd, LK_NBLCK, 1)`
polled every 50 ms up to `timeout`; elsewhere `fcntl.flock(LOCK_EX|LOCK_NB)` — chosen by which module imports (a
capability). After acquiring, the holder writes `pid ts` space-padded to 64 bytes at offset 0 (outside the locked byte, so
another process can read it on Windows). The OS releases the lock when the process dies. Names: `journal` (appends, id
issue, every read of a journal copy that feeds a write), `main-merge` (C3).
D2 counter: `<common>/forge-journal/counter.json` `{"<letter or empty>": <last issued number>}`; read and written only under
the `journal` lock; write-temp-then-`os.replace`. Next number = 1 + max(counter[letter], the max number with that letter in
THIS worktree's logical journal, and on first use the max over every worktree copy listed by `git worktree list
--porcelain`). It never goes down.
D3 letter: the registry `logs/journal-letters.json` (tracked) `{"letters": [{"letter": "", "slug": "dev1", "clone":
"<uuid>", "since": "<ts>"}, …]}`, one row per line, sorted by letter; the clone id is `<common>/forge-journal/clone-id`
(uuid4, created once). A clone's letter = the row whose `clone` is its id. `journal_write.py clone --claim` adds the row:
letter `""` when the slug has no row yet, else the lowest free `a..z`, then `aa..zz`; it prints the `git add`/commit line.
Two clones claiming one letter offline conflict TEXTUALLY on the JSON at merge (the after-the-fact detector).
D4 rule 9a'' (B0 item 2) replaces "exactly max+1". The validator cannot see the counter (local; CI lacks it), so "issued by
this clone's counter" is the WRITER's check (E-B1-13), and "never seen + jump cap" is the validator's.
D5 one road per action (P31): issuing an id — ONE road, `journal_write` under the lock from the counter, with the clone
letter; retired for new lines: bands (rule 9e) and `where`'s max+1 advice; kept read-only: BandState over old bands.
Reading a task — ONE key, `(label, id)`; `journal_keys.py declare` stays as the repair of collisions already in history; a
declaration covering a line dated after the switch is a WARN at `check`.
D6 TEMPORAL:
- before B0+B1 merge: no counter, registry or clone-id; ids by hand as today (Edit/Write, bands legal).
- B0 and B1 merge back to back (§2 Landing); nobody issues an id between the two merges (the Lead's session does both).
- first `journal_write` call in a clone: creates `<common>/forge-journal/` (clone-id; counter from the max over worktree
  copies). No registry row → it REFUSES to issue (exit 2) with the door `journal_write.py clone --claim`; hooks print the
  same as a WARN and write nothing.
- after: every new id comes from the counter.

### B1 — the one writer `tools/journal_write.py` (library + CLI) and `tools/journal_lock.py`

CLI (each call writes at most ONE line to `journal_keys.current_path(root)` of the repo containing `--repo` or cwd):

| subcommand | writes | required args | notes |
|---|---|---|---|
| `next [--n K]` | nothing; reserves K ids (1..20) | — | prints the ids, one per line |
| `delegated` | `delegated` | `--agent --model --worker --notes`, `--task` (else a new id is issued) | `--node`, `--feature`, `--attempt`, `--replaces <worker_ref>` (written as the `replaces_worker:` token), `--category` (default from `AGENT_ROWS`) |
| `returned` | `returned` | `--task --worker` | `--model` default = the matching `delegated`'s |
| `accept` | `accepted` | `--task --agent --model --by --notes`; for agent=builder exactly one of `--run "<cmd>"`, `--witness-file <path>`, `--witness "<text>"` | `--basis`, `--allow-red "<reason>"`; sets `witness_by` |
| `reject` | `rejected` | `--task --agent --model --by --attempt --failure-class --notes` | |
| `skip` | `dispatch_skipped` | `--agent --notes` | `--task` named in notes as `t-NNN` |
| `escalate`, `defect`, `decomposable`, `degraded`, `restored`, `calibrated` | their events | per CLAUDE.md shapes | |
| `event --json '<obj>'` | any event | a JSON object without `ts` | the door for a rare or retro line ("retroactive" in notes) |
| `clone --claim` / `clone --show` | the registry row / nothing | — | D3 |

Order of one write (BL-2, POSITIONAL): (1) parse and check the arguments; (2) produce the witness OUTSIDE the lock —
run `--run` (E-B1-8) or read `--witness-file` (E-B1-10); (3) take the `journal` lock (CLI 15 s, hooks 5 s); (4) read the
logical journal (seed + file) and the counter; (5) issue the id if none was given; stamp `ts` from the system clock
(`datetime.now()`, ISO local, no zone, seconds); build the object; (6) run `journal_validator.validate_new_lines([line],
head_lines=file_lines, now, seed_lines=...)` plus `feature_warnings` / `node_warnings`; any violation → nothing written,
exit 2, stderr = the validator's own texts + the door; (7) append through `hooklib.append_jsonl_line` (F-B1-3 (a): the
torn-tail rule) and update the counter; (8) release; (9) outside the lock: `journal_echo.echo_for_lines` (F-B1-2 (a))
and print `journal: <event> <task_id> written (<path>:<line no>)` plus every WARN. Invariant: the lock is never held across
a subprocess, a file read other than the journal/counter, or the echo — holding it is bounded to milliseconds.
Library: `write_event(root, obj, *, via, lock_timeout) -> Result(written: bool, line_no, messages)` used by the hooks;
never raises out (an exception → `written=False` with the reason).

Data row `AGENT_ROWS`: `scout: recon`, `builder: implementation`, `critic: review`, `designer: spec`; an agent not in the
row → category `other` and a WARN (the validator decides legality).

Edges (CLI args are outside input → adversarial table rows):
- E-B1-1 notes: > 300 chars → refused for the CLI ("notes are at most 300 characters (CLAUDE.md rule 12)"), AT 300 legal;
  empty / whitespace → refused. Control characters `\x00-\x1f` → a space; JSON with `ensure_ascii=False`. Invariant: one
  event is exactly one physical line.
- E-B1-2 (S-11) `--task`: the read grammar of B0; an id given for a NEW task (no line of it in the logical journal) must be
  canonical and carry THIS clone's letter ("this clone's letter is X"); an id of another clone's letter on an EXISTING task
  (`accept`, `reject`, `returned`, a repeat `delegated`) is legal. Invariant: a clone only ever issues ids of its own
  letter.
- E-B1-3 lock timeout → exit 3, "journal busy: held by pid N since ts" (the text read from bytes 0-63 while the other
  process holds the byte at 4096); nothing written.
- E-B1-4 not a git repo / `git` missing / common dir unreadable → exit 2 naming the cause; nothing written. Invariant: a
  line is never written without the lock.
- E-B1-5 counter.json corrupt / non-JSON / negative → rebuilt from the worktree copies (safe direction: higher), one
  stderr note; a counter BELOW the file max → the file max wins.
- E-B1-6 crash between append and counter update → next call takes max(counter, file) → no reuse (test: write a line
  without touching the counter).
- E-B1-7 `ts` equal to the previous line's → legal; a clock BEHIND the last line → the validator's monotonicity refusal;
  door: `event --json` with an `order-known:<ts>` token (rule 19).
- E-B1-8 (BL-3) `accept --run`: the command runs as `[bash, "-c", cmd]`, `cwd=<repo root>`, `timeout=600`, stdout+stderr
  merged, decoded UTF-8 `errors="replace"`, control chars stripped. `bash` = `shutil.which("bash")`, then a capability probe
  `[bash, "-c", "test -f tools/journal_write.py"]` in the repo root: not found / probe fails (e.g. a WSL launcher that does
  not see this path) → `--run` refused, exit 2: "no bash that sees this repo; run the witness yourself and pass
  --witness-file <path>". Witness = `"$ <cmd>\n" + last 40 lines (cap 6,000 chars, cut from the START with "[… N lines
  cut]") + "\nexit=<rc>"`. rc ≠ 0 → nothing written unless `--allow-red "<reason>"` (then `allow-red: <reason>` in notes).
  Timeout → nothing written, exit 3. Invariant: the shell that runs the text is the shell whose grammar judged it.
- E-B1-9 `--run` is judged first by `hygiene_gate.run_allowed(cmd, cwd=<repo root>)` (B0 item 9); not ok → exit 2 with the
  gate's text. Reused function in a more consequential role (the only check before an unhooked subprocess): error direction
  = REFUSE on doubt. Adversarial rows that must stay REFUSED: `echo x >> logs/journal/dev1.jsonl`, the backslash form,
  `python -c "open('logs/journal/dev1.jsonl','a').write('x')"`, `git checkout -- .` on a dirty tree, `cd tools && pytest`,
  `$(echo cd) x`, a 70 KB command, a command with a NUL byte. Rows that are ALLOWED and must stay HARMLESS (they run under
  bash, where the quotes hold): `echo ' >> logs\journal\probe.jsonl '` and `python -m pytest -q ' & echo x >>
  logs\journal\probe.jsonl '` → the test asserts that `logs/journal/probe.jsonl` does NOT exist afterwards (the critic's
  cmd.exe probe, inverted).
- E-B1-10 `--witness-file`: missing / a directory / non-UTF-8 / > 1 MB → refused, nothing written; cut as in E-B1-8.
- E-B1-11 two processes call `delegated` with no `--task` at the same moment → two different ids, two valid lines.
- E-B1-12 two worktrees of one temp clone issue ids → distinct numbers; their copies union-merge and validate (E-B0-7).
- E-B1-13 (BL-1) an explicitly given NEW id must be ≤ counter[letter] (issued by this clone's counter): `--task t-905`
  when the counter stands at 902 → refused ("t-905 was not issued; take one from `next`"). Rows: reserved t-900..t-902,
  written t-902, t-900, t-901 → all written.
- E-B1-14 (BL-2) a 30 s `--run` in process A while process B writes `delegated` → B writes within its timeout; A writes
  after its run. Invariant: no write waits on another call's subprocess.
- E-B1-15 (S-3) `--repo <root>/tools` and `--repo <root>` → the same lock file path; a call from a linked worktree → the
  same path.
- E-B1-16 (S-12) stdout/stderr never echo witness text or notes; the outcome lines are `journal: … written (…)`, the
  validator's refusal texts, the echo's WARN lines, and for `--run` one line `run: exit=<rc>`. Invariant: nothing the
  writer prints can be mistaken by dod_track's text heuristic for a pytest summary of THIS command.

Tests (F-T1): `tools/test_journal_write.py` — one table per subcommand family over a temp git repo with a seeded journal;
the concurrency rows (E-B1-11/12/14) with real processes; the `--run` rows (E-B1-8/9) through the real gate and real bash
(skipped with a reason when the probe finds no bash — a capability, stated in the skip text); lock rows (E-B1-3/15).
Witness: `python -m pytest tools/test_journal_write.py -q`.

### B23 — the dispatch-record hooks, the journal Edit/Write gate, dod_track

Step 0 (one measurement before code, hygiene 6a): from a scratch session with a logging hook on PostToolUse(Agent) and
SubagentStop that dumps payloads to the scratchpad, launch one background scout, one foreground scout and one
worktree-isolated background scout; record (a) whether the launch's agent id equals the stop's `agent_id`; (b) the order of
the two events for a foreground launch; (c) the `tool_response` shape (dict fields; text); (d) the `cwd` of the
SubagentStop payload for the worktree-isolated worker (BL-5); (e) whether a background launch draws a second
PostToolUse(Agent) at completion, and its shape (X-2); (f) whether `resolvedModel` is present (F-B23-2). The result goes
into the report verbatim; the design below assumes (a) yes, (b) stop-before-post, (d) the parent's cwd, (e) possible; a
difference is returned as a question before code.

Behaviour:
1. `journal_hooks.py post-agent` (PostToolUse, matcher `Task|Agent`, a NEW entry beside `negative_lint.py`): read the
   payload; agent id = `transcripts.launch_agent_id(tool_response)` (X-2, K14: the ONE reader — a dict's `agentId` field
   first, else the first `agentId: ([A-Za-z0-9_-]+)` in the text of a string or of content blocks; `hop_metrics._LAUNCH_RE`
   becomes an import of the same pattern from `transcripts`); agent = `tool_input.subagent_type`; model =
   `dispatch_gate.label_model_family(tool_input.description)` (S-1: a public wrapper over `_LABEL_LEADING_TOKEN_RE` +
   `_model_family`; the leading token's family word, e.g. `sonnet`); task / node / feature =
   `dispatch_manifest.header_ids(cut)` (F-B2-1 (a)); notes = the description cut to 300 chars (`…` as the 300th when cut)
   + `replaces_worker:<ref>` when the prompt carries that token. Repeat legality (critic entry / retry with `attempt` =
   rejected count + 1 / replacement) computed from the journal and judged by the validator. Idempotent: a `delegated`
   with this `worker_ref` already in the journal → nothing written (E-B23-12). Write through
   `journal_write.write_event(..., via="hook", lock_timeout=5)`; on success also write the index entry
   `<common>/forge-journal/open/<agent_id>` = the absolute journal path written to.
   If the cut has `designer: skip -- <reason>` (`designer_skip_reason`) → also write `dispatch_skipped` (agent=designer,
   notes `designer skip for t-NNN: <reason>`, once per task id).
   Then: a pending-return marker for this agent id (item 3) → write `returned` right after and delete the marker.
2. `dod_gate.py`: on every exit-0 decision path that has a payload (pass, doc-only exemption, safety-valve skip; NOT the
   early returns before a payload is parsed, :560-581) call `journal_hooks.record_returned(payload)` inside try/except; its
   failure never changes dod_gate's exit code or message (F-B3-1 (a)). `record_returned` (BL-5, X-8): find the `delegated`
   whose `worker_ref` is `agent:<agent_id>` — (1) through the index entry (its journal path); (2) else scan the last 3,000
   lines of every journal copy listed by `git worktree list --porcelain` of the payload's repo; found and open → write
   `returned` into THAT copy (via hook, model copied) and delete the index entry; already returned → nothing (idempotent);
   (3) not found → create `<common>/forge-journal/pending-returns/<agent_id>` (O_EXCL) for item 1.
3. Pending markers older than 24 h are pruned by the next hook call, and each prune prints one WARN line
   `JOURNAL: returned lost for agent:<id> (stop at <ts>, no delegated found in 24 h)` — read by check 48 (c). Index entries
   older than 7 days are pruned the same way with `JOURNAL: open-dispatch index entry for agent:<id> pruned`.
4. (moved to B0 item 9: the hygiene door text and `run_allowed`.)
5. `mechanism_gate.MECHANISM_PREFIXES` (S-13): the list is TAKEN FROM the closure test after the change, not from memory:
   `tools/journal_hooks.py` (a live hook), `tools/journal_write.py`, `tools/journal_lock.py` (reached from dod_gate /
   journal_hooks), plus by choice of this spec `tools/test_volume.py` (live once L places commit-msg), `tools/wave.py` (the
   merge road), `logs/journal-letters.json` (data that decides id issue). `hop_metrics.py` is NOT reached once the reader
   lives in `transcripts.py`; if the closure test still reaches it, it is added with its whole closure. The builder reports
   the closure test's output before and after. `hook_liveness_probe.py`: one case per new hook entry (post-agent writes on
   a sample payload in a temp repo; record_returned writes after a passing stop; pre-edit warns).
6. `.claude/settings.json.proposed`: the current file plus two entries — PostToolUse `{"matcher": "Task|Agent", "hooks":
   [{"type": "command", "command": "python tools/journal_hooks.py post-agent"}]}` and PreToolUse `{"matcher": "Edit|Write",
   "hooks": [{"type": "command", "command": "python tools/journal_hooks.py pre-edit"}]}`; the Lead places it.
7. (S-7, F-B4-1 (a)) `journal_hooks.py pre-edit`: an Edit/Write whose `file_path` resolves to `logs/journal/*.jsonl` or
   `logs/routing-log.jsonl` of any worktree → data constant `JOURNAL_EDIT_MODE`: `"warn"` (shipped) prints one
   additionalContext line `JOURNAL: by-hand edit -- the writer is python -B tools/journal_write.py <event> … (event --json
   for a retro line); this becomes a refusal at node B23-S`, exit 0; `"refuse"` (node B23-S) returns
   `permissionDecision: "deny"` with the same door. During the WARN phase a by-hand Edit appends without the lock; the Edit
   tool's own stale-read check refuses an Edit after a hook append (an estimate, not measured) — friction, not loss.
8. (S-12) `dod_track.py`: `is_verification_command` returns False for a command whose first `python` program argument is
   `tools/journal_write.py` (any subcommand). Invariant: a writer call never counts as a verification run (neither green
   nor red) — the inner `--run` is recorded in the journal's witness, not in the track. Row in `tools/test_dod_track.py`:
   `python -B tools/journal_write.py accept --witness "12 passed" …` with rc 0 → no run recorded.
Output channel: `hookSpecificOutput.additionalContext`, one line, exit 0 always (pre-edit in `"refuse"` mode: the deny
shape) — a journal hook never blocks a tool by error.

Edges (hook payloads are outside input):
- E-B23-1 payload: empty stdin, non-JSON, a JSON list, `tool_response` absent / a string / a list of content blocks / a
  dict / nested dicts, 2 MB response, non-UTF-8 bytes → no write, one line `JOURNAL: delegated NOT written -- <reason>;
  write it: python -B tools/journal_write.py delegated …`. Invariant: a launched dispatch is never left unrecorded
  SILENTLY.
- E-B23-2 no agent id (launch failed, host form change) → as E-B23-1; two ids → the field wins over the text, else the
  first.
- E-B23-3 (S-1) no tier family in the description's leading token ("fix flaky test") → no write + the CLI door.
  Invariant: the hook never writes a model it did not read as a tier word.
- E-B23-4 task id absent from the dispatch → a new id from the counter; the line says `task id issued by the hook: t-NNN
  (the dispatch named none)`; check 46 compares.
- E-B23-5 the validator refuses → nothing written, its text shown with the door.
- E-B23-6 lock busy 5 s (another writer, or C3's root-refresh dance) → no write, the door shown. Invariant: a hook never
  waits longer than 5 s.
- E-B23-7 POSITIONAL (hook order): PostToolUse hooks of one matcher run in parallel; the journal hook reads no other
  hook's output and `negative_lint.py` reads nothing it writes. SubagentStop: `returned` only from dod_gate's exit-0
  decision. Invariant: a blocked stop (exit 2) never writes `returned`; the later real stop writes it once.
- E-B23-8 foreground order: stop first → marker; PostToolUse writes `delegated` then `returned`. Invariant: `returned`
  never precedes its `delegated` in the file.
- E-B23-9 a dispatch refused by a PreToolUse gate → no PostToolUse → nothing. Invariant: a refused dispatch never appears.
- E-B23-10 (BL-5) the delegating session lives in a linked worktree, background launch → `returned` is written into THAT
  worktree's copy (through the index; and with the index deleted, through the scan). Invariant: a `returned` is written
  into the same copy as its `delegated`, or a loud WARN says it was lost.
- E-B23-11 two parallel sessions: each call takes the machine lock; `session` field = payload `session_id[:8]`.
- E-B23-12 (X-2) a second PostToolUse(Agent) for the same agent id (a completion event) → no second `delegated`
  (idempotent by worker_ref); it never writes `returned` (F-B3-1 (a)).
- E-B23-13 pre-edit: a journal path through `..`, a backslash form, another worktree's journal, upper-case drive letter →
  recognised; a non-journal `.jsonl` (e.g. `logs/other.jsonl`) → silent. Invariant: the mode constant alone decides
  warn vs refuse.

Tests (F-T1 for `journal_hooks`; rows in the owned test files for the rest): payload table E-B23-1..6/12 over sample
payloads (step 0's, scrubbed, as fixtures); order rows E-B23-7/8; the linked-worktree row E-B23-10; pre-edit rows
E-B23-13 in both modes; dod_gate rows (exit 2 writes nothing, exit 0 writes once, recorder exception keeps exit 0);
dod_track row (item 8); `launch_agent_id` rows in `test_transcripts.py` (dict, text, content blocks, none);
`label_model_family` rows in `test_dispatch_gate.py` ("sonnet: x" → sonnet, "fix flaky test" → None, "opus-x: y" → opus);
`test_hop_metrics.py` unchanged results; the closure / settings tests of `test_mechanism_gate.py` green. Witness:
`python -m pytest tools/test_journal_hooks.py tools/test_dod_gate.py tools/test_dod_track.py tools/test_dispatch_gate.py tools/test_transcripts.py tools/test_hop_metrics.py tools/test_mechanism_gate.py tools/test_hook_liveness_probe.py -q`.

### C1 — the dispatch header generator `tools/dispatch_new.py` (wave 2)

Behaviour: `python -B tools/dispatch_new.py --kind builder|critic|designer|scout --task t-NNN [--feature Fnn] [--node
<slug>/<N>/<id>] --given <p>… --owns <abs>… --non-goals "<t>" --handoff <abs .md> --edges "<t>" --dod "<cmd>" --siblings
"<t>" [--designer <abs>|"skip -- <why>"|"resubmission t-NNN"]` prints the header lines in the form `dispatch_manifest`
reads (incl. `task:`/`node:`/`feature:` of B0 item 8), then runs `dispatch_manifest.check({"tool_input": {"subagent_type":
kind, "prompt": text}})` and exits 2 with the checker's message when it would refuse. stdout only; no file.

Edges: E-C1-1 a relative `--owns` → refused (the checker's text). E-C1-2 a one-word `--dod` → refused. E-C1-3 an argument
holding a newline or a backtick → refused. E-C1-4 `--designer` absent with ≥3 owns → refused by the checker. E-C1-5 a
`--given` path that does not exist → printed + one stderr note. E-C1-6 `--task` per B0's read grammar. Invariant: the
generator has no grammar of its own — whatever it prints, the checker accepts; whatever the checker refuses, it refuses.

Tests (F-T1): table (args → exit, printed headers) incl. the round trip "printed text passes `check`" and "the hook's
`header_ids` reads back task/node/feature". Witness: `python -m pytest tools/test_dispatch_new.py -q`.

### C2 — `ci_read.py why`

Behaviour: `why [<run_id>|latest] [--workflow canon.yml] [--branch <b>] [--tail N]`: `latest` = the newest run of the
workflow (on `--branch` when given); print `run <id> <conclusion> <title> <sha8>`; for each job with conclusion
`failure`/`timed_out` (at most 3): `job <id> <name>`, its failing steps (`steps[]`: number, name, conclusion), and the last N
lines (default 60, 1..500) of that step's section of the job log, cut at the `##[group]Run` / step-name boundary; ends with
`(N of M lines)`. Remote text goes through `sanitize()`.

Edges: E-C2-1 green → `run <id> success: nothing failed`. E-C2-2 in progress / queued → that status, exit 0. E-C2-3 failure
with no failed job → the conclusion and `no failed job`. E-C2-4 step boundary not found → the job log tail and `step section
not found: job log tail`. Invariant: never an empty answer for a red run. E-C2-5 `--tail` 500 legal, 501 / 0 / negative →
refused before any request. E-C2-6 non-numeric run id → argparse refusal. E-C2-7 > 3 failed jobs → first 3 by job id and
`+K more failed jobs`. E-C2-8 log 404/410 → `log expired` for that job.

Tests: rows in `tools/test_ci_read.py` over canned API answers. Witness: `python -m pytest tools/test_ci_read.py -q`.
Commit: `axes: not a mechanism (a read-only CLI subcommand)` (K11: ci_read.py is a prefixed path).

### C3 — `tools/wave.py merge` (F-C3-1 (b), F-C3-2 (a))

Behaviour: `python -B tools/wave.py merge <branch> --task t-NNN [--node <slug> <N> <id>]`:
1. take `machine_lock("main-merge", 60 s)`;
2. `git fetch origin`;
3. refuse when `<branch>` is unknown on origin;
4. print the last known `forge-check` state of the branch head through `ci_read` as information (`forge-check: success |
   failure | pending | unknown`); it never waits and never refuses on it (owner's word, §11; X-6);
5. a temporary worktree `W` at `origin/main` (detached) under `.claude/worktrees/wave-<ts>`; in W: `git merge --ff-only
   origin/<branch>`, else `git merge --no-ff -m "wave: merge <branch> (t-NNN)" origin/<branch>`; a conflict → `git merge
   --abort`, remove W, refuse naming the conflicted paths;
6. with `--node`: `python tools/piles.py status <slug> <N> <id> --set принято --hash <merge sha> --task t-NNN` in W, commit;
7. `git push origin HEAD:main`; non-fast-forward → remove W, back to 5 (at most 3 attempts; then refuse "main moved 3 times
   during the merge");
8. commit the journal (S-14): under `machine_lock("journal")` read the root's journal bytes and release; in a second short
   W' at the new origin/main, when origin's journal is a byte-prefix of those bytes, write them, commit `journal: wave
   <branch> (t-NNN)` (the pre-commit validator runs), push with the same retry; otherwise print `journal not committed:
   origin holds lines the root lacks -- commit it from <root>`;
9. refresh the root checkout (BL-4 (a)) only when: the root is on branch `main`; its tracked changes ⊆ {its own journal
   file}; its HEAD is an ancestor of origin/main; origin's journal is a byte-prefix of the root's journal file. Under
   `machine_lock("journal")`: copy the root journal's bytes to `<common>/forge-journal/wave-copy-<ts>` and take their
   sha256 H; set the file to its HEAD state (HEAD's bytes from `git show HEAD:<path>`, or absent when HEAD has no such
   path) by a Python byte write; `git -C <root> merge --ff-only origin/main`; WHATEVER the result, write the copy's bytes
   back; verify sha256(file) == H; release. Mismatch → `JOURNAL RESTORE MISMATCH: copy kept at <path>`, exit 1, the copy
   never deleted; match → the copy is deleted. Otherwise print `root checkout not refreshed: <why>` and touch nothing;
10. delete the branch (BL-4 (b), X-5): if the branch is checked out in a worktree, remove that worktree when clean
    (`worktree_sweep`'s rules), else keep the branch and print the worktree; then: root refreshed → `git -C <root> branch -d
    <branch>`; not refreshed → `git merge-base --is-ancestor refs/heads/<branch> origin/main` true → `git update-ref -d
    refs/heads/<branch> <its sha>` (the old-value guard), false → keep and print; `git push origin --delete <branch>`;
11. remove W/W', release the lock, print a 4-line summary (merge sha, node, branch deleted, root refreshed / not).

Edges: E-C3-1 dirty root (a tracked change beyond its journal) → the merge still happens (it never uses the root), step 9
skipped with the reason. Invariant: wave never stashes, resets, checks out or discards anything in the root; the root
journal after step 9 is byte-identical to before it. E-C3-2 the lock held by another wave → wait 60 s, then refuse with
the holder. E-C3-3 `--task` per B0. E-C3-4 a push hook / pre-commit refuses → stop, remove W, print the hook's text.
E-C3-5 the branch already merged → `nothing to merge`, still steps 6, 8-10. E-C3-6 network failure → refuse with the step
name; W removed. E-C3-7 piles status refuses after the push → print the refusal and the exact command, exit 1 (never undo
a pushed merge). E-C3-8 POSITIONAL: steps 1-5 write nothing outside W. Invariant: a run refusing at 3 or 5 changed nothing
anywhere. E-C3-9 the root not on `main` (detached or another branch) → not refreshed, reason printed. E-C3-10 the merge in
step 9 fails (e.g. an untracked file in the way) → the copy restored and verified, `root checkout not refreshed: <git's
text>`. E-C3-11 a hook appends during step 9 → it waits on the lock (≤ 5 s, else its own door, E-B23-6); no line lost.
E-C3-12 the branch checked out in a dirty worktree → branch and worktree kept, printed. E-C3-13 `update-ref` old-value
mismatch (the branch moved) → kept, printed. E-C3-14 the journal path absent in the root's HEAD (a new developer file) →
step 9 deletes it before the merge and restores it after.

Tests (F-T1): over a temp bare "origin" + clone, no network: ff merge, no-ff merge, conflict, non-ff push retry (a second
clone pushes between), dirty root, journal prefix / not prefix, already merged, TWO WAVES IN A ROW (root refreshed both
times, journal intact), a concurrent appender thread taking the journal lock during step 9 (no line lost, hash verified),
the root on another branch, a branch checked out in a clean / dirty worktree. Witness: `python -m pytest tools/test_wave.py -q`.

## 4. DoD skeletons per dispatch (the Lead writes the dispatch; each carries these lines)

Every builder dispatch of this spec carries: `given:` this file + the files of its stream row + `plans/builder-rules.md`
(7b, 7d) + `docs/TESTING.md`; `owns:` the stream row's absolute paths, inline; `non-goals:` every other stream's paths,
the package, CI runs, slow files, placing `.claude/settings.json` or `.githooks/commit-msg`; `handoff:`
`docs/tasks/handoffs/<task>-<stream>.md`; `edges:` the E-rows of its section; `DoD:` the witness command of its section in
backticks + "the report names every E-row with the table row that covers it"; `siblings:` the §7 axis lines marked for
the stream; `designer:` this file's absolute path. Landing line per §2: A1/B0/B23/B23-S — "do NOT commit; hand over the
staged worktree, the patch file and the witness on the staged tree (a Fable session commits)"; A3/C2 — the skip line named
in §2; B1/C1/C3 — commit with the §7 axis lines of their mechanism. The witness command is the test file that judges the
owned path (CLAUDE.md rule 4: forge paths have no `scenario_walk.py --witness-for` row). Builders never run CI.

## 5. Order, dependencies, cost

Order: wave 1 = A1, A2, A3, B0, C2. Wave 2 = B1, C1 (both branch from B0's committed tip). Merge B0 → B1 back to back
(C1 after B0). Wave 3 = B23, C3. Stream L after wave 3 merges (placement of commit-msg after B23 has put
`tools/test_volume.py` into the net — the githooks coverage test of `test_mechanism_gate.py` demands it). B23-S later, on
its trigger.

Cost (estimates, not measured): 9 builder dispatches (A1 ~40 lines, A2 ~60, A3 ~150 + table, B0 ~500-700 over 10 files + 13
test files, B1 ~700+, B23 ~450, C1 ~150, C2 ~120, C3 ~450), 1 critic on this plan (done) + its fix round (this file), 3 topic
critics (A, B mandatory, C). Fable time (BL-6): one Fable session per landing of A1, B0 (commit only), B0+B1 merge, B23,
B23-S, and stream L (~1 h) — about five Fable sessions, not one; they can be batched into two (after wave 1+2, after wave
3) if the Lead holds the merges. Saving (the owner's goal): per dispatch the coordinator stops writing `delegated`,
`returned`, `dispatch_skipped` by hand (3 Edit turns → 0); `accepted` becomes one CLI call that also runs the witness (2-3
turns → 1); per merge wave `wave.py merge` replaces ~8-12 git/piles turns; `ci_read why` replaces the jobs→log→grep chain
(~3 turns → 1). Measured by check 48 (§6.4).

## 6. Exact proposed rule texts

### 6.1 Role files and builder-rules (stream A1; F-A1-1 (b); N-5)

`.claude/agents/builder.md`, appended:

```
8. Tests are written by `docs/TESTING.md` — read it before your first
   test; its section «Как писать эффективный тест на нашем проекте» is
   the how-to. The test volume rule is TESTING.md «Бюджет / Объём»;
   when your diff goes over it, name the reason in one line of your
   report AND in a line `tests-over: <reason>` of the commit message
   (the commit-msg hook WARNs without it, it never refuses). A new case
   is a row of an existing scenario, table or junction, not a new file
   (the one exception: «Бюджет / Файлы»).
```

`.claude/agents/critic.md`, appended:

```
20. Tests, on every diff gate, with their own verdict line: the
   question is docs/tasks/critic-diff-brief.md question 5 (the rule
   text is docs/TESTING.md «Бюджет»). A diff over the volume rule with
   no reason named — in the report and in the commit's `tests-over:`
   line — is a finding; a named reason that does not hold is a finding
   too.
```

`plans/builder-rules.md` 7d, the volume sentence becomes: «объём тестов — `docs/TESTING.md` «Бюджет / Объём»; больше —
причина строкой отчёта и строкой `tests-over:` в сообщении коммита».

### 6.2 docs/TESTING.md (stream A2)

a) «### Бюджет», bullet «**Файлы**», appended sentence (F-T1-2 (a), the recommendation):

```
  Исключение (слово владельца 14.11.2026, спека
  `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md`): новый инструмент форджа этой спеки (`tools/<x>.py`)
  получает один свой тестовый файл `tools/test_<x>.py` — одна параметризованная таблица и строки стыков, до 10 с;
  строки `keep` у тестов форджа нет (`test-layers.json` — носитель пакета).
```

b) line 55: «нового тестового файла на новый скрипт» gains «(исключение — «Бюджет / Файлы»)».

c) the new section after «### Бюджет»:

```
### Как писать эффективный тест на нашем проекте

Раздел ничего не добавляет к правилам выше — он собирает их в порядок работы билдера.

1. **Сначала найти, где поведение уже проверяется.** Пакет: `scenario_walk.py --witness-for <пути owns>` печатает
   истории и строки `keep`, которые покрывают правку. Фордж (`tools/`): тестовый файл инструмента. Новый случай — строка:
   `variants.json` истории, строка таблицы, строка стыка; нового файла нет («Бюджет / Файлы»).
2. **Случай приходит из дефекта.** Одна строка, которая падала до правки (FR-32): найденного живым прогоном, критиком или
   CI. Не «по проверке на каждый ключ DoD».
3. **Один параметризованный тест на поведение.** Id параметра называет случай, по красной строке видно, какой случай и
   какая ветка упали (P16). Ввод −1, 0, 1.5, «абв» с одним исходом — один тест с параметрами.
4. **Утверждать исход, не устройство.** Стадия принята или отказана и чем, какой вопрос задан человеку, что ушло дальше.
   Ни пина текста роли, ни пина исходника, ни измеренной константы (таблица «Что не пишется»).
5. **Данные — из настоящих прогонов.** Срезы `fixtures/stories/<id>/`, `fixtures/run-*`; не выдуманный словарь из трёх
   ключей, который код никогда не увидит.
6. **Мир — один раз на файл**, проверки снимаются с него («Бюджет», «Время»; открытый вопрос об исключении сухой истории —
   находка `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`, ждёт слова
   владельца).
7. **Враждебный ввод — только снаружи.** Тикет, слова человека, конфиг проекта, ответ хоста, аргументы CLI, полезная
   нагрузка хука: размер, вложенность, кодировка, пустое и битое, каждый предел — на нём и за ним; строкой сценария или
   таблицы. Внутренняя граница теста не получает.
8. **Цена.** Объём — «Бюджет / Объём» (больше — причина в отчёте и строка `tests-over:` в коммите); новый файл (часть
   разрезанного — до 60 с в CI) укладывается в 10 с; тест, покрасневший второй раз без дефекта, удаляется («Когда тест
   покраснел»).

Плохо: `test_fix_13797.py` с проверкой «фраза стоит в `agents/qa-automator.md`» и копией файла без ключа, которая должна
упасть. Хорошо: строка `variants.json` истории, где ответ человека «нет» на гейте A даёт тот вопрос и ту стадию, что ждёт
требование, и которая была красной до правки.
```

### 6.3 CLAUDE.md (stream L; Fable only)

a) Routing log, first paragraph, "One JSON line per event, written with an Edit/Write tool:" becomes:

```
One JSON line per event, written by the one writer
`python -B tools/journal_write.py <event> …` (the machine lock, the
clock, the validator BEFORE the write; the owner's word 14.11.2026):
the Task/Agent PostToolUse hook writes `delegated` (and the owed
designer `dispatch_skipped`) and the SubagentStop gate writes
`returned` by themselves; the coordinator writes `accepted`,
`rejected` and the rest with one call (`accept --run "<cmd>"` runs the
verification under bash and stores its verbatim tail as the witness):
```

b) The id paragraph ("Issuing a task_id means re-reading the tail … a band is the before-issuing road.") becomes:

```
A task id is issued by `journal_write.py next` (or by the writer when
no id is given) under the machine lock, from the clone's counter in
the git common directory, shared by every session and worktree of the
clone; ids may skip and land out of order, never repeat (validator
rule 9a: never seen, at most 1000 above its letter's max). An id
carries the clone's LETTER — none for the first clone of a developer,
`a`, `b`, … for the next ones (`logs/journal-letters.json`,
`journal_write.py clone --claim`; the owner's word 14.11.2026 «Номер
123 и 123А», written in lower case ASCII: `t-123`, `t-123a`). Bands
(`id_band`) are retired for new lines and still read in old ones;
`journal_keys.py declare` repairs only collisions already in history.
```

c) Event SHAPES table, a new row after `delegated`:

```
| `returned` | `task_id`, `worker_ref` (the `delegated` it ends), `model`; written by the SubagentStop gate when a worker's stop passes; never closes a task — the open-dispatch scan shows it as RESULT PENDING until `accepted`/`rejected` |
```
and the events sentence "Events: the six of the table — … — plus `decomposable`, …" gains `returned`.

d) Command hygiene point 5 becomes:

```
5. Log entries — through `tools/journal_write.py` only (the owner's
   word 14.11.2026: «это было правило для экономии токенов модели, так
   как сейчас писать будет код то экономия только больше. Я своим
   словом разрешаю»); a redirect, tee, in-place editor or payload that
   writes `logs/journal/*.jsonl` or `logs/routing-log.jsonl` is refused;
   an Edit/Write of them draws a WARN until node B23-S makes it a
   refusal (F-B4-1).
```

e) Rule 8 DETERMINISTIC SCRIPT RUNS gains nothing; rule 2's acceptance sentence is unchanged (the witness is still the
verbatim run; `accept --run` is one way to produce it).

### 6.4 PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (stream L)

New check 48 (journal by code): per window (a) Agent launches in the Lead transcripts (`hop_metrics`) vs `delegated` lines
with `via: hook` / `via: cli` / no `via` (by hand) — target: by hand = 0 after the switch; one full window at 0 is the
trigger of node B23-S; (b) `JOURNAL: … NOT written` lines (`tools/warn_density.py`) and whether each was followed by a CLI
line; (c) `returned` coverage: every finished worker (`transcripts.is_finished`) has a `returned`; every `JOURNAL: returned
lost` WARN listed; (d) `accept --run` witnesses with `allow-red` listed with their reasons; (e) counts printed with their
commands (hygiene 6b). Check 46 amended: after the switch the race count is expected 0 by construction; a duplicate id or a
declaration covering a post-switch line is a finding against the lock/counter. Check 33 amended: commits that drew a TEST
VOLUME WARN, how many carried `tests-over:`, how many of those the critic judged. Check 37 amended: branches merged by
`wave.py` vs by hand; a `root checkout not refreshed` or `JOURNAL RESTORE MISMATCH` line standing over a day.

### 6.5 docs/SIBLING_MAP.md (stream L)

Axis 1 row "Journal readers <-> the task key": add the id grammar owner (`journal_keys.ID_RE` / `parse_id` / `is_canonical`,
the letter), the writer (`tools/journal_write.py`), the counter and lock (`tools/journal_lock.py`), the registry
(`logs/journal-letters.json`), and "`returned` is read by session_context, forge_metrics, calibration_counts,
compact_snapshot; piles reads ids through the same grammar". Axis 29: `journal_write` appends through
`hooklib.append_jsonl_line` (F-B1-3 (a)). Axis 9: `tools/test_volume.py` as a FORGE reader of "is this a test" with its own
question and error direction (unsure → product). Axis 14: the launch id has one reader, `transcripts.launch_agent_id`
(hop_metrics and journal_hooks). Axis 3: a forge live hook imports the package's `hooklib` (a package change to it re-runs
`tools/test_journal_write.py`).

## 7. Four questions per mechanism (CLAUDE.md rule 10)

Mechanisms: M1 the volume rule in the roles + TESTING how-to + the F-T1 carrier (A1, A2); M2 the volume WARN (A3, L
placement); M3 the one writer, id issue, lock, counter, letter (B0, B1, B5); M4 the dispatch-record hooks, `returned`,
dod_track exclusion (B23, B0 items 4-5); M5 hygiene pt.5 one road: the Bash refusal door (B0 item 9) and the Edit/Write
gate with its switch (B23 item 7, B23-S, L); M6 `wave.py merge` (C3); M7 `dispatch_new.py` (C1). `ci_read why` (C2) is a
reader extension: `axes: not a mechanism (a read-only CLI subcommand)`.

(a) cost and who pays:
- M1: two role paragraphs (~120 tokens per builder/critic load) + one TESTING sentence; one report line when over.
- M2: one git call per commit (~50 ms); a WARN line; a `tests-over:` line when over.
- M3: one CLI call per non-hook event; the first use per clone pays `clone --claim` + a one-row commit; the CLI waits on
  the lock only for milliseconds (BL-2).
- M4: ~100-200 ms per dispatch launch and per worker stop; a WARN line when a write fails or a `returned` is lost.
- M5: none beyond M3; an Edit of the journal draws a WARN, after B23-S a refusal with the door.
- M6: one CLI call per merge; a temp worktree per merge; up to 60 s on another session's merge; hooks may wait up to 5 s
  during the root-refresh dance.
- M7: one CLI call per dispatch instead of hand-typed headers.
- Fable time: the landings of §5 (BL-6).

(b) axis enumeration (every axis of docs/SIBLING_MAP.md; each line closes M1-M7 by name):
- axis 1: covered — M3/M4/M5 change the journal, its readers and CLAUDE.md together (B0 + L, §6.3, §6.5); M1 changes role
  files only (role duty, §6.1); M2, M6, M7 n/a (M6's journal commit goes through git, not a new reader).
- axis 2: covered for M1 — the critic.md edit owes the critic exam (critic.md rule 10); the exam file is absent, the
  deviation is named in the Fable commit (E-A1-3, F-A1-2); builder row "witness-based acceptance" kept by `accept --run`;
  n/a for M2-M7 (no exam instrument changes).
- axis 3: covered for M3 — a live forge hook (dod_gate → journal_hooks → journal_write) imports the package's
  `hooklib.append_jsonl_line`; a hooklib change re-runs `tools/test_journal_write.py` (canon); n/a for M1, M2, M4-M7.
- axis 4: covered for M1 (AGENTS.md regenerated on agent-file change), M4/M5 (settings.json → AGENTS.md); n/a for M2, M3,
  M6, M7.
- axis 5: n/a for all — package stage twins untouched.
- axis 6: covered for M4 — `forge_metrics` learns `returned` (B0 item 6); n/a for M1-M3, M5-M7.
- axis 7: n/a for all — package test identity.
- axis 8: n/a for all — package story paths.
- axis 9: covered for M2 — a forge reader with its own question and direction (§6.5; F-A3-2 (a)); n/a for others.
- axis 10: covered for M3/M6 — the repo top and common dir through `git rev-parse` with `--path-format=absolute` (S-3);
  `GIT_DIR` steering is the axis's caveat (E-B1-4); n/a for M1, M2, M4, M5, M7.
- axis 11: covered for M3 (`--run`) — judged by hygiene_gate's own decider through `run_allowed`, run by the same shell
  grammar (bash; BL-3); n/a for others.
- axis 12: covered for M6 — node status only through `piles.py status`; n/a for others.
- axis 13: covered for M4 (designer skip and task/node/feature from the one cut), M7 (prints, the one checker judges); n/a
  for others.
- axis 14: covered for M4 — the launch id has one reader `transcripts.launch_agent_id` (hop_metrics imports it);
  finished workers in check 48 through `transcripts`; n/a for others.
- axis 15: covered for M2, M3, M6, M7 — new CLIs set UTF-8 console streams through the tools helper; n/a for M1, M4/M5
  hooks (hook JSON channel).
- axis 16: n/a for all — package JSON reader.
- axis 17: n/a for all — package detector verdict shape.
- axis 18: covered — no ratchet raised; n/a otherwise.
- axis 19: n/a for all — no role `tools:` line changes.
- axis 20: n/a for all — host receipt names (package).
- axis 21: n/a for all — package markdown tables.
- axis 22: covered for M4 — the host's launch form (dict field / text) is read at one place and measured in step 0; a form
  change is E-B23-2 (loud); n/a for others.
- axis 23: n/a for all.
- axis 24: n/a for all.
- axis 25: n/a for all.
- axis 26: n/a for all.
- axis 27: n/a for all.
- axis 28: n/a for all.
- axis 29: covered for M3 — one appender (`hooklib.append_jsonl_line`, F-B1-3 (a)) under the lock; n/a for others.
- axis 30: n/a for all.
- axis 31: covered for M1 — one owner per aspect: TESTING.md «Бюджет / Объём», pointers elsewhere incl. builder-rules 7d
  (N-5); n/a for others.
- axis 32: n/a for all — package judgment census; M2 is a WARN on data.
- axis 33: n/a for all — package dispatch identity.
- axis 34: covered — M3/M5: one road to write the journal (the writer; the Edit/Write road is a named transitional WARN
  closed by node B23-S), one road to issue an id (bands retired); M2: the classifier is a data row; M6: one merge road
  (F-C3-2 (a)); n/a for M1, M4, M7.
- axis 35: n/a for all.
- axis 36: n/a for all.
- axis 37: n/a for all.

(c) registered detectors: M1 — check 33 + critic question 5; M2 — check 33 amended; M3 — check 46 amended, check 13, the
validator (pre-commit + write time); M4 — check 48 (new) and check 7; M5 — check 27 + check 48 (a)/(b); M6 — check 37
amended; M7 — check 11 (`warn_density.py`).

(d) what stops the skip: M1 — the role files load on every dispatch; otherwise discipline, detector check 33. M2 —
commit-msg on every commit (WARN by the owner's word). M3 — the validator before every write and at pre-commit; the
Edit/Write gate (WARN, then refusal). M4 — PostToolUse and SubagentStop hooks fire on every launch/stop. M5 — hygiene_gate
(Bash) + the pre-edit gate. M6 — on discipline (a by-hand merge stays possible as the named fallback); detector check 37.
M7 — on discipline; the manifest checker stays the gate.

## 8. Small choices closed by the designer (no design weight; the Lead can reopen)

1. Lock timeouts: CLI 15 s, hooks 5 s, wave `main-merge` 60 s.
2. `next --n` cap 20; `ID_JUMP_MAX` 1000.
3. Witness tail 40 lines / 6,000 chars; `--run` timeout 600 s; `--witness-file` cap 1 MB.
4. `accept --run` red → refused unless `--allow-red "<reason>"`.
5. Optional fields `via`, `session` (`session_id[:8]`), `witness_by` (`run`/`file`/`text`).
6. Category map as a data row (`AGENT_ROWS`).
7. `ci_read why` defaults: tail 60, at most 3 failed jobs.
8. Letters after `z`: `aa..zz`.
9. The hooks live in ONE module `tools/journal_hooks.py` with three entry points (`post-agent`, `pre-edit`, the library
   `record_returned`), not three files.
10. Pending-return markers pruned after 24 h, index entries after 7 days, each with a WARN line.
11. («решила сама», for the owner — N-3) The owner wrote «123А» (Cyrillic, upper case); the ids use ASCII lower case
    (`t-123a`): one grammar for regexes and JSON keys, no look-alike letters. Reversible before B0 lands.
12. Lock byte at offset 4096; holder text 64 bytes at offset 0.
13. The open-dispatch index under `<common>/forge-journal/open/`; the fallback scan reads 3,000 tail lines per copy.
14. The launch-id reader lives in `transcripts.py` (already in the mechanism net; K14), not in hop_metrics.
15. Canonical id form: 3 digits zero-padded, 4-9 digits with no leading zero.
16. C3 commits the journal (step 8) BEFORE refreshing the root (step 9), so after a wave the root's HEAD equals origin/main
    and only the new tail is uncommitted.

## 9. r1 forks — decided (see §11; listed for the trail)

F-A1-1 (b); F-A3-2 (a); F-T1 (a) by the owner's word; F-B1-2 (a); F-B1-3 (a); F-B2-1 (a); F-B3-1 (a); F-B4-1 (a) with the
WARN transition (now owned: B23 item 7, node B23-S); F-B5-2 (a); F-C3-1 reversed by the owner to (b) (C3 step 4); F-C3-2
(a); F-ORD-1 (a) (executable through §2 Landing, S-10). None of them is changed by this round.

## 9'. New forks raised by r2 (RETURNED — the Lead decides; recommendation first; the text is executable by it)

- F-LAND-1 how mechanism-path streams land (BL-6): (a, recommended) the builder hands over a staged, uncommitted worktree +
  a patch; a Fable session commits with the axis lines and its own `tier:` line, then merges — no false tier line, the
  Fable act is the commit itself; costs a Fable session per landing (§5); (b) the builder commits on its branch with the
  full §7 axis block and no `tier:` line, the commit is refused locally, so the builder leaves it as `git commit
  --no-verify`… — rejected by the designer as a road around a gate; (c) the coordinator (Opus) commits with
  `tier: claude-opus-5-5` — the gate refuses it (below the Fable binding), so (c) requires changing the binding, which is the
  owner's.
- F-A1-2 critic.md rule 10 with `PROCESS/CRITIC_EXAM.md` absent (S-6): (a, recommended) A1 lands with the deviation named in
  the Fable commit and a finding opened by the Lead (the critic's queue line) — the rule cannot be met, the gap becomes
  visible and owned; (b) hold the critic.md half of A1 until the exam exists (`critic-exam-gen` skill) — delays the owner's
  word 6 for critic; (c) generate the exam first as a new node — scope growth beyond this spec.
- F-B1-4 how `--run` stays inside the judged grammar (BL-3): (a, recommended) `[bash, "-c", cmd]` with a capability probe —
  the gate already judges Bash syntax, so judge and runner agree; costs a bash dependency (present here through Git Bash;
  CI Linux has it); (b) `shell=False` over `shlex.split(cmd)` with every shell metacharacter (`|&;<>$\``, unbalanced quotes)
  refused — no bash needed, but `pytest a b -k "x or y"` works while `cd x && pytest` or a pipe is refused, and the gate's
  judgment becomes partly redundant.
- F-B23-2 the `model` of a hook-written `delegated`: (a, recommended) the declared family read from the description
  (`label_model_family`, S-1), the self-declaration CLAUDE.md asks for; when the launch response carries `resolvedModel`
  whose family differs, the hook prints `TIER MISMATCH at launch: declared <x>, resolved <y>` beside the line (a measurement,
  not a rewrite); (b) write `resolvedModel` as the model — truer, but the declaration disappears and journal_echo's MISMATCH
  check compares the measurement with itself.
- F-T1-2 the scope of the owner's «Свой файл каждому»: (a, recommended) the exception covers the new tools of THIS spec
  only (the owner's words were said about them; §6.2 a names the spec); (b) a general rule "a new forge tool gets one test
  file" — reads more into the word than was said; a question for the owner if wanted.

## 10. Trail

r1's trail (its §10) stands for the facts carried unchanged. This round read:
- the verdict `docs/tasks/specs/reviews/20261114-coordinator-offload-plan-critic.md` (whole, 1-274) and r1 (whole, 1-796).
- `tools/mechanism_gate.py` 200-290 (`MECHANISM_PREFIXES`), 370-380 (`_matches`, `mechanism_paths`), 574-592
  (`resolve_lead_binding`), 805-968 (`tier_declared_ok`, `_tier_queue_note`, `_decide_core`, `decide_full`).
- `delegation.config.yaml` (Grep `lead:|model:`: roles.lead subscription model `claude-fable-5-1`).
- `tools/test_mechanism_gate.py` 1262-1383 (settings / githooks / transitive-closure tests).
- `tools/dispatch_gate.py` 1025-1064 (`_FAMILY_NAMES`, `_LABEL_LEADING_TOKEN_RE`, `_model_family`).
- `tools/dod_track.py` 1-60, 115-264 (`VERIFICATION_COMMAND_RE`, outcome rules, `is_verification_command`); Grep of
  `determine_outcome|outcome`.
- `tools/dod_gate.py` 30-54, 570-619 (`main`, early returns, agent_id).
- `tools/negative_lint.py` 190-239 (async launch `tool_response` shape).
- `tools/hop_metrics.py` Grep `^import|^from|_LAUNCH_RE` (imports :57-74, regex :89).
- Grep `agentId` over `tools/*.py` (positive control: hop_metrics.py:89 hit).
- `tools/journal_validator.py` 1280-1307 (`_novelty_text`); `tools/compact_snapshot.py` 305-332.
- `tools/journal_echo.py` `^def ` list (collectors are private `_collect_*` + `build_*_segment`).
- `tools/hygiene_gate.py` Grep `_decide_command|decide|MSG_JOURNAL_BLOCK` (:82-85, :1509, :1560-1563).
- `tools/piles.py` Grep of id regexes (:2687, :2832, :3002, :3223, :3256); `tools/test_piles*.py` Grep `--task|t-\d{3}`
  (count per file) and `--task` (rows in `test_piles_take.py:336-392`); Grep `сделано: t-|t-nnn` (count: close_gate 37,
  close 10, findings 2).
- `tools/claim_control_gate.py` 1-40 (a negative-claim WARN gate — a different concern, so the journal gate is not hosted
  there).
- `.claude/agents/critic.md` 56-65 (rule 10), 155-172 (rules 18-19), Grep of rule numbers (last rule 19).
- Glob `PROCESS/*EXAM*` → `DEPLOYMENT_ECONOMY_EXAM.md`, `LEAD_RANKING_EXAM.md` (positive control of the same Glob form: it
  lists existing exam files; `CRITIC_EXAM.md` absent).
- Grep `critic-exam-gen|critic_exam_gen` -i (the skill exists in worktree copies and `docs/SIBLING_MAP.md`; the root
  checkout's `.claude/skills/critic-exam-gen/` was not opened).
- `docs/TESTING.md` 40-148 («Что пишется», «Бюджет», «Кто что делает»).
- Glob of the owned test files (`tools/test_{claim_control_gate,dod_track,transcripts,hop_metrics,worktree_sweep,
  journal_validator_merge,hook_liveness_probe}*.py` and the B0 list) — all exist.
- `logs/journal/dev1.jsonl` Grep of `delegated` worker_ref form (`agent:<id>`, model full ids).
Not opened (needed beyond the manifest: none): `tools/worktree_sweep.py` (C3 reuses "its rules" by name, as in r1),
`tools/transcripts.py` (the new function is additive), `.claude/skills/critic-exam-gen/SKILL.md` in the root checkout.

## 11. Lead decisions on the forks (14.11.2026, coordinator on Opus, degraded window; final acceptance queued to Fable)

Owner present; technical forks decided by the coordinator on the designer's recommendation, reversible, reported to the owner
the same turn ("решила сама"). Owner's own words cover F-B5-2 («123 и 123А») and F-A1-1 («в роль ... дать ссылку на тестинг»).

- F-A1-1: (b). F-A3-2: (a). F-B1-2: (a). F-B1-3: (a). F-B2-1: (a). F-B3-1: (a). F-B4-1: (a), with the WARN transition as
  written. F-B5-2: (a). F-C3-1: (a). F-C3-2: (a). F-ORD-1: (a).
- F-T1: (a) — owner's word 14.11.2026: «Свой файл каждому (рекомендация дизайнера) - ок». One test file per new tool.
- F-C3-1: REVERSED to (b) by the owner's word 14.11.2026: «нет, не хочу ждать CI на каждой ветке. У нас в правилах при
  нескольких готовых к слиянию ветках мы всё мержим и один билдер чинит CI». `wave.py merge` neither waits for nor refuses
  on the branch's CI; it may print the last known state of `forge-check` as information. A red `main` after a wave is one
  builder's fix (PROJECT.md «Командная работа» п. 12).
- Owner's word 14.11.2026 «План работ. Три волны - делаем»: the three-wave order of §5 is approved; builders start after
  the plan critic's verdict is accepted.
- Brief corrections K1-K10 accepted as facts of the carriers (K4 false close of `closes:t-123a` and K5 rule 9a gaps are
  load-bearing; K9 stays the first measurement of stream B23).

### 11'. Lead decisions on the r2 forks (§9'), 14.11.2026 12:2x, coordinator on Opus (degraded window), reversible

Accepted r2 (t-845) by trail: BL-2 positional order read at §3.B1 "Order of one write" (run/witness before the lock — holds);
S-3 absolute common dir read at the §0' row and §3.B5 D1 (holds; matches the coordinator's own measurement `../.git` from tools/).

- F-LAND-1: (a) — mechanism-path streams (A1, B0, B23, B23-S) hand over a staged worktree + patch; a Fable session commits.
- F-A1-2: (a) — A1 lands with the absent `PROCESS/CRITIC_EXAM.md` named in the Fable commit; the Lead opens the finding.
- F-B1-4: (a) — `[bash, "-c", cmd]` with a capability probe; no bash → `--run` refused, door `--witness-file`.
- F-B23-2: (a) — declared family from the description; a differing `resolvedModel` prints TIER MISMATCH beside the line.
- F-T1-2: (a) — the one-file-per-tool exception covers the new tools of this spec only.
- C1 moved to wave 2 (it reads B0's header grammar): accepted as an ordering detail inside the owner's three waves.
