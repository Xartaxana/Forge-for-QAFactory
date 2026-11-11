# t-2045 N0 - frame measurement (task t-2059)

Measured 2026-11-06 in the scratch folder `D:/ws1/mybooks-stand\tr-probe\_n0-t2045\` (removed at the end, see the last section). No package file, no existing file of the copy, no app was touched. Playwright 1.56.0 (from `tr-probe\node_modules`, a link to `tr-arm-b\node_modules`), Node v22.23.4, pytest 8.3.3.

## Deviations and gaps, first

- The pytest command of the spec was REFUSED by the factory plugin's PRE-TOOL GUARD ("a direct pytest launch is blocked, and a factory dispatch is open"). Per the spec edge, the Python shapes ran through `run_py.py` in the scratch folder, which calls `pytest.main([...])` with the same arguments (`-q --junitxml=...\py\junit.xml`). Source below. Not retried in the refused form.
- Shape (f) not measured (no browser run; the spec says "not measured", rule 2 applies).
- (p4) `hamcrest` does not import (`ModuleNotFoundError`): not measured, no row.
- (p6) `playwright` imports, but with no browser there is no Locator/Page: `expect(1, message=...)` raised `ValueError: Unsupported type: <class 'int'>` BEFORE any message use. So p6 does NOT measure the Playwright-for-Python message; it is "not measured". Its row is shown only as what it is.
- Jest and Vitest: not in `node_modules` (`ls node_modules | grep -i -E "jest|vitest|eslint-scope"` prints only `eslint-scope`; the positive control `eslint-scope` is found in the same call). Not measured, no row.
- The Playwright run took 61.6 s (exit 1, 11 failed, as forced); the pytest run 1.2 s. Whole under 2 minutes.
- The run output below is the tool's returned text; the tool dropped ~1.7k characters from the middle (the blocks of shapes c and d); the junit rows printed by the analysis script carry every shape's message and frames in full.

## Answers

### 1. Per runner, shape -> frame (line, col) -> inside the span "close of expect(...) .. matcher's ("

Playwright (TypeScript). "first" = the frame `assertion_site` reads (the deepest, first in the text). Column from the raw frame `file:line:col`. The span is computed by bracket balancing on a string-and-comment-blanked skeleton (script below).

| shape | kind | first frame (line:col) | span of its statement (close of expect(...) .. matcher's `(`) | inside |
|---|---|---|---|---|
| a `expect(thrower()).toBe(1)` | thrown | shapes.spec.ts 4:9 (in `thrower`, `throw` line, no expect) ; call site 13:10 | 13:19 .. 13:25 | NO (first: no expect on its statement; call site: before the close) |
| b `expect(await rejectsLater()).toBe(1)` | thrown | 9:9 (in `rejectsLater`) ; call site 17:10 | 17:30 .. 17:36 | NO |
| c `expect(1).not.toBe(1)` | inverted | 21:17 | 21:11 .. 21:21 | YES |
| d `expect(1).toBe(thrower())` | thrown | 4:9 ; call site 25:18 | 25:11 .. 25:17 | NO (after the matcher `(`) |
| e1 `await expect(Promise.reject(..)).resolves.toBe(1)` | thrown | 29:9 | 29:46 .. 29:61 | NO (col 9 = the `expect` token) |
| e2 `await expect(async()=>{..}).toPass({timeout:200})` | thrown | 33:55 | 33:53 .. 33:61 | **YES - a thrown shape INSIDE the span** |
| f `page.setContent(..)`/`toHaveText` | inverted | not measured (no browser) | - | - |
| g `expect(1)\n .not\n .toBe(1)` | inverted | 39:6 | 37:11 .. 39:10 | YES |
| h1 `expect` from `./fx` | inverted | h1.spec.ts 4:17 | 4:11 .. 4:21 | YES |
| h2 `expect(1, marker).not.toBe(1)` | inverted (marker in message) | 43:48 | 43:42 .. 43:52 | YES |
| i `expect(await po.get()).toBe(1)` | thrown | po.ts 3:11 ; call site i.spec.ts 5:19 | 5:24 .. 5:30 | NO |
| j helper `check()` holding `expect(1).toBe(2)` | check in helper | h.ts 4:13 (first) ; j.spec.ts 5:3 | h.ts 4:11 .. 4:17 | first YES; call site has no expect (OFF) |

pytest (Python): the frame has a LINE only (no column in the traceback), so a column span does not exist for Python; rows in answer 5. Nothing here is measured against the column rule for Python.

### 2. Decision rule (written before the run, spec N0) applied

Rule: every thrown shape (a, b, d, e1, e2, i) off the span AND every inverted shape (c, f, g, h1) on it -> that runner's `form_id` goes in `assertion_probes.typescript.line_proof_runners`; one miss or one shape not measured -> no row for that runner.

- thrown a, b, d, e1, i: off. **e2: ON the span (33:55 inside 33:53..33:61) - a MISS.**
- inverted c, g, h1: on. **f: not measured.**

Verdict: **NO ROW for Playwright.** `line_proof_runners` stays empty for typescript; marker-less forms go to the critic there; the owner is told. (Two independent reasons: the e2 miss and the unmeasured f.) No row for Jest/Vitest (not measured), none for Python (no column data; not a rule-2 candidate from this run). The only thing depending on this measurement is that row, and it is absent: a guess became no row.

One reading detail for N3b: in every sync-thrown shape the deepest frame lies in the throwing function or helper (a, b, d: `thrower`/`rejectsLater`; i: `po.ts`), so a line-only reader that takes the first frame sees a line with no `expect(` at all; a column is needed only for e1/e2 (frame in the spec file, on the statement itself), and e2's frame column is the name of the matcher `toPass` itself, the same place an inverted failure puts it (c: `toBe` name at col 17; g: col 6; h1: col 17).

### 3. `fires_as` T1/T2 against e1's text

Yes, T1 matches e1's text on a STRIPPED line. e1's failure text line is `    Error: expect(received).resolves.toBe()` (then `    Received promise rejected instead of resolved`); T1 `fires_as` (`^(?:Error: )?expect\(received\)(?:\.(?:resolves|rejects))?\.to[A-Z]\w*\(`) matches the stripped line `Error: expect(received).resolves.toBe()`. It does NOT match on the raw (4-space-indented) lines nor on the whole text with no flags (the text starts with the `[c] › file:line:col › name ───` header, so `^` anchoring finds nothing): whether the critic's suspicion bites depends on how N3b feeds the text (per stripped line = a thrown, never-asserted rejected promise reads as "the un-inverted form fired"). T2 does not match e1. Control: shape c (a real `.not.` failure, `Error: expect(received).not.toBe(expected) // Object.is equality`) matches T2 on the stripped line and not T1; a (a plain throw) matches neither. Output below (`fires.py`).

### 4. Frame order (`frames_deepest`)

- Playwright (TypeScript): **first**. j: frame list `h.ts:4:13` (inside `check`) THEN `j.spec.ts:5:3` (the caller). i: `po.ts:3:11` then `i.spec.ts:5:19`. a/b/d: the throwing function first, the spec's call site second. `failure_frames` returns them in text order; `assertion_site` returns the first.
- pytest (Python), from p2: the traceback lists the test frame first and the helper frame last (`test_n0.py:15` then `test_n0.py:7`); `assertion_site` (pytest's last traceback line) returns `test_n0.py:7`, the helper's raise line. So the deepest is **last**. (For p1/p5 there is a single user frame.)

### 5. Python

- Joined token `qa-probe-tok` in the JUnit failure message: p1 YES (`AssertionError: qa-probe-tok\nassert not 1 == 1`, also in the text); p5 YES (`AssertionError: 1 == 1 : qa-probe-tok`); p4 not measured (hamcrest absent); p6 not measured (ValueError before the message was used; token appears only in the text's echo of the source line, not the message).
- p7 (assert in a fixture, F12): row `status: error`, problem kind `error`, message `failed on setup with "AssertionError: fixture said no\nassert False"`; `assertion_site` gives `{'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:34', 'failure_kind': 'assertion'}` - an `assertion` kind at the FIXTURE's line (not the test's), on an `error` row.
- Last-line site of p2: `test_n0.py:7` (`raise AssertionError('stand said 503')` inside `helper`), kind `assertion` - the marker-less thrown helper reads as an assertion. p3: `test_n0.py:19`, kind `exception` (`ValueError: invalid literal for int()...`; the line is the `assert not (int('abc') == 1), 'm'` line).
- Row ids of p8: `mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p8[a]` (passed, `assertion_site {}`) and `...::test_p8[b]` (failed, `test_n0.py:43`, kind `assertion`). Other ids carry the same dotted-path prefix: `...test_n0::test_p1`, `...test_n0.TestP5::test_p5`.

## Verbatim frames (Playwright raw lines, from the junit rows)

```
a   at thrower (D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:4:9)
    at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:13:10
b   at rejectsLater (...\shapes.spec.ts:9:9) / at ...\shapes.spec.ts:17:10
c   at ...\shapes.spec.ts:21:17
d   at thrower (...\shapes.spec.ts:4:9) / at ...\shapes.spec.ts:25:18
e1  at ...\shapes.spec.ts:29:9
e2  at ...\shapes.spec.ts:33:55
g   at ...\shapes.spec.ts:39:6
h2  at ...\shapes.spec.ts:43:48
h1  at ...\h1.spec.ts:4:17
i   at Object.get (...\po.ts:3:11) / at ...\i.spec.ts:5:19
j   at check (...\h.ts:4:13) / at ...\j.spec.ts:5:3
```
(`...` stands for `D:/ws1/mybooks-stand\tr-probe\_n0-t2045`; the full lines are in the script output below.)

Code-frame lines Playwright printed for e2 and g, to show the caret column:
```
      32 | test('e2', async () => {
    > 33 |   await expect(async () => { await rejectsLater(); }).toPass({ timeout: 200 });
         |                                                       ^
      37 |   expect(1)
      38 |     .not
    > 39 |     .toBe(1);
         |      ^
```

## Run 1 - Playwright

Command: `node D:/ws1/mybooks-stand\tr-probe\node_modules\@playwright\test\cli.js test --config D:/ws1/mybooks-stand\tr-probe\_n0-t2045\playwright.config.ts` ; `exit=1 sec=61.6390151`. Output (the `NO_COLOR` node warnings and ANSI colour codes of the original are collapsed; the middle of the output, shapes c and d, was cut by the tool as stated above):

```
Running 11 tests using 4 workers
  1) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:12:1 › a
    Error: stand said 503
      2 |
      3 | function thrower(): number {
    > 4 |   throw new Error('stand said 503');
        |         ^
      5 | }
        at thrower (D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:4:9)
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:13:10

  2) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\i.spec.ts:4:1 › i
    Error: po said 503
       at po.ts:3
    > 3 |     throw new Error('po said 503');
        at Object.get (D:/ws1/mybooks-stand\tr-probe\_n0-t2045\po.ts:3:11)
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\i.spec.ts:5:19

  3) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\h1.spec.ts:3:1 › h1
    Error: expect(received).not.toBe(expected) // Object.is equality
    Expected: not 1
    > 4 |   expect(1).not.toBe(1);
        |                 ^
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\h1.spec.ts:4:17

  4) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\j.spec.ts:4:1 › j
    Error: expect(received).toBe(expected) // Object.is equality
    Expected: 2
    Received: 1
       at h.ts:4
    > 4 |   expect(1).toBe(2);
        |             ^
        at check (D:/ws1/mybooks-stand\tr-probe\_n0-t2045\h.ts:4:13)
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\j.spec.ts:5:3

  5) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:16:1 › b
    Error: action timed out
    >  9 |   throw new Error('action timed out');
        at rejectsLater (D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:9:9)
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:17:10

  [... shapes c, d: cut by the tool, present in the rows below ...]

  8) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:28:1 › e1
    Error: expect(received).resolves.toBe()
    Received promise rejected instead of resolved
    Rejected to value: [Error: x]
    > 29 |   await expect(Promise.reject(new Error('x'))).resolves.toBe(1);
         |         ^
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:29:9

  9) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:32:1 › e2
    Error: action timed out
    Call Log:
    - Timeout 200ms exceeded while waiting on the predicate
    > 33 |   await expect(async () => { await rejectsLater(); }).toPass({ timeout: 200 });
         |                                                       ^
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:33:55

  10) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:36:1 › g
    Error: expect(received).not.toBe(expected) // Object.is equality
    Expected: not 1
    > 39 |     .toBe(1);
         |      ^
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:39:6

  11) [c] › ..\mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:42:1 › h2
    Error: qa-probe-tok
    expect(received).not.toBe(expected) // Object.is equality
    Expected: not 1
    > 43 |   expect(1, ['qa-probe', 'tok'].join('-')).not.toBe(1);
         |                                                ^
        at D:/ws1/mybooks-stand\tr-probe\_n0-t2045\shapes.spec.ts:43:48

  11 failed
    h1, i, j, a, b, c, d, e1, e2, g, h2   (all [c], all failed)
exit=1 sec=61.6390151
```

## Run 2 - pytest (through `run_py.py`, after the guard refused the direct command)

Refused command: `python -m pytest D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py -q --junitxml=D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py\junit.xml` (PRE-TOOL GUARD: "a direct pytest launch is blocked, and a factory dispatch is open"). Run: `python -B D:/ws1/mybooks-stand\tr-probe\_n0-t2045\run_py.py` -> `exit=1`:

```
FFFFFE.F                                                                 [100%]
ERROR at setup of test_p7:   AssertionError: fixture said no   (test_n0.py:34)
test_p1:  AssertionError: qa-probe-tok / assert not 1 == 1      (test_n0.py:11)
test_p2:  helper() raise AssertionError: stand said 503         (test_n0.py:15 -> test_n0.py:7)
test_p3:  ValueError: invalid literal for int() with base 10: 'abc'   (test_n0.py:19)
TestP5.test_p5: AssertionError: 1 == 1 : qa-probe-tok           (test_n0.py:24)
test_p6:  ValueError: Unsupported type: <class 'int'>           (playwright\sync_api\__init__.py:142)
test_p8[b]: AssertionError: assert 'b' == 'a'                   (test_n0.py:43)
- generated xml file: D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py\junit.xml -
6 failed, 1 passed, 1 error in 1.16s
```
(Code-frame detail lines abbreviated to one line per test; the pytest long form was shown in full in the run and is reproduced by the reader below.)

## Reader output (both XMLs through `reporters.read_rows`, `assertion_site`, `failure_frames`)

Command: `python -B D:/ws1/mybooks-stand\tr-probe\_n0-t2045\analyse.py` (exit 0). Verbatim:

```
=== TYPESCRIPT (Playwright) ===
row keys: ['problems', 'status', 'test_id']

-- shape h1 id='h1.spec.ts::h1' status=failed
   message head (raw, escapes shown): '    Error: expect(received).not.toBe(expected) // Object.is equality'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\h1.spec.ts:4:17']
   assertion_site    : {'location': '_n0-t2045/h1.spec.ts:4', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\h1.spec.ts:4:17'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/h1.spec.ts', 4)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/h1.spec.ts', 4, 17)]
   FIRST(deepest, the one assertion_site reads) h1.spec.ts:4:17: close of expect(...) at (4, 11); matcher '(' at (4, 21); INSIDE span: True; text 'expect(1).not.toBe(1);'

-- shape i id='i.spec.ts::i' status=failed
   message head (raw, escapes shown): '    Error: po said 503'
   raw frame lines   : ['at Object.get (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\po.ts:3:11)', 'at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\i.spec.ts:5:19']
   assertion_site    : {'location': '_n0-t2045/po.ts:3', 'failure_kind': 'exception', 'frame': '        at Object.get (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\po.ts:3:11)'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/po.ts', 3), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/i.spec.ts', 5)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/po.ts', 3, 11), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/i.spec.ts', 5, 19)]
   FIRST(deepest, the one assertion_site reads) po.ts:3:11: no expect( on its statement -> OFF span; text "throw new Error('po said 503');"
   frame#2 i.spec.ts:5:19: close of expect(...) at (5, 24); matcher '(' at (5, 30); INSIDE span: False; text 'expect(await po.get()).toBe(1);'

-- shape j id='j.spec.ts::j' status=failed
   message head (raw, escapes shown): '    Error: expect(received).toBe(expected) // Object.is equality'
   raw frame lines   : ['at check (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\h.ts:4:13)', 'at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\j.spec.ts:5:3']
   assertion_site    : {'location': '_n0-t2045/h.ts:4', 'failure_kind': 'exception', 'frame': '        at check (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\h.ts:4:13)'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/h.ts', 4), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/j.spec.ts', 5)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/h.ts', 4, 13), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/j.spec.ts', 5, 3)]
   FIRST(deepest, the one assertion_site reads) h.ts:4:13: close of expect(...) at (4, 11); matcher '(' at (4, 17); INSIDE span: True; text 'expect(1).toBe(2);'
   frame#2 j.spec.ts:5:3: no expect( on its statement -> OFF span; text 'check();'

-- shape a id='shapes.spec.ts::a' status=failed
   message head (raw, escapes shown): '    Error: stand said 503'
   raw frame lines   : ['at thrower (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:4:9)', 'at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:13:10']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:4', 'failure_kind': 'assertion', 'frame': '        at thrower (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:4:9)'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 4), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 13)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 4, 9), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 13, 10)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:4:9: no expect( on its statement -> OFF span; text "throw new Error('stand said 503');"
   frame#2 shapes.spec.ts:13:10: close of expect(...) at (13, 19); matcher '(' at (13, 25); INSIDE span: False; text 'expect(thrower()).toBe(1);'

-- shape b id='shapes.spec.ts::b' status=failed
   message head (raw, escapes shown): '    Error: action timed out'
   raw frame lines   : ['at rejectsLater (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:9:9)', 'at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:17:10']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:9', 'failure_kind': 'assertion', 'frame': '        at rejectsLater (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:9:9)'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 9), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 17)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 9, 9), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 17, 10)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:9:9: no expect( on its statement -> OFF span; text "throw new Error('action timed out');"
   frame#2 shapes.spec.ts:17:10: close of expect(...) at (17, 30); matcher '(' at (17, 36); INSIDE span: False; text 'expect(await rejectsLater()).toBe(1);'

-- shape c id='shapes.spec.ts::c' status=failed
   message head (raw, escapes shown): '    Error: expect(received).not.toBe(expected) // Object.is equality'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:21:17']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:21', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:21:17'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 21)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 21, 17)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:21:17: close of expect(...) at (21, 11); matcher '(' at (21, 21); INSIDE span: True; text 'expect(1).not.toBe(1);'

-- shape d id='shapes.spec.ts::d' status=failed
   message head (raw, escapes shown): '    Error: stand said 503'
   raw frame lines   : ['at thrower (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:4:9)', 'at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:25:18']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:4', 'failure_kind': 'assertion', 'frame': '        at thrower (D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:4:9)'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 4), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 25)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 4, 9), ('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 25, 18)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:4:9: no expect( on its statement -> OFF span; text "throw new Error('stand said 503');"
   frame#2 shapes.spec.ts:25:18: close of expect(...) at (25, 11); matcher '(' at (25, 17); INSIDE span: False; text 'expect(1).toBe(thrower());'

-- shape e1 id='shapes.spec.ts::e1' status=failed
   message head (raw, escapes shown): '    Error: expect(received).resolves.toBe()'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:29:9']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:29', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:29:9'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 29)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 29, 9)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:29:9: close of expect(...) at (29, 46); matcher '(' at (29, 61); INSIDE span: False; text "await expect(Promise.reject(new Error('x'))).resolves.toBe(1);"

-- shape e2 id='shapes.spec.ts::e2' status=failed
   message head (raw, escapes shown): '    Error: action timed out'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:33:55']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:33', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:33:55'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 33)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 33, 55)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:33:55: close of expect(...) at (33, 53); matcher '(' at (33, 61); INSIDE span: True; text 'await expect(async () => { await rejectsLater(); }).toPass({ timeout: 200 });'

-- shape g id='shapes.spec.ts::g' status=failed
   message head (raw, escapes shown): '    Error: expect(received).not.toBe(expected) // Object.is equality'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:39:6']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:39', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:39:6'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 39)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 39, 6)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:39:6: close of expect(...) at (37, 11); matcher '(' at (39, 10); INSIDE span: True; text '.toBe(1);'

-- shape h2 id='shapes.spec.ts::h2' status=failed
   message head (raw, escapes shown): '    Error: qa-probe-tok'
   raw frame lines   : ['at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:43:48']
   assertion_site    : {'location': '_n0-t2045/shapes.spec.ts:43', 'failure_kind': 'assertion', 'frame': '        at D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\shapes.spec.ts:43:48'}
   failure_frames    : [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 43)]
   frames with column: [('D:/ws2/mybooks-stand/tr-probe/_n0-t2045/shapes.spec.ts', 43, 48)]
   FIRST(deepest, the one assertion_site reads) shapes.spec.ts:43:48: close of expect(...) at (43, 42); matcher '(' at (43, 52); INSIDE span: True; text "expect(1, ['qa-probe', 'tok'].join('-')).not.toBe(1);"

=== PYTHON (pytest junit) ===

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p1'
   status: failed | problem kind: failure
   message attr: 'AssertionError: qa-probe-tok\nassert not 1 == 1'
   joined token qa-probe-tok in message/text: True / True
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:11', 'failure_kind': 'assertion'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p2'
   status: failed | problem kind: failure
   message attr: 'AssertionError: stand said 503'
   joined token qa-probe-tok in message/text: False / False
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:7', 'failure_kind': 'assertion'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p3'
   status: failed | problem kind: failure
   message attr: "ValueError: invalid literal for int() with base 10: 'abc'"
   joined token qa-probe-tok in message/text: False / False
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:19', 'failure_kind': 'exception'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0.TestP5::test_p5'
   status: failed | problem kind: failure
   message attr: 'AssertionError: 1 == 1 : qa-probe-tok'
   joined token qa-probe-tok in message/text: True / True
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:24', 'failure_kind': 'assertion'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p6'
   status: failed | problem kind: failure
   message attr: "ValueError: Unsupported type: <class 'int'>"
   joined token qa-probe-tok in message/text: False / True
   assertion_site: {'location': 'C:\\Users\\dev1\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\sync_api\\__init__.py:142', 'failure_kind': 'exception'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p7'
   status: error | problem kind: error
   message attr: 'failed on setup with "AssertionError: fixture said no\nassert False"'
   joined token qa-probe-tok in message/text: False / False
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:34', 'failure_kind': 'assertion'}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p8[a]'
   status: passed | problem kind: None
   message attr: ''
   joined token qa-probe-tok in message/text: False / False
   assertion_site: {}

-- test_id='mybooks-stand.tr-probe._n0-t2045.py.test_n0::test_p8[b]'
   status: failed | problem kind: failure
   message attr: "AssertionError: assert 'b' == 'a'\n  \n  - a\n  + b"
   joined token qa-probe-tok in message/text: False / False
   assertion_site: {'location': '..\\mybooks-stand\\tr-probe\\_n0-t2045\\py\\test_n0.py:43', 'failure_kind': 'assertion'}
```

Notes on this output: (1) `failure_kind: assertion` for a/b/d thrown shapes is the reader's label for ANY frame in the test file (it compares the file only), i.e. a throw in `thrower()` inside the spec file reads as an `assertion` at the throw line; only a throw in a different file (i: `po.ts`, j: `h.ts`) reads `exception`. (2) An earlier pass of the script mislabelled kinds/shapes (name key and a drive-letter regex bug); both were fixed in the script before this final run, the printed run is the final one.

## fires_as check (answer 3)

Command: `python -B D:/ws1/mybooks-stand\tr-probe\_n0-t2045\fires.py` (exit 0). Verbatim:

```
-- e1: first non-empty lines of the failure text: ['[c] › shapes.spec.ts:28:1 › e1 ───────────────────────────────────────────────────────────────────', '    Error: expect(received).resolves.toBe()', '    Received promise rejected instead of resolved']
   T1 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=['Error: expect(received).resolves.toBe()']
   T2 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
-- e2: first non-empty lines of the failure text: ['[c] › shapes.spec.ts:32:1 › e2 ───────────────────────────────────────────────────────────────────', '    Error: action timed out', '    Call Log:']
   T1 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
   T2 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
-- a: first non-empty lines of the failure text: ['[c] › shapes.spec.ts:12:1 › a ────────────────────────────────────────────────────────────────────', '    Error: stand said 503', '      2 |']
   T1 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
   T2 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
-- c: first non-empty lines of the failure text: ['[c] › shapes.spec.ts:20:1 › c ────────────────────────────────────────────────────────────────────', '    Error: expect(received).not.toBe(expected) // Object.is equality', '    Expected: not 1']
   T1 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
   T2 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=['Error: expect(received).not.toBe(expected) // Object.is equality']
-- h1: first non-empty lines of the failure text: ['[c] › h1.spec.ts:3:1 › h1 ────────────────────────────────────────────────────────────────────────', '    Error: expect(received).not.toBe(expected) // Object.is equality', '    Expected: not 1']
   T1 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=[]
   T2 fires_as: search(whole text, no flags)=False; per raw line=[]; per stripped line=['Error: expect(received).not.toBe(expected) // Object.is equality']
```

## Script sources

`playwright.config.ts`:
```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({ testDir: '.', retries: 0, timeout: 5000, reporter: [['junit', { outputFile: 'junit.xml' }]], projects: [{ name: 'c' }] });
```

`shapes.spec.ts` (line numbers as in the frames):
```ts
import { test, expect } from '@playwright/test';

function thrower(): number {
  throw new Error('stand said 503');
}

async function rejectsLater(): Promise<number> {
  await new Promise((r) => setTimeout(r, 10));
  throw new Error('action timed out');
}

test('a', () => {
  expect(thrower()).toBe(1);
});

test('b', async () => {
  expect(await rejectsLater()).toBe(1);
});

test('c', () => {
  expect(1).not.toBe(1);
});

test('d', () => {
  expect(1).toBe(thrower());
});

test('e1', async () => {
  await expect(Promise.reject(new Error('x'))).resolves.toBe(1);
});

test('e2', async () => {
  await expect(async () => { await rejectsLater(); }).toPass({ timeout: 200 });
});

test('g', () => {
  expect(1)
    .not
    .toBe(1);
});

test('h2', () => {
  expect(1, ['qa-probe', 'tok'].join('-')).not.toBe(1);
});
```
`fx.ts`: `export { test, expect } from '@playwright/test';` ; `h1.spec.ts`: `import { test, expect } from './fx';` + `test('h1', () => {` / `  expect(1).not.toBe(1);` / `});` ; `po.ts`: `export const po = { get(): number { throw new Error('po said 503'); } };` (formatted over 5 lines, throw on line 3) ; `i.spec.ts`: imports `po`, `test('i', async () => {` / `  expect(await po.get()).toBe(1);` ; `h.ts`: `export function check(): void {` / `  expect(1).toBe(2);` / `}` (line 4 holds the expect) ; `j.spec.ts`: `import { check } from './h';` `test('j', () => {` / `  check();` (line 5).

`py\test_n0.py`:
```python
import unittest

import pytest


def helper():
    raise AssertionError('stand said 503')


def test_p1():
    assert not (1 == 1), '-'.join(['qa-probe', 'tok'])


def test_p2():
    assert not (helper())


def test_p3():
    assert not (int('abc') == 1), 'm'


class TestP5(unittest.TestCase):
    def test_p5(self):
        self.assertNotEqual(1, 1, msg='-'.join(['qa-probe', 'tok']))


def test_p6():
    from playwright.sync_api import expect
    expect(1, message='-'.join(['qa-probe', 'tok'])).not_to_be_visible()


@pytest.fixture
def broken():
    assert False, 'fixture said no'


def test_p7(broken):
    assert True


@pytest.mark.parametrize('v', ['a', 'b'], ids=['a', 'b'])
def test_p8(v):
    assert v == 'a'
```

`run_py.py` (the pytest-through-script fallback):
```python
import sys
import pytest

sys.exit(pytest.main([r"D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py", "-q",
                      "--junitxml=D:/ws/mybooks-stand\\tr-probe\\_n0-t2045\\py\\junit.xml"]))
```

`fires.py`:
```python
import json
import re
import sys

sys.path.insert(0, r"D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts")
import reporters as R  # noqa: E402

DET = json.load(open(r"D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json", encoding="utf-8"))
PAIRS = {p["id"]: p["fires_as"] for p in DET["assertion_probes"]["typescript"]["assertions"][0]["invert"]}
rows = {r["test_id"].split("::")[-1]: r for r in R.read_rows("D:/ws2/mybooks-stand/tr-probe/_n0-t2045/junit.xml", "junit-xml")}
for shape in ("e1", "e2", "a", "c", "h1"):
    text = rows[shape]["problems"][0]["text"]
    lines = text.splitlines()
    print(f"-- {shape}: first non-empty lines of the failure text: {[l for l in lines if l.strip()][:3]!r}")
    for pid, rx in PAIRS.items():
        c = re.compile(rx)
        whole = bool(c.search(text))
        per_line = [l for l in lines if c.search(l)]
        stripped = [l.strip() for l in lines if c.search(l.strip())]
        print(f"   {pid} fires_as: search(whole text, no flags)={whole}; per raw line={per_line!r}; per stripped line={stripped!r}")
```

`analyse.py` (full source, final version; it reads `reporters.read_rows` -> `assertion_site` (TS `frames`/`skip_frames`/`frame_path` from `detectors.json`, `pytest_command=False`; pytest rows `pytest_command=True`) -> `failure_frames`, and the span by bracket balancing):
```python
import json
import re
import sys

sys.path.insert(0, r"D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts")
import reporters as R  # noqa: E402

ROOT = "D:/ws2/mybooks-stand/tr-probe/_n0-t2045"
DET = json.load(open(r"D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json", encoding="utf-8"))
TS = DET["assertion_probes"]["typescript"]

FILES = {"a": "shapes.spec.ts", "b": "shapes.spec.ts", "c": "shapes.spec.ts", "d": "shapes.spec.ts",
         "e1": "shapes.spec.ts", "e2": "shapes.spec.ts", "g": "shapes.spec.ts", "h2": "shapes.spec.ts",
         "h1": "h1.spec.ts", "i": "i.spec.ts", "j": "j.spec.ts"}


def skeleton(text):
    """Blank out string literals and comments (same length), enough for bracket balancing here."""
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i)); i = j
        elif ch in "'\"`":
            j = i + 1
            while j < n and text[j] != ch:
                j += 2 if text[j] == "\\" else 1
            out.append(ch + " " * (j - i - 1) + ch); i = j + 1
        else:
            out.append(ch); i += 1
    return "".join(out)


def balanced_close(sk, open_idx):
    depth = 0
    for k in range(open_idx, len(sk)):
        if sk[k] in "([{":
            depth += 1
        elif sk[k] in ")]}":
            depth -= 1
            if depth == 0:
                return k
    return None


def span_of(text, line):
    """Statement holding `line` (1-based): from after the previous ; { } at/above the line to its ; ; then
    close of the first expect(...) and the matcher's ( that follows."""
    sk = skeleton(text)
    starts = [0]
    for m in re.finditer(r"\n", text):
        starts.append(m.end())
    ls = starts[line - 1]
    k = ls
    # walk back over blank/prefix: the statement starts at the first non-space char of the nearest line at/above that begins an expect(
    ln = line
    while ln >= 1:
        seg = sk[starts[ln - 1]:(starts[ln] if ln < len(starts) else len(sk))]
        if re.search(r"\bexpect\s*\(", seg):
            break
        ln -= 1
    if ln < 1:
        return None
    seg_start = starts[ln - 1]
    m = re.search(r"\bexpect\s*\(", sk[seg_start:])
    eo = seg_start + m.end() - 1
    ec = balanced_close(sk, eo)
    mm = re.compile(r"\s*\.\s*(?:(?:resolves|rejects|not)\s*\.\s*)*(?:toBe|toPass|toHaveText)\w*\s*\(").match(sk, ec + 1)
    if not mm:
        return {"expect_open": eo, "expect_close": ec, "matcher_paren": None}
    return {"expect_open": eo, "expect_close": ec, "matcher_paren": mm.end() - 1}


def lc(text, idx):
    line = text.count("\n", 0, idx) + 1
    col = idx - (text.rfind("\n", 0, idx) + 1) + 1
    return line, col


def raw_frame_lines(row, frames, skips):
    out = []
    rxs = [re.compile(p) for p in frames]
    sk = [re.compile(p) for p in skips]
    for p in row.get("problems") or []:
        for line in (p.get("text") or "").splitlines():
            if any(r.search(line) for r in sk):
                continue
            if any(r.search(line) for r in rxs):
                out.append(line.strip())
    return out


print("=== TYPESCRIPT (Playwright) ===")
rows = R.read_rows(ROOT + "/junit.xml", "junit-xml")
print("row keys:", sorted(rows[0].keys()))
for row in rows:
    name = row.get("test_id") or ""
    shape = name.split("::")[-1].strip()
    status = row.get("status")
    problem = (row.get("problems") or [{}])[0]
    text = problem.get("text") or ""
    head = next((l for l in text.splitlines() if l.strip().startswith("Error")), "")
    fname = FILES.get(shape, "")
    test_file = f"{ROOT}/{fname}"
    site = R.assertion_site(row, "junit-xml", "D:/ws2/mybooks-stand/tr-probe", test_file, pytest_command=False,
                            runtime="node", frames=TS["frames"], skip_frames=TS["skip_frames"], frame_path=TS["frame_path"])
    allf = R.failure_frames(row, TS["frames"], TS["skip_frames"])
    print(f"\n-- shape {shape} id={name!r} status={status}")
    print("   message head (raw, escapes shown):", repr(head[:120]))
    print("   raw frame lines   :", raw_frame_lines(row, TS["frames"], TS["skip_frames"]))
    print("   assertion_site    :", site)
    print("   failure_frames    :", allf)
    # raw frame (the first one) with column
    cols = []
    for line in raw_frame_lines(row, TS["frames"], TS["skip_frames"]):
        m = re.search(r"((?:[A-Za-z]:)?[^\s():][^():]*?):(\d+):(\d+)\)?$", line)
        if m:
            cols.append((m.group(1).replace("\\", "/"), int(m.group(2)), int(m.group(3))))
    print("   frames with column:", cols)
    for idx, (path, line, col) in enumerate(cols):
        tag = "FIRST(deepest, the one assertion_site reads)" if idx == 0 else f"frame#{idx + 1}"
        src = open(path, encoding="utf-8").read()
        sp = span_of(src, line)
        stmt = src.splitlines()[line - 1].strip()
        if not sp:
            print(f"   {tag} {path.rsplit('/', 1)[-1]}:{line}:{col}: no expect( on its statement -> OFF span; text {stmt!r}")
            continue
        e_line, e_col = lc(src, sp["expect_close"])
        mp = sp["matcher_paren"]
        m_line, m_col = (lc(src, mp) if mp is not None else (None, None))
        fr = (line, col)
        lo = (e_line, e_col)
        hi = (m_line, m_col) if mp is not None else None
        inside = hi is not None and lo <= fr <= hi
        print(f"   {tag} {path.rsplit('/', 1)[-1]}:{line}:{col}: close of expect(...) at {lo}; matcher '(' at {hi}; INSIDE span: {inside}; text {stmt!r}")

print("\n=== PYTHON (pytest junit) ===")
rows = R.read_rows(ROOT + "/py/junit.xml", "junit-xml")
for row in rows:
    problem = (row.get("problems") or [{}])[0]
    text = problem.get("text") or ""
    msg = problem.get("message") or ""
    site = R.assertion_site(row, "junit-xml", "D:/ws2/mybooks-stand/tr-probe", ROOT + "/py/test_n0.py", pytest_command=True)
    print(f"\n-- test_id={row.get('test_id')!r}")
    print("   status:", row.get("status"), "| problem kind:", problem.get("kind"))
    print("   message attr:", repr(msg[:150]))
    print("   joined token qa-probe-tok in message/text:", "qa-probe-tok" in msg, "/", "qa-probe-tok" in text)
    print("   assertion_site:", site)
```
Known weakness of the span script (stated, not hidden): the statement is found by walking back to the nearest line holding `expect(`, strings/`//` comments are blanked, template-literal interpolation and regex literals are not handled; fine for these forced shapes, not a production reader. The matcher regex it accepts is `toBe*`, `toPass`, `toHaveText*` with optional `.resolves/.rejects/.not`.

## Before / after listing of `tr-probe` top level, and the folder's removal

Before (`ls -A D:/ws2/mybooks-stand/tr-probe`, taken before any file of the scratch folder was written): `.claude .env .git .github .gitignore core env.example eslint.config.js global-setup.ts global-teardown.ts mock-server.mjs mock-server.ts node_modules package.json package-lock.json playwright.config.ts playwright-report qa-factory reports scripts storage-state TEST_AUTOMATION_BEST_PRACTICES.md test-cases test-results tests tsconfig.json` (27 entries; the earlier `ls -la` also showed `test-results` mtime Nov 6 09:01 before my run).

Scratch folder content at removal time (`Get-ChildItem -Force`): `py/ analyse.py fires.py fx.ts h.ts h1.spec.ts i.spec.ts j.spec.ts junit.xml playwright.config.ts po.ts run_py.py shapes.spec.ts` (Playwright's own `test-results` outputDir did not appear in it).

Removal: `Remove-Item -Recurse -Force D:/ws1/mybooks-stand\tr-probe\_n0-t2045 -Confirm:$false` ; `Test-Path D:/ws1/mybooks-stand\tr-probe\_n0-t2045` -> `False`.

After (`Get-ChildItem -Force D:/ws1/mybooks-stand\tr-probe`): `.claude .github core node_modules playwright-report qa-factory reports scripts storage-state test-cases test-results tests .env .git .gitignore env.example eslint.config.js global-setup.ts global-teardown.ts mock-server.mjs mock-server.ts package-lock.json package.json playwright.config.ts TEST_AUTOMATION_BEST_PRACTICES.md tsconfig.json` - the same 27 names; no `_n0-t2045`, no `.pytest_cache`, no new top-level entry (this lists names only; contents of existing folders were not diffed).

## Needed beyond the manifest

- `reporters.py` internals beyond the three named functions: `_junit` row shape (`test_id`, `status`, `problems[{kind,message,text}]`) learned by running; `_pytest_site`/`_TRACE_TAIL` behaviour read from the output.
- The spec itself says "Nothing else" for `given`; I additionally read `detectors.json` lines 248-300 for T1/T2 `fires_as` (named in answer 3).

## Same-class observations (not fixed, not in scope)

- `assertion_site` labels a throw inside a local function of the SAME test file as `failure_kind: assertion` (a, b, d above) and `junit` rows of a hard throw read as assertions at the throw line; N3b should not read `failure_kind` as "a check failed" without the statement.
- The pytest PRE-TOOL GUARD refuses a direct `pytest` command inside any open factory dispatch, including a measurement in a scratch folder with no test of the factory; the script fallback worked. The spec edge already names it.
