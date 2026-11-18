"""driver: a part of test_story_sides.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
from story_sides_common import ABSENT, SUBSTITUTED, copy_registry  # noqa: E402


def driver_cases():
    """t-2181 PC-1b in the driver at S0: the second story is not asked; the answer is recorded once (writer 2); a no_trace story
    keeps it in `pipeline.sides` with the line; C15; an unreadable registry is `sides_unknown`."""
    import project_knowledge as PK
    from story_run_common import eq as check_eq   # this one takes a detail text (the process output) as a fourth argument
    from story_run_common import s0_answer, s0_pipeline, s0_project, s0_run, s0_state, stub_calls
    repos = {"code_repos": [{"name": "app", "path": "app"}]}
    # PC2-7 (t-043): ONE table - the implicit `product` is carried exactly when no side of the story is a real side of this team, whatever the
    # registry holds from earlier stories and with or without `--no-trace`. Each S0 row runs traced AND `--no-trace` and the two records are
    # equal without `at`; the id of the row names the case in every label. `second-story` has no `--no-trace` half (that flow asks again).
    product_default = {"reality": "real", "deliverable": True, "source": "default"}
    ours, theirs = (("ui", True, ""),), (("backend", False, "platform team"),)
    # id, registry rows (name, deliverable, settles_by), launch flags, the answer to sides.deliverable (None: not asked), `product`, `backend`
    rows = (
        ("own-answer", (), ("--side", "backend=substituted"), "another team's", product_default, (SUBSTITUTED, False, "")),
        ("other-story-row", theirs, ("--side", "backend=substituted"), None, product_default, (SUBSTITUTED, False, "platform team")),
        ("real-side-named", ours, ("--side", "backend=substituted"), "another team's", None, None),
        ("other-team-real", (("ui", False, ""),), ("--side", "backend=substituted"), "another team's", product_default, None),
        ("reference-only", (), ("--reference", "ui=old"), None, None, None),
        ("second-story", (), ("--side", "backend=substituted"), "another team's", product_default, (SUBSTITUTED, False, "")),
    )

    def strip(sides):
        return {name: {k: v for k, v in entry.items() if k != "at"} for name, entry in sides.items()}

    def story_one(row, *extra):
        """A fresh project, the registry rows seeded, the launch and the answer; `(root, task_root, env, out)` - the caller cleans up."""
        root, task_root, env = s0_project("PROJ-1", config=repos)
        for name, deliverable, settles_by in row[1]:
            PK.record(root, key=PK.SIDES_KEY, environment="", element=name, state="known", scope="project",
                      value={"deliverable": deliverable, "settles_by": settles_by}, words="the person said", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1", *extra, *row[2])
        if row[3]:
            out = s0_answer(root, env, "PROJ-1", row[3], *extra)
        return root, task_root, env, out

    for row in rows:
        name, found = row[0], {}
        for mode, extra in (("traced", ()), ("no-trace", ("--no-trace",))):
            if name == "second-story" and extra:
                continue
            root, task_root, env, out = story_one(row, *extra)
            try:
                found[mode] = strip(s0_pipeline(task_root)["sides"])
                check_eq(f"{name} ({mode}): S0 ends and nothing is left asked", (out.returncode, s0_state(task_root).get("s0_block")), (0, None),
                         out.stdout[-500:] + out.stderr[-300:])
                check_eq(f"{name} ({mode}): `product` is as the rule says", found[mode].get("product"), row[4])
                if row[5]:
                    got = found[mode]["backend"]
                    check_eq(f"{name} ({mode}): the registry's deliverable and settles_by are recorded with the launch's reality",
                             (got["reality"], got["deliverable"], got.get("settles_by", "")), row[5])
                if name == "second-story":      # story 2 of the project: the same launch, a copy of the registry, nothing asked
                    root2, task_root2, env2 = s0_project("PROJ-2", config=repos)
                    try:
                        copy_registry(root, root2)
                        out2 = s0_run(root2, env2, "PROJ-2", *row[2])
                        second = strip(s0_pipeline(task_root2)["sides"])
                        check_eq(f"{name}: story 2 is not asked", (out2.returncode, s0_state(task_root2).get("s0_block")), (0, None),
                                 out2.stdout[-500:] + out2.stderr[-300:])
                        check_eq(f"{name}: story 2 carries story 1's `product`, whole", second.get("product"), found[mode]["product"])
                        check_eq(f"{name}: story 2's backend equals story 1's on reality and deliverable (its source differs by design)",
                                 {k: second["backend"][k] for k in ("reality", "deliverable")},
                                 {k: found[mode]["backend"][k] for k in ("reality", "deliverable")})
                    finally:
                        harness.cleanup(root2)
            finally:
                harness.cleanup(root)
        if "no-trace" in found:
            check_eq(f"{name}: the traced and the `--no-trace` records are equal without `at`", found["traced"], found["no-trace"])
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        s0_run(root, env, "PROJ-1", "--side", "backend=substituted")
        out = s0_answer(root, env, "PROJ-1", "another team's")
        row = PK.state(root, PK.SIDES_KEY, "", "backend")["row"] or {}
        check_eq("writer 2: the answer is a project row, by driver, source person, state known",
                 (out.returncode, row.get("value"), (row.get("provenance") or {}).get("by"), (row.get("provenance") or {}).get("source"), row.get("state")),
                 (0, {"deliverable": False, "settles_by": ""}, "driver", "person", "known"))
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        s0_run(root, env, "PROJ-1", "--no-trace", "--side", "backend=substituted")
        out = s0_answer(root, env, "PROJ-1", "ours", "--no-trace")
        check_eq("a no_trace story keeps the answer in pipeline.sides (source person)",
                 (out.returncode, {k: s0_pipeline(task_root)["sides"]["backend"][k] for k in ("deliverable", "source")}),
                 (0, {"deliverable": True, "source": "person"}), out.stdout[-400:] + out.stderr[-300:])
        line = "your answer about backend was kept for this story only (an experiment leaves no trace)"
        check("... says the one line", line in out.stdout, out.stdout[-400:])
        check("... and the line is a warning of the story's record too (F5)", line in s0_pipeline(task_root)["warnings"],
              s0_pipeline(task_root)["warnings"])
        check_eq("... and records nothing in the registry", PK.record_path(root).exists(), False)
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="ui", state="known", scope="project", value={"deliverable": True},
                  words="ours", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1", "--side", "UI=substituted")
        check_eq("C15: `UI` beside a recorded `ui` is refused, S0 is not recorded", (task_root / "pipeline.json").exists(), False,
                 out.stdout[-400:] + out.stderr[-300:])
        # the guard hands a refusal to the conductor, so the refusal text is the prompt of the conductor call (no default that holds the name)
        prompts = [call.get("prompt", "") for call in stub_calls(root) if call.get("kind") == "conductor"]
        check("... the refusal (the conductor's prompt) names the recorded name and the flag that is the door",
              any("`ui`" in text and "Start again with --side" in text for text in prompts), prompts[-1][-600:] if prompts else "no conductor call")
        check_eq("... the offending name is not kept in launch (the corrected flag is the door)",
                 "UI" in ((s0_state(task_root).get("launch") or {}).get("side") or {}), False)
        out = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        check_eq("... and the recorded spelling goes through", (out.returncode, (task_root / "pipeline.json").exists()), (0, True),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        out = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        pipeline = s0_pipeline(task_root)
        check_eq("an unreadable registry: S0 ends with pipeline.sides_unknown written and no side recorded as real",
                 (out.returncode, sorted(pipeline.get("sides_unknown") or {}), "sides" in pipeline), (0, ["at", "why"], False),
                 out.stdout[-400:] + out.stderr[-300:])
        first_at = pipeline["sides_unknown"]["at"]
        out = s0_run(root, env, "PROJ-1")
        check_eq("F1 (b): the file still unreadable on the relaunch: the mark is kept, its `at` unchanged",
                 (out.returncode, (s0_pipeline(task_root).get("sides_unknown") or {}).get("at")), (0, first_at),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)
    stands = {"code_repos": [{"name": "app", "path": "app"}], "environments": [{"name": "dev"}]}
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        s0_run(root, env, "PROJ-1")
        check_eq("F1 (a): S0 over an unreadable registry gives sides_unknown", bool(s0_pipeline(task_root).get("sides_unknown")), True)
        PK.record_path(root).unlink()
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
                  value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("F1 (a): the repaired registry on the relaunch clears the mark and records the substituted side (source registry)",
                 (out.returncode, bool(pipeline.get("sides_unknown")), entry.get("reality"), entry.get("deliverable"), entry.get("source")),
                 (0, False, SUBSTITUTED, False, "registry"), out.stdout[-400:] + out.stderr[-300:])
        check_eq("F1 (a): ... and the re-read carries the implicit `product` as the default, as S0 spells it (K-b2, AR-19)",
                 {k: v for k, v in ((pipeline.get("sides") or {}).get("product") or {}).items() if k != "at"}, product_default)
        check_eq("... and a third launch with no mark does nothing more (the record is as it was)", (s0_run(root, env, "PROJ-1").returncode,
                 s0_pipeline(task_root)["sides"]), (0, pipeline["sides"]))
    finally:
        harness.cleanup(root)
    # t-2277 batch 2b W2 (4): a relaunch re-read of a side with NO recorded deliverable answer keeps the default `ours` (the owner accepted it)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        s0_run(root, env, "PROJ-1")
        PK.record_path(root).unlink()
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("W2 (4): the re-read records the stand's reality and writes NO deliverable for a side nobody answered (source registry)",
                 (out.returncode, bool(pipeline.get("sides_unknown")), entry.get("reality"), "deliverable" in entry, entry.get("source")),
                 (0, False, SUBSTITUTED, False, "registry"), out.stdout[-400:] + out.stderr[-300:])
        import contract
        check_eq("... and the readers take it as ours (default true), the question is not raised by the re-read",
                 (contract.story_sides(pipeline)["backend"]["deliverable"], s0_state(task_root).get("s0_block")), (True, None))
    finally:
        harness.cleanup(root)
    # PC3-1 (t-057 N1, N6): the re-read after a registry repair records what S0 would have recorded with a readable registry -
    # same merge (registry + launch words + the person's answers), same `product` default. Ids name the case in every label.
    def seed_backend_theirs(root):
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
                  value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")

    def break_registry(root):
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")

    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        seed_backend_theirs(root)
        control = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        control_sides = strip(s0_pipeline(task_root)["sides"])
        check_eq("reread-launch-words (control): a readable registry at S0 with `--side ui=real` records ui, backend, and no `product`",
                 (control.returncode, sorted(control_sides)), (0, ["backend", "ui"]), control.stdout[-400:] + control.stderr[-300:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "ui=real")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        check_eq("reread-still-unreadable: the registry still broken keeps the mark and records no side",
                 (out.returncode, bool(pipeline.get("sides_unknown")), "sides" in pipeline), (0, True, False), out.stdout[-400:] + out.stderr[-300:])
        PK.record_path(root).unlink()
        seed_backend_theirs(root)
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        check_eq("reread-launch-words: the launch's `--side ui=real` survives the repair, so the re-read equals S0 with a readable registry",
                 (out.returncode, bool(pipeline.get("sides_unknown")), strip(pipeline.get("sides") or {})), (0, False, control_sides),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "ui=substituted")      # the registry is unreadable: the question stands
        s0_answer(root, env, "PROJ-1", "another team's", "--side", "ui=real")    # the person said `another team's` before the repair
        PK.record_path(root).unlink()
        seed_backend_theirs(root)
        out = s0_run(root, env, "PROJ-1")
        sides = strip(s0_pipeline(task_root).get("sides") or {})
        check_eq("reread-person-answer: an answer given before the repair reaches the record (ui another team's, source person) and `product` follows",
                 (out.returncode, sides.get("ui"), sides.get("product")),
                 (0, {"reality": "real", "deliverable": False, "source": "person"}, product_default), out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "UI=real")     # names are empty while the registry is unreadable, so C15 cannot fire
        PK.record_path(root).unlink()
        PK.record(root, key=PK.SIDES_KEY, environment="", element="ui", state="known", scope="project",
                  value={"deliverable": False, "settles_by": "web team"}, words="theirs", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        log = (root / "stub-log.jsonl").read_text(encoding="utf-8") if (root / "stub-log.jsonl").is_file() else ""
        check_eq("reread-case-twin: `--side UI=real` beside a registry `ui` is the C15 refusal as at S0 (the mark stays, no side is written, "
                 "the name is dropped from the kept launch)",
                 ("side names are compared exactly" in out.stdout + out.stderr + log, bool(pipeline.get("sides_unknown")), "sides" in pipeline,
                  (s0_state(task_root).get("launch") or {}).get("side")),
                 (True, True, False, {}), out.stdout[-400:] + out.stderr[-300:] + log[-400:])
    finally:
        harness.cleanup(root)
    for case, rows_after in (("reread-all-real-registry", (("ui", True, ""),)), ("reread-empty-registry", ())):
        root, task_root, env = s0_project("PROJ-1", config=stands)
        try:
            break_registry(root)
            s0_run(root, env, "PROJ-1")
            PK.record_path(root).unlink()
            for name, deliverable, settles_by in rows_after:
                PK.record(root, key=PK.SIDES_KEY, environment="", element=name, state="known", scope="project",
                          value={"deliverable": deliverable, "settles_by": settles_by}, words="ours", source="person", story="S-0", by="conductor")
            out = s0_run(root, env, "PROJ-1")
            pipeline = s0_pipeline(task_root)
            check_eq(f"{case}: no non-real side and no reference: the mark lifts, no side (`product` included) is written",
                     (out.returncode, bool(pipeline.get("sides_unknown")), "sides" in pipeline), (0, False, False), out.stdout[-400:] + out.stderr[-300:])
        finally:
            harness.cleanup(root)
    import contract
    first, second = contract.product_default_entry(), contract.product_default_entry()
    first["settles_by"] = "x"
    check_eq("product_default_entry: the values, and a fresh dict on every call", (second, first is second), (product_default, False))
    # t-2277 batch 2b W2 (1, 2): the answer is the PROJECT's (a registry row) and a later word overwrites it; the next story reads the latest
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project", value={"deliverable": False, "settles_by": ""},
                  words="another team's", source="person", story="S-0", by="driver")
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project", value={"deliverable": True, "settles_by": ""},
                  words="no, this backend is ours", source="person", story="S-1", by="conductor")
        out = s0_run(root, env, "PROJ-1", "--side", "backend=substituted")
        entry = s0_pipeline(task_root)["sides"]["backend"]
        check_eq("W2 (2): the later word overwrites: the story reads `ours`, and is asked nothing",
                 (out.returncode, s0_state(task_root).get("s0_block"), entry["deliverable"]), (0, None, True), out.stdout[-400:] + out.stderr[-300:])
        row = PK.state(root, PK.SIDES_KEY, "", "backend")["row"]
        check_eq("... the registry's latest row carries the person's words, who and when",
                 (row["provenance"]["words"], row["provenance"]["story"], bool(row["at"])), ("no, this backend is ours", "S-1", True))
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
                  value={"deliverable": False, "settles_by": ""}, words="theirs", source="person", story="S-0", by="conductor")
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("F2: no --env, the stand `dev` selected: its substituted row reaches pipeline.sides (never read as real)",
                 (out.returncode, pipeline.get("environment"), entry.get("reality"), entry.get("deliverable")),
                 (0, "dev", SUBSTITUTED, False), out.stdout[-500:] + out.stderr[-300:])
        check("F6: no side of the story is a real side of this team (backend is substituted, another team's), so `product` is implied in pipeline.sides",
              "product" in (pipeline.get("sides") or {}), sorted(pipeline.get("sides") or {}))
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": ABSENT}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        check_eq("F2 sibling: a side known only from the selected stand's row is asked sides.deliverable (never silently ours)",
                 (out.returncode != 0 or s0_state(task_root).get("s0_block") is not None, (task_root / "pipeline.json").exists(),
                  str(s0_state(task_root).get("s0_block"))), (True, False, "deliverable:backend"), out.stdout[-500:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def main() -> None:
    driver_cases()
    harness.finish("test_story_sides_driver")


# split: runner piece 1
if __name__ == "__main__":
    main()
