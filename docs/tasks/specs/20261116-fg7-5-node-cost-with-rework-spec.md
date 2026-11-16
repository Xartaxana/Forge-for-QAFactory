# FG7-5 -- the price of an accepted node, rework included (`forge_metrics --node-cost`) -- DRAFT

task: t-898 | node: forge/7/FG7-5 | feature: F19 | drafted by: designer (Opus 5.5), 17.11.2026 | status: DRAFT, forks open, for Lead acceptance

Source: `plans/piles/forge/findings/20261104-tsena-uzla-s-brakom-v-forge-metrics.md` («Что сделать» items 1-3, owner's word 04.11.2026);
batch line `plans/piles/forge/batch-7-vhodyashchie-4.md:28`. Principles: P18, FR-41, FR-51, FR-55, P27.

Everything written below as "the builder does X" is executable on the RECOMMENDED option of each fork (PROJECT.md «Командная
работа» п. 11); the forks list (§7) says what changes if the Lead picks otherwise.

---

## §1 What changes, and whom it serves

**Change.** `tools/forge_metrics.py` gains ONE new, print-only mode `--node-cost`: it groups the journal's dispatches by
NODE (a pile node, or a task when no node is linked), prices every dispatch from its worker transcript, and prints (a) one
table row per node of the window, (b) the top 5 most expensive ACCEPTED nodes with their reasons as journal facts,
(c) the lines "not measured", "shared" and the totals. The existing modes (bare report, `--write`, `--json`, `--check`)
change by NOT ONE byte of output (invariant I-1 below).

**Owner served (P27 / AR-29 vocabulary, applied by analogy -- this is not a package file):** DATA (code). The code
joins and sums; it never says WHY a node was expensive. The reason column holds counts of journal events only
(rejects by `failure_class`, critic passes, repeated delegations, escalations, defects after acceptance). The judgment
"why, and what to cut" belongs to the calibration role (FG7-6), accepted by the Lead -- finding item 2: «причина — факт
из журнала, а не вывод кода о том, "почему дорого"».

**Package / AR-n.** `ai-packages/qa-factory/` is NOT touched (owns are two `tools/` files), so designer rule 1's AR-n /
census clause does not apply: `architecture: none -- outside the package`. The forge-side equivalents it keeps:
one reader per fact (transcripts through `tools/transcripts.py`, SIBLING_MAP axis 14 closing rule, `docs/SIBLING_MAP.md:351`;
the node through `journal_keys.node_of`; the task key through `journal_keys.task_key`/`ref_key`; prices through
`usage_report.load_prices` + `usage_report.accounted_cost`, the tools side of axis 14 row "request-parts reader",
`docs/SIBLING_MAP.md:345`).

**Mechanism status (CLAUDE.md rule 10).** `tools/forge_metrics.py` is on the mechanism gate's path list
(`tools/mechanism_gate.py:253`: `"tools/forge_metrics.py",       # .githooks/pre-merge-commit ...`), and the mode feeds
the weekly calibration -> treat as a mechanism: the commit carries the axis block and a `tier:` line (Lead writes them);
the builder leaves the tree STAGED if the gate asks for `tier:` (`plans/builder-rules.md` item 18).
(c) detector: calibration check 31 (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:951-962`) reads `forge_metrics`; FG7-6 adds
the node-cost form there (not in this node). (d) on the path: nothing gates it -- a measurer; "on discipline alone"
with check 31 as the leak detector.

---

## §2 The data join

### 2.1 Inputs (all read-only)

| Input | Read through | Premise (carrier) |
|---|---|---|
| every journal file (history + `logs/journal/<dev>.jsonl`) | `journal_keys.load_all(root)` -> `Journal` (`rows`, `segments`, `label_ids`, `aliases`); events are `LabeledEvent` with the file label | `tools/forge_metrics.py:843-853` already loads it this way in `compute()` (t-581); `tools/journal_keys.py:864-904` |
| task key `(label, task_id)` | `journal_keys.task_key(obj, journal.segments)`; display `journal_keys.display(key)` (`t-505`, `t-505@dev2`) | `tools/journal_keys.py:502-512`, `:548-551` |
| node of a `delegated` line | `journal_keys.node_of(obj)` -> `(node | None, reason)` (field first, else ONE notes token; two tokens -> None, never guessed) | `tools/journal_keys.py:238-260` |
| a `ref` / a cited task id | `journal_keys.ref_key(token, carrier_obj, segments, journal.label_ids, journal.aliases)` | `tools/journal_keys.py:525-545`; same call as `forge_metrics.py:742-743` |
| `replaces_worker:` marker | `journal_validator.extract_replaces_worker(notes)` | `tools/journal_validator.py:434` (hop_metrics uses the same reader, `tools/hop_metrics.py:132`) |
| worker transcript of `agent:<id>` | `transcripts.find_agent_transcripts(ids, root=projects)` -- ONE walk; None for unsafe id / no match / 2+ matches | `tools/transcripts.py:111-128` ("a measurement on the wrong file is worse than none", `:99`) |
| per-request token parts | `transcripts.request_parts(path, skipped=<list>, counts=<dict>)` | `tools/transcripts.py:448-477` |
| price of one part | `usage_report.accounted_cost(model, input, output, cache_creation, cache_read, prices, cache_creation_1h_tokens)` -> `(cost | None, None)`; `prices = usage_report.load_prices(path)` raises `PricesError` | `tools/usage_report.py:575-602`, `:326-390`; prices file `tools/model_prices.json` (`"as_of": "2026-10-16"`) |

The agent id of a `worker_ref` is `ref[len("agent:"):]` when `ref` starts with `agent:` and
`transcripts.agent_file_name(id)` is not None (`tools/transcripts.py:84-88`) -- no new regex. (Analog noticed, not fixed
here: two copies of the agent-ref regex already differ -- `tools/hop_metrics.py:88` `^agent:([A-Za-z0-9_-]+)$` vs
`tools/journal_echo.py:308` `^agent:([a-z0-9-]+)$`.)

The journal carries NO token counts: `Grep -i "subagent_tokens|total_tokens" logs/journal/dev1.jsonl` -> 0 hits;
positive control, same tool and file: `"witness"|subagent_tokens|total_tokens` -> 480 hits. So the finding's
«`subagent_tokens` уведомлений» are not a journal carrier; the worker transcript is the only cost carrier this node
uses (a second, independent source for P18's equality check is fork F5).
The journal carries no test-run count either (event SHAPES table, CLAUDE.md «Routing log»: no such field), so the
finding's «число прогонов тестов, если журнал его несёт» is not printed -- it does not carry it.

### 2.2 Which dispatches form one node (the grouping rule)

A DISPATCH = one `delegated` line. A TASK = all events of one task key. A ROW = one node of the report.

1. **Same task id** (retries `attempt` >= 2, `replaces_worker:` replacements, a critic-entry under the same id, e.g.
   `logs/journal/dev1.jsonl:1302` critic on `t-505`): one task -> always one row. No link needed.
2. **Own node.** A task whose `delegated` lines yield a node through `node_of` (first non-None, line order -- the same
   rule as `hop_metrics.load_chains`, `tools/hop_metrics.py:117-118`) is a member of row `<node>`. All tasks with the
   same node are ONE row (several builder tasks of one pile node merge).
3. **Attachment by explicit token** (only for a task with NO own node):
   - a `critic:t-NNN` token in the `notes` of an `accepted` or `rejected` line of task X, where `t-NNN` resolves (via
     `ref_key`, carrier = that line) to a task that HAS a `delegated` line with `agent == "critic"` -> that critic task
     attaches to X's row. Semantics = journal_echo S5: the token on an acceptance names the critic verdict that covers it
     (`tools/journal_echo.py:1877-1895`). A token naming a task with no critic `delegated` links nothing (one warning).
   - a `defect_found` line with `ref` R: the defect line's own task (when it has `delegated` lines, i.e. the fix work)
     attaches to R's row (`ref_key` with carrier = the defect line).
4. **Resolution.** An attached task goes to the row of its target (transitively: the target's own row). Attached to
   exactly ONE row -> member of that row. Attached to TWO OR MORE distinct rows (a bundling critic pass covering several
   nodes, CLAUDE.md rule 3 / journal_echo S5) -> SHARED: it is in no row's total; every citing row names it in its reason
   ("shared t-528"), and the "shared" line prints its cost ONCE (fork F4).
5. **Unlinkable.** Prose is NEVER parsed for links ("fix round after critic t-521", "FV1-19 N1", "Covers t-519"): a task
   with no node and no token attachment is its own row named by its task display (`t-515`). The summary counts these
   "rows with no node and no link token" -- reported, never guessed (FR-41; node_of's I4 rule).
6. **Not a dispatch.** `accepted`, `rejected`, `escalated`, `returned`, `defect_found` add no cost; they feed status and
   reasons only. Events with no task id are ignored by this mode (they belong to no node).

Measured scale of the linking carriers (Grep counts on `logs/journal/dev1.jsonl`, the only journal file of this clone;
`logs/routing-log.jsonl` is absent here -- Glob `logs/*.json*` lists 4 files, none of them it):
`"event":"delegated"` 1005 lines; of them with a `"node":"` field 339; lines `accepted|rejected|delegated` holding a
`critic:t-<digit>` token 225. So roughly two thirds of dispatches have no node field: the "unlinked" count will be large
at first and is itself a calibration reading.

### 2.3 Status of a row

- A task's OUTCOME = its last `accepted`/`rejected` event in journal order; `accepted` -> accepted, anything else (only
  rejects, or no outcome event) -> open.
- A row is `accepted` iff EVERY member task (own + attached, shared excluded) is accepted; otherwise `open`.
  (An attached defect-fix task that is still open makes the row open: its price is not final -- invariant I-4.)
- `defect_found` lines whose `ref` resolves to a member task are counted as "defects after acceptance" of the row.

### 2.4 Price of a dispatch

For a `delegated` line with an agent id and ONE transcript:
`tokens` = sum over `request_parts` parts of `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`;
`cost` = sum of `accounted_cost(part["model"], part["input_tokens"], part["output_tokens"], part["cache_creation_input_tokens"],
part["cache_read_input_tokens"], prices, part["cache_creation_1h_tokens"])[0]`.

`unmeasured` reasons (codes reuse `hop_metrics`' vocabulary, `tools/hop_metrics.py:27-34`):
`bad_ref` (worker_ref absent or not `agent:<id>`: old lines, `cli:`, `retro:`), `no_transcript` (none or 2+),
`unreadable` (OSError), `no_usage` (request_parts returned []), `bad_usage` (`skipped` list non-empty: those lines are not
priced), `unpriced:<model>` (a part whose `accounted_cost` is None -- the KNOWN parts stay summed, the dispatch is PARTIAL).
`same_worker` (the agent id already priced on an earlier `delegated` line): measured, cost 0 here, note "priced on line N".

**Error direction (designer rule 1: reused functions in a more consequential role -- `accounted_cost` and
`request_parts` move from usage advice to a RANKING).** The node cost may err HIGH, never LOW silently:
`request_parts` over-counts a keyless line as its own request by design ("an over-count is allowed, an under-count is not",
`tools/transcripts.py:303-304`); every source of a LOW figure (no transcript, unpriced model, skipped usage line, a
`cli:` ref) is NAMED as unmeasured/partial and makes the row's cost print as `>= $X`. Adversarial inputs that must stay
on the safe side: a worker_ref of another worker's id (two transcripts -> `no_transcript`, never the wrong file); an id
with a glob metacharacter (`agent:a*`) -> `bad_ref`; a model absent from the price file -> `unpriced`, never $0;
a usage value `"12abc"` -> `bad_usage`, never a traceback; one transcript cited by two lines -> priced once.

---

## §3 The output

### 3.1 CLI

`python -B tools/forge_metrics.py --node-cost [--window YYYY-MM-DD] [--json] [--projects-root DIR]`

- `--window`: the existing flag and `_normalize_window` (`tools/forge_metrics.py:1318-1321`); default `DEFAULT_WINDOW`
  (`"2026-09-26"`, `:71`). The calibration passes its own window start.
- `--json`: prints `node_costs()`'s dict (sorted keys, indent 1, as `:1360`) to stdout.
- `--projects-root DIR`: the transcripts root (default `transcripts.projects_root()`); a test never touches the home
  folder (hop_metrics precedent, `tools/hop_metrics.py:54`).
- `--node-cost` together with `--write`, `--out` or `--check` -> exit 2, one stderr line:
  `forge_metrics --node-cost: prints only -- money is never written to a repository file (P18); drop --write/--out/--check`.
- `--node-cost` does NOT read `plans/features.json` (a missing registry does not block it).

### 3.2 New functions (in `tools/forge_metrics.py`, new section `# node cost` before `# report`)

```python
TOP_NODES = 5

def node_costs(root, window, projects=None, prices=None) -> dict
def render_node_costs(d: dict) -> str
```
`node_costs` imports `transcripts` and `usage_report` LAZILY inside its body (invariant I-2). `prices` = a dict from
`usage_report.load_prices`; None -> `usage_report.load_prices()` (default file). The dict:

```
{"window": "2026-11-10", "prices_as_of": "2026-10-16", "source": "worker transcripts",
 "rows": [{"row": "forge/7/FG7-4" | "t-505", "kind": "node" | "task", "status": "accepted" | "open",
           "tasks": ["t-505", ...], "dispatches": 4, "unmeasured": [{"task": "t-505", "line": 1241,
           "file": "logs/journal/dev1.jsonl", "worker_ref": "...", "why": "no_transcript"}],
           "tokens": 0, "cost": 0.0 | None, "partial": false,
           "rejects": {"spec": 2, "capability": 0, "recon": 0, "tooling": 0, "unclassified": 0},
           "critic": 1, "redelegations": 2, "replaced": 0, "escalations": 1, "defects": 0, "shared": ["t-528"]}],
 "shared": [{"task": "t-528", "cited_by": ["t-519", "t-530"], "tokens": 0, "cost": 0.0 | None, "partial": false}],
 "top": ["forge/7/FG7-4", ...],
 "totals": {"rows": 0, "accepted": 0, "open": 0, "unlinked": 0, "dispatches": 0, "measured": 0, "unmeasured": 0,
            "tokens": 0, "cost": 0.0, "partial": false},
 "warnings": ["..."]}
```
Field meanings: `critic` = member `delegated` lines with `agent == "critic"`; `redelegations` = per task, non-critic
`delegated` lines beyond the first, summed (attempt >= 2 and replacements alike); `replaced` = those carrying
`replaces_worker:`; `escalations` = member `escalated` lines; `rejects` = member `rejected` lines by `failure_class`
(absent or a value outside the four -> `unclassified`); `defects` = 2.3; `cost` None only when NO dispatch of the row
was priced; `partial` true when any dispatch is unmeasured or partially priced.

### 3.3 Exact text (`render_node_costs`)

```
## Node cost (printed, never written: P18)
window: since 2026-11-10; source: worker transcripts (tools/transcripts.py); prices: tools/model_prices.json as_of 2026-10-16 -- API list price of the tokens, an estimate, not a bill
rows 42 (accepted 35, open 7; 21 with no node and no link token); dispatches 118: measured 109, unmeasured 9; total >= $123.45, tokens 98765432
| row | status | dispatches | unmeasured | tokens | cost | rejects | critic | redelegations | escalations | defects after acceptance |
|---|---|---|---|---|---|---|---|---|---|---|
| forge/7/FG7-4 | accepted | 5 | 0 | 4567890 | $12.34 | 2 (spec 2) | 2 | 2 (replaced 0) | 1 | 0 |
| t-777 | open | 1 | 1 | 0 | n/d | 0 | 0 | 0 (replaced 0) | 0 | 0 |

Top 5 accepted nodes by cost (journal facts; why it cost that is the calibration's judgment):
1. forge/7/FG7-4 $12.34 (5 dispatches, 0 unmeasured) -- rejects 2 (spec 2), critic passes 2, redelegations 2 (replaced 0), escalations 1, defects after acceptance 0
2. t-505 >= $8.10 (4 dispatches, 1 unmeasured) -- rejects 2 (spec 2), critic passes 1, redelegations 2 (replaced 0), escalations 1, defects after acceptance 0; shared t-528

not measured: t-505 line 1241 (no_transcript), t-777 line 1400 (bad_ref cli:2026-11-12T10:00:00)
shared (counted once, in no row): t-528 $1.20 cited by t-519, t-530
```
Rules of the text: rows sorted by known cost descending, then row name ascending; `cost` cell `$%.2f`, `>= $%.2f` when
partial, `n/d` when None; `rejects` cell `N` plus ` (spec a, capability b, recon c, tooling d, unclassified e)` listing
only non-zero classes, `0` alone when none; the "total" prints `>= ` when any dispatch is unmeasured; the
"not measured" list is capped at `TOP_N` (10, `tools/forge_metrics.py:72`) entries plus `(+N more)`; the "shared" line
is omitted when there is none. Top 5: only `accepted` rows with `cost` not None, ranked by known cost (a partial row
ranks by its known part and prints `>=`). Fewer than 5 -> those that exist; none -> the line
`Top 5 accepted nodes by cost: none in the window`. Empty window -> header, the line
`rows 0; dispatches 0 -- no nodes in the window`, no table, and the "none in the window" top line; exit 0.

### 3.4 Worked example -- task t-505 (real lines, `logs/journal/dev1.jsonl`)

| line | event | agent / model | attempt | worker_ref | link facts |
|---|---|---|---|---|---|
| 1241 | delegated | builder sonnet | (1) | agent:a6c661e08a242c74f | no `node` field; notes "FV1-19 N1 ..." is not a node token (upper-case slug, NODE_TOKEN_RE `tools/journal_keys.py:116` wants `[a-z]...`) |
| 1267 | rejected | builder | 1 | -- | failure_class spec |
| 1268 | delegated | builder sonnet | 2 | agent:a1897d0194789fedc | |
| 1269 | delegated (task t-515) | critic opus | -- | agent:a7afec76e62a1c680 | separate task; notes "Code critic on FV1-19 N1" -- prose only |
| 1282 | rejected | builder | 2 | -- | failure_class spec; notes "rejected on critic t-515 B1" -- a SPACE, not the `critic:t-515` token |
| 1283 | escalated | builder opus | -- | -- | |
| 1284 | delegated | builder opus | 3 | agent:aaa221fc8cef1bbff | |
| 1302 | delegated | critic opus | -- | agent:a2711aed8cb19fd1f | critic-entry under the SAME task id |
| 1307 | accepted | builder, basis critic | -- | -- | notes hold no `critic:t-` token |

Result by §2: row `t-505`, `accepted`, dispatches 4 (1241, 1268, 1284, 1302), rejects 2 (spec 2), critic passes 1,
redelegations 2 (replaced 0), escalations 1, defects after acceptance 0. The code critic `t-515` is NOT linked: its own
row `t-515` (accepted at line 1281, 1 dispatch, critic 1) and counted among "rows with no node and no link token". That
gap is the real finding this example shows: the price of t-505 in this mode excludes its first critic, and the report
says so by listing t-515 as a separate unlinked row, never by guessing the link. (A `node` field example for the
merge rule: `t-525`, line 1298 `"node":"project-knowledge/2/PK2-9"`, accepted line 1304.)

Transcripts: Glob `*/*/subagents/agent-{a6c661e08a242c74f,a1897d0194789fedc,aaa221fc8cef1bbff,a2711aed8cb19fd1f,a7afec76e62a1c680}.jsonl`
under `C:/Users/i_mas/.claude/projects` -> exactly one file each, all in session `61b75a79-16bf-492f-9cd2-02266607001d`.
**Costs NOT measured by the designer**: this role has no shell (tools: Read/Glob/Grep/Write), so neither
`hop_metrics` (which, besides, prints weighted units, not money, and cannot select t-505 by `--node` -- it has no node)
nor a pricing run could be executed. The builder's report attaches the live line for `t-505` from
`python -B tools/forge_metrics.py --node-cost --window 2026-11-13` as a smoke reading (report text, not a test).

---

## §4 Edges -- behavior and the invariant each protects

| # | Edge | Behavior | Invariant |
|---|---|---|---|
| E1 | open node (a member task has no `accepted` as last outcome) | row printed with status `open`; never in the top 5 | an unfinished price is never ranked against finished ones |
| E2 | a task with `delegated` but no `accepted`/`rejected` at all | outcome open (E1); its dispatches still priced in totals | every dispatch of the window is in the totals once (I-3) |
| E3 | a task with only outcome events and no `delegated` (e.g. old retro accepted) | a row with dispatches 0, cost `n/d`, not in the top 5 | no row prints $0.00 for "nothing measured" |
| E4 | task id reused across clones (`t-505` in dev1 and dev2) | two task keys, two rows (`t-505`, `t-505@dev2`) via `task_key`/`display`; an undeclared collision INSIDE one file is glued, as every hook reads it (`forge_metrics.py:686-690`) and the existing stderr line about an unreadable declaration is printed (`:857-859`) | a link or price never crosses to another clone's task unless it names that label (`ref_key` rule) |
| E5 | `defect_found` after acceptance | counted in "defects after acceptance"; the defect line's task, if it has `delegated` lines, attaches to the ref's row; while that fix is open the row is `open` | a late defect never lowers or hides the node's price; a closed task is never "reopened" -- the fix is its own task inside the row |
| E6 | `defect_found` whose `ref` resolves to nothing (`ref_key` None or an unknown key) | a warning line `defect_found line N: ref <r> names no task`; the defect task stays its own row | an unresolvable ref never links |
| E7 | transcript missing / ambiguous / unreadable / no usage / bad usage / unpriced model | `unmeasured` entry with its code; row `partial`, cost `>= $X` (or `n/d` if nothing priced) | an unknown is never printed as zero (FR-41) |
| E8 | lines older than the typed fields (no `worker_ref`, no `attempt`, no `failure_class`, no `node`) | `bad_ref` unmeasured; reject -> `unclassified`; redelegations counted from line count, not from `attempt`; task row named by its id | old lines are read as what they say, never back-filled |
| E9 | `worker_ref` of another kind (`cli:`, `retro:`, `job:`) | `bad_ref` with the ref text in the "not measured" list | only an agent transcript is a price carrier |
| E10 | the same agent id on two `delegated` lines | priced once; the later line `same_worker` | one transcript is never priced twice (I-3) |
| E11 | a critic task cited by `critic:` tokens from two different rows | SHARED (§2.2 step 4) | total = sum of row totals + shared, each dispatch once (I-3) |
| E12 | a `critic:t-NNN` token naming a task with no critic `delegated` (or a task of another clone) | no link; one warning line | a token links only a real critic dispatch (S5 semantics) |
| E13 | two different node tokens / a bad `node` field (`node_of` reasons `two_tokens`, `node_not_form`, `node_not_string`) | no node from that line; a warning line `t-NNN: <reason>` (hop_metrics precedent `:121-122`); a later line may still give the node | a link is never guessed |
| E14 | a task whose lines give two DIFFERENT valid nodes | the first (line order) wins, a warning `t-NNN: two nodes <a>, <b>` | one task, one row |
| E15 | window | a row is in the report iff at least one of its events has `ts[:10] >= window`; ALL its events count, also those before the window | a node's price is never cut at the window edge |
| E16 | empty journal / no journal file (fresh clone, cutover O3) | the "no nodes in the window" text, exit 0 | absence is a printed fact, not an error |
| E17 | journal lines that are not JSON | skipped by `load_all`; one stderr line `forge_metrics: N journal line(s) unreadable` | nothing raises |
| E18 | price file missing/malformed (`PricesError`) | exit 2, one stderr line `forge_metrics --node-cost: <the PricesError text>`; nothing printed on stdout | an unreadable table never reads as $0 (`usage_report.py:336-338`) |
| E19 | `--projects-root` given but not a directory | exit 2, `forge_metrics --node-cost: --projects-root <p> is not a directory`; the DEFAULT root missing (a machine with no `~/.claude/projects`) is NOT an error: every dispatch `no_transcript` | a bad argument is refused, a missing carrier is reported |
| E20 | a live worker (transcript still growing) | priced as read now; its task is open (E1) | a moving figure is never ranked |
| E21 | `--node-cost` with `--write`/`--out`/`--check` | exit 2, the §3.1 line | money is never written to a repo file (P18) |
| E22 | more than `TOP_N` unmeasured dispatches | first 10 in line order, then `(+N more)`; `--json` carries all | truncation is announced |
| E23 | a row whose known cost ties another | ordered by row name | deterministic output for one repo + transcripts state |

Conflicting-requirement pairs, resolved: (i) "sum every attempt by task_id" vs a critic pass shared by nodes ->
shared bucket (E11, fork F4); (ii) "price of an ACCEPTED node" vs "print open nodes" -> table shows all, the top 5 only
accepted (E1); (iii) "the calibration reads it" vs P18 -> stdout only, refused with `--write` (E21, fork F2).

**Temporal (CLAUDE.md rule 11 (i)).** No artifact is created by this change; the price file and the journal exist
before and after. **Positional (11 (ii)).** The `--node-cost` branch in `main()` goes BEFORE the `--check` branch
(`tools/forge_metrics.py:1338`) and before `compute()` (`:1356`); invariant: with `--node-cost` absent, every existing
path runs exactly as today (I-1), and with it present neither `compute()` nor `run_check()` runs and nothing is written.

**Invariants pinned by the tests (§5):**
- I-1 the bare report, `--write`, `--json` (without `--node-cost`) and `--check` produce today's bytes (no node-cost key in
  `compute()`'s dict, no line in `render_markdown`).
- I-2 `import forge_metrics` imports neither `transcripts` nor `usage_report` (the hooks `.githooks/pre-commit:38`,
  `.githooks/pre-merge-commit:17` and `tools/piles.py:105`'s load-time import stay as light as today).
- I-3 totals.cost == sum(row costs) + sum(shared costs), and every `delegated` line of the window's rows is counted in
  exactly one of: a row, the shared bucket.
- I-4 a row is in the top 5 only if `accepted` and its cost is not None.

---

## §5 Tests (`tools/test_forge_metrics.py`, `docs/TESTING.md` layer 3 "money"; one parameterised table per behaviour)

No new test file (`docs/TESTING.md:118`); journal and transcripts built under `tmp_path` with the existing `ev_line`
helper (`tools/test_forge_metrics.py:101-105`) and a tiny transcript writer (assistant lines with `requestId`, `model`,
`usage`); a tmp price file with two models (prices are data of the test, never the live file -- no pin of a measured
constant, `docs/TESTING.md:95`). The world is built once per table (a module-level fixture), checks are rows.

**T1 `test_node_cost_grouping_and_price` -- parametrize, one row per case (ids name the case):**

| id | journal + transcripts | expected |
|---|---|---|
| `two_attempts_and_critic_same_id` | t-001 builder (a1), rejected spec attempt 1, builder attempt 2 (a2), critic (a3), accepted | one row `t-001`, accepted, dispatches 3, cost = sum of 3 workers, rejects {spec:1}, critic 1, redelegations 1 (finding item 1's expectation) |
| `node_field_merges_tasks` | t-001 and t-002 both `node: forge/7/FG7-9`, both accepted | one row `forge/7/FG7-9`, tasks [t-001, t-002] |
| `critic_token_attaches` | t-001 accepted with notes `critic:t-002`; t-002 critic delegated | t-002 inside row t-001 |
| `critic_token_two_rows_is_shared` | t-001, t-003 accepted, both notes `critic:t-002` | t-002 in `shared`, cited_by [t-001, t-003]; I-3 holds |
| `critic_token_to_non_critic_links_nothing` | notes `critic:t-002`, t-002 is a builder | two rows, one warning |
| `prose_is_not_a_link` | t-002 critic, notes "critic on t-001" (space) | two rows; totals.unlinked counts both |
| `defect_after_acceptance` | t-001 accepted; t-004 `defect_found ref t-001` + t-004 builder delegated, open | row t-001 status open, defects 1, tasks [t-001, t-004] |
| `missing_transcript_is_unmeasured` | worker a9 has no file | unmeasured `no_transcript`; row cost n/d, partial (finding item 1: «не молчит») |
| `cli_ref_and_old_line` | `worker_ref: cli:...`; a rejected with no `failure_class` | `bad_ref`; rejects {unclassified:1} |
| `unpriced_model_is_partial` | one part with a model absent from the tmp price file | known part summed, partial, `unpriced:<model>` |
| `same_worker_twice` | two delegated lines with agent:a1 | priced once; second `same_worker` |
| `clone_collision_two_rows` | t-001 in dev1 and dev2 files | rows `t-001@dev1`/`t-001` as `display` gives them, never merged |
| `window_keeps_row_whole` | row's first dispatch before window, accepted inside | row present, cost includes the early dispatch |

**T2 `test_node_cost_render` -- parametrize over rendered cases:** `empty_journal` (the "no nodes" line and
`Top 5 accepted nodes by cost: none in the window`; finding item 3's «пустой журнал»), `six_accepted_top_is_five_with_reasons`
(order by cost, the exact reason line of §3.3), `open_row_not_in_top`, `partial_prints_ge`, `ties_by_name`,
`more_than_ten_unmeasured_announced`.

**T3 `test_node_cost_cli_doors` -- parametrize over argv (input from outside: the adversarial mini-battery of rule 11):**
`--node-cost --write` -> 2 + the P18 line, nothing written; `--node-cost --check` -> 2; `--node-cost --window 2026-13-99`
-> the existing window refusal; `--node-cost --projects-root <file>` -> 2; a broken price file -> 2, one stderr line,
empty stdout; `--node-cost --json` -> valid JSON with the §3.2 keys; `--node-cost` with no `plans/features.json` -> 0.

**T4 `test_node_cost_import_stays_light`** -- a subprocess `python -I -c "import sys; sys.path.insert(0,'tools'); import
forge_metrics; print(sorted(m for m in ('transcripts','usage_report') if m in sys.modules))"` prints `[]` (precedent:
`tools/test_digest_form.py:731-737`). I-2.

I-1 is held by the existing K8 tests (`tools/test_forge_metrics.py:636-661`) staying green; no new "as before" test
(`docs/TESTING.md:97`).

---

## §6 The builder stream (one)

task: t-898 (designer); builder task id issued at dispatch | node: forge/7/FG7-5 | feature: F19
given: `tools/forge_metrics.py`, `tools/test_forge_metrics.py`, `tools/journal_keys.py` (task_key, ref_key, node_of,
display, load_all), `tools/transcripts.py` (find_agent_transcripts, agent_file_name, request_parts), `tools/usage_report.py`
(load_prices, accounted_cost, PricesError), `tools/journal_validator.py` (extract_replaces_worker), `tools/journal_echo.py:1877-1895`
and `:1960` (S5 semantics, CRITIC_TOKEN_RE), `tools/hop_metrics.py:1-56,102-125` (precedent: reason codes, n/d discipline),
`docs/TESTING.md`, `plans/builder-rules.md`, this spec.
owns:
C:/QAFactory/forge-repo/tools/forge_metrics.py
C:/QAFactory/forge-repo/tools/test_forge_metrics.py
non-goals: `tools/hop_metrics.py`, `tools/transcripts.py`, `tools/usage_report.py`, `tools/journal_echo.py` (read, not
changed); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (FG7-6); coordinator turns / SendMessage per node (FG7-7, fork F3);
a second cost source (fork F5); the package; `plans/forge-metrics.md` (never regenerated by this node).
edges: §4 E1-E23 and invariants I-1..I-4.
DoD: §5 T1-T4 green; the existing tests of the file green; the report names the live line for `t-505`.
Verification run (owned path outside the package -> the test file that judges it, CLAUDE.md rule 4; no
`scenario_walk.py` row covers `tools/`): `python -m pytest tools/test_forge_metrics.py -q`.
siblings: SIBLING_MAP axis 14 (a new reader of agent transcripts imports `transcripts` -- this one does); axis 14 row
"request-parts reader" (`docs/SIBLING_MAP.md:345`: the price rule is `request_parts` + `accounted_cost`, no copy);
`hop_metrics` (the same chain/node notion, units not money -- not changed; fork F1); `session_retro` (stays apart: it
counts a MAIN session's turns, `tools/session_retro.py:1-10`, with no task link -- nothing reused).
handoff: builder report per `.claude/agents/builder.md` rule 7; tree STAGED for the Lead if the mechanism gate asks `tier:`.

Critic: rule 3 -- the diff is likely > 100 lines and carries money accounting -> critic mandatory (money: start with
EMPIRICS -- control values on the T1 world).

### Readers of every touched file (designer rule 3)

Commands (Grep tool) and counts:
- `forge_metrics` over `tools/` -> 60 hits in 16 files; over `.githooks/` -> 2 hits (`pre-commit:38`, `pre-merge-commit:17`);
  over `.claude/settings.json` -> 0 (positive control `journal_echo`, same file -> 1); over `.claude/agents/` -> 0
  (control `handoff` -> 8 hits / 3 files). Hits under `.claude/worktrees/*` are other branches' copies, not readers.
- `test_forge_metrics` over `tools/` -> 2 hits (its own docstring; a comment in `test_journal_per_developer.py:11`).
- Changed names: only NEW names (`node_costs`, `render_node_costs`, `TOP_NODES`, `--node-cost`, `--projects-root`); no
  existing name changes, so readers of existing names are judged by I-1/I-2.

| Reader | What it reads | Verdict |
|---|---|---|
| `.githooks/pre-commit:38`, `.githooks/pre-merge-commit:17` | `forge_metrics.py --check` | unchanged (I-1, I-2: no new import on the hook path) |
| `tools/piles.py:105` | `from forge_metrics import BaseError, compile_glob, parse_backlog_text, resolve_base` at load time | unchanged (names kept; I-2 keeps the load light) |
| `tools/collect_intake.py:49,859-907,1130` | load_registry, FileIndex, walk_files, _file_tokens, TAG_RE, _features_of_tokens, compile_glob, RegistryError | unchanged |
| `tools/piles_split.py:39,285-544` | FileIndex, tracked_files, package_files, walk_files, load_registry, RegistryError, BACKTICK_RE, BARE_PATH_RE, classify_path, CLOSED_RE | unchanged |
| `tools/test_journal_fresh_clone.py:27` | `compute()` on a clone with no journal | unchanged (I-1) |
| `tools/test_digest_form.py:734` | asserts digest_form does not import forge_metrics | unchanged |
| `tools/test_hop_metrics.py:802` | asserts hop_metrics does not import forge_metrics | unchanged (forge_metrics does not import hop_metrics on the recommended F1) |
| `tools/test_workflows.py:149-150`, `tools/test_journal_validator_merge.py:1333-1339` | the `--check` command strings in CI/hooks | unchanged |
| `tools/mechanism_gate.py:253` | the path is a mechanism path | the commit carries the axis block (Lead) |
| `tools/journal_validator.py:239,314-318,1438,1751`, `tools/md_table.py:4,8`, `tools/test_piles_findings.py:5`, `tools/test_gitcmd.py:130`, `tools/test_journal_per_developer.py:11` | comments/docstrings naming the module | unchanged |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:951-962` (check 31; outside the grep scope, read because it is the consumer) | how calibration runs forge_metrics | changes in stream FG7-6 (the node-cost form); see the contradiction note in §8 |

---

## §7 Forks (returned, not decided)

**F1 -- where the mode lives.** `tools/hop_metrics.py` already groups `delegated` lines by pile node (`load_chains`,
`:102-125`), locates each worker's transcript in one walk (`locate`, `:166-184`) and measures usage with the n/d
discipline -- and it says "no money is printed anywhere (P18)" (`:20`).
(a) `forge_metrics --node-cost` using the shared PRIMITIVES (`journal_keys`, `transcripts`, `usage_report`) and not
importing hop_metrics -- **recommended**: the owner's word and the batch line name `forge_metrics`; the grouping here is
by task with outcome events (hop_metrics' groups only `delegated` and only by node), so it is not a copy of
`load_chains`; hop_metrics' import chain (dispatch_manifest, handback_extract, digest_form) stays out of a module that
`piles.py` imports at load. Cost: two measurers that both know "a hop of a node"; the line "node of a task = first
node_of of its delegated lines" exists twice (3 lines) -- named in both docstrings.
(b) a `--node-cost` mode in `hop_metrics` -- one measurer of chains, but owns change (hop_metrics + its test), against
the node text, and hop_metrics' units become money.
(c) forge_metrics imports `hop_metrics.load_chains`/`locate` -- one grouping, but a heavy import (lazy), and
load_chains drops outcome events, so the task grouping is rebuilt anyway.

**F2 -- money or units.** (a) USD from `accounted_cost` plus raw tokens, ranking by USD, printed to stdout only, refused
with `--write` -- **recommended**: P18 forbids money in repository FILES ("Деньги в файлы репозитория (отчёт) не
пишутся", PROJECT.md P18), not on a terminal; tokens of Opus and Sonnet are not comparable, so a ranking by tokens mixes
tiers; the finding asks for «цена». Cost: FG7-6's form must say the calibration copies counts and ranks, not dollars,
into any repo file. (b) tokens (or hop_metrics' weighted units) only -- no money anywhere, the hop_metrics precedent;
the ranking is then cross-tier and misleading. (c) both, USD behind an extra flag.

**F3 -- FG7-7 in the same spec?** FG7-7 asks for coordinator turns per node: repeated `delegated` (+ `replaces_worker`)
AND worker resumes by `SendMessage` (`findings/20261104-khody-koordinatora-na-uzel-v-tsene.md:11-12`).
(a) keep FG7-7 separate; FG7-5 already prints the journal half (`redelegations`, `replaced`), FG7-7 adds the
`SendMessage` column later through the same `node_costs` -- **recommended**: SendMessage lives in the MAIN session
transcript, which needs a per-task join of the parent session (hop_metrics' Lead side, `:302+`), a separate risk;
FG7-7's expectation «событие без task_id — строка "без узла"» is compatible. Cost: FG7-7 re-opens the same two files
after FG7-5 (queue `FG7-5 -> FG7-7`, already the batch's dependency, `batch-7...md:30`). (b) one spec for both --
one pass over the files, but doubles the scope and drags in the main-transcript scan. `session_retro` is reused by
neither: it counts per main session (operator messages, compactions, `Agent` re-dispatch by description,
`tools/session_retro.py:71-141`) with no task id.

**F4 -- a critic pass shared by several nodes.** (a) SHARED bucket, counted once, named on each citing row --
**recommended**: P18's "sum of costs = the whole" holds (I-3) and nothing is invented. (b) split evenly between the
citing rows -- every row gets a number, but the split is a guess (FR-41). (c) full cost on every citing row -- the
column sum exceeds the spend, a P18 defect.

**F5 -- a second, independent cost source (P18: "равенство из двух независимых источников").** The finding names
"`subagent_tokens` notifications" (the usage the harness reports to the parent session). (a) not in this node; a new
finding in `forge/findings/` for the cross-check (worker transcript vs parent-session notification) -- **recommended**:
the notification lives in the main transcript (same join as F3); this node prints its single source on the header
line ("source: worker transcripts"). (b) do it now -- doubles the reader work.

**F6 -- the `critic:t-NNN` token grammar.** It lives in `tools/journal_echo.py:1960` (`CRITIC_TOKEN_RE`), a hook
module. (a) build the same pattern in forge_metrics from `journal_keys.ID_PATTERN` and add ONE table row asserting
`forge_metrics`'s pattern equals `journal_echo.CRITIC_TOKEN_RE.pattern` -- **recommended**: the precedent of the
`closes:` regex copies pinned equal by a test (`tools/journal_keys.py:99-101`); no hook import. (b) import
`journal_echo` lazily -- one copy, a heavy hook import. (c) move the regex to `journal_keys` -- the clean survivor,
but `journal_echo.py` is outside the owns (a second stream).

**F7 -- what links count.** Recommended set: same task id, `node` field / single node token, `critic:t-NNN` on
accepted/rejected, `defect_found.ref`. Not used: `closes:` (closes phantoms, not work), prose. Option: also accept a
`critic:` token on the critic's OWN `delegated` line ("Covers t-519: critic:t-528", `dev1.jsonl:1303`) -- that token
names the critic itself, so it carries no target; recommended NOT to use it (the target is prose).

---

## §8 Small choices closed by the designer (no design weight)

- `TOP_NODES = 5` constant beside `TOP_N`; the "not measured" list reuses `TOP_N` (10).
- Exit 2 for the node-cost refusals, as the module's existing "nothing is written" code (`forge_metrics.py:33-34`).
- Reason codes reuse `hop_metrics`' names; new ones: `unpriced:<model>`, `same_worker`.
- Row name = node string or `journal_keys.display(task key)`.
- Tokens printed as plain integers (no locale separators); cost `$%.2f`.
- `--node-cost` does not need the feature registry.
- The new section sits before `# report` in the module; lazy imports inside `node_costs`.

## §9 Noticed analogs / contradictions (reported, scope not widened)

1. `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:953-954` says `python tools/forge_metrics.py` "(rewrites `plans/forge-metrics.md`)";
   `main()` writes only with `--write` (`tools/forge_metrics.py:1361-1367`). Check 31's text is stale -- for FG7-6 / Lead.
2. Two agent-ref regexes disagree (`hop_metrics.py:88` vs `journal_echo.py:308`, upper case and `_` allowed or not).
3. A builder-tier fix round under a NEW task id with the link only in prose (`t-524` "fix round after critic t-521",
   `dev1.jsonl:1296`) is unlinkable by any token: a journal convention gap (a `node` field on every pile-node dispatch, or
   a `fix-of:t-NNN` token) that this measurer will expose but cannot close -- a finding for the Lead.
4. The finding's «402K» figures are context SIZES (agent_budget's last usage, `tools/transcripts.py:226-228`), not
   cumulative spend; the node cost here is cumulative, so it will not reproduce those numbers.
5. Freshness: the root checkout is at `26dcf3d6` (session git status); the `read-main` worktree named by the machine
   memory does not exist (Grep on `.claude/worktrees/read-main/tools/forge_metrics.py` -> path does not exist); origin
   divergence NOT verified (no shell) -- estimate, not verified.

## §10 Reading trail

Read whole or in part: the finding (all); `tools/forge_metrics.py` (1-1373); `tools/test_forge_metrics.py` (1-112,
320-430, 620-670, def list); `tools/session_retro.py` (all); `tools/transcripts.py` (all); `tools/model_prices.json`;
`tools/usage_report.py` (270-640, imports); `tools/hop_metrics.py` (1-305, def list); `tools/journal_keys.py` (94-263,
481-555, 847-938, def list); `tools/journal_validator.py:385,434-440`; `tools/journal_echo.py:1860-1899,1956-1964,2074-2082`;
`logs/journal/dev1.jsonl` (lines 288-318 by grep t-113, 1241-1325 by grep t-505, 1290-1309 read, t-515 grep);
`plans/piles/forge/batch-7-vhodyashchie-4.md:1-30`; FG7-7 finding (all); `docs/TESTING.md:40-164`;
`plans/builder-rules.md` 7b/7d (grep); `docs/SIBLING_MAP.md:335-351`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:945-964,1025-1049`;
`ai-packages/qa-factory/scripts/tests/test-layers.json` (grep: no `test_forge_metrics`/`test_hop_metrics` row -- control
`tools/` -> 4 hits in the same file); Glob of the five t-505/t-515 transcripts.
Needed beyond the manifest: `tools/hop_metrics.py`, `tools/journal_keys.py`, `tools/transcripts.py`, `tools/usage_report.py`,
`tools/model_prices.json`, `tools/journal_echo.py`, `tools/journal_validator.py`, `logs/journal/dev1.jsonl`,
`docs/SIBLING_MAP.md`, `docs/TESTING.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, the FG7-7 finding, the batch file.

## Lead decisions on the forks (Lead, 17.11.2026)

F1 (a) `forge_metrics --node-cost` on the shared primitives; F2 (a) USD + tokens on stdout only, refused with `--write`
(P18); F3 (a) FG7-7 stays a separate node; F4 (a) a shared critic pass is counted once in a SHARED bucket; F5 (a) the
second cost source is a new finding, not this node; F6 (a) pattern rebuilt from `journal_keys.ID_PATTERN` with one
equality row; F7 the recommended link set, the critic's own `delegated` token is not used.
