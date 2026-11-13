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
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, finish  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import handoff  # noqa: E402
import handoff_check as HC  # noqa: E402
import hooklib  # noqa: E402
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


SYNTHETIC_FORM = """schema_version: 1
contract: synthetic
stage: S3
from_role: qa-test-strategist
to_role: qa-case-designer

header:
  role: qa-test-strategist
  stage: S3
  window: <TICKET>
  verdict: <one of vocabulary.header_verdicts>

probe:
  p_id: <P-n, the row's stable id>
  pr_or_empty: <PR-n, or the empty list>
  file_fn: <file::function or T-n of the planned test>
  debt: <bugs/DEBT-n.md>
  r_of_2: <r of 2>
  limit: <= 80 characters>
  tf_or_omit: <true|false, or omit when the table holds no share>
  level: <one of vocabulary.test_levels - unit|integration|api|e2e-ui|other>
  colon_first: <TEST_BUG:collection|FLAKY|reorder>
  author: "work/handoffs/<the author's dispatch>.yaml"
  alt2: <P-n or R-n>
  alt3: <R-n, K-n or B-n>
  id_text: <R-n, a source id or an area>
  case_or_p: <case id or P-n>
  count_n: <n>
  number: <2>
  free: <what is being checked, one sentence>
  no_list: <one of vocabulary.no_such_list>
  dispatch: "work/handoffs/<dispatch>.yaml"

rows:
  - key: <one sentence>
    other: <one sentence>
  - key: <one sentence>
    other: <one sentence>

artifacts:
  run_witness: <path of the run_suite summary with the exit code and the totals line>
"""


def _at(data, path: str):
    """The value at `a.b[1].c` of a parsed form; the string "<missing>" when the path leads nowhere."""
    cur = data
    for part in re.findall(r"[A-Za-z_][\w\-]*|\[\d+\]", path):
        try:
            cur = cur[int(part[1:-1])] if part.startswith("[") else cur[part]
        except (KeyError, IndexError, TypeError):
            return "<missing>"
    return cur


def form_filler_hint_cases() -> None:
    """The filler's table "hint -> value" (P1-a spec 4.1 awkward inputs, E1-E3, E6, E10, E12, E13, E20): one row per case, the
    row name is the case. A synthetic form carries each awkward hint; the real contracts are walked by the next function."""
    import form_filler as FF
    ABS = FF.ABSENT
    ctx = FF.FillContext(author_dispatch="S2-author-1")
    levels = handoff_allowed("test_levels")
    rows = [
        # (name, ctx, variant, overrides, path, expected value | ABS | "<missing>")
        ("<P-n, the row's stable id> -> P-1, not TS-1", ctx, "base", None, "probe.p_id", "P-1"),
        ("<PR-n, or the empty list> base -> PR-1", ctx, "base", None, "probe.pr_or_empty", "PR-1"),
        ("<PR-n, or the empty list> empty_lists -> []", ctx, "empty_lists", None, "probe.pr_or_empty", []),
        ("<file::function or T-n ...> base", ctx, "base", None, "probe.file_fn", "file::function"),
        ("<file::function or T-n ...> alt:1", ctx, "alt:1", None, "probe.file_fn", "T-1"),
        ("<bugs/DEBT-n.md> -> a path with its id", ctx, "base", None, "probe.debt", "bugs/DEBT-1.md"),
        ("<r of 2> -> 1 of 2", ctx, "base", None, "probe.r_of_2", "1 of 2"),
        ("<= 80 characters> base is within the limit", ctx, "base", None, "probe.limit", "filled limit"),
        ("<= 80 characters> AT is exactly 80", ctx, "at_limit", None, "probe.limit", ("len", 80)),
        ("<= 80 characters> BEYOND is 81", ctx, "beyond_limit", None, "probe.limit", ("len", 81)),
        ("<true|false, or omit ...> base -> true", ctx, "base", None, "probe.tf_or_omit", True),
        ("<true|false, or omit ...> omit_optional -> left out", ctx, "omit_optional", None, "probe.tf_or_omit", "<missing>"),
        ("<one of vocabulary.test_levels - ...> -> a word of the vocabulary", ctx, "base", None, "probe.level", levels[0]),
        ("<TEST_BUG:collection|FLAKY|reorder> -> the colon does not cut the word", ctx, "base", None, "probe.colon_first", "TEST_BUG:collection"),
        ("<the author's dispatch> -> work/handoffs/<ctx.author_dispatch>.yaml", ctx, "base", None, "probe.author", "work/handoffs/S2-author-1.yaml"),
        ("<P-n or R-n> base -> P-1", ctx, "base", None, "probe.alt2", "P-1"),
        ("<P-n or R-n> alt:1 -> R-1", ctx, "alt:1", None, "probe.alt2", "R-1"),
        ("<R-n, K-n or B-n> alt:2 -> B-1", ctx, "alt:2", None, "probe.alt3", "B-1"),
        ("<R-n, a source id or an area> base -> an id", ctx, "base", None, "probe.id_text", "R-1"),
        ("<R-n, a source id or an area> alt:1 -> a word", ctx, "alt:1", None, "probe.id_text", "area-1"),
        ("<case id or P-n> alt:1 -> P-1", ctx, "alt:1", None, "probe.case_or_p", "P-1"),
        ("<n> -> 1", ctx, "base", None, "probe.count_n", 1),
        ("<2> -> 2", ctx, "base", None, "probe.number", 2),
        ("free text -> filled <leaf>", ctx, "base", None, "probe.free", "filled free"),
        ("override missing path", ctx, "base", {"probe.nowhere": "x"}, "<unfillable>", "probe.nowhere"),
        ("override on a section but not ABSENT/[]", ctx, "base", {"probe": "x"}, "<unfillable>", "probe"),
        ("ABSENT on required", ctx, "base", {"probe.p_id": ABS}, "probe.p_id", "<missing>"),
        ("override on code field", ctx, "base", {"artifacts.run_witness": "work/evidence/x.json"}, "artifacts.run_witness", "work/evidence/x.json"),
        ("code field without override stays for code", ctx, "base", None, "<left_for_code>", "artifacts.run_witness"),
        ("section[] vs section[0]: every row", ctx, "base", {"rows[].key": "all"}, "rows[1].key", "all"),
        ("section[] vs section[0]: one row, the row", ctx, "base", {"rows[0].key": "one"}, "rows[0].key", "one"),
        ("section[] vs section[0]: one row, the other row untouched", ctx, "base", {"rows[0].key": "one"}, "rows[1].key", "filled key"),
        ("section[0] beats section[]", ctx, "base", {"rows[].key": "all", "rows[0].key": "one"}, "rows[1].key", "all"),
        ("override beyond the template's rows names no field", ctx, "base", {"rows[5].key": "x"}, "<unfillable>", "rows[5].key"),
        ("section ABSENT leaves the section out", ctx, "base", {"rows": ABS}, "rows", "<missing>"),
        ("empty_lists empties every list but keeps the contract's required ones", ctx, "empty_lists", None, "rows", []),
        ("<one of vocabulary.no_such_list> is unfillable (E10)", ctx, "base", None, "<unfillable>", "probe.no_list"),
        ("token <dispatch> has no key in the context (E12)", ctx, "base", None, "<unfillable>", "probe.dispatch"),
        ("token <the author's dispatch> with no author_dispatch (E12)", FF.FillContext(), "base", None, "<unfillable>", "probe.author"),
        ("<TICKET> -> ctx.task_key", FF.FillContext(task_key="ZZ-9", author_dispatch="a"), "base", None, "header.window", "ZZ-9"),
        ("same input, same bytes", ctx, "base", None, "<same bytes>", True),
    ]
    root = harness.temp_dir()
    saved = handoff.CONTRACTS
    try:
        for name in ("index.yaml", "vocabulary.yaml"):
            (root / name).write_bytes((saved / name).read_bytes())
        (root / "synthetic.yaml").write_text(SYNTHETIC_FORM, encoding="utf-8")
        handoff.CONTRACTS = root
        for name, cx, variant, overrides, path, expected in rows:
            filled = FF.fill_form("synthetic", cx, verdict="ok", variant=variant, overrides=overrides)
            if path == "<unfillable>":
                got = [u.path for u in filled.unfillable]
                if "override" in name:
                    ok = expected in got and all(u.why.startswith("override names no field of synthetic") for u in filled.unfillable if u.path == expected)
                else:
                    ok = expected in got
            elif path == "<left_for_code>":
                got, ok = filled.left_for_code, expected in filled.left_for_code
            elif path == "<same bytes>":
                got, ok = filled.text, FF.fill_form("synthetic", cx, verdict="ok", variant=variant).text == filled.text
            else:
                got = _at(filled.data, path)
                if isinstance(expected, tuple):
                    ok = isinstance(got, str) and len(got) == expected[1]
                elif expected == "<missing>" or expected == []:
                    ok = got == expected or (expected == [] and got in ({}, []))
                else:
                    ok = got == expected
            check(f"filler: {name}", ok, f"got {got!r}, wanted {expected!r}; unfillable {[(u.path, u.why) for u in filled.unfillable]}")
        # the two refusals of the interface
        try:
            FF.fill_form("synthetic", ctx, variant="cite_hint:probe.p_id")
            check("filler: a variant the form does not have raises", False, "no error")
        except ValueError:
            check("filler: a variant the form does not have raises", True)
        try:
            FF.fill_form("synthetic", ctx, verdict="ok").require()
            check("filler: require() raises NotFillable naming the field", False, "no error")
        except FF.NotFillable as exc:
            check("filler: require() raises NotFillable naming the field", exc.path in ("probe.no_list", "probe.dispatch"), str(exc))
        try:
            FF.write_dispatch_form(root, "../x", "synthetic", ctx, "ok")
            check("filler: write_dispatch_form refuses a dispatch id that is a path", False, "no error")
        except ValueError:
            check("filler: write_dispatch_form refuses a dispatch id that is a path", True)
    finally:
        handoff.CONTRACTS = saved
        harness.cleanup(root)


def handoff_allowed(name: str) -> list:
    import handoff as H
    return H.allowed(name)


def _form_world(root) -> None:
    """The world every form is read in: a triage that shows nothing to repair and a run that shows nothing failed (the world in
    which the null outcome of S7 is true); built ONCE for the walk."""
    (root / "work").mkdir(parents=True, exist_ok=True)
    (root / "work" / "triage.json").write_text(json.dumps({"triage": []}), encoding="utf-8")
    (root / "work" / "run-report.json").write_text(
        json.dumps({"totals": {"passed": 1, "failed": 0, "error": 0}, "results": []}), encoding="utf-8")


def every_form_fills_from_its_own_hints() -> None:
    """P1-a N1: every handoff form, filled from its own hints in every variant, passes its own check (`handoff_check.check`).

    Row id `<contract>[<verdict>/<variant>]`. A hint the filler cannot fill is a red row `unfillable <contract>:<path> «<hint>»`
    (a finding about the form); the one form of kind `help` that the check cannot read is `form-kind-unread: <contract>`.
    Fields code fills (`_code_fills`) are not judged here (E11, N3 judges them with `fix=True`)."""
    import form_filler as FF
    index = handoff.index()
    forms = list(dict.fromkeys([r["contract"] for r in index["handoffs"]] + [index["escalation"]["contract"]]))
    help_forms = {index["escalation"]["contract"]}
    # pins of the size of the walk, both ways, no literal (spec verdict 1)
    files = {p.stem for p in (harness.PLUGIN_ROOT / "handoffs").glob("*.yaml")} - {"index", "vocabulary"}
    for name in sorted(files - set(forms)):
        check(f"form file not in index: {name}", False, "handoffs/ holds a form no row of index.yaml names")
    for name in sorted(set(forms) - files):
        check(f"index names no file: {name}", False, "a row of index.yaml names a contract with no file in handoffs/")
    words = handoff_allowed("header_verdicts")
    root = harness.temp_dir()
    real_vocabulary, cache = handoff.vocabulary, []

    def vocabulary_once():                        # the file does not change during the walk; reading it per choice field is the cost
        if not cache:
            cache.append(real_vocabulary())
        return cache[0]
    handoff.vocabulary = vocabulary_once
    seen, rows, fields, left_total, short = {}, 0, 0, 0, []
    try:
        _form_world(root)
        ctx = FF.FillContext(author_dispatch="S2-author-1")
        for contract in forms:
            spec = handoff.spec(contract)
            cx = FF.FillContext(author_dispatch="S2-author-1", dispatch_id=f"{contract}-w1")     # the dispatch the world reads the form as
            listed = FF.variants(contract)
            if len(listed) < max(len(words) if "header.verdict" in spec else 1, 1):
                short.append(contract)
            for index_of, (verdict, variant) in enumerate(listed):
                rows += 1
                row = f"{contract}[{verdict}/{variant}]"
                filled = FF.fill_form(contract, cx, verdict=verdict, variant=variant)
                if index_of == 0:
                    fields += len(filled.fills) + len(filled.left_for_code) + len(filled.unfillable)
                    left_total += len(filled.left_for_code)
                for u in filled.unfillable:
                    seen.setdefault((contract, u.path, u.hint), u.why)
                skip = {u.path for u in filled.unfillable}
                try:
                    _doc, _fixed, problems, _judged, _derived = HC.check(
                        handoff.parse(filled.text), contract, HC.Artifacts(root, dispatch=f"{contract}-w1"), fix=False, use_judge=False)
                except Exception as exc:          # E14: an exception is never a pass
                    if contract in help_forms:
                        check(f"form-kind-unread: {contract}", False, f"{row}: {type(exc).__name__}: {exc}")
                    else:
                        check(f"{row}: crashed: {type(exc).__name__}", False, str(exc))
                    continue
                problems = [p for p in problems if p.path not in skip and not (p.kind == "blank" and HC._code_fills(p.path))]
                if contract in help_forms:
                    stray = [p for p in problems if re.sub(r"\[\d+\]", "[]", p.path) not in spec]
                    if stray:
                        check(f"form-kind-unread: {contract}", False, f"{row}: refused on {[p.path for p in stray]}")
                        continue
                if variant == FF.BEYOND_LIMIT:
                    beyond = {f.path for f in filled.fills if isinstance(f.value, str)
                              and spec[re.sub(r"\[\d+\]", "[]", f.path)].max_len
                              and len(f.value) > spec[re.sub(r"\[\d+\]", "[]", f.path)].max_len}
                    refused = {p.path for p in problems if p.limit}
                    other = [p.path for p in problems if not p.limit]
                    check(row, refused == beyond and not other,
                          f"BEYOND not refused by the reader: {sorted(beyond - refused)}; other problems {other[:3]}")
                else:
                    check(row, not problems, "; ".join(p.line()[:140] for p in problems[:3]))
        # the negative rows: what the reader MUST refuse (E5, E6)
        negatives = [
            ("owed rows absent are refused", "s2-stage-critic-to-tester", "concerns", {"findings": FF.ABSENT}, "findings"),
            ("scope [] without a null outcome is refused", "s3-strategist-to-designer", "ok", {"scope": []}, "scope"),
        ]
        base = FF.fill_form("s2-stage-critic-to-tester", ctx, verdict="concerns")
        unfilled = {f.path: f.hint for f in base.fills if f.path.startswith("stage_acceptance.")}
        negatives.append(("an owed section left as the template is refused", "s2-stage-critic-to-tester", "concerns", unfilled,
                          "stage_acceptance"))
        for name, contract, verdict, overrides, path in negatives:
            filled = FF.fill_form(contract, ctx, verdict=verdict, overrides=overrides)
            _doc, _fixed, problems, _judged, _derived = HC.check(
                handoff.parse(filled.text), contract, HC.Artifacts(root, dispatch=f"{contract}-w1"), fix=False, use_judge=False)
            hit = [p for p in problems if p.path == path or p.path.startswith(path + ".")]
            check(f"reader: {name}", bool(hit) and not filled.unfillable, f"problems {[p.path for p in problems][:4]}")
    finally:
        handoff.vocabulary = real_vocabulary
        harness.cleanup(root)
    for (contract, path, hint), why in sorted(seen.items()):
        check(f"unfillable {contract}:{path} «{hint}»", False, why)
    check("the walk walked forms, variants and fields", bool(forms) and rows > 0 and fields > 0, f"{len(forms)}, {rows}, {fields}")
    check("every form has at least as many variants as header_verdicts words", not short, str(short))
    print(f"forms {len(forms)}, variants {rows}, fields {fields}, unfillable {len(seen)}, left_for_code {left_total}")


def _stage_json_outputs() -> set:
    """The output names of references/stages.json, read here a second time and by its own keys: the pin against `stage_outputs()`."""
    names = set()
    for stage in json.loads((harness.PLUGIN_ROOT / "references" / "stages.json").read_text(encoding="utf-8"))["stages"]:
        names.update(stage.get("outputs") or [])
        names.update(d["output"] for d in stage.get("optional_dispatches") or [] if isinstance(d, dict) and d.get("output"))
    return names


def every_stage_output_fills_or_is_named() -> None:
    """P1-a N2a (C8): every output of every stage is classified into exactly one of three named results (`FilledArtifact`, `ByCode`,
    `NotCovered`), and a filled one is read by its own reader (`validate_artifacts.collect_errors`).

    Row id `output: <name>[<variant>]`. A role-written output with neither a template nor a `not_covered` row, an output with no
    writer, a stale row, an unfillable hint and a refusal on a filled output are red rows. An output no reader refuses even with its first
    required field gone is NAMED in the summary (`outputs no reader refuses`), a `NotCovered` one too; neither is red (E7, E21)."""
    import form_filler as FF
    import validate_artifacts as VA
    ctx = FF.FillContext(task_key="TP1-1", dispatch_id="S1-dispatch-1", cases=["TC-001", "TC-002"], bugs=["BUG-1", "BUG-2"],
                         minted={"P": ["P-1"], "TC": ["TC-001"]})
    try:
        pairs = FF.stage_outputs()
    except Exception as exc:                       # an unreadable table is red, never "no outputs"
        check("stage_outputs() reads references/stages.json", False, f"{type(exc).__name__}: {exc}")
        return
    names = list(dict.fromkeys(name for _stage, name in pairs))
    listed = _stage_json_outputs()
    check("the table walked outputs of the stages", bool(names) and bool(listed), f"{len(names)} / {len(listed)}")
    for name in sorted(listed - set(names)):
        check(f"output {name}: stages.json names it, the table has no row", False, "stage_outputs() does not return it")
    for name in sorted(set(names) - listed):
        check(f"table row {name} names no output of stages.json", False, "stage_outputs() returns it")
    tables = FF.rules()
    subkinds = sorted(key for key, row in tables["artifact_templates"].items() if row.get("subkind_of"))
    languages = FF.test_file_languages()
    walked = [name for key in subkinds for name in ([key.replace(FF.LANG, lang) for lang in languages] if FF.LANG in key else [key])]
    check("the table walks every language of detectors.json and every runner key of case-markers.json", len(languages) > 1 and len(walked) >= len(subkinds),
          str(languages))
    for section in ("artifact_templates", "not_covered"):
        for key in tables[section]:
            if key in subkinds:
                parent = tables[section][key]["subkind_of"]
                if parent not in names:
                    check(f"stale fill row {key}", False, f"the sub-kind names {parent}, which is no output of stages.json")
                continue
            if key not in names:
                check(f"stale fill row {key}", False, f"{section} names an output no stage of stages.json lists")
                continue
            try:
                code_written = not FF.writer_of(key).endswith(FF.ROLE_WRITER)
            except FF.Unclassified:
                continue                           # said by the row of the output itself
            if code_written:
                check(f"stale fill row {key}", False, f"{section} names an output whose writer is code ({FF.writer_of(key)})")
    root = harness.temp_dir()
    by_code, not_covered, unread, rows, filled_count = 0, [], [], 0, 0

    def task_root_of(world):
        return world / "qa-factory" / "artifacts" / ctx.task_key

    def refusals(world, result) -> list:
        """What the reader says of every file of `result` written into `world`. The world is a project (marker + the register the
        cases cover), and the hook layer is pointed at it for the call: a case is read against the register of ITS project."""
        if not (world / "qa-factory" / "config.json").is_file():
            harness.mark_project(world)
            FF.write_outputs(task_root_of(world), world, FF.fill_artifact("work/requirements-register.md", ctx).require())
            FF.write_outputs(task_root_of(world), world, FF.fill_artifact("test_file:pytest", ctx).require())   # the file a manifest row names
            if result.output == "manifest_row":        # a manifest row is read against the plan row it serves and the case it covers
                FF.write_outputs(task_root_of(world), world, FF.fill_artifact("test-plan.md", ctx).require())
                FF.write_outputs(task_root_of(world), world, FF.fill_artifact("case", ctx, variant="cite_hint:body:Plan row:").require())
        old = os.environ.get("CLAUDE_PROJECT_DIR")
        os.environ["CLAUDE_PROJECT_DIR"] = str(world)
        hooklib._PROJECT_ROOT_CACHE = None
        try:
            return [e for path in FF.write_outputs(task_root_of(world), world, result) for e in VA.collect_errors(path, {})]
        finally:
            if old is None:
                os.environ.pop("CLAUDE_PROJECT_DIR", None)
            else:
                os.environ["CLAUDE_PROJECT_DIR"] = old
            hooklib._PROJECT_ROOT_CACHE = None
    try:
        for name in names + walked:
            row = f"output: {name}[base]"
            try:
                kind = FF.classify(name)
            except FF.Unclassified as exc:
                check(str(exc), False, "the table cannot place this output")
                continue
            try:
                result = FF.fill_artifact(name, ctx)
            except Exception as exc:               # E14 by analogy: an exception is never a pass
                check(f"{row}: crashed: {type(exc).__name__}", False, str(exc))
                continue
            rows += 1
            if isinstance(result, FF.ByCode):
                by_code += 1
                check(row, kind == "code" and result.writer == FF.writer_of(name) and bool(result.writer.strip()), f"{kind} / {result.writer!r}")
            elif isinstance(result, FF.NotCovered):
                not_covered.append((name, result.why))
                check(row, kind == "not_covered" and bool(result.why.strip()), f"{kind} / {result.why!r}")
            else:
                filled_count += 1
                check(f"{row}: classified as role", kind == "role", kind)
                for u in result.unfillable:
                    check(f"unfillable output {name}:{u.path} «{u.hint}»", False, u.why)
                if result.unfillable:
                    continue
                template = FF._row_of(name)
                contract_lines = [ln.rstrip() for ln in (harness.PLUGIN_ROOT / template["contract"]).read_text(encoding="utf-8").splitlines()]
                check(f"output: {name}[anchor]", template["anchor"] in contract_lines, f"{template['contract']} has no line {template['anchor']!r}")
                errors = refusals(root / ("manifest" if name == "manifest_row" else "base"), result)   # a manifest row has a world of its own: one case, its plan row
                check(row, errors == [], "; ".join(errors))                  # the whole refusal: no printed list is cut
                for variant in FF.artifact_variants(name, ctx)[1:]:          # the citation read by its own hint (3.5)
                    cited = FF.fill_artifact(name, ctx, variant=variant)
                    for u in cited.unfillable:
                        check(f"unfillable output {name}[{variant}]:{u.path} «{u.hint}»", False, u.why)
                    errors = [] if cited.unfillable else refusals(root / "base", cited)
                    check(f"output: {name}[{variant}]", not cited.unfillable and errors == [] and cited.files != result.files,
                          "; ".join(errors) or "the variant wrote the same bytes as the base")
                required = FF.required_of(name)
                if not required:
                    unread.append(name)            # nothing to remove: no broken variant can be built
                    continue
                broken = FF.fill_artifact(name, ctx, overrides={required[0]: FF.ABSENT})
                variant = f"ABSENT {required[0]}"
                check(f"output: {name}[{variant}]: the override lands", not broken.unfillable, str([(u.path, u.why) for u in broken.unfillable]))
                if not broken.unfillable and not refusals(root / f"broken-{rows}", broken):
                    unread.append(name)
        # the rows of the S3-S4 group (E24 directory outputs, the citation of an issued id, the sections code writes)
        cases_dir, case_name, plan_json = "work/test-cases/", "case", "work/test-plan.json"
        two = FF.fill_artifact(cases_dir, ctx)
        check(f"output: {cases_dir}[two cases, two files]", sorted(two.files) == [f"{cases_dir}general/TC-001.md", f"{cases_dir}general/TC-002.md"]
              and all(f"id: {Path(p).stem}\n" in t for p, t in two.files.items()), str(sorted(two.files)))
        one = FF.fill_artifact(case_name, ctx)
        check(f"output: {case_name}[one document of the first id]", sorted(one.files) == [f"{cases_dir}general/TC-001.md"], str(sorted(one.files)))
        empty_ctx = FF.FillContext(task_key="TP1-1", minted={"P": ["P-1"]})
        empty = FF.fill_artifact(cases_dir, empty_ctx)
        shown = [(u.path, u.why) for u in empty.unfillable]
        check(f"output: {cases_dir}: no case in the context", not empty.files and len(empty.unfillable) == 1 and empty.unfillable[0].path == cases_dir
              and empty.unfillable[0].why.startswith("no ids in ctx for a directory output"), str(shown))
        try:
            FF.write_outputs(task_root_of(root / "e24"), root / "e24", empty)
            check(f"output: {cases_dir}: no case in the context[nothing is written]", False, "no error")
        except FF.NotFillable:
            check(f"output: {cases_dir}: no case in the context[nothing is written]", not (root / "e24").exists(), "something was written")
        (task_root_of(root / "e24b") / "work" / "test-cases").mkdir(parents=True)
        said = VA.collect_errors(task_root_of(root / "e24b") / "work" / "test-cases", {})
        check(f"output: {cases_dir}: the reader on an empty folder", said == [], f"collect_errors says {said!r}")
        print(f"collect_errors on an empty {cases_dir} folder says: {said!r}")
        for name, ids in (("an id that escapes the folder", ["../x"]), ("an id that is empty", [""]), ("an id twice", ["TC-001", "TC-001"])):
            got = FF.fill_artifact(cases_dir, FF.FillContext(task_key="TP1-1", minted={"P": ["P-1"]}, cases=ids))
            if ids == ["../x"]:
                try:
                    FF.write_outputs(task_root_of(root / "e22b"), root / "e22b", got)
                    check(f"output: {cases_dir}[{name}]", False, "write_outputs wrote it")
                except ValueError:
                    check(f"output: {cases_dir}[{name}]", not (root / "e22b").exists() or not list((root / "e22b").rglob("x.md")), "a file was written")
            else:
                check(f"output: {cases_dir}[{name}]", len(got.unfillable) >= 1 and (name != "an id twice" or len(got.files) == 1), str(shown))
        for name, minted in (("no issued id", {}), ("an empty list of issued ids", {"P": []})):
            got = FF.fill_artifact(case_name, FF.FillContext(task_key="TP1-1", cases=["TC-001"], minted=minted))
            check(f"output: {case_name}[{name}: unfillable naming the hint]", [(u.path, u.hint) for u in got.unfillable] == [("body:Plan row: <TS-n>", "<TS-n>")],
                  str([(u.path, u.hint, u.why) for u in got.unfillable]))
        same = FF.FillContext(task_key="TP1-1", cases=["TC-001"], minted={"P": ["TS-1"]})
        check(f"output: {case_name}[the issued id has the hint's own prefix: no cite_hint variant]", FF.artifact_variants(case_name, same) == ["base"]
              and "Plan row: TS-1\n" in FF.fill_artifact(case_name, same).files[f"{cases_dir}general/TC-001.md"], str(FF.artifact_variants(case_name, same)))
        base_text, cite = one.files[f"{cases_dir}general/TC-001.md"], FF.artifact_variants(case_name, ctx)
        cited_text = FF.fill_artifact(case_name, ctx, variant=cite[1]).files[f"{cases_dir}general/TC-001.md"] if len(cite) > 1 else ""
        check(f"output: {case_name}[base cites the issued id, the variant the hint's own]", cite == ["base", "cite_hint:body:Plan row:"]
              and "Plan row: P-1\n" in base_text and "Plan row: TS-1\n" in cited_text, str(cite))
        over = FF.fill_artifact(case_name, ctx, variant="cite_hint:body:Plan row:", overrides={"body:Plan row:": "Plan row: X-9"})
        check(f"output: {case_name}[an override beats the cite_hint of its path]", "Plan row: X-9\n" in over.files[f"{cases_dir}general/TC-001.md"]
              and not over.unfillable, str(over.unfillable))
        try:
            FF.fill_artifact(plan_json, ctx, variant="cite_hint:rows")
            check(f"output: {plan_json}[a cite_hint the output does not have raises]", False, "no error")
        except ValueError:
            check(f"output: {plan_json}[a cite_hint the output does not have raises]", True)
        grounding = FF.fill_artifact("work/grounding.yaml", ctx)
        keys = {line.split(":")[0] for line in grounding.files["work/grounding.yaml"].splitlines() if line and not line.startswith(" ")}
        check("output: work/grounding.yaml[the sections code writes are left_for_code, not filled]", bool(grounding.left_for_code)
              and not keys & set(grounding.left_for_code) and keys == {"rows", "claims"}, f"keys {sorted(keys)}, left {grounding.left_for_code}")
        for name in ("plan_md_row", "plan_json_row"):
            check(f"output: {name}[lands at the path of its parent]", list(FF.fill_artifact(name, ctx).files) ==
                  [FF._row_of(name)["path"]] and FF._row_of(name)["path"] == tables["artifact_templates"][name]["subkind_of"], str(list(FF.fill_artifact(name, ctx).files)))
        # the rows of the S5-S6 group (the fields of a manifest row from the module, the case marker from its file, per-case sub-kinds)
        import window_record as WR
        row_name, test_name, manifest_out = "manifest_row", "test_file:pytest", "work/automation-manifest.json"
        fields = list(WR.REQUIRED_ROW_FIELDS)
        made = json.loads(FF.fill_artifact(row_name, ctx).files[manifest_out])["tests"][0]
        check(f"output: {row_name}[the row holds exactly the fields of window_record.REQUIRED_ROW_FIELDS]", bool(fields) and all(f in made for f in fields)
              and FF.required_of(row_name)[:len(fields)] == [f"tests[0].{f}" for f in fields], f"fields {fields}, row {sorted(made)}")
        check(f"output: {row_name}[its marker and file are the ones of {test_name}]", made["marker"] == "TC-001" and made["covers"] == ["TC-001"]
              and f"project:{made['file'].removeprefix('qa-factory/')}" in FF.fill_artifact(test_name, ctx).files, f"{made['file']} / {list(FF.fill_artifact(test_name, ctx).files)}")
        check(f"output: {row_name}[the obligation refs are objects with an id and a hash]", isinstance(made["obligation_refs"], list)
              and sorted(made["obligation_refs"][0]) == ["obligation_hash", "obligation_id"], str(made["obligation_refs"]))
        for field_name in fields:                      # E20 on every field the module names: ABSENT removes exactly that key
            got = FF.fill_artifact(row_name, ctx, overrides={f"tests[0].{field_name}": FF.ABSENT})
            kept = json.loads(got.files[manifest_out])["tests"][0] if got.files else {}
            check(f"output: {row_name}[ABSENT tests[0].{field_name}: the override lands]", not got.unfillable and field_name not in kept
                  and all(f in kept for f in fields if f != field_name), str([(u.path, u.why) for u in got.unfillable]))
        lost = FF.fill_artifact(row_name, ctx, overrides={"tests": FF.ABSENT})
        check(f"output: {row_name}[control: the reader refuses a manifest with no tests]", not lost.unfillable and any("'tests' is missing" in e for e in refusals(root / "control", lost)),
              "collect_errors did not refuse it")
        saved, kept_module = dict(WR.REQUIRED_ROW_FIELDS), sys.modules.get("window_record")
        try:
            WR.REQUIRED_ROW_FIELDS["zz_new_field"] = WR.RowField("a field added after the rules were written", "always", (), "automator", WR.FRAGMENT_DOOR, True)
            grown = FF.fill_artifact(row_name, ctx)
            check(f"output: {row_name}[a field the module gains is in the row, no list is copied]", "zz_new_field" in json.loads(grown.files[manifest_out])["tests"][0]
                  and not grown.unfillable and "tests[0].zz_new_field" in FF.required_of(row_name), str(grown.unfillable))
            del WR.REQUIRED_ROW_FIELDS["zz_new_field"]
            del WR.REQUIRED_ROW_FIELDS["obligation_refs"]
            stale = FF.fill_artifact(row_name, ctx)
            check(f"output: {row_name}[a shape for a field the module lost is unfillable]", [u.path for u in stale.unfillable] == ["tests[0].obligation_refs"], str([(u.path, u.why) for u in stale.unfillable]))
            WR.REQUIRED_ROW_FIELDS.clear()
            empty_list = FF.fill_artifact(row_name, ctx)
            check(f"output: {row_name}[REQUIRED_ROW_FIELDS empty: unfillable naming the module, never an empty row]", len(empty_list.unfillable) == 1
                  and "window_record" in empty_list.unfillable[0].why and "empty" in empty_list.unfillable[0].why, str([(u.path, u.why) for u in empty_list.unfillable]))
            try:
                FF.write_outputs(task_root_of(root / "emptyrow"), root / "emptyrow", empty_list)
                check(f"output: {row_name}[REQUIRED_ROW_FIELDS empty: nothing is written]", False, "no error")
            except FF.NotFillable:
                check(f"output: {row_name}[REQUIRED_ROW_FIELDS empty: nothing is written]", not (root / "emptyrow").exists(), "something was written")
            sys.modules["window_record"] = None            # an import of it now raises
            gone = FF.fill_artifact(row_name, ctx)
            check(f"output: {row_name}[window_record not importable: unfillable naming the module]", len(gone.unfillable) == 1 and "window_record" in gone.unfillable[0].why
                  and "cannot supply" in gone.unfillable[0].why, str([(u.path, u.why) for u in gone.unfillable]))
        finally:
            WR.REQUIRED_ROW_FIELDS.clear()
            WR.REQUIRED_ROW_FIELDS.update(saved)
            if kept_module is None:
                sys.modules.pop("window_record", None)
            else:
                sys.modules["window_record"] = kept_module
        check(f"output: {row_name}[the module is restored for the rows after this one]", list(WR.REQUIRED_ROW_FIELDS) == fields, str(list(WR.REQUIRED_ROW_FIELDS)))
        marker_text = FF.fill_artifact(test_name, ctx).files["project:tests/TC-001_test.py"]
        check(f"output: {test_name}[the marker is the prefix and the name of case-markers.json]", '@pytest.mark.qa(case="TC-001", then=[1])\n' in marker_text, marker_text)
        old_references = FF.REFERENCES
        for name, content, language, wanted in (
                ("the file is missing", None, "pytest", "cannot be read"), ("the file is not JSON", "{not json", "pytest", "cannot be read"),
                ("the file is not an object", "[1]", "pytest", "not a JSON object"),
                ("no entry for the language", '{"decorator_prefix": "@pytest.mark.", "pytest": {"case": "qa"}}', "java", "no marker form for the language java"),
                ("the entry has no marker name", '{"decorator_prefix": "@pytest.mark.", "pytest": {}}', "pytest", "empty marker form"),
                ("the marker name is empty", '{"decorator_prefix": "@pytest.mark.", "pytest": {"case": "  "}}', "python", "empty marker form"),
                ("the prefix is empty", '{"decorator_prefix": "", "pytest": {"case": "qa"}}', "pytest", "`decorator_prefix` is empty"),
                ("the name of the language is a key that is no entry", '{"decorator_prefix": "@pytest.mark.", "note": "x", "pytest": {"case": "qa"}}', "note", "no marker form for the language note")):
            fake = harness.temp_dir()
            try:
                (fake / "detectors.json").write_bytes((old_references / "detectors.json").read_bytes())
                if content is not None:
                    (fake / "case-markers.json").write_text(content, encoding="utf-8")
                FF.REFERENCES = fake
                got = FF.fill_artifact(f"test_file:{language}", ctx)
                said = got.unfillable[0].why if got.unfillable else ""
                check(f"output: test_file:{language}[{name}: unfillable naming the file and the language]", len(got.unfillable) == 1 and not got.files
                      and "case-markers.json" in said and language in said and wanted in said, str([(u.path, u.hint, u.why) for u in got.unfillable]))
            finally:
                FF.REFERENCES = old_references
                harness.cleanup(fake)
        for name in (row_name, test_name):             # a sub-kind per case, with no case in the context: no file, a named line (as the case directory)
            got = FF.fill_artifact(name, empty_ctx)
            check(f"output: {name}[no case in the context]", not got.files and len(got.unfillable) == 1 and got.unfillable[0].path == name
                  and got.unfillable[0].why.startswith("no ids in ctx for a directory output"), str([(u.path, u.why) for u in got.unfillable]))
            try:
                FF.write_outputs(task_root_of(root / "nocase"), root / "nocase", got)
                check(f"output: {name}[no case in the context: nothing is written]", False, "no error")
            except FF.NotFillable:
                check(f"output: {name}[no case in the context: nothing is written]", not (root / "nocase").exists(), "something was written")
        escape = FF.fill_artifact(test_name, FF.FillContext(task_key="TP1-1", cases=["../x"]))
        try:
            FF.write_outputs(task_root_of(root / "e22t"), root / "e22t", escape)
            check(f"output: {test_name}[an id that escapes the folder]", False, "write_outputs wrote it")
        except ValueError:
            check(f"output: {test_name}[an id that escapes the folder]", not (root / "e22t").exists() or not list((root / "e22t").rglob("x_test.py")), "a file was written")
        for name in ("work/s5-plan.json", "work/s5-notes/", "work/evidence/manual/<case>/tried.md"):
            got = FF.fill_artifact(name, ctx)
            check(f"output: {name}[named, not covered]", isinstance(got, FF.NotCovered) and name in names and "not landed" not in got.why, repr(got))
        check("output: work/evidence/manual/<case>/tried.md[the stage table writes the placeholder, the filler writes no folder of that name]",
              not [p for p in root.rglob("*") if "<" in p.name or ">" in p.name], str([str(p) for p in root.rglob("*") if "<" in p.name]))
        # the rows of the S7-S9 group (a file per bug of the context, the cited case, the report's rows per case, the project files with no shape)
        import contract as C
        triage, drafts, bugs_dir, report, retro = "work/triage.json", "work/bug-drafts/", "project:bugs/", "test-report.md", "retro.md"
        made = json.loads(FF.fill_artifact(triage, ctx).files[triage])["triage"][0]
        check(f"output: {triage}[the verdict of the template is a word of contract.TRIAGE_VERDICTS, the evidence is not empty]",
              made["verdict"] in C.TRIAGE_VERDICTS and bool(str(made["evidence"]).strip()), str(made))
        two_drafts, two_bugs = FF.fill_artifact(drafts, ctx), FF.fill_artifact(bugs_dir, ctx)
        check(f"output: {drafts}[two bugs, two files, each citing the case the context issued]", sorted(two_drafts.files) == [f"{drafts}BUG-1.json", f"{drafts}BUG-2.json"]
              and all(json.loads(t)["case"] == "TC-001" for t in two_drafts.files.values()), str(sorted(two_drafts.files)))
        check(f"output: {bugs_dir}[two bugs, two files, each naming the draft file of its own bug]", sorted(two_bugs.files) == [f"{bugs_dir}BUG-1.md", f"{bugs_dir}BUG-2.md"]
              and all(f"source_draft: {drafts}{Path(p).stem}.json\n" in t and f"{drafts}{Path(p).stem}.json" in two_drafts.files and "cases: [TC-001]\n" in t
                      for p, t in two_bugs.files.items()), str(sorted(two_bugs.files)))
        placed = FF.write_outputs(task_root_of(root / "s7"), root / "s7", two_bugs) + FF.write_outputs(task_root_of(root / "s7"), root / "s7", two_drafts)
        check(f"output: {bugs_dir}[a bug file lands under the project's qa-factory/bugs/, a draft under the task's work/bug-drafts/]",
              placed == [(root / "s7" / "qa-factory" / "bugs" / f"BUG-{n}.md").resolve() for n in (1, 2)]
              + [(task_root_of(root / "s7") / "work" / "bug-drafts" / f"BUG-{n}.json").resolve() for n in (1, 2)], str(placed))
        for name in (drafts, bugs_dir):
            none = FF.fill_artifact(name, empty_ctx)
            check(f"output: {name}[no bug in the context: no file, a named line]", not none.files and [u.path for u in none.unfillable] == [name]
                  and none.unfillable[0].why.startswith("no ids in ctx for a directory output (ctx.bugs"), str([(u.path, u.why) for u in none.unfillable]))
            try:
                FF.write_outputs(task_root_of(root / "nobug"), root / "nobug", none)
                check(f"output: {name}[no bug in the context: nothing is written]", False, "no error")
            except FF.NotFillable:
                check(f"output: {name}[no bug in the context: nothing is written]", not (root / "nobug").exists(), "something was written")
            for what, ids in (("an id that escapes the folder", ["../x"]), ("an id that is empty", [""]), ("an id twice", ["BUG-1", "BUG-1"])):
                got = FF.fill_artifact(name, FF.FillContext(task_key="TP1-1", bugs=ids, minted={"TC": ["TC-001"]}))
                if ids == ["../x"]:
                    try:
                        FF.write_outputs(task_root_of(root / "e22bug"), root / "e22bug", got)
                        check(f"output: {name}[{what}]", False, "write_outputs wrote it")
                    except ValueError:
                        check(f"output: {name}[{what}]", not (root / "e22bug").exists() or not list((root / "e22bug").rglob("x.*")), "a file was written")
                else:
                    check(f"output: {name}[{what}]", len(got.unfillable) >= 1 and (what != "an id twice" or len(got.files) == 1), str([(u.path, u.why) for u in got.unfillable]))
            for what, minted in (("no issued case", {}), ("an empty list of issued cases", {"TC": []})):
                got = FF.fill_artifact(name, FF.FillContext(task_key="TP1-1", bugs=["BUG-1"], minted=minted))
                check(f"output: {name}[{what}: unfillable naming the hint]", [(u.path, u.hint) for u in got.unfillable] == [("case" if name == drafts else "cases", "<TC-n>")],
                      str([(u.path, u.hint, u.why) for u in got.unfillable]))
        both = FF.fill_artifact(drafts, ctx, overrides={"title": FF.ABSENT})
        check(f"output: {drafts}[ABSENT title lands in every file]", not both.unfillable and all("title" not in json.loads(t) for t in both.files.values()), str(both.unfillable))
        for name, wrong in ((triage, "triage[3].test"), (drafts, "nowhere.x"), (retro, "body:## Nowhere")):
            got = FF.fill_artifact(name, ctx, overrides={wrong: 1})
            check(f"output: {name}[override missing path {wrong}]", [u.path for u in got.unfillable][:1] == [wrong] and got.unfillable[0].why.startswith("override names no field of"),
                  str([(u.path, u.why) for u in got.unfillable]))
        for name in ("work/ledger.json", "work/ledger.md", "work/proposals/"):
            check(f"output: {name}[written by code: the filler names the writer and writes nothing]", FF.classify(name) == "code" and isinstance(FF.fill_artifact(name, ctx), FF.ByCode)
                  and name in names, FF.classify(name))
        shapeless = "project:obligations.md", "project:factory-backlog.md"
        for name in shapeless:
            got = FF.fill_artifact(name, ctx)
            check(f"output: {name}[named, not covered: no shape in the contract]", isinstance(got, FF.NotCovered) and got.why == 'no shape in artifact-contract.md "Project-level files"'
                  and names.count(name) == 1, repr(got))
        both_stages = sorted(stage for stage, name in pairs if name == shapeless[0])
        check(f"output: {shapeless[0]}[named by two stages, one template row for both]", len(both_stages) == 2, str(both_stages))
        heading = "## Project-level files"
        contract_lines = (harness.PLUGIN_ROOT / "references" / "artifact-contract.md").read_text(encoding="utf-8").splitlines()
        found_at = next((i for i, ln in enumerate(contract_lines) if ln.rstrip() == heading), None)
        if found_at is None:                           # found by the HEADING, never by a line number: a heading that is gone is red
            check(f"output: project-level files[artifact-contract.md has the heading {heading!r}]", False, "heading absent: re-judge the not_covered rows of the two project files")
        else:
            body = []
            for line in contract_lines[found_at + 1:]:
                if line.startswith("#"):
                    break
                body.append(line)
            shaped = [ln for ln in body if ln.lstrip().startswith(("|", "```", "---"))]
            check("output: project-level files[the section names the two files and gives no table, fence or front matter]",
                  not shaped and all(any(Path(n.split(":", 1)[1]).stem in ln for ln in body) for n in shapeless), str(shaped))
        base_files = FF.fill_artifact(triage, ctx).files
        saved_root = FF.ROOT
        for what, edit in (("the heading moved down three lines", lambda t: "\n\n\n" + t), ("the heading renamed", lambda t: t.replace("## `triage.json`", "## `triage-rows.json`"))):
            fake = harness.temp_dir()
            try:
                (fake / "references").mkdir()
                (fake / "references" / "artifact-contract-run.md").write_text(edit((saved_root / "references" / "artifact-contract-run.md").read_text(encoding="utf-8")),
                                                                              encoding="utf-8")
                FF.ROOT = fake
                got = FF.fill_artifact(triage, ctx)
            finally:
                FF.ROOT = saved_root
                harness.cleanup(fake)
            if "moved" in what:
                check(f"output: {triage}[{what}: found by its heading, the same bytes]", not got.unfillable and got.files == base_files, str(got.unfillable))
            else:
                check(f"output: {triage}[{what}: unfillable naming the file and the heading, no file]", not got.files and len(got.unfillable) == 1
                      and "artifact-contract-run.md" in got.unfillable[0].why and "## `triage.json`" in got.unfillable[0].why, str([(u.path, u.why) for u in got.unfillable]))
        text2 = FF.fill_artifact(report, ctx).files[report]
        appendix = [ln for ln in text2.splitlines() if ln.startswith("| R-1 |")]
        left = [ln for ln in text2.splitlines() if ln.startswith("1. ") and "To check:" in ln]
        check(f"output: {report}[two cases: two appendix rows and two items, each naming its case]", [ln.split("|")[2].strip() for ln in appendix] == ctx.cases
              and len(left) == 2 and all(f"R-1, {c})" in ln for ln, c in zip(left, ctx.cases)), str(appendix + left))
        piped = FF.fill_artifact(report, FF.FillContext(task_key="TP1-1", cases=["TC|1"])).files[report]
        check(f"output: {report}[a bar in a case id goes through grammar.escape_cell in the appendix row only]", "| R-1 | TC\\|1 | pass |\n" in piped and "(R-1, TC|1)" in piped, "the bar was not escaped")
        got = FF.fill_artifact(report, FF.FillContext(task_key="TP1-1"))
        check(f"output: {report}[no case in the context: unfillable naming the token]", {u.hint for u in got.unfillable} == {"<case id>"}, str([(u.path, u.hint) for u in got.unfillable]))
        got = FF.fill_artifact(report, FF.FillContext(task_key="TP1-1", cases=["TC-001", "TC-001", ""]))
        check(f"output: {report}[a repeated or empty id: unfillable, one row per distinct id]", len([u for u in got.unfillable if "empty or repeated" in u.why]) == 2
              and len([ln for ln in got.files[report].splitlines() if ln.startswith("| R-1 |")]) == 1, str([(u.path, u.why) for u in got.unfillable]))
        unfilled = []
        nothing = FF._fill_md("synthetic", {"template": "x: < >\n"}, ctx, {}, [], unfilled)
        check("output: synthetic template[a hint no rule fills is unfillable, the text stays as written]", [u.why for u in unfilled] == ["the template holds no hint for this field"]
              and nothing == "x: < >\n", str(unfilled))
        check("output: E16[no row of not_covered says a group has not landed]", not [(n, w) for n, w in tables["not_covered"].items() if "not landed" in w],
              str([(n, w) for n, w in tables["not_covered"].items() if "not landed" in w]))
        # the rows of the interface itself (E20, E22, the escape of a cell, determinism)
        manifest, register, understanding = "work/context-manifest.json", "work/requirements-register.md", "understanding.md"
        for name, overrides, wanted in (
                (manifest, {"nowhere.x": 1}, "nowhere.x"), (manifest, {"related[3].key": "x"}, "related[3].key"),
                (register, {"nowhere": 1}, "nowhere"), (understanding, {"body:## Nowhere": FF.ABSENT}, "body:## Nowhere")):
            got = FF.fill_artifact(name, ctx, overrides=overrides)
            check(f"output: {name}[override missing path {wanted}]",
                  [u.path for u in got.unfillable] == [wanted] and got.unfillable[0].why == f"override names no field of {name}",
                  str([(u.path, u.why) for u in got.unfillable]))
        landed = json.loads(FF.fill_artifact(manifest, ctx, overrides={"related[].key": "ZZ-9", "related[0].source": "one"}).files[manifest])
        check(f"output: {manifest}[override section[] and section[0]]", landed["related"][0]["key"] == "ZZ-9" and landed["related"][0]["source"] == "one",
              str(landed["related"]))
        check(f"output: {register}[override front matter key lands verbatim]",
              "confidence: low\n" in FF.fill_artifact(register, ctx, overrides={"confidence": "low"}).files[register], "no `confidence: low` line")
        check(f"output: {understanding}[override body line ABSENT removes the line]",
              "## Why this change" not in FF.fill_artifact(understanding, ctx, overrides={"body:## Why this change": FF.ABSENT}).files[understanding], "heading kept")
        check(f"output: {manifest}[same input, same bytes]", FF.fill_artifact(manifest, ctx).files == FF.fill_artifact(manifest, ctx).files, "bytes differ")
        check(f"output: {manifest}[token with no key in the context]", [u.path for u in FF.fill_artifact(manifest, FF.FillContext(task_key="")).unfillable] == ["ticket"],
              "the empty task key was written")
        cell = FF._fill_md("synthetic", {"template": "| <TICKET> | x |\n"}, FF.FillContext(task_key="A|B"), {}, [], [])
        check("output: synthetic table row[a bar in a cell goes through grammar.escape_cell]", cell == "| A\\|B | x |\n", repr(cell))
        for name, bad in (("a parent step", "../escape.txt"), ("a step inside", "work/../../escape.txt"), ("an absolute path", str(root / "abs.txt")),
                          ("a project parent step", "project:../escape.txt"), ("an empty path", "")):
            try:
                FF.write_outputs(task_root_of(root / "e22"), root / "e22", FF.FilledArtifact("synthetic", {"work/ok.txt": "x", bad: "y"}, [], [], []))
                check(f"output: synthetic[write_outputs refuses {name}]", False, "no error")
            except ValueError:
                check(f"output: synthetic[write_outputs refuses {name}]", not (task_root_of(root / "e22") / "work" / "ok.txt").exists() and not (root / "escape.txt").exists(),
                      "something was written before the refusal")
        placed = FF.write_outputs(task_root_of(root / "e22"), root / "e22", FF.FilledArtifact("synthetic", {"work/ok.txt": "x", "project:probe.md": "y"}, [], [], []))
        check("output: synthetic[write_outputs: a story file under the task root, a project file under qa-factory/]",
              placed == [(task_root_of(root / "e22") / "work" / "ok.txt").resolve(), (root / "e22" / "qa-factory" / "probe.md").resolve()], str(placed))
        try:
            FF.write_outputs(task_root_of(root / "e22"), root / "e22", FF.FilledArtifact("synthetic", {"work/never.txt": "x"}, [], [FF.Unfillable("a", "<h>", "why")], []))
            check("output: synthetic[write_outputs refuses a half-filled output]", False, "no error")
        except FF.NotFillable:
            check("output: synthetic[write_outputs refuses a half-filled output]", not (task_root_of(root / "e22") / "work" / "never.txt").exists(), "a file was written")
        try:
            FF.fill_artifact(manifest, ctx, variant="empty_lists")
            check(f"output: {manifest}[a variant the output does not have raises]", False, "no error")
        except ValueError:
            check(f"output: {manifest}[a variant the output does not have raises]", True)
    finally:
        harness.cleanup(root)
    check("the table classified every output of the stages and every sub-kind", rows == len(names) + len(walked), f"{rows} of {len(names)} + {len(walked)}")
    print(f"outputs {len(names)}, sub-kinds {len(walked)}, filled {filled_count}, by code: {by_code}, not covered {len(not_covered)}")
    for name, why in not_covered:
        print(f"not covered: {name} — {why}")
    print(f"outputs no reader refuses: {', '.join(unread) if unread else 'none'}")


def main() -> None:
    every_required_field_has_a_producer_or_a_declared_gap()
    the_two_paths_this_walk_wired()
    the_sensitivity_gap_is_reported_not_hidden()
    known_red_ledger_cases()
    form_filler_hint_cases()
    every_form_fills_from_its_own_hints()
    every_stage_output_fills_or_is_named()
    finish("test_field_producers")


if __name__ == "__main__":
    main()
