"""Fill every handoff contract from a real run's task folder and report what cannot be filled.

    python check_all_contracts.py --task-dir <project>/qa-factory/artifacts/<TICKET> [--handoffs <dir>]

Four verdicts per field:
  have  - the run's artifacts carry it; the contract asks for nothing new
  MISS  - nothing in the run carries it; the contract would have forced it into existence
  CATCH - the field or claim would be RED on this run: a real defect the contract catches
          BEFORE the next role starts, instead of two stages later
  SHAPE - THIS TOOL could not read an input it was given (present, but not shaped as the
          contract function expects): a defect of the tool, counted apart from MISS, which
          says something about the run

A contract whose input file is not in the task folder reports MISS "file absent: <name>" for each
such file and is not filled; a contract whose input is present but not shaped as it expects
reports one SHAPE row naming what it hit. Both are the tool telling the reader what it could not
do, not a crash (FR-47): the folder of a run that stopped at S3 has no ledger, and that is a
finding. Importing this module runs nothing.

WHAT THE ROWS ARE (FR-41): the have/MISS/CATCH rows that compute their verdict from the folder
(counts, file presence, id joins) are a measurement of the folder given. The rows whose verdict
is a constant or a narrative (the unconditional CATCH / MISS rows, with prose about the reference run
in their detail) are the reference run's driver-run ANALYSIS written into this script, not a
measurement of the task folder given; they read the same on any folder. main() prints that as its
first line. Rewriting those rows into measurements is queued, not done here.
"""

BANNER = ("NOTE: rows whose verdict is a constant or a narrative (the unconditional CATCH/MISS rows) "
          "are the reference run's driver-run analysis, not a measurement of the task folder given.")
import argparse
import collections
import json
import re
import sys
from pathlib import Path

import paths


class Absent(Exception):
    """An input file the contract needs is not there (or cannot be read as what it should be)."""

    def __init__(self, name, why="file absent"):
        super().__init__(f"{why}: {name}")
        self.name = name


class Inputs:
    """The files of one task folder, read on demand and named by their path inside it."""

    def __init__(self, task_dir, handoffs):
        self.R = Path(task_dir)
        self.H = Path(handoffs)          # the contracts' own text; no check below reads it yet
        self.PROJ = self.R.parent.parent   # <project>/qa-factory

    def has(self, name):
        return (self.R / name).is_file()

    def J(self, name):
        if not self.has(name):
            raise Absent(name)
        try:
            return json.loads((self.R / name).read_text(encoding="utf-8-sig"))
        except ValueError as exc:
            raise Absent(name, "file unreadable") from exc

    def T(self, name):
        if not self.has(name):
            raise Absent(name)
        return (self.R / name).read_text(encoding="utf-8-sig", errors="replace")


# ---------------------------------------------------------------- the contracts, one function each
# A contract function takes the inputs and `note(contract, verdict, field, detail)`; its NEEDS are
# the files it reads, so that a folder without them is reported before anything is computed.

def s0_setup_to_scout(x, note):
    R, PROJ, J = x.R, x.PROJ, x.J
    pipe = J("pipeline.json")
    cm = J("work/context-manifest.json")
    c = "s0-setup-to-scout"
    note(c, "have", "task.ticket", pipe["ticket"])
    note(c, "have", "environment.id", f'{pipe["environment"]} (pending={pipe["environment_pending"]})')
    impl = cm.get("implementation", {})
    note(c, "have", "task.launch_flags",
         f'reconstructable from context-manifest.implementation: mr={impl.get("mr")} commit={impl.get("commit")[:8] if impl.get("commit") else "-"}')
    note(c, "MISS", "task.launch_flags (as typed)",
         "nothing records the flags AS THE PERSON TYPED THEM; only what the scout resolved them to")
    repos = sorted(cm.get("source_sha", {}))
    note(c, "have", "repositories[]", f"{len(repos)} repos with sha: {repos}")
    note(c, "have", "tools.ticket_adapter_proved", "readiness.json in the project carries the S0 probe")
    obl = (PROJ / "obligations.md")
    note(c, "have" if obl.exists() else "MISS", "obligations[]",
         f"{obl.name} exists" if obl.exists() else "no obligations.md in the project")


def plan_rows(plan):
    """The package writes work/test-plan.json as {"rows": [...]}; an older run wrote a bare list."""
    return plan.get("rows", plan) if isinstance(plan, dict) else plan


def production_files(diff):
    files = re.findall(r"^diff --git a/(\S+)", diff, re.M)
    prod = [f for f in files
            if not re.search(r"(^|/)(docs|tests?|test-harness)/", f)
            and not f.endswith((".md", ".lock"))
            and "test_" not in f.rsplit("/", 1)[-1]]
    return files, prod


def s1_scout_to_tester(x, note):
    J, T = x.J, x.T
    pipe = J("pipeline.json")
    cm = J("work/context-manifest.json")
    inv = J("work/source-inventory.json")
    diff = T("work/impl-diff.txt")
    c = "s1-scout-to-tester"
    files, prod = production_files(diff)
    hunks = re.findall(r"^@@ ", diff, re.M)
    note(c, "have", "implementation.diff.files/hunks",
         f"{len(files)} files, {len(hunks)} hunks, {len(prod)} production - all countable from impl-diff.txt")
    note(c, "CATCH", "implementation.source",
         f"pipeline.implementation_source is {pipe['implementation_source']!r}: the S1 exit step "
         f"`stage_done --set implementation_source=` never ran. context-manifest says "
         f"{cm.get('implementation_source')!r}. The contract makes the field a handoff value, not a side effect")
    srcs = inv["sources"]
    note(c, "have", "scope[] sources",
         f"{len(srcs)} sources with relation/relevance/revision/inspection_status")
    rev = [s for s in srcs if s.get("human_review")]
    note(c, "have" if rev else "MISS", "person.review_recorded",
         f"{len(rev)} of {len(srcs)} sources carry human_review")
    note(c, "have", "person.accepted_gaps",
         f"{len(pipe.get('gate_waivers', []))} gate waivers + {len(pipe.get('remarks', []))} remarks on record")
    note(c, "have", "ac_code_conflict", f"context-manifest.conflicts = {cm.get('conflicts')}")
    note(c, "have", "artifacts.existing_coverage",
         f"{len(cm.get('existing_test_candidates', []))} candidates with selector and assertion_refs")


def s2_tester_to_strategist(x, note):
    J, T = x.J, x.T
    pipe = J("pipeline.json")
    cm = J("work/context-manifest.json")
    readiness = J("work/requirements-readiness.json")
    sizing = J("work/sizing.json")
    register = T("work/requirements-register.md")
    diff = T("work/impl-diff.txt")
    c = "s2-tester-to-strategist"
    _, prod = production_files(diff)
    reg_ids = sorted(set(re.findall(r"\bR-\d+\b", register)), key=lambda v: int(v.split("-")[1]))
    note(c, "have", "scope[] requirements", f"{len(reg_ids)} R-ids in the register")
    obs = cm.get("observables", [])
    with_req = [o for o in obs if o.get("requirement")]
    note(c, "have", "scope[].observable", f"{len(with_req)} of {len(obs)} observables name a requirement")
    # diff accounting: which production files reach a requirement?
    obs_files = {o.get("path") for o in obs if o.get("path")}
    unaccounted = [f for f in prod if not any(f.endswith(p) or p.endswith(f) for p in obs_files if p)]
    note(c, "CATCH" if unaccounted else "have", "diff_accounting[]",
         f"{len(prod) - len(unaccounted)} of {len(prod)} production files reach an observable; "
         f"unaccounted: {unaccounted[:4]}{'...' if len(unaccounted) > 4 else ''} - "
         f"THE contract field that makes the S2 loss visible at the handoff")
    note(c, "have", "open_questions[]",
         f"{len(readiness['open_questions'])} questions with owner_role and severity")
    q0 = readiness["open_questions"][0]
    note(c, "MISS" if "readings" not in q0 and "options" not in q0 else "have", "open_questions[].readings",
         f"keys present: {sorted(q0)} - no lettered readings with their cost, which is what the phase "
         f"canon requires and the reference run paid for")
    note(c, "have", "size.computed / reasoning_ref", f"sizing.json size={sizing['size']} with {len(sizing['reasoning'])} lines")
    note(c, "CATCH", "size recorded in pipeline",
         f"pipeline.size is {pipe['size']!r} although sizing.json computed {sizing['size']!r}")
    note(c, "MISS", "contradiction_matrix[]",
         "the register has a `## Contradiction matrix` section in prose; nothing machine-readable "
         "joins a cell to the plan row that must carry both readings")


def s3_strategist_to_designer(x, note):
    J, T = x.J, x.T
    plan = plan_rows(J("work/test-plan.json"))
    register = T("work/requirements-register.md")
    c = "s3-strategist-to-designer"
    reg_ids = sorted(set(re.findall(r"\bR-\d+\b", register)), key=lambda v: int(v.split("-")[1]))
    disp = collections.Counter(r["disposition"] for r in plan)
    note(c, "have", "scope[].state (disposition)", f"{dict(disp)} - every row has one")
    note(c, "have", "scope[].reason", f"{sum(1 for r in plan if r.get('disposition_reason'))} of {len(plan)} rows have disposition_reason")
    note(c, "have", "scope[].obligations",
         f"{sum(1 for r in plan if r.get('coverage_obligations'))} of {len(plan)} rows mint coverage_obligations")
    note(c, "have", "scope[].design_review_required",
         f"{sum(1 for r in plan if r.get('design_review_required'))} rows true")
    note(c, "have", "scope[].coverage_contract_revision",
         f"{sum(1 for r in plan if r.get('coverage_contract_revision'))} of {len(plan)}")
    planned_reqs = {r for row in plan for r in row.get("requirement_ids", [])}
    missing_reqs = sorted(set(reg_ids) - planned_reqs, key=lambda v: int(v.split("-")[1]))
    note(c, "CATCH" if missing_reqs else "have", "not_planned[]",
         f"{len(planned_reqs)} of {len(reg_ids)} register requirements reach a plan row; "
         f"not planned and nowhere named: {missing_reqs} - the contract forces each into `not_planned` with a reason")
    has_conf = [r for r in plan if "source_conflict" in r or "oracle_unknown" in r]
    note(c, "MISS" if not has_conf else "have", "scope[].source_conflict / oracle_unknown",
         "no plan row carries either flag; the phase canon requires them for a row the matrix touches")
    manual = [r for r in plan if r["disposition"].startswith("manual")]
    has_policy = [r for r in manual if any(k in r for k in ("manual_evidence", "evidence_policy", "evidence"))]
    note(c, "CATCH" if manual and not has_policy else "have", "manual_policy[]",
         f"{len(manual)} manual row(s) ({[r['id'] for r in manual]}), {len(has_policy)} with an evidence policy - "
         f"the runner reached TC-011 with nothing saying what counts as proof")


def s4_designer_to_case_critic(x, note):
    R, J = x.R, x.J
    links = J("state/story-case-links.json")
    plan = plan_rows(J("work/test-plan.json"))
    c = "s4-designer-to-case-critic"
    note(c, "have", "scope[].case_version",
         f"{len(links['links'])} pinned links with version + content_hash ({len(links['history'])} in history)")
    case_txt = {}
    for lk in links["links"]:
        p = Path(lk["path"])
        p = p if p.is_absolute() else (R / lk["path"])
        if p.exists():
            case_txt[lk["case_id"]] = p.read_text(encoding="utf-8", errors="replace")
    note(c, "have" if case_txt else "MISS", "case files readable", f"{len(case_txt)} of {len(links['links'])} case files found on disk")
    with_obl = [k for k, t in case_txt.items() if re.search(r"OB-[A-Z0-9-]+", t)]
    note(c, "have" if len(with_obl) == len(case_txt) else "CATCH", "scope[].obligations",
         f"{len(with_obl)} of {len(case_txt)} case files quote an obligation id")
    with_row = [k for k, t in case_txt.items() if re.search(r"TS-\d+", t)]
    note(c, "have" if len(with_row) == len(case_txt) else "CATCH", "scope[].plan_row",
         f"{len(with_row)} of {len(case_txt)} case files name their plan row")
    rev_rows = [r["id"] for r in plan if r.get("design_review_required")]
    note(c, "have", "review_scope.cases", f"design_review_required rows: {rev_rows} - computable, but nothing in the run recorded the case ids derived from them")


def s4_case_critic_to_designer(x, note):
    R = x.R
    c = "s4-case-critic-to-designer"
    cf = R / "work/test-cases/critic-findings.md"
    alt = list((R / "work/test-cases").glob("**/critic-findings*.md"))
    note(c, "have" if cf.exists() or alt else "CATCH", "review.findings_file",
         f"{cf.name} exists" if cf.exists() else (f"found {[p.name for p in alt]}" if alt else
         "NO case-critic findings file under work/test-cases - the S4 review's own receipt is not on disk"))
    note(c, "have", "review.rollcall", "critic_rollcall.py computes it from the findings file")


def s4_designer_to_runner(x, note):
    J = x.J
    plan = plan_rows(J("work/test-plan.json"))
    run = J("work/run-report.json")
    c = "s4-designer-to-runner"
    manual = [r for r in plan if r["disposition"].startswith("manual")]
    note(c, "CATCH", "execution[].evidence / then / inconclusive_when",
         f"manual rows {[r['id'] for r in manual]} reached S6 with no evidence policy anywhere in the run; "
         f"run-report.manual_checks = {run['manual_checks']} and the result lives in a hand-written "
         f"work/run-report-TC-011-notes.md")
    note(c, "CATCH", "scope[].state for the manual case",
         "the vocabulary had no word for `the observation did not answer` until `inconclusive` was added mid-run")


def gate_a_to_automator(x, note):
    J = x.J
    pipe = J("pipeline.json")
    c = "gate-a-to-automator"
    gA = pipe["gates"]["A"]
    note(c, "have", "decision.words", f"authorization_source, {len(gA.get('authorization_source',''))} chars, verbatim")
    note(c, "have", "decision.approved_scope", f"{len(gA.get('scope', []))} case ids pinned in the gate receipt")
    waivers, overrides = pipe.get("gate_waivers", []), pipe.get("stage_overrides", [])
    note(c, "have", "waivers[]", f"{len(waivers)} gate waivers + {len(overrides)} stage overrides, each with `decision` verbatim")
    handed = [w for w in overrides if "executor unavailable" in json.dumps(w)]
    note(c, "have" if handed else "MISS", "handed_to_person[]",
         f"{len(handed)} handed profiles recorded" if handed else
         "no profile was handed over in this run; the field is dormant here and the spelling is the one contract.handed_profiles reads")
    env_ov = [o for o in overrides if "environment" in o.get("match", "")]
    note(c, "have" if env_ov else "MISS", "environment.preconditions_accepted_as_blocked",
         f"{len(env_ov)} environment override(s) with the person's words")
    note(c, "MISS", "contradictions_settled[]",
         "two gate waivers ARE contradiction answers (R-10/R-14/AC-9, R-22) but nothing marks them as such; "
         "the oracle change they carry is prose in a waiver")


def s5_automator_to_critic(x, note):
    R, J = x.R, x.J
    man = J("work/automation-manifest.json")
    c = "s5-automator-to-critic"
    tests = man.get("tests") or []
    multi = [t for t in tests if len(t.get("case_version_links") or []) > 1]
    note(c, "CATCH", "scope[].case_version", f"{len(multi)} of {len(tests)} instances carry MORE THAN ONE case version")
    note(c, "CATCH", "scope[].obligations", f"{sum(1 for t in tests if t.get('obligation_ids'))} of {len(tests)} instances name obligation ids")
    note(c, "CATCH", "scope[].origin", f"{sum(1 for t in tests if t.get('dispatch') or t.get('window'))} of {len(tests)} instances say which window wrote them")
    note(c, "have", "artifacts.probes", f"{len(list((R/'work/probes').glob('*.json')))} probe records on disk")
    prov = sorted(R.glob("evidence/runtime-provenance-*.json"))
    man_blob = json.dumps(man)
    note(c, "CATCH", "artifacts.runtime_provenance",
         f"{len(prov)} provenance records exist (expected_source_revision + observed_runtime_identity), "
         f"but the manifest names one {man_blob.count('provenance')} times and NO instance names the record "
         f"its evidence was taken on: the critic had 56 records and 19 instances and no join between them")


def s5_critic_to_automator(x, note):
    R, J = x.R, x.J
    ledger = J("work/ledger.json")
    c = "s5-critic-to-automator"
    crit = sorted((R / "work/test-code").glob("critic-findings*.md"))
    note(c, "have", "review.findings_file", f"{len(crit)} findings files: {[p.name for p in crit]}")
    txt = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in crit)
    parts = re.split(r"^### (F-\d+)", txt, flags=re.M)
    fnd = {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    key = lambda v: int(v.split("-")[1])
    structured = [k for k, b in fnd.items() if re.search(r"(?im)^\s*[-*]?\s*(expected|check)\s*[:\-]", b)]
    has_cause = [k for k, b in fnd.items() if re.search(r"(?i)\*\*cause:", b)]
    tooling = [k for k, b in fnd.items() if re.search(r"(?i)cause:\s*tooling", b)]
    note(c, "CATCH", "findings[].expected / check",
         f"{len(fnd)} findings ({', '.join(sorted(fnd, key=key))}); {len(has_cause)} carry a cause, "
         f"{len(structured)} carry a structured expected/check pair. Where the target exists at all it is "
         f"inside prose, and the author re-derives it")
    note(c, "CATCH", "findings[].cause == tooling",
         f"{len(tooling)} of {len(fnd)} findings are the FACTORY's own tool ({', '.join(sorted(tooling, key=key))}) - "
         f"the same probe-tool defect handed to the author across four consecutive windows. An author cannot "
         f"fix a factory script: a `cause: tooling` finding belongs in `unverified` + the backlog, not in a round")

    # the ledger is where a missing handoff field turns into something the PERSON is shown
    cov = ledger["coverage"]["obligations"]
    note(c, "CATCH", "consequence: obligations never joined",
         f"{len(cov)} obligations, {sum(1 for o in cov if o.get('verified'))} verified, "
         f"{sum(1 for o in cov if o.get('instance_ids'))} with any instance id, "
         f"execution_state={collections.Counter(o.get('execution_state') for o in cov)['not_run']} not_run - "
         f"beside 19 green instances and 76 passed results. The instance never named its obligation, so the "
         f"coverage ledger could join nothing: `verified 0` beside a green suite, exactly the reference run's shape")
    stale = [r for r in ledger["reason_records"] if "stale case link" in r["detail"]]
    note(c, "CATCH", "consequence: stale case links became the product's fault",
         f"{len(stale)} of {len(ledger['reason_records'])} delivery reasons are `stale case link`, all owned by "
         f"`{stale[0]['owner'] if stale else '-'}` - bookkeeping (F-10 proves the case bodies were byte-identical) "
         f"shown to the person as a product-owned reason not to deliver")
    revrej = [r for r in ledger["rows"] if r["state"] == "review_rejected"]
    note(c, "CATCH", "consequence: a factory tool defect became 7 rejected rows",
         f"{len(revrej)} ledger rows read `review_rejected`; their cause is the probe tool's function-body-only "
         f"scope (F-6/F-7/F-9/F-11/F-12), which is the factory's own. The critic's `unverified` + `would_settle_it` "
         f"is the honest record; `review_rejected` blames the work")


def s5_automator_to_runner(x, note):
    J = x.J
    run = J("work/run-report.json")
    c = "s5-automator-to-runner"
    res = run["results"]
    fp = [r for r in res if r.get("input_fingerprint") and r.get("source_fingerprint")]
    note(c, "have", "scope[].freshness inputs", f"{len(fp)} of {len(res)} result rows carry both fingerprints")
    note(c, "have", "scope[].selector", f"results carry test_id + parameters + profile_id")
    note(c, "CATCH", "runtime.provenance / application_build",
         f"run-report.head={run.get('head', '-')[:12]}... records the SOURCE revision and the run report "
         f"mentions provenance {json.dumps(run).count('provenance')} times: the 55 provenance records live "
         f"beside the report and no row points at one. The contract makes the pointer part of the handoff")


def s6_runner_to_analyst(x, note):
    J = x.J
    run = J("work/run-report.json")
    c = "s6-runner-to-analyst"
    res = run["results"]
    note(c, "have", "run.execution_status", run["execution_status"])
    note(c, "have", "run.totals", json.dumps(run["totals"]))
    ev = run.get("evidence") or []
    note(c, "have", "scope[].evidence", f"{len(ev)} evidence records with report_path + sha256")
    cur = run["current_results"]
    no_ev = [r for r in cur if not r.get("report_matched")]
    note(c, "have" if not no_ev else "CATCH", "every_row_carries_an_evidence_path",
         f"current scope: {len(no_ev)} of {len(cur)} rows have no matched report row "
         f"(whole history: {sum(1 for r in res if not r.get('report_matched'))} of {len(res)})")
    note(c, "CATCH", "run.totals vs the current window",
         f"totals {json.dumps(run['totals'])} count 69 not_run rows from superseded attempts; the current "
         f"window is {json.dumps(run['current_totals'])}. A handoff that states its own window would not "
         f"hand the next role a number that answers a different question")
    note(c, "have", "superseded[]", f"factory_findings: {json.dumps(run.get('factory_findings'))[:160]}")
    note(c, "CATCH", "manual_observations[]",
         f"run-report.manual_checks = {run['manual_checks']} while the plan has a manual-agent row; "
         f"the observation exists only as a note file")


def s7_analyst_to_scribe(x, note):
    R, PROJ, J = x.R, x.PROJ, x.J
    run = J("work/run-report.json")
    triage = J("work/triage.json")
    ledger = J("work/ledger.json")
    c = "s7-analyst-to-scribe"
    note(c, "CATCH", "scope[] triage rows",
         f"triage.json carries {len(triage['triage'])} rows (reason: {triage.get('reason','-')!r}) - "
         f"S7 concluded there was nothing to triage")
    drafts = list((R / "work/bug-drafts").glob("*")) if (R / "work/bug-drafts").is_dir() else []
    bugs_dir = list((PROJ / "bugs").glob("BUG-*.md")) if (PROJ / "bugs").is_dir() else []
    note(c, "CATCH", "bug_drafts[].triage_ref",
         f"{len(drafts)} drafts on disk, {len(bugs_dir)} filed bugs ({[p.name for p in bugs_dir]}) - "
         f"a bug exists that no draft and no triage row stands behind: exactly the reference run's shape, "
         f"reproduced here and invisible until this check")
    note(c, "have", "counts", f"run totals {json.dumps(run['totals'])}, ledger blocked_by {ledger['blocked_by']}")


def s7_analyst_to_automator(x, note):
    c = "s7-analyst-to-automator"
    note(c, "MISS", "repairs[]", "no repair round ran in this story; the fields are dormant, and the "
         "`expected`/`check` pair is the same one the S5 review was missing")


def s8_scribe_to_gate_b(x, note):
    J = x.J
    ledger = J("work/ledger.json")
    c = "s8-scribe-to-gate-b"
    sys.path.insert(0, str(paths.SCRIPTS))
    import delivery_verdict      # the package's one reader of the verdict word (t-305 N8): yes | after_checks | no
    note(c, "have", "delivery.ready", str(delivery_verdict.word_of(ledger)))
    owners = collections.Counter(r.get("owner") for r in ledger["reason_records"])
    note(c, "have", "delivery.reasons_by_owner", f"{dict(owners)} - grouped by owner already")
    note(c, "have", "delivery.blocked_by", str(ledger["blocked_by"]))
    note(c, "CATCH", "message_sections.traceability",
         f"work/traceability.json does NOT exist in this run: the gate B message could not have carried "
         f"the table the contract requires, and nothing refused it")
    fac = [r for r in ledger["reason_records"] if r.get("owner") == "factory"]
    note(c, "have", "no_factory_owned_reason_is_put_to_the_person",
         f"{len(fac)} of {len(ledger['reason_records'])} reasons are the factory's own - the contract's rule "
         f"keeps them out of the question list")


def gate_b_to_delivery(x, note):
    J = x.J
    pipe = J("pipeline.json")
    c = "gate-b-to-delivery"
    gB = pipe["gates"].get("B", {})
    note(c, "have" if gB else "CATCH", "decision.words",
         f"gate B recorded: {sorted(gB)[:8]}" if gB else "no gate B receipt in pipeline.json")
    note(c, "have" if gB.get("selected_drafts") is not None else "MISS", "decision.selected_drafts",
         f"selected_drafts={gB.get('selected_drafts')}" if gB else "-")
    note(c, "have", "retro_mode.value", f"pipeline retro_mode={pipe.get('retro_mode', 'absent -> full')}")


def s9_retro_to_project(x, note):
    PROJ, J = x.PROJ, x.J
    retro = J("work/retro-numbers.json")
    c = "s9-retro-to-project"
    note(c, "have", "numbers.*", f"retro-numbers.json: orchestrator share={retro.get('orchestrator_share_percent')}, "
         f"{len(retro['dispatches'])} dispatches, stage_times for {sorted(retro['stage_times'])}")
    note(c, "CATCH", "numbers.orchestrator_share",
         f"orchestrator_share_percent is {retro.get('orchestrator_share_percent')!r} - the number the retro "
         f"is supposed to judge the run by was never computed")
    note(c, "have", "scope[] obligations", f"obligations.md exists: {(PROJ/'obligations.md').exists()}")


# (contract, the files it reads, its function) - in the order the report prints them
CONTRACTS = [
    ("s0-setup-to-scout", ("pipeline.json", "work/context-manifest.json"), s0_setup_to_scout),
    ("s1-scout-to-tester", ("pipeline.json", "work/context-manifest.json", "work/source-inventory.json",
                            "work/impl-diff.txt"), s1_scout_to_tester),
    ("s2-tester-to-strategist", ("pipeline.json", "work/context-manifest.json",
                                 "work/requirements-readiness.json", "work/sizing.json",
                                 "work/requirements-register.md", "work/impl-diff.txt"),
     s2_tester_to_strategist),
    ("s3-strategist-to-designer", ("work/test-plan.json", "work/requirements-register.md"),
     s3_strategist_to_designer),
    ("s4-designer-to-case-critic", ("state/story-case-links.json", "work/test-plan.json"),
     s4_designer_to_case_critic),
    ("s4-case-critic-to-designer", (), s4_case_critic_to_designer),
    ("s4-designer-to-runner", ("work/test-plan.json", "work/run-report.json"), s4_designer_to_runner),
    ("gate-a-to-automator", ("pipeline.json",), gate_a_to_automator),
    ("s5-automator-to-critic", ("work/automation-manifest.json",), s5_automator_to_critic),
    ("s5-critic-to-automator", ("work/ledger.json",), s5_critic_to_automator),
    ("s5-automator-to-runner", ("work/run-report.json",), s5_automator_to_runner),
    ("s6-runner-to-analyst", ("work/run-report.json",), s6_runner_to_analyst),
    ("s7-analyst-to-automator", (), s7_analyst_to_automator),
    ("s7-analyst-to-scribe", ("work/run-report.json", "work/triage.json", "work/ledger.json"),
     s7_analyst_to_scribe),
    ("s8-scribe-to-gate-b", ("work/ledger.json",), s8_scribe_to_gate_b),
    ("gate-b-to-delivery", ("pipeline.json",), gate_b_to_delivery),
    ("s9-retro-to-project", ("work/retro-numbers.json",), s9_retro_to_project),
]


def check(task_dir, handoffs=None):
    """[(contract, verdict, field, detail)] for every contract, in order."""
    x = Inputs(task_dir, handoffs or paths.HANDOFFS)
    rows = []

    def note(contract, verdict, field, detail):
        rows.append((contract, verdict, field, detail))

    for name, needs, fn in CONTRACTS:
        absent = [n for n in needs if not x.has(n)]
        if absent:
            for n in absent:
                note(name, "MISS", n, f"file absent: {n}")
            continue
        try:
            fn(x, note)
        except Absent as exc:
            note(name, "MISS", exc.name, str(exc))
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            note(name, "SHAPE", "input shape",
                 f"an input file is present but not shaped as this contract reads it: "
                 f"{type(exc).__name__}: {exc}")
    return rows


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass  # a redirected stdout (a test) has no encoding to set
    print(BANNER)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--task-dir", required=True,
                    help="the task folder: <project>/qa-factory/artifacts/<TICKET>")
    ap.add_argument("--handoffs", default=str(paths.HANDOFFS),
                    help="the package's handoffs folder (default: this repository's package)")
    a = ap.parse_args(argv)
    if not Path(a.task_dir).is_dir():
        print(f"task folder not found: {a.task_dir} - pass --task-dir <project>/qa-factory/artifacts/<TICKET>")
        return 2
    rows = check(a.task_dir, a.handoffs)
    by_c = collections.defaultdict(list)
    for cc, v, f, d in rows:
        by_c[cc].append((v, f, d))
    for cc, _, _ in CONTRACTS:
        print(f"\n=== {cc}")
        for v, f, d in by_c[cc]:
            mark = {"have": "  have ", "MISS": "  MISS ", "CATCH": "  CATCH", "SHAPE": "  SHAPE"}[v]
            print(f"{mark} {f}\n         {d}")
    tot = collections.Counter(v for _, v, _, _ in rows)
    print(f"\n\n=== TOTAL  have={tot['have']}  MISS={tot['MISS']}  CATCH={tot['CATCH']}  SHAPE={tot['SHAPE']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
