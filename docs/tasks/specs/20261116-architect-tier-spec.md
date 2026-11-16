# Spec draft — Lead moves to Opus, Architect (Fable) above Lead (t-893, F19)

Status: DRAFT by designer (opus) for Lead acceptance; forks are returned, not decided. Then critic-on-plan
(PROJECT.md «новая идея», step 6). Rules are cited by NAME/NUMBER, never by CLAUDE.md line numbers (the parallel
spec `docs/tasks/specs/20261116-boot-by-topic-spec.md` will move CLAUDE.md sections afterwards).

The owner's word, 16.11.2026 (carrier: the Lead's intent brief t-893): «Переводим Опус на лида. Фейбл будет уровень
ещё выше — Архитектор, для анализа новых идей, оптимизации процесса и сложных вопросов. Лид может сказать мне что
лучше позвать Архитектора… Так же я сама что-то большое буду сначала обсуждать с фейбл». Decisions 1-8 of the brief
are taken as given and are not reopened (quoted as D1..D8 below).

---

## §0 Premises (measured in this draft; every load-bearing claim below points here)

| # | claim | carrier (file:line + quote, or command + output) |
|---|---|---|
| P1 | lead binding is Fable | `delegation.config.yaml:19-21` `lead:` / `subscription:` / `model: claude-fable-5-1` |
| P2 | `reserve` is a COMMENTED optional rung above lead | `delegation.config.yaml:27` «OPTIONAL: a rung ABOVE lead, summoned only by the operator's own word»; `:43-49` `# reserve:` … `#     model: claude-fable-5` |
| P3 | critic Opus, builder/scout Sonnet; designer has no row | `delegation.config.yaml:52-54`, `:61-63`, `:70-72`; `:33-36` «`designer` deliberately has NO row here (see the onboarding skill's binding step)» |
| P4 | config comments point at the onboarding skill for rebinding and exams | `delegation.config.yaml:38-42` «rewalk the onboarding skill's binding step for `lead`, re-run that step's exam gate»; `:95-96` «see the onboarding skill, once installed under .claude/skills/onboarding/»; `:98-99` `exam: mandatory: true` |
| P5 | tier-gate ladder | `tools/mechanism_gate.py:673` `ROLE_RANKS = {"scout": 0, "builder": 1, "critic": 2, "lead": 3, "reserve": 4}`; `:208` `LEAD_FAMILIES = ("fable", "opus", "sonnet", "haiku")` |
| P6 | lead-binding default is "fable" | `tools/mechanism_gate.py:591-600` `if not config_text: return "fable"` … `return model or "fable"` |
| P7 | a family strictly above the binding passes the tier gate | `tools/mechanism_gate.py:851-853` `if declared_fam is not None and LEAD_FAMILIES.index(declared_fam) < LEAD_FAMILIES.index(fam): return True` → with lead=opus, `tier: opus` and `tier: fable` pass, `tier: sonnet` fails |
| P8 | duplicated model id on several rungs resolves to the MAX rank | `tools/mechanism_gate.py:727-730` «when the SAME model_id sits on SEVERAL rungs … the MAXIMUM rank among all exact matches is taken»; `:789-790` `return max(exact_matches)` |
| P9 | designer deliberately absent from the tier-gate ladder | `tools/mechanism_gate.py:667-672` «roles.designer is ALSO not a ladder rung … see test_build_role_ladder_ignores_designer» |
| P10 | the tier gate's queue note names a CURRENT_CONTEXT section that does not exist | `tools/mechanism_gate.py:866` «it goes into the Lead queue in CURRENT_CONTEXT.md»; `CURRENT_CONTEXT.md` headings (Grep `^#`): `# Current Context`, `## Maintenance Rule`, `## Current Milestone`, `## Current Task` — no queue section; Grep `-i queue\|очеред` on it: one hit, line 22 (a snapshot pointer) |
| P11 | `delegation.config.yaml` is NOT a mechanism path | `tools/mechanism_gate.py:211-283` `MECHANISM_PREFIXES` lists `CLAUDE.md`, `DECISIONS.md`, `PROCESS/`, `.claude/agents/`, `.claude/skills/`, `tools/session_context.py`, `.claude/settings.json`, `tools/journal_validator.py`, `logs/journal-letters.json` (as DATA) … and no `delegation.config.yaml` |
| P12 | the validator's family order and agent tiers | `tools/journal_validator.py:345` `TIER_ORDER = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}`; `:346-355` `AGENT_TIER` scout=haiku, builder=sonnet, critic=opus, designer=opus; `:366` `QUEUED_TO_LEAD_AGENTS = {"critic", "designer"}` |
| P13 | matrix branches | `tools/journal_validator.py:676-677` `if agent == "lead": return None`; `:680` unknown `by` FAILS; `:735` ok_tier `by_tier > agent_tier` legal at any basis; `:744` floor below sonnet; `:761-762` `basis == "critic"` legal iff `TIER_ORDER["opus"] > agent_tier`; `:779-781` queued-to-lead legal iff agent in {critic, designer} and `by in ("sonnet", "opus")` |
| P14 | only APPENDED lines are judged; HEAD lines are state | `tools/journal_validator.py:1100-1102` «HEAD and seed lines contribute their ids … none of them is judged»; `--all --base <ref>` checks «as an append to that ref» (`:2093`) |
| P15 | `escalated` needs an EARLIER event of the task in the file | `tools/journal_validator.py:1287-1297` `elif event in ("accepted", "rejected", "escalated", "defect_found") … if task_id not in seen_task_ids:` → violation; `tools/journal_write.py:78` `NEW_TASK_EVENTS = ("delegated", "decomposable")` |
| P16 | MODEL line text | `tools/session_context.py:221-226` `("fable", "Lead(top)"), ("opus", "critic-tier"), ("sonnet", "builder-tier"), ("haiku", "scout-tier")`; `:1031-1033` `f"MODEL: {sanitized} -> tier {tier}" " (declared by harness, not measured; Lead tier = fable)"` |
| P17 | SessionStart prints at most 25 lines | `tools/session_context.py:183` `MAX_LINES = 25`; order of lines `:2180` `lines = [now_line(now), model_line(stdin_payload)]` |
| P18 | session default model is a second carrier, read by no tool | `.claude/settings.json:2` `"model": "claude-fable-5-1"`; Grep `\.get\(["']model["']\)\|\[["']model["']\]` over the 16 tools that name `settings.json`: hits only in `agents_md.py:193` (role frontmatter), `mechanism_gate.py:598/685` (config), `compact_snapshot.py:537` (journal), `session_context.py:954` (hook payload) — none reads settings' `model` |
| P19 | other family-tuple carriers | `tools/tier_echo.py:126` `KNOWN_TIER_WORDS = ("haiku", "sonnet", "opus", "fable")`; `tools/dispatch_gate.py:1033` `_FAMILY_NAMES = ("fable", "opus", "sonnet", "haiku")`; `tools/journal_echo.py:643-668` `_extract_declared_word` iterates `tier_echo.KNOWN_TIER_WORDS`; `tools/savings_report.py:71` `_UNBOUND = "fable"`; `tools/agents_md.py:198-216` `tier_words` AST-parses the literal `TIER_ORDER` of the validator; `tools/token_usage_stats.py:172-182` `family()` (`"fable" in m or "mythos" in m` …) — NOT in the brief; `tools/journal_hooks.py:210` door text «(sonnet / opus / fable / haiku)» — NOT in the brief |
| P20 | `journal_write.py LEAD_ROWS` is NOT a family carrier (brief listed it) | `tools/journal_write.py:75` `LEAD_ROWS = {"lead_degraded": "coordination", "lead_restored": "process", "calibrated": "calibration"}` — event → category |
| P21 | savings counterfactual = lead binding | `tools/savings_report.py:122-138` `def top_tier_model` «the one bound to roles.lead … read through mechanism_gate.resolve_lead_binding»; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:535` «priced … at top-tier rates» |
| P22 | journal history volume (TEMPORAL edge) | Grep count over `logs/journal/`: `"by": ?"fable"` → 656 (dev1.jsonl); `"by": ?"opus"` → 278; `"basis": ?"queued-to-lead"` → 73 |
| P23 | the Lead queue file is read by no tool and no boot step | Grep `-i lead queue\|lead-queue` over `tools/` → 5 hits, none names `lead-queue-fable` (control: the same call finds `mechanism_gate.py:866`); Grep `lead-queue-fable` on `BOOT.md`, `CURRENT_CONTEXT.md`, `PROCESS/` → 0; `BOOT.md:27` «Read CURRENT_CONTEXT.md.» is its only queue-adjacent step; title `docs/tasks/lead-queue-fable.md:1` «# Очередь для полного Lead (Fable)», `:4` «вычёркивает (строкой «сделано: <хэш>») Fable»; `:22-24` two items still OPEN |
| P24 | calibration checks 5-6 speak of the "top tier" | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:108-113` «Cross-check the actual models of Lead sessions … Lead-tier activity on a model below the top tier, outside a declared window, is silent degradation»; `:119-124` acceptance from above by session tier vs `agent` tier, «"queued for the full Lead" note» |
| P25 | critic role text | `.claude/agents/critic.md:52-57` «When the coordinator is below the top tier (degradation, or the standard mid-tier mode …)» |
| P26 | Lead exam names TIER_ORDER and "top of the order" | `PROCESS/LEAD_RANKING_EXAM.md:29-31` «top of this deployment's tier order (`TIER_ORDER` in `tools/journal_validator.py`), no model above it exists to judge» |
| P27 | function table | `docs/TWO_VOCABULARIES.md:15` «**Lead** — decomposition, specs, graph acceptance \| coordinator; full authority only on the Lead tier \| Fable session \| Fable alias» |
| P28 | D-0003 | `DECISIONS.md:30` «D-0003 — Bindings: lead claude-fable-5-1, critic and designer claude-opus-5-5, builder and scout claude-sonnet-5-5» |
| P29 | SIBLING_MAP: Lead Queue + the two skills | `docs/SIBLING_MAP.md:655-661` «Below-lead sessions put drafted axes into CURRENT_CONTEXT.md's "Lead Queue" section»; `:519` «`.claude/skills/next-task/SKILL.md` \| Lead \| next-task procedure»; `:522` «`.claude/skills/onboarding/SKILL.md` \| Lead \| install and upgrade, per-tier exams»; axis 1 `:29-30` role profiles `{scout,builder,critic,designer}`, model binding `delegation.config.yaml` |
| P30 | readers of the onboarding skill's NAME outside history | `PROCESS/PATCH_PROTOCOL.md:22-23` «the closing step of an upgrade (the onboarding skill's Upgrade mode, step 7)»; `docs/ADOPTION_LEDGER.md:3-4,23,52,77,143` («filled in by the onboarding skill's "Ledger" step (`.claude/skills/onboarding/SKILL.md`)» …); `.claude/skills/critic-exam-gen/SKILL.md:163,182` («the onboarding skill point», «Mirror the flow the other exams already use (`onboarding` skill, step»); `delegation.config.yaml:34,39,95-96` |
| P31 | install parity does NOT name the two skills | `tools/install_parity_anchors.json:657-661` unit `skills`, `"host_path": ".claude/skills"`, `"kind": "path"` — a directory unit; Grep `onboarding` (-i) over `tools/` → 24 hits in 8 files, none in `install_parity_anchors.json`; the hits in `tools/test_wiring_check.py:487-526` build a SYNTHETIC repo (`_add_skill(repo, ".claude/skills/onboarding/…")`) |
| P32 | AGENTS.md generator reads hooks, role files, tier words and a CLAUDE.md copy — not skills | `tools/agents_md.py:219-223` `build_setup`: `hooks_rows`, `roles_rows`, `tier_words`; Grep `skill\|exam-gen` (-i) on `AGENTS.md` → 0, control Grep `Hooks\|fable` → `AGENTS.md:885` (CLAUDE.md copy «(`haiku`/`sonnet`/`opus`/`fable`)»), `:994` `### Hooks` |
| P33 | FG7-33 / FG7-14 rows; batch 7 is NOT taken (editable) | `plans/piles/forge/batch-7-vhodyashchie-4.md:3` «статус: ожидает \| взял: —»; `:57` «FG7-33 \| П2 \| Opus-координатор точечно вызывает Fable субагентом для вопросов лида … не строим сейчас»; `:37` «FG7-14 \| П2 \| Метка диспатча несёт роль, а не модель … `tools/dispatch_gate.py`, `tools/test_dispatch_gate.py`, `CLAUDE.md` … ожидает» |
| P34 | a new test file is forbidden by default | `docs/TESTING.md:118` «новый тестовый файл не создаётся»; `:125-128` the exception exists only by the owner's word 14.11.2026 for tools of the offload spec |
| P35 | the tier-gate audit lists label mismatches, not the commits | `tools/mechanism_gate.py:55-57` «`python tools/mechanism_gate.py --audit --since <date>` (audit_labels()): per mechanism commit of the window, every axis line whose label mismatches the current map» |
| P36 | no role named architect exists (brief) | Grep `architect` was not re-run over `.claude/agents/` (positive control impossible to separate from `architecture` hits); verified instead structurally: `docs/SIBLING_MAP.md:29` role profiles are `{scout,builder,critic,designer}`; `.claude/agents/critic.md:2` `name: critic` — LABEL: brief's claim, structurally consistent, not re-grepped |

---

## §1 What changes; mechanisms touched; the owner of every check

**What changes, in one paragraph.** The FUNCTION Lead is bound to Opus (`claude-opus-5-5`); a new FUNCTION
Architect is bound to Fable (`claude-fable-5-1`) and sits one rung above Lead. critic and designer stay on Opus (D1).
The acceptance matrix compares FUNCTION ranks scout < builder < critic = designer < lead < architect (D2); the code
that today compares model families (P12, P13) is brought to that rule through ONE ladder home (§2). Mechanism
commits are made by the Opus Lead after the critic; the Architect reviews them as a weekly batch (D3) from a start
checklist that only an Architect session loads (D4, §4). DECISIONS.md stays one file (D5). Two old source skills are
deleted (D6). The Opus Lead exam is a П3 node that blocks nothing (D7). The Lead never launches the Architect: it
tells the owner and writes `escalated` (D8).

**Package:** `ai-packages/qa-factory/` is NOT touched by any stream of this spec → no AR-n invariant applies; no
package commit is made, so no `architecture:` line is owed. (Should any stream drift into the package, that is a
scope violation, not an AR question.)

**Mechanisms touched (rule 10 recognition):** routing policy (CLAUDE.md «Tiers», «Role ≠ tier», «Lead degradation»,
rule 10's tier line, the Routing log `by` paragraph); the tier gate (`tools/mechanism_gate.py`); the journal gate
(`tools/journal_validator.py`); the SessionStart hook (`tools/session_context.py`); the model binding
(`delegation.config.yaml`, which becomes acceptance-deciding DATA → joins the mechanism net, §2.5); calibration
checks 5, 6 and 18 (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`); the critic role file; a new start checklist; two
queue carriers; two deleted skills.

**Checks added or altered — owner served, census class.** (The package census `judgment-census.json` is not
touched; the class below is the AR-29 vocabulary applied to forge checks.)

| check | added/altered | owner it serves | class |
|---|---|---|---|
| journal matrix: rank of `by` and of `agent` read from the ladder home (§3) | altered | DATA (code): who accepted whom, by shape; the MEANING of each acceptance stays the acceptor's judgment, re-judged at calibration by the Architect | data — shape/join, refusal |
| matrix: `basis: queued-to-lead` written by an acceptor ranked lead or above (§3, fork F5) | added (WARN recommended) | DATA (code) | data — shape, report only |
| matrix: pre-cutover lines judged by the legacy table (§3.4, fork F18) | added | DATA (code) | data — temporal join |
| tier gate: ladder read from the home, `architect` rung (§2) | altered | DATA (code): form of the `tier:` line; its TRUTH is calibration's judgment (Architect) | data — shape, refusal |
| tier gate: `delegation.config.yaml` and the home module join `MECHANISM_PREFIXES` (§2.5) | added | DATA (code) | data — presence |
| SessionStart MODEL line by function; ARCHITECT line (§4.4, §5.4) | altered/added | DATA (code) reports; the session's entry decision is JUDGMENT (the session's own tier check) | data — report, no refusal |
| pin: `.claude/settings.json` `model` == lead binding (fork F15) | added | DATA (code) | data — join, test row |
| `mechanism_gate.py --list --since` (commits for the Architect's batch review, §4.5) | added | DATA (code) lists; the review verdict is JUDGMENT (Architect, a tier above Lead) | data — listing |
| Architect start checklist (§4.5) | added | JUDGMENT (Architect), accepted by INTENT (owner — the owner switches the model) | judgment procedure |
| weekly batch review of mechanism commits (§4.6) | added | JUDGMENT (Architect over Lead's work) | judgment |
| Lead's signal «лучше позвать Архитектора» + `escalated` (§4.3) | added | JUDGMENT (Lead), INTENT (owner decides to switch) | judgment + intent |
| calibration check 5/6 wording by function rank (§5.5) | altered | JUDGMENT (calibrator = Architect, fork F10) on DATA from the ladder home | judgment on data |

---

## §2 The ladder as data — one home, one reader

### 2.1 The home

ONE module holds the three facts every reader needs, and ONE file holds the bindings:

1. `FAMILIES` — the model-family vocabulary in ONE order, weakest → strongest: `("haiku", "sonnet", "opus", "fable")`,
   with an alias row `{"mythos": "fable"}` (taken from `token_usage_stats.family`, P19). A reader needing
   strongest-first reverses it; no reader keeps its own tuple.
2. `FUNCTION_RANKS` — `{"scout": 0, "builder": 1, "critic": 2, "designer": 2, "lead": 3, "architect": 4}` (D2:
   critic = designer). `COORDINATION_FUNCTIONS = ("scout", "builder", "critic", "lead", "architect")` — the rungs a
   CONFIG binding is read for (designer stays out of the config ladder, P9; its rank is used only to judge it as an
   executor).
3. Bindings — `delegation.config.yaml` `roles.<function>.subscription.model` / `.api.model` (unchanged format), read
   by the home's one parser.

Where the module lives is fork **F2** (new leaf `tools/tier_ladder.py` vs inside `tools/mechanism_gate.py`). Whether
the rank ORDER lives in code or in the config is fork **F3**. The rung's key name is fork **F1** (recommended:
`architect`).

### 2.2 The reader functions (public names; one road for every reader)

- `family_of(model_id) -> str | None` — substring match on `FAMILIES` + aliases, lowercase; `None` for a non-Claude id.
- `bindings(config_text) -> dict[function, model_id]` — the coordination functions that have a model; absent file,
  broken YAML, or no `roles` → `{}` (callers decide the fallback; see 2.4).
- `rank_of_function(name) -> int | None` — `FUNCTION_RANKS`; unknown name → `None`.
- `rank_of_model(model_word_or_id, config_text) -> int | None` — THE function the matrix and the tier gate share:
  (a) exact id match on a bound rung → max rank among matches (keeps P8); (b) else the family: the max rank of
  functions bound to that family; (c) a known family bound to NOTHING → placed by family order: stronger than the
  lead binding's family → `architect` rank ("a rung above lead", the existing reserve-above-binding concept, P7);
  weaker than every bound family → `-1` (below scout: the floor); between two bound families → the rank of the
  nearest WEAKER bound family's top function (rounds DOWN); (d) unknown family, non-Claude id with no exact match →
  `None`. The family-strength guard of `_resolve_ladder_rank` (P5, `:780-807`: a rung bound to a family WEAKER than
  lead's never inherits a rank ≥ lead) moves into this function unchanged.
- `lead_binding(config_text) -> str | None` and `architect_binding(config_text) -> str | None`.
- `function_of_session(model_id, config_text) -> (function | None, note)` — for the MODEL line (§5.4).

**Error direction (rule 1: an advisory resolver becomes a GATE input).** `rank_of_model` may err only DOWNWARD
(lower rank → a basis is needed / the tier line is refused); it may never invent a rank above what the bindings or
the family order give. Adversarial inputs that must stay on the safe side (each a table row in the home's test):
`by="claude-opus-5-5"` (full id where a word is expected — the validator still FAILS it, as CLAUDE.md says today);
`"Opus"` / `" opus "` (case/space: the validator compares exact lowercase keys today, P12 — keep FAIL); `"lead"`
(a function word where a model word is expected, under fork F4 option A → FAIL with a door); `"opus-lead"`;
`"fable"` with NO architect key (→ architect rank by family, case c — the one permissive case, kept because P7
already encodes it and 656 old lines carry it, P22); a config binding critic=fable, lead=opus (nonsense: a lower
function on a stronger family) → fable resolves to `critic` rank by the guard's positional rule, not above lead;
lead and architect bound to the SAME id → exact match max rank = architect, and opus (now unbound) rounds DOWN to
builder; empty / non-string; a YAML bomb or a 10 MB config (the parser reads the tracked file; refuse > 64 KB with
a door — small choice C3).

### 2.3 Every current carrier — reads the home / deleted / stays

| carrier | today | after |
|---|---|---|
| `tools/mechanism_gate.py:673` `ROLE_RANKS` | own ranks | DELETED; reads `FUNCTION_RANKS`/`COORDINATION_FUNCTIONS` (or IS the home under F2-b) |
| `tools/mechanism_gate.py:208` `LEAD_FAMILIES` | own tuple strongest-first | DELETED; reads `FAMILIES` reversed |
| `tools/mechanism_gate.py:582-611` `resolve_lead_binding`, `lead_family` | own parser, default "fable" | thin wrappers over `lead_binding`/`family_of` kept for their importers (`savings_report.py:63`); the "fable" default (P6) becomes: no lead binding → the tier gate reads the LEGACY default (lead family = fable, i.e. fail-closed for anyone below Fable) — unchanged behaviour for a config-less clone |
| `tools/mechanism_gate.py:690-810` `build_role_ladder`, `_resolve_ladder_rank` | own ladder | DELETED into `rank_of_model` |
| `tools/journal_validator.py:345` `TIER_ORDER` | family → 0..3 | kept ONLY as the LEGACY table (§3.4) under the name `LEGACY_TIER_ORDER`; `TIER_ORDER` as a name disappears (its readers below move) |
| `tools/journal_validator.py:346-355` `AGENT_TIER` | agent → family | DELETED; agent rank = `rank_of_function(agent)` |
| `tools/journal_validator.py:366` `QUEUED_TO_LEAD_AGENTS` | {critic, designer} | stays (a data row of the matrix, not a ladder fact); its condition reads ranks (§3) |
| `tools/session_context.py:221-226` `_MODEL_TIER_SUBSTRINGS`, `:986` `model_tier` | own tuple → labels | DELETED; `function_of_session` |
| `tools/tier_echo.py:126` `KNOWN_TIER_WORDS` | own tuple weakest-first | reads `FAMILIES` (same order; `test_extract_declared_word_picks_first_known_tier_words_order` stays green) |
| `tools/journal_echo.py:643` `_extract_declared_word` | via tier_echo | unchanged code (reads through tier_echo, which now reads the home) |
| `tools/dispatch_gate.py:1033` `_FAMILY_NAMES`, `_model_family` | own tuple | reads `FAMILIES` / `family_of`; the module docstring's «implemented locally (this layer does not import any other gate module for it)» (`:1047-1050`) is retired — the home is a leaf, not a gate |
| `tools/journal_hooks.py:210` door text «(sonnet / opus / fable / haiku)» | literal list | built from `FAMILIES` |
| `tools/savings_report.py:71` `_UNBOUND = "fable"`, `:122` `top_tier_model` | lead binding | reads `lead_binding` (None ⇒ the existing PricesError); the counterfactual's model is fork **F11** |
| `tools/agents_md.py:198-216` `tier_words` (AST of validator `TIER_ORDER`) | parses a literal in another file | reads the home's `FAMILIES` literal (AST of the home, same technique) — AGENTS.md text unchanged in content |
| `tools/token_usage_stats.py:172` `family()` | own heuristic + display case | reads `family_of`; display capitalisation stays local (a presentation, small choice C4) |
| `tools/journal_write.py:75` `LEAD_ROWS` | event → category | UNCHANGED — not a ladder carrier (P20; the brief's list was wrong here) |
| `tools/fixtures/host_pre_delivery_CLAUDE.md` | frozen old text | UNCHANGED — a frozen fixture by design |
| `PROCESS/LEAD_RANKING_EXAM.md:29-31` | names `TIER_ORDER` in the validator | pointer to the home's `FUNCTION_RANKS`; «no model above it exists» is no longer true for Lead (Fable is above) → text in stream F |
| `.claude/settings.json:2` `"model"` | Fable | Lead binding value (fork F15); read by the harness only (P18) |

### 2.4 Edges of the home (TEMPORAL and absent inputs)

- **Config without the architect key** (other clones, an old checkout, the world before stream L): `bindings()` has
  no `architect`; `rank_of_model("fable")` → architect rank by case (c) ⇒ old `by: fable` lines and `tier: fable`
  commits behave exactly as with the key. Invariant: *removing or never adding the key never makes any party MORE
  privileged than with it*. (With the key bound to Fable the results are identical; with the key bound to a
  non-Claude id, fable still ranks above lead by family — stated, tested.)
- **Config with the old `reserve:` key uncommented** (a clone that bound it): fork F1 — recommended: `reserve` is
  NOT read (it was commented in every tracked copy, P2), and the home's parser prints a one-line WARN naming the
  rename door («rename `roles.reserve` to `roles.architect`»). Invariant: a key the code does not read never
  silently raises a rank.
- **Absent / unparsable config**: `bindings() == {}` → `rank_of_model` uses the LEGACY mapping (sonnet → builder,
  opus → critic, fable → lead, haiku → -1). Invariant: *a broken config can only make acceptance STRICTER than the
  live one* (Opus would need a basis to accept critic work — the safe direction).
- **lead and critic on the same id** (the new live state; `duplicate_model_id` cases in `test_mechanism_gate.py`):
  max rank = lead (P8). Invariant: a critic subagent never writes `accepted` lines (only the coordinator does), so
  the shared id never lets a critic certify itself; the critic's independence rests on its separate context (D2).
- **A session model matching no binding**: §5.4.

### 2.5 The mechanism net

`delegation.config.yaml` becomes DATA that decides acceptance legality and the tier gate (like
`logs/journal-letters.json`, P11) → it joins `MECHANISM_PREFIXES` with a comment «DATA that decides the acceptance
matrix and the tier gate: an edit re-ranks every acceptor». Under F2-a the new module joins too («imported by
journal_validator / session_context / mechanism_gate / tier_echo / dispatch_gate»); the closure test
`test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` (named at `mechanism_gate.py:259`)
enforces it. TEMPORAL: the commit that adds the config to the net is itself the first commit gated by it — it
carries the axis block and `tier:` line (it touches `tools/mechanism_gate.py` anyway).

---

## §3 The acceptance matrix by function

### 3.1 The table (rank of the acceptor = `rank_of_model(by)`; rank of the executor = `rank_of_function(agent)`)

| executor (`agent`) ↓ / acceptor rank → | below builder (−1; e.g. haiku) | builder rank (Sonnet coordinator, degraded) | lead (Opus) | architect (Fable) |
|---|---|---|---|---|
| scout (0) | ILLEGAL (floor; only `judge` — not used here, rule 13) | legal | legal | legal |
| builder (1) | ILLEGAL | needs `basis: critic` | legal (the "critic: skipped" waiver available) | legal |
| critic (2) | ILLEGAL | needs `basis: queued-to-lead` | legal — **Lead accepts a critic verdict** | legal |
| designer (2) | ILLEGAL | needs `basis: queued-to-lead` | legal — **Lead accepts a designer draft** | legal |
| lead (`agent: "lead"`) | no matrix (P13 `:676`) | no matrix | no matrix | no matrix |
| architect (`agent: "architect"`) | no matrix (new: same branch as `lead`) | no matrix | no matrix | no matrix |
| unknown agent | no matrix (unchanged, P13 `:678`) | — | — | — |

Branch order of `_matrix_d0058_violation` is KEPT (judge → unknown-`by` FAIL → ok_rank → floor → critic →
queued-to-lead → generic). Positional invariant (rule 11 (ii)): the unknown-`by` enum check stays FIRST after judge,
so no rank arithmetic ever runs on an unidentifiable acceptor; the floor stays before every basis, so no basis
rescues a below-builder acceptor.

### 3.2 `basis` after the change

- `basis: critic` — legal iff `rank_of_function("critic") > rank(agent)` (scout, builder). Unchanged semantics; the
  literal `TIER_ORDER["opus"]` (P13 `:762`) becomes the critic's FUNCTION rank — so a deployment that binds critic
  elsewhere keeps the rule.
- `basis: queued-to-lead` — legal iff `agent ∈ QUEUED_TO_LEAD_AGENTS` AND `builder rank ≤ rank(by) < lead rank`.
  Today's literal `by in ("sonnet", "opus")` (P13 `:780`) becomes this rank band. A line where `rank(by) ≥ lead`
  already passed at ok_rank before the basis is read — such a line queues work to itself; fork **F5** (recommended:
  WARN, not FAIL, so pre-cutover lines merged late stay legal).

### 3.3 What `by` holds in a NEW line — fork **F4**

Recommended **option A**: `by` stays the bare MODEL-FAMILY word (`haiku`/`sonnet`/`opus`/`fable`) — the session's
self-declared model, the thing calibration can reconcile against transcripts; the validator turns it into a FUNCTION
rank through `rank_of_model` (D2 satisfied: ranks are function ranks). Nothing changes for writers
(`journal_write.py accept --by B`, P-free), 656/278/73 history lines (P22) keep their vocabulary.
Option B (function words `lead`/`architect`/… in `by`) is laid out in F4 with its costs.

### 3.4 Both worlds (TEMPORAL)

- **Old lines are never re-judged** (P14): HEAD lines are state. So the 656 `by: "fable"` lines stay as they are.
- **Late-merged lines written before the switch** (a branch of another clone, judged as "our side's tail" at merge):
  the new ranks are monotone-permissive for every pair that was legal before (checked pair by pair: fable >
  everything both worlds; opus+critic+queued-to-lead → passes at ok_rank; sonnet+builder+critic → passes; sonnet +
  scout → builder > scout), but they would also legalise lines that WERE self-certification then (`by: opus`,
  `agent: critic`, no basis, written while Opus was a degraded Lead). Recommended (fork **F18**): a constant
  `LADDER_FROM = "<ts of the stream-L commit>"`; a line with `ts < LADDER_FROM` is judged by `LEGACY_TIER_ORDER` +
  the old `AGENT_TIER` (kept as the legacy pair), a line at/after by the function ranks. Invariant: *a line is
  judged by the table that was in force when it was written*. Same pattern exists: `FEATURE_WARN_FROM`
  (`journal_validator.py:321`), `NODE_WARN_FROM` (`:328`).
- **`tier: fable` lines in old commits**: the tier gate judges only the commit being made (`decide_full`,
  `mechanism_gate.py:947-980`); `--audit` judges axis labels only (P35). Old commits are never re-judged; new
  `tier: fable` commits pass (P7 / case c).

### 3.5 The Sonnet coordinator's `queued-to-lead` items — who clears them

The full Lead is now Opus. Every `queued-to-lead` acceptance — the 73 old ones (P22, written when the full Lead was
Fable) and new ones — is cleared by a Lead-ranked session (Opus or Fable). Clearing = a later `accepted` of the same
task by a Lead-ranked `by` with `closes:`-style note, as today. The Architect does NOT owe the clearing (it is Lead
work; an Architect session MAY do it, §5.2).

---

## §4 The Architect function

### 4.1 Its work (owner's list + the brief's decisions)

1. Analysis of new ideas — the owner discusses big things with Fable first (owner's word); PROJECT.md «новая идея»
   steps 1-4 may run in an Architect session; steps 5-8 go to the Lead's routing as today.
2. Process optimisation and hard questions the Lead escalates (§4.3).
3. The weekly batch review of mechanism commits, at calibration «или чаще, если на него переключаются» (D3, §4.6).
4. Decisions into `DECISIONS.md` (same file, D5; who physically writes the Architect's line — fork **F21**).

**Not its work:** routine coordination, dispatching and accepting workers (Lead), each mechanism commit (D3 — Lead
after critic), being launched as a subagent (D8: the owner switches the session model), the Lead's queue items
(§3.5).

### 4.2 Summoning

Only by the owner's switch of the session model (`/model` or a new session on the Fable binding). Never routed to
automatically; never a subagent. FG7-33 («Opus-координатор точечно вызывает Fable субагентом», P33) is SUPERSEDED by
D8: the node's status becomes «снят: заменён решением владельца 16.11.2026 (спека 20261116-architect-tier-spec)»
— a Lead edit in an untaken batch (P33 `:3`).

### 4.3 The Lead's signal

When a question is Architect-class (a new idea's architecture, a process trade-off, a rule conflict the Lead cannot
settle, a disagreement with a critic verdict the Lead cannot resolve), the Lead (a) tells the owner in plain Russian
«лучше позвать Архитектора: <вопрос одной строкой>, <что ждёт>», (b) writes the question as an item of the Architect
queue (§4.4), (c) writes `escalated` (agent = `architect`, model = the Lead's own model, task_id, notes = the item's
one-line summary + the queue path). Edge — **no task exists yet** (a fresh idea; P15 refuses an `escalated` whose
task has no earlier event): fork **F6** (recommended: `escalated` with `agent: "architect"` joins
`NEW_TASK_EVENTS`, so it may open a task id issued by `journal_write.py next`). Work on that question waits for the
Architect; unrelated work continues.

### 4.4 The queue carriers (fork **F8**)

Recommended: TWO files, one per direction, both outside the mechanism net:
- `docs/tasks/lead-queue.md` — `git mv` of `docs/tasks/lead-queue-fable.md`, retitled «Очередь для Lead»: what a
  below-Lead session cannot do (mechanism commits, Lead-class acceptance). Written by any coordinator; struck
  («сделано: <хэш | t-nnn>») by a Lead-ranked session. Its two OPEN items (P23 `:22-24`) move with it. The tier gate's
  note (P10) and `docs/SIBLING_MAP.md:659` point HERE instead of the non-existent CURRENT_CONTEXT section.
- `docs/tasks/architect-queue.md` — new: items the Lead (or the owner) puts to the Architect. Item form, one per
  line: `- [ ] <YYYY-MM-DD> <task_id|—> <question one line> (от: Lead|владелец)`; struck by the Architect:
  `- [x] … — сделано: <D-nnnn | хэш | t-nnn | ответ одной строкой>`. Written by the Lead and the owner; read by an
  Architect session at start (checklist step 2); the SessionStart line counts `- [ ]` items (§4.4 line below).

**SessionStart line** (stream C), printed ONLY when `function_of_session(model) == "architect"`, placed directly
after the MODEL line so the 25-line cut (P17) can never drop it:
`ARCHITECT SESSION: start with PROCESS/ARCHITECT_START.md; queue docs/tasks/architect-queue.md (<N> open)`.
Edges: queue file absent → `(queue file absent)`; unreadable → `(queue unreadable: <reason>)`; N = 0 → `(0 open)`;
architect key absent → the line is NOT printed and the MODEL line says `above lead (no architect binding)` (§5.4).
Invariant: *a non-Architect session never pays boot bytes for the Architect*.

### 4.5 The START CHECKLIST (D4) — `PROCESS/ARCHITECT_START.md` (fork **F7** on where it lives)

Loaded only via the SessionStart pointer above (zero bytes for other sessions; not in CLAUDE.md body). Ordered:

1. **Tier check.** The MODEL line says function `architect`. If not — this file does not apply; stop.
2. **The owner's reason first.** If the owner switched with a question, that question is item 0; the steps below run
   after it is answered or in parallel only when cheap.
3. **Architect queue.** Read `docs/tasks/architect-queue.md`; every `- [ ]` item gets an answer, a decision, or an
   explicit «оставлено: <почему>».
4. **Open escalations.** Journal `escalated` events with `agent: "architect"` that have no later closing event
   (`closes:<task-id>` token or `accepted` by a Lead-ranked/architect `by`) — read through the existing open-dispatch
   reader (stream C extends `open_dispatch_lines` to report them as `ESCALATED TO ARCHITECT`, or a small choice: a
   grep command named here). Each must match a queue item; a mismatch is a finding.
5. **Mechanism commits since the last Architect review.** Command (stream A adds it):
   `python -B tools/mechanism_gate.py --list --since <date-or-sha>` — one line per commit touching a mechanism path
   (`mechanism_paths()`), merges against first parent: `<sha> <committer date> <tier: values> <subject>` + its
   mechanism paths. The "since" value = the last review marker (fork **F9**). Each commit: OK, or a finding /
   `defect_found` against the accepting task.
6. **Calibration.** If the SessionStart `Last calibration` line is older than 7 days → run the weekly calibration
   (fork **F10** on whether it is the Architect's), which includes step 5.
7. **Boot budget.** The `BOOT BUDGET` line: over WARN → the boot-diet backlog item is put to the Lead queue (the
   Architect does not trim boot files itself unless the owner says so).
8. **Close the review.** Write the review marker (F9) — one journal line through `tools/journal_write.py`.

### 4.6 The weekly batch review

The Architect reviews the mechanism commits of the window (step 5) for: the axis block truthful, the rule placed at
the right level (rule 9), the detector registered (rule 10 c), D-entries consistent. Verdicts go into the
calibration report; a defect is a `defect_found` (agent = the accepting tier, `ref` = the original task) or a
finding in `plans/piles/forge/findings/` with its batch row (PROJECT.md «Командная работа» п. 2).

---

## §5 «Role ≠ tier» and «Lead degradation» for the new ladder

### 5.1 Definitions (rewrite)

- The TIER of a session = the FUNCTION RANK of its actual model: `rank_of_model(model)` — the highest function bound
  to it (Opus → lead even though critic and designer share the id).
- Full Lead = a coordinator whose rank is ≥ lead (Opus, or Fable doing Lead work). Only it changes mechanisms, the
  decision log, table statuses and gates.

### 5.2 The matrix by the coordinator's actual function rank

- **Architect (Fable)** — unrestricted; may do any Lead work WITHOUT an event (it is above Lead; the tier gate
  already passes `tier: fable`, P7). Recommended: no new event for "Architect did Lead work" — the `model` field of
  its journal lines and the main-chain transcript already record it (alternatives in F-list: none needed beyond F9).
- **Lead (Opus)** — full Lead: coordination, dispatch, acceptance of scout/builder/critic/designer (§3.1), the
  "critic: skipped" waiver over builder, mechanism commits after the critic (D3), DECISIONS.md (D5), statuses.
  Architect-class questions → §4.3.
- **builder rank (Sonnet coordinator)** — coordination, dispatches; accepts scout; a builder diff only with critic
  input; critic/designer work → `queued-to-lead`; Lead-class work → `docs/tasks/lead-queue.md`.
- Below builder rank — no coordination.

### 5.3 Lead degradation

1. Trigger: the Lead model (Opus) refuses / is unavailable, or the operator switches to a model ranked below lead →
   drop to builder rank (Sonnet) + `lead_degraded`. ONE step down now (Opus → Sonnet); the old «upper-mid, then mid»
   two-step disappears.
2. **Fable unavailable / refusing is NOT a Lead degradation**: no `lead_degraded`; Architect queue items wait; the
   owner is told once. Invariant: *the Architect's absence never stops Lead work*.
3. EXIT (rule «tier verification», point b): a rise from builder rank to lead OR architect rank proves a window →
   retro `lead_degraded` + window acceptance + `lead_restored`, as today. A switch Opus → Fable or Fable → Opus is
   NOT a window (both ≥ lead): no event.
4. While degraded: unchanged list (no statuses/gates; decision-log entries queued to the Lead).

### 5.4 Tier verification at entry — the MODEL line

`MODEL: <id> -> function <f> (declared by harness, not measured; lead = <lead binding>, architect = <architect
binding | unbound>)`. Cases:
- id matches a binding → `<f>` = the highest function bound (Opus → `lead`; Fable → `architect`; Sonnet → `builder`).
- Claude family bound to nothing, stronger than lead (Fable with no architect key) → `above lead (no architect
  binding)`; acts as full Lead; no ARCHITECT line.
- Claude family bound to nothing, weaker than lead → `<nearest weaker function> (unbound family)`; below-lead rules.
- **No binding matches and no family is recognised** (a new model name, a non-Claude id) → `function none (matches
  no binding in delegation.config.yaml) -- coordinate under the below-lead rules until verified`. Invariant: *an
  unrecognised model never reads as Lead*. The validator FAILS its `by` (unknown family, P13 `:680`) and the tier gate
  refuses its `tier:` (case d) — the same direction everywhere.
- No model in the payload → unchanged fallback (`MODEL: not provided by hook input -- verify tier yourself`).
- Config unreadable → the line appends `(config unreadable: legacy ranks)`.

### 5.5 Calibration checks 5, 6, 18

- Check 5: «Lead-tier activity on a model below the top tier» → «Lead-tier activity on a main chain ranked below
  lead (`rank_of_model`), outside a declared window». An Architect (Fable) main chain doing Lead work is NOT
  degradation. "Lead activity" = main chains whose model ranks ≥ lead.
- Check 6: the acceptor's tier = `rank_of_model` of the main-chain model at the event; «"queued for the full Lead"»
  → «queued for the Lead».
- Check 18 / savings: fork F11.

---

## §6 Files to change, with readers

Reader search method (designer rule 3): the Grep tool over `tools/`, `.githooks/`, and `.claude/` restricted to
`.claude/settings.json`, `.claude/agents/`, `.claude/skills/` (an unrestricted `.claude/` search drowns in
`.claude/worktrees/*` copies — 5258 hits / 1911 files, timed out; those copies are other workers' trees, not
readers). Controls: `.githooks` searched for `mechanism_gate|journal_validator|session_context` → 3 hits
(`commit-msg:6`, `pre-commit:8`, `pre-merge-commit:18`), so a 0 there is real.

| file | change | readers (command → hits) and their fate |
|---|---|---|
| `delegation.config.yaml` | lead → `claude-opus-5-5`; new `architect:` rung → `claude-fable-5-1` (F1); comments: drop onboarding-skill references (P4, F14), say «ranks: see the ladder home» | Grep `delegation\.config` `tools/` → 29 hits / 12 files: `mechanism_gate.py` (6 — changes, stream A), `savings_report.py` (5 — A), `test_savings_report.py` (4 — A), `test_mechanism_gate.py` (1 — A), `claim_control_gate.py` (3 — scope list, unchanged), `test_claim_control_gate.py` (3 — unchanged), `dispatch_gate.py` (1, docstring `:92` — unchanged), `agents_md.py` (1, text `:257` — unchanged), `install_parity_anchors.json` (2, path unit — unchanged), `test_install_parity.py` (1 — unchanged), `tests/test_role_carriers_one_owner.py` (1, TWO_VOCABULARIES row `:73` — unchanged unless F stream edits that cell, then re-run), `fixtures/host_pre_delivery_CLAUDE.md` (1 — frozen). `.githooks` → 0. `.claude/skills/onboarding/SKILL.md` (deleted, D6), `critic-exam-gen/SKILL.md` (3 — stream F text), `scout-exam-gen/SKILL.md` (2 — unchanged: binding-generic). New readers: the home (A), `journal_validator.py` (B), `session_context.py` (C) |
| home module (F2: `tools/tier_ladder.py` new, or inside `mechanism_gate.py`) | new | importers after the change: mechanism_gate, savings_report (via wrappers), journal_validator, session_context, tier_echo, dispatch_gate, journal_hooks, agents_md (AST), token_usage_stats; `MECHANISM_PREFIXES` entry; closure test in `test_mechanism_gate.py` |
| `tools/mechanism_gate.py` | ladder → home; `architect` rung; `--list --since`; queue-note text → `docs/tasks/lead-queue.md`; `MECHANISM_PREFIXES` += config (+ home) | Grep `KNOWN_TIER_WORDS\|LEAD_FAMILIES\|_FAMILY_NAMES\|resolve_lead_binding\|lead_family\(\|model_tier\(\|_MODEL_TIER_SUBSTRINGS` `tools/` → 58 hits / 9 files: `mechanism_gate.py` 21, `test_mechanism_gate.py` 12 (A), `savings_report.py` 4 (A), `session_context.py` 4, `test_session_context.py` 5 (C), `dispatch_gate.py` 4 (D), `journal_echo.py` 3, `tier_echo.py` 3, `test_journal_echo.py` 2 (D). Grep `duplicate_model_id\|ROLE_RANKS\|"reserve"\|reserve:` → `mechanism_gate.py` 8, `test_mechanism_gate.py` 15 (A). Grep `-i lead queue` → `test_mechanism_gate.py:1085` `assert "Lead queue" in reason` (A — keep the words "Lead queue" in the new note). `.githooks/commit-msg:6` runs it (unchanged hook). `test_mechanism_gate_md.py` (13 `fable` hits — A, re-run) |
| `tools/journal_validator.py` | matrix by ranks; legacy table + `LADDER_FROM`; `agent: architect` no-matrix; `escalated` as new-task event for architect (F6); F5 WARN | Grep `TIER_ORDER\|AGENT_TIER\|QUEUED_TO_LEAD_AGENTS` `tools/` → 35 hits / 4 files: `journal_validator.py` 20, `test_journal_validator.py` 8 (B), `agents_md.py` 4, `test_agents_md.py` 3 (B — `tier_words` re-pointed). Text readers: `PROCESS/LEAD_RANKING_EXAM.md:29` (F), CLAUDE.md Routing-log `by` paragraph (L), `AGENTS.md:885` copy (L regen). Hooks: `.githooks/pre-commit:8`, `pre-merge-commit:18` (unchanged hook lines). Importers: `journal_echo.py` re-validates newest lines (unchanged code, behaviour follows) |
| `tools/journal_write.py` | ONLY if F6 is taken: `NEW_TASK_EVENTS` gains `escalated` for agent=architect | readers of `NEW_TASK_EVENTS`: the writer itself (stream B owns it under F6) |
| `tools/session_context.py` | MODEL line by function; ARCHITECT line; optional ESCALATED TO ARCHITECT | Grep `Lead tier = fable\|Lead\(top\)\|critic-tier` → 13 hits / 3 files: `session_context.py` 3, `test_session_context.py` 8 (C), `test_journal_validator.py` 2 (comments `:645`, `:706` — unchanged). `.claude/settings.json` SessionStart wiring — unchanged |
| `tools/tier_echo.py`, `tools/journal_echo.py`, `tools/dispatch_gate.py`, `tools/journal_hooks.py`, `tools/token_usage_stats.py` | read `FAMILIES`/`family_of` | their tests `test_tier_echo.py` (7 fable), `test_journal_echo*.py`, `test_dispatch_gate.py` (5), `test_journal_hooks.py` (2), `test_token_usage_stats.py` (6) — stream D, expected green with no edit (same words, same order) |
| `tools/savings_report.py` | F11; `_UNBOUND` → `lead_binding() is None` | `test_savings_report.py` (17 fable — A); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:535` (F) |
| `tools/agents_md.py` | `tier_words` reads the home | `test_agents_md.py:30,309-322` pins (B); `.githooks/pre-commit` runs `agents_md.py --check` (`MECHANISM_PREFIXES:272` comment) — AGENTS.md must be regenerated in the SAME commit as any CLAUDE.md edit (L) |
| `.claude/settings.json` | `"model"` → lead binding (F15) | no tool reads the key (P18); the pin row (F15) becomes its reader (C). Hook-count pins (`test_hook_liveness_probe.py`) unaffected: no hook added |
| `CLAUDE.md` | «Tiers» (+ architect line; Lead (Opus)); «Role ≠ tier» (§5.1-5.2); «Lead degradation» (§5.3); rule 10 tier line («below the lead binding» stays true); rule 11a apex unchanged; Routing log `by` paragraph (`TIER_ORDER` → the home); rule 7 label «"sonnet: …" / "opus: …"» unchanged | readers: `AGENTS.md` (generated copy — regen), `tools/install_parity_anchors.json:8,32` (anchors «Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)», «5. Flat delegation (flat delegation rule):» — KEEP those heading texts verbatim or update anchors in the same commit), `docs/FACTORY_RULES_INDEX.md`/`ARCHITECTURE_INDEX.md` (untouched), `tools/fixtures/host_pre_delivery_CLAUDE.md` (frozen), the parallel boot-by-topic spec (moves sections later) |
| `DECISIONS.md` | new D-nnnn: Lead → Opus, Architect → Fable, matrix by function, Opus exam deferred to a П3 node by the owner's word (D7) recorded as the `exam.on_failure` informed pass (P4 `:98-106`); D-0003 gets «superseded by D-nnnn» | readers: `MECHANISM_PREFIXES` (mechanism commit), calibration (Last decision), every session's boot |
| `docs/TWO_VOCABULARIES.md` | Lead row → Opus; new Architect row | `tools/tests/test_role_carriers_one_owner.py:73` (re-run, stream F) |
| `docs/SIBLING_MAP.md` | `:519`, `:522` rows deleted (D6); `:655-661` «Lead Queue» → `docs/tasks/lead-queue.md`; axis 1 role list (`:29`) unchanged (no architect role FILE), axis 1 table gains «ladder home» row; axis 2 Lead-exam row note «Opus candidate, П3 node» | readers: `tools/mechanism_gate.py` reads axis headings as gate keys (headings NOT renamed → no key change); `install_parity_anchors.json:524-528` path unit (unchanged) |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | checks 5, 6 (§5.5), 18 (F11), Architect's batch review as a step (F10) | readers: calibration sessions; `test_calibration_counts.py` (13 fable hits — counts by journal values, re-run in F; expected unchanged since `by` vocabulary is unchanged under F4-A) |
| `PROCESS/LEAD_RANKING_EXAM.md` | `:29-31` pointer + «Fable judges an Opus candidate» | readers: the П3 exam node |
| `PROCESS/PATCH_PROTOCOL.md` | `:22-23` drop «the onboarding skill's Upgrade mode, step 7»; keep the install-parity duty in its own words (F14) | readers: Lead at patching |
| `PROCESS/ARCHITECT_START.md` | new (§4.5) | reader: SessionStart pointer only |
| `.claude/agents/critic.md` | `:52-57` «below the top tier» → «below the Lead rank»; rule 10 (`:58-61`) unchanged (critic binding unchanged, D1) | harness; `agents_md.py` roles table (frontmatter unchanged → AGENTS.md unchanged by this file) |
| `.claude/skills/critic-exam-gen/SKILL.md` | `:163`, `:182` references to the onboarding skill (F14) | harness (skill index) |
| `.claude/skills/onboarding/`, `.claude/skills/next-task/` | DELETED (D6) | readers of the names: `docs/SIBLING_MAP.md:519,522` (F), `PROCESS/PATCH_PROTOCOL.md:23` (F), `docs/ADOPTION_LEDGER.md:3-4,23,52,77,143` (F), `delegation.config.yaml:34,39,95-96` (L), `critic-exam-gen/SKILL.md:163,182` (F); `tools/test_wiring_check.py:487-526` — synthetic repo, UNCHANGED; `install_parity_anchors.json:657-661` — dir unit, UNCHANGED (other skills remain); `AGENTS.md` — does not list skills (P32), UNCHANGED; history files (`docs/tasks/specs/*`, `reports/*`, `compact-snapshots/*`, Grep `next-task\|skills/onboarding\|onboarding skill` over `docs/` → 10 files) — history, UNCHANGED |
| `docs/ADOPTION_LEDGER.md` | onboarding-skill references → «retired 16.11.2026 (D-nnnn)» (F14) | readers: none in tools (Grep `delegation\.config` list above has none; it is a human record) |
| `docs/tasks/lead-queue-fable.md` → `docs/tasks/lead-queue.md`; new `docs/tasks/architect-queue.md` | F8 | readers: none in tools today (P23); after: `session_context.py` counts architect-queue items (C); `mechanism_gate.py` note (A); `docs/SIBLING_MAP.md:659` (F) |
| `plans/piles/forge/batch-7-vhodyashchie-4.md` | FG7-33 status «снят: заменён …»; FG7-14 row gets «зависит от потока A спеки 20261116-architect-tier» (F12) | `tools/piles.py check` reads the batch (untaken → editable, P33) |
| new П3 node «Lead exam for Opus» | in the next untaken forge batch + findings file + card row (PROJECT.md «Командная работа» п. 2) | `piles.py check`, `test_pile_cards_contents.py` |

---

## §7 Phases and parallel streams

Order: **A** first (the home; everything imports it) → **B, C, D, F** in parallel (disjoint owns) → **L** (Lead's own:
live config/settings/CLAUDE.md/DECISIONS.md, AGENTS.md regen, FG7 rows) LAST, because the live config switch flips
the gates for every session; until L lands, every stream must keep today's behaviour with today's config (the
home's tests run on fixture configs for BOTH worlds). Mechanism-path commits (A, B, C, D, F all touch
`MECHANISM_PREFIXES` paths) carry the axis block + `tier:` line; builders hand content, the Lead (Opus, after the
critic of the topic — ONE critic pass for the topic, R13-g) commits (enforcement-file review rule for anything
self-activating: `tools/session_context.py`, hooks).

Witness scope: these owns are outside the package → `scenario_walk.py --witness-for` has no row; the witness is
the test file that judges each path, named per stream (CLAUDE.md rule 4). No CI wait, no mutations (PROJECT.md
«Командная работа» п. 13). New test cases are ROWS of the existing tables; a new test file only under F2-a with the
owner's word (P34).

### Stream A — the ladder home + tier gate + savings

given: this spec §0, §2, §3.4 (tier-gate part), §4.5 step 5; `tools/mechanism_gate.py`; `tools/savings_report.py`; `delegation.config.yaml`; `docs/TESTING.md`
owns:
C:/QAFactory/forge-repo/tools/mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate_md.py
C:/QAFactory/forge-repo/tools/savings_report.py
C:/QAFactory/forge-repo/tools/test_savings_report.py
C:/QAFactory/forge-repo/tools/tier_ladder.py
C:/QAFactory/forge-repo/tools/test_tier_ladder.py
non-goals: no edit of `delegation.config.yaml`, `.claude/settings.json`, CLAUDE.md (stream L); no validator/session_context change; the last two owns exist only under F2-a with the owner's word
handoff: diff + witness + the four questions (rule 10) block for the Lead's mechanism commit
edges: §2.2 adversarial rows; §2.4 all four; config without `architect` key and with it give identical results for `tier: fable`; `reserve:` uncommented → WARN, not read; config > 64 KB → refused with door; `--list --since` with a bad date → exit 1 naming the form (as `--audit`, `:1082`); empty window → «0 commits», exit 0; `test_mechanism_gate.py:1085` keeps «Lead queue»
DoD: `python -m pytest tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q` (+ `tools/test_tier_ladder.py` under F2-a) green, with new table rows: lead=opus → `tier: opus` ok, `tier: fable` ok, `tier: sonnet` refused; duplicate id lead=critic=opus → rank lead; architect absent/present parity; closure test covers the home and the config
siblings: axis 34 (one road for the ladder), axis 1 (binding ↔ policy)
designer: this file

### Stream B — journal gate by function

given: §3 whole, §2.2; `tools/journal_validator.py`; `tools/journal_write.py` (F6 only); `tools/agents_md.py`
owns:
C:/QAFactory/forge-repo/tools/journal_validator.py
C:/QAFactory/forge-repo/tools/test_journal_validator.py
C:/QAFactory/forge-repo/tools/agents_md.py
C:/QAFactory/forge-repo/tools/test_agents_md.py
C:/QAFactory/forge-repo/tools/journal_write.py
non-goals: no rewrite of any journal line; no change to `by` vocabulary unless F4-B is taken; `journal_write.py` only under F6
handoff: diff + witness
edges: §3.1 every cell as a row; §3.4 a pre-`LADDER_FROM` `by: opus, agent: critic`, no basis → FAIL (legacy), the same post → OK; `by: "claude-opus-5-5"` → FAIL; `by: "lead"` → FAIL with door (F4-A); config absent → legacy ranks; F5 line → WARN text names «queued to itself»; `escalated` agent=architect with a fresh id → OK under F6, any other agent → still refused
DoD: `python -m pytest tools/test_journal_validator.py tools/test_agents_md.py -q` (+ `tools/test_journal_write.py` under F6) green; `python -B tools/agents_md.py --check` clean
siblings: axis 1 (journal ↔ policy)
designer: this file

### Stream C — SessionStart

given: §4.4, §5.4, F15; `tools/session_context.py`
owns:
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/test_session_context.py
non-goals: no new SessionStart hook; no reading of `PROCESS/ARCHITECT_START.md` content (pointer only)
handoff: diff + witness; the file is self-activating → content handed over, the Lead places it
edges: §5.4 all six cases; ARCHITECT line present only for function architect, directly after MODEL, survives the 25-line cut with 30 candidate lines; queue absent/unreadable/0 open; architect key absent → no line; settings model ≠ lead binding → one WARN line (F15)
DoD: `python -m pytest tools/test_session_context.py -q` green
siblings: axis 1
designer: this file

### Stream D — family readers

given: §2.3 rows for tier_echo, journal_echo, dispatch_gate, journal_hooks, token_usage_stats
owns:
C:/QAFactory/forge-repo/tools/tier_echo.py
C:/QAFactory/forge-repo/tools/dispatch_gate.py
C:/QAFactory/forge-repo/tools/journal_hooks.py
C:/QAFactory/forge-repo/tools/token_usage_stats.py
non-goals: `journal_echo.py` code unchanged (reads via tier_echo); FG7-14 (label carries role) NOT done here; no behaviour change
handoff: diff + witness
edges: order-sensitive pin `test_extract_declared_word_picks_first_known_tier_words_order` green; «mythos» still maps to Fable in token stats; `dispatch_gate.py` is shared with FG7-14 → function list of this stream: `_model_family`, `_FAMILY_NAMES` only (PROJECT.md «Командная работа» п. 3)
DoD: `python -m pytest tools/test_tier_echo.py tools/test_journal_echo.py tools/test_dispatch_gate.py tools/test_journal_hooks.py tools/test_token_usage_stats.py -q` green with no test edit
siblings: axis 14 (transcript readers: tier_echo/journal_echo), axis 34
designer: this file

### Stream F — rule texts outside CLAUDE.md, deletions

given: §4.5, §5.5, §6 rows for these files; F7, F8, F10, F11, F14
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
non-goals: CLAUDE.md, DECISIONS.md, config, settings (L); no SIBLING_MAP heading rename (gate keys)
handoff: diff + DOC-DISPATCH witness (rule 11: keys quoted from this spec before the run, script in full, a negative control)
edges: critic.md is a role file → `PROCESS/CRITIC_EXAM.md` re-run duty (`critic.md:58-61`) — the edit changes no duty of the critic, only the name of the rank; F: state «exam not re-run: wording only» in the commit or run it; `test_role_carriers_one_owner.py` after TWO_VOCABULARIES edit
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_calibration_counts.py -q` green + the key-presence run
siblings: axis 1, axis 2 (exam rows), axis 31 (role carriers)
designer: this file

### Stream L — Lead's own (after A-F are accepted)

`delegation.config.yaml` (bindings + `architect:` + comments), `.claude/settings.json` model (F15), CLAUDE.md
(«Tiers», «Role ≠ tier», «Lead degradation», Routing-log `by` paragraph), `DECISIONS.md` (new D + D-0003 note),
`python -B tools/agents_md.py` regen in the same commit as CLAUDE.md, `LADDER_FROM` constant value = this commit's
time (B leaves a placeholder the Lead fills — small choice C2), FG7-33/FG7-14 rows, the П3 exam node with its
finding and card row. Witness: the narrow sets of A-D re-run on the merged tree + `python -B tools/journal_validator.py`
+ `python -B tools/agents_md.py --check`; BATCH CANON on CI per RUNBOOK §7.

---

## Forks (returned; recommendation marked)

- **F1 — key of the new rung.** (a) rename `reserve` → `architect` **[recommended]**: the function has a name now,
  and the key matches the rule vocabulary; `reserve` is commented in every tracked copy (P2) so no live config
  breaks; an uncommented `reserve` gets a WARN with the rename door. (b) keep `reserve`: zero code rename, but the
  config says "reserve" while every rule says "Architect" — two names for one rung. (c) read both: two roads (P31).
- **F2 — where the home lives.** (a) new leaf `tools/tier_ladder.py` + `tools/test_tier_ladder.py`
  **[recommended]**: a leaf importable by hooks with no gate coupling; COST: a new test file — forbidden by
  `docs/TESTING.md:118` without the owner's word (precedent 14.11 exception, P34) → the Lead asks the owner.
  (b) inside `tools/mechanism_gate.py` (already owns ROLE_RANKS/LEAD_FAMILIES and is «the ONE reader of the Lead
  binding», `savings_report.py:63`); tests as rows of `test_mechanism_gate.py`; COST: journal_validator,
  session_context, tier_echo, dispatch_gate import a commit-msg gate module (+ pyyaml at import in the validator,
  which today imports no yaml). If the owner says no to (a), (b) is the road.
- **F3 — rank order: code constant vs config data.** (a) constant in the home **[recommended]**: the order is
  POLICY (CLAUDE.md), not a binding; the config's own header says «Changing a binding below does not change any
  rule» (`delegation.config.yaml:8`). (b) a `ladder:` list in the config: an operator edit could re-rank functions
  silently.
- **F4 — what `by` holds.** (A) model-family word, ranked through the home **[recommended]**: no writer change, no
  vocabulary migration, calibration reconciles a model word against transcripts. (B) function word (`lead`,
  `architect`, …) from a cutover ts: reads like the rule; COSTS: CLI/doc/door changes, a degraded Sonnet
  coordinator has no honest function word (`builder`?), and transcripts must be mapped back to functions anyway.
- **F5 — `queued-to-lead` written by a Lead-ranked acceptor.** (a) WARN **[recommended]** (pre-cutover lines merged
  late stay legal; the mark is misleading, not dangerous). (b) silent pass (today's branch order). (c) FAIL.
- **F6 — `escalated` to the Architect with no task yet.** (a) `escalated` with `agent: architect` may open a task id
  (joins `NEW_TASK_EVENTS`) **[recommended]**. (b) escalate only on an existing task; a fresh idea first gets a
  `decomposable`/dummy event (an event that lies about what happened). (c) no journal line, queue item only
  (breaks D8 «пишет `escalated`»).
- **F7 — where the start checklist lives.** (a) `PROCESS/ARCHITECT_START.md`, pointed to only by the SessionStart
  ARCHITECT line **[recommended]**: zero bytes for other sessions. (b) a skill `.claude/skills/architect-start/`:
  its description loads into every session's skill index. (c) a BOOT.md section: every restore pays it.
- **F8 — queue carriers.** (a) two files: `lead-queue.md` (renamed) + new `architect-queue.md` **[recommended]**;
  fixes the non-existent CURRENT_CONTEXT «Lead Queue» (P10, P29). (b) rename the old file into the Architect queue
  and create the CURRENT_CONTEXT section for the Lead queue (CURRENT_CONTEXT is «only the state of main, ≤ 10 KB»,
  PROJECT.md «Командная работа» п. 5).
- **F9 — the "last Architect review" marker.** (a) the existing `calibrated` event gains an optional typed field
  `reviewed_through: <sha>` **[recommended]** (typed-fields rule; one validator rule). (b) a token
  `reviewed-through:<sha>` in notes (the `closes:` pattern; no schema change, but a load-bearing fact in prose).
  (c) a line in `architect-queue.md` (outside the journal: not seen by calibration counters).
- **F10 — who runs the weekly calibration.** (a) the Architect **[recommended]**: calibration judges the Lead's own
  acceptance and degradation — a Lead calibrating itself is self-certification; D3 ties the batch review to it.
  (b) the Lead runs it, the Architect reviews only the mechanism part.
- **F11 — savings counterfactual.** (a) lead binding (Opus), relabelled «coordinator model» **[recommended]**: the
  report measures what delegation saves against the coordinator doing it all; the Architect is rare.
  (b) architect binding (keeps the literal «top-tier»; inflates savings by Fable's price).
- **F12 — FG7-14 (label carries the role).** (a) stays independent, depends on stream A (reads the home's
  bindings) **[recommended]**; (b) absorbed here (widens a P1 change with a dispatch-label redesign).
- **F14 — the deleted onboarding skill's procedures (binding change + exam gate; Upgrade step 7).** (a) retire the
  references; PATCH_PROTOCOL keeps the install-parity duty in its own words; the config comment says «a rebinding
  is a D-entry + the tier's exam» **[recommended]**. (b) inline the old binding steps into the config comment
  (copies a procedure the owner called stale).
- **F15 — session default model + pin.** (a) `.claude/settings.json` `model` = the lead binding (Opus) and a
  SessionStart WARN row when they differ **[recommended]**: the owner opens Lead sessions by default and switches
  to Fable herself (D8). (b) keep Fable as default: every new session starts as Architect and pays Fable price for
  Lead work. (c) (a) without the pin.
- **F18 — legacy table for pre-switch lines.** (a) `LADDER_FROM` + legacy pair **[recommended]** (§3.4).
  (b) no cutover: simpler, legalises old self-certifications on a late merge.
- **F21 — who writes the Architect's decision line in DECISIONS.md.** (a) the Architect session writes it itself
  (it is above Lead; PROJECT.md «Командная работа» п. 5 «пишет только Lead владельца» read as «Lead rank or above»)
  **[recommended]**. (b) the Opus Lead transcribes it (one writer function, an extra hop and a paraphrase risk).

## Small technical choices closed by the designer

- C1. `FAMILIES` order weakest → strongest (matches `TIER_ORDER` and `KNOWN_TIER_WORDS`, P12/P19); strongest-first
  readers reverse.
- C2. `LADDER_FROM` value is filled by the Lead at the stream-L commit (the switch moment), not by a builder.
- C3. The home refuses a config file > 64 KB with a door (input from outside: the magnitude case); 64 KB ≈ 40× the
  current file.
- C4. `token_usage_stats` keeps its display capitalisation locally; only recognition moves to the home.
- C5. The ARCHITECT line sits directly after MODEL (survives the 25-line cut by position).
- C6. `agent: "architect"` takes the same no-matrix branch as `agent: "lead"`.
- C7. No architect ROLE FILE in `.claude/agents/`: the Architect is a session, never a subagent (D8); axis 1's role
  list stays four.

## Noticed in the brief (reported, scope not widened)

- `tools/journal_write.py LEAD_ROWS` is not a family carrier (P20).
- `tools/install_parity_anchors.json` does not name the two skills (dir unit, P31); `AGENTS.md` does not list skills
  (P32) — both unchanged by D6.
- Extra family carriers not in the brief: `tools/token_usage_stats.py:172`, `tools/journal_hooks.py:210` (P19).
- `delegation.config.yaml` is outside the mechanism net today (P11) — after this spec it decides acceptance.
- `escalated` cannot open a task (P15) — D8 needs F6.
- `docs/TESTING.md:118` forbids a new test file (F2).
- The onboarding skill is also referenced by `PROCESS/PATCH_PROTOCOL.md`, `docs/ADOPTION_LEDGER.md`,
  `critic-exam-gen/SKILL.md` (P30).
- `--audit --since` does not list commits (P35) → a new `--list` mode.
- The validator today accepts an Opus Lead's acceptance of critic work only via `queued-to-lead` — i.e. the live
  code would force the new Lead to queue work to itself (P13 `:779-781`), the concrete reason stream B is not
  optional.
- Analog not touched: `PROCESS/DEPLOYMENT_ECONOMY_EXAM.md:238` «subagent on your top tier» — generic text, unchanged.

## Reading trail

Read: `delegation.config.yaml` (whole); `tools/mechanism_gate.py:90-114, 208-283, 575-884, 945-994` + greps for
`ROLE_RANKS|resolve_lead_binding|…`, `--audit`, `MECHANISM_PREFIXES`; `tools/journal_validator.py:340-379, 645-810,
960-999, 1067-1106, 1280-1304, 2070-2098` + greps; `tools/session_context.py:215-229, 975-1035, 2149-2228`, grep
`MAX_LINES`; `tools/tier_echo.py:110-149`; `tools/dispatch_gate.py:190-209, 1020-1069`; `tools/journal_echo.py:630-669`;
`tools/journal_hooks.py:195-219`; `tools/savings_report.py:55-94, 118-142`; `tools/agents_md.py:190-234`;
`tools/token_usage_stats.py:165-184`; `tools/journal_write.py:68-82` + greps; `tools/install_parity_anchors.json:495-669`
+ grep; `.claude/settings.json:1-8`; `.claude/agents/critic.md:1-12, 48-61`; `docs/TWO_VOCABULARIES.md:1-25`;
`docs/SIBLING_MAP.md:24-68, 150-161, 505-534, 640-662` + axis heading grep; `docs/TESTING.md:118-147`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:95-134` + greps; `PROCESS/PATCH_PROTOCOL.md:18-27`;
`docs/tasks/lead-queue-fable.md:1-40`; `plans/piles/forge/batch-7-vhodyashchie-4.md:1-14` + FG7 greps;
greps on `DECISIONS.md` (D-0003), `CURRENT_CONTEXT.md`, `BOOT.md`, `PROJECT.md`, `DELEGATION_TABLE.md`, `AGENTS.md`,
`PROCESS/LEAD_RANKING_EXAM.md`, `docs/ADOPTION_LEDGER.md`, `.claude/skills/*` (critic-exam-gen, scout-exam-gen,
boot-diet), `logs/journal/` counts. Not read: the bodies of the two skills to be deleted (deletion needs only their
readers); `docs/tasks/specs/20261116-boot-by-topic-spec.md` (parallel, being drafted).

## Lead decisions on the forks (Lead, 17.11.2026) -- the plan critic reviews the spec WITH these

Technical forks, decided by the Lead (each is the recommended option): F1 (a) `architect`; F3 (a) constant in the home;
F4 (A) `by` keeps the model-family word; F5 (a) WARN; F6 (a) `escalated` with `agent: architect` may open a task id;
F7 (a) `PROCESS/ARCHITECT_START.md`; F8 (a) two queue files; F9 (a) typed field `reviewed_through`; F11 (a) lead binding;
F12 (a) FG7-14 independent, after stream A; F14 (a) retire the references; F18 (a) `LADDER_FROM` + legacy pair.

Asked of the owner, executable on the recommendation until her word: F2 (a new leaf `tools/tier_ladder.py` with its own
test file -- `docs/TESTING.md` needs the owner's word; without it, option (b) inside `tools/mechanism_gate.py`);
F10 (a) the Architect runs the weekly calibration; F15 (a) session default model = the lead binding, WARN on a difference
(`.claude/settings.json` is changed only after the owner's word -- stream L holds that one line until then);
F21 (a) the Architect writes its own decision line.
