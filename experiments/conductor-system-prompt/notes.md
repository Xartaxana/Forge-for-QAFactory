# Conductor prompt: replace or append (F-O4, card C5, node RD1-16, task t-1496)

Question (owner, 17.11): the orchestrator is to be replaced by the conductor entirely, so the conductor must cope. Today
`driver_runner.claude_cmd` appends `references/conductor.md` to the host's default system prompt
(`--append-system-prompt-file`). Does it cope when `conductor.md` REPLACES it (`--system-prompt-file`)?

## Step 1 (Lead, 18.11)

`claude 2.1.322 --help` lists `--system-prompt <prompt>` ("System prompt to use for the session") and
`--system-prompt-file`. A replacing flag exists. (Re-checked here: `claude --version` -> `2.1.322 (Claude Code)`.)

## Method

- Questions: three rows of the stand run's `state/conductor.jsonl` (`C:/QAFactory/mybooks-stand/arm-factory/test-automation-framework/qa-factory/artifacts/LOCAL-1/state/conductor.jsonl`,
  53 rows, 12-13.11), picked by session id, each a different class and each a session that ran commands:
  - `7c9e0b6f` row 0, boundary `S2:S2-qa-requirements-tester-1`, recorded action `continue` (exit-gate refusal, rework move).
  - `7bcc3333` row 1, boundary `S2:S2-qa-case-critic-3`, recorded action `ask_person` (why_person `gate_word`).
  - `6d1a7ffb` row 31, boundary `S5:S5-qa-code-critic-3:answer`, recorded action `retry` (a person's words, waivers).
- Replay input: the conductor row stores only `refusal[:2000]`, so the exact prompt is NOT in the row. It IS the first
  user message of the session's own transcript, `C:/Users/i_mas/.claude/projects/C--QAFactory-mybooks-stand-arm-factory-test-automation-framework/<session_id>.jsonl`
  (all 3 present). `run_pair.py` takes it verbatim; the only edits are path prefixes (stand project -> a copy; recorded
  plugin root `exp-fvf\pkg\qa-factory` -> `forge-repo\ai-packages\qa-factory`).
- Copy: `shutil.copytree` of the stand project to the OS temp dir (without `node_modules`, `test-results`, `.env`), one
  fresh copy per run, deleted after. The stand was only read: newest mtime in it is 13.11 00:57 (`driver-question.md`).
- Each question ran twice per arm (reps 1, 2): 3 questions x 2 reps = 6 pairs, 12 runs, all finished (none near 10 min;
  25-44 s each). Runs: `python -B run_pair.py --question <id> --rep <n> --out <OUT>`, 3 questions in parallel.
- Raw command lines (argv, from `<OUT>/<sid8>-<arm><rep>.cmd.txt`; `<OUT>` = `C:/Users/i_mas/AppData/Local/Temp/cps-out`):
  - A: `C:\Users\i_mas\AppData\Roaming\npm\claude.CMD -p --output-format json --permission-mode acceptEdits --model sonnet --allowedTools Bash,Read,Grep --plugin-dir C:\QAFactory\forge-repo\ai-packages\qa-factory --append-system-prompt-file C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md --max-turns 20`
  - B: the same line with `--system-prompt-file` in place of `--append-system-prompt-file` (diff of the two argv files: that one line only).
  - cwd = the copy; the prompt on stdin; (A) is built by `driver_runner.DriverRunner.claude_cmd` itself, (B) is its list with the one flag renamed.
- Carriers: `<OUT>/<sid8>-<arm><rep>.json` (claude's raw stdout; turns and tokens), `<OUT>/<sid8>-<arm><rep>.summary.json`
  (carries the transcript path), the session transcript under `C:/Users/i_mas/.claude/projects/C--Users-i-mas-AppData-Local-Temp-cps-<sid8>-<arm><rep>-<random>-project/<session>.jsonl`.
  No money figure is read or written (P18).

## Table (a-e per run; tokens are the `usage` of `<OUT>/<run>.json`)

in = input_tokens, cc = cache_creation_input_tokens, cr = cache_read_input_tokens.

| run | (a) turns | (b) in / cc / cr | (c) shape valid | (d) decision | (e) copes |
|---|---|---|---|---|---|
| 7c9e0b6f A1 | 2 | 4 / 26895 / 84284 | yes | continue: `story_step.py where` -> next is S7, "S2 is past its gate" | yes |
| 7c9e0b6f A2 | 3 | 4 / 30295 / 84292 | yes | continue (same reason) | yes |
| 7c9e0b6f B1 | 2 | 4 / 54490 / 52476 | yes | **different**: ask_person (`subjective`), read the two reference tables, ran no `where` | yes |
| 7c9e0b6f B2 | 2 | 4 / 20619 / 85138 | yes | continue via `controller.py rework S2 qa-requirements-tester` (the move the RECORDED session took); no `where` | yes |
| 7bcc3333 A1 | 2 | 4 / 30533 / 87662 | yes | ask_person `risk` | yes |
| 7bcc3333 A2 | 2 | 4 / 31889 / 87651 | yes | ask_person `subjective` | yes |
| 7bcc3333 B1 | 3 | 6 / 25090 / 145498 | yes | ask_person `gate_word` (same as the recorded class) | yes |
| 7bcc3333 B2 | 3 | 6 / 25212 / 145677 | yes | ask_person `gate_word` | yes |
| 6d1a7ffb A1 | 3 | 6 / 28765 / 141159 | yes | retry: waivers for refusal lines 1, 3, 4 | yes |
| 6d1a7ffb A2 | 4 | 8 / 29347 / 197873 | yes | retry: waivers for lines 1-4 | yes |
| 6d1a7ffb B1 | 2 | 4 / 22303 / 85708 | yes | retry: waivers for three lines | yes |
| 6d1a7ffb B2 | 2 | 4 / 21848 / 85708 | yes | retry: waivers for lines 1 and 3 | yes |

How (c), (e) were judged: (c) `run_pair.shape`: last line is JSON, `action` in the four, and for `ask_person`/`stop` a non-empty
`question`, `why_person`, `checked` and each option carrying token/move/says/factory/person/story. (e) in every summary
`tools.tool_errors` is empty (no `is_error` tool result), `permission_denials` is `[]` and `subtype` is `success` in all 12 raw
JSONs; and I read the B transcripts by hand (FR-26): 7c9e B1/B2, 7bcc B1/B2, 6d1a B1/B2 each made 1-2 well-formed Bash calls
(`python -c`, `controller.py`, `waiver.py`), each result was real output, and no turn re-explained tools. Not seen in any B run: a
refused command, a malformed call, a call to a tool outside Bash/Read/Grep (A1 of 6d1a used `Write`, an A run).

Readings:
- (a) Turns: A 2,3,2,2,3,4 (mean 2.7); B 2,2,3,3,2,2 (mean 2.3). No systematic change.
- (b) Cache creation (the part a smaller system prompt shrinks): A mean 29.6k; B mean 28.3k, or 23.0k without the one outlier
  (7c9e B1: 54.5k, a run that read more files). Cache read follows the turn count, not the arm. The total input per run is
  driven by turns; the default host prompt is not a large share of it here.
- (d) Decisions: 6d1a same class in all four; 7bcc same action in all four (the `why_person` class varies within A as well:
  `risk` / `subjective`, so the class is not a stable signal); 7c9e the only divergence: B1 asked the person where A both
  times continued. Reason of the divergence: the copy holds the stand's END state (S7), but the prompt is the S2 refusal of
  12.11, so the question has no single right answer in the copy; A took the cheap road (`where`), B1 asked, B2 reworked as the
  recorded session did. I accept it as a judgement difference, not a failure of the replaced prompt, but it is one run of six.

## Caveats (what this measures and does not)

- n = 6 pairs of one run's questions; a pilot, not a statistic. One question class not tried: `stop`.
- The copy is at the stand's final state, not at the state of each question (both arms see the same copy, so A against B is
  fair; the match with the RECORDED decision is not claimed except where stated).
- The prompts of 6d1a name an older plugin root (`exp-fvf\pkg-fix1\qa-factory`) that was not rewritten; the models used it for
  `waiver.py` in both arms (a package that exists on this machine). `--plugin-dir` was the forge checkout in both arms.
- `Write` is not in `--allowedTools` and was used once (A1 of 6d1a): `--permission-mode acceptEdits` lets it through; equal in both arms.
- Not tried: a tool call the guard refuses by design; a run that needs more than ~4 turns (the recorded sessions go up to 15).

## Verdict for the owner

**Switch.** On these 12 runs the conductor does as well with `conductor.md` as its whole system prompt as with it appended: every
answer had the valid shape, every tool call was well formed, nothing was refused, turns and tokens are no worse. Do it as its
own builder node (`driver_runner.claude_cmd` and the two callers) with a live-proof row, and watch the first live runs for the
7c9e kind of difference (asks the person where the appended prompt looked at state first). No short tool section is needed on this evidence.
