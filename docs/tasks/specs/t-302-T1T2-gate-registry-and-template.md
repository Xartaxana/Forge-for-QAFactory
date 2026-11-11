# t-302 T1 + T2 — the gate registry with audit A26, then `gate_template.acceptable()` at the literal verdict sites (node spec)

The Lead's decisions over the designer draft t-339 (opus, 02.10 21:10). **The body is the draft, read whole:**
[drafts/t-302-T1T2-gate-registry-and-template.designer-draft.md](drafts/t-302-T1T2-gate-registry-and-template.designer-draft.md)
(§0 ground G1–G11, §1 the two dispatches with owns and sequencing, §2 `references/gate-registry.json`, §3 A26 =
`scripts/gate_registry.py --check|--sites|--json`, §4 `gate_template.py`'s API, §5 keys with negative controls, §6
edges, §7 live proof, §8 four questions, §9 FR walk, §10 forks, the small choices S1–S10, the integration list, the
analogs, the trail). The small choices stand.

Sequencing: **T1 after t-336 (N1a) is accepted** (Q2-A: it owns the `CLI_SCRIPTS` line); **T2 after t-300 N2 and N3**
(Q1-A: every site is then already on `acceptable_provenance` and the image-identity path is gone — the brief's "after
t-336" was the dispatcher's defect). Before T1 the Lead opens the ~7 backlog rows the registry's `debt_ref` needs
(Q9-A: G6, G8, G13, G15, G16, the F9 reporter rehearsal, `s5_stand_limits`).

## §0. Forks — decided by the Lead

| Q | decision |
|---|---|
| Q1 | **A** — T2 after t-300 N2/N3 (one change of meaning per node; no forbidden `unknown:image` token). |
| Q2 | **A** — T1 after t-336; T1 owns the `CLI_SCRIPTS` line. |
| Q3 | **A** — A26 scans `anchor_words` package-wide + each gate's full `words` inside its registered sites + `allow` entries for non-acceptance comparisons; the stated blind spot (a gate comparing only non-anchor words outside any registered site) is in A26's scope text. |
| Q4 | **A** — T2's library is `CLASSES`, `classify`, `acceptable`, `refusal`; the policy-registry helpers are extracted at T6 (the real second user). |
| Q5 | **A** — `gate_preflight._derive_probe` is a registered `dispatch` site of `stand_identity`, unchanged; N3 reshapes it. |
| Q6 | **A** — `source_preflight.assess_freshness`: an `exempt` row + a backlog line to delete or wire it. |
| Q7 | **A with C's compatibility clause** — `accepts` is a consumer id resolved in the registry (`<gate>.<consumer>`, S10); the token form stays only inside `acceptable_provenance` for K27. |
| Q8 | **A** — `promotable` = whether a person's word may lift this gate's unknown into `person_confirmed`; `false` forbids the token in every `accepts` (the baseline refuses it, t-300 §4). |
| Q9 | **A** — `debt_ref` matches `^B-\d{3}$` only; the Lead opens the missing rows before T1. |
| Q10 | **D (Identity and evidence)** — FR-59 is free today (G1); R-4 takes the next id if it lands first. |

Brief defects (dispatcher, for calibration): "T2 after t-336" (Q1); `promotable` named in the brief with no carrier
(Q8); the brief did not say that A26 must stay OUT of `audit_factory.main()` (the project doctor) — the draft read
it from t-305 Q6(c)/t-313 F9 and put the check in `gate_registry.py --check` under selftest `--contracts`.

## §1. What the Lead adds

- Integration owed by the Lead at T1: the FR-59 text in section D + the index regeneration (a mechanism commit with
  the tier line); the debt lines; the ~7 backlog rows; the `--contracts` selftest hunk naming
  `test_gate_registry.py` next to `test_null_outcomes.py`; `plans/features.json` for the four new files; the
  SIBLING_MAP axis-5 row; CHANGELOG lines; a builder-rules 7 line naming `test_gate_registry.py`.
- Analogs → backlog at T1: `metrics_projection` :355 produces the C03 word from a match list (a `produce` site);
  `execution_request` :145 validates a dead data-seed field (already queued by R-2); A26's twin of A24's limit (a second
  comparison inside an `allow`-prefixed line is not caught).
- T2's reconcile list (from t-356/t-359): `provenance.rehearsal` [matched, person_confirmed] vs the three live rehearsal
  token sets — `execution_request.rehearsal_probe` (matched + no_changed_file), `gate_preflight._observed_identity`
  (matched + person_confirmed), `story_run.build_outcome` via `profile_contract.ACCEPTS` (matched, person_confirmed,
  not_applicable:no_changed_file) — ONE set, in data (B-291 д); the `allow` entries of S5 (`coverage_contract` :680 vs
  :685 are the identical text — `allow` matches the WHOLE comparison exactly, never a prefix: t-360 lands the exact
  match in T1, T2 fills the entries); the non-anchor provenance comparisons of B-291 (б).

## §2. Critic t-359 (opus, 03.10 05:0x) over builder t-356 — FIT WITH FIXES; the Lead's decisions → fix pass t-360

The report verbatim: [reports/t-359-critic-t-356.md](reports/t-359-critic-t-356.md); the builder's report
[reports/t-356-builder-report.md](reports/t-356-builder-report.md). D1–D13 all FIT (D9 with F4; D10 vacuous by F1).

| F | decision |
|---|---|
| F1 | **Re-home the consumers:** `provenance.baseline` → row `baseline_identity`, `provenance.environment_preparation` → row `environment_preparation` (their `promotable: false` then guards them); `_check_registry` ALSO applies the promotable value of the row named by a consumer's `<gate>` prefix when the consumer sits elsewhere (belt and braces: a consumer whose prefix names a `promotable: false` row inherits false). Key: adding `person_confirmed` to either consumer on a scratch copy → exactly 1 finding naming the consumer id and the row. |
| F2 | **Suppress a name-bound token set only when EVERY use of the name is inside a comparison;** any other use (a call argument, a return value, an attribute) reports the set at its binding line as an unregistered vocabulary. Then `profile_contract.py:<module>` (`ACCEPTS`, `PROVENANCE_RESULTS` if it trips) is registered as `vocabulary` under `provenance_acceptance`, as the draft §2 says — the registry gains the rows, `--check` stays green. Key: the critic's F2 probe (a set used as an argument, no comparison) → 1 finding; the live tree after registration → 0. |
| F3 | **Exact match now, in T1:** an `allow` entry matches the whole comparison text (the `ast.unparse` form, `"`→`'`), never a prefix; a prefix entry is a registry finding ("allow must be the whole comparison"). Key: the prefix `rec['result'] ==` whitelists nothing (1 finding); the exact text whitelists exactly its line. T2 fills S5's entries (D12). |
| F4 | **A per-row key `vocabulary: "target" \| "code"`** (data): `target` = the row's words are the class words standing in for the gate's own; `code` = the gate's real words. `_check_registry`: a `converted` row must say `code`; a `debt`/`exempt` row may say either. Key: flipping a `target` row to `converted` → a finding naming the row and the key. |
| F5 | The five missed forms (+ `.get` by a word key, comprehension filters, `not in`) named in the docstring's "Invisible to it" list, one line each; no scanner change (the detector for them is the per-gate behaviour test, Q8-C; B-291 а). |
| F6 | `--sites` prints `<row id> NOT ALLOWED` for a registered converted accept site outside its allow list; `UNREGISTERED` only for a site in no row. Key: one line each form. |
| F7 | Lead: the reconcile list above (§1). |
| F8 | Lead: B-290 opened; t-360 puts `B-290` into `source_freshness.exempt_reason` in place of "backlog line is pending". |
| K-T1.14 | The `--json` document is compared against a shape built INDEPENDENTLY from the registry file (row count by status, the debt ids, the exempt ids) — not the same code path twice. FR-45: the "writes nothing" check becomes a before/after hash of the package tree's mtimes/sizes over a `--check` run on a scratch copy (or the test asserts no `open(..., "w")`/`write_text` by AST over `gate_registry.py`, named as the weaker form). |

Dispatcher defects (calibration): the `promotable` consumer placement was decided in the draft row text (D6) without a
probe; the `allow` prefix semantics came from A24's shape without asking what a prefix can whitelist.

  T2 gets a critic-on-plan when its turn comes (after N2/N3 — the sites' meaning may have moved by then).
