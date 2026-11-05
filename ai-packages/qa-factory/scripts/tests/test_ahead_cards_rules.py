#!/usr/bin/env python3
"""The rules an S3/S4 role is judged by stand in its card, before its first attempt (t-1685 N3-1, N3-3, N3-5).

A1/A2 the strategist and designer cards hold the rules the exits judge; A3 the sentences that moved are absent from the
charter (one place); A4 a built S4 designer brief carries the card line, with its negative control; A5 the case twins
hold ONE basis rule, read against the grammar's own regex. V1 (N3-5) the uncommitted count of the test repository leaves
out the factory's own folder and nothing else. (The file name is the spec's; V1 sits here because it is this node's
second test file's neighbour in `owns`.)
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import PLUGIN_ROOT, check, check_eq, check_in, check_not_in, finish  # noqa: E402

sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import brief_pack  # noqa: E402
import gate_preflight  # noqa: E402
import grammar as G  # noqa: E402

CARDS = json.loads((PLUGIN_ROOT / "references" / "ahead-cards.json").read_text(encoding="utf-8"))["cards"]
DESIGNER, STRATEGIST, CRITIC = "qa-case-designer", "qa-test-strategist", "qa-case-critic"
ROW_LINE = "One case per plan row, an `unverifiable` row too"
BASIS_HEADING = "## A case's basis"


def charter(role: str) -> str:
    return (PLUGIN_ROOT / "agents" / f"{role}.md").read_text(encoding="utf-8")


def a1_the_strategist_card_holds_the_branch_rule() -> None:
    text = CARDS[STRATEGIST]["text"]
    check_in("A1: sufficiency_review with its fields", "`sufficiency_review {author_dispatch_id, input_hash, rationale}`", text)
    check_in("A1: observation_contract", "`observation_contract`", text)
    check_in("A1: oracle_unknown false on a settling branch", "`oracle_unknown: false`", text)
    check_in("A1: oracle_status resolved on a settling branch (t-1692 B4; planning_contract keeps an unresolved obligation unverified)", "`oracle_status: resolved`", text)


def a2_the_designer_card_holds_the_row_and_key_rules() -> None:
    text = CARDS[DESIGNER]["text"]
    check_in("A2: one case per plan row, unverifiable included", ROW_LINE, text)
    check_in("A2: the readiness id of a question", "requirements-readiness.json", text)
    check_in("A2: now / before, never letters", "`now` / `before`", text)


def a3_the_moved_sentences_are_absent_from_the_charters() -> None:
    designer = charter(DESIGNER)
    check_not_in("A3: the designer charter no longer holds the now/before key rule", "never by letter", designer)
    check_in("A3: and keeps 'One case per plan row' (the card adds the unverifiable case; X1 charter wording, capitalised)", "One case per plan row", designer)
    strategist = charter(STRATEGIST)
    if "Each letter branch of a row whose only open question is Q" in strategist:
        # N2 owns that file; its pointer lands in the same text as N2-5 and the integrator checks the pair. Said, not hidden.
        print("NOTE A3 (strategist): the charter still holds the old branch sentence - N2's pointer has not landed in this tree")
    else:
        check_in("A3: the strategist charter points at the card", "the card's rule", strategist)


def built_designer_brief(card_text: str):
    """The S4 designer brief of a fixture story, built with the card `card_text` (None = the real one)."""
    root = harness.temp_project("qa-ahead-rules-")
    real = brief_pack.ahead_card
    try:
        harness.use_project(root)
        task = root / "qa-factory/artifacts/QA-9"
        (task / "work").mkdir(parents=True)
        (task / "pipeline.json").write_text(json.dumps(
            {"ticket": "QA-9", "size": "S", "environment": "local",
             "stages": {"S0": {"status": "done"}}, "gates": {}, "halts": []}), encoding="utf-8")
        if card_text is not None:
            brief_pack.ahead_card = lambda _role: card_text
        return brief_pack.build("QA-9", "S4", DESIGNER, "S4-qa-case-designer-1", write=False)["markdown"]
    finally:
        brief_pack.ahead_card = real
        shutil.rmtree(root, ignore_errors=True)


def a4_a_built_brief_carries_the_card_line() -> None:
    real = built_designer_brief(None)
    check_in("A4: the S4 designer brief holds the card line", ROW_LINE, real)
    stripped = CARDS[DESIGNER]["text"].replace(ROW_LINE, "")
    # negative control: the same assertion on a card copy without the line must fail, or the assertion cannot fail
    check("A4 NEGATIVE CONTROL: a brief built from a card without the line does not hold it", ROW_LINE not in built_designer_brief(stripped))


def basis_kinds_of_the_grammar() -> list:
    inner = re.match(r"^\^\((.*)\)\$$", G.ORACLE_RE.pattern).group(1)
    return [alt.split(":")[0] for alt in inner.split("|")]


def basis_section(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    at = text.find(BASIS_HEADING)
    return text[at:].split("\n<!--", 1)[0] if at >= 0 else ""


def a5_the_twins_hold_one_basis_rule() -> None:
    kinds = basis_kinds_of_the_grammar()
    source = basis_section(PLUGIN_ROOT / "references" / "vocabularies.md")
    listed = re.findall(r"`([a-z]+):", source.split("The plan row", 1)[0])
    check_eq("A5: the kinds the paragraph lists are the alternatives of grammar.ORACLE_RE", sorted(listed), sorted(kinds))
    check_eq("A5: six of them", len(kinds), 6)
    for role in (DESIGNER, CRITIC):
        got = basis_section(PLUGIN_ROOT / "references" / "slices" / role / "vocabularies.md")
        check(f"A5: the {role} slice holds the paragraph", got.strip() == source.strip(), got[:80])
    check_not_in("A5: the designer card no longer lists the kinds", "consistency:<where>", CARDS[DESIGNER]["text"])
    check_not_in("A5: and the critic card never did", "consistency:<where>", CARDS[CRITIC]["text"])
    check_in("A5: the paragraph says the plan oracle column is another field", "`oracle` column is another field", source)


def v1_the_vcs_count_leaves_out_the_factory_folder_only() -> None:
    out = gate_preflight.outside_factory_home
    lines = ["?? qa-factory/artifacts/x", " M qa-factory/records/journal.jsonl", "?? src/a.ts"]
    check_eq("V1: qa-factory/artifacts/x + src/a.ts -> the count is 1", out(lines, "qa-factory/"), ["?? src/a.ts"])
    check_eq("V1: an untracked folder shown as the folder itself is the factory's", out(["?? qa-factory/"], "qa-factory/"), [])
    check_eq("V1: a look-alike folder is the person's", out(["?? qa-factory-notes/a.md"], "qa-factory/"), ["?? qa-factory-notes/a.md"])
    check_eq("V1: a rename out of the folder is kept", out(["R  qa-factory/a.md -> docs/a.md"], "qa-factory/"),
             ["R  qa-factory/a.md -> docs/a.md"])
    check_eq("V1: a rename inside the folder is the factory's", out(["R  qa-factory/a.md -> qa-factory/b.md"], "qa-factory/"), [])
    check_eq("V1: with no home known every line is counted (error toward counted)", out(lines, ""), lines)
    check_eq("V1: nothing to count, nothing returned", out([], "qa-factory/"), [])
    pp = gate_preflight.porcelain_path
    check_eq("V1: the first line, stripped by _git (`M src/a.ts`), keeps its whole path", pp("M src/a.ts"), "src/a.ts")
    check_eq("V1: an unstripped ` M src/a.ts` gives the same path", pp(" M src/a.ts"), "src/a.ts")
    check_eq("V1: an untracked line", pp("?? src/b.ts"), "src/b.ts")
    check_eq("V1: a path with a space inside keeps it", pp(" M my dir/a.ts"), "my dir/a.ts")
    check_eq("V1 (the old cut): line[3:] of the stripped first line lost a character", "M src/a.ts"[3:], "rc/a.ts")
    # end to end on a real working tree: the home is told relative to the top of the git tree
    tmp = Path(tempfile.mkdtemp(prefix="qa-vcs-"))
    try:
        project = tmp / "proj"
        (project / "qa-factory" / "artifacts").mkdir(parents=True)
        (project / "qa-factory" / "artifacts" / "x").write_text("1", encoding="utf-8")
        (project / "src").mkdir()
        (project / "src" / "a.ts").write_text("1", encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        home = gate_preflight._factory_home_in_repo(project, project)
        check_eq("V1: the home relative to the git top", home, "qa-factory/")
        status = gate_preflight._git(project, "status", "--porcelain", "-uall")
        check_eq("V1: on a real tree the count is 1", len(out(status.splitlines(), home)), 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    a1_the_strategist_card_holds_the_branch_rule()
    a2_the_designer_card_holds_the_row_and_key_rules()
    a3_the_moved_sentences_are_absent_from_the_charters()
    a4_a_built_brief_carries_the_card_line()
    a5_the_twins_hold_one_basis_rule()
    v1_the_vcs_count_leaves_out_the_factory_folder_only()
    finish("test_ahead_cards_rules")


if __name__ == "__main__":
    main()
