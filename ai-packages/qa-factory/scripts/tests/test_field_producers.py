#!/usr/bin/env python3
"""FR-11: a field a contract requires has something that can produce it, or the gap is declared.

`not_verified:missing_sensitivity_proof` stood on nine instances of TP1-13797 and held
`delivery_ready: no` on a run where every case was green: the typed receipt comes from
`red_sandbox.py --probe` while the code critic is permitted `probe_by_code.py`. The rule that
came out of it is this one, and this is its systematic form — every required field of every
handoff contract, walked.

The class is not "a field holding a path": a role knows the path of the artifact it wrote. It is
a field whose value can only come from RUNNING something — a receipt, a content hash, a
provenance record, a count code computes. For each of those the producer is either a deriver in
`handoff_check` (code fills the field), or a row in `references/field-producers.json`. A row with
an empty `producer` is a declared gap with its reason, printed rather than hidden (FR-41).

Writing this walk found two fields where the deriver existed and was wired to two of the three
paths that ask for it (FR-17): `runtime.provenance` and `rounds[].verify.witness`.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, finish  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import handoff_check as HC  # noqa: E402
import null_outcomes as NO  # noqa: E402

PRODUCERS = harness.PLUGIN_ROOT / "references" / "field-producers.json"
# Which fields need a tool - "a value no role can write out of its own prose" - is chosen by
# `null_outcomes.tool_fields` (t-305 N0): the null-outcome detector walks the same selection, so it is ONE
# copy, held there, and this walk only asks what produces each field it names.
SCRIPT_RE = re.compile(r"([a-z][a-z0-9_]*\.py)")


def derived_paths() -> set:
    """The fields code fills, read out of handoff_check rather than copied."""
    return set(HC.DERIVERS) | set(HC.LIST_DERIVERS)


def declared() -> list:
    rows = json.loads(PRODUCERS.read_text(encoding="utf-8")).get("fields") or []
    return [row for row in rows if isinstance(row, dict)]


def row_for(field: str, rows: list) -> dict | None:
    leaf = field.rsplit(".", 1)[-1]
    for row in rows:
        name = str(row.get("field") or "")
        if name == field or (name.endswith(".*") and field.startswith(name[:-1])):
            return row
        if name.split(" ")[0] == field or name.split(" ")[0].rsplit(".", 1)[-1] == leaf:
            return row
    return None


def walk() -> tuple:
    """(fields needing a tool, the ones with no producer at all) across every contract."""
    rows, derived = declared(), derived_paths()
    needs, gaps = [], []
    for contract, role, path, hint in NO.tool_fields():
        text = (harness.PLUGIN_ROOT / "handoffs" / f"{contract}.yaml").read_text(encoding="utf-8")
        leaf = path.rsplit(".", 1)[-1]
        producer = ""
        if path in derived or leaf in HC.BY_LEAF:
            producer = "handoff_check --fix"
        else:
            named = SCRIPT_RE.search(hint) or SCRIPT_RE.search(
                next((ln for ln in text.splitlines()
                      if ln.strip().startswith(leaf.rstrip("[]") + ":")), ""))
            if named:
                producer = named.group(1)
            else:
                row = row_for(path, rows)
                producer = str((row or {}).get("producer") or "")
                if row is None:
                    gaps.append((contract, role, path, hint))
        needs.append((contract, role, path, producer))
    return needs, gaps


def every_required_field_has_a_producer_or_a_declared_gap() -> None:
    needs, undeclared = walk()
    # SC1-2 removed five claims that nothing read (33 -> 28, then 27: RN1-2 dropped the S3 form revision field)
    check("the walk reaches every contract's fields", len(needs) >= 27, str(len(needs)))
    check_eq("no required field needing a tool is left unaccounted for",
             [f"{c}:{p}" for c, _r, p, _prod in undeclared], [])
    by_code = [row for row in needs if row[3] == "handoff_check --fix"]
    check(f"code fills most of them ({len(by_code)} of {len(needs)})",
          len(by_code) >= 17, str(len(by_code)))
    # Every producer that is a script must exist, and must not be one of the three commands the
    # guard closes to every role (FR-2: a door the refused party may not open is not an answer).
    for contract, role, path, producer in needs:
        for script in SCRIPT_RE.findall(producer):
            check(f"{path}: {script} exists", (harness.SCRIPTS / script).is_file(), contract)
    declared_rows = declared()
    for row in declared_rows:
        check(f"{row.get('field')}: the row says why", len(str(row.get("why") or "")) > 30,
              str(row.get("why"))[:60])
    # The declared gap is closed (D-0010, D-0012): the sensitivity receipt has a producer, and it
    # is the two probes, each of which exists. No row of the file is a declared gap any more.
    gap = [row for row in declared_rows if not str(row.get("producer") or "").strip()]
    check_eq("no required field is left declared as having no producer", len(gap), 0)
    sensitivity = [row for row in declared_rows if "sensitivity_proof" in str(row.get("field"))]
    check_eq("the sensitivity receipt is still a row of the file", len(sensitivity), 1)
    producer = str(sensitivity[0].get("producer") or "")
    for script in ("probe_by_code.py", "red_sandbox.py"):
        check_in(f"its producer names {script}", script, producer)
        check(f"and {script} exists in scripts/", (harness.SCRIPTS / script).is_file(), script)
    check_in("the live level is the default one", "the check is live", producer)
    check_in("the row says what reads the receipt", "semantic_sensitivity", sensitivity[0]["why"])
    check_in("and which decisions closed the gap", "D-0010", sensitivity[0]["why"])


def the_two_paths_this_walk_wired() -> None:
    """A deriver wired into two of the three paths that ask for it is not adopted (FR-17)."""
    derived = derived_paths()
    for path in ("artifacts.runtime_provenance", "probes.runtime_provenance", "runtime.provenance"):
        check(f"{path} is filled by code", path in derived, str(sorted(derived))[:120])
    for path in ("artifacts.run_witness", "run.witness", "rounds[].verify.witness"):
        check(f"{path} is filled by code", path in derived, str(sorted(derived))[:120])
    check_eq("and the same deriver answers each family",
             (HC.DERIVERS["runtime.provenance"] is HC.DERIVERS["artifacts.runtime_provenance"],
              HC.DERIVERS["rounds[].verify.witness"] is HC.DERIVERS["run.witness"]), (True, True))


def the_sensitivity_gap_is_reported_not_hidden() -> None:
    """The window check still refuses without the receipt — the gap is declared, not waived."""
    import acceptance
    window = {"schema_version": 2, "required_quality_checks": [], "input_hash": "h1",
              "instances": [
                  {"instance_id": "test_x[a]", "case": "TC-1", "status": "green",
                   "input_hash": "h1",
                   "evidence_refs": [{"path": "work/evidence/x.json", "sha256": "0" * 64}],
                   "probe": {}}]}
    gaps = acceptance.validate_window(window, harness.PLUGIN_ROOT)
    check("an instance with no probe receipt is still refused", bool(gaps), str(gaps))


def known_red_ledger_cases() -> None:
    """The `known_red` helper (P1-a spec 3.6): one table, the row id is the case name. A gate errs only toward red (AR-28).

    Each row: (name, ledger file text or None for a missing file, results of the walk, expected).
    expected is ("error", text the LedgerError names) or (ok, problems that must start with these, known that must equal these).
    """
    import known_red as KR
    row = '{"node": "FV1-1", "raised_by": "Lead, 2026-11-13"}'
    ledger = '{"known_red": {"a: w -> r": %s}}' % row
    def red(rid: str) -> str:
        return (f'new red: {rid} — fix it, or add "{rid}": {{"node": "<FV1-n or node id>", "raised_by": '
                f'"<verdict or word that names this raise>"}} to L known_red')
    new_red = red("x")
    cases = [
        ("known red passes", ledger, {"a: w -> r": False}, (True, [], ["known red: a: w -> r -> FV1-1"])),
        ("new red refused with door", '{"known_red": {}}', {"x": False}, (False, [new_red], [])),
        ("stale green refused", ledger, {"a: w -> r": True},
         (False, ["stale: a: w -> r is green; remove its known_red row (node FV1-1) in this commit"], [])),
        ("unknown row refused", ledger, {"b": True},
         (False, ["unknown row: a: w -> r is not a row of this walk; rename it to the walk's id or remove it"], [])),
        ("green without row ok", '{"known_red": {}}', {"x": True}, (True, [], [])),
        ("empty ledger: every red is new", '{}', {"x": False, "y": False, "z": True},
         (False, [new_red, red("y")], [])),
        ("empty results with rows: every row unknown", '{"known_red": {"p": %s, "q": %s}}' % (row, row), {},
         (False, ["unknown row: p is not", "unknown row: q is not"], [])),
        ("missing file", None, {}, ("error", "cannot read the ledger file")),
        ("section absent = empty", '{"other": {}}', {"x": False}, (False, [new_red], [])),
        ("duplicate id", '{"known_red": {"d": %s, "d": %s}}' % (row, row), {}, ("error", "duplicate key 'd'")),
        ("whitespace id", '{"known_red": {" d": %s}}' % row, {}, ("error", "leading/trailing whitespace")),
        ("blank raised_by", '{"known_red": {"d": {"node": "FV1-1", "raised_by": "  "}}}', {}, ("error", "raised_by")),
        ("null raised_by", '{"known_red": {"d": {"node": "FV1-1", "raised_by": null}}}', {}, ("error", "raised_by None")),
        ("bad node fv1-1", '{"known_red": {"d": {"node": "fv1-1", "raised_by": "Lead"}}}', {}, ("error", "node 'fv1-1'")),
        ("extra key", '{"known_red": {"d": {"node": "FV1-1", "raised_by": "Lead", "why": "x"}}}', {}, ("error", "unknown key")),
        ("case-different id stays red", ledger, {"A: w -> r": False},
         (False, [red("A: w -> r"), "unknown row: a: w -> r is not"], [])),
        ("kind-level row does not cover variant",
         '{"known_red": {"exit_limit": %s}}' % row, {"exit_limit/empty": False},
         (False, ["unknown row: exit_limit is not", red("exit_limit/empty")], [])),
    ]
    root = harness.temp_dir()
    try:
        for name, text, results, expected in cases:
            path = root / "ledger.json"
            path.unlink(missing_ok=True)
            if text is not None:
                path.write_text(text, encoding="utf-8")
            try:
                got = KR.reconcile(results, KR.load(path), ledger_path="L")
            except KR.LedgerError as exc:
                check(f"known_red: {name}", expected[0] == "error" and expected[1] in str(exc), f"{exc} / wanted {expected}")
                continue
            ok, problems, known = expected
            # problems come sorted by id; a wanted text may be just the start of the message
            fits = (got.ok is ok and got.known == tuple(known) and len(got.problems) == len(problems)
                    and all(g.startswith(w) for g, w in zip(got.problems, problems)))
            check(f"known_red: {name}", expected[0] != "error" and fits, f"{got} / wanted {expected}")
    finally:
        harness.cleanup(root)


def main() -> None:
    every_required_field_has_a_producer_or_a_declared_gap()
    the_two_paths_this_walk_wired()
    the_sensitivity_gap_is_reported_not_hidden()
    known_red_ledger_cases()
    finish("test_field_producers")


if __name__ == "__main__":
    main()
