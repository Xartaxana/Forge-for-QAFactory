#!/usr/bin/env python3
"""k35 k36: a part of test_story_run_stand_identity.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_stand_identity_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import OTHER_SCRIPT, run_scenarios, d2_answer, d2_conductor_calls, d2_enter, eq, human_broken, s0_question, set_control
from story_run_stand_identity_common import (  # noqa: E402
    DIGEST, HEAD, LABEL, NOWHERE, OLD, Rig, asked, flag, journal_answers, mismatched, run_entry,
    sources_mismatched, unknown, use_plan,
)


# --- K35: the question and its texts ----------------------------------------------------------------------------

def realistic_persons(driver) -> dict:
    """Every variant, and the prefixes stacked on them, with the slots a real stand gives: a label name, a container path, a
    command with a flag and a script name in it (which the text must not carry), a docker message with a flag in it."""
    import stand_identity as SI
    out = SI.data()["outcomes"]
    tried = [{"method": "oci_label", "outcome": out["oci_label.no_label"].format(container="testproject1-ui-static", label=LABEL)},
             {"method": "build_sha_file", "outcome": out["build_sha_file.missing"].format(
                 path="/usr/share/nginx/html/build-sha.txt", container="testproject1-ui-static", why="cat: can't open the file")}]
    row = {"environment_id": "localhost", "profile_id": "e2e-ui", "method": "oci_label", "label": LABEL, "source": "person",
           "recorded_at": "2026-10-01T10:00:00+00:00", "words": "x"}
    command_row = dict(row, method="command", argv=["python3", "print_build.py", "--short"])
    confirms_row = dict(row, method="person_confirms")

    def make(variant, rec, with_row=None, stage="S6", kind="both"):
        return driver.build_person(stage, kind, "localhost", "e2e-ui", rec, with_row, variant)
    voided = {"what": "the checkout moved to commit eeeeee000000", "earlier_at": "2026-10-02T08:00:00+00:00"}
    return {
        "how": make("how", unknown("e2e-ui", tried=tried, container="testproject1-ui-static")),
        "how, more tried": make("how", unknown("e2e-ui", tried=[{"method": "docker", "outcome": "no container is named for this profile"}], tried_more=2)),
        "how, a docker message with a flag": make("how", unknown("e2e-ui", tried=[
            {"method": "docker", "outcome": "docker did not answer (unknown flag: --format; see 'docker inspect --help')"}])),
        "how, registry unreadable": make("how", unknown("e2e-ui", tried=tried, registry_error="qa-factory/records/stand-identity.json: bad")),
        "mismatched": make("mismatched", mismatched("e2e-ui"), row),
        "mismatched by a command": make("mismatched", mismatched("e2e-ui", provenance={
            "technical_verification": True, "source_linkage": "exact", "identity_kind": "command", "deployed_source_revision": OLD,
            "verified_source_revisions": [HEAD]}), command_row),
        "mismatched_sources": make("mismatched_sources", sources_mismatched("e2e-ui", ["src/app/page.ts", "src/app/main.ts"])),
        "mismatched_sources, a script among them": make("mismatched_sources", sources_mismatched("e2e-ui", ["src/app/page.ts", "build.py"])),
        "confirm": make("confirm", unknown("e2e-ui", asks="confirm"), confirms_row),
        "method_failed": make("how", unknown("e2e-ui", tried=tried, registry_method_failed=out["command.failed"].format(
            why="python3: can't open file 'print_build.py'")), command_row),
        "method_failed, a plain label": make("how", unknown("e2e-ui", tried=tried, registry_method_failed=out["oci_label.no_label"].format(
            container="testproject1-ui-static", label=LABEL)), row),
        "voided": make("how", unknown("e2e-ui", tried=tried, voided=voided)),
        "voided confirm": make("confirm", unknown("e2e-ui", asks="confirm", voided=voided), confirms_row),
        "voided mismatched": make("mismatched", mismatched("e2e-ui", voided=voided), row),
    }


def k35_the_question_and_its_texts() -> None:
    rig = Rig(profiles=("e2e-ui",))
    try:
        use_plan({"TC-1": ("e2e-ui", "automate")})
        rig.records(**{"e2e-ui": unknown("e2e-ui", container="ui-c")})
        code, out, started, driver = run_entry(rig, s5=("TC-1",))
        eq("K35: `unknown` + asks_person how at the S5 entry: exit 3", code, 3)
        eq("K35: the question is kind stand_identity at S5", (asked(rig).get("kind"), asked(rig).get("stage")), ("stand_identity", "S5"))
        eq("K35: no role was started", started, [])
        shown = s0_question(rig.task_root)
        eq("K35: the question text obeys human-questions.md, answer block included", human_broken(shown.split("\n", 6)[-1].split("\n---\nAnswer:")[0]), [])
        for needle in ("localhost", "qa-factory/records/stand-identity.json", "`deployed`", "`always confirm`", "`retry`", "`label <name>`",
                       "no container is named for this profile", "e2e-ui tests", "repo-e2e-ui", HEAD[:12]):
            check_in(f"K35: the how text names {needle}", needle, shown)
        packet = flag(rig)
        eq("K35: the flag carries the packet, set by ask() alone (stand, profile, variant, commits, what was offered)",
           (packet.get("environment"), packet.get("profile"), packet.get("variant"), packet.get("revision"), packet.get("answers")),
           ("localhost", "e2e-ui", "how", HEAD, ["label", "file", "command", "deployed", "always confirm", "retry"]))
        check("K35: the factory's own words went to the details file, and the body names no script or flag",
              "tried - docker: no container" in (rig.task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8")
              and ".py" not in shown.split("---\nAnswer:")[0] and "--" not in shown.split("---\nAnswer:")[0])
        argv = rig.calls()[0]["argv"]
        eq("K35 (R5/R1/R4 rule): the rehearsal run carries --no-evidence and the story's own --task-root",
           ("--no-evidence" in argv, Path(argv[argv.index("--task-root") + 1]).resolve() if "--task-root" in argv else None),
           (True, rig.task_root.resolve()))
        # every variant, with the prefixes stacked on it
        persons = realistic_persons(driver)
        for label, person in persons.items():
            eq(f"K35: the `{label}` text obeys human-questions.md", human_broken(person.text), [])
            eq(f"K35: `{label}` is a Person of kind stand_identity with its packet", (person.kind, bool(person.build_question["answers"])),
               ("stand_identity", True))
        for label in ("how", "how, registry unreadable", "method_failed", "voided"):
            for needle in ("`deployed`", "`always confirm`", "`retry`", "qa-factory/records/stand-identity.json", "`localhost`"):
                check_in(f"K35: the `{label}` text names {needle}", needle, persons[label].text)
        for needle in (OLD[:12], HEAD[:12], "`test deployed`", "`stop`", "`retry`"):
            check_in(f"K35: `mismatched` names {needle}", needle, persons["mismatched"].text)
        for needle in ("`src/app/page.ts`", HEAD[:12], "`stop`", "`retry`"):
            check_in(f"K35: `mismatched_sources` names {needle}", needle, persons["mismatched_sources"].text)
        check_not_in("K35: `mismatched_sources` offers no `test deployed` (the build there has no commit to name)", "test deployed",
                     persons["mismatched_sources"].text)
        check_in("K35: a path with a folder in it (`src/app/main.ts`) breaks no rule and is named", "`src/app/main.ts`", persons["mismatched_sources"].text)
        scripted = persons["mismatched_sources, a script among them"]
        check_not_in("K35: a bare file name that is a script name breaks the rules - it is not named in the body (FR-6)", "build.py", scripted.text)
        check_in("K35: ... the count is said instead", "2 of the files this story changes", scripted.text)
        check_in("K35: ... and the details file keeps the names", "build.py", scripted.details)
        check_not_in("K35: a command with a flag and a script name is not quoted in the body (FR-6)", "print_build.py", persons["mismatched by a command"].text)
        check_not_in("K35: ... nor in a failed way's sentence", "print_build.py", persons["method_failed"].text)
        check_not_in("K35: a docker message with a flag in it is not quoted in the body (FR-6)", "--format", persons["how, a docker message with a flag"].text)
        check_in("K35: ... its details are in the file", "--format", persons["how, a docker message with a flag"].details)
        check_in("K35: the failed way's text says what it was and when", "The way you gave on 2026-10-01", persons["method_failed, a plain label"].text)
        check_in("K35: the voided text says when and what moved", "You confirmed it on 2026-10-02; since then the checkout moved", persons["voided"].text)
        check_in("K35: a registry that cannot be read says so and that `deployed` and `retry` still work", "while `deployed` and `retry` still work",
                 persons["how, registry unreadable"].text)
        check("K35: the five variants are different texts (FR-7: the text moves when the situation moved)",
              len({persons[k].text for k in ("how", "mismatched", "mismatched_sources", "confirm", "method_failed", "voided")}) == 6)
        check_in("K35: more tried than shown says how many more", "and 2 more", persons["how, more tried"].text)
        check("K35: tried outcomes that name the image label are in the body whole when the rules of human-text.json allow it, in plain words when "
              "they do not (the rules move: t-363's `config_key`) - and either way the text obeys them",
              ("the details of what I tried are in the file named at the end" in persons["how"].text or LABEL in persons["how"].text)
              and human_broken(persons["how"].text) == [])
        check_in("K35: ... and the details file keeps them whole", LABEL, persons["how"].details)
        # the limit on the files named: AT 5 all named, BEYOND 6 one more is counted
        at = driver.build_person("S6", "both", "localhost", "e2e-ui", sources_mismatched("e2e-ui", [f"f{i}.ts" for i in range(5)]), None, "mismatched_sources")
        beyond = driver.build_person("S6", "both", "localhost", "e2e-ui", sources_mismatched("e2e-ui", [f"f{i}.ts" for i in range(6)]), None, "mismatched_sources")
        check("K35: AT 5 differing files all five are named, none counted more", all(f"`f{i}.ts`" in at.text for i in range(5)) and "more" not in at.text.split("differ")[0])
        check("K35: BEYOND (6) the sixth is not named and `and 1 more` is said", "`f5.ts`" not in beyond.text and "and 1 more" in beyond.text)
        # NEGATIVE CONTROL: the checker is not asleep
        check("K35 NEGATIVE CONTROL: a text with a script name, a flag and an exit code IS caught by the same checker",
              set(human_broken("I ran stand_identity.py confirm --task X and it said exit 2.")) >= {"script_name", "flag", "exit_code"})
        # the data: every answer a variant offers is in its text and has a form; every executor slot is one the driver fills
        import stand_identity as SI
        data = SI.data()
        forms = data["answers"]["forms"]
        for name, variant in data["question"]["variants"].items():
            body = "\n".join(variant["text"])
            check(f"K35 data: every answer of `{name}` is a form and is named in its text (`word` or `word <value>`)",
                  all(a in forms and (f"`{forms[a]['word']}`" in body or f"`{forms[a]['word']} <" in body) for a in variant["answers"]),
                  str(variant["answers"]))
        slots = driver.build_answer_slots({"environment": "localhost", "profile": "api", "revision": HEAD, "deployed": OLD, "image": DIGEST}, "w", "a")
        for name, spec in forms.items():
            for argv in spec.get("runs") or []:
                try:
                    driver.build_expand(argv, slots)
                    filled = True
                except KeyError:
                    filled = False
                check(f"K35 data: the executor of `{name}` uses only slots the driver fills", filled)
    finally:
        rig.done()


# --- the closed forms: the reader, at and beyond its limits -------------------------------------------------------

def forms_reader() -> None:
    import stand_identity as SI
    import story_run
    forms = SI.data()["answers"]["forms"]
    everything = list(forms)
    read = lambda words, offered=everything: story_run.Driver.build_read_answer(words, offered, forms)  # noqa: E731
    for words, form, arg in (("deployed", "deployed", ""), ("Deployed.", "deployed", ""), ("`deployed`", "deployed", ""), ("  DEPLOYED!  ", "deployed", ""),
                             ("test deployed", "test deployed", ""), ("Test   Deployed", "test deployed", ""), ("always confirm", "always confirm", ""),
                             ("retry", "retry", ""), ("stop", "stop", ""), ("\ufeffretry", "retry", ""),
                             ("label", "label", ""), ("label org.example.rev", "label", "org.example.rev"), ("label `org.example.rev`", "label", "org.example.rev"),
                             ("file /usr/share/x.txt", "file", "/usr/share/x.txt"), ("file", "file", ""), ("command", "command", ""),
                             ("command python3 sha.py --short", "command", "python3 sha.py --short"),
                             ('command "C:/Program Files/p.exe" -c "print(1)"', "command", '"C:/Program Files/p.exe" -c "print(1)"'),
                             ("deployed 0123456", "deployed", "0123456"), ("deployed " + "AB" * 20, "deployed", "ab" * 20)):
        got = read(words)
        eq(f"forms: `{words}` reads as {form} {arg!r}", (got.get("form"), got.get("arg", "")), (form, arg))
    for label, words in (("a form with prose after it", "deployed, I checked it yesterday"), ("`retry` with a word after it", "retry please"),
                         ("a commit one character short (6)", "deployed 012345"), ("a commit one character long (41)", "deployed " + "a" * 41),
                         ("a non-hex word where a commit would go", "deployed ghijklm"), ("prose", "the stand is fine, I looked at it"),
                         ("another script", OTHER_SCRIPT), ("two lines", "deployed\nretry"), ("a form hidden in a sentence", "yes, deployed"),
                         ("prose after `label` (t-366 F3, the critic's D4)", "label i do not know which one, use the default"),
                         ("a label of two words", "label org.example rev"), ("a `file` value that is no path", "file my notes"),
                         ("a `file` value that is a relative path", "file build-sha.txt"), ("a path with a space in it", "file /srv/my file.txt"),
                         ("empty", ""), ("only a BOM", "\ufeff"), ("only quotes", "``")):
        got = read(words)
        eq(f"forms: {label} is NOT read (it goes to the conductor)", (got.get("form"), bool(got.get("why"))), ("", True))
    named = read("test deployed", ["deployed", "retry"])
    eq("forms: a form this question did not offer is not read, and is named", (named["form"], named.get("named")), ("", "test deployed"))
    eq("forms: `test deployed` is never read as `deployed` plus words", read("test deployed")["form"], "test deployed")


# --- K36: the answers (the real ladder) -----------------------------------------------------------------------------

def k36_deployed_always_confirm_retry() -> None:
    # deployed: the confirm executor ran, the registry is untouched, the words are whole in the journal, the next entry starts the role
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K36 setup: the stand is asked about (exit 3)", (code, asked(rig).get("kind"), flag(rig).get("variant")), (3, "stand_identity", "how"))
        question_text = s0_question(rig.task_root).split("\n---\nAnswer:")[0]       # the answer block is where a command may stand (rule 5)
        check_in("K36 setup: the real ladder said why", "no container is named for this profile", question_text)
        words = "Deployed."        # the form, as a person types it: case and the closing full stop do not matter, the words are kept whole
        code, out, started, _ = run_entry(rig, words, s5=("TC-1",))
        eq("K36 deployed: the answer is taken and the next entry starts the role (exit 0)", (code, ("S5", "qa-automator") in started), (0, True))
        rows = rig.confirmations()
        eq("K36 deployed: ONE confirmation line, for this story, with this story's commit and the words whole",
           [(r["kind"], r["revision"], r["task"], r["words"], r["image"]) for r in rows], [("deployed", rig.head, rig.task, words, "absent")])
        eq("K36 deployed: the registry is untouched (still absent)", rig.registry().exists(), False)
        check("K36 deployed: the journal's human_answer holds the words WHOLE", any(words in n and "stand build at S5 (localhost, api tests)" in n for n in journal_answers(rig)),
              str(journal_answers(rig)))
        check_in("K36 deployed: the next entry says the build is the person's word, in a line", "confirmed by your word of", out)
        check("K36 (M10, FR-6): the person is shown no script name, flag or exit code - not in the question, not in what the driver printed",
              all(bad not in out and bad not in question_text for bad in ("stand_identity.py", "--revision", "--words", "--task", "exit ")), out[:400])
        eq("K36 deployed: the next entry asked nothing", (asked(rig), flag(rig)), ({}, {}))
    finally:
        rig.done()
    # a story started BEFORE N1b has no confirmations file: the registry alone answers (TE6, edge ix); the word is read first afterwards
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.put_row("person_confirms")
        check("K36 temporal: a story with no confirmations file yet", not (rig.task_root / "state" / "stand-confirmations.jsonl").exists())
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K36 temporal: the question works from the registry alone (the `confirm` variant)", (code, flag(rig).get("variant")), (3, "confirm"))
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("K36 temporal: after the file exists the word is read first: the next entry goes on (exit 0)", (code, len(rig.confirmations())), (0, 1))
    finally:
        rig.done()

    # always confirm: a person_confirms row, THEN a confirmation; with the record failing no confirmation, and the question returns
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        driver, started, steps, probes = rig.driver(s5=("TC-1",), answer=d2_answer(rig.root, "always confirm"))
        seq, real_py = [], driver.py

        def spy(script, *args, **kw):
            if script == "stand_identity.py":
                seq.append(args[0])
            return real_py(script, *args, **kw)
        driver.py = spy
        code = d2_enter(driver, "S5")
        eq("K36 always confirm: a person_confirms row, then the confirmation, in that order", seq, ["record", "confirm"])
        eq("K36 always confirm: the row is the person's, method person_confirms; the story is confirmed too",
           ([(r["method"], r["source"]) for r in rig.rows()], [r["kind"] for r in rig.confirmations()]), ([("person_confirms", "person")], ["deployed"]))
        eq("K36 always confirm: the stage goes on (exit 0)", code, 0)
    finally:
        rig.done()
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.registry().parent.mkdir(parents=True, exist_ok=True)
        rig.registry().write_text("{ this is not json", encoding="utf-8")
        before = rig.sha(rig.registry())
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K36 AE4: a registry nobody can read still asks (the defaults ran)", (code, flag(rig).get("variant")), (3, "how"))
        check_in("K36 AE4: the question says the file cannot be read and `deployed` and `retry` still work", "while `deployed` and `retry` still work", s0_question(rig.task_root))
        seq = []
        driver, started, steps, probes = rig.driver(s5=("TC-1",), answer=d2_answer(rig.root, "always confirm"))
        real_py = driver.py

        def spy2(script, *args, **kw):
            if script == "stand_identity.py":
                seq.append(args[0])
            return real_py(script, *args, **kw)
        driver.py = spy2
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = d2_enter(driver, "S5")
        eq("K36 always confirm, the record step FAILS: the confirmation never ran", seq, ["record"])
        eq("K36 ... no confirmation was written and the corrupt file was not touched", (rig.confirmations(), rig.sha(rig.registry())), ([], before))
        eq("K36 ... the question comes back (exit 3) saying nothing was recorded", (code, flag(rig).get("variant")), (3, "how"))
        check_in("K36 ... changed, and it names the failure", "I could not write down your last answer", s0_question(rig.task_root))
        check_in("K36 ... the factory's own words are in the details file", "stand-identity.json", (rig.task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8"))
        check("K36 ... and the journal has the words, said as not recorded", any("not recorded" in n and "always confirm" in n for n in journal_answers(rig)))
        # `deployed` still works with that file (AE4: the confirmation never touches the registry)
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("K36 AE4: `deployed` goes through while the registry is unreadable", (code, [r["kind"] for r in rig.confirmations()], rig.sha(rig.registry())),
           (0, ["deployed"], before))
    finally:
        rig.done()

    # retry: nothing is written; the question comes back with the FR-7 notice
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        first = s0_question(rig.task_root)
        code, out, started, _ = run_entry(rig, "retry", s5=("TC-1",))
        eq("K36 retry: nothing is written (no registry, no confirmation)", (rig.registry().exists(), rig.confirmations()), (False, []))
        eq("K36 retry: the stand is checked at once and is still unknown: asked again (exit 3)", (code, flag(rig).get("variant")), (3, "how"))
        check_in("K36 retry: FR-7 - the same question comes back with the notice that it was answered before", "You have answered this exact question before", s0_question(rig.task_root))
        check_not_in("K36 retry CONTROL: the FIRST ask carried no such notice", "You have answered this exact question before", first)
    finally:
        rig.done()


def k36_method_answers() -> None:
    # label: a `record` row and an immediate re-probe; the way fails (no container) so the next text differs and names it (FR-7)
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        first = s0_question(rig.task_root)
        words = f"label {LABEL}"
        code, out, started, _ = run_entry(rig, words, s5=("TC-1",))
        rows = rig.rows()
        eq("K36 label: a registry row, the person's, with the label and the words whole",
           [(r["method"], r["source"], r["label"], r["words"]) for r in rows], [("oci_label", "person", LABEL, words)])
        eq("K36 label: the re-probe ran in the same move: the way failed, so the question comes back (exit 3), in the failed-way text", (code, flag(rig).get("variant")), (3, "how"))
        second = s0_question(rig.task_root)
        check_in("K36 label: the second text names the failed way and when (FR-7)", "The way you gave on", second)
        check_in("K36 label: ... and why, in the details file (the label name in the body would break the `config_key` rule)", "no container is named for this profile",
                 (rig.task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8"))
        check("K36 label: the second text is NOT the first", second != first and "did not answer" in second and "did not answer" not in first)
        check_in("K36 label: ONE outcome line says it is recorded (data, t-366 F5)", "S5: the person's answer for stand `localhost` (api tests) is recorded; the build is checked again", out)
        check("K36 label: the script's own acknowledgement is NOT echoed (it names a state path) - one line, not two (t-366 F5)",
              "Recorded the decision" not in out and "stand-identity.json" not in out.split("# Driver question")[0]
              and out.count("is recorded") == 1, out[:600])
        # a second recording answer for the same stand and profile: the last one counts, the log says so, the record quotes the earlier line
        code, out, started, _ = run_entry(rig, "label example.org/revision", s5=("TC-1",))
        check_in("K36 last wins: the log says the stand was answered more than once and the last line counts", "answered more than once in this story; the last line counts", out)
        last = rig.rows()[-1]
        eq("K36 last wins: two rows, the last in force, with the label", (len(rig.rows()), last["label"]), (2, "example.org/revision"))
        check_in("K36 last wins: the record quotes the earlier line", "(replaces their earlier line: label org.opencontainers.image.revision)", last["words"])
        check_in("K36 last wins CONTROL: the FIRST recording answer carried no such note", "label org.opencontainers.image.revision", rig.rows()[0]["words"])
        check_not_in("K36 last wins CONTROL: ... and was not marked as replacing anything", "replaces", rig.rows()[0]["words"])
    finally:
        rig.done()

    # command (the Windows spelling of a path, quotes round a word) and file: recorded, the ladder reads them at once
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        argv = rig.command_script(rig.head)
        words = f'command "{Path(argv[0]).as_posix()}" "{Path(argv[1]).as_posix()}"'
        code, out, started, _ = run_entry(rig, words, s5=("TC-1",))
        eq("K36 command: a registry `command` row with the argv split the platform's way", [r.get("argv") for r in rig.rows()],
           [[Path(argv[0]).as_posix(), Path(argv[1]).as_posix()]])
        eq("K36 command: the next probe runs it, reads this story's commit, and the stage goes on (exit 0)", (code, ("S5", "qa-automator") in started), (0, True))
        check_in("K36 command: the entry says the build is this story's, in a line", "the stand runs this story's build", out)
        eq("K36 FR-45: the entry check is a rehearsal - it wrote no evidence file and no `probe discovered` row (only the person's row is there)",
           (sorted((rig.task_root / "evidence").glob("runtime-provenance-*")) if (rig.task_root / "evidence").is_dir() else [],
            [r["source"] for r in rig.rows()]), ([], ["person"]))
    finally:
        rig.done()
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        code, out, started, _ = run_entry(rig, "file /usr/share/nginx/html/build-sha.txt", s5=("TC-1",))
        eq("K36 file: a registry row with the path", [(r["method"], r["path"]) for r in rig.rows()], [("build_sha_file", "/usr/share/nginx/html/build-sha.txt")])
        # `file` with nothing after it: asked again, naming the form; no conductor
        rig2 = Rig(profiles=("api",), real=True)
        try:
            set_control(rig2.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
            run_entry(rig2, s5=("TC-1",))
            code, out, started, _ = run_entry(rig2, "file", s5=("TC-1",))
            eq("K36 `file` with nothing after it: asked again (exit 3), no conductor, nothing written",
               (code, len(d2_conductor_calls(rig2.root)), rig2.rows(), rig2.confirmations()), (3, 0, [], []))
            check_in("K36 ... naming the form and what is needed", "You answered `file` with nothing after it. I need the path of the file inside the container", s0_question(rig2.task_root))
            check_in("K36 ... and how to write it", "file /path/inside/the/container", s0_question(rig2.task_root))
            eq("K36 ... the question is still the same one (the packet is kept)", flag(rig2).get("variant"), "how")
            run_entry(rig2, "command", s5=("TC-1",))
            check_in("K36 `command` with nothing after it: the same, naming the command form", "You answered `command` with nothing after it", s0_question(rig2.task_root))
        finally:
            rig2.done()
    finally:
        rig.done()


def k36_mismatched_answers() -> None:
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.put_row("command", argv=rig.command_script(rig.old))
        registry_before = rig.sha(rig.registry())
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K36 mismatched setup: the stand reads another commit of the checkout: a question, no role", (code, flag(rig).get("variant"), started), (3, "mismatched", []))
        text = s0_question(rig.task_root)
        check("K36 mismatched setup: the question names both commits", rig.old[:12] in text and rig.head[:12] in text)
        eq("K36 mismatched setup: the packet carries the commit the stand runs", (flag(rig)["deployed"], flag(rig)["revision"]), (rig.old, rig.head))
        # a plain `deployed` is no answer here (it never lifts a proven mismatch): the conductor reads it, nothing is recorded
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("K36 NEGATIVE CONTROL: `deployed` at the mismatched question is not read as a form: one conductor call, no confirmation", (len(d2_conductor_calls(rig.root)), rig.confirmations()), (1, []))
        # test deployed -> confirm --revision D --story-revision HEAD; the probe then says person_confirmed, the role starts
        code, out, started, _ = run_entry(rig, "test deployed", s5=("TC-1",))
        rows = rig.confirmations()
        eq("K36 test deployed: ONE line, kind test_deployed, revision = the deployed commit, story_revision = this story's",
           [(r["kind"], r["revision"], r["story_revision"]) for r in rows], [("test_deployed", rig.old, rig.head)])
        eq("K36 test deployed: the registry is unchanged by a mismatch answer, and the stage goes on (exit 0)", (rig.sha(rig.registry()), code), (registry_before, 0))
        check_in("K36 test deployed: the next entry says it is the person's word", "confirmed by your word of", out)
    finally:
        rig.done()
    # stop: the words are journaled, the question stays open with the held text, exit 3, nothing passed
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.put_row("command", argv=rig.command_script(rig.old))
        run_entry(rig, s5=("TC-1",))
        code, out, started, _ = run_entry(rig, "stop", s5=("TC-1",))
        eq("K36 stop: exit 3, no role, nothing recorded for the stand", (code, started, rig.confirmations()), (3, [], []))
        held = s0_question(rig.task_root)
        check_in("K36 stop: the held text says it stopped and nothing was passed", "You said to stop the story here. Nothing runs on `localhost` and nothing is passed", held)
        check_in("K36 stop: the question is still there with its answers", "`test deployed`", held)
        eq("K36 stop: the question stays open (kind stand_identity, flag set)", (asked(rig).get("kind"), bool(flag(rig))), ("stand_identity", True))
        check("K36 stop: the words are in the journal, with the owner", any("stop; owner: environment" in n and n.endswith(": stop") for n in journal_answers(rig)), str(journal_answers(rig)))
        eq("K36 stop: the held text is not an echo of the first ask (it moved)", "You said to stop" in held, True)
        code, out, started, _ = run_entry(rig, "retry", s5=("TC-1",))
        eq("K36 stop, then `retry`: the held question is answered like any other (the stand is read again: mismatched, asked again)", (code, flag(rig).get("variant")), (3, "mismatched"))
    finally:
        rig.done()


def k36_other_words_and_edges() -> None:
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        run_entry(rig, s5=("TC-1",))
        before = rig.sha(rig.registry())
        # M9: other words, in any language, are NOT read as a form - exactly one conductor call carrying the exact command lines
        for said in ("the stand is fine, I looked at it yesterday", OTHER_SCRIPT, "deployed, I checked"):
            calls_before = len(d2_conductor_calls(rig.root))
            code, out, started, _ = run_entry(rig, said, s5=("TC-1",))
            eq(f"K36 other words `{said[:30]}`: exactly one conductor call, nothing recorded", (len(d2_conductor_calls(rig.root)) - calls_before, rig.confirmations(), rig.rows()), (1, [], []))
        prompt = d2_conductor_calls(rig.root)[0]["prompt"]
        for needle in ("`localhost`", "`api`", rig.task, "qa-factory/records/stand-identity.json", "stand_identity.py", " confirm ", "--revision " + rig.head,
                       " record ", "--method person_confirms", "--method oci_label", "--method build_sha_file", "--method command", "<their words, verbatim>", "## The question"):
            check_in(f"K36 conductor: the note carries {needle}", needle, prompt)
        check_not_in("K36 conductor: ... and offers no form the question did not (`test deployed` is for a mismatch)", "--story-revision",
                     prompt.split("## Files the refusal names")[0])
        eq("K36 other words: the question is not changed by it: still asked (the loop re-entered the stage)", (asked(rig).get("kind"), flag(rig).get("variant")), ("stand_identity", "how"))
        # an answer for a stand the config no longer has: the conductor, never a crash, no executor ran
        cfg = json.loads(rig.config_path.read_text(encoding="utf-8"))
        cfg["environments"] = [{"name": "elsewhere", "base_url": "http://elsewhere"}]
        rig.config_path.write_text(json.dumps(cfg), encoding="utf-8")
        calls_before = len(d2_conductor_calls(rig.root))
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("K36 a stand the config no longer has: the conductor reads the answer, nothing was recorded", (len(d2_conductor_calls(rig.root)) - calls_before, rig.confirmations(), rig.sha(rig.registry())), (1, [], before))
        check_in("K36 ... and the note says what is missing", "is not in this project's config", d2_conductor_calls(rig.root)[-1]["prompt"])
        # an empty answer file and a BOM-only one: never a crash
        empty = rig.root / "answer.md"
        empty.write_bytes(b"")
        driver, started, steps, probes = rig.driver(s5=("TC-1",), answer=str(empty))
        eq("K36 an empty answer file: a stop with a message (exit 1), the question stays open", (driver.run(), bool(asked(rig))), (1, True))
        calls_before = len(d2_conductor_calls(rig.root))
        code, out, started, _ = run_entry(rig, "\ufeff", s5=("TC-1",))
        eq("K36 a BOM-only answer: the conductor, no crash, nothing recorded", (len(d2_conductor_calls(rig.root)) - calls_before, rig.confirmations()), (1, []))
    finally:
        rig.done()

    # (vi) a commit the answer names that is not the story's: asked again ONCE with the reason, then the conductor
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        run_entry(rig, s5=("TC-1",))
        code, out, started, _ = run_entry(rig, f"deployed {NOWHERE}", s5=("TC-1",))
        eq("K36 a commit that is no commit of the checkout: asked again once (exit 3), nothing recorded, no conductor", (code, rig.confirmations(), len(d2_conductor_calls(rig.root))), (3, [], 0))
        check_in("K36 ... with the reason", "is not a commit of this story's checkout, so I recorded nothing", s0_question(rig.task_root))
        eq("K36 ... the packet remembers it was asked once", flag(rig).get("reasked"), True)
        code, out, started, _ = run_entry(rig, f"deployed {NOWHERE}", s5=("TC-1",))
        eq("K36 ... the SECOND bad commit goes to the conductor", (len(d2_conductor_calls(rig.root)), rig.confirmations()), (1, []))
        # a commit of the checkout that is not THIS story's: the same re-ask, with its own reason
        run_entry(rig, s5=("TC-1",))
        code, out, started, _ = run_entry(rig, f"deployed {rig.old[:10]}", s5=("TC-1",))
        check_in("K36 a commit of the checkout but not this story's: the reason names this story's commit", f"but this story is commit {rig.head[:12]}", s0_question(rig.task_root))
        eq("K36 ... nothing recorded", rig.confirmations(), [])
        # CONTROLS: this story's own commit, abbreviated or whole, IS `deployed`
        for how in ("abbreviated", "whole", "upper case"):
            rig3 = Rig(profiles=("api",), real=True)
            try:
                spelling = {"abbreviated": rig3.head[:10], "whole": rig3.head, "upper case": rig3.head.upper()[:12]}[how]
                use_plan({"TC-1": ("api", "automate")})
                run_entry(rig3, s5=("TC-1",))
                code, out, started, _ = run_entry(rig3, f"deployed {spelling}", s5=("TC-1",))
                eq(f"K36 CONTROL: `deployed {spelling[:12]}` (this story's commit) is recorded and the stage goes on", (code, [r["kind"] for r in rig3.confirmations()]), (0, ["deployed"]))
            finally:
                rig3.done()
    finally:
        rig.done()


def main() -> None:
    run_scenarios([], [
        forms_reader,
        k35_the_question_and_its_texts,
        k36_deployed_always_confirm_retry,
        k36_method_answers,
        k36_mismatched_answers,
        k36_other_words_and_edges,
    ])
    harness.finish("test_story_run_stand_identity_k35_k36")


# split: runner piece 1
if __name__ == "__main__":
    main()
