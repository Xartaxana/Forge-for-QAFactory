# Pre-release 0.9 — common intent brief for every designer node (Lead, 06.10.2026)

> Superseded by D-0056 (21.10.2026) for verification scope; kept as the 0.9 record.

Read this before the node brief in your dispatch. Every node of `docs/tasks/pre-release-0.9.md`
is drafted from a Lead intent brief = this file + the node section in the dispatch text.

## Where things are

- Repository root (absolute, use it in every `owns:` path): `D:/ws1/yml-text-factory`.
- The package: `ai-packages/qa-factory/` — `scripts/` (code), `scripts/tests/` (its tests,
  `test_<name>.py`), `references/` (data files the code reads, FR-13), `skills/*/SKILL.md`,
  `agents/*.md`, `phases/*.md` (role texts), `hooks/`, `CHANGELOG.md`, `design/factory-rules.md`.
  Backlog rows name paths from `ai-packages/qa-factory/` (bare names = `scripts/`).
- The owner's decisions behind the nodes: `DECISIONS.md` D-0025…D-0031 (06.10.2026). D-0025 says
  every "owner's decision/answer" dated 02–06.10 inside the Codex-fixes branch material (wave-4
  decisions, "owner's answer 3" in code comments) was the branch author's word, not the owner's.
- Backlog rows: `plans/BACKLOG.md` lines 422–442 (B-361, B-364, B-373, B-399…B-416). Recon digests:
  `docs/tasks/single-tuning-inventory.md` (t-457), `docs/tasks/colleague-findings-2026-10-06.md`
  (t-460). Line numbers in those carriers were measured on 06.10.2026 on main 96a544c; verify
  every one you rely on by reading (designer rule 3).
- Rules the spec must satisfy: `ai-packages/qa-factory/design/factory-rules.md` (FR-1…FR-59; the
  index is `docs/FACTORY_RULES_INDEX.md`), `PROJECT.md` principles P1…P21, `plans/builder-rules.md`,
  `docs/SIBLING_MAP.md` (axes 1–8). Load-bearing: P1 (code helps a role, never replaces it), P2 and
  FR-13 (closed variety in data, open variety is a role's or a person's word), P9/FR-6 (text to a
  person in human words), P13 (a person's word passes any gate), FR-1/FR-57 (a refusal names what
  is wrong and a door), FR-15 (a path a role needs is given), FR-29 (no heredoc escape sequences, no
  control bytes), FR-30 (package English, no Cyrillic anywhere in the package), FR-33 (a fix is
  proved by a live run), FR-54 (siblings by the map).

## What you return — one spec per node (English), in the shape of `docs/tasks/specs/t-430-journal-merge-mode.md`

1. `# <node ids> — <subject>`; `## Why (measured)` — the facts, each with its carrier (file:line
   you read, not the brief); `## Intent` — the owner's decision verbatim from DECISIONS.md where
   one exists.
2. `## Requirements` — numbered; each names the file and the function/section it changes; a
   requirement that turns a code constant into data names the data file, its schema, and the
   default that keeps every existing project behaving as today.
3. `## Edges` — every limit, empty/absent input, conflicting pair, temporal edge (an artifact the
   change creates: behaviour before and after it exists, which move creates it), positional edge
   (where a branch goes and the invariant that position preserves). Each edge states the
   INVARIANT it protects (host adaptation 2, D-0021). A function reused in a more consequential
   role gets its error direction and adversarial inputs.
4. `## Acceptance keys` — what the Lead/critic checks; `## Tests` — the named test files, one
   mutation → the ONE test file that kills it (builder-rules 7a); `## Live proof (FR-33)` — what a
   live run (a story or an onboarding on a target project, or a CI job) must show for the node to
   count as proved; the release waits for it.
5. `## DoD` — the exact verification run(s), in backticks, from the repository root with no `cd`
   prefix and no `2>&1`: the node's test files
   (`python -B ai-packages/qa-factory/scripts/tests/test_<name>.py`), every existing test that
   imports a changed module (`grep -l "<module>" ai-packages/qa-factory/scripts/tests/*.py` — name
   them), `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`,
   `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`; `test_hooks_wiring.py` if
   hooks change, `test_gate_registry.py` if a gate/key/outcome word changes, `test_null_outcomes.py`
   if a mandatory list, a stage exit or a tool field changes, `test_words_doors.py` if a person's
   words carrier changes. The full `selftest.py` and `install_smoke.py` are NOT run on the owner's
   machine — CI runs them (`.gitlab-ci.yml`); say so in the DoD.
6. Manifest for the builder: `given:` (enumerated files/fixtures, sufficient), `owns:` (ABSOLUTE
   paths the builder may write — one per line right under `owns:`, no blank line), `non-goals:`,
   `handoff:` (what comes back: diff summary ≤ 500 words, the FR walk by touched sections A–G one
   line each, "needed beyond the manifest", "Needed from integration" for files it may not write,
   analogs noticed). Builder-rules item 1 lists integrator-only files (`CHANGELOG.md`,
   `selftest.py`, `install_smoke.py`, `plugin.json`, `README.md`, `INSTALL.md`,
   `templates/config.json`, `contract.py`, `qa-story/SKILL.md`): a node's builder writes one of them
   ONLY when the spec's `owns:` names it explicitly (the Lead grants it per node); the CHANGELOG
   `## Unreleased` line(s) always come back as TEXT in the handoff, the integrator writes them.
7. `## FR walk` — the sections A–G the diff will touch and the rules the builder must answer for.
8. `## Siblings` — SIBLING_MAP axes the change touches (by number) and the analogs you noticed
   outside the node (report, do not widen scope). `## Parallel nodes` — for every node the dispatch
   names as drafted in parallel on a shared file: the seam (the function/data key you expect from
   it, or the one you offer), so the builders can be serialized without rewriting.
9. `## Forks` — every design decision or intent reading, options + your recommendation (returned,
   never closed by you); `## Small choices closed`; `## Trail` — what you read (file:lines) and the
   searches with their controls.

Completeness criterion for the draft: every path in the node's "Пишет в" column is in `owns:` or
explicitly excluded with the reason; every requirement has an acceptance key and a test; every edge
has an invariant; every reading of intent not fixed by D-0025…D-0031 is a fork. Scope ceiling (rule
11): tests = acceptance keys + the edges + boundaries at and beyond each limit — no full regress.
Size caps (builder-rules 5): `skills/*/SKILL.md` ≤ 19000 bytes / 500 lines, `agents/*.md` ≤ 9000,
`references/*.md` ≤ 12000; text added to a role file is paid for by removing redundant text.
A spec that changes the MEANING of a field, a gate or a condition goes to a critic-on-plan review
before the builder (PROJECT.md item 6); mark such requirements with `[meaning]`.

Your final message is the whole draft (designer rule 5). You write nothing to the tree.
