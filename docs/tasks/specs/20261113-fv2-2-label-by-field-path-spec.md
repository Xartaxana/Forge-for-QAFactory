# FV2-2 - the "code fills this" label keyed by the full field path (DRAFT, designer)

Pile `live-run-fvf`, batch 2 (`plans/piles/live-run-fvf/batch-2-live-run-fvf.md:29`; the brief's alternative name
`batch-2-ostatki-kritikov.md` does not exist in that folder - Glob `batch-2*` found only `batch-2-live-run-fvf.md`).
Finding: `plans/piles/live-run-fvf/findings/20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md`.
Base tree for every fact below: `C:\QAFactory\forge-repo\.claude\worktrees\fv2-1` (branch `wip/fv2-1` at `a60160e`). All
`file:line` are package-relative (`ai-packages/qa-factory/...`) unless they start with `plans/` or `docs/`. Status: draft for Lead
acceptance; forks in §7 are returned, not decided.

## 1. Architecture, owners, census, rules (designer rule 1 / CLAUDE.md rule 10)

AR-n touched and the change check each demands (copied into the DoD, §6):

| AR | how this node touches it | change check (in the DoD) |
|---|---|---|
| AR-22 (every field read has a producer; every field produced has a reader) | the label is a producer (`BY_PATH` + `_code_fills`) read by 9 sites (§2.5); the S3/S8 fields lose a false "code produces this" | producer and every reader change in ONE commit; `grep -rn BY_LEAF scripts/` empty after the change with the positive control `grep -rn BY_PATH scripts/` finding `handoff_check.py`; `test_field_producers.py` green |
| AR-13 (a fact with a reader function is read only through it) | the label has ONE answer, `_code_fills`, and the fill-time lookup and the test walk go through one helper `_by_path` instead of re-deriving the leaf | no site keeps `rsplit(".", 1)[-1] in BY_...`; the test walk calls `HC._by_path` |
| AR-10 (a check's requirement reaches the role before the work, in its fields) | the refusal skeleton, the row hints and the pre-tool guard now name `scope[0].requirements` / `inputs_read[0].requirements` (S3) and `filed[0].requirements` (S8) as the role's | the skeleton rows of §6 (test_handoff_values_refusal.py, K-A20 skeleton table) |
| AR-28 (an unknown never becomes a pass) | an empty, absent or unknown contract makes `_code_fills` answer False: the field stays the role's and its blank is refused, never forgiven | the K-A20 rows with contract `""` / `None` / a case-different id |
| AR-29 (code judges shape, joins, presence) | the only check that changes is PRESENCE (a blank field refused by the guard on three more paths); no code ever judges whether an R-id list is right | `test_judgment_census.py` green, census counts unchanged, no census row edited |
| AR-19 / axis 5 (stage twins change together) | the two S4 designer forms (`s4-designer-to-case-critic`, `s4-designer-to-runner`) get identical rows | the K-A20 rows cover both twins |
| AR-1 (closed variety is a data row) | not touched as a project-variety table: `BY_PATH` maps package contract fields to deriver FUNCTIONS, the same carrier and shape as `DERIVERS` (`scripts/handoff_check.py:576-606`); see fork F-2 | n/a, reason in F-2 |

Every check this node adds or alters, with the owner it serves and its census class (AR-29):

| check | where | owner served | census class | census row |
|---|---|---|---|---|
| blank refusal of the guard on S3 `scope[].requirements`, S3 `inputs_read[].requirements` (S8 `filed[].requirements` is optional: offered, never refused) | `handoff_check.values_report` (`:2909`) called by `guard_pre_tool.handoff_values_check` | data (presence of a field the role must write) | shape | `scripts/tests/fixtures/judgment-census.json:421` (`guard_pre_tool.py::handoff_values_check`, shape/data) - unchanged |
| the fill-time deriver lookup | `handoff_check.check` (`:1557`) | data | shape | `judgment-census.json:444` (`handoff_check.py::check`, shape/data) - unchanged |
| `_code_fills` (a label, not a refusal site) | `handoff_check.py:2732` | data | - (no refusal site; not a census unit) | none |
| the content of the three fields (which R-ids a plan row covers, which R-ids a bug violates, how many register rows) | the role; accepted on meaning by the S3 stage critic / the scribe | judgment | - | none: no code check is added on it |

Factory rules walk (sections touched): C - FR-11 (the role can produce the field: it writes R-ids or a count itself), FR-38
(the requirement reaches the role before the work: skeleton and guard), FR-17 (the S4 twins wired alike); D - FR-59 (unknown
contract -> the declared safe default "role's", never a pass); G - FR-30 (English; the ledger notes and the changelog fragment
carry no Cyrillic), FR-32 (root cause + test). A, B, E, F: not touched (no refusal text, no person text, no delivery, no money).
Principles: P27 (code owns data, the role owns the R-id list), P31 (one table read by one function for every contract; no
per-stage branch).

## 2. Facts (each read in the base tree)

### 2.1 Every place that keys the label by the LEAF name

| # | file:line | function | what it does today |
|---|---|---|---|
| L1 | `scripts/handoff_check.py:612-616` | module table `BY_LEAF` | `{"case_version": _case_version, "requirements": _requirements_of, "plan_row": _plan_row_of}` |
| L2 | `scripts/handoff_check.py:2741` | `_code_fills` | `if generic.rsplit(".", 1)[-1] in BY_LEAF: return True` - any path whose last dotted segment is one of the three leaves is "code's" |
| L3 | `scripts/handoff_check.py:1557` | `check` (the `--fix` fill) | `deriver = DERIVERS.get(generic) or BY_LEAF.get(generic.rsplit(".", 1)[-1])` - the fill tries the leaf deriver on every contract |
| L4 | `scripts/tests/test_field_producers.py:105-107` | `walk` | `leaf = path.rsplit(".", 1)[-1]` ... `if path in derived or leaf in HC.BY_LEAF:` |
| L5 | `scripts/tests/test_handoff.py:929-931` | `the_same_fact_derives_under_the_same_name` | asserts on `set(H.BY_LEAF)` and `"case_version" in H.BY_LEAF` |

The finding's line references are stale against this tree: it cites `:564-609` and `:2725-2734`; the table is at `:612-616`
and `_code_fills` at `:2732-2743`. `_requirements_of` is at `:414-426` (finding: `:414-427`).

### 2.2 Every field path carrying one of the three leaves, per stage (enumerated from `handoffs/*.yaml`)

Search: Grep `(requirements|plan_row|case_version)\b` case-insensitive over `handoffs/`, and the anchored form
`^\s*-?\s*(requirements|plan_row|case_version)\s*:`; both found the hits below (positive control: they found the known
`s4-designer-to-case-critic.yaml:50` `plan_row:`), no inline-flow `{requirements: ...}` occurrence exists.

| stage / contract | generic path | template line | row identity (what `_row_of` gives the deriver) | can the deriver answer? | label after FV2-2 |
|---|---|---|---|---|---|
| S3 `s3-strategist-to-designer` | `inputs_read[].requirements` | `handoffs/s3-strategist-to-designer.yaml:37` `<how many rows the register carries>` (a COUNT) | `{path, version, requirements}` - no `case`, no `id` | never: `_requirements_of` takes `row.case or row.id` (`handoff_check.py:416`) -> `""` -> not a case id -> None (`:420-426`); and the fact is a count, not R-ids | ROLE'S (must not be covered) |
| S3 `s3-strategist-to-designer` | `scope[].requirements` | `:55` `"<the R-ids this row covers>"` | `id` = a plan row `P-n` (`:52`) | never: `P-n` is no case id (`C.is_case_id`, `:421`) -> None; a plan row has no case file | ROLE'S (must not be covered) |
| S4 `s4-designer-to-case-critic` | `scope[].requirements` | `handoffs/s4-designer-to-case-critic.yaml:52` | `id` = case id (`:47`) | yes, from the case's `covers:` (`:422-426`); None when the case is absent or covers no `R-n` | CODE'S (must be covered) |
| S4 `s4-designer-to-runner` | `scope[].requirements` | `handoffs/s4-designer-to-runner.yaml:50` | `id` = case id (`:45`) | same | CODE'S |
| S4 `s4-designer-to-case-critic` | `scope[].plan_row` | `:50` `<P-n>` | case id | by design yes, through `contract.case_plan_row` (`handoff_check.py:429-447`); TODAY never on a `P-n` case (§2.4) | CODE'S (fork F-1) |
| S4 `s4-designer-to-runner` | `scope[].plan_row` | `:48` | case id | same | CODE'S (fork F-1) |
| S8 `s8-bug-reporter-to-scribe` | `filed[].requirements` | `handoffs/s8-bug-reporter-to-scribe.yaml:60` (optional: "or a dash", `scripts/handoff.py:35`, `:434`) | `{draft, bug, action, cases, ...}` - `cases` (plural), no `case`, no `id` (`:55-62`) | never | ROLE'S (must not be covered) |
| S4 `s4-case-critic-to-designer` | `scope[].case_version` | `handoffs/s4-case-critic-to-designer.yaml:60` | case id (`:57`) | yes (`_case_version`, `handoff_check.py:356-364`) | CODE'S - already by `DERIVERS["scope[].case_version"]` (`:603`) |
| S4 `s4-designer-to-case-critic` | `scope[].case_version` | `:53` | case id | yes | CODE'S via `DERIVERS` |
| S4 `s4-designer-to-runner` | `scope[].case_version` | `:51` | case id | yes | CODE'S via `DERIVERS` |
| S5 `s5-automator-to-critic` | `scope[].case_version` | `handoffs/s5-automator-to-critic.yaml:51` | `id` = "case or instance id" (`:44`), no `case` key | only when the row's id is a case id | CODE'S via `DERIVERS` (analog A-1, §9) |
| S5 `s5-automator-to-runner` | `scope[].case_version` | `handoffs/s5-automator-to-runner.yaml:52` | `case` key (`:51`) | yes | CODE'S via `DERIVERS` |

No other contract (S1, S2, S6, S7, S9, gates, `role-to-conductor`) carries any of the three leaves. Every `case_version` path is
`scope[].case_version`, already a `DERIVERS` key, so dropping `case_version` from the leaf table changes no answer for any path
of today's contracts.

### 2.3 The three FV2-2 ledger rows: the code path that reddens each today, and what greens it

Ledger: `scripts/tests/fixtures/form-rounds.json:72-74`. Judge: `test_field_producers.every_derived_field_meets_its_deriver`
(`scripts/tests/test_field_producers.py:1361-1405`) and `red_rows_equal_the_known_red_ledger` (`:1460-1489`, reader
`scripts/tests/known_red.py`).

Common path today (all three): `form_filler._Survey` (`scripts/tests/form_filler.py:326`) asks `handoff_check._code_fills(path)`
-> `True` through the leaf test (L2, `handoff_check.py:2741`) -> the field is `kind == "code"` and lands in `left_for_code`.
The deriver round then emits `derive: <contract>:<path>` for every `left_for_code` path (`test_field_producers.py:1394-1399`)
and runs `HC.check(..., fix=True)` (`:1388`); the fill lookup L3 (`handoff_check.py:1557`) finds no `DERIVERS` key and takes
`BY_LEAF["requirements"]` = `_requirements_of`, which returns None, so the field stays a placeholder and the row is red; the
ledger names it, so it prints `KNOWN RED` (`test_field_producers.py:63-66`).

| ledger row | why `_requirements_of` returns None |
|---|---|
| `derive: s3-strategist-to-designer:inputs_read[0].requirements` (`form-rounds.json:72`) | `_row_of(doc, "inputs_read[0].requirements")` (`handoff_check.py:995-1003`) gives `{path, version, requirements}`; `case = row.case or row.id or ""` -> `""` (`:416`); `C.is_case_id("")` false -> `front = {}` (`:421`) -> `covers = ""` -> None (`:426`) |
| `derive: s3-strategist-to-designer:scope[0].requirements` (`:73`) | the row's `id` is the filler's `P-1` (hint `<P-n, ...>`, `form-fill-rules.json:12` id-prefix rule); `C.is_case_id("P-1")` false -> None |
| `derive: s8-bug-reporter-to-scribe:filed[0].requirements` (`:74`) | the `filed` row has `cases`, no `case`/`id` (`s8-bug-reporter-to-scribe.yaml:55-62`) -> `case = ""` -> None |

What greens it (the change of §3): `_code_fills(path, contract)` answers False for these three `<contract>:<path>` (no `BY_PATH`
key, no `DERIVERS` key, not a claim). Then `form_filler._Survey` takes the generator branch (`form_filler.py:331`) and the
`free-text` rule (`scripts/tests/fixtures/form-fill-rules.json:19`, pattern `.+`, generator `_gen_free_text`,
`form_filler.py:170-171`) fills `filled requirements`; the field is no longer in `left_for_code`, and the `before` pass has no
blank on it, so `skipped` is empty for it (`test_field_producers.py:1393`). The deriver round therefore emits NO
`derive: ...requirements` row for these three paths, and `known_red.reconcile` reports each ledger row as
`unknown row: <id> is not a row of the walk; rename it to the walk's id or remove it` (message form:
`test_field_producers.py:200-201`). The ledger rows are removed in the same commit; that removal is forced by the reconcile,
which refuses the commit otherwise. The N1 rows of the two forms (`s3-strategist-to-designer[<verdict>/<variant>]`,
`s8-bug-reporter-to-scribe[...]`, `test_field_producers.py:526`, `:557-560`) stay green: `check(fix=False)` accepts any
non-placeholder text in a `text` field (`handoff.py:429-447`: these three fields have kind `text`, no options, no `max_len`).
In the walk's terms "green by the code itself" therefore means: the code no longer claims the field, the role-side filler fills
it, and the row id leaves the walk (small choice C-5).

### 2.4 The re-attribution item: the cause, verified

The three rows FV2-1 left red (`form-rounds.json:55`, `:75`, `:76`) are red because of the plan-row id form, not the reader:

- `_plan_row_of` now reads `contract.case_plan_row` (`scripts/handoff_check.py:429-447`); no front-matter key is read.
- `contract.case_plan_row` (`scripts/contract.py:3617-3619`) matches `CASE_PLAN_ROW_RE = r"^\s*Plan row:\s*(TS-\d+)"`
  (`scripts/contract.py:3052`): `TS-<n>` only.
- The round world mints the plan row id from the S3 form (`issued = scope[0].id`, filled `P-1`) and gives it to every later
  writer as `minted={"P": [issued], ...}` (`scripts/tests/test_field_producers.py:1065-1068`); with a `P` id minted, the case
  artifact's base variant writes `Plan row: P-1` (asserted at `test_field_producers.py:750-751`; with a TS id minted it writes
  `Plan row: TS-1`, `:745-747`).
- So the forward row (feed `_f_art_case`, `test_field_producers.py:1140-1142`: `_plan_row_of(Artifacts(w.task), None,
  {"case": "TC-001"})`) gets None for `P-1` - the FV2-1 report's "was given 'P-1' and answered None"
  (`docs/tasks/specs/reports/20261113-fv2-1-report.md:16`) - and the two `derive: ... scope[0].plan_row` rows meet the same
  reader on the same case (S4 `scope[0].id` is filled `TC-001` by the `case-id-of-the-world` rule, `form-fill-rules.json:13`).

Cause confirmed as stated by the Lead: the P-n / TS-n plan-row identity. Node FV1-14's row
(`plans/piles/live-run-fvf/batch-1-live-run-fvf.md:46`) names "one id of the plan row and one reader ... TS-only readers ...
`handoff_check` ... through the reader `contract`", so FV1-14 owns it. Observation for the Lead (fork F-4): the ledger
already attributes the SAME reader `contract.case_plan_row`, failing on the same `P-1`, to FV1-1
(`form-rounds.json:53`, `:54`, and the note of `:71`).

### 2.5 The existing carriers that tell the role which of its fields code fills (no new carrier)

All read `_code_fills`; after the change they name the three S3/S8 fields as the role's:

| carrier | file:line | what the role sees |
|---|---|---|
| refusal skeleton (one ready command) | `handoff_check.values_skeleton`, `:2802` | a section problem lists a line for every field of the row EXCEPT the code-filled ones |
| row-form hints | `_row_lists` `:2196`, `_nested_rows` `:2259`, `_ValuesHints.aim` `:2311`; `row_form` callers `:1503`, `:1513`, `:2299`, `scripts/handoff_init.py:105` | the sample row lines shown in a refusal and in the form's `# Fill:` line |
| pre-tool guard | `values_report` `:2909` (called by `scripts/guard_pre_tool.py:1160`) | a blank code-filled field is NOT refused; any other blank required field is |
| `--json` answer | `_answer_json` `:2955` | `code_fills: true/false` on each problem |

The three templates never claim the code fills these fields (`s3-strategist-to-designer.yaml:37`, `:55`;
`s8-bug-reporter-to-scribe.yaml:60`), nor do the role pages (`references/slices/qa-test-strategist/handoff-keys.md:23`, `:30`;
`references/slices/qa-bug-reporter/handoff-keys.md:31`): no template or page text changes.

### 2.6 Other facts the node depends on

- `test_handoff.py:925-926` asserts `_plan_row_of` reads the case's FRONT MATTER (fixture `TC-003.md` holds `plan_row: TS-3` in
  front matter and no body `Plan row:` line, `:899-902`). FV2-1 changed `_plan_row_of` to the body line only, so
  `H._plan_row_of(...)` returns None there and `None[0]` raises TypeError: `test_handoff.py` is red on the base tree (by reading;
  not run - the builder measures it first, §6 step 0). FV2-1's temporal scan covered `fixtures/stories` only
  (`20261113-fv2-1-report.md:10-11`), not this inline fixture. Fork F-3.
- FV2-1 put its new test in `scripts/tests/test_handoff_check_investigation.py`, which is in the `quarantine` section of
  `scripts/tests/test-layers.json` (`:8373`, the section starts at `:7104`) - analog A-5.
- `test_handoff.py`, `test_field_producers.py`, `test_handoff_values_refusal.py` are `keep` rows (`test-layers.json:2294`,
  `:1681`, `:2367`); `test_case_id_form_sites.py` is quarantined (`:7390`).
- The batch row names the ledger `references/form-rounds.json` (`batch-2-live-run-fvf.md:29`); the file is
  `scripts/tests/fixtures/form-rounds.json`. The batch row's `owns` column is wrong on that path.
- Known-red count today: 29 rows (`20261113-fv2-1-report.md:14`, `:42`); `known_red` has no count pin, `not_in_world` is pinned
  at 47 (`form-rounds.json:4`).
- `null_outcomes.tool_fields` (`scripts/null_outcomes.py:116-133`, regex `:48-50`) selects no field with one of the three leaves
  (their hints match none of `receipt|witness|sha256|...|revision`), so the L4 clause never decides a row today; it must still
  change (it reads `BY_LEAF`, which is removed).

## 3. Design

1. Replace the leaf table L1 by a table keyed by the FULL field path, `"<contract>:<generic path>"`, placed where `BY_LEAF` is
   (`handoff_check.py:609-616`), with exactly four rows:

   ```python
   # A fact code reads only where the contract's row IS a case (the designer's S4 rows): keyed by the FULL field path,
   # `<contract>:<generic path>`, never by the leaf name. The same leaf elsewhere - the S3 plan row's `requirements`, the S3
   # register count `inputs_read[].requirements`, the S8 filed bug's `requirements` - is the role's: no deriver can answer it
   # there (FV2-2). Judgement fields (`reason`, `state`, `what`, `origin`) are deliberately absent. `case_version` is no row
   # here: every contract holds it as `scope[].case_version`, a `DERIVERS` key.
   BY_PATH = {
       "s4-designer-to-case-critic:scope[].requirements": _requirements_of,
       "s4-designer-to-runner:scope[].requirements": _requirements_of,
       "s4-designer-to-case-critic:scope[].plan_row": _plan_row_of,
       "s4-designer-to-runner:scope[].plan_row": _plan_row_of,
   }


   def _by_path(contract, path):
       """The deriver `BY_PATH` names for this field of this contract, or None. Row indexes are generalised; an empty, absent
       or unknown contract names none, so the field stays the role's (AR-28: the label errs only toward the role)."""
       return BY_PATH.get(f"{contract or ''}:{INDEXED.sub('[]', str(path or ''))}")
   ```

   (`INDEXED` is defined at `:2119`, after this table; the helper reads it at call time, which is legal Python.)
2. `check` (L3, `:1557`): `deriver = DERIVERS.get(generic) or _by_path(contract, generic)`. Update the comment above it
   (`:1552-1556`) to say the same fact under the same name lives in `DERIVERS` by its generic path, and a fact that holds only
   in some contracts is keyed by contract and path in `BY_PATH`.
3. `_code_fills(path, contract)` (L2, `:2732-2743`): signature gains a REQUIRED positional `contract`; the leaf test becomes
   `if _by_path(contract, generic) is not None: return True`; the docstring names `BY_PATH` instead of `BY_LEAF`.
4. Readers of the label, each passes the contract it already holds:
   - `_row_lists(spec, nodes=None, contract="")`, `_nested_rows(spec, name, nodes=None, contract="")`,
     `row_form(spec, name="", nodes=None, contract="")`: the new keyword is passed down to `_code_fills(generic, contract)`
     (`:2196`, `:2259`; `row_form` passes it to `_row_lists`, `:2215`).
   - `_ValuesHints.hint`/`aim`: `_row_lists(..., contract=self.contract)` (`:2295`), `_nested_rows(..., contract=self.contract)`
     (`:2296`), `row_form(..., contract=self.contract)` (`:2299`), `_code_fills(dotted, self.contract)` (`:2311`).
   - `check`: `row_form(spec, section, _template_nodes(contract), contract=contract)` at `:1503` and `:1513`.
   - `values_skeleton`: `_code_fills(g, contract)` (`:2802`).
   - `values_report`: `_code_fills(p.path, contract)` (`:2909`).
   - `_answer_json`: `_code_fills(p.path, out.contract)` (`:2955`).
   - `scripts/handoff_init.py:105`: `handoff_check.row_form(handoff.spec_of(doc), "", doc.nodes, contract=str(doc.get("contract") or ""))`.
   - `scripts/tests/form_filler.py:316`, `:318`, `:326`: `handoff_check._code_fills(path, self.contract)`.
   - `scripts/tests/test_field_producers.py:107`: `if path in derived or HC._by_path(contract, path) is not None:` (drop the
     `leaf` variable if nothing else uses it - `:112` uses it, keep it); `:545` and `:1393`: `HC._code_fills(p.path, contract)`.
   - Docstrings naming `BY_LEAF` or the old one-argument form: `handoff_check.py:42`, `:2191`, `:2733-2737`, `:2888`, `:2954`
     (wording only).
5. The ledger (`scripts/tests/fixtures/form-rounds.json`): remove `:72`, `:73`, `:74`; rewrite `:55`, `:75`, `:76` exactly as in
   §6 DoD key K4. No row is added; no pin changes (`known_red` has none; `pins.not_in_world` stays 47).
6. A changelog fragment `changelog.d/fv2-2-code-fills-by-path.md` (one bullet, English).

No template, role page, charter or hook text changes. No new carrier: the role is told through the four carriers of §2.5.

## 4. Edges (each with the invariant it protects)

| edge | behaviour | invariant |
|---|---|---|
| E1 a path present in two forms with different fill status: `scope[].requirements` in S3 (role's) and in both S4 designer forms (code's) | the key carries the contract: `s3-strategist-to-designer:scope[].requirements` is no key -> role's; the two S4 keys -> code's | a field no deriver can ever answer is never labelled code's; a field a deriver answers by design keeps its label in both S4 twins |
| E2 a field code fills only SOMETIMES: S4 `scope[].requirements` when the case file is absent or `covers:` holds no `R-n` (`test_handoff.py:923-924` documents that None); S4 `scope[].plan_row` on a `P-n` case (today: always); `scope[].case_version` with no pin, or an S5 critic row whose id is an instance id | UNCHANGED: the label stays code's; the guard does not refuse the blank (`values_report`, `:2909`); at `finish` `check(fix=True)` leaves it blank and refuses it as `not filled. <hint>` (`:1576-1582`), and the refusal skeleton carries that field's own line (`values_skeleton` `:2798` adds a problem's own path whatever its label), so the role then writes it; the same edge for `case_version` is already proved by `test_guard_dispatch_budget_and_logs.py:626-650` (K-B8) | a blank is never a silent pass at `finish` (AR-28): the code fills it or the role is refused with the field named |
| E3 a form with no such leaf (S1, S2, S6, S7, S9, gates, `role-to-conductor`; and e.g. `scope[].plan_row` asked of the S3 form) | `_code_fills` False for every path of those forms that is not a `DERIVERS`/`LIST_DERIVERS`/claim path - identical to today, since none holds one of the leaves (§2.2) | a future contract that adds a `requirements` or `plan_row` field gets the role's label by default; it becomes code's only by a `BY_PATH` row, and a row naming a field its contract lacks is red (the BY_PATH rows of §6, test_handoff.py) |
| E4 S8 `filed[].requirements` is OPTIONAL ("or a dash", `handoff.py:35`, `:434`) | after the change the skeleton OFFERS `"filed[0].requirements": <...>`; the guard and `finish` never refuse its blank (`check` skips optional blanks, `:1577`) | a field the contract calls optional is never made required by this node |
| E5 TEMPORAL - a dispatch form written before the change and read after (a story resumed under the new release) | the label is computed at READ time from the form's `contract:` and the path; nothing persists it (the only persisted trace is the form's `derived:` section, which never holds these three paths because `_requirements_of` never answered them). Before the change: the S3/S8 role was not shown the lines and the guard let the blank through; `finish` refused the S3 blanks late. After: the same form, still blank, is refused by the guard / `finish` with the field named and the skeleton line offered - the role fills it. A REPAIR form of S3 carries `inputs_read[].requirements` from its parent only when the parent answered it (`handoffs/index.yaml:73-87`); a parent written blank before the change carries nothing, so the repair role is asked | no world in which a blank S3 field passes; no world in which the old and new code disagree on a field the S4 deriver answers |
| E6 TEMPORAL - the ledger rows | the commit that changes `_code_fills` removes `form-rounds.json:72-74` and rewrites `:55`, `:75`, `:76`; a tree with only one of the two is red (`reconcile`: `unknown row` if the code changed and the rows stay; `new red`... cannot occur: the rows only leave) | the ledger only shrinks (AR-20); no pin is raised |
| E7 POSITIONAL - `check` lookup order `DERIVERS.get(generic) or _by_path(contract, generic)` (`:1557`, same position as the old leaf lookup) | `DERIVERS` first, `BY_PATH` second | no `BY_PATH` key's generic part is a `DERIVERS` key, so the order never changes an answer (a BY_PATH row shadowed by DERIVERS is red: the shadow rows of §6) |
| E8 POSITIONAL - `_code_fills` branch order (DERIVERS/LIST_DERIVERS, then BY_PATH, then CLAIMS) | all branches are OR'ed: order is irrelevant to the boolean | none of the three role paths is reachable through any branch: no `DERIVERS` key ends in `.requirements` (`:576-606`, `:953`), `LIST_DERIVERS` holds `artifacts.tests`, `artifacts.probes`, `blast_radius` (`:571-574`, `:952`), CLAIMS only `claims.*` |
| E9 empty / absent inputs: `contract` `""` or None; `path` `""` | `_by_path` -> None; `_code_fills("", c)` -> False | unknown never becomes "code's" (AR-28) |
| E10 conflicting requirements: "label by full path" (this node) vs "a fact keeps its name wherever it sits" (TP1-13797, `handoff_check.py:1552-1556`, `test_handoff.py:885-892`) | a fact that IS the same everywhere keeps its generic `DERIVERS` key (`scope[].case_version`, `inputs_read[].version`); a leaf that names different facts in different contracts is keyed by contract | the TP1-13797 lesson stays (the designer never types a pin); the leaf-wide over-claim goes |

Limits / truncations: the node introduces none.

## 5. `_code_fills` in its consequential role: error direction and adversarial inputs

`_code_fills` is a label that decides whether the pre-tool guard FORGIVES a blank (`values_report`) and whether the refusal
HIDES a field from the role (`values_skeleton`, row hints). Allowed error: toward False ("the role's") only - the worst case is
that the role is asked for a value code could have filled (the role can write R-ids and plan rows itself; one redundant line).
Forbidden error: True for a field no deriver can answer (a blank forgiven by the guard, a line hidden from the role, a late
refusal at `finish` the role was never warned of).

Adversarial inputs that must stay on the safe side (each a row of the K-A20 table, §6):

| input | expected |
|---|---|
| `("scope[0].requirements", "s3-strategist-to-designer")` | False |
| `("inputs_read[0].requirements", "s3-strategist-to-designer")` | False |
| `("filed[0].requirements", "s8-bug-reporter-to-scribe")` | False |
| `("scope[0].requirements", "")` - unknown contract | False |
| `("scope[0].requirements", None)` - absent contract | False |
| `("scope[0].requirements", "S4-DESIGNER-TO-CASE-CRITIC")` - case-different id | False |
| `("requirements", "s4-designer-to-case-critic")` - a bare leaf with no section (old code: True) | False |
| `("scope[0][1].requirements", "s4-designer-to-case-critic")` - extra nesting | False |
| `("inputs_read[0].requirements", "s4-designer-to-case-critic")` - a path the form lacks | False |
| `("scope[0].plan_row", "s3-strategist-to-designer")` - a form with no such leaf | False |
| `("scope[0].requirements", "s4-designer-to-case-critic")`, `("scope[7].requirements", "s4-designer-to-runner")` | True (control: index generalised) |
| `("scope[0].plan_row", "s4-designer-to-case-critic")`, `("scope[0].plan_row", "s4-designer-to-runner")` | True |
| `("scope[0].case_version", "s5-automator-to-critic")` | True (DERIVERS, unchanged) |

## 6. Node FV2-2 (one builder node; the files do not force a split)

given: the finding `C:\QAFactory\forge-repo\.claude\worktrees\findings-lead\plans\piles\live-run-fvf\findings\20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md`; this spec `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-fv2-2-label-by-field-path-spec.md` (§2-§5 are the facts and the design); the FV2-1 report `C:\QAFactory\forge-repo\.claude\worktrees\fv2-1\docs\tasks\specs\reports\20261113-fv2-1-report.md`; `ai-packages/qa-factory/design/factory-rules.md` whole and `plans/builder-rules.md` (PROJECT.md, package change item 1); `ai-packages/qa-factory/design/architecture.md` AR-10, AR-13, AR-22, AR-28, AR-29; `docs/TESTING.md`; base branch `wip/fv2-1` at `a60160e`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\handoff_check.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\handoff_init.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\form_filler.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\test_field_producers.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\test_handoff.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\test_handoff_values_refusal.py
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\fixtures\form-rounds.json
C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\changelog.d\fv2-2-code-fills-by-path.md
non-goals: no change to `_requirements_of`, `_plan_row_of`, `_case_version` or any `DERIVERS` key; no change to the P-n / TS-n id (FV1-14) or to `contract.py`; no template, role page, charter or hook text; no new test file, no quarantined file run or edited (`test_handoff_check_investigation.py`, `test_case_id_form_sites.py`); no change to the `code_fills` JSON key's shape; no new `known_red` or `not_in_world` row, no pin raised; the analogs of §9 are reported, not fixed
handoff: the commit on branch `wip/fv2-2` (from `wip/fv2-1` `a60160e`) + a report `C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\docs\tasks\specs\reports\20261113-fv2-2-report.md` (builder.md rule 7 form, builder-rules item 11 content, the FR walk of §1, the witness tails verbatim, the class enumeration of §9 with a verdict per item)
edges: §4 E1-E10 and §5 of this spec, each implemented exactly as written; E2 and E4 are "unchanged / never refused" behaviours - do not add a refusal for them
DoD: K1-K8 below; verification run `python -B C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for scripts/handoff_check.py scripts/handoff_init.py scripts/tests/form_filler.py scripts/tests/test_field_producers.py scripts/tests/test_handoff.py scripts/tests/test_handoff_values_refusal.py scripts/tests/fixtures/form-rounds.json changelog.d/fv2-2-code-fills-by-path.md`, then every non-quarantined test file it prints, plus `python -B C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` and `python -B C:\QAFactory\forge-repo\.claude\worktrees\fv2-2\ai-packages\qa-factory\scripts\selftest.py --lang`
siblings: S4 designer twins (axis 5: both forms get identical rows); the five leaf-keyed sites L1-L5 (§2.1, all in owns); analogs A-1..A-5 of §9 reported with verdicts, not fixed
designer: this draft, once accepted by the Lead

Step 0 (measurement before any edit): run `python -B <WT>\ai-packages\qa-factory\scripts\tests\test_handoff.py` and
`python -B <WT>\ai-packages\qa-factory\scripts\tests\test_field_producers.py` on the untouched base and paste the tails in the
report: expected a TypeError (or a red check) at `test_handoff.py:925-926` (§2.6) and
`known red rows 29, not in world rows 47`. If `test_handoff.py` is GREEN at step 0, stop and report it as a question (§2.6
would be wrong).

What to change: exactly §3 items 1-6. Tests (rows in existing tables only, `docs/TESTING.md`):

- T1 `scripts/tests/test_handoff_values_refusal.py`, function `a_blank_field_code_fills_is_not_refused_by_values_report`
  (K-A20, `:203-232`): replace the two list checks at `:221-226` by ONE table of rows `(row_id, path, contract, expected)`,
  each checked as `check_eq(f"K-A20 _code_fills: {row_id}", H._code_fills(path, contract), expected)`. Rows: the existing seven
  "yes" paths and five "no" paths of `:221-223`, each with contract `S4` (`:17`), ids `yes <path>` / `no <path>`; plus every row
  of the §5 table, ids `s3 scope requirements`, `s3 inputs_read requirements`, `s8 filed requirements`, `unknown contract`,
  `absent contract`, `case-different contract`, `bare leaf`, `extra nesting`, `path the form lacks`, `form with no such leaf`,
  `s4c scope requirements`, `s4r scope requirements index 7`, `s4c plan_row`, `s4r plan_row`, `s5 critic case_version`.
- T2 same function, a second table `(row_id, contract, section, role, needle, present)` checked as
  `sketch = H.values_skeleton([H.Problem(section, "no rows", "fix")], contract, role)` then `check_in` / `check_not_in`
  `f"K-A20 skeleton: {row_id}"`. Rows:
  `s3 scope offers requirements` (`s3-strategist-to-designer`, `scope`, `qa-test-strategist`, `"scope[0].requirements": <`, present);
  `s3 inputs_read offers requirements` (`s3-strategist-to-designer`, `inputs_read`, `qa-test-strategist`, `"inputs_read[0].requirements": <`, present);
  `s8 filed offers requirements` (`s8-bug-reporter-to-scribe`, `filed`, `qa-bug-reporter`, `"filed[0].requirements": <`, present);
  `s4c hides requirements` / `s4c hides plan_row` (`s4-designer-to-case-critic`, `scope`, `qa-case-designer`, `scope[0].requirements` / `scope[0].plan_row`, absent);
  `s4r hides requirements` / `s4r hides plan_row` (`s4-designer-to-runner`, same, absent).
- T3 same function, a third table `(row_id, contract, path, refused)`: write `handoff.template(contract).text()` to
  `<story>/work/handoffs/<contract>-fv22.yaml` (story from `_story(root)`, already used by this function), call
  `H.values_report(form, "header.verdict: ok\n")`, and check `path in _paths(problems)` == `refused`,
  name `f"K-A20 guard: {row_id}"`. Rows: `s3 scope requirements refused` (`s3-strategist-to-designer`, `scope[0].requirements`, True);
  `s3 inputs_read requirements refused` (`s3-strategist-to-designer`, `inputs_read[0].requirements`, True);
  `s8 filed requirements optional, not refused` (`s8-bug-reporter-to-scribe`, `filed[0].requirements`, False);
  `s4c requirements forgiven (code's)` (`s4-designer-to-case-critic`, `scope[0].requirements`, False);
  `s4c plan_row forgiven (code's)` (`s4-designer-to-case-critic`, `scope[0].plan_row`, False).
  If a template does not load through `values_report` (an exception), the row is red with the exception text - never skipped.
- T4 `scripts/tests/test_handoff.py`, function `the_same_fact_derives_under_the_same_name`: replace `:929-931` by, for each
  `key` of `H.BY_PATH` (`contract, generic = key.split(":", 1)`): `check(f"BY_PATH names a field of its contract: {key}",
  generic in handoff.spec(contract))` and `check(f"BY_PATH is not shadowed by DERIVERS: {key}", generic not in H.DERIVERS)`;
  then `check("judgement fields have no deriver, on purpose", not ({"reason", "state", "what", "origin"} & {k.rsplit(".", 1)[-1] for k in H.BY_PATH}))`
  and `check_in("and the case pin is filled under its one name", "scope[].case_version", H.DERIVERS)`. Update the docstring
  (`:891-892`) to say `requirements` and `plan_row` are facts of a CASE row (S4), keyed by contract and path.
  `:925-926`: per fork F-3 (recommended in this node): move the fixture's `plan_row: TS-3` from the front matter (`:900`) to a
  body line `Plan row: TS-3` after `Given x`, and name the check "the plan row comes from the case's own `Plan row:` line".
- T5 `scripts/tests/test_field_producers.py`: no new row - the walk itself is the scenario. Only the three call sites of §3.4.

DoD keys (acceptance reads the report's verbatim tails):

- K1 `test_field_producers.py` ends `=== test_field_producers: <n>/<n> ok ===` and prints
  `known red rows 26, not in world rows 47`; its output holds no line containing
  `derive: s3-strategist-to-designer:inputs_read[0].requirements`, `derive: s3-strategist-to-designer:scope[0].requirements` or
  `derive: s8-bug-reporter-to-scribe:filed[0].requirements`; it holds the three lines
  `known red: plan-row: s4.scope[].plan_row -> handoff_check._plan_row_of -> FV1-14`,
  `known red: derive: s4-designer-to-case-critic:scope[0].plan_row -> FV1-14`,
  `known red: derive: s4-designer-to-runner:scope[0].plan_row -> FV1-14`; no line starts with `FAIL` for
  `derive: s4-designer-to-case-critic:scope[0].requirements` or `derive: s4-designer-to-runner:scope[0].requirements` (the
  code-filled control stays met).
- K2 `test_handoff_values_refusal.py` all ok, every T1/T2/T3 row id present in the output as passed.
- K3 `test_handoff.py` all ok (step 0 showed it red; the T4 rows present).
- K4 `form-rounds.json`: rows `:72-74` gone; rows `:55`, `:75`, `:76` read exactly
  `{"node": "FV1-14", "raised_by": "<the row's current raised_by, unchanged>; re-attributed to FV1-14 by the Lead 2026-11-13 (FV2-1 report)", "note": "<N>"}`
  with `<N>` = for `:55`: `the reader is fixed (FV2-1: _plan_row_of reads contract.case_plan_row); still red because the world's case says Plan row: P-1 (the S3 form mints P-n plan row ids) and contract.CASE_PLAN_ROW_RE accepts only TS-<n>: the P-n / TS-n plan-row identity of node FV1-14`;
  for `:75` and `:76`: `the deriver reads the case through contract.case_plan_row (FV2-1); still red because the world's case says Plan row: P-1 (the S3 form mints P-n plan row ids) and contract.CASE_PLAN_ROW_RE accepts only TS-<n>: the P-n / TS-n plan-row identity of node FV1-14`.
  ASCII only (no em-dash, no Cyrillic). No other row of the file changes; `pins` unchanged.
- K5 `grep -rn "BY_LEAF" <WT>/ai-packages/qa-factory/scripts` prints nothing, with the positive control
  `grep -rn "BY_PATH" <WT>/ai-packages/qa-factory/scripts` finding `handoff_check.py` (both outputs in the report); and
  `grep -rn 'rsplit(".", 1)\[-1\] in' <WT>/ai-packages/qa-factory/scripts/handoff_check.py` prints nothing.
- K6 `test_judgment_census.py` all ok, no census row edited (AR-29 change check: classes of §1 unchanged, no count raised).
- K7 `selftest.py --lang` ok (FR-30: ledger notes and changelog fragment English).
- K8 every other non-quarantined file `--witness-for` printed: all ok, tails in the report; a line
  `no scenario or keep row covers changelog.d/fv2-2-code-fills-by-path.md` is a report line, not a run (builder-rules 7b).

The commit message carries `architecture: AR-22 -- producer (BY_PATH, _code_fills) and its nine readers in one commit; AR-13
-- one helper _by_path; AR-10 -- the role is told by the existing skeleton and guard; AR-28 -- unknown contract errs toward the
role; AR-29 -- presence only, census unchanged` and a `judgment:` line naming that no judgment check is added.

## 7. Forks (returned, not decided)

- F-1 S4 `scope[].plan_row` label while the P-n / TS-n split stands. The deriver never answers on today's `P-n` cases (§2.4),
  so the S4 field is the same class as the S3/S8 ones until FV1-14 lands. Options: (a) keep both S4 `plan_row` rows in
  `BY_PATH` - the label is right by contract, the input is wrong; the blank is refused at `finish` with the field named (E2),
  never silent; the three re-attributed rows stay red under FV1-14 and turn green with it; (b) drop them until FV1-14 - the
  designer is asked for `plan_row` up front, the two `derive: ... plan_row` rows leave the walk (their ledger rows would be
  REMOVED, not re-attributed, which contradicts the Lead's decision), and FV1-14 must re-add the rows. Recommendation: (a).
- F-2 Where the path table lives. Options: (a) in `handoff_check.py` beside `DERIVERS` (same carrier, same shape: path ->
  function); (b) a data row in `references/field-producers.json` read by a new reader that maps a string to a deriver function.
  AR-1 targets project variety (tracker forms, markers); this table is package-internal contract fields bound to functions.
  Cost of (b): a second dispatch (string -> function) and a new reader for four rows. Recommendation: (a).
- F-3 The stale FV2-1 assertion `test_handoff.py:925-926` (§2.6). Options: (a) fix it in FV2-2 (same function as T4, already in
  owns; one fixture line moved; the Lead journals a `defect_found` against the FV2-1 node); (b) send it back to FV2-1 as a fix
  round, FV2-2 waits (its witness `test_handoff.py` is red until then). Recommendation: (a).
- F-4 Attribution consistency of the plan-row rows. The Lead re-attributes the three rows to FV1-14 (FV1-14's row names
  `handoff_check` and the `contract` reader); the ledger names FV1-1 for the same reader `contract.case_plan_row` failing on
  the same `P-1` (`form-rounds.json:53`, `:54`, `:71`). Options: (a) FV1-14 as decided, leave the FV1-1 rows untouched (this
  node writes only the three rows); (b) attribute all six to one node. Recommendation: (a) for this node; the Lead checks the
  FV1-1 / FV1-14 boundary when FV1-14 is specified.

## 8. Small choices closed by the designer

- C-1 `_code_fills(path, contract)` takes `contract` as a REQUIRED positional (every gate-side caller must pass it; no silent
  default), while `row_form` / `_row_lists` / `_nested_rows` take `contract=""` by keyword (their default errs toward "role's"
  and only changes which sample lines a hint shows). The contract id is read from the form or the caller's own argument, never
  parsed out of `spec["contract"].hint` (AR-13).
- C-2 One helper `_by_path` is the one lookup for `check`, `_code_fills` and the test walk (AR-13), instead of three f-strings.
- C-3 `case_version` gets no `BY_PATH` row: every occurrence is `scope[].case_version`, a `DERIVERS` key (`:603`); listing it
  twice would make the shadow rows of T4 red by construction.
- C-4 Test rows go into the existing K-A20 function (it already owns the `_code_fills` yes/no answer and the guard's
  forgiveness) and the existing `the_same_fact_derives_under_the_same_name` (it already owns the leaf-table assertions).
- C-5 "green by the code itself" for the three rows is realised as "the row id leaves the walk and the reconcile forces its
  removal" (§2.3); the N1 rows of S3/S8 and T1-T3 are the positive proof.
- C-6 The builder's worktree is named `C:\QAFactory\forge-repo\.claude\worktrees\fv2-2` (branch `wip/fv2-2` from `wip/fv2-1`
  `a60160e`); the Lead may rename it - then every `owns:` line and `<WT>` changes with it.
- C-7 The changelog fragment is one bullet: `- the handover check marks a field "code fills this" by its contract and full path,
  not by its leaf name: the S3 plan row's and register count's requirements and the S8 filed bug's requirements are the role's
  again, named in the refusal and asked by the guard (FV2-2)`.

## 9. Class sweep (finding item 2) and analogs noticed (reported, not fixed)

Enumeration of the leaf table, a verdict each:

- `requirements`: applied - 5 paths, 2 code's (`BY_PATH`), 3 role's (§2.2).
- `plan_row`: applied - 2 paths, both code's (`BY_PATH`); red rows re-attributed to FV1-14 (F-1, F-4).
- `case_version`: applied - removed from the leaf table, no answer changes (C-3); one row-level remainder, A-1.

Sweep of the same artifact (`handoff_check.py`, the label block and its readers): `_row_lists` applied; `_nested_rows`
applied; `aim` applied; `values_skeleton` applied; `values_report` applied; `_answer_json` applied; `check` fill lookup
applied; `LIST_DERIVERS` / `CLAIMS` branches not applicable (no leaf keying).

Analogs (queue to the Lead; none widened here):

- A-1 `s5-automator-to-critic:scope[].case_version` - a `DERIVERS` generic key whose deriver answers only when the row's id is a
  case id (`s5-automator-to-critic.yaml:44`, `handoff_check.py:356-364`); on an instance id the label claims a field code cannot
  fill (same class at row granularity; E2 keeps it non-silent).
- A-2 `inputs_read[].version` is a `DERIVERS` generic key (`:605`) filled by `_version_of` (a sha256 of the file), while
  `s8-bug-reporter-to-scribe.yaml:38` asks `<the gate B decision id>` and `s4-designer-to-case-critic.yaml:33` asks
  `<plan_revision>`: same name, possibly different facts (`handoff_init.py:224` already distinguishes "the measured kind").
- A-3 `test_field_producers.row_for` (`scripts/tests/test_field_producers.py:88-96`) matches a `field-producers.json` row by the
  LEAF (`rsplit(".", 1)[-1] == leaf`): the same keying class in the producers walk.
- A-4 The `--json` problem key `code_fills` (`handoff_check.py:2955`) has no reader in the package: Grep `code_fills` over
  `ai-packages/qa-factory/` found only `handoff_check.py` and test files (positive control: the same Grep found
  `handoff_check.py:2955`); its comment names "the stop-time reader" (SC2-38 F-2), which no longer reads it (AR-22, produced
  with no reader).
- A-5 FV2-1 placed its new test in the quarantined `test_handoff_check_investigation.py` (`test-layers.json:8373`), against
  builder-rules 7b and designer rule 1 ("a DoD never asks for a new test file outside the keep rows"), and its temporal scan
  missed the inline fixture of `test_handoff.py:899-902` (F-3).
- Axis note: the finding names SIBLING_MAP axis 23; axis 23 is "fields of a `tests[]` row" (`docs/SIBLING_MAP.md:432`) and does
  not fit; the relevant axes are 5 (stage twins), 18 (shrink-only ratchets), 32 (judgment census), 34 (one road).

## 10. Reading trail

Read whole or in the cited ranges (all in `C:\QAFactory\forge-repo\.claude\worktrees\fv2-1` unless noted):
`findings-lead/plans/piles/live-run-fvf/findings/20261113-by-leaf-...md` (whole); `findings-lead/.../batch-2-live-run-fvf.md`
(Grep FV2-1/FV2-2: `:18-19`, `:28-31`); `findings-lead/.../batch-1-live-run-fvf.md:34-46`; `scripts/tests/fixtures/form-rounds.json`
(whole); `docs/tasks/specs/reports/20261113-fv2-1-report.md` (whole); `scripts/handoff_check.py:350-640`, `:990-1009`,
`:1520-1610`, `:2180-2325`, `:2720-2820`, `:2880-2970`, Grep for `BY_LEAF|_code_fills|DERIVERS|requirements|INDEXED`;
`handoffs/s3-strategist-to-designer.yaml` (whole), `s8-bug-reporter-to-scribe.yaml` (whole),
`s4-designer-to-case-critic.yaml:1-70`, `s4-designer-to-runner.yaml:30-59`, `s5-automator-to-critic.yaml:40-55`,
`s5-automator-to-runner.yaml:44-55`, `index.yaml:60-109`, Grep over `handoffs/` (two forms, §2.2);
`scripts/handoff.py:399-470`, `:577-658`, Grep OPTIONAL_WORDS; `scripts/contract.py:2765`, `:3052`, `:3617-3619`;
`scripts/handoff_init.py:90-113`; `scripts/null_outcomes.py:48-51`, `:116-133`; `scripts/tests/form_filler.py:1-60`, `:260-340`,
Grep `free_text`; `scripts/tests/fixtures/form-fill-rules.json` (Grep rules `:4-19`); `scripts/tests/test_field_producers.py:1-330`,
`:344-458`, `:484-563`, `:604-615`, `:730-769`, `:1022-1151`, `:1355-1505`; `scripts/tests/known_red.py` (Grep keys);
`scripts/tests/test_handoff.py:1-30`, `:882-934`; `scripts/tests/test_handoff_values_refusal.py:14-27`, `:195-234`,
`:328-350`, `:455-485`, `:805-834`; `scripts/tests/handoff_values_common.py` (Grep defs); `scripts/tests/test_case_id_form_sites.py:515-549`;
`scripts/tests/test_guard_dispatch_budget_and_logs.py:601-656`; `scripts/tests/test-layers.json:1-40`, `:1675-1694`, `:2290-2380`,
`:8370-8381`, Grep section heads; `scripts/tests/fixtures/judgment-census.json:421`, `:439-448`; `scripts/tests/scenario_walk.py:887-931`;
`design/architecture.md:35-46`, `:134-169`, `:233-244`; `changelog.d/fv2-1-plan-row-reader.md`; `plans/builder-rules.md:15-27`;
`docs/SIBLING_MAP.md` (axis heads, `:432-455`).
Negative claims with their positive controls: "no other contract carries the three leaves" (two Greps over `handoffs/`, both
finding `s4-designer-to-case-critic.yaml:50`); "no reader of the JSON key `code_fills`" (Grep found `handoff_check.py:2955`);
"no census row for `_code_fills`/`values_report`" (the same Grep form found `handoff_check.py` rows at `:439-448`).
Not run: no test was executed by the designer; the red state of `test_handoff.py` is by reading (§6 step 0 measures it).
