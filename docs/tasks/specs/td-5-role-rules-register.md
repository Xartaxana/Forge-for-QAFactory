# TD-5 — one register of mandatory role rules instead of role-text pins

Status: Revision 2 (designer, t-2262, 10.11.2026), after the critic-on-plan review t-2257
(`docs/tasks/specs/reviews/td-5-plan-critic.md`, ACCEPT WITH FIXES). Every fork is decided by the Lead (§8). Rule text:
`docs/TESTING.md` «Правила ролей не теряются: один реестр вместо пинов» (lines 66-76); plan: `docs/tasks/test-diet.md` row
TD-5; the owner's word 10.11.2026 (a rule of a role cut to fit a size cap must not be lost silently). Branch:
`experiment/thinking-roles` (main is frozen). Package text is English (FR-30).

## Revision 2 — what changed, per finding

| Finding | Lead decision | Sections changed |
|---|---|---|
| B1 (a)(b) comment stripping vs template guidance | the matcher strips ONLY the package's own marker comments; every other HTML comment is text in every carrier | §2.3, §2.4, §3.2, §3.3 ("only in a marker" replaces "only in a comment"), §6 E-12 rewritten, new E-23 and E-24, §8.3 |
| B1 (c) a key that does not hold today | no row; `red before:` with the old pin's output line; the Lead decides; that pin file stays | §3.5 shipped case, §4.6, §7.1 non-goals, DoD 1-3 |
| B2.1 mixed_then K3a | a row (twin with critic K4 and rubric K1a); every owner-word mention renamed `K3a-sub` | §4.1, §4.4.7, §8 F8 |
| B2.2 blocked_by_env handoff duties | rows for `instance_ids` and `remedy`; the `detail` line is a carrier of the detail row | §4.4.1 |
| B2.3 the critic charter pointer | a twin row: rubric heading + critic pointer | §4.4.1 |
| B2.4 s1 halt on an unresolved conflict | a row, anchor "Halt only on an unresolved conflict" | §4.4.11 |
| B2.5 K14-phase and K6 | K14 is a twin row analyst + s7; K6 dropped because the K5 row holds its rule, not as "single token" | §4.4.2 |
| B3 §4.4 directions | §4.4 is a row table for all ten files, each anchor counted; per-file accounting of every key | §4.4 (whole), §7.1 DoD 1 |
| R1 stale text | decisions written in, F1-B branches deleted, s7 line 145 -> 148, §2.1 states the three carriers already say `design/` | §1.1, §1.2, §2.1, §3.6, §4.3, §6, §8 |
| R2 F8 on the facts | `OWNER_WORD_FA` dropped; F8 reworded on FA-10/FA-11 | §8 F8 |
| R3 retire-line gate | NOT in TD-5.1; a separate last node, forge tool, after the migration waves | §7.4 (new), §6 E-19 |
| R4 `<why>` in refusals | probe order stated | §3.1, §3.3 |
| R5 K-R1-1a partial edit | second row `red-then-read-triage-row` | §4.3 |
| R6 B-K13 | named in the TD-5.1 known-losses list | §4.4.10, §7.1 DoD 8 |
| R7 driver golden | named, not edited | §4.5 |
| Lead decision 8 | `plans/features.json` lists 9 of the 12, named; the other seven registries list none | §4.5 |

## 1. What the change touches

### 1.1 Architecture invariants (AR-n) and the change check each demands (copied into the node DoDs, §7)

| AR | How the change touches it | Change check (goes into the DoD) |
|---|---|---|
| AR-1 closed variety is a data row | The list of mandatory role rules moves out of 12 test files (Python tuples/dicts) into ONE data file with one reader | after the node, no list of role-text keys stays in any of the 12 files (they are deleted, except a file kept under `red before:`/`doubt:`, §7.1); `git -C <wt> grep -n "role-rules.json" -- ai-packages/qa-factory/scripts` names only `role_rules.py`, `selftest.py` (`cmd_limits`) and `test_role_rules.py` |
| AR-13 a fact with a reader is read only through it | The register gets ONE reader `scripts/role_rules.py` (`load`, `findings`); JSON is read through `hooklib.read_json` (axis 16), never a second `json.loads` | `git -C <wt> grep -n -E "json\.loads\|role-rules.json" -- ai-packages/qa-factory/scripts/role_rules.py` shows no `json.loads` (positive control: `git -C <wt> grep -n read_json -- ai-packages/qa-factory/scripts/role_rules.py` finds the call) |
| AR-15 a shared problem has one survivor | 12 private helpers (`key_present` x5, `missing`, `problems_of` x3, `failures`, `absent`, `folded`) collapse into `role_rules.findings` | the helpers leave with their files; no new helper of the same shape appears in a test |
| AR-19 stage twins change together | author/critic twin rules become ONE row with several carriers, all of which must hold it | every twin row of §4.4 carries every carrier listed there |
| AR-23 every required list declares its empty outcome | the register may hold 0 rows | the reader prints `role-rules: 0 rows - no rule of a role is guarded` and passes; an UNREADABLE register is a finding, never 0 rows (§3.4) |
| AR-29 a code check judges data | the new check is a join between the register and package text: presence of a developer-authored anchor in a developer-authored file; it never runs at story time and never reads a role's output | census rows for every check unit of `role_rules.py` (class and owner per §1.3); `test_judgment_census.py` green; commit line `judgment: adds data check role_rules.findings` |
| AR-11 a role gets only the context it needs | the anchor is 2-6 of the rule's own words (F1-A): no byte is added to any delivered text | `role_load.py --all` output unchanged by the node (the node edits no delivered text) |

Not touched, one line each: AR-2 (no open variety judged), AR-14 (the register has one writer: the developer's diff; waves
are sequential, F7), AR-20 (no ratchet added), AR-22 (every row field is read: `rule`/`source` by the refusal text,
`carriers` by the search).

### 1.2 Factory rules (FR) walked

- FR-1 — every finding names what is wrong, what was expected, and the door (§3.3).
- FR-13 — the rules are data; code holds no list of them. The anchor is closed data the developer writes, not a phrase list
  over open variety.
- FR-44 — the register lives in `design/role-rules.json` (F2 decided): nothing loads it at run time,
  `release_fingerprint.py:17` keeps `design/` outside the fingerprint for that reason, and `design/` ships with the release
  copy, so the shipped case runs in the release CI.
- FR-12 — not touched: the check never reads a person's or a role's wording; it reads the package's own source text against
  the package's own register.
- FR-38 — not touched for roles (no role output is judged); the requirement is stated to the BUILDER before the work by
  `plans/builder-rules.md` 7d and by the refusal text.
- FR-30 — the register, reader and test are English; `selftest.py --lang` covers every file of the package, `design/*.json`
  included (`scripts/selftest.py:11`).
- FR-45 — the reader writes nothing.
- FR-54 — siblings by the map: §10 (analogs reported, not widened).

### 1.3 Every check the spec adds: the owner it serves and its census class

| Check (in `scripts/role_rules.py`) | Owner served | Census class |
|---|---|---|
| register readable, an object with `schema_version` 1 and a `rows` list | data (code) | shape |
| row schema (keys, types, id form, anchor 2-6 words, carrier home) | data (code) | shape |
| no duplicate `id`; no duplicate (carrier, folded anchor) across rows | data (code) | xref |
| every carrier path exists and is readable | data (code) | xref |
| the anchor stands exactly once in each carrier, after the package marker comments are removed (§3.2) | data (code) | xref |

Whether a rule SHOULD stay is not code's: retiring it is the person's word (intent) and the critic judges the diff (judgment,
a tier above). The class must not be written as `word-list`: the census ceiling for `word-list` is 0
(`scripts/tests/fixtures/judgment-census.json`, `ratchet`), and this check reads no role's or person's words — it is a join
between two package files. Pointing `role_rules` at a story artifact (a role's output) would make it a word-list check over a
role's wording, a breach of AR-29: `findings` reads only files under the package homes of §2.4. The reader returns strings
and raises nothing, so `refusal_registry.sites` gives it no blocking unit (critic t-2257, Q4).

## 2. The data file

### 2.1 Location

`ai-packages/qa-factory/design/role-rules.json`, written `<REG>` below (F2 decided). The three forge carriers already say
so: `docs/TESTING.md:70`, `docs/tasks/test-diet.md:22`, `plans/builder-rules.md:48` (commit cac99e83d) — no Lead edit of the
path is owed.

### 2.2 Shape

```json
{
  "schema_version": 1,
  "note": "Mandatory rules of role texts (docs/TESTING.md). One row per rule a role must keep. Read only by scripts/role_rules.py. A rule leaves a role text only together with its row, in the same diff, with the word that retires it named.",
  "rows": [
    {
      "id": "case-focus-twin",
      "rule": "A field whose value goes to the server or redraws the page on each key has the Then 'value kept whole, field still in focus'; the case critic never strikes it and flags its absence.",
      "source": "RN1-7; t-1675 K4",
      "carriers": [
        {"file": "agents/qa-case-designer.md", "anchor": "still in focus"},
        {"file": "agents/qa-case-critic.md", "anchor": "still in focus"}
      ]
    }
  ]
}
```

Row keys, exactly these (an unknown key is a finding — it catches `anchors`, `carrier` typos):

| Key | Type | Rule |
|---|---|---|
| `id` | str | `[a-z0-9]+(-[a-z0-9]+)*`, unique in the register |
| `rule` | str | non-empty, one line, at most 300 characters: what the role must do or never do, in plain words. It is printed in the refusal and it is what the critic reads when an anchor is re-pointed |
| `source` | str | non-empty: the owner's word (`owner 28.10.2026`), a finding id, a spec id with key (`t-1508 K-R1-2`), or a backlog id |
| `carriers` | list, at least 1 | each item `{"file": <package-relative posix path>, "anchor": <str>}`; two or more items = twin carriers, ALL must hold the rule; each carrier has its own anchor (twins may word the rule differently) |

`schema_version` other than 1, a missing `rows`, or `rows` not a list: one register-level finding.

### 2.3 How an anchor is chosen (F1-A decided)

1. Take the sentence of the carrier that states the duty.
2. Pick 2-6 consecutive words of it (hard bound 2..6 words after whitespace folding, at most 80 characters; an empty anchor
   is 0 words and refused; `docs/TESTING.md` aims at 2-4 — the reader refuses only outside 2..6) that name THIS duty and
   occur EXACTLY ONCE in the carrier (case-insensitive, whitespace folded, the package marker comments removed — every
   other HTML comment counts, §3.2). Run `role_rules.py --check`; it says how many times the anchor stands.
3. Prefer the words that carry the duty (`never`, the object, the condition) over decoration; never a single identifier.
4. Never an anchor that is only a field name, a vocabulary word or a command flag: when a script reads that token, the
   script's own test guards it (TESTING.md: «если фразу ЧИТАЕТ код — тест на этот код»).

Why exactly once (F4 decided): with one occurrence, deleting the rule's sentence always takes the count to 0 and turns red;
with two, deleting the rule leaves the other occurrence and the loss is silent. Observed: in `agents/qa-scout.md` the phrase
"A conflict nothing settles" stands twice case-insensitively (lines 83 and 85), so it cannot be an anchor; the unique
"Triangulate a conflict" (line 61) can.

### 2.4 What a carrier may be

A file a role or the orchestrator is handed at run time, package-relative posix path, no `..`, no drive or leading `/`, no
backslash:

- `agents/*.md`;
- `skills/**/*.md` (SKILL.md and `phases/*.md`);
- `references/**/*.md`, `references/*.json` (string values, §3.2), `references/templates/*`, and the generated slices
  `references/slices/<role>/*.md`;
- `handoffs/*.yaml`.

Anything else (`design/`, `scripts/`, `skills/**/evals/*.json`, `CHANGELOG.md`) is refused: "not a role carrier: a rule lives
where a role reads it (FR-44)". One comment rule for every carrier (§3.2): no directory is exempt and none is special.

A generated carrier (`references/slices/<role>/*.md`, rendered by `scripts/contract_slices.py` from a reference; the page
`references/slices/<role>/handoff-keys.md`, rendered from that role's handoff form) is a legal carrier, but a row never
holds it ALONE: the row also carries the SOURCE file the slice is cut from. The slice stays as a twin carrier where the old
pin read it, because a rule moved into a section not marked for that role vanishes from the slice while its source keeps it
(E-18). The source of each slice used in §4.4 is named in that row.

## 3. The one reader and the one test

### 3.1 `scripts/role_rules.py` (new script; TESTING.md allows a new test file only for a new script)

- `load(root) -> (rows, problems)`: probes `<REG>` first, then reads it through `hooklib.read_json(path, default=None,
  kind=dict)`. Probe order, each with its `<why>` for the register-level refusal (R4): `not path.is_file()` -> `absent`;
  `path.stat().st_size == 0` -> `0 bytes`; `read_json` returns `None` -> `not a UTF-8 JSON object` (read_json returns only
  its default, with no reason, `scripts/hooklib.py:694`; the probe names the two cases it can tell). Error direction of the
  reused `read_json`: its `default` means "nothing there"; here "nothing there" must be a FINDING, never an empty register.
- `findings(root=PLUGIN_ROOT) -> list[str]`: every problem, one FR-1 line each, in this order: register-level, then row
  schema, then duplicates, then per row per carrier. A row with a schema problem is not searched (a malformed row never
  counts as holding its rule).
- Carrier read, each with its `<reason>`: `read_bytes()` raising `OSError` -> `cannot open (<exception class>)`; decoding as
  `utf-8-sig` raising `UnicodeDecodeError` -> `not UTF-8`; a `.json` carrier through `read_json(path, default=None)` returning
  `None` -> `not JSON`.
- CLI: `python -B scripts/role_rules.py --check` prints the findings, then one summary line
  `role-rules: <n> rows, <m> carriers checked, <k> finding(s)`; exit 0 when no finding, 1 otherwise. No other mode (FR-14:
  that is the whole output contract).
- Nothing is truncated: findings print whole; the files read are bounded by `selftest --limits`.

### 3.2 Search semantics (Lead decision B1)

- Text of an `.md` / `.yaml` / template carrier: read as UTF-8 (`utf-8-sig`). Removed first are ONLY the package's own
  marker comments, each a one-line comment matching `<!--\s*(?:kind:|roles:|gen|/gen)[^\n]*?-->` — the `<!-- kind: … -->`
  marker (`role_load.KIND_MARKER`), the `<!-- roles: … -->` marker (`contract_slices.ROLE_MARKER`), the `<!-- gen… -->`
  markers (`<!-- gen:digest … -->` in charters, `<!-- generated from … -->` on the first line of a slice) and `<!-- /gen -->`.
  The TEXT between a `<!-- gen… -->` and its `<!-- /gen -->` stays. Every other `<!-- … -->` is text and is searched, in every
  carrier: roles read these files raw (`scripts/brief_pack.py:93` hands the template's path; no product script strips
  comments before delivery — critic t-2257 B1), so a comment is delivered text.
- Then folded with `" ".join(text.split())` (CRLF, indentation, line wraps, U+00A0 fold to one space) and `casefold()`. The
  anchor is folded the same way.
- `.json` carrier (e.g. `references/ahead-cards.json`): read through `hooklib.read_json`; every string VALUE, recursively,
  joined with `"\n"`, then folded. Keys are not searched.
- Count = non-overlapping occurrences of the folded anchor in the folded text. 1 = holds; 0 = lost; >1 = ambiguous.
- `.yaml` comment lines (`# ...`) are searched: the handoff forms carry their guidance to the role in comments.

### 3.3 Refusal texts (FR-1), exact form

- Lost: `role-rules: <id>: <file> lost the rule "<rule>" (source: <source>) - the anchor "<anchor>" is not in the text.
  Expected: the anchor exactly once. Restore the rule in <file>; if you reworded it, put 2-6 words of the new wording that
  occur once into the row's anchor in the same diff; if the rule is retired, remove the row in the same diff and name whose
  word retires it (owner's word, finding or spec id) in the commit message as "role-rules: retire <id> -- <whose word>".`
- Twin lost: the same, plus `- still held by: <other carriers>` so the fixer sees the twin wording.
- Only in a marker: `... the anchor "<anchor>" stands only inside a package marker comment (<!-- kind/roles/gen -->), which
  is not text a rule lives in. Put the rule in the text, or retire the row as above.` (count 0 after the markers are removed,
  more than 0 before.)
- Ambiguous: `role-rules: <id>: <file> carries the anchor "<anchor>" <n> times. Expected exactly once, so that deleting the
  rule turns this red. Choose 2-6 words of the rule's own sentence that occur once (role_rules.py --check counts them).`
- Missing carrier: `role-rules: <id>: carrier <file> does not exist. If the text moved, point the row at the new file in
  the same diff; if the rule is retired, remove the row as above.`
- Unreadable carrier: `role-rules: <id>: carrier <file> cannot be read (<reason>). Expected a UTF-8 text file.` (`<reason>`
  per §3.1.)
- Not a carrier home: `role-rules: <id>: <file> is not a role carrier (agents/, skills/, references/, handoffs/). A rule
  lives where a role reads it (FR-44).`
- Schema: `role-rules: row <index> (<id or "no id">): <key> <what is wrong>; expected <the rule of §2.2>.`
- Duplicate id: `role-rules: id <id> is used by rows <i> and <j>; expected unique ids - rename one.`
- Duplicate guard: `role-rules: rows <id1> and <id2> guard the same anchor "<anchor>" in <file>; one rule, one row - merge
  them.`
- Register unreadable: `role-rules: <REG> cannot be read (<why>). Expected a JSON object {"schema_version": 1, "note",
  "rows": [...]}; restore it from git or fix the JSON.` (`<why>` per §3.1.)

### 3.4 Null outcome and the before/after worlds (temporal edge)

- Before TD-5.1 lands: no `<REG>`, no reader, no test; the 12 pin files guard the rules (TESTING.md: the old pin stays until
  the register takes the rule). TD-5.1 creates `<REG>`, the reader and the test in ONE commit that also deletes the pin files
  whose every key went to a row or a dropped kind (§7.1).
- After: an absent or unreadable `<REG>` is a register-level finding (red), never "0 rows".
- `rows: []` is legal: the reader passes and prints `role-rules: 0 rows - no rule of a role is guarded`. Invariant: an empty
  register never reads as "all rules hold"; the line says nothing is guarded, and a diff emptying the register is a diff
  removing every rule (critic, §5; the TD-5.4 gate, after the waves).

### 3.5 The test `scripts/tests/test_role_rules.py` (one parameterised test, harness style like its neighbours)

- One table `CASES = [(case_id, files: {path: text}, register: object | raw str, expect: [substring, ...])]`; one loop builds
  a temporary package tree (harness `temp_dir` / `cleanup`), calls `role_rules.findings(root)` and checks that every
  expected substring is in exactly one finding and that there is no finding beyond those (case id in the message, so a red
  line names the case).
- The shipped case: `findings(PLUGIN_ROOT) == []`, printing the summary line. It holds because a key that does not hold in
  its carrier today has NO row (Lead decision B1(c), §7.1); the rows that ship are only the rows whose anchors count 1.
- The table rows are the edges of §6 (one row each). They are inputs to the reader through its door, NOT a negative control
  of the shipped files (TESTING.md: no corrupted copy of a real file).
- Budget (TESTING.md): test lines in the diff not above product lines (reader + register); the file runs under 10 s; no
  subprocess per case (one CLI call at most, for the exit code).

### 3.6 Where else it is wired (F5 decided: (c))

- CI: `selftest.py --tests` and `--fast` glob every `scripts/tests/test_*.py`, so the test runs there without a list entry.
- `selftest.py --limits` (`cmd_limits`) calls `role_rules.findings(PLUGIN_ROOT)` and fails on a finding, printing each: trimming
  a file to its cap is the owner's scenario, and `--limits --lang` is what a builder runs on a size edit and the integrator
  runs before every commit (`plans/builder-rules.md` 7b, PROJECT.md p. 2).
- NOT `audit_factory.main()`: that is the project doctor, run in every project; role texts are package files a project never
  changes (precedent and reason: `scripts/gate_registry.py` docstring lines 16-19).
- NOT `CONTRACT_TESTS` (TD-9 collapses the registries of test names; adding one works against it).
- Census: rows in `scripts/tests/fixtures/judgment-census.json` for each check unit of `role_rules.py`, class and owner per
  §1.3; `roles` as `test_judgment_census.py` C1 demands (precedent: `gate_registry.py` rows carry `["conductor"]`).

## 4. Migration of the 12 pin files

### 4.1 Criterion: which keys become rows (the rule for TD-5.3 waves; §4.4 already applies it to the 12 files)

A key becomes a row when ALL hold:

1. it states a duty, a ban or a judgment the role (or orchestrator, conductor) applies — not a field name, vocabulary token,
   command flag, heading-only form, section order, size or count;
2. its file is a carrier of §2.4 (not `design/`, not `evals.json`);
3. it is not already retired in the pin itself (`X7_3_RETIRED` sets cite spec `t-1765-x7-pins.md`, R-drop);
4. no other row already guards the same rule in the same carrier (keys of one rule become one row: one anchor per carrier per
   rule; keys of one rule in several files become one row with twin carriers; a rule guarded by two pin files is ONE row
   whose `source` names both old keys);
5. it holds in its carrier today (else: no row, `red before:`, §7.1).

A separate clause of one sentence (a ban beside a duty, a second thing to read first) is its own row: one anchor guards only
the words it stands in, and a partial edit removing the other clause would be silent (R3-2d, R5).

Dropped, by kind (one report line per kind per file):

| Kind | Why dropped | Who guards it instead |
|---|---|---|
| ABSENCE key (an old sentence must not come back), the regex ban, the "rule lives in the rubric, not the charter" absence, the owner-word sub-keys K2a/K2b/K3a-sub | F3 decided (a) | the critic reads the diff; where the text carries a POSITIVE sentence of the ban, that sentence is a row |
| COUNT key, position/order key | a pin of form; exactly-once of the row's anchor carries the count of THAT anchor; a second wording elsewhere is the critic's question | critic |
| size cap (`RUBRIC_CAP`, `SKILL_CAP`, `CAP`) | duplicate of `selftest.py --limits` | `--limits` |
| `evals.json` structure | not a role rule (a live-run eval scenario) | nothing (TESTING.md "Тест документа…") |
| a single token READ BY CODE (`field_absent`, `blocking_check`, `` `thens: [n]` ``, `retracted_unresolved`, `unknown: <why>`, `ASSERT_STRICTER`) | an anchor must be 2-6 words naming a duty; the token is a contract of code | the reading script's test; the duty sentence, where one exists, is a row (named per key in §4.4) |
| a single token NO script reads (`oracle_field_absent`, "whole", the word keys of the scout pin) | below the 2-word floor, never unique | the row that holds its rule, named per key in §4.4 |
| a key in `design/` (`design/state-exits.md`) | not a role carrier (FR-44) | nothing; named in the known-losses list (R6) |
| negative controls, `zzz-not-in-any-file`, positive controls of a control | TESTING.md: not written | nothing |

### 4.2 Worked example 1 — `test_case_roles_twin_rules.py` (RN1-7)

Keys: `("goes to the server or redraws the page", "whole", "still in focus")` in BOTH `agents/qa-case-designer.md` and
`agents/qa-case-critic.md`, plus a negative control per key.

- `"whole"`: dropped — one word, matches anywhere; it could never catch a deletion (below the 2-word floor, not unique);
  its rule is held by `case-focus-twin`.
- `"goes to the server or redraws the page"` and `"still in focus"`: the same sentence of the same rule in each carrier —
  one anchor per carrier is enough. `still in focus` is chosen: it names the Then the critic must not strike. Counted:
  designer line 32 (1), critic line 63-64 across the wrap (1).
- `test_case_role_twins.py` K4 (`its Then is the value kept whole and the field still in focus`, designer) is the same rule
  in the same carrier: the same row (two rows on one anchor would raise the duplicate-guard finding).
- Negative controls: dropped.

Resulting row:

```json
{"id": "case-focus-twin",
 "rule": "A field whose value goes to the server or redraws the page on each key has the Then 'value kept whole, field still in focus'; the case critic never strikes it and flags its absence.",
 "source": "RN1-7 (test_case_roles_twin_rules); t-1675 K4 (test_case_role_twins)",
 "carriers": [{"file": "agents/qa-case-designer.md", "anchor": "still in focus"},
              {"file": "agents/qa-case-critic.md", "anchor": "still in focus"}]}
```

### 4.3 Worked example 2 — `test_red_then_texts.py` (t-1508 R1/R3, owner 28.10.2026)

PRESENT after the `X7_3_RETIRED` filter: K-R1-1a, K-R1-1b, K-R1-2, K-R1-3, K-R1-4, K-R1-6, K-R1-7 (s7.md, conductor.md),
K-R3-3, K-R3-8, R3-2d (qa-failure-analyst.md). ABSENT: K-R3-5. Regex ban: K-R1-5. Each anchor below counts 1 (critic t-2257
run 1, and this revision's search, §4.4 "How counted").

| Old keys | Verdict | Row |
|---|---|---|
| K-R1-1a | a rule (read the case's triage row first): its own row (R5) | `red-then-read-triage-row` |
| K-R1-1b | a separate clause of the same sentence (read the Self-probe notes) | `red-then-read-self-probe` |
| K-R1-2 (s7), K-R1-4 (conductor) | one ban in two carriers: twin | `red-then-no-s5-rework` |
| K-R1-3 | a rule (the person's words go by file) | `person-words-by-file` |
| K-R1-6 (s7), K-R1-7 (conductor) | one rule (say the rerun price first), worded differently: twin, two anchors | `red-then-price-first` |
| K-R1-5 (regex: no "comment out" near "Then" in three files) | the ban has a POSITIVE sentence at s7 line 148 ("Nobody comments out the red"): that is the row; the absence over conductor/analyst is dropped (F3, known loss) | `red-never-commented-out` |
| K-R3-3 | a rule (diagnostic run only in a copy) | `independent-then-copy-only` |
| R3-2d | a separate clause of the same sentence (the diagnostic never changes the verdict) | `diagnostic-run-not-verdict` |
| K-R3-8 | a rule | `reorder-reviewed-by-code-critic` |
| K-R3-5 (ABSENT, old 2c) | dropped (absence, F3) | — |
| K-R3-1, K-R3-2, K-R3-4, K-R3-7, R3-rule7 | dropped: already retired in the pin (spec t-1765-x7-pins, R-drop) | — |
| negative controls, `zzz` | dropped | — |
| K-R3-6 | lives in `test_brief_pack_roles.py` (a behaviour file): §4.6 inventory | — |

Accounting: 17 keys (15 PRESENT incl. the retired, 1 ABSENT, 1 regex) = 11 row / 6 dropped / 0 `red before:`.

Resulting rows:

```json
{"id": "red-then-read-triage-row", "rule": "Asked to check the Thens a red stopped, read the case's triage row first.", "source": "owner 28.10.2026; t-1508 K-R1-1a", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "the case's triage row"}]},
{"id": "red-then-read-self-probe", "rule": "Asked to check the Thens a red stopped, read the case file's Self-probe notes before anything starts.", "source": "owner 28.10.2026; t-1508 K-R1-1b", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "Self-probe notes"}]},
{"id": "red-then-no-s5-rework", "rule": "Thens behind a red are checked through the S7 rework with the person's words, never `rework --stage S5`.", "source": "owner 28.10.2026; t-1508 K-R1-2, K-R1-4", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "never `rework --stage S5`"}, {"file": "references/conductor.md", "anchor": "never `rework --stage S5`"}]},
{"id": "person-words-by-file", "rule": "A rework carrying the person's words always takes --words-file, never --reason.", "source": "t-1508 K-R1-3", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "always takes `--words-file`"}]},
{"id": "red-then-price-first", "rule": "Before a rerun of Thens behind a red, tell the person its price: the report writer runs again and gate B is asked again.", "source": "owner 28.10.2026; t-1508 K-R1-6, K-R1-7", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "report writer run again"}, {"file": "references/conductor.md", "anchor": "say so first"}]},
{"id": "red-never-commented-out", "rule": "A red Then is never commented out; the asserts of independent Thens are moved above it and the test stays red at the same Then.", "source": "owner 28.10.2026; FA-10; t-1508 K-R1-5", "carriers": [{"file": "skills/qa-story/phases/s7.md", "anchor": "Nobody comments out"}]},
{"id": "independent-then-copy-only", "rule": "An independent Then behind a red gets one diagnostic run in a copy; the test in the repository is never changed.", "source": "t-1508 K-R3-3", "carriers": [{"file": "agents/qa-failure-analyst.md", "anchor": "repository is never changed"}]},
{"id": "diagnostic-run-not-verdict", "rule": "The diagnostic run of an independent Then is not a control experiment and never changes the red's verdict.", "source": "t-1508 R3-2d", "carriers": [{"file": "agents/qa-failure-analyst.md", "anchor": "never changes the red's verdict"}]},
{"id": "reorder-reviewed-by-code-critic", "rule": "An independent Then after the red is reordered by the author, and a code critic reviews that one test.", "source": "t-1508 K-R3-8", "carriers": [{"file": "agents/qa-failure-analyst.md", "anchor": "reviews that one test"}]}
```

Lines (s7.md / conductor.md / analyst): triage row s7:255; Self-probe s7:256; `rework --stage S5` s7:259, conductor:34;
`--words-file` s7:261; report writer s7:260; say so first conductor:34; Nobody comments out s7:148; the three analyst anchors
analyst:58.

### 4.4 The rows of the other ten files

**How counted.** Every anchor below was searched in its carrier with the Grep tool, case-insensitive, multiline, the pattern
being the anchor regex-escaped with every whitespace run replaced by `\s+` (so a line wrap is found) — e.g. `still\s+in\s+focus`,
`the\s+norms\s+hold\s+\(default\)`. HTML comments were NOT removed in the search, which is the matcher of Lead decision B1
(none of the hits sits inside a `kind`/`roles`/`gen` marker). Where the searched pattern was a prefix of the anchor (marked
"prefix"), the anchor counts at most what the prefix counts (1) and the line shows the whole anchor. The `n` column is the
count (all 1) and `@` the line at revision time (informational; the reader does not read line numbers). A row copies into
`<REG>` as: `id`, `rule`, `source` verbatim, and `carriers` in the order listed, each `{"file", "anchor"}` with the anchor
written without the surrounding quotes.

#### 4.4.1 `test_blocked_by_env_texts.py` (t-219)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `blocked-row-names-every-instance` | A `blocked_by_env` row names in `instance_ids` every instance the stand blocked. | t-219 (1), (9); X7-1 | `references/artifact-contract-automation.md` -> "every instance the stand blocked" (1 @31); `handoffs/s5-automator-to-critic.yaml` (the source of the generated key page) -> "every instance the stand blocked" (1 @116); `references/slices/qa-automator/handoff-keys.md` (generated from that handoff by `contract_slices.py`) -> "every instance the stand blocked" (1 @55) |
| `product-answer-is-red` | A product answer (a wrong status code, a wrong body, a failed assertion) is red, never a stand block. | t-219 (2); P20; FR-34 | `agents/qa-automator.md` -> "a product answer is never" (1 @41) |
| `stand-blocked-test-still-written` | A test this stand blocks is still written, and a person runs it elsewhere (the last rung). | t-219 (3) | `agents/qa-automator.md` -> "a person runs it elsewhere" (1 @41) |
| `critic-reads-red-reason` | For a `blocked_by_env` row whose test ran red, the code critic reads `last_run.reason` against the change. | t-219 (5) | `references/code-review-rubric.md` -> "read the reason against the change" (1 @85) |
| `unverified-not-a-pass` | `critic_verdict: unverified` never covers a test that ran red. | t-219 (6) | `references/code-review-rubric.md` -> "unverified is not a pass" (1 @89) |
| `all-blocked-window-null-outcome` | A window where every instance is blocked by the stand closes with the verdict blocked: a recorded null outcome, not a missing one. | t-219 (9); FR-23 | `references/artifact-contract-automation.md` -> "recorded null outcome" (1 @171-172) |
| `gate-b-shows-ran-red` | Gate B shows the person `ran red: <reason>` beside every blocked row that ran. | t-219 (9) | `references/artifact-contract-automation.md` -> "beside every blocked row that ran" (1 @174) |
| `red-that-ran-needs-detail` | A blocked instance that ran and failed carries a `detail`. | t-219 (4), (9); t-121 12b | `references/artifact-contract-automation.md` -> "required when the instance ran" (1 @33); `references/slices/qa-automator/artifact-contract-automation.md` (generated from the contract) -> "required when the instance ran" (1 @33) |
| `detail-names-stand-control` | The `detail` of a blocked instance that ran names the control that shows the stand, not the product, blocked it. | t-219 (4); t-219 (8) `detail` | `references/artifact-contract-automation.md` -> "the control that shows the stand" (1 @33); `references/slices/qa-automator/artifact-contract-automation.md` (generated from the contract) -> "the control that shows the stand" (1 @33); `handoffs/s5-automator-to-critic.yaml` -> "names the control you did" (1 @114) |
| `blocked-red-rule-in-rubric` | A blocked row that ran red is judged by the rubric rule of that name; the code critic's charter points at it. | t-219 (7) KEYS heading and the charter pointer count | `references/code-review-rubric.md` -> "A blocked row that ran red" (1 @83); `agents/qa-code-critic.md` -> "A blocked row that ran red" (1 @37) |
| `blocked-row-one-per-case` | `blocked_by_env` is one row per case. | t-219 (9) row shape | `references/artifact-contract-automation.md` -> "`blocked_by_env` is one row per case" (1 @30-31; prefix `one\s+row\s+per\s+case`) |
| `critic-checks-instance-list` | The code critic checks that `instance_ids` is complete and that the newest run of those instances shows the stand. | t-219 (8) `instance_ids` | `handoffs/s5-automator-to-critic.yaml` -> "the list is complete" (1 @116) |
| `remedy-exact-fix-no-credential` | The code critic checks that a `remedy` names an exact fix and carries no credential value. | t-219 (8) `remedy` | `handoffs/s5-automator-to-critic.yaml` -> "carries no credential value" (1 @117) |

- Rows (13 rows, 17 keys): KEYS[0] PAGE + KEYS[12] CONTRACT -> `blocked-row-names-every-instance`; KEYS[1] ->
  `product-answer-is-red`; KEYS[2] -> `stand-blocked-test-still-written`; KEYS[3] -> `critic-reads-red-reason`; KEYS[4] ->
  `unverified-not-a-pass`; KEYS[5] -> `all-blocked-window-null-outcome`; KEYS[6] -> `gate-b-shows-ran-red`; KEYS[7] SLICE +
  KEYS[13] CONTRACT -> `red-that-ran-needs-detail`; KEYS[8] SLICE + HANDOFF_FIELDS `detail` -> `detail-names-stand-control`;
  KEYS[10] + the charter pointer count (`:104-107`) -> `blocked-red-rule-in-rubric`; KEYS[11] -> `blocked-row-one-per-case`;
  HANDOFF_FIELDS `instance_ids` -> `critic-checks-instance-list`; HANDOFF_FIELDS `remedy` -> `remedy-exact-fix-no-credential`.
- Dropped (3): KEYS[9] `last_run.reason` (single token; its rule is held by `critic-reads-red-reason`); the two charter
  absences "ran red: read the reason against the change" and "unverified is not a pass" in `agents/qa-code-critic.md`
  (absence, F3; known loss).
- `red before:` none (every key holds today: critic t-2257 run 2, and the counts above).
- Count line: 20 keys = 17 row + 3 dropped + 0 red before; 6 negative controls (not keys) dropped.

#### 4.4.2 `test_case_role_twins.py` (t-1675 / t-1679)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `case-focus-twin` | (§4.2) | (§4.2) | (§4.2) |
| `focus-then-oracle-own-requirement` | The `then_oracles` ref of a focus-and-partial-input Then is the field's own requirement R, never `unknown`. | t-1675 K4b | `references/artifact-contract.md` (the source of the slice) -> "the field's own requirement R" (1 @139); `references/slices/qa-case-designer/artifact-contract.md` -> "the field's own requirement R" (1 @137) |
| `then-field-found-in-shape` | A Then whose value is read from an API response names the field, and the case critic finds that field in the response shape; a field observable another way and absent is a `fail`. | t-1675 K5, K6 | `agents/qa-case-critic.md` -> "you find that field" (1 @66) |
| `own-requirement-expected-red` | A case whose own requirement needs data the product holds nowhere is the requirement's one expected red, not a case defect. | t-1675 K7 | `agents/qa-case-critic.md` -> "expected red, not a case defect" (1 @66) |
| `unread-shape-unverified` | A response shape the case critic could not read is a concern marked unverified, never a pass. | t-1675 K8, K8b | `agents/qa-case-critic.md` -> "a shape you could not read" (1 @66) |
| `then-answers-own-case` | A Then answers only its own case's requirements: a Then whose oracle is an R-n outside the case's covers belongs to that R-n's case, and the case critic flags it as a repeat. | t-1675 K9, K10 | `agents/qa-case-critic.md` -> "outside this case's covers" (1 @67); `references/artifact-contract.md` -> "asserts only its own requirements" (1 @138); `references/slices/qa-case-designer/artifact-contract.md` (generated from it) -> "asserts only its own requirements" (1 @136) |
| `parametrised-inputs-no-repeat` | Several inputs of one requirement in one parametrised case are no repeat. | X5-1; P16; t-1675 K9b | `agents/qa-case-critic.md` -> "one parametrised case are no repeat" (1 @67) |
| `one-behaviour-unit-level` | "One behaviour per case" is a unit-level rule, not an API or e2e one. | X5-1; P16; t-1675 K9c | `agents/qa-case-critic.md` -> "is a unit-level rule" (1 @39) |
| `automator-owns-test-count` | How many tests the automator writes for a case is the automator's call (P17), never the case critic's. | X5-1; P17; t-1675 K9d | `agents/qa-case-critic.md` -> "how many tests the automator writes" (1 @41) |
| `field-absent-needs-shape-ref` | A red because the response lacks the field the Then reads carries `field_absent` with a `shape_ref`; no `shape_ref`, no block. | t-1675 K11 | `agents/qa-automator.md` -> "carries no field the Then reads" (1 @82) |
| `field-absent-accepted-red` | A `field_absent` row is accepted red by the code critic, never called a product bug. | t-1675 K13 | `agents/qa-code-critic.md` -> "never called a product bug" (1 @84) |
| `field-absent-judged-by-shape-ref` | A `field_absent` row is judged by its `shape_ref`, not by the control experiment. | t-1675 K14, K14-phase | `agents/qa-failure-analyst.md` -> "judged by its shape_ref" (1 @80); `skills/qa-story/phases/s7.md` -> "judged by its `shape_ref`" (1 @239) |

- Rows (11 rows of this file + `case-focus-twin`, 14 keys): K4 -> `case-focus-twin`; K4b -> `focus-then-oracle-own-requirement`;
  K5 -> `then-field-found-in-shape`; K7 -> `own-requirement-expected-red`; K8 -> `unread-shape-unverified`; K9 + K10 ->
  `then-answers-own-case` (author/critic twin, AR-19); K9b, K9c, K9d -> their rows; K11 -> `field-absent-needs-shape-ref`;
  K13 -> `field-absent-accepted-red`; K14 + K14-phase -> `field-absent-judged-by-shape-ref` (B2.5).
- Dropped (5): K6 `oracle_field_absent` (single token no product script reads — `git grep -l oracle_field_absent -- scripts/*.py
  hooks` finds only the pin, same-shape control `field_absent` finds `manifest_from_tests.py`; dropped because
  `then-field-found-in-shape` holds its rule, the field read from a response must be found in its shape, B2.5); K8b
  `unverified: no response shape` (the concern's text; its rule is held by `unread-shape-unverified`); K12,
  K12-slice-automator, K12-slice-code-critic `field_absent` (single token read by code, `manifest_from_tests.py`; its duty
  sentence is the row `field-absent-needs-shape-ref`).
- `red before:` none.
- Count line: 19 keys = 14 row + 5 dropped + 0 red before; 1 negative control dropped.

#### 4.4.3 `test_case_roles_twin_rules.py` (RN1-7)

- Rows: the row `case-focus-twin` (§4.2) takes the 4 keys "goes to the server or redraws the page" x2 and "still in focus"
  x2 (the same sentence of one rule in each carrier; one anchor per carrier).
- Dropped (2): "whole" x2 (single token no script reads; its rule is held by `case-focus-twin`).
- `red before:` none.
- Count line: 6 keys = 4 row + 2 dropped + 0 red before; 6 negative controls dropped.

#### 4.4.4 `test_critic_lines_hf2.py` (HF2-13/14/15)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `no-second-helper` | The code critic looks for a second helper beside an existing one and asks to extend or fix the existing helper. | HF2-13; TQ1-13; t-084 D13a | `agents/qa-code-critic.md` -> "second helper beside an existing one" (1 @34) |
| `no-fixture-twice` | The same fixture created twice in one window is a finding. | HF2-13; t-084 D13b | `references/code-review-rubric.md` -> "the same fixture created twice" (1 @64) |
| `count-before-unpacking` | Assert the count before unpacking, so the red line names the Then. | HF2-14; TQ1-14; t-084 D14a | `references/test-code-patterns.md` (the source of both slices) -> "assert the count before unpacking" (1 @146); `references/slices/qa-automator/test-code-patterns.md` -> "assert the count before unpacking" (1 @140); `references/slices/qa-code-critic/test-code-patterns.md` -> "assert the count before unpacking" (1 @46) |
| `red-line-names-then` | An unpacking with no asserted count is a finding: the red line names the Then only when the count is asserted first. | t-084 D14b | `references/code-review-rubric.md` -> "the red line names the Then" (1 @53) |
| `level-matches-plan` | The code critic checks that the test's level matches the S3 plan, or that its author names the deviation. | t-084 D14c | `agents/qa-code-critic.md` -> "level matches the S3 plan" (1 @54) |
| `refusal-test-discriminates` | A refusal test discriminates the cause: the reason the product names, or a control run that passes without the violated condition. | HF2-15; TQ1-12; t-084 D15a | `references/code-review-rubric.md` -> "a refusal test discriminates the cause" (1 @46) |
| `masked-not-compared-with-masked` | A masked value compared with a masked value is not a preservation check. | t-084 D15b | `references/code-review-rubric.md` -> "compared with a masked value" (1 @54) |

- Rows (7 rows, 9 keys): D13a, D13b, D14b, D14c, D15a, D15b -> their rows; D14a + the two slice keys (`SLICES_WITH_D14A`) ->
  `count-before-unpacking`. D13a, D14c and D15b keys were 7-8 words: the anchors are 5-6 of their words.
- Dropped: none. `red before:` none.
- Count line: 9 keys = 9 row + 0 dropped + 0 red before; 1 negative control dropped.

#### 4.4.5 `test_detection_role_texts.py` (t-1685 N1/N2, t-1692, t-1765 X1)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `scout-data-path-screens` | A story about one action is also about every screen where the person sees, changes or undoes what it wrote. | t-1685 K1-1 | `agents/qa-scout.md` -> "where they CHANGE or UNDO" (1 @37) |
| `scout-follow-the-data` | Follow the data: who reads and who changes what the function writes. | t-1685 K1-3 | `agents/qa-scout.md` -> "then follow the data" (1 @37) |
| `scout-source-is-a-record` | A source is a record in the inventory, never only a name inside a note. | t-1685 K1-2 | `agents/qa-scout.md` -> "only a name inside a note" (1 @83) |
| `scout-tool-miss-not-the-end` | A tool that did not read a source does not end the search: try the tracker search, the recorded route and the browser before writing it unavailable. | t-1685 K1-4 | `agents/qa-scout.md` -> "did not read a source" (1 @73) |
| `derived-norm-is-requirement` | A derived product norm IS a requirement, and the norm is its oracle. | t-1685 K1-5 (charter and template) | `agents/qa-requirements-tester.md` -> "the norm is its oracle" (1 @42); `references/templates/requirements-register.md` -> "the norm is its oracle" (1 @59, inside the guidance comment) |
| `one-question-per-fork` | One open question per fork, never one for a class. | t-1685 K1-6 (charter and template) | `agents/qa-requirements-tester.md` -> "never one for a class" (1 @79); `references/templates/requirements-register.md` -> "never one for a class" (1 @61, comment) |
| `norm-list-examples` | The derived product norms include: a missing item cannot be added, stock is respected, nobody touches another owner's data, a failed call is not shown as success. | t-1692 B3 | `references/templates/requirements-register.md` -> "a missing item cannot be added" (1 @58, comment) |
| `norms-one-confirmation-question` | The derived norms go to the person in one confirmation question, and the norm stays the default reading. | t-1685 F5 (b) | `references/templates/requirements-register.md` -> "ONE confirmation question" (1 @62, comment) |
| `norms-none-no-question` | With no norm derived, no confirmation question is asked. | t-1685 F5 (b) edge | `references/templates/requirements-register.md` -> "none derived, no such question" (1 @63, comment) |
| `norm-departure-expected-red` | Code that departs from a derived norm is an expected red (`contradicts`), with no question of its own. | t-1692 B1 | `references/templates/requirements-register.md` -> "no question of its own" (1 @63, comment) |
| `norm-readings` | The readings of the norms question are: the norms hold (default), or one does not apply (`from: person`). | t-1692 B2 | `references/templates/requirements-register.md` -> "the norms hold (default)" (1 @64, comment) |
| `norm-never-dropped-by-code` | No reading `from: code` ever drops a norm. | t-1692 B2 | `references/templates/requirements-register.md` -> "that drops the norm" (1 @64, comment) |
| `s0-tracker-query` | A page, filter or search read of the tracker goes through `ticket_adapter.py query`, never a tracker API of one's own. | t-1685 K1-7 | `skills/qa-story/phases/s0.md` -> "a page, filter or search" (1 @57) |
| `s1-use-words-not-accept-gap` | Words that say to use a source the factory could not read are not accept-gap: assess the source relevant with their words and resume the scout with the route. | t-1685 K1-8 | `skills/qa-story/phases/s1.md` -> "assess it relevant with their words" (1 @259, a fenced block; prefix `assess\s+it\s+relevant`) |
| `strategist-walk-every-function` | Every function of the register's `## Functions` gets a plan row that walks it as a person does. | t-1685 K2-1 | `agents/qa-test-strategist.md` -> "gets a row that WALKS it" (1 @26) |
| `strategist-record-oddities` | A walk records every oddity on the way. | t-1685 K2-2 | `agents/qa-test-strategist.md` -> "records every oddity on the way" (1 @26) |
| `one-off-check-no-automation` | A one-off check of new behaviour that will not join the regression needs no automated test; the agent walks it by hand. | P28; X5-0; K2-4 | `agents/qa-test-strategist.md` -> "needs no automated test" (1 @54) |
| `blast-radius-is-evidence` | `work/blast-radius.json` is evidence, not the radius; the strategist names the radius in the plan with the reason. | P27; X5-1 | `agents/qa-test-strategist.md` -> "not the radius; name the radius" (1 @58; prefix `not\s+the\s+radius`) |
| `name-what-index-missed` | The strategist names what the index could not see (dynamic calls, routes, UI to API, non-Python). | P27; X5-1 | `agents/qa-test-strategist.md` -> "what the index could not see" (1 @58) |
| `norm-row-does-not-wait` | A norm row does not wait on the norms-list question: it is planned with the norm as the oracle. | t-1685 F5 (b) S3 side; t-1816 F5 | `agents/qa-test-strategist.md` -> "A norm row does not wait" (1 @45) |
| `letter-branch-settles-oracle` | A letter branch whose answer settles the oracle sets `oracle_unknown: false`. | t-1685 K2-3 (card) | `references/ahead-cards.json` -> "whose answer settles the oracle" (1, a string value, @27; no JSON escape inside the anchor's span) |

- Rows (21 rows, 23 keys): K1-1..K1-4 -> the four scout rows; K1-5 charter + K1-5 template -> `derived-norm-is-requirement`;
  K1-6 charter + K1-6 template -> `one-question-per-fork`; t-1692 B3, F5 (b), F5 (b) edge, t-1692 B1, t-1692 B2 x2 -> the six
  template rows; K1-7, K1-8 -> the s0 and s1 rows; K2-1, K2-2, K2-4, X5-1 x2, F5 (b) S3 -> the six strategist rows; K2-3 ->
  `letter-branch-settles-oracle`. The eight template anchors stand inside the template's guidance comment (lines 29-66): they
  count under the matcher of decision B1 (§3.2) and would be red under full comment stripping (critic t-2257 B1).
- Dropped (6): K1-9 `unknown: <why>` (form token read by code: `code_says` is read by `contract.py` and its tests); ABSENT x5
  (scout "That is the whole job", "keyword-search the requirement text across the test"; tester "One question per class.",
  "ONE question for the whole class"; template "ONE question for the whole class") — absence, F3.
- `red before:` none.
- Count line: 29 keys = 23 row + 6 dropped + 0 red before; 3 negative controls dropped.

#### 4.4.6 `test_gate_continuation_texts.py` (HF1-8, GW1-12; spec t-050 3.7)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `gate-answer-read-whole` | Read the gate-decision answer whole and follow its `next_action` in this window. | HF1-8; GW1-12; t-050 3.7 | `skills/qa-story/SKILL.md` -> "Read the gate-decision answer whole" (1 @124) |
| `window-changes-only-by-window-line` | Only the gate-decision answer's `window` line changes the window. | HF1-8; t-050 3.7 | `skills/qa-story/SKILL.md` -> "only its `window` line changes it" (1 @125) |
| `recovered-window-goes-on` | A window that only recovered or recorded has not done its stage: it goes on, with no second restart. | GW1-12; t-050 3.7 | `skills/qa-story/SKILL.md` -> "only recovered or recorded" (1 @125) |
| `stop-after-gate-a` | With `pipeline.stop_after: "gate_A"` the story ends after gate A's decision is recorded, when `next_action` is `stop`. | t-050 3.7 | `skills/qa-story/phases/s4.md` -> "`next_action` is then `stop`" (1 @40) |
| `s4-start-s5-same-window` | After gate A is recorded, S5 starts in the same window; only the answer's `window` line asks for a change, and the orchestrator never writes a restart line of its own. | HF1-8; t-050 3.7 | `skills/qa-story/phases/s4.md` -> "restart line of your own" (1 @219-220) |
| `gate-answer-never-piped` | The controller's gate answer is read whole, never piped through `cut`, `head` or `tail`. | t-050 3.7 (s4 and s8 keys) | `skills/qa-story/phases/s4.md` -> "never pipe it through" (1 @212); `skills/qa-story/phases/s8.md` -> "never pipe it through" (1 @297) |
| `s8-go-on-to-s9` | After gate B, the orchestrator goes on to S9 in this window once `next` answers `closed`. | HF1-8; t-050 3.7 | `skills/qa-story/phases/s8.md` -> "Then go on to S9" (1 @459) |

- Rows (7 rows, 8 keys): the three SKILL.md keys -> the three SKILL rows; s4 "the gate-decision answer's `next_action` is then
  `stop`" -> `stop-after-gate-a`; s4 "start S5 in this window unless …" -> `s4-start-s5-same-window` (the key counts 2 in s4,
  lines 22 and 219: the anchor is other words of the line-219 sentence); s4 + s8 "never pipe it through …" ->
  `gate-answer-never-piped`; s8 "go on to S9 in this window" -> `s8-go-on-to-s9` (the key counts 2 in s8, lines 34 and 459:
  the anchor "Then go on to S9" stands only at 459).
- Dropped (19): ABSENT x7 ("stop with one line", "is at S<n>;", "Then end your window", "One step left: the retro.", "fresh
  window" x3) — absence, F3; `SKILL_CAP` (size cap, `--limits`); evals 18, 19, 20 present, eval 14's assertion
  `s5-in-same-window`, and the seven assertion names of evals 18-20 (11 keys: a live-run eval scenario, not a role rule).
- `red before:` none.
- Count line: 27 keys = 8 row + 19 dropped + 0 red before; 7 negative controls dropped.

#### 4.4.7 `test_mixed_then_texts.py` (HF2-3 part 3d, spec t-085 3.6)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `independent-then-before-red` | An independent Then is moved before the red assert that would stop it; one left behind a red with no `blocked_by_check` row is a code-review finding. | owner 28.10.2026 (HF5-16); t-085 K1a, K3a, K4 | `agents/qa-automator.md` -> "independent Thens before the red one" (1 @68); `agents/qa-code-critic.md` -> "an independent Then behind a red" (1 @35); `references/code-review-rubric.md` -> "placed after a failing assert" (1 @65) |
| `no-commented-out-checks` | No check is commented out outside the dimension-8 sanctioned path. | t-085 K1b | `references/code-review-rubric.md` -> "commented-out checks outside the dimension-8" (1 @65) |
| `commented-out-then-path` | A commented-out Then carries its reason, its `then_bindings` row with reason `handed_to_person` or `blocked_by_check`, and its Left with you line (rubric dimension 8). | t-085 K2, K3-ref, K5-ref | `references/code-review-rubric.md` -> "a commented-out Then with its reason" (1 @76); `agents/qa-automator.md` -> "commented out: rubric dimension 8" (1 @68); `references/artifact-contract-automation.md` -> "A commented-out Then: rubric dimension 8" (1 @70) |
| `blocked-then-recorded` | A Then the red stops is recorded as `blocked_by_check` and sent through `manifest_put.py --fragment` after the last `manifest_from_tests.py` run. | t-085 K3b | `agents/qa-automator.md` -> "record a Then the red stops" (1 @68) |
| `stopped-then-own-row` | A Then another check stops is its own `then_bindings` row (`reason: blocked_by_check`, `blocking_check`), never an `unresolved[]` row. | t-085 K5a | `references/artifact-contract-automation.md` -> "another check stops is its own row" (1 @66) |
| `resent-row-replaces-slice` | A re-sent `contradicts_requirement` row replaces its slice, and its `thens` separately. | t-085 K5e | `references/artifact-contract-automation.md` (the source of both slices) -> "row replaces its slice" (1 @69); `references/slices/qa-automator/artifact-contract-automation.md` -> "row replaces its slice" (1 @67); `references/slices/qa-code-critic/artifact-contract-automation.md` -> "row replaces its slice" (1 @67) |
| `order-between-cases` | A Then that only makes sense after another case's check says which case. | t-085 K6 | `agents/qa-case-designer.md` -> "another case's check says which case" (1 @40) |
| `red-triaged-once` | A red that stops other Thens is triaged once; the Thens it blocks are not failures. | t-085 K7 | `agents/qa-failure-analyst.md` -> "Thens it blocks are not failures" (1 @58) |

- Rows (8 rows, 14 keys): K1a (rubric) + K3a (automator, B2.1) + K4 (critic) -> `independent-then-before-red` (author, critic,
  rubric: one rule, AR-19); K1b -> `no-commented-out-checks`; K2 + K3-ref + K5-ref -> `commented-out-then-path` (the two
  pointers to dimension 8 are twin carriers of the rule they point at — the same verdict as the blocked-by-env and
  recommended pointers, B2.3); K3b -> `blocked-then-recorded`; K5a -> `stopped-then-own-row`; K5e + the two slice keys
  (`SLICES_WITH_K5`) -> `resent-row-replaces-slice`; K6 -> `order-between-cases`; K7 -> `red-triaged-once`.
- Dropped (9): K5b `blocking_check` (single token read by code: `contract.py`, `handoff_check.py`, `s5_precheck.py`; its rule
  is held by `stopped-then-own-row`); K5c `` `thens: [n]` `` (single token read by code: `contract.py`, `s5_precheck.py`; its
  rule is held by `resent-row-replaces-slice`); K5d `retracted_unresolved` (single token read by code: `manifest_put.py`,
  `s5_precheck.py`); the dimension-8 safe side x3: "dimension 8 was found" (position/structure), "dimension 8 does not name
  `contradicts_requirement`" (absence, F3; known loss), "dimension 8 names both reasons" (the same sentence the row
  `commented-out-then-path` anchors names both reasons); the owner-word sub-keys K2a, K2b, K3a-sub (absence; F8 decided (a):
  each counts 0 today, the flag `OWNER_WORD_FA` leaves with the file).
- `red before:` none.
- Count line: 23 keys = 14 row + 9 dropped + 0 red before; 1 negative control dropped.

#### 4.4.8 `test_recommended_rule.py` (GW1-44, t-538 section 3)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `recommend-only-after-executor` | An option is called recommended only after the one who carries it out is named; the conductor follows this rule. | GW1-44; t-538 3; CART-1 | `references/human-questions.md` -> "is called recommended only after" (1 @40); `references/conductor.md` -> "Recommend an option only after" (1 @79) |
| `recommendation-names-reader` | The executor of a recommended option is the function or field of the factory that reads what the option changes. | t-538 3 | `references/human-questions.md` -> "reads what the option changes" (1 @40) |
| `no-reader-not-recommended` | With no reader found, the option is not recommended, and an option kept anyway says it is unchecked and why. | t-538 3 | `references/human-questions.md` -> "the text says it is unchecked" (1 @40) |
| `config-key-reader-first` | An option that changes a config key looks for that key's reader first; no reader, no option, and the text says why. | t-538 3 | `references/human-questions.md` -> "no reader, no option" (1 @40) |

- Rows (4 rows, 5 keys): KEY + POINTER -> `recommend-only-after-executor`; the three sub-rule keys -> their rows. KEY was 7
  words: the anchor is 5 of them.
- Dropped (3): "the rule follows item 6" (position); the two byte caps (size cap, `--limits`).
- `red before:` none.
- Count line: 8 keys = 5 row + 3 dropped + 0 red before; the stages.json negative control and its positive control (2,
  not keys) dropped.

#### 4.4.9 `test_red_then_texts.py`

§4.3 (9 rows; 17 keys = 11 row + 6 dropped + 0 red before).

#### 4.4.10 `test_s7_control_experiment_texts.py` (HF2-18 part B, spec t-1247, round t-1343)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `stricter-no-repair` | `ASSERT_STRICTER` gets no repair, no draft, no rework and no gate A; the person removes the assert or refines the requirement. | owner 25.10.2026; t-1247 B-K2c | `skills/qa-story/phases/s7.md` -> "no repair, no draft, no rework" (1 @243) |
| `control-experiment-first` | A red on an extra or different value gets the control experiment first: the same action without the change under test. | owner 25.10.2026; t-1247 B-K3, B-K8, N2 | `skills/qa-story/phases/s7.md` -> "gets the control experiment first" (1 @114); `handoffs/s6-runner-to-analyst.yaml` -> "gets the control experiment first" (1 @116); `agents/qa-failure-analyst.md` -> "without the change under test" (1 @53) |
| `stricter-no-gate-a-return` | An assert stricter than the requirement means no return to gate A and no rewrite of the case; the person decides. | t-1247 B-K4 | `agents/qa-failure-analyst.md` -> "no return to gate A" (1 @54) |
| `weak-data-test-bug` | Test data weaker than the case's Given is a `TEST_BUG` of the data when the weakness alone explains the red. | t-1247 B-K5 | `agents/qa-failure-analyst.md` -> "is a `TEST_BUG` of the data" (1 @79; "test data weaker than" counts 2, lines 35 and 79) |
| `app-bug-after-control` | `APP_BUG` when both readings are tenable, and only after the control experiment. | t-1247 B-K6 | `agents/qa-failure-analyst.md` -> "`APP_BUG` when both readings are tenable" (1 @72; "when both readings are tenable" counts 2, lines 55 and 72) |
| `stricter-assert-twin` | The code critic asks whether the assert is stricter than the requirement, by the rubric section of that name. | t-1247 B-K10a, B-K10b | `agents/qa-code-critic.md` -> "Is the assert stricter than" (1 @50); `references/code-review-rubric.md` -> "An assert stricter than the requirement" (1 @99) |
| `never-case-defect-on-effect` | With the effect there and the requirement silent, the verdict is never `CASE_DEFECT`, even when the assert is the case's own Then. | t-1247 N3c | `skills/qa-story/phases/s7.md` -> "it is never `CASE_DEFECT`" (1 @241-242; prefix `never\s+`CASE_DEFECT``) |
| `judge-never-skips-control` | A judge's leaning, decided or not, never skips the control experiment. | t-1247 N3d | `skills/qa-story/phases/s7.md` -> "never skips the control experiment" (1 @77) |
| `every-difference-outside` | With differences on both sides of the requirement, an assert is stricter than the requirement only when every difference is outside the requirement. | t-1247 N8a | `agents/qa-failure-analyst.md` -> "EVERY difference is outside the requirement" (1 @54) |
| `rerun-is-reproduction` | Running the action again with the same change is a reproduction, not a control experiment. | t-1247 E14 | `agents/qa-failure-analyst.md` -> "is a reproduction, not a control" (1 @53) |
| `control-output-under-evidence` | The control experiment's output is saved under `evidence/` and recorded as `control` on the row. | t-1247 E21b | `skills/qa-story/phases/s7.md` -> "its output under `evidence/`" (1 @115; the key "under `evidence/`" counts 2, lines 115 and 244) |
| `weak-data-and-effect` | Weak data and the effect together give `ASSERT_STRICTER` with `given_gap`. | t-1343 F1c | `skills/qa-story/phases/s7.md` -> "both, weak data and the effect" (1 @118) |
| `no-effect-app-bug-or-case-defect` | With no effect without the change, the verdict is `APP_BUG`, or `CASE_DEFECT` when the case misread the requirement. | t-1343 F2a | `skills/qa-story/phases/s7.md` -> "no effect shows without the change" (1 @119) |
| `effect-silent-stricter` | The effect without the change, with the requirement silent on what the assert asks, is `ASSERT_STRICTER`. | t-1343 F2b2 | `skills/qa-story/phases/s7.md` -> "silent on what the assert asks" (1 @117) |
| `stricter-note-findings-file` | A Then that asks more than the requirement is a note with no `cause`, only in the critic's findings file, never in the form's `findings[]`. | t-1343 F4a, F4b | `references/code-review-rubric.md` -> "never in the form's `findings[]`" (1 @105; prefix `never\s+in\s+the\s+form's`); `agents/qa-code-critic.md` -> "never in the form's `findings[]`" (1 @73; prefix) |
| `s7-control-runs-anyway` | S7 runs its control experiment on such a red anyway; the critic's note is for the reader of the review. | t-1343 F4c, F4d | `references/code-review-rubric.md` -> "on such a red anyway" (1 @105); `agents/qa-code-critic.md` -> "on such a red anyway" (1 @73) |
| `scribe-left-with-you-stricter` | The report's Left with you carries one item for an assert stricter than its requirement. | t-1343 Scribe | `agents/qa-doc-scribe.md` -> "an assert stricter than its requirement" (1 @23) |

- Rows (17 rows, 22 keys): B-K2c -> `stricter-no-repair`; B-K3 + B-K8 + N2 -> `control-experiment-first` (analyst, phase,
  handoff); B-K4, B-K5, B-K6 -> their rows; B-K10a + B-K10b -> `stricter-assert-twin`; N3c, N3d, N8a, E14, E21b, F1c, F2a,
  F2b2 -> their rows (each a separate rule: no repair for `ASSERT_STRICTER` / never `CASE_DEFECT` / never skips the control
  experiment / evidence under `evidence/` are four rules, critic t-2257 B3); F4a + F4b and F4c + F4d -> the two twin rows;
  Scribe -> `scribe-left-with-you-stricter`.
- Dropped (43): B-K2b `ASSERT_STRICTER` (single token read by code: `contract.py`, `check_delivery.py`; its rule is held by
  `stricter-no-repair`); B-K9b "`CASE_DEFECT` · `ASSERT_STRICTER`" (an entry of the closed verdict list, a vocabulary read by
  code; its rule is held by `stricter-no-repair`); B-K13 `design/state-exits.md` (not a role carrier, FR-44; known loss,
  R6); the 21 keys of `X7_3_RETIRED` (B-K1, B-K2a, B-K7, B-K9a, N3a, N3b, E21a, F2b, Role, Rule1, Witness, B1, F1a, F1b, F1d,
  F5, F6, F7, F10a, F10b, F10c: already retired in the pin, R-drop t-1765-x7-pins); ABSENT x12 (old-2b, old-s7a, old-s7b,
  old-s6, old-F1, old-F1d, old-F2a, old-F2b, old-F4a, old-F4b, old-F5, old-F10; absence, F3); COUNT x3 (B-K11a, B-K11b,
  F2-one-summary; count — exactly-once of `stricter-assert-twin` and `effect-silent-stricter` keeps the count of their own
  anchors); positions x2 (the rubric section between two headings, the critic bullet in Techniques); `RUBRIC_CAP` (size cap,
  `--limits`); eval 21 (1 group: its structure, 8 assertion names, 12 words; a live-run eval scenario).
- `red before:` none.
- Count line: 65 keys = 22 row + 43 dropped + 0 red before; 16 negative controls dropped.

#### 4.4.11 `test_scout_conflict_rule.py` (RC1-13, t-1765 X1)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `conflict-settled-no-halt` | A requirement/code conflict that the ticket's comments, description or linked issues settle is no halt: the settling quote and its source are recorded. | RC1-13 (word keys comments, linked, quote, unresolved in both files); t-1765 X1 | `agents/qa-scout.md` -> "Triangulate a conflict" (1 @61); `skills/qa-story/phases/s1.md` -> "it is no halt" (1 @377) |
| `scout-unsettled-conflict` | A conflict nothing settles goes to `unresolved_facts` with both quotes. | t-1765 X1 fix-4, F7 | `agents/qa-scout.md` -> "with both quotes" (1 @85) |
| `s1-halt-only-unresolved` | S1 halts only on a conflict no source settles. | RC1-13 (s1 halt digest key) | `skills/qa-story/phases/s1.md` -> "Halt only on an unresolved conflict" (1 @377) |

- Rows (3 rows, 10 keys): the word keys "comments", "linked", "quote", "unresolved" x2 files (8; single words, the row's
  anchors are the rule's own words) -> `conflict-settled-no-halt`; s1 "requirement/code conflict:" -> `s1-halt-only-unresolved`
  (B2.4; no product script reads that string: `git grep -l -i "requirement/code conflict" -- scripts/*.py hooks references`
  finds only tests and `references/halts.md`, same-shape control `unresolved_facts` finds `context_bundle.py`); the scout
  When-to-ask sentence -> `scout-unsettled-conflict`.
- Dropped (3): "requirement/code conflict:" absent from the scout (absence, F3); the conflict-passage checks for s1 and the
  scout (position: "the rule sits next to the conflict").
- `red before:` none.
- Count line: 13 keys = 10 row + 3 dropped + 0 red before; 8 negative controls dropped.

#### 4.4.12 `test_time_fork_rule.py` (TQ1-24, t-1701 D5-B, t-1755 F2)

| id | rule | source | carriers -> anchor (n @line) |
|---|---|---|---|
| `time-fork-case-tolerance` | A Then on a value the server writes later needs a tolerance from the requirements and a 'cannot tell' outcome; the case critic flags a time-fork Then without either. | TQ1-24; t-1701 D5-B K1 | `agents/qa-case-designer.md` -> "needs a tolerance from the requirements" (1 @37); `agents/qa-case-critic.md` -> "A time-fork Then with no tolerance" (1 @68) |
| `time-fork-test-window` | A stamp written after the response is checked in the window [t_before - tolerance, t_after + tolerance]; inside the tolerance the test skips with 'cannot tell', never a pass or a red, and the code critic checks it. | TQ1-24 K2, K3 | `references/test-code-patterns.md` -> "inside the tolerance the outcome" (1 @134); `references/code-review-rubric.md` -> "time fork uses the case's tolerance" (1 @59) |
| `manual-evidence-twin` | A manual case's evidence follows `references/manual-evidence.md`, and the case critic holds the case to that policy. | t-1755 F2 | `agents/qa-case-designer.md` -> "A manual case's evidence follows" (1 @67); `agents/qa-case-critic.md` -> "its manual-evidence policy included" (1 @73) |

- Rows (3 rows, 9 keys): K1 x4 (designer and critic, "from the requirements" and "cannot tell") -> `time-fork-case-tolerance`
  ("cannot tell" counts 2 in both charters and "from the requirements" 3 in the designer, so the anchors are other words of
  the same sentences); K2 x2 + K3 -> `time-fork-test-window` (author's pattern and critic's rubric; `cannot-tell` is read by
  `guard_pre_tool.py:2220`, so the token itself is not the anchor); F2 x2 -> `manual-evidence-twin`.
- Dropped: none. `red before:` none.
- Count line: 9 keys = 9 row + 0 dropped + 0 red before; 1 negative control dropped.

#### 4.4.13 Totals

104 rows (1 + 13 + 11 + 7 + 21 + 7 + 8 + 4 + 9 + 17 + 3 + 3), 138 carriers. `role_rules.py --check` on the TD-5.1 tree prints
`role-rules: 104 rows, 138 carriers checked, 0 finding(s)`; each row moved to `red before:` or `doubt:` lowers the two numbers
by that row and its carriers, and the report names it.

| Pin file | keys | row | dropped | red before |
|---|---|---|---|---|
| blocked_by_env_texts | 20 | 17 | 3 | 0 |
| case_role_twins | 19 | 14 | 5 | 0 |
| case_roles_twin_rules | 6 | 4 | 2 | 0 |
| critic_lines_hf2 | 9 | 9 | 0 | 0 |
| detection_role_texts | 29 | 23 | 6 | 0 |
| gate_continuation_texts | 27 | 8 | 19 | 0 |
| mixed_then_texts | 23 | 14 | 9 | 0 |
| recommended_rule | 8 | 5 | 3 | 0 |
| red_then_texts | 17 | 11 | 6 | 0 |
| s7_control_experiment_texts | 65 | 22 | 43 | 0 |
| scout_conflict_rule | 13 | 10 | 3 | 0 |
| time_fork_rule | 9 | 9 | 0 | 0 |

Negative and positive controls are not keys and are all dropped (TESTING.md).

Known losses (F3, R6), listed in the TD-5.1 report as one block: the FA-10 "comment out" absence over conductor and analyst
(red_then K-R1-5); the "rule lives in the rubric only" absence of blocked_by_env (2 keys); mixed_then's dimension-8 safe side
(dimension 8 must not name `contradicts_requirement`; it does not today); every ABSENT key above; B-K13 in
`design/state-exits.md`.

### 4.5 One commit, and the registries

The pin files are deleted (`git rm`) in the SAME commit that adds their rows. `plans/features.json` lists 9 of the 12 and
loses those 9 names in that commit (lines at revision time): 375 `test_gate_continuation_texts`, 414
`test_recommended_rule`, 440 `test_detection_role_texts`, 517 `test_mixed_then_texts`, 724
`test_s7_control_experiment_texts`, 725 `test_red_then_texts`, 1129 `test_critic_lines_hf2`, 1133
`test_scout_conflict_rule`, 1136 `test_time_fork_rule`. It does not list `test_blocked_by_env_texts`,
`test_case_role_twins`, `test_case_roles_twin_rules` (the same `git grep -n -o -E` pattern found the other nine, which is the
positive control). The other seven registries list none of the 12 (critic t-2257 Q5, each with a same-shape positive
control): `scripts/tests/fixtures/driver-layers.json`, `references/gate-registry.json`, `references/stage-joints.json`,
`scripts/selftest.py` (`CONTRACT_TESTS`/`TEST_TIMEOUTS`), `.gitlab-ci.yml`, `scripts/slow_tests.json`, `.github/`.
Not edited: `CHANGELOG.md` (history); `experiments/driver-golden/MANIFEST.json:1394`, which hashes
`scripts/tests/test_blocked_by_env_texts.py` in `package_files` (read by `scripts/tests/driver_golden.py:130-132` as
provenance) and already disagrees with many files (11 of the 12 pins are not in it): TD-5.1 breaks nothing new there, and
it is not on the cleanup list (R7).

### 4.6 Role-text pins inside behaviour files: the inventory rule

A check in a behaviour file is a ROLE-TEXT PIN when its input is the text of a carrier of §2.4 and it asserts presence,
absence, count or order of a phrase, WITHOUT running package code on that text. Then:

- when package code READS that phrase or marker (e.g. `contract_slices` markers, `person-owned: <id>` checked against
  `references/person-owned.json` by `test_conductor_investigates_first.py` K4): it is a data join — KEEP;
- otherwise apply §4.1: a rule becomes a row, the rest is dropped; the check (and helpers left unused) is deleted in the SAME
  commit that adds its rows; a key that does not hold today gets no row and goes to `red before:` (Lead decision B1(c)).

The sieve that finds candidates (a sieve, not the verdict — reading is):
`git -C <wt> grep -l -E "\"(agents|skills|references|handoffs)/[^\"]+\.(md|yaml|json)|\"(agents|skills|references|handoffs)\" /" -- ai-packages/qa-factory/scripts/tests/test_*.py`.
Measured at drafting time with the first alternative only (Grep tool on this worktree): 153 files, all 12 pin files among them
(positive control); it MISSED `test_gate_brief_and_retro.py`, which reaches s0.md as `SCRIPTS.parent / "skills" / ...`
(line 286) — hence the second alternative, and hence the inventory adds every file named in `docs/tasks/test-diet.md` TD-5
whether the sieve finds it or not.

## 5. From now on

### 5.1 A builder adding a rule to a role text

In the same diff as the text: one row in `<REG>` (§2.2, anchor by §2.3), then `python -B scripts/role_rules.py --check`. No
new pin file, no negative control, no key list in a test. A builder trimming a file to its cap runs `selftest.py --limits`,
which runs the same check (F5-c): a lost rule is red there with the door. After TD-5.1 the parenthesis of
`plans/builder-rules.md` 7d «до его появления — существующий пин остаётся» is obsolete (Lead edit, §7.5).

### 5.2 What the critic checks (a line for `docs/tasks/critic-diff-brief.md` question 5, Lead edit)

- A row removed from `<REG>` = a rule removed from a role. It needs the word that retires it (owner's word, finding or spec
  id) named in the commit line `role-rules: retire <id> -- <whose word>` (F6-a); none — finding. (After the waves, TD-5.4
  checks the presence of that line as data; the meaning of the word stays the critic's.)
- A changed anchor: the new anchor still names the SAME rule (`rule` field vs the new words); an anchor re-pointed to an
  unrelated phrase while the rule's sentence disappeared is a finding — code cannot see it (blind spot, §6 E-19).
- A rule wrapped into an HTML comment in a role text: the reader still counts it (§3.2, E-24) — the critic reads it as a
  rule removed unless the diff names the retiring word.
- A role-text diff that adds a duty without a row, a new pin test or a negative control in a test: finding (TESTING.md).
- A row whose `carriers` lost a twin: a twin dropped is a rule dropped for that role.

## 6. Edges (each with its invariant)

Error direction of the gate: it may err RED (a rewording, a casing the fold does not cover, an em dash for a hyphen, an
emphasis mark inserted) — the refusal names the row and the door; it must never err GREEN on a rule deleted from the text a
role reads. Adversarial inputs that must stay red: E-1..E-12, E-16, E-18, E-22; inputs that must stay green (no false red):
E-13..E-15, E-20, E-23, E-24 (E-24 is green by design and named as the critic's, §5.2).

| # | Input | Behaviour | Invariant protected |
|---|---|---|---|
| E-1 | `<REG>` absent (after TD-5.1) | one register-level finding `(absent)`, exit 1 | an absent register never reads as 0 rows |
| E-2 | `<REG>` 0 bytes, not UTF-8, not JSON, not an object, `rows` missing or not a list, `schema_version` != 1 | one register-level finding with its `<why>` (§3.1), no row checked | an unreadable register never passes |
| E-3 | `rows: []` | pass, prints `role-rules: 0 rows - no rule of a role is guarded` | empty never claims coverage |
| E-4 | row missing a key, unknown key, wrong type, empty `rule`/`source`, bad `id` form, `carriers` empty, anchor empty or under 2 or over 6 words or over 80 chars, `rule` over 300 chars or multi-line | schema finding; the row is not searched | a malformed row never counts as holding |
| E-5 | duplicate `id` | finding naming both rows | an id names one rule |
| E-6 | two rows, same carrier, same folded anchor | finding "merge them" | one rule, one row (a retire of one row cannot hide behind the other) |
| E-7 | carrier path absolute, with `..`, a backslash, or outside §2.4 homes | finding | only files a role reads are carriers |
| E-8 | carrier file missing (renamed, deleted) | finding naming row and path; never skipped | a moved text is followed by its row in the same diff |
| E-9 | carrier unreadable / not UTF-8 / JSON carrier not JSON | finding with its `<reason>` | an unreadable carrier never holds a rule |
| E-10 | anchor absent | the "lost" finding (§3.3) | a cut rule is never silent |
| E-11 | anchor present 2+ times | the "ambiguous" finding | deleting the rule always turns red |
| E-12 | anchor only inside a package marker comment (`<!-- kind: … -->`, `<!-- roles: … -->`, `<!-- gen… -->`, `<!-- /gen -->`) | the "only in a marker" finding | a marker is the package's metadata, never the place a rule lives |
| E-13 | anchor inside a fenced code block | counts | fenced text is delivered to the role (templates, examples) |
| E-14 | anchor wrapped across lines, indented, CRLF, U+00A0 | found (fold) | layout never reads as a loss |
| E-15 | case differs (sentence-initial capital) | found (casefold; the count is casefolded too) | capitalisation is a rewording, not a loss |
| E-16 | twin carrier lost the anchor, the other holds it | finding names the lost carrier and `still held by:` the others | a twin dropped is a rule dropped for that role (AR-19) |
| E-17 | `.json` carrier: anchor only in a KEY | not found (values only) -> lost | a key name is not text a role reads as a rule |
| E-18 | generated slice regenerated without the rule's section | finding on the slice; door: mark the section for that role (`<!-- roles: -->`) or remove the slice carrier with the word that says the role no longer needs it | a rule leaving a role's slice is a rule leaving that role |
| E-19 | row deleted, or anchor re-pointed to an unrelated phrase | not detectable by `role_rules.py` (by design) | critic §5.2; named blind spot. The row-deletion half becomes data-checkable by the TD-5.4 commit-msg gate after the waves (an id in `HEAD:<REG>` missing from the staged `<REG>` needs a `role-rules: retire <id> --` line) |
| E-20 | anchor on a `# ...` comment line of a handoff `.yaml` | counts | handoff guidance comments are delivered |
| E-21 | rule legitimately retired | row removed in the same diff + the retiring word in the commit line (F6-a); the reader never reads history | retirement is visible in the diff, decided by the person's word, judged by the critic |
| E-22 | zero-width space or other non-whitespace char inside the anchor's words in the text | not found -> lost (red) | the safe side: a false red, never a false green |
| E-23 | anchor inside an ordinary HTML comment of a template (the guidance of `references/templates/requirements-register.md`) | counts | a comment a role reads raw is delivered text; one comment rule for every carrier |
| E-24 | anchor inside an ordinary HTML comment of any other carrier (an agent file, a phase, a reference), and the text between `<!-- gen… -->` and `<!-- /gen -->` | counts | the same single rule; a rule commented out is still in the role's input, and the critic judges it as a removal (§5.2) |

Conflicting requirement pairs, resolved: exactly-once vs a carrier that states a rule twice -> choose words from one of the
two sentences that differ (§2.3; done in §4.4 for s4, s8, analyst and s7 keys counting 2), else `doubt:`; casefold vs
exactly-once -> the count is casefolded too, so a capitalised duplicate is a duplicate; marker stripping vs a rule inside a
comment -> only the four marker forms are stripped (E-12), every other comment counts (E-23, E-24); `red before:` vs "the
pin leaves only with its rows" (TESTING.md line 74) -> a pin file with a key under `red before:` or `doubt:` is not deleted
by TD-5.1 (§7.1).

## 7. Nodes

`<wt>` = the node's worktree root (branch `td/5-<n>` from `experiment/thinking-roles`; push before launch). Commit lines
(test-diet-brief form, adapted): `architecture: AR-1, AR-13, AR-15, AR-19, AR-23, AR-29 -- <how kept>`,
`judgment: adds data check role_rules.findings` (TD-5.1) / `judgment: none -- test files only` (waves),
`piles-skip: TD-5.<n> -- the owner's word 10.11.2026, docs/tasks/test-diet.md`, `[F15]`. TD-5.1 adds a duty for future
builders and a check: it is a mechanism commit (CLAUDE.md rule 10) — the four questions and the axis block are the Lead's
(§7.5); draft answers: (a) cost: one row per rule edit, paid by the editing builder; (c) detector of a leak: critic question 5
and calibration check 33; (d) on the path: CI `--tests`/`--fast`, and `selftest.py --limits` (F5-c).

### 7.1 TD-5.1 — builder (Sonnet): reader, register, test, the 12 files

- given: this spec; `docs/TESTING.md`; `docs/tasks/test-diet-brief.md`; the 12 pin files; `scripts/hooklib.py` (`read_json`);
  `scripts/gate_registry.py` head (house reader); `scripts/selftest.py` (`cmd_limits`); `scripts/contract_slices.py`
  (`ROLE_MARKER`, `KIND_LINE`, `_provenance`: the marker forms of §3.2); `scripts/tests/fixtures/judgment-census.json` and
  `scripts/tests/test_judgment_census.py`; `design/factory-rules.md` whole and `plans/builder-rules.md` (PROJECT.md p. 1).
- owns (absolute in the dispatch):
  `<wt>\ai-packages\qa-factory\scripts\role_rules.py` (new);
  `<wt>\ai-packages\qa-factory\design\role-rules.json` (new);
  `<wt>\ai-packages\qa-factory\scripts\tests\test_role_rules.py` (new);
  the 12 files under `<wt>\ai-packages\qa-factory\scripts\tests\` (delete only);
  `<wt>\ai-packages\qa-factory\scripts\selftest.py` (`cmd_limits` only);
  `<wt>\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows for `role_rules.py`);
  `<wt>\ai-packages\qa-factory\changelog.d\test-diet-td-5-role-rules.md` (new);
  `<wt>\plans\features.json` (the 9 names of §4.5 only).
- non-goals: no edit of any role text, reference, slice, handoff (a key that does not hold today goes to `red before:`, not
  repaired, and gets no row); no behaviour file (§4.6 is TD-5.2/TD-5.3); no `audit_factory.py`, no `CONTRACT_TESTS`; no forge
  doc; no edit of `CHANGELOG.md` or `experiments/driver-golden/MANIFEST.json`.
- What to do, per item (file, function, behaviour, test):
  1. `scripts/role_rules.py`: `load`, `findings`, the CLI, per §3.1-§3.3; tested by `test_role_rules.py` `CASES` (item 3).
  2. `design/role-rules.json`: the 104 rows of §4.2, §4.3 and §4.4, copied verbatim (id, rule, source, carriers in the listed
     order); tested by the shipped case and `role_rules.py --check`.
  3. `scripts/tests/test_role_rules.py`: one row of `CASES` per edge E-1..E-18, E-20, E-22, E-23, E-24 (E-19 and E-21 are
     named in the module docstring of `role_rules.py` as out of code); the shipped case.
  4. `scripts/selftest.py` `cmd_limits`: calls `role_rules.findings(PLUGIN_ROOT)`, prints each finding, fails on any; tested
     by the verification run `selftest.py --limits --lang` (green on the shipped tree).
  5. Census rows for each check unit of `role_rules.py` (§1.3); tested by `test_judgment_census.py`.
  6. Before deleting, run each of the 12 pin files once; then `git rm` each file whose every key is a row or a dropped kind,
     and remove its name from `plans/features.json` when it is one of the 9 of §4.5.
- Edge of the migration (Lead decision B1(c)): a key whose pin line is red before deletion (`python -B <wt>\…\<file>.py`
  reports it) gets NO row: the builder leaves out the row(s) built on that key, lists the key under `red before:` with the
  old pin's output line, and KEEPS that pin file and its `plans/features.json` line; the Lead decides. The same for an
  anchor of §4.4 that `role_rules.py --check` counts other than 1: that row is left out, listed under `doubt:` with the
  count, and its pin file kept. Invariant: a rule leaves its old guard only into a row or by the Lead's word (TESTING.md
  line 74). Expected under this revision: both lists empty.
- DoD:
  1. `<REG>` holds the rows of §4.2-§4.4 verbatim, minus any row named under `red before:`/`doubt:`; the report gives, per old
     file, the three lists as in §4.4 (row ids / dropped with kind / `red before:`) and the count line.
  2. Each of the 12 files run ONCE before deletion: `python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py`, summary
     lines verbatim in the report (a red line: under `red before:` with its key).
  3. The deleted files go in the same commit as the rows; `git -C <wt> grep -n -E "test_(scout_conflict_rule|time_fork_rule|case_role_twins|critic_lines_hf2|red_then_texts|s7_control_experiment_texts|mixed_then_texts|detection_role_texts|gate_continuation_texts|blocked_by_env_texts|recommended_rule|case_roles_twin_rules)" -- ai-packages/qa-factory/scripts plans/features.json`
     prints nothing, except the names of files kept under `red before:`/`doubt:` (positive control in the report: the same
     command with `role_rules` prints the new files).
  4. Every edge of item 3 is one row of `CASES`; E-19/E-21 are named in the module docstring.
  5. Refusal texts as §3.3 (the table asserts the id, the file and the door words of each).
  6. AR checks of §1.1; census rows; FR-30.
  7. Test lines <= product lines (reader + register) in the diff, else one reason line.
  8. The known-losses block of §4.4.13 copied into the report.
- verification (the witness, verbatim):
  `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_role_rules.py`
  `python -B <wt>\ai-packages\qa-factory\scripts\role_rules.py --check` (expected summary: `role-rules: 104 rows, 138 carriers checked, 0 finding(s)`)
  `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py`
  `python -B <wt>\ai-packages\qa-factory\scripts\selftest.py --limits --lang`
- edges: §6 entire; the migration edge above.
- handoff: report file named in the dispatch (builder-rules 11 form).

### 7.2 TD-5.2 — scout (Sonnet), read-only: the inventory of role-text pins in behaviour files

- question: for every file of the §4.6 sieve plus every file named in `docs/tasks/test-diet.md` TD-5, list each role-text
  pin (function or line), its kind (rule -> proposed row with carrier and a candidate anchor checked unique by
  `role_rules.py --check` on a scratch copy of `<REG>` outside the tree / data join -> keep / dropped kind of §4.1), and the
  file's line count. A file with no role-text pin gets a line `none: <why>`.
- completeness: every sieve file has a line; the TD-5 named files are present even where the sieve misses them.
- DoD: the table in the handoff file; the sieve command and its file count verbatim; the positive control (the sieve finds
  a known pin file).
- handoff: `<wt>\docs\tasks\handoffs\td-5-2-inventory.md` (report path, not owns).
- Runs after TD-5.1 is merged (it uses the reader).

### 7.3 TD-5.3.k — builder (Sonnet) waves: migrate behaviour-file pins

- Wave composition: the Lead cuts the inventory into waves (TD-4 precedent: up to ~6 500 test lines per wave, under the
  250K worker cap); waves are sequential (F7 decided: `очередь: TD-5.3.1 -> TD-5.3.2 ...`), all write `<REG>`.
- given: this spec §2-§4, §6; `docs/tasks/test-diet-brief.md`; the wave's rows of the inventory; the wave's files.
- owns: the wave's test files (edit; `git rm` when emptied, then its `plans/features.json` line) and `<REG>` (append rows).
- non-goals: no behaviour check removed or weakened (test-diet-brief "What you never do"); no role text edited; no reader
  change.
- DoD: every pin of the wave's inventory rows is a register row, a dropped-kind line or a `red before:` line; each check
  deleted in the same commit as its rows; per owned file the before/after summary lines (test-diet-brief "Witness");
  `role_rules.py --check` clean.
- verification: `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_role_rules.py` and, per owned file still present,
  `python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py` before and after (a `slow_tests.json` file above 60 s is
  edited by reading and judged by the wave's CI, test-diet-brief "Edges").
- edges: §6 (rows), plus test-diet-brief "Edges" (mixed check: remove only the pin lines; unused helpers removed).

### 7.4 TD-5.4 — builder (Sonnet), forge tool: the retire-line gate (AFTER the migration waves; R3, Lead decision 6)

Not part of TD-5.1. A commit-msg data gate: a row id present in `HEAD:<REG>` and absent from the staged `<REG>` must have a
line `role-rules: retire <id> -- <whose word>` in the commit message. It is a join (the `tools/architecture_gate.py`
pattern): it checks the presence of the line and the id, never the meaning of the word (that stays the critic's, §5.2;
AR-29-clean; owner served: data (code), class xref).

- given: this spec §2.2, §5.2, §6 E-3/E-19/E-21; `tools/architecture_gate.py` (house pattern of a commit-msg gate reading
  the message file); `tools/test_architecture_gate.py` (house test form); `.githooks/commit-msg` (read only).
- owns: `<wt>\tools\role_rules_gate.py` (new); `<wt>\tools\test_role_rules_gate.py` (new).
- non-goals: no package file; no edit of `.githooks/commit-msg` — the builder hands the hook line
  `python tools/role_rules_gate.py "$1"` as content in the report and the Lead puts it on the live path (enforcement-file
  review rule, CLAUDE.md rule 2); no judgment of the retiring word.
- What to do, per item:
  1. `tools/role_rules_gate.py main(msg_file) -> int`: reads ids from `git show HEAD:ai-packages/qa-factory/design/role-rules.json`
     and from `git show :ai-packages/qa-factory/design/role-rules.json` (the index); every id missing from the index needs a
     line matching `^role-rules: retire <id> -- \S` in the message; prints one FR-1 refusal per missing line (what is
     missing, the expected line, the door: add the line naming whose word retires the rule, or restore the row) and exits 1;
     exit 0 otherwise. Test: one parameterised table in `tools/test_role_rules_gate.py` over pure functions fed with the two
     JSON texts and the message.
- edges (each with its invariant): `<REG>` absent in HEAD (before TD-5.1) -> exit 0, nothing to compare (the gate guards
  only an existing register); `<REG>` not staged / unchanged -> exit 0; the staged `<REG>` deleted or holding `rows: []` ->
  every HEAD id needs its line (an emptied register is every rule removed, E-3); staged `<REG>` unreadable JSON -> one
  refusal "the staged register cannot be read" (never a pass on an unknown); an id renamed (old id gone, new id present) ->
  the old id needs its retire line (a rename is a removal plus an addition; the critic judges); a merge commit
  (`git rev-parse --git-path MERGE_HEAD` exists) -> exit 0 (the removal passed its own branch's gate); a retire line for an
  id still present -> a note line, exit 0 (not a removal).
- DoD: the test table covers every edge above; the refusal names the id and the expected line; mechanism commit with the
  axis block and the four questions written by the Lead.
- verification: `python -B <wt>\tools\test_role_rules_gate.py`.
- handoff: report file named in the dispatch, with the hook line as content.

### 7.5 Lead edits (forge rule carriers; not builder owns)

`plans/builder-rules.md` 7d (drop «до его появления — существующий пин остаётся» after TD-5.1); `docs/tasks/test-diet-brief.md`
row "role-text pin -> KEEP UNTOUCHED" becomes "migrate by `docs/tasks/specs/td-5-role-rules-register.md` §4.6" once TD-5.1
lands; `docs/tasks/critic-diff-brief.md` question 5 gets §5.2; the SIBLING_MAP placement (§10); the hook line of TD-5.4 on
`.githooks/commit-msg` at its acceptance. No path edit is owed (§2.1).

## 8. Forks

### 8.1 Decided (Lead, 10.11.2026)

- **F1 — anchor form.** Decided (Lead, 10.11.2026): (A) 2-6 of the rule's own words, unique in the carrier. (B) markers and
  (C) hybrid are not used; a rule with no unique 2-6 words goes to `doubt:`.
- **F2 — where the register lives.** Decided (Lead, 10.11.2026): (b) `design/role-rules.json`.
- **F3 — absence, count and position keys.** Decided (Lead, 10.11.2026): (a) dropped; a positive sentence of a ban is a row;
  the known losses are listed (§4.4.13).
- **F4 — exactly once vs at least once.** Decided (Lead, 10.11.2026): exactly once.
- **F5 — wiring.** Decided (Lead, 10.11.2026): (c) the test file plus `selftest.py --limits`; never `audit_factory`, never
  `CONTRACT_TESTS`.
- **F6 — how a retirement is recorded.** Decided (Lead, 10.11.2026): (a) the row is removed in the same diff with the commit
  line `role-rules: retire <id> -- <whose word>`; the critic judges; the line's presence becomes a data gate in TD-5.4.
- **F7 — waves on one shared register.** Decided (Lead, 10.11.2026): (a) sequential.
- **F8 — `OWNER_WORD_FA`.** Decided (Lead, 10.11.2026): (a) dropped with the file. The facts (critic t-2257 Q3, read on their
  carriers for this revision): FA-10 was answered on 28.10.2026 — HF5-16 in
  `plans/piles/hotfix-12586/batch-5-run-12586-manual-red-then-bugs.md:61` (the red-by-bug Then goes last; no commenting
  when reordering is possible; accepted 818bba85); its meaning stands in other words at `skills/qa-story/phases/s7.md:148`
  ("Nobody comments out the red"), guarded by the row `red-never-commented-out`. FA-11 took the soft-assert road (batch 6,
  `plans/piles/hotfix-12586/README.md:35`, closed 855d4e5c), so `K3a-sub` is an option nobody took. The sub-keys K2a, K2b
  and `K3a-sub` count 0 in the rubric and the automator today; no role text depends on the flag. They are dropped as
  absence (F3). The live key K3a ("move independent Thens before the red one") is NOT one of them: it is a row (§4.4.7).

### 8.2 Revision-2 decisions applied (Lead, 10.11.2026)

- B1: only the package marker comments are stripped; every other comment counts in every carrier (§3.2).
- B1(c): a key that does not hold today gets no row; `red before:` with the old pin's output; the Lead decides (§7.1).
- B2: the five completeness fixes (§4.4.1, §4.4.2, §4.4.7, §4.4.11).
- B3: §4.4 is a row table (§4.4).
- R1, R2, R4, R5, R6, R7 as the critic wrote; R3 as the separate node TD-5.4, after the waves.
- `plans/features.json` loses the 9 names it lists in the deleting commit (§4.5).

### 8.3 Open questions

None. Checked for decision B1's instruction: no carrier makes an anchor of this spec count other than 1 under the matcher of
§3.2 — every count of §4.2-§4.4 was taken with comments included, and no hit sits inside a `kind`/`roles`/`gen` marker. No
key was found whose anchor cannot be made unique in 2-6 words.

## 9. Small choices closed here (no design weight)

- One `carriers` list covers single and twin carriers (no separate `twins` key).
- Case-insensitive match (casefold) with the casefolded count (E-15).
- Fenced blocks and YAML `#` lines searched (E-13, E-20).
- `.json` carriers: string values only, recursively; no `file#key` addressing (exactly-once already catches a phrase shared by
  two cards).
- Generated carriers: the row carries the SOURCE file, plus the slice the old pin read (§2.4) — the dispatch edge "point at
  the source" and the slice guard of E-18 both hold.
- A pointer to a rule (the critic's pointer to the blocked-row rubric rule, the conductor's pointer to the recommendation
  rule, the automator's and the contract's pointers to dimension 8) is a twin carrier of the rule it points at — one
  verdict for the class (B2.3).
- A pin file with a `red before:` or `doubt:` key stays undeleted in TD-5.1 (TESTING.md line 74).
- Anchor hard bound 2..6 words / 80 chars; `rule` <= 300 chars, one line.
- Reader is a new script `scripts/role_rules.py` with `--check` only (TESTING.md: a new test file only for a new script).
- JSON read through `hooklib.read_json` (AR-13); duplicate KEYS inside one JSON object are not detected (`json.loads` keeps
  the last) — a named blind spot, rather than a second parser.
- Waves migrate the KEYS the pins hold; they do not invent new rows for unpinned duties. (§4.4 adds anchors for rules a pin
  guarded through single words or a pointer — the rules were pinned; only the words are new.)
- The marker regex of §3.2 is one line per marker; a multi-line comment is never a marker.

## 10. Reported, not widened (analogs and contradictions in the brief)

- The brief's caps: `agents/*.md <= 9000 B` is no longer a violation — `scripts/selftest.py` lines 355-365 print it as a
  note; the real bound of a role is audit A22 in tokens (`references/role-load.json`, `process_ratchet_tokens` slack 0).
  `plans/builder-rules.md` item 5 still states the 9000 B cap and A22 "42000 bytes" (stale against `role-load.json`).
- The brief names SIBLING_MAP axis 31 "role carriers": axis 31 covers the FORGE's role carriers (`.claude/agents/*.md`,
  builder-rules, critic brief), not the package's `agents/*.md`; axis 32 is the judgment census. The package role-text
  register has no axis yet: a new axis or a row on 32 is a Lead-tier write.
- Forge analogs of the same pattern (TD-8 territory): `tools/install_parity_anchors.json` (anchor lists per role file),
  `tools/tests/test_role_carriers_one_owner.py`, `tools/test_handoff_rule_anchors.py`.
- `test_conductor_investigates_first.py` mixes role-text pins (K1-K3 anchors) with a data join (K4 marker -> `person-owned.json`):
  inventory material, the join stays.
- `test_oracle_provenance.py` already addresses a card as `<file>#<role>` (lines 66-75) — a sibling reader the register
  replaces in TD-5.3.
- `docs/tasks/test-diet-brief.md` tells pruning nodes to keep role-text pins untouched — it needs the §7.5 edit when TD-5.1
  lands, or TD-4 waves and TD-5.3 waves contradict each other.
- `docs/tasks/test-diet.md:64` still says "F8 — сверить статус FA-10/FA-11": stale after §8.1 F8 (a Lead line).

## 11. Reading trail

Revision 1: `docs/TESTING.md` (whole); `docs/tasks/test-diet.md` (whole); `docs/tasks/test-diet-brief.md` (whole); the 12 pin
files (whole); `references/role-load.json`; `references/gate-registry.json` (head); `scripts/gate_registry.py` (1-90);
`design/architecture.md` (AR-1, AR-29, AR-13..AR-18); `design/factory-rules.md` FR-1/2, FR-13..15, FR-38/39, FR-44;
`docs/SIBLING_MAP.md` axes 31-33; `plans/builder-rules.md` items 5-14; `scripts/selftest.py` (`cmd_homes`, `cmd_limits`,
`CONTRACT_TESTS`); `scripts/release_fingerprint.py` (1-40); `scripts/role_load.py` (`craft_split`); `scripts/hooklib.py`
`read_json`; `judgment-census.json` (head); `agents/qa-failure-analyst.md`; `tools/install_parity_anchors.json` (head);
`test_oracle_provenance.py` 55-94; `test_conductor_investigates_first.py` (header, SITES).

Revision 2 (this designer, t-2262): the critic's review `docs/tasks/specs/reviews/td-5-plan-critic.md` (whole); the 12 pin
files (whole, again); `docs/TESTING.md:64-89`; `plans/builder-rules.md:46-50`; `scripts/contract_slices.py:1-80` (marker forms,
provenance line, `handoff-keys.md`); `references/templates/requirements-register.md:40-69`; `skills/qa-story/phases/s4.md:36-43,
208-221`; `skills/qa-story/SKILL.md:120-129`; `skills/qa-story/phases/s7.md:72-81, 108-123, 140-151, 228-259`;
`agents/qa-case-critic.md:60-69`; `handoffs/s6-runner-to-analyst.yaml:112-117`; `references/artifact-contract-automation.md:60-71`;
`references/code-review-rubric.md:44-47`; `plans/piles/hotfix-12586/batch-5-run-12586-manual-red-then-bugs.md:61`;
`plans/piles/hotfix-12586/README.md:35`.
Searches (Grep tool, case-insensitive, multiline, `\s+` between words, comments included): every anchor of §4.2-§4.4 in its
carrier (counts in the tables); the marker comment forms in `agents/qa-scout.md`, `agents/qa-code-critic.md`; the
`ahead-cards.json` string around the anchor (`-o`); `code_says`, `blocking_check`, `"thens"`, `retracted_unresolved`,
`ASSERT_STRICTER` in non-test `scripts/*.py` (readers found — each search is itself positive); the 12 names in
`plans/features.json` (9 found; the 3 absent ones are a negative claim backed by the same pattern finding the 9);
`role-rules` in the forge carriers (all three say `design/`); `python` lines of `.githooks/commit-msg`; the house test of
`architecture_gate.py` (Glob).
Needed beyond the manifest: `scripts/contract_slices.py`, `scripts/*.py` readers of the dropped tokens, `plans/features.json`,
`plans/piles/hotfix-12586/*`, `plans/builder-rules.md`, `.githooks/commit-msg`, `tools/test_architecture_gate.py`.
