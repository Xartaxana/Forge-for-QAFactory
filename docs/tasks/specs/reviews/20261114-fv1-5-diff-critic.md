# t-752 — critic on FV1-5 diff (a03ea51, origin/wip/fv1-5 vs origin/main)

Reviewer: critic (Opus), one pass, no code edited. DoD: spec `docs/tasks/specs/20261113-fv1-17-5-15-stand-login-spec.md`, card "### FV1-5" (items 1-6, edges, DoD, AR) and 2.3; the Lead's two extra edges from the dispatch.

**Verdict: fit_with_fixes (NEEDS WORK). 0 blockers against the card as written. One fix for this round needs the Lead to amend the spec, because it changes a meaning (PROJECT.md acceptance 6): the card's own mapping `no_address -> "did not answer"` is false (F1).** This verdict is input to acceptance. The decision to accept, and the spec amendment, belong to the Lead.

## Findings

**F1 (fix this round; needs a Lead amendment of the card, item 3 and the INVARIANT): a stand with NO ADDRESS is worded "did not answer when I checked it just now", but the probe says nothing was asked.** I ran it end to end, a real subprocess with `--env Local` on a config whose `environments: [{"name": "Local"}]` has no address:
```
{'access': {'kind': 'none'}} exit 1 words ['no_address']
  liveness line: ["liveness: unchecked — no address: the environments[] entry 'Local' has none of its own, and the environment block names none, so nothing was asked. Door: give the environments[] entry its own base_url ..."]
  person reads: the stand `Local` did not answer when I checked it just now
```
Lines: `driver_stage_build.py:42` (`"no_address": "dead"`) and `:50`. The producer is `env_probe.py:1102` (`unchecked_under_env` = liveness `unchecked`). This is exactly the defect class FV1-5 exists for: a false "did not answer" when the stand was never asked (FR-41, AR-28). The builder followed the card, which wrongly calls `no_address` "the probe's evidence of a dead stand". The fix is one map entry: `no_address -> "config"`. Then the person reads "could not be checked: its setting in the project's config is missing or broken", which is literally what the probe's Door says. Move the test row `("no_address", ["no_address"], DEAD_SAYS)` (`test_human_questions.py`, STAND_WHY_ROWS) to CONFIG_SAYS. Same surface, a sibling to decide with it: the `config` class (and `unknown`) still get the dead-stand retry option "bring `<x>` up, or fix what stops it answering" (`driver_stage_build.py:68-70`), which is wrong for a config fault. Recommendation: one `config` retry text ("fix the stand's setting in the project's config; I check it again"). The card says "others unchanged", so this is the Lead's call.

**F2 (fix this round, report): the builder's claim that `test_story_run_stand.py:40,62` go red is wrong, by empirics.** Those rows run the REAL probe against the discard port `D2_DEAD = http://127.0.0.1:9` (`story_run_common.py:475`, `d2_seed`/`d2_stand_at`). I ran the same config by subprocess. Output: `REAL Local exit 1 words ['stand_dead']`, `REAL Staging exit 1 words ['stand_dead']`, `dead sentence: True` for both. So :40 ("the stand `Local` did not answer when I checked it just now"), :42 ("bring `Local` up") and :62 ("the stand `Staging` did not answer") stay GREEN. The report (`20261114-fv1-5-report.md:110`) must not hand the owner two quarantine reds that do not exist. The builder's own words for them: "slow, not run". This is an unverified claim (critic rule 12). It is an inference from my in-process run of the same probe; I did not run the quarantined file itself.

**F3 (fix this round, changelog accuracy): `changelog.d/fv1-5-stand-check-words.md:9-10`** says the S0 warning "now say[s] 'did not pass its check'". The S0 warning says "did not pass **the** check" (`driver_s0.py:2435`). Line 7 also says the stand question "has four sentences". The `config` sentence is not reachable from `stand_check` (F5), so a release reader is told about a behaviour the driver never shows. Word it as "can say".

**F4 (queue, proposed node; owner Lead, live-run-fvf): the reason for "why the probe blocks" travels by two roads that disagree.** `--json` carries the producer's words. The driver re-parses the text by prefixes. `selection`, `env_file` and `device` lines have no fixed prefix, so through the driver they are `unknown`. Real run: `REAL selection exit 1 words ['unknown']`. Also, "ENVIRONMENT: not configured" is printed only when `not env_name` (`env_probe.py:1248`), and `stand_check` always passes `--env`. So the `config` sentence (and `device -> dead`) is unreachable in production: a missing env file reads "I could not check the stand". This is safe-direction (no false verdict), and the builder flagged it honestly ("Choices", report :119-121). It is still one fact with two roads (P31 / AR-13, critic-diff-brief item 12). Proposed node: the probe prints its `blocked_by` words on a column-0 line beside the three verdict lines, and `blocked_by_of` reads that line. One road, all seven words, and the LAYER1 prefix matching (F6) is no longer load-bearing.

**F5 (queue, same node as F4): `device` conflates a crashed device probe with a dead device.** `_device_answer` gives `["device"]` to "could not be read" / "could not be checked (<Exception>)" / "gave no verdict" (`env_probe.py:965-976`). The card maps `device -> "did not answer"`. Today only `--json` carries the word and no consumer maps it, so the risk is latent. Once F4 lands, a crashed device probe would read "did not answer", which breaks the INVARIANT's "a crashed probe is unknown". Split the word (`device` vs `unknown`) in the same node.

**F6 (queue, code quality, low): two edit sites per Layer-1 word.** `_word_of_item` (`env_probe.py:1220-1230`) hard-codes one branch per LAYER1 key instead of iterating `LAYER1`. A word added to `LAYER1` without a branch silently reads `unknown`. That is the safe direction, so this is not a blocker. Fold it into F4's node.

**F7 (queue, duplication): two parsers of the same Layer-1 block with different stop rules.** `driver_s0.probe_reason` (`driver_s0.py:2502-2507`) takes the first `- ` line after the header and skips blanks. `blocked_by_of` (`env_probe.py:1206-1214`) stops at the first non-`- ` line. Probe: header + blank + dead item gives `blocked_by_of -> ['unknown']`, while `probe_reason` finds the item. The producer never emits that shape, so this has no live effect. The card sanctions both readers ("probe_reason stays"). Converging on one `layer1_items(out)` helper in `env_probe` belongs to F4's node.

**F8 (queue; owner Lead, FV1-15 / first-look finding item 3):** the login `retry` option says "...or name the way the project signs in". This asks the PERSON for what the owner's word of 13.11 gives to the ROLE (see key 10). It is text the card dictated, so this is not a builder defect.

**F9 (queue, sibling carriers outside the owns; map axis 5 "Acquisition ladder", the stand row):**
- `skills/qa-story/phases/s0.md:405`: "a probe that did not answer" (role prose about `environment_pending`; the builder noticed it).
- `references/stand-answers.json:132`: `login_not_tried.skipped = "the stand did not answer"`, read by `stand_health.py:733`. A recorded `skipped` login also comes from "the stand has no address", "the env file was not found", "a device stand has no login by code" and `--no-login`. So `stand_health` can say "was not tried (the stand did not answer)" for a stand that was never asked. I found this by reading, not by running.

Each needs a line `<what> | узел: <id>` in an untaken live-run-fvf batch (Lead).

## Keys

1. **Items 1-6 and edges.**
   - Item 1: built as written. `LAYER1` is used by the producer lines. The body-shape line keeps `receipt["fix"]`, whose only producer is `stand_access.LOGIN_FIELD_FIX` (`stand_access.py:404`). The fatal and device returns carry their words.
   - Item 2: built as written. The builder decided that `[]` needs a `liveness:` line and otherwise returns `unknown`; that is the safe direction.
   - Items 3-6: built as written. The retry `what` slot is shortened; that is acceptable.
   - Edges: INVARIANT literal holds (key 2), but its no_address premise is false (F1). POSITIONAL holds. The first word decides. EMPTY holds. TEMPORAL: no reader of the old warning text (Grep below). The Lead's edges: an unknown word gives `unknown` (`why=['STAND_DEAD']`, `['wrong_door']` row), and `None` behaves as empty (empirics below).
2. **Direction of error.** No input made a non-dead word say "did not answer", and no unknown said "answers". Empirics are in the trail.
   - Edge cases that resolve to `unknown`: a traceback, a traceback quoting the print source, a `py()` timeout text, a non-ASCII item, a missing space after the colon, an upper-case variant, a blank first item, an empty body-shape fix.
   - Edge cases that resolve to `stand_dead`: CRLF stays correct, and a key whose name sits inside a dead prefix stays `stand_dead`.
   - Two theoretical shapes read as dead: a header at column 0 *inside* a traceback, and an indented header. The probe never emits either. Only F1 is a live false sentence.
   - Exit-0 text with a block: `stand_check` returns at `code == 0` (`driver_stage_build.py:132`) before the reader, so it is unreachable.
3. **Producer and JSON.** `blocked_by` is appended in the same statement as each `layer1` line (`env_probe.py:1138-1157`). The test row checks equal length and that exit 0 gives `[]`. Real `--json` keys: `['liveness', 'login', 'keys', 'layer1', 'blocked_by']`. The four old keys are untouched. The six `test_env_selected_stand` rows (`:383`, `:396`, `:495` and others) assert `sorted(data) == [four]`, so they are red for the ADDITIVE key only.
4. **Text a person reads.** The four sentences and both retry texts pass `human_text.problems` (rows green in my re-run). Read by hand against `human-questions.md`: no field name, path, key value or URL. The question body carries only the stand's name, and the probe text goes to `details`, as before. The `says` reference to "the details" points at the details file named in the answer block (rule 5). The open-ended "name the way" is F8.
5. **Layer-1 producer words.** Diffed: each `-` line and its `+` line concatenate to the same bytes (`"the stand does not answer: " + note` equals `LAYER1["stand_dead"] + note`, and the same for the other five). Unchanged.
6. **P27 / AR-29.** `blocked_by_of` reads only our output form and no person's words. No refusal and no judgment moved into code: retry, go on and another stand stay the person's answer. Census: no row added. The builder reports `test_judgment_census` 25/25; I accepted that and did not re-run it (slow list).
7. **Driver files.** Checked by AST. The changed lines sit only in `s0_rest` (driver_s0:2435), `s1_review_text` (driver_sources:736), `stand_probe` docstring (driver_machine:212), `resume_on_refusal` (:315), and `stand_question_text`/`stand_check`. In env_probe: the constants, `probe`, `_device_answer.answer` (required by item 1's device word), `main`, and the new functions.
8. **Skill road and old words.** `s1.md`, the `role-rules.json` anchor and `s1_review_text` changed in one commit. Case-insensitive Grep for `did not answer the check|did not answer when|stand does not answer|stand did not answer|probe that did not answer` over the package (positive control: it returned the new `driver_stage_build.py:50` hit and the test hits). For each hit:
   - Changed: the four sites.
   - Legitimate (a true dead stand or exception, or another object): `driver_machine.py:313` print line, `env_probe.py:20/101`, `gate_preflight.py:1423/5416`, `manual_capture.py:2249/4828`, `stand_health.py:646`, `source_inventory.py:1614` (the tracker), `role-commands.json:252`.
   - Missed, queued (F9): `s0.md:405`, `stand-answers.json:132`.
9. **Quarantine.**
   - `test_story_run_s0_stand_trace:93-94,113`: red for the intended reason (old warning words; the `probe_reason` part is unchanged code).
   - `test_story_run_stand_c:95`: red for the intended reason (old S1 words).
   - `test_env_selected_stand` (6 rows): red for the additive key only.
   - `test_story_run_stand:40,62`: NOT red (F2).
   - No protected behaviour is lost. The S5 dead-stand sentence now has a kept row (STAND_WHY_ROWS `stand_dead`). The rest are wording pins, and a missing pin is not a finding. All four files are in `quarantine` (test-layers.json :8085, :10161, :10197, :10215 > :7168). The owner is told of the reds via the quarantine-watch path. Lead: tell the owner the corrected list.
10. **The first-look finding's owner words** (`20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md:39-44`): «Роль находит как входить, код записывает для всех остальных»; «собственная догадка пробы никогда не перекрывает эту запись». Nothing in this diff contradicts them: no record of a role-found way exists yet, so nothing overrides one. The change also removes the probe's guess being stated as a FACT about the stand ("did not answer" becomes "the login recorded for this project did not get in", a true statement about the probe's own attempt). Two parts stay open against those words, outside FV1-5's owns, and are FV1-15's / first-look item 3's to carry: `stand_check` still stops S5/S6 on the probe's login failure and asks the person, and the retry text "or name the way the project signs in" (`driver_stage_build.py:66-67`) asks the person before any role has tried (F8).
11. **Tests.** One function, `the_stand_check_words`, built from parameterised tables (STAND_WHY_ROWS × 4 checks, the 17-row reader `shapes`, the 5-row probe table, plus 5 extras). Each id names the case. This is one table with a battery, not a test per line. The killing power is shown by the builder's negative control (385/392, hashes equal). Test lines (124) are close to product lines (~100). No new test file.
12. **Duplication and consistency:** found. F7 (second block parser beside `probe_reason`, card-sanctioned, queued) and F4 (two roads for the words). The closed mapping words-to-sentence is written once (`driver_stage_build.py:42-55`). Grep `ENVIRONMENT CANNOT BE USED` over the package: only `driver_s0.py:2505` and `env_probe.py:1208/1264` outside tests.
    **Code quality:** F6 (low). No new function is over 60 lines. `stand_question_text` stays one function, about 60 lines. Nesting is at most 3. `classes` is rebuilt per call, which is negligible.
    **One road (P31):** F4. A case (a config fault) does not reach the shared words on the driver's road. Residual: proposed node, owner Lead.
13. **FV1-15 extension.** A new word mapped to an existing class is one edit (`classes`). A new class is three entries in the same function (`classes`, the sentence dict, and possibly the retry branch). The text reader needs a `LAYER1` entry plus a `_word_of_item` branch, which is a second site (F6). Under F8(A) (one `login` word), FV1-15 adds no word, so nothing blocks FV1-15 today.

## Trail

Read:
- the diff (all 10 files);
- spec §1.1 C2-C22, §1.2 E1-E8, §1.3, §2.3, card FV1-5 (:298-376);
- the report;
- both findings;
- `human-questions.md:1-70`;
- `critic-diff-brief.md`;
- `SIBLING_MAP.md` headers and axis 5;
- `env_probe.py:935-1030`, `:1096-1167`, `:1166-1270`;
- `driver_stage_build.py:25-147`;
- `driver_s0.py:2496-2511`;
- `driver_runner.py:211-229` (py = stdout+stderr; timeout text);
- `story_run_common.py:471-562`;
- `test_story_run_stand.py:1-75`;
- `stand_access.py:300/404`;
- `test-layers.json` row lines.

Reruns:
- `( cd <wt>/ai-packages/qa-factory && python -B scripts/tests/test_human_questions.py )` gave `=== test_human_questions: 392/392 ok ===` (matches the witness).
- An in-process empirics script (heredoc, nothing written to the repo): `blocked_by_of` on 25 shapes and `stand_question_text` on 16 `why` values. Real `env_probe.py` subprocess runs: dead port Local/Staging (`stand_dead`, dead sentence True), `--json` (keys above, `blocked_by ['stand_dead']`), selection `Nowhere` (`['unknown']`), and no address (`['no_address']`, which gives the false "did not answer", F1).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Four driver sites C11-C14 changed together with the s1.md and role-rules anchor (axis 5). Missed carriers of the same class, queued: skills/qa-story/phases/s0.md:405 and references/stand-answers.json:132 (login_not_tried.skipped read by stand_health.py:733). The no_address mapping (F1) is a live instance of the class inside the diff. Selection/env_file/device are unreachable through the text reader (F4, proposed node).",
  "fixes": [
    "F1: driver_stage_build.py:42 maps no_address to dead, so a stand never asked (probe: 'nothing was asked') reads 'did not answer when I checked it just now'; map no_address to config and move the test row; consider a config retry text (:68-70); needs the Lead's amendment of card item 3 and the INVARIANT (meaning change).",
    "F2: report 20261114-fv1-5-report.md:110 lists test_story_run_stand.py:40,62 as red; a real probe on the discard port yields stand_dead and the dead sentence, so those rows stay green; correct the list given to the owner.",
    "F3: changelog.d/fv1-5-stand-check-words.md:9-10 says S0 says 'did not pass its check' (code: 'the check'), and line 7 implies the config sentence is shown although stand_check cannot reach it; reword.",
    "Queue (owner Lead, live-run-fvf): F4 one road for blocked_by (probe prints its words on a column-0 line), with F5 split device crash vs dead, F6 _word_of_item iterate LAYER1, F7 one Layer-1 block parser shared with probe_reason; F8 retry text vs the owner word (FV1-15 / first-look item 3); F9 s0.md:405 and stand-answers.json:132."
  ],
  "trail": {
    "read": [
      "git diff origin/main...a03ea51 (10 files)",
      "docs/tasks/specs/20261113-fv1-17-5-15-stand-login-spec.md sections 1, 2.3, card FV1-5",
      "docs/tasks/specs/reports/20261114-fv1-5-report.md",
      "plans/piles/live-run-fvf/findings/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md",
      "plans/piles/live-run-fvf/findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md",
      "ai-packages/qa-factory/references/human-questions.md:1-70",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis headers, axis 5",
      "scripts/env_probe.py:935-1270",
      "scripts/driver_stage_build.py:25-147",
      "scripts/driver_s0.py:2496-2511",
      "scripts/driver_runner.py:211-229",
      "scripts/tests/story_run_common.py:471-562",
      "scripts/tests/test_story_run_stand.py:1-75",
      "scripts/tests/test-layers.json row lines"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_human_questions.py (worktree package dir)", "result": "=== test_human_questions: 392/392 ok ==="},
      {"command": "in-process blocked_by_of on 25 text shapes + stand_question_text on 16 why values", "result": "no non-dead word gives 'did not answer'; unknown/None/[]/non-str give 'I could not check'; CRLF ok; traceback -> unknown"},
      {"command": "env_probe.py --env Local|Staging on discard port 127.0.0.1:9 (subprocess)", "result": "exit 1, words ['stand_dead'], dead sentence True for both"},
      {"command": "env_probe.py --env Local --json --no-login (subprocess)", "result": "keys ['liveness','login','keys','layer1','blocked_by'], blocked_by ['stand_dead']"},
      {"command": "env_probe.py --env Nowhere (subprocess)", "result": "exit 1, words ['unknown']"},
      {"command": "env_probe.py --env Local, entry with no address (subprocess)", "result": "exit 1, words ['no_address'], liveness 'nothing was asked', person reads 'did not answer when I checked it just now'"}
    ]
  }
}
```
