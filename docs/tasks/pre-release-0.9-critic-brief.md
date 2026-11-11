# Pre-release 0.9 — common brief for every critic-on-plan dispatch (Lead, 06.10.2026)

You review a DESIGNER DRAFT that the Lead has accepted with fork decisions written at its top ("Lead
decisions"). The review runs BEFORE any builder starts (PROJECT.md "Как принимается изменение пакета"
item 6; CLAUDE.md rule 3, critic-on-plan). Repository root: `D:/ws1/yml-text-factory`. The
designer's shared brief is `docs/tasks/pre-release-0.9-brief-common.md`; the graph is
`docs/tasks/pre-release-0.9.md`; the owner's decisions are `DECISIONS.md` D-0025…D-0031.

## What to review against

1. **Facts by trail.** Every load-bearing claim in "Why (measured)" and in the requirements: open the
   carrier (file:line) and confirm it. Verify at least every claim the requirements rest on and
   EVERY negative claim ("X is nowhere"), each with a positive control of the same form (command
   hygiene point 6). A wrong fact is a finding with the carrier quoted.
2. **Each `[meaning]` requirement**: is the new meaning of the field / gate / condition the right
   one, and is every edge of it decided correctly (not just named)? Error direction of every reused
   function in a more consequential role: does the spec's direction hold under the adversarial
   inputs it lists, and which inputs it missed?
3. **The Lead's fork decisions**: challenge each one; say where you would decide otherwise and why
   (facts, rules, cost). A decision that contradicts an owner's decision in DECISIONS.md or a
   principle in PROJECT.md is a finding.
4. **Feasibility**: can a builder implement it from this text alone (rule 11: DoD inline, edges
   named, given sufficient, owns absolute)? Name every place where the builder would have to guess.
5. **Class-wide completeness** (rule 9, FR-54): walk `docs/SIBLING_MAP.md` axes 1–8 for this change
   and the "Parallel nodes" seams; a sibling the spec neither fixes nor queues is a finding; a seam
   that two parallel specs describe differently is a finding (read the other spec's seam section).
6. **Tests and witness**: one mutation → one killing test file; boundaries at and beyond; the
   DoD commands runnable from the repository root with no `cd`; the live proof (FR-33) concrete.
7. **Rules**: FR walk honest (FR-1/57 doors, FR-13 data vs code, FR-6/P9 human text, FR-41/59
   unknowns, FR-29/30); P1–P3 (code helps the role, never replaces it; the conductor is called for
   a problem, never to run a command); the size caps.
8. **Duplication and consistency** (the owner, 06.10.2026): does the spec make the builder write a
   second implementation of something the package already has — a reader, a writer, a helper, a data
   table, a refusal text builder, a path resolver? Name the existing one with file:line and say
   whether the spec should reuse it, extend it, or has queued the convergence. A grep of the same
   shape over the package is the positive control for "no second implementation". For a diff gate
   the same duty, plus code quality, is `docs/tasks/critic-diff-brief.md`.

You may run read-only commands (grep, git log/show, a Python one-liner that reads) as controls;
you write nothing to the tree and change no file. Do not re-derive the whole design: the verdict
layer is yours, the mechanics the designer already read are checked by spot-reading.

## What you return (the whole report in your final message)

- `## Verdict` per spec: `accept` / `accept with amendments` / `reject` — one line each with the
  reason.
- `## Amendments` — a numbered list; each item: the spec section it changes, the exact text to
  replace or add (so the Lead can apply it by hand), the evidence (file:line or rule), and whether
  it BLOCKS the builder or may follow.
- `## Fork challenges` — the Lead decisions you would overturn, with the argument; or "none".
- `## Missed siblings and seams` — per SIBLING_MAP axis one line (applied / n/a / finding).
- `## Spot-checks` — the claims you verified with their carriers, and the negatives with their
  controls.
- `## Trail` — what you read (file:lines) and the commands you ran.

Keep it under ~1500 words per spec; a finding is a fact with a carrier, not an opinion.
