# B-220 — the test command is probed and cured at onboarding; gate A is the safety net (node spec)

The Lead's decisions over the designer draft t-379 (opus, 03.10 10:4x — the revision of t-377 after the owner's ruling)
and critic-on-plan t-380 (opus, 11:2x — NOT FIT as written: two blockers F1/F2, fixes F3–F12, queue F13/F14; no
redesign). **The body is the draft, read whole:**
[drafts/b-220-toolchain-answer-executor.designer-draft.md](drafts/b-220-toolchain-answer-executor.designer-draft.md);
the critic verbatim: [reports/t-380-critic-on-plan-b220.md](reports/t-380-critic-on-plan-b220.md).

The owner's ruling (03.10, chat): the test command is recorded at onboarding; right there the factory probes it, and
when it needs a change for the factory it proposes the fix and asks "Do it?"; when the factory does not know the fix,
the LLM explains the situation at that point and asks how to proceed (FR-50's three answers). A proposed command may
be shown as text: "I propose to run it as: `<command with flag>`" (B-292 (г) closed). Gate A keeps its reporter card
as the safety net (forms `command` / `myself` / `accept`).

## §0. The blockers — decided

| F | decision |
|---|---|
| F1 | **(a)**: S5 accepts `{report_path}` EMBEDDED in one argv token (exactly one token contains it; `execution_request.validate_request` :130 accepts "one token contains the placeholder" for junit-xml/trx; `run_suite` :1954 substitutes INSIDE the token the way the probe does at `gate_preflight` :1975 — `token.replace`). These two hunks are NOT this node's: they go to the **t-300 N2 builder** (which owns both files) as item F1-b220 with one key each (K: a dotnet-style `trx;LogFileName={report_path}` token is valid and substituted; negative: two tokens carrying the placeholder → refused naming both). TEMPORAL edge for this node: before N2's hunk lands, the dotnet cure's key is reported PARTIAL ("awaiting N2 F1-b220"), never faked green; after it lands the key is DONE. In addition the candidate probe runs S5's command contract (`_command_from_profile` + the argv/report_path rules — imported, read-only) BEFORE a cure is "proven": a probe that passes but whose command S5 would refuse is not proven (FR-59). karma/jest cures need a package AND a config edit → not a one-flag cure: they stay in A-O2 (the LLM explains; Y11 as noted by the critic). |
| F2 | **One proposal per profile, sealed when it is asked**, not all up front: the maker makes profile i's proposal only after profile i-1's answer is applied or refused, with `input_hash` recomputed from the config as it is then. Key K-two-profiles: two cured profiles → two "Do it?" rounds, both applied, the second never "stale". |

## §1. The fixes — in the spec (binding over the draft)

| F | amendment |
|---|---|
| F3 | A-O2 answer (a) "here is the command" at onboarding has an executor: the same maker takes the person's line, splits it (shlex, as t-354's `command_argv`), probes it, runs S5's contract, and seals a proposal → one more "Do it?" (so a person-given command is applied by the same approved path, never written raw). Answer (c) "decide later" records NOTHING in project decisions (a deferred decision on a list pointer is a dead end: `_set_pointer` refuses `/profiles/<n>/…`, witnessed): the profile keeps its command, and gate A's reporter card is the safety net that asks again — that IS the design. The p4:144 dead end → B-296. |
| F4 | The sentence the person saw is in `listing` (covered by `PROPOSAL_COVERS`' hash) and is RENDERED from the sealed file at "Do it?" time; E30 rewritten: a yes binds to the displayed sentence, a sealed file edited after display → "proposal is stale". |
| F5 | KO6 reconciled with O-X2: a cure may set `reporter.target` AND `reporter.kind` (a trx report needs `kind: trx` to be parsed); `probe_candidate(kind=…)` takes the kind; the proposal lists both pointers. |
| F6 | KO5 via the real carriers: (i) the gate A fix line (`the fix:` action slot, exempt) and (ii) the onboarding proposal sentence — both pass `human_text.problems(...) == []`; the action-line exemption applies to EVERY rule row incl. `script_name` (a `manage.py` command on the action line is legal); a test asserts the onboarding sentence itself. |
| F7 | E29 restated: the maker leaves `conflicts`, `added`, `reasked` empty; `apply_plan` refuses only on `validate` errors — the test exercises that refusal (a proposal whose target key fails validation). |
| F8 | Edges added: a second "yes" at onboarding → "already done" (idempotent; never a stale refusal); pytest `no_report` is a DIAGNOSIS (there is no reporter flag to add: the person is told what it means with FR-50's three answers, no "Do it?"); `add_argv` already present and only the dependency missing → the proposal carries the dependency step only, no duplicate flag; `references/report-cures.json` unreadable → the probe says "the cure table could not be read: <why>" and falls to A-O2 (FR-1); the vitest row corrected: built-in junit reporter (`--reporter=junit --outputFile={report_path}`). |
| F9 | Cure proposals carry a hash-covered `kind: "cure"`; `record_approval` REFUSES a `headless:` ref for that kind (the person's word is the only approval of a cure); `onboard_apply --apply` without `--approval-ref` refuses a cure proposal by name. Detector (question c): the key + the approvals-log audit queued as B-294 (с). |
| F10 | O-X5 gains both phase texts: p4:496-499 "do not execute tests while generating" gets its one exception (the candidate probe runs the reporter slot only, on the probe's temp report path); the p3 summary names the probe run as a listed action (the yes covers listed actions only, p3:146-148). |
| F11 | The durable row stores `argv` (the proven command) and is keyed by (profile, argv digest) WITHOUT the environment: the reporter proof is a property of the command on this machine, not of a stand; gate A reuses it when the profile's argv digest matches; "no longer" = the argv digest changed (the command changed) vs the same digest failing (it stopped working) — two different sentences. |
| F12 | Y7 + `change` on a reporter card with NO cure is unread by `read_stand_gap_answers` (gate_brief :554): the person gets the FR-1 refusal naming the words that apply (`command` / `myself` / `accept`). |
| F13 | queued B-294 (а): a role can call `config_contract.py --record-approval/--apply` past the guard; `--probe-profiles` hands sealed files. |
| F14 | queued B-295: `launch_check` in-place repair; the approvals log rewritten without a lock (gate A brings concurrent writers). In the spec: §5(a) counts the confirmation run — THREE runs per cured profile (probe, cure, confirmation), the whole suite when there is no placeholder. |

Forks: Y2, Y3, Y5 (the onboarding collect proves the templates, not S5 — stated), Y6, Y7 (+F12), Y8, Y10, Y11 (karma/jest
in A-O2) — as the critic agreed. **Y9: an absolute path in the person's answer is refused in words** (A20; p4:140), never
recorded. Y4 (a) with F4/F5; the mixed approvals log stays (tracker lines already share it).

## §2. Dispatch

Builder (sonnet) after the package commit of 03.10 and in parallel with the t-300 N2 builder (owns disjoint: this
node owns `config_contract.py` (the maker, `probe_candidate`, `record_approval`'s cure refusal), `onboard_apply.py`
(the cure refusal, `--probe-profiles`), `gate_preflight.py` reporter card + `read_stand_gap_answers`'s unread line,
`gate_brief.py` :554 region, `references/report-cures.json` (new, from `REPORT_CURES`), `references/human-text.json`
(the exemption for every row), skills/qa-onboarding p3/p4 texts, tests `test_config_contract.py`, `test_onboard_apply.py`,
`test_gate_preflight.py` reporter keys — N2 owns `execution_request.py` / `run_suite.py` incl. F1-b220). given = this
file + the draft + the critic report. DoD = the draft's KO keys with the amendments above + K-two-profiles + the F8
edges as keys + the F9 refusals; the critic gate on the diff (a config writer with a person's approval changes
meaning); live proof: the Lead runs `/qa-factory:qa-onboarding` p4's probe on a cmp2r copy with a junit-less pytest
profile and a dotnet-shaped fake profile (no role launch; P8).
