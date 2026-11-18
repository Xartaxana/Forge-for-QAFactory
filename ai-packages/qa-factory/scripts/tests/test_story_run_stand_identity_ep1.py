#!/usr/bin/env python3
"""ep1: a part of test_story_run_stand_identity.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_stand_identity_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import run_scenarios, d2_conductor_calls, d2_pipeline, eq, human_broken, set_control
from story_run_stand_identity_common import (  # noqa: E402
    DIGEST, HEAD, Rig, flag, line_broken, record, run_entry, sources_mismatched, unknown, use_plan,
)


CONTENT = "c" * 64


def fb8_with_identity(files, content=CONTENT, image=DIGEST) -> dict:
    rec = dict(sources_mismatched("api", files))
    if content:
        rec["content_identity"] = content
    if image:
        rec["observed_image"] = image
    return rec


def fb8_mismatched_sources_offers_test_as_is() -> None:
    """FB-8 (R13): the content-mismatch question offers `test as is` beside `retry` and `stop`, its text obeys the question rules and
    names the third door, and the packet carries the content the word will bind to and the image the probe read."""
    rig = Rig(profiles=("api",))
    try:
        driver = rig.driver()[0]
        person = driver.build_person("S5", "", "localhost", "api", fb8_with_identity(["Makefile"]), None, "mismatched_sources")
        packet = person.build_question
        eq("FB8 the answers", packet["answers"], ["retry", "test as is", "stop"])
        eq("FB8 the packet: the content fingerprint and the image the probe read", (packet["content"], packet["image"]), (CONTENT, DIGEST))
        check_in("FB8 the text names the third door", "`test as is`", person.text)
        check_in("FB8 ... and says the report will say it was the person's decision", "the report says the tests ran by your decision", person.text)
        check_not_in("FB8 ... and no longer says no door exists", "no way to test it as it is", person.text)
        eq("FB8 the text obeys human-questions.md", human_broken(person.text), [])
        bare = driver.build_person("S5", "", "localhost", "api", fb8_with_identity(["Makefile"], content="", image=""), None, "mismatched_sources")
        eq("FB8 a record with no identity: the packet says so (empty content, no image)", (bare.build_question["content"], bare.build_question["image"]), ("", ""))
        slots = driver.build_answer_slots(packet, "w", "")
        eq("FB8 the answer slots carry the content", slots["content"], CONTENT)
    finally:
        rig.done()


def fb8_test_as_is_runs_confirm_with_content() -> None:
    """FB-8 (K-door, R13, E20): `test as is` runs `confirm ... --content <identity> --image <image>` with the words whole; a packet
    without it among its answers (a question asked before this change) sends the words to the conductor and records nothing."""
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=fb8_with_identity(["Makefile"]))
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("FB8 the entry asks the content question, no role", (code, flag(rig).get("variant"), started), (3, "mismatched_sources", []))
        eq("FB8 the open packet offers `test as is`", "test as is" in flag(rig)["answers"], True)
        run_entry(rig, "test as is", s5=("TC-1",))
        eq("FB8 ONE line: kind content_accepted, this story's commit, the content, the image and the words whole",
           [(r["kind"], r["revision"], r["content"], r["image"], r["words"]) for r in rig.confirmations()],
           [("content_accepted", HEAD, CONTENT, DIGEST, "test as is")])
    finally:
        rig.done()
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=fb8_with_identity(["Makefile"], content=""))
        run_entry(rig, s5=("TC-1",))
        eq("FB8 (E20) the packet offers `test as is` although it carries no content",
           ("test as is" in flag(rig)["answers"], flag(rig).get("content")), (True, ""))
        run_entry(rig, "test as is", s5=("TC-1",))
        eq("FB8 (E20) an empty content never records a word nobody gave (`--content ''` reaches the CLI, which refuses): "
           "nothing recorded", rig.confirmations(), [])
    finally:
        rig.done()
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=fb8_with_identity(["Makefile"]))
        run_entry(rig, s5=("TC-1",))
        path = rig.task_root / "state" / "driver-state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["build_question"]["answers"] = ["retry", "stop"]          # a question asked before this change
        path.write_text(json.dumps(state), encoding="utf-8")
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        run_entry(rig, "test as is", s5=("TC-1",))
        eq("FB8 (E20) a packet that did not offer it: one conductor call, nothing recorded",
           (len(d2_conductor_calls(rig.root)), rig.confirmations()), (1, []))
    finally:
        rig.done()


def fb8_person_content_line_replaces_confirmed() -> None:
    """FB-8 (R16): the build-check line of a person-confirmed record of kind content_accepted is `person_content`, never the base
    `person_confirmed` / `person_confirmed_no_image` pair; the files are capped at the question's limit (5 at, 6 beyond)."""
    rig = Rig(profiles=("api",))
    try:
        driver = rig.driver()[0]

        def line_of(files, identity="person-confirmed:2026-10-03T09:30:00+00:00"):
            rec = record("api", "person_confirmed", observed_runtime_identity=identity, evidence_refs=[],
                         content_identity=CONTENT, accepted_files=files,
                         provenance={"technical_verification": False, "identity_kind": "person_confirmed"},
                         person_confirmation={"words": "test as is", "at": "2026-10-03T09:30:00+00:00", "task": rig.task,
                                              "kind": "content_accepted", "revision": HEAD, "content": CONTENT})
            return driver.build_outcome("S5", "", "localhost", "api", rec, "")
        names = [f"build/Makefile{n}" for n in range(1, 7)]
        text, person = line_of(names[:5])
        check_in("FB8 the line says it was tested as it is, by the person's word, with the date", "tested as it is by your word of 2026-10-03", text)
        check("FB8 five files: all named, none counted", all(f"`{n}`" in text for n in names[:5]) and "more" not in text, text)
        check_not_in("FB8 no base sentence (the build is not 'confirmed')", "the build is confirmed", text)
        six, _ = line_of(names, identity="image:sha256:" + "b" * 64)
        check("FB8 six files (and an image identity): five named and 'and 1 more'; the no-image sentence is still not used",
              f"`{names[5]}`" not in six and "and 1 more" in six and "no image was read" not in six, six)
        eq("FB8 it is a line, never a question; it obeys the rules", (person, line_broken(text)), (None, []))
    finally:
        rig.done()


def ep1_28_host_run_stand_asks_the_version() -> None:
    """EP1-28 (H-1, H-2, H-7): a stand whose application runs on the host (no container) reaches the build question on the
    manual half of S6, with no probe registered; a role-less repository pair says why in ONE line and asks nothing."""
    import runtime_probe
    import story_run
    app = {"repo_id": "app", "local_path": "ui", "role": "application", "execution_profile_id": "web"}
    tests = {"repo_id": "tests", "local_path": "ui-tests", "role": "tests", "execution_profile_id": "web"}

    def host_rig(*repos):
        rig = Rig(profiles=("web",), real=True, host=True)
        cfg = json.loads(rig.config_path.read_text(encoding="utf-8"))
        cfg["implementation_repos"] = [dict(r) for r in repos]
        cfg["execution"]["runtime_probes"] = {}
        rig.config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        use_plan({"TC-1": ("web", "manual-agent")})
        return rig
    saved = runtime_probe.containers
    runtime_probe.containers = lambda *a, **k: []
    rig = host_rig(app, tests)
    try:
        driver = rig.driver()[0]
        try:
            driver.build_check("S6", "manual", cases=["TC-1"])
            check("EP1-28 the MyBooks-shape fixture (web profile, application + tests repositories, no entry) asks", False)
        except story_run.Person as person:
            bq = person.build_question
            eq("EP1-28 the MyBooks-shape fixture reaches the `no_container` question, for the application's checkout",
               (bq["variant"], bq["profile"], bq["answers"]), ("no_container", "web", ["deployed", "retry", "command", "stop"]))
            check_in("EP1-28 the question says the application is not run by a container", "not run by a container I can read", person.text)
            check_not_in("EP1-28 docker names nothing: no docker line", "Docker runs", person.text)
            eq("EP1-28 the question obeys human-questions.md", human_broken(person.text), [])
    finally:
        rig.done()
    # same role twice: ONE line with the reason, no question, no probe
    rig = host_rig(dict(app, role="tests"), tests)
    try:
        driver = rig.driver()[0]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            driver.build_check("S6", "manual", cases=["TC-1"])
        text = out.getvalue()
        check_in("EP1-28 two repositories of one role: the line says why no probe could be worked out", "2 implementation repositories for profile web", text)
        check_in("EP1-28 ... and that nothing is asked", "nothing is asked of you", text)
        eq("EP1-28 ... it is a line and obeys the rules", line_broken(text.strip()), [])
        eq("EP1-28 ... no probe ran", rig.calls(), [])
        # F-1: S5 and the automation half keep the old line (no derived probe there)
        for stage, kind in (("S5", ""), ("S6", "automation")):
            use_plan({"TC-1": ("web", "automate")})
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                driver.build_check(stage, kind, cases=["TC-1"])
            check_in(f"EP1-28 F-1 {stage} {kind or 'window'}: the plain no-probe line", "is registered for the web tests, so it is not checked here", out.getvalue())
    finally:
        rig.done()
        runtime_probe.containers = saved
    # H-7: the docker line of the question
    rig = Rig(profiles=("web",))
    try:
        driver = rig.driver()[0]

        def text_with(containers):
            runtime_probe.containers = containers if callable(containers) else (lambda *a, **k: containers)
            try:
                return driver.build_person("S6", "manual", "localhost", "web", unknown("web", container=""), None, "no_container").text
            finally:
                runtime_probe.containers = saved
        check_not_in("EP1-28 H-7 no docker (OSError): no docker line, no error", "Docker runs", text_with(lambda *a, **k: (_ for _ in ()).throw(OSError("x"))))
        quiet = text_with([])
        check_not_in("EP1-28 H-7 docker runs nothing: no docker line", "Docker runs", quiet)
        check_in("EP1-28 H-7 ... and the paragraphs keep their one blank line", "is your call.\n\nWhat I need from you is one of these:", quiet)
        foreign = text_with([("proj-db-1", "postgres"), ("proj-mail-1", "mailpit")])
        check_in("EP1-28 H-7 foreign containers: named, with the invitation to say which", "Docker runs `proj-db-1`, `proj-mail-1` on this machine", foreign)
        check_in("EP1-28 H-7 ... `deployed` is still the person's word, offered as before", "(a) answer `deployed`", foreign)
        six = text_with([(f"c{n}", "img") for n in range(1, 7)])
        check("EP1-28 H-7 six containers: five named and a count", all(f"`c{n}`" in six for n in range(1, 6)) and "`c6`" not in six and "and 1 more" in six, six)
        five = text_with([(f"c{n}", "img") for n in range(1, 6)])
        check("EP1-28 H-7 five containers: all named, none counted", "`c5`" in five and "more on this machine" not in five, five)
        for label, text in (("foreign", foreign), ("six", six)):
            eq(f"EP1-28 H-7 {label}: the question obeys human-questions.md", human_broken(text), [])
    finally:
        rig.done()


def ep1_41c_the_stand_of_the_profile() -> None:
    """EP1-41c: `build_check` asks about the stand of the PROFILE (surfaces.stand_of_profile), not the story's `pipeline.environment`:
    on a mixed project the native profile's question names the device stand and the web profile's the API stand; a profile with no
    stand of its own is a line and no question; a project that names no `surface` reads the table 0 times and is asked as before."""
    import runtime_probe
    import story_run
    import surfaces
    device = {"name": "emulator", "surface": "android", "driver": {"url": "http://127.0.0.1:4723"}, "app": {"id": "com.example.app"}}
    api = {"name": "localhost", "base_url": "http://localhost:8080"}
    web_p, native_p = {"profile_id": "web", "capabilities": ["web"]}, {"profile_id": "android", "capabilities": ["native"]}
    saved = runtime_probe.containers
    runtime_probe.containers = lambda *a, **k: []

    def rig_of(environments, profiles, plan, selected="localhost", **records):
        rig = Rig(profiles=tuple(p["profile_id"] for p in profiles))
        cfg = json.loads(rig.config_path.read_text(encoding="utf-8"))
        cfg["environments"], cfg["profiles"] = [dict(e) for e in environments], [dict(p) for p in profiles]
        rig.config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        d2_pipeline(rig.task_root, environment=selected, environment_pending=False)       # the stand the story confirmed
        use_plan(plan)
        rig.records(**records)
        return rig

    def ask(driver, stage="S6", kind="manual", cases=("TC-1", "TC-2")):
        """(None, printed text) or (the Person's build_question, text)."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                driver.build_check(stage, kind, cases=list(cases))
            except story_run.Person as person:
                return person.build_question, out.getvalue()
        return None, out.getvalue()
    plan = {"TC-1": ("web", "manual-agent"), "TC-2": ("android", "manual-agent")}
    rig = None
    try:
        # a mixed project, two stands: the native profile asks about the device stand, the web profile about the API stand
        rig = rig_of([api, device], [web_p, native_p], plan, web=unknown("web", container=""), android=unknown("android", container=""))
        driver = rig.driver()[0]
        eq("41c mixed: the story's stand is the API stand (confirmed)", driver.pipeline().get("environment"), "localhost")
        bq, text = ask(driver, cases=("TC-2",))
        eq("41c mixed: the native profile's question is about the DEVICE stand, not `pipeline.environment`",
           (bq or {}).get("environment"), "emulator")
        eq("41c mixed: ...for the native profile, a question that obeys the rules", (bq["profile"], human_broken(bq["text"])), ("android", []))
        check_in("41c mixed: ...and the text names the device stand", "`emulator`", bq["text"])
        bq, text = ask(driver, cases=("TC-1",))
        eq("41c mixed: the web profile's question stays on the API stand", (bq or {}).get("environment"), "localhost")
        eq("41c mixed: the probe was told the profile's own stand", sorted(c["profile"] for c in rig.calls()), ["android", "web"])
        rig.done()
        # one stand only, and it is the device: the native profile asks about it; the web profile has no stand of its own
        rig = rig_of([device], [web_p, native_p], plan, selected="emulator", web=unknown("web", container=""),
                     android=unknown("android", container=""))
        driver = rig.driver()[0]
        bq, text = ask(driver, cases=("TC-2",))
        eq("41c one stand: the native profile asks about the only (device) stand", (bq or {}).get("environment"), "emulator")
        before = len(rig.calls())
        bq, text = ask(driver, cases=("TC-1",))
        check("41c one stand: the web profile has no stand of its own - a line, NO question, no probe run",
              bq is None and "web tests have no stand of their own" in text and len(rig.calls()) == before, text)
        eq("41c ... the line is a line and obeys the rules", line_broken(text.strip().splitlines()[-1]), [])
        check_not_in("41c ... and it names no flag or script", "story_run", text)
        rig.done()
        # two device stands: the one whose `surface` is the profile id
        tablet = dict(device, name="tablet", surface="ios")
        ios_p = {"profile_id": "ios", "capabilities": ["native"]}
        rig = rig_of([device, tablet], [native_p, ios_p], {"TC-1": ("android", "manual-agent"), "TC-2": ("ios", "manual-agent")},
                     selected="emulator", android=unknown("android", container=""), ios=unknown("ios", container=""))
        driver = rig.driver()[0]
        eq("41c two device stands: profile `android` -> the stand with surface android", (ask(driver, cases=("TC-1",))[0] or {}).get("environment"), "emulator")
        eq("41c two device stands: profile `ios` -> the stand with surface ios", (ask(driver, cases=("TC-2",))[0] or {}).get("environment"), "tablet")
        rig.done()
        other = {"profile_id": "mobile", "capabilities": ["native"]}
        rig = rig_of([device, tablet], [other], {"TC-1": ("mobile", "manual-agent")}, selected="emulator", mobile=unknown("mobile", container=""))
        driver = rig.driver()[0]
        bq, text = ask(driver, cases=("TC-1",))
        check("41c two device stands and no surface equal to the profile id: a line, no question (the stand is never guessed)",
              bq is None and "no stand of their own" in text and rig.calls() == [], text)
        rig.done()
        # the API stand is still pending: build_check returns at once - native is not asked either (the safe side)
        rig = rig_of([api, device], [web_p, native_p], plan, android=unknown("android", container=""))
        d2_pipeline(rig.task_root, environment="localhost", environment_pending=True)
        driver = rig.driver()[0]
        bq, text = ask(driver, cases=("TC-2",))
        eq("41c a pending story stand: no probe, no question, no line", (bq, text, rig.calls()), (None, "", []))
        rig.done()
        # a broken table is a line (the check broke), never a question and never a pass
        rig = rig_of([api, dict(device, surface="andriod")], [web_p, native_p], plan, android=unknown("android", container=""))
        driver = rig.driver()[0]
        bq, text = ask(driver, cases=("TC-2",))
        check("41c a `surface` the table lacks: one line says the check broke, no question", bq is None and "could not be checked" in text, text)
        rig.done()
        # a project that names no `surface`: the table is read 0 times and the question is about the story's stand as before
        reads = {"n": 0}
        real_rows = surfaces.rows
        surfaces.rows = lambda: (reads.__setitem__("n", reads["n"] + 1), real_rows())[1]
        try:
            rig = rig_of([api], [web_p], {"TC-1": ("web", "manual-agent")}, web=unknown("web", container=""))
            driver = rig.driver()[0]
            bq, text = ask(driver, cases=("TC-1",))
        finally:
            surfaces.rows = real_rows
        eq("41c a web config: the question is about the story's stand, the table was read 0 times",
           ((bq or {}).get("environment"), reads["n"]), ("localhost", 0))
    finally:
        runtime_probe.containers = saved
        if rig is not None:
            rig.done()


def ep1_41e_the_device_build_question() -> None:
    """EP1-41e: `how` on a record that says `device_stand` is the `device_build` question (chosen by the FIELD, before the container
    test); what it says the device holds and what voids the word follow what the probe could see (hash read / not read / no build
    read), so the promise of the question is always one the code can keep. The binding itself is proved in test_stand_identity.py."""
    import story_run
    rig = Rig(profiles=("android",))
    seen = "com.example.app 1.2.3 (42) sha256:" + "a" * 12
    ident = "image:sha256:" + "b" * 64
    try:
        driver = rig.driver()[0]

        def ask(**extra):
            rec = unknown("android", container="", device_stand=True, observed_runtime_identity=ident, **extra)
            line, person = driver.build_outcome("S6", "manual", "emulator", "android", rec, "")
            return line, person

        line, person = ask(observed_device_build=seen)
        bq = person.build_question
        eq("41e: a device record's `how` is the device_build question, with the four answers the no-container question has",
           (line, bq["variant"], bq["answers"]), ("", "device_build", ["deployed", "retry", "command", "stop"]))
        check_in("41e: it names the device stand", "on the device stand `emulator`", person.text)
        check_in("41e: it says what the device holds", f"The device has {seen}.", person.text)
        check_in("41e: with the file hashed, the promise is about the BUILD", "a different build on the device voids it;", person.text)
        check_not_in("41e: ...and says nothing of the container the no-container question speaks of", "container", person.text)
        eq("41e: ...it obeys human-questions.md", human_broken(person.text), [])
        eq("41e: ...and the word binds to the identity the probe read (the `{image}` of the executor)", bq["image"], ident)
        check_in("41e: the details file keeps what the check said", "stand `emulator`", person.details)
        # the hash could not be read: the promise narrows to the version
        _line, narrow = ask(observed_device_build="com.example.app 1.2.3 (42)",
                            limitation="the installed file was not hashed, so a rebuild with the same version is not seen")
        check_in("41e: hash unread: the promise is about the VERSION", "a different version on the device voids it;", narrow.text)
        check_not_in("41e: ...and no promise about a build is left in the text", "a different build", narrow.text)
        eq("41e: ...it obeys the rules", human_broken(narrow.text), [])
        # no build read at all (a platform with no way to read it): no promise that nothing can keep
        _line, blind = ask()
        check_in("41e: no build read: it says so", "I could not read which build is installed.", blind.text)
        check_not_in("41e: ...and promises nothing about a different build or version", "voids", blind.text)
        check_in("41e: ...the answers are still there", "(a) answer `deployed` if this build holds that commit; I take your word for this story only;", blind.text)
        # chosen by the field, before the container test; the other variants are unchanged
        rec = unknown("android", container="ui-c", device_stand=True, observed_device_build=seen)
        eq("41e: a device record with a container named is still the device question",
           driver.build_outcome("S6", "manual", "emulator", "android", rec, "")[1].build_question["variant"], "device_build")
        rec = unknown("android", container="", observed_device_build=seen)
        eq("41e: control: the same record without the field is the no-container question (the old road)",
           driver.build_outcome("S6", "manual", "emulator", "android", rec, "")[1].build_question["variant"], "no_container")
        rec = unknown("android", asks="confirm", device_stand=True, observed_device_build=seen)
        eq("41e: `confirm` on a device stand stays `confirm`",
           driver.build_outcome("S6", "manual", "emulator", "android", rec, "")[1].build_question["variant"], "confirm")
        rec = unknown("android", asks=None, device_stand=True, error="com.example.app is not installed on the device")
        line, person = driver.build_outcome("S6", "manual", "emulator", "android", rec, "")
        check("41e: an unreadable device build (no `asks_person`) is a line and no question", person is None and "com.example.app is not installed" in line, line)
        eq("41e: ...the line obeys the rules", line_broken(line), [])
        # a build line that breaks a rule of the questions falls back to plain words, never to the broken text
        _line, odd = ask(observed_device_build="com.example.app 1.2.3 (42) --flag build.py")
        eq("41e: a build line the rules do not allow in a question is said in plain words", (human_broken(odd.text), "build.py" in odd.text), ([], False))
        check_in("41e: ...and the details are not lost", "stand `emulator`", odd.details)
        data = SI_data()["question"]["variants"]["device_build"]
        check_eq_keys = {"device_has", "device_unread", "voids_build", "voids_version", "voids_unseen"} <= set(data)
        check("41e data: the variant carries the sentences it fills (FR-13: words are data)", check_eq_keys and story_run is not None)
    finally:
        rig.done()


def SI_data() -> dict:
    import stand_identity
    return stand_identity.data()


def main() -> None:
    run_scenarios([], [
        ep1_41e_the_device_build_question,
        ep1_41c_the_stand_of_the_profile,
        ep1_28_host_run_stand_asks_the_version,
        fb8_mismatched_sources_offers_test_as_is,
        fb8_test_as_is_runs_confirm_with_content,
        fb8_person_content_line_replaces_confirmed,
    ])
    harness.finish("test_story_run_stand_identity_ep1")


# split: runner piece 1
if __name__ == "__main__":
    main()
