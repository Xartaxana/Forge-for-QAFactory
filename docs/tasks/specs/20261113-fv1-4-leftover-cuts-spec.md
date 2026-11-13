# FV1-4 leftovers — the remaining cuts with no pointer to the whole (DRAFT spec, designer → Lead, task t-544)

Status: DRAFT for Lead acceptance. Forks are RETURNED (§6), not decided. The spec is English (FR-30 applies to what the builder writes).
Pile `live-run-fvf`, follow-up of node FV1-4 (spec `docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md`, "the FV1-4 spec" below);
inputs: the topic code critic `docs/tasks/specs/reviews/20261113-fv14-topic-code-critic.md` (QUEUE Q1, Q4, Q5, Q6, Q7 and its "Class
completeness" table), the intent brief of t-544.

The rule (set by the owner for FV1-4, not re-opened here): what the factory gathered travels whole (P4, AR-21, AR-24, FR-49); a text
shown shortened ALWAYS names where the whole is (a path the reader can open) and how much was left out; a person's words are never
cut. Length is the forge's concern, never a reason to drop content silently.

`PKG` = `C:\QAFactory\forge-repo\.claude\worktrees\fv14-fix\ai-packages\qa-factory` (branch `wip/fv14-fix`; the branch ref
`.git/refs/heads/wip/fv14-fix` reads `7101d251f7bb…`, read by this designer; that the working tree has no uncommitted change on top is
an estimate, not verified — the designer has no shell). Every `file:line` below is read in that tree on 13.11.2026. Owns paths are
written against the repository root `C:\QAFactory\forge-repo\`; the Lead re-roots them to the builder's worktree at dispatch.

---

## §0 Goal and DoD by class

After the four nodes, the four places the critic queued render whole or name their whole:
- `app_card.py` (the walker's map, `work/app-card.md`) shows no character-clipped value; every remaining COUNT cap prints how many
  were left out and the file that holds them; a person's lesson words are whole (Q4);
- a person's multi-line answer with a line over `WORDS_LINE_WIDTH` is wrapped like the one-line case, with the `<decisions>` pointer
  (Q1);
- the `human_answer` note of material a person supplied names every file (Q5);
- the "a first-look line was clipped" fact comes from the function that clipped it, not from the output's shape (Q6);
- `role-load.json`'s two FV1-4 allowance keys are validated like every other key (Q7).
No ratchet rises (§3 last column, each node's DoD). No new test file; every new case is a row in an existing keep file (§4).

---

## §1 Architecture, owners, census (AR-29; CLAUDE.md rule 10, P27)

| AR | Touched how | Change check written into the DoD |
|---|---|---|
| AR-21 (what a stage gathers travels whole) | the card's lines from the stand, sign-in, accounts, test data, page objects, notes and first look stop being clipped (L1); the pasted-material note names every file (L3) | L1 DoD (1)-(3): table rows; L3 DoD (1) |
| AR-24 (a person's words reach whoever acts, whole) | the walk card stops cutting a person's lesson words at 400 (L1, Q4); a multi-line answer's long line is wrapped with a pointer, never left as one unreadable line (L2, Q1); the note of what a person supplied is no longer cut at 1 500 (L3, Q5) | "follow each answer to the command that consumes it" (`architecture.md:252`): L1 row LESSON-*, L2 rows Q1-*, L3 rows M-* |
| AR-15 (one survivor per shared problem) and AR-19 (stage twins change together, axis 5) | the card renders the stand lines `brief_pack.manual_stand_lines` builds; after FV1-4 N2 the brief shows them whole (`_stand_text`, `_stand_names` unbounded, `brief_pack.py:2799-2812`) while the card re-clips them at 300 (`app_card.py:164-166`) — two renderings of one text; the card's first-look reasons are clipped (`app_card.py:414, :417, :421`) where the brief twin `_fl_state` shows them whole (`brief_pack.py:4045-4052`) | L1 DoD (4): the twin pairs named in the report; no new twin |
| AR-13 (a fact with a reader is read only through it) | Q6: the clip fact has one source, the function that clips (`_fl_line`); the shape-inference reader `_fl_line_clipped` goes | L2 DoD (4); grep `_fl_line_clipped` over `PKG` returns nothing |
| AR-22 (removing a producer re-homes its readers in one commit) | L1 deletes `LESSON_LINE_CHARS`, `LINE_CHARS`, `NOTE_CHARS`, `FIRST_LOOK_LINE_CHARS`, `_clip`, `_cut` of `app_card.py` (if F2 = (a)); L2 deletes `_fl_line_clipped` | each DoD: case-insensitive Grep of every removed name over `PKG\scripts`, `agents`, `skills`, `references`, `handoffs` with a positive control; hits only in quarantined tests (expected red, not edited) |
| AR-20 (shrink-only ratchets; a raise is named) | no ratchet is added or raised; `app_card.CARD_MAX_BYTES` (8 000) is not a ratchet of any keep test (§2 F-4) | each DoD: "no ratchet row moved"; a `RATCHET` line that moves in L2's run is a stop and a question, never a re-base |
| AR-29 (a code check judges data; judgment by a tier above) | L1, L2, L3 add or alter NO check: they change displays. L4 alters one check, `role_load._settings_problems` (census row `judgment-census.json:858`: class `shape`, owner `data`) — it gains two key validations; class and owner unchanged | L4 DoD (2); `test_judgment_census.py` only if `--witness-for` prints it |

Not touched: AR-1…AR-12 (no data row, role judgment, config key, host read, refusal, path a role searches, tool), AR-14 (L3 keeps the one
writer of journal note files, `person_words.write_words` via `answer_row`, `driver_runner.py:282-292`), AR-16 (no question text
changes — the s1_gap question's own caps are reported, F7), AR-17, AR-18, AR-23 (every `not known:` line of the card is unchanged),
AR-25…AR-28.

### §1a Every check the nodes add or alter — owner and census class

| Check | Where | Change | Owner it serves | Census class |
|---|---|---|---|---|
| `allowances.brief` / `allowances.brief_charter_head`, when present, are whole numbers ≥ 0 | `role_load._settings_problems` `role_load.py:77-112` (today only `packet`, `launch` are checked, `:87-89`) | added (L4) | data (code) — the shape of a package-owned settings file | shape (row `:858` unchanged) |

No other check is added, altered or removed: a character clip and a count cap are renderings, not checks (the FV1-4 spec §1a treats
them the same way). `app_card.py` and `driver_sources.py` hold no census row (Grep `"file": "(app_card|driver_sources|brief_pack)\.py"`
over `judgment-census.json` finds only the two `brief_pack.py` rows `:59-60` — the positive control of the same pattern).

---

## §2 Facts read first (load-bearing, `PKG` tree)

**Who reads the card.** `driver_dispatch.py:1135` runs `app_card.py build --task-root <T>` before a walk; the walk brief names it
(`brief_pack.py:3822` `App card: <story>/work/app-card.md`); the walk rule forbids the application's sources ("the app card and the page
are your map", `brief_pack.py:3746`; `references/walk-charter.md:3`). Reader: the walking role at S6 (a manual case). The card is the
role's map of the stand — a clipped selector, path or account name there is wrong data, not a shorter one.

**The card's budget.** `CARD_MAX_BYTES = 8000` (`app_card.py:41`). Only two sections give way, both with a pointer: First look collapses to
`FIRST_LOOK_POINTER` naming `work/first-look.yaml` (`:48`, `:528`, `:538-539`), then entry routes are cut with `- +N more:
work/flow-requests.json` (`:522`, `:540-551`). Fixed sections are not bounded by it (docstring `:18-20`); when they alone pass 8 000 B, no `k`
fits, `shown = 0` and the card is written over 8 000 B — never a refusal (`:546-552`). `inputs_hash` hashes `FORMAT` (`"1"`, `:42`) and
`CARD_MAX_BYTES` (`:440`): a card whose inputs did not change is left as it is (`:573-574`). Size asserts: only in the QUARANTINED
`test_app_card.py` (`:156`, `:184`, `:436-445`; `test-layers.json:7112`). The keep files that cover `app_card.py`
(`test-layers.json` `covers`): `test_app_card_stand_lessons.py` (`:77-84`, layer `table`) and `test_first_look_briefs.py` (`:6727`, covers
`:6732`); neither asserts a card size (Grep `CARD_MAX_BYTES` over `PKG` finds `app_card.py`, `story_step.py` (its own 4000 card),
`test_ahead_cards.py:52` (T3a's 1200, a different constant), the quarantined `test_app_card.py`, `test_report_texts.py`,
`test_stage_cards.py`, `test_story_step_card.py`). So `app_card.CARD_MAX_BYTES` is NOT the constant T3a removes (that is
`test_ahead_cards.CARD_MAX_BYTES = 1200`) — the answer to the FV1-4 spec's §9b row 2 question. The told-before-work spec names no
`app_card` (Grep `app_card|app-card|FIRST_LOOK_LINE_CHARS`: none; positive control `FIRST_LOOK_|T3b` finds 15 lines there).

**The card's clip.** `_clip(text, limit=LINE_CHARS, tokens=True)` (`app_card.py:87-89`) = `scrub` (redaction + whitespace fold, `:74-84`)
then a HEAD cut `text[:limit-3] + "..."` — the tail (a file name, the end of a selector) is what is lost. `_cut(text, limit)` (`:349-351`)
is the same head cut without scrub, used once (`:426`). The scrub `tokens` flag differs per site (structural values `tokens=False`, values
`tokens=True`) and is a safety property (E3.3) the nodes keep site by site.

**The helpers FV1-4 introduced for this class** (`brief_pack.py`): `_clipped(text, limit) -> bool` (`:438-440`, "the caller then names where
the whole is") and `_text_whole(text) -> str` (`:443-446`, "the one road for a summary whose text has no other carrier"); the pointer
wording of N2: inline ` (whole: <path>)` (`:617`, `:2859`, `:2945`, `:3147`), a section's last line `whole: <path>` (`SIDES_WHOLE` `:858`,
`BIND_WHOLE` `:863`, `:4132`), a count `+N more: <path>` (`:4131`). The card's own existing count wording: `(+N more lines: <rel>)`
`:151`, `(+N more keys: qa-factory/config.json)` `:275`, `(+N more: <map>)` `:307`, `(+N older notes: …)` `:335`, `+N: work/first-look.yaml`
`:429`, `:432`.

**Q1.** `_words_block` `brief_pack.py:1691-1711`: `broken = "\n" in text.strip()` (`:1702`); the one-line form (`:1703-1704`); `wrapped =
not broken` (`:1705`) — a multi-line text is never wrapped; body `text.split("\n")` (`:1706`); fence (`:1707-1708`); the head gets
`WORDS_WRAPPED_NOTE` (`:1670`) and the block is a `_Pointer` only when `wrapped` (`:1709-1711`). `_wrapped(text)` (`:1678-1688`) wraps one
line at the last whitespace within `WORDS_LINE_WIDTH = 1000` (`:64`), no character dropped. `_head_words` (`:1714-1721`) strips the
note for the head (no side file there). A `_Pointer` in `shown` appends `DECISIONS_ALL_LINE` (`:1833-1835`) and makes the decisions
side file written (`:4469`); `pointed` replaces the placeholder in the first line only (`:4419-4425`).

**Q6.** `_fl_line(row, body)` (`brief_pack.py:4017-4024`) clips at `FIRST_LOOK_LINE_CHARS - len(mark) - 1` and keeps the marker;
`_fl_line_clipped(line)` (`:4027-4030`) re-infers it (length == 180 and a `... [first-look:…]` tail); its one product reader is
`first_look_lines` (`:4129`, `:4132`); callers of `_fl_line`: `_fl_body` `:4088`, `:4103`; tests `test_brief_pack.py:2917-2926`
(`n2_summaries_name_their_whole`), `test_first_look_briefs.py:450` (`check_in` on the returned text). Grep `_fl_line|_fl_line_clipped|
first_look_lines` over `PKG` (positive: these hits) finds no other reader.

**Q5.** `driver_sources.py:87` (`_answer_s1_gap`, fenced answer) and `:142` (`record_gaps`, fenced answer): `self.answer_row("S1 material
supplied by the person: " + "; ".join(pasted)[:1500], "", what=…)`. `pasted` = `record_pasted`'s lines `"<url> <- work/<rel> (pasted by
the person)"` (`:453`, `:470`). `answer_row` writes the note through `person_words.write_words` and passes `--notes-file` (FV1-4 N0,
`driver_runner.py:282-292`): the transport no longer bounds the note. No test pins the line (Grep `material supplied by the person`
over `PKG`: only `:87`, `:142` — the hits are the control). Sibling found: `driver_sources.py:96` `shown = …[:1500]` passed as
`accept-gap --shown-text` (the sentence the person was shown, stored as `shown_text`, `source_inventory.py:3244`) while the other caller
`driver_dispatch.py:3873` passes `shown` whole (F5).

**Q7.** `role_load.settings` (`role_load.py:115-132`) validates through `_settings_problems` (`:77-112`), which checks `allowances.packet`
/ `launch` only (`:87-89`); `:131` merges `{"brief": 6144, "brief_charter_head": 1024, **doc["allowances"]}`; `_brief_allowance`
(`:455-465`) does `int(allowances["brief"])` / `int(allowances["brief_charter_head"])` — a string `"6144"` is silently accepted today, a
`null`, a list or `"x"` raises a raw `TypeError`/`ValueError`. The test pattern for a validated key: `test_role_load.py:282-295`
(`test_slack_key`: bad values `(-1, "1000", None, True)` refused naming the key; 0 legal).

---

## §3 `app_card.py` — every ceiling, per site (item 1)

Legend of "Outcome": **removed** = the clip goes, the value is rendered whole on one line by `scrub(value, tokens=<the site's own flag>)`
(no character dropped except what redaction replaces); **kept + pointer** = a count cap stays and its line says how many and where;
**stays** = already names its whole. "Card budget" = what the change does to `CARD_MAX_BYTES` (8 000 B, §2): a fixed section that grows
makes First look collapse to its pointer sooner and routes cut sooner (both name their file); no keep ratchet is touched; NO ratchet must
rise (§2: no keep test asserts a card size).

| # | Site (`app_card.py`) | Bound today | Value / reader | Where the whole lives | Outcome (recommended) | Reason | Card budget |
|---|---|---|---|---|---|---|---|
| C1 | `_stand_lines` `:165` `_clip(x, LESSON_LINE_CHARS)` (const `:57`, comment false since FV1-4 N1) | 400 chars, middle-free head cut, no pointer | a PERSON's lesson words (`- Stand lessons: …`, one line per lesson, `brief_pack.py:2778`) | `records/project-knowledge.json` (`PK.record_path`) | **removed**; `LESSON_LINE_CHARS` and its comment deleted | a person's words are never cut (the rule); the brief twin shows them whole (FV1-4 N1 2a) | grows by the lesson lengths |
| C2 | `_stand_lines` `:164` `_clip(x, tokens=False)` on `- Stand:`/`- API:`/`- Frontend:` | `LINE_CHARS` 300 | stand addresses and reasons, built whole by `brief_pack.manual_stand_lines` | `qa-factory/config.json` `environments` / the env file | **removed** | one text, one rendering (AR-15, axis 5): the brief shows it whole after N2 | negligible (addresses) |
| C3 | `_stand_lines` `:166` `_clip(x, tokens=False)` on `- Accounts:`/`- Env keys:` | 300 | every `--as "<role>"` and every env key NAME (`_stand_names` unbounded after N2, `brief_pack.py:2805, :2812`) | `config.json` `credentials_by_role`; the env file | **removed** | today a stand with many roles loses role names silently — the walker cannot sign in as a role it cannot see | grows with the role count |
| C4 | `_bounded` `:149` `_clip(line…)` (profile sections) | 300 per line; count `PROFILE_LINES` 10 with `(+N more lines: <rel>)` `:150-151` | lines of `strategy/project-profile.md` sections (entry points, test data) | `qa-factory/strategy/project-profile.md` | per-line clip **removed**; count cap **stays** | the count already names its file; a clipped line names nothing | ≤ 10 lines grow |
| C5 | `_test_data` `:273` `_clip(value)` (tokens=True) | 300 | a scalar test-data value the walker types | `config.json` `test_data.<key>` | **removed** (scrub tokens=True kept) | a value cut is a wrong value | ≤ 10 values |
| C6 | `_test_data` `:260` `_clip(key, 60, tokens=False)` | 60 | a test-data KEY name — and the input of `EP.SECRET_NAME.search(key)` (`:261`) | `config.json` | **removed** | an identifier; and a SAFETY defect today: a key of 64 chars ending `_password` is clipped before the secret-name test, so the test sees `…_pa...` and the value may print (adversarial row TD-SECRET) | negligible |
| C7 | `_test_data` `:268` `TEST_DATA_NAMES` 8 (const `:63`) and `_clip(k, 40)` | first 8 entry names, each 40; count `N entries` printed, the rest NOT named | names of a structured test-data entry | `config.json` `test_data.<key>` | count cap **kept + pointer**: `(names: a, …, h; +K more: qa-factory/config.json \`test_data.<key>\`)`; per-name clip **removed** | a dict may be a large catalogue (a real size, not an accident); the pointer names the key's own place | unchanged (8 names) |
| C8 | `_test_data` `:258`/`:274-275` `PROFILE_LINES` keys with `(+N more keys: qa-factory/config.json)` | count + pointer | — | config | **stays** | names its whole | — |
| C9 | `_route_rows` `:182` method `_clip(…, 12)`, source path `_clip(…, 120)` | 12 / 120 | HTTP method; the `path:line` of the request in the code | `work/flow-requests.json` | both **removed** | the head cut drops the FILE NAME of a long path; a method is an identifier; the routes already give way to the budget with `+N more: work/flow-requests.json` (`:522`), so a longer row moves loss from silent to pointed | fewer routes fit before the pointer |
| C10 | `_signin.box` `:200-201` `_clip(…, 80)` | 80 | a sign-in field selector (`role "name"` or raw) | `config.json` `manual_capture.login.ui` | **removed** | a clipped selector selects nothing | negligible |
| C11 | `_signin` `:203` recipe path `_clip(…, 120)` | 120 | sign-in route | config | **removed** | identifier | negligible |
| C12 | `_signin` `:208` `proven[:8]` + `_clip(a, 60)` | first 8, NO count, NO pointer | accounts gate A proved (the names a `ui --session <account>` call takes) | `state/sign-in-probe.json` (`MC.SIGN_IN_PROBE`) | cap and clip **removed**: every proven account, whole (F-choice C12 below) | a silent count cap; the list is the stand's proven accounts (small by nature); the walker needs each name verbatim | grows with the account count |
| C13 | `_accounts` `:227-228` key names `_clip(…, 60)` ×2, env file `_clip(…, 120)` | 60 / 120 | default account's env key NAMES and env file path | config / env file | **removed** | identifiers; a cut key name is unusable | negligible |
| C14 | `_accounts` `:233` `_clip(created, 400)` | 400 | `report_facts.created_accounts_line` (names, walker's words for a name confirmed on its word; its own cap `CREATED_SHOWN` with `+K more` and NO path, `report_facts.py:961-962`) | `state/created-accounts.json` | card clip **removed**; the producer's pathless `+K more` is a sibling outside the card (F6) | the card must not cut a line the producer already bounds; the walker's words inside it are whole | ≤ line length |
| C15 | `_page_objects` `:305` `_clip(x[2:], 200)` | 200 per line; count `PAGE_OBJECT_LINES` 8 with `(+N more: work/briefs/<map>)` `:306-307` | repo-map bullets (module path + what it holds) | the repo map file `work/briefs/repo-map-*.md` | per-line clip **removed**; count cap **stays** | the count names the map; a clipped line names nothing | ≤ 8 lines grow |
| C16 | `_notes` `:333` `_clip(n, NOTE_CHARS)` (const `:61`) | 200 per note; count `NOTE_LINES` 12 with `(+N older notes: …)` `:334-335` | walkers' notes to the next walker (a role's words) | `work/app-card-notes.jsonl` | per-note clip **removed**; count cap **stays**; `NOTE_CHARS` deleted | the knowledge the note carries is the point of the section; a multi-line note stays one folded line (scrub folds), no character dropped | ≤ 12 notes grow — the largest growth; F3 |
| C17 | `_first_look` `:426` `_cut(x, FIRST_LOOK_LINE_CHARS - 2/-4)` (const `:47`) | 200 per line, no pointer; counts `FIRST_LOOK_REQ_LINES` 8 / `FIRST_LOOK_REQ_MAX` 20 with `+N: work/first-look.yaml` (`:428-432`) | screen URL, steps, locator selectors, api, samples, data seen | `work/first-look.yaml` | F2 — recommended (a): clip **removed** (`_cut` and `FIRST_LOOK_LINE_CHARS` deleted), count caps **stay** | a clipped selector is wrong data; the section already gives way WHOLE to its pointer when the card is full, so nothing is lost silently | the First look section collapses sooner on a full card |
| C18 | `_first_look` `:414` `_clip(null reason, 80)`, `:417` `_clip(problem, 80)`, `:421` `_clip(problem, 120)` | 80/80/120 | a no-first-look / stale / unreadable reason (code text, no carrier) | none | **removed** | the brief twin `_fl_state` shows them whole (`brief_pack.py:4045-4052`, FV1-4 N2) — one rendering of one reason | negligible |
| C19 | `_why` `:93` `_clip(…, 160, tokens=False)` (used `:110`, `:194`, `:230`, `:468`) | 160 | exception text in `not known:` lines (no carrier) | none | **removed** (whole, scrub tokens=False) | FV1-4 N2 renders every "could not" text whole; no file holds it | negligible |
| C20 | `CARD_MAX_BYTES` 8000 (`:41`) with First look → pointer, routes → `+N more` | byte budget, both give-ways name their file | the whole card | the two files named | **stays** (F3) | complies with the rule (each shortened part names its file and how much); not a brief | — |
| C21 | `FIRST_LOOK_REQ_MAX` 20, `FIRST_LOOK_REQ_LINES` 8, `PROFILE_LINES`, `NOTE_LINES`, `PAGE_OBJECT_LINES` | counts with `+N …: <file>` | — | named | **stay** | name their whole | — |
| C22 | `_route_rows` `:181` URL: `split("?")[0].split("#")[0]` | query and fragment dropped | — | `work/flow-requests.json` | **stays — why**: a security rule ("a token may sit in it", docstring `:171-172`), not a length cut; class `safety`, the whole one named file away | — | — |

After the node, `_clip` has no caller and is deleted; `LINE_CHARS`, `LESSON_LINE_CHARS`, `NOTE_CHARS` are deleted; `_cut` and
`FIRST_LOOK_LINE_CHARS` are deleted under F2 (a). Docstrings `:18-20` and `:403-404` are reworded (no per-line limit).
**C12 small choice closed:** remove the cap rather than add a pointer, because the proven accounts are the stand's own accounts (not a
catalogue); if the Lead prefers a pointer, the line is `… (+K more: state/sign-in-probe.json)` — no other change.

---

## §4 Nodes (for a weaker model; owns by FUNCTION; witness via `scenario_walk.py --witness-for`)

Order: L1, L2, L3, L4 are file-disjoint and independent; all four may run in parallel. L3 and L4 are small: the Lead may send them as ONE
builder dispatch (small-work batch, CLAUDE.md rule 8) — owns stay as written. `brief_pack.py` hot-file queue: L2 lands after the FV1-4 fix
branch `wip/fv14-fix` merges (it edits `_words_block`, `_fl_line`, `first_look_lines` that FV1-4 N1/N2 wrote) and before T3b
(`очередь: FV1-4 N1/N2/fix → L2 → T3b`); T3b owns `FIRST_LOOK_*` constants of `brief_pack.py` — L2 edits none of them.

### L1 — `app_card.py`: no character clip; every count cap names how many and where (item 1, Q4)
given: this spec §2, §3, §6; `PKG\scripts\app_card.py` (whole); `PKG\scripts\brief_pack.py:438-446, 2768-2817, 4040-4053`;
`PKG\scripts\report_facts.py:935-962`; `PKG\scripts\tests\test_app_card_stand_lessons.py` (whole); `PKG\scripts\tests\test_app_card.py:1-80`
(helpers `make`, `card_of`, `body` — import only, the file is quarantined); `PKG\scripts\tests\test_first_look_briefs.py:425-451`;
`PKG\scripts\tests\test-layers.json:77-84`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\app_card.py (constants FORMAT, FIRST_LOOK_LINE_CHARS, LESSON_LINE_CHARS, LINE_CHARS, NOTE_CHARS, TEST_DATA_NAMES comment; _clip, _why, _bounded, _stand_lines, _route_rows, _signin, _accounts, _test_data, _page_objects, _notes, _cut, _first_look; the module docstring :18-20)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_app_card_stand_lessons.py (one new parametrised test function)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-4-leftover-app-card.md
non-goals: `CARD_MAX_BYTES` and the give-way logic of `build_card` (`:535-552`, F3); `first_look_path_items`, `first_look_head`, `scrub` (shared with the briefs); `report_facts.created_accounts_line` (F6); `brief_pack.py` (L2); the quarantined `test_app_card.py` (not run, not edited; its rows that pin a clip go red in quarantine-watch — list them in the report); `test-layers.json` (F4).
handoff: builder report (rule 7 of `.claude/agents/builder.md`) with the witness output; per row C1-C22 of §3 one line `applied | stays` with the test row id that proves it; the twin pairs (C2/C3/C18 ↔ `brief_pack`) named; the FR walk (C, D, E, G); the list of quarantined `test_app_card.py` functions expected red.
edges (each with its invariant):
- E1 empty / absent values (no lesson registry, `config.json` without `test_data`, no notes file, no first look, an empty selector dict `{}`) → the existing line or `not known:` text, byte-identical to today. Invariant: an absent value is said, never silently dropped (AR-23).
- E2 a value AT the old bound (lesson 400, line 300, selector 80, key 60, note 200, first-look line 200, proven accounts 8, entry names 8) and ONE beyond (401, 301, 81, 61, 201, 201, 9, 9) and 10× → whole at every size; the counts: 8 entry names shown and `+1 more: qa-factory/config.json \`test_data.<key>\`` at 9 (C7), `+92 more` at 100. Invariant: no value is shortened at any length; a list cap always says how many and where.
- E3 multi-line value (a walker note or a lesson with `\n`, a profile line with tabs) → one line, whitespace folded by `scrub`, no character dropped. Invariant: a line of the card is never split into a second line that reads as a section or a bullet.
- E4 non-ASCII (a Cyrillic lesson of 401 characters = 802 B; an emoji in a note) → whole; the card's byte count grows by bytes, the give-way logic counts bytes (`:535`) as today. Invariant: no clip by characters or bytes remains outside the two give-ways.
- E5 a value whose whole has no file to point at (exception text C19, first-look reasons C18) → whole on one line, no pointer. Invariant: a text with no carrier is never shortened (nothing could lead to the rest).
- E6 pointer path with spaces: the only new pointer (C7) names a constant path and the key in backticks; a key with a space or a backtick is printed as the line already prints it (scrubbed, folded) inside the backticks; an env file path with a space (`my env/.env`, C13) is printed whole. Invariant: the pointer names the file the code reads (`CONFIG_REL`), spelled as the code writes it (FR-37).
- E7 TEMPORAL — a card written before L1 with unchanged inputs: `FORMAT` goes `"1"` → `"2"` in the same commit, so `inputs_hash` differs and the next `build` rewrites the card once. Before L1 lands nothing changes. Invariant: no story keeps a clipped card after the release that removes the clips.
- E8 the card over 8 000 B because fixed sections grew → First look collapses to `FIRST_LOOK_POINTER`, then routes give way with `+N more: work/flow-requests.json`; if fixed sections alone pass 8 000 B, the card is written over 8 000 B with every route counted in the pointer (today's `:546-552` behaviour, unchanged). Invariant: every route is either listed or counted in a line naming `work/flow-requests.json`; the card is never refused or emptied for size.
- E9 SAFETY (the reused function in a more consequential role: `scrub` becomes the whole-value renderer of every site) — error direction: OVER-redaction only, as today; each site keeps its own `tokens` flag (structural `tokens=False`: method, path, selector, recipe path, key names, env file, stand/accounts lines, first-look lines, `_why`; value `tokens=True`: test-data scalar, walker notes). Adversarial inputs that must stay safe: a test-data key `"x"*55 + "_password"` with a scalar value (the value is `(value not printed)` — fails before L1, row TD-SECRET); a selector holding a 30-char `data-testid` (shown whole, `tokens=False`); a recipe path with `user:pass@` (removed by `_USERINFO`); a note holding a JWT or `token=abc` (`[not printed]`); a lesson saying `password: hunter2` (`[not printed]`). Invariant: whole never means unredacted.
DoD (acceptance keys): (1) every row of §3 marked removed/kept+pointer is applied; Grep `_clip\(|_cut\(|LINE_CHARS|NOTE_CHARS` over `app_card.py` returns nothing (positive control: the same Grep on the base tree finds `:87`, `:349`); (2) one new parametrised pytest function in `test_app_card_stand_lessons.py` (e.g. `test_card_values_whole_or_counted`), one row per id below, each row red on the base tree and green after: LESSON-400/401/1000/CYR401 (C1), ACCOUNTS-30-ROLES (C3, every `--as "<role>"` of 30 roles × 20 chars present), PROFILE-301 (C4), TD-VALUE-301 (C5), TD-SECRET (C6, E9), TD-NAMES-8/9/100 + TD-NAME-41 (C7), ROUTE-METHOD-13 + ROUTE-PATH-121 (C9), SELECTOR-81 + RECIPE-121 (C10, C11), PROVEN-8/9 (C12), KEYS-61 + ENVFILE-SPACE-121 (C13), CREATED-401 (C14), PAGE-201 (C15), NOTE-201 + NOTE-MULTILINE (C16, E3), FL-SELECTOR-300 (C17, under F2 (a)), FL-REASON-121 (C18), WHY-161 (C19), FORMAT-REBUILD (E7: a card written with the old hash is rewritten), FULL-CARD (E8: fixed sections over 8 000 B → the card is written, First look is the pointer, every route counted); the empty rows of E1 ride as rows of the same table; (3) the existing `test_stand_lessons_reach_the_card_and_rebuild_it` stays green unchanged; `test_first_look_briefs.py` stays green unchanged; (4) the report names the twin pairs (C2/C3 ↔ `manual_stand_lines`, C18 ↔ `_fl_state`) and says each side now renders whole; (5) no ratchet row moved; the AR-22 Grep of every deleted name (case-insensitive, over `PKG\scripts`, `agents`, `skills`, `references`, `handoffs`, positive control: `CARD_MAX_BYTES` hits `app_card.py:41`) returns only the quarantined `test_app_card.py`. Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/app_card.py` — run every file it prints (quarantine excluded; expected by `test-layers.json` `covers`: `test_app_card_stand_lessons.py`, `test_first_look_briefs.py` — an estimate, the designer did not run the command); all green.
siblings: axis 5 (the card ↔ brief twins C2, C3, C17, C18); axis 34 (one road: the card has one rule for every value on every project and language, no branch); `report_facts.created_accounts_line` pathless `+K more` (F6); `brief_pack._fl_line` keeps its clip with a pointer (T3b's constant; F2 note).
designer: this draft.

### L2 — `brief_pack.py`: wrap a long line of a multi-line answer (Q1); the clip fact comes from `_fl_line` (Q6)
given: this spec §2 (Q1, Q6); the FV1-4 spec §5.1, §8 E-22/E-23/E-30, §9c F10; `PKG\scripts\brief_pack.py:1660-1722, 1780-1840, 4011-4135, 4415-4426, 4466-4471`; `PKG\scripts\tests\test_brief_pack.py:1816-1866, 2793-2930`; `PKG\scripts\tests\test_first_look_briefs.py:440-451`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (_words_block; _fl_line; _fl_line_clipped (deleted); first_look_lines (the `clipped` line :4129 only); a new marker class next to `_Pointer` — no other function, no FIRST_LOOK_* constant)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (rows in `p4_long_words` and in `n2_summaries_name_their_whole` :2916-2926 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-4-leftover-brief-wrap.md
non-goals: `WORDS_LINE_WIDTH`, `_wrapped`, `_head_words`, `decisions`, `question_answer_lines`, `render`, `pointed` (unchanged: they already carry a `_Pointer` and strip the note for the head); `FIRST_LOOK_LINE_CHARS` and every `FIRST_LOOK_*` (T3b); `app_card.py` (L1); quarantined tests.
handoff: builder report with the witness output; the FR walk (B, C, D, G); per row id below one line with its result.
Mechanism:
- Q1: in `_words_block`, for the multi-line case, every line of `text.split("\n")` longer than `WORDS_LINE_WIDTH` characters is replaced by the lines of `_wrapped(line)`; `wrapped` becomes `True` when the one-line case is wrapped OR any line of a multi-line text was wrapped; the rest of the function is unchanged (the head gets `WORDS_WRAPPED_NOTE`, the block is a `_Pointer`, so `decisions` appends `DECISIONS_ALL_LINE` and the side file holds the bytes as given; `_head_words` strips the note for the head, as today). A line of exactly `WORDS_LINE_WIDTH` characters is not wrapped. Lines are measured as given (after `person_words.lf`), not folded; leading spaces of a line are kept.
- Q6: a new `class _Clipped(str)` beside `_Pointer` ("a line `_fl_line` shortened; `first_look_lines` ends its block naming the record"); `_fl_line` returns `_Clipped(line)` when it clipped, a plain `str` otherwise; `first_look_lines` computes `clipped = any(isinstance(line, _Clipped) for line in lines[:FIRST_LOOK_LINES_MAX])`; `_fl_line_clipped` is deleted. The returned text is byte-identical to today's (callers and `test_first_look_briefs.py:450` unchanged).
edges (each with its invariant):
- E1 empty words / a blank line inside a block → as today (the "not recorded" clause; a blank line kept as an empty line). Invariant: an absent word is said; paragraph structure kept (FV1-4 E-20, E-23).
- E2 a multi-line answer whose longest line is exactly 1 000 characters → not wrapped, no `<decisions>`, not a `_Pointer` (byte-identical to today); 1 001 → that line wrapped into lines of ≤ 1 000, head carries `<decisions>`, the entry list ends with `DECISIONS_ALL_LINE`; `"a\n" + "x"*200000` → no line of the block over 1 000, the wrapped pieces joined equal the original line. Invariant: no character is dropped and every line of the brief is readable by a by-range read (F10's reason, now for both shapes).
- E3 multi-line with a long line that has whitespace → cut at the last whitespace within the width (kept at the end of its piece); with none → split at exactly 1 000. Invariant: the same wrapping rule as the one-line case (one road, AR-15).
- E4 non-ASCII: a line of 1 001 Cyrillic characters (2 002 B) → wrapped by characters at 1 000 (the width is in characters, F10). Invariant: the width means the same on every language.
- E5 a backtick run longer than the width in a long line → split by the wrap; the fence is computed on the whole text before wrapping (`:1707`), so it stays longer than any run. Invariant: the person's text never closes the block early (FV1-4 E-30).
- E6 the head (`_head_words`: a repair reason or purpose with a 1 001-char line) → wrapped, no `WORDS_WRAPPED_NOTE`, no `<decisions>` in the head. Invariant: a pointer never names a side file this build does not write (FV1-4 E-9).
- E7 pointer path with spaces: `<decisions>` is replaced by `RP.story_text(...)` of the side file (`:4416`) as today — a task root with spaces is printed as is; `--output`/`--dry-run` add " (side files not written in this run)" (`:4417`). Invariant: unchanged from FV1-4 N1.
- E8 Q6 — a value whose whole has no file: n/a (`work/first-look.yaml` always exists when rows exist). A line shortened by `_fl_line` but cut away by the count cap (`lines[FIRST_LOOK_LINES_MAX:]`) adds no `whole:` line (the `+N more: work/first-look.yaml` line names the file). Invariant: a `whole:` line appears exactly when a SHOWN line was shortened.
- E9 Q6 — the reused function `_fl_line` in a more consequential role (its type now carries the fact): error direction allowed: NONE for a clipped line (a shortened line is never unmarked); an unclipped line that happens to be exactly 180 characters and end in `... [first-look:R-1]` is NOT marked (today it is, a harmless extra pointer). Adversarial: a body exactly `room` long (not clipped), `room + 1` (clipped); a req id that is not `R-n` (mark `?`); a body ending in `...`.
DoD (acceptance keys): (1) rows in `p4_long_words` (each red on the base tree, green after): Q1-AT-1000, Q1-1001, Q1-200K, Q1-WHITESPACE, Q1-CYR-1001, Q1-BACKTICK-RUN, Q1-HEAD (through `_head_words`); the existing E-22/E-23/E-24/E-30 rows stay green unchanged; (2) in `n2_summaries_name_their_whole` the `_fl_line_clipped` row (`:2919-2921`) becomes `isinstance(…, brief_pack._Clipped)` on the short and the 600-char lines, plus Q6-COINCIDENCE (an unclipped 180-char line ending `... [first-look:R-1]` → `first_look_lines` adds no `whole:` line — red before) and Q6-CUT-AWAY (E8); the `first_look_lines` rows `:2922-2926` stay; (3) no `RATCHET` line moves in the witness run (`ROLE_BRIEF_BYTES_MAX`, `S5_PLAN_BRIEF_BYTES_MAX`): a moved number is a stop and a question to the Lead, never a re-base; (4) Grep `_fl_line_clipped` (case-insensitive) over `PKG` returns nothing (positive control: on the base tree it finds `brief_pack.py:4027`). Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py` — every file it prints, quarantine excluded, a slow file of PROJECT.md п. 2 judged by CI; all green.
siblings: axis 5 (`_words_block` is the one renderer for every stage and role); axis 34 (one wrap rule for one-line and multi-line text, every language); `_Pointer` is the precedent of a str marker (AR-15: the same device, not a second one).
designer: this draft.

### L3 — `driver_sources.py`: the note of supplied material names every file (Q5)
given: this spec §2 (Q5), §6 F5; `PKG\scripts\driver_sources.py:60-151, 419-470`; `PKG\scripts\driver_runner.py:282-292`; `PKG\scripts\driver_core.py:293-300`; `PKG\scripts\tests\test_story_run_refusals.py:415-431`; `PKG\scripts\tests\fixtures\driver-layers.json` (names homed in `driver_sources`); `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_sources.py (Driver._answer_s1_gap :87 and Driver.record_gaps :142 only; :96 in Driver._accept_gap_kinds only if F5 = (a))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_run_refusals.py (rows next to the `record_pasted` block :417-431 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-4-leftover-supplied-names.md
non-goals: `record_pasted`, `answer_row`, `_answer_note`, `person_words` (unchanged: the note already goes by a file); the s1_gap question caps `name_list` / `clip_bytes` / `GAP_*` (F7); `driver-layers.json` (no new name: closed choice §7); `driver_dispatch.py`.
handoff: builder report with the witness output; the FR walk (A, B, C, D, G).
Mechanism: at both sites drop `[:1500]`: the note is `"S1 material supplied by the person: " + "; ".join(pasted)`, passed to `answer_row` exactly as now (words `""`). Under F5 (a) also `:96` drops `[:1500]`.
edges (each with its invariant):
- E1 empty `pasted` → the branch is not reached (`if pasted` `:86`; `if not pasted: return False` `:140-141`), unchanged. Invariant: no note claims material that was not recorded.
- E2 the joined names exactly 1 500 characters / 1 501 / 15 000 (40 files of long URLs) → the note holds every name whole at all three. Invariant: every file the person supplied is named in the journal every later brief reads (`answers_of`).
- E3 multi-line: a URL holding a line break (inventory data) → the note goes by `--notes-file` (multi-line safe); the brief renders it through `_words_block` (fenced). Invariant: the transport never cuts a note (FV1-4 N0).
- E4 non-ASCII URL (IDN host, Cyrillic path) → whole; the note file is UTF-8 (`write_words`). Invariant: no byte/char limit applies.
- E5 a value whose whole has no file: n/a — the note IS the whole (no pointer needed); each name also points at its own `work/sources/<id>/pasted-<n>.md`.
- E6 pointer path with spaces: no pointer is added; a `local_ref` with a space is printed as `record_pasted` wrote it.
- E7 F5 (a) only — `shown` of 1 500 / 1 501 characters reaches `accept-gap --shown-text` whole; `shown` is derived from the question body, which `s1_gap_cap` bounds at `GAP_TEXT_MAX` bytes (docstring `:631-632`; the value of `GAP_TEXT_MAX` not read here), so the list argv stays under the Windows 32 767 limit. Invariant: the stored `shown_text` is the sentence the person was shown, the same on both callers (`driver_dispatch.py:3873` passes it whole).
DoD (acceptance keys): (1) Grep `\[:1500\]` over `driver_sources.py` returns nothing at `:87`/`:142` (and `:96` under F5 (a)); positive control: on the base tree it finds the three lines; (2) one loop of rows in `test_story_run_refusals.py` next to `:417-431`: with `record_pasted` returning N lines and `answer_row` spied, both callers (`_answer_s1_gap` with a fenced answer, `record_gaps` with a fenced answer) give a note holding every line — rows M-1500, M-1501, M-15000, M-CYR (each red on the base tree except M-1500); under F5 (a) one row S-1501 on `_accept_gap_kinds` (`--shown-text` argument whole); (3) no new name in `driver_sources.py` (`driver-layers.json` unchanged). Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_sources.py` — run every printed file that is not in `slow_tests.json` / PROJECT.md п. 2's slow list (`test_story_run_*` are judged by CI, not run locally); the report lists the printed files and which were left to CI.
siblings: axis 29 (the journal appender, unchanged); axis 5 (the two fenced-answer roads `_answer_s1_gap` / `record_gaps` change together — they are twins); F5 (`:96` vs `driver_dispatch.py:3873`), F7 (`name_list`).
designer: this draft.

### L4 — `role_load.py`: validate the two FV1-4 allowance keys (Q7)
Designer's call (the brief left it open): a NODE, not a queue pointer — rule 6 of the designer role: "a residual of this class is a node
with owns and a test; a line closes nothing"; cost: one condition and one test loop, batchable with L3.
given: this spec §2 (Q7); `PKG\scripts\role_load.py:73-132, 455-466`; `PKG\scripts\tests\test_role_load.py:51-62, 282-296`; `PKG\references\role-load.json`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py (_settings_problems only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_role_load.py (test_slack_key: one new loop)
non-goals: `settings` (its default merge `:131` stays, E-13 of FV1-4); `_brief_allowance`; `role-load.json` values; census rows.
handoff: builder report with the witness output; FR walk (A, C, G).
Mechanism: in `_settings_problems`, after the `packet`/`launch` check: for each of `brief`, `brief_charter_head` PRESENT in `allowances` (a dict), if `not whole(value, 0)` → `problems.append(f"\`allowances.{key}\` must be a whole number >= 0 when present")`.
edges: E1 the key absent → no problem, `settings()` default 6144 / 1024 (TEMPORAL, an older file — FV1-4 E-13). Invariant: an older settings file still loads. E2 present and `0` → legal. E3 `-1`, `"6144"`, `None`, `True`, `6144.0`, `[]` → `RoleLoadError` naming `allowances.brief` (resp. `brief_charter_head`). Invariant: a malformed allowance is refused with its key named (FR-1), never a raw `TypeError`/`ValueError` from `int(...)`; `"6144"` (accepted silently today) is refused — the package file holds integers, so the stricter reading is safe. E4 `allowances` not a dict → the existing `packet`/`launch` problem only (no second message). Limit/empty/multi-line/non-ASCII/pointer edges: n/a — a package-owned JSON number.
DoD: (1) in `test_slack_key`, rows `for key in ("brief", "brief_charter_head"): for bad in (-1, "6144", None, True, 6144.0): … check_in(key, raised)`, plus absent → `(6144, 1024)` and `0` → legal (each bad row red on the base tree as "not refused naming the key"); (2) census row `judgment-census.json:858` unchanged (class `shape`, owner `data`). Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/role_load.py` — every printed file, quarantine excluded; all green.
siblings: none -- one validator of one settings file; axis 18 untouched (no ratchet value changes).
designer: this draft.

---

## §5 Rule 10 — four questions (one block per mechanism)

M1 "the card renders every value whole; a count cap names how many and where" (L1): (a) cost: a bigger card on stands with many
roles/notes/long selectors; the walker pays bytes once per read; the First look and routes give way sooner (each named). (b) axes: 1 n/a;
2 n/a; 3 n/a; 4 covered (finding rows via the pile); 5 covered (card ↔ brief twins C2, C3, C17, C18); 6 n/a (no measurer reads the
card); 7-16 n/a (no test identity, story location, test-file, git, shell, plan carrier, dispatch text, transcript, console, JSON reader
change); 17 n/a; 18 covered (no ratchet; `CARD_MAX_BYTES` is not a keep ratchet); 19-28 n/a; 29 n/a (no jsonl writer); 30 n/a; 31 n/a;
32 covered (no census unit); 33 n/a; 34 covered (one rule for every value, project, language); 35 n/a; 36 n/a. (c) detector: the L1
table rows in a keep file (canon); a clip creeping back is caught by DoD (1)'s Grep only at review — no code gate (on discipline, detector:
critic question on class completeness + this table). (d) on the path: `build_card` is the only producer of the card.
M2 "one wrap rule for any long line of a person's words" (L2 Q1): (a) none beyond a few lines on rare answers; (b) axes 5, 34 covered,
others n/a as M1; (c) `p4_long_words` rows; (d) `_words_block` is the one renderer.
M3 "the clip fact has one source" (L2 Q6): (a) none; (b) axis 5 covered (the card twin under F2 (b) would reuse the same device), others
n/a; (c) `n2_summaries_name_their_whole` rows; (d) `_fl_line` is the only producer of a first-look line.
M4 "allowances keys validated" (L4): (a) none at run time; (b) axis 18 n/a (no value moves), 32 covered (row `:858`), others n/a;
(c) `test_slack_key` rows; (d) `settings()` is THE reader of `role-load.json`.
L3 is not a mechanism (a cut removed, no duty added): "axes: not a mechanism (a display cut removed in two call sites)".

---

## §6 Forks — RETURNED (options, cost, recommendation)

**F1. The "shortened with a pointer" helper in `app_card.py`.** The brief asks that the new nodes reuse the helper FV1-4 introduced:
`brief_pack._clipped` / `_text_whole` and N2's pointer wording. Under the §3 outcomes the card keeps NO character clip, so `_clipped` has
no site; the whole-value road is the card's `scrub` (which already folds whitespace exactly like `_text_whole`, and redacts). (a) the card
renders through its own `scrub` (redaction is mandatory there, E3.3) and uses the shared wording for its one new count pointer
(`+K more: <path>`, the form of `brief_pack.py:4131` and of the card's `:307`); no import of `brief_pack` helpers; (b) wrap every value as
`brief_pack._text_whole(scrub(x))` — a no-op call kept for "one helper"; (c) if a clip were kept anywhere in the card (F2 (b)), its
fact must come from the card's own clip (scrub first), because `brief_pack._clipped` measures the unscrubbed text and errs both ways
(`token=x` → `token: [not printed]` is longer; a long run → `[not printed]` is shorter). *Recommended: (a)*; cost: none.

**F2. The card's First look line clip (C17, `FIRST_LOOK_LINE_CHARS` 200).** Its brief twin `_fl_line` keeps a 180 clip with a `whole:`
line (FV1-4 N2; constant owned by T3b). (a) remove the clip in the card: lines whole; the section already collapses whole to its pointer
when the card is full — nothing is lost silently, `_cut` and the constant go; (b) mirror the brief: keep the clip, the card's clip returns
the fact (the Q6 device: a str marker), and the section ends `- whole: work/first-look.yaml` when a shown line was shortened. Cost of (b):
a marker class in `app_card.py`, one more row. One road: both options comply; the shapes already differ (the card shows one item per line,
the brief joins items with "; "). *Recommended: (a)* — a selector the walker copies must be whole, and the card has a whole-section
give-way the brief lacks.

**F3. `CARD_MAX_BYTES` itself (8 000 B).** The owner's word for FV1-4 «в прогоне фабрики вообще не должно быть потолка» was applied to the
BRIEF; the Lead's rule for this follow-up admits a shortened text that names its whole and how much. (a) keep it: both give-ways name
their file and count (C20), and removing the clips makes them fire sooner on large stands (the cost of keeping); (b) remove it: the card
always shows every route and the whole First look — the card can grow without bound on a large app (hundreds of routes); `inputs_hash`
loses the constant, the quarantined rows go red. No ratchet rises under either. *Recommended: (a)*; the Lead takes (b) to the owner if
the owner's word is meant for every run-time artifact, not only the brief.

**F4. Where the card's test rows live.** The only keep file covering `app_card.py` behaviour is `test_app_card_stand_lessons.py`
(`test-layers.json:77-84`, layer `table`, why "SS1-11 F5 stand lessons reach the app card and rebuild it"); `test_app_card.py` is
quarantined (`:7112`) and may be neither run nor edited; a new test file is forbidden (docs/TESTING.md «Бюджет»). (a) the new parametrised
function goes into `test_app_card_stand_lessons.py` and the Lead rewords its keep `why` (e.g. "the app card: stand lessons, and every value
whole or counted with its file") in the integration commit — the row keeps its layer and `covers`; (b) the same, `why` left as is (the
row then under-describes the file; critic question 5 may flag it); (c) only LESSON-* rows (the person's words, critic Q4) get a test,
the other card rows ride on the critic's diff reading — leaves 19 changed sites without a red-before row. *Recommended: (a)*; whether
a hand edit of a keep row's `why` is legal outside `tools/test_quarantine.py` is the Lead's call (AR-20 names only leaving a row as the
tool's).

**F5. `driver_sources.py:96` — the shown text of a kinds acceptance cut at 1 500 (found in this draft, a sibling of Q5).** `shown` is
stored as `shown_text` ("the sentence the person was shown", `source_inventory.py:3244`); the other caller `driver_dispatch.py:3873`
passes it whole: two roads for one action (P31). (a) include in L3 (drop `[:1500]`, one row S-1501); the argv stays bounded by the
question body cap (L3 E7); (b) a separate finding/node. *Recommended: (a)*; cost: one line and one row in the same owns.

**F6. `report_facts.created_accounts_line` — `+K more` names no file (`report_facts.py:961-962`, `CREATED_SHOWN`).** The card shows this
line (C14) and the walker needs each name for `--as created:<username>`; a report reader sees the same line. (a) a node L5 in this spec:
the line ends `+K more: state/created-accounts.json` (owns: `report_facts.created_accounts_line` + its keep test rows; readers: the
report and the card); (b) a finding in the pile for the next batch. *Recommended: (a)* — rule 9: the rest of the class is a named node;
the Lead may move it if `report_facts.py` is busy in another pile. Not drafted as a node until the Lead decides (owns and test file not
read beyond `:935-962`).

**F7. The s1_gap question's own caps — `name_list` `(+K more)` with no file and `GAP_NAME_MAX` 100 B clips
(`driver_sources.py:580-597`), and `clip_bytes(gap_class_problem, 300)` (`:612`).** Text a PERSON reads; the source lines already name
the details file (`s1_gap_more` `:627-628`), these lists do not. (a) a finding for the gates-and-words / question-text owner (AR-16:
a question text change goes through `human_text.problems` and its price rows); (b) a node in this spec. *Recommended: (a)*, because the
question form has its own rules and owner; the Lead files it with the line "found by t-544".

---

## §7 Small choices closed by the designer (no design weight)

- Every removed card clip becomes `scrub(value, tokens=<the site's existing flag>)` — the flag is copied site by site (E9).
- C7's pointer wording: `+K more: qa-factory/config.json \`test_data.<key>\`` (the brief_pack form `whole: pipeline.json \`sides\``,
  `brief_pack.py:858`, for a key inside a file).
- C12: the proven-accounts cap is removed rather than pointed (§3 note).
- `FORMAT` `"1"` → `"2"` (E7) so cards rebuild once.
- Q6 device: a `str` subclass `_Clipped` (the `_Pointer` precedent, `brief_pack.py:1572`), so `_fl_line`'s callers and
  `test_first_look_briefs.py:450` keep their shape; a tuple return was rejected (three call sites and two test files would change).
- L3 adds no helper for the twice-written note (a new `Driver` member needs a `driver-layers.json` row); the two literal lines change
  together.
- L4's message names the key path `allowances.<key>`, the form of the existing `allowances` message (`role_load.py:89`).

---

## §8 Contradictions and analogs noticed (reported, not widened)

1. The brief's "render-sites axis" of `docs/SIBLING_MAP.md`: no axis by that name; Grep `render` (case-insensitive) finds axis 17
   (`detector_verdict.render`) and axis 28 ("the render site of the row form"), neither about cuts. Walked instead: axis 5 (twins), 17
   (the FV1-4 spec's own sibling note), 18, 28 (n/a: the row form is not touched), 34.
2. The critic's line numbers were from `wip/fv14-topic`; at 7101d25 `_words_block`'s `wrapped = not broken` is `:1705` (critic: `~1708`),
   `_fl_line_clipped` `:4027` (critic `~4017` is `_fl_line`); `app_card.py` lines equal the scout's.
3. The FV1-4 spec's pointer wording for a character clip (` (whole: <path>)`) names WHERE but not HOW MUCH; the Lead's rule for this
   follow-up says both. The §3 outcomes add no character clip, so this spec does not have to choose; the N2 sites are the Lead's to
   revisit if "how much" applies to a character clip too.
4. `driver_sources.py:450-451` keeps `out[-200:]` of a failed `inspect` output in a person's held question (`failed` list) — tool output
   tail, reported only (the class "tool output shown to a person" is not this spec's).
5. Critic Q2/Q3 (the inline LF rule in `take_answer`, the three copies of the notes-file road) are outside the brief; untouched.

---

## §9 Reading trail

Read (Read tool): the critic verdict `docs/tasks/specs/reviews/20261113-fv14-topic-code-critic.md` (whole); the FV1-4 spec (whole, three
pages); `PKG\scripts\app_card.py` (whole); `PKG\scripts\brief_pack.py:420-454, 1125-1139, 1568-1637, 1640-1769, 2620-2819, 3990-4139,
4412-4431`; `PKG\scripts\driver_sources.py:1-170, 419-473, 540-669`; `PKG\scripts\driver_runner.py:280-295`; `PKG\scripts\report_facts.py:935-969`
(via Grep -A and Read); `PKG\scripts\role_load.py:73-134`; `PKG\scripts\tests\test_brief_pack.py:1816-1868, 2895-2934`;
`PKG\scripts\tests\test_first_look_briefs.py:425-464`; `PKG\scripts\tests\test_story_run_words.py:150-309`;
`PKG\scripts\tests\test_story_run_refusals.py:385-444`; `PKG\scripts\tests\test_role_load.py:280-351`;
`PKG\scripts\tests\test_app_card_stand_lessons.py` (whole); `PKG\scripts\tests\test-layers.json:77-101, 7108-7119`;
`PKG\design\architecture.md:134-258`; `docs\TESTING.md` (whole); `docs\SIBLING_MAP.md:311-328, 452-455, 582-594`; `.git` HEAD ref of the
worktree (`.claude/worktrees/fv14-fix/.git`, `.git/worktrees/fv14-fix/HEAD`, `.git/refs/heads/wip/fv14-fix`).
Searched (Grep; positive controls): `def (_text_whole|_clipped|…)` on `brief_pack.py`; `_Pointer|WORDS_LINE_WIDTH…`; `_fl_line|…` over
`PKG` (the hits are the control); `whole: |_clipped\(|_text_whole\(` on `brief_pack.py`; `pasted|1500|…` on `driver_sources.py`;
`material supplied by the person` over `PKG` (control: the two product hits); `shown.text|shown_text` (-i) over `PKG\scripts`;
`record_pasted|…` over tests (count, then content); `app_card` over tests (count); `app-card|app_card|app card` (-i) over `PKG` md/py/json;
`CARD_MAX_BYTES` over `PKG`; `"(app_card|…)\.py"` over `test-layers.json` (control: many `driver_sources.py` hits); keep/quarantine
section heads of `test-layers.json`; `"file": "(app_card|driver_sources|brief_pack)\.py"` over `judgment-census.json` (control: the two
`brief_pack` rows); `_settings_problems|…` over tests (census row `:858` found); `app_card|app-card|FIRST_LOOK_LINE_CHARS` on the
told-before-work spec (empty; control `FIRST_LOOK_|T3b` finds 15 lines); `driver_sources` over `driver-layers.json`; `wip/fv14-fix` in
`packed-refs` (empty; the loose ref file found by Glob is the control); axis headings and `render` (-i) over `SIBLING_MAP.md`;
`^### AR-…|Change check` over `architecture.md`.
Not run: `scenario_walk.py --witness-for` (no shell): the files it prints are an estimate from `test-layers.json` `covers`.
Not opened: `factory-rules.md` (index only, loaded in the session), `references/walk-charter.md` beyond the Grep line, `GAP_TEXT_MAX`'s
value, `report_facts.py`'s keep tests (F6 not drafted), `test_app_card.py` beyond its Grep lines.

Needed beyond the manifest: `PKG\scripts\driver_runner.py`, `PKG\scripts\report_facts.py`, `PKG\scripts\tests\test_story_run_refusals.py`,
`test_story_run_words.py`, `test_first_look_briefs.py`, `test_app_card_stand_lessons.py`, `test_role_load.py`,
`PKG\scripts\tests\fixtures\judgment-census.json`, `driver-layers.json`, `test-layers.json`, the told-before-work spec (Grep only).
