"""local_keys.py and the local-story road of ticket_adapter.py (SS1-14, N2a): the key of a story no tracker holds.

What this file holds, and the mutation each part kills (the one file that kills it):
  is_local ........................ every input both ways: exact spelling, the file, the mark; any exception is False
  mint ............................ repeat, a folder takes a number, case, O_EXCL, the 100/101 limit, empty, project_keys, cleanup
  the main key .................... `LOCAL-1`, `PROJ-9` in its text, no MR: collect (no client) -> review --record -> source_inputs
  the inventory ................... no /browse/ row, story_state sees the key, one task source, text_source survives refresh
  peek / collect other relations .. exit 3, the text file named
  record-source ................... every edge, then the bundle (B1)
  get / freshness ................. the file, never the tracker (a client stub that fails when called)
  get --output .................... the key gate, its door, an old story passes
  external_writes ................. a local key is never addressed
  forms ........................... LOCAL-1 under jira, github, file+key_pattern (case_forms reads story_pattern)
Runnable on its own: `python -B scripts/tests/test_local_keys.py`."""
import contextlib
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, temp_project, use_project  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import adapter_forms as AF  # noqa: E402
import case_forms as CF  # noqa: E402
import local_keys as LK  # noqa: E402
import source_inventory as SI  # noqa: E402
import ticket_adapter as TA  # noqa: E402

GITHUB = {"adapters": {"ticket": {"name": "github"}}}
TEXT = "# Add to cart\n\nA reader adds a book to the cart. See PROJ-9 for the price rules.\n"


def cli(root: Path, *args) -> SimpleNamespace:
    """ticket_adapter.main() in this process, as the verb is called."""
    use_project(root)
    out, err = io.StringIO(), io.StringIO()
    saved, code = sys.argv, 0
    sys.argv = ["ticket_adapter.py", *[str(a) for a in args]]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = TA.main()
    except SystemExit as exc:
        code = 0 if exc.code is None else (exc.code if isinstance(exc.code, int) else 1)
    finally:
        sys.argv = saved
    return SimpleNamespace(code=code if isinstance(code, int) else 0, out=out.getvalue(), err=err.getvalue())


def words(root: Path, text: str, name: str = "words.txt") -> str:
    path = root / name
    path.write_bytes(text.encode("utf-8"))
    return str(path)


def project(prefix: str = "qa-local-keys-") -> Path:
    root = temp_project(prefix)
    use_project(root)
    return root


def text_file(root: Path, key: str, text: str = TEXT) -> Path:
    path = root / "qa-factory" / "local-tickets" / f"{key}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def mark_snapshot(root: Path, key: str, mark) -> None:
    work = root / "qa-factory" / "artifacts" / key / "work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "ticket-snapshot.json").write_text(json.dumps({"key": key, "provenance": {"local_key": mark}}), encoding="utf-8")


def work_of(root: Path, key: str) -> Path:
    path = root / "qa-factory" / "artifacts" / key / "work"
    path.mkdir(parents=True, exist_ok=True)
    return path


# --- is_local ------------------------------------------------------------------------------------------------------

def is_local_battery() -> None:
    root = project()
    try:
        text_file(root, "LOCAL-1")
        mark_snapshot(root, "LOCAL-2", True)
        mark_snapshot(root, "LOCAL-3", "yes")
        mark_snapshot(root, "PROJ-1", True)
        broken = work_of(root, "LOCAL-4")
        (broken / "ticket-snapshot.json").write_text("{not json", encoding="utf-8")
        for value, want, why in (
                ("LOCAL-1", True, "the file is there"),
                ("LOCAL-2", True, "the mark is true and no file (a lost text file keeps the story local)"),
                ("LOCAL-3", False, "the mark is the word yes, not true"),
                ("PROJ-1", False, "a tracker key with the mark true"),
                ("LOCAL-4", False, "a broken snapshot and no file"),
                ("LOCAL-5", False, "no file and no mark"),
                ("LOCAL-", False, "no number"),
                ("LOCAL-1 ", False, "a trailing blank"),
                ("LOCAL-1\n", False, "a trailing newline"),
                ("local-1", False, "lower case: fullmatch, not a case-blind file system"),
                ("../../README", False, "a path"),
                ("LOCAL-1/../x", False, "a path under a real key"),
                ("", False, "empty"), (None, False, "None"), (7, False, "a number")):
            check_eq(f"is_local({value!r}): {why}", LK.is_local(value, root), want)
        # a case-blind file system finds `local-6.md` for `LOCAL-6`: the exact name from the listing decides
        text_file(root, "local-6")
        check_eq("is_local: `LOCAL-6` with only `local-6.md` on disk is False on every file system", LK.is_local("LOCAL-6", root), False)
        check_eq("ticket_path: a key that is no local key builds no path", [
            _raises(lambda: LK.ticket_path("../../README", root)), _raises(lambda: LK.ticket_path("PROJ-1", root))], [True, True])
        check_eq("ticket_path of a local key", LK.ticket_path("LOCAL-1", root), (root / "qa-factory" / "local-tickets" / "LOCAL-1.md").resolve())
        # any exception is False (AR-28): the project root is a file, so every listing and read fails
        check_eq("is_local: a root that raises is False", LK.is_local("LOCAL-1", root / "qa-factory" / "config.json"), False)
        # old world: a table with no `local` row recognises nothing
        check_eq("is_local: no table row, no local key", _with_table_without_local(lambda: LK.is_local("LOCAL-1", root)), False)
    finally:
        cleanup(root)


def _raises(call) -> bool:
    try:
        call()
    except ValueError:
        return True
    return False


def _with_table_without_local(call):
    table = AF.load_table()
    old = AF._TABLE_CACHE
    try:
        object.__setattr__(table, "local", None)
        return call()
    finally:
        object.__setattr__(table, "local", {"key": "LOCAL-\\d+", "example": "LOCAL-1"})
        AF._TABLE_CACHE = old


# --- mint ----------------------------------------------------------------------------------------------------------

def mint_battery() -> None:
    root = project()
    try:
        key1, rel1 = LK.mint(TEXT, {}, root)
        key2, _ = LK.mint("second", {}, root)
        check_eq("mint: the first key and its relative path", (key1, rel1), ("LOCAL-1", "qa-factory/local-tickets/LOCAL-1.md"))
        check_eq("mint: a second call is another number", key2, "LOCAL-2")
        check_eq("mint: the text is stored byte for byte", (root / rel1).read_bytes(), TEXT.encode("utf-8"))
        crlf = "a\r\nb\r\n"
        key3, rel3 = LK.mint(crlf, {}, root)
        check_eq("mint: line breaks are not translated", (root / rel3).read_bytes(), crlf.encode("utf-8"))
        # a story folder takes a number, with or without pipeline.json; so does superseded/, any case
        (root / "qa-factory" / "artifacts" / "LOCAL-9").mkdir(parents=True)
        check_eq("mint: a folder without pipeline.json takes its number", LK.mint("x", {}, root)[0], "LOCAL-10")
        (root / "qa-factory" / "artifacts" / "superseded" / "local-12").mkdir(parents=True)
        check_eq("mint: superseded/ and the case of a folder name count", LK.mint("x", {}, root)[0], "LOCAL-13")
        # a `file` tracker's folder
        tickets = root / "tickets"
        tickets.mkdir()
        (tickets / "LOCAL-20.md").write_text("x", encoding="utf-8")
        cfg = {"adapters": {"ticket": {"name": "file", "path": "tickets"}}}
        check_eq("mint: the folder of a `file` tracker counts", LK.mint("x", cfg, root)[0], "LOCAL-21")
        # empty text
        before = sorted(p.name for p in (root / "qa-factory" / "local-tickets").iterdir())
        for empty in ("", "   \n\t", None):
            exc = _mint_refusal(empty, {}, root)
            check_eq(f"mint: {empty!r} is refused with exit 2", exc and exc.code, 2)
            check_in(f"mint: {empty!r}: the sentence", "the local key is given with the story's text; none was given", str(exc))
        check_eq("mint: and no file was made", sorted(p.name for p in (root / "qa-factory" / "local-tickets").iterdir()), before)
        # project_keys
        exc = _mint_refusal("x", {"adapters": {"ticket": {"project_keys": ["proj", "local"]}}}, root)
        check_eq("mint: project_keys with the prefix (any case) is exit 2", exc and exc.code, 2)
        check_in("mint: ... and names the door", "create a ticket there and start the story with its key and --ticket-file <your text>", str(exc))
        check_eq("mint: project_keys LOCALX passes", LK.mint("x", {"adapters": {"ticket": {"project_keys": ["LOCALX"]}}}, root)[0][:6], "LOCAL-")
        check_eq("mint: project_keys that is not a list is not checked", LK.mint("x", {"adapters": {"ticket": {"project_keys": "LOCAL"}}}, root)[0][:6], "LOCAL-")
    finally:
        cleanup(root)


def _mint_refusal(text, cfg, root):
    try:
        LK.mint(text, cfg, root)
    except LK.MintRefused as exc:
        return exc
    return None


def mint_race_and_limit() -> None:
    root = project()
    try:
        folder = root / "qa-factory" / "local-tickets"
        folder.mkdir(parents=True)
        real_taken = LK._taken
        # O_EXCL: the scan says 0 (it lost a race), the file of LOCAL-1 is there: the next number is given, the text kept
        (folder / "LOCAL-1.md").write_text("somebody else's", encoding="utf-8")
        LK._taken = lambda *a: 0
        try:
            key, _ = LK.mint("mine", {}, root)
            check_eq("mint race: a busy number moves to the next, never overwrites", key, "LOCAL-2")
            check_eq("mint race: the other session's text is untouched", (folder / "LOCAL-1.md").read_text(encoding="utf-8"), "somebody else's")
            # the limit: AT it (100 busy numbers after the first, the 100th free) and BEYOND it
            for number in range(3, 3 + LK.MINT_ATTEMPTS - 1):
                (folder / f"LOCAL-{number}.md").write_text("x", encoding="utf-8")
            LK._taken = lambda *a: 2
            key, _ = LK.mint("at the limit", {}, root)
            check_eq("mint limit: the 100th attempt still gives a key", key, f"LOCAL-{3 + LK.MINT_ATTEMPTS - 1}")
            LK._taken = lambda *a: 2
            exc = _mint_refusal("beyond", {}, root)
            check_eq("mint limit: the 101st is exit 4", exc and exc.code, 4)
            check_in("mint limit: and names the folder", "qa-factory/local-tickets", str(exc))
        finally:
            LK._taken = real_taken
        # an exception after O_EXCL leaves no file and the number is free again
        real_fdopen = os.fdopen

        def broken(*a, **kw):
            raise OSError("disk full")
        os.fdopen = broken
        try:
            try:
                LK.mint("lost", {}, root)
                raised = False
            except OSError:
                raised = True
        finally:
            os.fdopen = real_fdopen
        check_eq("mint: an exception after O_EXCL is raised, not swallowed", raised, True)
    finally:
        cleanup(root)


def mint_cleanup_after_write_error() -> None:
    root = project()
    try:
        folder = root / "qa-factory" / "local-tickets"
        folder.mkdir(parents=True)

        class Failing:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def write(self, data):
                raise OSError("disk full")
        real = os.fdopen

        def fake(handle, mode):
            os.close(handle)
            return Failing()
        os.fdopen = fake
        try:
            try:
                LK.mint("lost", {}, root)
            except OSError:
                pass
        finally:
            os.fdopen = real
        check_eq("mint: a write that fails after O_EXCL leaves no file", sorted(p.name for p in folder.iterdir()), [])
        check_eq("mint: and the number is free again", LK.mint("again", {}, root)[0], "LOCAL-1")
    finally:
        cleanup(root)


def local_key_verb() -> None:
    root = project()
    try:
        got = cli(root, "local-key", "--words-file", words(root, TEXT), "--json")
        check_eq("local-key: exit 0 and one JSON object", (got.code, json.loads(got.out)),
                 (0, {"key": "LOCAL-1", "ticket_file": "qa-factory/local-tickets/LOCAL-1.md"}))
        check_not_in("local-key: the path is relative (AR-4)", str(root), got.out)
        got = cli(root, "local-key", "--words-file", words(root, "  \n"))
        check_eq("local-key: a blank words file is exit 2 (person_words names the file)", (got.code, "is empty" in got.err), (2, True))
        got = cli(root, "local-key")
        check_eq("local-key: no words at all is exit 2 with the sentence", (got.code, "none was given" in got.err), (2, True))
        check_eq("local-key: and no second key was made", sorted(p.name for p in (root / "qa-factory" / "local-tickets").iterdir()), ["LOCAL-1.md"])
    finally:
        cleanup(root)


# --- the main key ----------------------------------------------------------------------------------------------------

class NoTracker:
    """Every road to a tracker raises: a local story must never reach one."""
    def __init__(self):
        self.calls = []

    def __call__(self, *a, **kw):
        self.calls.append(a)
        raise AssertionError("a tracker was asked for a local story")


def stub_tracker():
    stub = NoTracker()
    saved = {name: getattr(TA, name) for name in ("traced_client", "get_ticket", "client_from_config", "require_direct_read")}
    for name in saved:
        setattr(TA, name, stub)
    return stub, saved


def restore_tracker(saved) -> None:
    for name, value in saved.items():
        setattr(TA, name, value)


def main_key() -> None:
    root = project()
    stub, saved = stub_tracker()
    try:
        key, rel = LK.mint(TEXT, {}, root)
        work = work_of(root, key)
        inventory = work / "source-inventory.json"
        # the S0 snapshot, as `get --output` writes it
        got = cli(root, "get", key, "--output", work / "ticket-snapshot.json")
        check_eq("main key: get --output on a local key reads the file, exit 0", (got.code, stub.calls), (0, []))
        snapshot = json.loads((work / "ticket-snapshot.json").read_text(encoding="utf-8"))
        check_eq("main key: the snapshot carries the mark (one writer)", snapshot["provenance"].get("local_key"), True)
        got = cli(root, "collect", key, "--output", inventory, "--relation", "task", "--summary")
        check_eq("main key: collect --relation task with no client: exit 0", (got.code, stub.calls), (0, []))
        data = json.loads(inventory.read_text(encoding="utf-8"))
        item = data["sources"][0]
        check_eq("main key: ONE source, the task, read, text_source, no mention", (len(data["sources"]), item["relation"], item["status"],
                 item.get("text_source"), item["mentioned_ticket_keys"]), (1, "task", "read", True, []))
        check_not_in("main key: no /browse/ row in the inventory (PROJ-9 in the text is not a source)", "/browse/", inventory.read_text(encoding="utf-8"))
        check_eq("main key: the source is named by the key, the id from the text kind", (item["canonical_ref"], item["source_id"] == SI.stable_source_id("text", key)), (key, True))
        check_eq("main key: the snapshot file lies where the inventory says and the hash is its", SI.verify_inventory_files(work.parent, data)["valid"], True)
        check_eq("main key: the receipt is stamped by the code", item["inspection_status"], "read")
        check_eq("main key: validate_inventory finds nothing", SI.validate_inventory(data), [])
        got = cli(root, "review", "--output", inventory, "--record", "--words-file", words(root, "go on"))
        check_eq("main key: review --record needs no tracker", (got.code, stub.calls), (0, []))
        got = cli(root, "review", "--output", inventory, "--json")
        check_eq("main key: review needs no tracker when every source is a text", (got.code, stub.calls), (0, []))
        got = cli(root, "refresh", "--output", inventory, "--json")
        check_eq("main key: refresh of text sources is an empty result, exit 0", (got.code, json.loads(got.out), stub.calls), (0, [], []))
        after = json.loads(inventory.read_text(encoding="utf-8"))["sources"][0]
        check_eq("main key: refresh did not touch the text source", (after["status"], after["revision"]), ("read", item["revision"]))
        summary = SI.completeness(json.loads(inventory.read_text(encoding="utf-8")))
        check_eq("main key: gate_blocked is false", summary["gate_blocked"], False)
        # the controller: source_inputs does not raise
        from controller import Controller
        story = root / "qa-factory" / "artifacts" / key
        controller = Controller(story)
        controller.apply("initialize", {"scope": ["TC-1"], "source_revision": "src", "known_paths": {"root": str(story)},
                                        "idempotency_key": "init"})
        got_inputs = controller.source_inputs()
        check_eq("main key: Controller.source_inputs does not raise and does not block", got_inputs["source_completeness"]["gate_blocked"], False)
        # the judge's story_state sees the key (the snapshot is a JSON object of the ticket's shape)
        import judge_sources
        state = judge_sources.story_state(work, json.loads(inventory.read_text(encoding="utf-8")), key)
        check_eq("main key: judge_sources.story_state sees the key", (state or {}).get("key"), key)
        # a second task source is refused, the first one stands
        other = cli(root, "record-source", "--output", inventory, "--ref", "docs/x.md", "--file", words(root, "y"), "--relation", "task")
        check_eq("main key: record-source never records a task", other.code, 2)
        try:
            SI.record_text_source(inventory, relation="task", ref="OTHER-1", snapshot={"key": "OTHER-1"}, required=True)
            conflict = False
        except ValueError:
            conflict = True
        check_eq("main key: a second task source is a ValueError (conflicting_task_source)", conflict, True)
        try:
            SI.record_text_source(inventory, relation="parentt", ref="docs/y.md", snapshot={}, required=False)
            bad = False
        except ValueError:
            bad = True
        check_eq("main key: a relation outside VALID_RELATIONS is a ValueError", bad, True)
        # peek and every relation but task: exit 3, the text file named
        for args in (("peek", key, "--output", inventory), ("collect", key, "--output", inventory, "--relation", "normative")):
            got = cli(root, *args)
            check_eq(f"main key: {args[0]} {args[-1]} on a local key is exit 3", (got.code, stub.calls), (3, []))
            check_in(f"main key: {args[0]}: names the text file", f"qa-factory/local-tickets/{key}.md", got.err)
        # the same bytes record the same revision
        again = cli(root, "collect", key, "--output", inventory, "--relation", "task")
        check_eq("main key: collect again, same source", (again.code, len(json.loads(inventory.read_text(encoding="utf-8"))["sources"])), (0, 1))
        # marked, no snapshot beside the inventory is impossible; the text file gone and no snapshot: not local, so the tracker road
        # (the stub raises); with the file gone but the snapshot there, collect still records from the snapshot
        (root / "qa-factory" / "local-tickets" / f"{key}.md").unlink()
        gone = cli(root, "collect", key, "--output", inventory, "--relation", "task")
        check_eq("main key: the text file lost, the marked snapshot beside the inventory is still recorded", (gone.code, stub.calls), (0, []))
    finally:
        restore_tracker(saved)
        cleanup(root)


def refresh_with_a_tracker_source() -> None:
    root = project()
    try:
        key, _ = LK.mint(TEXT, {}, root)
        work = work_of(root, key)
        inventory = work / "source-inventory.json"
        cli(root, "get", key, "--output", work / "ticket-snapshot.json")
        cli(root, "collect", key, "--output", inventory, "--relation", "task")
        data = json.loads(inventory.read_text(encoding="utf-8"))
        data["sources"].append({"source_id": "SRC-t", "canonical_ref": "https://j.example/browse/PROJ-9", "relation": "referenced",
                                "relevance": "relevant", "status": "read", "required": True})
        check_eq("only_text_sources: one tracker source among texts is False", SI.only_text_sources(data), False)
        check_eq("only_text_sources: the empty list is False", SI.only_text_sources({"sources": []}), False)
        check_eq("only_text_sources: texts only is True", SI.only_text_sources({"sources": [{"text_source": True}]}), True)
        check_eq("refresh_targets: the text source is left out, the tracker one is in",
                 [s["source_id"] for s in SI.refresh_targets(data)], ["SRC-t"])
        TA.load_config()
        inventory.write_text(json.dumps(data), encoding="utf-8")
        got = cli(root, "refresh", "--output", inventory, "--json")
        check_eq("refresh: with a tracker source the tracker requirement stays (exit 3, no direct read configured)", got.code, 3)
    finally:
        cleanup(root)


# --- record-source -----------------------------------------------------------------------------------------------------

def record_source_edges() -> None:
    root = project()
    try:
        work = work_of(root, "PROJ-1")
        inventory = work / "source-inventory.json"
        doc = root / "page.md"
        doc.write_bytes("# Price rules\n\nA book costs 5.\n".encode("utf-8"))

        def record(*args, ref="docs/price-rules.md", file=None, relation="normative"):
            return cli(root, "record-source", "--output", inventory, "--ref", ref, "--file", file or doc, "--relation", relation, *args)

        got = record("--summary")
        check_eq("record-source: a text is recorded, exit 0", got.code, 0)
        line = json.loads(got.out)
        check_eq("record-source: the summary names the source and the count", (line["record"]["relation"], line["inventory"]["source_count"]), ("normative", 1))
        data = json.loads(inventory.read_text(encoding="utf-8"))
        item = data["sources"][0]
        check_eq("record-source: required false, relevant, text_source, read", (item["required"], item["relevance"], item.get("text_source"), item["status"]),
                 (False, "relevant", True, "read"))
        check_eq("record-source: the revision is sha256:<12>", item["revision"], "sha256:" + item["content_hash"][:12])
        snap = json.loads((work / item["snapshot_ref"]).read_text(encoding="utf-8"))
        check_eq("record-source: the snapshot is a JSON document titled by the last part of the locator",
                 (snap["type"], snap["title"], snap["key"]), ("document", "price-rules.md", "docs/price-rules.md"))
        check_eq("record-source: it is the bytes of ticket_adapter.snapshot_bytes", (work / item["snapshot_ref"]).read_bytes(), TA.snapshot_bytes(snap))
        check_eq("record-source: validate and verify pass", (SI.validate_inventory(data), SI.verify_inventory_files(work.parent, data)["valid"]), ([], True))
        # idempotent
        record()
        check_eq("record-source: same locator, same bytes: the same revision, no new record",
                 (len(json.loads(inventory.read_text(encoding="utf-8"))["sources"]), json.loads(inventory.read_text(encoding="utf-8"))["sources"][0]["revision"]),
                 (1, item["revision"]))
        # other bytes: a new revision, the old one kept
        doc.write_bytes("# Price rules\n\nA book costs 6.\n".encode("utf-8"))
        record()
        new = json.loads(inventory.read_text(encoding="utf-8"))["sources"]
        check_eq("record-source: other bytes are a new revision with prior_revisions", (len(new), new[0]["revision"] != item["revision"],
                 [h["revision"] for h in new[0].get("prior_revisions", [])]), (1, True, [item["revision"]]))
        # FV1-23 A-2: a folder of the project and the files a refusal must not echo
        (root / "docs" / "token=abc123").mkdir(parents=True)
        (root / "docs" / "a.md").write_bytes(b"# A\n")
        (root / "docs" / "token=abc123.md").write_bytes(b"# T\n")
        before = inventory.read_bytes()
        # edges: every one refused, the inventory untouched
        empty = root / "empty.md"
        empty.write_bytes(b"")
        blank = root / "blank.md"
        blank.write_bytes(b" \n\t")
        binary = root / "bin.dat"
        binary.write_bytes(bytes([0xff, 0xfe, 0x00, 0x81]))
        nul = root / "nul.md"
        nul.write_bytes(b"ab\x00cd")
        cases = (
            ("no file", record(file=root / "nope.md"), 2, "nothing to record"),
            ("empty file", record(file=empty), 2, "nothing to record"),
            ("blank file", record(file=blank), 2, "nothing to record"),
            ("not UTF-8", record(file=binary), 3, "is not text: record the gap in your manifest with the reason"),
            ("a NUL byte", record(file=nul), 3, "is not text"),
            ("empty ref", record(ref=" "), 2, "usage"),
            ("absolute ref", record(ref=str(root / "x.md")), 2, "give the locator relative to the project"),
            ("rooted ref", record(ref="/etc/hosts"), 2, "give the locator relative to the project"),
            ("backslash-rooted ref", record(ref="\\\\server\\share"), 2, "give the locator relative to the project"),
            ("drive ref", record(ref="C:\\x\\y.md"), 2, "give the locator relative to the project"),
            ("dotdot ref", record(ref="docs/../../x.md"), 2, "give the locator relative to the project"),
            ("secret in the ref", record(ref="https://w.example/p?token=abc123"), 2, "credential-like"),
            ("password in the URL (F5)", record(ref="https://user:pw0rd9@host.example/x"), 2, "credential-like"),
            ("a drive taken for a scheme (F5)", record(ref="C://Users/dev7/x.md"), 2, "give the locator relative to the project"),
            ("a file: URL names this machine (F5)", record(ref="file:///C:/Users/dev7/x.md"), 2, "give the locator relative to the project"),
            ("FILE: in capitals (F5)", record(ref="FILE:///home/me/x.md"), 2, "give the locator relative to the project"),
            ("a backslash escape docs\\..\\..\\x.md (B-1)", record(ref="docs\\..\\..\\x.md"), 2, "give the locator relative to the project"),
            ("a NUL inside the ref", record(ref="a\0b.md"), 2, "give the locator relative to the project"),
            ("outside the project and every declared repository", record(ref="../elsewhere/a.md"), 2, "resolves outside"),
            ("a credential-like path outside is refused for the credential, never echoed (B-2)",
             record(ref="../elsewhere/token=abc123.md"), 2, "credential-like"),
            ("a credential-like folder name on a folder ref (B-2)", record(ref="docs/token=abc123"), 2, "credential-like"),
            ("a folder ref names the one document the file sits in", record(ref="docs", file=root / "docs" / "a.md"), 2,
             "is a folder; one record per document: --ref `docs/a.md`"),
            ("a folder ref with a credential-like file name keeps a placeholder (B-2)",
             record(ref="docs", file=root / "docs" / "token=abc123.md"), 2, "--ref `docs/<file name>`"),
            ("a folder ref with a file from elsewhere", record(ref="docs/"), 2, "is a folder"),
            ("the project itself is a folder", record(ref="."), 2, "is a folder"),
            ("relation task", record(relation="task"), 2, "one task source"),
            ("no relation", cli(root, "record-source", "--output", inventory, "--ref", "a.md", "--file", doc), 2, "usage"),
        )
        for label, got, code, needle in cases:
            check_eq(f"record-source edge {label}: exit", got.code, code)
            check_in(f"record-source edge {label}: says what was expected", needle, got.err)
        check_not_in("record-source edge: the secret value is not printed", "abc123", "".join(c[1].err + c[1].out for c in cases))
        check_not_in("record-source edge: the URL password is not printed", "pw0rd9", "".join(c[1].err + c[1].out for c in cases))
        check_eq("record-source edges: the inventory is untouched", inventory.read_bytes(), before)
        # a URL with a scheme is a locator; a big file has no limit
        got = record(ref="https://wiki.example/pages/Price+rules")
        check_eq("record-source: a URL locator is accepted", got.code, 0)
        check_eq("record-source: a URL with no credential and a relative path still pass (F5)",
                 (record(ref="https://host.example/x").code, record(ref="docs/ok.md").code), (0, 0))
        big = root / "big.md"
        big.write_bytes(("line of text\n" * 200000).encode("utf-8"))
        check_eq("record-source: a large file has no limit", record(ref="docs/big.md", file=big).code, 0)
        # B1: the bundle carries the source
        import context_bundle
        manifest = {"ticket": "PROJ-1", "implementations": [{"repo_id": "app", "source_sha": "abc", "diff_path": "change.diff"}],
                    "changed_areas": ["src"], "facts": [], "known_paths": ["src/a.py"]}
        story = work.parent
        (story / "change.diff").write_text("diff --git a/x b/x\n+x\n", encoding="utf-8")
        try:
            bundle = context_bundle.build(manifest, story)
            rows = [r for r in bundle.get("requirement_sources", []) if r["ref"] == "docs/price-rules.md"]
            check_eq("B1: context_bundle.requirement_sources carries the recorded text, evidence_ref on its snapshot",
                     (len(rows), rows and rows[0]["evidence_ref"].startswith("work/sources/")), (1, True))
        except Exception as exc:  # noqa: BLE001
            check("B1: context_bundle.build over the recorded inventory", False, f"{type(exc).__name__}: {exc}")
        import branch_accounting
        try:
            branch_accounting.collect(story)
            check("B1: branch_accounting.collect does not fail on a text source", True)
        except Exception as exc:  # noqa: BLE001
            check("B1: branch_accounting.collect does not fail on a text source", False, f"{type(exc).__name__}: {exc}")
    finally:
        cleanup(root)


def _set_config(root: Path, **keys) -> dict:
    """Write `keys` into the project's config.json (the marker the tests share) and return the config as written."""
    path = root / "qa-factory" / "config.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg.update(keys)
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return cfg


def record_source_declared_roots() -> None:
    """FV1-23 A-2 (record_source_edges, the accept rows): a ref that resolves inside a declared `code_repos` root is a source
    under its normal ref. Mutation: restore the `_safe_rel` test in `_record_source`, or let `declared_place` take a malformed
    code_repos entry through (a traceback)."""
    root = project()
    sib = root.parent / (root.name + "-sib")
    try:
        (sib / "docs").mkdir(parents=True)
        (sib / "docs" / "A.md").write_bytes(b"# A\n")
        (sib / "docs" / "B.md").write_bytes(b"# B\n")
        _set_config(root, code_repos=[{"path": 123}, {"path": ""}, {"name": "sib", "path": "../" + sib.name}])
        work = work_of(root, "PROJ-1")
        inventory = work / "source-inventory.json"

        def record(ref, file):
            return cli(root, "record-source", "--output", inventory, "--ref", ref, "--file", file, "--relation", "normative")

        def refs():
            return sorted(s["canonical_ref"] for s in json.loads(inventory.read_text(encoding="utf-8"))["sources"]) if inventory.exists() else []

        prefix = f"../{sib.name}/docs/"
        got = record(prefix + "A.md", sib / "docs" / "A.md")
        check_eq("declared root: a dotdot ref into a code_repos checkout is recorded (a malformed entry before it is skipped)", (got.code, refs()), (0, [prefix + "A.md"]))
        got = record(prefix.replace("/", "\\", 1) + "A.md", sib / "docs" / "A.md")
        check_eq("declared root: the mixed-slash spelling is the same record", (got.code, refs()), (0, [prefix + "A.md"]))
        got = record(prefix + "B.md", sib / "docs" / "B.md")
        check_eq("declared root: two documents of one folder are two records (the second defect of F-1)", (got.code, refs()),
                 (0, [prefix + "A.md", prefix + "B.md"]))
        got = record(f"../{sib.name}/docs", sib / "docs" / "A.md")
        check_eq("declared root: the folder ref is refused and names the document", (got.code, "--ref `" + prefix + "A.md`" in got.err), (2, True))
        for label, ref in (("another folder next to the project", "../elsewhere/x.md"), ("a climb out of the checkout", f"../{sib.name}/../x.md"),
                           ("a backslash climb", "docs\\..\\..\\x.md")):
            got = record(ref, sib / "docs" / "A.md")
            check_eq(f"declared root: {label} is refused, no traceback", (got.code, "Traceback" in got.err), (2, False))
        check_eq("declared root: the refused refs left the inventory as it was", len(refs()), 2)
        # no marker above --output: nothing to check a `..` against (FR-59); a ref without one keeps today's rule
        loose = harness_dir()
        try:
            out = loose / "work" / "source-inventory.json"
            out.parent.mkdir(parents=True)
            doc = loose / "t.md"
            doc.write_bytes(b"# t\n")
            got = cli(root, "record-source", "--output", out, "--ref", "../x.md", "--file", doc, "--relation", "normative")
            check_eq("no project: a dotdot ref is refused and says why", (got.code, "no qa-factory/config.json above --output" in got.err), (2, True))
            got = cli(root, "record-source", "--output", out, "--ref", "docs/ok.md", "--file", doc, "--relation", "normative")
            check_eq("no project: a ref without a dotdot is recorded as before", got.code, 0)
        finally:
            cleanup(loose)
    finally:
        cleanup(sib)
        cleanup(root)


def harness_dir() -> Path:
    from harness import temp_dir
    return temp_dir("qa-local-keys-loose-")


DOC_HEAD = ("Documents under {} (record each one you read on its own: record-source --ref <the path as listed> --relation normative; "
            "a first look at each, charter: the walk of references):")


def document_places() -> None:
    """FV1-23 A-2: `source_inventory.document_place_lines`, one table (the lines a scout is told about the documents of a folder
    row). One tool, one run: the volume is the limits (25/26, 40/41, depth 3, 2000/2001, 200/201) and the files that must never be
    listed (NUL, UTF-16, empty, credential-like, left out), each with its own id. Mutation: drop the predicate (a listed path
    `record-source` refuses), a cap, or a count line."""
    root = project()
    sib = root.parent / (root.name + "-sib")
    try:
        (sib / "docs").mkdir(parents=True)
        task = work_of(root, "PROJ-1").parent
        repos = [{"name": "sib", "path": "../" + sib.name}]

        def put(rel, data=b"alpha\n", base=root):
            path = base / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return path

        def listing(*locators, kind="file", status="verified", **config):
            rows = [{"source_id": f"s{n}", "kind": kind, "locator": locator, "status": status} for n, locator in enumerate(locators)]
            return SI.document_place_lines(_set_config(root, requirements_sources=rows, code_repos=config.pop("repos", []), **config), task)

        def paths(lines):
            return [line[2:].split(" (")[0] for line in lines if line.startswith("- ") and " (" in line and " B)" in line]

        put("docs/a.md"), put("docs/b.md", b"bravo bravo\n"), put("docs/c.md")
        put("docs/sub/d.md")
        got = listing("docs")
        check_eq("places: a folder with files lists them in order, one heading, sizes in B",
                 got, [DOC_HEAD.format("docs"), "- docs/a.md (6 B)", "- docs/b.md (12 B)", "- docs/c.md (6 B)", "- docs/sub/d.md (6 B)"])
        check_eq("places: the same listing for kind repository", listing("docs", kind="repository"), got)
        # JOIN: what is listed is what record-source accepts
        inventory = work_of(root, "PROJ-1") / "source-inventory.json"
        codes = [cli(root, "record-source", "--output", inventory, "--ref", ref, "--file", root / ref, "--relation", "normative").code for ref in paths(got)]
        check_eq("places JOIN: every listed path is accepted by record-source", codes, [0, 0, 0, 0])
        put("docs/deep.md", b"x\n" * 40)
        check_eq("places: a file over the read cap says so", [l for l in listing("docs", read={"max_bytes": 50}) if "deep.md" in l or "a.md" in l],
                 ["- docs/a.md (6 B)", "- docs/deep.md (80 B) over the read cap: read it with offset/limit"])
        _set_config(root, read={})
        # limits
        for n in (25, 26):
            for i in range(n):
                put(f"d{n}/f{i:02d}.md")
        got = listing("d25")
        check_eq("places AT 25 files: 25 listed, no remainder line", (len(paths(got)), [l for l in got if "more" in l]), (25, []))
        got = listing("d26")
        check_eq("places BEYOND 25 files: 25 listed and 'and 1 more' with its place",
                 (len(paths(got)), [l for l in got if "more" in l]), (25, ["- and 1 more under d26: list them yourself"]))
        for i in range(15):
            put(f"d15/f{i:02d}.md")
        for i in range(16):
            put(f"d16/f{i:02d}.md")
        put("last/z.md")
        got = listing("d25", "d15", "last")
        check_eq("places AT the total 40: 40 listed, the next folder row says the list is full",
                 (len(paths(got)), got[-1]), (40, "s2: last: not listed (the list is full); search it yourself"))
        got = listing("d25", "d16", "last")
        check_eq("places BEYOND the total 40: the row holding the 40th counts its remainder, the next row is full",
                 (len(paths(got)), [l for l in got if "more" in l], got[-1]),
                 (40, ["- and 1 more under d16: list them yourself"], "s2: last: not listed (the list is full); search it yourself"))
        # depth: a file directly in the folder is depth 1; a folder at depth 3 is not entered
        for rel in ("dp/f1.md", "dp/a/f2.md", "dp/a/b/f3.md", "dp/a/b/c/f4.md"):
            put(rel)
        got = listing("dp")
        check_eq("places depth: the file at depth 3 is listed, the folder at depth 3 is counted not walked",
                 (paths(got), [l for l in got if "deeper" in l]),
                 (["dp/a/b/f3.md", "dp/a/f2.md", "dp/f1.md"], ["- 1 folder(s) deeper than 3 levels not walked under dp: list them yourself"]))
        # entries: the Nth examined, the (N+1)th stops the walk. The shipped N is 2000; the rows run the same code on N = 20 (the 10 s
        # budget of this file: 2001 files cost 3 s), and one row holds the shipped constant
        check_eq("places: the shipped entries cap is 2000", SI.DOC_ENTRIES_SCANNED, 2000)
        shipped, SI.DOC_ENTRIES_SCANNED = SI.DOC_ENTRIES_SCANNED, 20
        try:
            for n, name in ((20, "e20"), (21, "e21")):
                for i in range(n):
                    put(f"{name}/{i:04d}.md", b"")
            check_eq("places AT the entries cap: all examined, no stop line",
                     listing("e20"), ["s0: no text file under e20", "- 20 file(s) not listed: not text or empty"])
            check_eq("places BEYOND the entries cap: the walk stops and says so with its place",
                     listing("e21")[-1], "- the walk stopped after 20 entries under e21: list the rest yourself")
        finally:
            SI.DOC_ENTRIES_SCANNED = shipped
        put("dots/.hidden/x.md"), put("dots/.env"), put("dots/ok.md")
        check_eq("places: dot entries are skipped and not counted", listing("dots"), [DOC_HEAD.format("dots"), "- dots/ok.md (6 B)"])
        # files that are not text, credential-like names, long names, left-out paths
        put("bad/nul.md", b"ab\x00cd"), put("bad/u16.md", "hi".encode("utf-16")), put("bad/empty.md", b""), put("bad/blank.md", b" \n\t")
        put("bad/image.png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"), put("bad/good.md")
        check_eq("places: NUL, UTF-16, empty, whitespace-only and an image are counted, never listed",
                 listing("bad"), [DOC_HEAD.format("bad"), "- bad/good.md (6 B)", "- 5 file(s) not listed: not text or empty"])
        put("onlyimg/p.png", b"\x89PNG\x00")
        os.makedirs(root / "nothing")
        check_eq("places: images only", listing("onlyimg"), ["s0: no text file under onlyimg", "- 1 file(s) not listed: not text or empty"])
        check_eq("places: an empty folder", listing("nothing"), ["s0: no text file under nothing"])
        put("cred/token=abc123.md"), put("cred/ok.md")
        got = listing("cred")
        check_eq("places: a credential-like file name is withheld, never printed",
                 (got, "abc123" in "".join(got)), ([DOC_HEAD.format("cred"), "- cred/ok.md (6 B)", "- 1 file(s) withheld: a credential-like name"], False))
        deep_name = "lg/" + "x" * 193
        try:
            put(deep_name + "1.md"), put("lg/" + "y" * 193 + "11.md"), put("lg/" + "z" * 193 + "11.mdx")
            got = listing("lg")
            check_eq("places AT 200 and BEYOND 200 characters of a path: listed / counted 'name too long'",
                     (len(paths(got)), [l for l in got if "too long" in l]), (1, ["- 2 file(s) not listed: name too long"]))
        except OSError as exc:
            print(f"skipped: places 200/201 character paths - the OS refused the file name ({type(exc).__name__})")
        # a left-out path: a HAND-MADE `as_written` entry (no exclusion kind names a path today)
        record = task / "work" / "source-exclusions.json"
        record.write_text(json.dumps({"schema_version": 1, "exclusions": [
            {"id": "X-1", "as_written": "docs/b.md", "target": {"kind": "ref", "branch": "none"}, "reason": "stale"}]}), encoding="utf-8")
        got = listing("docs")
        check_eq("places: a path the person's word names is counted left out, not listed (hand-made as_written entry)",
                 ("docs/b.md" in "".join(got), got[-1]), (False, "- 1 file(s) left out by the person's word"))
        record.write_text("not json", encoding="utf-8")
        check_eq("places: an unreadable exclusion record gives no listing (left_out_lines refuses next)", listing("docs"), [])
        record.unlink()
        # rows that are not a folder to list
        put("f.md")
        for label, locator, kw, expected in (
                ("a file locator adds nothing", "docs/a.md", {}, []),
                ("a missing path", "nope", {}, ["s0: nope is not on disk here: a gap with that reason, not a question"]),
                ("a climb out of the project", "../../..", {}, ["s0: ../../.. is outside the project's repositories: not listed"]),
                ("an absolute locator", str(root), {}, [f"s0: {str(root)[:200]} is outside the project's repositories: not listed"]),
                ("the project itself is a whole repository", ".", {}, []),
                ("a code_repos root is a whole repository", "../" + sib.name, {"repos": repos}, []),
                ("a folder of a code_repos checkout is listed", "../" + sib.name + "/docs", {"repos": repos}, ["s0: no text file under ../" + sib.name + "/docs"]),
                ("a status that is not verified", "docs", {"status": "unknown"}, []),
                ("a kind routed to the role", "docs", {"kind": "wiki"}, []),
                ("a kind outside the table", "docs", {"kind": "mystery"}, []),
                ("a credential locator", "docs?token=abc123", {}, []),
        ):
            check_eq(f"places: {label}", listing(locator, **kw), expected)
        check_eq("places: no requirements_sources", [SI.document_place_lines(cfg, task) for cfg in ({}, {"requirements_sources": []}, {"requirements_sources": "x"}, None)], [[], [], [], []])
        check_eq("places: a row that is not a dict is skipped", SI.document_place_lines({"requirements_sources": ["x", 3, None]}, task), [])
        check_eq("places: no project above the task root gives nothing", SI.document_place_lines(_set_config(root, requirements_sources=[
            {"kind": "file", "locator": "docs", "status": "verified"}]), sib), [])
    finally:
        cleanup(sib)
        cleanup(root)


def linked_documents_rows() -> None:
    """FV1-23 A-3: `ticket_light.path_candidates`, `source_inventory.linked_documents` and the stderr listing and
    `linked_document` rows of `record-source`. One table of texts, one outcome per row; the volume is the adversarial list of
    the spec (every row a case of the input from outside) and the join rows with the reader and the settler. Mutation: keep a
    path outside the roots, double an origin, print on stdout, let the listing change the exit code."""
    import brief_pack
    import ticket_light as TL
    # -- path_candidates: the grammar, characters only
    long200, long201 = "a" * 197 + ".md", "a" * 198 + ".md"
    for label, text, expected in (
            ("a link, a bare name in backticks, a percent-encoded name with a query", "[x](docs/a.md#part) and `README.md`, docs/My%20Doc.md?x=1.",
             ["docs/a.md", "README.md", "docs/My Doc.md"]),
            ("a URL, mailto, a drive, a home path and a UNC share are no relative paths", "https://h.example/d/a.md mailto:a@b.example C:\\x\\y.md ~/x.md \\\\srv\\sh\\x.md file:///x/y.md", []),
            ("a rooted path stays, the caller decides its base", "see /docs/a.md.", ["/docs/a.md"]),
            ("a word with neither a slash nor a dot is no path", "cart merge README", []),
            ("200 characters stay, 201 go", f"{long200} {long201}", [long200]),
            ("a repeat is one candidate, first occurrence order", "b.md a.md b.md", ["b.md", "a.md"]),
            ("a NUL after decoding is kept for the predicate to refuse", "a%00.md", ["a\x00.md"]),
            ("not text", None, []),
    ):
        check_eq(f"path_candidates: {label}", TL.path_candidates(text), expected)
    # -- linked_documents through record-source
    def scenario(repos=None, refs=True):
        root = project()
        sib = root.parent / (root.name + "-sib")
        (sib / "docs").mkdir(parents=True)
        _set_config(root, code_repos=[{"name": "sib", "path": "../" + sib.name}] if repos is None else repos)
        work = work_of(root, "PROJ-1")
        if refs:
            (work / "ticket-references.json").write_text(json.dumps({"rows": [], "scanned": ["ticket"], "written_by": ["S0"]}), encoding="utf-8")
        return root, sib, work

    def put(base, rel, data=b"alpha\n"):
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def rec(root, work, ref, text, *extra, on_disk=True):
        if on_disk and not (root / ref).exists() and "://" not in ref:      # the ref names the document the text was read from
            put(root, ref, text.encode("utf-8"))
        return cli(root, "record-source", "--output", work / "source-inventory.json", "--ref", ref, "--file", words(root, text, "t.txt"),
                   "--relation", "normative", *extra)

    def rows_of(work):
        return json.loads((work / "ticket-references.json").read_text(encoding="utf-8"))["rows"]

    def listed(err):
        return [line[2:].split(" (")[0] for line in err.splitlines() if line.startswith("- ") and " B)" in line]

    root, sib, work = scenario()
    try:
        for rel in ("docs/a.md", "docs/My Doc.md", "NOTES.md", "docs/token=abc123.md"):
            put(root, rel)
        put(root, "img/p.png", b"\x89PNG\x00\x01")
        put(sib, "docs/A.md")
        (root / "docs" / "sub").mkdir()
        text = ("# R\n[x](../../../etc/passwd) C:\\x\\y.md ~/x.md file:///x/y.md https://h.example/docs/b.md\n"
                "[a](docs/a.md#part) [m](docs/My%20Doc.md) docs/a.md?x=1 docs/ README.md img/p.png docs/token=abc123.md a%00.md\n"
                f"{'x' * 198}.md `NOTES.md` [s](../{sib.name}/docs/A.md)\n")
        got = rec(root, work, "README.md", text, "--summary")
        check_eq("links: the exit code and the stdout shape are the record's own (one JSON line)", (got.code, len(got.out.splitlines()), json.loads(got.out)["record"]["relation"]), (0, 1, "normative"))
        check_eq("links: only existing, contained, regular, non-empty text files, none twice, never the text itself",
                 listed(got.err), ["docs/a.md", "docs/My Doc.md", "NOTES.md", f"../{sib.name}/docs/A.md"])
        check_in("links: the heading points at the charter", "Linked from README.md, inside the declared repositories (a first look at each, charter: the walk of references;", got.err)
        check_eq("links: a credential-like name, a NUL, an escape, a 201 character name and an image are not printed",
                 [w for w in ("abc123", "passwd", "p.png", "\x00") if w in got.err], [])
        check_eq("links: the stdout carries no listing", "Linked" in got.out, False)
        check_eq("links: the rows are the listed paths, origin mention:document:<ref>, not read",
                 sorted((r["ref"], r["kind"], r["origins"], r["status"]) for r in rows_of(work)),
                 sorted((p, "linked_document", ["mention:document:README.md"], SI.LINKED_DOCUMENT_STATUS)
                        for p in ("docs/a.md", "docs/My Doc.md", "NOTES.md", f"../{sib.name}/docs/A.md")))
        before = rows_of(work)
        rec(root, work, "README.md", text)
        check_eq("links: a text recorded twice is one row per path, origins not doubled", rows_of(work), before)
        check_eq("links JOIN reader: brief_pack.reference_gap_lines shows an unread linked document",
                 [l for l in brief_pack.reference_gap_lines(work.parent) if "docs/a.md" in l and "linked document" in l] != [], True)
        got = rec(root, work, "docs/a.md", "alpha\n")
        check_eq("links JOIN settler: recording a listed path settles its row, the reader stops showing it",
                 ([r["status"] for r in rows_of(work) if r["ref"] == "docs/a.md"], [l for l in brief_pack.reference_gap_lines(work.parent) if "docs/a.md" in l]),
                 (["fetched"], []))
        check_eq("links: a text with a document already recorded counts it and does not list it", (listed(rec(root, work, "README.md", text).err)[:1], "1 linked document(s) already recorded" in rec(root, work, "README.md", text).err),
                 (["docs/My Doc.md"], True))
        # text refs that list nothing: a key, a URL, a task-relative copy
        for ref in ("PROJ-9", "https://wiki.example/p", "work/raw/copy.md"):
            check_eq(f"links: the text ref {ref} lists nothing", "Linked from" in rec(root, work, ref, "see docs/a.md and NOTES.md", on_disk=False).err, False)
        # no file of references (a story older than S0's file): the lines still print, nothing is written
        (work / "ticket-references.json").unlink()
        check_eq("links TEMPORAL: no references file: the listing prints, no file is born",
                 ("- NOTES.md (6 B)" in rec(root, work, "README2.md", "see NOTES.md").err, (work / "ticket-references.json").exists()), (True, False))
        # a failure while listing never changes the verdict
        real = SI.linked_documents
        SI.linked_documents = lambda *a, **k: 1 / 0
        try:
            got = rec(root, work, "README3.md", "see NOTES.md")
        finally:
            SI.linked_documents = real
        check_eq("links: a failure inside the listing is one stderr line and exit 0", (got.code, "links of README3.md could not be listed (ZeroDivisionError)" in got.err), (0, True))
        # a folder the text names, 25 / 26 kept, 500 / 501 names
        for name, count in (("m25", 25), ("m26", 26)):
            for i in range(count):
                put(root, f"{name}/f{i:02d}.md")
            got = rec(root, work, f"{name}.md", " ".join(f"{name}/f{i:02d}.md" for i in range(count)))
            check_eq(f"links AT/BEYOND 25: {count} kept", (len(listed(got.err)), f"- and {count - 25} more linked from {name}.md: look for them yourself" in got.err), (25, count > 25))
        for count in (500, 501):
            put(root, "n/n000.md"), put(root, f"n/n{count - 1:03d}.md")
            got = rec(root, work, f"t{count}.md", " ".join(f"n/n{i:03d}.md" for i in range(count)))
            check_eq(f"links AT/BEYOND 500 names: {count} (the 501st name is never tried)",
                     (listed(got.err), "more than 500 names in the text: only the first 500 were checked" in got.err),
                     (["n/n000.md", "n/n499.md"], count == 501))
        check_eq("links: a text with no candidate lists nothing", "Linked" in rec(root, work, "plain.md", "# nothing here\n").err, False)
        outside = root.parent / (root.name + "-outside.md")
        outside.write_bytes(b"secret outside\n")
        try:
            os.symlink(outside, root / "docs" / "ln.md")
            check_eq("links: a link to a file that points outside every root is not listed", "ln.md" in rec(root, work, "ln.md.txt", "see docs/ln.md NOTES.md").err, False)
        except OSError:
            print("skipped: links to a symlink pointing outside - the OS refused to make a file link")
        finally:
            outside.unlink()
        # an exclusion record the person wrote (hand-made as_written entry: no kind names a path) keeps a path out; an unreadable one lists nothing
        excl = work / "source-exclusions.json"
        excl.write_text(json.dumps({"schema_version": 1, "exclusions": [{"id": "X-1", "as_written": "NOTES.md", "target": {"kind": "ref", "branch": "none"}, "reason": "old"}]}), encoding="utf-8")
        check_eq("links: a path the person's word names is not listed", "NOTES.md" in rec(root, work, "r4.md", "see NOTES.md docs/a.md").err.split("already")[0], False)
        excl.write_text("not json", encoding="utf-8")
        check_eq("links: an unreadable exclusion record lists nothing", SI.linked_documents(root, _set_config(root), "README.md", text, work.parent)["paths"], [])
        excl.unlink()
        # attachments: the refactor guard (the merge survivor keeps its behaviour)
        client = SimpleNamespace(base_url="https://jira.example", references_context={}, project_keys=[])
        (work / "ticket-references.json").write_text(json.dumps({"rows": [{"kind": "url", "ref": "https://o.example/x", "origins": ["mention:description"], "status": "person"}], "scanned": [], "written_by": []}), encoding="utf-8")
        for _ in range(2):
            SI.append_attachment_references(client, work / "source-inventory.json", "PROJ-1", {}, {"notes.txt": "see https://o.example/x"})
        document = json.loads((work / "ticket-references.json").read_text(encoding="utf-8"))
        check_eq("attachments refactor guard: the origin joins the existing row once, scanned and written_by are marked",
                 ([r["origins"] for r in document["rows"] if r["ref"] == "https://o.example/x"], document["scanned"], document["written_by"]),
                 ([["mention:description", "notes.txt"]], ["attachments"], ["S1"]))
    finally:
        cleanup(sib)
        cleanup(root)
    # -- a document recorded BEFORE the text that links it is born fetched; a rooted link and nested roots
    root, sib, work = scenario(repos=[{"name": "app", "path": "app"}])
    try:
        put(root, "x.md"), put(root, "app/x.md"), put(root, "app/README.md"), put(root, "docs/a.md")
        rec(root, work, "docs/a.md", "alpha\n")
        got = rec(root, work, "app/README.md", "see /x.md and docs/a.md ../docs/a.md")
        check_eq("links: a rooted link resolves against the innermost declared root; a recorded document is counted, not listed",
                 (listed(got.err), "1 linked document(s) already recorded" in got.err), (["app/x.md"], True))
        check_eq("links: the document recorded before is born fetched", sorted((r["ref"], r["status"]) for r in rows_of(work)),
                 [("app/x.md", SI.LINKED_DOCUMENT_STATUS), ("docs/a.md", "fetched")])
    finally:
        cleanup(sib)
        cleanup(root)


def record_source_never_replaces() -> None:
    """F1 (t-551): a text never replaces a record it did not write. Mutation: remove the `same` check in
    `source_inventory.record_text_source`."""
    root = project()
    try:
        key, _ = LK.mint(TEXT, {}, root)
        work = work_of(root, key)
        inventory = work / "source-inventory.json"
        doc = root / "o.txt"
        doc.write_bytes("some text\n".encode("utf-8"))
        cli(root, "get", key, "--output", work / "ticket-snapshot.json")
        check_eq("F1: the task source is collected", cli(root, "collect", key, "--output", inventory, "--relation", "task").code, 0)
        before = inventory.read_bytes()
        got = cli(root, "record-source", "--output", inventory, "--ref", key, "--file", doc, "--relation", "subject")
        check_eq("F1: a text under the task source's locator is refused (exit 2)", got.code, 2)
        check_in("F1: ... saying the source is not replaced and where a gap goes", "already a source of this story", got.err)
        check_eq("F1: ... and the inventory is byte for byte the same", inventory.read_bytes(), before)
        # a required source that is a gap: only accept-gap with the person's words closes it
        data = json.loads(inventory.read_text(encoding="utf-8"))
        data["sources"].append({"source_id": "SRC-gap", "canonical_ref": "https://jira.example/browse/APP-2", "relation": "normative",
                                "relevance": "relevant", "status": "unavailable", "required": True})
        inventory.write_text(json.dumps(data, indent=2), encoding="utf-8")
        before = inventory.read_bytes()
        got = cli(root, "record-source", "--output", inventory, "--ref", "https://jira.example/browse/APP-2", "--file", doc,
                  "--relation", "normative")
        check_eq("F1: a text under a required gap's locator is refused (exit 2)", got.code, 2)
        check_eq("F1: ... and the gap stays open: inventory byte for byte the same", inventory.read_bytes(), before)
        # the own repeat stays legal: same locator, same relation, written by record-source
        rep = ("record-source", "--output", inventory, "--ref", "docs/own.md", "--file", doc, "--relation", "normative")
        check_eq("F1: a text is recorded", cli(root, *rep).code, 0)
        check_eq("F1: the same text again (own record, same relation) is still fine", cli(root, *rep).code, 0)
        other = cli(root, "record-source", "--output", inventory, "--ref", "docs/own.md", "--file", doc, "--relation", "parent")
        check_eq("F1: the same locator under another relation is refused", other.code, 2)
    finally:
        cleanup(root)


# --- get / freshness ----------------------------------------------------------------------------------------------------

def get_and_freshness() -> None:
    root = project()
    stub, saved = stub_tracker()
    try:
        key, _ = LK.mint(TEXT, {}, root)
        got = cli(root, "get", key, "--json")
        check_eq("get: a local key reads its file, no tracker", (got.code, stub.calls, json.loads(got.out)["provenance"]["source"]), (0, [], "person_pasted"))
        work = work_of(root, key)
        got = cli(root, "get", key, "--output", work / "ticket-snapshot.json", "--raw-dir", work / "ticket-raw")
        check_eq("get: --raw-dir writes the references of the text as a paste", (got.code, (work / "ticket-references.json").is_file()), (0, True))
        task_root = work.parent
        got = cli(root, "freshness", key, "--task-root", task_root, "--json")
        check_eq("freshness: the file is read, unchanged text is none, no tracker", (got.code, json.loads(got.out)["result"], stub.calls), (0, "none", []))
        # the file changes: a requirements change, still no tracker
        text_file(root, key, TEXT + "A new paragraph.\n")
        got = cli(root, "freshness", key, "--task-root", task_root, "--json")
        check_eq("freshness: a changed text file is a change, no tracker", (got.code, json.loads(got.out)["result"], stub.calls), (0, "requirements", []))
        # the text file is gone: the snapshot (marked) stands, nobody asks a tracker
        (root / "qa-factory" / "local-tickets" / f"{key}.md").unlink()
        got = cli(root, "freshness", key, "--task-root", task_root, "--json")
        check_eq("freshness: marked and no file: exit 0, no HTTP", (got.code, json.loads(got.out)["result"], stub.calls), (0, "none", []))
        check_in("freshness: ... and says so", "local story: its text file is not here; the snapshot stands", got.err)
        # a pasted text under a REAL key does not become local
        work_of(root, "PROJ-5")
        paste = root / "paste.md"
        paste.write_text("# T\n\nbody\n", encoding="utf-8")
        got = cli(root, "get", "PROJ-5", "--ticket-file", paste, "--json")
        check_eq("a text pasted under a real key is not marked local", (got.code, "local_key" in json.loads(got.out)["provenance"]), (0, False))
        check_eq("... and is_local stays False for it", LK.is_local("PROJ-5", root), False)
        # F2 (t-551): a pasted snapshot that carries the mark never makes a real key local (the mark has ONE writer).
        # Mutation: remove the `pop` in `ticket_adapter.read_ticket_file`.
        copied = root / "copy.json"
        copied.write_text(json.dumps({"key": "LOCAL-7", "title": "T", "acceptance_criteria": [], "comments": [],
                                      "provenance": {"source": "file", "local_key": True}}), encoding="utf-8")
        out7 = root / "qa-factory" / "artifacts" / "LOCAL-7" / "work" / "ticket-snapshot.json"
        got = cli(root, "get", "LOCAL-7", "--ticket-file", copied, "--output", out7)
        check_eq("F2: the pasted copy is read", (got.code, got.err[-200:]), (0, ""))
        check_eq("F2: the mark of a pasted copy is dropped", "local_key" in json.loads(out7.read_text(encoding="utf-8"))["provenance"], False)
        check_eq("F2: a real LOCAL-7 is not local after the write", LK.is_local("LOCAL-7", root), False)
    finally:
        restore_tracker(saved)
        cleanup(root)


# --- get --output: the key gate -----------------------------------------------------------------------------------------

def key_gate() -> None:
    root = project()
    try:
        paste = root / "paste.md"
        paste.write_text("# T\n\nbody\n", encoding="utf-8")
        out = root / "qa-factory" / "artifacts" / "ADD-TO-CART" / "work" / "ticket-snapshot.json"
        got = cli(root, "get", "ADD-TO-CART", "--ticket-file", paste, "--output", out)
        check_eq("get --output: ADD-TO-CART is exit 3 and nothing is written", (got.code, out.exists()), (3, False))
        for needle in ("is not a key of this project's tracker", "ticket_adapter.py local-key --words-file <file>",
                       "--key-form-word --words-file <file>"):
            check_in(f"get --output refusal names: {needle}", needle, got.err)
        out2 = root / "qa-factory" / "artifacts" / "CART-1" / "work" / "ticket-snapshot.json"
        check_eq("get --output: CART-1 passes", cli(root, "get", "CART-1", "--ticket-file", paste, "--output", out2).code, 0)
        out3 = root / "qa-factory" / "artifacts" / "LOCAL-1" / "work" / "ticket-snapshot.json"
        check_eq("get --output: LOCAL-1 is a key under every kind", cli(root, "get", "LOCAL-1", "--ticket-file", paste, "--output", out3).code, 0)
        # the person's words let the name stand, and are kept in the snapshot
        out4 = root / "qa-factory" / "artifacts" / "ADD-TO-CART" / "work" / "ticket-snapshot.json"
        got = cli(root, "get", "ADD-TO-CART", "--ticket-file", paste, "--output", out4, "--key-form-word",
                  "--words-file", words(root, "keep this name"))
        check_eq("get --output --key-form-word: passes", got.code, 0)
        check_eq("... and the words are in provenance.key_form_word", json.loads(out4.read_text(encoding="utf-8"))["provenance"]["key_form_word"], "keep this name")
        # an old story: pipeline.json beside the work folder, or a file already at --output
        old = root / "qa-factory" / "artifacts" / "OLD-NAME"
        (old / "work").mkdir(parents=True)
        (old / "pipeline.json").write_text("{}", encoding="utf-8")
        check_eq("get --output: an existing pipeline.json passes", cli(root, "get", "OLD-NAME", "--ticket-file", paste, "--output", old / "work" / "ticket-snapshot.json").code, 0)
        older = root / "qa-factory" / "artifacts" / "OLDER-NAME" / "work"
        older.mkdir(parents=True)
        (older / "ticket-snapshot.json").write_text("{}", encoding="utf-8")
        check_eq("get --output: an existing file at --output passes", cli(root, "get", "older name", "--ticket-file", paste, "--output", older / "ticket-snapshot.json").code, 0)
        # a guessed form never refuses
        cfg = json.loads((root / "qa-factory" / "config.json").read_text(encoding="utf-8"))
        cfg["adapters"] = {"ticket": {"name": "linear"}}
        (root / "qa-factory" / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
        check_eq("get --output: a guessed tracker form does not refuse", cli(root, "get", "eng-123", "--ticket-file", paste,
                 "--output", root / "qa-factory" / "artifacts" / "eng-123" / "work" / "ticket-snapshot.json").code, 0)
        # the flag on a verb that does not honour it is refused
        check_eq("--key-form-word on another verb is exit 2", cli(root, "peek", "X-1", "--output", root / "i.json", "--key-form-word").code, 2)
    finally:
        cleanup(root)


# --- external_writes -----------------------------------------------------------------------------------------------------

def external_writes_guard() -> None:
    from test_external_writes_bug_refusals import Rig
    root = project()
    rig = Rig(root)
    try:
        text_file(root, "LOCAL-1")
        use_project(root)
        for label, fields, want in (
                ("external_id LOCAL-1", {"action": "comment", "external_id": "LOCAL-1"}, "REJECT"),
                ("parent as a string", {"action": "create", "fields": {"summary": "s", "parent": "LOCAL-1"}}, "REJECT"),
                ("parent as {key}", {"action": "create", "fields": {"summary": "s", "parent": {"key": "LOCAL-1"}}}, "REJECT"),
                ("PROJ-1 as external_id", {"action": "comment", "external_id": "PROJ-1"}, "ok"),
                ("a real LOCAL-7 with no file and no mark", {"action": "comment", "external_id": "LOCAL-7"}, "ok"),
                ("external_id local-1 (case, F6)", {"action": "comment", "external_id": "local-1"}, "REJECT"),
                ("external_id ' LOCAL-1' (space, F6)", {"action": "comment", "external_id": " LOCAL-1 "}, "REJECT"),
                ("parent 'local-1' (F6)", {"action": "create", "fields": {"summary": "s", "parent": "local-1"}}, "REJECT"),
                ("parent {key: ' Local-1'} (F6)", {"action": "create", "fields": {"summary": "s", "parent": {"key": " Local-1"}}}, "REJECT"),
                ("parent LOCAL-1 on a comment (F6: any action)", {"action": "comment", "external_id": "PROJ-1", "fields": {"parent": "LOCAL-1"}}, "REJECT"),
                ("a parent that is not text", {"action": "comment", "external_id": "PROJ-1", "fields": {"parent": 7}}, "ok"),
                ("PROJ-1 as a parent", {"action": "comment", "external_id": "PROJ-1", "fields": {"parent": "PROJ-1"}}, "ok"),
                # LAST: a create that passes records an external_id, and every later create is then a SKIP
                ("LOCAL-1 in the description", {"action": "create", "fields": {"summary": "s", "description": "see LOCAL-1"}}, "ok")):
            rig.calls.clear()
            rig.write(**fields)
            status = rig.run()
            word = status[0][0] if status else "none"
            local = word == "REJECT" and "local key" in status[0][2]
            check_eq(f"external_writes {label}: {'refused as local' if want == 'REJECT' else 'passes'}", local, want == "REJECT")
            if want == "REJECT":
                check_eq(f"external_writes {label}: the transport was not called", rig.calls, [])
    finally:
        rig.close()
        cleanup(root)


# --- the forms ---------------------------------------------------------------------------------------------------------------

def forms_all_kinds() -> None:
    root = project()
    try:
        key, _ = LK.mint(TEXT, {}, root)
        for label, cfg in (("jira", {"adapters": {"ticket": {"name": "jira"}}}), ("github", GITHUB),
                           ("file+key_pattern", {"adapters": {"ticket": {"name": "file", "key_pattern": "[A-Z]{2,4}-\\d+"}}})):
            cfg = dict(cfg, case_id_form="{ticket}_TC_{nnn}")
            check_eq(f"forms: the minted key is a key under {label}", AF.is_key(key, cfg), True)
            check_eq(f"forms: {key}_TC_001 is a case id under {label}", CF.is_id(f"{key}_TC_001", cfg), True)
    finally:
        cleanup(root)


def taken_artifact_root() -> None:
    """OF3-1d item 7 (AR-4): `_taken` counts the story folders of the configured root (already so), and a config that is a JSON
    list, bad JSON or a non-string root falls back to today's folder with no crash. One row set, both worlds."""
    rows = (  # (id, config text or None, folder holding the story LOCAL-7, expected highest number)
        ("no config: the default folder", None, "qa-factory/artifacts", 7),
        ("configured root: its folders count", '{"artifact_root": "stories"}', "stories", 7),
        ("configured root: the old folder no longer counts", '{"artifact_root": "stories"}', "qa-factory/artifacts", 0),
        ("config a JSON list: today's folder, no crash", "[]", "qa-factory/artifacts", 7),
        ("config bad JSON: today's folder, no crash", "{not json", "qa-factory/artifacts", 7),
        ("config non-string root: today's folder, no crash", '{"artifact_root": 5}', "qa-factory/artifacts", 7),
    )
    for label, config, where, expected in rows:
        root = project()
        try:
            (root / where / "LOCAL-7").mkdir(parents=True)
            if config is not None:
                (root / "qa-factory" / "config.json").write_text(config, encoding="utf-8")
            check_eq(f"taken: {label}", LK._taken(root, {}, r"LOCAL-\d+"), expected)
        finally:
            cleanup(root)


def main() -> None:
    taken_artifact_root()
    is_local_battery()
    mint_battery()
    mint_race_and_limit()
    mint_cleanup_after_write_error()
    local_key_verb()
    main_key()
    refresh_with_a_tracker_source()
    record_source_edges()
    record_source_declared_roots()
    document_places()
    linked_documents_rows()
    record_source_never_replaces()
    get_and_freshness()
    key_gate()
    external_writes_guard()
    forms_all_kinds()
    finish("test_local_keys")


if __name__ == "__main__":
    main()
