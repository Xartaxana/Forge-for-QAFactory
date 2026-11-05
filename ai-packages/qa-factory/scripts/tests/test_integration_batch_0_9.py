#!/usr/bin/env python3
"""Pre-release 0.9, the package half of the integration small-work batch: key presence of its text items.

The items are documents and data rows with no test set of their own: the CHANGELOG lines, the three prose twins of the
report validator's note, the two rows of `design/state-exits.md`, the two debt rows, the critic handoff's verdict line,
the gate registry's probe row and the two config template keys. A key here is quoted from the batch's dispatch as it was
written before the run, never chosen after it. `--control` adds one key that is in no file: the run must fail (the
negative control of a key-presence witness: a script that cannot fail proves nothing); the same control also runs in
process, so the plain run proves the checker can fail.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, finish  # noqa: E402

PKG = harness.PLUGIN_ROOT


def read(rel: str) -> str:
    return (PKG / rel).read_text(encoding="utf-8")


def unreleased_of(text: str) -> str:
    """The newest release's section: from the first `## ` heading to the `## 0.8.1` one. It does not name the first
    heading, so renaming `## Unreleased` to `## 0.9.0` on release day leaves this test green (F3)."""
    start = text.index("\n## ") + 1
    return text[start:text.index("\n## 0.8.1", start)]


def unreleased() -> str:
    return unreleased_of(read("CHANGELOG.md"))


# One tag per merged node of the carrier's CHANGELOG item; the tag is the node's own mark at the end of its line.
NODE_TAGS = ("(B-373 a)", "(B-373 b)", "(B-373 c, D-0028)", "(B-409)", "(B-413)", "(B-404)", "(B-408)", "(B-415)",
             "(B-411)", "(B-410)", "(B-361, the", "(B-407 D)", "(B-407 B-run)", "(B-405/B-406)", "(B-364)", "(B-412)",
             "(B-414, D-0029", "(B-416)", "(B-407 A)", "(B-407 A-map)", "(B-407 C)", "(B-407 B-report)")
TWIN_SENTENCE = "is NOTED to the author, never refused"
TWINS = ("references/artifact-contract-json.md", "references/artifact-contract-results.md",
         "references/slices/qa-doc-scribe/artifact-contract-results.md")


def keys() -> list:
    """(name, text it must be in, the needle). A needle is a literal."""
    changelog = unreleased()
    out = [(f"CHANGELOG names the node {tag}", changelog, tag) for tag in NODE_TAGS]
    out += [("CHANGELOG: the B-407 D line says what the price does (incomplete, never agrees)", changelog,
             "the price then reads `incomplete`"),
            ("CHANGELOG: B-364 one command with one trigger on both paths", changelog,
             "Ticket `freshness` is one command with one trigger on both paths"),
            ("CHANGELOG: B-364 the ticket_changed question", changelog, "The driver asks `ticket_changed` when the requirements moved")]
    out += [(f"twin {rel} says the validator NOTES a stage claim", read(rel), TWIN_SENTENCE) for rel in TWINS]
    exits = read("design/state-exits.md")
    out += [("state-exits has a row for the ticket_changed question", exits, "| the `ticket_changed` question"),
            ("state-exits has a row for the ticket_rework state", exits, "| `ticket_rework{}`")]
    debt = read("design/factory-rules-debt.md")
    out += [("debt :21 is narrowed, not closed", debt, "**narrowed 07.10 (B-373 c, D-0028)**"),
            ("debt :21 stays open until the live proof", debt, "Open until the live proof on a non-Python project"),
            ("debt :130 states the collect-error part", debt, "the collect-error part is residue")]
    out += [("the critic handoff's verdict line carries `incomplete`", read("handoffs/s5-critic-to-automator.yaml"),
             "verdict: <one of vocabulary.probe_verdicts - intended_failure|no_failure|wrong_location|not_executed|incomplete>"),
            ("the gate registry has the probe verdict row", read("references/gate-registry.json"), '"id": "probe_verdict"')]
    template = read("references/templates/config.json")
    out += [("template: cost.external_agent_forms", template, '"external_agent_forms": []'),
            ("template: run.dependency_files", template, '"dependency_files": []')]
    detectors = read("references/detectors.json")
    out += [(f"detectors.json skip_markers carries {word}", detectors, needle)
            for word, needle in (("it.skip(", '"\\\\bit\\\\.skip\\\\("'), ("[Ignore]", '"\\\\[Ignore\\\\b"'),
                                 ("t.Skip(", '"\\\\bt\\\\.Skip\\\\("'))]
    slow_list = read("scripts/slow_tests.json")
    # `test_story_run_monorepo.py` was a third name here until the nightly measurement of 2026-10-23 (1.4 s, under the 5 s fast
    # threshold): the ratchet's own `--update` takes a listed file out when it measures fast, so the list is no place to pin it.
    out += [(f"slow_tests.json lists {name}", slow_list, f'"{name}":') for name in
            ("test_stand_gap_carry.py", "test_story_run_freshness.py")]
    return out


def failing(rows: list) -> list:
    return [name for name, haystack, needle in rows if needle not in haystack]


def structure() -> None:
    """What a needle cannot say: the template and the keys table agree, each node is named once, the data is JSON."""
    changelog = unreleased()
    check_eq("no node is named twice", {t: changelog.count(t) for t in NODE_TAGS if changelog.count(t) != 1}, {})
    check("the CHANGELOG lines carry no Cyrillic", re.search(f"[{chr(0x400)}-{chr(0x4ff)}]", changelog) is None)   # code points: no Cyrillic in the package (FR-30)
    check("the B-407 D line does not promise a range the price does not print", "a range, never one figure" not in changelog)
    flat = " ".join(changelog.split())      # a line wrapped inside a phrase is still the phrase
    check("F1: the B-407 A line does not say the handoff excludes `*Tests.cs` or `Tests/` in any case (the agree rule keeps "
          "a name or a folder alone as a row)", "`*Tests.cs`, `Tests/` and `docs/` in any case" not in flat
          and "ALONE keeps the row" in flat)
    check("F1: the B-416 line does not read as a 5 MB total", "5 files, 5 MB at most" not in flat
          and "each at most 5 MB" in flat)
    renamed = read("CHANGELOG.md").replace("## Unreleased", "## 0.9.0", 1)
    check_eq("F3: the section is found when the release renames `## Unreleased` to a version heading",
             re.match(r"## \d+\.\d+\.\d+", unreleased_of(renamed)) is not None, True)
    gates = read("references/gate-registry.json")
    # HF2-10 Part B (t-091, spec B-K1/B-K3): the collect is taken ONCE per request and an unreadable, timed-out or absent
    # one is named as not verified while the run decides; this supersedes the 0.9 wording «a collect error is noted as
    # "collect failed: ..." and is not named as not verified». The 0.9 negative stays: no import error / collect error pair.
    check("F4: collected_ids.decides says an unreadable, timed-out or absent collect is named as not verified and the run decides",
          "an unreadable, timed-out or absent collect are named as not verified and the run goes on" in gates
          and "an import error or a collect error is named" not in gates)
    template = json.loads(read("references/templates/config.json"))
    table = json.loads(read("references/config-keys.json"))
    check_eq("template: cost.external_agent_forms and run.dependency_files are empty lists",
             (template["cost"]["external_agent_forms"], template["run"]["dependency_files"]), ([], []))
    check_eq("config-keys: a row for each of the two keys, since 0.9.0, a missing key is a default",
             [table["keys"][k] for k in ("cost.external_agent_forms", "run.dependency_files")],
             [{"since": "0.9.0", "absent_means": "default"}] * 2)
    check("each note says a config without the key behaves as before",
          all("behaves as before" in text for text in (template["cost"]["note"], template["run_dependency_files_note"])))
    check_eq("config-keys: the cost.note history ends with the template's text, the new note's history is the template's",
             (table["notes"]["cost.note"]["note_history"][-1], table["notes"]["run_dependency_files_note"]["note_history"]),
             (template["cost"]["note"], [template["run_dependency_files_note"]]))
    registry = {row["id"]: row for row in json.loads(read("references/gate-registry.json"))["rows"]}
    row = registry.get("probe_verdict") or {}
    check_eq("the probe row maps the five words of vocabulary.yaml's probe_verdicts",
             sorted(row.get("words", [])), ["incomplete", "intended_failure", "no_failure", "not_executed", "wrong_location"])


def main() -> None:
    rows = keys()
    check_eq("every key of the batch's text items is present", failing(rows), [])
    absent = ("NEGATIVE CONTROL: a sentence that is in no file", read("CHANGELOG.md"), "this sentence is in no file of the package")
    check_eq("NEGATIVE CONTROL: one key deliberately absent -> the checker reports exactly that key",
             failing(rows + [absent]), [absent[0]])
    structure()
    if "--control" in sys.argv:
        check("NEGATIVE CONTROL (run form): the run with the absent key must fail", not failing(rows + [absent]),
              f"missing: {failing(rows + [absent])}")
    finish("test_integration_batch_0_9")


if __name__ == "__main__":
    main()
