# FG7-14 - the dispatch label carries the role, not the model (draft card)

task: t-1420 | node: forge/7/FG7-14 | feature: F19 | designer draft 18.11.2026 | status: DRAFT, for the Lead's acceptance
source: `plans/piles/forge/batch-7-vhodyashchie-4.md` row FG7-14; finding
`plans/piles/forge/findings/20261111-metka-dispatcha-neset-rol-d-0016-ne-sdelano.md`; D-0016 (`docs/DECISIONS_ARCHIVE.md:184`).

## 0. Target on main, measured (file:symbol)

Measured on the root checkout (branch `main`, HEAD 63e511cf per the session's git snapshot; whether the root matches
origin/main is not verified here: estimate, the Lead runs `git -C C:/QAFactory/forge-repo fetch` + `rev-parse`).

| # | fact | carrier |
|---|---|---|
| M1 | Check 3 is a FORM check only: `description`, if present, must match `^\S+[ :-]`; absent -> skipped | `tools/dispatch_gate.py::LABEL_MODEL_PREFIX_RE` (:401), `::decide_full` (:880-882), docstring item 3 (:87-95) |
| M2 | The refusal text still says the tier: «The dispatch label starts with the worker's tier (rule 7): e.g. 'sonnet: ...'» | `tools/dispatch_gate.py::BLOCK_MESSAGE_NO_LABEL` (:574-577) |
| M3 | The label-vs-tier comparison the finding names is NOT check 3: it is the non-blocking WARN layer, label family vs the role file's `model:` | `tools/dispatch_gate.py::role_type_warn` (:1197-1261), `::_find_agent_role_model` (:1162), `::_LABEL_LEADING_TOKEN_RE` (:1101) |
| M4 | The journal dispatch hook writes `delegated` ONLY when the description opens with a tier word; the model written is that word's family | `tools/journal_hooks.py::_post_agent` (:208-212) via `tools/dispatch_gate.py::label_model_family` (:1113-1125) |
| M5 | The hook already ignores the label for everything else: agent = `subagent_type` (:213), `notes` = the cut description (:256) | `tools/journal_hooks.py::_post_agent` |
| M6 | The rule text lives in COORDINATOR.md, not CLAUDE.md: «The visible dispatch label (`description`) starts with the worker's model: "sonnet: …" / "opus: …"» | `COORDINATOR.md` rule 7 (:195-199); mirrored in generated `AGENTS.md:351-352` |
| M7 | Live CLAUDE.md has no rule 7 and no host-adaptation list (sections: Worker duties, rule 11, Command hygiene, Язык) | `CLAUDE.md` (read whole at session start); history of clauses: `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` (Grep `dispatch label|sonnet: ` -> 0 hits there; control: the same Grep finds `COORDINATOR.md:195`) |
| M8 | Role files carry no label form | Grep `(?i)sonnet: |tier word|dispatch label` in `.claude/agents` -> 0; control `(?i)sonnet|description\b` same path -> 8 hits |
| M9 | `designer` has NO config row by decision: «`designer` has no row here: it is bound in its role file's frontmatter»; the ladder never reads the config for it | `delegation.config.yaml:4-5, :32-33`; `tools/tier_ladder.py:24-27` (`COORDINATION_FUNCTIONS` = scout, builder, critic, lead, architect) |
| M10 | Role files bind: scout/builder `claude-sonnet-5-5`, critic/designer `claude-opus-5-5`, judge `sonnet` | `.claude/agents/*.md` frontmatter `model:` (Grep `^(name|model):`) |
| M11 | `journal_echo` reads the journal line's `model` field, never the label | `tools/journal_echo.py::_extract_declared_word` (:637-663) |
| M12 | `tier_echo` reads `payload["description"]` on SubagentStop (a field the payload practically never carries) for an optional MISMATCH | `tools/tier_echo.py::_extract_declared_tier` (:158-173), docstring :19-31 |
| M13 | The one config FILE reader: absent -> None, unreadable -> None + one WARN; callers then use `DEFAULT_BINDINGS` | `tools/journal_validator.py::read_config_text` (:601-625); used by `tools/journal_write.py:591` |
| M14 | Model-word labels in test fixtures that go through `dispatch_gate.decide` (directly or via owns_gate / critic_snapshot): test_dispatch_gate 98, test_dispatch_gate_md 13, test_owns_gate 14, test_owns_gate_retry 2, test_owns_gate_md 1, test_critic_snapshot 2, test_dispatch_cut 2; probe `tools/hook_liveness_probe.py` 6 (cases 1, 2, 2a, 10, 17, 18) | Grep `"description":\s*"(sonnet|opus|haiku|fable|claude)|description="(sonnet|...)` over `tools/` (count) |
| M15 | None of the six non-gate test files asserts on ROLE-TYPE / `label_model_family` / the label message | Grep `ROLE-TYPE|label_model_family|role_type_warn|BLOCK_MESSAGE_NO_LABEL|worker's tier` -> 0 in those six; the same glob finds their 34 label strings |
| M16 | `dispatch_new.py` calls `decide_full` with no description: «no description, so no label check» | `tools/dispatch_new.py:11` |
| M17 | `dispatch_gate.py` and `journal_hooks.py` are mechanism paths (live hooks) | `tools/mechanism_gate.py::MECHANISM_PREFIXES` (:239, :289) |
| M18 | Async launch responses carry `resolvedModel` | `tools/negative_lint.py:203-207`; fixture `tools/test_journal_hooks.py:70` |

## 1. What stream A of the architect-tier spec already did, and what remains

Done (stream A + stream D of `docs/tasks/specs/20261116-architect-tier-spec.md`, merged 17.11):
- The role -> model resolver exists: `tools/tier_ladder.py::effective_bindings` (the ONE reader of `roles.<function>`,
  `DEFAULT_BINDINGS` on absent/broken config), `::family_of`, `::COORDINATION_FUNCTIONS`.
- `dispatch_gate._FAMILY_NAMES` / `_model_family` and the hook's door text read the ladder home (`dispatch_gate.py:1088-1110`,
  `journal_hooks.py:211`).
- The spec itself says FG7-14 was left out: stream D non-goal «FG7-14 (label carries role) NOT done here» (spec :783);
  F12 «DECIDED (a) independent, after stream A» (spec :880).

Remains (this node): M1, M2 (check 3 and its message), M3 (the WARN layer's label premise), M4 (the hook's model
source), M6 (the rule text, a Lead edit), AGENTS.md regeneration. Nothing in stream A has to be redone.

Correction to the finding: it says check 3 compares the model family with the label; measured, check 3 is form-only (M1)
and the family comparison is the WARN layer (M3). The finding's item 4 points at CLAUDE.md host adaptations; measured,
the rule is COORDINATOR.md rule 7 (M6, M7).

## 2. Architecture

- AR-13 (one reader per fact, applied by analogy: no package file is touched): bindings are read only through
  `tier_ladder.effective_bindings`; the config file only through `journal_validator.read_config_text`; role files only
  through `dispatch_gate._find_agent_role_model`. The node adds no parser. Change check: Grep `yaml|safe_load|model:` in
  the diff of card A -> no new reader.
- AR-29 (a code check judges data): new check 3 judges the SHAPE of one payload against another field of the same
  payload (label prefix == `subagent_type`). Owner: data (code). It judges no role's judgment. The census line does
  not apply: a forge tool, outside the package census.
- AR-1 (closed variety is a data row): where a role is bound is decided by the existing data
  `tier_ladder.COORDINATION_FUNCTIONS` (config) with the role file as the default carrier (M9). No new list of role
  names in code.
- `variety: none -- forge tools outside ai-packages/qa-factory; the role vocabulary is the payload's own subagent_type, compared as data`.
- Mechanism commit (M17): the acceptance commit carries the four questions block and the tier line in the form
  `tools/mechanism_gate.py` checks (pointer only; the grammar is not copied here). Self-activating files: the builder
  works in its worktree; the Lead places both hooks by the merge after the critic (CLAUDE.md, Worker duties).

## 3. Design

D1. Check 3 (in `decide_full`, still LAST: completeness -> handoff -> facts -> path -> label). With `description`
present: let `role = subagent_type.strip()`. Passes when `description.lower()` starts with `role.lower() + ":"`.
Otherwise refused (exit 2) with a message that names the expected form WITH this dispatch's role, e.g.
«The dispatch label starts with the worker's role (COORDINATOR.md rule 7, D-0016): 'builder: ...'. The model comes
from the role's binding; the label names no model.» `subagent_type` absent / blank / not a string: see F3 (recommended:
refused, the message names the missing `subagent_type`). `description` absent: check 3 skipped (unchanged; M16 relies on it).
`LABEL_MODEL_PREFIX_RE` and `_LABEL_LEADING_TOKEN_RE` are deleted along with their last readers.

D2. One public resolver `dispatch_gate.role_bound_model(subagent_type, config_text, agents_dir=AGENTS_DIR) -> tuple[str | None, str]`
(model id or None, a road note). It replaces `label_model_family` as the hook's reader.
- role (lowercased, stripped) in `tier_ladder.COORDINATION_FUNCTIONS` -> `tier_ladder.effective_bindings(config_text)[0].get(role)`;
  road `delegation.config.yaml roles.<role>`, or `default bindings (<note>)` when the ladder defaulted; no model ->
  `(None, "roles.<role> names no model")`.
- any other role (designer, judge, a project role, a harness built-in) -> the role file's `model:` via
  `_find_agent_role_model` (which gains the `agents_dir` parameter, default `AGENTS_DIR`); none -> `(None, "no binding:
  not a delegation.config.yaml function and no model: in .claude/agents for '<role>'")`.
- Never raises (non-string input -> `(None, "no role")`).

D3. `journal_hooks._post_agent`: the model is no longer read from the description. Order: `subagent_type` check first
(existing door), then `config_text = journal_validator.read_config_text(root)` (`root` = the journal's repo root,
`jw.repo_root(cwd)`, so the hook and the journal read the same repo), then `role_bound_model`. Written `model` =
`tier_ladder.family_of(bound)` or the bound id when it has no family (F7). `None` -> no line, the door
«the dispatch's role '<role>' has no bound model (<road>), and the hook writes no model it did not read». A defaulted
road appends to the done line «; model by default bindings (delegation.config.yaml absent or unreadable)». F5: an
explicit `tool_input["model"]` (non-empty string) wins over the binding (recommended).

D4. `role_type_warn` (F4, recommended (b)): the family-mismatch branch and every description read are removed; the
layer warns only when `subagent_type` has no role file (PROJECT / BUILTIN texts kept, «declared tier '<x>'» dropped
from both, the shared prefix «ROLE-TYPE WARN: » and the substring «no role file» kept byte for byte). A divergence
between the config binding and a role file's `model:` surfaces through the measurement: the hook declares the config
binding, `journal_echo` measures the transcript and prints MISMATCH (COORDINATOR.md rule 7, «closes by MEASUREMENT»).

D5. Not changed: `journal_echo` (M11), `tier_echo` (F6, recommended), `journal_write.py` CLI door, `owns_gate`,
`critic_snapshot`, `dispatch_new`, `.claude/settings.json`, `tier_ladder.py`, `delegation.config.yaml`.

D6. Lead edits (not builder): COORDINATOR.md rule 7 sentence (proposed text in § 9), `python -B tools/agents_md.py`
regeneration of AGENTS.md (rule 7 mirror + the hooks row built from `dispatch_gate.py`'s first docstring paragraph),
the FG7-14 pile row (owns `CLAUDE.md` -> `COORDINATOR.md`, Lead edit). All three in the acceptance commit of card A.
CLAUDE.md: no edit (M7).

## 4. Edges, each with its invariant

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | role and no model: `builder: fix x`, subagent_type builder | passes; hook writes the binding's family | the first token the operator sees is the role the harness loads, never another role |
| E2 | model and no role: `sonnet: fix x` (legacy). BEFORE card A: passes check 3, hook writes `sonnet`. AFTER: refused, message shows `builder: ...`; a payload that reaches the hook anyway (bypass, replay) is recorded by its `subagent_type`'s binding | after the change no model is ever read from a label |
| E3 | today's Lead form `sonnet: builder — x` | AFTER: refused (first token is not the role) | one form; no prefix-scan for a role further inside the label |
| E4 | role absent from the config: (a) a coordination function with no model in a readable config; (b) designer / judge / project role; (c) a harness built-in with no role file (`general-purpose`) | check 3 judges the label only and passes all three (F2); hook: (a) door naming `roles.<role>`, (b) the role file's `model:`, (c) door naming the role; `role_type_warn`: (c) BUILTIN WARN | the journal never records a model no carrier names (E-B23-3 kept); a missing binding never blocks a dispatch |
| E5 | unreadable config: non-UTF-8, OS error, YAML alias/anchor, > 64 KB, no `roles`, no lead model, pyyaml missing | `read_config_text` -> None or text the ladder defaults; hook writes the DEFAULT_BINDINGS family and says «default bindings» on its done line; check 3 reads no config at all | a broken config never blocks a dispatch and is never recorded silently as the deployment's binding |
| E6 | TEMPORAL, the journal hook, both worlds: BEFORE = gate accepts any `^\S+[ :-]`, hook records only tier-word labels; AFTER = gate accepts only `<subagent_type>:`, hook ignores the label. The move that creates AFTER is the merge of card A (gate + hook in ONE commit, with the Lead's rule text) | a hook-only change is safe in both worlds (it does not read the label); a gate-only change would leave every dispatch unrecorded | no commit on main where the gate's accepted set and the hook's recordable set are disjoint |
| E7 | in-flight dispatch across the merge (delegated before, stop after) | `returned` reuses the `delegated` line's model (`known.get("model")`, unchanged) | a stop never re-resolves a model |
| E8 | `subagent_type` absent / blank / non-string with a description | F3 (recommended: refused naming `subagent_type`) | the gate never passes what the recorder cannot record (`journal_hooks.py:214-215` door) |
| E9 | description: absent -> skipped; `""` / whitespace / leading space ` builder: x` -> refused; non-string -> refused (no exception any more); 1 MB starting with the role -> passes in O(len(role)) | outside input: magnitude, emptiness, type | check 3 never raises and never scans the whole label |
| E10 | encoding: `BUILDER: x` passes (lower()); Cyrillic homoglyph `buіlder: x` refused; any text after the colon (Cyrillic, emoji) passes | | the compare is exact on the role's characters |
| E11 | role with a hyphen `general-purpose: x` | passes (prefix compare, not a lazy token regex) | a role containing `-` or a space is never cut at its first separator |
| E12 | POSITIONAL: check 3 stays after completeness / handoff / facts / path | a dispatch failing completeness AND the label gets the completeness message (existing `test_priority_*` rows) | the F3 refusal lives inside check 3, so it never pre-empts an earlier refusal |
| E13 | Agent tool `model` parameter present (F5) | recommended: it is the declared model for the journal line | a stand-in dispatch (COORDINATOR.md rule 6 outage clause) is never recorded as the bound model |
| E14 | `role_type_warn` after D4: known role file -> silent whatever the label; no file -> WARN; agents dir missing -> silent; any exception -> "" | | the layer stays informational: never exit 2 |

Conflicting requirement pairs, named: finding item 2 «role without a config binding -> refusal» vs D-0067 / M9 «designer
has no config row» -> F2. Finding item 4 «CLAUDE.md host adaptation» vs M6/M7 -> the COORDINATOR.md Lead edit (D6).

## 5. Builder cards (R11-f)

### Card A - the gate, the resolver, the hook

task: <Lead issues>
node: forge/7/FG7-14
feature: F19
given: this draft §§ 0-4; `tools/dispatch_gate.py`; `tools/journal_hooks.py`; `tools/tier_ladder.py`; `tools/journal_validator.py::read_config_text`; `tools/hook_liveness_probe.py`; `docs/TESTING.md`
owns:
C:/QAFactory/forge-repo/tools/dispatch_gate.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate.py
C:/QAFactory/forge-repo/tools/journal_hooks.py
C:/QAFactory/forge-repo/tools/test_journal_hooks.py
C:/QAFactory/forge-repo/tools/hook_liveness_probe.py
non-goals: no edit of COORDINATOR.md, AGENTS.md, CLAUDE.md, tier_ladder.py, journal_validator.py, delegation.config.yaml, .claude/agents, tier_echo.py, journal_echo.py; no test file outside owns (cards B, C); no commit (the Lead commits, mechanism commit)
handoff: diff + witness + the four questions block (rule 10) for the mechanism commit + the list of rewritten/deleted test rows
edges: E1-E14 of this draft (the forks as the Lead closed them); check 3 stays last (E12); hook-and-gate in one diff (E6)
DoD: `python -m pytest tools/test_dispatch_gate.py tools/test_journal_hooks.py -q` green, then `python -B C:/QAFactory/forge-repo/tools/hook_liveness_probe.py --json` with cases 1, 2, 2a, 10, 17, 18 ok
siblings: SIBLING_MAP axis 34 (one road for the ladder), axis 1 (binding <-> policy); the journal dispatch hook; dispatch_gate check 3; tier_echo (unchanged, F6); journal_echo (unchanged, M11)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-14-dispatch-label-role-card.md

Items:
- A1 `dispatch_gate.py::decide_full` check 3 per D1; `BLOCK_MESSAGE_NO_LABEL` -> a template carrying the role (and the
  F3 text); docstring item 3, the first paragraph («starts with the worker's role»), the decide_full docstring (no
  raise on a non-string description). Delete `LABEL_MODEL_PREFIX_RE`, `_LABEL_LEADING_TOKEN_RE`, `label_model_family`.
- A2 `dispatch_gate.py::role_bound_model` per D2; `_find_agent_role_model(subagent_type_norm, agents_dir=AGENTS_DIR)`.
- A3 `dispatch_gate.py::role_type_warn` per D4 (F4 as closed); `ROLE_TYPE_WARN_MISMATCH` deleted if F4 (b); module
  docstring «Role-type WARN layer» rewritten to the new contract.
- A4 `journal_hooks.py::_post_agent` per D3; the old door text (:211) replaced.
- A5 `hook_liveness_probe.py`: labels of cases 1, 2, 2a, 10, 17, 18 -> `<subagent_type>: ...`; expected verdicts unchanged.
- A6 fixture labels in `test_dispatch_gate.py` / `test_journal_hooks.py` -> `<subagent_type>: ...` (helpers build the
  label from the subagent_type they pass).

test lines (strongest first; stop when test lines reach code lines, report the rest as not written):
- test: tools/test_dispatch_gate.py::a new parametrized table for check 3 (rows E1, E2, E3, E9, E10, E11, E8) | expected from: this draft D1, E1-E3, E8-E11; D-0016
- test: tools/test_journal_hooks.py::a table «the model written is the binding of subagent_type» (scout default -> sonnet; a tmp-repo config binding critic -> opus; a tmp `.claude/agents/designer.md` model -> opus; legacy label `haiku: x` with critic -> opus; non-UTF-8 config -> default + the line says so; F5 row) | expected from: D3, E2, E4(b), E5, E13
- test: tools/test_journal_hooks.py::NOT_RECORDED rows: `description_without_tier_word` -> `role_without_binding` (general-purpose, no role file) and `coordination_role_without_model` (config without `roles.builder`); `description_missing` moves OUT (now recorded) | expected from: D3, E4(a)(c)
- test: tools/test_dispatch_gate.py::role_type_warn rows (known role silent under any label; no role file -> PROJECT / BUILTIN; mismatch rows deleted) | expected from: D4, E14

Cost (docs/TESTING.md «Бюджет»): code about +60 / -90 lines in dispatch_gate.py, +20 / -6 in journal_hooks.py; new
test rows about 25-30 (two tables + rows); fixture label rewrites are edits, not new lines (about 100 strings). Two
whole test files + one probe run; none is in a slow list or `canon_only` (Grep of `slow_tests.json` /
`test-layers.json` for these names -> 0; control finds `test_story_step`).

### Card B - owns_gate fixtures (world-agnostic)

task: <Lead issues>
node: forge/7/FG7-14
feature: F19
given: this draft § 5 card B; the three files below
owns:
C:/QAFactory/forge-repo/tools/test_owns_gate.py
C:/QAFactory/forge-repo/tools/test_owns_gate_retry.py
C:/QAFactory/forge-repo/tools/test_owns_gate_md.py
non-goals: no code edit; no assertion changed; no payload semantics changed (subagent_type stays as it is); no commit
handoff: diff + witness; any test whose assertion depends on the tier word is NOT rewritten and is returned as a question (measured expectation: 0, M15)
edges: a helper's default label becomes `f"{subagent_type}: ..."`; a fixture with a description and no subagent_type -> returned as a question, not changed
DoD: `python -m pytest tools/test_owns_gate.py tools/test_owns_gate_retry.py tools/test_owns_gate_md.py -q` green
siblings: card A (the new check 3); `<subagent_type>: x` passes the old `^\S+[ :-]` and the new rule alike, so this card lands before or with A
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-14-dispatch-label-role-card.md

Items: 17 label strings (M14) -> `<subagent_type>: <same text>`.
test: none -- fixture text only, no behaviour | expected from: this draft § 5 card B

### Card C - dispatch_gate_md / critic_snapshot / dispatch_cut fixtures (world-agnostic)

task: <Lead issues>
node: forge/7/FG7-14
feature: F19
given: this draft § 5 card C; the three files below
owns:
C:/QAFactory/forge-repo/tools/test_dispatch_gate_md.py
C:/QAFactory/forge-repo/tools/test_critic_snapshot.py
C:/QAFactory/forge-repo/tools/test_dispatch_cut.py
non-goals: no code edit; no assertion changed; no commit
handoff: diff + witness; a tier-word-dependent assertion is returned as a question (expected 0, M15)
edges: `test_critic_snapshot.py::_blocked_critic_payload` keeps `nomodelprefixlabelatall` (refused in both worlds); its docstring (:353-360) loses the `LABEL_MODEL_PREFIX_RE` reference (card A deletes the name) and says «no `critic:` prefix»
DoD: `python -m pytest tools/test_dispatch_gate_md.py tools/test_critic_snapshot.py tools/test_dispatch_cut.py -q` green
siblings: card A; same world-agnostic property as card B
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-14-dispatch-label-role-card.md

Items: 17 label strings (M14) -> `<subagent_type>: <same text>`; the docstring above.
test: none -- fixture text only, no behaviour | expected from: this draft § 5 card C

Order: B and C in parallel, any time (green in both worlds); A next; the Lead's D6 edits ride A's acceptance commit.

## 6. Readers of every touched file

The `tools/owns_readers.py` block was NOT attached (facts: none). Hand grep below; the Lead runs
`python -B tools/owns_readers.py --paths tools/dispatch_gate.py tools/journal_hooks.py tools/hook_liveness_probe.py COORDINATOR.md --names LABEL_MODEL_PREFIX_RE _LABEL_LEADING_TOKEN_RE label_model_family BLOCK_MESSAGE_NO_LABEL role_type_warn ROLE_TYPE_WARN_MISMATCH _find_agent_role_model`
(flags as the designer rules quote them; estimate) and the plan critic answers its block under Q13 (d).

Hand grep: `label_model_family|LABEL_MODEL_PREFIX_RE|_LABEL_LEADING_TOKEN_RE|BLOCK_MESSAGE_NO_LABEL|role_type_warn` over
`tools/` -> 113 hits in 5 files (dispatch_gate 18, test_dispatch_gate 91, test_critic_snapshot 2, journal_hooks 1,
dup-baseline.json 1). `get("description")` over non-test `tools/*.py` -> 12 lines in 6 files.

| touched file | reader | answer |
|---|---|---|
| tools/dispatch_gate.py | tools/journal_hooks.py:209 (`label_model_family`) | changes in card A (D3) |
| | tools/owns_gate.py:1112 (`dispatch_gate.decide`) | code unchanged; verdict changes for model labels; its tests in card B |
| | tools/critic_snapshot.py:134 (`decide`) | code unchanged; its tests in card C |
| | tools/dispatch_new.py:11 (`decide_full`, no description) | unchanged: absent -> skipped is kept (D1) |
| | tools/test_critic_snapshot.py:356-358 (names `LABEL_MODEL_PREFIX_RE` in a docstring) | changes in card C |
| | tools/test_dispatch_gate.py | changes in card A |
| | tools/test_dispatch_gate_md.py, test_dispatch_cut.py | fixture labels, card C |
| | tools/test_owns_gate*.py | fixture labels, card B |
| | tools/hook_liveness_probe.py cases 1, 2, 2a, 10 | changes in card A |
| | tools/dup-baseline.json (9 entries name dispatch_gate.py) | unchanged by hand; line shifts are judged by the dup check at batch canon (estimate) |
| | tools/mechanism_gate.py:239 `MECHANISM_PREFIXES` | unchanged; makes the acceptance commit a mechanism commit |
| | AGENTS.md:1104 (hooks row from the first docstring paragraph) | changes by the Lead's regen (D6) |
| | .claude/settings.json PreToolUse Task|Agent entry | unchanged (the command is not edited; file not read in this draft) |
| tools/journal_hooks.py | tools/dod_gate.py (`record_returned`) | unchanged (E7) |
| | tools/hook_liveness_probe.py cases 17, 18 | changes in card A |
| | tools/test_journal_hooks.py | changes in card A |
| | tools/mechanism_gate.py:289 | unchanged |
| tools/hook_liveness_probe.py | tools/test_hook_liveness_probe.py (Grep -i `description|journal_hooks` -> 0; the same call counts its `def test_` lines) | unchanged |
| | .githooks/post-merge (runs the probe; mechanism_gate.py:283 comment) | unchanged |
| COORDINATOR.md (Lead) | AGENTS.md:347-352 (generated mirror) | Lead regen, same commit (pre-commit enforces, SIBLING_MAP:105-107) |
| | boot-by-topic / SessionStart `COORDINATOR RULES:` (heading «Rule 7 · background by default») | unchanged: the heading is kept |
| tools/tier_echo.py (NOT touched) | reads `description` on SubagentStop | unchanged (F6): a role word never equals a family word, so its optional branch stays as inert as it is today |
| tools/journal_echo.py (NOT touched) | reads the journal `model` | unchanged (M11); now receives the binding's family |
| tools/session_retro.py:128, tools/owns_gate.py:1075 | read the description as opaque text | unchanged |

## 7. Forks (returned, not decided)

- F1 Transition: accept both label forms for a while? (a) one form at once; (b) both until the taken batches end.
  Recommend (a): P31; every dispatch is written by the Lead; the refusal names the exact expected form, so the first
  refused dispatch self-corrects. Cost of (b): a dual-form branch plus a removal node with its own test.
- F2 A role with no binding (E4): (a) check 3 judges the label only; the hook writes no line and names the missing key;
  designer / judge / project roles resolve through their role file (the D-0067 carrier, M9); (b) the finding's literal:
  check 3 refuses a dispatch whose role has no binding, naming the key. Recommend (a): (b) blocks every harness
  built-in (`general-purpose`, `Explore`) and every designer dispatch unless designer is exempted by name, and it makes
  a PreToolUse gate depend on a data file whose breakage already defaults (E5). Cost of (a): an unbound role launches
  and is recorded only by hand (the door line says so).
- F3 `subagent_type` absent / blank with a description: (a) refuse, naming `subagent_type`; (b) expect `general-purpose`
  (the harness default: estimate, not verified; the Lead checks the Agent tool schema); (c) keep the old form-only
  check for this case. Recommend (a): gate and recorder agree (the hook already refuses to record such a launch).
- F4 The WARN layer: (a) rekey the mismatch to config binding vs role file `model:` (about 40 test rows rewritten);
  (b) drop the mismatch branch, keep the no-role-file WARN, leave the divergence to the `journal_echo` measurement;
  (c) delete the layer. Recommend (b): the layer's premise (a label that declares a tier) is gone; the rule closes a
  tier by measurement; net code and test deletion. Cost: the divergence is seen after the first run, not before launch.
- F5 An explicit Agent tool `model` parameter (E13): (a) it is the declared model for the journal line; (b) the
  binding always. Recommend (a). Estimate: that the harness's Agent tool accepts `model` is not verified here; the
  Lead checks the tool schema (one look). With (b), a stand-in launch is recorded as the bound model and only
  `journal_echo` MISMATCH reveals it.
- F6 `tier_echo` (D-0016 names it: «dispatch_gate / tier_echo resolve role -> model»): (a) unchanged, its label branch
  stays inert, the declared-vs-measured check is `journal_echo`'s; (b) widen card A: read SubagentStop `agent_type` ->
  `role_bound_model` -> MISMATCH (+ about 10 code lines, 2 rows in `test_tier_echo.py`, and a second MISMATCH line for
  the same worker next to `journal_echo`'s). Recommend (a); (b) is the literal text of D-0016.
- F7 The journal `model` value: (a) the binding's family word (`sonnet`), as the hook writes today; (b) the bound id
  (`claude-sonnet-5-5`). Recommend (a): the field's form stays continuous for calibration distributions; `journal_echo`
  compares by family either way. Cost: the version (5-5 vs 5-1) is not recorded (the transcript has it).

Observation, not a fork: async launch responses carry `resolvedModel` (M18), a harness MEASUREMENT. Using it as the
journal `model` would turn the declaration into a measurement and leave `journal_echo` nothing to cross-check; the
draft does not read it.

Noticed in the brief: the pile row FG7-14 lists `CLAUDE.md` in owns, but the rule lives in `COORDINATOR.md` (M6, M7):
a pile-row edit for the Lead (D6). The finding says check 3 compares model families (it does not, M1/M3).

## 8. Small choices closed by the designer

- Separator `:` only (the documented form); the role compare is case-insensitive (`lower()`); no leading-whitespace strip.
- A non-string description is refused rather than raised (removes the documented raise; callers keep their guards).
- `role_bound_model` lives in `dispatch_gate.py` (the hook already imports it; no new module; the role-file reader is there).
- The hook reads the config of the journal's repo (`jw.repo_root(cwd)`), the same root `journal_write.py:591` uses.
- With F4 (b), check 3 and `role_type_warn` read no config; only the hook does.
- The DoD's probe run is the tool's own canonical form (`--json`).

## 9. Lead edit text (COORDINATOR.md rule 7, proposed)

Replace «The visible dispatch label (`description`) starts with the worker's model: "sonnet: …" / "opus: …" (a
non-standard agent: its actual model) — the operator sees the tier in the background-task list, the same
self-declaration as the journal's `model` field (reconciled by calibration check 4).» with «The visible dispatch label
(`description`) starts with the worker's role — the dispatch's `subagent_type` — and a colon: "builder: …" / "critic: …"
(D-0016: the interface already shows the model). The model is the role's binding (`delegation.config.yaml`
`roles.<function>`; a role the config does not bind: its role file's `model:`), written to the journal's `model` field
by the dispatch hook (reconciled by calibration check 4).» The rest of rule 7 unchanged; heading unchanged.

## 10. Reading trail

Read: batch-7 row FG7-14 (Grep -C3); the finding (whole); architect-tier spec Grep (stream A :660-704, F12 :880, :783,
:223-224, :595-601); `tools/dispatch_gate.py` :1-8, :80-219, :395-404, :570-581, :812-901, :1040-1289; Grep of its
`def`/label names; `tools/journal_hooks.py` :1-60, :180-272; `tools/tier_ladder.py` :1-200; `delegation.config.yaml`
whole; `tools/tier_echo.py` :1-96, :155-234; `tools/journal_echo.py` :630-669; `tools/journal_validator.py` :598-629,
:860-879; `tools/test_journal_hooks.py` :25-159; `tools/test_dispatch_gate.py` :470-514, :1795-1819, :3500-3515;
`tools/test_critic_snapshot.py` :345-374; `tools/hook_liveness_probe.py` :585-614, :660-679, :885-899, :1110-1159;
`tools/session_retro.py` :115-144; `tools/owns_gate.py` :1072-1083; `COORDINATOR.md` :188-209; `tools/mechanism_gate.py`
:270-314; `docs/SIBLING_MAP.md` :100-109; `docs/TESTING.md` :75-149; `ai-packages/qa-factory/design/architecture.md`
AR-13, AR-29 (Grep).
Negative claims and their controls: M7, M8, M15, the test_hook_liveness_probe row, the slow-list row (each control in
its line); Grep `frontmatter.{0,60}(config|binding)` in `tools/*.py` -> 0 with control `frontmatter.{0,60}(model|name)`
-> 45: no check ties a role file's `model:` to the config (estimate: narrow pattern).
No test was run (cost discipline of the brief).

## 11. Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1 (a) one form at once. F2 (a) check 3 judges the label only; unbound roles resolve through their role file or get the hook's door line. F3 (a) refuse, naming `subagent_type`. F4 (b) drop the mismatch branch, keep the no-role-file WARN. F5 (a) an explicit Agent `model` parameter is the declared model (measured: the Lead's Agent tool schema carries an optional `model` enum). F6 (a) tier_echo unchanged. F7 (a) the family word.
- Order: cards B and C (world-agnostic fixtures) and card A run in parallel worktrees; merge order B, C, then A. The D6 Lead edits (COORDINATOR.md rule 7 text of section 9, AGENTS.md regeneration, the pile row owns CLAUDE.md -> COORDINATOR.md) ride card A's acceptance commit. From that merge on, the Lead's dispatch labels read `<subagent_type>: ...`.
