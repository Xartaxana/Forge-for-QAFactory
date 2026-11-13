# FV1-19 — one road for `obligation_refs`, one reader of a valid reference, a factory repair never put to the person — DESIGNER DRAFT

designer (opus), 13.11.2026. Pile `live-run-fvf`, batch 1, row FV1-19 (`batch-1-live-run-fvf.md:58`). Status: DRAFT for Lead acceptance,
FIX ROUND t-496 applied after the critic on the plan (t-490, `docs\tasks\specs\reviews\20261113-fv1-19-plan-critic.md`, ACCEPT WITH FIXES);
what changed and where: §8b. Forks in §8 are RETURNED, never decided (F1-F6 decided by the Lead in §8a; F7-F9 new, open); node texts in §6
are written per the recommendation of each open fork so that they are executable the moment the Lead accepts (or edits) the fork. Package
code read ONLY from `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (origin/main) — every `file:line` below is
that tree, `PKG\scripts\` abbreviated `S\`. Node owns in §6 are written as absolute paths of the working tree; `P\` in prose =
`C:\QAFactory\forge-repo\ai-packages\qa-factory\`.

## §0. Brief, restated, and what changed against the finding

Finding: `findings-1413c\plans\piles\live-run-fvf\findings\20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md` (read whole: three
defects, critic analysis t-185, "Дверь t-186 неполна"). Review: `docs\tasks\specs\reviews\t-181-exit-go-on-diagnosis.md` (read whole; same
text in read-main and the root checkout — the findings worktree has no copy).

Two corrections to the brief/finding, from reading main (report, not scope widening):
1. **"`manifest_from_tests.py` reads the marker only from Python" is stale in form, true in substance.** Main has a non-Python road since
   EP1-37: `_files` sends every non-`.py` file to `LanguageFile` (`S\manifest_from_tests.py:1627-1628`), read by `test_source.read_file`
   (`:369`), rows written by `build.language_rows` (`:1338-1389`). That road writes rows from titles that carry a case id, but NO
   `obligation_refs`/`obligation_ids` and no Then bindings — it says so: "Then bindings are the author's: this language has no marker"
   (`:1385`). So for TS/Java/C# the field is still never produced by code; the defect stands.
2. **Defect 3 does not live in `story_run.py`.** The exit-limit seam is `driver_dispatch.py` (`exit_limit` `:3584`, `exit_limit_facts`
   `:3687`, `_exit_go_on` `:3816`; Grep `def exit_limit` over `S\` finds only these — positive control: same Grep, same call, finds the
   three defs). The batch row's `scripts/story_run.py` is therefore NOT written by any node here (the brief's preference holds by fact).

Analogs noticed, not widened (rule 9 report): (a) `obligation_bindings[].obligation_hash` is the same class (a plan hash typed by a role:
read by `S\coverage_contract.py:580` and `:280-282`, written by hand through `manifest_put` with no check) — taken in as fork F5;
(b) `manifest_from_tests._files` picks the Python reader by the literal suffix `.py` (`:1627`), a language name in code (AR-1) — pre-existing,
queued as a census line (§9 axis 34), not fixed here; (c) the finish demands refs of EVERY v2 instance (`S\controller.py:7298`) while the
precheck demands them only of rows whose case owes an automated obligation (`S\window_record.py:233-236`) — fork F3 (decided (c));
(d) critic t-490 K7, queue candidates of the same class, not taken: `assertion_id` (computed for Python, `trace_binding.assertion_refs` is
`[]` for TS, `S\manifest_from_tests.py:1377`), `obligation_bindings[].instance_ids` (that is F1 (c)), `novelty` never measured for non-Python
rows (`:1386`) and refused from a role (`S\manifest_put.py:2386-2394`); (e) `brief_pack.py:225-230` (the automator's tool line for
`manifest_from_tests.py`) describes the Python marker: it is the description of the Python reader itself, true for Python; T3b owns
`brief_pack`; reported, not widened.

## §1. Facts read first (file:line, read-main)

### 1.1 Who writes `obligation_refs` today, per language
| Road | Where | What it writes |
|---|---|---|
| Python marker `qa(obligations=[...])` | `S\manifest_from_tests.py:1323-1324` (`read_mark` → `Story.obligation` `:745-759`, refuses an id the case's plan row does not name, `:755-758`, and a case with no plan row, `:749-752`), `:1462-1465` | `obligation_ids` + `obligation_refs: [{obligation_id, obligation_hash: content_hash(<plan obligation>)}]` — the ONLY code that builds a per-ref hash |
| TS / Java / C# (`LanguageFile`) | `S\manifest_from_tests.py:1338-1389` | no obligation field at all; note `:1385` |
| Hand fragment, any language | `S\manifest_put.py` `run` `:2353-`; `merge`/`_merge_entry` `:1383-1386` takes any key (`result.update(patch)`: a key sent as `null` overwrites the stored value, documented at `S\manifest_from_tests.py:1698-1700`) | whatever the role sends; no per-ref check. `obligation_hash_problems` (`:592-622`) checks only the ROW-level `obligation_hash` (= `content_hash(refs)`), never `refs[].obligation_hash` |
| Code writer `migrate_artifacts.py` | through `manifest_put` (`_run_manifest_put` `:91-112`): `_retract_case_ghosts` resends whole stored rows (`:211-226`), its twin `_retract_legacy_selector_rows` (`:295-310`), `_legacy_obligation_patches` (`:346-350`, `dict(r, obligation_id=new)` keeps the old per-ref hash), `_rename_legacy_obligations` (`:395`, `dict(binding, obligation_id=new)` keeps the old binding hash) | stored refs, bindings and hashes forwarded as they are |
| Brief text | `cart-1\work\briefs\S5-qa-automator-*-code.md:11` (fixture of a real TS story) | "written by the marker, not by hand: the marker `qa(obligations=[...])` on the test, then `manifest_from_tests.py`" — i.e. the factory TELLS a TS role to use a road that does not exist for it |
| Role charter | `P\agents\qa-automator.md:69` (section `## Tools`, under `<!-- kind: process -->` `:64`) | "`obligation_refs`: `qa(obligations=)`" — the same wrong door, for every language |
| Stage text | `P\skills\qa-story\phases\s5.md:292-299` | "The automator's manifest comes from its markers" (Python markers, `obligation_refs` among the derived fields) |

Where the hash comes from: `event_store.content_hash` = sha256 of `json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False)`
(`S\event_store.py:106-108`), applied to the plan's obligation object (`coverage_obligations[]` item of `work/test-plan.json`).

### 1.2 Who reads it
| Reader | Where | What it demands |
|---|---|---|
| S5 precheck (gate, family `manifest`, tag `row-fields-missing`) | `S\s5_precheck.py:3798-3840` → `window_record.row_field_gaps` `S\window_record.py:270-292` → `_obligation_refs_problem` `:226-244` | only when the row's case owes an automated (non-`manual-*`) obligation (`:233-236` returns `''` before reading refs otherwise); then: a list with ≥1 dict carrying a non-empty `obligation_id`, ids unique; non-dict items skipped "as `build` skips them". **No hash read** (`:237-244`) |
| Carrier of the row fields | `S\window_record.py:161-189`: `obligation_refs` = `RowField(..., "plan_obligation", (), "marker", MARKER_DOOR, True)`; `MARKER_DOOR` `:175`; the `filled_by` comment `:169-170` | `filled_by="marker"` drives the render sites |
| Origin notes | `S\window_record.py:127-143`: `ORIGIN["obligation_refs"]`, `["obligation_ids"]`, `["obligation_hash"]` all say "the automator writes the plan's obligation ids and hashes there" | contradicts F2 (a typed hash is refused) |
| Render site 1 (refusal text) | `S\s5_precheck._row_fields_text` `:3768-3795` (`by_marker` branch `:3788-3791`) | names a door that does not exist for TS |
| Render site 2 (row form, axis 28) | `S\manifest_from_tests._legend_line` `:1674-1685` (`:1678-1679`), `_row_form` `:1690-1723` (calls `WR.row_field_gaps(entry, cfg, owed)` `:1717`; null slots only for `filled_by=="automator"` `:1720`), `_blank_row_form` `:1779` | same |
| Render site 3 (brief line) | `S\brief_pack._row_field_lines` `:2000-2013` (marker `else` branch `:2009-2010`, "written by the marker, not by hand") | owned by T3b (ported into `window_record.row_field_lines`) |
| Window record build | `S\window_record.py:1299-1312` | drops non-dict refs (`:1299`), copies the rest as a list; derives `obligation_ids`, `obligation_hash = content_hash(refs)`; `:1346-1350` drops empty fields with an ORIGIN note |
| Window finish (controller, tier 3) | `S\controller.py:7289-7323` (`_s5_v2_collect`) | map `{str(id): content_hash(ob)}` by a dict comprehension over ALL plan rows (`:7291-7293`, last occurrence wins); per instance: refs a non-empty list, every ref a dict with truthy `obligation_id` AND `obligation_hash`, ids unique (`:7298-7302`, ValueError); then execution fingerprint (`:7311-7314`); then every ref hash == the map's value for `str(id)` (`:7315-7317`, StateConflict — with an EMPTY map every ref fails here); then `obligation_ids` == ref ids as sets (`:7319`); then row hash (`:7322`). First failure per instance stops. `controller.py` imports `contract` only inside functions (no top-level import) |
| Acceptance | `S\acceptance.py:1189-1190`, `:1227` | item-level hash |
| Coverage / traceability | `S\coverage_contract.py:280-282`, `:580` | the plan hash on refs and on bindings |
| Probe | `S\probe_by_code.py:2845-2859` (`obligation_fields`: `entry.get("obligation_hash") or content_hash(refs)` — the STORED row hash wins, `:2854`) | row-level hash as stored |
| Other readers (unchanged) | `S\manifest_view.py:65`, `S\contract.py:5254` | ids / refs as stored |
| Plan reader | `S\contract.py:5178-5189` (`_plan_rows_of`: absent or unreadable file → `[]`, silently), `:5192-5203` (`plan_obligations`, schema-2 only) vs `S\controller.py:2251-2259` (`_plan_document`, all rows; unreadable → StateConflict) | two readers of the same plan, different schema filter |

### 1.3 Where the hand-written value passed, and where it then failed
- Precheck accepts `[{"obligation_id": "OB-6"}]` (no hash): `_obligation_refs_problem` returns `''` (`S\window_record.py:237-244`; t-181 probe).
- `manifest_put` accepts a WRONG per-ref hash: only the row hash is checked (`S\manifest_put.py:592-622`, call `:2427-2431`).
- Finish refuses both: no hash → `:7298-7302`; a hand hash ≠ plan → `:7315-7317` (×7 in the live run, finding `:63-71`).

### 1.4 The road by which the repair reached the person
`s5_precheck` emits the finding in family `manifest`, outside `PASSABLE` (`S\s5_precheck.py:82`, `:3812-3813`, `:3840`); the exit gate
classes the record `refused` (t-181 R1); after the free resume the driver reaches `exit_limit` (`S\driver_dispatch.py:3584-3609`), which calls
`no_move` with `call: False` (`:3607`) → `_no_move` raises the person's question at once, before any conductor call
(`S\driver_conductor.py:631-632`). `exit_limit_facts` withholds `go on` only for an incomplete handover form (`:3707-3710`) — never for a
record the gate refuses to every word (t-181 R2); `_exit_go_on` writes waiver rows and the caller prints "recorded" with no read-back
(`:3833-3838`, `:3795`). The class comment says it asks the person directly by design (`:3532-3535`, D-0041/t-217).

### 1.5 Neighbouring work that changes this ground
- **FV1-30a (running)** makes the `manifest` family word-passable (`20261113-p1-specs-amendment-owner-words.md:302`, A3 requirement 1
  `:330-332`): after it, `go on` DOES pass `row-fields-missing` at the precheck — while the finish (`controller.py:7298-7317`) reads no word
  and refuses the same refs; FV1-30a's lower-readers table (`:398-404`) has no row for it — fork F8. FV1-30b rewrites the tail of
  `s5_precheck.report` and `refusal_cause` (`:383-390`).
- **П1-а** row C3 `row-fields: obligation_refs <- manifest_from_tests@{typescript,java,csharp}` carries `known_red: FV1-19`
  (`20261113-p1a-writer-reader-round-spec.md:427`; ledger `P\scripts\tests\fixtures\form-rounds.json`, section `known_red`, `:226`;
  reconciled by П1-а N3 item 7 through `known_red.reconcile`, `:542`; rule `:640`). Per the Lead (t-496, D6) the removal of that mark is
  П1-а's work, not a node of this spec (§6 Crossings).
- **П1-б** C10 (`20261113-p1b-dry-story-spec.md:87`): the standing end-to-end detector of precheck/finish agreement (row
  `s5.window_finish/ref_without_hash`, `:939`).
- **П1-в** N0 and N2 own `driver_dispatch.handoff_ladder` (both) and `exit_limit` (N0) (`20261113-p1v-run-scoreboard-spec.md:444,446`).
- **T5** (`20261113-told-before-work-mechanism-spec.md:396`) owns `s5_precheck.report` + family producers, `manifest_put` functions of §5.4
  (incl. `obligation_hash_problems` `:553`); wave table `:374`: T5 enters after FV1-18/19 merge. Queue: **FV1-19 → T5**.
- **T3b** owns `brief_pack` and the new `window_record.row_field_lines` (port of `brief_pack._row_field_lines`).

## §2. Premise about DATA, measured (PROJECT.md package change item 6a)

Command (one, on real data: the TS test files that came from live runs, stored as package fixtures):
`Grep -i "obligation|annotation|@OB|OB-" --glob "*.{ts,java,cs}" S\tests\fixtures` (the Grep tool; this designer has no shell).
Result: 6 hits, all `test.info().annotations.push({type: 'sessions' | 'g3-change-status', ...})` in
`fixtures\local1-playwright\add-to-cart.spec.ts:151,170,198` and its twin in `local1-manifest\` — **no obligation id in any TS/Java/C# test
text**. Positive control of the same call: it finds `annotation` (the hits above). Critic t-490 reproduced it and added: 12 TS/Java/C# files
in the package; the Java/C# ones are synthetic `probe-languages` fixtures, so the "real data" premise rests on the two TS files.
Companion facts, same fixtures: the case id and partition live in the TITLE (`add-to-cart.spec.ts:27`); every TS manifest row nevertheless
carries `obligation_refs` WITH hashes, typed by the role (`fixtures\local1-playwright\manifest-run3.json:18-46` ff.,
`fixtures\stories\cart-1\work\automation-manifest.json:20-46` ff., fragment `cart-1\work\frag-s5-7.json:18-26` and a binding hash `:76-79`).
Many tests → one obligation is the common shape (`manifest-run3.json:46,99,152`; `cart-1 automation-manifest.json:189-497`).
Conclusion: (1) a TS marker would be NEW authoring practice; (2) the roles already type the ids AND the hashes by hand for TS — the hashes
are the error-prone half (live run: `c7ca9a5f…` vs the plan's `91f02946…`). The design takes ids from the role on ONE door for every
language and makes the hash the code's alone.

## §3. Requirements (numbered; N = 6)

1. **One road for the hash.** Every `obligation_refs[].obligation_hash`, every `obligation_bindings[].obligation_hash` (F5) and the row-level
   `obligation_hash` / `obligation_ids` derived from the refs are written by ONE code function from the plan, at write time, whatever road
   brought the ids (Python marker, row form, hand fragment, a code writer). A role never has to compute a hash; a code writer never forwards
   one.
2. **One door for the ids, named the same for every language.** Every text that tells a role how to fill `obligation_refs` — the precheck
   refusal, the row form legend, the origin notes, the role charter — names the fragment door
   `{"tests": [{"instance_id": "<id>", "obligation_refs": [{"obligation_id": "<plan obligation id>"}]}]}` through
   `manifest_put.py --task <T> --fragment <file>`; no text tells a role to use a road its language lacks (FR-2, FR-5, FR-11). Residual render
   sites owned elsewhere are queued by name (§6 Crossings: `brief_pack._row_field_lines` → T3b; `s5.md:292-299` → queue).
3. **One reader of a valid reference.** Precheck, window finish and the writer judge a PRESENT reference by ONE predicate (shape; id known to
   the plan; hash == `content_hash` of that plan obligation) over ONE map of plan obligations (AR-13, AR-15). Whether refs are DEMANDED is a
   separate rule of each caller (precheck: owed automated obligation; finish: every v2 instance — F3 (c)); the demand rule governs only the
   `missing` verdict, never whether present refs are judged.
4. **Nothing unproducible is demanded, and an unknown never passes the finish.** Demand (precheck) reads the schema-2 obligations of the row's
   case (`contract.plan_obligations`, `S\contract.py:5192-5203`; existing direction `S\window_record.py:229-232`). Validity reads the map of
   ALL plan rows (M1, the finish's present reading). Where that map is empty (no plan, a plan naming no obligation, an unreadable plan), the
   writer and the precheck refuse nothing about hashes and ids (the writer prints one note when the plan file exists but cannot be read); the
   finish, which judges with `strict=True`, refuses every ref as it does today (AR-28).
5. **A factory repair does not become the person's question** while the role can still be sent back or restarted (FR-3, P22) — fork F4 (held).
6. **TEMPORAL.** Manifests written before the change keep folding; rows whose refs lack a hash or carry a stale one get ONE repair command
   named (send the refs again, ids only), never a silent pass, never a trap — for a role and for a code writer alike.

## §4. Mechanism

M1 — **reader + stamp in `contract.py`** (new public functions, pure, lazy `from event_store import content_hash`):
- `obligation_map(rows) -> dict` — `{str(obligation_id): obligation}` over ALL plan rows given (no schema filter); a LATER occurrence of the
  same id replaces an earlier one (last wins — the finish's dict comprehension, `S\controller.py:7291-7293`); non-dict rows, a
  non-list `coverage_obligations`, non-dict items and id-less items are skipped.
- `plan_obligation_map(task_root, notes=None) -> dict` — `obligation_map(_plan_rows_of(task_root))`. When the plan file exists (the paths
  `_plan_rows_of` tries, `work/test-plan.json` then `test-plan.json`) but cannot be read or parsed, it appends ONE sentence to `notes` (when a
  list is given) — "the plan <path> could not be read (<cause>): obligation_refs are stored as sent, without hashes, and the window finish
  refuses them until the plan reads" — and returns `{}`. An absent plan adds no note.
- `obligation_ref_problems(refs, plan_map=None, strict=False) -> list[(kind, text)]` — kinds:
  `shape` (refs not a list; an item not a dict; `obligation_id` not a non-empty `str`; an id twice; `obligation_hash` absent, `None`, `""` or
  not a `str`); when any `shape` problem exists ONLY the shape problems are returned (a broken list never reaches the hash comparison, E18);
  `unknown` (id not in `plan_map` when `plan_map` is non-empty; with `strict=True` and `plan_map` `None` or empty, EVERY ref is `unknown`);
  `stale` (hash ≠ `content_hash(plan_map[id])`). With `strict=False` and `plan_map` `None` or empty → only `shape`. An empty list → `[]`
  (whether refs are DEMANDED is the caller's question, E11). Callers: the precheck `strict=False`, the finish `strict=True`.
- `stamp_obligation_refs(fragment, plan_map) -> (fragment', problems)` — pure, never edits its input. Per `tests[]` row, in this order:
  1. **null = not sent (D7).** A key `obligation_refs`, `obligation_ids` or `obligation_hash` whose value is `None` is DROPPED from the row
     before anything else, so `_merge_entry` keeps the stored value (the row form's null slot sent back unfilled never wipes stored refs).
     To clear refs a role sends `[]`.
  2. A row that does not send `obligation_refs` (after step 1) is not touched by steps 3-5 (a row sending only `obligation_ids` keeps
     today's behaviour, E24).
  3. **Shape** of the sent value: not a list, a non-dict item, an `obligation_id` that is not a non-empty `str`, an id twice → a problem
     naming `tests[i].obligation_refs[j]` and the expected shape `[{"obligation_id": "<plan obligation id>"}]`.
  4. **Per-ref hash** (only with a NON-empty `plan_map`): an id not in the map → a problem naming the plan's ids; a ref with no hash
     (absent / `""`) gets `obligation_hash = content_hash(plan_map[id])`; a ref that carried a DIFFERENT hash (a non-`str` included) is a
     problem ("tests[i].obligation_refs[j]: <id> carries hash <sent>, the plan's obligation hashes to <h>; leave `obligation_hash` out, the
     code writes it"). With an empty map refs keep what they carry (no stamp, no refusal; the finish judges, E3).
  5. **Derived row fields** (plan-independent): a sent `obligation_ids` whose SET differs from the refs' ids is a problem
     ("tests[i].obligation_ids <sent> are not the ids of its obligation_refs (<ids>); leave it out, the code writes it" — the same one
     direction as a differing hash, m3 (b)); the row then gets `obligation_ids` = the refs' ids in refs order. A row that sent no
     `obligation_hash` gets `obligation_hash = content_hash(<stamped refs>)` (`""` for `[]`), so the stored row hash never outlives the refs
     it bound (m3 (c), E25); a row that sent one keeps it for the existing `obligation_hash_problems` check, which runs after the stamp
     against the stamped refs.
  Per F5, every `obligation_bindings[]` row: an `obligation_hash: null` key is dropped (step 1); a binding whose `obligation_id` is in a
  non-empty map gets its hash stamped when it carried none and is a problem when it carried a different one; a binding whose id is NOT in
  the map is left untouched (no refusal: `unknown_obligation_refusal` owns unknown binding ids and keeps its word road, `S\manifest_put.py:2407-2408`,
  critic K2).

M2 — **writers.** `manifest_put.run` builds `notes = []`, `plan_map = C.plan_obligation_map(task_root, notes)` and calls
`stamp_obligation_refs(fragment, plan_map)` BEFORE the commit, between the expectation-change block (ends `:2425`) and the existing row-hash
check (`:2426`); each note → one stderr line `manifest_put: note: <sentence>` (exit unaffected); problems →
`"manifest_put: " + _problems_text(task_root, "obligation-refs", problems) + ". " + REPAIR_MARKER + "."`, `EXIT_BAD_FRAGMENT` (the shape of
`:2427-2431`); the stamped fragment is what every later check and the commit see. `manifest_from_tests.build` replaces its own hash line
(`:1462-1465`) by ids-only refs passed through the same function with `C.plan_obligation_map(task_root)` (so `--dry-run` and
`_form_after_write` see stamped rows); `manifest_put.run` stamping again is idempotent (every hash and derived field it meets is equal to
what it would write). **Code writers** (D4): a code writer that forwards stored refs or bindings drops what the stamp writes — per-ref
`obligation_hash`, binding `obligation_hash`, row `obligation_hash`, and, on a row that carries `obligation_refs`, `obligation_ids` — and lets
the stamp write it: `migrate_artifacts` gets ONE helper `_forwardable(row) -> dict` used at its four forwarding sites (§6 N1).

M3 — **carrier** `window_record.REQUIRED_ROW_FIELDS["obligation_refs"]` becomes `RowField(<what>, "plan_obligation", (), "automator",
FRAGMENT_DOOR, False)`; `what` = "the plan's obligation ids the test proves, as [{\"obligation_id\": \"<plan obligation id>\"}]; the code adds
each hash". `window=False` keeps it out of `window_text_fields` (`S\window_record.py:192-196`; `build` copies refs itself, `:1310`) — the
invariant: the window item's `obligation_refs` stays a LIST. Both owned render sites then name the fragment door with no code branch (axis
28). `MARKER_DOOR`, the `marker` value of `filled_by` (comment `:169-170`) and the `by_marker` / marker branches of `s5_precheck` and
`manifest_from_tests` lose their last user and are removed (AR-22); the one remaining marker branch, `brief_pack._row_field_lines`
`:2009-2010`, goes dead and is removed by T3b's port (queue line, §6 Crossings). The origin notes `ORIGIN["obligation_refs"]`,
`["obligation_ids"]` and `["obligation_hash"]` (`:138-143`) say: the automator sends the plan's obligation ids through the fragment door;
the code writes the hashes and the ids list. The role charter line `P\agents\qa-automator.md:69` says the same in one clause.

M4 — **precheck** `window_record._obligation_refs_problem(entry, plan, known=None)`: refs ABSENT or with no id-bearing item → `missing`
when the case owes an automated obligation, else `''` (the demand rule, unchanged); refs PRESENT (key with a value other than `None` and
`[]`) → judged on EVERY row, owed or not, through `C.obligation_ref_problems(refs, known)` (strict=False): the shape text (incl. "missing
hash" for a ref stored before the change), `unknown` (naming the plan's ids), `stale` ("the plan's obligation changed after the row was
written, or the hash was typed: send the row's obligation_refs again, ids only"). `row_field_gaps(entry, cfg, plan, known=None)` passes
`known` through; `check_row_fields` and `manifest_from_tests._row_form` pass `known=C.plan_obligation_map(task_root)`.

M5 — **finish** `Controller._s5_v2_collect` imports `contract as C` inside the function (lazy, like every `contract` import in
`controller.py`), builds `approved_obligations = C.obligation_map(approved_rows)` and judges refs through
`C.obligation_ref_problems(refs, approved_obligations, strict=True)`: `shape` → the existing text `:7302` (ValueError); then the fingerprint
check unchanged; then `unknown`/`stale` → the existing text `:7317` (StateConflict). Order and texts identical (E18); the one input class on
which the site of a refusal moves is named (E27).

M6 — **driver** (fork F4, HELD for the owner's word Q1) — `driver_dispatch`: a set whose every line is refused to every word at its source does
not get `go on` offered (t-181 A2); a set whose every line the source marks as the role's repair goes to the conductor (`call: True`, moves
`round`/`fresh`) before the person; `_exit_go_on` re-runs the gate after writing and never prints "recorded" over lines that still block
(t-181 A3).

### 4.1 AR-n touched, with the change check written into the DoD
| AR | How kept | Change check (DoD) |
|---|---|---|
| AR-13 (a fact with a reader is read through it) | one predicate + one map for writer, precheck, finish | Grep `obligation_hash` in `controller.py`, `window_record.py`, `manifest_put.py`, `manifest_from_tests.py`, `migrate_artifacts.py`: no inline per-ref hash comparison left outside `contract.obligation_ref_problems` / `stamp_obligation_refs` (row-level `content_hash(refs)` in `window_record.build` and `obligation_hash_problems` stays) |
| AR-14 (one artifact, one writer) | the per-ref, binding and derived row hashes have one writer function; code writers forward none | rows N1 (a), (b), (k), (n)-(p) |
| AR-15 (shared problem, one survivor, wired everywhere) | marker road, fragment road and code-writer road meet in `stamp_obligation_refs` | row N1 (h): Python marker and hand fragment store byte-identical refs |
| AR-20 (shrink-only ratchets; a raise named) | the charter line grows: `role-load.json` `process_ratchet_tokens["qa-automator"]` (slack 0) moves by the measured delta | the raise (or fall) is named in the N2 commit and in the critic verdict; `test_role_load.py` green in the witness |
| AR-22 (producer ↔ reader) | `MARKER_DOOR`, the `marker` filled_by value and marker branches removed with their last reader | Grep -i `MARKER_DOOR\|by_marker\|written by the marker` over `S\` → hits only in `brief_pack.py` `_row_field_lines` (T3b, queued line) |
| AR-23 / AR-28 (empty outcome; unknown never a pass) | empty map: writer and precheck refuse nothing about hashes (unreadable plan: one note), finish refuses strict; stale hash never passes the precheck | rows N1 (d), (q); N2 (f); N3 (e) |
| AR-1 / AR-2 (variety) | no language list added; the door text has no language branch | Grep `typescript\|\.spec\.ts\|java\|csharp` in the diff of `s5_precheck.py`/`window_record.py`/`manifest_put.py`/`contract.py` → none |
| AR-9 / AR-10 (refusal names expected + door; requirement told before work) | the carrier's `what`, FRAGMENT_DOOR, the ORIGIN notes and the charter line reach the role before work | rows N2 (a), (i), (k), (l) |
| AR-17 / AR-25 (state with no move → conductor; every state a move) | M6 | rows of N4 |
| AR-29 (code judges data; a role's judgment by a tier above) | every check added is DATA (shape/join against the plan); which obligation a test proves stays the automator's judgment, judged by the code critic (P17) | §4.2 |

### 4.2 Owner and census class of every check added or altered (AR-29, P27)
| Check | Owner it serves | Census class |
|---|---|---|
| `contract.obligation_ref_problems` (new predicate, `strict` flag) | data (code): shape and join against the plan | data check (shape/join) — the builder confirms the class word against `S\tests\fixtures\judgment-census.json`'s vocabulary and adds a row only if `test_judgment_census.py` requires one for the function (question back otherwise) |
| `stamp_obligation_refs` refusals in `manifest_put.run` (per-ref hash, binding hash, shape, unknown ref id, differing `obligation_ids`) | data (code): what the code computes is never typed | data check; refusal site for T5's registry (T5 converts it to `refusal(...)`, row id proposal `manifest_put:obligation_ref_hash`) |
| `plan_obligation_map` note (unreadable plan) | data (code) | not a check: a note line |
| `_obligation_refs_problem` (altered: present refs judged on every row; + unknown/stale) | data (code) | unchanged class (data) |
| finish `_s5_v2_collect` refs (altered: same verdicts through the predicate, strict) | data (code) | unchanged |
| `migrate_artifacts._forwardable` | not a check: a writer step | — |
| M6 driver offer / conductor road | intent of the person is not asked for what the factory owns; judgment of round vs fresh → the conductor (a role), its question accepted by the person | conductor judgment (`conductor_only` group if the census has one) |
Which obligation(s) a test proves: judgment of the automator (P17, many-to-many), reviewed by the code critic — no code check judges it
(fork F7 makes the marker road say the same).

## §5. Edges (behaviour | invariant)

| # | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | Test file with no marker (any language) | nothing changes in the reader: Python unmarked function ignored (`S\manifest_from_tests.py:22-23`); TS title without case id skipped (`:1354-1355`). The row, if it exists and its case owes an automated obligation, gets the precheck finding naming the fragment door | a field is never demanded through a door the file's language lacks |
| E2 | Marker / fragment names an obligation that does not exist | per F7 (b) both roads judge membership against the WHOLE plan's map: Python marker refused by `Story.obligation` naming the plan's ids; fragment refused by `stamp_obligation_refs` naming the plan's ids; when the map is empty neither refuses (ids stored unhashed) | an id the plan does not name never reaches the manifest while the plan names any (TP2-2553 class) |
| E3 | Legacy plan / no plan / plan unreadable (map empty) | writer: no per-ref stamp, no hash/unknown refusal; null keys still dropped, shape and derived fields still handled; unreadable plan → one note line (E26). Precheck: nothing demanded; present refs judged for shape only (strict=False). Finish: `strict=True` → every ref `unknown` → the `:7317` text, StateConflict — what an empty map gives today; an unreadable plan still raises at `_plan_document` (`S\controller.py:2253-2258`) | an unknown never becomes a pass at the finish (AR-28); nothing unproducible is demanded before it (FR-5) |
| E4 | One test → several obligations | refs list of several ids, each stamped; duplicate id in one row refused (shape) | each ref's hash binds its own plan obligation |
| E5 | Several tests → one obligation | each row carries the same `{id, hash}`; the binding names all instance ids (role's) | identical ids hash identically (one function) |
| E6 | Parameterised tests (`pytest.param`, `test.each`, partition titles) | refs are per ROW (instance); a marker on the function applies to each param instance as today (`:1426`); a fragment sends refs per instance id | no instance inherits refs it was not given |
| E7 | Row stored BEFORE the change with refs lacking a hash, or with a hash the plan no longer gives (TEMPORAL, world 1) | precheck, on EVERY row that carries refs (D3): `obligation_refs (missing hash ...)` / `(stale ...)` with the fragment door — one fragment with ids only repairs it; manifests are NOT migrated; `merge`/`fold`/`--recover` replay old events unchanged (the stamp sits in `run`, never in `merge`, like `stamp_provisional` `:2466-2468`). A CODE writer that forwards the stored row drops the hashes (M2, E29) and is never refused for them. A ROLE that copies the whole stored row back gets refused, in one call, by the stamp (per-ref hash differs: "leave `obligation_hash` out, the code writes it"), by `obligation_hash_problems` (row hash ≠ hash of the stamped refs: "leave it out, the code builds it") and, if its `obligation_ids` differ, by the ids problem — every text names the door: send `obligation_refs` with ids only | a reference measured on other bytes never counts; an old journal keeps folding; the copy-back refusal always has a door the role can use |
| E8 | Row written AFTER the change (world 2) | hashes always present and equal to the plan at write time | precheck and finish give the same verdict on the same refs (N2 (n) + N3 (c); end-to-end П1-б C10) |
| E9 | Hand-written ref without hash | accepted; the code writes the hash at write time | the refusal text's promise "the code builds it" is true (t-186 defect) |
| E10 | Hand-written ref with a wrong / uppercase / non-string hash | refused at write with the code's value (F2) | a hash the code did not compute is never stored |
| E11 | `obligation_refs: []` or refs absent on a row of an owed case | writer: `[]` accepted and CLEARS the stored refs (row gets `obligation_ids: []`, `obligation_hash: ""`); absent: untouched; precheck: `missing`; finish: shape refusal as today (`not refs`) | demand is the caller's rule; validity is one rule |
| E12 | Instance whose case owes no automated obligation and that carries NO refs, in a v2 window | precheck: not demanded; finish: still refuses "requires unique obligation_refs" (`:7298`) — divergence kept and NAMED (F3 (c), residual node) | no new trap is added; the existing one is surfaced, not hidden |
| E13 | Language with no reader (no `assertion_probes` row for the suffix) | `LanguageFile.no_entry` note as today (`:1342-1343`); the fragment door is the same text; never a refusal for lack of a reader | a language with no row is a note with a door, never a demand it cannot meet |
| E14 | Fragment `obligation_refs` (or `obligation_ids` / row or binding `obligation_hash`) sent as `null`; refs a string / dict / a list with a non-dict item | `null` → the stamp DROPS the key before the merge (= not sent): the stored value stays, so the row form sent back with its null slot never wipes stored refs (D7, `_merge_entry` `:1385-1386` would otherwise store `None`); to clear refs a role sends `[]` (E11); string / dict / non-dict item → refused at write naming the shape | a malformed list never folds into the manifest to fail later at the finish; an unfilled slot never erases a value |
| E15 | Plan changes between write and finish (re-plan) | finish refuses `:7317` as today; precheck says `stale` with the door | an approval measured on the old plan never counts |
| E16 | Magnitude: 1000 refs on one row / 200 rows in one fragment | every problem is collected; the refusal is ONE line through `_problems_text` (`S\manifest_put.py:1119-1123` → `detector_verdict.joined`, ceiling `FINDINGS_MAX_BYTES` = 6000 characters, `S\detector_verdict.py:63`, `:471-504`): AT the ceiling (joined text exactly 6000 characters) the whole list is in the line, no pointer; BEYOND it (6001) the items that fit, then `(+K more problems — the whole list: <story>\state\findings\manifest-put-obligation-refs.txt)`, the file written by the same call | one repair round, not one per row; the rest of a long list is never lost |
| E17 | Positional (M2): stamp placed after `unknown_obligation_refusal` (`:2407`) and the expectation-change block (`:2419-2425`), before `obligation_hash_problems` (`:2426-2427`) | the row hash check, `validate`/`_refuse_unmergeable` (`:2485`) and `fragment_key` (`:2477`) see stamped refs; binding ids unknown to the plan are skipped by the stamp | a row hash is never checked against unstamped refs; a word-passed `obligation-id` refusal (`_passed_by_word` `:2408`, bindings only, `:1031-1033`) never lets an unknown REF id through (the stamp refusal is not word-passable: a repair with a one-line door) |
| E18 | Positional (M5): predicate calls in the finish | order shape → fingerprint → plan, first failure per instance stops, texts byte-identical; the predicate returns shape problems alone when there are any | the driver/critic readers of these texts see no change; a broken ref list never reaches the hash comparison |
| E19 | Error direction of the reused `_obligation_refs_problem` (advice-shaped → now also judges hashes at a gate) | the demand rule may err only toward "not demanded" (it governs `missing` alone); PRESENT refs are judged on every row; with `known` non-empty it must NEVER pass a stale or unknown ref on any row, owed or not; with `known` absent or empty it may err only toward silence on hashes and ids, a side the finish covers with `strict=True`. Adversarial inputs that must stay refused (owed AND non-owed rows): hash of another obligation; hash with trailing space; uppercase hex; ref id with different case; id present twice with two hashes; `{"obligation_id": "OB-1", "obligation_hash": null}` stored before the change | a reference measured on other bytes never counts — at the precheck as at the finish |
| E20 | Error direction of `stamp_obligation_refs` (new writer-side gate) | may refuse a ROLE's fragment that it then resends without hashes (false refusal costs one turn); never refuses a CODE writer's forwarded row for a hash, because code writers drop hashes (M2); must never store a hash ≠ `content_hash(plan obligation)` and never stamp an id the plan does not name | AR-14; FR-5/FR-57 for code writers |
| E21 | Conflicting requirements: req 2 (one door text) vs the Python marker still writing ids; a Python row written by the marker AND by a fragment | both roads end in the same stamp; the text names only the fragment door (it works for Python too); the marker stays as a Python authoring form (F1 (a)); the LAST write wins (a later marker run rewrites the refs a fragment sent, and the reverse), both stamped identically | one door that works for every language is always named; whichever road writes last, the stored hash is the code's |
| E22 | Row whose case owes NO automated obligation but which CARRIES refs (D3; e.g. owes only `[{"obligation_id":"OB-M","decision":"manual-run"}]` and carries `[{"obligation_id":"OB-M","obligation_hash":"<pre-replan>"}]`) | precheck judges the present refs: stale → `stale`, no hash → `missing hash`, unknown → named; no refs → nothing (E12) | what the finish refuses on present refs, the precheck names first (one predicate, req 3); the finding has the ids-only door, so it is no trap |
| E23 | Same obligation id in two plan rows (an invalid plan; `coverage_contract.py:321-344` refuses it for schema-2) / a schema-1 row carrying `coverage_obligations` | the map reads all rows and the LAST occurrence wins — at the writer, the precheck and the finish alike (the finish's present reading); demand still reads schema-2 rows only (`plan_obligations`) | the three readers hash against one map, so they never disagree on the same plan |
| E24 | Role-sent `obligation_ids` (m3 (b)) | on a row that sends refs: a SET different from the refs' ids → refused ("leave it out, the code writes it"); the same set → the stamp writes the refs' order; on a row that sends `obligation_ids` without `obligation_refs` → untouched, today's behaviour (the finish judges ids against refs, `:7319`) | ids the code did not derive from the refs are never stored beside refs written in the same call |
| E25 | Stored row-level `obligation_hash` and an ids-only repair (m3 (c)) | a row that sends refs and no `obligation_hash` gets `content_hash(<stamped refs>)` (`""` for `[]`), replacing the stored one by the merge; a row that sends one keeps today's `obligation_hash_problems` check against the stamped refs | a row hash that binds other refs never survives a refs write (`probe_by_code.py:2854` prefers the stored value) |
| E26 | Plan file present but unreadable at the writer (m3 (d)) | one stderr line `manifest_put: note: the plan <path> could not be read (<cause>): obligation_refs are stored as sent, without hashes, and the window finish refuses them until the plan reads`; exit unaffected; nothing stamped; the precheck demands nothing; the finish raises at `_plan_document` | an unknown is named, never silent (FR-41, AR-23); nothing unproducible is refused (FR-5) |
| E27 | Non-string truthy `obligation_id` or `obligation_hash` at the finish (m3 (e), e.g. `{"obligation_id": 7, ...}`, `"obligation_hash": 123`) | today: passes the shape test (`:7298-7301`) and is refused at `:7317` (StateConflict) — or, for an int id whose `str` matches a plan id with the right hash, reaches `:7319`; after M5: `shape` → the `:7302` text (ValueError). The one input class on which a finish refusal moves site and class; named by a row of N3 | a ref whose id or hash is not a string never passes; refused earlier, never later |
| E28 | A non-dict item in stored refs (m3 (f), `[{"obligation_id":"o1"},"junk"]`) | the precheck gives a shape finding (door: send the refs again, ids only); `window_record.build` drops the item (`:1299`), so the finish passes the same row | the precheck is never more lenient than the finish (the safe direction); the stricter side has a door |
| E29 | A code writer forwarding stored rows or bindings (D4: `migrate_artifacts`) | `_forwardable` drops per-ref, binding and row `obligation_hash`, and `obligation_ids` on a row with refs; the stamp writes them from the current plan. A forwarded row citing an id the plan no longer names is refused by the stamp; `_run_manifest_put` returns the refusal text and the migration reports it under `left` (`:109-112`); the row stays as stored | an id the plan does not name never re-enters through a code writer; a migration never stops silently and never forwards a stale hash |

## §6. Nodes (owns by FUNCTION; for a weaker model; every test is a row in an existing keep file)

Common to every node: given `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (whole),
`C:\QAFactory\forge-repo\plans\builder-rules.md`, `C:\QAFactory\forge-repo\docs\TESTING.md`, this spec. Witness:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` and the files it prints, nothing larger (builder-rules
7b). New cases are ROWS of existing tables in the named keep files (`test-layers.json` keep: `test_manifest_put_merge.py` `:2912`,
`test_manifest_from_tests.py` `:2841`, `test_s5_precheck.py` `:4770`, `test_window_record.py` `:6865`, `test_controller_state.py` `:1078`,
`test_words_doors.py` `:6927`, `test_obligation_join.py` `:3345` (layer `detector`, `covers` lists `migrate_artifacts.py`),
`test_role_load.py` `:4512`); no new test file; the quarantined `test_row_fields.py`, `test_contract.py`, `test_exit_limit_halt_answered.py`,
`test_case_id_form_sites.py`, `test_story_resume_migration.py` are not run or edited. No node's test row needs a row of another unmerged
node: every cross-node agreement is proved by composition through N1's predicate (N2 (n) + N3 (c)).

### N1 — reader + stamp + writers (FV1-19a)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py` (new `obligation_map`, `plan_obligation_map`, `obligation_ref_problems`, `stamp_obligation_refs` only, placed after `legacy_obligation_map`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_put.py` (`run`: one stamp call, one note print, one refusal block between `:2425` and `:2426`; nothing else of `run`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_from_tests.py` (`build`: lines `:1462-1465` only; `Story.obligation` `:745-759` only under F7 (b))
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\migrate_artifacts.py` (new `_forwardable`; its calls in `_retract_case_ghosts` (`resend`, `:215`), `_retract_legacy_selector_rows` (`resend`, `:299`), `_legacy_obligation_patches` (`:346-350`), `_rename_legacy_obligations` (`:395`))
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_put_merge.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_from_tests.py` (rows of `build`/stamp only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_obligation_join.py` (section 4 rows, `:177-249`, and new rows beside it per F9)
Expected behaviour and one test row each:
(a) fragment `[{"obligation_id": "OB-1"}]` → stored ref carries `content_hash(plan OB-1)`, row `obligation_ids == ["OB-1"]`, row
`obligation_hash == content_hash(<stored refs>)`;
(b) wrong hash → exit `EXIT_BAD_FRAGMENT`, stderr names `<id>`, the sent and the plan's hash, "leave `obligation_hash` out",
`REPAIR_MARKER`; manifest revision unchanged;
(c) unknown id with a non-empty plan → refused naming the plan's ids;
(d) empty plan / no plan → refs stored as sent (no hash added), exit 0, no note; derived `obligation_ids`/row hash written;
(e) refs `"OB-1"` (string), `{"obligation_id": "OB-1"}` (dict) and `[1]` → refused (shape);
(f) D7: a row sending `"obligation_refs": null` over a stored row with refs → stored refs unchanged (key dropped); `[]` → refs cleared,
`obligation_ids == []`, row `obligation_hash == ""`; the same null drop for a row `obligation_ids: null`, a row `obligation_hash: null` and a
binding `obligation_hash: null`;
(g) duplicate id in one row → refused;
(h) Python marker `obligations=["OB-1"]` and a hand fragment for the same instance produce byte-identical `obligation_refs` (AR-15 row);
(i) `--dry-run` row form of a marker run reports no `obligation_refs` gap (stamped before the merge view);
(j) a replay of a journal holding an old unstamped event folds unchanged (merge stays pure);
(k) F5: a binding without hash → stamped; with a wrong hash → refused; a binding with an id the plan does not name → untouched by the stamp
(the `obligation-id` refusal and its word road unchanged);
(l) magnitude: 1000 refs on one row, 3 bad → ONE refusal line naming the 3 problems; AT the ceiling (problems whose joined text is exactly
6000 characters) → whole list, no pointer; BEYOND (6001) → the pointer `(+K more problems — the whole list: ...manifest-put-obligation-refs.txt)`
and that file holds every problem;
(m) m3 (b): a row sending refs `[OB-1, OB-2]` and `obligation_ids: ["OB-1"]` → refused "leave it out, the code writes it"; with
`["OB-2", "OB-1"]` → accepted, stored ids in refs order `["OB-1", "OB-2"]`; a row sending only `obligation_ids` → stored as sent;
(n) m3 (c): a stored row with `obligation_hash` H_old; an ids-only fragment for it → stored row hash == `content_hash(<new stamped refs>)` ≠ H_old;
(o) D4, in `test_obligation_join.py` section 4: the existing check "and so do its obligation_refs, hash untouched" (`:231-232`, expects
`"obligation_hash": "h1"`) is REWRITTEN: after the migration the ref is `{"obligation_id": "TS-1-O1", "obligation_hash":
content_hash(<plan obligation TS-1-O1>)}` and `--if-older` exits 0 (today `h1` would be refused by the stamp); a seed binding carrying an
`obligation_hash` → the renamed binding carries the plan's hash of its new id;
(p) D4, the two retraction sites (per F9 (a), rows beside section 4 of `test_obligation_join.py`): a ghost row covered by a real row whose
stored refs carry a stale hash → `_retract_case_ghosts` commits, the covering row's refs carry the current plan hash; the same for
`_retract_legacy_selector_rows`; a covering row citing an id the plan no longer names → the retraction lands in `left` with the stamp's
text (E29);
(q) m3 (d): a plan file that is not JSON → exit 0, one stderr line starting `manifest_put: note: the plan`, refs stored as sent;
(r) F7 (b) only: a marker naming an obligation of ANOTHER plan row → accepted and stamped; a marker naming an id absent from the whole plan →
refused naming the plan's ids; with an empty map → ids stored unhashed, no refusal.
DoD: rows (a)-(r) green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the owns above>` and the files it
prints, output attached verbatim; FR walk lines for A (refusal text), C (contracts: FR-11, FR-14), D (FR-16), G; `architecture:` line names
AR-13, AR-14, AR-15, AR-23, AR-28.

### N2 — carrier, precheck, owned render sites, origin notes, charter (FV1-19b; depends N1)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py` (`REQUIRED_ROW_FIELDS` entry `obligation_refs`; `MARKER_DOOR` removal; the `filled_by` comment `:169-170`; `ORIGIN["obligation_refs"]`, `ORIGIN["obligation_ids"]`, `ORIGIN["obligation_hash"]`; `_obligation_refs_problem`; `row_field_gaps` signature + docstring)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py` (`check_row_fields`: the one call line passing `known`; `_row_fields_text`: `by_marker` branch removal — NOT `report`, NOT `refusal_cause`, NOT any FV1-30a function)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_from_tests.py` (`_legend_line`: marker branch removal; `_row_form`: the `row_field_gaps` call passing `known`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-automator.md` (section `## Tools`, the line `:69`: the `obligation_refs` clause only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json` (`process_ratchet_tokens["qa-automator"]` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_window_record.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_from_tests.py` (rows of the row form; the K7 rows `:1848-1852`)
Expected behaviour, one row each:
(a) TS row of an owed case without refs → finding fix names the fragment door with `"obligation_refs": [{"obligation_id": "<plan obligation
id>"}]`, no "marker", no "qa(obligations" (also for a Python row: one text);
(b) row form prints a null slot for `obligation_refs` with the legend `what`;
(c) refs without hash stored before the change → `obligation_refs (missing hash ...)`;
(d) stale hash → `stale` text; (e) unknown id → named with the plan's ids;
(f) owed empty (legacy plan) and refs absent → no finding (E3); owed empty and refs present with an empty map → shape only;
(g) the window item built from a row with refs keeps `obligation_refs` as a LIST and `window_text_fields()` does not contain it (M3);
(h) E19 adversarial rows (six inputs, one row each, all refused) — on an owed row AND on a non-owed row;
(i) brief line generator (`brief_pack._row_field_lines`, read only) prints the new `what` with no marker text — assertion in
`test_window_record.py` over `REQUIRED_ROW_FIELDS` (`filled_by == "automator"`, `origin_door == FRAGMENT_DOOR`), not a `brief_pack` edit
(T3b owns it);
(j) D3: a NON-owed row (case owes only `manual-*`) with a stale ref → `stale`; with a ref lacking a hash → `missing hash`; with no refs →
no finding;
(k) D1: `ORIGIN["obligation_refs"]`, `["obligation_ids"]`, `["obligation_hash"]` name the fragment door and "the code writes the hashes";
none says the automator writes hashes (`test_window_record.py`);
(l) D1: the line of `agents/qa-automator.md` that names `obligation_refs` contains `manifest_put.py` and "ids" and does not contain
`qa(obligations=` (`test_window_record.py`, a row reading the charter file by its package path);
(m) m4: the K7 rows of `test_manifest_from_tests.py:1848-1852` are rewritten — the legend for `obligation_refs` names the fragment door and
not `qa(obligations=`; rows of owed cases WITHOUT refs now carry an `obligation_refs` slot; the `test_limit` row (the marker wrote its refs)
still asks for the four fields only;
(n) D5, agreement by composition (merge-order independent): on inputs {valid, stale, missing hash, unknown id with a non-empty plan, a
non-owed row with a stale ref}, the precheck's verdict for the row (no `obligation_refs` problem / a named problem) equals whether
`C.obligation_ref_problems(refs, C.obligation_map(<plan rows>), strict=True)` returns `[]` — N1's predicate only, never the controller.
DoD: rows green; the precheck names the fragment door for a TS row (row (a)); Grep -i `MARKER_DOOR|by_marker|written by the marker` over
`S\` → hits only in `brief_pack.py` `_row_field_lines`; `process_ratchet_tokens["qa-automator"]` moved by the delta `role_load.py`
measures, the raise or fall named in the commit message and handed to the critic (AR-20), `test_role_load.py` green in the witness;
witness via `--witness-for <the owns above>`. The charter edit is a role-behaviour change (FR-33): closed by code, not proven; the Lead adds
the batch's «Живые доказательства» row "a TS story: the automator sends `obligation_refs` ids-only through `manifest_put.py --fragment`;
the manifest stores the code's hashes; the window finish passes" (moved to `live-runs` per PROJECT.md «Командная работа» 9). N2 does NOT
touch `form-rounds.json` (D6: the `known_red: FV1-19` removal is П1-а's).

### N3 — finish through the one reader (FV1-19c; depends N1; parallel with N2)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py` (`Controller._s5_v2_collect` lines `:7289-7323` only, incl. one lazy `import contract as C` inside it — not `_s5_gap_problems`, `_record_person_pass`, `_record_s5_word_passes`, `_plan_refusal` (FV1-30a), not any T9a function)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_state.py` (rows)
Expected behaviour, one row each:
(a) the five existing verdict texts byte-identical on their old inputs (string ids and hashes);
(b) order E18 (a broken list never reaches the hash comparison; a missing fingerprint still comes before a stale hash);
(c) D5, finish side only: on {valid, stale, missing hash, unknown id, empty map}, the finish's verdict equals the kind list of
`C.obligation_ref_problems(refs, C.obligation_map(<approved rows>), strict=True)` — `shape` → the `:7302` text (ValueError), `unknown`/`stale`
→ the `:7317` text (StateConflict), `[]` → the later checks run;
(d) a plan obligation in a schema-1 row is in the map (today's behaviour kept);
(e) D2: an approved plan whose rows name no obligation (empty map) → every instance with refs gets the `:7317` text, StateConflict — as today;
(f) m1: the same obligation id in two plan rows with different objects → the LAST row's object is the one hashed (as today);
(g) m3 (e): `{"obligation_id": 7, "obligation_hash": "<plan hash of \"7\">"}` and `{"obligation_id": "OB-1", "obligation_hash": 123}` →
the `:7302` text (ValueError) — the one named move (E27).
DoD: rows green; `--witness-for <the owns above>`; critic on the diff (controller is core, CLAUDE.md rule 3).

### N4 — the driver does not put a factory repair to the person (FV1-19d; fork F4 HELD; independent of N1-N3; after FV1-30a merges)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`handoff_ladder` — only the count of refused/repair records before `refusal_lines` flattens, `:535`; `exit_limit`; `exit_limit_facts`; `_exit_go_on`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (rows)
очередь: П1-в N0 → FV1-19 N4 (`driver_dispatch.handoff_ladder`, `driver_dispatch.exit_limit`; `20261113-p1v-run-scoreboard-spec.md:444`)
очередь: П1-в N2 → FV1-19 N4 (`driver_dispatch.handoff_ladder`; `20261113-p1v-run-scoreboard-spec.md:446`)
(N4 is held for Q1; when dispatched it merges `main` into its tree after П1-в N0/N2 and resolves the two functions itself, critic after the
merge — PROJECT.md «Командная работа» 3. The same two lines go into П1-в's batch file by its Lead.)
Expected behaviour (per F4 (a)), one row each: (a) every reaching line refused to every word at its source → `go on` absent with "the check
refuses every word for N of these lines; only <role> can repair them" (a second row of the `absent` structure `:3707`, not a new branch);
(b) every reaching line marked the role's repair, and `round` or `fresh` open → `no_move` with `call: True` and `site_doors` `round`/`fresh`;
no `driver-question.md` is written before the conductor answers; the conductor's `ask_person` still reaches the person (P22); (c) (a) with
`round` and `fresh` both absent → the conductor (`call: True`), never a person-only `stop` (FR-57); (d) mixed set (some lines passable) →
today's question unchanged; (e) after `go on`, `_exit_go_on` re-runs the stage's exit errors; lines still blocking → `held_question` "your
word was recorded but the check does not accept a word for: <lines>; only the role can repair them", no "recorded" print; (f) the conductor
cap spent (`ConductorSpent`) → today's priced question (`driver_conductor.py:646-647`).
DoD: rows green; `--witness-for <the owns above>`; critic on the diff.

Merge order: N1 → (N2 ∥ N3) → T5. N4 after FV1-30a and after П1-в N0/N2, any order with N1-N3. No node writes `story_run.py`.

### Crossings — function-level owns, checked
| Other node | Its owns in the same files | Overlap with FV1-19 |
|---|---|---|
| FV1-30a | `s5_precheck`: `_passable`, `passed_by_word`, word-selection helpers, `word_passes`, `run.word_passes`; `controller`: `_record_person_pass`, `_record_s5_word_passes`, `_s5_gap_problems`, `_plan_refusal`; `branch_accounting.s5_problems` | no function overlap (N2: `check_row_fields` one line, `_row_fields_text`; N3: `_s5_v2_collect`). MEANING crossing: after FV1-30a a word passes `row-fields-missing` at the precheck while `_s5_v2_collect` reads no word and refuses the same refs — fork F8; FV1-30a's lower-readers table (`p1-specs-amendment-owner-words.md:398-404`) needs the row whichever way F8 goes |
| FV1-30b | `s5_precheck.report` tail, `refusal_cause` | none |
| T5 | `s5_precheck.report` + family producers (`check_row_fields`, `_row_fields_text` ARE family producers), `manifest_put` §5.4 functions (`obligation_hash_problems` …), `execution_request.validate_request`, `run_suite` | sequential by queue FV1-19 → T5 (`told-before-work-mechanism-spec.md:374`); T5 merges main after FV1-19 and converts the new `manifest_put.run` refusal to `refusal(...)` |
| T3b (`brief_pack`) | `window_record.row_field_lines` (new), `brief_pack._row_field_lines` | queue line to T3b: "`row_field_lines`: no marker branch (FV1-19)" — the `else` branch `brief_pack.py:2009-2010` goes dead after N2 and is not ported |
| T3b × `test_window_record.py` | T3b's rows for `row_field_lines` in the same keep file N2 adds rows to | `очередь: FV1-19 N2 → T3b` on `test_window_record.py`: FV1-19 first; T3b merges main and keeps N2's rows (i), (k), (l) green |
| П1-а | ledger `P\scripts\tests\fixtures\form-rounds.json` section `known_red` (row C3, `known_red: FV1-19`); its N3 item 7 reconciles it | D6: FV1-19 writes NO line of П1-а's files. The removal of `known_red: FV1-19` is П1-а's: if П1-а N3 merges AFTER FV1-19 N2, its ledger is written without the FV1-19 row (C3 green); if BEFORE, N2's merge turns the row `stale` and П1-а's Lead removes it in the next П1-а commit. П1-а's rule `:640` ("the repairing node removes its row") needs this exception written by П1-а's Lead (queue line to П1-а); F6 (a) (C3 reads the carrier as the producer) stays П1-а's walker work |
| П1-в N0, N2 | `driver_dispatch.handoff_ladder` (N0, N2), `driver_dispatch.exit_limit` (N0) | the two `очередь:` lines of N4 above; N4 is held (F4), so П1-в goes first |
| other specs of 13.11 on `migrate_artifacts.py` / `test_obligation_join.py` | none (Grep -i `migrate_artifacts\|test_obligation_join` over `docs\tasks\specs\20261113-*.md`: hits only in this spec and its critic review — positive control: the same call finds this spec's own line) | N1 owns the four functions alone |

Queued, not in a node (rule 9, each with its pointer):
- `P\skills\qa-story\phases\s5.md:292-299` ("The automator's manifest comes from its markers"; `obligation_refs` among the derived fields) →
  the F1 (c) node of the untaken `live-run-fvf` batch (the same owner; its text changes with F1 (c)); until then the precheck, the row
  form, the origin notes and the charter name the fragment door.
- `brief_pack._row_field_lines` marker branch → T3b (above).
- F3 (c) residual node and F1 (c) node → `live-run-fvf` untaken batch (§8a).
- Other `pass_block` writers without read-back (axis 17 below) → t-181 class line `:121`.

## §7. Four questions (CLAUDE.md rule 10)

(a) **Cost and who pays.** One stamp call per `manifest_put` write (a plan read: `_plan_rows_of`, already read by `unknown_obligation_refusal`
in the same call) — code time, no LLM. Role: one fewer field to type (hashes), one door to learn; the charter line grows by a few tokens
(process ratchet raise, named). Precheck: one map build per run. Migration: no extra call (the stamp runs inside the `manifest_put` it
already calls). Driver (N4): one paid conductor call per all-repair exit_limit set, instead of a free person question (F4 names this price).
(b) **Axes** (36, `docs\SIBLING_MAP.md` headings `:24-606`), mechanism "one reader + stamp" (M1-M5) and mechanism "driver offer" (M6):
axis 1: n/a — no forge policy / forge role file / journal change (the package charter line is axis 28 and 34). axis 2: n/a — no exam
instrument. axis 3: n/a here — release copy follows at release. axis 4: covered — no new FR; debt none (FR-5/FR-11 instance removed).
axis 5: covered — S5 only; no stage twin carries `obligation_refs`. axis 6: n/a — measurers unaffected. axis 7: n/a — test identity
untouched. axis 8: n/a. axis 9: n/a — "is a test file" untouched. axis 10-11: n/a. axis 12: covered — the П1-а `known_red` mark is П1-а's,
named in Crossings with both merge orders. axis 13: n/a. axis 14-16: n/a. axis 17: covered by N4 (the driver honours the `refused` class;
the other `pass_block` writers share write-without-read-back — queued, t-181 class line `:121`, NOT in this spec). axis 18: covered — the
`process_ratchet_tokens["qa-automator"]` move is named in the N2 commit and the critic verdict (AR-20); if `judgment-census.json` gains a row
it is named in the verdict. axis 19-22: n/a. axis 23: covered — the carrier row changes and every reader (precheck, row form, brief, origin
notes) reads it. axis 24-27: n/a (axis 27 `profile_id` untouched). axis 28: covered — the owned render sites (precheck, row form) change in
one node (N2); the third (`brief_pack._row_field_lines`) is T3b's, queued by line; the stage text `s5.md` queued by pointer. axis 29-31:
n/a. axis 32: covered — §4.2. axis 33: n/a. axis 34: covered — one door for every language, no language list; one membership rule for
both id roads (F7 (b)); the residual (Python marker as an authoring form; `.py` suffix in `_files`) is F1 + a census line. axis 35-36: n/a.
(c) **Detectors.** П1-б C10 (`p1b-dry-story-spec.md:87`, row `s5.window_finish/ref_without_hash`) for precheck/finish agreement end to end;
N2 (n) + N3 (c) for the same agreement at unit level; П1-а C3 for producibility per language; `test_manifest_put_merge.py` rows for the
stamp; `test_obligation_join.py` for the code-writer road; `test_role_load.py` / audit A22 for the ratchet; calibration check 41 (judgment
census) for §4.2.
(d) **What stops a skip.** The stamp sits on `manifest_put.run`, the only writer of the manifest (AR-14) — every road, code writers
included, passes it; the carrier row is read by every render site (AR-13); the finish calls the predicate on every window. N4: the seam is
the only exit-limit road (`driver_dispatch.py:3532-3535`). Discipline-only part: the queued render sites (T3b line, `s5.md` pointer) —
their detector is the AR-22 Grep of the N2 DoD and the critic's axis-28 walk.

## §8. Forks — RETURNED (options, consequences, recommendation)

**F1 — the road for the IDS (P31, axis 34).**
(a) Fragment door for every language is THE named door; the Python `qa(obligations=)` marker keeps working as an authoring form that feeds
the same stamp. Cost: small; the residual (two authoring forms meeting in one stamp) leaves only with (c). (b) Add a TS marker now (a title
tag such as `@ob:<id>` read from `test_source` `tags`, `S\test_source.py:206-208, 353`); Java/C# keep the fragment (no `title_tag` in their
entries, `S\..\references\detectors.json:86-264`). Cost: a data key + a reader branch in `language_rows` + rows; it invents a practice no
project writes today (§2) and still leaves two languages on the fragment. (c) Derive refs from `obligation_bindings[]` (the role already binds
every obligation to instance ids, all languages, `S\s5_precheck.py:3843-3894`): no marker at all, one road truly; removes the duplicate the
role keeps in sync by hand (`coverage_contract.py:280-282`). Cost: refs become derived — every reader of row refs (`window_record.py:1299`,
`probe_by_code.py:2847`, `manifest_view.py:65`, `coverage_contract.py:280`) moves to one reader; a meaning change → critic on plan; collides
with T5/T3b timing. **Recommendation: (a) now** (nodes written per it), **(c) as the class fix** in a later node of the pile (owner: Lead of
`live-run-fvf`; owns the four readers named; test: rows in `test_window_record.py`). (Fix round t-496: the `obligation_marker` data row
earlier promised under (a) is struck — no node created it, and F7 (b) leaves no membership difference for it to carry.)

**F2 — a hand-typed ref hash that differs from the plan.** (a) refuse at write with the code's value (consistent with the row-hash check
`manifest_put.py:592-622`; a mismatch may mean the role read another plan); (b) overwrite silently. **Recommendation: (a).**

**F3 — the finish demands refs of every v2 instance; the precheck only of owed rows (E12).** (a) the finish takes the same demand rule (needs
the instance → case → plan-row join in the controller: a meaning change, critic on plan); (b) the precheck demands refs on every row of a v2
task — a trap for rows whose case owes none (FR-5); (c) keep both, name the edge, open a residual node (owns `Controller._s5_v2_collect`,
`window_record.build` — an `owes_obligation` fact on the item; test rows in `test_controller_state.py`). **Recommendation: (c)** — validity
is unified here (req 3); the demand rule is a separate meaning. (D3 of t-490 is not F3: present refs are now judged on every row.)

**F4 — a set the source marks as the role's repair reaches `exit_limit` (defect 3).** (a) N4: refused-at-source → no `go on`; all-repair
with a live move → the conductor first (`call: True`); `go on` read back. Consequence: a paid conductor call where today a free question;
departs from the letter of t-217 (`call=False` on an unchanged set) though not from D-0041 (no new words exist) — P22 (09.10) is the owner's
later and wider word. (b) only A2 + A3 (truthful offer, read-back), the person still asked. (c) nothing in FV1-19. **Recommendation: (a)**,
and it needs the owner's word (price and the t-217 letter) — question Q1 below. Until the answer, N4 is held; N1-N3 do not depend on it.

**F5 — `obligation_bindings[].obligation_hash` (same class, read by the coverage projection).** (a) stamp it in the same function (N1 row
(k)); (b) leave it. **Recommendation: (a)** — same artifact, same writer, same class (rule 9 sweep).

**F6 — П1-а C3 may define "producer" as `manifest_from_tests` only.** If N2 lands and C3 stays red because the walker does not accept the
fragment door (filled_by `automator`) as the producer, the row's definition contradicts the one road; options: (a) the П1-а row reads the
carrier (`REQUIRED_ROW_FIELDS.filled_by` + `origin_door`) as the producer; (b) keep red until F1 (c). **Recommendation: (a)** — Lead of П1-а.

**F7 — the two id roads judge MEMBERSHIP differently (P31; critic t-490 m2).** The marker refuses an id that is not an obligation of the
CASE'S OWN plan row (`S\manifest_from_tests.py:749-758`; a case with no plan row is refused too); the fragment stamp refuses only an id
absent from the WHOLE plan. Two roads, two rules for the same act — a P31 defect whichever is kept, unless the owner says otherwise.
(a) One rule = the case's own plan row, on both roads: the stamp needs the instance → case → plan-row join at the writer (`case_plan_row`
lives in `s5_precheck`; `manifest_put` would import it or a contract twin of it). Cost: a new join in the writer's import graph, a meaning
change at the writer (critic on plan), and it forbids under code what P17 allows (a test proving another row's obligation — many-to-many).
(b) One rule = the whole plan, on both roads: `Story.obligation` looks the id up in `C.obligation_map(<all plan rows>)` and hashes that
object (no plan-row requirement; with an empty map ids are stored unhashed, as the fragment does). Cost: one function in N1 (row (r)); the
"right id, wrong row" typo guard of the marker goes — what remains judges it: the code critic (P17, AR-29) and the coverage projection,
where the binding shows which instance proves which obligation. (c) Keep both, named as a residual node — legal only with the owner's word
(P31). **Recommendation: (b)** — membership is DATA (is the id the plan's?); which obligation a test proves is the automator's judgment, by
P17 many-to-many, judged by the critic; N1 is written with row (r) conditional on (b) (struck under (a)/(c)).

**F8 — a person's word passes `row-fields-missing` at the precheck (after FV1-30a) while the finish reads no word (cross-spec gap, critic
t-490).** After FV1-30a, `go on` passes the precheck's `obligation_refs` gap; `_s5_v2_collect` (`S\controller.py:7298-7317`) then refuses
the same refs and no word reaches it — the person's word is taken and the factory stops one stage later, at tier 3. (a) The finish reads
the same word: an instance whose `obligation_refs` gap the person passed is not refused by the refs checks, and its obligations reach the
coverage projection as `unknown` / a gap under the person's word (never as proven; AR-28), the pass written to the findings (P13). Owner of
the change: FV1-30a (its word reader, `_record_s5_word_passes` / `_s5_gap_problems`), plus one line in its lower-readers table; N3 is not
changed. Cost: a new reader of the word in the controller (FV1-30a's functions), and a story that delivers with a named coverage gap.
(b) The word does not pass an `obligation_refs` gap: after N1-N2 the repair is always producible (one ids-only fragment, every language), so
the precheck emits this field under a tag outside the word-passable set. Cost: narrows P13 ("the person's word passes any gate") for one
field — needs the owner's word; the repair then always falls to the role (and, with F4 (a), to the conductor). (c) Leave it: the person's
word is accepted and then betrayed by the finish (FR-8, AR-24 broken). **Recommendation: (a)** — P13 is the owner's word, and the
person's pass becomes a named gap instead of a silent stop; the Lead puts the row to the FV1-30a spec. (b) only if the owner narrows P13.

**F9 — the keep file for the two retraction sites of `migrate_artifacts` (D4).** The only keep file that judges `migrate_artifacts.py` is
`test_obligation_join.py` (layer `detector`, `covers` lists it, `test-layers.json:3345-3359`); today it exercises ONLY the rename road
(section 4, `:177-249`). The retraction roads (`_retract_case_ghosts`, `_retract_legacy_selector_rows`) are judged only by quarantined files
(`test_case_id_form_sites.py:678`, `test_story_resume_migration.py:192`; quarantine section from `test-layers.json:7046`). (a) Add the
retraction rows of N1 (p) beside section 4 of `test_obligation_join.py` (its subject is the obligation join; the rows test that a
retraction never trips over a stale obligation hash). (b) Leave the retraction sites with `_forwardable` but no row (the helper is proved by
the rename rows (o)); a queue line for a retraction row. (c) Instead of stripping, the two retraction sites send the covering rows WITHOUT
the obligation keys at all (`_merge_entry` keeps the stored values): the retraction never re-cites obligations, so an id the plan no longer
names never blocks it (E29 disappears for these two sites); stale stored refs are then named by the precheck (E7). Cost: a second rule for
code writers beside D4's, which the Lead decided as ONE rule. **Recommendation: (a)** with D4's one rule; (c) is listed because it removes
the E29 stop for retractions, at the price of a second rule.

### Question for the owner (plain language, process/price only)
- **Q1 (F4).** «Когда проверка автотестов называет недочёт ремонтом самой роли, а роль уже дважды вернулась с ним же, — звать дирижёра
  (это платный вызов модели, он сам решит: дать роли ещё ход или начать заново) или, как сейчас, сразу спрашивать вас? Рекомендую дирижёра:
  вы не знаете об этом недочёте больше, чем проверка».
- **Q2 (F8, only if the Lead leans to (b)).** «Если вы сказали "иди дальше" при недочёте в ссылках автотеста на обязательства плана, а
  исправить его можно одной правкой роли, — пропускать дальше с пометкой "пробел покрытия по вашему слову" (рекомендую) или ваше слово этот
  недочёт не снимает и правит роль?»

## §8a. Lead acceptance of the draft, 13.11.2026 (t-483) — forks

| fork | decided | by | note |
|---|---|---|---|
| F1 | (a) now; (c) is the class fix and gets its own node in the untaken batch of `live-run-fvf` | Lead ("решила сама", shown to the owner) | P31 residual, named: after (a) the IDS still have two authoring forms (Python marker, fragment) that meet in one stamp; only (c) removes it. The owner is told; her word may pull (c) forward |
| F2 | (a) refuse at write with the code's value | Lead | same direction as the row-hash check |
| F3 | (c) keep both, edge E12 named, residual node | Lead | the demand rule is a separate meaning (package change item 6 (г)) |
| F4 | HELD — owner's question Q1 (price of a conductor call) | owner | N4 is not dispatched before her word; N1-N3 do not depend on it |
| F5 | (a) bindings stamped by the same function | Lead | same artifact, same writer (rule 9 sweep) |
| F6 | (a) the П1-а row reads the carrier as the producer | Lead (of П1-а too) | goes into П1-а N2 walker work; if C3 stays red after N2 of this spec, the builder returns it |

Next: critic on the plan (schema of the manifest row + controller core + forks; CLAUDE.md rule 3), then N1.

## §8b. Fix round after the critic on the plan (t-490) — task t-496, 13.11.2026

Verdict: `docs\tasks\specs\reviews\20261113-fv1-19-plan-critic.md` (ACCEPT WITH FIXES). The Lead's decisions per item (binding) applied in
place; one row per item: what changed, and where.

| item | what changed | where |
|---|---|---|
| D1 | N2 owns gain `agents/qa-automator.md` (`## Tools` line `:69`, the `obligation_refs` clause) and `ORIGIN["obligation_refs"]` / `["obligation_ids"]` (plus the sibling `["obligation_hash"]`, same block, sweep) with rows (k), (l); `role-load.json` `process_ratchet_tokens["qa-automator"]` owned, raise named (AR-20); charter edit named as needing a `live-runs` row (FR-33); queue line to T3b "`row_field_lines`: no marker branch (FV1-19)"; Crossings row T3b × `test_window_record.py`, FV1-19 first; `s5.md:292-299` queued; AR-22 grep widened to `written by the marker` | §1.1 (charter, stage text rows), §1.2 (origin notes, render site 3), §3 req 2, §4 M3, §4.1 (AR-20, AR-22), §6 N2 owns/rows/DoD, §6 Crossings + "Queued", §7 (b) axis 18/28 |
| D2 | `obligation_ref_problems(refs, plan_map=None, strict=False)`; the finish passes `strict=True`: an empty or missing map makes every ref `unknown` → the `:7317` text, as today; N3 row (e); E3 and §9.2 corrected | §4 M1, M5; §3 req 4; §5 E3; §6 N3 (e); §9.2 |
| D3 | the demand rule governs ONLY `missing`; present refs are judged on every row for shape, unknown and stale; new edge E22; E19 reworded; N2 rows (h) (non-owed side) and (j) | §3 req 3; §4 M4; §5 E19, E22; §6 N2 (h), (j) |
| D4 | one rule: a code writer forwarding stored refs or bindings drops what the stamp writes (`migrate_artifacts._forwardable`); the four sites in N1 owns; keep file `test_obligation_join.py` named (rename road row (o), incl. rewriting the "hash untouched" check `:231-232`); the retraction sites have no keep-file judge today (only quarantined files) — returned as F9, rows (p) written per F9 (a); E7 names the copy-back refusal and its door; new edge E29; E20 reworded | §1.1 (code writer row), §3 req 1/6, §4 M2, §5 E7, E20, E29, §6 N1 owns/(o)/(p), §8 F9 |
| D5 | N3 (c) tests the finish against `C.obligation_ref_problems` only; the precheck side is N2 (n), which calls only N1's predicate — the agreement holds by composition, independent of merge order | §6 N2 (n), N3 (c), §6 header note; §5 E8 |
| D6 | the `known_red: FV1-19` removal moved OUT of N2 to П1-а (both merge orders written; П1-а's rule `:640` exception queued to its Lead); N2's DoD keeps "the precheck names the fragment door for a TS row"; N4 gets two `очередь:` lines against П1-в N0 / N2 on `handoff_ladder` / `exit_limit`; Crossings rows П1-а (rewritten) and П1-в (new) | §1.5, §6 N2 DoD, §6 N4 owns, §6 Crossings, §7 (b) axis 12 |
| D7 | decided: the stamp DROPS an `obligation_refs: null` key (and, as the same rule, `obligation_ids` / row and binding `obligation_hash` null) before the merge — null = not sent; `[]` clears; E14 and N1 (f) reworded (rows for null and for `[]`); E11 says `[]` clears | §4 M1 step 1, §5 E11, E14, §6 N1 (f) |
| m1 | `obligation_map`: last occurrence wins (the finish's reading); req 4 split into demand (schema-2) vs validity map (all rows); new edge E23; N3 row (f) | §3 req 4, §4 M1, §5 E23, §6 N3 (f), §9.2 |
| m2 | membership-scope difference RETURNED as fork F7 (options, recommendation (b) whole plan); N1 row (r) conditional on F7 (b); E2 reworded; the `obligation_marker` data row struck from F1 (a) | §8 F7, F1; §5 E2; §6 N1 owns/(r) |
| m3 | (a) `_problems_text` ceiling 6000 characters, spill file named, AT/BEYOND rows — E16, N1 (l); (b) a role-sent `obligation_ids` that differs from the refs is refused like a differing hash — M1 step 5, E24, N1 (m); (c) the stamp recomputes the row-level `obligation_hash` on every refs write — M1 step 5, E25, N1 (n); (d) unreadable plan at the writer prints one note line — M1 `plan_obligation_map`, M2, E26, N1 (q); (e) non-string truthy id/hash moves from `:7317` to `:7302` — E27, N3 (g); (f) non-dict item: precheck stricter than `build`, named — E28 | §4 M1, M2; §5 E16, E24-E28; §6 N1 (l)-(n), (q); N3 (g) |
| m4 | `test_manifest_from_tests.py:1848-1852` named as rows N2 rewrites (N2 (m), owns line); N3 uses a lazy `import contract as C` inside `_s5_v2_collect` (§9.1 reworded) | §6 N2 owns/(m), N3 owns, §4 M5, §9.1 |
| cross-spec gap | Crossings row FV1-30a (meaning crossing) + fork F8 (options: the finish reads the same word / the word does not pass an `obligation_refs` gap / leave; recommendation (a)); owner question Q2 drafted for (b) | §1.5, §6 Crossings, §8 F8, §8 Q2 |

## §8c. Lead acceptance of the fix round, 13.11.2026 (t-496)

Checked: every D1-D7 / m1-m4 item has a §8b row and the named section says it (N1 owns and rows (a)-(r) read whole; F7-F9 read whole).

| fork | decided | by | note |
|---|---|---|---|
| F7 | (b) the whole plan is the membership rule on both id roads; N1 row (r) stands | Lead ("решила сама") | membership is data; which obligation a test proves is the automator's judgment, judged by the code critic (P17, AR-29) |
| F8 | (a) the finish reads the same word; the passed obligations reach coverage as a named gap under the person's word, never as proven | Lead, by recommendation until the owner's word | goes into the FV1-30a fix round after its code critic (t-499); P13 stays whole, Q2 is not asked |
| F9 | (a) retraction rows beside section 4 of `test_obligation_join.py` | Lead | D4 stays ONE rule |

N1 is dispatched now (independent of F4 and F8). N2 and N3 follow N1; N4 waits for the owner's word on Q1.

## §9. Small technical choices closed by the designer
1. The predicate and the stamp live in `contract.py` (pure data contracts; `manifest_put`, `manifest_from_tests`, `window_record` import
   `contract` at module level, `controller` imports it inside functions — N3 adds one such lazy import in `_s5_v2_collect`;
   `window_record` is kept out of `manifest_put`'s import graph, `manifest_from_tests.py:1700-1701`).
2. `obligation_map` reads all plan rows with last-wins (the finish's current reading), so the finish's verdicts are kept on every input
   with string ids and hashes, the empty map included (`strict=True`); the one named move is E27 (non-string id/hash).
3. `window=False` for `obligation_refs` (instead of a special case in `window_text_fields`) — the carrier states the truth: `build` copies
   refs by itself.
4. The stamp also writes row `obligation_ids` and the row `obligation_hash` (one road writes all derived fields; m3 (b)/(c)).
5. The stamp refusal is not word-passable (a one-line repair with a door; the `obligation-id` word road of `:2408` stays for bindings).
6. Census line for axis 34 (t-2046 census): "`obligation_refs` ids — fragment door for every language; Python marker an authoring form
   (F1 (a)); `_files` picks the Python reader by `.py` suffix (`manifest_from_tests.py:1627`) — queued".
7. (t-496) The null-drop of D7 is applied to the three stamp-written keys and the binding hash alike — the same `_merge_entry` wipe threatens
   each; one rule, not one per key.
8. (t-496) `obligation_ids` is compared as a SET (the finish's reading `:7319`); the stored order is the refs' order. A row that sends
   `obligation_ids` without refs is not judged by the stamp (today's behaviour; a code writer renaming ids on a refs-less row keeps working).
9. (t-496) The unreadable-plan note is passed through a `notes` list argument of `plan_obligation_map` (the package's pattern, e.g.
   `manifest_from_tests._form_after_write(..., notes)`), printed by `manifest_put.run` on stderr as `manifest_put: note: ...`.
10. (t-496) `_forwardable` lives in `migrate_artifacts.py` (the only code writer that forwards stored rows, per the Grep of §6 Crossings);
    it drops `obligation_ids` only on a row that carries `obligation_refs` (choice 8 keeps refs-less id rows untouched by the stamp).
11. (t-496) The ORIGIN entry `obligation_hash` (`window_record.py:142-143`) changes with its two siblings — same block, same wrong claim
    (sweep-the-artifact-first).
12. (t-496) Stamp problems in `manifest_from_tests.build` (impossible for marker ids `Story.obligation` accepted, both read one map) are
    printed and nothing is written, the exit of a refused marker.

## §10. Reading trail
Read (whole or the ranges named): finding `20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md` (whole); `batch-1-live-run-fvf.md`
(Grep `FV1-19`: `:58, :75-76, :84`); `t-181-exit-go-on-diagnosis.md` (whole); `20261113-told-before-work-mechanism-spec.md:360-405`, §5.4 rows
via Grep (`:525-563`); `20261113-p1-specs-amendment-owner-words.md:261-420, :875-916`; Grep `FV1-19` over `docs\tasks\specs` (p1a `:427,
:640`; plan `:59, :219, :324`; p1b `:87, :939`). PKG: `manifest_from_tests.py:1-135, 295-394, 660-769, 1122-1546, 1600-1799` + Grep defs;
`window_record.py:125-364, 1285-1354` + Grep; `s5_precheck.py:3760-3900, 4505-4544` + Grep; `controller.py:7225-7340, 2251-2259`;
`manifest_put.py:590-622, 821-860, 1021-1055, 1925-1945, 2353-2482` + Grep defs; `coverage_contract.py:255-285, 560-594`; `contract.py:5170-5226`
+ Grep; `event_store.py:106-108`; `driver_dispatch.py:3525-3863`; `driver_conductor.py:602-691`; `test_source.py:100-359`;
`references\detectors.json:85-371`; `test-layers.json` (keep rows named in §6); `plans\builder-rules.md` 7b; `docs\SIBLING_MAP.md` headings;
`DECISIONS.md` (Grep D-0041, obligation, marker); `docs\DECISIONS_ARCHIVE.md` (Grep obligation, marker, D-0041). Fixtures:
`local1-playwright\add-to-cart.spec.ts` (whole), `manifest-run3.json` (Grep), `cart-1\work\frag-s5-7.json` (whole), `cart-1\work\automation-manifest.json`
(Grep), `cart-1\work\briefs` (Grep).
Fix round t-496 (read-main unless named): critic verdict `docs\tasks\specs\reviews\20261113-fv1-19-plan-critic.md` (whole);
`agents\qa-automator.md:60-74`; `window_record.py:125-149, 158-250, 1296-1313`; `manifest_put.py:590-623, 1110-1145, 1380-1391, 2400-2435`;
`detector_verdict.py:63` (Grep), `:471-504`; `controller.py:7286-7325`; `migrate_artifacts.py:85-113, 166` (Grep), `196-415`;
`manifest_from_tests.py:740-760, 1455-1468, 1692-1723`; `probe_by_code.py:2844-2859`; `brief_pack.py:215-230, 1998-2013`; `contract.py:5176-5225`;
`skills\qa-story\phases\s5.md:290-301` + Grep; `references\role-load.json` (whole); `tests\test_manifest_from_tests.py:1830-1855`;
`tests\test_obligation_join.py:150-259` + Grep; `tests\test-layers.json` (Grep `migrate_artifacts` → `:808` test_console_encoding,
`:3355` test_obligation_join, `:4589` test_runtime_paths; section starts `:35` keep, `:6992` pin_holds, `:6998` cohorts, `:7046` quarantine;
`test_case_id_form_sites.py` `:7332` and `test_story_resume_migration.py` `:9950` in quarantine; `test_role_load.py` `:4512` keep); Grep
`process_ratchet_tokens` over `scripts\` (`role_load.py`, `audit_factory.py`, `tests\test_role_load.py`); `docs\SIBLING_MAP.md:24-33, 452-454`
(axis 1, axis 28); `20261113-p1a-writer-reader-round-spec.md` (Grep FV1-19/known_red/N-headings: `:226`, `:427`, `:446-461`, `:527-551`, `:640`);
`20261113-p1v-run-scoreboard-spec.md:436-453`; Grep -i `migrate_artifacts|test_obligation_join` over `docs\tasks\specs\20261113-*.md` (only this
spec and its review; control: finds this spec's own `:54` line); Grep `row_field_lines` over the same (T3b in `told-before-work`, `fv1-4`).
Searched and not found (with positive controls): obligation id in TS/Java/C# fixture test text (§2; control: `annotation` hits); a per-ref
hash check in `manifest_put` (control: the same Grep finds `:611`); `def exit_limit` outside `driver_dispatch.py` (control: finds its three
defs); a decision on markers/`obligation_refs` in `DECISIONS.md` / `DECISIONS_ARCHIVE.md` (case-insensitive; control: `obligation` finds
`DECISIONS_ARCHIVE.md:49`); a keep-file judge of `_retract_case_ghosts` / `_retract_legacy_selector_rows` (Grep over `scripts\tests`: only the two
quarantined files; control: the same Grep shape finds `test_obligation_join.py:244` for `_rename_legacy_obligations`).
Not read (needed beyond the manifest, for the Lead/builder): `judgment-census.json` vocabulary (§4.2 class word); `exit_gate.word_class` /
`detector_verdict` record attributes N4 counts (t-181 trail: `exit_gate.py:1748-1749`, `detector_verdict.py:321-322`); `role_load.py` body
(how the A22 delta is printed — the builder reads it); FV1-30a's word reader internals (F8 (a) implementation is FV1-30a's).
