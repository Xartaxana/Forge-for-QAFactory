# t-922 — critic on builder diff t-916 (Architect spec, Stream A: ladder home + tier gate + savings)

Diff: commit c61bcd4e, branch `worktree-agent-ae7f47813d0989cf3`, `git diff origin/main...HEAD` (merge base 3181a91f).
Spec/DoD: `docs/tasks/specs/20261116-architect-tier-spec.md` §0, §2, §3.4, §4.5 step 5, §7 Stream A (A1-A6).

## Verdict

**NEEDS WORK (fit_with_fixes): 1 blocking finding (F1), 7 non-blocking fixes (F2-F8).** No REJECT: the empirics gate
(key 1) passes on every control value in both worlds. Under today's config the gate's verdict matches the old gate on
every spec row. The core design (one matcher, stdlib-only leaf, lazy yaml, alias-rejecting loader) is sound. Whether
to accept stays with the Lead (rule 6).

## Key 1: empirics first (the gate)

I loaded the new gate and tier_ladder from the worktree, and the OLD gate from merge base 3181a91f (`git show` into
the scratchpad), and ran `tier_declared_ok(d, resolve_lead_binding(cfg), cfg)` on each. TODAY = the worktree's real
`delegation.config.yaml`. AFTER = the same file with lead set to claude-opus-5-5 and an `architect: claude-fable-5-1`
rung added.

| config | tier | expected | new | old |
|---|---|---|---|---|
| TODAY | fable | ok | True | True |
| TODAY | claude-fable-5-2 | ok | True | True |
| TODAY | opus | REFUSED | False | False |
| TODAY | claude-opus-5-5 | refused | False | False |
| TODAY | sonnet / haiku | refused | False / False | False / False |
| TODAY + architect key (fable) | fable / opus | ok / refused | True / False | True / False |
| AFTER | opus | ok | True | True |
| AFTER | claude-opus-5-5 | ok | True | True |
| AFTER | fable / claude-fable-5-2 | ok | True / True | True / True |
| AFTER | sonnet / haiku | refused | False / False | False / False |
| AFTER, no architect key | fable / opus / sonnet | ok / ok / refused | True / True / False | same |
| missing (None) / empty | fable / opus / sonnet | ok / refused / refused | True / False / False | same |
| oversize (64 KB + 1) | fable / opus | default: ok / refused | True / False | same |
| alias bomb | fable / opus | default: ok / refused | True / False | same |
| broken YAML | fable / opus | default: ok / refused | True / False | same |
| `reserve:` uncommented | fable / opus | ok / refused | True / False | same |
| pyyaml missing (`sys.modules["yaml"]=None`) | fable / opus | default: ok / refused | True / False | (old: ImportError at import = every commit blocked) |
| no lead, architect=opus | opus / claude-opus-5-5 | refused | False / False | False / False |

Fallback notes from `effective_bindings` (measured): `config absent`, `config is over 64 KB`, `config is not readable
YAML (a YAML alias or anchor is not allowed)`, `config is not readable YAML (while parsing a block mapping)`,
`pyyaml is not installed`, `roles.reserve is not read: rename it to roles.architect`. More malformed inputs, all fall
back to the defaults: `!!python/object/apply` (constructor error), 5000-deep `[` (RecursionError caught), `roles: [..]`,
a top-level list, `lead: <scalar>`. The size boundary: exactly 65536 bytes is parsed, 65537 gives the default. The
gate module no longer imports yaml (`'yaml' in sys.modules` → False after `import mechanism_gate`).

Where the verdict differs from the old gate (none is in a spec row; each is named here):
- `tier: mythos` under TODAY now **passes** (old: refused). This comes from the spec's `ALIASES = {"mythos": "fable"}`
  in `family_of`. It is a data-row loosening the spec mandates, not a defect.
- `tier: opus, fable` under TODAY is now refused (old: passed): `family_of` takes the weakest family first. This is
  stricter.
- lead=sonnet, critic=opus, `tier: opus` is now refused (old: passed via family-above). By spec case (b) the family is
  bound to critic. Stricter.
- critic=fable, lead=opus, `tier: fable` is now refused (old: passed). This is the §2.2 row ("resolves to critic
  rank"). Stricter.
- A non-Claude lead with critic and architect both on opus: `tier: opus` now passes. This is deviation (i), see key 2.

**The one miss — F1 (BLOCKING).** With the fallback, the gate prints no WARN and no note anywhere. Spec §2.4: "the tier
gate's refusal text (if it refuses) carries the same note". Measured:
`decide_full("...tier: opus", ..., config_text=<lead=claude-opus-5-5 + broken line>)` →
`Not lead tier: "tier: opus" does not match the binding (fable) -- ...`. Same for the oversize config. The operator
bound opus. The refusal names a binding "fable" that appears nowhere in their file, and it does not say the config was
unreadable. That breaks FR-1 (say what is wrong) and the spec edge. After stream L, any YAML slip makes every Opus
mechanism commit refused with a misleading reason.

## Key 2: the builder's deviations

- (i) Ambiguous family by max rank: **accept.** It does NOT open today's config: TODAY `opus` → False, and TODAY +
  architect key `opus` → False (table above). The loosening can only change a verdict when ≥2 rungs share a family AND
  the lead is non-Claude. With a Claude lead, `_usable` drops any rung above lead that is bound weaker than lead. A
  same-family rung above lead is then at least lead's family, which passes anyway. The spec's (b) wording ("the max
  rank of the functions bound to that family") mandates it.
- (ii) `effective_bindings` falls back to the defaults when no lead is bound: **accept** (stricter only). Measured: no
  lead + architect=opus gives `opus` False. Old behaviour (`no_lead_reserve_opus`) is kept. Side effect, F3:
  `function_of_session` then says "config unreadable", which is false.
- (iii) Savings reads `bindings()`, not `lead_binding()`: **accept.** `lead_binding()` would never be empty, so the
  FR-41 PricesError rows could not hold. Two consequences: F4 (the error text gives the wrong reason) and a spec text
  residual (key 3).

## Key 3: A3 absent config vs FR-41

**I confirm the Lead's reading: keep PricesError.** A counterfactual priced at a model the config never named is an
unknown reported as a fact (FR-41). It is also a money figure that is not true (P18). The tier_ladder defaults exist so
that a gate fails closed. A savings figure is not a gate, and the "stricter is safe" argument does not carry over to
money. The spec text must follow: §7 A3 (lines 695-696, "NO — absent config gives DEFAULT_BINDINGS lead = fable …
(row)") and the §2.2 sentence "EVERY reader below goes through this one function" both need a carve-out for the savings
reader. That spec edit is the Lead's own (F8).

## Key 4: lost coverage in `test_mechanism_gate.py`

I listed 47 deleted tests and 13 deleted fixtures (`git diff ... | grep '^-def test_'`) and mapped each one:
- `tier_declared_ok_exact_and_family_vs_non_claude` → `fable-lead` / `non-claude-lead` rows. Still judged.
- `build_role_ladder_fixed_order_and_ranks` → `test_bindings_table` today/after plus the `test_rank_of_model_table`
  TODAY rows. Still judged.
- `build_role_ladder_empty_without_config` → bindings `none` / `empty`. Still judged.
- **`build_role_ladder_ignores_judge_and_analyst`, `build_role_ladder_ignores_designer` → LOST.** The only remaining
  check is a pin on the constant `COORDINATION_FUNCTIONS` (`test_families_...:167-168`). No config with
  `judge:` / `analyst:` / `designer:` keys is parsed anywhere. Two silent bugs would survive: a refactor that iterates
  `roles.items()`, or `designer` added to the tuple. Then `designer: claude-fable-x` would rank (F5).
- **`build_role_ladder_role_without_model_no_rung` → partly LOST.** The old case was a rung key present with an empty
  model, beside a bound lead. The nearest rows are `api-fallback` and `non-string-model`. Neither shows that an empty
  `architect:` beside a bound lead yields no architect rung. That is exactly the state an operator creates while
  editing the AFTER config (F5).
- The non-Claude ladder rows (exact id passes, lower rung fails) → `non-claude-ladder` rows in both tables. Still
  judged.
- The reserve rows (exact id or family at a non-Claude lead, real shape opus+fable) → `non-claude-lead-architect-fable`
  and `opus-lead-architect-fable`. Still judged.
- `no_reserve_tier_fable_still_passes`, `family_above_binding_passes` → `opus-lead` fable. Still judged.
- `family_below_binding_fails` → `opus-lead` sonnet. Still judged.
- `fable_binding_nothing_above_regression_pin` → `fable-lead` opus, `none` opus. Still judged.
- `non_claude_binding_unaffected...`, `non_claude_declaration_does_not_match_higher_family` → `non-claude-lead` fable,
  `opus-lead` llama. Still judged.
- The four `decide_full_lead_binding_*` and the two `decide_full_ladder_*` → `test_decide_full_tier_line_table`. Still
  judged.
- `ambiguous_family_match_does_not_resolve` → the expectation flips, named in the handoff (key 2 (i)).
- `no_config_regression_pin_explicit_none` → `none` rows. Still judged.
- The nonsense reserve below lead rows (3) → `architect-below-lead` plus `ARCHITECT_WEAKER`. Still judged.
- The no-lead reserve opus rows (3) → `no-lead-architect-opus` plus `LEAD_MISSING`. Still judged.
- The exact weaker / stronger / non-Claude step rows (6) → `architect-below-lead`, `architect-above-sonnet-lead`,
  `architect-non-claude-step`, `ARCHITECT_NON_CLAUDE`. Still judged.
- The duplicate model id rows (3) → `duplicate-model-id` in both tables. Still judged.

The handoff's list is complete except that it calls judge/analyst/designer "covered", and they are not.

Killing power: the row `("lead-equals-critic-opus", "claude-opus-5-5", True)` (test_mechanism_gate.py:655) passes on
the `declared == binding` first pass. It would stay green if max-rank broke (F6). Max rank is still judged in
`test_rank_of_model_table` (`OPUS`, AFTER → 3).

## Key 5: one road (axis 34), class completeness

I grepped `tools/*.py` case-insensitively for
`ROLE_RANKS|LEAD_FAMILIES|TIER_ORDER|FAMILY_ORDER|KNOWN_TIER_WORDS|_FAMILY_NAMES|_MODEL_TIER_SUBSTRINGS|AGENT_TIER|_UNBOUND`
plus literal family tuples. Positive control: the same call finds `tier_ladder.py:21 FAMILIES`. What remains, and
which stream owns it:
- `journal_validator.py:345-346, 678-762` `TIER_ORDER` / `AGENT_TIER` → **B**.
- `agents_md.py:199-260` (AST of `TIER_ORDER`) and `test_agents_md.py` → **B** (B7).
- `session_context.py:221, 1000` `_MODEL_TIER_SUBSTRINGS` → **C**.
- `tier_echo.py:126` `KNOWN_TIER_WORDS` → **D**.
- `dispatch_gate.py:1039-1180` `_FAMILY_NAMES` → **D**.
- `journal_hooks.py:210` door literal → **D**.
- `token_usage_stats.py:119, 172` → **D**.
- `journal_echo.py` reads through tier_echo → unchanged by design (§2.3).
- Prose mentions only, no copies: `dispatch_gate.py:199`, `tier_echo.py:71, 159`.

Every reader has an owning stream: **no orphan**. The second parser of `roles.lead` is gone: `grep 'get\("roles"\)'`
finds only `tier_ladder.py:97`. Importers of the removed names: none outside the gate and its test (grep over the
worktree; `test_streams.py` copies the gate as text for an AST census and does not import it). `tier_ladder.py` imports
only `__future__` at module level; `yaml` is loaded inside `bindings()` (subprocess test plus my probe).
Axis 1 (binding ↔ policy): the CLAUDE.md text belongs to stream L. Covered by the spec's ordering.

## Key 6: standing questions

1. **Fit to the spec:** A1-A6 are implemented, except the §2.4 note in the tier-gate refusal (F1).
2. **The builder's own decisions:** deviations (i)-(iii) are safe (key 2). Deviation 3 moves the guard to rungs above
   lead only; it gives the §2.2 rows correctly (`CRITIC_ON_FABLE`). Deviation 4 (non-Claude lead, family declared →
   None) errs downward. Deviation 5 (no header line for `--list`) is fine.
3. **Seams:** `resolve_lead_binding` / `lead_family` are kept as wrappers. `savings_report` no longer imports the gate
   (this also drops the gate's former top-level pyyaml import from the savings path). The new prefix entries are
   additive.
4. **Class completeness:** key 5. In the same artifact, F3 and F4 are the same class as F1: a fallback road drops the
   reason note. Every caller of `bindings()` / `effective_bindings()` in this diff was swept: the gate (F1),
   `function_of_session` (F3), `savings_report` (F4).
5. **Tests:** the tables are one test per behaviour, with param ids. The adversarial battery on the config (outside
   input) covers magnitude (64 KB at the limit and beyond), nesting (alias bomb; deep nesting measured by me, no row),
   encoding (a BOM parses; no row) and broken / empty input. Volume: `tools/test_volume.py` rules (docs/ excluded)
   give +349 test lines vs +305 product lines, and the commit message carries **no `tests-over:` line**. Net, the test
   files shrink by 122 lines. The reason (one new file sanctioned by the owner's word P34, plus 40 single-assert tests
   folded into tables) holds, but it must be written (F7). Lost rows: F5. Weak row: F6.
6. **DUPLICATION AND CONSISTENCY:** none found beyond what the spec queues. I grepped for a second roles parser
   (`get("roles")`, `delegation.config`), family tuples, and sha regexes (`[0-9a-f]{7,40}` appears in `piles.py` in
   other grammars; a one-line regex in a different context, not a shared reader). The clone ratchet is read from the
   branch's forge-check, not re-run (not attached; batch level).
7. **CODE QUALITY:** no new function is over 60 lines or nested more than 3 levels deep (`bindings` 71-108,
   `_resolve` 139-167, `list_commits` 932-962). Two names do not tell the truth: the note `"config unreadable"` for a
   readable config (F3), and the PricesError reason (F4). Refusal texts: the `--list` bad-value text names both forms
   (good). For an 8-digit value like `20261116`, `--list --since` treats it as a sha (all hex). Git then fails with
   `bad revision`, and the message names no form (F2b). The tier refusal says "does not match the binding" but does
   not say what passes (lead binding or a model ranked lead or above) (F2a).
8. **Hygiene:** not a package diff; FR does not apply; ASCII.
9. **Ratchets:** none touched.
10. **Architecture:** not a package diff. No AR-n is owed (spec §1).
11. **Judgment:** none moved. The gate judges the shape of the `tier:` line; its truth stays with calibration.
12. **One road:** the ladder has one home, with readers queued by stream (key 5). The savings carve-out from
    `effective_bindings` is a money-vs-gate difference with a stated reason (FR-41), not an exclusion of a case. The
    spec text must say so (F8). Language/project exclusions: none found (grep of the diff for language or runner
    names: none).

## Findings and fixes (all in this node's fix round)

- **F1 (BLOCKS the merge)** `tools/mechanism_gate.py:770-786` (`decide_full`). When
  `tier_ladder.effective_bindings(config_text)[1]` is not None, append it to BOTH refusal texts ("No tier line" and
  "Not lead tier") in the spec §2.4 form, e.g. ` (delegation.config.yaml unreadable: <note> -- default bindings,
  lead=fable, used; fix the file)`. Add a `test_decide_full_tier_line_table` row: broken-YAML config binding opus +
  `tier: opus` → code 1 and the fragment "not readable YAML". Add one more row for the oversize config.
- **F2a** `mechanism_gate.py:783-785`: the refusal says what was expected: "expected the lead binding (<b>) or a model
  ranked lead or above on tools/tier_ladder.py".
- **F2b** `mechanism_gate.py:903-904`: in sha mode, a git failure appends "(a value of 7-40 hex digits is read as a
  commit sha; a date is YYYY-MM-DD)". Add a row: `20261116` with a failing runner → the hint is present.
- **F3** `tools/tier_ladder.py:200-201`: when the defaults are used, return the real note (e.g.
  `"config unreadable: default bindings (roles.lead names no model)"`) instead of a fixed string that is false for a
  readable config with no lead. Adjust the `test_function_of_session_table` rows and add a `LEAD_MISSING` row.
- **F4** `tools/savings_report.py:133-136`: call `found, note = tier_ladder.bindings(text)`. When there is no lead,
  the PricesError names `note` when present (oversize / alias / not readable YAML / pyyaml missing), and keeps "roles.lead
  names no model" only when that is the actual reason. Add a row to the existing PricesError table: alias-bomb config →
  the message contains "alias".
- **F5** `tools/test_tier_ladder.py:97-106` (`test_bindings_table`): add rows (a) a config with `judge:`, `analyst:`,
  `designer:` (designer on a fable id) beside today's roles → `found` holds no such key, and `rank_of_model` of the
  designer id is None; (b) `architect:` present with an empty model beside a bound lead → no `architect` in `found`.
- **F6** `tools/test_mechanism_gate.py:655`: declare `"opus"` (the family word) instead of the exact binding, so the row
  goes through the max-rank road.
- **F7** commit message: add `tests-over: one new test file by the owner's word (P34); 40 single-assert tests folded
  into tables; net test lines -122`. The Lead's commit or amend carries it.
- **F8 (Lead's spec edit, not the builder's)** `docs/tasks/specs/20261116-architect-tier-spec.md:695-696` (A3) and §2.2
  "EVERY reader below goes through this one function": state that the savings counterfactual reads `bindings()` and
  that an absent or unreadable config is a PricesError (FR-41).

## Spot-checks (claims verified)

- Witness "715 passed": re-run reproduced it (below).
- "the old ladder carriers are gone": grep shows `ROLE_RANKS` / `LEAD_FAMILIES` only in the gone-test, and no importer
  elsewhere (positive control: the same grep finds the test line).
- "tier_ladder stdlib only": `grep '^import\|^from'` → only `__future__`. Probe: `import mechanism_gate` loads no yaml.
- "behaviour identical under today's config": table above, compared with the merge-base gate.
- Handoff "no change needed to test_mechanism_gate_md.py": its loader uses the sibling copy if present, else the live
  file. No `tools/mechanism_gate_md.py` exists (ls). Green in the re-run.

## Trail

- Read: the spec §0-§3.4, §4.5, §6, §7 (lines 16-355, 432-460, 582-806); the handoff; the brief; `tools/tier_ladder.py`
  (whole); the `tools/mechanism_gate.py` diff plus lines 600-650, 750-860, 985-1010; `tools/savings_report.py` diff;
  `tools/test_tier_ladder.py` (whole); `tools/test_mechanism_gate.py` 100-125, 590-760, 1370-1410; the deleted bodies
  at 3181a91f (604-725); `tools/test_mechanism_gate_md.py` 60-100; `tools/test_streams.py` 236-325;
  `tools/test_volume.py` 1-40; `docs/TESTING.md` «Бюджет»; the worktree's `delegation.config.yaml`.
- `( cd <worktree> && python -m pytest tools/test_tier_ladder.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q -p no:cacheprovider )`
  → `715 passed in 6.84s`.
- Probe (python stdin, new gate vs `git show 3181a91f:tools/mechanism_gate.py`): the table in key 1. The `decide_full`
  broken / oversize probe → `Not lead tier: "tier: opus" does not match the binding (fable) -- ...` with no note.
- `git diff origin/main...HEAD --numstat` → tier_ladder 208, mechanism_gate +88/-229, savings +9/-10, tests
  +180 / +153-471 / +16.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 tools/mechanism_gate.py:770-786 decide_full: on a broken/oversize/aliased/no-pyyaml config the tier refusal names binding (fable) with no note; spec 2.4 requires the effective_bindings note in the refusal text (measured: broken config binding opus + tier: opus -> 'does not match the binding (fable)' and nothing else)"
  ],
  "class_completeness": "No second ladder copy is left without an owner: journal_validator/agents_md -> B, session_context -> C, tier_echo/dispatch_gate/journal_hooks/token_usage_stats -> D; journal_echo reads through tier_echo. One roles parser left (tier_ladder.py:97). The same class as F1 (a fallback road drops the reason note) is swept in this diff: function_of_session (F3) and savings_report (F4).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-architect-tier-spec.md (16-355, 432-460, 582-806)",
      ".claude/worktrees/agent-ae7f47813d0989cf3/docs/tasks/handoffs/t-916-architect-stream-a.md",
      "docs/tasks/critic-diff-brief.md",
      "tools/tier_ladder.py (worktree, whole)",
      "tools/mechanism_gate.py (worktree diff, 600-650, 750-860, 985-1010)",
      "tools/savings_report.py (worktree diff)",
      "tools/test_tier_ladder.py (worktree, whole)",
      "tools/test_mechanism_gate.py (worktree 100-125, 590-760, 1370-1410; 3181a91f 604-725)",
      "tools/test_mechanism_gate_md.py 60-100",
      "tools/test_streams.py 236-325",
      "tools/test_volume.py 1-40",
      "docs/TESTING.md Budget section",
      "delegation.config.yaml (worktree)"
    ],
    "reruns": [
      {
        "command": "( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-ae7f47813d0989cf3 && python -m pytest tools/test_tier_ladder.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q -p no:cacheprovider )",
        "result": "715 passed in 6.84s"
      },
      {
        "command": "python stdin probe: tier_declared_ok on new worktree gate vs merge-base 3181a91f gate over TODAY/AFTER/no-architect/missing/empty/oversize/alias-bomb/broken/reserve/no-pyyaml configs",
        "result": "all spec rows match expected (TODAY: fable ok, claude-fable-5-2 ok, opus refused, sonnet refused; AFTER: opus ok, claude-opus-5-5 ok, fable ok, sonnet refused; bad configs -> default bindings); diffs vs old gate: mythos now passes (spec alias), 'opus, fable' / lead-sonnet opus / critic-fable fable now refused (stricter), ambiguous non-Claude-lead opus now passes (deviation i)"
      },
      {
        "command": "python stdin probe: decide_full with broken and oversize config binding opus, tier: opus",
        "result": "code 1, 'Not lead tier: \"tier: opus\" does not match the binding (fable) -- ...' with no config note"
      }
    ]
  },
  "fixes": [
    "F1 tools/mechanism_gate.py:770-786: append the effective_bindings note to both tier refusals; rows for broken and oversize config (blocks merge)",
    "F2a tools/mechanism_gate.py:783-785: the refusal states what passes (lead binding or a model ranked lead or above)",
    "F2b tools/mechanism_gate.py:903-904: on a git failure in sha mode, hint that 7-40 hex is read as a sha and a date is YYYY-MM-DD; row with 20261116",
    "F3 tools/tier_ladder.py:200-201: function_of_session returns the real default-bindings note, not a fixed 'config unreadable' for a readable config with no lead; LEAD_MISSING row",
    "F4 tools/savings_report.py:133-136: PricesError names the bindings() note (oversize/alias/unreadable/pyyaml) instead of always 'roles.lead names no model'; alias-bomb row",
    "F5 tools/test_tier_ladder.py:97-106: bindings rows for judge/analyst/designer keys not read, and for an empty architect model beside a bound lead (lost behaviours of the deleted build_role_ladder tests)",
    "F6 tools/test_mechanism_gate.py:655: declare 'opus' so the row goes through the max-rank road, not the exact-binding first pass",
    "F7 commit message: add a tests-over line (+349 test vs +305 product by test_volume rules; net test lines -122; one new file by P34)",
    "F8 Lead's spec edit: 20261116-architect-tier-spec.md:695-696 (A3) and section 2.2 'EVERY reader': savings reads bindings() and an absent config is a PricesError (FR-41)"
  ]
}
```
