"""Fail-closed checker for critic verdict JSON blocks -- part of this
toolkit's critic acceptance-gate tooling (the role-vs-tier acceptance
matrix's critic entry: a machine-checkable shape for a critic's
final-message verdict, so "fit / fit_with_fixes / blocker" plus its
required trail are enforced by code, not by convention alone).

Extracts the LAST fenced ```json ... ``` block from a critic's final-
message text and validates it against a hardcoded expected shape
(required/enum AND cross-field rules -- NOT a generic JSON-Schema
validator by design, for a small, stable, fully-enumerable shape).

Usage:
    python tools/critic_verdict_check.py <path-to-verdict-text>
    python tools/critic_verdict_check.py -        (reads stdin)

Exit codes:
    0  valid verdict -> stdout: "VERDICT OK: <verdict>, blockers: N, fixes: M"
    1  no block / broken JSON / not an object / schema violation -> stderr:
       ASCII diagnostic lines, one per violation, each naming the concrete
       field/rule that failed.

All diagnostic text and the success line are ASCII-only by construction:
diagnostics never interpolate raw field VALUES from the (possibly
non-ASCII) input, only field names, indices and fixed expected-shape text.

Two sharp edges of the fence-extraction regex, both intentional trade-offs
of the "no generic parser" design:
  - The fence opener is matched case-sensitively as a literal lowercase
    ```json. ```JSON, ```Json or a bare ``` opener are NOT recognized as
    a verdict block.
  - The block body is matched non-greedily up to the first ``` that
    follows the opener. A verdict field VALUE that itself contains a
    literal ``` sequence truncates the captured body there: the JSON
    typically fails to parse (or parses into something that no longer
    satisfies the schema), so an otherwise-valid verdict is rejected
    fail-closed rather than silently misread.
"""

import json
import os
import re
import sys
import threading
from pathlib import Path

VERDICT_ENUM = ("fit", "fit_with_fixes", "blocker")

_FENCE_RE = re.compile(r"```json[ \t]*\r?\n(.*?)```", re.DOTALL)


def extract_last_json_block(text):
    """Return the text of the LAST closed ```json ... ``` fence, or None."""
    matches = list(_FENCE_RE.finditer(text))
    if not matches:
        return None
    return matches[-1].group(1)


def _is_str_list(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


# --- mutants (test rules S-D): a critic's mutation probes, shape and joins
# only. Error direction: may FALSE-PASS a fabricated kill (the transcript
# count of check 50 (b) is the guard for that), must NEVER false-refuse.
# The cap 3 is data here; its rule is .claude/agents/critic.md rule 21.
MUTANT_CAP = 3
_MUTANT_OUTCOMES = ("killed", "survived", "invalid", "restore-mismatch")
_MUTANT_LIMITS = {"place": 300, "change": 300, "run": 500}
_KILLED_BY_MAX = 300
_FLAG_RE = re.compile(r"--(test|target)\s+(?:\"([^\"]*)\"|'([^']*)'|(\S+))")
_WORD_RE = re.compile(r"\w")
_PREDATES = (
    "missing required field: mutants (a verdict written before this field "
    "existed is accepted only with the reason \"verdict predates a required "
    "field (mutants)\" where its acceptance is recorded: "
    ".claude/agents/critic.md rule 17)"
)


def _flag_values(run, flag):
    values = []
    for m in _FLAG_RE.finditer(run):
        if m.group(1) == flag:
            values.append(next(g for g in m.groups()[1:] if g is not None))
    return values


def _first_word(entry):
    parts = entry.split()
    return parts[0].rstrip(":") if parts else ""


def _resolve_remark(remark, entries):
    """Entries of blockers + fixes whose first word is the remark's."""
    key = remark.strip().rstrip(":")
    if not key:
        return []
    return [e for e in entries if _first_word(e) == key]


def _one_mutant(i, m, obj, entries, reruns, seen_runs, tests):
    """Errors of mutants[i]; appends its --test values to tests (S-D-2 split)."""
    errors = []
    tag = "mutant %d" % i
    if not isinstance(m, dict):
        errors.append("field 'mutants[%d]' must be an object" % i)
        return errors
    bad = False
    for name, cap in _MUTANT_LIMITS.items():
        v = m.get(name)
        if not isinstance(v, str) or not (1 <= len(v) <= cap):
            errors.append(
                "%s: field '%s' must be a string of 1-%d characters" % (tag, name, cap)
            )
            bad = True
    outcome = m.get("outcome")
    if outcome not in _MUTANT_OUTCOMES:
        errors.append(
            "%s: field 'outcome' invalid: expected one of killed, survived, "
            "invalid, restore-mismatch" % tag
        )
        bad = True
    kb = m.get("killed_by")
    if outcome == "killed":
        if not isinstance(kb, str) or not (1 <= len(kb) <= _KILLED_BY_MAX):
            errors.append(
                "%s: outcome killed needs 'killed_by', a string of 1-300 characters" % tag
            )
    elif kb is not None:
        errors.append("%s: 'killed_by' must be absent or null unless outcome is killed" % tag)
    if bad:
        return errors

    run = m["run"]
    if run in seen_runs:
        errors.append("%s: run repeats another mutant's run" % tag)
    seen_runs.add(run)
    if "mutate_once.py" not in run:
        errors.append("%s: run does not contain mutate_once.py" % tag)
    joined = [r for r in reruns if r["command"] == run]
    if not joined:
        errors.append("%s: run equals no trail.reruns command" % tag)
    elif not any(("outcome: %s" % outcome) in r["result"] for r in joined):
        errors.append(
            "%s: the joined rerun result lacks 'outcome: %s'" % (tag, outcome)
        )
    tvals = _flag_values(run, "test")
    if not tvals:
        errors.append("%s: run names no --test" % tag)
    tests.extend(tvals)

    if outcome == "survived":
        errors.extend(_survivor_errors(m, tag, entries))
    elif outcome == "restore-mismatch":
        errors.extend(_restore_errors(m, tag, run, obj, entries))
    return errors


def _survivor_errors(m, tag, entries):
    errors = []
    eq = m.get("equivalent")
    rk = m.get("remark")
    has_eq = isinstance(eq, str) and bool(_WORD_RE.search(eq))
    has_rk = isinstance(rk, str) and bool(rk.strip())
    if has_eq == has_rk:
        errors.append(
            "%s: outcome survived needs exactly one of 'equivalent' or 'remark'" % tag
        )
    elif has_rk:
        hits = _resolve_remark(rk, entries)
        if not hits:
            errors.append(
                "%s: remark names no blockers or fixes entry (its first word)" % tag
            )
        elif len(hits) > 1:
            errors.append("%s: remark names 2 or more entries" % tag)
    return errors


def _restore_errors(m, tag, run, obj, entries):
    errors = []
    rk = m.get("remark")
    hits = _resolve_remark(rk, entries) if isinstance(rk, str) else []
    targets = _flag_values(run, "target")
    ok = (
        obj.get("verdict") != "fit"
        and len(hits) == 1
        and "show HEAD:" in hits[0]
        and any(t and t in hits[0] for t in targets)
    )
    if not ok:
        errors.append(
            "%s: outcome restore-mismatch needs a verdict other than fit and "
            "a fix entry, named by remark, stating the target and the restore "
            "door \"git -C <tree> show HEAD:<path> > <tree>/<path>\" "
            "(.claude/agents/critic.md rule 21)" % tag
        )
    return errors


def _mutant_errors(obj):
    errors = []
    if "mutants" not in obj:
        return [_PREDATES]
    mutants = obj.get("mutants")
    if not isinstance(mutants, list):
        return ["field 'mutants' must be an array"]
    none = obj.get("mutants_none")
    if not mutants:
        if not (isinstance(none, str) and _WORD_RE.search(none)):
            errors.append(
                "field 'mutants' is empty: 'mutants_none' with a reason is required"
            )
        return errors
    if none is not None:
        errors.append("field 'mutants_none' must be absent when 'mutants' is non-empty")
    if len(mutants) > MUTANT_CAP:
        errors.append(
            "field 'mutants' has %d items: at most %d (the cap of "
            ".claude/agents/critic.md rule 21)" % (len(mutants), MUTANT_CAP)
        )

    entries = []
    for key in ("blockers", "fixes"):
        val = obj.get(key)
        if isinstance(val, list):
            entries.extend(e for e in val if isinstance(e, str))
    reruns = []
    trail = obj.get("trail")
    if isinstance(trail, dict) and isinstance(trail.get("reruns"), list):
        reruns = [
            r for r in trail["reruns"]
            if isinstance(r, dict)
            and isinstance(r.get("command"), str)
            and isinstance(r.get("result"), str)
        ]

    seen_runs = set()
    tests = []
    for i, m in enumerate(mutants):
        errors.extend(_one_mutant(i, m, obj, entries, reruns, seen_runs, tests))
    for t in dict.fromkeys(tests):
        if not any(
            "mutate_once.py" not in r["command"] and t in r["command"] for r in reruns
        ):
            errors.append(
                "green control missing: no rerun without mutate_once.py names the --test value of a mutant"
            )
            break
    return errors


def validate_verdict(obj):
    """Return a list of ASCII violation strings; empty list means valid."""
    errors = []

    if not isinstance(obj, dict):
        errors.append(
            "JSON root is not an object (type: %s)" % type(obj).__name__
        )
        return errors

    required_top = ("verdict", "blockers", "class_completeness", "trail")
    for field in required_top:
        if field not in obj:
            errors.append("missing required field: %s" % field)

    # verdict
    verdict = obj.get("verdict")
    verdict_valid = False
    if "verdict" in obj:
        if not isinstance(verdict, str) or verdict not in VERDICT_ENUM:
            errors.append(
                "field 'verdict' invalid: expected one of fit, fit_with_fixes, blocker"
            )
        else:
            verdict_valid = True

    # blockers
    blockers = obj.get("blockers")
    blockers_valid = False
    if "blockers" in obj:
        if not _is_str_list(blockers):
            errors.append("field 'blockers' must be an array of strings")
        else:
            blockers_valid = True

    if verdict_valid and blockers_valid:
        if verdict == "fit" and len(blockers) != 0:
            errors.append(
                "field 'blockers' must be empty when verdict is fit"
            )
        if verdict == "blocker" and len(blockers) == 0:
            errors.append(
                "field 'blockers' must be non-empty when verdict is blocker"
            )

    # class_completeness
    if "class_completeness" in obj:
        if not isinstance(obj.get("class_completeness"), str):
            errors.append("field 'class_completeness' must be a string")

    # trail
    if "trail" in obj:
        trail = obj.get("trail")
        if not isinstance(trail, dict):
            errors.append("field 'trail' must be an object")
        else:
            if "read" not in trail:
                errors.append("missing required field: trail.read")
            elif not _is_str_list(trail.get("read")):
                errors.append("field 'trail.read' must be an array of strings")

            if "reruns" not in trail:
                errors.append("missing required field: trail.reruns")
            else:
                reruns = trail.get("reruns")
                if not isinstance(reruns, list):
                    errors.append("field 'trail.reruns' must be an array")
                else:
                    for idx, item in enumerate(reruns):
                        if not isinstance(item, dict):
                            errors.append(
                                "field 'trail.reruns[%d]' must be an object" % idx
                            )
                            continue
                        if "command" not in item or not isinstance(
                            item.get("command"), str
                        ):
                            errors.append(
                                "field 'trail.reruns[%d]' missing required string field: command"
                                % idx
                            )
                        if "result" not in item or not isinstance(
                            item.get("result"), str
                        ):
                            errors.append(
                                "field 'trail.reruns[%d]' missing required string field: result"
                                % idx
                            )

    # fixes (conditionally required)
    if verdict_valid and verdict == "fit_with_fixes":
        fixes = obj.get("fixes")
        if "fixes" not in obj:
            errors.append(
                "missing required field: fixes (required when verdict is fit_with_fixes)"
            )
        elif not _is_str_list(fixes):
            errors.append("field 'fixes' must be an array of strings")
        elif len(fixes) == 0:
            errors.append(
                "field 'fixes' must be non-empty when verdict is fit_with_fixes"
            )
    elif "fixes" in obj and obj.get("fixes") is not None:
        if not _is_str_list(obj.get("fixes")):
            errors.append("field 'fixes' must be an array of strings")

    errors.extend(_mutant_errors(obj))
    return errors


def check_text(text):
    """Run the full pipeline on raw text. Returns (ok, errors, obj_or_None)."""
    block = extract_last_json_block(text)
    if block is None:
        return False, ["no fenced ```json block found in input"], None

    try:
        obj = json.loads(block)
    except json.JSONDecodeError as exc:
        return False, ["invalid JSON in fenced block: %s" % str(exc)], None

    errors = validate_verdict(obj)
    if errors:
        return False, errors, obj
    return True, [], obj


# --- BEGIN stdin-deadline helper (a local copy -- a shared module across
# hooks/tools is deliberately not introduced, the same self-containment
# principle this toolkit's other scripts already apply) ---------------
_STDIN_DEADLINE_DEFAULT = 10.0
_STDIN_DEADLINE_MAX = 600.0
_STDIN_DEADLINE_ENV = "OSLLM_STDIN_TIMEOUT"


def _stdin_deadline_seconds():
    """Deadline seconds: env override, else the default. Invalid,
    non-numeric, <=0, or > _STDIN_DEADLINE_MAX -> the default; there is
    NO "0 = wait forever" mode on purpose (that would resurrect the very
    hang this helper closes)."""
    try:
        value = float(os.environ.get(_STDIN_DEADLINE_ENV, ""))
    except (TypeError, ValueError):
        return _STDIN_DEADLINE_DEFAULT
    if not (0.0 < value <= _STDIN_DEADLINE_MAX):
        return _STDIN_DEADLINE_DEFAULT
    return value


def _read_stdin_bytes_deadline():
    """(bytes, timed_out). Reads stdin to EOF, but no longer than the
    deadline. A cross-platform form: select/poll doesn't work on pipes on
    Windows, so a daemon reader thread does the actual read, and the
    deadline is held by join(timeout). A TTY -> b"" without reading (the
    same guard this toolkit's other stdin-reading scripts already carry).
    Any read error -> b"" (fail-open, the same principle as elsewhere in
    this toolkit)."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return b"", False
    try:
        if stdin.isatty():
            return b"", False
    except Exception:
        pass
    stream = getattr(stdin, "buffer", stdin)
    box = {}

    def _reader():
        try:
            box["data"] = stream.read()
        except Exception:
            box["data"] = b""

    thread = threading.Thread(target=_reader, name="stdin-deadline", daemon=True)
    thread.start()
    thread.join(_stdin_deadline_seconds())
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8", "replace")
    return data, False


_STDIN_DEADLINE_MSG = "stdin deadline exceeded -- fail-open, payload discarded"
# --- END stdin-deadline helper ---

# A background reader thread left blocked on the REAL stdin buffer at
# ordinary interpreter shutdown can crash the process with "Fatal Python
# error: _enter_buffered_busy" instead of a clean exit -- the same class
# this toolkit's other stdin-reading hooks/scripts already guard against.
# main() itself is unchanged (still a plain `return <rc>`, safe
# in-process); only the actual __main__ script-exit path below escalates
# to os._exit() on a timeout.
_STDIN_DEADLINE_STATE = {"hit": False}


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: critic_verdict_check.py <path-or-->\n")
        return 1

    source = argv[1]
    if source == "-":
        raw_bytes, timed_out = _read_stdin_bytes_deadline()
        if timed_out:
            _STDIN_DEADLINE_STATE["hit"] = True
            sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
            return 1  # the same failure class as an empty/invalid input
        try:
            text = raw_bytes.decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            sys.stderr.write("INVALID VERDICT: input is not valid UTF-8\n")
            return 1
    else:
        try:
            with open(source, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            sys.stderr.write("cannot read input file: %s\n" % str(exc))
            return 1
        except (UnicodeDecodeError, ValueError):
            sys.stderr.write("INVALID VERDICT: input is not valid UTF-8\n")
            return 1

    ok, errors, obj = check_text(text)
    if not ok:
        sys.stderr.write("INVALID VERDICT:\n")
        for err in errors:
            sys.stderr.write("  - %s\n" % err)
        return 1

    blockers = obj.get("blockers") or []
    fixes = obj.get("fixes") or []
    sys.stdout.write(
        "VERDICT OK: %s, blockers: %d, fixes: %d\n"
        % (obj.get("verdict"), len(blockers), len(fixes))
    )
    return 0


if __name__ == "__main__":
    _rc = main(sys.argv)
    if _STDIN_DEADLINE_STATE["hit"]:
        try:
            sys.stdout.flush()
        except Exception:
            pass
        try:
            sys.stderr.flush()
        except Exception:
            pass
        os._exit(_rc)
    sys.exit(_rc)
