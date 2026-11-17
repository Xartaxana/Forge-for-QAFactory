# Rules-debt wave 3 — cards C3-j and C3-k (k1..k4), header-ready (t-1086, F19)

Designer draft for the Lead. The parent is `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (called "the spec"
below); its §1, the C3 shared items S-a..S-f, the E-c table, the decided-branches table and every "Lead decisions" section
apply to these cards and are not repeated. The spec is not edited here.

**Where the facts were read.** The root checkout is on `main` = `origin/main` = `cc1eb6b876369c6f1080e8f1f455e85c4e1b04b9`
(`.git/HEAD` -> `refs/heads/main`; both ref files read directly). On that main, C3-R, C3-0, C3-rr and C3-b1 are merged.
`gate_template.py` is on main (read whole, 97 lines). C3-b2, C3-d and C3-reg-precondition are not on main yet. Every
`file:line` below was read on cc1eb6b8. Lines in `execution_request.py` move when C3-b2 merges (it edits `_match`), so the
cards anchor on function names there. This dispatch had no shell. Nothing was RUN. Every command below is for the
builder or the Lead.

**Main today, the S-f base (read on cc1eb6b8, `scripts/tests/test_gate_registry.py`):**
- `EXPECTED_DEBT` :60-63 has six rows: stand_identity, provenance_acceptance, test_identity, s5_window, baseline_identity,
  s5_stand_limits;
- K-T1.2 :252 reads `"6 gate(s) left as debt:"`;
- the split :342-343 is 21 converted / 6 debt / 6 exempt;
- `D13_ITEM_COUNT = 145` (:1043, merged-tree comment :1042);
- the D13 set is :954-1013 and the F4 `code` list is :740-747.

After C3-b2 and C3-d merge, the debt set is stand_identity, provenance_acceptance, baseline_identity and s5_stand_limits.
Every number a card applies is a DELTA from the main it is based on (S-f).

---

## §1. Architecture, rules, owners (designer rule 1)

FR sections: C3-j A/B/C/D/E (a new card a person reads: B, FR-6/FR-7/FR-9). C3-k A/C/D/E/F (no text a person reads
changes, except F-k5).

AR-n touched, with the change check each card's DoD carries (`design/architecture.md`; the lines are the spec's §1 reading):
- AR-13 (:166): a fact with a reader function is read only through it. C3-k: the provenance word comes only from
  `profile_contract.provenance_word`, and the request's local-source exemption only from
  `profile_contract.local_source_request`. C3-j: the cover is read only through `environment_record.covering`, and the
  key only through `environment_record.lasting`.
- AR-15 (:180): a shared problem has one survivor. C3-k: the four copies of the local-source test become one function
  (k1). C3-j: one road for "do not ask this stand again", the stand-gap card -> record -> cover road.
- AR-20: the registry pins move by the named delta, and D13 is re-measured (S-f).
- AR-22: every field read has a producer, and every consumer lands with its reader. C3-j: the `stand_limit` key's writer
  (`record_lasting` / the CLI) and its reader (`_environment_cover`) land in one commit. C3-k: each consumer id enters
  `accepts` in the commit that wires its reader. The two dead consumers leave in the commit that adds their replacement.
- AR-24 (C3-j): the person's words reach the record whole (`environment_record.record` keeps `words` whole).
- AR-28 (:282): each new gate read states its behaviour on missing, unreadable and empty input, and a test pins it.
- AR-29 (:155-157): every check below names its owner and census class. Run `test_judgment_census.py` (slow: judged by
  the canon). A raised count is named in the verdict.

Checks added or moved (AR-29). The census rows were read in `scripts/tests/fixtures/judgment-census.json`:

| check | card | owner | census class | blocking |
|---|---|---|---|---|
| `unmeasured` stand limit -> a stand-gap card at gate A, with `accept always` when a key exists | C3-j | intent: the answer is the person's word (P13, FR-4) | the existing unit `gate_preflight.py::check_s5_stand_limits` stays `shape`/data (:418). The new helper adds no refusal site, so it adds no unit. Precedent: `_stand_limit_card` has no census row (grep, control `check_s5_stand_limits` found at :418) | yes: waits at gate A |
| the cover lookup for a `stand_limit` key | C3-j | data: a key join, as `environment_property_cover` | xref; no unit (`_environment_cover` has no census row; it appends to lists) | no: it lifts a card |
| `_limit_key` / the `lasting` branch / the CLI `--limit` subject | C3-j | data | unchanged. `environment_record.py::_refuse` and `::_story_context` stay `shape`/data (:306-307), and the new refusals go through `_refuse` | refuses, as the other subjects |
| `profile_contract.provenance_word` (new producer) and `local_source_request` (new) | C3-k1 | data | no unit: neither raises nor refuses | no |
| each provenance accept site through `acceptable(provenance_word(...), <consumer>)` | C3-k2, C3-k3 | data: a word joined to its registry row; the validation itself stays `validate_runtime_provenance` / `person_confirmed`, as today | unchanged. Each site keeps its existing unit and class: `validate_request` safety (:343), `execution_fingerprint.build` shape (:324), `run_suite.probe_runtime` xref (:956), `_provenance_errors` shape (:676), `validate_baseline_record` shape (:691), `validate_manual_current` xref (:255) | unchanged: the same records are refused |
| `acceptable_provenance` recast to a consumer id (F-k3) | C3-k4 | data | unchanged: `profile_contract.py::acceptable_provenance` shape (:826). If the recast removes its `ValueError` raise (the unit), `test_judgment_census.py` shrinks it, and the shrink is named in the verdict (AR-20) | no |

If `test_judgment_census.py` reads any of these differently, the node stops and returns a question (spec S6 E1 precedent).

Commit lines: every package commit carries `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py`
accepts. That file is the only carrier of the grammar, and it is not copied here. Each card gives the CONTENT.
`judgment: none` always carries its ` -- <why>`.

---

## §2. Card C3-j — s5_stand_limits: an unmeasured limit is asked, the answer persisted (B-282)

Wave 3. gate_preflight HOT queue position 2 (`C3-rr` is merged, so C3-j is next). Plan critic before the build (spec
§3: every C3 card). Decided: F-O1 (the owner), F-C1 (a), F-C2 (a), F-j1 (stand_gaps road), F-j2 (E9).

**Facts (cc1eb6b8):**
- The note. `check_s5_stand_limits` (`gate_preflight.py:3166-3218`) turns `unmeasured` into a NOTE only (:3192-3195).
  `over` becomes a PERSON_DECIDES card through `_stand_limit_card` (:3243-3273). `unreadable` and `incomplete` become
  FACTORY_DEFECT findings (:3196-3216).
- The states. `_e2e_limit` (:3089-3164) returns `n/a`, `unmeasured` (four returns: :3124, :3151, :3155, :3160),
  `unreadable`, `incomplete`, `within` and `over`. The stale return (:3160) carries no `wait`.
- The second reader of the word. `check_s5_reporter` reads `_e2e_limit(...)["state"] == "over"` at :3323 (E5).
- The waiver match. The card's message must open with the block text `e2e stand limit: <profile>`: `add()` matches a
  recorded waiver against the message plus the finding's doors (:3256-3259, :1631-1642).
- The record. `environment_record.py` knows two scopes: `LEVEL, CASE` (:35), fields at :50-51.
  - `lasting` (:133-147), `current_key` (:165-185) and `near_miss` (:188-203) branch on the scope.
  - `_valid_key` (:292-297) accepts only the two field sets, every field a non-empty `str`.
  - `record` (:326-348) is the one writer. It refuses a non-whole key, empty words and an unreadable record.
  - `covering` (:300-315) is pure, and its only error is "not covered".
  - An absent file is `([], "")` (:217-218, :275-279).
- The driver's door. The driver writes an `accept always` through `stand_gaps.record_lasting` (`stand_gaps.py:1243-1254`;
  caller `driver_machine.py:2897`), with the gap's `property_key`. `record_lasting` is generic over the key: it needs no
  edit.
- The rehearsal's own derivation. `_lasting_of` (`gate_preflight.py:4201-4213`) and `_environment_cover` (:4215-4250)
  are the rehearsal side. `_environment_cover`'s `near_miss` text table (:4242-4246) keys `command`, `reason` and
  `address`.
- When `accept always` is offered. The stand-gap card offers it only when the gap has a key (`gate_brief.py:965`, read
  as a grep hit only). The words come from data (`stand_gap_words`, `gate_brief.py:724-740`), so no vocabulary edit is
  needed. The spec's sketch named `question-vocabulary.json` in owns; this draft drops it, see small choices.
- The registry row. `s5_stand_limits` is `gate-registry.json:479-499`: vocabulary target, words matched/mismatched/unknown,
  one site `check_s5_stand_limits` accept, `unknown_branch`/`on_no_answer` debt, `test` test_gate_preflight.py, debt
  B-282.

**Measured premise (PROJECT.md п. 6 (а)).** Grep over `scripts/tests/fixtures/stories/` for
`page_object_max_wait_s|e2e_page_load_s|e2e_stand_limit` (case-insensitive) found 0 hits. The same call with `"level"`
added found 179 hits in 13 files (the positive control, same tool, same path and flags). So no recorded story carries a
stand-limit record or an `e2e_stand_limit` finding, and the change moves no recorded story. Its live effect is
unmeasured, which is why it gets a live-runs row (FR-33, spec §5). The command for the Lead, to confirm on the dry
stories' gate A output if wanted:
`python -B -c "import glob,json;print([p for p in glob.glob('C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/**/*.json',recursive=True) if 'e2e_stand_limit' in open(p,encoding='utf-8',errors='replace').read()])"`.
Expected: `[]`.

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`, this card, the spec's C3 shared items S-a..S-f; read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/gate_preflight.py:104-110,1582-1660,3089-3330,4130-4250,6078-6110`, `scripts/environment_record.py` (whole), `scripts/stand_gaps.py:190-340,422-440,955-1020,1243-1255`, `scripts/gate_brief.py:720-760,960-1000`, `references/gate-registry.json:479-548` (s5_stand_limits and its model row environment_property_cover), `scripts/tests/test_environment_record.py`, `scripts/tests/test_gate_preflight.py` (grep `e2e_stand_limit|skip_stand_limits`, :2927), `scripts/tests/test_gate_registry.py` (S-f lines: :60-74, :252, :337-343, :740-747, :954-1043)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_record.py` (the third scope `stand_limit`: `LIMIT`, `LIMIT_FIELDS`, `_limit_key`, the branches of `lasting`, `current_key`, `near_miss`, `_valid_key`, `about_of`; `cmd_record` and its parser: the `--limit <profile>` subject; the module docstring's key list)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (`_e2e_limit`: the stale return carries `wait`; `check_s5_stand_limits`: the `unmeasured` branch; new `_limit_gap_row`; `_environment_cover`: one `wait` entry in the near-miss text table) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stand_gaps.py` (only the reads of a gap row's `scope` that must treat `stand_limit` as a profile-level gap, item 5)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `s5_stand_limits` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_environment_record.py` (rows, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (rows of the stand-limit table, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `s5_stand_limits` only, item 8)
non-goals: writing `config.json` `environments[].measured` or `profiles[].page_object_max_wait_s` (onboarding's); the `over`, `unreadable` and `incomplete` branches and `_stand_limit_card` (unchanged text and door); `stand_gaps.record_lasting`, `driver_machine.py`, `gate_brief.py`, `references/question-vocabulary.json` (generic over the key and the words); `project_knowledge.py` (F-C2 (a)); `judgment-census.json` (no unit expected: the stop rule is in §1); any new test file
handoff: report path given by the Lead
edges: E1-E14 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, and `s5_stand_limits` is absent from the `N gate(s) left as debt:` block; then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stand_gaps.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_environment_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py`, plus the printed non-slow files (`test_environment_record.py` is keep and fast, spec §0.3). `test_gate_preflight.py`, `test_gate_registry.py` and `test_judgment_census.py` are slow: judged by the batch canon and named in the report.
siblings: axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins): the row's words change, so the builder greps `skills/qa-story/phases/s5.md`, `references/*.md` and `agents/*.md` for `e2e stand limit|page_object_max_wait_s|stand limit`, and gives each hit "checked, no edit (meaning unchanged)" or an edit named as a finding. A1's class ("a converted row's word compared in an unregistered function"): `check_s5_reporter`'s `== "over"` (:3323) is registered (item 6). The B-414 record road (`environment_property_cover`, reporter LEVEL gaps) is the model, not edited.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (C3-j)

Items:
1. **The `stand_limit` key (`environment_record.py`).**
   - `LIMIT = "stand_limit"` and `LIMIT_FIELDS = ("scope", "environment", "definition_sha", "contour", "wait_s")`.
   - `_limit_key(gap, cfg, stand)`:
     - `contour = str(gap.get("contour") or "")`;
     - `stand` is stripped, and is non-empty and not `PLACEHOLDER_STAND`;
     - `sha = stand_identity.definition_sha_for(cfg, stand)` (as `_case_key` does, :125-128);
     - the wait is read FROM THE CONFIG: the profile whose `profile_id == contour`, field `page_object_max_wait_s`, parsed
       by the same reader `_e2e_limit` uses (`limit_seconds`). If that reader lives in `gate_preflight.py` and importing it
       here would cycle or load the gate module, the node stops with a question;
     - `wait_s = f"{wait:g}"`;
     - any part missing -> `{"key": None, "why": NO_KEY}`.
   - The gate and the CLI therefore derive one key from one place (M8). The gap row's own `wait_s` is shown on the card,
     never keyed.
   - `lasting` gets the `LIMIT` branch, and so does `_valid_key`.
   - `current_key` gets a `LIMIT` branch: the same subject with `definition_sha` and `wait_s` as the config holds them now.
     It is None when it cannot be built.
   - `near_miss` gets a `LIMIT` branch: a live row with the same `environment` and `contour` but another `wait_s` gives
     `why = "wait"`; the same `wait_s` with another `definition_sha` gives `why = "address"`.
   - `about_of` for `LIMIT` returns `f"whether the {contour} e2e tests fit the page load (their page objects wait at most {wait_s} s)"`.
     `says()` then reads "on this environment whether the web e2e tests fit the page load … cannot be checked".
   - expected from: the spec's C3-j item 2 (the key) and FR-7.
2. **The CLI form.** `environment_record.py record --task <T> --limit <profile> --option accept --words-file <F>`. Exactly one
   of `--contour`, `--case` or `--limit` is given; any other count is refused through `_refuse`, naming the three forms.
   The gap is `{"scope": "stand_limit", "contour": <profile>}`, keyed by `lasting` (item 1). With no key, the refusal says
   which part is missing (stand, stand definition, profile, or its wait) and that nothing was recorded. The module
   docstring lists the form and the third key. expected from: the existing two forms (:20-21, :423-431) and FR-1.
3. **The card (`gate_preflight.py`, F-C1 (a): gate A, where the check already runs, `run` :6089).** In
   `check_s5_stand_limits`, the `unmeasured` branch (today :3192-3195) builds `row = self._limit_gap_row(profile_id,
   limit)`, then `self._lasting_of(row)`, then `if self._environment_cover(check, row): continue`. Otherwise it puts the
   card up. `_limit_gap_row` returns:
   - `{"id": f"SL-{profile_id}", "case": "", "scope": "stand_limit", "contour": profile_id, "cases": list(limit["cases"]),
     "kind": "stand_limit", "wait_s": limit.get("wait"), "what": <the measured why>, "state": "unmet", "remedy": <a remedy
     in the reporter row's shape whose `where_words` names the two config fields of `limit["fields"]`>}`.

   The finding: `self.add(check, PERSON_DECIDES, f"e2e stand limit: {profile_id} — {GAP_SLOT} — " + <"the stand's page load
   is not measured and the page objects wait at most N s" / limit["why"]> + ", so whether the e2e rows of `<profile>` fit
   this stand is unknown", self.card_door(row["id"]), gap=row["id"], gap_case="", profile=profile_id, cases=list(cases),
   answers=[<line (b)>, <line (c)>])`.
   - Line (b) is the existing handed door: `self.waiver_command(f"{HANDED_MATCH_PREFIX} {profile_id}", "S5", "handed")`,
     as in `_stand_limit_card` :3268.
   - Line (c) is "`<case id>: manual` for each of <named_ids(cases)>".
   - `accept` and `accept always` come from the card's own words (data). `accept always` is offered only when
     `property_key` is set (gate_brief :965).

   The message opens with the block `e2e stand limit: <profile>`, so a waiver recorded earlier still passes (E9). When
   `add()` does not append the finding (a recorded word passed it), no unanswered card may remain: the builder reads how
   `gap_name` and `stand_gaps.collect` treat a row whose finding was dropped (the reporter's order, row then add, :4152-4153),
   and if such a row would render as an unanswered card, the row is not left in `self.stand_gaps`. expected from: the
   owner's word (F-O1), FR-4 (a recorded word passes), FR-9 (each option has an executor) and FR-7.
4. **Near-miss text.** `_environment_cover`'s table (:4242-4246) gains `"wait": f"the page objects' wait changed since
   {date}, when you recorded an answer for the earlier one"`. The card then says the earlier answer no longer applies
   (FR-7: never the same text for another fact). `_e2e_limit`'s stale return (:3160) also carries `wait=wait` (and
   `load=load`). It is the one unmeasured return whose wait is known but not returned today.
5. **`stand_gaps.py`: the profile-level gap.** Every read of a gap row's `scope` that means "a profile-level gap with a
   `cases` list and no `case_id`" treats `stand_limit` like `level`. The builder greps `"level"` in `stand_gaps.py`; the
   hits read are :227-228, :277, :303, :959, :1007, :1014. Each hit gets a report line: applied / not applicable — why.
   :1007 and :1014 are the gate B covered-block reads of a record `subject.scope == "level"`: the stand-limit check runs at
   gate A only, so the expected verdict is "not applicable — gate A only". One shared tuple (e.g.
   `PROFILE_SCOPES = ("level", "stand_limit")`), not a second literal per site (P31). expected from: the reporter LEVEL gap,
   the model of a profile-level card (`_reporter_gap_row` :4160-4192).
6. **Registry row `s5_stand_limits`.**
   - `vocabulary: code`.
   - `words: ["within", "over", "unmeasured", "unreadable", "incomplete", "n/a"]`: the states `_e2e_limit` returns and
     `check_s5_stand_limits` compares (S-c).
   - `verdict_map`: within -> matched; over -> mismatched; unmeasured -> unknown, owner environment; unreadable -> unknown,
     owner factory; incomplete -> unknown, owner factory; n/a -> not_applicable. The owners follow the card classes
     (:3197 and :3208 are FACTORY_DEFECT, "onboarding's own record").
   - `accepts: {}` (no accept site, F-D1 (b)).
   - `promotable: false` stays.
   - `unknown_branch: question`, `on_no_answer: wait`, `waits_at: gate_a`, `closed_by: ["person"]`,
     `addressee: ["code_routes", "person"]`, `person_subject: "world"`.
   - `policy_file`, `scope_keys`, `binding_keys`, `question_kind` are copied in shape from `environment_property_cover`
     (:527-548, the row whose answer lives in the same record), with `scope_keys ["environment", "contour"]` and
     `binding_keys` = `LIMIT_FIELDS` minus `scope`.
   - Sites:
     - `check_s5_stand_limits` re-roled `produce` (E-c table: "it measures and cards; it accepts no record");
     - `_e2e_limit` registered `produce` (it returns the words);
     - `check_s5_reporter` registered `validate` (it reads `over` to skip the reporter rehearsal and accepts nothing; A1's
       class).
   - `status: converted`, `debt_ref: ""`; `test` stays `scripts/tests/test_gate_preflight.py`.
   - `decides` rewritten: "the stand's own limits are checked before S5 plans over it: a measured page load longer than
     the page objects' wait is a card; an unmeasured one is a card at gate A whose answer `accept always` is kept in the
     environment record under the stand, its definition, the profile and the wait; a recorded limit that cannot be read
     or is incomplete is onboarding's defect; never a pass on an unknown".

   expected from: `_check_row` (`gate_registry.py:485-681`), S-c, F-C1 (a).
7. **Tests: rows in existing tables, expectations from this card.** First the builder greps `e2e_stand_limit` in
   `test_gate_preflight.py` and `lasting|_case_key|near_miss` in `test_environment_record.py`, and adds rows to the tables
   found. If a table pins "unmeasured -> note", its row flips; the flip is named in the report as the owner's decision.

   `test_environment_record.py` (keep, fast):
   - `limit-key`: stand, definition and wait present -> the five-field key, with `wait_s` the `:g` string;
   - `limit-no-stand`, `limit-placeholder`, `limit-no-definition`, `limit-no-wait`, `limit-wait-zero`,
     `limit-wait-not-number`: each -> `{"key": None, "why": "no_key"}`;
   - `limit-cover-round-trip` (AR-22): `record(root, key, "accept", "ok", "T-1")` then `covering(load(root)[0], key)` ->
     that row;
   - `limit-near-miss-wait`: a live row with wait 10, key with wait 30 -> `(row, "wait")`;
   - `limit-near-miss-address`: another definition_sha -> `(row, "address")`;
   - `limit-current-key`: the config's wait changes -> `current_key` carries the new `wait_s`;
   - CLI `record --limit web`: recorded; the same key again -> "already there" (`created` False); the forms
     `--limit` + `--contour` -> refused, nothing written;
   - words at and beyond the existing words limit, only if the table holds no such rows (E8).

   `test_gate_preflight.py` (slow, canon):
   - `unmeasured-card`: load absent, wait 10 -> one `stand_gaps` row `SL-web` with `property_key` set, and one PERSON_DECIDES
     finding whose message starts `e2e stand limit: web`;
   - `unmeasured-covered`: the same, with a live record row under the key -> no finding, one note "not asked - …", the row
     in `covered_gaps`;
   - `unmeasured-wait-changed`: the record row under wait 10, config wait 30 -> a card whose row has `changed_since`
     naming the wait;
   - `unmeasured-no-wait`: wait absent -> a card, `property_key` None (no `accept always`);
   - `unmeasured-both-absent` -> a card, no key;
   - `old-waiver` (E9): a recorded waiver for `e2e stand limit: web` -> no finding, and no unanswered card;
   - `record-unreadable` (E3): an unreadable record file -> one note, and the card shown;
   - `switch-off` (E4): `skip_stand_limits` -> no card, the record not read;
   - `over-unchanged`: the over row stays as pinned;
   - `reporter-not-lost` (E5): an unmeasured profile is still rehearsed by `check_s5_reporter`.

   expected from: the owner's word, FR-7, FR-4, FR-59 and the edges below — never from the code's output before the change.
8. **S-f pins (`test_gate_registry.py`, deltas from the base).**
   - `EXPECTED_DEBT` loses `s5_stand_limits`, and `EXPECTED_CONVERTED` gains it.
   - K-T1.2 N-1, and the split converted +1 / debt -1, with its AR-20 comment line (`C3-j, t-<id>`).
   - The F4 `code` list gains `s5_stand_limits` (`target` -> `code`).
   - D13 re-measured with `GR.analyse(PLUGIN_ROOT)` before and after. Expected new triples:
     `("gate_preflight.py", "check_s5_stand_limits", "s5_stand_limits")` (its `state == 'unmeasured' / 'unreadable' /
     'incomplete' / 'over'`, words now counted) and `("gate_preflight.py", "check_s5_reporter", "s5_stand_limits")`
     (`... == 'over'`, :3323).
   - `D13_ITEM_COUNT` rises by the number of comparisons the scan attributes. That is about five, but the number is the
     measurement, named in the S-f comment form with the list. A different set of triples is a stop and a question.

architecture content: `AR-22 -- the stand_limit key's writers (record_lasting, the CLI) and its reader (_environment_cover) land in one commit`; `AR-24 -- the person's words reach the environment record whole`; `AR-28 -- an unmeasured limit is asked at gate A, an unreadable record covers nothing, pinned`; `AR-13 -- the key is derived only by environment_record.lasting, the cover read only by covering`; `AR-29 -- check_s5_stand_limits stays shape/data; the answer is intent (the person), the cover a data key join (xref), no new unit`; `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured and named`. judgment content: `none -- the person answers the card (intent, P13); code only joins the recorded answer's key to the stand, as for every stand-gap card`.

Edges (each with the INVARIANT it protects):
- E1 (absent / placeholder stand): no key; the card is shown without `accept always`. INVARIANT: nothing is recorded under
  a placeholder key (`environment_record` docstring :17).
- E2 (absent, zero or unreadable wait): no key; the card offers `accept` (this story), (b) and (c). INVARIANT: a cover
  never holds for an unknown wait.
- E3 (unreadable record): said once, covers nothing, the card is shown (`_environment_cover` :4229-4232). INVARIANT: an
  unknown never suppresses a question (FR-59).
- E4 (the off switch `skip_stand_limits`): unchanged — no card, no record read (:3181). INVARIANT: an informed switch stays
  informed.
- E5 (the reporter rehearsal, skipped only on `over`, :3323): an `unmeasured` profile is still rehearsed. INVARIANT: the
  reporter proof is not lost to the new card.
- E6 TEMPORAL: the record file may not exist before any `record`; then the rows are `[]` and nothing is covered (:217-218).
  The `stand_limit` scope exists only after this card. A record written before holds only `level` / `case` rows, and they
  stay valid (an extra scope is additive; `load_rows` does not check scopes). INVARIANT: no recorded answer changes meaning.
  A record row written by this card and read by an OLDER plugin (another machine, same project file) fails that plugin's
  `_valid_key`, so it covers nothing there and the card is asked: the safe side.
- E7 POSITIONAL: the cover is read only on the `unmeasured` branch, after `_e2e_limit` has measured. INVARIANT: a recorded
  measurement in the config always wins (`within` / `over` never read the record), and the record never hides `over`,
  `unreadable` or `incomplete`.
- E8 (outside input: the person's words): `record` keeps them whole after `.strip()` and refuses empty words (:336-338).
  Words travel through `person_words.read` (`_words` :382-393): rows AT and BEYOND its existing limit, plus empty and
  broken-encoding files, only if the table holds none (CLAUDE.md rule 11, adversarial mini-battery).
- E9 (temporal, FR-4; F-j2): a waiver already recorded for `e2e stand limit: <profile>` still passes the new card (the
  message opens with that block). INVARIANT: an informed word recorded before the change is never re-asked. (Known
  breadth: such a waiver was written for an `over` card; it now also passes the `unmeasured` card of the same profile.
  This is F-j2 as decided; the residue is noted in fork F-j4.)
- E10 TEMPORAL (S-f): the pins are deltas from the main C3-j is based on. C3-j follows C3-rr (merged) on `gate_preflight.py`.
  INVARIANT: S-f.
- E11 (conflict on `gate_preflight.py`, HOT): function-disjoint with C3-k2 (`_observed_identity`) and C3-h. Queue:
  `очередь: C3-rr → C3-j → C3-k2 → C3-h` (gate_preflight.py). INVARIANT: no two open nodes edit the HOT file at once.
- E12 (limit): the card shows `named_ids(cases)` (its existing cut). `about` is cut at 160 characters by `record` (:346).
  No new limit.
- E13 (conflicting pair: E9 vs the stand-gap road): a recorded STAND-GAP answer (`stand gap: SL-<p>: accept`) and an old
  waiver both pass. INVARIANT: both roads are a person's word; neither is a pass on an unknown.
- E14 (one road, P31): the card, its answer and its cover use the same stand-gap -> record -> cover road as the reporter
  and precondition cards. No second "do not ask again" store (F-C2 (a)). The key reads no language name and no project
  name.

Builder's commit lines (content): `architecture: AR-13, AR-20, AR-22, AR-24, AR-28, AR-29 -- <the content above>`;
`judgment: none -- the person answers the card (intent); the cover is a data key join; no new census unit`. Form: as
`tools/architecture_gate.py` accepts. A mechanism commit is not involved (package only).

---

## §3. Card C3-k — provenance_acceptance (B-255): split, order, and the decision it rests on

**Every accept site of the row, read on cc1eb6b8** (row :37-93; sites :41-69; `accepts` :80-86; field `result`; words =
the five classes, which are exactly `profile_contract.PROVENANCE_RESULTS` :21, so `vocabulary: code` is honest with the
words unchanged):

| site (registry line) | what decides today | literals left (row words) | after (recommended) |
|---|---|---|---|
| `execution_request.validate_request` (:41) | `acceptable_provenance(provenance, ACCEPTS, task=…)` :175, or the local_source literal :176 | :166 `checked['result'] == 'not_applicable'` (refusal text), :169 `provenance.get('result') == 'person_confirmed'` (a refusal), :176 (an acceptance), the seed allow (:42) | accept: `acceptable(provenance_word(…, local_source=…), "provenance.automation")`; :176 gone; :166 and :169 get `allow` (k2) |
| `execution_request.rehearsal_probe` (:43) | `acceptable_provenance(value, accepts, rehearsal=True)` :2499, `accepts=ACCEPTS` | none | accept, `consumer="provenance.rehearsal"` default (k2) |
| `execution_fingerprint.build` (:44) | `acceptable_provenance(…, ACCEPTS)` or any valid NA :121-122 | :122 (acceptance), :134 `runtime.get('result') == 'person_confirmed'` (a fingerprint key) | accept, `provenance.fingerprint`; :134 gets `allow` (k2) |
| `manual_evidence._provenance_errors` (:45) | :86 NA refusal text, :89-90 predicate or local NA | :86, :90 | accept, `provenance.manual`; :86 gets `allow` (k3) |
| `manual_evidence._other_profile_errors` (:46) | delegates to `_provenance_errors` (:121); :129 skips the revision binding for an NA probe | :129 | re-role `validate` (k3): it calls no predicate and accepts nothing `_provenance_errors` refused |
| `manual_evidence.validate_baseline_record` (:47) | :682 pc -> its own sentence; :686 valid and `in {matched, not_applicable}` | :682, :686 | accept, `baseline_identity.capture` (under this row); :682 gets `allow` (text); :686 gone (k3) |
| `coverage_contract.validate_manual_current` (:48) | :831-832 predicate or local NA | :832, :839 (skips the binding for NA), :845 (a second NA refusal) | accept, `provenance.manual`; :839 and :845 get `allow` (k3) |
| `environment_preparation._run_step` (:49) | :388 `checked['result'] == 'matched'` plus revision and environment equalities | :388 | accept, `environment_preparation.deploy_proof` (A2) (k3) |
| `probe_by_code.probe_runtime` (:50) | delegates to `run_suite.probe_runtime` (:2886-2887) | none | re-role `dispatch` (k2) |
| `manual_capture.stand_probe` (:51) | `acceptable_provenance(value, ACCEPTS, task=story)` :1612 | none | accept, `provenance.manual_capture` (tokens: F-k2) (k3) |
| `run_suite.probe_runtime` (:52) | `acceptable_provenance(value, ACCEPTS)` :928 | none | accept, new `provenance.run` (k2) |
| `gate_preflight._observed_identity` (:53) | hands `accepts=("matched", "person_confirmed")` to `rehearsal_probe` :3444 | the token tuple :3444 | re-role `dispatch`, passes `consumer="provenance.identity"` (k2) |
| `profile_contract.acceptable_provenance` (:54) | the token logic :908-923 | :917-922 | F-k3 (k4) |

Also read, outside the row: `driver_stage_build.build_outcome` (:381) calls `acceptable_provenance(record, ACCEPTS,
rehearsal=True)`. It is registered only as a `dispatch` site of `stand_identity` (:15), so it is an unregistered provenance
acceptance, invisible to A26 (a call is not a comparison). It moves in k4 (a reader of the changed name).

**Why `acceptable` cannot simply replace `acceptable_provenance` (F-T2, second half).** `gate_template.acceptable` takes
the word from `value[row["field"]]` and validates nothing (:75-94). The C3-0 pin `live-record` proves it:
`{"result": "person_confirmed"}` under `provenance.manual` is `True` (`test_gate_registry.py:1136`). That record carries no
words, no time and no story. `acceptable` also reads a not_applicable reason only from `verdict_map[word]`, never from the
record's `reason_code` (:86, :91-93), so `not_applicable:no_changed_file` can never match a record today. And
`not_applicable:local_source` is a property of the REQUEST (`runtime_required False` and `target_kind local_source`), not
of the probe record. So `validate_runtime_provenance`, `person_confirmed(record, task)` and `no_changed_file(record)` must
stay where they are, and the word given to `acceptable` must be computed after them. → fork F-k1.

**The A26 constraint.** Once the row is `converted`, every `accept` site must call a function named exactly `acceptable`
(`gate_registry.py:837-841`). A call to `acceptable_provenance` does not count; the pin is `test_gate_registry.py:587-589`.
Every row word compared in an accept site must equal an `allow` entry (:37-41, :772-783). So the sites call
`acceptable(...)` themselves; a wrapper does not satisfy F-b.

**Split and order (recommended).** Four builder cards, serial: they edit the same registry row and the same S-f pins.
- **C3-k1**: foundation. The producer, the local-source test, and the row's two new words. No site moves.
- **C3-k2**: the execution side. `execution_request` (validate_request, rehearsal_probe), `gate_preflight._observed_identity`
  (HOT), `run_suite.probe_runtime`, `execution_fingerprint.build`, and the `probe_by_code` re-role.
- **C3-k3**: the manual side. `manual_evidence` (three sites), `coverage_contract.validate_manual_current`,
  `manual_capture.stand_probe`, `environment_preparation._run_step`, and the two dead consumers (A2 and F-k4).
- **C3-k4**: the conversion. Row status and shape, `acceptable_provenance` and `ACCEPTS` (F-k3), `driver_stage_build`, the
  `refusal_text` registry clause (F-k5), the S-f pins, and the S-b row.

Queues:
- `test_gate_registry.py`: … C3-d → C3-j → C3-k1 → C3-k2 → C3-k3 → C3-k4 → C3-h;
- gate_preflight HOT: C3-rr → C3-j → C3-k2 → C3-h;
- `execution_request.py`: C3-b2 → C3-k2;
- the F1 consumer block: C3-g → C3-k3 (spec §3).

k2 and k3 touch disjoint files except the registry row and `test_gate_registry.py`, so they stay serial (row-local edits of
one row). The builder may run k1+k2 as one node if the Lead prefers fewer nodes. k3 and k4 stay separate: k4 is the one
commit that turns the gate on.

**Behaviour preservation (PROJECT.md п. 6 (а)), the named control on recorded data.** There are 25 recorded probe records
(Glob `scripts/tests/fixtures/stories/*/**/*provenance*`: 20 in cart-1, 5 in local-1-0108). Run before k4 deletes the old
function, at the end of k2 and of k3:
`python -B -c "import json,glob,sys; sys.path.insert(0,'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import profile_contract as P, gate_template as G; fs=sorted(glob.glob('C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/evidence/runtime-provenance-*.json')); rs=[json.load(open(f,encoding='utf-8')) for f in fs]; old=[P.acceptable_provenance(r,P.ACCEPTS) for r in rs]; new=[G.acceptable(P.provenance_word(r),'provenance.run') for r in rs]; bad=[G.acceptable(P.provenance_word(r),'nope.x') for r in rs]; print(len(rs), old==new, old==bad, sorted({str(r.get('result')) for r in rs}))"`
- expected: `25 True False [...]`;
- `old==bad` False is the negative control: the harness can fail, provided at least one record is accepted today;
- if every record is refused today, `old==bad` prints True and the control is void: report it, and add the synthetic
  matrix of k1 item 3 as the evidence.

Not run here (no shell).

### Fork F-k1 (F-T2, second half) — how a provenance site reaches the one predicate

- (a) **Recommended.** A PRODUCER of the acceptance word, then the predicate at each site.
  - `profile_contract.provenance_word(record, *, rehearsal=False, task=None, local_source=False) -> str` holds the
    validation of `acceptable_provenance` unchanged and returns one word of the row:
    - `matched`;
    - `person_confirmed` (only when `person_confirmed(record, task)`);
    - `no_changed_file` (a valid not_applicable with `reason_code: no_changed_file`);
    - `local_source` (a valid not_applicable on a local-source request);
    - `not_applicable` (any other valid not_applicable);
    - otherwise `unknown` or `mismatched` (never acceptable).
  - The row gains the words `no_changed_file` (not_applicable, reason_code `no_changed_file`) and `local_source`
    (not_applicable, reason_code `local_source`), so the existing tokens `not_applicable:no_changed_file` /
    `not_applicable:local_source` finally match through `acceptable`, and a bare `not_applicable` token takes every NA word.
  - At k4 the row's `field` turns `null`, so a raw record handed to `acceptable` is never acceptable (the C3-0 `live-record`
    row flips to False). Error direction: toward refusal, whatever a caller passes.
  - Cost: two words, one producer, one site edit per site, and the k4 test churn.
- (b) `gate_template.acceptable` grows a provenance branch that calls `acceptable_provenance`. That puts closed variety (one
  row's validator) in the generic predicate (FR-13, AR-1), and `gate_template` would import `profile_contract`. Not
  recommended.
- (c) The sites keep `acceptable_provenance` and are re-roled `validate`, with `acceptable_provenance` the only accept site
  (it calls `acceptable`). Every per-site literal acceptance (the local-source NA at :176, :832, :90) would have to move
  inside it, the re-roles hide the per-site decision from A26 (E-c), and K-T1.7's intent ("a call to acceptable_provenance
  is NOT the predicate") is bypassed. Not recommended.

Error direction of the reused function (`validate_runtime_provenance` / `person_confirmed`, now feeding a gate word):
toward refusal only. These adversarial inputs must stay refused, and become rows of k1's table:
- `MATCHED` and `Person_Confirmed` (the case) -> `unknown`;
- a `matched` with no evidence, outside rehearsal -> `unknown`;
- a `matched` whose deployed revision differs (effective `mismatched`) -> `mismatched`;
- a pc word given for another story -> `unknown`;
- a pc dressed as a reading (`technical_verification` true) -> `unknown`;
- a not_applicable with `reason_code` `No_Changed_File` -> `not_applicable` (not `no_changed_file`);
- `local_source=True` with an invalid NA -> `unknown`;
- a non-dict, `None` or a list -> `unknown`.

### Fork F-k2 — the bare `not_applicable` residue (registry `decides` :39; tokens :82, :84)

- `provenance.fingerprint` (`["matched", "person_confirmed", "not_applicable"]`). The code today takes ANY valid NA
  (`execution_fingerprint.py:121-122`, comment :118-119 "X3: the local_source request has no probe word; its own gate is
  validate_request"). (a) **Recommended**: keep the bare token, because it is the code's behaviour and the request gate
  stays stricter. (b) Tighten it to `not_applicable:no_changed_file` and `not_applicable:local_source`: a local-source run
  would lose its fingerprint (`local_source` is not passed at `build`), which is a behaviour change for local-source
  stories.
- `provenance.manual_capture` (`["matched", "person_confirmed", "not_applicable"]`). The code takes only `ACCEPTS`
  (`manual_capture.py:1612`), so no bare NA. (a) **Recommended**: tighten the token to `not_applicable:no_changed_file`, so
  the registry says what the code does. Converting with the bare token would WIDEN manual capture to every valid NA, a
  silent relax. (b) Keep the bare token and widen the code: a meaning change, which needs the owner.
- `decides` (k4) drops "residue: …" and says, per consumer, which not_applicable each takes.

### Fork F-k3 — what remains of `acceptable_provenance` and `ACCEPTS` (k4)

- (a) Keep `acceptable_provenance(record, consumer, *, rehearsal=False, task=None, local_source=False) -> bool` as the
  composition `acceptable(provenance_word(...), consumer)`, for non-site readers (`driver_stage_build.build_outcome`) and
  tests. `ACCEPTS` is deleted. It stays an `accept` site, and it calls `acceptable`.
- (b) Delete both; every reader spells `acceptable(provenance_word(...), consumer)`.

**Rec (a)**: one road (it IS the composition, P31), the smallest test churn (callers change their token argument to a
consumer id), and `build_outcome` keeps one call. Either way, `ACCEPTS`' readers change in k4: `execution_request.py:17`
(the import), `test_execution_request.py:17, :682-686, :1334`, `test_profile_contract.py:291-505` (eight calls),
`test_runtime_probe_onboarding.py:823, :1277, :1389`, and `test_role_commands.py:964` (`PC.ACCEPTS[:2]`). Under (a) the
`ValueError` on an unknown token (`profile_contract.py:908-910`) goes away, because an unknown consumer is False (C3-0
item 3). That is the census unit of the function; its shrink is named (AR-20).

### Fork F-k4 — the baseline consumer (F-T3 meets C3-k)

- Today `provenance.baseline: ["matched", "not_applicable"]` sits in `baseline_identity` (:349). Its tokens are exactly
  `validate_baseline_record`'s rule (:682-687), but under that row `acceptable("matched", "provenance.baseline")` resolves
  to `baseline_identity`'s words.
- C3-g (F-T3 (a), not yet carded) gives that row the receipt words `captured` / `inconclusive`, so the consumer cannot
  serve the provenance reader there.
- (a) **Recommended**: C3-k3 owns the move, because the consumer lands with its reader (AR-22).
  - It removes `provenance.baseline` wherever the merged main holds it.
  - It adds `baseline_identity.capture: ["matched", "not_applicable"]` under `provenance_acceptance`. The prefix
    `baseline_identity` inherits `promotable: false` through the prefix rule (`gate_registry.py:728-742`), so a later
    `person_confirmed` on it is a finding: the K-N2.12 NEG pin (:291-298) moves to this id and stays "exactly one finding".
  - C3-g's card then leaves `provenance.baseline` alone.
- (b) C3-g removes it and C3-k3 only adds the new id.

The Lead tells C3-g's designer which. Until then, k3 handles both worlds (E-k3.5).

### Fork F-k5 — the refusal text on an unreadable registry (FR-41, C3-b2 E8's class)

From k2 on, an unreadable registry makes every provenance site refuse, with "runtime provenance must be valid matched…" +
`refusal_text(probe)`: a false cause. (a) **Recommended**: `profile_contract.refusal_text` (the one sentence builder of
every provenance refusal, a `library` site :59) starts with "the gate registry cannot be read (<reason>): a factory
defect, the probe's answer was not judged" when `gate_template.registry_problem()` is non-empty. That is one place (AR-15)
and the family wording of the spec's small choices (t-1043). (b) No text; rely on C3-reg-precondition stopping the stage
first. Cost of (a): one branch and one test row, in k4. Until k4, k2 and k3 live with (b), as C3-b2 did before its
registry-why branch.

---

## §4. Card C3-k1 — the provenance word and the local-source test (foundation)

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`, §3 of this file and this card, the spec's S-a..S-f; read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/profile_contract.py:15-30,700-925`, `scripts/gate_template.py` (whole), `scripts/gate_registry.py:20-80,467-560`, `references/gate-registry.json:37-93`, `scripts/tests/test_profile_contract.py` (its tables, grep `acceptable_provenance|no_changed_file`), `scripts/tests/test_gate_registry.py:950-1043`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py` (new `provenance_word`, new `local_source_request`; nothing else)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: `words` +2, `verdict_map` +2, `sites` +2)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_profile_contract.py` (one table, item 3)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 only, item 4)
non-goals: every accept site (k2, k3); `acceptable_provenance` and `ACCEPTS` (k4); `accepts` (no new consumer: none has a reader yet, AR-22); status, vocabulary and field of the row (k4); `gate_template.py`; the census
handoff: report path given by the Lead
edges: E-k1.1-E-k1.6
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 (the debt block unchanged); then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py`, plus the printed non-slow files. `test_gate_registry.py` is slow: canon.
siblings: axis 5 (the row's words grow; the prose twins are walked in k4, when `decides` changes); the four copies of the local-source test (`execution_request.py:164`, `manual_evidence.py:80`, `coverage_contract.py:824, :845`) get one survivor here and are wired in k2/k3 (AR-15)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (C3-k1)

Items:
1. **`provenance_word(record, *, rehearsal=False, task=None, local_source=False) -> str`**, never raising. The body is
   `acceptable_provenance`'s (:911-923) with words in place of booleans:
   - a non-dict -> `unknown`;
   - `checked = validate_runtime_provenance(rehearsal_view(record) if rehearsal else record)`;
   - not valid, or `checked["result"] != declared` -> `checked["result"]` when it is `mismatched`, else `unknown`;
   - declared `matched` -> `matched`;
   - declared `person_confirmed` -> `person_confirmed` if `person_confirmed(record, task)` else `unknown`;
   - declared `not_applicable` -> `no_changed_file` if `no_changed_file(record)`, else `local_source` if `local_source`,
     else `not_applicable`;
   - anything else -> `unknown`.

   Docstring: the error direction (toward a word no consumer takes) and the fact that it is the ONE producer of every
   provenance consumer's word (C3-b2 E11's invariant).
2. **`local_source_request(record) -> bool`** = `isinstance(record, dict) and record.get("runtime_required") is False and
   record.get("target_kind") == "local_source"`: the one test the four sites copy.
3. **Registry.**
   - `words` += `no_changed_file`, `local_source`;
   - `verdict_map` += `"no_changed_file": {"class": "not_applicable", "reason_code": "no_changed_file"}` and
     `"local_source": {"class": "not_applicable", "reason_code": "local_source"}`;
   - `sites` += `{"file": "profile_contract.py", "function": "provenance_word", "role": "produce"}` and
     `{"file": "profile_contract.py", "function": "local_source_request", "role": "validate"}`.
   - Test, one table in `test_profile_contract.py` (the builder greps for an existing provenance table first and adds rows
     there). The rows are §3 F-k1's adversarial list plus the plain words: a valid matched -> `matched`; a pc for this
     story -> `person_confirmed`; a valid NA `no_changed_file` -> `no_changed_file`; a valid NA with `local_source=True` ->
     `local_source`; a valid NA alone -> `not_applicable`; a rehearsal matched with `observed_without_evidence` ->
     `matched` only when `rehearsal=True`.
   - Plus a cross-check row: for each row, `acceptable(provenance_word(r), c)` equals the old
     `acceptable_provenance(r, ACCEPTS)` for `c = "provenance.rehearsal"`, on the live registry.
   - expected from: the docstrings of `validate_runtime_provenance`, `person_confirmed`, `no_changed_file` and
     `acceptable_provenance`, and FR-59 — never from the new function's output.
4. **D13 (S-f).** Re-measure before and after. Expected new triples: `("profile_contract.py", "provenance_word",
   "provenance_acceptance")` and `("profile_contract.py", "local_source_request", "provenance_acceptance")`. The existing
   triples `validate_request`, `_provenance_errors` and `validate_manual_current` gain items (their `== 'local_source'`
   comparisons are now row words: about 4), and `no_changed_file` gains one (`== NO_CHANGED_FILE`, a module-level name,
   `gate_registry.py:24-25`). The count is the measurement, named with that list. A different set of new triples is a stop.

architecture content: `AR-13 -- one producer of the provenance word, one reader of the local-source exemption`; `AR-15 -- four copies of the local-source test get one survivor (wired in k2/k3)`; `AR-22 -- no consumer added before its reader`; `AR-20 -- D13 +2 triples, count re-measured and named`. judgment content: `none -- a producer of a data word after the existing validation; no check moves into judgment`.

Edges:
- E-k1.1 (empty / None / non-dict record): `unknown`. INVARIANT: an absent record never yields an acceptable word.
- E-k1.2 (case): `MATCHED` -> `unknown`. INVARIANT: only the exact word counts (C3-0 E3).
- E-k1.3 POSITIONAL: the validation runs BEFORE any word is chosen; the NA reason is read only after validity. INVARIANT:
  an invalid record never yields `no_changed_file` / `local_source`.
- E-k1.4 TEMPORAL: after k1, no site reads the new function yet. The row's two new words make the four `== 'local_source'`
  comparisons counted in debt accept sites, which is allowed until k4, and k2/k3 remove them. INVARIANT: `--check` stays
  green at every step.
- E-k1.5 (limit): none.
- E-k1.6 (one road): one producer for every provenance consumer, keyed by no language or project.

Commit lines (content): `architecture: AR-13, AR-15, AR-20, AR-22 -- <above>`; `judgment: none -- <above>`.

---

## §5. Card C3-k2 — the execution side through the predicate

given: as k1, plus `scripts/execution_request.py` (`validate_request`, `rehearsal_probe`, the import block :17-20; anchor by function name: C3-b2 moves lines), `scripts/execution_fingerprint.py:25-35,104-151`, `scripts/run_suite.py:120-126,916-930`, `scripts/probe_by_code.py:2880-2887`, `scripts/gate_preflight.py:3421-3447`, `scripts/tests/test_execution_request.py` (grep `rehearsal_probe|ACCEPTS|acceptable_provenance`, :590-690, :1330-1336), `scripts/tests/test_gate_preflight.py:4250-4340`, `scripts/tests/test_gate_registry.py:255-320,636-668,950-1043`, the merged k1 diff
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (`validate_request`: the runtime block; `rehearsal_probe`: signature `consumer="provenance.rehearsal"` and its body; the import line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_fingerprint.py` (`build`: the provenance condition; the import line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py` (`probe_runtime`; the import line :124)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (`_observed_identity` only) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: consumers, allow entries, two re-roles)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (rows; the K-N2.5 pin :1334-1335)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (the stub at :4261 and one row)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (the K-N2.12 callee rows of its sites :273-284; the NEG list :312-315; the F1 consumer list :642-645; D13)
non-goals: `_match` and `green_over_same_bytes` (C3-b2's); `probe_by_code.py` code (registry re-role only); the manual sites (k3); `acceptable_provenance` / `ACCEPTS` (k4); row status, vocabulary, field (k4)
handoff: report path given by the Lead
edges: E-k2.1-E-k2.8
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; the §3 recorded-data control printed with `25 True False`; then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`, plus the printed non-slow files. `test_execution_request.py`, `test_gate_preflight.py` and `test_gate_registry.py` are slow: canon.
siblings: axis 26-class "one reader of a verdict word" (the provenance word now has one producer); `driver_stage_build.build_outcome:381` (k4); axis 5 prose twins in k4
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (C3-k2)

Items:
1. **`validate_request`.**
   - `local_source = local_source_request(data)` replaces the literal at :164.
   - `word = provenance_word(provenance, task=data.get("task"), local_source=local_source)` and
     `taken = acceptable(word, "provenance.automation")` replace :175-176.
   - The refusal: `if not (taken or said_local)` with the same sentence.
   - :166 (the NA-specific sentence) and :169 (a person's word on a request that skips the probe) stay as they are and get
     `allow` entries, whole texts in the `ast.unparse` form `checked['result'] == 'not_applicable'` and
     `provenance.get('result') == 'person_confirmed'`, whys "picks the refusal sentence for a bare not_applicable; the
     acceptance is the acceptable() call" and "refuses a person's word on a request that skips the probe; it never lets a
     record through".
   - expected from: the comments :158-163, :170-174 and the current tokens of `provenance.automation` (:81).
2. **`rehearsal_probe(spec, consumer="provenance.rehearsal")`**: `if acceptable(provenance_word(value, rehearsal=True),
   consumer): return value`. The docstring's "ONE set" paragraph (:2493-2495) now names the consumer.
   `gate_preflight._observed_identity` passes `consumer="provenance.identity"` in place of the tuple (:3444).
   - Registry: new consumer `"provenance.identity": ["matched", "person_confirmed"]`.
   - `_observed_identity` is re-roled `dispatch` (it hands the consumer to the reader that accepts; no literal is left).
     That is a NEW E-c row for the plan critic.
3. **`run_suite.probe_runtime`**: `if acceptable(provenance_word(value), "provenance.run"): return value`. Registry: new
   consumer `"provenance.run": ["matched", "person_confirmed", "not_applicable:no_changed_file"]` (today's `ACCEPTS`,
   :877). `probe_by_code.probe_runtime` is re-roled `dispatch` (a pure delegate, :2886-2887; NEW E-c row).
4. **`execution_fingerprint.build`**: `if not acceptable(provenance_word(spec["runtime_provenance"]),
   "provenance.fingerprint")` replaces :121-122. :134 gets an `allow` entry
   (`runtime.get('result') == 'person_confirmed'`, why "keys the fingerprint of a run on a person's word; not an
   acceptance"). F-k2 (a): the bare token stays.
5. **Tests.**
   - `test_execution_request.py`: K-N2.5 becomes `er.rehearsal_probe.__defaults__[0] == "provenance.rehearsal"`. Rows in
     the existing provenance table (:590-690):
     - a local-source request with a valid NA -> admitted;
     - the same with an invalid NA -> refused;
     - `Person_Confirmed` -> refused;
     - the unreadable registry (the `gate_template._READ` seam, saved and restored in `finally`, precedent
       `test_gate_registry.py:1145-1157`) -> refused.
   - `test_gate_preflight.py:4261`: the stub's signature becomes `lambda spec, consumer=None: …`. One row: the call passes
     `consumer="provenance.identity"`.
   - expected from: item 1-4 and FR-59.
6. **Pins (`test_gate_registry.py`).**
   - K-N2.12: the callee of `run_suite.probe_runtime`, `execution_request.rehearsal_probe` / `validate_request` and
     `execution_fingerprint.build` becomes `acceptable`.
   - The K-T1.2 NEG list (:312-315) loses `gate_preflight._observed_identity` (its anchor tuple is gone).
   - F1 (:642-645): the provenance consumer list gains `provenance.identity`, `provenance.run`.
   - D13 re-measured. Expected: `_observed_identity`'s triple leaves; `validate_request` loses :164 and :176;
     `execution_fingerprint.build` loses :122. Named.

architecture content: `AR-13 -- every execution-side provenance acceptance reads the word through provenance_word and the predicate`; `AR-22 -- provenance.identity and provenance.run land with their readers`; `AR-28 -- an absent, malformed, other-case or unaccepted provenance is refused; an unreadable registry refuses, pinned`; `AR-29 -- each site's census unit and class unchanged`; `AR-20 -- D13 re-measured and named`. judgment content: `none -- a membership join of a validated data word; the validation is unchanged`.

Edges:
- E-k2.1 POSITIONAL (`validate_request`): :166 and :169 stay BEFORE the predicate and `said_local` still suppresses the
  second sentence. INVARIANT: one sentence per refused record, the same sentence as today.
- E-k2.2 (unreadable registry, from this card on): every provenance read of these sites refuses: a run, a rehearsal or a
  fingerprint is refused (cost and a false cause until k4's F-k5). C3-reg-precondition stops the dispatch first. INVARIANT:
  a broken registry never admits a probe.
- E-k2.3 TEMPORAL: the row is still `debt`, so the literals left are allowed; the allow entries are written now and are
  inert until k4. INVARIANT: `--check` green at every step, and every allow entry matches a comparison (F-d).
- E-k2.4 (consumer typo): `acceptable` is False, the probe is refused, and A26 `--check` plus the positive table rows turn
  red in CI (C3-reg-precondition E2). INVARIANT: no false accept.
- E-k2.5 (one producer per consumer, C3-b2 E11): every provenance consumer is fed only by `provenance_word`.
- E-k2.6 (HOT): `очередь: C3-rr → C3-j → C3-k2 → C3-h` (gate_preflight.py); `C3-b2 → C3-k2` (execution_request.py).
- E-k2.7 (TEMPORAL, recorded records): the 25 recorded probe records give the same answers (the §3 control). INVARIANT: no
  recorded run changes meaning.
- E-k2.8 (limit): none.

Commit lines (content): `architecture: AR-13, AR-20, AR-22, AR-28, AR-29 -- <above>`; `judgment: none -- <above>`.

---

## §6. Card C3-k3 — the manual side, the deploy proof, the dead consumers

given: as k1, plus `scripts/manual_evidence.py:15-20,74-133,658-707`, `scripts/coverage_contract.py:771-858`, `scripts/manual_capture.py:95-100,1585-1615`, `scripts/environment_preparation.py:330-402`, `references/gate-registry.json:315-356`, `scripts/tests/test_gate_registry.py:255-320,636-668`, the merged k1/k2 diffs, the merged C3-g diff if any
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py` (`_provenance_errors`, `validate_baseline_record`; the import line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py` (`validate_manual_current`: the runtime block and its import line :818)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py` (`stand_probe`; the import line :99)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_preparation.py` (`_run_step`: the provenance condition :388 and an import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: consumers, allow entries, one re-role; row `environment_preparation`: `accepts` emptied (A2); row `baseline_identity`: `provenance.baseline` removed if still there (F-k4))
- the existing keep test files that `--witness-for` prints for these four scripts (rows only; the builder names them before writing)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (K-N2.12 rows of its sites; the g7 list :262-267 and the NEG list :312-315 lose `_run_step`; F1 :639-656; K-N2.12 NEG :291-298; D13)
non-goals: the execution side (k2); conversion (k4); `manual_evidence.validate`, `person_sentences`; `_other_profile_errors` code (registry re-role only); `baseline_contract.py` (C3-g)
handoff: report path given by the Lead
edges: E-k3.1-E-k3.7
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; the §3 control `25 True False`; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`, plus the printed non-slow files (`test_environment_preparation.py` is keep and fast, spec §0.3); the slow ones named, canon.
siblings: F-T3 / C3-g (the baseline consumer, F-k4); A2 (the deploy consumer); axis 19 (stage twins: manual capture <-> manual record keep one rule, AR-19 `_provenance_errors` docstring :75-76)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (C3-k3)

Items:
1. **`_provenance_errors`**: `local_source = local_source_request(record)` (:80). The elif at :89-90 becomes
   `elif not acceptable(provenance_word(probe, task=story, local_source=local_source), "provenance.manual")`. :86 gets an
   `allow` entry (`probe.get('result') == 'not_applicable'`, why "picks the NA-specific sentence; the acceptance is the
   acceptable() call"). `_other_profile_errors` is re-roled `validate`, with why: it calls `_provenance_errors` for each
   pair (pinned :281-282), and its :129 only skips the revision binding for a probe that bound none. NEW E-c row.
2. **`validate_baseline_record`**: `if not acceptable(provenance_word(probe), "baseline_identity.capture")` then the error
   is `say_refusal("baseline_person") if checked["result"] == "person_confirmed" else "manual baseline runtime provenance
   is unverified"` (`checked` kept for the sentence). :686 is gone; :682's comparison gets an `allow` entry (why "picks the
   refusal sentence; a person's word is refused by the consumer's tokens").
   - Registry: `"baseline_identity.capture": ["matched", "not_applicable"]` under `provenance_acceptance` (F-k4 (a)).
     `provenance.baseline` is removed from `baseline_identity` if the merged main still holds it.
3. **`validate_manual_current`**:
   - `local_source = local_source_request(record)` (:824);
   - :831-832 become `acceptable(provenance_word(probe, task=story, local_source=local_source), "provenance.manual")`;
   - :845's inline copy of the local-source test becomes `local_source`;
   - :839 and :845 get `allow` entries: "an NA probe compared nothing and binds no checkout revision" and "a second
     refusal sentence for a bare not_applicable; never lets a record through".
4. **`stand_probe`**: `if not acceptable(provenance_word(value, task=story), "provenance.manual_capture")`. F-k2 (a): the
   consumer's tokens become `["matched", "person_confirmed", "not_applicable:no_changed_file"]`.
5. **`_run_step`** (A2): `provenance_ok = bool(acceptable(provenance_word(receipt), "environment_preparation.deploy_proof")
   and <the two equalities>)`. `checked` stays for `provenance_validation`.
   - Registry: `"environment_preparation.deploy_proof": ["matched"]` under `provenance_acceptance`. Its prefix names
     `environment_preparation` (`promotable: false`), so a `person_confirmed` added later is a finding (the F1 guard, kept
     by the prefix rule).
   - `provenance.environment_preparation` is removed from the row `environment_preparation` (`accepts: {}`).
   - This reads A2's "under a row whose promotable is false" through the prefix rule: the consumer must sit under a row
     whose WORDS include `matched` (`environment_preparation`'s are `blocked`/`unknown`, :322) — see fork F-k6.
6. **Tests.** In the keep files printed for each script, the builder greps for the existing provenance rows and adds:
   - a local-source manual record with a valid NA -> no error;
   - an invalid NA -> error;
   - a manual capture probe with a valid bare NA (no `reason_code`) -> refused (F-k2);
   - a baseline pc -> the `baseline_person` sentence;
   - a deploy receipt `person_confirmed` -> `provenance_ok` False;
   - the unreadable registry -> refused in each.

   Expected from: items 1-5, the docstrings, FR-59.
7. **Pins (`test_gate_registry.py`).**
   - F1 :639-641: the two ids are replaced by `baseline_identity.capture` and `environment_preparation.deploy_proof`, both
     under `provenance_acceptance`.
   - F1 :646-647 stays: both guarding rows are promotable false.
   - The F1 loop :648-656 runs on the new ids, still one finding each, naming the consumer and the guarding row.
   - K-N2.12 NEG :291-298 uses `baseline_identity.capture`.
   - g7 and NEG lists lose `_run_step`.
   - K-N2.12 callee rows of these sites -> `acceptable`.
   - D13 re-measured: `_run_step`'s triple leaves; the others lose their acceptance literals. Named.

architecture content: `AR-13 -- every manual-side provenance acceptance reads the word through provenance_word and the predicate`; `AR-22 -- the two replacement consumers land with their readers, the two dead ones leave in the same commit`; `AR-28 -- unaccepted, malformed or unreadable-registry provenance is refused, pinned`; `AR-29 -- units and classes unchanged`; `AR-20 -- D13 re-measured`. judgment content: `none -- <as k2>`.

Edges:
- E-k3.1 POSITIONAL: the NA-specific sentence (:86) stays before the predicate (elif). INVARIANT: one sentence per refused
  probe.
- E-k3.2 (the baseline): a person's word is refused by the tokens, and the sentence still says why (`baseline_person`).
  INVARIANT: a person's word never stands in for the old build (`baseline_identity.decides` :337).
- E-k3.3 (manual capture tightened, F-k2 (a)): the code already refused a bare NA; the registry now says so. INVARIANT: no
  probe refused today is taken after.
- E-k3.4 (deploy proof): only `matched`. INVARIANT: a person's word never stands in for the deploy's proof (F1).
- E-k3.5 TEMPORAL (C3-g): in world (i), C3-g merged and removed `provenance.baseline`: nothing to remove. In world (ii),
  it is still in `baseline_identity`: removed here. INVARIANT: after k3, no consumer without a reader exists, and the guard
  pins (F1, K-N2.12 NEG) still count exactly one finding.
- E-k3.6 (unreadable registry): as E-k2.2.
- E-k3.7 (limit): none.

Commit lines (content): `architecture: AR-13, AR-20, AR-22, AR-28, AR-29 -- <above>`; `judgment: none -- <as k2>`.

---

## §7. Card C3-k4 — the conversion

given: as k1, plus all merged k1-k3 diffs, `scripts/driver_stage_build.py:360-400`, `scripts/tests/test_profile_contract.py:280-510`, `scripts/tests/test_runtime_probe_onboarding.py:815-830,1270-1395`, `scripts/tests/test_role_commands.py:955-970`, `scripts/tests/test_gate_registry.py` (S-f lines, :697-704, :1131-1136)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: status, debt_ref, vocabulary, field, decides, the `provenance.manual_capture` tokens if not done)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py` (`acceptable_provenance` recast, `ACCEPTS` deleted (F-k3 (a)), `refusal_text`'s registry clause (F-k5 (a)))
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (the import line only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py` (`build_outcome`: the one call at :381)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_profile_contract.py`, `.../test_runtime_probe_onboarding.py`, `.../test_role_commands.py`, `.../test_execution_request.py` (the `ACCEPTS` / `acceptable_provenance` call rows only; the S-b row)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `provenance_acceptance`; F2 live check :697-704; K-N2.12 positive control :287-288; the C3-0 row `live-record` :1136)
non-goals: any site's acceptance logic (k2, k3); `gate_template.py`; C3-reg-precondition's block
handoff: report path given by the Lead
edges: E-k4.1-E-k4.7
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, `provenance_acceptance` is absent from the debt block, and no F-b line names any of its accept sites; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`, plus the printed non-slow files; slow ones named, canon.
siblings: axis 5: `decides` changes, so the builder greps `references/execution-lifecycle.md`, `manual-evidence.md`, `environment-preparation.md`, `phases/s5.md` / `s6.md` for `acceptable_provenance|ACCEPTS|not_applicable` and gives a line per hit; findings named in the waiting list (C3-rr `selector_contract`, C3-b2 R12)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (C3-k4)

Items:
1. **Row.**
   - `status: converted`, `debt_ref: ""`, `vocabulary: code`, `field: null` (F-k1 (a)).
   - `decides`: "the probe's record is good enough for this use: `profile_contract.provenance_word` validates it and names
     its word, and `gate_template.acceptable` takes it for the consumer; per consumer: …", one clause each, no residue.
   - `unknown_branch` / `on_no_answer` / `waits_at` keep `question / wait / stage_entry` (decided table: keep).
2. **`acceptable_provenance(record, consumer, *, rehearsal=False, task=None, local_source=False)`** =
   `acceptable(provenance_word(record, rehearsal=rehearsal, task=task, local_source=local_source), consumer)`. `ACCEPTS` is
   deleted. `driver_stage_build.py:381` becomes `acceptable_provenance(record, "provenance.rehearsal", rehearsal=True)`. Test
   callers change their token argument to a consumer id:
   - `P.ACCEPTS` -> `"provenance.run"`;
   - `("matched",)` -> `"environment_preparation.deploy_proof"`;
   - `("matched", "person_confirmed")` -> `"provenance.identity"`;
   - `test_role_commands.py:964` reads the words from the registry row (`PC.ACCEPTS[:2]` was `matched`, `person_confirmed`);
   - `test_execution_request.py:686` (an unknown token raised `ValueError`) becomes "an unknown consumer is False" (C3-0
     item 3).
3. **`refusal_text`** (F-k5 (a)) starts with the registry sentence when `registry_problem()` is non-empty. One row in
   `test_profile_contract.py` (the `_READ` seam).
4. **S-b (the registry `test` file `test_execution_request.py`).** One row: a request whose provenance is `unknown` ->
   refused, nothing runs; the unreadable registry -> refused, and the sentence names the registry. Expected from FR-59 and
   F-k5.
5. **S-f pins.**
   - `EXPECTED_DEBT` loses the row and `EXPECTED_CONVERTED` gains it; K-T1.2 N-1; split +1/-1; F4 `code` list +1.
   - K-N2.12 positive control: `validate_runtime_provenance` is now called in `provenance_word`, so the control reads that
     function.
   - The F2 live check (:701-704) on `profile_contract.ACCEPTS` is re-pointed to a set the module still binds, or dropped
     with its reason in the diff (the set is gone; F2's synthetic rows still pin the rule).
   - C3-0 `live-record` -> False (`field: null`).
   - D13 re-measured: the `<module>` vocabulary item of `ACCEPTS` leaves; with `vocabulary: code` no new word is counted (the
     words are unchanged since k1). Named.

architecture content: `AR-13`, `AR-15 -- one provenance predicate path: provenance_word then acceptable; acceptable_provenance is its composition`, `AR-28 -- an unknown or unreadable-registry provenance is refused and says why, pinned by the S-b row`, `AR-29 -- acceptable_provenance's census unit shrinks if its raise goes (named)`, `AR-20 -- debt -1, converted +1, F4 +1, D13 named`. judgment content: `none -- the row converts; every acceptance is a data join after the unchanged validation`.

Edges:
- E-k4.1 TEMPORAL: before k4 the row is debt and literals are allowed; after it, every accept site needs `acceptable` and
  every literal an `allow`. k2/k3 already did both. INVARIANT: `--check` green on k4's tree.
- E-k4.2 (field null): a record passed whole to `acceptable` under a provenance consumer is False. INVARIANT: no
  unvalidated record is ever accepted.
- E-k4.3 (unreadable registry): the refusal names the registry (F-k5). INVARIANT: FR-41.
- E-k4.4 (stories in flight, E-a): a probe record written before k4 is re-judged by the same rules. INVARIANT: the §3
  control equal.
- E-k4.5 (S-f TEMPORAL): deltas from the main k4 is based on, after C3-j.
- E-k4.6 (readers of `ACCEPTS`): every reader listed in F-k3 changes in this commit. INVARIANT: no import of a deleted
  name survives (an `ImportError` at import time breaks a whole script).
- E-k4.7 (limit): none.

Commit lines (content): `architecture: AR-13, AR-15, AR-20, AR-28, AR-29 -- <above>`; `judgment: none -- <above>`.

---

## §8. Forks (returned, not decided)

- **F-k1** (F-T2 second half): the provenance word producer + `acceptable` at each site; rec (a). §3.
- **F-k2** (the bare not_applicable residue): fingerprint keeps bare, manual_capture tightened to `no_changed_file`;
  rec (a)/(a). §3.
- **F-k3** (`acceptable_provenance` / `ACCEPTS`): recast to a consumer id, `ACCEPTS` deleted; rec (a). §3.
- **F-k4** (baseline consumer, coordination with C3-g): C3-k3 owns the move to `baseline_identity.capture`; rec (a). §3.
- **F-k5** (registry sentence in `refusal_text`): rec (a), in k4. §3.
- **F-k6** (A2's wording): A2 says the deploy consumer goes "under a row whose promotable is false". Under `acceptable`, a
  consumer resolves to its row's WORDS, and `environment_preparation`'s words (`blocked`, `unknown`) hold no `matched`, so
  such a consumer could accept nothing. (a) **Rec**: the consumer `environment_preparation.deploy_proof` sits under
  `provenance_acceptance`. Its prefix inherits `promotable: false` through `gate_registry.py:728-742`, so the guard is the
  same rule, enforced. (b) Give `environment_preparation` the word `matched`: that adds a word its own code does not write
  (S-c), which is dishonest. The Lead confirms the reading.
- **F-k7** (the split): four cards k1..k4 (rec), or k1+k2 merged into one node. Cost: k1+k2 together is one HOT-file
  node that is larger to review.
- **F-j3** (the card form): (a) **Rec**: a stand-gap row with `card_door` (accept / accept always from data) plus the two
  existing doors as `answers` lines. (b) A PERSON_DECIDES finding like `_stand_limit_card`, with `accept always` only as a
  CLI door. That is a second road for "do not ask again" (P31) and against F-C2 (a)'s "existing card -> record -> cover
  road".
- **F-j4** (E9's breadth, an owner-facing note): a waiver written for an `over` card of a profile also passes its
  `unmeasured` card, because both open with `e2e stand limit: <profile>` (F-j2 as decided). (a) Keep, as decided. (b) Give
  the unmeasured card its own block (`e2e stand limit not measured: <profile>`), so an old `over` waiver does not cover a
  different fact. The waivers recorded on unmeasured cards are none, because no card existed (a note only, :3192). Rec
  (b) is closer to FR-7 ("a boundary answered is never re-asked with the SAME text" — and an answer is not stretched to
  another boundary), but F-j2 was decided (a). Returned to the Lead, not re-decided here.

## §9. Small technical choices closed

- The gap id `SL-<profile>` (stand limit), beside `RP-<profile>` (reporter).
- `wait_s` is a string in the key, `f"{wait:g}"`, because `_valid_key` requires str fields.
- The wait is keyed from the config in `_limit_key`, not from the gap row (one derivation for the gate and the CLI, M8).
- `references/question-vocabulary.json` and `gate_brief.py` are dropped from C3-j's owns: `accept always` is offered by
  `property_key` presence (gate_brief :965) and the words are data. The spec's sketch named them.
- `check_s5_reporter` is registered `validate` under `s5_stand_limits` (A1's class).
- New consumers `provenance.run` and `provenance.identity`: one consumer per decision (C3-b2 E11's spirit), rather than
  reusing `provenance.automation` for the run path.
- The local-source test becomes one function (`local_source_request`), so the new row word `local_source` is compared
  only in a `validate` site.

## §10. Readers of every touched file (rule 7)

Commands (Grep tool, count mode):
- `environment_record|gate_preflight|gate-registry|profile_contract|execution_request|manual_evidence|coverage_contract|manual_capture|run_suite|execution_fingerprint|environment_preparation|probe_by_code|driver_stage_build|stand_gaps|gate_template`
  over `tools/`: 23 hits in 10 files.
- The changed names `acceptable_provenance|ACCEPTS|rehearsal_probe|check_s5_stand_limits|record_lasting|_observed_identity`
  over `tools/`: 0. The positive control is the previous call: the same tool, path and mode found `gate-registry` hits.
- The file names with control `architecture_gate` over `.githooks/`: 1. With control `hygiene_gate` over
  `.claude/settings.json`: 1. With control `designer` over `.claude/agents/`: 3. Each count equals the control's own count
  in t-1043 §8, so 0 for the names (the per-hit content was not printed).

| touched | reader | verdict |
|---|---|---|
| gate-registry.json (C3-j, k1-k4) | `tools/source-split-carriers.json:15` (verify `test_gate_registry.py`), `:35`; `tools/test_quarantine.py:2199` (path); `tools/source_split.py` (9 hits, the registry carrier, spec §8); package: `gate_registry.py`, `gate_template.py`, `test_gate_registry.py` | unchanged: file name and row form unchanged; pins: S-f per card |
| test_gate_registry.py | `tools/source-split-carriers.json` (D13 py-triple carrier, spec §8), `tools/source_split.py` (selftest strings) | unchanged: triples keep the `(file, function, row)` form |
| execution_fingerprint.py (k2) | `tools/dup-baseline.json:109` (`_dotted` clone group); `tools/controller-blocks-gen.py:191` (text) | unchanged: `build` is edited, not `_dotted` |
| probe_by_code.py (k2: registry only) | `tools/controller-blocks-gen.py:145` (text) | unchanged |
| test_execution_request.py (k2, k4) | `tools/lint-baseline.json:223-225` (`execution_request as er` import) | unchanged unless the import line moves; the builder re-runs the lint ratchet check named in the report if it does |
| coverage_contract.py | `tools/story_capture.py:500` (`coverage_contract_revisions`, a key name, false positive) | unchanged |
| test_piles.py / test_piles_split.py / fixtures K8.txt | name strings (not read per hit) | unchanged: no file is renamed |
| environment_record.py, gate_preflight.py, stand_gaps.py, profile_contract.py, manual_*.py, run_suite.py, environment_preparation.py, driver_stage_build.py | no hit in tools/ beyond the above | unchanged |
| package readers of changed names | `acceptable_provenance`: the sites above, `driver_stage_build.py:381` and five test files (grep listed in F-k3); `ACCEPTS`: `execution_request.py:17`, `coverage_contract.py:818`, `execution_fingerprint.py:30`, `manual_capture.py:99`, `manual_evidence.py:17`, `run_suite.py:124`, and tests; `rehearsal_probe`'s parameter: `gate_preflight.py:3438-3444`, `test_gate_preflight.py:4261`, `test_launch_wrappers.py:168` (positional, unchanged), `execution_request.py:3317` (the function object, unchanged) | change in k2 (rehearsal_probe readers), k2/k3 (the site imports), k4 (`ACCEPTS`, `acceptable_provenance`) |

## §11. Reading trail

On cc1eb6b8 (the root checkout, main = origin/main, refs read directly):
- the spec :1-115, :270-409, :533-1381, :1547-1745, :1745-2348 (forks, every Lead decision section, the reading trails);
- `references/gate-registry.json` :1-95, :315-356, :479-527 (+ grep of `"id":`);
- `scripts/gate_template.py` whole;
- `scripts/gate_registry.py` :20-130, :200-264, :460-743, :746-899;
- `scripts/tests/test_gate_registry.py` :36-75, :240-349, :575-775, :945-1159 (+ grep of the pins);
- `scripts/profile_contract.py` :690-940 (+ grep `PROVENANCE_RESULTS`, `ACCEPTS`);
- `scripts/execution_request.py` :120-229, :2440-2527 (+ grep `rehearsal_probe`);
- `scripts/execution_fingerprint.py` :80-160;
- `scripts/manual_evidence.py` :20-160, :618-707;
- `scripts/coverage_contract.py` :771-858;
- `scripts/environment_preparation.py` :330-420 (+ grep);
- `scripts/manual_capture.py` :1575-1634;
- `scripts/run_suite.py` :895-939;
- `scripts/probe_by_code.py` :2880-2905;
- `scripts/gate_preflight.py` :1582-1660, :3089-3303, :3418-3467, :4130-4250, :6078-6110 (+ greps);
- `scripts/driver_stage_build.py` :340-400;
- `scripts/environment_record.py` :1-440;
- `scripts/stand_gaps.py` :420-449, :1243-1272 (+ grep of `scope` reads);
- `scripts/tests/fixtures/judgment-census.json` (grep of the owned functions);
- greps over `scripts/*.py` for `acceptable_provenance\(`, `\bACCEPTS\b`, `_e2e_limit\(|skip_stand_limits`,
  `record_lasting|stand_gap_words|accept always`;
- Glob of the recorded provenance records (25) and of the fixture stories;
- the fixture grep for stand-limit fields (0, with the control 179);
- the rule-7 greps above;
- `tools/dup-baseline.json` :100-115.

Not read (never written as checked):
- `limit_seconds`' defining module;
- `gate_name` / `stand_gaps.collect`'s handling of a row whose finding was dropped (C3-j item 3 leaves it to the builder,
  bound by its invariant);
- `stand_gaps.py` :190-340 and :955-1020 beyond the grep lines;
- `gate_brief.py` :720-1000 beyond the grep lines;
- `environment_property_cover`'s row body (:527-548);
- the existing test tables named in the cards;
- `test_judgment_census.py`'s reading of the new helpers;
- `references/question-vocabulary.json`;
- C3-b2's diff `18f585f5` (no shell; the cards anchor on function names in `execution_request.py`);
- whether C3-g is carded or built.

Nothing was RUN: no `--check`, no `--sites`, no `GR.analyse`, no recorded-data control. Every D13 delta is an expectation
from the read comparisons, and the measurement decides.

## Lead decisions on the forks (17.11.2026, owner away: by recommendation, until the owner's word)

- F-k1 = (a); F-k2 = (a)/(a); F-k3 = (a); F-k5 = (a); F-k6 = (a) (the reading is confirmed against
  `gate_registry.py:728-742`: a consumer's prefix inherits its row's `promotable`); F-k7 = four serial cards k1..k4.
- F-k4 = (a), with a collision to settle: card C3-g (`20261117-rules-debt-wave3-g-h-cards.md`, G-0 (a)) removes
  `provenance.baseline` and adds the consumer `baseline_identity.readiness`; C3-k3 moves the baseline consumer to
  `baseline_identity.capture`. The plan critic of these cards says whether the two are one consumer under two names
  or two true sites, and which card owns the registry edit; C3-g lands first.
- F-j3 = (a): a stand-gap row with `card_door`.
- F-j4 = (b), CHANGING F-j2's earlier (a): the unmeasured card gets its own block text
  (`e2e stand limit not measured: <profile>`), so a waiver recorded for an `over` card does not pass a different fact
  (FR-7, FR-4: a check stops a silent pass). Safe direction: one more question, never a silent pass. For the owner's
  morning list.
- All five cards go to ONE plan critic before any builder; anchors are re-read by each builder on its base.
