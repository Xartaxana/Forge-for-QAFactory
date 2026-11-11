# Boot Sequence

The repository is the only source of truth.

Note: CLAUDE.md (the routing policy) auto-loads into every session on
its own — that auto-load is NOT a boot. Full state recovery is this
sequence, run on the operator's request ("restore context from
BOOT.md" or equivalent).

When starting a new session, read Layer A then Layer B:

## Layer A — Orientation (stable, always read)

1. Read SYSTEM_PROMPT.md.
2. Read DECISIONS.md.

If the SessionStart hook's output already includes a "--- BOOT LAYER A
INJECTED ..." block (verbatim content of these two files, closed by a
"--- END BOOT LAYER A: N files, N lines, N bytes emitted ---" line),
Layer A is ALREADY in your context — do not re-read these files. Read
a file anyway only if the closing line is missing (a truncated
injection) or that file is shown as "[missing: ...]" (it was not
printed).

## Layer B — State (the current in-flight picture, read yourself)

3. Read CURRENT_CONTEXT.md.

Layer B is NOT injected by the SessionStart hook — the session reads
it itself, every time (it is the source of the Boot Report below).

## Read when needed, not at boot

- README.md — setup after a clone; written for a person.
- DELEGATION_TABLE.md — the routing table; read at calibration and when
  a task type's tier is in doubt.

After loading these documents, produce a Boot Report per
PROCESS/BOOT_REPORT_PROTOCOL.md (the template and its rules live
there):

- summarize the current state;
- name the current milestone;
- name the next task;
- then STOP and wait for the operator's explicit confirmation.

Boot recovery is not work authorization: do not start the next task
(reading further files for implementation, writing code) until the
operator confirms.

If repository content conflicts with chat history, the repository
always wins.
