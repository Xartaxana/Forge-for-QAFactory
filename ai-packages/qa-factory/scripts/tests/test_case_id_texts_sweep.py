#!/usr/bin/env python3
"""t-069 (B-013 analogs): the role-read texts that still taught the old `TC-NNN` case id shape.

The comparison run is on a project whose case ids look like `TP1-13797_TC_001`
(config.case_id_form). t-068 moved the designer's brief, card, charter and the case-file section
of the contract to `<case id>` plus "in the form your brief names"; this file is the same sweep
over the remaining texts a role or a person reads, and a grep-style guard so the shape does not
come back.

Keys, written before the first run:
  S1  none of the owned texts carries `TC-NNN` as a shape (also `<TC-`, `<TC>`, `TC-*` and the
      `<TC-id>` spelling). Markdown is read whole; a .py file is read as its string constants and
      docstrings (what a role or a person is shown), never as comments (they explain code).
  S2  `<case id>` is present in agents/qa-automator.md and in references/artifact-contract-automation.md;
      qa-automator.md also says the id is in the form the brief names.
  S3  NEGATIVE control: a fixture text containing `TC-NNN` fails the scanner; a clean one and a
      .py fixture whose only `TC-NNN` is in a comment do not.
  S4  the slices generated from the owned references carry no such shape either, and
      contract_slices reports nothing stale.
  S5  qa-automator's whole start load stays within the role_load threshold (role_load.static_load, tokens; the charter is
      one layer of it); the old 9000-byte per-file cap is retired (t-286, as K19 of
      test_case_id_form_texts.py), audit A22 bounds the whole start load.
  S6  conductor.md has the one row for the stray case file, mirroring s4.md.
Owned texts are listed once, below; a literal default-form example (`TC-001` in a labelled
example, a legacy `TC-012::` spelling) is not a shape and is not banned.
"""
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import contract_slices  # noqa: E402
from content_size import content_bytes  # noqa: E402

PLUGIN = harness.PLUGIN_ROOT

OWNED = (
    "agents/qa-automator.md",
    "references/artifact-contract-plan.md",
    "references/artifact-contract-automation.md",
    "references/external-writes.md",
    "references/conductor.md",
    "references/templates/requirements-register.md",
    "scripts/external_writes.py",
    "scripts/validate_artifacts.py",
    "scripts/judge_results.py",
    "scripts/brief_pack.py",
    "scripts/manifest_from_tests.py",
    "skills/qa-onboarding/phases/p1-discovery.md",
    "skills/qa-onboarding/phases/p2-interview.md",
)
SLICED = ("artifact-contract-plan.md", "artifact-contract-automation.md")

# The shapes a role must not be taught as THE id form.
SHAPE_RE = re.compile(r"TC-NNN|<TC-|<TC>|TC-\*")


def role_text(name: str, source: str) -> str:
    """What a role or a person reads out of a file: markdown whole, a .py file as its string
    constants (docstrings included), never its comments."""
    if not name.endswith(".py"):
        return source
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    return "\n".join(node.value for node in ast.walk(tree)
                     if isinstance(node, ast.Constant) and isinstance(node.value, str))


def shapes_in(name: str, source: str) -> list:
    return sorted(set(SHAPE_RE.findall(role_text(name, source))))


def read(rel: str) -> str:
    return (PLUGIN / rel).read_text(encoding="utf-8")


def main() -> None:
    # S1
    for rel in OWNED:
        check_eq(f"S1 {rel}: no TC-NNN / <TC-...> / TC-* shape", shapes_in(rel, read(rel)), [])

    # S2
    automator = read("agents/qa-automator.md")
    check_in("S2 qa-automator.md names <case id>", "<case id>", automator)
    check_in("S2 and says the id is in the form the brief names", "in the form your brief names", automator)
    check_in("S2 artifact-contract-automation.md names <case id>", "<case id>",
             read("references/artifact-contract-automation.md"))
    check_in("S2 the run command takes case ids, not TC-001", "run_suite.py --mine <case id>[,<case id>]", automator)

    # S3
    check("S3 NEGATIVE control: a markdown fixture with TC-NNN fails", shapes_in("x.md", "| `test-cases/<area>/TC-NNN.md` |") == ["TC-NNN"])
    check("S3 NEGATIVE control: `<TC-id>` and `TC-*` fail too",
          shapes_in("x.md", "extend:<TC-id> and files TC-*.md") == ["<TC-", "TC-*"])
    check("S3 NEGATIVE control: a .py fixture with TC-NNN in a string fails",
          shapes_in("x.py", 'MSG = "no TC-NNN marker"\n') == ["TC-NNN"])
    check("S3 NEGATIVE control: ... and in a docstring",
          shapes_in("x.py", 'def f():\n    """TC-NNN.md"""\n') == ["TC-NNN"])
    check_eq("S3 a clean markdown fixture passes", shapes_in("x.md", "| `<case id>.md` | TC-001 (default form) |"), [])
    check_eq("S3 a .py fixture whose only TC-NNN is a comment passes", shapes_in("x.py", "x = 1  # TC-NNN in a comment\n"), [])

    # S4
    for slice_dir in sorted((PLUGIN / "references" / "slices").iterdir()):
        for name in SLICED:
            path = slice_dir / name
            if path.is_file():
                rel = path.relative_to(PLUGIN).as_posix()
                check_eq(f"S4 {rel}: no such shape", shapes_in(rel, read(rel)), [])
    check_eq("S4 contract_slices reports no stale or missing slice", contract_slices.findings(PLUGIN), [])

    # S5
    size = content_bytes(PLUGIN / "agents/qa-automator.md")
    import role_load
    load = role_load.static_load("qa-automator", plugin_root=PLUGIN)
    check(f"S5 qa-automator's whole start load is within the role_load threshold ({load['tokens']} <= {load['threshold_tokens']} tokens)",
          load["verdict"] == "within", str(load["tokens"]))
    check("S5 the charter is a layer of that load", next(l["bytes"] for l in load["layers"] if l["name"] == "charter") == size)
    # negative control: the same verdict is `over` when the threshold sits below the load (a local, not a file)
    check("S5 control: a threshold below the load is refused", not (load["tokens"] <= load["tokens"] - 1))

    # S6
    conductor = read("references/conductor.md")
    check_in("S6 conductor.md: the stray case file row", "the one case-file deletion you may make", conductor)
    check_in("S6 it deletes the OLD file the refusal named, and nothing else", "delete each OLD file the refusal named and nothing else", conductor)
    check_in("S6 only once the new file exists, never the only copy", "only once the new file exists (never the only copy)", conductor)
    check_in("S6 a person's word removes nothing", "a person's word or `config.case_id_form` removes nothing", conductor)
    s4 = read("skills/qa-story/phases/s4.md")
    check_in("S6 the twin paragraph in s4.md is still there", "**A stray case file is yours to delete.**", s4)

    data = Path(__file__).read_bytes()
    check("FR-29 this file carries no 0x07/0x08/0x0b/0x0c byte", not any(b in data for b in (7, 8, 11, 12)))
    check("FR-30 this file is ASCII", all(b < 128 for b in data))
    harness.finish("test_case_id_texts_sweep")


if __name__ == "__main__":
    main()
