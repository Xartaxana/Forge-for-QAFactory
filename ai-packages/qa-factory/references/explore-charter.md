# Exploration charter - qa-runner at S6

Read with your brief: its `Exploration cells:` line names the file of the cells this charter talks about (read it before your
first capture; a dash in place of the file says why there is none), its `## The stand` section is where you
are, and the case of your window is the carrier of everything you find. You still run the case first; the charter adds what a
user's world does to the same flow.

<!-- kind: process -->
## Outcome

You try to break the story's flow the way the world breaks it for a user - a dependency fails, a field is keyed one character at a
time, the page is reloaded in the middle of a save - and you leave a `tried` table that says, for every cell you took, what the
requirements expect, what you saw and which captured file shows it.

<!-- kind: process -->
## Good outcome

The tier above accepts the window by these points, each with its witness:
1. The case of the window is judged first, by its own Thens, as the rest of your role says. No cell changes that verdict.
2. Every cell of `Exploration cells:` is one row of `work/evidence/manual/<case>/tried.md`: taken (outcome `held` or `violated`, with
   the evidence path) or `not tried` with the reason in words (a tool cannot do it, the stand refused, the cell does not apply - why).
   A field you met on the page is a cell too, one row per field and kind.
3. Every row names its hypothesis, its oracle and the observation that would refute it, written BEFORE the capture of that cell.
   The oracle quotes a requirement (`R-n`, the words); where the requirements are silent it is the axis oracle of your brief, and the
   row says `oracle: axis, requirements silent` - that row also carries a question (point 5).
4. Every `violated` row is an entry of the record's `observations[]` - `{step, expected, seen, evidence, quote}`, the quote copied
   from a capture of THIS attempt - so the analyst at S7 judges it. You never call it a bug; you never leave it in prose only.
5. Every doubt that is not a violated oracle - an intent you cannot tell, a cell you could not reach - is recorded the moment you meet
   it, with `exploratory_findings.py add`, not collected at the end.
6. "Nothing broke" is an outcome only with the table: an empty `observations[]` and an empty register with no `tried` rows is
   not a clean result, it is an unexplored flow, and it is returned.

| tried.md column | what it holds |
|---|---|
| cell | `<axis> x <request or field> x <kind>` as the brief spells it |
| hypothesis | `H-n`: the breakage you expect, one sentence |
| oracle | `R-n: "<quoted words>"`, or `axis, requirements silent` |
| refuted by | what you would see if the product is right |
| outcome | `held` / `violated` / `not tried: <why>` |
| seen | what the capture shows, in the product's words |
| evidence | the capture path under `work/evidence/manual/<case>/<attempt>/`, and `#obs<n>` or `EX-n` when there is one |

<!-- kind: craft -->
## Where bugs hide on this stage

- **A field whose value goes to the server on every change** (a quantity, an amount, a count). The page saves after the first
  character, shows a loading state, redraws, and the field is a new element: the second digit lands nowhere and "12" becomes "1".
  `fill` sets the whole value at once and hides it. Only typing one character at a time, then reading the value and the focus after
  each character and after the page settles, shows it.
- **The same field emptied.** An empty value goes out as null or "not a number"; the answer is an error message, a silent reset to an
  old value, or a removed row. Which one the requirements want is often unsaid - that is a question, not a guess.
- **Values past the stated limit**: 0, a negative number, the limit plus one, many digits. A silent clamp and a refusal in words are
  different behaviours; the requirement decides, never what the code happens to do.
- **Paste instead of typing.** A handler bound to keys never sees an inserted value.
- **A page composed from several requests.** When the code reads one answer without looking at its status, or one error boundary
  wraps the whole page, a single failing request (an error status or no answer at all) takes the whole page down. The other parts
  must still show, and the person must be told in words what is missing.
- **State held before sign-in that is merged into the account on sign-in** (a guest basket, a draft, a half-filled form). The merge
  call fails, the sign-in still says success, and the state is gone with no word. Silent loss of what the person had is a defect of
  impact even when no requirement names the merge.
- **A reload or back while a save is in flight**: the change is lost, applied twice, or shown as saved when it was not.

<!-- kind: craft -->
## Techniques

- **Hypotheses before the route.** Write the `H-n` of a cell - breakage, oracle, refuting observation - before you capture it. A
  hypothesis without a refuting observation cannot fail; rewrite it until it can.
- **Perturbation matrix.** The brief's cells are the matrix (`references/perturbations.json`: axes, kinds, axis oracles). Take every
  request cell; for the fields, take every input field of the flow you meet with every kind of `keyboard_input`.
- **One cell per call, with a control.** Fail ONE request per `ui` call, so a broken page is attributable. Look at the same step with
  no failure first: a page that looks the same without the failure says nothing about it.
- **Fail first, then act.** `fail_request` acts from its line on: put it before the `goto` or the action that sends the request, then
  capture `post_action`. A failure that never fired is named in `failures_without_hits`, and its `post_action` capture is refused -
  that cell is `not tried: the request was not sent` until you find the action that sends it.
- **Boundary values and equivalence classes** on every field: one value inside, one at the limit, one beyond it, empty, multi-digit.
  The limit comes from the requirements; if they give none, ask (point 5) and try 0, -1 and a long number anyway.
- **State transitions**: reload (`goto` the same address) right after the action that saves, before the page settles.
- **Sign-in as a state transition.** Build the state as a guest (add the item, fill the draft), then sign in through the page in the
  SAME `--session` (`fill-account` types the account's login and password), once plain and once with the merge request failed
  (`fail_request` on its glob, put before the sign-in submit). Compare what the account holds with what you built. If the page offers
  no guest state or no sign-in, the row is `not tried: <what the page does not offer>`.
- **Error guessing from the code facts in your brief** (a request whose answer is never checked, a `catch` that only logs): they say
  where to look first. They are never the oracle (code is never an oracle).

<!-- kind: process -->
## Tools

- `manual_capture.py ui --task-root <T> --case <C> --steps-file <S> --session <actor>`: the calls of the case join its open attempt,
  so the case and its cells share one attempt and one record. Steps you use here: `type <sel> <text> [<delay_ms>]` (one character at
  a time; the log has `n value focus=yes|no` per character, then `settled`), `press <sel> <key>` (`Control+A`, then `Backspace`,
  empties a field), `paste <sel> <text>`, `fail_request <url_glob> <status|timeout>`, `restore_request <url_glob>`, `goto <url>` (the
  same address reloads), `read`, `capture pre_action|post_action <label>`.
- What `fail_request` can and cannot do: browser requests to a stand host only; a status 400-599 with an empty JSON body, or a
  dropped request (`timeout` fails at once - it is not a slow answer); a request sent by the page's server is not seen.
- The glob of a request is printed in its cell line (the side file named by the brief's `Exploration cells:` line): copy it whole. It
  matches the full URL on any stand host, with or without a query string; a pattern you shorten by hand may not match, and the call
  then says `failures_without_hits`.
- `manual_evidence.py build ... --observations-file <file.json>`: the record, with the `violated` rows as `observations[]`.
- `exploratory_findings.py add --task-root <T> --by <your dispatch id> --kind observation|unresolved_question|coverage_gap --title ...
  --statement ... --why-not-a-bug ... --evidence <captured file>` (`--question` and `--owner-role` for a question,
  `--missing-prerequisite` for a gap).

<!-- kind: process -->
## When to ask

- The requirements are silent on what a failure or an odd value should do: record an `unresolved_question` (owner `person`, oracle
  `owner_question`) at once and go on with the next cell. Nothing in this charter stops the window.
- A cell the tools cannot do, or a request you know of that is not in your cells: a `coverage_gap` naming what is missing, and the row
  `not tried: <the gap>`. Never adapt the cell into something it is not.
- A call that ends `env_blocked` (exit 3): the refusals of your role apply. If the case's attempt is blocked, capture the case
  again in a new attempt without the cell that broke the stand, and say so in that cell's row and in a `coverage_gap`.
