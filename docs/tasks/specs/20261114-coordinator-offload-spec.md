# Coordinator offload: journal by code, safe for parallel sessions; test volume in the roles (draft, t-842)

status: DRAFT by designer (t-842) for Lead acceptance. Forks in §9 are RETURNED, not decided. Nothing here is accepted.
scope: forge tooling only. `ai-packages/qa-factory/` is out of scope, so no AR-n of `design/architecture.md` applies
(`architecture: none -- forge tooling` on every commit of this spec). CLAUDE.md rule 10 (four questions, axis enumeration)
applies: §7.

## 0. The owner's words (14.11.2026, verbatim)

1. «Координатор тратит много ходов для того что бы вести журнал. Нельзя это как-то оптимизировать? Например создать
   скрипт который будет автоматически вести лог начала и конца диспачей? И вообще как уменьшить количество ходов
   координатора не связанных с тем что может делать только ИИ»
2. «все эти пункты реализовать, но убедится что они будут работать если разрабатывают две параллельные сессии на одном
   компьютере»
3. On the hygiene rule «журнал пишется только через Edit/Write»: «это было правило для экономии токенов модели, так как
   сейчас писать будет код то экономия только больше. Я своим словом разрешаю»
4. On id collisions between parallel sessions: «придумать что-то что решить эту проблему. Например пусть добавляют буквы.
   Номер 123 и 123А»
5. New event `returned` for the end of a dispatch: «ок».
6. Test volume: «Перенести правило в роль билдера и критика, в роли билдера дать ссылку на файл тестинг. Убедиться что в
   файле тестинг есть объяснение как делать эффективные тесты на нашем проекте. Поставить варн хук на случай если строк
   тестов больше чем строк кода билдера». WARN placement (Lead's brief): a commit-msg hook.

Carrier of the words: the Lead's intent brief of t-842 (journal line `logs/journal/dev1.jsonl:2065`, notes). The words are
quoted from the brief; whether they were said in a session with the owner is the Lead's to confirm (PROJECT.md «Командная
работа» п. 6).

## 1. Corrections to the brief (facts read in the carriers; designer rule 3)

| # | Brief said / implied | The carrier says | Consequence |
|---|---|---|---|
| K1 | `dispatch_gate.py` "only reminds" that `dispatch_skipped` is owed | the reminder is `DESIGNER_SKIP_NOTE_TEMPLATE` in `tools/dispatch_manifest.py:155-157`; dispatch_gate calls the manifest | B2 reads the skip reason through the manifest's cut (one reader, axis 13) |
| K2 | B4: hygiene_gate must be taught a legal road | `hygiene_gate.py` refuses the journal only when a journal path is a LITERAL write target of a redirect / tee-like / in-place editor / python `-c` payload / .NET write (`_add_target` :1282-1291, `_dotnet` :1369-1374, `decide` :1515-1519). `python -B tools/journal_write.py ...` names no such target and already passes (CLAUDE.md hygiene pt.4a: a named committed script) | B4's CODE change is the refusal's door text (`MSG_JOURNAL_BLOCK` :82-85) and the `--run` guard (§3.B1 E-B1-9); the rule TEXT changes are Lead's |
| K3 | the writer's lines get the echo checks | `journal_echo.py` triggers ONLY on `tool_input.file_path` (:499-508, :2351-2352); a journal written from Bash is invisible to it (tier MISMATCH, witness echo, notes length, escalation echo) | fork F-B1-2 |
| K4 | a letter suffix only needs the validator | `journal_keys.CLOSES_RE = (?<!\w)closes:(t-\d+)(@[A-Za-z0-9_-]*)?` (:83) reads `closes:t-123a` as **closes t-123** — a FALSE CLOSE of the bare id; `REF_RE` (:75), `ID_NUM_RE` (:103), `BAND_RE` (:102), validator `TASK_ID_RE = ^t-(\d{3,})$` (:355) refuse or misread a letter; fallback copies of CLOSES_RE live in `session_context` and `calibration_counts` (pinned equal, journal_keys.py:81-82). Files holding a `t-\d` pattern (Grep `t-\\d|t-\(\\d|t-\[0-9\]` over `tools/*.py`, positive control journal_keys.py hit): journal_validator, journal_keys, session_context, journal_echo, compact_snapshot, calibration_counts, piles, dispatch_manifest (+ test_calibration_counts) | stream B0 owns all eight |
| K5 | a shared counter is enough | validator rule 9a: a brand-new id is EXACTLY the file's next id (`BandState.may_issue`, journal_keys.py:337-347). Two worktrees of one clone hold two COPIES of `logs/journal/<dev>.jsonl`; with one counter each copy sees gaps (t-900 here, t-901 there) and 9a refuses | rule 9a changes (§3.B5 D4) |
| K6 | builder.md lacks the volume rule | true, but `plans/builder-rules.md` 7d (:57-58) already carries it («строк теста в диффе не больше строк продукта (больше — причина строкой отчёта)») and `docs/tasks/critic-diff-brief.md` Q5 (:41-42) already has the finding | fork F-A1-1 (axis 31: one owner per aspect) |
| K7 | a SubagentStop hook can write `returned` beside dod_gate | dod_gate may BLOCK the stop (exit 2: no green run after the last edit, a missing handoff; dod_gate.py:12-30, :590-609). Hooks of one event run in parallel (Claude Code hook semantics — estimate, not verified here), so a sibling hook cannot know the stop was blocked | fork F-B3-1 |
| K8 | hook files are edited by builders | `.claude/settings.json` and `.githooks/commit-msg` are self-activating enforcement files (CLAUDE.md rule 2): the builder hands them as content / a neighbouring file, the Lead places them at acceptance | B2/B3 and A3 DoDs say so |
| K9 | worker_ref of the launch equals SubagentStop `agent_id` | hop_metrics finds `agentId: <id>` in the launch tool_result (:89, :345-347); dod_gate reads `agent_id` from the stop payload (:588); tier_echo documents the payload (tier_echo.py:9-17). That the two ids are the SAME string is an ESTIMATE, not verified; foreground order (SubagentStop before the parent's PostToolUse) is an estimate too | the first step of stream B23 is ONE measurement (CLAUDE.md hygiene 6a) |
| K10 | category values | the live journal uses builder→`implementation`, critic→`review`, scout→`recon`, designer→`spec` (dev1.jsonl:2053-2065) | the writer's data row (§3.B1) |

## 2. Streams, owned paths, order

Each stream is one future builder dispatch. Owned paths do not overlap between streams. Every builder works in its own
worktree; nothing is live until the Lead merges (a hook script edited in a worktree is not on the live path: the live
hooks run `python tools/<x>.py` from the root checkout).

| Stream | Owns (absolute; all under `C:\QAFactory\forge-repo\`) | Depends on | Wave |
|---|---|---|---|
| A1 | `.claude\agents\builder.md`, `.claude\agents\critic.md` | — | 1 |
| A2 | `docs\TESTING.md` | — | 1 |
| A3 | `tools\test_volume.py` (new), `.githooks\commit-msg.proposed` (new; content for the Lead), its test file (F-T1) | — | 1 |
| B0 | `tools\journal_validator.py`, `tools\journal_keys.py`, `tools\session_context.py`, `tools\journal_echo.py`, `tools\compact_snapshot.py`, `tools\calibration_counts.py`, `tools\piles.py` (only its `t-` id regexes), `tools\dispatch_manifest.py` (id regex + `designer_skip_reason` + the header lines of F-B2-1), `tools\forge_metrics.py` (event kind), and their test files (`tools\test_journal_validator.py`, `tools\test_journal_keys.py`, `tools\test_session_context.py`, `tools\test_journal_echo.py`, `tools\test_calibration_counts.py`, `tools\test_compact_snapshot.py`, `tools\test_dispatch_manifest.py`, `tools\test_forge_metrics.py`) | — | 1 |
| C1 | `tools\dispatch_new.py` (new) + its test file (F-T1) | B0's header grammar only if F-B2-1 = (a) | 1 |
| C2 | `tools\ci_read.py`, `tools\ci_read_common.py`, `tools\test_ci_read.py` | — | 1 |
| B1 | `tools\journal_lock.py` (new), `tools\journal_write.py` (new), `logs\journal-letters.json` (new), their test file(s) (F-T1) | B0 | 2 |
| B23 | `tools\journal_hooks.py` (new), `tools\dod_gate.py`, `tools\hygiene_gate.py` (door text + `run_allowed()`), `tools\mechanism_gate.py` (`MECHANISM_PREFIXES`), `tools\hook_liveness_probe.py`, `.claude\settings.json.proposed` (new; content for the Lead), test files `tools\test_dod_gate.py`, `tools\test_hygiene_gate.py`, `tools\test_mechanism_gate.py`, `tools\test_hook_liveness_probe.py`, + the hooks' own (F-T1) | B1 | 3 |
| C3 | `tools\wave.py` (new) + its test file (F-T1) | B1 (`journal_lock`) | 3 |
| L | rule texts: `CLAUDE.md`, `PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md`, `docs\SIBLING_MAP.md`, `DECISIONS.md` entry, `docs\tasks\critic-diff-brief.md` (if F-A1-1 = (a)), placement of `.claude\settings.json` and `.githooks\commit-msg` | B23, A3 | with wave 3 |

`AGENTS.md` is generated (`tools/agents_md.py`; pre-commit `--check` refuses a stale copy, SIBLING_MAP axis 4): every stream
that changes an agent file, `CLAUDE.md` or `.claude/settings.json` regenerates it on its branch; a merge conflict on it is
resolved by regenerating, never by hand (integrator's duty). No stream owns it.

Stream L lands ONLY through a Fable (full Lead) session: CLAUDE.md, the calibration protocol and DECISIONS.md are mechanism
paths (`tools/mechanism_gate.py`) whose commits carry a `tier:` line the gate refuses below the lead binding.

Wave 1 = six parallel writers (the cap, CLAUDE.md rule 12). Critic: one pass per topic (A, B, C); topic B touches the
journal schema → critic mandatory (rule 3); critic-on-plan for this draft is mandatory (a new idea of the owner, PROJECT.md
step 6).

## 3. Behaviour per stream

### A1 — the volume rule in the builder and critic roles

Behaviour (the text is in §6.1; F-A1-1 decides whether the role line is a pointer or the owner):
- `builder.md` gains rule 8: tests are written by `docs/TESTING.md`, link to it and to its how-to section (A2); the
  volume duty in one sentence, with the report line and the commit-message line `tests-over: <reason>` (A3's door).
- `critic.md` gains rule 20: tests are a standing question with its own verdict line, pointing at
  `docs/tasks/critic-diff-brief.md` question 5 (which already names the volume finding, :41-42).

Edges:
- E-A1-1 (conflicting pair: owner's «перенести» vs axis 31 «one owner per aspect»): F-A1-1. Invariant: after the change
  exactly ONE carrier holds the full rule text; every other carrier holds a duty sentence + pointer that cannot drift
  from it (the pointer names the section, not a paraphrased number).
- E-A1-2: rule numbering — rules are appended (builder 8, critic 20); no existing rule is renumbered, because
  `tools/test_handoff_rule_anchors.py`, `tools/tests/test_role_carriers_one_owner.py` and `tools/install_parity_anchors.json`
  pin role files by anchor. Invariant: every existing anchor still found.

Tests: no new test. Witness: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_agents_md.py -q`
and `python -B tools/agents_md.py --check`, plus the DOC-DISPATCH key-presence run (CLAUDE.md rule 11: keys quoted
verbatim from the DoD before the run, script attached in full, one negative control). Keys: `docs/TESTING.md`,
`tests-over:`, `critic-diff-brief.md question 5`.

### A2 — «Как писать эффективный тест на нашем проекте» in docs/TESTING.md

Behaviour: a new section (text §6.2) placed right after «### Что пишется — три слоя, и только они» and before «Чего больше
нет» is NOT where it goes — it goes after «### Бюджет» and before «### Когда тест покраснел», so that the how-to reads
after the rule and the budget it compiles. It only gathers what the file and its measurement already say; it adds no rule.

Edges:
- E-A2-1 (exclusion, owner's word pending): the paragraph «Время: … запуск подпроцесса на каждую проверку — дефект теста»
  (TESTING.md:124-125) is NOT edited; the new section says "one world per file" by pointing at «Бюджет», and names the open
  finding `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`. Invariant: the
  diff touches no line of «### Бюджет».
- E-A2-2: the section adds no number not already in the file (10 s, 60 s, ratio 1:1); a new measured number would need its
  carrier (hygiene 6b). Invariant: every number in the section appears elsewhere in TESTING.md.
- E-A2-3: forge tools tests (`tools/test_*.py`) — the section says where a tools case goes (the tool's test file, a row),
  pending F-T1.

Witness: DOC-DISPATCH key-presence run (keys: `### Как писать эффективный тест на нашем проекте`, `variants.json`,
`одна строка, которая падала до правки`, `20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`), and a
`git diff --stat` showing only TESTING.md; negative control mandatory.

### A3 — the test-volume WARN on commit

Behaviour: `tools/test_volume.py <msg-file>` reads the STAGED diff (`git diff --cached --numstat -M`), sums ADDED lines per
class, and prints ONE WARN line to stderr when `test_added > product_added` and the message carries no `tests-over:`
line with a non-empty reason. It ALWAYS exits 0. `.githooks/commit-msg.proposed` = the current hook plus, as its LAST line,
`python tools/test_volume.py "$1" || true`.

Classifier (data row in the tool, `CLASSES`, first match wins; paths as git prints them, `/`):
1. excluded: `docs/**`, `plans/**`, `logs/**`, `kb/**`, `**/changelog.d/**`, `.claude/**`, `.githooks/**`, `experiments/**`
   except `experiments/measurers/**`, root files (`*.md`, `*.yaml`, `.gitattributes`, …);
2. test: a path with a segment `tests` or `test` or `fixtures`, or a basename `test_*.py`, `*_test.py`, `conftest.py`,
   or `*_testkit.py`;
3. product: `ai-packages/**`, `tools/**`, `gateway/**`, `experiments/measurers/**` (code AND text: role files, phases,
   references count as product, as in TESTING.md's measurement table);
4. anything else: excluded.
Error direction (it is a WARN): unsure → product (fewer WARNs; the leak is caught by check 33's ratio, §7).

Edges (adversarial mini-battery: the message file and the staged diff come from outside):
- E-A3-1 merge commit: `MERGE_HEAD` exists in the git dir → silent, exit 0. Cherry-pick / revert are NOT exempt (door).
  Invariant: a merge never WARNs; a non-merge test-heavy commit without a reason always WARNs.
- E-A3-2 binary (`-\t-\t`) → skipped; a rename counts its added lines only.
- E-A3-3 `tests-over:` line: a line starting `tests-over:` (case-insensitive, leading spaces allowed), reason = rest after
  the colon stripped; empty reason → WARN says "reason empty"; lines starting `#` are ignored (git strips them).
  Invariant: a commented-out door never silences the WARN.
- E-A3-4 equality `test == product` → no WARN (the rule is "not more"). Both zero → silent. Product 0 and test > 0 → WARN.
- E-A3-5 the message file absent / unreadable / not UTF-8 → read with `errors="replace"`; absent → as no door.
- E-A3-6 git missing / not a repo / numstat fails → one stderr line `test_volume: not measured -- <reason>`, exit 0.
  Invariant: the tool can never change the hook's exit code (`|| true` and an outer try/except).
- E-A3-7 magnitude: a 50,000-line fixture capture → counted as test; the WARN prints the three numbers and the door.
- E-A3-8 POSITIONAL: last line of commit-msg, after the three refusing gates. Invariant: a commit a gate refuses prints no
  volume WARN first (no noise before the real refusal), and a refused gate is never masked (`set -e` stays).
WARN text (one line): `TEST VOLUME (WARN, the commit goes on): +<t> test lines vs +<p> product lines in this commit; name the reason in a line "tests-over: <reason>" of the message and in your report (docs/TESTING.md «Бюджет»).`

Tests: one parametrised table over (numstat text, message text, merge flag) → (warned, numbers); cases: equal, test>product,
door present, door empty, door commented, merge, binary, rename, excluded paths only, git failure. Witness:
`python -m pytest tools/test_test_volume.py -q` (name per F-T1).

### B0 — journal schema: the id with a letter, rule 9a, bands retired, the `returned` event

Behaviour:
1. ONE id grammar in `journal_keys`: `ID_RE = ^t-([0-9]{3,9})([a-z]{0,2})\Z` (ASCII class, `\Z`); `parse_id(s) -> (num, letter) | None`;
   `REF_RE`, `CLOSES_RE`, `ID_NUM_RE` rebuilt on it; `CLOSES_RE` ends with `(?![A-Za-z0-9])` before the optional `@label`.
   The validator's `TASK_ID_RE` imports it (no second copy); `session_context` / `calibration_counts` fallback copies are
   updated and stay pinned equal; `piles.py --task`, `dispatch_manifest` `resubmission t-<id>`, `compact_snapshot`,
   `journal_echo` read through it.
2. Rule 9a' (validator): a brand-new id is legal when its number is GREATER than every number already seen WITH THE SAME
   LETTER in the logical journal (seed + file), and at most `ID_JUMP_MAX = 1000` above that max. Gaps are legal. 9b-9d
   (repeats) unchanged, keyed by the full id (`t-123` and `t-123a` are two tasks).
3. Bands retired for NEW lines: a new line carrying `id_band` is a violation `band_retired` whose text names the door
   (`python -B tools/journal_write.py next`); old lines' bands still feed `BandState.top` (TEMPORAL). `where` prints the
   next id per letter from the file and says the counter of B1 is the issuer.
4. `returned`: in `EVENTS`; required fields `task_id`, `worker_ref`, `model`; the task must already have an open
   `delegated` with the SAME `worker_ref` earlier in the logical journal; at most one `returned` per (task, worker_ref);
   it is not a novelty-issuing event. Optional fields accepted on any event: `via` (`hook` | `cli`), `session` (≤ 16
   chars `[A-Za-z0-9-]`).
5. Open-dispatch reconciliation (`session_context.open_dispatches` and the session-handoff reader): `returned` NEVER closes
   a task; a task whose last lifecycle touch is `delegated` with a later matching `returned` is shown as
   `RESULT PENDING: t-NNN agent=X returned <ts>` (same 3-line cut, own first); without `returned` it stays `OPEN DISPATCH`.
6. `forge_metrics`, `calibration_counts`, `compact_snapshot` learn the event kind (SIBLING_MAP axis 6 row "Forge metrics").
7. The PARALLEL SESSION note (`journal_keys.peer_note`, read by session_context and journal_echo) no longer tells anyone to
   open a band: "ids come from the clone counter; nothing to do" when B1 is live (TEMPORAL below).
8. `dispatch_manifest.designer_skip_reason(cut) -> str | None` — the reason of a `designer: skip -- <reason>` header from the
   ONE cut (used by B23); the header grammar of F-B2-1 (a) if chosen.

Edges:
- E-B0-1 adversarial ids: `t-123A` (upper case), `t-123а` (Cyrillic а), `t-１２３` (fullwidth), `t-123abc` (3 letters),
  `t-12` (2 digits), `t-1234567890` (10 digits) → all NOT ids (form violation on a new line; `closes:` drops them).
  Invariant: no non-ASCII or upper-case id is ever accepted or closes anything.
- E-B0-2 `closes:t-123a` closes exactly `t-123a`; `closes:t-123` never closes `t-123a`; `closes:t-123ab@codex` resolves
  by label. Invariant: a token never closes an id other than the one it spells (K4 is the defect this prevents).
- E-B0-3 jump AT 1000 legal, 1001 refused; a gap of 1 legal. Invariant: a typo id far above the sequence is still refused.
- E-B0-4 an id issued twice in one file (the 13.11 race) is still refused as a duplicate under 9a' (it is not greater
  than the max). Invariant: removing "exactly max+1" never makes a reused id legal.
- E-B0-5 TEMPORAL: old journals — bare ids, bands, `<id>@<label>` declarations — validate exactly as today (old lines are
  never judged); the first new line after the switch with a gap is legal. Both worlds are tested on the same fixture.
- E-B0-6 `returned` without a matching open `delegated` (wrong worker_ref, closed task, no task) → violation naming the
  door (`journal_write.py returned --task … --worker …` is the only legal form). Invariant: a `returned` can never open,
  reopen or close a task.
- E-B0-7 merge mode (`--merge-parent`): two worktree copies with interleaved counter ids (t-900 in one, t-901 in the other)
  merge with no NOVELTY violation; the same id in both copies with different content is still the collision WARN/refusal
  of today.

Tests: rows in the existing tables of each owned test file (no new file): id grammar table (E-B0-1/2), 9a' table
(E-B0-3/4/5), `returned` table (E-B0-6), open-dispatch table (RESULT PENDING), merge row (E-B0-7). Witness:
`python -m pytest tools/test_journal_validator.py tools/test_journal_validator_merge.py tools/test_journal_keys.py tools/test_session_context.py tools/test_journal_echo.py tools/test_calibration_counts.py tools/test_compact_snapshot.py tools/test_dispatch_manifest.py tools/test_forge_metrics.py -q`
(`tools/test_piles.py` only its id rows, `-k` named by the builder in the report).

### B5 — parallel sessions on one machine (design; implemented in B0 + B1)

Who can write one journal number space, and what keeps them apart:

| Writers | Share | Today | After |
|---|---|---|---|
| two sessions, same worktree | one file | max+1 race (13.11) → bands by discipline | the machine lock + the clone counter |
| two sessions, two worktrees of one clone | the git common dir; two file copies | ids meet at the merge | the clone counter (one per common dir) |
| two clones (any machine), different developer slugs | nothing | file label `<id>@<label>` | unchanged: the file label is the READ key |
| two clones, the SAME developer slug (a second machine) | the file name | collision at the union merge | the clone LETTER |

D1 lock: `journal_lock.machine_lock(name, timeout)` — a lock file `<common>/forge-journal/<name>.lock`, where
`<common>` = `git rev-parse --git-common-dir` resolved against the repo root (absolute). Windows: `msvcrt.locking(fd,
LK_NBLCK, 1)` polled every 50 ms up to `timeout`; elsewhere (CI is Linux) `fcntl.flock(LOCK_EX|LOCK_NB)` — chosen by which
module imports (a capability, not a platform name). The OS releases the lock when the process dies: no stale lock. The
holder writes `pid ts` into the file for the refusal text. Names: `journal` (appends and id issue), `main-merge` (C3).
D2 counter: `<common>/forge-journal/counter.json` `{"<letter or empty>": <last issued number>}`; read and written only under
the `journal` lock; written by write-temp-then-`os.replace`. Next number = 1 + max(counter[letter], max number with that
letter in THIS worktree's logical journal, and on first use the max over every worktree copy listed by
`git worktree list --porcelain`). It never goes down.
D3 letter: the registry `logs/journal-letters.json` (tracked) `{"letters": [{"letter": "", "slug": "dev1", "clone":
"<uuid>", "since": "<ts>"}, …]}`; the clone id is `<common>/forge-journal/clone-id` (uuid4, created once). A clone's letter
= the row whose `clone` is its id. `journal_write.py clone --claim` adds the row: letter `""` when the slug has no row yet,
else the lowest free `a..z`, then `aa..zz`; it prints the `git add`/commit line (the row is shared only once committed and
pushed). Two clones claiming one letter offline conflict TEXTUALLY on the JSON at merge (rows are one per line, sorted by
letter) — the after-the-fact detector; F-B5-2 holds the scope question.
D4 rule 9a' (B0 item 2) replaces "exactly max+1": the lock removes the race the strict rule guarded, and worktree copies
legitimately skip.
D5 composition with the existing roads (P31: one road per action):
- issuing an id: ONE road — `journal_write` under the lock from the counter, with the clone letter. Retired for new lines:
  bands (`id_band`, validator rule 9e) and `where`'s "max+1" advice. Kept READ-ONLY for old lines: BandState over old bands.
- reading a task: ONE key — `(label, id)` of `journal_keys.task_key`; the letter is part of the id, the label stays the
  file's. `journal_keys.py declare` (segments) stays as the repair of COLLISIONS ALREADY IN HISTORY; a new collision
  cannot arise by construction, so a declaration covering a line dated after the switch is a WARN at `check`.
D6 TEMPORAL (both worlds; which move creates what):
- before B1 merges: no counter, no registry, no clone-id; the hand-written path of today stays (Edit/Write) and the
  validator already accepts gaps (B0 merges first). Bands written in this window are accepted? NO: B0 refuses new bands
  — so B0 and B1 merge in ONE wave boundary with B0 activated only together with B1 (the Lead merges B0 then B1 back to
  back before any session issues an id; F-ORD-1 holds the alternative).
- first `journal_write` call in a clone: creates `<common>/forge-journal/` (clone-id, counter from the max over worktree
  copies). No registry row → it REFUSES to issue an id (exit 2) with the door `journal_write.py clone --claim`; hooks print
  the same as a WARN and write nothing.
- after: every new id comes from the counter.

### B1 — the one writer `tools/journal_write.py` (library + CLI) and `tools/journal_lock.py`

CLI (all write ONE line to `journal_keys.current_path(root)` of the repo containing `--repo` or cwd):

| subcommand | writes | required args | notes |
|---|---|---|---|
| `next [--n K]` | nothing; reserves K ids (1..20) in the counter | — | prints the ids, one per line |
| `delegated` | `delegated` | `--agent --model --worker --notes`, `--task` (else a new id is issued) | `--node`, `--feature`, `--attempt`, `--replaces <worker_ref>` (written as the `replaces_worker:` token), `--category` (default from the agent row) |
| `returned` | `returned` | `--task --worker` | `--model` default = the matching `delegated`'s |
| `accept` | `accepted` | `--task --agent --model --by --notes`; for agent=builder exactly one of `--run "<cmd>"`, `--witness-file <path>`, `--witness "<text>"` | `--basis`, `--allow-red "<reason>"` |
| `reject` | `rejected` | `--task --agent --model --by --attempt --failure-class --notes` | |
| `skip` | `dispatch_skipped` | `--agent --notes` | `--task` named in notes as `t-NNN` |
| `escalate`, `defect`, `decomposable`, `degraded`, `restored`, `calibrated` | their events | per CLAUDE.md shapes | |
| `event --json '<obj>'` | any event | a JSON object without `ts` | the generic door for a rare or retro line ("retroactive" in notes) |
| `clone --claim` / `clone --show` | the registry row / nothing | — | D3 |

Common behaviour: take the `journal` lock (timeout 15 s CLI); read the logical journal (seed + file); stamp `ts` from the
system clock INSIDE the lock (`datetime.now()`, ISO local, no zone, seconds); add `feature` when given; build the object;
run `journal_validator.validate_new_lines([line], head_lines=file_lines, now, seed_lines=...)` plus `feature_warnings` and
`node_warnings`; any violation → nothing written, exit 2, stderr lines = the validator's own texts + the door; else append
`line + "\n"` (a file that does not end in `\n` gets one first — axis 29's torn-tail rule, F-B1-3), update the counter,
release, print `journal: <event> <task_id> written (<path>:<line no>)` and every WARN. Library: `write_event(root, obj, *,
via) -> Result(written: bool, line_no, messages)` used by the hooks; never raises out (an exception → `written=False` with
the reason).

Data row `AGENT_ROWS` (closed variety in data, not code): `scout: recon`, `builder: implementation`, `critic: review`,
`designer: spec`; an agent not in the row → category `other` and a WARN (the validator decides legality).

Edges (CLI args are outside input → adversarial battery as table rows):
- E-B1-1 notes: > 300 chars → refused for CLI ("notes are at most 300 characters (CLAUDE.md rule 12)"), AT 300 legal;
  empty / whitespace → refused (base field). Control characters (`\x00-\x1f` except none) → replaced by a space; JSON is
  written with `ensure_ascii=False`. Invariant: one event is always exactly one physical line.
- E-B1-2 `--task`: grammar of B0 E-B0-1; a task id with another clone's letter → refused ("this clone's letter is X").
- E-B1-3 lock timeout (another writer holds it 15 s) → exit 3, "journal busy: held by pid N since ts"; nothing written.
- E-B1-4 not a git repo / `git` missing / common dir unreadable → exit 2 naming the cause; nothing written. Invariant: a
  line is never written without the lock.
- E-B1-5 counter.json corrupt / non-JSON / negative → rebuilt from the worktree copies (the safe direction: higher), one
  stderr note. A counter BELOW the file max → the file max wins.
- E-B1-6 crash between the append and the counter update → next call takes max(counter, file) → no reuse (test: simulate
  by writing a line without touching the counter).
- E-B1-7 `ts` equal to the previous line's ts (same second) → legal (rule 10 allows equal); a clock BEHIND the last line
  (NTP step) → the validator's monotonicity refusal is shown; door: `event --json` with an `order-known:<ts>` token (rule 19).
- E-B1-8 `accept --run`: runs the command with `subprocess.run(<cmd>, shell=True, cwd=<repo root>, timeout=600)`,
  stdout+stderr merged, decoded UTF-8 `errors="replace"`, control chars stripped; witness = `"$ <cmd>\n" + last 40 lines
  (cap 6,000 chars, cut from the START with a "[… N lines cut]" marker) + "\nexit=<rc>"`. rc ≠ 0 → nothing written unless
  `--allow-red "<reason>"` (then `allow-red: <reason>` goes into notes). Timeout → nothing written, exit 3.
- E-B1-9 `--run` is not a road around the hygiene gate: the command is first judged by `hygiene_gate.run_allowed(cmd,
  tool="Bash") -> (ok, reasons)` (B23 exposes it over the gate's own `_decide_command`); a deny → exit 2 with the gate's
  text. Reused function in a more consequential role (the gate already refuses; here it is the only check before an
  unhooked subprocess): error direction = REFUSE on doubt (an unresolvable payload, a `cd`, a rollback shape, a journal
  target, a payload over the cap). Adversarial inputs that must stay refused: `echo x >> logs/journal/dev1.jsonl`,
  `python -c "open('logs/journal/dev1.jsonl','a').write('x')"`, `git checkout -- .` on a dirty tree, `cd tools && pytest`,
  `$(echo cd) x`, a 70 KB command, a command with a NUL byte.
- E-B1-10 `--witness-file`: a missing / directory / non-UTF-8 / > 1 MB file → refused, nothing written; the witness is
  cut as in E-B1-8.
- E-B1-11 two sessions call `delegated` with no `--task` at the same moment → two different ids (the lock); a test runs two
  processes against one temp repo and asserts distinct ids and two valid lines.
- E-B1-12 two worktrees of one temp clone issue ids → distinct numbers; their copies union-merge and validate (E-B0-7).

Tests (F-T1): one table per subcommand family over a temp git repo with a seeded journal; the two concurrency rows
(E-B1-11/12); the adversarial `--run` rows (E-B1-9) through the real gate. Witness: `python -m pytest tools/test_journal_write.py -q`.

### B23 — the dispatch-record hooks (start and end of a dispatch)

Step 0 (one measurement before code, CLAUDE.md hygiene 6a): launch one background scout and one foreground scout from a
scratch session with a logging hook on PostToolUse(Agent) and SubagentStop that dumps both payloads to the scratchpad;
record (a) whether `agentId` in the launch result equals the stop's `agent_id`, (b) the order of the two events for a
foreground launch, (c) the `tool_response` shape. The result goes into the report verbatim; the design below assumes (a)
yes, (b) stop-before-post for foreground, and is adjusted only through a question if reality differs.

Behaviour:
1. `journal_hooks.py post-agent` (PostToolUse, matcher `Task|Agent`; a NEW entry, beside `negative_lint.py`): read the
   payload; take `agentId: <id>` from the text of `tool_response` (the first `agentId: ([A-Za-z0-9_-]+)`, the regex of
   `hop_metrics._LAUNCH_RE` — import it, no copy); agent = `tool_input.subagent_type`; model = the leading tier word of
   `tool_input.description` read by `dispatch_gate.LABEL_MODEL_PREFIX_RE` (one reader); task = the dispatch's task id
   (F-B2-1); node / feature from the dispatch's header lines when present; notes = the description cut to 300 chars
   (`…` as the 300th char when cut) + `replaces_worker:<ref>` when the prompt carries that token. Repeat legality
   (critic entry / retry with `attempt` = rejected count + 1 / replacement) is computed from the journal and then judged
   by the validator. Write through `journal_write.write_event(..., via="hook")` with the lock timeout 5 s.
   If the cut has `designer: skip -- <reason>` (B0 `designer_skip_reason`) → also write `dispatch_skipped`
   (agent=designer, notes `designer skip for t-NNN: <reason>`, once per task id).
   Then: if a pending-return marker for this agent id exists (item 3) → write `returned` right after and delete the marker.
2. `dod_gate.py`: on every exit-0 path (pass, doc-only exemption, safety-valve skip) call
   `journal_hooks.record_returned(payload)` inside try/except; its failure never changes dod_gate's exit code or message
   (F-B3-1 (a)). `record_returned`: find the open `delegated` whose `worker_ref` is `agent:<agent_id>` in the journal of
   the payload's repo; found → write `returned` (via hook, model copied); already returned → nothing (idempotent); not
   found → create `<common>/forge-journal/pending-returns/<agent_id>` (O_EXCL) for item 1.
3. Pending markers older than 24 h are pruned by the next hook call (a stop of a dispatch launched before the hooks were
   live, TEMPORAL).
4. `hygiene_gate.py`: `MSG_JOURNAL_BLOCK` names the door: "the journal is written by `python -B tools/journal_write.py
   <event> …` (the hooks write delegated/returned themselves); reading it with grep, cat or tail is fine." `run_allowed()`
   exposed for E-B1-9. The refusal classes are unchanged.
5. `mechanism_gate.MECHANISM_PREFIXES` += `tools/journal_write.py`, `tools/journal_lock.py`, `tools/journal_hooks.py`,
   `tools/test_volume.py`, `tools/wave.py`, `logs/journal-letters.json`. `hook_liveness_probe.py`: one case per new hook
   entry (post-agent writes on a sample payload in a temp repo; record_returned writes after a passing stop).
6. `.claude/settings.json.proposed`: the current file with ONE added PostToolUse entry `{"matcher": "Task|Agent", "hooks":
   [{"type": "command", "command": "python tools/journal_hooks.py post-agent"}]}`; the Lead places it at acceptance.
Output channel: `hookSpecificOutput.additionalContext` one line (`JOURNAL: delegated t-NNN written` / the refusal), exit 0
always — a journal hook never blocks a tool (P1 analog: code reports).

Edges (hook payloads are outside input → battery rows):
- E-B23-1 payload: empty stdin, non-JSON, a JSON list, `tool_response` absent / a string / a list of content blocks /
  nested dicts, 2 MB response, non-UTF-8 bytes → no write, one line `JOURNAL: delegated NOT written -- <reason>; write it:
  python -B tools/journal_write.py delegated …` Invariant: a launched dispatch is never left unrecorded SILENTLY.
- E-B23-2 no `agentId` in the response (the launch failed, or a host form change) → as E-B23-1. Two `agentId:` → the first.
- E-B23-3 description without a tier prefix (dispatch_gate already WARNs) → model `unknown`? NO: no write + the CLI door
  (the `model` field is a self-declaration; code never invents it). Invariant: the hook never writes a model it did not read.
- E-B23-4 task id absent from the dispatch → a new id is issued from the counter and the line says `task id issued by the
  hook: t-NNN (the dispatch named none)`; calibration check 46 compares the dispatch's id with the line's.
- E-B23-5 the validator refuses (e.g. a repeat delegated on a closed task) → nothing written, its text shown with the door.
- E-B23-6 lock busy 5 s → no write, the door shown. Invariant: a hook never waits longer than 5 s.
- E-B23-7 POSITIONAL (hook order): PostToolUse hooks of one matcher run in parallel; the journal hook depends on NO other
  hook's output, and `negative_lint.py` reads nothing it writes. Invariant: no ordering between the two is needed.
  SubagentStop: `returned` is written only from dod_gate's exit-0 decision. Invariant: a blocked stop (exit 2) never
  writes `returned`; the later real stop writes it once.
- E-B23-8 foreground order: SubagentStop first (no `delegated` yet) → marker; PostToolUse writes `delegated` then
  `returned`. Invariant: `returned` never precedes its `delegated` in the file.
- E-B23-9 a dispatch refused by a PreToolUse gate → no PostToolUse → nothing written. Invariant: a refused dispatch never
  appears as `delegated`.
- E-B23-10 worktree cwd: the stop payload's cwd is the worker's worktree → `record_returned` looks in that repo's journal
  first, then in the main worktree's (`git worktree list` first entry); not found → marker in the shared common dir.
- E-B23-11 two parallel sessions: each hook call takes the machine lock; `session` field = payload `session_id[:8]`, so the
  open-dispatch reader can say whose dispatch it is.

Tests (F-T1 for `journal_hooks`; rows in the owned test files for dod_gate/hygiene_gate/mechanism_gate/probe): payload
table E-B23-1..6 over sample payloads (the measured ones of step 0, scrubbed, as fixtures); the order rows E-B23-7/8;
dod_gate rows: exit 2 writes nothing, exit 0 writes once, an exception in the recorder keeps exit 0; hygiene rows: the
door text, `run_allowed` on the E-B1-9 list. Witness:
`python -m pytest tools/test_journal_hooks.py tools/test_dod_gate.py tools/test_hygiene_gate.py tools/test_mechanism_gate.py tools/test_hook_liveness_probe.py -q`.

### C1 — the dispatch header generator `tools/dispatch_new.py`

Behaviour: `python -B tools/dispatch_new.py --kind builder|critic|designer|scout --task t-NNN [--feature Fnn] [--node
<slug>/<N>/<id>] --given <p>… --owns <abs>… --non-goals "<t>" --handoff <abs .md> --edges "<t>" --dod "<cmd>" --siblings
"<t>" [--designer <abs>|"skip -- <why>"|"resubmission t-NNN"]` prints the header lines in the form `dispatch_manifest`
reads (each on its own line, outside fences; owns one per line under `owns:`; a path with spaces in backticks; DoD
command in backticks), then runs `dispatch_manifest.check({"tool_input": {"subagent_type": kind, "prompt": text}})` and
exits 2 with the checker's own message when it would refuse. stdout only; it writes no file.

Edges: E-C1-1 a relative `--owns` → refused (the checker's text). E-C1-2 a `--dod` with one word → refused (the checker
needs 2+ tokens). E-C1-3 an argument holding a newline or a backtick → refused (it would break the header grammar). E-C1-4
`--designer` absent with ≥3 owns → refused by the checker (threshold), never silently filled. E-C1-5 a `--given` path that
does not exist → printed + one stderr note (the path check of dispatch_gate judges it at the send). Invariant: the
generator has no grammar of its own — whatever it prints, the checker accepts; whatever the checker refuses, it refuses.

Tests (F-T1): table (args → exit, printed headers) including the round trip "printed text passes `check`". Witness:
`python -m pytest tools/test_dispatch_new.py -q`.

### C2 — `ci_read.py why`

Behaviour: `why [<run_id>|latest] [--workflow canon.yml] [--branch <b>] [--tail N]`: `latest` = the newest run of the
workflow (on `--branch` when given); print `run <id> <conclusion> <title> <sha8>`; for each job with conclusion
`failure`/`timed_out` (at most 3): `job <id> <name>`, its failing steps (`steps[]` of the jobs endpoint: number, name,
conclusion), and the last N lines (default 60, 1..500) of that step's section of the job log, the section cut at the
`##[group]Run` / step-name boundary; ends with `(N of M lines)`. Remote text goes through `sanitize()`.

Edges: E-C2-1 run green → `run <id> success: nothing failed`. E-C2-2 in progress / queued → that status, exit 0, nothing
else. E-C2-3 conclusion failure with no failed job (startup failure, cancelled) → the conclusion and `no failed job`.
E-C2-4 the step boundary not found in the log → the last N lines of the whole job log and the line `step section not
found: job log tail`. Invariant: never an empty answer for a red run. E-C2-5 `--tail` 500 legal, 501 / 0 / negative →
refused before any request (`_check`). E-C2-6 run id non-numeric → argparse refusal. E-C2-7 more than 3 failed jobs →
the first 3 by job id and `+K more failed jobs`. E-C2-8 the log endpoint 404/410 (expired) → `log expired` for that job.

Tests: rows in `tools/test_ci_read.py` over canned API answers (the existing fake opener). Witness:
`python -m pytest tools/test_ci_read.py -q`.

### C3 — `tools/wave.py merge`

Behaviour: `python -B tools/wave.py merge <branch> --task t-NNN [--node <slug> <N> <id>] [--despite-red "<reason>"]`:
1. take `machine_lock("main-merge", 60 s)`; 2. `git fetch origin`; 3. refuse when `<branch>` is unknown on origin;
4. read the branch head's `forge-check` status (GitHub checks through `ci_read`); handling per F-C3-1;
5. a temporary worktree `W` at `origin/main` (detached) under `.claude/worktrees/wave-<ts>`; in W: `git merge --ff-only
   origin/<branch>`, else `git merge --no-ff -m "wave: merge <branch> (t-NNN)" origin/<branch>`; a conflict → `git merge
   --abort`, remove W, refuse naming the conflicted paths (no auto-resolve);
6. with `--node`: `python tools/piles.py status <slug> <N> <id> --set принято --hash <merge sha> --task t-NNN` in W, commit;
7. `git push origin HEAD:main`; non-fast-forward → remove W, back to 5 (at most 3 attempts; then refuse "main moved 3
   times during the merge");
8. delete `origin/<branch>` and the local branch (`git branch -d`, never `-D`); remove the branch's worktree if it is
   clean (worktree_sweep's rules), else leave it and print it;
9. refresh the root checkout: only when its tracked changes are a subset of {its own journal file} AND origin's journal
   file is a byte-prefix of the root's → `git -C <root> merge --ff-only origin/main`; otherwise print `root checkout not
   refreshed: <why>` and touch nothing;
10. commit the journal: in a second short W' at the new origin/main, when origin's journal is a byte-prefix of the root's,
   copy the root's bytes, commit `journal: wave <branch> (t-NNN)` (the pre-commit validator runs), push with the same
   retry; otherwise print `journal not committed: origin holds lines the root lacks -- commit it from <root>`;
11. remove W/W', release the lock, print a 4-line summary (merge sha, node, branch deleted, root refreshed / not).

Edges: E-C3-1 dirty root checkout (any tracked change but its own journal) → the merge still happens (it never uses the
root), step 9 is skipped with the reason. Invariant: wave never stashes, resets, checks out or discards anything in the
root (hygiene pt.7). E-C3-2 the lock held by another session's wave → wait 60 s, then refuse with the holder. E-C3-3
`--task` grammar per B0. E-C3-4 the push hook / pre-commit refuses → stop, remove W, print the hook's text; nothing
half-pushed (a push is atomic). E-C3-5 the branch is already merged (ancestor of origin/main) → `nothing to merge`, still
does steps 6, 8-10. E-C3-6 network failure at any git call → refuse with the step name; W removed. E-C3-7 piles status
refuses (closed batch, wrong node) → the merge is already pushed: print the refusal and the exact command to run,
exit 1 (never undo a pushed merge). E-C3-8 POSITIONAL: the forge-check read (4) is BEFORE any write. Invariant: a run
that refuses at 3-5 has changed nothing anywhere.

Tests (F-T1): over a temp bare "origin" + clone: ff merge, no-ff merge, conflict, non-ff push retry (a second clone
pushes between), dirty root, journal prefix / not prefix, already merged. No network. Witness:
`python -m pytest tools/test_wave.py -q`.

## 4. DoD skeletons per dispatch (the Lead writes the dispatch; each carries these lines)

Every builder dispatch of this spec carries: `given:` this spec + the files of its stream row + `plans/builder-rules.md`
(7b, 7d) + `docs/TESTING.md`; `owns:` the stream row's absolute paths; `non-goals:` every other stream's paths, the
package, CI runs; `handoff:` `docs/tasks/handoffs/<task>-<stream>.md`; `edges:` the E-rows of its section; `DoD:` the
witness command of its section in backticks + "the report names every E-row with the table row that covers it";
`siblings:` the §7 axis lines marked for the stream; `designer:` this file's absolute path. Builders never run CI, never
run slow files, never place `.claude/settings.json` or `.githooks/commit-msg` (they write the `.proposed` neighbours).

## 5. Order, dependencies, cost

Order: wave 1 = A1, A2, A3, B0, C1, C2 (parallel, no shared path). Wave 2 = B1 (needs B0's validator and id grammar).
Wave 3 = B23 (needs B1's library) and C3 (needs `journal_lock`). Stream L (rule texts, hook placement, calibration checks)
lands in a Fable session together with or right after wave 3. B0 is merged and B1 is merged back to back (D6), or B0 keeps
bands legal until B1 lands (F-ORD-1).

Cost line (estimates, not measured): 9 builder dispatches (A1 ~30 lines, A2 ~50, A3 ~150 + table, B0 ~350 over 9 files,
B1 ~450, B23 ~350, C1 ~150, C2 ~120, C3 ~350), 1 critic on this plan, 3 topic critics (A, B mandatory for schema, C), 1
Fable session for stream L (~1 h). Saving (the owner's goal): per dispatch the coordinator stops writing `delegated`,
`returned`, `dispatch_skipped` by hand (3 Edit turns → 0) and the `accepted` line becomes one CLI call that also runs the
witness (2-3 turns → 1); per merge wave, `wave.py merge` replaces ~8-12 git/piles turns; `ci_read why` replaces the
jobs→log→grep chain (~3 turns → 1). Measured by calibration check 48 (§7).

## 6. Exact proposed rule texts (land only through a Fable session; mechanism commits)

### 6.1 Role files (stream A1; text per F-A1-1 (b), the recommendation)

`.claude/agents/builder.md`, appended:

```
8. Tests are written by `docs/TESTING.md` — read it before your first
   test; its section «Как писать эффективный тест на нашем проекте» is
   the how-to. The volume rule lives there («Бюджет»): the added test
   lines of your diff do not exceed its added product code and text
   lines; when they do, name the reason in one line of your report AND
   in a line `tests-over: <reason>` of the commit message (the
   commit-msg hook WARNs without it, it never refuses). A new case is a
   row of an existing scenario, table or junction, not a new file.
```

`.claude/agents/critic.md`, appended:

```
20. Tests, on every diff gate, with their own verdict line: the
   question is docs/tasks/critic-diff-brief.md question 5 (the rule
   text is docs/TESTING.md). More added test lines than product lines
   with no reason named — in the report and in the commit's
   `tests-over:` line — is a finding; a named reason that does not hold
   is a finding too.
```

### 6.2 docs/TESTING.md (stream A2), the new section after «### Бюджет»

```
### Как писать эффективный тест на нашем проекте

Раздел ничего не добавляет к правилам выше — он собирает их в порядок работы билдера.

1. **Сначала найти, где поведение уже проверяется.** Пакет: `scenario_walk.py --witness-for <пути owns>` печатает
   истории и строки `keep`, которые покрывают правку. Фордж (`tools/`): тестовый файл инструмента. Новый случай — строка:
   `variants.json` истории, строка таблицы, строка стыка; нового файла нет («Бюджет»).
2. **Случай приходит из дефекта.** Одна строка, которая падала до правки (FR-32): найденного живым прогоном, критиком или
   CI. Не «по проверке на каждый ключ DoD».
3. **Один параметризованный тест на поведение.** Id параметра называет случай, по красной строке видно, какой случай и
   какая ветка упали (P16). Ввод −1, 0, 1.5, «абв» с одним исходом — один тест с параметрами.
4. **Утверждать исход, не устройство.** Стадия принята или отказана и чем, какой вопрос задан человеку, что ушло дальше.
   Ни пина текста роли, ни пина исходника, ни измеренной константы (таблица «Что не пишется»).
5. **Данные — из настоящих прогонов.** Срезы `fixtures/stories/<id>/`, `fixtures/run-*`; не выдуманный словарь из трёх
   ключей, который код никогда не увидит.
6. **Мир — один раз на файл**, проверки снимаются с него («Бюджет», «Время»; открытый вопрос об исключении сухой истории —
   находка `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`, ждёт слова
   владельца).
7. **Враждебный ввод — только снаружи.** Тикет, слова человека, конфиг проекта, ответ хоста, аргументы CLI, полезная
   нагрузка хука: размер, вложенность, кодировка, пустое и битое, каждый предел — на нём и за ним; строкой сценария или
   таблицы. Внутренняя граница теста не получает.
8. **Цена.** Строк теста не больше строк продукта (больше — причина в отчёте и строка `tests-over:` в коммите); новый
   файл (часть разрезанного — до 60 с в CI) укладывается в 10 с; тест, покрасневший второй раз без дефекта, удаляется
   («Когда тест покраснел»).

Плохо: `test_fix_13797.py` с проверкой «фраза стоит в `agents/qa-automator.md`» и копией файла без ключа, которая должна
упасть. Хорошо: строка `variants.json` истории, где ответ человека «нет» на гейте A даёт тот вопрос и ту стадию, что ждёт
требование, и которая была красной до правки.
```

### 6.3 CLAUDE.md (stream L; Fable only)

a) Routing log, first paragraph, the sentence "One JSON line per event, written with an Edit/Write tool:" becomes:

```
One JSON line per event, written by the one writer
`python -B tools/journal_write.py <event> …` (the machine lock, the
clock, the validator BEFORE the write; the owner's word 14.11.2026):
the Task/Agent PostToolUse hook writes `delegated` (and the owed
designer `dispatch_skipped`) and the SubagentStop gate writes
`returned` by themselves; the coordinator writes `accepted`,
`rejected` and the rest with one call (`accept --run "<cmd>"` runs the
verification and stores its verbatim tail as the witness):
```

b) The id paragraph ("Issuing a task_id means re-reading the tail … a band is the before-issuing road.") becomes:

```
A task id is issued by `journal_write.py next` (or by the writer when
no id is given) under the machine lock, from the clone's counter in
the git common directory (`git rev-parse --git-common-dir`), shared by
every session and worktree of the clone; ids may skip, never repeat
(validator rule 9a). An id carries the clone's LETTER — none for the
first clone of a developer, `a`, `b`, … for the next ones
(`logs/journal-letters.json`, `journal_write.py clone --claim`; the
owner's word 14.11.2026 «Номер 123 и 123А», written in lower case
ASCII: `t-123`, `t-123a`). Bands (`id_band`) are retired for new lines
and still read in old ones; `journal_keys.py declare` repairs only
collisions already in history.
```

c) Event SHAPES table, a new row after `delegated`:

```
| `returned` | `task_id`, `worker_ref` (the `delegated` it ends), `model`; written by the SubagentStop gate when a worker's stop passes; never closes a task — the open-dispatch scan shows it as RESULT PENDING until `accepted`/`rejected` |
```
and the events sentence "Events: the six of the table — … — plus `decomposable`, …" gains `returned`.

d) Command hygiene point 5 becomes:

```
5. Log entries — through `tools/journal_write.py` only (the owner's
   word 14.11.2026: «это было правило для экономии токенов модели, так
   как сейчас писать будет код то экономия только больше. Я своим
   словом разрешаю»); a redirect, tee, in-place editor or payload that
   writes `logs/journal/*.jsonl` or `logs/routing-log.jsonl` is refused,
   and so is an Edit/Write of them (F-B4-1).
```

e) Rule 8 DETERMINISTIC SCRIPT RUNS gains nothing; rule 2's acceptance sentence is unchanged (the witness is still the
verbatim run; `accept --run` is one way to produce it).

### 6.4 PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (stream L)

New check 48 (journal by code): per window (a) Agent launches in the Lead transcripts (`hop_metrics`, `agentId:` lines)
vs `delegated` lines with `via: hook` / `via: cli` / no `via` (by hand) — target: by hand = 0 after the switch, every
launch has a line; (b) `JOURNAL: … NOT written` lines (`tools/warn_density.py`) and whether each was followed by a CLI
line; (c) `returned` coverage: every finished worker (`transcripts.is_finished`) has a `returned`; (d) `accept --run`
witnesses with `allow-red` listed with their reasons; (e) counts printed with their commands (hygiene 6b).
Check 46 amended: after the switch the race count is expected 0 by construction; a duplicate id or a declaration
covering a post-switch line is a finding against the lock/counter. Check 33 amended: the ratio line adds the count of
commits that drew a TEST VOLUME WARN, how many carried `tests-over:`, and how many of those the critic judged. Check 37
amended: branches merged by `wave.py` vs by hand; a `root checkout not refreshed` line left standing over a day.

### 6.5 docs/SIBLING_MAP.md (stream L)

Axis 1 row "Journal readers <-> the task key": add the id grammar owner (`journal_keys.ID_RE` / `parse_id`, the letter),
the writer (`tools/journal_write.py`, the one writer), the counter and lock (`tools/journal_lock.py`), the registry
(`logs/journal-letters.json`), and "`returned` is read by session_context, forge_metrics, calibration_counts,
compact_snapshot". Axis 29: `journal_write` as a forge jsonl writer (F-B1-3). Axis 9: `tools/test_volume.py` as a FORGE
reader of "is this a test" with its own question (the forge repo's layout) and its error direction (unsure → product).

## 7. Four questions per mechanism (CLAUDE.md rule 10)

Mechanisms: M1 the volume rule in the roles + TESTING how-to (A1, A2); M2 the volume WARN (A3); M3 the one writer, id
issue, lock, counter, letter (B0, B1, B5); M4 the dispatch-record hooks and `returned` (B23, B0 item 4-5); M5 hygiene pt.5
one road (B23 item 4, L); M6 `wave.py merge` (C3); M7 `dispatch_new.py` (C1). `ci_read why` (C2) is a reader extension,
not a mechanism (no duty, no check): `axes: not a mechanism (a read-only CLI subcommand)`.

(a) cost and who pays:
- M1: two role paragraphs (~120 tokens per builder/critic load); the builder writes one report line when over.
- M2: one git call per commit (~50 ms); a WARN line to the builder; a `tests-over:` line when over.
- M3: one CLI call per non-hook event; the first use per clone pays `clone --claim` + a commit of one registry row.
- M4: ~100-200 ms per dispatch launch and per worker stop; a WARN line when a write fails.
- M5: none beyond M3; an Edit of the journal is refused with the door (F-B4-1).
- M6: one CLI call per merge; a temp worktree per merge (~seconds); waits up to 60 s on another session's merge.
- M7: one CLI call per dispatch instead of hand-typed headers.

(b) axis enumeration (every axis of docs/SIBLING_MAP.md, each line closes M1-M7 by name):
- axis 1: covered — M3/M4/M5 change the journal, its readers and CLAUDE.md together (B0 + L, §6.3, §6.5); M1 changes role
  files and CLAUDE.md is not touched by it (role duty only, checked against builder/critic profiles: §6.1); M2, M6, M7 n/a
  (no policy/role/journal change except M6's journal commit through the writer).
- axis 2: n/a for all — no exam instrument changes; builder row "witness-based acceptance" is kept by `accept --run`.
- axis 3: n/a for all — package/release untouched.
- axis 4: covered for M1 (AGENTS.md regenerated on agent-file change), M4 (settings.json → AGENTS.md); n/a for M2, M3, M5,
  M6, M7 (no rules/index change).
- axis 5: n/a for all — package stage twins untouched.
- axis 6: covered for M4 — `forge_metrics` learns `returned` (B0 item 6, its test); n/a for M1, M2, M5, M6, M7.
- axis 7: n/a for all — package test identity.
- axis 8: n/a for all — package story paths.
- axis 9: covered for M2 — named as a forge reader with its own question and direction (§6.5; F-A3-2); n/a for others.
- axis 10: covered for M3/M6 — they read the repo top and the common dir through `git rev-parse` (`gitcmd.git`, the one
  runner, axis 10 row); `GIT_DIR` steering is the axis's known caveat, stated in E-B1-4; n/a for M1, M2, M4, M5, M7.
- axis 11: covered for M3 (`--run`) — the command is judged by hygiene_gate's own decider, no private tokenizer (E-B1-9);
  n/a for others.
- axis 12: covered for M6 — node status only through `piles.py status` (the one writer, axis 12 row); n/a for others.
- axis 13: covered for M4 (designer skip read from the one cut), M7 (prints, then the one checker judges); n/a for others.
- axis 14: covered for M4 — the launch id read with hop_metrics' regex; finished workers in check 48 through
  `transcripts`; n/a for others.
- axis 15: covered for M2, M3, M6, M7 — new CLIs set UTF-8 console streams through the tools helper of axis 15; n/a for M1,
  M4 hooks print through the hook JSON channel (as dod_gate).
- axis 16: n/a for all — package JSON reader.
- axis 17: n/a for all — package detector verdict shape.
- axis 18: covered — no ratchet raised; `dup_ratchet` / `lint_ratchet` stay batch-level (canon); n/a otherwise.
- axis 19: n/a for all — no role `tools:` line changes.
- axis 20: n/a for all — host receipt names (package).
- axis 21: n/a for all — package markdown tables.
- axis 22: covered for M4 — the host's return form (`agentId:` in the launch result) is read at one place and measured in
  step 0; a form change is E-B23-2 (loud, never silent); n/a for others.
- axis 23: n/a for all.
- axis 24: n/a for all.
- axis 25: n/a for all.
- axis 26: n/a for all.
- axis 27: n/a for all.
- axis 28: n/a for all.
- axis 29: covered for M3 — the torn-tail rule (F-B1-3); queued if the copy is chosen; n/a for others.
- axis 30: n/a for all.
- axis 31: covered for M1 — one owner per aspect (F-A1-1); n/a for others (no role carrier change).
- axis 32: n/a for all — the package judgment census; M2 is a WARN on data (line counts), no judgment.
- axis 33: n/a for all — package dispatch identity.
- axis 34: covered — M3/M5: one road to write the journal (F-B4-1), one road to issue an id (bands retired, D5); M2: the
  classifier is a data row, not per-language branches; M6: one road to merge (F-C3-2); n/a for M1, M7.
- axis 35: n/a for all.
- axis 36: n/a for all.
- axis 37: n/a for all.

(c) registered detectors: M1 — check 33 (ratio) + critic question 5; M2 — check 33 amended (§6.4); M3 — check 46 amended,
check 13 (typed fields), the validator itself (pre-commit + write time); M4 — check 48 (new) and check 7; M5 — check 27
(hygiene audit) + check 48 (b); M6 — check 37 amended; M7 — check 11 (PATH CHECK / DISPATCH INCOMPLETE density through
`warn_density.py`).

(d) what stops the skip: M1 — the role files are loaded on every dispatch; on discipline otherwise, detector check 33.
M2 — commit-msg on every commit (code on the path; WARN by the owner's word, never a refusal). M3 — the validator before
every write, the pre-commit gate, and (F-B4-1 (a)) the Edit/Write refusal on the journal path. M4 — the PostToolUse and
SubagentStop hooks fire on every launch/stop. M5 — hygiene_gate (Bash) + the Edit/Write refusal. M6 — on discipline (a
by-hand merge stays possible); detector check 37. M7 — on discipline; the manifest checker stays the gate.

## 8. Small choices closed by the designer (no design weight; listed so the Lead can reopen)

1. Lock timeouts: CLI 15 s, hooks 5 s, wave 60 s.
2. `next --n` cap 20; `ID_JUMP_MAX` 1000 (the old `BAND_MAX_SIZE`).
3. Witness tail 40 lines / 6,000 chars; `--run` timeout 600 s; `--witness-file` cap 1 MB.
4. `accept --run` red → refused unless `--allow-red "<reason>"` (an informed pass, FR-4's analog).
5. Optional fields `via` (`hook`/`cli`) and `session` (`session_id[:8]`) — typed facts for check 48 and the reader.
6. Category map as a data row (`AGENT_ROWS`), values from the live journal (K10).
7. `ci_read why` defaults: tail 60, at most 3 failed jobs.
8. Letters after `z`: `aa..zz` (702 clones).
9. The hooks live in ONE new module `tools/journal_hooks.py` with two entry points, not two files.
10. Pending-return markers pruned after 24 h.

## 9. Forks (RETURNED — the Lead decides; recommendation first)

- F-A1-1 «Перенести правило в роль»: (b, recommended) TESTING.md «Бюджет» stays the owner; builder.md gets the duty
  sentence + link, critic.md a pointer to brief Q5 (§6.1) — axis 31 kept, the owner's goal (the rule in the file the
  builder always loads) met; (a) the rule text MOVES into builder.md (owner) and TESTING.md / builder-rules 7d / brief Q5
  become pointers — literal reading of «перенести», costs three pointer edits and makes the role file the owner of a
  testing rule the designer and critic also read. Third carrier to align either way: builder-rules 7d (K6).
- F-A3-2 test classifier: (a, recommended) a forge classifier in `test_volume.py` (data row, §3.A3), named on axis 9 as a
  different question — the package leaf `test_files.file_kind` says "a test only UNDER a test place, never by a name
  alone" (SIBLING_MAP axis 9), which reads every flat `tools/test_*.py` as production and would invert the count; (b) call
  `test_files` with a forge consumer row and teach it the forge layout — a package change for a forge need.
- F-T1 test files for NEW tools (TESTING.md «Бюджет / Файлы»: «новый тестовый файл не создаётся»; «нового тестового файла
  на новый скрипт» больше нет): (a, recommended, needs the owner's word because the text forbids it literally) one test
  file per new tool (`test_test_volume.py`, `test_journal_write.py` covering journal_lock too, `test_journal_hooks.py`,
  `test_dispatch_new.py`, `test_wave.py`), each one parametrised table + its junction rows, ≤ 10 s; (b) host the rows in
  existing files (writer/lock → `test_journal_keys.py`, hooks → `test_dod_gate.py`, test_volume → `test_mechanism_gate.py`,
  dispatch_new → `test_dispatch_manifest.py`, wave → `test_worktree_sweep.py`) — costs merging streams B0/B1/B23 and
  C1/B0 into sequential dispatches (owned test files would overlap) and hides each tool's tests in another tool's file.
- F-B1-2 echo checks for writer lines (K3): (a, recommended) `journal_write` calls the echo's collectors itself
  (tier MISMATCH through `transcripts`, notes length, escalation; the witness echo is moot when `--run` produced the
  witness) and prints their lines — one echo, called from the one writer; (b) teach `journal_echo` to fire on a Bash
  command naming `tools/journal_write.py` — a second trigger road that sees the line only after it is written.
- F-B1-3 the torn-tail append (axis 29): (a, recommended) import `ai-packages/qa-factory/scripts/hooklib.append_jsonl_line`
  under the machine lock (one appender; precedent: measurers import package scripts through `paths.SCRIPTS`); (b) a forge
  copy named on axis 29 as a second member — avoids importing the large `hooklib` into a hook (import time unmeasured).
- F-B2-1 where the hook reads the task id (and node/feature): (a, recommended) header lines `task: t-NNN`, `node: …`,
  `feature: Fnn` in the dispatch, printed by `dispatch_new.py` and read through the manifest cut (axis 13), with the fallback
  "the first `Task t-NNN` in the first 200 characters"; (b) only the free-text `Task t-NNN` convention — no grammar change,
  but a quoted id elsewhere in the prompt can be taken.
- F-B3-1 who writes `returned` (K7): (a, recommended) dod_gate calls `record_returned` on its exit-0 paths — the only place
  that knows the stop passed; couples a gate with a journal write (guarded by try/except); (b) a sibling SubagentStop hook
  that re-runs `dod_gate.decide` read-only — two evaluations that can disagree if the track changes between them; (c) write
  on every stop, idempotent — a blocked stop writes a premature `returned` (ts too early).
- F-B4-1 the Edit/Write road to the journal (P31: one road per action): (a, recommended) the writer becomes the ONE road —
  a PreToolUse Edit|Write branch (in `claim_control_gate.py`, or a new tiny gate) refuses an Edit/Write of
  `logs/journal/*.jsonl` / `logs/routing-log.jsonl` with the writer as the door, from the day check 48 shows a week with no
  by-hand line (until then a WARN; the switch is a named node of this spec, so the slice is no exclusion); retro and
  unusual lines go through `event --json`; (b) both roads stay, the writer preferred — two roads for one action, a P31
  defect unless the owner says so.
- F-B5-2 the letter's scope: (a, recommended) every clone gets a registry row; the first clone of each developer slug has
  letter "" and later clones of the same slug get `a`, `b`, … — the owner's «123 и 123А» exactly, no change for anyone
  today; (b) every clone except the owner's history clone gets a letter, including other developers' first clones — ids
  unique across the team in speech, but other developers' ids change shape and the file label already separates them;
  (c) the letter from `tools/dev.config.yaml` (`id_letter:`), no registry — no claim race detector at all.
- F-C3-1 a red `forge-check` on the branch head: (a, recommended) refuse with the door `--despite-red "<reason>"` (the
  reason goes into the merge commit message); a pending or absent check is not waited for (PROJECT.md «Командная работа»
  п. 12: «Волны слияния CI не ждут») and is printed; (b) never read CI at all (п. 12 literally) — merges a KNOWN red into
  main; (c) refuse on pending too — contradicts п. 12.
- F-C3-2 one road to merge: (a, recommended) `wave.py merge` becomes THE merge road in PROJECT.md «Командная работа» п. 1/12
  and RUNBOOK §7 (stream L, a text change), a by-hand merge stays legal only as a named fallback when wave refuses; (b) wave
  is an optional helper — two roads.
- F-ORD-1 the switch moment (D6): (a, recommended) B0 and B1 merge back to back in one Fable session before any session
  issues the next id (B0 refuses new bands); (b) B0 keeps new bands legal (WARN) until B1 merges, then a one-line flip —
  safer if wave 2 slips, but one more change.

## 10. Trail (files read for this draft)

- `CLAUDE.md`, `PROJECT.md`, `docs/FACTORY_RULES_INDEX.md`, `docs/ARCHITECTURE_INDEX.md` (auto-loaded).
- `docs/SIBLING_MAP.md`: lines 1-200 (axes 1-7), 200-347 (axes 8-14), 456-495 (axes 29-31), 559-598 (axes 32-35), the
  heading list of all 37 axes (Grep `^## Axis`).
- `docs/TESTING.md` (whole); `plans/builder-rules.md` lines 9-72 (7, 7b, 7d, 7c, 7a).
- `.claude/agents/builder.md` (whole); `.claude/agents/critic.md` rule list + lines 155-172; `.claude/settings.json` (whole).
- `.githooks/commit-msg` (whole); `.gitattributes` (journal lines 28-36).
- `tools/journal_validator.py` lines 1-120, 280-360, 1022-1051, the `def` list; `tools/journal_keys.py` lines 1-140,
  200-409, the `def`/regex list.
- `tools/journal_echo.py`: the trigger lines (Grep `tool_name|file_path|def main`), the `def` list, lines 1210-1299.
- `tools/hygiene_gate.py` lines 70-94, 425-469, 1270-1379, 1495-1534.
- `tools/dod_gate.py` lines 1-60, 560-625; `tools/tier_echo.py` lines 1-40.
- `tools/hop_metrics.py` (Grep `agentId`, lines 86-92, 335-348).
- `tools/dispatch_gate.py` (Grep for description/subagent_type/O_EXCL; lines 1760-1799); `tools/dispatch_manifest.py`
  lines 1-180 and the designer-skip Grep.
- `tools/ci_read.py` lines 1-260.
- `tools/piles.py` lines 3331-3469.
- `tools/session_context.py` lines 460-579 and the open-dispatch Grep.
- `tools/mechanism_gate.py` (Grep `SubagentStop|MECHANISM_PREFIXES`).
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: the numbered checklist (Grep), lines 116-135 (checks 6-7), 1106-1110
  (checks 45-47).
- `docs/tasks/critic-diff-brief.md`: headings + lines 37-46 (Q5).
- `logs/journal/dev1.jsonl`: the last six `delegated` lines (2053-2065) for category values and worker_ref form.
- `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md` lines 1-15.
- Globs: tools test files (`tools/test_{journal_*,session_context,ci_read,dispatch_*,mechanism_gate,hygiene_gate,dod_gate,…}*.py`).
- Greps with positive controls: `t-\\d…` over `tools/*.py` (control: journal_keys.py hit); `SubagentStop` over
  `tools/*.py`; `agents/builder.md` over `tools/`; `test-layers.json` over `tools/`.
- Not read (needed beyond the manifest: none; not opened by design): `tools/dod_track.py` (how the outer `journal_write`
  command is classified as a run — a sibling the B1 builder checks: an inner refused `--run` must not count as a green
  verification for `main_gate`), `tools/claim_control_gate.py` (host of F-B4-1 (a)), `tools/compact_snapshot.py`,
  `tools/calibration_counts.py`, `tools/forge_metrics.py` (their id/event readers are named in B0 by the Grep census only).

## 11. Lead decisions on the forks (14.11.2026, coordinator on Opus, degraded window; final acceptance queued to Fable)

Owner present; technical forks decided by the coordinator on the designer's recommendation, reversible, reported to the owner
the same turn ("решила сама"). Owner's own words cover F-B5-2 («123 и 123А») and F-A1-1 («в роль ... дать ссылку на тестинг»).

- F-A1-1: (b). F-A3-2: (a). F-B1-2: (a). F-B1-3: (a). F-B2-1: (a). F-B3-1: (a). F-B4-1: (a), with the WARN transition as
  written. F-B5-2: (a). F-C3-1: (a). F-C3-2: (a). F-ORD-1: (a).
- F-T1: (a) — owner's word 14.11.2026: «Свой файл каждому (рекомендация дизайнера) - ок». One test file per new tool.
- F-C3-1: REVERSED to (b) by the owner's word 14.11.2026: «нет, не хочу ждать CI на каждой ветке. У нас в правилах при
  нескольких готовых к слиянию ветках мы всё мержим и один билдер чинит CI». `wave.py merge` neither waits for nor refuses
  on the branch's CI; it may print the last known state of `forge-check` as information. A red `main` after a wave is one
  builder's fix (PROJECT.md «Командная работа» п. 12).
- Owner's word 14.11.2026 «План работ. Три волны - делаем»: the three-wave order of §5 is approved; builders start after
  the plan critic's verdict is accepted.
- Brief corrections K1-K10 accepted as facts of the carriers (K4 false close of `closes:t-123a` and K5 rule 9a gaps are
  load-bearing; K9 stays the first measurement of stream B23).
