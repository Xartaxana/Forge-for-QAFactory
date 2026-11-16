# Spec — Lead moves to Opus, Architect (Fable) above Lead (t-893, F19; fix round 1 t-911)

Status: DRAFT by designer (opus), FIX ROUND 1 applied (t-911) after the plan critic t-902 (verdict: go with fixes,
`docs/tasks/specs/reviews/t-902-architect-tier-plan.md`). Forks still open are in the forks list with a recommendation;
decided forks carry their decision and its carrier. Rules are cited by NAME/NUMBER, never by CLAUDE.md line numbers (the
parallel spec `docs/tasks/specs/20261116-boot-by-topic-spec.md` moves CLAUDE.md sections AFTER this spec lands, §7.0).
The fix table is at the end of the file («Fix round 1 (t-911) — review t-902»).

The owner's word, 16.11.2026 (carrier: the Lead's intent brief t-893): «Переводим Опус на лида. Фейбл будет уровень
ещё выше — Архитектор, для анализа новых идей, оптимизации процесса и сложных вопросов. Лид может сказать мне что
лучше позвать Архитектора… Так же я сама что-то большое буду сначала обсуждать с фейбл». Decisions 1-8 of the brief
are taken as given and are not reopened (quoted as D1..D8 below).

---

## §0 Premises (every load-bearing claim below points here)

Rows P1-P36 were measured by the designer at draft time; the plan critic re-ran P1, P5-P8, P10-P20, P22, P23, P30,
P31, P33, P34 (t-902 «Premise re-check»). Rows P37-P54 were added in fix round 1 and measured by the designer by
reading the carrier (Read/Grep; this round had no shell). Line numbers drift: a dispatch re-reads the rows it relies
on (rule 11 checklist item 5).

| # | claim | carrier (file:line + quote, or command + output) |
|---|---|---|
| P1 | lead binding is Fable | `delegation.config.yaml:19-21` `lead:` / `subscription:` / `model: claude-fable-5-1` (re-read in round 1) |
| P2 | `reserve` is a COMMENTED optional rung above lead | `delegation.config.yaml:27` «OPTIONAL: a rung ABOVE lead, summoned only by the operator's own word»; `:43-49` `# reserve:` … `#     model: claude-fable-5` |
| P3 | critic Opus, builder/scout Sonnet; designer has no row | `delegation.config.yaml:52-54`, `:61-63`, `:70-72`; `:33-36` «`designer` deliberately has NO row here (see the onboarding skill's binding step)» |
| P4 | config comments point at the onboarding skill for rebinding and exams | `delegation.config.yaml:38-42` «rewalk the onboarding skill's binding step for `lead`, re-run that step's exam gate»; `:95-96` «see the onboarding skill, once installed under .claude/skills/onboarding/»; `:98-106` `exam: mandatory: true` … `on_failure: "warning + decision-log entry (operator override recorded)"` |
| P5 | tier-gate ladder | `tools/mechanism_gate.py:673` `ROLE_RANKS = {"scout": 0, "builder": 1, "critic": 2, "lead": 3, "reserve": 4}`; `:208` `LEAD_FAMILIES = ("fable", "opus", "sonnet", "haiku")` |
| P6 | lead-binding default is "fable" | `tools/mechanism_gate.py:591-600` `if not config_text: return "fable"` … `return model or "fable"` |
| P7 | a family strictly above the binding passes the tier gate; with the LIVE config Opus fails | `tools/mechanism_gate.py:851-853` `if declared_fam is not None and LEAD_FAMILIES.index(declared_fam) < LEAD_FAMILIES.index(fam): return True`; critic probe t-902 on the live config: `opus False`, `claude-opus-5-5 False`, `fable True`, `sonnet False` |
| P8 | duplicated model id on several rungs resolves to the MAX rank | `tools/mechanism_gate.py:727-730` «the MAXIMUM rank among all exact matches is taken»; `:789-790` `return max(exact_matches)` |
| P9 | designer deliberately absent from the tier-gate ladder | `tools/mechanism_gate.py:667-672` «roles.designer is ALSO not a ladder rung … see test_build_role_ladder_ignores_designer» |
| P10 | the tier gate's queue note names a CURRENT_CONTEXT section that does not exist | `tools/mechanism_gate.py:863-867` `_tier_queue_note` «it goes into the Lead queue in CURRENT_CONTEXT.md» (re-read in round 1); `CURRENT_CONTEXT.md` headings: `# Current Context`, `## Maintenance Rule`, `## Current Milestone`, `## Current Task` |
| P11 | `delegation.config.yaml` is NOT a mechanism path | `tools/mechanism_gate.py:211-283` `MECHANISM_PREFIXES` — no `delegation.config.yaml`; its only hits are the docstring `:98` and `CONFIG_PATH :206` (t-902) |
| P12 | the validator's family order and agent tiers | `tools/journal_validator.py:345` `TIER_ORDER = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}`; `:346-355` `AGENT_TIER` scout=haiku, builder=sonnet, critic=opus, designer=opus; `:366` `QUEUED_TO_LEAD_AGENTS = {"critic", "designer"}` (re-read in round 1) |
| P13 | matrix branches | `tools/journal_validator.py:676-677` `if agent == "lead": return None`; `:678-679` unknown agent → None; `:680` `if by not in TIER_ORDER` FAIL; `:710-732` judge branch; `:735` ok_tier; `:744` floor; `:761-762` `basis == "critic"` iff `TIER_ORDER["opus"] > agent_tier`; `:779-781` queued-to-lead iff agent in {critic, designer} and `by in ("sonnet", "opus")` (re-read in round 1) |
| P14 | only APPENDED lines are judged; HEAD lines are state | `tools/journal_validator.py:1100-1102` «HEAD and seed lines contribute their ids … none of them is judged» |
| P15 | `escalated` needs an EARLIER event of the task in the file | `tools/journal_validator.py:1287-1297` `elif event in ("accepted", "rejected", "escalated", "defect_found") … if task_id not in seen_task_ids:` → violation (re-read in round 1); `tools/journal_write.py:78` `NEW_TASK_EVENTS = ("delegated", "decomposable")` |
| P16 | MODEL line text | `tools/session_context.py:222` `("fable", "Lead(top)")`; `:998` `def model_tier`; `:1020` `def model_line`; `:1045` `" (declared by harness, not measured; Lead tier = fable)"` (lines re-read in round 1; the draft's 1031-1033 had drifted) |
| P17 | SessionStart prints at most 25 lines | `tools/session_context.py:183` `MAX_LINES = 25`; `:2192` `lines = [now_line(now), model_line(stdin_payload)]` (re-read in round 1) |
| P18 | session default model is a second carrier, read by no tool | `.claude/settings.json:2` `"model": "claude-fable-5-1"` (re-read); no tool reads settings' `model` (draft Grep; t-902 `git grep` agrees) |
| P19 | other family-tuple carriers | `tools/tier_echo.py:126` `KNOWN_TIER_WORDS`; `tools/dispatch_gate.py:1033` `_FAMILY_NAMES`; `tools/journal_echo.py:643-668` `_extract_declared_word` via `tier_echo.KNOWN_TIER_WORDS`; `tools/savings_report.py:71` `_UNBOUND = "fable"`; `tools/agents_md.py:198-216` `tier_words` AST-parses `TIER_ORDER`; `tools/token_usage_stats.py:172-182` `family()`; `tools/journal_hooks.py:210` door text «(sonnet / opus / fable / haiku)» (re-read in round 1) |
| P20 | `journal_write.py LEAD_ROWS` is NOT a family carrier | `tools/journal_write.py:75` `LEAD_ROWS = {"lead_degraded": "coordination", "lead_restored": "process", "calibrated": "calibration"}` |
| P21 | savings counterfactual = lead binding | `tools/savings_report.py:122-138` `def top_tier_model` «the one bound to roles.lead»; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:535` «priced … at top-tier rates» |
| P22 | journal history volume (TEMPORAL edge; grows daily) | Grep count `"by": ?"fable"` over `logs/journal/` → 671 (round 1; draft 656, t-902 663); `"by": ?"opus"` → 278 and `"basis": ?"queued-to-lead"` → 73 (t-902); one journal file exists (`dev1.jsonl`) |
| P23 | the Lead queue file is read by no tool and no boot step | Grep `lead-queue` over `tools/` → 0 naming the file (t-902, control `lead-queue-fable` over `docs` → 2 files); `docs/tasks/lead-queue-fable.md:1` «# Очередь для полного Lead (Fable)»; `:22-24` two items OPEN |
| P24 | calibration checks 5-6 speak of the "top tier" | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:104-115` check 5 «Lead-tier activity on a model below the top tier, outside a declared window, is silent degradation»; `:116-126` check 6 «"queued for the full Lead" note» (re-read in round 1) |
| P25 | critic role text | `.claude/agents/critic.md:52-57` «9. When the coordinator is below the top tier (degradation, or the standard mid-tier mode …)» (re-read in round 1) |
| P26 | Lead exam names TIER_ORDER and "top of the order" | `PROCESS/LEAD_RANKING_EXAM.md:29-31` «top of this deployment's tier order (`TIER_ORDER` in `tools/journal_validator.py`), no model above it exists to judge» |
| P27 | function table | `docs/TWO_VOCABULARIES.md:15` «**Lead** — … \| Fable session \| Fable alias» |
| P28 | D-0003 | `DECISIONS.md:30` «D-0003 — Bindings: lead claude-fable-5-1, critic and designer claude-opus-5-5, builder and scout claude-sonnet-5-5» |
| P29 | SIBLING_MAP: Lead Queue + the two skills | `docs/SIBLING_MAP.md:655-661` «Below-lead sessions put drafted axes into CURRENT_CONTEXT.md's "Lead Queue" section»; `:519` next-task row; `:522` onboarding row; axis 1 `:29-30` |
| P30 | readers of the onboarding skill's NAME outside history | `PROCESS/PATCH_PROTOCOL.md:22-23`; `docs/ADOPTION_LEDGER.md:3-4,23,52,77,143`; `.claude/skills/critic-exam-gen/SKILL.md:163,182`; `delegation.config.yaml:34,39,95-96` (t-902 `git grep` agrees) |
| P31 | install parity does NOT name the two skills | `tools/install_parity_anchors.json:657-661` unit `skills`, `"kind": "path"` — a directory unit |
| P32 | AGENTS.md generator does not list skills | `tools/agents_md.py:219-223` `build_setup`: `hooks_rows`, `roles_rows`, `tier_words` |
| P33 | FG7 rows; batch 7 is NOT taken (editable) | `plans/piles/forge/batch-7-vhodyashchie-4.md:3` «статус: ожидает \| взял: —»; FG7-14 `:37`; FG7-33 `:56` |
| P34 | a new test file is forbidden by default — lifted for this spec's leaf by the owner's word | `docs/TESTING.md:118` «новый тестовый файл не создаётся»; the owner's word 17.11.2026 «да» to F2 (a) (carrier: section «The owner's word» at the end of this file) |
| P35 | the tier-gate audit lists label mismatches, not the commits | `tools/mechanism_gate.py:55-57` `--audit --since` (audit_labels()) |
| P36 | no role named architect exists | `docs/SIBLING_MAP.md:29` role profiles `{scout,builder,critic,designer}`; `.claude/agents/*.md` `name:` lines (round 1 Grep `^name:` → scout, builder, judge, critic, designer) |
| P37 | the LIVE Fable session id differs from the binding | Grep `"model":"claude-fable-[0-9-]+"` -o over `logs/journal/dev1.jsonl` → 4 hits, all `claude-fable-5-2` (lines 231, 881, 1325, 2143); the binding is `claude-fable-5-1` (P1, P18) |
| P38 | a subagent's hook payload carries `agent_id`; the main thread's does not | `tools/agent_budget.py:6-8` «Hook input keys the harness gives (measured, t-575): … -- inside a subagent only -- agent_id» (PreToolUse, all tools); `tools/handoff_gate.py:11,18` «the main session (no `agent_id` in the payload)», order step «2. no agent_id -> pass» |
| P39 | critic has Bash, designer has none | `.claude/agents/critic.md:5` `tools: Read, Glob, Grep, Write, Bash`; `.claude/agents/designer.md:5` `tools: Read, Glob, Grep, Write`; builder `:5` has Bash/PowerShell |
| P40 | `journal_write.py` has no subagent check | Grep `agent_id\|agent_type` count over `tools/*.py` → 47 files, none is `journal_write.py` (control: the same call counts `journal_echo.py` 8, `handoff_gate.py` 15) |
| P41 | `escalated` field convention: `agent` = the function that acts next, `model` = the model it acts on; the writer's field order | `logs/journal/dev1.jsonl:308,423,451,1283,1558` e.g. `{"ts":"2026-11-12T19:50:32","event":"escalated","agent":"builder","model":"opus","task_id":"t-133",…"attempt 3 on an opus builder"}` — all five start `"ts":…,"event":"escalated","agent":` |
| P42 | `escalated` CLOSES a task for the open-dispatch reader | `tools/session_context.py:233` `_OPEN_LIFECYCLE_EVENTS = {"delegated", "accepted", "rejected", "escalated", "decomposable"}`; `:16-18` «OPEN iff its LAST lifecycle event … is `delegated`» |
| P43 | the matrix's ACTUAL branch order (the draft's §3.1 had it wrong) | `tools/journal_validator.py:676` lead → `:678` unknown agent → `:680` unknown-`by` FAIL → `:710` judge → `:735` ok_tier → `:744` floor → `:761` critic → `:779` queued-to-lead → `:795` generic |
| P44 | `basis: "judge"` is legalised by branch (1), not by `BASIS_VALUES` | `tools/journal_validator.py:373` `BASIS_VALUES = {"critic", "queued-to-lead"}` (no judge); `:374` `JUDGE_BASIS_VALUE = "judge"`; `:710-732` legal on a leaf category for scout/builder; Grep count `judge` in `tools/test_journal_validator.py` → 58. FG7-16's finding text («убрать `"judge"` из `BASIS_VALUES`») names the wrong carrier |
| P45 | a second `accepted` on a closed task is not refused | `tools/journal_validator.py:1287-1297` (an `accepted` needs only a `seen_task_ids` entry); reopening is refused only for `delegated` (`:1197-1207`); t-902 E3: 71 queued-to-lead tasks, 2 with a second accepted |
| P46 | `journal_write.py calibrated` takes no typed option today; `escalate` requires `--task` | `tools/journal_write.py:675` `add("calibrated", req=("notes",), opt=("agent", "model", "feature", "category"))`; `:670` `add("escalate", req=("task", "agent", "model", "notes"), …)`; Grep `reviewed_through\|NEW_TASK_EVENTS` over `tools/` → 2 hits, both `journal_write.py` (control for the same call) |
| P47 | FG7-54 (the Opus Lead exam, П3) already exists; FG7-16 and FG7-22 share the validator | `plans/piles/forge/batch-7-vhodyashchie-4.md:77` «FG7-54 \| П3 \| Экзамен лида для Опуса … (слово владельца 16.11: «запиши как узел П3. Когда-нибудь прогоним») \| Lead (Архитектор запускает)»; `:39` FG7-16 `tools/journal_validator.py`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`; `:45` FG7-22 `tools/journal_validator.py` «FG7-16 (общий файл)» |
| P48 | calibration checks end at 48; check 20 calls itself the judge's only detector | Grep `^(\d+)\. \*\*` over `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` → 1..48, last at `:1113`; `:673-681` check 20 «`tools/journal_validator.py` still accepts the value (residual node R-1 of t-013), so (b) is its only detector» |
| P49 | the boot-by-topic spec waits for this spec | `docs/tasks/specs/20261116-boot-by-topic-spec.md:351` «Phase 0 (Lead): … the architect-tier spec merged (its headings are read then — E17)»; `:502` E17 «S1 reads the headings of «Tiers», «Role ≠ tier», «Lead degradation» as they stand after it» |
| P50 | the tier gate matches a declared id by FAMILY substring | `tools/mechanism_gate.py:833-836` `fam = lead_family(binding)` … `if fam in declared.lower(): return True` → `tier: claude-fable-5-2` passes against a fable binding today |
| P51 | a second family ORDER carrier | `tools/token_usage_stats.py:119` `FAMILY_ORDER = ["Haiku", "Sonnet", "Opus", "Fable"]`; read at `:280-281` |
| P52 | hygiene gate shape | `tools/hygiene_gate.py:1554-1576` `decide(payload)`: Bash/PowerShell only, refusal = `permissionDecision: "deny"` on stdout, any exception fails OPEN visibly; `tools/permission_audit.py:469` imports the pure walk `hygiene_gate._collect_signals(command)`; `tools/test_warn_messages.py:540` pins `"Command hygiene: "` in the source; `tools/warn_layers.json:197-201` layer `HYGIENE` literal `"Command hygiene: "` |
| P53 | the Lead exam's purpose sentence assumes Lead ≠ critic model | `PROCESS/LEAD_RANKING_EXAM.md:3-4` «Purpose: distinguish the Lead tier from the builder/critic tier» |
| P54 | `.claude/settings.json` names no skill | read whole (193 lines): `permissions.allow` holds only Bash/PowerShell command patterns; no `skills` key |

---

## §1 What changes; mechanisms touched; the owner of every check

**What changes, in one paragraph.** The FUNCTION Lead is bound to Opus (`claude-opus-5-5`); a new FUNCTION
Architect is bound to Fable (`claude-fable-5-1`) and sits one rung above Lead. critic and designer stay on Opus (D1).
The acceptance matrix compares FUNCTION ranks scout < builder < critic = designer < lead < architect (D2); the code
that today compares model families (P12, P13) is brought to that rule through ONE ladder home (§2). Because Lead,
critic and designer now share one model, the critic's independence — until now guaranteed by Fable sitting above the
critic — gets a code refusal and a detector (§2.4, stream E). Mechanism commits are made by the Opus Lead after the
critic; the Architect reviews them as a weekly batch (D3) from a start checklist that only an Architect session loads
(D4, §4). DECISIONS.md stays one file (D5). Two old source skills are deleted (D6). The Opus Lead exam is the existing
П3 node FG7-54, which blocks nothing (D7, P47). The Lead never launches the Architect: it tells the owner and writes
`escalated` (D8). THIS landing is committed by a Fable session; the switch itself is one commit (§7.0).

**Package:** `ai-packages/qa-factory/` is NOT touched by any stream of this spec → no AR-n invariant applies; no
package commit is made, so no `architecture:` line is owed. (Should any stream drift into the package, that is a
scope violation, not an AR question.)

**Mechanisms touched (rule 10 recognition):** routing policy (CLAUDE.md «Tiers», rule 6, «Routing log» — the `by`
paragraph and the SHAPES rows `escalated` and `calibrated` —, «Role ≠ tier», «Lead degradation»); PROJECT.md «Как
разрабатывается новая идея владельца» (one line, m2); the tier gate (`tools/mechanism_gate.py`); the journal gate
(`tools/journal_validator.py`) and the one writer (`tools/journal_write.py`); the PreToolUse Bash hook
(`tools/hygiene_gate.py`); the SessionStart hook (`tools/session_context.py`); the model binding
(`delegation.config.yaml`, which becomes acceptance-deciding DATA → joins the mechanism net, §2.5); calibration checks
5, 6, 18, 20 and a new check 49 (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`); the critic role file; a new start
checklist; two queue carriers; two deleted skills.

**Checks added or altered — owner served, census class.** (The package census `judgment-census.json` is not
touched; the class below is the AR-29 vocabulary applied to forge checks.)

| check | added/altered | owner it serves | class |
|---|---|---|---|
| journal matrix: rank of `by` and of `agent` read from the ladder home (§3) | altered | DATA (code): who accepted whom, by shape; the MEANING of each acceptance stays the acceptor's judgment, re-judged at calibration by the Architect | data — shape/join, refusal |
| matrix: `basis: "judge"` refused (FG7-16, §3.1) | altered (legal → refused) | DATA (code): rule 13 says no judge is bound | data — enum, refusal |
| matrix: `basis: queued-to-lead` written by an acceptor ranked lead or above (§3.2, F5) | added, WARN | DATA (code) | data — shape, report only |
| validator: `accepted` of critic/designer work at a lead-ranked `by` with no earlier `delegated` of that agent carrying `worker_ref: agent:<id>` (§2.4, B4) | added, WARN | DATA (code): a separate context existed, by shape; whether it was independent in MEANING is JUDGMENT (the Architect at calibration, check 6) | data — join, report only |
| validator: `calibrated.reviewed_through` shape; `escalated` with `agent: architect` may open a task (§4.3, §4.5) | added | DATA (code) | data — shape, refusal |
| hygiene gate: `journal_write.py accept`/`reject` from a subagent payload refused (§2.4, B4) | added | DATA (code): who may write an acceptance line (the coordinator's main chain), by payload shape | data — presence, refusal |
| tier gate: ladder read from the home, `architect` rung (§2) | altered | DATA (code): form of the `tier:` line; its TRUTH is calibration's judgment (Architect) | data — shape, refusal |
| tier gate: `delegation.config.yaml` and the home module join `MECHANISM_PREFIXES` (§2.5) | added | DATA (code) | data — presence |
| SessionStart MODEL line by function; ARCHITECT line; calibration-overdue suffix (§4.4, §5.4, M2) | altered/added | DATA (code) reports; the session's entry decision is JUDGMENT (the session's own tier check) | data — report, no refusal |
| SessionStart WARN: `.claude/settings.json` `model` ≠ lead binding (F15, owner's word) | added | DATA (code) | data — join, report only |
| `mechanism_gate.py --list --since` (commits for the Architect's batch review, §4.5) | added | DATA (code) lists; the review verdict is JUDGMENT (Architect, a tier above Lead) | data — listing |
| Architect start checklist (§4.5) | added | JUDGMENT (Architect), accepted by INTENT (owner — the owner switches the model) | judgment procedure |
| weekly batch review of mechanism commits (§4.6) | added | JUDGMENT (Architect over Lead's work) | judgment |
| Lead's signal «лучше позвать Архитектора» + `escalated` (§4.3, §4.7) | added | JUDGMENT (Lead), INTENT (owner decides to switch) | judgment + intent |
| calibration checks 5/6 by function rank; check 6 independent-context item; check 20 wording; check 49 Architect cadence (§5.5) | altered/added | JUDGMENT (calibrator = Architect, F10 owner's word) on DATA from the ladder home and the validator WARNs | judgment on data |

---

## §2 The ladder as data — one home, one reader

### 2.1 The home

ONE module, the new leaf `tools/tier_ladder.py` with its own test file `tools/test_tier_ladder.py` (F2 (a), the
owner's word 17.11.2026, P34), holds the facts every reader needs; ONE file holds the bindings:

1. `FAMILIES` — the model-family vocabulary in ONE order, weakest → strongest: `("haiku", "sonnet", "opus", "fable")`,
   with an alias row `ALIASES = {"mythos": "fable"}` (taken from `token_usage_stats.family`, P19). A reader needing
   strongest-first reverses it; no reader keeps its own tuple.
2. `FUNCTION_RANKS` — `{"scout": 0, "builder": 1, "critic": 2, "designer": 2, "lead": 3, "architect": 4}` (D2:
   critic = designer). `COORDINATION_FUNCTIONS = ("scout", "builder", "critic", "lead", "architect")` — the rungs a
   CONFIG binding is read for (designer stays out of the config ladder, P9; its rank is used only to judge it as an
   executor). The order is a code constant (F3 (a)).
3. `DEFAULT_BINDINGS = {"lead": "fable", "critic": "opus", "builder": "sonnet", "scout": "sonnet"}` — the bindings
   used when the config yields none (absent, unparsable, oversize, aliased, no pyyaml). It equals today's live config
   by family, so a config-less clone and a broken config behave exactly as today (one road: the same `rank_of_model`
   runs on it; there is no second table — M4/M6).
4. Bindings — `delegation.config.yaml` `roles.<function>.subscription.model` / `.api.model` (unchanged format), read
   by the home's one parser.

**Import discipline (M5, compatible with F2 (a)).** The module imports only the standard library at import time;
`yaml` is imported LAZILY inside `bindings()`. So `tier_echo`, `dispatch_gate` and `journal_hooks`, which need only
`FAMILIES`/`family_of`, take no pyyaml dependency on the hook path, and the validator imports no yaml until it reads
the config. The leaf imports no other tool module (a leaf, not a gate). The key of the new rung is `architect`
(F1 (a)).

### 2.2 The reader functions (public names; one road for every reader)

- `family_of(model_id) -> str | None` — lowercase substring match on `FAMILIES` + `ALIASES`; `None` for a non-Claude
  id, an empty or non-string input.
- `bindings(config_text) -> tuple[dict[function, model_id], str | None]` — the coordination functions that have a
  model, and a problem note. Absent text, text over 64 KB, any YAML alias/anchor (a loader subclass that raises on an
  alias event), a parse error, no `roles` mapping, or pyyaml missing → `({}, "<reason>")`; the callers then use
  `DEFAULT_BINDINGS` and print the note once (§2.4). An uncommented `roles.reserve` → its value is NOT read; the note
  says «`roles.reserve` is not read: rename it to `roles.architect`» (F1).
- `effective_bindings(config_text) -> tuple[dict, str | None]` — `bindings()` or, when it yields `{}`,
  `DEFAULT_BINDINGS` with the note. EVERY reader below goes through this one function.
- `rank_of_function(name) -> int | None` — `FUNCTION_RANKS`; unknown name → `None`.
- `rank_of_model(model_word_or_id, config_text) -> int | None` — THE function the matrix, the tier gate and the
  MODEL line share, on `effective_bindings`:
  (a) exact id match on a bound rung → max rank among matches (keeps P8);
  (b) else the FAMILY: the max rank of functions bound to that family (this is the case of the live session
      `claude-fable-5-2` against the binding `claude-fable-5-1`, P37);
  (c) a known family bound to NOTHING → placed by family order: stronger than the lead binding's family →
      `architect` rank ("a rung above lead", the existing reserve-above-binding concept, P7); weaker than every bound
      family → `-1` (below scout: the floor); between two bound families → the rank of the nearest WEAKER bound
      family's top function (rounds DOWN);
  (d) unknown family, non-Claude id with no exact match, empty, non-string → `None`.
  The family-strength guard of `_resolve_ladder_rank` (P5, `mechanism_gate.py:780-807`: a rung bound to a family
  WEAKER than lead's never inherits a rank ≥ lead) moves into this function unchanged.
- `lead_binding(config_text) -> str | None` and `architect_binding(config_text) -> str | None` — from
  `effective_bindings` (so the lead binding of a broken config is `"fable"`, P6 kept).
- `function_of_session(model_id, config_text) -> tuple[str | None, str]` (B2) — DERIVED from `rank_of_model`, never a
  matcher of its own: rank → the COORDINATION function of that rank (`2` → `critic`; designer is never a session
  function), plus a note naming the road taken: `""` (exact id), `"family match: <binding id>"` (case b),
  `"no architect binding"` (case c above lead), `"unbound family"` (case c below lead), `"config unreadable: default
  bindings"` (the note of `effective_bindings`). Rank `-1` → `(None, "below builder")`; `None` → `(None, "matches no
  binding")`.

**Error direction (rule 1: an advisory resolver becomes a GATE input).** `rank_of_model` may err only DOWNWARD
(lower rank → a basis is needed / the tier line is refused); it may never invent a rank above what the bindings or
the family order give. Adversarial inputs that must stay on the safe side (each a table row in `test_tier_ladder.py`):
`by="claude-opus-5-5"` (full id where a word is expected — the VALIDATOR still FAILS it at its enum check, §3.1, as
CLAUDE.md says today; `rank_of_model` itself ranks it, which is what the tier gate needs); `"Opus"` / `" opus "`
(the validator compares exact lowercase keys today, P12 — keep FAIL); `"lead"` (a function word where a model word is
expected → `None`, and the validator FAILS it with a door, F4-A); `"opus-lead"`; `"fable"` with NO architect key
(→ architect rank by case (c) when lead is not fable; lead rank when lead is fable — the one permissive case, kept
because P7 already encodes it and 671 old lines carry `by: fable`, P22); a config binding critic=fable, lead=opus
(nonsense: a lower function on a stronger family) → fable resolves to `critic` rank by the guard's positional rule,
not above lead; lead and architect bound to the SAME id → exact match max rank = architect, and opus (now unbound)
rounds DOWN to builder; `claude-fable-5-2` against `claude-fable-5-1` → architect via case (b) (B2 row);
`claude-fable-5-2` against a config whose architect key is absent and lead=opus → architect rank via case (c); empty /
non-string; a config with an alias bomb (`a: &a [*a, *a]` style) → `({}, note)` → DEFAULT_BINDINGS, never a hang; a
config of 64 KB + 1 byte → `({}, note)`; a config of exactly 64 KB → parsed.

### 2.3 Every current carrier — reads the home / deleted / stays

| carrier | today | after |
|---|---|---|
| `tools/mechanism_gate.py:673` `ROLE_RANKS` | own ranks | DELETED; reads `FUNCTION_RANKS`/`COORDINATION_FUNCTIONS` |
| `tools/mechanism_gate.py:208` `LEAD_FAMILIES` | own tuple strongest-first | DELETED; reads `FAMILIES` reversed |
| `tools/mechanism_gate.py:582-611` `resolve_lead_binding`, `lead_family` | own parser, default "fable" | thin wrappers over `lead_binding`/`family_of`, kept for their importers (`savings_report.py:63`); default "fable" now comes from `DEFAULT_BINDINGS` (P6 kept) |
| `tools/mechanism_gate.py:690-810` `build_role_ladder`, `_resolve_ladder_rank` | own ladder | DELETED into `rank_of_model` |
| `tools/mechanism_gate.py:831-860` `tier_declared_ok` | exact / family substring / family-above / ladder | `rank_of_model(declared, cfg) >= FUNCTION_RANKS["lead"]` (the four branches are the cases (a)-(c) of the one function; P50's family substring match is case (b)) |
| `tools/journal_validator.py:345` `TIER_ORDER` | family → 0..3 | DELETED (no legacy table: F18 (b)); the enum check of `by` reads `FAMILIES` |
| `tools/journal_validator.py:346-355` `AGENT_TIER` | agent → family | DELETED; agent rank = `rank_of_function(agent)`; "agent known to the matrix" = `agent in FUNCTION_RANKS` |
| `tools/journal_validator.py:366` `QUEUED_TO_LEAD_AGENTS` | {critic, designer} | stays (a data row of the matrix, not a ladder fact); its condition reads ranks (§3.2) |
| `tools/journal_validator.py:374,710-732` `JUDGE_BASIS_VALUE` and branch (1) | judge legal on a leaf | branch becomes a REFUSAL (FG7-16, §3.1); `LEAF_CATEGORIES` stays only if another reader needs it (builder checks by Grep; else deleted) |
| `tools/session_context.py:221-226` `_MODEL_TIER_SUBSTRINGS`, `:998` `model_tier` | own tuple → labels | DELETED; `function_of_session` |
| `tools/tier_echo.py:126` `KNOWN_TIER_WORDS` | own tuple weakest-first | `KNOWN_TIER_WORDS = tier_ladder.FAMILIES` (same order; `test_extract_declared_word_picks_first_known_tier_words_order` stays green) |
| `tools/journal_echo.py:643` `_extract_declared_word` | via tier_echo | unchanged code (reads through tier_echo, which now reads the home) |
| `tools/dispatch_gate.py:1033` `_FAMILY_NAMES`, `_model_family` | own tuple | reads `FAMILIES` / `family_of`; the docstring's «implemented locally (this layer does not import any other gate module for it)» (`:1047-1050`) is reworded: the home is a leaf, not a gate |
| `tools/journal_hooks.py:210` door text «(sonnet / opus / fable / haiku)» | literal list | built as `" / ".join(FAMILIES)` (order becomes weakest-first; no test pins the literal: Grep `fable` in `tools/test_journal_hooks.py` → 2 hits, both `"by": "fable"` values at `:167,190`) |
| `tools/savings_report.py:71` `_UNBOUND = "fable"`, `:122` `top_tier_model` | lead binding | reads `lead_binding` (F11 (a): the lead binding, relabelled «coordinator model») |
| `tools/agents_md.py:198-216` `tier_words` (AST of validator `TIER_ORDER`) | parses a literal in another file | AST of the home's `FAMILIES` literal (same technique) — AGENTS.md content: the CLAUDE.md copy's word list follows CLAUDE.md (L) |
| `tools/token_usage_stats.py:172` `family()` | own heuristic + display case | reads `family_of`; display capitalisation stays local (C4) |
| `tools/token_usage_stats.py:119` `FAMILY_ORDER` (M7, P51) | own ORDER list | `FAMILY_ORDER = [f.capitalize() for f in tier_ladder.FAMILIES]` — same value, order from the home |
| `tools/journal_write.py:75` `LEAD_ROWS` | event → category | UNCHANGED — not a ladder carrier (P20) |
| `tools/fixtures/host_pre_delivery_CLAUDE.md` | frozen old text | UNCHANGED — a frozen fixture by design |
| `PROCESS/LEAD_RANKING_EXAM.md:3-4, 29-31` | purpose «distinguish the Lead tier from the builder/critic tier»; names `TIER_ORDER` | stream F: purpose reworded (M3, P53), pointer to the home's `FUNCTION_RANKS`, «Fable (Architect) judges an Opus candidate» |
| `.claude/settings.json:2` `"model"` | Fable | the lead binding value (F15 (a), owner's word); read by the harness, and compared by the SessionStart WARN (stream C) |

### 2.4 Edges of the home (TEMPORAL and absent inputs)

- **Config without the architect key** (other clones, an old checkout, the world before stream L): `bindings()` has
  no `architect`; with lead=fable (today) `rank_of_model("fable")` = lead rank, exactly as today; with lead=opus,
  fable → architect rank by case (c). Invariant: *removing or never adding the key never makes any party MORE
  privileged than with it*. (With the key bound to Fable the results are identical; with the key bound to a
  non-Claude id, fable still ranks above lead by family — stated, tested.)
- **Config with the old `reserve:` key uncommented**: not read; one note line names the rename door (F1 (a)).
  Invariant: a key the code does not read never silently raises a rank.
- **Absent / unparsable / oversize / aliased config, or no pyyaml** (M6 — ONE behaviour, no refusal): `bindings()`
  → `({}, note)` → `DEFAULT_BINDINGS` (today's ranks) + the note printed ONCE by the caller: the validator prints
  `WARN: delegation.config.yaml unreadable (<reason>) -- default bindings (lead=fable) used; fix the file` to stderr;
  the MODEL line appends `(config unreadable: default bindings)`; the tier gate's refusal text (if it refuses) carries
  the same note. Invariant: *a broken config can only make acceptance STRICTER than the live one* (after L, Opus
  would need a basis to accept critic work — the safe direction); nobody is ever refused for the config itself.
- **lead, critic and designer on the same model** (the new live state; P8 max rule → an Opus `by` ranks as lead) —
  the critic's independence (D2) no longer comes from a stronger acceptor model. It is kept by two layers (B4):
  (i) CODE on the path: the PreToolUse Bash hook `tools/hygiene_gate.py` refuses a `journal_write.py accept` or
  `reject` call made from a subagent payload (one carrying `agent_id`, P38; the same detection `handoff_gate` and
  `agent_budget` rely on, measured in t-575). Refusal text (FR-1/FR-2, ASCII English, under the gate's existing
  `Command hygiene: ` deny wrapper, P52): «Command hygiene: an acceptance or rejection is written by the coordinator's
  main chain, not by a worker -- put your verdict in your handoff file; the coordinator records it». (ii) DETECTOR:
  the validator WARNs on an appended `accepted` with `agent ∈ {critic, designer}` and a lead-ranked or higher `by`
  when no earlier `delegated` of that same agent on that task carries a `worker_ref` starting `agent:` — text
  `WARN: INDEPENDENT CONTEXT: <task> accepted at by=<by> with no agent:<id> delegated of <agent> -- a review must come
  from a separate worker context`; calibration check 6 lists these WARNs over the window (registered by stream F).
  Invariant: *a worker never writes an acceptance line, and an acceptance of critic/designer work at the Lead's own
  model always points at a separate worker context*. Error direction of the refusal: it may refuse a harmless
  subagent command (a false refusal costs a worker one command; door: the Grep tool / the handoff file); it must
  never pass a real invocation in the forms listed in stream E. Residual, stated: an INDIRECT invocation (a script
  file or `python -c` that calls the writer) and a hook exception (the gate fails open visibly, P52) are not caught
  by (i) — (ii) catches the resulting line.
- **A session model matching no binding**: §5.4.

### 2.5 The mechanism net

`delegation.config.yaml` becomes DATA that decides acceptance legality and the tier gate (like
`logs/journal-letters.json`, P11) → it joins `MECHANISM_PREFIXES` with a comment «DATA that decides the acceptance
matrix and the tier gate: an edit re-ranks every acceptor». `tools/tier_ladder.py` joins too («imported by
journal_validator / session_context / mechanism_gate / tier_echo / dispatch_gate / journal_hooks»); the closure test
`test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` (named at `mechanism_gate.py:259`)
enforces it. TEMPORAL: the commit that adds the config to the net is stream A's; it touches `tools/mechanism_gate.py`
anyway, so it carries the axis block and `tier: fable` (§7.0). From that commit on, the stream-L flip of the config
is itself a gated mechanism commit.

---

## §3 The acceptance matrix by function

### 3.1 The table (rank of the acceptor = `rank_of_model(by)`; rank of the executor = `rank_of_function(agent)`)

| executor (`agent`) ↓ / acceptor rank → | below builder (−1; e.g. haiku) | builder rank (Sonnet coordinator, degraded) | lead (Opus) | architect (Fable) |
|---|---|---|---|---|
| scout (0) | ILLEGAL (floor) | legal | legal | legal |
| builder (1) | ILLEGAL | needs `basis: critic` | legal (the "critic: skipped" waiver available) | legal |
| critic (2) | ILLEGAL | needs `basis: queued-to-lead` | legal — **Lead accepts a critic verdict** (+ the independent-context WARN, §2.4) | legal (+ the same WARN) |
| designer (2) | ILLEGAL | needs `basis: queued-to-lead` | legal — **Lead accepts a designer draft** (+ the same WARN) | legal (+ the same WARN) |
| lead (`agent: "lead"`) | no matrix (P13 `:676`) | no matrix | no matrix | no matrix |
| architect (`agent: "architect"`) | no matrix (new: same branch as `lead`, C6) | no matrix | no matrix | no matrix |
| unknown agent | no matrix (unchanged, P13 `:678`) | — | — | — |

`basis: "judge"` on ANY row → REFUSED (FG7-16): «role-vs-tier acceptance matrix: basis "judge" is not legal here --
no judge is bound in this deployment (CLAUDE.md rule 13); accept from a tier above, or use basis 'critic' /
'queued-to-lead' for the (by, agent) pair».

Branch order of `_matrix_d0058_violation` — the ACTUAL order (P43; the draft misquoted it) with the judge branch
turned into a refusal: lead/architect no-matrix → unknown agent no-matrix → unknown-`by` FAIL (`by not in FAMILIES`,
exact lowercase) → `basis == "judge"` REFUSED → ok_rank (`rank(by) > rank(agent)`) → floor (`rank(by) < builder
rank`) → `basis: critic` → `basis: queued-to-lead` → generic FAIL. Positional invariants (rule 11 (ii)): the
unknown-`by` enum check stays FIRST among the checks of a known agent, so no rank arithmetic ever runs on an
unidentifiable acceptor; the judge refusal precedes ok_rank, so no acceptor rank — Fable included — makes a judge
basis legal (today a judge basis was decided before ok_tier too); the floor stays before every remaining basis, so no
basis rescues a below-builder acceptor. The independent-context WARN (§2.4) runs AFTER the matrix and only on lines
the matrix passed; it never turns a pass into a FAIL.

### 3.2 `basis` after the change

- `basis: critic` — legal iff `rank_of_function("critic") > rank(agent)` (scout, builder). Unchanged semantics; the
  literal `TIER_ORDER["opus"]` (P13 `:762`) becomes the critic's FUNCTION rank.
- `basis: queued-to-lead` — legal iff `agent ∈ QUEUED_TO_LEAD_AGENTS` AND `builder rank ≤ rank(by) < lead rank`.
  Today's literal `by in ("sonnet", "opus")` (P13 `:780`) becomes this rank band. A line where `rank(by) ≥ lead`
  already passed at ok_rank before the basis is read — such a line queues work to itself: WARN (F5 (a)) `WARN:
  queued to itself: <task> by=<by> ranks lead or above -- drop the basis`.
- `basis: "judge"` — refused (§3.1).

### 3.3 What `by` holds in a NEW line — F4 (A), decided

`by` stays the bare MODEL-FAMILY word (`haiku`/`sonnet`/`opus`/`fable`) — the session's self-declared model, the
thing calibration can reconcile against transcripts; the validator turns it into a FUNCTION rank through
`rank_of_model` (D2 satisfied: ranks are function ranks). Nothing changes for writers (`journal_write.py accept --by
B`); the 671/278/73 history lines (P22) keep their vocabulary.

### 3.4 Both worlds (TEMPORAL) — no cutover (F18 (b), decided in fix round 1)

- **Old lines are never re-judged** (P14): HEAD lines are state.
- **No legacy table, no `LADDER_FROM`.** Every appended line is judged by the function ranks over the CURRENT
  working-tree config of the repo being validated. Why this is enough (t-902 M4): an old-world line that was ILLEGAL
  cannot be in a committed journal — `.githooks/pre-commit:8` runs the validator, `pre-merge-commit:18` runs
  `--merge-parent`, CI `forge-check.yml:72` runs `--all --base "$BASE"`; and every old-legal pair stays legal under
  the new ranks (pair by pair: fable > everything in both worlds; opus + critic + queued-to-lead passes at ok_rank
  after L, in the band before L; sonnet + builder + critic passes; sonnet + scout passes, builder > scout).
  Residual, stated: a `--no-verify` line of another clone written before the switch as a self-certification (`by:
  opus`, `agent: critic`, no basis) would pass at a merge after L — CI at that clone's branch already flagged it, and
  calibration check 6 reads acceptance by session model, not by this table.
- **The transitional world (rule 11 (i); B1).** Streams A-F land while `delegation.config.yaml` still binds lead to
  Fable. Until stream L flips it, every gate behaves EXACTLY as today, because `rank_of_model` on today's config gives
  today's order (fable = lead 3, opus = critic 2, sonnet = builder 1, haiku = −1 unbound weaker). Pair check (each a
  row of the B DoD on a fixture config equal to today's): `by: opus, agent: critic`, no basis → FAIL (2 > 2 false;
  generic) — as today; same with `basis: queued-to-lead` → OK (band 1 ≤ 2 < 3) — as today; `by: fable, agent: critic`
  → OK; `by: sonnet, agent: builder, basis: critic` → OK; `by: haiku` any → FAIL (floor); `by: opus, agent: builder`
  → OK. The tier gate on today's config: `tier: fable` and `tier: claude-fable-5-2` pass, `tier: opus` is refused —
  as today (P7, P50). The only behaviour changes before L are the ADDED ones: the judge refusal (FG7-16), the two
  WARNs, `reviewed_through`, `escalated` agent=architect opening a task, the subagent refusal, the MODEL line wording.
- **The flip** is ONE commit — stream L, made by a Fable session (§7.0) — carrying the config change, the settings
  model, CLAUDE.md, AGENTS.md regen, DECISIONS.md, the PROJECT.md line and the batch-7 rows. Nothing else in the code
  has a date or a placeholder to fill.
- **Cross-clone note.** The config is tracked: the flip is global for every developer of the forge once merged. A
  second developer's Fable session keeps passing everything; an Opus session of theirs becomes a full Lead. The Lead
  tells the other developers (§7, L).
- **`tier: fable` lines in old commits**: the tier gate judges only the commit being made (`decide_full`,
  `mechanism_gate.py:947-980`); `--audit` judges axis labels only (P35). New `tier: fable` commits pass (case (b)/(c)).

### 3.5 `queued-to-lead` items — who clears them, by which road (M9)

- **Old items** (73 lines, P22, written when the full Lead was Fable): already closed by the written `lead_restored`
  window acceptances (t-902 E3: that is today's practice; 2 of 71 tasks also carry a second `accepted`). No backlog is
  owed; nobody re-clears them.
- **New items** (a Sonnet coordinator accepts critic/designer work with `basis: queued-to-lead`): ONE road, fork
  **F23** (recommended (a)): a Lead-ranked session clears an item by a SECOND `accepted` of the same task with its own
  `by` and no basis (legal today: a second `accepted` on a closed task is not refused, P45); calibration check 6 lists
  queued-to-lead lines of the window with no later lead-ranked `accepted` of the task. `docs/tasks/lead-queue.md` is
  NOT a carrier of queued acceptances (it holds what a below-Lead session cannot do at all, §4.4).
- The Architect does NOT owe the clearing (Lead work); an Architect session MAY do it (§5.2).

---

## §4 The Architect function

### 4.1 Its work (owner's list + the brief's decisions + the owner's word 17.11)

1. Analysis of new ideas — the owner discusses big things with Fable first (owner's word); PROJECT.md «Как
   разрабатывается новая идея владельца» steps 1-4 may run in an Architect session; steps 5-8 go to the Lead's routing
   as today. Stream L adds this as one line to that PROJECT.md section (m2), so the owner's word does not live only in
   this spec.
2. Process optimisation and hard questions the Lead escalates (§4.3), including rule-6 escalations above Opus (§4.7).
3. The weekly calibration, which includes the batch review of mechanism commits (D3; F10 (a), owner's word
   17.11.2026: the Architect runs the weekly calibration), «или чаще, если на него переключаются» (§4.6).
4. Decisions into `DECISIONS.md` (same file, D5); the Architect session writes its own line (F21 (a), owner's word
   17.11.2026; PROJECT.md «Командная работа» п. 5 «пишет только Lead владельца» read as «Lead rank or above»).

**Not its work:** routine coordination, dispatching and accepting workers (Lead), each mechanism commit (D3 — Lead
after critic; THIS landing is the stated exception, §7.0), being launched as a subagent (D8: the owner switches the
session model), the Lead's queue items (§3.5).

### 4.2 Summoning

Only by the owner's switch of the session model (`/model` or a new session on the Fable binding). Never routed to
automatically; never a subagent. FG7-33 («Opus-координатор точечно вызывает Fable субагентом», P33) is SUPERSEDED by
D8: stream L sets the node's status to «снят: заменён решением владельца 16.11.2026 (спека 20261116-architect-tier-spec)»
— a Lead edit in an untaken batch (P33 `:3`).

### 4.3 The Lead's signal

When a question is Architect-class (a new idea's architecture, a process trade-off, a rule conflict the Lead cannot
settle, a disagreement with a critic verdict the Lead cannot resolve, a rule-6 escalation above Opus §4.7), the Lead
(a) tells the owner in plain Russian «лучше позвать Архитектора: <вопрос одной строкой>, <что ждёт>», (b) writes the
question as an item of the Architect queue (§4.4), (c) writes `escalated` with `agent: "architect"`, `model` = the
ARCHITECT BINDING (`claude-fable-5-1`; P41: `agent` names the function that acts next and `model` the model it acts
on — the existing convention, which calibration check 4 reconciles against transcripts; M8), `task_id`, notes = the
item's one-line summary + the queue path. **No task exists yet** (a fresh idea; P15 refuses an `escalated` whose task
has no earlier event) — F6 (a), decided: an `escalated` with `agent: "architect"` may OPEN a task: the writer issues
the id when `--task` is absent and `--agent architect` (stream B), and the validator accepts the line as a new task
under the same novelty rule as a `delegated` (9a''). Any other `escalated` still needs an earlier event (P15).
Work on that question waits for the Architect; unrelated work continues. The CLAUDE.md SHAPES row of `escalated` is
rewritten by stream L to say both (B3.3).

### 4.4 The queue carriers (F8 (a), decided)

TWO files, one per direction, both outside the mechanism net:
- `docs/tasks/lead-queue.md` — `git mv` of `docs/tasks/lead-queue-fable.md`, retitled «Очередь для Lead»: what a
  below-Lead session cannot do (mechanism commits, Lead-class decisions; builder diffs that wait out an Opus outage,
  §5.3). Written by any coordinator; struck («сделано: <хэш | t-nnn>») by a Lead-ranked session. Its two OPEN items
  (P23 `:22-24`) move with it. The tier gate's note (P10) and `docs/SIBLING_MAP.md:659` point HERE instead of the
  non-existent CURRENT_CONTEXT section. Not a carrier of `queued-to-lead` acceptances (§3.5).
- `docs/tasks/architect-queue.md` — new: items the Lead (or the owner) puts to the Architect. Item form, one per
  line: `- [ ] <YYYY-MM-DD> <task_id|—> <question one line> (от: Lead|владелец)`; struck by the Architect:
  `- [x] … — сделано: <D-nnnn | хэш | t-nnn | ответ одной строкой>`. Written by the Lead and the owner; read by an
  Architect session at start (checklist step 3); the SessionStart line counts `- [ ]` items.

**SessionStart line** (stream C), printed ONLY when `function_of_session(model)[0] == "architect"` (so the live id
`claude-fable-5-2` prints it through the family match, B2), placed directly after the MODEL line so the 25-line cut
(P17) can never drop it:
`ARCHITECT SESSION: start with PROCESS/ARCHITECT_START.md; queue docs/tasks/architect-queue.md (<N> open)`.
Edges: queue file absent → `(queue file absent)`; unreadable → `(queue unreadable: <reason>)`; N = 0 → `(0 open)`;
architect key absent and the session's family stronger than lead → the line is NOT printed and the MODEL line says
`above lead (no architect binding)` (§5.4). Invariant: *a non-Architect session never pays boot bytes for the
Architect*.

### 4.5 The START CHECKLIST (D4) — `PROCESS/ARCHITECT_START.md` (F7 (a), decided)

Loaded only via the SessionStart pointer above (zero bytes for other sessions; not in CLAUDE.md body). Ordered:

1. **Tier check.** The MODEL line says function `architect` (exact or `family match`). If not — this file does not
   apply; stop.
2. **The owner's reason first.** If the owner switched with a question, that question is item 0; the steps below run
   after it is answered or in parallel only when cheap.
3. **Architect queue.** Read `docs/tasks/architect-queue.md`; every `- [ ]` item gets an answer, a decision, or an
   explicit «оставлено: <почему>».
4. **Escalations to the Architect** (B3.4, decided: a named command, no new event, no SessionStart reader — the
   existing open-dispatch reader cannot serve, because `escalated` CLOSES a task there, P42). Run
   `git -C C:/QAFactory/forge-repo grep -n "\"event\":\"escalated\",\"agent\":\"architect\"" -- logs/journal/`
   (the one writer emits `"ts"`, `"event"`, `"agent"` in this order, P41). Every hit dated after the previous
   `reviewed_through` marker must match a queue item (open or struck) by its task id; a hit with no item, or an item
   whose task id has no hit, is a finding. Error direction: a line written in another field order (by hand, against
   hygiene pt.5) is missed by the grep — the reverse direction (item → hit) and check 49 (c) catch that side.
5. **Mechanism commits since the last Architect review.** `python -B tools/mechanism_gate.py --list --since
   <reviewed_through sha>` (stream A) — one line per commit touching a mechanism path (`mechanism_paths()`), merges
   against first parent: `<sha> <committer date> <tier: values> <subject>` + its mechanism paths. The "since" value =
   the `reviewed_through` field of the newest `calibrated` line (F9 (a)); none yet → the date of stream L's commit.
   Each commit: OK, or a finding / `defect_found` against the accepting task.
6. **Calibration.** If the SessionStart `Last calibration` line says overdue (> 7 days) → run the weekly calibration
   (F10 (a)), which includes step 5.
7. **Boot budget.** The `BOOT BUDGET` line: over WARN → the boot-diet backlog item goes to the Lead queue (the
   Architect does not trim boot files itself unless the owner says so).
8. **Close the review.** Write the marker: `python -B tools/journal_write.py calibrated --reviewed-through <sha of
   the last reviewed commit> --notes "<period, counts>"` (stream B adds the option).

### 4.6 The weekly batch review

The Architect reviews the mechanism commits of the window (step 5) for: the axis block truthful, the rule placed at
the right level (rule 9), the detector registered (rule 10 c), D-entries consistent. Verdicts go into the
calibration report; a defect is a `defect_found` (agent = the accepting tier, `ref` = the original task) or a
finding in `plans/piles/forge/findings/` with its batch row (PROJECT.md «Командная работа» п. 2).

**Weekly trigger on the Lead's path (M2).** The calibration lives in the Architect checklist, which loads only once
the owner switches. So stream C extends the existing `Last calibration` line (no new line): when the newest
`calibrated` is older than 7 days, or there is none, the line ends with — in a session whose function is not
architect — `-- overdue: tell the owner «лучше позвать Архитектора» (calibration and mechanism review)`; in an
Architect session — `-- overdue: run the calibration (PROCESS/ARCHITECT_START.md step 6)`. The Lead's move on
seeing it (CLAUDE.md «Role ≠ tier», Lead bullet, stream L): tell the owner once per session and put one item into
`docs/tasks/architect-queue.md` if none is open for this calibration. Detector: check 49 (b) (stream F). Edges: an
unparsable `ts` → the line as today (`age unknown`), no suffix (an unknown is not reported as overdue, FR-41);
exactly 7 days → not overdue; NONE → overdue.

### 4.7 Rule 6 above Opus (M1)

- **Escalation.** Two `rejected` on critic- or designer-class work (Opus) → "one tier up" is the Architect, which is
  never a subagent (D8). The move: the §4.3 road — an architect-queue item + `escalated` (`agent: "architect"`,
  `model` = architect binding, the existing `task_id`). The work waits for the Architect. Builder escalations are
  unchanged (Sonnet → an Opus builder, P41). Stream L writes this into CLAUDE.md rule 6.
- **Whether a Fable SUBAGENT may stand in** (e.g. a critic run on Fable while Opus is down) is an intent question:
  fork **F22** (owner), executable on the recommendation (no) until her word.

---

## §5 «Role ≠ tier» and «Lead degradation» for the new ladder

### 5.1 Definitions (rewrite)

- The TIER of a session = the FUNCTION RANK of its actual model: `rank_of_model(model)` — the highest function bound
  to it, by exact id or by family (Opus → lead even though critic and designer share the id; `claude-fable-5-2` →
  architect through the family).
- Full Lead = a coordinator whose rank is ≥ lead (Opus, or Fable doing Lead work). Only it changes mechanisms, the
  decision log, table statuses and gates.

### 5.2 The matrix by the coordinator's actual function rank

- **Architect (Fable)** — unrestricted; may do any Lead work WITHOUT an event (it is above Lead; the tier gate
  passes `tier: fable`, P7). No new event for "Architect did Lead work": the `model` field of its journal lines and
  the main-chain transcript record it.
- **Lead (Opus)** — full Lead: coordination, dispatch, acceptance of scout/builder/critic/designer (§3.1), the
  "critic: skipped" waiver over builder, mechanism commits after the critic (D3), DECISIONS.md (D5), statuses.
  Architect-class questions → §4.3; overdue calibration → §4.6. The Lead never writes an acceptance from inside a
  worker (§2.4 (i)); critic/designer verdicts reach it through the worker's handoff file.
- **builder rank (Sonnet coordinator)** — coordination, dispatches; accepts scout; a builder diff only with critic
  input; critic/designer work → `basis: queued-to-lead` (cleared by §3.5); Lead-class work → `docs/tasks/lead-queue.md`.
- Below builder rank — no coordination.

### 5.3 Lead degradation and the Opus outage

1. Trigger: the Lead model (Opus) refuses / is unavailable, or the operator switches to a model ranked below lead →
   drop to builder rank (Sonnet) + `lead_degraded`. ONE step down now (Opus → Sonnet); the old «upper-mid, then mid»
   two-step disappears.
2. **An Opus outage removes Lead, critic and designer at once (M1).** The Sonnet coordinator may accept a builder
   diff ONLY with critic input, and `queued-to-lead` is illegal for builder work (P13 `:780`). The move: builder diffs
   finished during the outage WAIT — each gets one line in `docs/tasks/lead-queue.md` («ждёт критика: <task_id>,
   <ветка>») and no `accepted`; critic/designer dispatches are not launched; recon and builder work under accepted
   specs continue. On return the Lead runs the critic and accepts. (F22 may add a Fable stand-in by the owner's word.)
3. **Fable unavailable / refusing is NOT a Lead degradation**: no `lead_degraded`; Architect queue items wait; the
   owner is told once. Invariant: *the Architect's absence never stops Lead work*.
4. EXIT (rule «tier verification», point b): a rise from builder rank to lead OR architect rank proves a window →
   retro `lead_degraded` + window acceptance + `lead_restored`, as today. A switch Opus → Fable or Fable → Opus is
   NOT a window (both ≥ lead): no event.
5. While degraded: unchanged list (no statuses/gates; decision-log entries queued to the Lead).

### 5.4 Tier verification at entry — the MODEL line

`MODEL: <id> -> function <f> (declared by harness, not measured; lead = <lead binding>, architect = <architect
binding | unbound>)`, `<f>` and its note from `function_of_session` (one road, B2). Cases (each a row of
`test_session_context.py`; the matching itself is tested in `test_tier_ladder.py`):
- id matches a binding exactly → `<f>` = the highest function bound (`claude-opus-5-5` → `lead`; `claude-fable-5-1`
  → `architect`; `claude-sonnet-5-5` → `builder`).
- **family bound, id differs** (the live case, P37) → that family's highest function with the note
  `(family match: <binding>)`: `claude-fable-5-2` against `claude-fable-5-1` → `architect (family match:
  claude-fable-5-1)`; prints the ARCHITECT line.
- Claude family bound to nothing, stronger than lead (Fable with no architect key) → `above lead (no architect
  binding)`; acts as full Lead; no ARCHITECT line.
- Claude family bound to nothing, weaker than lead → `<nearest weaker function> (unbound family)`, or `below builder`;
  below-lead rules.
- **No binding matches and no family is recognised** (a new model name, a non-Claude id) → `function none (matches
  no binding in delegation.config.yaml) -- coordinate under the below-lead rules until verified`. Invariant: *an
  unrecognised model never reads as Lead*. The validator FAILS its `by` (enum check) and the tier gate refuses its
  `tier:` (case d) — the same direction everywhere.
- No model in the payload → unchanged fallback (`MODEL: not provided by hook input -- verify tier yourself`).
- Config unreadable → the line appends `(config unreadable: default bindings)`.

**Settings pin (F15 (a), owner's word).** When `.claude/settings.json` `model` differs (exact string) from the lead
binding, SessionStart prints one line `WARN: .claude/settings.json model <x> != lead binding <y> -- new sessions open
on <x>; align one of them`. Edges: settings absent or without `model` → no line (nothing to compare); settings
unparsable → `WARN: .claude/settings.json unreadable (<reason>)`; config unreadable → no pin line (the MODEL line
already says so). The line is placed after the ARCHITECT line slot and before the rest, so the 25-line cut cannot
drop it.

### 5.5 Calibration checks 5, 6, 18, 20, and new check 49 (stream F)

- Check 5: «Lead-tier activity on a model below the top tier» → «Lead-tier activity on a main chain ranked below
  lead (`rank_of_model`), outside a declared window». An Architect (Fable) main chain doing Lead work is NOT
  degradation.
- Check 6: the acceptor's tier = `rank_of_model` of the main-chain model at the event; «"queued for the full Lead"» →
  «queued for the Lead». ADDED items: (i) the validator's `INDEPENDENT CONTEXT` WARNs of the window
  (`python -B tools/journal_validator.py --all --base <sha at the window's start>`), each a finding unless the notes
  name the worker; (ii) every `accepted` of critic/designer work in the window has an earlier `delegated` of that agent
  with `worker_ref: agent:<id>` whose transcript is a sidechain (check 7's reader); (iii) queued-to-lead lines of the
  window without a later lead-ranked `accepted` (F23 (a)).
- Check 18 / savings: F11 (a) — the counterfactual model is the lead binding, wording «coordinator model».
- Check 20 (FG7-16): (b) loses «`tools/journal_validator.py` still accepts the value (residual node R-1 of t-013),
  so (b) is its only detector» → «the validator refuses the value (FG7-16); (b) watches for lines that bypassed it».
- **New check 49 — Architect tier** (next free number, P48; if a parallel stream takes 49 first, the next free one —
  the title is the key): (a) every mechanism commit since the previous `reviewed_through` appears in the review
  record; (b) the gap between consecutive `calibrated` lines carrying `reviewed_through` — over 7 days is a finding
  against the cadence, listed with the SessionStart overdue days; (c) every `escalated` with `agent: architect` of the
  window has an architect-queue item and vice versa (the §4.5 step 4 command); (d) refusals by the stream-E rule in
  the window (hook stderr is not logged — so: `accepted`/`rejected` lines whose session transcript shows a sidechain
  author are the leak). Detector of this check's own leak: a `calibrated` line after stream L without
  `reviewed_through`.

---

## §6 Files to change, with readers

Reader search method (designer rule 3): the Grep tool over `tools/`, `.githooks/`, and `.claude/` restricted to
`.claude/settings.json`, `.claude/agents/`, `.claude/skills/` (an unrestricted `.claude/` search drowns in
`.claude/worktrees/*` copies — other workers' trees, not readers). Controls: `.githooks` searched for
`mechanism_gate|journal_validator|session_context` → 3 hits (`commit-msg:6`, `pre-commit:8`, `pre-merge-commit:18`),
so a 0 there is real.

| file | change | readers (command → hits) and their fate |
|---|---|---|
| `delegation.config.yaml` | lead → `claude-opus-5-5`; new `architect:` rung → `claude-fable-5-1` (F1); comments: drop onboarding-skill references (P4, F14), say «ranks: `tools/tier_ladder.py`» | Grep `delegation\.config` `tools/` → 29 hits / 12 files (t-902 agrees): `mechanism_gate.py` (6 — A), `savings_report.py` (5 — A), `test_savings_report.py` (4 — A), `test_mechanism_gate.py` (1 — A), `claim_control_gate.py` (3 — scope list, unchanged), `test_claim_control_gate.py` (3 — unchanged), `dispatch_gate.py` (1, docstring `:92` — unchanged), `agents_md.py` (1, text `:257` — unchanged), `install_parity_anchors.json` (2, path unit — unchanged), `test_install_parity.py` (1 — unchanged), `tests/test_role_carriers_one_owner.py` (1 — re-run in F), `fixtures/host_pre_delivery_CLAUDE.md` (1 — frozen). `.githooks` → 0. `.claude/skills/onboarding/SKILL.md` (deleted, D6), `critic-exam-gen/SKILL.md` (3 — F), `scout-exam-gen/SKILL.md` (2 — unchanged). New readers: `tier_ladder.py` (A) — the ONE parser; validator, session_context via the home |
| `tools/tier_ladder.py` + `tools/test_tier_ladder.py` (new) | the home (§2) | importers after the change: mechanism_gate, savings_report (via wrappers), journal_validator, session_context, tier_echo, dispatch_gate, journal_hooks, token_usage_stats; agents_md (AST); `MECHANISM_PREFIXES` entry; closure test in `test_mechanism_gate.py` (A) |
| `tools/mechanism_gate.py` | ladder → home; `architect` rung; `--list --since`; queue-note text → `docs/tasks/lead-queue.md`; `MECHANISM_PREFIXES` += config + home | Grep `KNOWN_TIER_WORDS\|LEAD_FAMILIES\|_FAMILY_NAMES\|resolve_lead_binding\|lead_family\(\|model_tier\(\|_MODEL_TIER_SUBSTRINGS` `tools/` → 58 hits / 9 files: `mechanism_gate.py` 21, `test_mechanism_gate.py` 12 (A), `savings_report.py` 4 (A), `session_context.py` 4, `test_session_context.py` 5 (C), `dispatch_gate.py` 4 (D), `journal_echo.py` 3 (unchanged code), `tier_echo.py` 3 (D), `test_journal_echo.py` 2 (unchanged). Grep `duplicate_model_id\|ROLE_RANKS\|"reserve"\|reserve:` → `mechanism_gate.py` 8, `test_mechanism_gate.py` 15 (A). `test_mechanism_gate.py:1085` `assert "Lead queue" in reason` (A — keep the words). `.githooks/commit-msg:6` runs it (unchanged hook). `test_mechanism_gate_md.py` (A, re-run). Parallel spec boot-by-topic also touches this file (§7.0) |
| `tools/journal_validator.py` | matrix by ranks (no legacy table); judge refused (FG7-16); `agent: architect` no-matrix; `escalated` agent=architect may open a task (F6); `calibrated.reviewed_through` shape (F9); F5 WARN; independent-context WARN (B4); config read from the validated repo's root | Grep `TIER_ORDER\|AGENT_TIER\|QUEUED_TO_LEAD_AGENTS` `tools/` → 35 hits / 4 files: `journal_validator.py` 20, `test_journal_validator.py` 8 (B), `agents_md.py` 4, `test_agents_md.py` 3 (B). Grep `judge` in `test_journal_validator.py` → 58 (B: the judge-legal rows flip to refused). Text readers: `PROCESS/LEAD_RANKING_EXAM.md:29` (F), CLAUDE.md Routing-log `by` paragraph (L), `AGENTS.md:885` copy (L regen), check 20 (F). Hooks: `.githooks/pre-commit:8`, `pre-merge-commit:18` (unchanged). Importers: `journal_echo.py` re-validates newest lines (unchanged code); `journal_write.py` validates before the write (B); `journal_hooks.py` writes through `journal_write.write_event` (unchanged; its tests use `by: fable` in tmp repos without a config → DEFAULT_BINDINGS → as today). FG7-22 (batch 7, untaken) also owns this file — it runs after stream B (§7.0) |
| `tools/journal_write.py` + `tools/test_journal_write.py` | `escalate`: `--task` optional when `--agent architect` (the writer issues the id: `NEW_TASK_EVENTS` logic); `calibrated --reviewed-through <sha>` → typed field `reviewed_through` | Grep `reviewed_through\|NEW_TASK_EVENTS` `tools/` → 2 hits, both `journal_write.py` (P46). Callers of the CLI: the coordinator; ARCHITECT_START step 8 (F); `hygiene_gate.py` names the writer in its journal message `:74` (unchanged) and recognises its calls (E) |
| `tools/hygiene_gate.py` + `tools/test_hygiene_gate.py` | subagent `accept`/`reject` refusal in `decide` (payload `agent_id`), NOT inside `_collect_signals` | Grep `hygiene_gate` `tools/` → 101 hits / 27 files; the ones that read code or text of the module: `permission_audit.py:110,469` imports `_collect_signals` (UNCHANGED: the new check lives outside that pure walk, so the audit's classification is unchanged), `test_warn_messages.py:95,494,539-540` (UNCHANGED: the refusal uses the existing `Command hygiene: ` wrapper), `warn_layers.json:197-201` (UNCHANGED, same literal), `hook_liveness_probe.py:63,316,909,1391` (UNCHANGED: no hook added; its note «MSG_JOURNAL_BLOCK are plain English» binds the new message too — ASCII English), `mechanism_gate.py:69,235` (prefix list — unchanged), `test_p4_stdin_deadline.py` (4, stdin helper — unchanged), `dup-baseline.json` (2 — the clone ratchet; a new helper must not duplicate `dod_track._is_journal_writer_call` beyond the baseline → E's edges), the rest name the hook in prose or lists (unchanged). `.githooks` → 0. `.claude/settings.json:38` wires it (unchanged) |
| `tools/session_context.py` | MODEL line by function; ARCHITECT line; settings pin; overdue suffix on `Last calibration` | Grep `Lead tier = fable\|Lead\(top\)\|critic-tier` → 13 hits / 3 files: `session_context.py` 3, `test_session_context.py` 8 (C), `test_journal_validator.py` 2 (comments `:645`, `:706` — unchanged). `last_calibration_line` (`:606`) is read only inside the module. `.claude/settings.json` SessionStart wiring — unchanged. Parallel spec boot-by-topic also touches it (§7.0) |
| `tools/tier_echo.py`, `tools/dispatch_gate.py`, `tools/journal_hooks.py`, `tools/token_usage_stats.py` | read `FAMILIES`/`family_of` (incl. `FAMILY_ORDER`, M7) | their tests `test_tier_echo.py`, `test_journal_echo*.py`, `test_dispatch_gate.py`, `test_journal_hooks.py`, `test_token_usage_stats.py` — stream D, green with no edit (same words, same order; the door text has no pin, §2.3) |
| `tools/savings_report.py` | F11 (a); `_UNBOUND` → `lead_binding()` | `test_savings_report.py` (A); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:535` (F) |
| `tools/agents_md.py` | `tier_words` reads the home | `test_agents_md.py:30,309-322` pins (B); `.githooks/pre-commit` runs `agents_md.py --check` — AGENTS.md is regenerated in the SAME commit as any CLAUDE.md edit (L) |
| `.claude/settings.json` | `"model"` → `claude-opus-5-5` (F15 (a)) | no tool reads the key today (P18); the SessionStart pin (C) becomes its reader. Hook-count pins (`test_hook_liveness_probe.py`) unaffected: no hook added |
| `CLAUDE.md` | §7.0 lists the sections | readers: `AGENTS.md` (generated copy — regen), `tools/install_parity_anchors.json:8,32` (anchors «Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)», «5. Flat delegation (flat delegation rule):» — KEEP those heading texts verbatim), `tools/fixtures/host_pre_delivery_CLAUDE.md` (frozen), the parallel boot-by-topic spec (re-measures after L, §7.0) |
| `PROJECT.md` | one line in «Как разрабатывается новая идея владельца» (m2) | every session (import); the boot-by-topic spec moves PROJECT.md sections after L (§7.0) |
| `DECISIONS.md` | new D-nnnn: Lead → Opus, Architect → Fable, matrix by function, the subagent refusal, the Opus exam deferred to FG7-54 by the owner's word (D7) recorded as the `exam.on_failure` informed pass (P4 `:98-106`); D-0003 gets «superseded by D-nnnn» | `MECHANISM_PREFIXES` (mechanism commit), calibration, every session's boot |
| `docs/TWO_VOCABULARIES.md` | Lead row → Opus; new Architect row | `tools/tests/test_role_carriers_one_owner.py:73` (re-run, F) |
| `docs/SIBLING_MAP.md` | `:519`, `:522` rows deleted (D6); `:655-661` «Lead Queue» → `docs/tasks/lead-queue.md`; axis 1 role list unchanged (no architect role FILE, C7), axis 1 table gains a «ladder home `tools/tier_ladder.py`» row; axis 2 Lead-exam row note «Opus candidate, FG7-54» | `tools/mechanism_gate.py` reads axis headings as gate keys (headings NOT renamed → no key change); `install_parity_anchors.json:524-528` path unit (unchanged); boot-by-topic spec (§7.0) |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | header: run by an Architect session (F10); checks 5, 6, 18, 20 (§5.5); new check 49 | calibration sessions; `test_calibration_counts.py` (re-run in F; expected unchanged since `by` vocabulary is unchanged) |
| `PROCESS/LEAD_RANKING_EXAM.md` | `:3-4` purpose (M3), `:29-31` pointer + «Fable judges an Opus candidate» | FG7-54 (the П3 run) |
| `PROCESS/PATCH_PROTOCOL.md` | `:22-23` drop «the onboarding skill's Upgrade mode, step 7»; keep the install-parity duty in its own words (F14) | Lead at patching |
| `PROCESS/ARCHITECT_START.md` | new (§4.5) | SessionStart pointer only |
| `.claude/agents/critic.md` | `:52-57` «below the top tier» → «below the Lead rank»; rule 10 (`:58-61`) unchanged (critic binding unchanged, D1) | harness; `agents_md.py` roles table (frontmatter unchanged); boot-by-topic spec S3 (§7.0) |
| `.claude/skills/critic-exam-gen/SKILL.md` | `:163`, `:182` references to the onboarding skill (F14) | harness (skill index) |
| `.claude/skills/onboarding/`, `.claude/skills/next-task/` | DELETED (D6) | readers of the names: `docs/SIBLING_MAP.md:519,522` (F), `PROCESS/PATCH_PROTOCOL.md:23` (F), `docs/ADOPTION_LEDGER.md` (F), `delegation.config.yaml:34,39,95-96` (L), `critic-exam-gen/SKILL.md:163,182` (F); `tools/test_wiring_check.py:487-526` — synthetic repo, UNCHANGED; `install_parity_anchors.json:657-661` — dir unit, UNCHANGED; `AGENTS.md` — does not list skills, UNCHANGED; `.claude/settings.json` names no skill (P54); history files UNCHANGED |
| `docs/ADOPTION_LEDGER.md` | onboarding-skill references → «retired 16.11.2026 (D-nnnn)» (F14) | a human record; no tool reader |
| `docs/tasks/lead-queue-fable.md` → `docs/tasks/lead-queue.md`; new `docs/tasks/architect-queue.md` | F8 (a) | after: `session_context.py` counts architect-queue items (C); `mechanism_gate.py` note (A); `docs/SIBLING_MAP.md:659` (F) |
| `plans/piles/forge/batch-7-vhodyashchie-4.md` | FG7-33 «снят: заменён …»; FG7-14 «зависит от потока A спеки 20261116-architect-tier» (F12); FG7-16 «поглощён потоком B спеки 20261116-architect-tier»; FG7-22 «после потока B (общий файл journal_validator.py)»; FG7-54 unchanged (referenced, D7) | `tools/piles.py check` reads the batch (untaken → editable, P33) |

---

## §7 Phases and parallel streams

### 7.0 The rule of this landing, order, and the parallel specs

- **Who commits (B1).** Every commit of streams A-F and the stream-L commit is made by a **FABLE** session (this
  Lead session is Fable and runs the landing) with the line `tier: fable`. Reason: until L flips the config, the tier
  gate refuses `tier: opus` (P7, critic probe), and every owned file of A-E and the `PROCESS/` and
  `docs/SIBLING_MAP.md` files of F are mechanism paths; the concept is the one `mechanism_gate.py:840-841` already
  states («the transitional commit re-binding Lead is committed BY a session of the old, higher tier»). The gate
  reads the WORKING-TREE config (`CONFIG_PATH`, `:206`): `tier: fable` passes both before and after the flip, so the
  L commit itself passes. After L, the Opus Lead commits with `tier: opus` (D3). This is the stated exception to
  «mechanism commits are made by the Opus Lead» (§4.1).
- **Transitional world.** Until stream L flips `delegation.config.yaml`, every gate behaves exactly as today (§3.4,
  pair check). The flip is ONE commit (L), made by Fable, carrying the config change; no `LADDER_FROM` or cutover
  survives (F18 (b)).
- **Order inside this spec.** **A** first (the home; everything imports it) → **B, C, D, E, F** in parallel (disjoint
  owns) → **L** LAST. Builders work in their own worktrees; placement on the live path is the coordinator's merge
  (`tools/wave.py merge`) after the ONE topic critic (R13-g) — that satisfies the enforcement-file review rule for the
  self-activating files (`session_context.py`, `hygiene_gate.py`, `dispatch_gate.py`, `journal_hooks.py`,
  `tier_echo.py`, `journal_validator.py`, `mechanism_gate.py`, `tier_ladder.py`).
- **Against the parallel specs (M10).** `очередь: architect-tier → boot-by-topic`. The boot-by-topic spec already
  waits for this one (P49: Phase 0, E17). Files both specs touch: `tools/session_context.py`,
  `tools/test_session_context.py` (C), `tools/mechanism_gate.py` (A), `docs/SIBLING_MAP.md`,
  `.claude/agents/critic.md` (F), `CLAUDE.md`, `PROJECT.md` (L). Stream L rewrites these CLAUDE.md sections, which
  the boot-by-topic spec re-measures (sizes, headings for its TOC) after L lands: «## Tiers» (+ Architect line; Lead
  (Opus)); «## Routing rules» rule 6 (escalation above Opus, §4.7); «## Routing log» — the `by` paragraph (`TIER_ORDER`
  → `tools/tier_ladder.py` `FAMILIES`) and the SHAPES rows `escalated` and `calibrated` (new row); «## Role ≠ tier»
  (§5.1-5.2, the Lead's overdue move); «## Lead degradation» (§5.3). Headings are NOT renamed. PROJECT.md: one line in
  «Как разрабатывается новая идея владельца». The reciprocal `очередь:` line in the boot-by-topic spec and in the
  batch files is the Lead's edit (outside this file). The third parallel spec (`20261116-spec-facts-by-code-spec.md`)
  was not read in this round: the Lead checks its owns against §7 before launch.

Witness scope: these owns are outside the package → `scenario_walk.py --witness-for` has no row; the witness is the
test file that judges each path, named per stream (CLAUDE.md rule 4). No CI wait, no mutations (PROJECT.md
«Командная работа» п. 13). New test cases are ROWS of the existing tables; the one new test file is
`tools/test_tier_ladder.py` (F2 (a), the owner's word 17.11.2026).

### Stream A — the ladder home + tier gate + savings

given: this spec §0, §2, §3.4 (tier-gate part), §4.5 step 5; `tools/mechanism_gate.py`; `tools/savings_report.py`; `delegation.config.yaml`; `docs/TESTING.md`
owns:
C:/QAFactory/forge-repo/tools/tier_ladder.py
C:/QAFactory/forge-repo/tools/test_tier_ladder.py
C:/QAFactory/forge-repo/tools/mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate_md.py
C:/QAFactory/forge-repo/tools/savings_report.py
C:/QAFactory/forge-repo/tools/test_savings_report.py
non-goals: no edit of `delegation.config.yaml`, `.claude/settings.json`, CLAUDE.md (stream L); no validator/session_context change; no commit (the Fable coordinator commits, §7.0)
handoff: diff + witness + the four questions (rule 10) block for the mechanism commit
edges: items A1-A6 below; §2.2 adversarial rows; §2.4 all bullets; config without `architect` key and with it give identical results for `tier: fable`; `--list --since` with a bad value → exit 1 naming the form (as `--audit`, `:1082`); empty window → «0 commits», exit 0; `test_mechanism_gate.py:1085` keeps «Lead queue»
DoD: `python -m pytest tools/test_tier_ladder.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q` green with the rows of A1-A6
siblings: axis 34 (one road for the ladder), axis 1 (binding ↔ policy)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

Items (file → function → behaviour → test row):
- A1 `tools/tier_ladder.py` → `FAMILIES`, `ALIASES`, `FUNCTION_RANKS`, `COORDINATION_FUNCTIONS`, `DEFAULT_BINDINGS`,
  `family_of`, `bindings`, `effective_bindings`, `rank_of_function`, `rank_of_model`, `lead_binding`,
  `architect_binding`, `function_of_session` as §2.1-2.2; stdlib-only import, `yaml` imported inside `bindings()`.
  Rows in `test_tier_ladder.py`: every adversarial input of §2.2; config fixtures TODAY (lead fable, critic opus,
  builder/scout sonnet) and AFTER (lead opus, architect fable, critic opus); `claude-fable-5-2` vs a
  `claude-fable-5-1` binding → `("architect", "family match: claude-fable-5-1")` (B2); 64 KB / 64 KB + 1; alias bomb;
  `roles.reserve` uncommented → not read + note; pyyaml import failure (monkeypatched) → DEFAULT_BINDINGS + note; a
  row asserting that importing `tier_ladder` does not import `yaml` (`"yaml" not in sys.modules` after a fresh import
  in a subprocess).
- A2 `tools/mechanism_gate.py` → delete `ROLE_RANKS`, `LEAD_FAMILIES`, `build_role_ladder`, `_resolve_ladder_rank`;
  `tier_declared_ok(declared, binding, cfg)` = `rank_of_model(declared, cfg) >= FUNCTION_RANKS["lead"]` (exact id
  `declared == binding` stays a first pass). Rows: config TODAY → `tier: fable` ok, `tier: claude-fable-5-2` ok,
  `tier: opus` refused, `tier: sonnet` refused; config AFTER → `tier: opus` ok, `tier: claude-opus-5-5` ok,
  `tier: fable` ok, `tier: sonnet` refused; duplicate id lead=critic=opus → rank lead; architect key absent/present
  parity. Existing `duplicate_model_id` and `reserve` rows are rewritten to `architect` (the builder lists each changed
  row in the handoff).
- A3 `mechanism_gate.py` `resolve_lead_binding`, `lead_family` → thin wrappers over the home; `savings_report.py`
  `_UNBOUND`/`top_tier_model` → `lead_binding()` (F11 (a); the label «coordinator model»). Rows in
  `test_savings_report.py`: config AFTER → counterfactual priced at Opus; config absent → the existing PricesError path
  unchanged? NO — absent config gives `DEFAULT_BINDINGS` lead = fable, so the counterfactual is Fable as today (row).
- A4 `MECHANISM_PREFIXES` += `"delegation.config.yaml"` (comment §2.5) and `"tools/tier_ladder.py"`. Row: the closure
  test covers the home; a commit staging only the config is a mechanism commit.
- A5 `_tier_queue_note()` → «… it goes into the Lead queue docs/tasks/lead-queue.md …» (keeps «Lead queue»). Row:
  the existing `:1085` assertion + the path.
- A6 `--list --since <date|sha>` → one line per commit touching `mechanism_paths()` (first parent for merges):
  `<sha> <committer date> <tier: values or "-"> <subject>` then indented paths. Rows: a fixture repo with two
  mechanism commits and one non-mechanism → 2 lines; bad value → exit 1 with the form; empty → «0 commits», exit 0.

### Stream B — journal gate and writer by function

given: §3 whole, §2.2, §2.4 (ii), §4.3, §4.5 step 8; `tools/journal_validator.py`; `tools/journal_write.py`; `tools/agents_md.py`; `plans/piles/forge/findings/20261111-basis-judge-razreshen-kodom-pri-neispolzuemom-sude.md`
owns:
C:/QAFactory/forge-repo/tools/journal_validator.py
C:/QAFactory/forge-repo/tools/test_journal_validator.py
C:/QAFactory/forge-repo/tools/journal_write.py
C:/QAFactory/forge-repo/tools/test_journal_write.py
C:/QAFactory/forge-repo/tools/agents_md.py
C:/QAFactory/forge-repo/tools/test_agents_md.py
non-goals: no rewrite of any journal line; no change to the `by` vocabulary (F4-A); no legacy table or `LADDER_FROM` (F18 (b)); no CLAUDE.md edit (L); no commit
handoff: diff + witness
edges: items B1-B7 below; config read from the root of the repo being validated (the `--repo`/root the validator already uses), absent there → DEFAULT_BINDINGS (existing tmp-repo tests stay green with no config); `by: "claude-opus-5-5"` → FAIL; `by: "lead"` → FAIL with door (F4-A); an unreadable config → the stderr WARN once per run, never a FAIL
DoD: `python -m pytest tools/test_journal_validator.py tools/test_journal_write.py tools/test_agents_md.py -q` green with the rows of B1-B7; `python -B tools/agents_md.py --check` clean
siblings: axis 1 (journal ↔ policy)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

Items:
- B1 `journal_validator.py` `_matrix_d0058_violation` → ranks from the home in the §3.1 order; delete `TIER_ORDER`,
  `AGENT_TIER`. Rows: every cell of §3.1 on config AFTER; the six transitional pairs of §3.4 on config TODAY (each
  must equal today's verdict).
- B2 (FG7-16) branch (1) → the refusal text of §3.1 for `basis: "judge"` on any agent/category/by. Rows: `"judge"` →
  refused (scout/implementation, builder/recon, critic, at by fable); `"critic"` and `"queued-to-lead"` → as before.
  The existing judge-legal rows (Grep `judge` → 58 hits) flip to refused; rows that test only the category/agent
  narrowing are removed (their branch no longer exists) — the builder lists them in the handoff.
- B3 F5 WARN «queued to itself» (§3.2). Row: `by: opus, agent: critic, basis: queued-to-lead` on config AFTER → OK +
  WARN; the same on config TODAY → OK, no WARN.
- B4 independent-context WARN (§2.4 (ii)): appended `accepted`, `agent ∈ {critic, designer}`, `rank(by) ≥ lead`, no
  earlier `delegated` of that agent on that task whose `worker_ref` starts `agent:` (`task_worker_refs` +
  `delegated_agents`, `:516-547`). Rows: with `agent:abc` delegated → no WARN; with only `cli:…`/`retro:…` → WARN; no
  delegated of that agent (another agent's only) → WARN; config TODAY with `by: opus` (rank critic) → no WARN (the
  matrix governs).
- B5 (F6) `escalated` with `agent: "architect"` and an unseen `task_id` → legal under the novelty rule (9a''); any
  other agent → still the `:1287-1297` violation. Rows: both; an architect `escalated` with a non-canonical id →
  the novelty violation. `journal_write.py` `escalate` → `--task` optional iff `--agent architect` (the writer issues
  the id as for `NEW_TASK_EVENTS`); without `--task` and another agent → refused naming `--task`. Rows in
  `test_journal_write.py`.
- B6 (F9) `calibrated` optional field `reviewed_through`: a git sha `^[0-9a-f]{7,40}\Z`; another event carrying it, or
  a bad shape → violation naming the form. `journal_write.py calibrated --reviewed-through <sha>`. Rows: good sha,
  uppercase / 6 chars / non-hex → violation; field on `accepted` → violation; CLI writes the field.
- B7 `agents_md.py` `tier_words` → AST of `tools/tier_ladder.py` `FAMILIES`. Rows: `test_agents_md.py:30,309-322`
  re-pointed; `--check` clean.

### Stream C — SessionStart

given: §4.4, §4.6 (weekly trigger), §5.4; `tools/session_context.py`; `tools/tier_ladder.py` (from A)
owns:
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/test_session_context.py
non-goals: no new SessionStart hook; no reading of `PROCESS/ARCHITECT_START.md` content (pointer only); no open-dispatch change for `escalated` (§4.5 step 4 uses a command); no commit
handoff: diff + witness
edges: items C1-C4; ARCHITECT line and pin line survive the 25-line cut with 30 candidate lines; queue absent/unreadable/0 open; config unreadable
DoD: `python -m pytest tools/test_session_context.py -q` green with the rows of C1-C4
siblings: axis 1
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

Items:
- C1 `model_line` → §5.4 text from `function_of_session`; delete `_MODEL_TIER_SUBSTRINGS`, `model_tier`. Rows: the
  seven cases of §5.4 incl. `claude-fable-5-2` vs `claude-fable-5-1` → `architect (family match: claude-fable-5-1)`.
- C2 ARCHITECT line (§4.4) right after MODEL when the function is `architect`. Rows: fable-5-2 session → printed;
  opus session → absent; no architect key + fable → absent; queue absent / unreadable / 0 / 3 open.
- C3 settings pin (§5.4). Rows: equal → no line; differ → WARN; settings without `model` → no line; unparsable →
  WARN unreadable.
- C4 `last_calibration_line(events, now, function=None)` overdue suffix (§4.6). Rows: 8 days non-architect → Lead
  suffix; 8 days architect → Architect suffix; exactly 7 → none; NONE → suffix; unparsable ts → none.

### Stream D — family readers

given: §2.3 rows for tier_echo, journal_echo, dispatch_gate, journal_hooks, token_usage_stats; `tools/tier_ladder.py` (from A)
owns:
C:/QAFactory/forge-repo/tools/tier_echo.py
C:/QAFactory/forge-repo/tools/dispatch_gate.py
C:/QAFactory/forge-repo/tools/journal_hooks.py
C:/QAFactory/forge-repo/tools/token_usage_stats.py
non-goals: `journal_echo.py` code unchanged (reads via tier_echo); FG7-14 (label carries role) NOT done here; no behaviour change; no commit
handoff: diff + witness
edges: `tier_echo` now imports the leaf `tier_ladder` (stdlib-only at import, so no pyyaml on the journal_echo hook path; m3); order-sensitive pin `test_extract_declared_word_picks_first_known_tier_words_order` green; «mythos» still maps to Fable in token stats; `FAMILY_ORDER` value unchanged; `dispatch_gate.py` is shared with FG7-14 → function list of this stream: `_model_family`, `_FAMILY_NAMES` and the docstring lines `:1047-1050` only (PROJECT.md «Командная работа» п. 3)
DoD: `python -m pytest tools/test_tier_echo.py tools/test_journal_echo.py tools/test_dispatch_gate.py tools/test_journal_hooks.py tools/test_token_usage_stats.py -q` green with no test edit
siblings: axis 14 (transcript readers: tier_echo/journal_echo), axis 34
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

Items: D1 `tier_echo.KNOWN_TIER_WORDS = tier_ladder.FAMILIES`; D2 `dispatch_gate._FAMILY_NAMES`/`_model_family` →
`FAMILIES`/`family_of` (strongest-first where the old tuple was: reversed); D3 `journal_hooks.py:210` door text from
`FAMILIES`; D4 `token_usage_stats.family()` → `family_of` + local capitalisation, `FAMILY_ORDER` derived (M7). Test
rows: the existing tables (no edit) are the witness that nothing changed.

### Stream E — no acceptance from a worker (B4 (i))

given: §2.4 (lead/critic/designer bullet); `tools/hygiene_gate.py`; `tools/handoff_gate.py:1-40` (the agent_id rule); `tools/dod_track.py:227-242` (`_is_journal_writer_call`, the existing recogniser of writer calls)
owns:
C:/QAFactory/forge-repo/tools/hygiene_gate.py
C:/QAFactory/forge-repo/tools/test_hygiene_gate.py
non-goals: no change to `_collect_signals` (read by `permission_audit.py:469`); no change to the fail-open posture of `decide`; no change to `journal_write.py` (stream B); no commit
handoff: diff + witness
edges: refusal only when the payload carries a non-empty string `agent_id` AND some python program invocation in the command (any `;`/`&&`/`|`/subshell segment, not only the first) is `tools/journal_write.py` (relative, absolute, quoted, backslashes) with first positional `accept` or `reject`; main thread (no/empty/null `agent_id`) → never refused by this rule; other subcommands (`returned`, `skip`, …) → not refused; a command merely mentioning the text (`grep "journal_write.py accept" f`) → not refused; refusal = the existing deny shape with the `Command hygiene: ` prefix and the §2.4 text (ASCII English); the recogniser reuses or mirrors `dod_track._PYTHON_PROGRAM_RE` forms (`py -3`, `-X utf8`, `-W ignore`, quoted path) without growing the clone ratchet past `tools/dup-baseline.json` (prefer an import of a public name from `dod_track`, or a scan of ALL matches with the same regex — the builder states which)
DoD: `python -m pytest tools/test_hygiene_gate.py tools/test_warn_messages.py tools/test_permission_audit.py -q` green, with table rows in `test_hygiene_gate.py`: subagent + `python -B tools/journal_write.py accept …` → deny; + `reject` → deny; + `py -3 tools/journal_write.py accept` → deny; + `python -X utf8 "C:/x y/tools/journal_write.py" accept` → deny; + `python -m pytest tools/x.py -q; python -B tools/journal_write.py accept` → deny; + `( cd C:/wt && python -B C:/wt/tools/journal_write.py reject … )` → deny; + PowerShell `& python tools/journal_write.py accept` → deny; + `returned` → pass; + `grep "journal_write.py accept" f` → pass; main thread + `accept` → pass; `agent_id: ""` / `null` → pass
siblings: axis 1 (policy ↔ code: «a worker never accepts»)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

### Stream F — rule texts outside CLAUDE.md, deletions

given: §4.5, §4.6, §5.5, §6 rows for these files; F7, F8, F10, F11, F14 (decided)
owns:
C:/QAFactory/forge-repo/PROCESS/ARCHITECT_START.md
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/PROCESS/LEAD_RANKING_EXAM.md
C:/QAFactory/forge-repo/PROCESS/PATCH_PROTOCOL.md
C:/QAFactory/forge-repo/docs/TWO_VOCABULARIES.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/docs/ADOPTION_LEDGER.md
C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/skills/critic-exam-gen/SKILL.md
C:/QAFactory/forge-repo/.claude/skills/onboarding/
C:/QAFactory/forge-repo/.claude/skills/next-task/
C:/QAFactory/forge-repo/docs/tasks/lead-queue-fable.md
C:/QAFactory/forge-repo/docs/tasks/lead-queue.md
C:/QAFactory/forge-repo/docs/tasks/architect-queue.md
non-goals: CLAUDE.md, DECISIONS.md, PROJECT.md, config, settings, batch files (L); no SIBLING_MAP heading rename (gate keys); no new П3 node (FG7-54 exists, M3); no commit
handoff: diff + DOC-DISPATCH witness (rule 11: keys quoted from this spec before the run, script in full, a negative control)
edges: items F1-F6; critic.md is a role file → `PROCESS/CRITIC_EXAM.md` re-run duty (`critic.md:58-61`) — the edit changes no duty, only the rank's name: the handoff states «exam not re-run: wording only» for the commit message, or the Lead runs it; `test_role_carriers_one_owner.py` after the TWO_VOCABULARIES edit
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_calibration_counts.py -q` green + the key-presence run over the keys of F1-F6
siblings: axis 1, axis 2 (exam rows), axis 31 (role carriers)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261116-architect-tier-spec.md

Items (keys for the key-presence run in quotes):
- F1 `PROCESS/ARCHITECT_START.md` — the eight steps of §4.5, with the step-4 command and the step-8 command verbatim;
  keys «ARCHITECT_START», «reviewed-through», «"event":"escalated","agent":"architect"».
- F2 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` — header «run by an Architect session»; checks 5, 6 (+ items i-iii),
  18, 20 as §5.5; new check 49 «Architect tier». Keys «ranked below lead», «INDEPENDENT CONTEXT», «Architect tier»,
  «refuses the value (FG7-16)».
- F3 `PROCESS/LEAD_RANKING_EXAM.md` `:3-4` purpose → «distinguish a Lead candidate from the critic/builder
  functions»; `:29-31` → `FUNCTION_RANKS` in `tools/tier_ladder.py`, «Fable (Architect) judges an Opus candidate».
  Keys «FUNCTION_RANKS», «Architect».
- F4 `PROCESS/PATCH_PROTOCOL.md`, `docs/ADOPTION_LEDGER.md`, `critic-exam-gen/SKILL.md` — onboarding references
  retired (F14); the two skill folders deleted. Negative keys (must be ABSENT): «onboarding skill's Upgrade mode».
- F5 `docs/TWO_VOCABULARIES.md`, `docs/SIBLING_MAP.md`, `.claude/agents/critic.md` — as §6 rows. Keys «Architect»,
  «docs/tasks/lead-queue.md», «below the Lead rank».
- F6 queue files: `git mv` lead-queue-fable → lead-queue (retitled «Очередь для Lead», two open items kept), new
  `architect-queue.md` with the item form of §4.4 and no items. Keys «Очередь для Lead», «- [ ] <YYYY-MM-DD>».

### Stream L — Lead's own, ONE commit by a Fable session (after A-F are merged)

Edits: `delegation.config.yaml` (lead → `claude-opus-5-5`, `architect:` → `claude-fable-5-1`, comments per F14);
`.claude/settings.json` `"model": "claude-opus-5-5"` (F15 (a)); CLAUDE.md sections of §7.0 — «Tiers», rule 6,
«Routing log» (`by` paragraph; SHAPES row `escalated`: «`task_id` (must already exist earlier in the file, except
with `agent: architect`, which may open a task — §4.3), `model` (the model the work moves to; for `architect`, the
architect binding)»; new SHAPES row `calibrated`: «optional `reviewed_through` — the sha of the last mechanism commit
the Architect reviewed»), «Role ≠ tier», «Lead degradation»; `python -B tools/agents_md.py` regen in the same
commit; PROJECT.md one line (m2); `DECISIONS.md` (new D + D-0003 note); batch-7 rows (§6). Commit message: axis
block, `tier: fable`, «exam not re-run: wording only» for critic.md if F did not run it. Witness: the narrow sets of
A-E re-run on the merged tree + `python -B tools/journal_validator.py` + `python -B tools/agents_md.py --check` + one
probe of the tier gate on the flipped config (`tier: opus` → ok); BATCH CANON on CI per RUNBOOK §7. After the commit:
the Lead tells the other developers of the forge that the binding is global (§3.4).

---

## Forks (returned; recommendation marked; decided forks carry their decision)

- **F1 — key of the new rung.** DECIDED (a) `architect` (Lead, 17.11). (b) keep `reserve`; (c) read both.
- **F2 — where the home lives.** DECIDED (a) new leaf `tools/tier_ladder.py` + `tools/test_tier_ladder.py` (the
  owner's word 17.11.2026 «да»). From the review's option (c) (inside `tier_echo.py`) only the compatible part is
  taken: lazy `yaml` import and a stdlib-only leaf (§2.1); (c) itself is not taken — the owner chose (a).
- **F3 — rank order.** DECIDED (a) constant in the home.
- **F4 — what `by` holds.** DECIDED (A) model-family word.
- **F5 — `queued-to-lead` by a Lead-ranked acceptor.** DECIDED (a) WARN.
- **F6 — `escalated` to the Architect with no task yet.** DECIDED (a) may open a task (stream B; SHAPES row by L).
- **F7 — where the start checklist lives.** DECIDED (a) `PROCESS/ARCHITECT_START.md`.
- **F8 — queue carriers.** DECIDED (a) two files.
- **F9 — the review marker.** DECIDED (a) `calibrated.reviewed_through` (stream B; SHAPES row by L).
- **F10 — who runs the weekly calibration.** DECIDED (a) the Architect (owner's word 17.11.2026).
- **F11 — savings counterfactual.** DECIDED (a) lead binding, «coordinator model».
- **F12 — FG7-14.** DECIDED (a) independent, after stream A.
- **F14 — the deleted skill's procedures.** DECIDED (a) retire the references.
- **F15 — session default model + pin.** DECIDED (a) settings = lead binding, with the SessionStart WARN (owner's
  word 17.11.2026). The review's «postpone the pin» is not taken: the owner's «да» covered the pin.
- **F18 — legacy table for pre-switch lines.** DECIDED (b) no cutover (Lead, fix round 1, on t-902 M4; §3.4).
- **F21 — who writes the Architect's decision line.** DECIDED (a) the Architect itself (owner's word 17.11.2026).
- **F22 — NEW (intent, for the owner): may a Fable SUBAGENT stand in for an Opus role while Opus is down (or for a
  rule-6 escalation above Opus)?** (a) **[recommended]** no: D8 «never a subagent» covers any Fable subagent;
  during an outage builder diffs wait in `lead-queue.md` and escalations go to the architect queue (§4.7, §5.3);
  cost: work waits for Opus or for the owner's switch. (b) yes, a critic/designer dispatch with `model: fable` during
  a declared outage only, each with a `dispatch_skipped`-style note and a check-6 line; cost: Fable price per review,
  and the Architect's model becomes a worker model — the separation D8 drew blurs. Executable on (a) until her word.
- **F23 — NEW: the one road that clears a NEW `queued-to-lead` acceptance (M9).** (a) **[recommended]** a second
  `accepted` of the same task by a Lead-ranked `by` (typed, countable by check 6 (iii), legal today, P45). (b) a line
  in `docs/tasks/lead-queue.md` struck when cleared (prose carrier; calibration cannot count it from the journal).
  (c) the `lead_restored` window acceptance (only exists for degradation windows, not for the standard mid-tier mode).
  Executable on (a); it touches no code (the validator already allows it), only check 6 text (F) and CLAUDE.md
  «Role ≠ tier» builder-rank bullet (L).

## Small technical choices closed by the designer

- C1. `FAMILIES` order weakest → strongest (matches `TIER_ORDER` and `KNOWN_TIER_WORDS`, P12/P19); strongest-first
  readers reverse.
- C2. (Withdrawn in fix round 1: no `LADDER_FROM`, F18 (b).)
- C3. (Rewritten in fix round 1, M6.) A config over 64 KB, with any YAML alias, or unparsable is UNREADABLE: default
  bindings + one WARN; no refusal anywhere. 64 KB ≈ 40× the current file (107 lines).
- C4. `token_usage_stats` keeps its display capitalisation locally; recognition and order come from the home.
- C5. The ARCHITECT line sits directly after MODEL, the settings pin after it (both survive the 25-line cut).
- C6. `agent: "architect"` takes the same no-matrix branch as `agent: "lead"`.
- C7. No architect ROLE FILE in `.claude/agents/`: the Architect is a session, never a subagent (D8).
- C8. The B4 refusal lives in `hygiene_gate.decide` (it needs the payload), not in `_collect_signals` (pure on the
  command; read by `permission_audit`), and uses the existing deny wrapper — so `permission_audit`, `warn_layers.json`
  and `test_warn_messages.py` stay unchanged.
- C9. `DEFAULT_BINDINGS` equals today's config by family — the fallback for a broken config is today's behaviour
  through the same function, not a second table.
- C10. Checklist step 4 reads escalations with one `git grep` command (no new event, no SessionStart reader).
- C11. The B4 detector is two-layered: a validator WARN (write time, reads data the validator already harvests) and a
  check-6 item (calibration reads the WARNs); no FAIL — the meaning of «independent» stays the Architect's judgment.
- C12. `reviewed_through` shape: lowercase hex, 7-40 chars.

## Noticed in the brief and the review (reported, scope not widened)

- `tools/journal_write.py LEAD_ROWS` is not a family carrier (P20).
- `tools/install_parity_anchors.json` does not name the two skills (P31); `AGENTS.md` does not list skills (P32);
  `.claude/settings.json` names no skill (P54) — all unchanged by D6.
- FG7-16's finding names `BASIS_VALUES` as the carrier; the value is legalised by branch (1) instead (P44). Stream B
  fixes the branch; the finding file is not edited (history).
- The draft's §3.1 misquoted the branch order (judge before the unknown-`by` check); the code checks unknown-`by`
  first (P43). Corrected.
- FG7-22 (batch 7, untaken) also owns `tools/journal_validator.py`: it must run after stream B (row in batch 7 by L).
- The third parallel spec (`20261116-spec-facts-by-code-spec.md`) was not read: owns overlap unknown.
- Analog not touched: `PROCESS/DEPLOYMENT_ECONOMY_EXAM.md:238` «subagent on your top tier» — generic text, unchanged.

## Reading trail

Draft: `delegation.config.yaml` (whole); `tools/mechanism_gate.py:90-114, 208-283, 575-884, 945-994` + greps;
`tools/journal_validator.py:340-379, 645-810, 960-999, 1067-1106, 1280-1304, 2070-2098` + greps;
`tools/session_context.py:215-229, 975-1035, 2149-2228`; `tools/tier_echo.py:110-149`; `tools/dispatch_gate.py:190-209,
1020-1069`; `tools/journal_echo.py:630-669`; `tools/journal_hooks.py:195-219`; `tools/savings_report.py:55-94, 118-142`;
`tools/agents_md.py:190-234`; `tools/token_usage_stats.py:165-184`; `tools/journal_write.py:68-82`;
`tools/install_parity_anchors.json:495-669`; `.claude/settings.json:1-8`; `.claude/agents/critic.md:1-12, 48-61`;
`docs/TWO_VOCABULARIES.md:1-25`; `docs/SIBLING_MAP.md:24-68, 150-161, 505-534, 640-662`; `docs/TESTING.md:118-147`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:95-134`; `PROCESS/PATCH_PROTOCOL.md:18-27`; `docs/tasks/lead-queue-fable.md:1-40`;
`plans/piles/forge/batch-7-vhodyashchie-4.md:1-14`; greps on `DECISIONS.md`, `CURRENT_CONTEXT.md`, `BOOT.md`,
`PROJECT.md`, `DELEGATION_TABLE.md`, `AGENTS.md`, `PROCESS/LEAD_RANKING_EXAM.md`, `docs/ADOPTION_LEDGER.md`,
`.claude/skills/*`, `logs/journal/` counts.

Fix round 1 (t-911): the review `docs/tasks/specs/reviews/t-902-architect-tier-plan.md` (whole); `.claude/settings.json`
(whole); `delegation.config.yaml` (whole, + Grep `[&*]` → 0); `tools/handoff_gate.py:1-40` + Grep `agent_id`;
`tools/agent_budget.py:1-12` + Grep `agent_id`; `tools/hygiene_gate.py:1554-1688` + Grep `agent_id|journal_write|def
decide`; `tools/dod_track.py:220-259`; `tools/journal_echo.py` Grep `agent_id`; Grep `agent_id|agent_type` count over
`tools/*.py` (47 files); `tools/journal_write.py` Grep `calibrated|opt=\(`; `tools/journal_validator.py:300-379, 650-800,
1160-1300` + Grep `delegated_agents|task_worker_refs|judge|BASIS_VALUES|"calibrated"`; `tools/mechanism_gate.py:815-884`
+ Grep prefixes; `tools/session_context.py` Grep `_OPEN_LIFECYCLE_EVENTS`, `model_line`, `calibration`;
`tools/token_usage_stats.py` Grep `FAMILY_ORDER`; `tools/journal_hooks.py:200-217`; `tools/test_journal_hooks.py` Grep
`fable`; `tools/test_warn_messages.py:485-555` + Grep; `tools/warn_layers.json` Grep; `tools/permission_audit.py`,
`hook_liveness_probe.py` Grep `hygiene_gate`; Grep `hygiene_gate` count over `tools/` (101 / 27) and `.githooks` (0);
`.claude/agents/*.md` Grep `^tools:|^model:|^name:`; `.claude/agents/critic.md:50-61`; `PROCESS/LEAD_RANKING_EXAM.md:1-8`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:93-132, 673-681, 1110-1119` + Grep check numbers; `plans/piles/forge/batch-7-vhodyashchie-4.md`
Grep FG7-14/16/33/54; `plans/piles/forge/findings/20261111-basis-judge-razreshen-kodom-pri-neispolzuemom-sude.md` (whole);
`docs/tasks/specs/20261116-boot-by-topic-spec.md:345-359, 500-505` + Grep `architect|Phase 0|очередь`; `logs/journal/dev1.jsonl`
Grep `"event": ?"escalated"`, `"model":"claude-fable-…"`, count `"by": ?"fable"`.

## Decisions on the forks — current state (Lead 17.11.2026 + the owner's word 17.11.2026 + fix round 1)

Superseding the draft's «Lead decisions on the forks» section (its F18 (a) line and its «asked of the owner» list are
replaced here). Lead: F1 (a), F3 (a), F4 (A), F5 (a), F6 (a), F7 (a), F8 (a), F9 (a) — assigned to stream B and the
SHAPES row to L —, F11 (a), F12 (a), F14 (a), F18 (b) (fix round 1, on t-902 M4). The owner's word 17.11.2026: F2
(a), F10 (a), F15 (a) (with the pin), F21 (a). Lead's choices on the blockers (t-911 dispatch): B1 — a Fable session
commits A-F and L; B2 — `function_of_session` from `rank_of_model`; B3 — F9 and `test_journal_write.py` in stream B,
the SHAPES rows in L, step-4 reader decided by the designer; B4 — a code refusal + a registered detector; FG7-16 folded
into stream B; this spec lands before boot-by-topic. Open: F22 (owner), F23 (Lead).

## The owner's word (17.11.2026, Lead session)

Asked: "do we take the Lead's recommendations on the five forks put to the owner" -- the owner's answer: «да». Every
fork listed above as "asked of the owner" is therefore decided as recommended (a new forge tool may have its own test
file; P1-P31 move to `docs/OWNER_PRINCIPLES.md` with a generated index; the code-gated mechanics of «Командная работа»
move to `docs/TEAMWORK.md`; the local fallback needs both conditions; the Architect runs the weekly calibration, the
session default model is the lead binding, the Architect writes its own decision line). (The OWNER_PRINCIPLES,
TEAMWORK and local-fallback items belong to the parallel specs; the rest are F2, F10, F15, F21 of this spec.)

---

## Fix round 1 (t-911) — review t-902

Every finding of the review has a line; none deferred; none returned as wrong. Two findings open a new fork (M1 → F22
for the owner; M9 → F23 for the Lead), each executable on its recommendation.

| finding | what changed | section |
|---|---|---|
| B1 | A Fable session commits every commit of A-F and the L commit with `tier: fable`; the transitional world stated (every gate as today until L, pair check); the flip is one Fable commit; no cutover survives | §7.0, §3.4, §4.1, §1, §2.5 |
| B2 | `function_of_session` derived from `rank_of_model` (exact, then family); case «family bound, id differs» with note `(family match: <binding>)`; test rows `claude-fable-5-2` vs `claude-fable-5-1` in A1 and C1; ARCHITECT line printed through it; P37 added | §2.2, §4.4, §5.1, §5.4, §7 A1/C1/C2, §0 |
| B3.1 | F9 `reviewed_through`: validator shape + `journal_write.py calibrated --reviewed-through` in stream B (item B6) | §7 B, §4.5 step 8 |
| B3.2 | `tools/test_journal_write.py` in stream B's owns and DoD | §7 B |
| B3.3 | CLAUDE.md SHAPES rows `escalated` (opens a task for architect; `model` meaning) and new `calibrated` row in stream L, with the text | §7 L, §7.0, §4.3 |
| B3.4 | Step-4 reader decided: one `git grep` command in `ARCHITECT_START.md` (stream F), no new event, no SessionStart reader (the open-dispatch reader cannot serve: P42); error direction stated | §4.5 step 4, §7 F1, C10 |
| B4 | Code refusal: `hygiene_gate.decide` denies `journal_write.py accept/reject` from a payload with `agent_id` (detection measured in t-575, P38) — new stream E with rows; detector: validator WARN `INDEPENDENT CONTEXT` (stream B4) + check 6 items, registered by stream F; residuals stated | §2.4, §3.1, §5.2, §5.5, §7 E, §7 B4, §1, C8, C11 |
| M1 | Escalation above Opus = architect-queue item + `escalated` (rule 6 text by L); Opus outage: builder diffs wait in `lead-queue.md`; owner question returned as F22 | §4.7, §5.3, §4.4, forks F22 |
| M2 | `Last calibration` line gains an overdue suffix (Lead / Architect variants); the Lead's move written for CLAUDE.md; check 49 (b) registered | §4.6, §7 C4, §5.5, §7 L |
| M3 | New П3 node, finding and card row dropped; FG7-54 referenced (D7); `LEAD_RANKING_EXAM.md:3-4` purpose reworded in F | §1, §2.3, §6, §7 F3, §7 L |
| M4 | F18 → (b): no `LADDER_FROM`, no legacy table; C2 withdrawn; fallback is `DEFAULT_BINDINGS` through the same function | §3.4, §2.1, §2.3, forks F18, C2, C9 |
| M5 | F2 kept (a) by the owner's word; lazy `yaml` import, stdlib-only leaf, a test row that importing the leaf loads no yaml; option (c) recorded and not taken | §2.1, §7 A1, forks F2 |
| M6 | One bad-config behaviour: oversize / alias / unparsable / no pyyaml → default bindings + one WARN, no refusal; alias rejected by a loader that raises on aliases | §2.2, §2.4, C3, §7 A1 |
| M7 | `token_usage_stats.FAMILY_ORDER` derived from `FAMILIES`; in stream D | §2.3, §7 D, P51 |
| M8 | `escalated` to the Architect: `model` = architect binding (existing convention, P41) | §4.3, §7 L SHAPES text |
| M9 | Old 73 items closed by window acceptances (no backlog); new items: one road, F23 (recommended a second `accepted`); `lead-queue.md` is not that carrier | §3.5, §4.4, §5.5 check 6 (iii), forks F23 |
| M10 | `очередь: architect-tier → boot-by-topic`; shared files listed; the CLAUDE.md sections L rewrites named for re-measurement; the reciprocal line is the Lead's edit | §7.0 |
| m1 | P16 → `:1045`, P17 → `:2192`, P22 → 671 re-read; a dispatch re-reads its rows | §0 |
| m2 | PROJECT.md «новая идея» gets one line in L | §4.1, §6, §7 L |
| m3 | Stream D edges: `tier_echo` imports the leaf `tier_ladder` (stdlib-only) | §7 D |
| FG7-16 (Lead) | Folded into stream B (item B2): judge refused with text; rows; check 20 wording in F; batch-7 row by L; the finding's wrong carrier noted (P44) | §3.1, §7 B2, §5.5, §6, Noticed |
| designer-found | The draft's branch order in §3.1 was wrong (P43) — corrected; every self-activating file is placed by the coordinator's merge | §3.1, §7.0 |

**Premises the Lead must measure (no shell in this round):**
1. That the PreToolUse payload of a BASH call inside a subagent carries `agent_id` (P38 rests on t-575's measurement
   for all tools and on `handoff_gate` for Write/Edit) — one harmless Bash from a builder with the hook log on.
2. P22 counts `"by": ?"opus"` 278 and `queued-to-lead` 73 (taken from t-902, not re-measured here).
3. That `journal_write.py` emits `"ts","event","agent"` in this order for every event (P41 rests on five lines).
4. That a second `accepted` on a closed task passes the full validator run (P45 rests on reading `:1287-1297`).
5. The third parallel spec's owns against §7 (not read).
6. The existing `duplicate_model_id` rows of `test_mechanism_gate.py` (not read; A2 rewrites them).
