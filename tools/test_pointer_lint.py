"""tools/pointer_lint.py as a table (FG7-52): ONE tmp git repo built once per module; a case writes some files, runs `main`,
and the working tree goes back to BASE. Expected values come from the card (D2-D4, E1-E14), not from the tool's output.
Run: python -m pytest tools/test_pointer_lint.py -q"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gitcmd  # noqa: E402
import pointer_lint as pl  # noqa: E402

REG = ["CLAUDE.md", "COORDINATOR.md", "docs/TESTING.md", ".claude/agents/critic.md", "CARRIER.md"]
RULES = "".join("### Rule %d%s\n\n" % (i, " · drafting → designer" if i == 2 else "") for i in range(1, 14))
BASE = {
    "docs/SIBLING_MAP.md": "# Map\n\n## Axis 31 — Role carriers\n\n| File | Owner / pointer |\n|---|---|\n" + "".join("| `%s` | owner |\n" % f for f in REG),
    "CLAUDE.md": "# C\n\n## Command hygiene (permission hygiene)\n\n1. a\n2. b\n3. c\n\n## The dispatch form (rule 11)\n\n11. DoD x\n\n## Worker duties\n",
    "COORDINATOR.md": ("# Coord\n\n## Contents — topic → where to read\n\n| Topic | Where |\n|---|---|\n| T | COORDINATOR.md § Tiers |\n"
                       "| R | COORDINATOR.md § Rule 2 · drafting → designer + COORDINATOR.md § 1 |\n| C | .claude/agents/critic.md § 21-24 |\n"
                       "| P | PROJECT.md § Сессия форджа |\n\n## Tiers (see x)\n\n1. Recon\n\n" + RULES + "11a. Question routing\n"),
    "PROJECT.md": "# P\n\n## Оглавление\n\n| Раздел | О чём |\n|---|---|\n| Сессия форджа | x |\n\n## Сессия форджа\n",
    ".claude/agents/critic.md": "# crit\n\n21. a\n22. b\n23. c\n24. d\n",
    "docs/TESTING.md": "# T\n", "CARRIER.md": "# carrier\n",
    "ai-packages/qa-factory/design/factory-rules.md": "".join("**FR-%d x\n" % i for i in range(1, 60)),
    "docs/OWNER_PRINCIPLES.md": "".join("- **P%d.** x\n" % i for i in range(1, 32)),
    "tools/gate.py": "CAP = 6\nWARN = 250000\n", "tools/x.py": "", "docs/a.md": "", "other/gone.md": "", "docs/файл.md": "",
    ".gitignore": "tools/dev.config.yaml\n",
}
PAIR = [("tools/gate.py::CAP", "CARRIER.md", r"more than (\w+) WRITING")]


@pytest.fixture(scope="module")
def repo(tmp_path_factory):
    root = tmp_path_factory.mktemp("pl")
    for rel, text in BASE.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    assert gitcmd.git(root, "init", "-q")[0] == 0 and gitcmd.git(root, "add", "-A")[0] == 0
    return root


def judge(repo, capsys, monkeypatch, edits, pairs=()):
    monkeypatch.setattr(pl, "NUMBER_PAIRS", list(pairs))
    try:
        for rel, text in edits.items():
            (repo / rel).write_text(text, encoding="utf-8")
        rc = pl.main(["--check", "--repo", str(repo)])
    finally:
        for rel in edits:
            if rel in BASE:
                (repo / rel).write_text(BASE[rel], encoding="utf-8")
            else:
                (repo / rel).unlink(missing_ok=True)
    return rc, capsys.readouterr().out


def C(text):
    return {"CARRIER.md": text}


def exempt(rows):
    return {pl.EXEMPT_FILE: json.dumps({"rows": rows})}


NOGONE = exempt({"CARRIER.md|docs/a.md": {"why": "x"}})
# (id, edits, pairs, expected exit, needles in stdout)
CASES = [
    ("base is green", {}, (), 0, ["ok ("]),
    # paths (E1-E6)
    ("rooted live, :line and ::symbol cut", C("`docs/a.md` `tools/x.py::f` `tools/x.py:12-14`"), (), 0, ["ok ("]),
    ("rooted deleted, namesake elsewhere", C("`docs/gone.md`"), (), 1, ["[P] docs/gone.md", "door:"]),
    ("bare suffix live", C("`x.py` and `gate.py`"), (), 0, ["ok ("]),
    ("bare name rescued by a namesake (known miss)", C("`gone.md`"), (), 0, ["ok ("]),
    ("../ past the root", C("`../../../x.md`"), (), 1, ["[P] ../../../x.md"]),
    ("../ from the carrier folder", C("`../docs/a.md`"), (), 1, ["[P] ../docs/a.md"]),
    ("placeholder, folder lives", C("`docs/<name>.md` `tools/*.py`"), (), 0, ["ok ("]),
    ("placeholder, folder gone", C("`nope/<name>.md`"), (), 1, ["[P] nope/<name>.md"]),
    ("non-path slash tokens", C("`origin/main` `forge/5/F5-2` https://x.org/a.md `/abs/p.md`"), (), 0, ["ok ("]),
    ("gitignored", C("`tools/dev.config.yaml`"), (), 0, ["ok ("]),
    ("exempt row", {**C("`docs/gone.md`"), **exempt({"CARRIER.md|docs/gone.md": {"why": "x"}})}, (), 0, ["ok ("]),
    ("in a fence", C("```\npython tools/no_such.py\n```"), (), 1, ["CARRIER.md:2: [P] tools/no_such.py"]),
    ("bare top/path outside backticks", C("see docs/gone2.md here"), (), 1, ["[P] docs/gone2.md"]),
    ("repo prefix, non-ASCII name", C("`C:/QAFactory/forge-repo/docs/a.md` `docs\\файл.md`"), (), 0, ["ok ("]),
    ("two-word span is judged by words", C("`python -B tools/no_such.py --check`"), (), 1, ["[P] tools/no_such.py"]),
    # ranges (E7)
    ("FR-1…FR-57 against 59", C("FR-1…FR-57"), (), 1, ["[R] FR-1…FR-57", "FR-59"]),
    ("FR-1…FR-59", C("FR-1…FR-59 and FR-4-FR-9"), (), 0, ["ok ("]),
    ("FR beyond the home", C("FR-50…FR-61"), (), 1, ["[R]"]),
    ("COORDINATOR.md rules 1-13", C("COORDINATOR.md rules 1-13"), (), 0, ["ok ("]),
    ("CLAUDE.md rules 1-13", C("`CLAUDE.md` rules 1-13"), (), 1, ["[R]", "item 1,2"]),
    ("enumeration is its union", C("COORDINATOR.md routing rules 1-10, 11a, 12, 13"), (), 0, ["ok ("]),
    ("enumeration short of the home", C("COORDINATOR.md rules 1-10, 11a"), (), 1, ["full-set claim"]),
    ("heading is not a claim", C("### P1–P9 OWNER_PRINCIPLES"), (), 0, ["ok ("]),
    ("P range with no home named (known miss)", C("P1–P23"), (), 0, ["ok ("]),
    ("P range, home named", C("OWNER_PRINCIPLES P1–P23"), (), 1, ["[R] P1–P23", "docs/OWNER_PRINCIPLES.md"]),
    ("P1–P31 with the home", C("OWNER_PRINCIPLES P1–P31"), (), 0, ["ok ("]),
    # the former STALE_ROWS of the role-carriers test
    *[("stale: " + t, C(t), (), 1, ["[A]" if "§" in t else "[R]"]) for t in [
        "see CLAUDE.md rule 3 for the gate", "`CLAUDE.md` rule 12, Cost gates", "CLAUDE.md routing rules 9", "CLAUDE.md § Tiers",
        "CLAUDE.md § Routing log", "CLAUDE.md § Contents", "CLAUDE.md § Role ≠ tier", "rule 10 of CLAUDE.md", "R13-g of CLAUDE.md",
        "| Critic gate | CLAUDE.md § 3 |", "| Cost gates | CLAUDE.md § Rule 12 · Cost gates |", "правило 3 `CLAUDE.md`", "правила 9 CLAUDE.md"]],
    *[("not stale: " + t, C(t), (), 0, ["ok ("]) for t in [
        "CLAUDE.md § 11", "rule 11 of CLAUDE.md", "toolkit/CLAUDE.md rule 10", "CLAUDE.md rule 11", "правило 11 `CLAUDE.md`",
        "COORDINATOR.md rule 3", "CLAUDE.md § Worker duties"]],
    ("a tools file citing a retired rule (rule kind over the wide set)", {"tools/x.py": "# see CLAUDE.md rule 3\n"}, (), 1, ["tools/x.py:1: [R]"]),
    # numbers (E8, E9)
    ("more than 4 against 6", C("more than 4 WRITING workers"), PAIR, 1, ["[N] more than 4 WRITING", "tools/gate.py::CAP = 6"]),
    ("a word is the same as its digit", C("more than Six WRITING, then шесть"), PAIR, 0, ["ok ("]),
    ("a Russian word", C("more than шесть WRITING"), PAIR, 0, ["ok ("]),
    ("the sentence is gone", C("nothing here"), PAIR, 1, ["[N]", "sentence is gone"]),
    ("an unknown word", C("more than lots WRITING"), PAIR, 1, ["[N] lots", "known number word"]),
    ("250K is 250000", C("WARN 250K"), [("tools/gate.py::WARN", "CARRIER.md", r"WARN (\d+K)")], 0, ["ok ("]),
    ("a gate number with no pair (known miss)", C("more than 4 WRITING workers"), (), 0, ["ok ("]),
    # anchors (the TOC tables)
    ("item 23 removed from § 21-24", {".claude/agents/critic.md": "# crit\n\n21. a\n22. b\n24. d\n"}, (), 1, ["[A] .claude/agents/critic.md § 21-24"]),
    ("renamed heading in PROJECT.md", {"PROJECT.md": BASE["PROJECT.md"].replace("## Сессия", "## Сеанс")}, (), 1, ["[A] PROJECT.md § Сессия форджа"]),
    ("a TOC file that is not tracked", {"COORDINATOR.md": BASE["COORDINATOR.md"].replace("critic.md § 21", "critic2.md § 21")}, (), 1, ["the file is not tracked"]),
    # exemptions (D4, E14)
    ("exempt row, token gone", exempt({"CARRIER.md|docs/gone.md": {"why": "x"}}), (), 1, ["[X]", "token left the carrier"]),
    ("exempt row, the path now resolves", {**C("`docs/a.md`"), **NOGONE}, (), 1, ["[X]", "resolves without the row"]),
    ("exempt row, empty why", {**C("`docs/gone.md`"), **exempt({"CARRIER.md|docs/gone.md": {"why": " "}})}, (), 1, ["no why"]),
    # cannot judge (E13)
    ("register without the table", {"docs/SIBLING_MAP.md": "# Map\n"}, (), 2, ["cannot judge", "control documents"]),
    ("a home with no openers", {"docs/OWNER_PRINCIPLES.md": "none\n"}, (), 2, ["no openers"]),
    ("a constant that is absent", {}, [("tools/gate.py::NOPE", "CARRIER.md", "x (1)")], 2, ["constant"]),
    ("malformed exemption json", {pl.EXEMPT_FILE: "{"}, (), 2, ["malformed"]),
    ("register row names a missing file", {"docs/SIBLING_MAP.md": BASE["docs/SIBLING_MAP.md"] + "| `docs/none.md` | owner |\n"}, (), 1, ["docs/none.md"]),
]


@pytest.mark.parametrize("edits,pairs,rc,needles", [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_pointer_lint(repo, capsys, monkeypatch, edits, pairs, rc, needles):
    got, out = judge(repo, capsys, monkeypatch, edits, pairs)
    assert got == rc and all(n in out for n in needles), out


def test_main_documents_is_the_one_reader(repo):
    absent = []
    assert pl.main_documents(repo, absent) == sorted(REG) and absent == []
