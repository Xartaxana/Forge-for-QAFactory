"""refusal_registry.py — A24: the registry matches the shipped sources, and every entry is
either passable by a person's word or says why it is not.

The audit is worth only as much as its scanner, so this file checks the scanner on synthetic
sources (a refusal nobody registered is caught; a registered refusal that was deleted is
caught) and then runs it against the real package, which is the regression that matters: a
refusal added to a hook without an entry fails here before it fails a live story.
"""
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, SCRIPTS, check, check_eq, check_in, cleanup, finish, \
    run_script, temp_dir  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import refusal_registry as RR  # noqa: E402


def _fake_package(body: str) -> Path:
    """A throwaway <root>/scripts/stage_guard.py the scanner can be pointed at."""
    root = temp_dir("qa-factory-refusals-")
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "stage_guard.py").write_text(textwrap.dedent(body), encoding="utf-8")
    return root


def part_scanner() -> None:
    root = _fake_package("""
        def deny(message):
            return 2

        def check_dispatch(event):
            if event:
                return deny("a brand new refusal nobody wrote down")
            raise ValueError("a raised one too")
    """)
    try:
        found = RR.sites(root)
        check_eq("the scanner sees both shapes of refusal", len(found), 2)
        check_eq("keyed by the function that refuses",
                 sorted({s["function"] for s in found}), ["check_dispatch"])
        check_in("and by the text of the refusal, without its quotes",
                 "a brand new refusal nobody wrote down", [s["call"] for s in found])
        check("a refusal with no entry is a finding",
              any("is not in refusal_registry.REGISTRY" in e for e in RR.findings(root)))
    finally:
        cleanup(root)

    # A registered refusal that has since been deleted is the other half: an entry pointing
    # at nothing tells a reader the factory still stops there when it no longer does.
    root = _fake_package("""
        def deny(message):
            return 2

        def check_dispatch(event):
            return 0
    """)
    try:
        stale = [e for e in RR.findings(root) if "the entry is stale" in e]
        check("a registered refusal that is gone is a finding", bool(stale),
              "nothing reported stale")
    finally:
        cleanup(root)

    # OH5-2 A (F2): a refusal source naming the host root variable is a finding, in any spelling (E13, E15); the
    # concatenation split is the named, accepted miss (E14). One variant row per spelling.
    for row, literal, flagged in (
            ("braced", "${CLAUDE_PLUGIN_ROOT}/scripts/x.py", True),
            ("bare", "$CLAUDE_PLUGIN_ROOT/scripts/x.py", True),
            ("cmd", "%CLAUDE_PLUGIN_ROOT%/scripts/x.py", True),
            ("powershell", "$env:CLAUDE_PLUGIN_ROOT/scripts/x.py", True),
            ("lowercase", "${claude_plugin_root}/scripts/x.py", True),
            ("split by concatenation (accepted miss)", "CLAUDE_PLUGIN_\" + \"ROOT/x.py", False),
            ("no variable", "scripts/x.py", False)):
        root = _fake_package(f'''
            def deny(message):
                return 2

            def check_dispatch(event):
                return deny("{literal}")
        ''')
        try:
            hit = [e for e in RR.findings(root) if "unexpanded host root variable" in e]
            check(f"a refusal source with `{row}` literal: flagged={flagged}", bool(hit) == flagged, str(hit))
            if flagged:
                check_in(f"{row}: the finding names file and line", "stage_guard.py:", hit[0])
        finally:
            cleanup(root)


def part_door_texts() -> None:
    """OH5-2 A (AR-8, FR-15): the doors the guard builds name existing scripts of the copy that runs it (E4, E10); the card head
    and the brief's SCRIPTS are spelled by the same survivor."""
    import json
    import re
    import guard_pre_tool as G
    import runtime_paths as RP

    class WF:
        @staticmethod
        def cases_of(owner):
            return "the window"

    root_posix = RP.package_root().as_posix()
    texts = {"_window_refusal": G._window_refusal(WF, "C:/tmp/story/task", "tests/a.py", "S5|x", 1)}
    project = temp_dir("qa-factory-doors-")
    try:
        plan = project / "qa-factory" / "artifacts" / "T-1" / "work" / "test-plan.json"
        plan.parent.mkdir(parents=True)
        plan.write_text(json.dumps([{"id": "TS-1"}]), encoding="utf-8")
        event = {"tool_name": "Write", "tool_input": {"file_path": plan.as_posix()}}
        texts["plan_write_check"] = G._blocked(G.plan_write_check, event, {}) or ""
        for name, text in texts.items():
            check(f"the {name} refusal was built", "PRE-TOOL GUARD" in text, text[:200])
            found = [a or b for a, b in re.findall(r"python (?:\"([^\"]+)\"|'([^']+)')", text)]
            check(f"{name} names at least one script door", bool(found), text[:300])
            for path in found:
                check(f"{name}: {Path(path).name} exists", Path(path).is_file(), path)
                check(f"{name}: {Path(path).name} is under this copy's scripts", path.startswith(root_posix + "/scripts/"), path)
        # E4 pinned: the script is missing from the copy -> the gap text, then the site's own argument tail
        bare = project / "bare-copy"
        (bare / "scripts").mkdir(parents=True)
        saved = RP.package_root
        RP.package_root = lambda: bare
        try:
            gap = G._blocked(G.plan_write_check, event, {}) or ""
        finally:
            RP.package_root = saved
        check_in("E4: the missing script is named with the gap and qa-doctor",
                 f"`plan_row.py` (missing from the plugin copy at {bare.as_posix()}; the conductor runs qa-doctor to repair "
                 "the installation) --task <TICKET> --row <TS-n> --set <field>=<value>", gap)
        check("E4: no path of the missing script is printed", "python \"" not in gap.split("plan_row.py")[0].split("\n")[-1], gap)
    finally:
        cleanup(project)
    # F8 / N4: the brief's SCRIPTS is the survivor's folder, and both card heads are built through the survivor
    import brief_pack
    check_eq("brief_pack.SCRIPTS is the package scripts folder", brief_pack.SCRIPTS, (RP.package_root() / "scripts").as_posix())
    # the card head follows the running copy, and a `$` root gets the single-quoted form (E3c) through the card itself
    saved = RP.package_root
    RP.package_root = lambda: Path("C:/qa$root/copy")
    try:
        card = brief_pack.command_card_lines(project / "qa-factory" / "artifacts" / "T-1", "walk-1", (), "")
        want = RP.script_command("<script>", must_exist=False)
    finally:
        RP.package_root = saved
    check_eq("the card head is the survivor's single-quoted form on a `$` root", want,
             "python 'C:/qa$root/copy/scripts/<script>'")
    check_in("the card head carries that command", f"Every command is `{want}`", card[0])


def part_live_package() -> None:
    check_eq("the shipped package has no unregistered refusal", RR.findings(PLUGIN_ROOT), [])
    p = run_script("refusal_registry.py", "--check")
    check("refusal_registry.py --check is green", p.returncode == 0,
          (p.stdout + p.stderr)[-600:])
    check_in("and names the refusals a person's word cannot pass",
             "a person's word cannot pass", p.stdout)

    # Every entry earns its place: what it refuses, the proof, and either the way through or
    # the reason there is none. "A person's word passes any block" is checked here, not
    # remembered.
    for entry in RR.REGISTRY:
        eid = entry["id"]
        check(f"{eid} names what it refuses", bool(str(entry.get("refuses") or "").strip()))
        check(f"{eid} names the test that proves it", bool(str(entry.get("test") or "").strip()))
        if not str(entry.get("override") or "").strip():
            check(f"{eid} says why no word can pass it",
                  bool(str(entry.get("unpassable_because") or "").strip()))
    check_eq("every id is unique", len({e["id"] for e in RR.REGISTRY}), len(RR.REGISTRY))

    # The two rules of the dispatch path that a person CAN pass are the ones TP1-15045 was about;
    # if either loses its waiver command the registry has stopped describing the code.
    for eid in ("SG-stage-rules", "CTRL-dispatch", "SD-stage-close"):
        entry = next(e for e in RR.REGISTRY if e["id"] == eid)
        check_in(f"{eid} names waiver.py as the way through", "waiver.py", entry["override"])

    # The profile-write refusal (t-286): registered, its door is the orchestrator's launch_check, and
    # a misspelled `call` makes A24 report the live refusal as unregistered again (negative control).
    entry = next(e for e in RR.REGISTRY if e["id"] == "PT-config-write")
    check_in("PT-config-write names the orchestrator's proof as the way through",
             "launch_check.py --profile <id>", entry["override"])
    check_in("PT-config-write names what the role reports", "launch: <cause>", entry["override"])
    saved = list(RR.REGISTRY)
    try:
        RR.REGISTRY[:] = [dict(e, call="CONFIG_WRITE_MSG.formta(what=what)") if e["id"] == "PT-config-write"
                          else e for e in saved]
        check("a misspelled PT-config-write call is a finding again",
              any("guard_pre_tool.py" in e and "CONFIG_WRITE_MSG.format(what=what)" in e
                  and "is not in refusal_registry.REGISTRY" in e for e in RR.findings(PLUGIN_ROOT)))
    finally:
        RR.REGISTRY[:] = saved

    # The combined dispatch refusal (t-868, F-1): the row names the compound call, says that the S6-S8 manifest
    # reason is one more item of it, and a misspelled call is a finding again (negative control).
    entry = next(e for e in RR.REGISTRY if e["id"] == "SG-stage-rules")
    check_eq("SG-stage-rules registers the compound deny", entry["call"], "DV.compound(blocking, prefix=")
    check_in("SG-stage-rules says the S6-S8 manifest reason is an item of the same refusal", "S6-S8", entry["refuses"])
    check_in("SG-stage-rules says one reason is one sentence", "One reason is the one sentence", entry["refuses"])
    check("SG-stage-rules is a live row (a site of check_dispatch starts with its call)",
          any(s["file"] == "stage_guard.py" and s["function"] == "check_dispatch"
              and s["call"].startswith(entry["call"]) for s in RR.sites(PLUGIN_ROOT)))
    try:
        RR.REGISTRY[:] = [dict(e, call="DV.compund(blocking, prefix=") if e["id"] == "SG-stage-rules" else e
                          for e in saved]
        check("a misspelled SG-stage-rules call is a finding again",
              any("stage_guard.py" in e and "DV.compound(blocking, prefix=" in e
                  and "is not in refusal_registry.REGISTRY" in e for e in RR.findings(PLUGIN_ROOT)))
    finally:
        RR.REGISTRY[:] = saved

    # The manifest that was not read (t-910, C4-1): the row exists, covers a live site of check_dispatch, says why no word
    # passes it, names both texts and the policy-skip world; dropping the row, or its test, is a finding (negative control).
    entry = next((e for e in RR.REGISTRY if e["id"] == "SG-manifest-unread"), None)
    check("SG-manifest-unread is registered", entry is not None)
    if entry is not None:
        for word in ("is absent", "could not be read", "pipeline.json", "skipped", "zero items"):
            check_in(f"SG-manifest-unread names `{word}`", word, entry["refuses"])
        # a person's word passes it (P13, FR-57): the row names that door and does not call the refusal unpassable
        check_in("SG-manifest-unread names the waiver door", "waiver.py", entry["override"])
        check_in("SG-manifest-unread: the pass is the standard gate_override record", "gate_override", entry["override"])
        check_eq("SG-manifest-unread is not marked unpassable", entry["unpassable_because"], "")
        check_in("SG-manifest-unread names the pinning test", "part_manifest_not_read", entry["test"])
        check("SG-manifest-unread is a live row (a site of check_dispatch starts with its call)",
              any(s["file"] == "stage_guard.py" and s["function"] == "check_dispatch"
                  and s["call"].startswith(entry["call"]) for s in RR.sites(PLUGIN_ROOT)))
        try:
            RR.REGISTRY[:] = [dict(e, function="check_dispatchh") if e["id"] == "SG-manifest-unread" else e for e in saved]
            check("a stale SG-manifest-unread row is a finding again",
                  any("SG-manifest-unread" in e and "the entry is stale" in e for e in RR.findings(PLUGIN_ROOT)))
        finally:
            RR.REGISTRY[:] = saved
    pin_src = (PLUGIN_ROOT / "scripts" / "tests" / "test_stage_guard.py").read_text(encoding="utf-8")
    check_in("the test the row names exists in test_stage_guard.py", "def part_manifest_not_read", pin_src)

    named = {Path(part.strip().split()[0]).name
             for entry in RR.REGISTRY for part in str(entry["test"]).split(",")
             if part.strip().startswith("scripts/tests/")}
    missing = sorted(n for n in named if not (PLUGIN_ROOT / "scripts" / "tests" / n).is_file())
    check("every test a registry entry names exists", not missing, f"missing: {missing}")


def part_fail_closed() -> None:
    """a refusal closed to a person's word BECAUSE a check did not run must say how it
    stops repeating itself. Without that, a defect inside the guard freezes the story where
    the person's word cannot reach it either: the same dead end, one level down."""
    closed = RR.escalations()
    check_eq("the two fail-closed refusals are the ones the plan named",
             sorted(e["id"] for e in closed), ["PT-patch-unchecked", "PT-unparsed-event"])
    for entry in closed:
        check_eq(f"{entry['id']} escalates after two in a row", entry.get("escalates_after"), 2)
        check_in(f"{entry['id']} names the factory as the owner of the diagnosis",
                 "factory", entry.get("escalation") or entry.get("unpassable_because") or "")

    # And the audit says so: an entry that is fail-closed with neither a pass nor an
    # escalation is a finding, not a silence.
    saved = list(RR.REGISTRY)
    try:
        RR.REGISTRY[:] = [dict(e, escalates_after=0, escalation="") if e["id"] == "PT-unparsed-event"
                          else e for e in saved]
        check("a fail-closed refusal with no escalation is a finding",
              any("escalates_after" in e for e in RR.findings(PLUGIN_ROOT)))
        RR.REGISTRY[:] = [dict(e, escalation="") if e["id"] == "PT-unparsed-event" else e
                          for e in saved]
        check("and `escalates_after` with nothing behind it is a finding too",
              any("no `escalation`" in e for e in RR.findings(PLUGIN_ROOT)))
    finally:
        RR.REGISTRY[:] = saved
    check_eq("the real registry is clean again", RR.findings(PLUGIN_ROOT), [])

    # a `next` answer that does not let the story move is a refusal like any other.
    entry = next(e for e in RR.REGISTRY if e["id"] == "CTRL-next-blocked")
    check_in("wait_existing_job is registered as a refusal", "wait_existing_job", entry["refuses"])
    check_in("and the way through is the person's word routed to release",
             "--operation release", entry["override"])
    check_in("carried by waiver.py", "waiver.py", entry["override"])


_SCOPE_START, _SCOPE_END = "Scanned refusal by refusal", "A refusal there is"


def _scope_gap(doc: str, scanned) -> tuple:
    """(missing, extra): the `SCANNED` modules the SCOPE span of `doc` does not name, and the `x.py` names it carries that
    `SCANNED` does not hold. The span runs from `Scanned refusal by refusal` to `A refusal there is`; a marker that is not
    there is reported as a missing item (never a silent pass)."""
    start = doc.find(_SCOPE_START)
    end = doc.find(_SCOPE_END, start + 1) if start >= 0 else -1
    if start < 0 or end < 0:
        absent = [m for m, at in ((_SCOPE_START, start), (_SCOPE_END, end)) if at < 0]
        return ["marker: " + m for m in absent], []
    named = set(re.findall(r"`([\w]+\.py)`", doc[start:end]))
    return sorted(set(scanned) - named), sorted(named - set(scanned))


def part_scope_docstring() -> None:
    """the SCOPE paragraph of the module docstring names every `SCANNED` module and no other `x.py` (AR-22: a docstring
    followed 4 of 6 names for a release; the carrier is `SCANNED`, the prose follows it)."""
    doc, scanned = RR.__doc__, RR.SCANNED
    check_eq("all six scanned modules are in SCANNED", len(scanned), 6)
    check_eq("the SCOPE span names every scanned module and nothing else", _scope_gap(doc, scanned), ([], []))
    for name in ("stage_guard.py", "inject_context.py", "guard_pre_tool.py", "native_context.py",
                 "codex_roles.py", "host_adapter.py"):
        check_in(f"{name} is scanned", name, scanned)
        check_eq(f"removing {name} from the span turns the gap on",
                 _scope_gap(doc.replace(f"`{name}`", "", 1), scanned), ([name], []))
    check_eq("a module added to SCANNED and not to the prose is missing",
             _scope_gap(doc, scanned + ("x.py",)), (["x.py"], []))
    check_eq("a `foo.py` added in the span is extra",
             _scope_gap(doc.replace(_SCOPE_START, _SCOPE_START + " `foo.py`", 1), scanned), ([], ["foo.py"]))
    check("a missing start marker is reported", _scope_gap(doc.replace(_SCOPE_START, "X", 1), scanned)[0])
    check("a missing end marker is reported", _scope_gap(doc.replace(_SCOPE_END, "X", 1), scanned)[0])


# --- the wide scan (told-before-work T0): table rows -------------------------------------------------------------------
# What `sites()` and `sites(raises=raise_family())` answered for this source BEFORE the wide scan existed (computed on the
# unmodified module; the `'` tail is the scanner's key text as it was, a quirk this row pins rather than fixes).
_DEFAULT_SRC = '''
import sys

class Mine(ValueError):
    pass

def deny(message):
    return 2

def block(message):
    return 2

def f(event):
    deny("alpha")
    block("beta")
    raise ValueError("gamma")

def g(event):
    raise Mine("delta")

def h(event):
    print("eps", file=sys.stderr)
    errors = []
    errors.append("zeta")
    if event:
        sys.exit("eta")
    return 2
'''
_DEFAULT_PLAIN = [{"file": "stage_guard.py", "function": "f", "call": "alpha'", "line": 14},
                  {"file": "stage_guard.py", "function": "f", "call": "beta'", "line": 15},
                  {"file": "stage_guard.py", "function": "f", "call": "gamma'", "line": 16}]
_DEFAULT_FAMILY = _DEFAULT_PLAIN + [{"file": "stage_guard.py", "function": "g", "call": "delta'", "line": 19}]


def _wide_package(files: dict) -> Path:
    """A throwaway <root>/scripts/<name> per entry (a name with a slash makes the folder)."""
    root = temp_dir("qa-factory-wide-")
    for name, body in files.items():
        path = root / "scripts" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(body, bytes):
            path.write_bytes(body)
        else:
            path.write_text(textwrap.dedent(body), encoding="utf-8")
    return root


def _wide(body, files=None, blocking=None, census=None) -> dict:
    """The wide report of ONE fixture file `stage_guard.py` (or of `files`): sites, walk errors, blind spots."""
    files = files if files is not None else {"stage_guard.py": body}
    root = _wide_package(files)
    try:
        return RR.wide_report(root, sorted(f for f in files if "/" not in f), census, blocking)
    finally:
        cleanup(root)


def _blind(rep: dict, needle: str) -> int:
    return sum(n for label, n in rep["blind_spots"].items() if needle in label)


def part_wide_defaults() -> None:
    """(a) The wide scan is one switch: without it the answers are the ones stored above, byte for byte."""
    root = _fake_package(_DEFAULT_SRC)
    try:
        check_eq("default sites() equals the stored answer", RR.sites(root), _DEFAULT_PLAIN)
        check_eq("sites(raises=raise_family()) equals the stored answer", RR.sites(root, raises=RR.raise_family(root)),
                 _DEFAULT_FAMILY)
        check("raise_family() without `wide` carries no transports",
              all("transports" not in spec for spec in RR.raise_family(root).values()))
        check_eq("raise_family(wide=True) carries WIDE_TRANSPORTS in every spec",
                 {spec.get("transports") for spec in RR.raise_family(root, wide=True).values()}, {RR.WIDE_TRANSPORTS})
        wide = RR.sites(root, raises=RR.raise_family(root, wide=True))
        check_eq("the wide scan keeps every default site (file, function, line)",
                 [(s["file"], s["function"], s["line"]) for s in wide if s["transport"] in ("deny", "block", "raises")],
                 [(s["file"], s["function"], s["line"]) for s in _DEFAULT_FAMILY])
        check("every wide site carries a transport and a state",
              all(s["transport"] in RR.WIDE_TRANSPORTS and s["state"] in RR.STATES for s in wide))
        check_eq("the list append and the `sys.exit(str)` of `h` are the wide scan's own sites (its stderr print is followed by "
                 "an assignment, so it is a note: a named blind spot, never a site)",
                 sorted(s["transport"] for s in wide if s["function"] == "h"),
                 ["list", "sys.exit(str)"])
    finally:
        cleanup(root)


def part_wide_transports() -> None:
    """(b) one fixture site per transport kind of WIDE_TRANSPORTS (each its own row)."""
    guard = "def deny(m):\n    return 2\n\ndef block(m):\n    return 2\n\n"
    rows = (
        ("deny", guard + "def f(e):\n    return deny('a')\n"),
        ("block", guard + "def f(e):\n    return block('a')\n"),
        ("refuse", "from role_cli import refuse\n\ndef f(e):\n    return refuse('cmd.py', 'a problem')\n"),
        ("run_guarded", "from role_cli import run_guarded\n\ndef f(e):\n    raise ValueError('a')\n\n"
                        "def main():\n    return run_guarded('cmd.py', f)\n"),
        ("raises", "def f(e):\n    raise ValueError('a')\n"),
        ("sys.exit(str)", "import sys\n\ndef f(e):\n    sys.exit('a')\n"),
        ("SystemExit(str)", "def f(e):\n    raise SystemExit('a')\n"),
        ("stderr-print+return", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    return 2\n"),
        ("stderr-write+return", "import sys\n\ndef f(e):\n    sys.stderr.write('a')\n    return 2\n"),
        ("list", "def f(e):\n    problems = []\n    problems.append('a')\n    return problems\n"),
    )
    check_eq("the rows cover WIDE_TRANSPORTS exactly", [r[0] for r in rows], list(RR.WIDE_TRANSPORTS))
    for transport, body in rows:
        rep = _wide(body)
        got = [s["transport"] for s in rep["sites"]]
        check_eq(f"{transport}: one site, of that transport", got, [transport])
        check_eq(f"{transport}: no walk error", (rep["walk_errors"], rep["check_arg_errors"]), ([], []))
    # the stderr print is a site only when the NEXT statement of its block fails (T0-gate change 1); each other shape is a NAMED
    # blind spot, with a count (a note or a progress line is never a refusal)
    tail = "not followed by a failing return"
    for label, body in (
            ("a return of zero next", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    return 0\n"),
            ("a return of an expression next", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    return len(e)\n"),
            ("a note, then a failing return two statements later",
             "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    e = 1\n    return 2\n"),
            ("a note in a loop, the failing return outside the block",
             "import sys\n\ndef f(e):\n    for x in e:\n        print('a', file=sys.stderr)\n    return 2\n"),
            ("two prints, only the second beside the return",
             "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    print('b', file=sys.stderr)\n    return 2\n"),
            ("nothing after it", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n")):
        rep = _wide(body)
        expect = 1 if label.startswith("two prints") else 0
        check_eq(f"stderr with {label}: sites", len(rep["sites"]), expect)
        check_eq(f"stderr with {label}: a named blind spot, counted", _blind(rep, tail), 2 - expect if label.startswith("two") else 1)
    check_eq("stderr beside a raise: a site", [s["transport"] for s in _wide(
        "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    raise SystemExit(2)\n")["sites"]], ["stderr-print+return"])
    for label, body in (("EXIT_ name", "EXIT_BAD = 3\n\ndef f(e):\n    print('a', file=sys.stderr)\n    return EXIT_BAD\n"),
                        ("sys.exit(2)", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    sys.exit(2)\n"),
                        ("return -1", "import sys\n\ndef f(e):\n    print('a', file=sys.stderr)\n    return -1\n")):
        check_eq(f"stderr beside {label}: a site", [s["transport"] for s in _wide(body)["sites"]], ["stderr-print+return"])
    # the list transport counts only inside a unit the census marks blocking; None means every function
    body = "def f(e):\n    errors = []\n    errors.append('a')\n"
    check_eq("list: blocking=None counts every function", len(_wide(body)["sites"]), 1)
    check_eq("list: a function outside the blocking set is not counted", len(_wide(body, blocking={("stage_guard.py", "g")})["sites"]), 0)
    check_eq("list: a function inside the blocking set is counted", len(_wide(body, blocking={("stage_guard.py", "f")})["sites"]), 1)


def part_wide_states() -> None:
    """(c) sourced / tagged / bare. `refusal` counts only when the file binds it to detector_verdict: the package has four
    other functions of that name (session_identity, role_digest, ...), and a call of those is NOT a Record."""
    head = "from detector_verdict import refusal, with_check\n\n"
    rows = (
        ("a refusal() Record at block", head + "def f(e):\n    return block(refusal('x:y', 'p'))\n", "sourced"),
        ("a refusal() Record at deny", head + "def f(e):\n    return deny(refusal('x:y', 'p'))\n", "sourced"),
        ("a refusal() Record at refuse", head + "def f(e):\n    return refuse('c', refusal('x:y', 'p'))\n", "sourced"),
        ("a refusal() Record in a list", head + "def f(e):\n    out = []\n    out.append(refusal('x:y', 'p'))\n", "sourced"),
        ("a list that is joined in its function",
         head + "def f(e):\n    out = []\n    out.append(refusal('x:y', 'p'))\n    return '\\n'.join(out)\n", "tagged"),
        ("a list that is str()-ed in its function",
         head + "def f(e):\n    out = []\n    out.append(refusal('x:y', 'p'))\n    return str(out)\n", "tagged"),
        ("a refusal() Record at stderr", head + "import sys\n\ndef f(e):\n    print(refusal('x:y', 'p'), file=sys.stderr)\n    return 2\n",
         "tagged"),
        ("a refusal() Record at a raise (not a sink)", head + "def f(e):\n    raise ValueError(refusal('x:y', 'p'))\n", "tagged"),
        ("a with_check() Record at block", head + "def f(e):\n    return block(with_check('t', 'x:y'))\n", "tagged"),
        ("module attribute form", "import detector_verdict as DV\n\ndef f(e):\n    return block(DV.refusal('x:y', 'p'))\n", "sourced"),
        ("from-import alias", "from detector_verdict import refusal as R\n\ndef f(e):\n    return block(R('x:y', 'p'))\n", "sourced"),
        ("a plain text", "def f(e):\n    return block('p')\n", "bare"),
        ("a name", "def f(e):\n    msg = build()\n    return block(msg)\n", "bare"),
        ("a refusal of ANOTHER module", "from session_identity import refusal\n\ndef f(e):\n    return block(refusal(e, 's.py'))\n",
         "bare"),
        ("a refusal with a module-attribute of another module", "import role_digest as RD\n\ndef f(e):\n    return block(RD.refusal(e, 1))\n",
         "bare"),
    )
    for label, body, want in rows:
        sites = _wide(body)["sites"]
        check_eq(f"{label}: {want}", [s["state"] for s in sites], [want])
    # the check id: a literal or a module constant is read; anything else is a walk error, named, never a crash
    rep = _wide(head + "ID = 'x:y'\n\ndef f(e):\n    return block(refusal(ID, 'p'))\n")
    check_eq("a module constant check id is read", [s.get("check") for s in rep["sites"]], ["x:y"])
    rep = _wide(head + "def f(e, check):\n    return block(refusal(check, 'p'))\n")
    check_eq("a check id that is a parameter is a walk error", [w["transport"] for w in rep["check_arg_errors"]], ["check_arg"])
    check_in("and the walk error says what to do", "name the check with a literal", rep["check_arg_errors"][0]["why"])
    rep = _wide("def refusal(check, problem):\n    return with_check(problem, check)\n",
                files={"detector_verdict.py": "def refusal(check, problem):\n    return with_check(problem, check)\n"})
    check_eq("inside detector_verdict the bare names count (a parameter pass-through is a walk error of T2 to settle)",
             len(rep["check_arg_errors"]), 1)


def part_wide_blind() -> None:
    """(d) every adversarial input of the spec and every census blind spot: one row, verdict `seen` (a site) or
    `named blind spot` (no site, a counted label of the report). What the scan cannot see is never silent."""
    fam = "class MyErr(ValueError):\n    pass\n\n"
    rows = (
        # name, source, verdict, wanted transport (seen) or blind-spot label fragment (named blind spot)
        ("an alias `b = block; b(msg)`", "def f(e):\n    b = block\n    return b('x')\n", "named blind spot", "alias of a transport"),
        ("a message built in another function and passed in", "def f(e):\n    return deny(build(e))\n", "seen", "deny"),
        ("print(json.dumps(..), file=sys.stderr) then return 2",
         "import sys, json\n\ndef f(e):\n    print(json.dumps({'a': 1}), file=sys.stderr)\n    return 2\n", "seen", "stderr-print+return"),
        ("sys.stderr.write(..) then return 2", "import sys\n\ndef f(e):\n    sys.stderr.write('x')\n    return 2\n", "seen",
         "stderr-write+return"),
        ("sys.exit('<message>')", "import sys\n\ndef f(e):\n    sys.exit('x')\n", "seen", "sys.exit(str)"),
        ("sys.exit(<name>)", "import sys\n\ndef f(e):\n    sys.exit(msg)\n", "named blind spot", "non-text expression"),
        ("raise SystemExit('<message>')", "def f(e):\n    raise SystemExit('x')\n", "seen", "SystemExit(str)"),
        ("a list under any name (reasons.append)", "def f(e):\n    reasons = []\n    reasons.append('x')\n", "seen", "list"),
        ("a list under any name (acceptance.problems.extend)", "def f(e, acceptance):\n    acceptance.problems.extend(['x'])\n", "seen", "list"),
        ("errors += [..]", "def f(e):\n    errors = []\n    errors += ['x']\n", "seen", "list"),
        ("a yield of an error string", "def f(e):\n    yield 'x'\n", "named blind spot", "yield of an error text"),
        ("a package subclass raise", fam + "def f(e):\n    raise MyErr('x')\n", "seen", "raises"),
        ("a stdlib subclass", "class E(RuntimeError):\n    pass\n\ndef f(e):\n    raise E('x')\n", "named blind spot",
         "stdlib exception base"),
        ("a base that is not a plain name", "def make():\n    return ValueError\n\nclass E(make()):\n    pass\n\ndef f(e):\n    raise E('x')\n",
         "named blind spot", "neither a plain name"),
        ("a raise through an assignment alias", fam + "def f(e):\n    E = MyErr\n    raise E('x')\n", "named blind spot",
         "alias of a transport"),
        ("`raise A` with no call", fam + "def f(e):\n    raise MyErr\n", "named blind spot", "no call"),
        ("`raise A()` with no argument", fam + "def f(e):\n    raise MyErr()\n", "named blind spot", "no message argument"),
        ("a raise of a module factory call", "def f(e):\n    raise _held_by(e)\n", "named blind spot", "factory function or method"),
        ("a raise of a method that returns the exception", "def f(self):\n    raise self._reuse_refusal(1)\n", "named blind spot",
         "factory function or method"),
        ("deny with no argument", "def f(e):\n    return deny()\n", "named blind spot", "no message argument"),
    )
    for label, body, verdict, want in rows:
        rep = _wide(body)
        if verdict == "seen":
            check_eq(f"{label}: seen as `{want}`", [s["transport"] for s in rep["sites"]], [want])
        else:
            check_eq(f"{label}: no site", rep["sites"], [])
            check("and named: a counted blind spot " + repr(want), _blind(rep, want) >= 1, str(rep["blind_spots"]))
    # a class defined only under scripts/tests: counted from the tests folder, outside the scan root
    rep = _wide("x = 1\n", files={"stage_guard.py": "x = 1\n", "tests/t_only.py": "class E(ValueError):\n    pass\n"})
    check_eq("a class defined only under scripts/tests: a named blind spot, counted", _blind(rep, "scripts/tests"), 1)
    # input from outside: encoding, nesting, magnitude, empty -- the scan never crashes and never skips silently
    for label, body, walk in (
            ("a null byte in the source", b"def f(e):\n    return deny('x')\n\x00\n", 1),
            ("nesting past the parser's limit", ("x = " + "(" * 300 + "1" + ")" * 300 + "\n").encode(), 1),
            ("a syntax error", b"def f(:\n", 1),
            ("bytes that are not UTF-8", b"def f(e):\n    return deny('x\xff\xfe')\n", 0),
            ("an empty file", b"", 0),
            ("a file of comments only", b"# nothing\n", 0)):
        rep = _wide(None, files={"stage_guard.py": body})
        check_eq(f"{label}: walk errors", len(rep["walk_errors"]), walk)
        if walk:
            check_eq(f"{label}: named by file and counted in the share", (rep["walk_errors"][0]["file"], rep["totals"]["walk_error_share"]),
                     ("stage_guard.py", 1.0))
    rep = _wide(None, files={"stage_guard.py": b"def f(:\n", "host_adapter.py": b"def f(e):\n    raise ValueError('x')\n"})
    check_eq("an unparsable file does not hide the next one", (len(rep["walk_errors"]), len(rep["sites"])), (1, 1))
    expr = " + ".join(["'a'"] * 4000)
    rep = _wide(f"def f(e):\n    return deny({expr})\n")
    check("a 4000-term message: no crash, and the call is a site, a counted blind spot or a named walk error",
          len(rep["sites"]) + sum(rep["blind_spots"].values()) + len(rep["walk_errors"]) >= 1, str(rep))
    rep = _wide("def f(e):\n    return deny('" + "x" * 100000 + "')\n")
    check_eq("a 100000-char message: a site, the key cut at KEY_CHARS", [len(s["call"]) <= RR.KEY_CHARS for s in rep["sites"]], [True])
    root = _wide_package({})
    try:
        rep = RR.wide_report(root, [])
    finally:
        cleanup(root)
    check_eq("an empty scan prints zero counts", (rep["totals"]["sites"], rep["totals"]["units"], rep["totals"]["walk_errors"],
                                                  rep["totals"]["walk_error_share"]), (0, 0, 0, 0.0))


def part_wide_census() -> None:
    """(e) the `--census` join: a unit gets the roles of its row by (file, function); no row -> `roles: null`, counted."""
    import json
    tmp = temp_dir("qa-factory-census-")
    try:
        census = tmp / "census.json"
        census.write_text(json.dumps({"rows": [
            {"file": "stage_guard.py", "function": "f", "class": "shape", "roles": ["qa-scout", "conductor"], "owner": "data"},
            {"file": "stage_guard.py", "function": "f", "class": "safety", "roles": ["qa-runner"], "owner": "data"},
            {"file": "stage_guard.py", "function": "c", "class": "shape", "roles": ["conductor"], "owner": "data"}]}),
            encoding="utf-8")
        loaded = RR.load_census(census)
        check_eq("two rows of one unit join as the union of their roles", loaded[("stage_guard.py", "f")],
                 ["qa-scout", "conductor", "qa-runner"])
        body = ("def f(e):\n    raise ValueError('a')\n\ndef c(e):\n    raise ValueError('b')\n\n"
                "def n(e):\n    raise ValueError('c')\n\ndef m(e):\n    raise ValueError('d')\n    raise ValueError('e')\n")
        rep = _wide(body, census=loaded)
        by = {u["function"]: u for u in rep["units"]}
        check_eq("a unit with a row carries its roles", by["f"]["roles"], ["qa-scout", "conductor", "qa-runner"])
        check_eq("a unit with no row: roles null, not dropped", (by["n"]["roles"], by["m"]["roles"], by["m"]["sites"]), (None, None, 2))
        t = rep["totals"]
        check_eq("units, units with a row, units with no row", (t["units"], t["units_with_row"], t["units_no_row"]), (4, 2, 2))
        check_eq("join share is units with a row over units", t["join_share"], 0.5)
        check_eq("role-reachable: a unit with any role besides the conductor; conductor-only counted apart",
                 (t["role_reachable_units"], t["conductor_only_units"], t["role_reachable_sites"]), (1, 1, 1))
        check_eq("no census passed: every roles is null and no join total is invented",
                 ([u["roles"] for u in _wide(body)["units"]], "join_share" in _wide(body)["totals"]), ([None] * 4, False))
        # the command line: absent, unreadable and not-a-census paths are exit 2 with the reason on stderr, before any scan
        for label, path, reason in (("absent path", tmp / "nope.json", "cannot read it"),
                                    ("a directory", tmp, "cannot read it"),
                                    ("not JSON", _write(tmp / "bad.json", "{not json"), "not JSON"),
                                    ("not a census", _write(tmp / "list.json", "[1, 2]"), "no `rows` list"),
                                    ("rows that are not a list", _write(tmp / "rows.json", '{"rows": 3}'), "no `rows` list")):
            p = run_script("refusal_registry.py", "--sites", "--census", path)
            check_eq(f"--census {label}: exit 2", p.returncode, 2)
            check_in(f"--census {label}: the reason on stderr", reason, p.stderr)
            check_eq(f"--census {label}: nothing on stdout", p.stdout, "")
        p = run_script("refusal_registry.py", "--sites", "--census", census, "--json")
        out = json.loads(p.stdout)
        check_eq("--sites --census (default scan): exit 0 and the sites are the A24 scan's", (p.returncode, len(out["sites"])),
                 (0, len(RR.sites())))
        check("and every unit of it is joined or null", all("roles" in u for u in out["units"]))
    finally:
        cleanup(tmp)


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def part_passthrough() -> None:
    """T1c, F7 (a): a def listed in `CHECK_PASSTHROUGH` hands its `check` parameter to `with_check`: the ids are the literals at
    its bare-name call sites in the scope where it is visible (matched by the INNERMOST def); every other shape stays a walk
    error. The ids travel as `check_id` records (state `walk_error`: a scan fact, never a unit or a total)."""
    head = "import detector_verdict as DV\n\n"
    inner = "    def own(records, check):\n        return [DV.with_check(r, check) for r in records]\n"

    def scan(body: str, name: str = "exit_gate.py") -> tuple:
        root = _wide_package({name: head + body})
        try:
            found = RR.sites(root, [name], raises=RR.raise_family(root, [name], wide=True))
            rep = RR.wide_report(root, [name])
        finally:
            cleanup(root)
        return sorted(s["check"] for s in found if s["transport"] == "check_id"), rep

    ids, rep = scan(f"def all_errors():\n{inner}    return own(f(), 'x:a') + own(g(), 'x:b')\n")
    check_eq("pass/literal-at-call: the ids are the literals at the call sites and there is no walk error",
             (ids, rep["check_arg_errors"], rep["walk_errors"]), (["x:a", "x:b"], [], []))
    check_eq("pass/literal-at-call: a check_id record is no site and no unit of the report",
             (rep["totals"]["sites"], rep["units"]), (0, []))
    ids, rep = scan(f"def all_errors():\n{inner}    return own(f(), 'x:a') + own(g(), name)\n")
    check_eq("pass/non-literal-at-call: a call that gives no literal is a walk error, at the CALL; the literal one still gives its id",
             (ids, [(w["transport"], w["line"]) for w in rep["check_arg_errors"]]), (["x:a"], [("check_arg", 6)]))
    check_in("pass/non-literal-at-call: and it says what to do", "name the check with a literal", rep["check_arg_errors"][0]["why"])
    ids, rep = scan(f"def all_errors():\n{inner.replace('own', 'own2')}    return own2(f(), 'x:a')\n")
    check_eq("pass/unlisted: the same shape under a name that is not listed is a walk error at the with_check call, and gives no id",
             (ids, [w["transport"] for w in rep["check_arg_errors"]]), ([], ["check_arg"]))
    ids, rep = scan(f"def build():\n{inner}    return own(f(), 'x:n')\n")
    check_eq("pass/nested-def: the listed def nested in ANOTHER def is matched by its innermost def (the outer name is not listed)",
             (ids, rep["check_arg_errors"]), (["x:n"], []))
    ids, rep = scan(f"def all_errors():\n{inner}    return own(f(), 'x:a') + m.own(g(), name)\n")
    check_eq("pass/attr-call-same-name-ignored: `m.own(x)` is no call site (no id, no walk error)",
             (ids, rep["check_arg_errors"]), (["x:a"], []))
    ids, rep = scan(f"def all_errors():\n{inner}    return []\n")
    check_eq("pass/E8: a listed def with no call that gives a literal is a walk error naming the list",
             (ids, [w["why"] for w in rep["check_arg_errors"]]),
             ([], ["`own` is listed in CHECK_PASSTHROUGH and has no call with a literal check"]))
    ids, rep = scan("def own(records, check):\n    return [DV.with_check(r, check) for r in records]\n\n\ndef run():\n    return own(f(), 'x:m')\n")
    check_eq("pass/module-level: a module-level listed def is read at the calls of the module", (ids, rep["check_arg_errors"]), (["x:m"], []))
    ids, rep = scan(f"def all_errors():\n{inner}    return own(f(), 'x:a')\n", name="other.py")
    check_eq("pass/file-listed: the list names (file, def): the same def in another file is not passed through",
             (ids, len(rep["check_arg_errors"])), ([], 1))
    real = RR.wide_report(PLUGIN_ROOT, ["exit_gate.py"])
    check_eq("pass/real-tree: exit_gate.py has no check_arg walk error (its `own` is listed)", real["check_arg_errors"], [])


def part_check_of() -> None:
    """`check_of(entry)` is `<file stem>:<id>`, the one namespace of a check; one id per A24 entry, never two the same."""
    check_eq("check_of: the stem of the file, a colon, the id", RR.check_of({"file": "scripts/manifest_put.py", "id": "X-y"}),
             "manifest_put:X-y")
    check_eq("check_of: a bare file name", RR.check_of({"file": "stage_guard.py", "id": "SG-1"}), "stage_guard:SG-1")
    ids = [RR.check_of(entry) for entry in RR.REGISTRY]
    check_eq("check_of: one id per A24 entry", len(set(ids)), len(ids))
    check("check_of: every id matches the family grammar of a check id",
          all(re.fullmatch(r"[A-Za-z0-9_]+:[A-Za-z0-9_.\[\]-]+", i) for i in ids))


def main() -> None:
    part_check_of()
    part_passthrough()
    part_wide_defaults()
    part_wide_transports()
    part_wide_states()
    part_wide_blind()
    part_wide_census()
    part_scanner()
    part_door_texts()
    part_live_package()
    part_fail_closed()
    part_scope_docstring()
    finish("test_refusal_registry")


if __name__ == "__main__":
    main()
