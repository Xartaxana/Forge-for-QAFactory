"""contract_slices.py — the role slices, on a synthetic plugin and on the shipped one.

The rules under test, each one a way a slice could lie to a role:
  a section reaches only the roles marked on its heading, and `all` reaches every reader;
  a `###` with no marker of its own stays with its `##`, a marked one leaves it;
  the lead is in every slice (a slice that opens mid-rule reads as a different document);
  a slice that is missing, stale, empty or orphaned is a finding, not a silent half-truth;
  a section whose **Writer** is a role that has a slice of that file cannot be dropped from
  it — that was the 0.7.7 defect this package closes (four roles writing fields out of
  documents nobody delivered to them);
  a marked subject is injected through slices only, never whole.

Runnable on its own: `python -B scripts/tests/test_contract_slices.py`.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    PLUGIN_ROOT, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir,
)

sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import contract_slices as CS  # noqa: E402

SOURCE = """# The subject

What this subject is.

## Manifest <!-- roles: qa-automator, qa-code-critic -->

**Writer** `qa-automator`. Fields: `a`, `b`.

### Deep detail

inherited by the manifest's readers.

### Critic only <!-- roles: qa-code-critic -->

the probe receipt.

## Everyone <!-- roles: all -->

shared law.

## Runner only <!-- roles: qa-runner -->

manual evidence.
"""


def fake_plugin(tmp: Path, roles: dict, source: str = SOURCE) -> Path:
    """A plugin root with one marked subject and an inject-map that asks for slices."""
    root = tmp / "plugin"
    (root / "references").mkdir(parents=True)
    (root / "references" / "subject.md").write_text(source, encoding="utf-8", newline="\n")
    (root / "references" / "inject-map.json").write_text(
        json.dumps({"common": [], "roles": roles}), encoding="utf-8", newline="\n")
    return root


def test_rendering() -> None:
    critic = CS.render("subject.md", "qa-code-critic", SOURCE)
    automator = CS.render("subject.md", "qa-automator", SOURCE)
    runner = CS.render("subject.md", "qa-runner", SOURCE)
    check_in("the lead is in every slice", "What this subject is.", runner)
    check_in("a marked section reaches its role", "Fields: `a`, `b`.", critic)
    check_in("an unmarked `###` stays with its `##`", "inherited by the manifest", automator)
    check_not_in("a marked `###` leaves its parent's other readers", "probe receipt", automator)
    check_in("and reaches the role it names", "probe receipt", critic)
    check_in("`all` reaches a role named on no other section", "shared law", runner)
    check_not_in("another role's section is not delivered", "manual evidence", critic)
    check_not_in("the marker itself is never injected", "<!-- roles:", automator)
    check_in("the slice names the source it was rendered from",
             "plugin:references/subject.md", automator.splitlines()[0])


def test_findings_and_write() -> None:
    tmp = temp_dir("qa-factory-slices-")
    try:
        roles = {"qa-automator": ["plugin:references/slices/qa-automator/subject.md"],
                 "qa-code-critic": ["plugin:references/slices/qa-code-critic/subject.md"]}
        root = fake_plugin(tmp, roles)
        check_in("BAD: a slice that was never generated is named as missing",
                 "missing", CS.findings(root))
        CS.write(root)
        check_eq("GOOD: after --write nothing is wrong", CS.findings(root), [])

        slice_path = root / "references" / "slices" / "qa-automator" / "subject.md"
        slice_path.write_text(slice_path.read_text(encoding="utf-8") + "\nhand-added line\n",
                              encoding="utf-8", newline="\n")
        check_in("BAD: a hand-edited slice is stale", "stale", CS.findings(root))
        CS.write(root)
        check_eq("and --write restores it from the source", CS.findings(root), [])

        (root / "references" / "slices" / "qa-scout").mkdir(parents=True)
        (root / "references" / "slices" / "qa-scout" / "subject.md").write_text(
            "left behind", encoding="utf-8", newline="\n")
        check_in("BAD: a slice no role is injected is an orphan", "no role is injected",
                 CS.findings(root))
        cleanup(root / "references" / "slices" / "qa-scout")

        # The writer of an artifact must be injected the section that defines it.
        moved = SOURCE.replace("## Manifest <!-- roles: qa-automator, qa-code-critic -->",
                               "## Manifest <!-- roles: qa-code-critic -->")
        (root / "references" / "subject.md").write_text(moved, encoding="utf-8", newline="\n")
        CS.write(root)
        found = CS.findings(root)
        check_in("BAD: the role named **Writer** cannot be left out of its own slice",
                 "**Writer**", found)
        check_in("and the finding names the role and the section", "qa-automator", found)

        # A marked subject is delivered through slices only.
        (root / "references" / "subject.md").write_text(SOURCE, encoding="utf-8", newline="\n")
        direct = dict(roles, **{"qa-runner": ["plugin:references/subject.md"]})
        (root / "references" / "inject-map.json").write_text(
            json.dumps({"common": [], "roles": direct}), encoding="utf-8", newline="\n")
        CS.write(root)
        check_in("BAD: a marked subject injected whole is refused with the entry to write",
                 "plugin:references/slices/qa-runner/subject.md", CS.findings(root))

        # A role in the map that no marker mentions would be handed a title and nothing else.
        (root / "references" / "subject.md").write_text(
            SOURCE.replace("## Everyone <!-- roles: all -->", "## Everyone <!-- roles: qa-runner -->"),
            encoding="utf-8", newline="\n")
        (root / "references" / "inject-map.json").write_text(json.dumps({"common": [], "roles": {
            "qa-doc-scribe": ["plugin:references/slices/qa-doc-scribe/subject.md"]}}),
            encoding="utf-8", newline="\n")
        CS.write(root)
        empty = [f for f in CS.findings(root) if "qa-doc-scribe" in f]
        check("BAD: a role marked on no section is named, not silently given a title",
              any("marked on no section" in f for f in empty), str(empty))
    finally:
        cleanup(tmp)


def test_shipped_package() -> None:
    """The package as it ships: every declared slice fresh, and every role's injection under
    A22's cap measured on the files the map really delivers."""
    check_eq("SHIPPED: every slice named in inject-map.json is present and fresh",
             CS.findings(PLUGIN_ROOT), [])
    declared = CS.targets(PLUGIN_ROOT)
    check("SHIPPED: the map delivers slices, not whole subjects, to the tight roles",
          {t["role"] for t in declared} >= {"qa-automator", "qa-code-critic", "qa-scout",
                                            "qa-requirements-tester", "qa-case-critic"},
          str(sorted({t["role"] for t in declared})))
    # The deferred injection findings of 0.7.7, as a test: these four roles write or cite
    # fields out of documents that used to reach nobody.
    owed = {("qa-code-critic", "artifact-contract-automation.md"),
            ("qa-failure-analyst", "artifact-contract-automation.md"),
            ("qa-case-critic", "case-lifecycle.md"),
            ("qa-doc-scribe", "coverage-design.md")}
    have = {(t["role"], t["subject"]) for t in declared}
    check_eq("SHIPPED: the four roles that wrote out of undelivered contracts now get them",
             sorted(owed - have), [])
    for role, subject, needle in (
            ("qa-code-critic", "artifact-contract-automation.md", "review_receipt_ref"),
            ("qa-code-critic", "artifact-contract-automation.md", "obligation_bindings"),
            ("qa-failure-analyst", "artifact-contract-automation.md", "`runs[]`"),
            ("qa-failure-analyst", "artifact-contract-automation.md", "instance_id"),
            ("qa-case-critic", "case-lifecycle.md", "## Gate A debts"),
            ("qa-doc-scribe", "coverage-design.md", "only reviewed coverage")):
        path = PLUGIN_ROOT / "references" / "slices" / role / subject
        check_in(f"SHIPPED: {role} is injected `{needle}`", needle,
                 path.read_text(encoding="utf-8") if path.exists() else "")


STRATEGIST_SLICE = PLUGIN_ROOT / "references" / "slices" / "qa-test-strategist" / "artifact-contract-plan.md"
PLAN_CONTRACT = PLUGIN_ROOT / "references" / "artifact-contract-plan.md"
# The sentence the plan contract carried before HF1-13: it named two vocabulary lists and no word, and the
# strategist (who may read only `references/`) could not open the file that holds them.
OLD_WORDS_SENTENCE = "Words:\n`vocabulary.grounding_labels`, `requirement_grounding_states`."


def reads_the_plugin_for_its_words(text: str) -> bool:
    """True when the text sends the role to a plugin file for the closed words: the `handoffs/` folder, or the bare
    `vocabulary.<list>` name with no value given (FR-15/AR-8: a role is handed its words, never a path it cannot open)."""
    return "handoffs/" in text or "vocabulary.grounding_labels" in text or "vocabulary.requirement_grounding_states" in text


def test_grounding_words() -> None:
    """HF1-13 (OH3-14 class): the plan contract hands the strategist the grounding WORDS, through the one vocabulary reader."""
    import handoff as H
    line = H.grounding_vocabulary_line()
    source = PLAN_CONTRACT.read_text(encoding="utf-8")
    shipped = STRATEGIST_SLICE.read_text(encoding="utf-8")
    check_in("WORDS: the contract source carries the generator's token, not a typed list", CS.GROUNDING_WORDS_TOKEN, source)
    check_not_in("WORDS: the source types no label by hand", "behaviour_change", source)
    check_in("WORDS: the strategist's slice holds the line `handoff.grounding_vocabulary_line` builds, whole", line, shipped)
    for name in ("grounding_labels", "requirement_grounding_states"):
        words = H.allowed(name)
        check(f"WORDS: `{name}` is non-empty in the shipped vocabulary (the control for the checks below)", bool(words))
        for word in words:
            check_in(f"WORDS: the slice names `{word}` ({name})", word, shipped)
    check_not_in("WORDS: the token never reaches the role", CS.GROUNDING_WORDS_TOKEN, shipped)
    check("WORDS: the slice names no plugin path outside references/ and no bare vocabulary list for the words",
          not reads_the_plugin_for_its_words(shipped), "handoffs/ or vocabulary.<list> in the slice")
    check_not_in("WORDS: the requirements tester's slice carries no word list (the section is the strategist's)",
                 "behaviour_change", CS.render("artifact-contract-plan.md", "qa-requirements-tester", source))

    # NEGATIVE CONTROL: the old sentence restored in the source FAILS the same predicate (a check that cannot fail is broken).
    new_sentence = source[source.index(CS.GROUNDING_WORDS_TOKEN):source.index("A plan row answers")]
    old_source = source.replace(new_sentence, OLD_WORDS_SENTENCE + " ")
    check("control: the old sentence is in the doctored source", OLD_WORDS_SENTENCE in old_source and old_source != source)
    check("control: a slice rendered from the old sentence FAILS the no-plugin-words predicate",
          reads_the_plugin_for_its_words(CS.render("artifact-contract-plan.md", "qa-test-strategist", old_source)))
    check("control: the slice rendered from the real source passes it",
          not reads_the_plugin_for_its_words(CS.render("artifact-contract-plan.md", "qa-test-strategist", source)))

    # ONE READER: the generator types no label of its own; its words come from the helper, so a vocabulary change is a
    # change of the slice and of nothing else.
    generator = Path(CS.__file__).read_text(encoding="utf-8")
    typed = [w for w in H.allowed("grounding_labels") + H.allowed("requirement_grounding_states")
             if f'"{w}"' in generator or f"'{w}'" in generator]
    check_eq("ONE READER: contract_slices.py holds no grounding word as a string literal", typed, [])
    check_in("ONE READER: the words come from `handoff.grounding_vocabulary_line`",
             "handoff.grounding_vocabulary_line()", generator)

    # THE RATCHET and the unreadable cases, on a synthetic plugin (the shipped slices are only read).
    tmp = temp_dir("qa-factory-slices-words-")
    real_vocabulary, real_allowed = H.vocabulary, H.allowed
    try:
        text = SOURCE.replace("shared law.", "shared law. Words: " + CS.GROUNDING_WORDS_TOKEN)
        root = fake_plugin(tmp, {"qa-runner": ["plugin:references/slices/qa-runner/subject.md"]}, text)
        CS.write(root)
        check_eq("GOOD: a token source and its slice are fresh after --write", CS.findings(root), [])
        out = (root / "references" / "slices" / "qa-runner" / "subject.md").read_text(encoding="utf-8")
        check_in("the written slice holds the helper's line", line, out)

        H.allowed = lambda name: real_allowed(name) + (["zz_new_word"] if name == "grounding_labels" else [])
        check_in("RATCHET: a word added to the vocabulary makes the slice stale until --write",
                 "stale", CS.findings(root))
        CS.write(root)
        check_eq("and --write brings it back", CS.findings(root), [])
        check_in("and the new word reached the slice", "zz_new_word",
                 (root / "references" / "slices" / "qa-runner" / "subject.md").read_text(encoding="utf-8"))
        H.allowed = real_allowed

        def gone():
            raise FileNotFoundError("vocabulary.yaml")

        H.vocabulary = gone
        unreadable = CS.render("subject.md", "qa-runner", text)
        check_in("UNREADABLE: no vocabulary -> the slice says NONE READABLE for the labels", "labels: NONE READABLE", unreadable)
        check_in("UNREADABLE: and for the requirement states", "requirement states: NONE READABLE", unreadable)
        check_not_in("UNREADABLE: the word is never left blank after `Words:`", "Words:  ", unreadable)
        check_in("UNREADABLE: and the stale committed slice is red, not silently kept", "stale", CS.findings(root))
        H.vocabulary = real_vocabulary

        sys.modules["handoff"], saved = None, sys.modules.get("handoff")     # an import that fails: the reader itself is broken
        try:
            broken = CS.grounding_words()
        finally:
            sys.modules["handoff"] = saved
        check_in("UNREADABLE: a reader that cannot be imported is declared, not blank", "NONE READABLE", broken)
    finally:
        H.vocabulary, H.allowed = real_vocabulary, real_allowed
        cleanup(tmp)


# --- SC1-9: the common rules are sliced per role ------------------------------------------------------------------------------

COMMON_SOURCE = PLUGIN_ROOT / "references" / "common-rules.md"
CORE = ("The witness contract", "Your handover: the form, then the digest line", "Real data in artifacts", "Language",
        "Cross-cutting rules carried from the factory's history", "Source lookups after grounding")
# Spec t-1765 X1-7: the four roles whose file is a charter are not handed these two sections (the charter's «When to ask» is
# their one road of a question, and their turn economy is the guard's refusal text). Every other role is, as before.
TURN_AND_HALTS = ("Turn economy", "Gates and halts — no questions in between")
SLIM_ROLES = ("qa-scout", "qa-requirements-tester", "qa-test-strategist", "qa-case-designer")
# Per role, the headings of its slice of common-rules.md beyond CORE - written out, one line per role, so that a rule
# that stops reaching a role which acts on it (A-K10) is a red line here and not a silent half-truth. The reasons are in
# the sections' markers (references/common-rules.md) and in the t-1252 spec table.
EXTRA = {
    "qa-scout": ("No writes to external systems", "What a path is relative to"),
    "qa-requirements-tester": ("No writes to external systems",),
    "qa-test-strategist": ("What a path is relative to",),
    "qa-case-designer": ("What a path is relative to",),
    "qa-case-critic": ("Your own test data",),
    "qa-automator": ("Quiet runs only, through the runner", "Your own test data", "What a path is relative to"),
    "qa-code-critic": ("Quiet runs only, through the runner", "Your own test data", "No writes to external systems",
                       "What a path is relative to"),
    "qa-runner": ("Quiet runs only, through the runner", "Your own test data", "No writes to external systems",
                  "What a path is relative to"),
    "qa-failure-analyst": ("Quiet runs only, through the runner", "Your own test data", "No writes to external systems",
                           "What a path is relative to"),
    "qa-bug-reporter": ("No writes to external systems", "What a path is relative to"),
    "qa-doc-scribe": ("No writes to external systems", "What a path is relative to"),
    "qa-retro-analyst": ("No writes to external systems", "What a path is relative to"),
}
NEVER_DELIVERED = ("Resolving the plugin root", "Runtime and discovery policy")
THIRTY_KB_RULE = "A whole read over 30 KB is blocked"


def squash(text: str) -> str:
    return " ".join(text.split())


def core_missing(text: str, slim: bool = False) -> list:
    """What a role's slice of the common rules lacks of the rules every role acts on (headings; for a role that is not
    SLIM also `Turn economy`, `Gates and halts` and the 30 KB rule, which lives in `Turn economy`)."""
    titles = [s.title for s in CS.parse(text)[1]]
    want = CORE if slim else TURN_AND_HALTS + CORE
    return [h for h in want if h not in titles] + ([] if slim or THIRTY_KB_RULE in squash(text) else [THIRTY_KB_RULE])


def slice_of(role: str) -> str:
    return (PLUGIN_ROOT / "references" / "slices" / role / "common-rules.md").read_text(encoding="utf-8")


def test_common_rules_slices() -> None:
    """A-K3 (every role gets the core, none gets the host-only sections) and A-K10 (no role loses a rule it uses)."""
    source = COMMON_SOURCE.read_text(encoding="utf-8")
    imap = json.loads((PLUGIN_ROOT / "references" / "inject-map.json").read_text(encoding="utf-8"))
    source_titles = [s.title for s in CS.parse(source)[1]]
    for gone in NEVER_DELIVERED:
        check(f"A-K3: the source still holds `{gone}` (the conductor and the skills read it)", gone in source_titles)
    check_eq("A-K10: the table names exactly the twelve roles of the map", sorted(EXTRA),
             sorted({t["role"] for t in CS.targets(PLUGIN_ROOT)}))
    for role in sorted(EXTRA):
        text = slice_of(role)
        slim = role in SLIM_ROLES
        check_eq(f"A-K3: {role}'s slice has every core rule", core_missing(text, slim), [])
        for gone in NEVER_DELIVERED:
            check_not_in(f"A-K3: {role}'s slice does not carry `{gone}`", gone, text)
        check_not_in(f"A-K3: {role}'s slice does not carry the host-only phrase", "Role files pin no model", text)
        titles = [s.title for s in CS.parse(text)[1]]
        check_eq(f"A-K10: {role}'s slice holds exactly its sections", sorted(titles),
                 sorted(CORE + (() if slim else TURN_AND_HALTS) + EXTRA[role]))
        check_eq(f"A-K10: {role}'s own list opens with its slice of the rules (who you are, how you work, then references)",
                 imap["roles"][role][0], f"plugin:references/slices/{role}/common-rules.md")
    for role in ("qa-test-strategist", "qa-case-designer", "qa-case-critic"):
        check_not_in(f"A-K3: {role} has no shell, so its slice names no `diff_pass`", "diff_pass", slice_of(role))
    check("A-K3: the failure analyst gets the test-data rule (it reads failures by their data)",
          "Your own test data" in [s.title for s in CS.parse(slice_of("qa-failure-analyst"))[1]])
    # The four charter roles lose the two sections; the case critic (S4's second role, byte for byte) and the others keep them.
    for role in SLIM_ROLES:
        for gone in TURN_AND_HALTS:
            check_not_in(f"X1-7: {role}'s slice does not carry `{gone}`", gone, slice_of(role))
    for kept in TURN_AND_HALTS:
        check_in(f"X1-7 control: qa-case-critic keeps `{kept}` (its slice is unchanged)", kept, slice_of("qa-case-critic"))
    # NEGATIVE control: the core check is red on a source where `Turn economy` is marked for one role only.
    doctored = source.replace("<!-- roles: qa-case-critic, qa-automator, qa-code-critic, qa-runner, qa-failure-analyst, "
                              "qa-bug-reporter, qa-doc-scribe, qa-retro-analyst -->\n## Turn economy",
                              "<!-- roles: qa-runner -->\n## Turn economy")
    check("A-K3 control: the doctored source differs", doctored != source)
    check_in("A-K3 NEGATIVE: the core check is red when `Turn economy` is not for every role that keeps it", "Turn economy",
             core_missing(CS.render("common-rules.md", "qa-automator", doctored)))
    check_eq("A-K3 control: and green on the shipped rendering of the same role",
             core_missing(CS.render("common-rules.md", "qa-automator", source)), [])
    # The common list holds the manifesto only; the rules are a slice (A-K1 reads the same fact in A22).
    check_eq("A-K1: `common` is the manifesto alone", imap["common"], ["plugin:references/tester-manifesto.md"])


def build_layer_tree(tmp: Path, source: str, roles=("qa-a", "qa-b")) -> Path:
    """A plugin root whose common list is one 100-byte manifesto and whose roles are handed a slice of `source`."""
    root = tmp / "plugin"
    (root / "references").mkdir(parents=True)
    (root / "references" / "m.md").write_text("m" * 99 + "\n", encoding="utf-8", newline="\n")
    (root / "references" / "common-rules.md").write_text(source, encoding="utf-8", newline="\n")
    (root / "references" / "inject-map.json").write_text(json.dumps({
        "common": ["plugin:references/m.md"],
        "roles": {r: [f"plugin:references/slices/{r}/common-rules.md"] for r in roles}}),
        encoding="utf-8", newline="\n")
    return root


LAYER_SOURCE = ("# Rules\n\nLead.\n\n"
                "<!-- roles: all -->\n## All\n\nshared line.\n\n"
                "<!-- roles: qa-a -->\n## Only A\n\nA only body here.\n\n"
                "<!-- roles: qa-b -->\n## Only B\n\nB only.\n")


def test_common_layer() -> None:
    """A-K9 (FR-28): the measurer of the layer every role gets alike, on a tree whose answer is known to the byte."""
    tmp = temp_dir("qa-factory-common-layer-")
    try:
        root = build_layer_tree(tmp, LAYER_SOURCE)
        CS.write(root)
        layer = CS.common_layer(root)
        # list: the manifesto, 100 B. shared rules: the lead (15 B: "# Rules\n\nLead.\n") + the `all` section
        # ("\n## All\n\nshared line.\n" = 22 B) = 37 B, WITHOUT the provenance line. Each role's slice also holds a
        # 131 B provenance line (it names the role) and its own section: A 30 B, B 20 B.
        check_eq("A-K9: the list is the manifesto's bytes", layer["list"], 100)
        check_eq("A-K9: shared = list + the lead and `all` sections, no provenance", layer["shared"], 137)
        check_eq("A-K9: per role = list + that role's own slice", layer["per_role"], {"qa-a": 298, "qa-b": 288})
        check_eq("A-K9: nothing went unmeasured", layer["errors"], [])
        check("A-K9: shared is not the minimum over roles (the 'min' measurer is wrong here)",
              layer["shared"] != min(layer["per_role"].values()))
        check("A-K9: and every role holds at least the shared bytes",
              all(v >= layer["shared"] for v in layer["per_role"].values()))
        shipped = CS.common_layer(PLUGIN_ROOT)
        check("A-K9: the shipped layer is measured (control)", shipped["shared"] > shipped["list"] > 0 and not shipped["errors"],
              str(shipped["errors"]))
        check("A-K9: and report() prints the same two numbers",
              f"list {shipped['list']:,} bytes, shared with every role {shipped['shared']:,} bytes" in CS.report(PLUGIN_ROOT))

        # unknown is not zero: the source gone while the map names its slices; a slice gone; a map nobody can read
        (root / "references" / "common-rules.md").unlink()
        gone = CS.common_layer(root)
        check("A-K9: a missing source is an error, not a zero", bool(gone["errors"]) and "common-rules.md" in gone["errors"][0],
              str(gone))
        check("A-K9: and report() says NOT MEASURED", "NOT MEASURED" in CS.report(root))
        (root / "references" / "common-rules.md").write_text(LAYER_SOURCE, encoding="utf-8", newline="\n")
        (root / "references" / "slices" / "qa-a" / "common-rules.md").unlink()
        check("A-K9: a missing slice is an error naming the role", any("qa-a" in e for e in CS.common_layer(root)["errors"]))
        (root / "references" / "inject-map.json").write_text("{not json", encoding="utf-8")
        check_eq("A-K9: an unreadable map measures nothing", CS.common_layer(root), {})
        # no common-layer slice in the map: nothing to add, nothing to complain about
        (root / "references" / "inject-map.json").write_text(json.dumps({"common": ["plugin:references/m.md"], "roles": {
            "qa-a": []}}), encoding="utf-8")
        check_eq("A-K9: a map with no common-rules slice has shared == list", CS.common_layer(root)["shared"], 100)
        # the catalogue never names the common-layer slice
        (root / "references" / "inject-map.json").write_text(json.dumps({"common": ["plugin:references/m.md"], "roles": {
            "qa-b": ["plugin:references/slices/qa-b/common-rules.md"]}}), encoding="utf-8")
        check_not_in("A-K2: the catalogue of a role skips its common-rules slice", "common-rules.md",
                     CS.catalogue(root, "qa-b"))
    finally:
        cleanup(tmp)


def test_cli() -> None:
    p = run_script("contract_slices.py", "--check")
    check("CLI: --check exits 0 on the shipped package", p.returncode == 0,
          (p.stdout + p.stderr)[-400:])
    p = run_script("contract_slices.py", "--selftest")
    check("CLI: --selftest exits 0", p.returncode == 0, (p.stdout + p.stderr)[-400:])
    p = run_script("contract_slices.py", "--report")
    check_in("CLI: --report prints the per-role weight", "qa-code-critic", p.stdout)


def test_plan_role_charter_line() -> None:
    """F-10: a role dispatched for the S5 plan as well as a window names no path and counts both units."""
    for role in ("qa-automator", "qa-code-critic"):
        line = CS.charter_line(PLUGIN_ROOT, role)
        check_in(f"F-10: {role} line covers the plan dispatch unit", "a plan dispatch: per case", line)
        check_not_in(f"F-10: {role} line names no artifact path", "`work/", line)
    other = CS.charter_line(PLUGIN_ROOT, "qa-bug-reporter")
    check_not_in("F-10 control: a role with one dispatch kind keeps its single line", "plan dispatch", other)
    text = (PLUGIN_ROOT / "agents" / "qa-automator.md").read_text(encoding="utf-8")
    check_not_in("F-10: the prose patch that contradicted the generated line is gone",
                 "Plan dispatch: one line per case", text)


def test_handoff_keys_pages() -> None:
    """X1-7: the generated key page of the four charter roles (`handoff_keys_page`): present, fresh, generated, and unknowns named."""
    roles = ("qa-scout", "qa-requirements-tester", "qa-test-strategist", "qa-case-designer")
    roles += ("qa-automator", "qa-code-critic")                       # X7-1
    roles += ("qa-case-critic",)                                      # T3a: the case critic has a page too
    # X7-3: the runner and the analyst have a key page too; their forms get the `tried` table in X7-7, so the table is checked for the four
    # X7-4: the reporter, the scribe and the retro analyst have one too
    x7_roles = ("qa-runner", "qa-failure-analyst", "qa-bug-reporter", "qa-doc-scribe", "qa-retro-analyst")
    check_eq("X1-7: the map names a key page for exactly the roles that have a slice", sorted({r for r, _e, _p in CS.keys_targets(PLUGIN_ROOT)}),     # a role with continuation pages is listed once per page
             sorted(roles + x7_roles))
    for role in x7_roles:
        page = (PLUGIN_ROOT / "references" / "slices" / role / CS.KEYS_NAME).read_text(encoding="utf-8")
        for anchor in ("## Outputs", "## Witness", "## Handoff form", "generated by scripts/contract_slices.py"):
            check_in(f"X7-3: {role}'s key page holds `{anchor}`", anchor, page)
    check_not_in("X1-7: `targets` never names a key page (no source file to cut it from)", CS.KEYS_NAME,
                 " ".join(t["subject"] for t in CS.targets(PLUGIN_ROOT)))
    for role in roles:
        page = (PLUGIN_ROOT / "references" / "slices" / role / CS.KEYS_NAME).read_text(encoding="utf-8")
        for anchor in ("## Outputs", "## Witness", "## Handoff form", "generated by scripts/contract_slices.py"):
            check_in(f"X1-7: {role}'s key page holds `{anchor}`", anchor, page)
        if role in ("qa-scout", "qa-requirements-tester", "qa-test-strategist", "qa-case-designer"):
            # the forms of S5-S9 get `tried` in X7-7 (handoff_check.TRIED_CONTRACTS); that node adds its roles to this tuple
            check_in(f"X1-7: {role}'s key page carries the tried table from its form", "`tried[].technique`", page)
            check_in(f"X1-7: {role}'s key page carries tried_note as optional", "`tried_note` (optional)", page)
    scout = (PLUGIN_ROOT / "references" / "slices" / "qa-scout" / CS.KEYS_NAME).read_text(encoding="utf-8")
    check_in("X1-7: the scout's page names the validator's keys (PHASE_JSON_KEYS)", "`acceptance_criteria`", scout)
    check_in("X1-7: the designer's page carries the token the case identity gate demands", "= the file name",
             (PLUGIN_ROOT / "references" / "slices" / "qa-case-designer" / CS.KEYS_NAME).read_text(encoding="utf-8"))
    check_in("X1-7: the tester's page carries the token the grounding gate demands", "derived",
             (PLUGIN_ROOT / "references" / "slices" / "qa-requirements-tester" / CS.KEYS_NAME).read_text(encoding="utf-8"))
    check_in("X1-7: the catalogue names the key page", CS.KEYS_NAME, CS.catalogue(PLUGIN_ROOT, "qa-scout"))
    unknown = CS.handoff_keys_page(PLUGIN_ROOT, "qa-nobody")
    check_in("X1-7 AR-28: a role in no stage is declared NOT KNOWN on its page, not given an empty one", "NOT KNOWN", unknown)
    tmp = temp_dir("qa-factory-keys-")
    try:
        root = tmp / "plugin"
        (root / "references").mkdir(parents=True)
        (root / "references" / "inject-map.json").write_text(json.dumps({"common": [], "roles": {
            "qa-scout": ["plugin:references/slices/qa-scout/handoff-keys.md"]}}), encoding="utf-8", newline="\n")
        (root / "references" / "stage-joints.json").write_text(json.dumps({"schema_version": 2, "when_exclusive": [], "joints": [], "told_ratchet": {
            "hand_cards": 0, "legacy_legs": 0, "unsited": 0}}), encoding="utf-8", newline="\n")    # T3a: the page reads the rows; no file is a red of its own
        check_in("BAD: a key page that was never generated is named as missing", "missing", " ".join(CS.keys_findings(root)))
        CS.keys_write(root)
        check_eq("GOOD: after the write nothing is wrong with the key page", CS.keys_findings(root), [])
        path = root / "references" / "slices" / "qa-scout" / CS.KEYS_NAME
        path.write_text(path.read_text(encoding="utf-8") + "hand-added\n", encoding="utf-8", newline="\n")
        check_in("BAD: a hand-edited key page is stale", "stale", " ".join(CS.keys_findings(root)))
        (root / "references" / "slices" / "qa-runner").mkdir(parents=True)
        (root / "references" / "slices" / "qa-runner" / CS.KEYS_NAME).write_text("left", encoding="utf-8", newline="\n")
        check_in("BAD: a key page no role is injected is an orphan", "no role is injected", " ".join(CS.keys_findings(root)))
    finally:
        cleanup(tmp)


def test_keys_through_load_rows() -> None:
    """T1b: `_keys_outputs` reads the rows through `stage_joints.load_rows` (AR-13) and the pages are what they were."""
    import stage_joints
    check_eq("keys/findings-clean: every generated key page of the shipped package is fresh (byte-identical after the rename)",
             CS.keys_findings(PLUGIN_ROOT), [])
    role, page = "qa-scout", "references/slices/qa-scout/handoff-keys.md"
    rows = {"joints": [{"producers": [{"roles": [role], "field": "a synthetic field", "demands": ["zz_demand_zz"],
                                       "told": [{"path": page}]}]}]}
    seen, saved = [], stage_joints.load_rows
    try:
        stage_joints.load_rows = lambda path=None: (seen.append(Path(path).name), (rows, ""))[1]
        lines = CS._keys_outputs(PLUGIN_ROOT, role, {"id": "S1"}, {})
        stage_joints.load_rows = lambda path=None: (None, "stage-joints.json cannot be read (OSError)")
        unread = CS._keys_outputs(PLUGIN_ROOT, role, {"id": "S1"}, {})
    finally:
        stage_joints.load_rows = saved
    check_eq("keys/through-load-rows: the page asks `load_rows` for the file", seen, ["stage-joints.json"])
    check_in("keys/through-load-rows: a row it returns reaches the page", "- a synthetic field: `zz_demand_zz`", "\n".join(lines))
    check_not_in("keys/through-load-rows: a file `load_rows` cannot read adds no demand line (as a lost file did before)", "zz_demand_zz", "\n".join(unread))


def test_ladder_one_carrier() -> None:
    """X7-0 (K-L1, K-L1b): the P28 decision and the P19 ladder live in the manifesto alone; roles refer to the rung."""
    manifesto = (PLUGIN_ROOT / "references" / "tester-manifesto.md").read_text(encoding="utf-8")
    check_in("K-L1: the manifesto decides what to automate first", "decided first", manifesto)
    check_in("K-L1: and the ladder answers only the level", "only at which level", manifesto)
    check_in("K-L1: the section is craft (kind marker directly above its heading)",
             "<!-- kind: craft -->\n## What to automate, and at which level", manifesto)
    ladder = "(1) an automated test"
    check_eq("K-L1b control: the manifesto carries the ladder once", manifesto.count(ladder), 1)
    others = [p for d in ("agents", "references") for p in sorted((PLUGIN_ROOT / d).rglob("*.md"))
              if p.name != "tester-manifesto.md"]
    check("K-L1b control: the scan sees files", len(others) > 20)
    retold = [str(p.relative_to(PLUGIN_ROOT)) for p in others if ladder in p.read_text(encoding="utf-8")]
    check_eq("K-L1b: no other agent or reference retells the ladder", retold, [])
    # NEGATIVE control: the same scan is red on a text that retells it.
    check("K-L1b NEGATIVE: a doctored file that retells the ladder is caught", ladder in (manifesto + "x"))


# --- T3a: the told section of the key page, the size rule, the inline set, K10 (rows a-j of the node) -----------------------------
WHEN_EXCLUSIVE = [["first_look", "not_first_look"], ["plan", "window"]]
GROUP_HEADINGS = ['### Only in a plan dispatch (replaces "Only in a window")',
                  '### Only in a window (replaced by "Only in a plan dispatch")',
                  "### Only in a manual block",
                  '### Only in a first look (replaces "Not in a first look")',
                  '### Not in a first look (replaced by "Only in a first look")',
                  "### Only in a walk"]


def told_row(check, roles=("qa-x",), stages=("S1",), when=None, text="A requirement.", door="d") -> dict:
    row = {"check": check, "stages": list(stages), "joint": None,
           "producers": [{"roles": list(roles), "field": "f", "told": [{"page": True}], "demands": []}],
           "requirement": text, "door": door}
    if when is not None:
        row["when"] = list(when)
    return row


def told_plugin(tmp: Path, rows=(), hand_cards=0, cards=None, lists=None, joints_text=None) -> Path:
    """A plugin root with the carriers the page reads: an inject-map listing `lists` (role -> page file names), two stages, the
    rows and the cards. `joints_text` replaces the rows file (a broken one)."""
    root = tmp / "plugin"
    refs = root / "references"
    refs.mkdir(parents=True, exist_ok=True)
    lists = lists or {"qa-x": ("handoff-keys.md",)}
    imap = {"common": [], "roles": {r: [f"plugin:references/slices/{r}/{p}" for p in pages] for r, pages in lists.items()}}
    (refs / "inject-map.json").write_text(json.dumps(imap), encoding="utf-8", newline="\n")
    stages = {"stages": [{"id": "S1", "roles": ["qa-x", "qa-y"], "required_outputs": []},
                         {"id": "S2", "roles": ["qa-y"], "required_outputs": []}], "witness": {}}
    (refs / "stages.json").write_text(json.dumps(stages), encoding="utf-8", newline="\n")
    joints = {"schema_version": 2, "when_exclusive": WHEN_EXCLUSIVE,
              "told_ratchet": {"hand_cards": hand_cards, "legacy_legs": 0, "unsited": 0}, "joints": list(rows)}
    (refs / "stage-joints.json").write_text(joints_text if joints_text is not None else json.dumps(joints), encoding="utf-8", newline="\n")
    (refs / "ahead-cards.json").write_text(json.dumps({"cards": cards or {}}), encoding="utf-8", newline="\n")
    return root


class Capabilities:
    """`stage_joints` asks the real host adapter whether a role has a shell and the real map which roles `*` stands for; a fixture
    role is neither there, so the two answers are set for the length of a block."""

    def __init__(self, shells=(), mapped=("qa-x", "qa-y", "qa-z")) -> None:
        self.shells, self.mapped = set(shells), set(mapped)

    def __enter__(self):
        import stage_joints
        self.sj, self.saved = stage_joints, (stage_joints._has_shell, stage_joints._mapped_roles)
        stage_joints._has_shell = lambda role: role in self.shells
        stage_joints._mapped_roles = lambda: set(self.mapped)
        return self

    def __exit__(self, *exc) -> None:
        self.sj._has_shell, self.sj._mapped_roles = self.saved


def section_of(page: str) -> str:
    return page[page.index("## What code will check of you"):]


def test_told_section_rows() -> None:
    """T3a (a), (b), (c): the section is the rows of the role (stage, capability, group, `*`), in the order of the spec."""
    tmp = temp_dir("qa-factory-told-")
    try:
        rows = [told_row("t:b-late", text="Late row."),
                told_row("t:a-early", text="Early row."),
                told_row("t:star", roles=("*",), stages=("*",), text="Star row."),
                told_row("t:only-s2", roles=("qa-y",), stages=("S2",), text="Only in S2."),
                told_row("t:y-only", roles=("qa-y",), text="Only for y."),
                told_row("t:shell", when=["shell"], text="Shell row."),
                told_row("t:noshell", when=["no_shell"], text="No-shell row.")]
        rows += [told_row(f"t:g-{token}", when=[token], text=f"Group {token}.") for token in
                 ("walk", "not_first_look", "first_look", "manual", "window", "plan")]
        root = told_plugin(tmp, rows)
        with Capabilities():
            page = CS.handoff_keys_page(root, "qa-x")
            ypage = CS.handoff_keys_page(root, "qa-y")
        text = section_of(page)
        for token in ("a-early", "star", "b-late", "noshell"):
            check_in(f"T3a (a): the row t:{token} is on qa-x's page", f"- [t:{token}] ", text)
        check_in("T3a (a): a row prints through the one line renderer `told_line`: `- [<check>] <text> Door: <door>.`", "- [t:a-early] Early row. Door: d.", text)
        check_not_in("T3a (a): a row of another role is not on qa-x's page", "t:y-only", text)
        check_not_in("T3a (a): a row of a stage the role is not in is not on its page", "t:only-s2", text)
        check_in("T3a (a): the other role gets its own row", "- [t:y-only] ", section_of(ypage))
        check_in("T3a (a): `*` stages x `*` roles reach every role at every stage (the second role too)", "- [t:star] ", section_of(ypage))
        check_in("T3a (a): a row of the second stage reaches a role of that stage", "- [t:only-s2] ", section_of(ypage))
        order = [text.index(f"- [t:{token}] ") for token in ("a-early", "b-late", "star")]
        check_eq("T3a (a): rows run by first stage index (`*` = 0), then check id", order, sorted(order))
        check_not_in("T3a (a): no shell: the shell row is not told", "t:shell]", text)
        with Capabilities(shells=("qa-x",)):
            shelled = section_of(CS.handoff_keys_page(root, "qa-x"))
        check_in("T3a (a): a shell: the shell row is told", "- [t:shell] ", shelled)
        check_not_in("T3a (a): a shell: the no-shell row is not told", "t:noshell]", shelled)
        check_in("T3a (a): no shell: the no-shell row is told", "- [t:noshell] ", text)
        positions = [text.index(h) for h in GROUP_HEADINGS]
        for heading in GROUP_HEADINGS:
            check_in(f"T3a (a): the group heading `{heading}` is on the page with its generated `(replaces ...)` text", heading + "\n", text)
        check_eq("T3a (a): the groups run in the order plan, window, manual, first look, not first look, walk", positions, sorted(positions))
        check("T3a (a): the capability-only rows come before the first group heading",
              text.index("- [t:b-late] ") < positions[0] and text.index("- [t:noshell] ") < positions[0], text)
        check_in("T3a (a): a group row stands under its heading", "Group walk.", text[positions[-1]:])
        check_not_in("T3a (a): an additive group has no `(replaces` text", "(replaces", text[text.index("### Only in a manual block"):text.index(GROUP_HEADINGS[3])])
        check_in("T3a (a): the legend names the three placeholders", "`<T>` is your ticket, `<ID>` your dispatch id, `<home>` the project's qa-factory folder", text)
        check_not_in("T3a (a): placeholders are not filled on the page (no value is known)", "QA-", text)
        check_not_in("T3a (c): no card and hand_cards 0: no `Not yet in rows`", "### Not yet in rows", text)
        # (b) a role with zero rows
        zero = section_of(CS.handoff_keys_page(told_plugin(tmp, []), "qa-x"))
        check_in("T3a (b): a role with zero rows prints its `none` line", "- none: code checks nothing of this role beyond the sections above", zero)
        check_not_in("T3a (b): and no sub-heading", "###", zero)
        # (c) the cards that are not yet rows
        with Capabilities():
            carded = section_of(CS.handoff_keys_page(told_plugin(tmp, rows[:1], hand_cards=3, cards={"qa-x": {"text": "Card sentence of x."}}), "qa-x"))
            only_card = section_of(CS.handoff_keys_page(told_plugin(tmp, [], hand_cards=3, cards={"qa-x": {"text": "Card sentence of x."}}), "qa-x"))
            spent = section_of(CS.handoff_keys_page(told_plugin(tmp, rows[:1], hand_cards=0, cards={"qa-x": {"text": "Card sentence of x."}}), "qa-x"))
        check_in("T3a (c): while hand_cards > 0 the role's card stands under `### Not yet in rows`", "### Not yet in rows\n\nCard sentence of x.", carded)
        check_in("T3a (c): beside the rows", "- [t:b-late] ", carded)
        check_not_in("T3a (c): a card is a block, not a `none` line", "- none:", only_card)
        check_not_in("T3a (c): hand_cards 0 (after T1r): the card is not told from the page even if the file still has it", "Card sentence", spent)
        check_eq("T3a (c): the card reader reads the plugin root it is given (a root with no cards gives none)",
                 CS.ahead_card("qa-x", told_plugin(tmp / "nocards")), "")
        real_card = CS.ahead_card("qa-scout")
        import brief_pack
        check_eq("T3a (c): on the real package the moved copy and the brief's own say the same", real_card, brief_pack.ahead_card("qa-scout"))
        check("T3a (c): the real scout page carries the real card under `Not yet in rows`", "### Not yet in rows\n\n" + real_card in
              (PLUGIN_ROOT / "references" / "slices" / "qa-scout" / CS.KEYS_NAME).read_text(encoding="utf-8"))
        # TEMPORAL: the rows file unreadable is named, never an empty section passed as fine
        broken = told_plugin(tmp, [], joints_text="{not json")
        page = CS.handoff_keys_page(broken, "qa-x")
        check_in("T3a temporal: an unreadable stage-joints.json is NOT KNOWN on the page", "NOT KNOWN: the rows of what code checks could not be read", page)
        CS.keys_write(broken)
        check_in("T3a temporal: and red naming the file", "references/stage-joints.json cannot be read", " ".join(CS.keys_findings(broken)))
        check_in("T3a temporal: the page the role reads is not the `none` line", "NOT KNOWN", section_of(page))
        check_eq("T3a: `requirement_section` is the attribute the page leg of stage_joints waits for", callable(getattr(CS, "requirement_section", None)), True)
    finally:
        cleanup(tmp)


def test_told_section_size_and_split() -> None:
    """T3a (d), (e): K8 at W-1, W, L+1 and the partition of rows between listed pages."""
    limit, width = CS.size_limits()
    check_eq("T3a: W is 80 % of the imported MAX_BLOCK_CHARS", (width, limit), ((limit * 8) // 10, __import__("inject_context").MAX_BLOCK_CHARS))
    tmp = temp_dir("qa-factory-k8-")
    try:
        with Capabilities():
            outcomes = {}
            for name, target in (("W-1", width - 1), ("W", width), ("L+1", limit + 1)):
                root = tmp / name.replace("+", "p")
                root.mkdir()
                size = 100
                for _round in range(2):                    # the page is linear in the sentence: one correction lands on the target
                    told_plugin(root, [told_row("t:one", text="a" * size)])
                    now = len(CS.handoff_keys_page(root / "plugin", "qa-x").strip())
                    size += target - now
                check_eq(f"T3a (d): the fixture page is exactly {name} = {target} characters", len(CS.handoff_keys_page(root / "plugin", "qa-x").strip()), target)
                CS.keys_write(root / "plugin")
                proc = run_script("contract_slices.py", "--check", "--plugin-root", str(root / "plugin"))
                outcomes[name] = (CS.keys_warnings(root / "plugin"), " ".join(CS.keys_findings(root / "plugin")), proc)
            warn, red, proc = outcomes["W-1"]
            check_eq("T3a (d): at W-1 K8 is silent (no WARN, no finding, exit 0)", (warn, red, proc.returncode), ([], "", 0))
            warn, red, proc = outcomes["W"]
            check_eq("T3a (d): at W it is a WARN, not a finding, exit 0", (len(warn), red, proc.returncode), (1, "", 0))
            check_in("T3a (d): the WARN names the file, the size, the 80 % and the split text", "WARN K8 references/slices/qa-x/handoff-keys.md: %d chars, at or over 80 %% of MAX_BLOCK_CHARS (%d)" % (width, limit), warn[0])
            check_in("T3a (d): and the one move", 'Split: add the line "plugin:references/slices/qa-x/handoff-keys-2.md" right after', warn[0])
            check_in("T3a (d): and the command", "then run python -B scripts/contract_slices.py --write", warn[0])
            check_in("T3a (d): the WARN is printed by --check", "WARN K8", outcomes["W"][2].stdout)
            warn, red, proc = outcomes["L+1"]
            check_in("T3a (d): at L+1 the same text is a finding", "K8 references/slices/qa-x/handoff-keys.md: %d chars" % (limit + 1), red)
            check_in("T3a (d): with the split move", "handoff-keys-2.md", red)
            check("T3a (d): and --check exits non-zero", proc.returncode != 0, proc.stdout + proc.stderr)
            check_eq("T3a (d): over L is not also a WARN line", warn, [])
        # (e) the partition
        with Capabilities():
            # T1r-pages: the partition splits at the stricter of W (20800 characters) and the 12000-byte slice cap, so the rows are sized
            # to the cap (1490 characters, not 2990): the same nine rows still need two pages and split inside the window group
            cap = [told_row(f"t:a{i}", text=f"a{i} " + "x" * 1490) for i in range(1, 4)]
            win = [told_row(f"t:w{i}", when=["window"], text=f"w{i} " + "y" * 1490) for i in range(1, 7)]
            root = told_plugin(tmp / "split", cap + win, lists={"qa-x": ("handoff-keys.md", "handoff-keys-2.md")})
            pages = CS.handoff_keys_pages(root, "qa-x")
            check_eq("T3a (e): two listed pages are two generated pages", len(pages), 2)
            check("T3a (e): page 1 stays at or under W", len(pages[0].strip()) <= width, str(len(pages[0].strip())))
            both = pages[0] + pages[1]
            check_eq("T3a (e): every row is on exactly one page, whole, none cut",
                     [(both.count(r["requirement"]), (r["requirement"] in pages[0]) != (r["requirement"] in pages[1])) for r in cap + win],
                     [(1, True)] * 9)
            check("T3a (e): the rows split between the pages (page 2 holds rows)", "- [t:w6] " in pages[1] and "- [t:a1] " in pages[0])
            check("T3a (e): the rows keep their order across the pages (the window rows run w1..w6, page 1 first)",
                  "- [t:w1] " in pages[0] and pages[0].index("- [t:a1] ") < pages[0].index("- [t:w1] ") and "- [t:w1] " not in pages[1])
            check_in("T3a (e): a continuation page opens with the continued heading", "## What code will check of you (continued from handoff-keys.md)", pages[1])
            check_in("T3a (e): and the legend", "`<T>` is your ticket", pages[1])
            check_in("T3a (e): a group whose rows continue repeats its heading with `(continued)`",
                     '### Only in a window (replaced by "Only in a plan dispatch") (continued)', pages[1])
            check_not_in("T3a (e): page 1 does not carry the `(continued)` text", "(continued)", pages[0].replace("(continued from", ""))
            check_not_in("T3a (e): a continuation page does not repeat the fixed sections", "## Handoff form", pages[1])
            CS.keys_write(root)
            check_eq("T3a (e): written pages are fresh and K8 is silent", (CS.keys_findings(root), CS.keys_warnings(root)), ([], []))
            # the last listed page takes every remaining row, a listed page with no row says so
            few = told_plugin(tmp / "few", cap[:1], lists={"qa-x": ("handoff-keys.md", "handoff-keys-2.md")})
            fp = CS.handoff_keys_pages(few, "qa-x")
            check_in("T3a (e): a listed page that gets no row says so (not red)", "- none: every row of this role stands on the pages before this one", fp[1])
            CS.keys_write(few)
            check_eq("T3a (e): and the pair is clean", CS.keys_findings(few), [])
            # an unlisted page file is red, and --write deletes it
            lone = told_plugin(tmp / "lone", cap[:1])
            CS.keys_write(lone)
            stale = lone / "references" / "slices" / "qa-x" / "handoff-keys-2.md"
            stale.write_text("left over", encoding="utf-8", newline="\n")
            check_in("T3a (e): an unlisted page file is red", "unlisted generated page references/slices/qa-x/handoff-keys-2.md", " ".join(CS.keys_findings(lone)))
            check_in("T3a (e): `--write` deletes it", "deleted references/slices/qa-x/handoff-keys-2.md", " ".join(CS.keys_write(lone)))
            check_eq("T3a (e): gone and clean", (stale.exists(), CS.keys_findings(lone)), (False, []))
            # non-consecutive pages are red
            gap = told_plugin(tmp / "gap", cap[:1], lists={"qa-x": ("handoff-keys.md", "handoff-keys-3.md")})
            CS.keys_write(gap)
            said = " ".join(CS.keys_findings(gap))
            check_in("T3a (e): listed pages with a gap are red naming the gap", "not consecutive - handoff-keys-2.md is not listed but handoff-keys-3.md is", said)
            # one row longer than W on its own
            big = told_plugin(tmp / "big", [told_row("t:huge", text="z" * (width + 1))])
            CS.keys_write(big)
            check_in("T3a (e): a row over W on its own is red: shorten the sentence, never cut", "one row is over the split threshold", " ".join(CS.keys_findings(big)))
    finally:
        cleanup(tmp)


def test_inline_set() -> None:
    """T3a (f), (g), (h), (i): the key pages are inline in every mode and never cut; the page of the case critic."""
    import inject_context as IC
    for name, expected in (("handoff-keys.md", True), ("handoff-keys-2.md", True), ("handoff-keys-17.md", True), ("common-rules.md", True),
                           ("plugin:references/slices/qa-x/handoff-keys-3.md", True), ("handoff-keys-1.md", False),
                           ("handoff-keys-02.md", False), ("handoff-keys-0.md", False), ("vocabularies.md", False), ("index.md", False)):
        check_eq(f"T3a (f): inline_subject({name!r})", CS.inline_subject(name), expected)
    check_eq("T3a (f): INLINE_SUBJECTS is the common layer and the key page", CS.INLINE_SUBJECTS, CS.COMMON_LAYER_SUBJECTS + (CS.KEYS_NAME,))
    tmp = temp_dir("qa-factory-inline-")
    real_root, real_mode = IC.PLUGIN_ROOT, IC.slices_mode
    try:
        root = tmp / "plugin"
        folder = root / "references" / "slices" / "qa-x"
        folder.mkdir(parents=True)
        bodies = {"common-rules.md": "RULES BODY", "handoff-keys.md": "KEYS PAGE ONE", "handoff-keys-2.md": "KEYS PAGE TWO",
                  "vocabularies.md": "VOCAB BODY", "index.md": "CATALOGUE BODY"}
        for name, body in bodies.items():
            (folder / name).write_text(body + "\n", encoding="utf-8", newline="\n")
        entries = [f"plugin:references/slices/qa-x/{n}" for n in ("common-rules.md", "handoff-keys.md", "handoff-keys-2.md", "vocabularies.md")]
        imap = {"common": [], "roles": {"qa-x": entries}}
        IC.PLUGIN_ROOT, IC.slices_mode = root, lambda: "on_demand"
        blocks = "".join(IC.collect_blocks("qa-x", imap, {}))
        for body in ("RULES BODY", "KEYS PAGE ONE", "KEYS PAGE TWO", "CATALOGUE BODY"):
            check_in(f"T3a (f): on_demand injects {body} inline", body, blocks)
        check_not_in("T3a (f): and names the other slice instead of delivering it", "VOCAB BODY", blocks)
        # the weight report does not count the inline subjects as named
        (root / "references" / "inject-map.json").write_text(json.dumps(imap), encoding="utf-8", newline="\n")
        line = [ln for ln in CS.report(root).splitlines() if ln.startswith("qa-x")][0]
        named = int(line.split()[4].replace(",", ""))
        inline_bytes = sum(len(bodies[n]) + 1 for n in ("common-rules.md", "handoff-keys.md", "handoff-keys-2.md"))
        check_eq("T3a (f): the on_demand weight counts the key pages and the rules as delivered, the catalogue, and not the named slice",
                 named, inline_bytes + len(bodies["index.md"]) + 1)
        # (g) a drop row on a key page: named by map_problems, ignored by delivered_text
        section = "## What code will check of you"
        text = (PLUGIN_ROOT / "references" / "slices" / "qa-scout" / CS.KEYS_NAME).read_text(encoding="utf-8")
        rel = "plugin:references/slices/qa-scout/handoff-keys.md"
        cut = {"common": [], "roles": {"qa-scout": [rel]}, "kinds": {"repair": {"qa-scout": {"drop_sections": {rel: [section]}}}}}
        check_in("T3a (g): the section is on the real page", section, text)
        problems = IC.map_problems(cut)
        check("T3a (g): map_problems names the drop row", len(problems) == 1 and "kinds.repair.qa-scout.drop_sections[" + rel + "]" in problems[0]
              and "a common entry, the common-rules slice or a generated key page is never cut (it reaches every dispatch)" in problems[0], str(problems))
        for kind in ("repair", "rework", "first"):
            check_eq(f"T3a (g): delivered_text returns the page whole to a {kind} dispatch", IC.delivered_text(rel, text, "qa-scout", cut, kind), text)
        check_eq("T3a (g): and the dropped-headings reader returns nothing for a key page", IC._dropped_headings(rel, "qa-scout", cut, "repair"), [])
        cont = "plugin:references/slices/qa-scout/handoff-keys-2.md"
        cut2 = {"common": [], "roles": {"qa-scout": [rel, cont]}, "kinds": {"rework": {"qa-scout": {"drop_sections": {cont: [section]}}}}}
        check("T3a (g): a continuation page is refused the same way", "generated key page is never cut" in " ".join(IC.map_problems(cut2)))
    finally:
        IC.PLUGIN_ROOT, IC.slices_mode = real_root, real_mode
        cleanup(tmp)
    check_eq("T3a (g): the shipped map says nothing that would not happen", IC.map_problems(IC.load_map()), [])
    # (h) the case critic has its page, right after its common-rules line
    imap = json.loads((PLUGIN_ROOT / "references" / "inject-map.json").read_text(encoding="utf-8"))
    critic = imap["roles"]["qa-case-critic"]
    check_eq("T3a (h): qa-case-critic lists its key page right after its common-rules slice",
             critic[:2], ["plugin:references/slices/qa-case-critic/common-rules.md", "plugin:references/slices/qa-case-critic/handoff-keys.md"])
    page = (PLUGIN_ROOT / "references" / "slices" / "qa-case-critic" / CS.KEYS_NAME).read_text(encoding="utf-8")
    for anchor in ("## Outputs", "## Witness", "## Handoff form", "## What code will check of you"):
        check_in(f"T3a (h): the case critic's page holds `{anchor}`", anchor, page)
    check_eq("T3a (h): the key pages of the shipped package are fresh and K8/K10 are silent", CS.keys_findings(PLUGIN_ROOT), [])
    check_eq("T3a (h): no shipped page is at or over 80 % of MAX_BLOCK_CHARS", CS.keys_warnings(PLUGIN_ROOT), [])
    # (i) the size pin of the cards is gone
    cards_test = (Path(__file__).resolve().parent / "test_ahead_cards.py").read_text(encoding="utf-8")
    check_not_in("T3a (i): `CARD_MAX_BYTES` is no longer in test_ahead_cards.py", "CARD_MAX_BYTES", cards_test)


def test_native_headroom() -> None:
    """T3a (j): K10 - the plugin share against the Codex native ceiling, with a named baseline for a role already over."""
    import role_load as RL
    tmp = temp_dir("qa-factory-k10-")
    try:
        def role_tree(name: str, charter_chars: int, baseline=None, project_entries: int = 0, settings: bool = True) -> Path:
            root = tmp / name
            (root / "agents").mkdir(parents=True)
            (root / "references").mkdir()
            (root / "agents" / "qa-x.md").write_text("a" * charter_chars, encoding="utf-8", newline="\n")
            entries = [f"project:qa-factory/p{i}.md" for i in range(project_entries)]
            (root / "references" / "inject-map.json").write_text(json.dumps({"common": [], "roles": {"qa-x": entries}}), encoding="utf-8", newline="\n")
            if settings:
                doc = {"threshold_tokens": 25000, "bytes_per_token": 4, "allowances": {"packet": 5400, "launch": 2000},
                       "control_tolerance_percent": 15, "ratchet_tokens": {}, "ratchet_slack_tokens": 0}
                if baseline is not None:
                    doc["native_headroom"] = baseline
                (root / "references" / "role-load.json").write_text(json.dumps(doc), encoding="utf-8", newline="\n")
            return root
        headroom = 100000 - 5400 - 200
        check_eq("T3a (j): at H the role is green", RL.native_headroom_problems(role_tree("at", headroom)), [])
        over = RL.native_headroom_problems(role_tree("over", headroom + 1))
        check_eq("T3a (j): one over H and no baseline is one red", len(over), 1)
        for part in ("K10 qa-x", f"{headroom + 1:,} bytes", f"headroom {headroom:,}", "baseline none", RL.NATIVE_FINDING, "Appendix A"):
            check_in(f"T3a (j): the red names `{part}`", part, over[0])
        check_eq("T3a (j): over H and AT its baseline is green", RL.native_headroom_problems(role_tree("base", headroom + 1, {"qa-x": headroom + 1})), [])
        check_eq("T3a (j): over H and below the baseline is green", RL.native_headroom_problems(role_tree("below", headroom + 1, {"qa-x": headroom + 50})), [])
        beyond = RL.native_headroom_problems(role_tree("beyond", headroom + 2, {"qa-x": headroom + 1}))
        check("T3a (j): one over its baseline is red and names the baseline", len(beyond) == 1 and f"baseline {headroom + 1:,}" in beyond[0], str(beyond))
        check_eq("T3a (j): under H a baseline is not needed", RL.native_headroom_problems(role_tree("under", 1000, {"qa-x": 5})), [])
        projected = RL.native_headroom_problems(role_tree("project", headroom - 26000 + 1, project_entries=1))
        check("T3a (j): a `project:` entry takes 26000 off the headroom", len(projected) == 1 and f"headroom {headroom - 26000:,}" in projected[0], str(projected))
        check_in("T3a (j): a baseline table that is not role -> bytes is not judged, said so", "not judged",
                 " ".join(RL.native_headroom_problems(role_tree("badbase", 10, {"qa-x": "many"}))))
        check_eq("T3a (j): a tree with no role-load.json judges nothing", RL.native_headroom_problems(role_tree("none", headroom + 1, settings=False)), [])
        check_eq("T3a (j): the shipped package is green (its one role over H stands at its named baseline)", RL.native_headroom_problems(PLUGIN_ROOT), [])
        shipped = json.loads((PLUGIN_ROOT / "references" / "role-load.json").read_text(encoding="utf-8"))["native_headroom"]
        check_eq("T3a (j): the shipped baselines are the roles that are over H today", sorted(shipped), ["qa-test-strategist"])
    finally:
        cleanup(tmp)


def test_t1rp() -> None:
    """T1r-pages: rows told at the call leave the page for one index line per family (the family list is data), the key page is
    split at the stricter of W and the slice cap, and no row is in neither carrier."""
    import re
    import stage_joints as SJ
    from stage_guard import stages_of_role
    call = lambda row: {**row, "producers": [{**row["producers"][0], "told": [{"page": True, "call": True}]}]}
    plan, plan_md = call(told_row("guard_pre_tool:PT-plan-rewrite", text="Never rewrite whole.")), call(told_row("guard_pre_tool:PT-plan-md-rewrite", text="Never rewrite md."))
    cmd, out = call(told_row("role_cli:plan_row.py", text="A command row.")), told_row("t:out", text="Output row.")

    words = json.loads((PLUGIN_ROOT / "references" / "stage-joints.json").read_text(encoding="utf-8"))["call_index_wording"]

    def joints(rows, families):
        return json.dumps({"schema_version": 2, "when_exclusive": WHEN_EXCLUSIVE, "call_told_families": families,
                           "call_index_wording": {f: words[f] for f in families},
                           "told_ratchet": {"hand_cards": 0, "legacy_legs": 0, "unsited": 0}, "joints": list(rows)})
    tmp = temp_dir("qa-factory-t1rp-")
    try:
        with Capabilities():
            fams = ["guard_pre_tool", "host_adapter", "role_cli"]
            root = told_plugin(tmp / "a", joints_text=joints([plan, plan_md, cmd, out], fams)) if (tmp / "a").mkdir() is None else None
            section = section_of(CS.handoff_keys_page(root, "qa-x"))
            check_in("T1rp/index-line/guard_pre_tool: one line, the count, the nothing-lost sentence",
                     "- [guard_pre_tool:*] 2 checks of your tool calls are told in the refusal of the call, with what they expect and the door; "
                     "nothing you have written is lost by them.", section)
            check_in("T1rp/index-line/role_cli: the count and the `--help` instruction before the input file, no nothing-lost sentence",
                     "- [role_cli:*] 1 checks of your commands are told in the refusal of the call, with what they expect and the door. "
                     "Run `plan_row.py --help` before you write an input file", section)
            check("T1rp/index-line/role_cli: and the sentence 'nothing you have written is lost' is not printed for it", "lost by them" not in section.split("- [role_cli:*]")[1])
            check_eq("T1rp/index-line/host_adapter: a listed family with 0 rows for the role has no line", "- [host_adapter:*]" in section, False)
            check_eq("T1rp/no-row-lost/fixture: the call-told rows are not on the page and the output row is",
                     ("- [guard_pre_tool:PT-plan-rewrite]" in section, "- [role_cli:plan_row.py]" in section, "- [t:out] " in section), (False, False, True))
            check_eq("T1rp/page-ids-and-call-ids/fixture: page ids + call-told ids == rows_for ids",
                     sorted(["t:out"] + [r["check"] for r in (plan, plan_md, cmd) if SJ.call_told(r, "qa-x", fams)]), sorted(r["check"] for r in SJ.rows_for("qa-x", ["S1"], None, data=json.loads(joints([plan, plan_md, cmd, out], fams)))))
            only = section_of(CS.handoff_keys_page(told_plugin(tmp / "b", joints_text=joints([plan], fams)) if (tmp / "b").mkdir() is None else None, "qa-x"))
            check_eq("T1rp/only-call-rows: a role whose rows are all told at the call has index lines, not the `none` line", ("- [guard_pre_tool:*]" in only, CS.NONE_ROLE in only), (True, False))
            back = section_of(CS.handoff_keys_page(told_plugin(tmp / "c", joints_text=joints([plan, plan_md, cmd, out], [])) if (tmp / "c").mkdir() is None else None, "qa-x"))
            check_eq("T1rp/reversible: the family list emptied, every row is on the page again and there is no index line",
                     ("- [guard_pre_tool:PT-plan-rewrite]" in back, "- [role_cli:plan_row.py]" in back, "told in the refusal of the call" in back), (True, True, False))
            check_eq("T1rp/unlisted-family-sleeps: a marker on a family not in the list leaves the row on the page",
                     "- [role_cli:plan_row.py]" in section_of(CS.handoff_keys_page(told_plugin(tmp / "d", joints_text=joints([cmd], ["guard_pre_tool"])) if (tmp / "d").mkdir() is None else None, "qa-x")), True)
        # the split at the stricter limit: under W (characters), over the cap (bytes)
        with Capabilities():
            rows = [told_row(f"t:w{i}", text=f"w{i} " + "x" * 2990) for i in range(1, 6)]
            root = tmp / "e"
            root.mkdir()
            told_plugin(root, rows, lists={"qa-x": ("handoff-keys.md", "handoff-keys-2.md")})
            pages = CS.handoff_keys_pages(root / "plugin", "qa-x")
            _limit, width = CS.size_limits()
            check_eq("T1rp/split-at-cap: five rows (about 15000 characters, under W) split over the cap: page 1 at or under it, both pages under W",
                     (len(pages), len(pages[0].encode()) <= CS.SLICE_MAX_BYTES, all(len(p.strip()) < width for p in pages), "- [t:w5] " in pages[1]), (2, True, True, True))
        check_eq("T1rp/one-cap: the slice cap is one literal, read by the partition and by selftest",
                 (CS.SLICE_MAX_BYTES, __import__("selftest").REFERENCE_MD_MAX_BYTES), (12000, 12000))
    finally:
        cleanup(tmp)
    # the real package, per role
    model = json.loads((PLUGIN_ROOT / "references" / "stages.json").read_text(encoding="utf-8"))
    data, _why = SJ.load_rows()
    fams = SJ.call_families(data)
    _limit, width = CS.size_limits()
    form = "a header `<role> <stage> <window>"
    for role in sorted(json.loads((PLUGIN_ROOT / "references" / "inject-map.json").read_text(encoding="utf-8"))["roles"]):
        pages = CS.handoff_keys_pages(PLUGIN_ROOT, role)
        text = "\n".join(pages)
        ids = [str(s.get("id")) for s in stages_of_role(model, role)]
        rows = SJ.rows_for(role, ids, None, data=data)
        on_page = {m for m in re.findall(r"^- \[([^\]]+)\]", text, re.M)}
        at_call = {r["check"] for r in rows if SJ.call_told(r, role, fams)}
        check_eq(f"T1rp/no-row-lost/{role}: page ids + call-told ids == rows_for ids (index lines are not rows)",
                 sorted((on_page - {f"{f}:*" for f in fams}) | at_call), sorted(r["check"] for r in rows))
        check_eq(f"T1rp/digest-once/{role}: the digest form sentence stands once on the pages", text.count(form), 1)
        check_eq(f"T1rp/pages-listed/{role}: the generated pages are the listed pages, each under W characters and at or under the cap in bytes",
                 (len(pages), len([1 for r, _e, _p in CS.keys_targets(PLUGIN_ROOT) if r == role]), all(len(p.strip()) < width and len(p.encode()) <= CS.SLICE_MAX_BYTES for p in pages)),
                 (len(pages), len(pages), True))


def test_t1rs() -> None:
    """T1r-sites S-2: which `execution_request` / `run_suite` rows are told at the call, per role, is DATA joined to PROOF. A producer
    entry carries the call marker for role R only when the row is proved on EVERY road R uses (`<id>` x `road`); a road that cannot be
    proved keeps the page for R (more text, never a row in neither carrier). The constants below are pinned to the two S-1 reports
    (`20261114-t1r-sites-s1a-report.md`, `...-s1b-report.md`): a site proved there as F is proved; W (written, not run) and N (not
    provoked) are not. `T1rs/marked-by-proof` recomputes the marker of every (row, role) from them and compares it with the data."""
    import re
    import stage_joints as SJ
    from stage_guard import stages_of_role
    er, rs = "execution_request:", "run_suite:"
    # S-1a / S-1b: the ids with a site written but not provoked by a test that ran (W: selector_args, window_first; N: the `stand`
    # site of `run_suite.main` (needs a live probe) and the launch-path `store.begin` printer of `run_suite:begin`)
    unproved_site = {er + "selector_args", er + "window_first", er + "stand", rs + "begin"}
    request = {er + k for k in ("purpose", "selection", "budget", "freshness", "runtime", "stand.reference", "fingerprint", "command",
                                "execution", "selector", "instance_contracts")}                 # the ids `validate_request` raises
    manifest = {er + k for k in ("no_test", "selector_args", "place_rows", "profile", "case_entries")}      # judge the automator's own rows
    roads_of = {"qa-automator": ["run_suite", "import_test_receipt"], "qa-runner": ["run_suite"],
                "qa-code-critic": ["run_suite", "red_sandbox", "probe_by_code"], "qa-failure-analyst": ["run_suite", "red_sandbox"]}
    scripts = ("run_suite", "red_sandbox", "probe_by_code", "import_test_receipt", "execution_scheduler")

    def carries(check, road):       # the roads whose printer is known to carry only some ids; every other road: any id (unknown)
        return check in request if road == "import_test_receipt" else True

    def proved(check, road):        # only the `run_suite` printers are proved for an id; `import_test_receipt` prints the FIRST check only
        return road == "run_suite" and check not in unproved_site   # and `red_sandbox` / `probe_by_code` answer dicts are written, not run

    def expected(check, role):
        if role == "qa-automator" and check in manifest:
            return False
        return all(proved(check, r) for r in roads_of[role] if carries(check, r))
    data, _why = SJ.load_rows()
    fams = SJ.call_families(data)
    rows = [r for r in data["joints"] if r["check"].split(":")[0] in ("execution_request", "run_suite")]
    ids = {r["check"] for r in rows}
    check_eq("T1rs/rows: the 31 rows of the two families", (len(rows), len(ids)), (31, 31))
    # the road list of a role is read from its agent file (the scripts it names), never typed twice
    for role, roads in roads_of.items():
        text = (PLUGIN_ROOT / "agents" / f"{role}.md").read_text(encoding="utf-8")
        check_eq(f"T1rs/roads-of-role/{role}: the scripts of the agent file are the constant's roads",
                 [s for s in scripts if f"{s}.py" in text], roads)
    sited = set(SJ.check_ids())
    for fam in ("execution_request", "run_suite"):
        check_eq(f"T1rs/sited/{fam}: every row id is the literal key of a site (not only a sub-id of one)",
                 sorted(r["check"] for r in rows if r["check"].startswith(fam + ":") and r["check"] not in sited), [])
    # one reading of the marker: per (row, role), `call_told` equals the proof; the other eight roles hold none of these rows
    wrong = []
    for row in rows:
        for role in roads_of:
            held = any(role in e["roles"] for e in row["producers"])
            if held and SJ.call_told(row, role, fams) != expected(row["check"], role):
                wrong.append((row["check"], role, SJ.call_told(row, role, fams)))
    check_eq("T1rs/marked-by-proof: call_told(row, role) is True exactly when the row is proved on every road the role uses", wrong, [])
    check_eq("T1rs/entry-uniform: every role of one producer entry takes the same carrier (an entry is split where the proof differs)",
             [row["check"] for row in rows for e in row["producers"]
              if len({bool(t.get("call")) for t in e["told"]}) != 1 or len({expected(row["check"], r) for r in e["roles"] if r in roads_of}) != 1], [])
    # the five manifest-row rows: the automator judges its own rows -> page; the others by their roads (runner only, today)
    for key in sorted(manifest):
        row = next(r for r in rows if r["check"] == key)
        check_eq(f"T1rs/partial-split/{key}: automator page; runner call unless unproved; code-critic and analyst page (their roads are unproved)",
                 [SJ.call_told(row, r, fams) for r in ("qa-automator", "qa-runner", "qa-code-critic", "qa-failure-analyst")],
                 [False, key not in unproved_site, False, False])
    # the page: one index line per family, the count of the role's call-told rows; the page-told rows stay whole lines
    model = json.loads((PLUGIN_ROOT / "references" / "stages.json").read_text(encoding="utf-8"))
    counted = {"qa-automator": (5, 5), "qa-runner": (10, 2), "qa-code-critic": (0, 0), "qa-failure-analyst": (0, 0)}   # measured
    for role, (n_er, n_rs) in counted.items():
        text = "\n".join(CS.handoff_keys_pages(PLUGIN_ROOT, role))
        stages = [str(s.get("id")) for s in stages_of_role(model, role)]
        held = [r for r in SJ.rows_for(role, stages, None, data=data) if r["check"] in ids]
        told_at_call = {r["check"] for r in held if SJ.call_told(r, role, fams)}
        for fam, n in (("execution_request", n_er), ("run_suite", n_rs)):
            line = re.findall(rf"^- \[{fam}:\*\] (\d+) checks", text, re.M)
            own = {c for c in told_at_call if c.startswith(fam + ":")}
            check_eq(f"T1rs/index-line/{fam}/{role}: one line holding the count of the role's call-told rows, none when there are none",
                     (line, len(own)), ([str(n)] if n else [], n))
            check_eq(f"T1rs/no-row-lost/{fam}/{role}: a held row is a whole page line or counted by the index line, never both",
                     sorted(c for c in (r["check"] for r in held) if c.startswith(fam + ":")
                            and (f"- [{c}] " in text) == (c in own)), [])
        check_eq(f"T1rs/index-line/execution_request/{role}: the before-work door and the three roads are named when the line is",
                 all(w in text for w in ("`run_suite.py --template request`", "`red_sandbox.py`", "`probe_by_code.py`")) if n_er else True, True)
    auto = "\n".join(CS.handoff_keys_pages(PLUGIN_ROOT, "qa-automator"))
    check_eq("T1rs/partial-family/qa-automator: the ER index line AND the five manifest rows as whole lines (E3)",
             ("- [execution_request:*] " in auto, [f"- [{k}] " in auto for k in sorted(manifest)]), (True, [True] * 5))


test_rendering()
test_told_section_rows()
test_told_section_size_and_split()
test_t1rp()
test_t1rs()
test_inline_set()
test_native_headroom()
test_handoff_keys_pages()
test_keys_through_load_rows()
test_plan_role_charter_line()
test_findings_and_write()
test_shipped_package()
test_grounding_words()
test_common_rules_slices()
test_common_layer()
test_cli()
test_ladder_one_carrier()

finish("contract slices (markup, generation, freshness, shipped map)")
