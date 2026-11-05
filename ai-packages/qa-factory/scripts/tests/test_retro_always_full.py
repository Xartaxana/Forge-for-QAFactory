"""GW1-3 (B-271): the retro is always the full one - no road writes `retro_mode` numbers or skip.

Keys K1-K7 of docs/tasks/specs/t-700-gw1-3-gate-b-words.md: the stage_done refusal and its door, the SETTABLE lexicon, the CLI
on a seeded story (bytes unchanged after a refusal), the conductor prompt, and the text of conductor.md / s8.md / s9.md / the
retro analyst. The text checker has its negative control (K7). Never launches a real `claude -p`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402

PKG = harness.PLUGIN_ROOT
sys.path.insert(0, str(harness.SCRIPTS))
CONDUCTOR = PKG / "references" / "conductor.md"
S8 = PKG / "skills" / "qa-story" / "phases" / "s8.md"
S9 = PKG / "skills" / "qa-story" / "phases" / "s9.md"
RETRO = PKG / "agents" / "qa-retro-analyst.md"
YAML = PKG / "handoffs" / "s8-scribe-to-gate-b.yaml"
FRAGMENT = PKG / "changelog.d" / "release-next-1-gw1-3.md"
CHANGELOG = PKG / "CHANGELOG.md"
RELEASE_HEADING = "## 0.10.9 "          # the section the release step folded the fragment into

# the conductor row 28 as it stood before this node (a literal copy: the negative control of K6a)
OLD_ROW_28 = ("| The retro they asked for by name (`numbers` / `skip`) | `stage_done.py --task <T> --set "
              "retro_mode=numbers\\|skip`; silence or anything else stays `full` |")


def text_problems(name: str, text, must: tuple = (), must_not: tuple = ()) -> list:
    """The failures of one text against its keys; a text that could not be read (None) is a failure naming the file (E10)."""
    if text is None:
        return [f"{name}: file missing or unreadable"]
    return ([f"{name}: lacks {n!r}" for n in must if n not in text]
            + [f"{name}: still has {n!r}" for n in must_not if n in text])


def read(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def k1_k2_k3() -> None:
    import stage_done
    for v in ("numbers", "skip", " NUMBERS ", "Skip"):
        try:
            stage_done.coerce_value("retro_mode", v)
            check(f"K1 {v!r} refused", False, "no ValueError")
        except ValueError as err:
            msg = str(err)
            check(f"K1 {v!r} refused with the door", "always the full one" in msg and "--remark --stage S9" in msg, msg)
            check(f"K1 {v!r} says where the words go, not the report",
                  "the gate B packet and the MR's open items carry them" in msg and "the report carries" not in msg, msg)
    import person_words
    # K3 (fix round): the door is the renderer's, byte-equal to the text it replaced
    by_hand = "waiver.py --task <T> --remark --stage S9 --words-file <file>"
    check("K3 person_words.door == the hand-written door",
          person_words.door("waiver.py --task <T> --remark --stage S9") == by_hand)
    try:
        stage_done.coerce_value("retro_mode", "skip")
    except ValueError as err:
        check("K3 the refusal carries the door whole", f"`{by_hand}`" in str(err), str(err))
    check("K2 full is accepted", stage_done.coerce_value("retro_mode", "full") == "full")
    check("K2 empty is None", stage_done.coerce_value("retro_mode", "") is None)
    check("K3 SETTABLE", stage_done.SETTABLE["retro_mode"] == ("full",), str(stage_done.SETTABLE["retro_mode"]))


def k4_cli() -> None:
    from story_run_common import seed
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        pipe = task_root / "pipeline.json"
        before = pipe.read_bytes()
        done = harness.run_script("stage_done.py", "--task", task, "--set", "retro_mode=skip", cwd=root, env=env)
        out = done.stdout + done.stderr
        check("K4 skip refused (exit non-zero)", done.returncode != 0, out)
        check("K4 pipeline.json bytes identical", pipe.read_bytes() == before)
        check("K4 the output names --remark", "--remark" in out, out)
        done = harness.run_script("stage_done.py", "--task", task, "--set", "retro_mode=full", cwd=root, env=env)
        check("K4 control: full exits 0", done.returncode == 0, done.stdout + done.stderr)
        import json
        check("K4 control: retro_mode == full", json.loads(pipe.read_text(encoding="utf-8")).get("retro_mode") == "full")
    finally:
        harness.cleanup(root)


def k5_prompt() -> None:
    import story_run
    text = story_run.Driver.generic_prompt("waiver", "S9", "q")
    check("K5 no retro_mode in the conductor prompt", "retro_mode" not in text)
    check("K5 control: the waiver road is named", "waiver.py --block/--remark" in text)


def k6_texts() -> None:
    cond, s8, s9, retro = read(CONDUCTOR), read(S8), read(S9), read(RETRO)
    problems = []
    problems += text_problems("conductor.md", cond,
                              ("Words asking to skip the retro or keep only its numbers",),
                              ("`stage_done.py --task <T> --set retro_mode=numbers", "and `--set retro_mode` record"))
    problems += text_problems("s8.md", s8,
                              ("**Words about the retro are not a choice.**", "It is\n     always the full retro (`retro_mode: full`)",
                               "which the gate B packet and the MR's open items carry",
                               "where no driver runs (this skill road),"),
                              ("retro_mode=full|numbers|skip", "skipped or cut", "numbers alone", "ilence is the full retro",
                               "The story ends with the retro", "with the waiver command its `fix` prints",
                               "which the report carries", "answer is recorded by the driver from"))
    problems += text_problems("s8-scribe-to-gate-b.yaml", read(YAML), ("the person's word that passes it is recorded by the conductor",),
                              ("with the waiver command its fix prints",))
    problems += text_problems("changelog fragment", release_note(), ("the gate B packet and the MR's open items carry",),
                              ("which the report carries",))
    problems += text_problems("s9.md", s9, ("## 0. The retro always runs in full", "never written from 0.10.9 on"),
                              ("unless the person said otherwise",))
    problems += text_problems("qa-retro-analyst.md", retro, ("on every story: the retro is always the full one",),
                              ("only when the human asked for the full retro", "unless the person asked in their own"))
    check("K6 texts (a-g)", not problems, "\n".join(problems))


def release_note(fragment: Path = FRAGMENT, changelog: Path = CHANGELOG):
    """The release-note text, from where it lives: the fragment before the release step, the 0.10.9 CHANGELOG section after it
    (the step deletes every fragment); None when neither carries it."""
    text = read(fragment)
    if text is not None:
        return text
    whole = read(changelog)
    if whole is None or RELEASE_HEADING not in whole:
        return None
    tail = whole.split(RELEASE_HEADING, 1)[1]
    return tail.split("\n## ", 1)[0]


def k7_negative_control() -> None:
    old = text_problems("conductor.md", OLD_ROW_28, (), ("`stage_done.py --task <T> --set retro_mode=numbers",))
    check("K7 the checker fails on the old conductor row", len(old) == 1, str(old))
    bad_s8 = text_problems("s8.md", "x numbers alone y", (), ("numbers alone",))
    check("K7 the checker fails on an s8 text with `numbers alone`", len(bad_s8) == 1, str(bad_s8))
    nowhere = release_note(PKG / "changelog.d" / "no-such.md", PKG / "references" / "no-such-file.md")
    check("K7 a release note found in neither the fragment nor CHANGELOG.md fails the check",
          len(text_problems("changelog fragment", nowhere, ("x",))) == 1 and nowhere is None, str(nowhere))
    missing = text_problems("gone.md", read(PKG / "references" / "no-such-file.md"), ("x",))
    check("K7 a missing file is a failure naming it", len(missing) == 1 and "gone.md" in missing[0], str(missing))


def main() -> None:
    k1_k2_k3()
    k4_cli()
    k5_prompt()
    k6_texts()
    k7_negative_control()
    harness.finish("test_retro_always_full")


if __name__ == "__main__":
    main()
