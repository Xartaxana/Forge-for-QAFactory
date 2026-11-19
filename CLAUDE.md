# CLAUDE.md — QA Factory development

Auto-loaded into every session and every worker: only what every reader applies — the dispatch form (rule 11), command
hygiene, worker duties, language. A worker's own rules are `.claude/agents/<role>.md` and its dispatch. The
coordinator's rules are not here: the SessionStart line `COORDINATOR RULES:` names their files.

## Worker duties

- A self-activating
   enforcement file (a hook on the active hooks path, etc.) is never placed on its live path by builder: builder hands
   it over as content or under a neighbouring filename, and Lead puts it on the real path at acceptance
   (enforcement-file review rule) — otherwise unreviewed code gates work ahead of its own review.

- A worker trims run output before it enters its context (`-q`, a 30-line tail, `Read` with a limit over 400 lines, `Grep` instead of reading a whole file) and closes a round with ONE witness run after all edits, never one after each edit (D-0035).

## The dispatch form (rule 11)

### Rule 11 · DoD in every dispatch

11. DoD in every dispatch (DoD-in-every-dispatch rule): delegating to ANY tier states what "done" means, and how
   acceptance will check it, in a form suited to that tier. builder: acceptance criteria + a verification run whose
   output becomes the witness, AND the spec NAMES ITS EDGE BEHAVIOR: for every limit/truncation it introduces, every
   empty/absent/None input its data can carry, and every pair of its own requirements that can conflict, the
   expected behavior is stated — or the fork is returned as an explicit question; a spec silent on an edge that its
   own requirements create is a dispatcher defect, not a guess left to the performer. Two sub-classes are dispatcher
   defects when silent: (i) TEMPORAL — an artifact the change itself brings into existence (a config, file or flag
   absent at spec time, present after): the behavior is stated for BOTH worlds, and the spec says which move creates
   it; (ii) POSITIONAL — when the spec prescribes WHERE in existing logic a branch goes (order, precedence,
   before/after which check), it states the INVARIANT that position must preserve (what stays unreachable, what must
   still be refused), not the location alone.

### Rule 11 · which tests a DoD asks for

   Which tests a DoD asks for: the rule text is `docs/TESTING.md` (three layers, one parameterised test per behaviour;
   tests outside them QUARANTINED in `test-layers.json`; SCOPE CEILING: that text, nothing more). Input from OUTSIDE
   (a CLI/UI that accepts user input, a ticket, a person's words, a project config, a host answer) gets an
   adversarial mini-battery — magnitude, nesting, encoding, empty/broken input — and every limit applied to it a
   case AT and BEYOND it, each a scenario variant row; an internal boundary gets no test. When the SessionStart line
   says `TEST QUARANTINE ALERT` or `READY TO DELETE`, the Lead tells the owner the same turn (detectors: check 33,
   `tools/test_quarantine.py check` in the nightly CI job
   `quarantine-check`).

### Rule 11 · scout and critic DoD; the manifest; the five-point checklist

   scout: an explicit question and a completeness criterion; "X is nowhere to be found" is a valid outcome and
   requires a trail. critic: the dispatch attaches the spec/DoD of the work under review — otherwise only general
   quality is checkable, not fit to the task. A dispatch with no DoD is returned by the worker as questions, before
   work starts. Alongside the DoD a dispatch carries a CONTEXT MANIFEST (dispatch-context-manifest rule): "given" —
   the files/data injected into the worker (its sufficiency is the Lead's responsibility); a WRITING dispatch also
   carries "owns" (the paths it may write), "non-goals" and "handoff" (what comes back for acceptance); a parallel
   fan-out declares ownership per COORDINATOR.md rule 4 plus an optional maxConcurrent cap. The manifest is DECLARATIVE on reads and
   NORMATIVE on writes: the worker reads the repo freely, and going past the basket is a report line "needed beyond
   the manifest", not a violation; for a targeted read-only dispatch the manifest is the explicit enumeration of what
   is attached. A writing/parallel dispatch with no manifest is returned as questions too. Completeness of the DoD
   and the manifest is the DISPATCHER's duty BEFORE sending, run as a FIVE-POINT CHECKLIST against every dispatch:
   (1) an explicit question / completeness criterion or acceptance keys; (2) the DoD inline (below)
   AND the edge behaviors NAMED — limits/truncations, empty/absent inputs, conflicting requirement pairs: stated, or
   explicitly forked up; (3) "given" enumerated AND sufficient — data, fixtures, paths NAMED, not implied; (4) a
   writing dispatch: owns/non-goals/handoff present and its witness scope named (COORDINATOR.md rule 4); (5) freshness — the spec's
   load-bearing facts checked against their carrier, not memory. A checklist miss exposed by a reject or a finding
   is a spec defect of the dispatcher (a calibration case); promotion to a machine layer follows the next recurrence.

### Rule 11 · inline DoD; the DOC-DISPATCH witness

   The DoD is written INLINE in the dispatch — named acceptance criteria plus the exact verification run; a bare
   pointer to a spec file or an earlier event is NOT a DoD. A brief carries FACTS by pointer: `given:` names the frozen
   file (a hand-back report, a digest) and the digest's objects by their exact ids (`q2a, q2b`), never by a prefix, so a
   scout's reservation travels with its object; changing code is pointed at by `path::symbol`, not a line range. The
   DoD, the edges and the non-goals stay inline. Prose outside the manifest is at most about 8 counted lines (a target
   read by calibration check 34, not a gate). DOC-DISPATCH WITNESS: when the owns are markdown/config
   with no test set of their own, a deterministic key-presence run is a legal mechanical layer ONLY with three
   properties: (i) the keys are quoted VERBATIM from the DoD as written BEFORE the run; (ii) the script is attached in
   FULL source with the witness in the report, never committed as a test; (iii) the run includes a NEGATIVE control
   (one key deliberately absent → the script reports failure). Missing any of the three → the witness is a
   retelling, not a run (detector: calibration check 13(k)). A worker returning a DoD-less or manifest-less dispatch
   is an emergency net, not the normal cycle: frequent returns are a coordinator defect, flagged at calibration.
   Lead-tier tasks are covered by their own mechanisms (the Lead exam, weekly calibration).

   | R11 | when | duty |
   |---|---|---|
   | m | a WRITING dispatch's "given" manifest | executed as a MARKED declaration: an inline enumeration, OR a pointer to a persisted spec that itself carries the enumeration, ONE hop away — no marker, no manifest; `owns` itself is always given INLINE, never by pointer |
   | f | a dispatch to builder, or any dispatch whose `owns:` holds an absolute path (D-0022) | carries its manifest as HEADER LINES outside fences and quotes: `given:`, `owns:` (absolute paths, on that line or right under it, no blank line, no heading marks; a path with spaces in backticks), `non-goals:`, `handoff:`, `edges:`, `DoD:` (the verification command in backticks), `siblings:` (entries, or `none -- <why>`) and, over COORDINATOR.md rule 2's threshold, `designer:` (the accepted draft's absolute path, `skip -- <reason>`, or `resubmission <task_id>`); `python -B tools/dispatch_new.py` prints these lines checked (never typed by hand); `tools/dispatch_manifest.py` refuses a dispatch without them and names what is missing; the informed pass is a line `manifest-skip: <item>[, <item>] -- <reason>` |
   | h | critic/designer dispatch | report path on `handoff:`, never `owns:`; `tools/dispatch_gate.py` refuses a dispatch whose `handoff:` names no single `.md` file in the role's folder; `tools/handoff_gate.py` lets it write only that file; a critic's probe (`.claude/agents/critic.md` rule 21) is no write of its own: the runner restores the file from a byte copy; a designer dispatch also carries `facts:` (COORDINATOR.md rule 2) |

## Command hygiene (permission hygiene)

The deployment runs in auto mode; three behaviours are refused by `tools/hygiene_gate.py`, every other form is allowed.
Doors: `git -C <dir> <cmd>`, `python -B <abs path>`, a Bash `( cd <dir> && ... )` subshell, a PowerShell
child shell, a byte copy (`cp`/`Copy-Item`) and its restore.

1. Tests — the canonical form, from the repo root: `python -m pytest tools/ -q` or a narrower target; locally only
   the narrow target the work needs; the full sets run on CI, never on this machine (PROJECT.md, package change p. 2);
   the canonical form of a tool = its correctly invoked form, the invocation that finds a known sample.
2. The proxy server — not used in this deployment: the contour is subscription and nothing in gateway/ is run.
3. The shell's working directory never moves (`cd`, `Set-Location`, `Push-Location`), not even inside one command (the
PowerShell location outlives the call): refused; the Bash `( cd <dir> && ... )` subshell is the door. Hooks run
`python tools/...` relative to the cwd: after a move they find no `tools/*.py` and EVERY tool is blocked. Package tests
that need the package as cwd run in the builder's worktree. A hook that "cannot find" its tools/ script -> stop and reset the
session folder to the root.

4. File edits — by any tool (the owner's word 16.11.2026: the Edit/Write-only rule is retired); a worker still writes
   only inside its `owns`, judged by the diff at acceptance.

5. Log entries — through `tools/journal_write.py` only (the owner's word 14.11.2026): a redirect, tee, in-place editor
   or payload that writes `logs/journal/*.jsonl` or `logs/routing-log.jsonl` is refused; an Edit/Write of them draws a
   WARN until node B23-S makes it a refusal.

### Command hygiene · point 6 — a claim needs a measurement

6. An environment-negative claim requires verification: empty output or "command not found" from an INCORRECTLY
   invoked tool is a miscall, not proof the object is absent; a negative claim about the environment ("the
   service/key/file is missing") is valid only after a positive check using the canonical form (point 1). Not just
   negatives — ANY load-bearing claim about environment state (a quota, a time window, a resource's presence,
   "already ready/open") in a report to the operator or in a plan is valid only after verification by measurement (the
   canonical command / an external clock / a database / a provider); an unverified claim carries an explicit
   "estimate, not verified" label. Worker claims are covered by witness/trail; this point closes the gap for Lead
   itself. The same class covers ANY content search (grep/glob/script) over the repo: an empty result is reportable
   only after a positive control of the invocation — the same tool and syntax must find a sample known to exist. The
   control shares the SHAPE of the checked call (case profile, type/glob filters): a control with a different pattern
   proves the pipe, not the absence (shell-grep alternation needs -E; -P needs a UTF-8 locale; the Grep tool is
   case-sensitive by default — a content-negative claim requires a case-insensitive search). Same class — the STATUS
   of a registry entry (escalations, decisions, tasks, ledgers): a claim about it is valid only after reading THROUGH
   that entry's status line, or grepping the status field itself; the entry merely appearing inside a read window is
   NOT a check — append-only registries put the verdict at the END of a multi-section entry.

   | pt.6 | when | duty |
   |---|---|---|
   | a | a project decision rests on an UNKNOWN property of the environment | run ONE experiment first; building machinery instead of measuring is legitimate only when the measurement itself doesn't port (e.g. a port number) or the experiment would be destructive |
   | b | a measured number appears in a norm/report | it carries its counting carrier (file/command) alongside it, or it isn't written at all; a comparison stays inside ONE metric |
   | c | a character-level claim (a slash, a case, a specific symbol) | valid ONLY by reading the carrier directly (the Read tool); a search tool's output is not a basis for it |

### Command hygiene · point 7 — probes

7. Temporary corruption (a probe) is rolled back by a BYTE COPY, never by `git checkout` /
   `git restore`: (a) take the copy BEFORE corrupting, and restore FROM IT; (b) the gate refuses these on a dirty
   path whatever its status was before, so the byte copy is the only road for a probe; (c) the
   witness is the VERBATIM comparison (a hash or a diff), not "restored"; (d) a live artifact (a ledger, a
   registry) is not corrupted at ALL when a pure function's verdict proves the point: corrupt a COPY.

## Язык

- **В чате с владельцем — по-русски.**
- **Всё, что уходит в релиз, — по-английски и без единого символа кириллицы:** файлы пакета
  (включая CHANGELOG и фикстуры тестов), сообщение релизного коммита, заголовок и описание PR в
  `QAFactory`. Пакет проверяет `python -B scripts/selftest.py --lang` (FR-30), и эта
  проверка входит в полный прогон перед пушем. Сообщение коммита и текст PR код не проверяет:
  перед пушем их вычитывают на кириллицу так же, как пакет.
- Рабочие документы этого репозитория вне пакета (`PROJECT.md`, `plans/`, `docs/`,
  `experiments/`) в релиз не уходят, поэтому могут быть на русском. Исходники страниц КБ в `kb/`
  пишутся по-английски: `kb/` в список русскоязычных не входит.
