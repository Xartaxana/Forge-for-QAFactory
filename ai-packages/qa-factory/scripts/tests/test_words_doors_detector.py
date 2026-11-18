#!/usr/bin/env python3
"""detector: a part of test_words_doors.py, split by tools/test_split.py (TD-11c). The shared helpers are in words_doors_common."""
import ast
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, SCRIPTS, check, check_eq, driver_sources, finish
sys.path.insert(0, str(SCRIPTS))
import person_words  # noqa: E402
from words_doors_common import DRIVER_KEY, FLAG, PENDING, hits_in  # noqa: E402


# Inline doors of upstream 0.8.1 that the merge brought in and that are queued, not converted
# (B-387 names the doors listed here; B-365 names two other carriers, `stand_identity --words` and
# `source_exclusions --revoke --words`, which the scan's command list does not read). A pending
# file lists the EXACT texts the scan matched there: a hit that
# is not one of them - a NEW inline door in the same file - still fails. The node that lands the
# file form removes its entry; a file found clean says so below. `gate_preflight.py` and
# `stand_gaps.py` are not here: their cards are upstream's renderer now (a person answers
# `<id>: <word>`, no script), and the scan finds nothing in them.
PENDING_REASON = "upstream 0.8.1 door, queued B-387"


# Entries whose reason is not the default one.
PENDING_PINNED = ("scripts/stage_done.py", "scripts/story_step.py")


PENDING_PINNED_REASON = "upstream 0.8.1 door pinned by an upstream test, queued B-387"


# A NAMED exemption, not a finding: the driver records a person's words by calling `waiver.py` itself
# with a LIST argv (no shell, so no cmd.exe cut at the first line break) and the words as one argument;
# the scan reads string constants and cannot see such a call, so `driver_inline_calls` finds them
# and the check below fails if the exemption no longer names one (a stale exemption is a lie).
# `waiver.py` and `person_words.read` keep accepting an inline `--decision` for them (spec t-428 L5).
EXEMPT = {
    DRIVER_KEY: "upstream's driver waiver calls: list argv, no shell, one card line (the "
                            "`take_stand_gap_answers` family)",
}


DOC_DIRS = ("skills", "references", "design", "handoffs", "agents")


DOC_SUFFIXES = (".md", ".yaml", ".yml", ".json")


SCRIPT_NAME = re.compile(r"[A-Za-z_][\w-]*\.py")


def _placeholder(part) -> str:
    """An f-string placeholder as `{}`, except one whose expression NAMES a script
    (`{self.scripts / 'waiver.py'}`): that is the command's own word, so it is kept as the script's
    basename. Rendered `{}`, the command vanished from the text and the door behind it was never read
    (the mode-switch door of the driver, which a person sees, was missed that way)."""
    try:
        source = ast.unparse(part.value if isinstance(part, ast.FormattedValue) else part)
    except Exception:  # noqa: BLE001 - an expression that cannot be unparsed is a plain placeholder
        return "{}"
    named = SCRIPT_NAME.search(source)
    return named.group(0) if named else "{}"


def _render(node):
    """A string constant, an f-string (every `{...}` as `{}`), or a `+` chain of them; else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(part.value if isinstance(part, ast.Constant) else _placeholder(part) for part in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _render(node.left), _render(node.right)
        if left is None and right is None:
            return None
        return ("{}" if left is None else left) + ("{}" if right is None else right)
    return None


def _strings(node, skip: set, out: list) -> None:
    if id(node) in skip:
        return
    text = _render(node)
    if text is not None:
        out.append(text)
        return
    for child in ast.iter_child_nodes(node):
        _strings(child, skip, out)


def python_texts(source: str) -> list:
    """The checked strings of one script. Skipped: an `add_argument` help (the CLI documents its
    own inline option beside the file form), the arguments of `.error(` (an argparse refusal
    names both options), and the module docstring of a CLI that itself names `--words-file`."""
    tree = ast.parse(source)
    skip: set = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_argument":
                skip.update(id(kw.value) for kw in node.keywords if kw.arg == "help")
            elif node.func.attr == "error":
                skip.update(id(arg) for arg in node.args)
    first = tree.body[0] if tree.body else None
    if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str) and FLAG in first.value.value):
        skip.add(id(first.value))
    out: list = []
    _strings(tree, skip, out)
    return out


def script_units(plugin_root: Path) -> list:
    """[(key, text)] of every script the inventory reads. The files of the driver set (`harness.driver_sources`) all
    carry the one key DRIVER_KEY, so a door that moves between the driver's parts keeps its entry."""
    in_driver = {path: text for path, text in driver_sources(plugin_root)}
    units = [(DRIVER_KEY, text) for text in in_driver.values()]
    for path in sorted((plugin_root / "scripts").glob("*.py")):
        if path in in_driver or path.name == "person_words.py":
            continue  # person_words: the reader and the renderer, they name the inline option to refuse it
        units.append((path.relative_to(plugin_root).as_posix(), path.read_text(encoding="utf-8")))
    return units


def scan(plugin_root: Path = PLUGIN_ROOT) -> dict:
    """{path relative to the package: [inline doors found]} over everything the detector reads."""
    found: dict = {}
    for key, source in script_units(plugin_root):
        try:
            texts = python_texts(source)
        except SyntaxError:
            continue  # another builder's unfinished edit: the syntax error is that node's to report
        hits = [hit for text in texts for hit in hits_in(text)]
        if hits:
            found.setdefault(key, []).extend(hits)
    for directory in DOC_DIRS:
        for path in sorted((plugin_root / directory).rglob("*")):
            if path.is_file() and path.suffix in DOC_SUFFIXES:
                hits = hits_in(path.read_text(encoding="utf-8", errors="replace"))
                if hits:
                    found[path.relative_to(plugin_root).as_posix()] = hits
    return found


def unlisted_of(found: dict) -> dict:
    """The hits that are neither in a pending file's own list of matched texts nor exempt by name."""
    out = {}
    for path, hits in found.items():
        listed = PENDING.get(path, ())
        rest = [hit for hit in hits if hit not in listed]
        if rest:
            out[path] = rest
    return out


def _is_door_call(node) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "door"
    return (isinstance(func, ast.Attribute) and func.attr == "door"
            and isinstance(func.value, ast.Name) and func.value.id in ("person_words", "PW"))


def converted_doors(plugin_root: Path = PLUGIN_ROOT) -> dict:
    """{script: number of `person_words.door()` calls}: the doors that ARE in the file form. The scan
    finds only the problem, so this is its positive control: a scan that finds nothing is read
    together with the files that were converted."""
    out: dict = {}
    for key, source in script_units(plugin_root):
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        count = sum(1 for node in ast.walk(tree) if _is_door_call(node))
        if count:
            out[key] = out.get(key, 0) + count
    return out


def driver_inline_calls(plugin_root: Path = PLUGIN_ROOT) -> list:
    """The `file:line` of the calls `X("waiver.py", ..., "--decision", value, ...)` in the driver set (`harness.driver_sources`): a
    list argv with the words as one argument (the named exemption)."""
    lines = []
    for path, text in driver_sources(plugin_root):
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Call):
                consts = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                if consts[:1] == ["waiver.py"] and "--decision" in consts:
                    lines.append(f"{path.name}:{node.lineno}")
    return sorted(lines)


def part_detector() -> None:
    inline = 'waiver.py --task T --stage S1 --block "x" --decision "<their words>"'
    check("negative control: the inline door is a hit", len(hits_in(inline)) == 1, str(hits_in(inline)))
    file_form = 'waiver.py --task T --stage S1 --block "x" --words-file <file>'
    check_eq("and the same door with --words-file is not", hits_in(file_form), [])
    check("a markdown line broken across two lines is still one door",
          len(hits_in('`waiver.py --task T --stage S1 --block "x" --decision\n"<their words>"`')) == 1)
    check("a yaml / json escaped quote is read",
          len(hits_in('recorded_by: "waiver.py --task <T> --block \\"k\\" --decision \\"<words>\\""')) == 1)
    check_eq("a bare option name (prose, no value shown) is a hit; the file option is not",
             [len(hits_in(text)) for text in ("`controller.py --operation release --dispatch S3-x --words (or ...)`",
                                              "`controller.py --operation release --dispatch S3-x --words-file <file>`")],
             [1, 0])
    check("a gate-decision door is a hit",
          len(hits_in("`controller.py --operation gate-decision --gate A --words \"<their words>\"`")) == 1)
    # B-411 A9: the notes CLI records a person's words (`answer`), so it is on the detector's closed command lists
    check("A9: an inline words option on onboarding_notes.py answer is a hit (the command is on the detector's list)",
          len(hits_in('onboarding_notes.py --root . answer --batch b1 --answered t1 --words "<their words>"')) == 1)
    check_eq("A9: the file form of the same door is not a hit",
             hits_in(f'onboarding_notes.py --root . answer --batch b1 --answered t1 {FLAG} <file>'), [])
    check_eq("A9: a bare option name in prose on that command is a hit too",
             len(hits_in("`onboarding_notes.py --root . answer --batch b1 --words (their words)`")), 1)
    # t-721 D4/T-door: `story_step.py decide` records a person's decision and takes its words ONLY by file
    check("decide: an inline words option on story_step.py decide is a hit (the command is on the detector's list)",
          len(hits_in('story_step.py decide --task T --dispatch-id D --hand TC-1 --words "<their words>"')) == 1)
    check_eq("decide: the file form of the same door is not a hit",
             hits_in(f'story_step.py decide --task T --dispatch-id D --hand TC-1 {FLAG} <file>'), [])
    decide_source = (PLUGIN_ROOT / "scripts" / "story_step.py").read_text(encoding="utf-8")
    import re as _re

    def decide_reads_by_file_only(source: str) -> bool:
        """The one search, run over a source text: `decide` reads through `person_words.read` from `--words-file`, names no
        inline `args.words`, and the parser has no inline `--words` option."""
        body = _re.search(r"\ndef decide\(.*?\n\n\n", source, _re.S)
        return (bool(body) and "person_words.read(None, args.words_file," in body.group(0)
                and "args.words," not in body.group(0) and 'add_argument("--words"' not in source)
    check("decide: the words come through the one reader, person_words.read, from --words-file (and no inline option)",
          decide_reads_by_file_only(decide_source))
    # t-827 FX-4: the control is the SAME search over a mutated copy of the real source (the reader switched to the inline
    # option), which must fail - and a copy that grew the inline parser option must fail too
    inline_reader = decide_source.replace("person_words.read(None, args.words_file,", "person_words.read(args.words, None,")
    check("decide: negative control - the mutation applied to the source text (exactly one reader call)",
          decide_source.count("person_words.read(None, args.words_file,") == 1 and inline_reader != decide_source)
    check_eq("decide: negative control - the same search over a copy that reads inline words fails",
             decide_reads_by_file_only(inline_reader), False)
    inline_option = decide_source.replace('p.add_argument("--words-file"', 'p.add_argument("--words")\n    p.add_argument("--words-file"')
    check_eq("decide: negative control - the same search over a copy with an inline `--words` parser option fails",
             (inline_option != decide_source, decide_reads_by_file_only(inline_option)), (True, False))
    check_eq("a bare `--text` of another command is not a door",
          hits_in('judge_reply.py --reply "<their words>" --text "x"'), [])
    # A markdown table cell writes the pipe inside it as `\|` (`--gate A\|B`): the escaped pipe is
    # still the same command, and the stretch rule used to stop there, hiding the door behind it.
    # The line is the one conductor.md carried before the file form (git HEAD of 2026-10-03).
    table_inline = ("| A person's words for gate A or B | `controller.py --task-root <task root> --operation "
                    "gate-decision --gate A\\|B --words \"<their words, verbatim>\"` (`--drafts <ref,ref>` at B "
                    "for the bug drafts they chose by number, taken from the gate message) |")
    table_file = table_inline.replace('--words "<their words, verbatim>"', f"{FLAG} <file>")
    check_eq("an escaped table pipe does not hide an inline door (the conductor.md gate-decision line)",
             len(hits_in(table_inline)), 1)
    check_eq("and the same line in the file form is not a hit", hits_in(table_file), [])
    check_eq("a bare option name behind an escaped pipe is a hit too",
             len(hits_in("`controller.py --operation gate-decision --gate A\\|B --words (their words)`")), 1)
    check_eq("an unescaped pipe still ends the command's stretch",
             hits_in("`controller.py --operation gate-decision --gate A` | `x --words \"<w>\"`"), [])
    check("a python string constant is read, an f-string with `{}` too",
          len([h for t in python_texts('x = f"waiver.py --task {t} --stage S --block \\"k\\" --decision \\"<w>\\""')
               for h in hits_in(t)]) == 1)
    # A door whose script path is a placeholder (`{self.scripts / 'waiver.py'}`) was rendered `{}`, so the
    # command word was gone and the door behind it was never read (the driver's mode-switch door).
    quote = chr(92) + '"'
    placed = ("x = f\"python {self.scripts / 'waiver.py'} --task {t} --stage S1 --decision " + quote
              + "<your words>" + quote + "\"\n")
    check_eq("a placeholder that names the script keeps its name, so the inline door behind it is a hit",
             [len(hits_in(t)) for t in python_texts(placed)], [1])
    check_eq("...the same door in the file form is not a hit",
             [len(hits_in(t)) for t in python_texts(
                 "x = f\"python {self.scripts / 'waiver.py'} --task {t} --words-file <file>\"\n")], [0])
    check_eq("...and a placeholder that names no script stays a plain `{}`",
             python_texts("x = f\"python {path} --task {t}\"\n"), ["python {} --task {}"])
    check_eq("an add_argument help and an .error( argument are skipped",
             [h for t in python_texts(
                 'ap.add_argument("--x", help=\'waiver.py --block k --decision "<w>"\')\n'
                 'ap.error(\'waiver.py --block k --decision "<w>"\')\n') for h in hits_in(t)], [])
    check_eq("a CLI docstring that also names --words-file is skipped, another one is not",
             [len([h for t in python_texts(f'"""{extra}waiver.py --block k --decision "<w>"\n"""\n')
                   for h in hits_in(t)]) for extra in (f"{FLAG} <f> ", "")], [0, 1])

    # The negative control of the whole scan, on a synthetic package: an inline door in a script, in
    # a document and in a pending file (a text that is not the listed one) is unlisted; a door in
    # the file form, the listed text of a pending file and a door built by `door()` are not.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp)
        (fake / "scripts").mkdir()
        (fake / "skills").mkdir()
        (fake / "scripts" / "new_door.py").write_text(
            'MSG = \'waiver.py --task T --stage S1 --block "x" --decision "<their words>"\'\n', encoding="utf-8")
        (fake / "scripts" / "story_run.py").write_text(
            'A = \'' + PENDING[DRIVER_KEY][0] + '<w>"\'\n'
            'B = \'waiver.py --task T --stage S2 --block "other" --decision "<w>"\'\n', encoding="utf-8")
        (fake / "scripts" / "file_form.py").write_text(
            'import person_words\nMSG = person_words.door(\'waiver.py --task T --stage S1 --block "x"\')\n'
            'FILE = \'waiver.py --task T --stage S1 --block "x" --words-file <file>\'\n', encoding="utf-8")
        (fake / "skills" / "s.md").write_text(
            '`waiver.py --task <T> --stage S1 --block "x" --decision "<their words>"`\n', encoding="utf-8")
        synthetic = scan(fake)
        check_eq("negative control: a synthetic package is scanned (script, pending file, document; not the file form)",
                 sorted(synthetic), ["scripts/new_door.py", DRIVER_KEY, "skills/s.md"])
        check_eq("negative control: an inline door in a new script and a new document is unlisted",
                 sorted(path for path in unlisted_of(synthetic) if path != DRIVER_KEY),
                 ["scripts/new_door.py", "skills/s.md"])
        check_eq("negative control: a pending file lists its own text only; a NEW door in it is unlisted",
                 ["other" in hit for hit in unlisted_of(synthetic).get(DRIVER_KEY, [])],
                 [True])

    found = scan()
    unlisted = unlisted_of(found)
    check("positive control: the scan read the package (it found the pending doors, so an empty "
          "`unlisted` is not an empty scan)", sum(len(hits) for hits in found.values()) >= len(PENDING), str(sorted(found)))
    converted = converted_doors()
    # `story_step.py` is not here: its mode-switch door is upstream's inline text again (pending above).
    expected = ("controller.py", "manifest_put.py", "stage_done.py", "story_run.py")
    check_eq("positive control: the files whose doors were converted call person_words.door()",
             [name for name in expected if f"scripts/{name}" not in converted], [])
    check("the doors in the file form are listed: " + ", ".join(f"{p.split('/')[-1]} {n}" for p, n in sorted(converted.items())),
          len(converted) >= len(expected), str(converted))
    calls = driver_inline_calls()
    check("the named exemption names real calls: " + EXEMPT[DRIVER_KEY] + f" ({len(calls)} at lines "
          + ", ".join(map(str, calls)) + ")", len(calls) >= 1, "the driver set holds no waiver call with an inline --decision: "
          "remove the exemption")
    check_eq("no inline door outside the exemption and the pending list (B-387)", unlisted, {})
    for path, texts in sorted(PENDING.items()):
        reason = PENDING_PINNED_REASON if path in PENDING_PINNED else PENDING_REASON
        if found.get(path):
            print(f"PENDING {reason}: {path}: {len(found[path])} inline door(s), not failed here")
        else:
            print(f"clean now: remove {path} (pending: {reason})")
    for path, hits in sorted(unlisted.items()):
        for hit in hits:
            print(f"INLINE DOOR {path}: {hit[:140]}")


# --- item 1: the renderer ----------------------------------------------------------------------

def part_renderer() -> None:
    command = 'waiver.py --task T --stage S1 --block "x"'
    check_eq("door: the file option is appended", person_words.door(command), command + " --words-file <file>")
    check_eq("door: trailing whitespace is dropped, nothing else changes",
             person_words.door(command + "  \n"), command + " --words-file <file>")
    check_eq("door: for a person the placeholder says what goes in the file",
             person_words.door(command, for_person=True), command + " --words-file <file with your words>")
    check("door: the command itself is never changed (block quoting stays the site's own)",
          person_words.door(command).startswith(command))
    for label, empty in (("empty", ""), ("whitespace-only", " \n\t "), ("None", None)):
        try:
            person_words.door(empty)
            check(f"door: a {label} command is refused", False, "no ValueError")
        except ValueError:
            check(f"door: a {label} command is refused", True)


def main() -> None:
    part_renderer()
    part_detector()
    finish("test_words_doors_detector")


# split: runner piece 1
if __name__ == "__main__":
    main()
