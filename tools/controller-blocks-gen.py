"""design/controller-blocks.md — every block of the controller and the route through it.

Both classes the controller refuses with reach the caller as a refusal, and they mean
different things:

  StateConflict — the request is fine, the story's recorded state says no.
  ValueError    — the request itself is malformed; the story has not been consulted yet.

So a fourth route exists beside person / command / unpassable: `caller`, where nobody needs a
person at all because the call was built wrong. Keeping them apart is the point of the walk:
the S5 window gate raised ValueError for a STATE block, which is exactly how it ended up with
no route for a person's word.
"""
import ast
import pathlib
import re
import sys

import streams

ROOT =pathlib.Path(__file__).resolve().parents[1] / "ai-packages" / "qa-factory"
SRC = ROOT / "scripts" / "controller.py"
LIT = re.compile(r'"((?:[^"\\]|\\.)+)"')


def refusal_classes() -> frozenset:
    """Every class a refusal of the controller is raised as: `ValueError` and what the event store
    derives from it (`StateConflict`, `DerivedViewStale`, ...). Derived from the module that defines
    them - the same way `test_controller_blocks.py` does, so the walk and its test cannot disagree
    about what a block is. A fixed pair of names let a subclass escape the walk."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import event_store
    found = {"ValueError"}
    for value in vars(event_store).values():
        if isinstance(value, type) and issubclass(value, ValueError) and value.__module__ == event_store.__name__:
            found.add(value.__name__)
    return frozenset(found)

PERSON_HEADS = ("S1 source collection pending/invalid", "S3 structured test plan invalid",
                "S5 completion needs a window acceptance")

COMMAND = {
    # G1-5: window 1 of S3 labels the table and writes no plan; no word of a person closes the stage from it, the driver's door is `finish --not-complete`
    "a window-1 (labelling) dispatch of S3 cannot close the stage": "the driver accepts window 1 with `story_step.py finish --not-complete --unresolved plan_pending`; the stage is closed by the exit window",
    # t-1455 q1: `prepare` with a derived EMPTY automated half names the empty half and its two doors
    "the automated half of the approved plan is empty": "a manual block (`story_step.py start --stage S6 --role qa-runner --execution-kind manual --scope <1..5 ids>`) for the manual-agent cases, or a plan row's disposition changed (S3 rework, then gate A)",
    # `_retry_holds` (F6) is the one head of the refusals of a superseded dispatch; each site adds its own door after it.
    "accept {retry[-1]}": "accept the retry, which the message names",
    "finish or pause {retry[-1]}": "finish or pause the retry, which the message names (`story_step.py finish` / `pause`)",
    # TR1-9 B3 (AR-25): a row a code close passed over; the refusal names the door itself
    "was passed over when its stage was closed by code": "`controller.py --operation rework`, which the message names: going back over the stage",
    # TR1-9 B4: the passed-over list in the request is stale; the close is sent again from the state as it is now
    "the state moved while the close was prepared": "send the close again: the request is rebuilt from the state as it is now",
    "approved Gate A required before deployment":"the gate decision itself (`gate-decision`)",
    "managed lifecycle requires work/test-plan.json": "the strategist writes the plan; `plan_row.py --add-row` adds one row",
    "current Gate A decision required": "`gate-decision --words-file <file>` records the person's approval",
    "current Gate ": "`gate-decision --words-file <file>` records the person's approval of that gate",
    "Gate A sources changed": "`--operation semantic_reopen`, then a new gate decision",
    "Gate A plan content changed after approval": "`--operation semantic_reopen`, then a new gate decision",
    "Gate A semantic plan content changed after approval": "`--operation semantic_reopen`, then a new gate decision",
    "Gate A oracle content changed after approval": "`--operation semantic_reopen`, then a new gate decision",
    "Gate A coverage-contract revisions changed after approval": "`--operation semantic_reopen`, then a new gate decision",
    "COVERAGE_CONTRACT_REVISION_REQUIRED": "`--operation coverage_migration` with its dry-run receipt",
    "source inventory required before completed discovery": "`ticket_adapter.py collect` writes the inventory",
    "sources pending/invalid": "`ticket_adapter.py collect|assess`, then `accept-gap` for what is unreachable",
    "S1 requires canonical source inventory": "`ticket_adapter.py collect` writes it",
    "S1 unavailable sources require explicit unresolved gap handoff": "the person's `ticket_adapter.py accept-gap` first (the refusal prints it), then a plain `story_step.py finish`, which derives `unresolved` and `reason` from the inventory",
    "checkpoint active work before revising scope": "`--operation checkpoint`",
    "checkpoint active work before reopening Gate A": "`--operation checkpoint`",
    "checkpoint active work before code-only completion": "`--operation checkpoint`",
    "checkpoint active work before invalidation": "`--operation checkpoint`",
    "resume existing dispatch; do not replace its checkpoint": "`--operation dispatch` with the retry packet `recover` prints",
    "sequential task already has an active dispatch": "`where` answers it with `wait_existing_job`; the driver knows this one by name",
    "cancellation requires the active dispatch": "`--operation request_cancel` on the running dispatch",
    "host worker is still active or cancellation unacknowledged": "wait for it, or cancel and acknowledge",
    "only a checkpointed dispatch can be resumed": "`--operation checkpoint` first",
    # FB-4 (`resume`): every refusal names the door of its own cause. The status of the record decides which one.
    "is superseded: this work was set aside": "`--operation next` prints what holds the stage now",
    "is {status}: it is not stopped": "`story_step.py finish` or `pause` takes the dispatch as it is",
    "is incomplete: it stopped with work left": "the retry packet `--operation recover` prints",
    "it never reached an agent, or a person set it free": "the relaunch packet `--operation next` prints",
    "its work is closed; going back over it is": "`--operation rework`",
    "only a dispatch stopped for a person (blocked or paused) is resumed": "`--operation next` prints what the story does now",
    "stopped on the story budget": "a person's word on the story budget, or fresh work with a new input hash",
    "has no recorded agent and the request names none": "`--agent-id <the id the Agent call returned>`, or the retry packet when that agent is gone",
    "is held by agent {mine}, the request names {theirs}":"the retry packet `--operation recover` prints",
    "stale stop: the request retires": "`story_step.py resume` builds the request again from the journal",
    "the story closed at {closed} (gate B is decided and S8 is done): a closed": "`--operation reopen_story` or `--operation rework`, each with the person's words",
    "no recorded stop to resume": "the retry packet `--operation recover` prints",
    "retry must inherit checkpoint": "the retry packet `recover` prints carries it",
    # `DerivedViewStale`: the event IS committed and only what follows it failed. Repeating the
    # action would write it twice; `recover` re-projects and refreshes (the driver runs it itself).
    "derived view not refreshed": "`--operation recover` refreshes the view; the event is committed, so the action is NOT repeated",
    # A continuation (`parent_retry` / `relaunch_of`) is tied to the dispatch it names; the packet
    # `next` prints is built from that dispatch's own record, so dispatching it as it stands passes.
    # SC1-7 R3 (S7-11): an accept/checkpoint request with no "id" key - the call's own field; the refusal lists the keys it had
    # and prints the conductor's door. Before the continuation row below, which this head would otherwise match.
    "the request names no dispatch": "put the dispatch's id in the request's `\\\"id\\\"`; the refusal lists the keys the request had and prints the door (`story_step.py finish`, or `--operation checkpoint` with flags)",
    "names no dispatch": "dispatch the `dispatch_request` (relaunch) or `packet` (retry) that `--operation next` prints for it, as it stands",
    "is {old.get('status')}: only a": "go back over accepted work with `--operation rework`; resume a stopped role with its retry packet (`recover` prints it)",
    "repeats that dispatch's work": "dispatch the `dispatch_request` that `--operation next` prints, as it stands; different work is a new dispatch sent without `relaunch_of`",
    "changed retry inputs require explicit invalidation": "`--operation invalidate` names what changed",
    "hard quota exhaustion is not automatically retried": "a person's decision to go on, recorded at the gate or as a waiver on the stage",
    "packet checkpoint threshold reached": "`--operation checkpoint`, then a fresh packet",
    "cumulative packet budget reached": "the person's word on the story budget (`STORY BUDGET` reaches them by the driver's own table)",
    "required prior logical stage incomplete": "close that stage, or skip it with a recorded reason",
    "scope expansion requires plan/gate revision": "`--operation revise_plan`, then the gate",
    # HF8-6: S4 before any gate A decision; the scope is the pinned cases and `--all` records it itself
    "the review scope does not hold yet": "`case_versions.py --task-root <root> --all` for a case file that exists; name the cases for a plan row",
    # `revise_plan` read the story's case files to resolve the scope and they do not build (a collision, a mismatch): the
    # story's files are at fault, not the call (`StateConflict`), and the message names them and the command that pins again.
    "the case index cannot be built": "fix the case files the message names, then `case_versions.py --task-root <root> --all` pins the cases again",
    # A dispatch REPLAYED under its committed id with another scope (CX1-11, N-2): the store's refusal made specific, raised
    # in `apply`. The committed scope is in the message; the door is the scope it was committed with, or the plan revision.
    "idempotency key reused with different inputs: dispatch": "re-send the scope the dispatch was committed with, or `--operation revise_plan` with the new scope and a new gate A decision",
    # A hand-written `revise_plan` key REUSED for another request (CX2-17, A6): the store's refusal made specific, raised in `apply`.
    # The two forms follow the fields that differ (a scope, or the plan's other fields); the door is a key of its own.
    "idempotency key reused with a different scope: the key": "a new `--operation revise_plan` request with a key of its own and the current `expected_revision`; the refusal names both, and the scope the key was committed with",
    "idempotency key reused with different": "a new `--operation revise_plan` request with a key of its own and the current `expected_revision`; the refusal names the fields that differ",
    "manual runner block must name 1..5 unique in-scope cases": "the refusal lists each problem with its door; a block over 5 is split (`story_step.py start` prints the next block)",
    "technical normalization preserves an existing current Gate A only": "`--operation semantic_reopen`",
    "semantic content changed; use semantic_reopen": "`--operation semantic_reopen`",
    "semantic reopen requires current approved Gate A": "`gate-decision` first",
    "fresh orchestrator context is not verified for this host": "`host_capability: manual_continuation` in the handoff",
    "orchestrator telemetry requires current lease": "`--operation handoff` takes the lease first",
    "host cannot provide verified orchestrator telemetry": "nothing: the host has no such capability, and the counters stay unknown",
    "coverage migration requires an active version 1 task": "nothing: the story is already v2",
    "coverage migration plan hash is stale": "re-run the dry-run on the current plan",
    "coverage migration dry_run failed": "fix what the dry-run names, then migrate",
    "only a stopped dispatch can be reconciled": "`--operation checkpoint` or `release` first",
    "reconciliation requires an accepted successor": "accept the successor first",
    "successor must cover the same stopped work": "dispatch a successor with the same scope and inputs",
    "dispatch reconciliation requires current expected_revision": "read `where` again and retry with the current revision",
    "unknown dispatch": "`--operation dispatch` registers it; `recover` prints the packet",
    "a stopped dispatch is not accepted": "retry it and accept the retry; the message carries the command",
    "only the active dispatch can finish": "finish the active one",
    "CASE_REVIEW_AFTER_GATE_A": "`--operation technical_normalize` or `semantic_reopen`",
    "instance obligation_refs do not match the current approved plan": "`manifest_put.py --fragment` re-binds them, or the plan is revised",
    "unresolved window": "the role resolves them, or the accept names them `unresolved` with a reason",
    "this window hands": "accept with `unresolved` naming the handed outcome and a reason",
    "this window holds instances the stand blocked": "accept it as `unresolved` naming `blocked_by_env` with a reason; `story_step.py finish` derives that pair from the window record",
    # HF1-14 (`_s5_gap_problems`): a probe gap no recorded word of the person names is refused even with a typed `unresolved` pair
    # (the orchestrator records the person's waiver, then the record is built again); a probe gap the person accepted closes the
    # window only as an unresolved acceptance naming `probe_gap`, which `story_step.py finish` derives from the window record.
    "this window claims a probe gap no recorded word of the person names": "the orchestrator records the person's waiver (`waiver.py --stage S5 --block \"<probe gap prefix> <instance id>\"`), then `window_record.py` builds the record again; otherwise `probe_by_code.py` writes the receipt",
    "this window holds named probe gaps": "accept with `unresolved` naming `probe_gap` and a reason; `story_step.py finish` derives that pair from the window record",
    # HF2-4b (`_s5_gap_problems`): a red test the requirement contradicts closes the window only as an unresolved acceptance naming
    # `contradicts_requirement`; `story_step.py finish` derives that pair from the window record, so no role types it.
    "this window holds red tests the requirement contradicts": "accept it as `unresolved` naming `contradicts_requirement`; `story_step.py finish` derives that pair from the window record",
    "a completed process with gaps cannot be passed_green": "name the gaps in the accept instead of claiming green",
    "coverage v2 S5 completion requires distinct accepted":"dispatch the missing half of the author/critic pair",
    "accepting": "pass `stage_complete: true` with the unresolved work named; the message carries the shape",
    "policy references stale source revision": "read the current source revision into the policy",
    "policy must bind the exact approved scope": "bind the approved scope",
    "preparatory policy requires completed S4": "close S4 first",
    "preparatory policy requires current Gate A approval": "`gate-decision` first",
    "preparatory policy cannot replace completed execution": "nothing: the execution already happened",
    "policy already recorded": "nothing: it is idempotent and already there",
    "stage already completed": "nothing: it is already closed",
    "invalidation names unknown records": "name records this story has",
    "invalidation may name only dispatches in its affected scope": "widen the affected scope, or invalidate the right dispatch",
    "Gate A applicability must name the current approved Gate A decision": "name the current decision",
    "Gate A applicability requires explicit unchanged requirements and oracle": "say which are unchanged, explicitly",
    "Gate A applicability must bind the unchanged current plan revision": "bind the current plan revision",
    "Gate A applicability must preserve the exact approved scope": "keep the approved scope",
    "mutation names an unknown author dispatch": "name an author dispatch that exists",
    "reviewed mutation needs an active independent qa-code-critic dispatch": "dispatch the critic",
    "author mutation must be checkpointed before independent review": "`--operation checkpoint`",
    "mutation writes must belong to an active author dispatch": "dispatch the author",
    "persist intent before changing files": "record the intent mutation first",
    "mutation progress cannot skip evidence steps": "record the steps in order",
    "which holds nothing back": "nothing: that status releases nothing",
    "initialize task before work": "`--operation initialize`",
    # SC1-14 B1b (the S5 plan order and the accept of a plan): the story's state says no; each message names its door.
    "the plan critic judges the author's plan": "`story_step.py start --stage S5 --role qa-automator --purpose s5_plan` dispatches the author's plan first",
    "the plan of {role} is accepted": "`--operation rework --stage S5 --role <role> --purpose s5_plan`: an accepted plan is reworked, not dispatched again",
    "the plan has {len(findings)} gap(s)": "the author mends the gaps `s5_plan.py --task <T> --check` names; the conductor returns them whole",
    "the rows the rework may change cannot be told": "the critic completes the form of the last review and `finish` stamps its receipt; the conductor returns it whole",
    "the rework changed the rows of": "the author keeps to the blocker rows; the conductor returns the refusal whole (a person's words on the rework lift the bound)",
    "the review {d['id']} cannot be read": "the critic completes the handover form; `finish` stamps the receipt; the conductor returns the refusal whole",
    "the review contradicts itself": "the critic makes the verdict and the list of remarks say one thing; the conductor returns the refusal whole",
    "the plan changed after this review was stamped": "the critic looks again at the current plan; the conductor returns the refusal whole",
    "the look scoped {": "the critic looks again over the moved rows (`rework --role qa-code-critic --purpose s5_plan --cases <moved>`); the conductor returns the refusal whole",
    "remark id(s) {": "the critic continues the numbering of the chain (PR-n); the conductor returns the refusal whole",
    # ValueError, but about the story's own evidence rather than the request's shape.
    "S5 window record is incomplete": "`window_record.py --task <T> --dispatch <ID>` writes every one of these from what is on disk",
    "S5 window needs a nonempty exact scope_instances map": "`window_record.py` builds the map from the manifest",
    "S5 window instances do not exactly cover the dispatched scope": "`window_record.py` rebuilds it for the dispatched scope",
    "coverage v2 task requires an S5 window schema_version 2": "`window_record.py` writes the current schema",
    "coverage v2 instance requires unique obligation_refs": "`manifest_put.py --fragment` binds the obligations",
    "coverage v2 instance requires execution_fingerprint": "`execution_fingerprint.py` writes it into the run block",
    "instance obligation IDs must match obligation_refs": "`manifest_put.py --fragment` re-binds them",
    "instance obligation_hash must bind exact obligation_refs": "`manifest_put.py --fragment` recomputes the hash",
    "S5 window input hash does not match its dispatch": "rebuild the record for THIS dispatch (`window_record.py --dispatch <ID>`)",
    "S5 window source revision is stale": "rebuild the record after the source moved",
    "window cannot omit project quality checks": "run the project's quality checks and name them in the record",
    "accept requires evidence, never an empty digest": "name the artifacts the role wrote as `evidence_refs`",
    # SC1-7 R8 (the Lead's decision 27.10): the sentence names both fields and the accept door; was "unresolved handoff needs an explicit reason"
    "given without \\\"reason\\\"": "say what is unresolved, in the accept: `reason` carries it (S1: the person's accept-gap words); the refusal prints the door",
    "baseline requires exactly one approved current-task plan row": "the plan carries one baseline row; revise the plan",
    "no accepted": "rework needs an accepted dispatch of that role on that stage; accept one first",
    "case(s) outside the approved scope": "name cases of the approved scope, or revise the scope at the gate",
    "plan row(s) not in the approved plan": "name rows of the approved plan, or revise the plan",
    "this story is closed": "reopening is the person's word: `--operation rework --reason <their words>`",
    # The two held-work ops of a closed story (B-331, C1-6a; `_held_work_refusal`): the state says no, and each refusal names the
    # held dispatches or `next`, which lists them.
    "holds no work back": "nothing: no work is held back, and `--operation next` says what the story does now",
    "is the retro (S9), which runs": "nothing: the retro needs no word on a closed story, and `--operation next` relaunches it",
    "not {NEVER_STARTED}:": "only a dispatch that never reached an agent is left; `--operation next` lists what is held (a released one asks for nothing)",
    "is not held back on this story": "name the dispatches `--operation next` lists as `held`; the message carries them",
    # `settle_order` (t-1509, GB-1a; `_settle_order_refusal`): the call's own fields first, then the state of gate B; each names the call that passes.
    "--order names the order of gate B to settle": "name an order the refusal lists (`bugs`, `mr`)",
    "--outcome is how the order ended": "`--outcome done` (an MR with its record) or `cancelled` (a person's words or a coded reason)",
    "bugs is done by the accepted qa-bug-reporter dispatch": "run the reporter (`--operation next` names it), or call the order off with `--outcome cancelled` and the person's words",
    "--ref is the MR's link or id": "`--ref <the MR link or id>`",
    "--reason-code is the delivery step's reason for the": "`--words-file <the person's words>` for `bugs` (or `release` of the reporter's dispatch); the code goes with `--order mr`",
    "Gate B decision request carries": "leave the projection's keys out; `gate-decision --gate B` builds the request with `orders` only",
    "--bugs not_ordered says no bug is to be filed": "drop `--drafts`, or record `--bugs ordered`",
    "--reason-code is the factory's own reason":"one of the reasons the refusal lists, with `--ref`",
    "--reason-code goes with --ref": "`--ref <the delivery step's one-line record>`",
    "a cancelled order is the person's call or the factory's coded reason": "`--words-file <the person's words>`, or `--reason-code` with `--ref`",
    "--ref holds an MR link or id": "a `--ref` of at most 2000 characters",
    "gate B is not decided, so it has no orders to settle": "record the decision: `gate-decision --gate B`",
    "not due, so there is nothing to settle": "`--operation next` says what the story does now",
    "the request settles an order of": "build the call again; `--operation next` names the orders of the newest decision",
    "policy requires evidence for the no-implementation decision": "name the evidence for the decision",
    "code-only receipts are allowed only for S0, S6, S7 or S8": "a stage with a role is closed by that role, not by code",
    "code-only receipt requires evidence": "name the artifact code produced",
    "Gate A applicability carry requires a new source revision": "carry it onto the new revision, not the old one",
    "Gate A applicability requires evidence of unchanged requirements": "name that evidence",
    "written progress requires content hashes": "record the hashes with the progress",
    "execution/review requires receipts": "name the receipts",
    "mutation requires intent, owned paths and before hashes": "record the intent mutation first, with its paths and hashes",
    # The problems of a `decision` request (`_decision_problems`, `_lifecycle_problems`): collected, then
    # refused whole by `_raise_all` (K1). `gate-decision` builds the whole request by code, so a receipt that
    # was not typed by hand has none of these; the rest name the work whose state says no.
    "decision references stale source revision": "`gate-decision` builds the request from the current source revision",
    "gate decision must bind the exact approved scope": "`gate-decision` builds the request with the approved scope",
    "gate decision must bind the current reviewed input": "`gate-decision` builds the request with the current reviewed input revision",
    "gate before prerequisite completion": "close the prerequisite stage; if its last role was accepted, `--operation recover` closes it from its own receipts",
    "Gate A must bind current source inventory hash": "`gate-decision` copies the current source inventory hash",
    "managed Gate A cannot approve a nonempty scope with an": "the strategist writes the plan rows (`plan_row.py --add-row`); the gate is decided after",
    "structured test plan invalid": "the strategist repairs the rows `planning_contract.py` names; `gate-decision` rehearses the gate again",
    "Gate A receipt must bind exact current structured plan": "`gate-decision` copies `--operation gate-inputs` unchanged",
    "Gate A receipt must bind server-derived semantic plan hash": "`gate-decision` copies `--operation gate-inputs` unchanged",
    "Gate A receipt must bind exact requirement oracle content hashes": "`gate-decision` copies `--operation gate-inputs` unchanged",
    "Gate A receipt must bind exact coverage-contract revisions": "`gate-decision` copies `--operation gate-inputs` unchanged",
    "lifecycle actions invalid": "the strategist repairs the lifecycle actions in the plan (`case_lifecycle.py` names each one)",
    "managed Gate A requires nonempty pinned case versions": "the case designer pins the versions of the approved cases at S4, then the gate is decided",
    "Gate A receipt must bind exact lifecycle actions hash": "`gate-decision` copies `--operation gate-inputs` unchanged",
    "retirement needs approved reviewable code removal at Gate A": "the strategist adds `proposed_code_changes` to the retire action in the plan",
    "Gate A must include lifecycle actions or explicit": "`gate-decision` includes the plan's lifecycle actions",
    "each lifecycle decision must bind action, source": "`gate-decision` builds each lifecycle decision with its action, revision and hash",
    # RH1-6 (the owner's F-2): a gate A approval over open `person_decides` items; the refusal names each item and its door
    "approve as is: the word for": "`gate-decision --as-is` again (a waiver already written is replaced, so a retry is harmless), or the person's word with `waiver.py`",
    # PC-6 (t-2181, the story held for code: `_hold_op_refusal`, `_hold_dispatch_refusal`, the hold part of `build_rework_request`): the state says no,
    # and each sentence carries the doors of `_hold_doors` (the code arriving, the person's stop, a rework of an earlier stage with their words).
    "this story is held for code (": "the doors the message prints: the code arrives (`--operation arrive`), the person stops the wait (`--operation stop_waiting`), or an earlier stage is reworked with their words",
    "this story was stopped while it waited for code: a rework of": "`controller.py --operation rework --stage <earlier stage> --role <role> --words-file <file>` with the person's own words (a typed `--reason` is refused)",
    "this story was stopped while it waited, and a bare `await`": "the code arrives (`--operation arrive`), or the person's words reopen an earlier stage (`--operation rework --words-file`); the message names both",
    "nothing is held for code, so there is no wait to stop": "nothing: no wait is held, and `--operation next` says what the story does now",
    "the wait was stopped already": "the code arrives (`--operation arrive`), or the person's words reopen an earlier stage (`--operation rework --words-file`); the message names both",
    "the wait was stopped: `first_look_continue`": "the code arrives (`--operation arrive`), or the person's words reopen an earlier stage (`--operation rework --words-file`); the message names both",
    "this story is held for {hold": "the code arriving or the person's stop (`--operation stop_waiting --words-file`): the only word that lifts a hold for code is the person's `not ours` about an absent side, carried out by the driver (`arrive` naming that side); the message names the doors",
    "`await_reopened` reopens a STOPPED story": "nothing: the story is not stopped; `--operation next` says what it does now",
    "a stopped story is reopened only by the rework": "`--operation rework` of an accepted dispatch below the held stage with the person's words, or the code arriving (`--operation arrive`)",
    "this story was stopped while it waited for code: no dispatch starts": "`--operation rework --words-file <file>` of an earlier stage, or the code arriving (`--operation arrive`)",
    "approve as is: still open after recording": "the refusal names the items still open; `waiver.py --stage <S> --block <the item's block>` records the person's word on each",
}

UNPASSABLE = {
    "controller mutation rejected: stale or missing orchestrator lease":
        "the lease is what makes this record one story's. A word cannot make a stale writer current, and two writers would interleave the log",
    "initialize once with explicit scope":
        "a second initialize would start a second story inside the same record, and nothing could tell the two apart afterwards",
    "mutation ownership and original content are immutable":
        "the record of who wrote what IS the evidence; a word that changed it would erase the thing it is evidence of",
    "structured test plan is unreadable":
        "nothing can be decided about a document that cannot be parsed - not by a person either. The file is repaired first, and then the decision is real",
    "structured test plan rows must be a list":
        "the same: a shape nothing can read carries no decision, so passing it would only move the failure further down",
    "checkpoint is not acceptance":
        "acceptance and a checkpoint are different facts about the same work, and calling one the other loses the difference the next session needs",
    "checkpoint requires remaining work and reason":
        "a checkpoint with neither says nothing at all, and the next session reads it as the only record of what is left",
    "missing environment job identity":
        "a job record without its identity cannot be observed or settled, and a word cannot give it one; the file is repaired",
    "environment job path does not match its identity":
        "the same: the record and its name disagree, so nothing can say which job it is",
    "unknown coverage migration target":
        "a migration to a version this build does not know would write a record nothing can read back",
}

CALLER_FUNCTIONS = {"build_gate_decision", "build_rework_request", "_decision_problems",
                    "build_checkpoint_request", "prepare", "gate_inputs", "_import_legacy_pipeline",
                    "main", "release_dispatch", "_cli_story_root", "manual_blocks"}
CALLER_SHAPES = ("must be one of", "must be an", "must be a ", "requires ", "required", "invalid ",
                 "needs ", "must be 0..100", "incomplete", "must name a nonempty", "mode must be",
                 "unsupported", "must carry", "must map", "names the dispatch", "records the person's own words",
                 "is not installed", "unknown ", "contains unsupported", "is the host's own id",
                 # the scope names something that is no pinned case (R1) or the story's own key (R2): the call's fault (CX1-11)
                 "scope member(s) that are not pinned case ids", "scope holds case ids",
                 # `reopen_story` / `leave_unlaunched` called with no dispatch id (C1-6a): the call's own field
                 "names the held dispatches",
                 # PC-6 hold ops: the call's own fields (`await`, `first_look_continue`, a dispatch carrying `await_reopened`)
                 "`cause` and `held_from` go together", "--source-head is the text", "--register-hash must be 64 hex",
                 "`await_reopened` is the person's word reopening")


def classify(cls, fn, head, seg, line, by_line):
    if seg in by_line:
        return by_line[seg]
    if any(head.startswith(p) for p in PERSON_HEADS):
        return "person", "reads `stage_overrides[]` through `_passed_by_person`"
    if "blocking[0]" in seg or "join(blocking)" in seg.replace(" ", ""):
        return "person", "raised from the list `_passed_by_person` has already filtered"
    for key, why in UNPASSABLE.items():
        if head.startswith(key) or key in head:
            return "unpassable", why
    for key, door in COMMAND.items():
        if head.startswith(key) or key in head:
            return "command", door
    if cls == "ValueError" and (fn in CALLER_FUNCTIONS or any(s in head for s in CALLER_SHAPES)):
        return "caller", "the request is malformed: whoever built the call fixes it, and no person is involved"
    return "?", ""


BY_SEGMENT = {
    # RH1-6: the open items of gate A (`open_gate_items`), refused beside the shared rules on the raw `decision` road. Each sentence
    # names its item and what the person words; `gate-decision` shows the same list with the recording door of each.
    "(StateConflict, item_sentence)": ("command", "the person words each open item (a door line, or a block `waiver.py` records), or answers the closed word `approve as is`; "
                                         "`gate-decision` lists the items with their doors"),
    # These raises carry no literal of their own: the message is a variable built above them.
    # A reference that does not resolve: the message is the sentence `contract.evidence_ref_issue` returns, collected one
    # item per failing reference and refused whole by `_raise_all` (C3-11, C4-4).
    "(ValueError, issue)": ("caller", "a reference in the request that does not resolve - the path is not there, or its sha does not match; fix the call"),
    # ONE site: `reconcile_dispatch` (the successor's STORED evidence). The call is well formed and no command rewrites a recorded
    # receipt, so the story's fault has the person's door through the conductor's closed question (P22) - never a dead end (FR-57).
    # `request_cancel`'s references are request fields (`(ValueError, issue)` above, since C4-10): a second site with this segment
    # would need its own key.
    "(StateConflict, issue)": ("command", "dispatch a successor with the same scope and inputs, accept it, reconcile against it (the stored successor's evidence no longer resolves: its file is gone or its sha changed, and a recorded receipt is replaced by a new successor, never rewritten)"),
    'raise StateConflict("; ".join(guard))': ("person", "`stage_guard.dispatch_errors` passes its messages through the person's recorded word before they arrive, and appends the waiver command"),
    # Collected pairs whose message is a variable (K1): the helper's own refusal, passed on whole.
    "(StateConflict, str(exc))": ("command", "a helper's own refusal passed on whole (`source_inputs`, the plan document, the coverage-contract revisions); the message names its command, e.g. `ticket_adapter.py collect` or the strategist writing the plan"),
    # ONE site: `_cli_story_root` passes on the refusal of `hooklib.story_root` (a key that is not one folder name, or names no
    # story folder). The call named the wrong story; no state was consulted, so it is the caller's, with the flag to pass instead.
    "(ValueError, str(exc))": ("caller", "`hooklib.story_root`'s own refusal passed on whole: the key is not one folder name, or names no existing story folder; the call names the wrong story and the message says which folder it looked in"),
    # RH1-10 (DC1-15): TWO sites (`prepare`, `validate`), one text: the automated runner half's membership sentences of
    # `_half_membership_problems`, one per cause, each with its door; an unreadable plan has the S6 person's-word block.
    # t-1455 q1: `prepare` with a derived EMPTY automated half; q3: `validate`'s empty-scope check over a plan that cannot be read
    "raise StateConflict(unreadable[0])": ("person", "the sentence of `_unreadable_plan_problems` already passed through `_passed_by_person`: a plan that cannot be read stops the empty-scope check of S6 until the person's word (`waiver.py --stage S6 --block \"S6 half membership: unreadable\"`) and of S5 until the person's word (`waiver.py --stage S5 --block \"S5 scope: unreadable\"`), or a repaired plan"),
    "raise StateConflict(self.automation_half_refusal(refused))": ("command", "the refusal lists each cause with its door: a manual block for a manual-agent case, leaving a handed case out, `--operation stage-scope` with `execution_kind: automation` for the cases the half may name; a plan that cannot be read is passed by the person's word (`waiver.py --stage S6 --block \"S6 half membership: unreadable\"`)"),
    # FB-9: `build_rework_request` forwards the sentences of `_rework_kind` and `_rework_block_problems` (with the membership check of
    # `_half_membership_problems`) whole: each says what is wrong in the call's cases and carries its own door (FR-1).
    "(ValueError, text)": ("caller", "a sentence of `_rework_kind` / `_rework_block_problems` passed on whole, or of the automated half's membership check (`_half_membership_problems`, `build_rework_request`): the cases name both halves, a case outside either half, an unknown kind, a manual block that is over 5 or not a manual-agent case, or - automated half - a manual-agent case, a case handed to the person, or a case of no half; each names its own door (a rework per half or per block of at most 5, leaving a handed case out, `--operation stage-scope`). One sentence is the exception and its door is the PERSON's word, not the caller's: a plan that cannot be read (`waiver.py --stage S6 --block \"S6 half membership: unreadable\"`)"),
    "(StateConflict, message)": ("command", "a design-review problem of one plan row; the message says which review is missing and `--operation gate-decision` builds the request with the reviews the story holds"),
    # ONE site: `_mutation_dispatch_problems`'s closure test (moved out of `validate`) (`_closed_dispatch_refusal`, C1-6a): a dispatch on a closed story with no person's word. The
    # message names both doors - `reopen_story` for work that never started, `rework` for new work - each with `--words-file`.
    "raise StateConflict(closed_refusal)": ("command", "`--operation reopen_story --dispatch <held ids> --words-file <file>` for work that never started (`next` lists it as `held`); `--operation rework --stage <Sn> --role <role> --cases <ids> --words-file <file>` for new work"),
    # ONE site: `_resume_problems` - the closure test is `_closed_dispatch_refusal`'s own text (the same doors as `raise StateConflict(closed_refusal)`).
    "(StateConflict, closed)": ("command", "`--operation reopen_story --dispatch <held ids> --words-file <file>` for work that never started; `--operation rework --stage <Sn> --role <role> --cases <ids> --words-file <file>` for new work; the retro (S9) needs no word"),
    # ONE site: `build_resume_request` passes a status's refusal (`_resume_status_problems`) on whole as the call's error class.
    "(ValueError, status_problem)": ("command","a status's own refusal of `resume`, passed on whole: it names the door of that status (`next`, `recover`, `rework`, `finish`)"),
    # ONE site: `validate`'s E-B11 gate (X2-5, `acceptance.stage_acceptance_refusal`): a stage with `acceptance_by` does not close without an accept record of its critic.
    "raise StateConflict(refusal)": ("command", "dispatch the stage critic (`story_step.py start --stage <Sn> --role <acceptance_by role, e.g. qa-case-critic>`) and record its verdict with `stage_done.py --task <key> --stage <Sn> --acceptance work/handoffs/<its dispatch>.yaml`; or the person's word with `waiver.py --stage <Sn> --block \"stage acceptance\"`"),
    'raise StateConflict(f"current Gate {gate} decision required")': ("command", "`gate-decision --words-file <file>` records the person's approval of that gate"),
}


def collect_rows(src: str, classes) -> list:
    """Every block of `src` - a `raise <refusal class>(...)` and a collected `(Class, message)` pair - as
    {line, fn, cls, seg, head}. `src` is the controller's text unless a test hands its own."""
    tree = ast.parse(src)
    rows = []

    class V(ast.NodeVisitor):
        def __init__(self):
            self.stack = []

        def visit_FunctionDef(self, node):
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def block(self, node, cls_name):
            seg = " ".join((ast.get_source_segment(src, node) or "").split())
            lit = LIT.search(seg)
            text = (lit.group(1) if lit else "").strip()
            # A literal that is only a joiner (`"; "`, `". "`) says nothing about the
            # block: show the call instead, and key on the same thing the test does.
            if len(text.strip(" .;,-")) < 4:
                text = seg[:70]
            rows.append({"line": node.lineno, "fn": self.stack[-1] if self.stack else "?",
                         "cls": cls_name, "seg": seg, "head": text})

        def visit_Raise(self, node):
            exc = node.exc
            if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id in classes:
                self.block(node, exc.func.id)
            self.generic_visit(node)

        def visit_ExceptHandler(self, node):
            # `except (StateConflict, ValueError):` names two classes and refuses nothing.
            for child in node.body:
                self.visit(child)

        def visit_Tuple(self, node):
            # A COLLECTED block (K1): `(StateConflict, "<message>")`, raised later with its
            # siblings by `_raise_all` - the same key as a `raise`, the same walk (the test
            # `test_controller_blocks.py` reads it identically).
            first, second = (node.elts + [None, None])[:2]
            if (len(node.elts) == 2 and isinstance(first, ast.Name) and first.id in classes
                    and not (isinstance(second, ast.Name) and second.id in classes)):
                self.block(node, first.id)
            self.generic_visit(node)

    V().visit(tree)
    return rows


def route_rows(rows) -> list:
    """Gives every row its `route` and `note`; returns the rows no table can place (route `?`)."""
    unknown = []
    for row in rows:
        route, note = classify(row["cls"], row["fn"], row["head"], row["seg"], row["line"], BY_SEGMENT)
        row["route"], row["note"] = route, note
        if route == "?":
            unknown.append(row)
    return unknown


def main() -> int:
    streams.utf8_stdio()
    rows = collect_rows(SRC.read_text(encoding="utf-8"), refusal_classes())
    unknown = route_rows(rows)
    for row in unknown:
        print(f"UNCLASSIFIED {row['line']:5} {row['cls']:14} {row['fn']:28} {row['head'][:80]}", file=sys.stderr)
    if unknown:
        # A row with no route is the defect this file exists to prevent: refuse, write nothing.
        print(f"FAILED: {len(unknown)} refusal(s) in {SRC} have no route (first: line {unknown[0]['line']}, "
              f"`{unknown[0]['fn']}`). Add the message to COMMAND, UNPASSABLE or BY_SEGMENT, or fix the "
              "raise so the caller shape is recognised.", file=sys.stderr)
        return 1
    counts = {}
    for row in rows:
        counts[row["route"]] = counts.get(row["route"], 0) + 1
    print(f"{len(rows)} blocks: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if len(sys.argv) > 1:
        pathlib.Path(sys.argv[1]).write_text(render(rows, counts), encoding="utf-8", newline="\n")   # LF on every platform: the committed file is LF
        print("written:", sys.argv[1])
    return 0


def render(rows, counts) -> str:
    head = f"""# Every block in the controller, and the route through it

`controller.py` refuses **{len(rows)}** times: {counts.get('caller', 0) + counts.get('command', 0) + counts.get('person', 0) + counts.get('unpassable', 0)} raises or collected `(Class, message)` problems (a request's problems are gathered and refused whole by `_raise_all`), as {', '.join('`' + name + '`' for name in sorted(refusal_classes()))} - two kinds that do not
mean the same thing. `StateConflict` says the request is fine and the story's recorded state is not
ready for it (`DerivedViewStale`, a subclass of it, says the event IS committed and only what
follows it failed); `ValueError` says the request itself is malformed and the story was never consulted. The
factory's oldest rule - a check stops a SILENT pass, never an informed one - applies to the
first kind, and this file is the walk that gives every block of both kinds a route (PLAN P21.4,
rules FR-4 and FR-5).

It exists because the rule had been kept per-check: S5's completion demanded a window
acceptance record with no way for a person's word to pass it, and that cost three answers and a
halt in TP1-13797 run 5. The walk found two more of exactly that shape - S1's sources and
S3's plan rows, five conductor sessions and $1.94 on the second - and it also found why: that
gate raised `ValueError`, the class for a malformed request, for a block about the story's own
evidence.

| route | blocks | what it means |
|---|---|---|
| `person` | {counts.get('person', 0)} | their recorded words pass it: `waiver.py --stage <S> --block "<part of the line>" --words-file <file>` |
| `command` | {counts.get('command', 0)} | a factory command clears it. The person decides, the command records; the message names it |
| `caller` | {counts.get('caller', 0)} | the call was built wrong. Whoever built it fixes it, and no person is involved |
| `unpassable` | {counts.get('unpassable', 0)} | no word passes it, and the reason is here. These are invariants of the record itself: passing one would destroy what the block protects |

The table was built by a classifier that lives with the plans, outside the package
(`tools/controller-blocks-gen.py` in the factory development repository): it reads every raise out of the controller and names
the ones it cannot place and writes nothing while one has no route, so a walk after the next controller change starts from what changed
rather than from scratch. The file is edited by hand as easily - the test below is what makes
either way safe.

`scripts/tests/test_controller_blocks.py` holds this file to the source: a block with no row
fails the build, a row with no block fails, and an `unpassable` row without its reason fails.
Add the row in the same change as the block - naming the route is part of writing the refusal
(FR-1, FR-2). The key is the function and the message, never a line number: a line moves with
every edit above it. Rows are in source order.

| where | class | block | route | the way through |
|---|---|---|---|---|
"""
    body = []
    for row in sorted(rows, key=lambda r: r["line"]):
        if row["route"] not in ("person", "command", "caller", "unpassable") or not row["note"].strip():
            raise SystemExit(f"line {row['line']} (`{row['fn']}`) has an empty route or way through; refusing to render")
        text = (row["head"] or row["seg"][:60]).replace("|", "\\|").strip()
        body.append(f"| `{row['fn']}` | `{row['cls']}` | {text[:110]} | `{row['route']}` | {row['note']} |")
    return head + "\n".join(body) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
