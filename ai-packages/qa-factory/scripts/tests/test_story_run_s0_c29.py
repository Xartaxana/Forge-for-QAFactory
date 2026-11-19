"""c29: a part of test_story_run_s0.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s0_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, s0_project, run_scenarios
from story_run_s0_common import price_broken  # noqa: E402


# --- C2-9 (D-0043): the factory does not ask about the known-impossible, and does not re-ask per instance -----------------------
C29_MR = "https://git.example.com/team/sdk/-/merge_requests/510"


C29_SHARE = "https://share.example.com/sites/x/video.mp4"


def c29_source(sid="SRC-1", media=(), **over):
    item = {"source_id": sid, "canonical_ref": f"https://jira.example.invalid/browse/APP-{sid[-1]}", "relation": "referenced",
            "relevance": "relevant", "required": True, "status": "read", "inspection_status": "read", "revision": "r1",
            "human_review": {"words": "ok", "shown": {"relevance": "relevant"}},
            "materials": {"comments": {"status": "read"}, "attachments": {"status": "read", "items": []},
                          "external_media": {"status": "unavailable" if media else "read", "items": list(media)}}}
    item.update(over)
    return item


def c29_write(task_root: Path, *sources) -> Path:
    path = task_root / "work" / "source-inventory.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema_version": 1, "sources": list(sources)}), encoding="utf-8")
    return path


def c29_s1_gap_question() -> None:
    """T9 (the text), T9b (`ask` writes what the question named, for `s1_gap` alone), T19 (`causes`)."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        asked_row = {"url": C29_MR, "status": "unavailable", "cause": "auth_required", "access_problem": True,
                     "error": "auth_required: 302 to the SSO login"}
        by_default = {"url": C29_SHARE, "status": "unavailable", "cause": "no_tool", "error": "no_tool: no browser"}
        c29_write(task_root, c29_source("SRC-1", [asked_row, by_default]))
        driver = driver_for(root, env, task)
        gap_ref = "source material unavailable and not accepted by a person: SRC-1"
        text = driver.s1_gap_text(gap_ref)
        check_in("T9 the asked point is listed with its cause", "auth_required: 302 to the SSO login", text)
        check_eq("T9 the point the factory itself established is not among the asked lines",
                 [line for line in str(text).splitlines() if line.startswith("- ") and C29_SHARE in line], [])
        check_in("T9 one line says it was recorded without a question", "Already recorded as gaps, without a question", text)
        check_in("T9 the access paragraph is for the asked point", "dropped VPN or an expired login", text)
        check_eq("T9 `not needed` and `skip all like these` are tokens when a cause is asked", tuple(text.priced),
                 ("not needed", "skip all like these"))
        check_eq("T9 the question names its source and its cause", (text.sources, text.classes), (("SRC-1",), ("auth_required",)))
        check_eq("T9 and every option has its price lines", price_broken(text + "\n---\nAnswer: x"), [])
        c29_write(task_root, c29_source("SRC-1", [by_default]))
        text = driver.s1_gap_text(gap_ref)
        check_eq("T9 nothing asked: no kind token, no source", (tuple(text.priced), text.sources, text.classes), (("not needed",), (), ()))
        check_not_in("T9 and no access paragraph", "lost access", text)
        # the limit: 60 sources, the body at most 6000 bytes, the rest in the details, the tokens name ALL of them
        many = [c29_source(f"SRC-{n:02x}", [dict(asked_row, url=f"https://git.example.com/team/sdk/-/merge_requests/{n}")]) for n in range(60)]
        c29_write(task_root, *many)
        ref = "; ".join(f"source material unavailable and not accepted by a person: SRC-{n:02x}" for n in range(60))
        text = driver.s1_gap_text(ref)
        body = str(text)[:str(text).index("## What each answer")]
        check("T9 60 sources: the body is at most 6000 bytes", len(body.encode("utf-8")) <= driver.GAP_TEXT_MAX, str(len(body.encode("utf-8"))))
        check_in("T9 and says how many it did not print", "more sources - the whole list is in the file named below", text)
        check_eq("T9 the details hold the whole list of 60; the tokens name all 60", (text.details.count("(SRC-"), len(text.sources)), (60, 60))
        three = [c29_source(f"SRC-a{n}", [dict(asked_row, url=f"https://git.example.com/team/sdk/-/merge_requests/{n}")]) for n in range(3)]
        c29_write(task_root, *three)
        small = driver.s1_gap_text("; ".join(f"source material unavailable and not accepted by a person: SRC-a{n}" for n in range(3)))
        check_not_in("T9 three sources: all printed, no `more`", "more sources", small)
        # T9b / T19
        driver.ask(story_run.Person("s1_gap", small, "S1", "S1-qa-scout-1"))
        asked = driver.state["asked"]
        check_eq("T9b `ask` writes what the s1_gap question named", (asked.get("sources"), asked.get("classes")),
                 (["SRC-a0", "SRC-a1", "SRC-a2"], ["auth_required"]))
        rows = [json.loads(l) for l in (driver.state_dir / "driver-questions.jsonl").read_text(encoding="utf-8").splitlines()]
        check_eq("T19 the detector row of an s1_gap carries the causes", rows[-1].get("causes"), ["auth_required"])
        other = story_run.Person("halt", "The conductor needs your word.", "S3")
        other.sources, other.classes = ("SRC-9",), ("auth_required",)
        driver.ask(other)
        rows = [json.loads(l) for l in (driver.state_dir / "driver-questions.jsonl").read_text(encoding="utf-8").splitlines()]
        check_eq("T9b a question of another kind never carries the fields", ("sources" in driver.state["asked"], "classes" in driver.state["asked"]),
                 (False, False))
        check_eq("T19 and its detector row has no `causes`", "causes" in rows[-1], False)
    finally:
        harness.cleanup(root)


def c29_gap_body(text) -> str:
    """The BODY of an `s1_gap` question: everything before the options (the blank line included)."""
    return str(text)[:str(text).index("## What each answer")]


def c29_s1_gap_cap() -> None:
    """T9 F-2 (the access paragraph names the real answer, the count is the options') and F-3 (the 6000-byte cap bounds the body:
    AT 6000 printed whole, 6001 cut with `+K more`; the access list is bounded; 150 sources keep a line)."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        mr = "https://git.example.com/team/sdk/-/merge_requests/510"
        auth = {"url": mr, "status": "unavailable", "cause": "auth_required", "access_problem": True, "error": "auth_required: SSO"}
        ref = lambda ids: "; ".join(f"source material unavailable and not accepted by a person: {i}" for i in ids)    # noqa: E731
        # F-2: the paragraph names the answer by its words; the count is the count of the answers offered
        c29_write(task_root, c29_source("SRC-1", [auth]))
        text = driver.s1_gap_text(ref(["SRC-1"]))
        check_in("F-2 the access paragraph names the route answer by its words", 'give the answer "here is how to reach it"', text)
        check_not_in("F-2 and no longer by a position", "second answer", text)
        check_in("F-2 four answers are offered (not needed, skip all like these, route, content): the count says Four", "Four answers work", text)
        check_eq("F-2 the words it quotes are the words of an option offered below", str(text).count("(c) here is how to reach it"), 1)
        c29_write(task_root, c29_source("SRC-1", [dict(auth, cause="transient", error="transient: timeout")]))
        text = driver.s1_gap_text(ref(["SRC-1"]))
        check_eq("F-2 an asked cause that is not about access: four answers, and no access paragraph",
                 ("Four answers work" in str(text), "lost access" in str(text)), (True, False))
        c29_write(task_root, c29_source("SRC-1", [{"url": C29_SHARE, "status": "unavailable", "cause": "no_tool", "error": "no_tool: x"}]))
        text = driver.s1_gap_text(ref(["SRC-1"]))
        check_eq("F-2 with nothing asked (no kind to offer) there are three answers: Three",
                 ("Three answers work" in str(text), tuple(text.priced)), (True, ("not needed",)))
        # F-3: 150 sources, each asked about lost access: the body stays inside the cap, a line is shown, the lists say `+K more`
        for count, pad in ((60, 0), (150, 0), (150, 80)):
            rows = [c29_source(f"SRC-{n:03x}", [dict(auth, url=f"https://share.example.com/sites/{'x' * pad}/doc-{n}.pdf")])
                    for n in range(count)]
            c29_write(task_root, *rows)
            text = driver.s1_gap_text(ref([f"SRC-{n:03x}" for n in range(count)]))
            body = c29_gap_body(text)
            shown = [line for line in body.splitlines() if line.startswith("- ")]
            check(f"F-3 {count} sources (names {pad}): the body is at most 6000 bytes ({len(body.encode('utf-8'))}) and shows a source line",
                  len(body.encode("utf-8")) <= driver.GAP_TEXT_MAX and len(shown) >= 1, str(len(shown)))
            check_eq(f"F-3 {count} sources: the access list is bounded and says how many it left out",
                     ("(+%d more)" % (count - driver.GAP_NAMES_SHOWN) in body, len(text.sources), text.details.count("(SRC-")),
                     (True, count, count))
            check_in(f"F-3 {count} sources: the line says how many sources it did not print",
                     "more sources - the whole list is in the file named below", body)
        # AT and BEYOND the cap: one source line grows a byte at a time (a cause that is not about access, so the tail is fixed)
        transient = {"url": mr, "status": "unavailable", "cause": "transient", "error": "transient: timeout"}

        def render(fixed: int, pad: int):
            rows = [c29_source(f"SRC-{n:02x}", [dict(transient, url=f"{mr}?{n}")]) for n in range(fixed)]
            rows.append(c29_source("SRC-ff", [dict(transient, url=f"{mr}?{'y' * pad}")]))
            c29_write(task_root, *rows)
            return driver.s1_gap_text(ref([f"SRC-{n:02x}" for n in range(fixed)] + ["SRC-ff"]))

        fixed = 20          # as many fixed lines as leave room for one line to grow the body from ~5700 to past 6000
        while len(c29_gap_body(render(fixed, 1)).encode("utf-8")) < 5700 and "more sources" not in c29_gap_body(render(fixed, 1)):
            fixed += 1
        last_whole = None
        for pad in range(1, 380):
            text = render(fixed, pad)
            body = c29_gap_body(text)
            if "more sources" in body:
                break
            last_whole = (pad, len(body.encode("utf-8")), text)
        check("AT: some body was printed whole before the cut", last_whole is not None)
        check_eq("AT: the largest body printed whole is exactly 6000 bytes, every source line in it, no details file",
                 (last_whole[1], last_whole[2].details), (driver.GAP_TEXT_MAX, ""))
        check_eq("BEYOND: the next byte (6001) is cut: `+1 more sources`, the whole list in the details, the body inside the cap",
                 ("(+1 more sources - the whole list is in the file named below)" in body, len(body.encode("utf-8")) <= driver.GAP_TEXT_MAX,
                  text.details.count("(SRC-")), (True, True, fixed + 1))
        check_eq("BEYOND: the tokens still name every source", len(text.sources), fixed + 1)
    finally:
        harness.cleanup(root)


def c29_s1_gap_answer() -> None:
    """T10 (the tokens have their executor and read ONLY tokens), T10b (an answer to another kind is not taken here)."""
    import source_inventory as SI
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        auth = {"url": C29_MR, "status": "unavailable", "cause": "auth_required", "error": "auth_required: SSO"}
        transient = {"url": C29_SHARE, "status": "unavailable", "cause": "transient", "error": "transient: timeout"}
        c29_write(task_root, c29_source("SRC-1", [auth, transient]))
        driver = driver_for(root, env, task)
        classes_file = task_root / "work" / "gap-classes.json"
        asked = {"kind": "s1_gap", "stage": "S1", "dispatch": "S1-qa-scout-1", "sources": ["SRC-1"], "classes": ["auth_required"]}
        taken = driver._answer_s1_gap("go on without it", asked, "- a\n", "S1", "S1-qa-scout-1")
        check_eq("T10 a phrase is not a token: not taken, nothing written", (taken, classes_file.exists()), (False, False))
        taken = driver._answer_s1_gap("skip all like these", dict(asked, classes=[]), "- a\n", "S1", "S1-qa-scout-1")
        check_eq("T10 the kind token with no kind offered goes to the conductor", (taken, classes_file.exists()), (False, False))
        taken = driver._answer_s1_gap("skip all like these", dict(asked, sources=[]), "- a\n", "S1", "S1-qa-scout-1")
        check_eq("T10 a token with no source named goes to the conductor", (taken, classes_file.exists()), (False, False))
        taken = driver._answer_s1_gap("skip all like these", asked, "- SRC-1 line\n", "S1", "S1-qa-scout-1")
        rows = json.loads(classes_file.read_text(encoding="utf-8"))["classes"] if classes_file.exists() else []
        check_eq("T10 the kind token records exactly the kinds the question OFFERED (not `transient`, which the inventory also holds)",
                 (taken, [(r["id"], r["cause"], r["words"]) for r in rows]), (True, [("GC-1", "auth_required", "skip all like these")]))
        check_eq("T10 and the point of that cause is now closed by the kind",
                 SI.completeness(SI.load_inventory(task_root / "work" / "source-inventory.json"), **SI.class_kwargs(task_root))["closed_by_class"],
                 {"SRC-1": {SI._media_id(auth, 0): "GC-1"}})
        c29_write(task_root, c29_source("SRC-2", [dict(transient)]))
        taken = driver._answer_s1_gap("not needed", {"sources": ["SRC-2"], "classes": []}, "- a\n", "S1", "S1-qa-scout-1")
        item = json.loads((task_root / "work" / "source-inventory.json").read_text(encoding="utf-8"))["sources"][0]
        check_eq("T10 `not needed` accepts the sources the question NAMED, in the person's words",
                 (taken, item.get("gap_acceptance", {}).get("words")), (True, "not needed"))
        # T10b the branch belongs to the kind
        called = []
        driver._answer_s1_gap = lambda *args: called.append(args) or True
        driver.state["asked"] = {"kind": "conductor", "stage": "S3", "dispatch": "", "classes": ["auth_required"], "sources": ["SRC-1"]}
        driver.state["pending_words"] = {}
        driver.state_dir.mkdir(parents=True, exist_ok=True)
        (driver.state_dir / "driver-question.md").write_text("---\nkind: conductor\n---\nQuestion?\n", encoding="utf-8")
        sent = root / "answer.md"
        sent.write_bytes(b"skip all like these")
        try:
            import contextlib
            import io
            with contextlib.redirect_stdout(io.StringIO()):
                driver.take_answer(sent)
        except Exception:
            pass            # what the conductor does with the words is not this test's business
        check_eq("T10b an answer to a question of another kind is not taken by the s1_gap branch", called, [])
    finally:
        harness.cleanup(root)


def c29_partial_accept() -> None:
    """T10 F-5: the kinds are written, a later call is refused - the text says the kinds were recorded, never `nothing was accepted`."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        auth = {"url": C29_MR, "status": "unavailable", "cause": "auth_required", "error": "auth_required: SSO"}
        bare = {"url": C29_SHARE, "status": "unavailable", "error": "no cause recorded"}
        c29_write(task_root, c29_source("SRC-1", [auth, bare]))
        driver = driver_for(root, env, task)
        real = driver.py

        def py(script, *args, **kw):
            if script == "ticket_adapter.py" and "--point" in args:
                return 1, "ticket_adapter: gap acceptance rejected: the disk is full"
            return real(script, *args, **kw)
        driver.py = py
        asked = {"kind": "s1_gap", "stage": "S1", "dispatch": "S1-qa-scout-1", "sources": ["SRC-1"], "classes": ["auth_required"]}
        try:
            driver._answer_s1_gap("skip all like these", asked, "- SRC-1 line\n", "S1", "S1-qa-scout-1")
            raised = details = None
        except story_run.Person as person:
            raised, details = str(person.text), str(person.details)
        check("F-5 a refusal of the second call raises the person's own question", raised is not None)
        check_eq("F-5 the kinds are on disk", (task_root / "work" / "gap-classes.json").is_file(), True)
        check_in("F-5 and the text says the kinds were recorded and covers the later ones", "recorded for the kinds of gap (auth_required)", raised or "")
        check_not_in("F-5 and never `nothing was accepted` after a write", "nothing was accepted", raised or "")
        check_in("F-5 and carries the recorded kinds and the refusal's own words in the details", "the disk is full", details or "")
        # the first call refused: nothing is written, and the text may say so
        (task_root / "work" / "gap-classes.json").unlink()
        driver.py = lambda script, *args, **kw: (1, "refused") if script == "ticket_adapter.py" else real(script, *args, **kw)
        try:
            driver._answer_s1_gap("skip all like these", asked, "- SRC-1 line\n", "S1", "S1-qa-scout-1")
            raised = None
        except story_run.Person as person:
            raised = str(person.text)
        check_in("F-5 when the FIRST call is refused nothing was recorded, and the text says so", "nothing was accepted", raised or "")
    finally:
        harness.cleanup(root)


def c29_class_problem_defect() -> None:
    """T-F4 (L-2 V-5 b): a damaged record of kinds after S1 closed is ONE finding of the factory, once per problem text."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        filed = []
        driver.file_defect = lambda ref, notes: filed.append(notes)
        driver.state_dir.mkdir(parents=True, exist_ok=True)

        def controller(s1: str, problem: str) -> None:
            (driver.state_dir / "controller.json").write_text(json.dumps(
                {"stages": {"S1": {"status": s1}}, "source_completeness": {"gap_class_problem": problem}}), encoding="utf-8")
        controller("completed", "")
        driver.report_gap_class_problem()
        controller("pending", "work/gap-classes.json cannot be read: bad json")
        driver.report_gap_class_problem()
        check_eq("F-4 no problem, or S1 not closed yet (the question carries the line): no finding", filed, [])
        controller("completed", "work/gap-classes.json cannot be read: bad json")
        driver.report_gap_class_problem()
        driver.report_gap_class_problem()
        check_eq("F-4 a damaged record after S1 closed: ONE finding, owner factory, naming the problem",
                 (len(filed), (filed or [""])[0].startswith("owner: factory"), "gap-classes.json cannot be read: bad json" in (filed or [""])[0]),
                 (1, True, True))
        controller("completed", "work/gap-classes.json cannot be read: another")
        driver.report_gap_class_problem()
        check_eq("F-4 a different problem is a new finding", len(filed), 2)
    finally:
        harness.cleanup(root)


def c29_s1_review_offer() -> None:
    """FV3-27 (edges a-c): `unavailable` is offered while something is ASKED, and an inventory the factory cannot read never hides it (AR-28).
    The one predicate `source_inventory.asked_open` is read by the text and by the dry walker's fact, so the two agree on every row."""
    import source_inventory as SI
    task = "QA-1"
    root, task_root, env = s0_project(task)
    asked_row = {"url": C29_MR, "status": "unavailable", "cause": "auth_required", "access_problem": True, "error": "auth_required: 302 to the SSO login"}
    by_default = {"url": C29_SHARE, "status": "unavailable", "cause": "no_tool", "error": "no_tool: no browser"}
    good = lambda *media: json.dumps({"schema_version": 1, "sources": [c29_source("SRC-1", list(media))]})      # noqa: E731
    path = task_root / "work" / "source-inventory.json"
    try:
        driver = driver_for(root, env, task)
        for label, raw, offered, defaulted_line in (
                ("a: nothing unavailable", good(), False, False),
                ("a: only what the factory itself established (a default)", good(by_default), False, True),
                ("a: one point still asked", good(asked_row), True, False),
                ("b: missing file", None, True, False), ("b: a directory at the path", "DIR", True, False), ("b: empty file", "", True, False),
                ("b: bytes not UTF-8", b"\xff\xfe{", True, False), ("b: invalid JSON", "{not json", True, False),
                ("b: JSON []", "[]", True, False), ("b: JSON null", "null", True, False), ("b: JSON \"x\"", '"x"', True, False), ("b: JSON 1", "1", True, False),
                ("b: sources a string", '{"sources": "x"}', True, False), ("b: sources [1]", '{"sources": [1]}', True, False),
                ("c: gap-classes.json unreadable, an asked point stays asked", good(asked_row), True, False)):
            if path.is_dir():
                path.rmdir()
            elif path.exists():
                path.unlink()
            if raw == "DIR":
                path.mkdir(parents=True)
            elif raw is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw if isinstance(raw, bytes) else raw.encode("utf-8"))
            classes = task_root / "work" / "gap-classes.json"
            if label.startswith("c:"):
                classes.write_text("{broken", encoding="utf-8")
            try:
                text = driver.s1_review_text("digest")
            except Exception as raised:      # noqa: BLE001 - the row judges that nothing comes out
                check(f"{label}: nothing raises out of s1_review_text", False, repr(raised))
                continue
            check_eq(f"{label}: `unavailable` offered", "for anything unavailable: get me access" in str(text), offered)
            check_eq(f"{label}: the defaulted line", "cannot reach by itself" in str(text), defaulted_line)
            check_eq(f"{label}: the predicate agrees with the text", SI.asked_open(task_root), offered)
    finally:
        harness.cleanup(root)


def c29_unreachable_mr() -> None:
    """T8 (the code writes the verdict of an unreachable merge request, with its carrier) and T14 (`handoff` collects again for a gap by
    default, with no error)."""
    import source_inventory as SI
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        def story(code: str):
            c29_write(task_root, c29_source("SRC-1", [{"url": C29_MR, "status": "pending"}]))
            driver = driver_for(root, env, task)
            driver.git_route = lambda *a, **k: ""
            real = driver.py

            def py(script, *args, **kw):
                if script == "vcs_evidence.py":
                    out = Path(args[args.index("--output") + 1])
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_text(json.dumps({"url": C29_MR, "status": "unavailable", "error": code} if code else
                                              {"url": C29_MR, "status": "unavailable"}), encoding="utf-8")
                    return 1, ""
                return real(script, *args, **kw)
            driver.py = py
            return driver

        def row():
            return json.loads((task_root / "work" / "source-inventory.json").read_text(encoding="utf-8"))["sources"][0][
                "materials"]["external_media"]["items"][0]

        driver = story("host_unreachable")
        got = driver.close_vcs_gaps([])
        summary = SI.completeness(SI.load_inventory(task_root / "work" / "source-inventory.json"))
        check_eq("T8 a receipt that says host_unreachable is written by CODE: unavailable, its cause, its carrier, collected",
                 (got, row().get("status"), row().get("cause"), row().get("probe_code"), bool(row().get("probe_sha256"))),
                 (True, "unavailable", "host_unreachable", "host_unreachable", True))
        check_eq("T8 and it is a gap by default: no question is born", (summary["defaulted_gaps"], summary["unavailable_materials"]),
                 (["SRC-1"], []))
        check_eq("T14 the condition `handoff` collects by sees it", driver._defaulted_vcs(), True)
        check_eq("T8 a second run over the same verdict changes nothing the caller must re-read", driver.close_vcs_gaps([]), False)
        driver = story("unauthenticated")
        got = driver.close_vcs_gaps([])
        summary = SI.completeness(SI.load_inventory(task_root / "work" / "source-inventory.json"))
        check_eq("T8 `unauthenticated` is an access problem the person is asked about, never a default",
                 (row().get("cause"), summary["defaulted_gaps"], summary["unavailable_materials"]), ("auth_required", [], ["SRC-1"]))
        for code in ("brand_new_code", ""):
            driver = story(code)
            got = driver.close_vcs_gaps([])
            check_eq(f"T8 a code the table does not know ({code or 'none'}) writes nothing: the item stays pending",
                     (got, row().get("status")), (False, "pending"))
        # T14 handoff reaches the collector although the gate has no error
        driver = story("host_unreachable")
        driver.close_vcs_gaps([])
        calls = []

        class Stop(Exception):
            pass

        def stub(errors):
            calls.append(list(errors))
            raise Stop()
        driver.close_vcs_gaps = stub
        driver.exit_errors = lambda role, digest, dispatch=None: []
        driver.form_errors = lambda dispatch: []
        driver.revoke_passes_of_dead = lambda: None
        try:
            driver.handoff("qa-scout", "S1", "S1-qa-scout-1", {"is_error": False, "result": "ok", "exit_code": 0, "stderr": ""})
        except Stop:
            pass
        except Exception:       # a handoff that never reached the collector goes on and dies elsewhere: the check below names it
            pass
        check_eq("T14 handoff calls the collector for a gap by default even with no error", calls, [[]])
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios(
        [],
        [
        c29_s1_gap_question,
        c29_s1_gap_cap,
        c29_s1_gap_answer,
        c29_partial_accept,
        c29_class_problem_defect,
        c29_s1_review_offer,
        c29_unreachable_mr,
    ],
    )
    harness.finish("test_story_run_s0_c29")


# split: runner piece 1
if __name__ == "__main__":
    main()
