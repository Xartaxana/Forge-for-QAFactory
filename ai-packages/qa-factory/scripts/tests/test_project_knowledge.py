#!/usr/bin/env python3
"""t-2142 PK0-1: the project's answer registry `project_knowledge.py` (AR-13, AR-14, AR-24, AR-25, AR-28, AR-29; FR-45, FR-59).

Keys: a fact recorded during a story outlives `restore_config` (the FIRST test); an absent file reads as config only and every
reader writes nothing; the ERROR DIRECTION is toward asking - an unreadable registry, a foreign `schema_version`, `facts` not a list,
a revoked row, a row for another spelling of a stand, twins, a malformed note, a state outside the list, an `asked` row and an
unparseable `at` never read as `known`; the latest row wins; the same state again is not a new row; a `no_trace` story, a busy lock
and an unreadable registry write nothing; `record` loads, decides, numbers and writes inside the lock (two writers keep both rows);
the account CLI writes the config first through `record_stand_account` and the registry second; the words travel whole.

Mutations this file kills: `state()` reading a registry row before the config | a revoked row still covering | `Dev` meeting `dev` |
an unparseable `at` winning | a second row for the same state | a write under `no_trace` | `load` called before the lock | a reader that
writes | a placeholder row of the template read as a role.

Run: python -B scripts/tests/test_project_knowledge.py    or    python -m pytest scripts/tests/test_project_knowledge.py -q
"""
import json
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import pytest  # noqa: E402

import config_contract as CC  # noqa: E402
import event_store as ES  # noqa: E402
import hooklib  # noqa: E402
import project_decisions as PD  # noqa: E402
import project_knowledge as PK  # noqa: E402
import environment_record as ER  # noqa: E402
import report_adapt as RA  # noqa: E402
import stand_gaps as SG  # noqa: E402
import stand_identity as SI  # noqa: E402

AUDITOR = "QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD"
NON_ASCII = "".join(chr(code) for code in (0x2014, 0x20, 0x430, 0x443, 0x434, 0x438, 0x442, 0x43E, 0x440))      # a dash and a Cyrillic word, by code point
WORDS = "yes, auditor is a read-only role;\nits account is QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD " + NON_ASCII
STAND_ARGS = ["--task", "T-1", "--role", "auditor", "--user-key", "QA_AUDITOR_EMAIL", "--secret-key", "QA_AUDITOR_PASSWORD"]


OPEN_LAUNCH = {"launch": {}}      # E9: a normal story at an S0 stop; the default of `Proj(driver_state=)`


class Proj:
    """A throwaway project: `qa-factory/config.json` with the stands, one story folder `T-1`, the hook layer pointed at it."""

    def __init__(self, path: Path, monkeypatch, stands=None, pipeline=None, driver_state=OPEN_LAUNCH):
        self.root = path / "proj"
        self.stands = stands if stands is not None else [{"name": "dev", "base_url": "http://localhost:8080", "credentials_by_role": {}}]
        self.config = self.root / "qa-factory" / "config.json"
        self.config.parent.mkdir(parents=True)
        self.write_config()
        self.task = self.root / "qa-factory" / "artifacts" / "T-1"
        self.task.mkdir(parents=True)
        if pipeline is not None:
            (self.task / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        if driver_state is not None:                    # None = no file; bytes = written raw (PK2-19: the launch record is a carrier)
            (self.task / "state").mkdir()
            (self.task / "state" / "driver-state.json").write_bytes(driver_state if isinstance(driver_state, bytes)
                                                                    else json.dumps(driver_state).encode("utf-8"))
        self.words = path / "words.txt"
        self.words.write_bytes(WORDS.encode("utf-8"))                                        # bytes: no platform line-ending change
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(self.root))
        monkeypatch.setattr(hooklib, "_PROJECT_ROOT_CACHE", None, raising=False)

    def write_config(self, **extra):
        self.config.write_text(json.dumps(dict({"environment": {}, "environments": self.stands}, **extra), indent=2) + "\n", encoding="utf-8")

    def cfg(self) -> dict:
        return json.loads(self.config.read_text(encoding="utf-8"))

    def path(self) -> Path:
        return PK.record_path(self.root)

    def facts(self, rows) -> None:
        self.path().parent.mkdir(parents=True, exist_ok=True)
        self.path().write_text(json.dumps({"schema_version": 1, "facts": rows}), encoding="utf-8")

    def rows(self) -> list:
        return json.loads(self.path().read_text(encoding="utf-8"))["facts"]

    def record(self, **over):
        args = dict(key=PK.ROLES_KEY, environment="", element="auditor", state="known", scope="project", value={"sign_in": "account"},
                    words="the person said so", source="person", story="T-1", by="conductor")
        args.update(over)
        return PK.record(self.root, **args)

    def state(self, key=PK.ROLES_KEY, environment="", element="auditor") -> dict:
        return PK.state(self.root, key, environment, element)


@pytest.fixture
def proj(tmp_path, monkeypatch):
    return Proj(tmp_path, monkeypatch)


def fact(id, key, environment, element, state, at, **extra) -> dict:
    scope = "stand" if key == PK.ACCOUNTS_KEY else "project"
    return dict({"id": id, "key": key, "environment": environment, "element": element, "state": state, "scope": scope, "value": None,
                 "provenance": {"source": "person", "words": "w", "story": "S-1", "by": "conductor", "where": ""}, "at": at}, **extra)


def role_fact(id, element, state, at, **extra) -> dict:
    return fact(id, PK.ROLES_KEY, "", element, state, at, **extra)


def account_fact(id, environment, element, at, **extra) -> dict:
    return fact(id, PK.ACCOUNTS_KEY, environment, element, "known", at, **extra)


def short_lock(monkeypatch):
    """The writers' lock with a 0.2 s wait, so a busy lock is a quick test."""
    real = PK.lock
    monkeypatch.setattr(PK, "lock", lambda root: real(root, 0.2))


def hold(proj: Proj):
    """Another handle holds the writers' lock (a second handle in one process is busy)."""
    return ES.take_file_lock(proj.root / Path(PK.LOCK_REL), 0.0, record_holder=True)


def run(argv) -> int:
    return PK.main(argv)


# --- the first test: the fact outlives the story ---------------------------------------------------------------------------

def test_fact_survives_restore_config(proj):
    proj.write_config()
    CC.snapshot_config(proj.root, proj.task, True)
    proj.write_config(note_by_hand="a hand edit of the story, no recorded writer")           # reverted at the end, unlike the account
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 0
    assert proj.cfg()["environments"][0]["credentials_by_role"] == {"auditor": AUDITOR}
    result = CC.restore_config(proj.root, proj.task)
    assert result["state"] == "reverted" and result["kept"] == ["/environments"], result       # the decision receipt is a recorded writer
    assert proj.cfg()["environments"][0]["credentials_by_role"] == {"auditor": AUDITOR}
    assert "note_by_hand" not in proj.cfg()
    assert [r["key"] for r in proj.rows()] == [PK.ACCOUNTS_KEY, PK.ROLES_KEY]                 # records/ is never reverted
    got = proj.state(PK.ACCOUNTS_KEY, "dev")
    assert got["state"] == "known" and got["row"]["id"] == "PK-1" and got["source"] == "person"


# --- reading ---------------------------------------------------------------------------------------------------------------

def test_absent_file_reads_config_only(proj):
    proj.stands[0]["credentials_by_role"] = {"auditor": AUDITOR}
    proj.write_config()
    assert not proj.path().exists()
    got = proj.state(PK.ACCOUNTS_KEY, "dev")
    assert (got["state"], got["source"], got["problem"], got["row"]) == ("known", "legacy_config", "", None)
    assert proj.state()["state"] == "unknown" and proj.state()["problem"] == ""
    roster = PK.roster(proj.root, proj.cfg(), "dev")
    assert [(e["role"], e["source"], e["account"]) for e in roster["elements"]] == [("auditor", "legacy_config", True)]
    assert not proj.path().exists() and not (proj.root / Path(PK.LOCK_REL)).exists(), "a reader wrote something"


def test_first_record_creates_file(proj):
    assert not proj.path().exists()
    row, problem, created = proj.record()
    assert problem == "" and created is True and row["id"] == "PK-1"
    assert proj.rows() == [row]
    assert (row["key"], row["environment"], row["element"], row["state"], row["scope"]) == ("product.roles", "", "auditor", "known", "project")
    assert row["provenance"] == {"source": "person", "words": "the person said so", "story": "T-1", "by": "conductor", "where": ""}
    assert row["at"].endswith("+00:00") and "revoked_at" not in row


def test_unreadable_registry_refuses_write_and_reads_config(proj):
    proj.stands[0]["credentials_by_role"] = {"auditor": AUDITOR}
    proj.write_config()
    for label, text in (("not json", "{ not json"), ("facts not a list", json.dumps({"schema_version": 1, "facts": {"a": 1}})),
                        ("not an object", "[1, 2]")):
        proj.path().parent.mkdir(parents=True, exist_ok=True)
        proj.path().write_text(text, encoding="utf-8")
        held = proj.path().read_bytes()
        got = proj.state(PK.ACCOUNTS_KEY, "dev")
        assert got["state"] == "known" and got["problem"], label                             # config first, the problem said (FR-41)
        assert proj.state()["state"] == "unknown" and proj.state()["problem"], label
        row, problem, created = proj.record()
        assert row is None and created is False and "nothing was written over it" in problem and "project_knowledge.py show" in problem, label
        assert proj.path().read_bytes() == held, label


def test_foreign_schema_version_is_unknown(proj):
    proj.path().parent.mkdir(parents=True)
    proj.path().write_text(json.dumps({"schema_version": 2, "facts": [role_fact("PK-1", "auditor", "not_needed", "2026-11-01T10:00:00+00:00")]}),
                           encoding="utf-8")
    got = proj.state()
    assert got["state"] == "unknown" and "schema_version" in got["problem"]
    assert PK.roster(proj.root, proj.cfg(), "dev")["removed"] == []
    row, problem, _ = proj.record()
    assert row is None and "schema_version" in problem


def test_revoked_row_covers_nothing(proj):
    row, _, _ = proj.record(state="not_needed", value=None)
    assert proj.state()["state"] == "not_needed"
    taken, problem = PK.revoke(proj.root, row["id"], "ask again")
    assert problem == "" and taken["revoked_at"] and taken["revoked_words"] == "ask again"
    assert proj.state()["state"] == "unknown"
    assert PK.roster(proj.root, proj.cfg(), "dev")["removed"] == []
    assert PK.revoke(proj.root, row["id"], "again")[0] is None                                 # already taken back
    assert "PK-9" in PK.revoke(proj.root, "PK-9", "x")[1] and "project_knowledge.py show" in PK.revoke(proj.root, "PK-9", "x")[1]
    assert PK.revoke(proj.root, row["id"], "  ")[0] is None                                    # empty words
    # a revoked later row covers what it superseded (Q3 a): taking an answer back never brings the older one back
    proj.facts([role_fact("PK-1", "auditor", "known", "2026-11-01T10:00:00+00:00"),
                role_fact("PK-2", "auditor", "not_needed", "2026-11-02T10:00:00+00:00", revoked_at="2026-11-03T10:00:00+00:00")])
    assert proj.state()["state"] == "unknown" and proj.state()["problem"] == ""


def test_stand_name_exact(proj):
    proj.stands[0]["credentials_by_role"] = {"auditor": AUDITOR}
    proj.write_config()
    proj.facts([account_fact("PK-1", "Dev", "auditor", "2026-11-01T10:00:00+00:00"),
                account_fact("PK-2", "", "auditor", "2026-11-01T10:00:00+00:00")])           # another spelling; an empty stand: skipped
    assert proj.state(PK.ACCOUNTS_KEY, "Dev")["state"] == "unknown"                          # no stand `Dev` in the config
    assert proj.state(PK.ACCOUNTS_KEY, "")["state"] == "unknown"
    got = proj.state(PK.ACCOUNTS_KEY, "dev")
    assert got["state"] == "known" and got["row"] is None and got["source"] == "legacy_config"   # the row of `Dev` is not the row of `dev`
    assert PK.roster(proj.root, proj.cfg(), "")["elements"][0]["account"] is None            # no stand chosen: not shown, not "no"


def test_twin_roles_are_unknown_with_twins(proj):
    proj.stands[0]["credentials_by_role"] = {"Admin": "A_USER / A_PASS", "admin": "B_USER / B_PASS"}
    proj.write_config()
    got = proj.state(PK.ACCOUNTS_KEY, "dev", "ADMIN")
    assert got["state"] == "unknown" and sorted(got["twins"]) == ["Admin", "admin"]
    exact = proj.state(PK.ACCOUNTS_KEY, "dev", "admin")                                      # the exact key wins beside a twin
    assert exact["state"] == "known" and exact["twins"] == []


def test_malformed_note_is_unknown_with_flag(proj):
    proj.stands[0]["credentials_by_role"] = {"auditor": "ONLY_ONE_KEY"}
    proj.write_config()
    got = proj.state(PK.ACCOUNTS_KEY, "dev")
    assert got["state"] == "unknown" and got["malformed"] is True and got["twins"] == []
    proj.stands[0]["credentials_by_role"] = {"auditor": "NOT provisioned locally"}
    proj.write_config()
    assert proj.state(PK.ACCOUNTS_KEY, "dev")["malformed"] is True


def test_known_row_without_config_is_unknown(proj):
    proj.facts([account_fact("PK-1", "dev", "auditor", "2026-11-01T10:00:00+00:00")])
    assert proj.state(PK.ACCOUNTS_KEY, "dev")["state"] == "unknown"                          # the value carrier is gone: the row believes nothing
    proj.stands[0]["credentials_by_role"] = {"auditor": "ONLY_ONE_KEY"}                      # a note that names one key now
    proj.write_config()
    got = proj.state(PK.ACCOUNTS_KEY, "dev")
    assert got["state"] == "unknown" and got["malformed"] is True
    proj.stands[0]["credentials_by_role"] = {"Auditor": AUDITOR, "auditor": AUDITOR}         # twinned now
    proj.write_config()
    assert proj.state(PK.ACCOUNTS_KEY, "dev", "AUDITOR")["state"] == "unknown"


def test_noticed_is_never_known(proj):
    proj.record(state="noticed_unconfirmed", source="role", by="driver", words="", where="R-2: a visitor sees the catalogue")
    got = proj.state()
    assert got["state"] == "noticed_unconfirmed" and got["state"] != "known" and got["source"] == "role"
    roster = PK.roster(proj.root, proj.cfg(), "dev")
    assert [(e["role"], e["state"]) for e in roster["elements"]] == [("auditor", "noticed_unconfirmed")]
    assert proj.state(PK.ACCOUNTS_KEY, "dev")["state"] == "unknown"                          # noticing a role never makes an account
    assert proj.rows()[0]["provenance"]["where"] == "R-2: a visitor sees the catalogue"


def test_unknown_state_value_ignored(proj):
    proj.facts([role_fact("PK-1", "auditor", "maybe", "2026-11-01T10:00:00+00:00"),
                role_fact("PK-2", "guest", "unknown", "2026-11-01T10:00:00+00:00"),
                dict(role_fact("PK-3", "viewer", "known", "2026-11-01T10:00:00+00:00"), key="product.colours"),
                dict(role_fact("PK-4", "editor", "known", "2026-11-01T10:00:00+00:00"), scope="story")])
    for name in ("auditor", "guest", "viewer", "editor"):
        assert proj.state(element=name)["state"] == "unknown", name
    assert PK.roster(proj.root, proj.cfg(), "dev")["elements"] == []
    row, problem, _ = proj.record(state="maybe")
    assert row is None and "maybe" in problem


def test_asked_row_is_skipped(proj):
    proj.facts([role_fact("PK-1", "auditor", "asked", "2026-11-01T10:00:00+00:00")])         # reserved for phase 2: no producer
    assert proj.state()["state"] == "unknown"
    assert PK.roster(proj.root, proj.cfg(), "dev") == {"elements": [], "removed": [], "problem": ""}
    row, problem, _ = proj.record(state="asked")
    assert row is None and "asked" in problem
    proj.facts([role_fact("PK-1", "auditor", "not_needed", "2026-11-01T10:00:00+00:00"),
                role_fact("PK-2", "auditor", "asked", "2026-11-02T10:00:00+00:00")])
    assert proj.state()["state"] == "not_needed"                                             # an `asked` row never suppresses nor lifts


def test_unparseable_at_loses(proj):
    good = role_fact("PK-1", "auditor", "known", "2026-11-01T10:00:00+00:00")
    for bad_at in ("not a time", "", None, 7):
        bad = role_fact("PK-2", "auditor", "not_needed", bad_at)
        for rows in ([good, bad], [bad, good]):
            proj.facts(rows)
            assert proj.state()["state"] == "known", (bad_at, [r["id"] for r in rows])
    proj.facts([role_fact("PK-1", "auditor", "known", "bad"), role_fact("PK-2", "auditor", "not_needed", "worse")])
    assert proj.state()["state"] == "not_needed"                                             # both unparseable: the tie, the later row


def test_latest_row_wins(proj):
    proj.facts([role_fact("PK-2", "auditor", "not_needed", "2026-11-02T10:00:00+00:00"),
                role_fact("PK-1", "auditor", "known", "2026-11-01T10:00:00+00:00")])         # file order is not time order
    assert proj.state()["state"] == "not_needed"
    proj.facts([role_fact("PK-1", "auditor", "known", "2026-11-01T10:00:00+00:00"),
                role_fact("PK-2", "auditor", "not_needed", "2026-11-01T10:00:00+00:00")])    # a tie: the later row
    assert proj.state()["state"] == "not_needed"
    proj.facts([role_fact("PK-1", "Auditor", "known", "2026-11-03T10:00:00+00:00"),
                role_fact("PK-2", "auditor", "not_needed", "2026-11-02T10:00:00+00:00")])    # elements meet by the role form
    assert proj.state(element="AUDITOR")["state"] == "known"
    assert [e["role"] for e in PK.roster(proj.root, proj.cfg(), "dev")["elements"]] == ["Auditor"]


def test_same_state_again_not_created(proj):
    first, _, created = proj.record()
    again, problem, created_again = proj.record(element="AUDITOR", words="said again")
    assert (created, created_again, problem) == (True, False, "") and again == first and len(proj.rows()) == 1
    proj.record(state="not_needed", value=None)
    back, _, created_back = proj.record()                                                    # a changed answer is a NEW row
    assert created_back is True and back["id"] == "PK-3" and [r["state"] for r in proj.rows()] == ["known", "not_needed", "known"]


def test_changed_value_is_a_new_row(proj, capsys):
    proj.record(value={"sign_in": "account"})
    assert run(["role", "--task", "T-1", "--role", "auditor", "--state", "known", "--sign-in", "none", "--words-file", str(proj.words)]) == 0
    assert "recorded (PK-2)" in capsys.readouterr().out and len(proj.rows()) == 2
    assert proj.state()["row"]["value"] == {"sign_in": "none"}                               # the person's latest word, not "already recorded"
    assert proj.record(value={"sign_in": "none"})[2] is False                                # same state and value: still deduplicated


def test_revoke_cli_needs_a_task_and_works(proj, capsys):
    row, _, _ = proj.record()
    with pytest.raises(SystemExit):
        run(["revoke", "--id", row["id"], "--words-file", str(proj.words)])                  # --task is required
    capsys.readouterr()
    assert run(["revoke", "--task", "T-1", "--id", row["id"], "--words-file", str(proj.words)]) == 0
    assert proj.rows()[0]["revoked_at"] and proj.state()["state"] == "unknown"


def test_account_lock_that_cannot_be_made_has_its_own_sentence(proj, monkeypatch, capsys):
    broken = ES.LockBroken(proj.root / "x.lock", "open failed", "open")
    cause = TimeoutError(str(broken))
    cause.__cause__ = broken

    def refuse(root, **kwargs):
        raise cause

    monkeypatch.setattr(PD, "record_stand_account", refuse)
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 2
    err = capsys.readouterr().err
    assert "not another writer" in err and "writable file" in err and "run the same command again" not in err


def test_account_record_failure_after_config_names_the_move(proj, monkeypatch, capsys):
    monkeypatch.setattr(PK, "record", lambda *a, **k: (None, "the disk is full", False))
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 2
    err = capsys.readouterr().err
    assert proj.cfg()["environments"][0]["credentials_by_role"] == {"auditor": AUDITOR}      # the config was written first
    assert "the disk is full" in err and "run the same command again once that is fixed" in err


# --- writing ---------------------------------------------------------------------------------------------------------------

# PK2-11/19: the writers refuse through ONE reader that reads both carriers (pipeline.json, the driver's launch record).
# world -> (Proj kwargs, expected exit of a CLI writer); `none` = a story with neither file (E10, FR-59); E4 = the person's explicit way out
WORLDS = {
    "launch_yes": (dict(driver_state={"launch": {"no_trace": True}}), 2),
    "none": (dict(driver_state=None), 2),
    "launch_open": (dict(), 0),
    "pipeline_no_over_launch": (dict(pipeline={"ticket": "T-1", "no_trace": False}, driver_state={"launch": {"no_trace": True}}), 0),
}
PROFILES = [{"profile_id": "web", "commands": {"one_test": {"argv": ["pytest", "-k", "x"], "cwd": "."}}}]
OLD, FEW, TWO = tuple(WORLDS), ("launch_yes", "launch_open"), ("launch_yes", "none", "launch_open")


def _mains(main, *argv):
    return lambda p: main([a(p) if callable(a) else a for a in argv])


def _words_in(p):
    return str(p.words)


def _text(p):
    p.words.with_name("text.txt").write_text("the report lacked the names of the tests", encoding="utf-8")
    return str(p.words.with_name("text.txt"))


# writer -> (world list, run(proj) -> exit code); every one runs AFTER its story is placed and BEFORE a byte is written (PK2-11 N2)
WRITERS = {
    "side": (OLD, _mains(PK.main, "side", "--task", "T-1", "--name", "ui", "--deliverable", "no", "--words-file", _words_in)),
    "account": (OLD, _mains(PK.main, "account", *STAND_ARGS, "--words-file", _words_in)),
    "revoke": (OLD, _mains(PK.main, "revoke", "--task", "T-1", "--id", "PK-1", "--words-file", _words_in)),
    "env-record": (TWO, _mains(ER.main, "record", "--task", "T-1", "--contour", "web", "--reason", "zero_tests", "--exit-code", "0",
                               "--option", "accept", "--words-file", _words_in)),
    "ask-again-pk": (FEW, lambda p: PK.main(SG.revoke_args(True, "PK-1", "T-1")[1:] + ["--words-file", str(p.words)])),
    "ask-again-env": (FEW, lambda p: ER.main(SG.revoke_args(False, "EP-1", "T-1")[1:] + ["--words-file", str(p.words)])),
    "report-kind": (("launch_yes",), _mains(RA.main, "kind", "--task", "T-1", "--profile", "web", "--reader", "trx", "--by", "driver")),
    "report-understood": (FEW, _mains(RA.main, "understood", "--task", "T-1", "--profile", "web", "--by", "driver", "--text-file", _text)),
    "report-forget": (FEW, _mains(RA.main, "forget", "--task", "T-1", "--id", "RA-1")),
    "stand-record": (FEW, _mains(SI.main, "record", "--task", "T-1", "--environment", "dev", "--profile", "web", "--method", "person_confirms",
                                 "--words", "I check it myself")),
    "stand-forget": (FEW, _mains(SI.main, "forget", "--task", "T-1", "--environment", "dev", "--profile", "web", "--words", "not any more")),
}
CASES = [pytest.param(w, world, id=f"{w}-{world}") for w, (worlds, _run) in WRITERS.items() for world in worlds]


def _bytes(proj: Proj) -> dict:
    return {p: p.read_bytes() for p in [proj.config, *sorted((proj.root / "qa-factory" / "records").glob("*"))]}


def _held(proj: Proj) -> None:
    """The rows `revoke` / `forget` take back, and the profile of the config the report and stand writers need."""
    proj.write_config(profiles=PROFILES)
    proj.facts([role_fact("PK-1", "auditor", "known", "2026-11-12T09:40:00+00:00")])
    ER.write_rows(ER.record_path(proj.root), "properties", 1, [{"id": "EP-1", "option": "accept"}])
    RA.append(proj.root, {"kind": "not_adapted", "by": "driver", "profile_id": "web", "argv_digest": "d", "understood": "x"})


@pytest.mark.parametrize("writer, world", CASES)
def test_writers_under_trace(writer, world, tmp_path, monkeypatch, capsys):
    kwargs, want = WORLDS[world]
    proj = Proj(tmp_path, monkeypatch, **kwargs)
    _held(proj)
    before = _bytes(proj)
    capsys.readouterr()
    code = WRITERS[writer][1](proj)
    err = capsys.readouterr().err
    assert code == want, err
    assert (_bytes(proj) == before) == bool(want)                      # refused: nothing written anywhere
    if want:
        assert ("could not be established" in err) == (world == "none") and ("(waiver)" in err) == (world == "launch_yes")
    elif writer.startswith("ask-again"):
        assert "revoked_at" in (proj.path() if writer.endswith("pk") else ER.record_path(proj.root)).read_text(encoding="utf-8")


def test_writers_under_trace_in_process_and_without_a_story(tmp_path, monkeypatch):
    """The in-process writers refuse on a closed story with their own shape and write for no story (E1); an unknown --task writes nothing (E2)."""
    proj = Proj(tmp_path, monkeypatch, driver_state={"launch": {"no_trace": True}})
    _held(proj)
    key = {"scope": "level", "contour": "web", "argv_digest": "d", "reason_class": "zero_tests"}
    row = {"kind": "not_adapted", "by": "driver", "profile_id": "web", "argv_digest": "d", "understood": "x"}
    say, before = [], _bytes(proj)
    SG.record_lasting(proj.root, {"gap": {"property_key": key, "contour": "web"}, "line": "w"}, "T-1", say.append, task_root=proj.task)
    assert RA.append(proj.root, row, task_root=proj.task)[1] == PK.NO_TRACE_WORDS
    with pytest.raises(SI.RegistryError, match="waiver"):
        SI.append_row(proj.root, SI.make_row(proj.cfg(), "dev", "web", "person_confirms", words="w"), task_root=proj.task)
    assert "the environment record is not (an experiment leaves no trace" in say[0] and _bytes(proj) == before
    assert SI.main(["forget", "--task", "nope", "--environment", "dev", "--profile", "web", "--words", "w"]) == 2
    assert ER.main(["revoke", "--task", "nope", "--id", "EP-1", "--words-file", str(proj.words)]) == 2
    assert RA.append(proj.root, row)[0] is not None and _bytes(proj) != before          # F1: no story named, written


def test_driver_dry_mode_launch_in_memory(tmp_path, monkeypatch):
    """Dry mode: no files on disk (not even the story folder), only the driver's in-memory launch record (PK2-19 round 2, sides keep)."""
    proj = Proj(tmp_path, monkeypatch, driver_state=None)
    ghost = proj.root / "qa-factory" / "artifacts" / "T-dry"
    assert proj.record(task_root=ghost, launch={}, by="driver")[0] is not None                        # no no_trace: the row is written
    row, problem, _ = proj.record(task_root=ghost, launch={"no_trace": True}, by="driver", element="other")
    assert row is None and "(waiver)" in problem                                                  # no_trace in memory: closed
    assert "could not be established" in proj.record(task_root=ghost, element="third")[1]       # no launch given: unknown, refused


def test_no_trace_refused(tmp_path, monkeypatch):
    proj = Proj(tmp_path, monkeypatch, pipeline={"ticket": "T-1", "no_trace": True})
    row, problem, created = proj.record(task_root=proj.task)
    assert row is None and created is False and "an experiment leaves no trace" in problem and "waiver" in problem
    assert not proj.path().exists()
    assert PK._refuse_no_trace(None) == "" and PK._refuse_no_trace(proj.task) != ""
    before = proj.config.read_bytes()
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 2
    assert run(["role", "--task", "T-1", "--role", "auditor", "--state", "not_needed", "--words-file", str(proj.words)]) == 2
    assert proj.config.read_bytes() == before and not proj.path().exists()                    # nothing recorded anywhere
    proj.task.joinpath("pipeline.json").write_text(json.dumps({"ticket": "T-1"}), encoding="utf-8")
    row, _, _ = proj.record()                                                                # a carried row, then the story becomes an experiment
    proj.task.joinpath("pipeline.json").write_text(json.dumps({"ticket": "T-1", "no_trace": True}), encoding="utf-8")
    held = proj.path().read_bytes()
    assert run(["revoke", "--task", "T-1", "--id", row["id"], "--words-file", str(proj.words)]) == 2
    assert proj.path().read_bytes() == held                                                  # a revoke is a trace too (P8)
    proj.task.joinpath("pipeline.json").write_text(json.dumps({"ticket": "T-1", "no_trace": False}), encoding="utf-8")
    assert proj.record(task_root=proj.task, element="other")[2] is True                      # the way out: the story is no experiment


def test_lock_busy_refused(proj, monkeypatch, capsys):
    short_lock(monkeypatch)
    holder = hold(proj)
    try:
        with pytest.raises(TimeoutError) as raised:
            proj.record()
        assert "busy" in str(raised.value) and "run the same command again" in str(raised.value)
        assert not proj.path().exists()
        assert run(["role", "--task", "T-1", "--role", "auditor", "--state", "known", "--words-file", str(proj.words)]) == 2
        assert "busy" in capsys.readouterr().err and not proj.path().exists()
    finally:
        holder.release()
    assert proj.record()[2] is True                                                          # free again: the same command works


def test_record_loads_inside_the_lock(proj, monkeypatch):
    real_load, seen = PK.load, []

    def watched(root):
        try:
            ES.take_file_lock(Path(root) / Path(PK.LOCK_REL), 0.0).release()
            seen.append("free")
        except ES.LockBusy:
            seen.append("held")
        return real_load(root)

    monkeypatch.setattr(PK, "load", watched)
    proj.record()
    assert seen == ["held"], "record read the registry outside its lock"
    monkeypatch.setattr(PK, "load", real_load)
    roles = [f"role{i}" for i in range(6)]
    errors = []

    def one(role):
        try:
            assert proj.record(element=role)[2] is True
        except Exception as exc:        # noqa: BLE001 - a thread reports into the list
            errors.append(repr(exc))

    threads = [threading.Thread(target=one, args=(r,)) for r in roles]
    for t in threads:
        t.start()
    for t in threads:
        t.join(60)
    assert errors == []
    rows = proj.rows()
    assert sorted(r["element"] for r in rows) == sorted(["auditor", *roles])               # two racing writers keep both rows
    assert len({r["id"] for r in rows}) == len(rows)


def test_revoke_holds_the_lock(proj, monkeypatch):
    row, _, _ = proj.record()
    held = proj.path().read_bytes()
    short_lock(monkeypatch)
    holder = hold(proj)
    try:
        with pytest.raises(TimeoutError):
            PK.revoke(proj.root, row["id"], "ask again")
        assert proj.path().read_bytes() == held
    finally:
        holder.release()
    assert PK.revoke(proj.root, row["id"], "ask again")[1] == ""


# --- the account command ---------------------------------------------------------------------------------------------------

def test_account_cli_config_then_registry(proj, monkeypatch, capsys):
    calls = []
    real = PD.record_stand_account

    def spy(root, **kwargs):
        calls.append({"registry_before": proj.path().exists(), "config_before": proj.cfg()["environments"][0]["credentials_by_role"]})
        result = real(root, **kwargs)
        calls[-1].update(registry_after_writer=proj.path().exists(), config_after=proj.cfg()["environments"][0]["credentials_by_role"])
        return result

    monkeypatch.setattr(PD, "record_stand_account", spy)
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 0
    assert len(calls) == 1 and calls[0]["config_before"] == {} and calls[0]["registry_before"] is False
    assert calls[0]["config_after"] == {"auditor": AUDITOR} and calls[0]["registry_after_writer"] is False   # config first, registry second
    assert capsys.readouterr().out.startswith("auditor on dev: recorded (DD-1, PK-1)")
    assert proj.rows()[0]["key"] == PK.ACCOUNTS_KEY and proj.rows()[0]["value"] is None       # the value stays in config (FK-1)
    source = Path(PK.__file__).read_text(encoding="utf-8")
    assert "config.json\", \"w" not in source and "write_text" not in source and "credentials_by_role\"] =" not in source
    # a refusal of the config writer leaves the registry untouched
    assert run(["account", *STAND_ARGS[:-1], "QA_AUDITOR_EMAIL", "--words-file", str(proj.words)]) == 2     # the same name twice
    assert len(proj.rows()) == 2 and "refused" in capsys.readouterr().err


def test_account_cli_element_is_real_key(proj):
    proj.stands[0]["credentials_by_role"] = {"auditor": AUDITOR}
    proj.write_config()
    args = ["account", "--task", "T-1", "--role", "Auditor", "--user-key", "QA_AUDITOR_EMAIL", "--secret-key", "QA_AUDITOR_PASSWORD",
            "--words-file", str(proj.words)]
    assert run(args) == 0
    account = [r for r in proj.rows() if r["key"] == PK.ACCOUNTS_KEY]
    assert [r["element"] for r in account] == ["auditor"]                                    # the key the readers read, not the spelling given
    assert proj.state(PK.ACCOUNTS_KEY, "dev", "Auditor")["row"]["id"] == account[0]["id"]


def test_account_cli_unchanged_prints_already_recorded(proj, capsys):
    argv = ["account", *STAND_ARGS, "--words-file", str(proj.words)]
    assert run(argv) == 0
    capsys.readouterr()
    assert run(argv) == 0
    assert capsys.readouterr().out.strip() == "auditor on dev: already recorded (PK-1)"
    assert len(proj.rows()) == 2 and len(list((proj.root / "qa-factory" / "state" / "decision-transactions").glob("DD-*.json"))) == 1


def test_account_cli_no_stand_refused(tmp_path, monkeypatch, capsys):
    stands = [{"name": "dev", "base_url": "http://a", "credentials_by_role": {}}, {"name": "stage", "base_url": "http://b", "credentials_by_role": {}}]
    proj = Proj(tmp_path, monkeypatch, stands=stands, pipeline={"ticket": "T-1"})
    before = proj.config.read_bytes()
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 2
    err = capsys.readouterr().err
    assert "no chosen stand" in err and "`dev`" in err and "`stage`" in err
    assert proj.config.read_bytes() == before and not proj.path().exists()
    # no `environments[]` row at all: the account writer's own refusal is printed whole
    bare = Proj(tmp_path / "bare", monkeypatch, stands=[])
    assert run(["account", *STAND_ARGS, "--words-file", str(bare.words)]) == 2
    assert "environments[]" in capsys.readouterr().err and not bare.path().exists()


def test_account_cli_adds_roster_element(proj):
    assert PK.roster(proj.root, proj.cfg(), "dev")["elements"] == []
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 0
    assert proj.state()["state"] == "known"
    roster = PK.roster(proj.root, proj.cfg(), "dev")
    assert [(e["role"], e["state"], e["source"], e["sign_in"], e["account"]) for e in roster["elements"]] == \
        [("auditor", "known", "person", "account", True)]
    proj.facts([role_fact("PK-1", "auditor", "noticed_unconfirmed", "2026-11-01T10:00:00+00:00")])
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 0
    assert proj.state()["state"] == "known"                                                  # an account confirms a noticed role


def test_role_cli_not_needed_removes_from_roster(proj, capsys):
    proj.record(element="superuser", state="known")
    assert [e["role"] for e in PK.roster(proj.root, proj.cfg(), "dev")["elements"]] == ["superuser"]
    assert run(["role", "--task", "T-1", "--role", "superuser", "--state", "not_needed", "--words-file", str(proj.words)]) == 0
    assert "superuser: not_needed recorded (PK-2)" in capsys.readouterr().out
    roster = PK.roster(proj.root, proj.cfg(), "dev")
    assert roster["elements"] == [] and [(r["role"], r["story"], r["id"]) for r in roster["removed"]] == [("superuser", "T-1", "PK-2")]
    assert proj.rows()[1]["value"] is None and proj.rows()[1]["provenance"]["words"] == WORDS
    assert run(["role", "--task", "T-1", "--role", "superuser", "--state", "known", "--words-file", str(proj.words)]) == 0     # taken back by a word
    assert PK.roster(proj.root, proj.cfg(), "dev")["removed"] == []


def test_not_needed_with_config_account_out_of_roster_account_known(proj):
    proj.stands[0]["credentials_by_role"] = {"superuser": "SU_USER / SU_PASS", "admin": "AD_USER / AD_PASS"}
    proj.write_config()
    proj.record(element="superuser", state="not_needed", value=None)
    roster = PK.roster(proj.root, proj.cfg(), "dev")
    assert [e["role"] for e in roster["elements"]] == ["admin"] and [r["role"] for r in roster["removed"]] == ["superuser"]
    assert proj.state(PK.ACCOUNTS_KEY, "dev", "superuser")["state"] == "known"               # config first: could the factory sign in
    assert proj.state(element="superuser")["state"] == "not_needed"                          # is it a product role
    assert proj.state(element="SuperUser")["state"] == "not_needed"
    assert proj.state(element="Super_User")["state"] == "unknown"                            # another form (a separator is a space, not nothing)
    assert proj.state(element="superusers")["state"] == "unknown"                            # merely resembling is not equal


def test_unsafe_role_name_refused(proj, capsys):
    for name in ("a,b", "a|b", "a\\b", "a\nb", "a\x00b", "", "   ", "default", "env:X", "created:y", "_ -",
                 "a b", "a b", "a\x85b", "a\x80b", "a\x9fb"):
        row, problem, created = proj.record(element=name)
        assert row is None and created is False and "nothing was recorded" in problem, repr(name)
    assert not proj.path().exists()
    assert run(["role", "--task", "T-1", "--role", "a,b", "--state", "known", "--words-file", str(proj.words)]) == 2
    assert "comma" in capsys.readouterr().err and not proj.path().exists()


def test_key_outside_keys_refused(proj):
    for key in ("product.colours", "", "environments.base_url", "PRODUCT.ROLES"):
        row, problem, _ = proj.record(key=key)
        assert row is None and "not a project-knowledge key" in problem and PK.ROLES_KEY in problem, key
    row, problem, _ = proj.record(key=PK.ACCOUNTS_KEY, environment="")                         # a fact of a stand with no stand
    assert row is None and "no stand is named" in problem
    row, problem, _ = proj.record(scope="story")                                             # a story answer is a waiver, not a row
    assert row is None and "waiver" in problem
    row, problem, _ = proj.record(key=PK.ACCOUNTS_KEY, environment="dev", scope="stand", state="not_needed")      # per-stand not_needed is not phase 0
    assert row is None and "`known` only" in problem
    assert not proj.path().exists()


def test_words_whole_and_door(proj, capsys):
    row, _, _ = proj.record(words=f"  {WORDS}  ")
    assert row["provenance"]["words"] == WORDS                                               # whole: line break, dash, Cyrillic - nothing cut
    assert proj.rows()[0]["provenance"]["words"] == WORDS
    empty, problem, _ = proj.record(element="x", words="  \n ")
    assert empty is None and "--words-file" in problem
    assert proj.record(element="x", words="", source="role", by="driver")[2] is True        # a role's inference carries no person's words
    assert run(["role", "--task", "T-1", "--role", "y", "--state", "known"]) == 2
    assert "--words-file" in capsys.readouterr().err and len(proj.rows()) == 2
    proj.words.write_text("   \n", encoding="utf-8")
    assert run(["role", "--task", "T-1", "--role", "y", "--state", "known", "--words-file", str(proj.words)]) == 2
    assert "--words-file" in capsys.readouterr().err and len(proj.rows()) == 2
    assert run(["show", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["facts"][0]["provenance"]["words"] == WORDS


# --- the roster ------------------------------------------------------------------------------------------------------------

def test_roster_legacy_accounts_dedup_by_form(tmp_path, monkeypatch):
    stands = [{"name": "dev", "base_url": "http://a", "credentials_by_role": {"Admin": "A_USER / A_PASS", "reader": "R_USER / R_PASS"}},
              {"name": "stage", "base_url": "http://b", "credentials_by_role": {"admin": "B_USER / B_PASS"}}]
    proj = Proj(tmp_path, monkeypatch, stands=stands)
    first = PK.roster(proj.root, proj.cfg(), "dev")
    assert [(e["role"], e["source"]) for e in first["elements"]] == [("Admin", "legacy_config"), ("reader", "legacy_config")]
    assert {e["role"]: e["account"] for e in first["elements"]} == {"Admin": True, "reader": True}
    assert {e["role"]: e["account"] for e in PK.roster(proj.root, proj.cfg(), "stage")["elements"]} == {"Admin": True, "reader": False}
    proj.record(element="ADMIN", words="the person confirmed admin")
    again = PK.roster(proj.root, proj.cfg(), "dev")
    assert [(e["role"], e["source"], e["story"]) for e in again["elements"]] == [("ADMIN", "person", "T-1"), ("reader", "legacy_config", "")]
    assert again["elements"][0]["account"] is True                                           # the account is read by the role form too


def test_reserved_roles_never_in_roster(tmp_path, monkeypatch):
    stands = [{"name": "dev", "base_url": "http://a", "credentials_by_role": {
        "default": "D_USER / D_PASS", "env:X_USER/X_PASS": "-", "created:walker": "-", "auditor": AUDITOR, "": "E_USER / E_PASS"}}]
    proj = Proj(tmp_path, monkeypatch, stands=stands)
    assert [e["role"] for e in PK.roster(proj.root, proj.cfg(), "dev")["elements"]] == ["auditor"]
    proj.facts([role_fact("PK-1", "default", "known", "2026-11-01T10:00:00+00:00")])         # a hand-written row of a reserved form
    assert [e["role"] for e in PK.roster(proj.root, proj.cfg(), "dev")["elements"]] == ["auditor"]
    assert proj.record(element="default")[0] is None


# --- the S3 form -----------------------------------------------------------------------------------------------------------

def strategist_form(proj: Proj, body: str, *, accepted=True) -> None:
    (proj.task / "state").mkdir(parents=True, exist_ok=True)
    (proj.task / "work" / "handoffs").mkdir(parents=True, exist_ok=True)
    dispatches = {"d1": {"id": "d1", "stage": "S3", "role": "qa-test-strategist", "status": "accepted" if accepted else "running"}}
    (proj.task / "state" / "controller.json").write_text(json.dumps({"dispatches": dispatches}), encoding="utf-8")
    (proj.task / "work" / "handoffs" / "d1.yaml").write_text(body, encoding="utf-8")


def test_story_roles_absent_empty_and_rows(proj):
    assert PK.story_roles(proj.task) == ([], "")                                             # no form at all
    strategist_form(proj, "scope:\n  - id: R-1\nblocked: none\n", accepted=False)
    assert PK.story_roles(proj.task) == ([], "")                                             # a form not accepted yet is no form
    strategist_form(proj, "scope:\n  - id: R-1\nblocked: none\n")
    assert PK.story_roles(proj.task) == ([], "")                                             # an old form: no section
    strategist_form(proj, "scope:\n  - id: R-1\nproduct_roles: []\nblocked: none\n")
    assert PK.story_roles(proj.task) == ([], "")                                             # an empty list
    strategist_form(proj, "product_roles:\n  - role: auditor\n    sign_in: account\n    where: R-2: a read-only user\n"
                          "  - role: guest\n    sign_in: none\n    where: R-3\nblocked: none\n")
    roles, reason = PK.story_roles(proj.task)
    assert reason == "" and roles == [{"role": "auditor", "sign_in": "account", "where": "R-2: a read-only user"},
                                      {"role": "guest", "sign_in": "none", "where": "R-3"}]
    (proj.task / "work" / "handoffs" / "d1.yaml").unlink()
    roles, reason = PK.story_roles(proj.task)
    assert roles == [] and "cannot be read" in reason                                        # an unreadable form says so
    before = proj.task.joinpath("state", "controller.json").read_bytes()
    assert PK.story_roles(proj.task / "nowhere") == ([], "")
    assert proj.task.joinpath("state", "controller.json").read_bytes() == before and not proj.path().exists()


def test_story_roles_skips_placeholder_row(proj):
    template = ("product_roles:\n  - role: <optional: the role's name as the requirements say it>\n    sign_in: <optional: account or none>\n"
                "    where: <optional: the requirement id and the words that name the role>\nblocked: none\n")
    strategist_form(proj, template)
    assert PK.story_roles(proj.task) == ([], "")                                             # the template's own row is never a role
    strategist_form(proj, "product_roles:\n  - role: <fill>\n    sign_in: account\n    where: R-1\n  - role: \"\"\n  - role: reader\nblocked: none\n")
    assert PK.story_roles(proj.task) == ([{"role": "reader", "sign_in": "account", "where": ""}], "")
    strategist_form(proj, "product_roles:\n  - role: auditor\n    sign_in: <optional: account or none>\n    where: <optional: the id>\nblocked: none\n")
    assert PK.story_roles(proj.task) == ([{"role": "auditor", "sign_in": "account", "where": ""}], "")      # a placeholder sign_in reads as account
    strategist_form(proj, "product_roles:\n  - role: auditor\n    sign_in: sometimes\nblocked: none\n")
    assert PK.story_roles(proj.task)[0][0]["sign_in"] == "account"                           # an unknown sign_in: toward asking


def test_acting_line_names_the_answers():
    row = account_fact("PK-3", "dev", "auditor", "2026-11-12T09:40:00+00:00")
    row["provenance"]["story"] = "LOCAL-7"
    assert PK.acting_line([row]) == ('Acting on your earlier answers: the account of "auditor" on "dev" (given in LOCAL-7 on 2026-11-12). '
                                     'To change it, say so.')
    assert PK.acting_line([]) == "" and PK.acting_line(None) == "" and PK.acting_line(["junk"]) == ""
    assert PK.acting_line([row, row]).count("the account of") == 2


# --- t-2181 PC-1b: the three side keys ---------------------------------------------------------------------------------------

def side_args(*more):
    return ["side", "--task", "T-1", *more]


def test_side_cli_writes_known_rows_for_each_key(proj, capsys):
    words = str(proj.words)
    assert run(side_args("--name", "ui", "--stand", "dev", "--reality", "substituted", "--words-file", words)) == 0
    assert run(side_args("--name", "ui", "--deliverable", "no", "--words-file", words)) == 0
    assert run(side_args("--name", "ui", "--stand", "old", "--reference", "--words-file", words)) == 0
    rows = {row["key"]: row for row in proj.rows()}
    assert set(rows) == {PK.STAND_SIDES_KEY, PK.SIDES_KEY, PK.REFERENCE_KEY}
    assert all(row["state"] == "known" and row["element"] == "ui" for row in rows.values())
    assert rows[PK.STAND_SIDES_KEY]["value"] == {"reality": "substituted"} and rows[PK.STAND_SIDES_KEY]["environment"] == "dev"
    assert rows[PK.SIDES_KEY]["value"] == {"deliverable": False, "settles_by": ""} and rows[PK.SIDES_KEY]["environment"] == ""
    assert rows[PK.REFERENCE_KEY]["value"] == {"reference": True} and rows[PK.REFERENCE_KEY]["environment"] == "old"
    assert rows[PK.SIDES_KEY]["provenance"]["words"] == WORDS.strip() and rows[PK.SIDES_KEY]["provenance"]["by"] == "conductor"
    settles = proj.words.parent / "settles.txt"
    settles.write_text("platform team\n", encoding="utf-8")
    assert run(side_args("--name", "api", "--deliverable", "yes", "--settles-by-file", str(settles), "--words-file", words)) == 0
    assert [r for r in proj.rows() if r["element"] == "api"][0]["value"] == {"deliverable": True, "settles_by": "platform team"}


def test_a_later_word_overwrites_whose_side_it_is_and_the_history_stays(proj, capsys):
    """t-2277 batch 2b W2 (2): the person's later word about `--deliverable` is the project's value from then on - the earlier row stays
    (it is history, with its words and time), the latest one is read, and a third word flips it back only by being a third row."""
    words = str(proj.words)
    assert run(side_args("--name", "backend", "--deliverable", "yes", "--words-file", words)) == 0
    assert PK.state(proj.root, PK.SIDES_KEY, "", "backend")["row"]["value"]["deliverable"] is True
    assert run(side_args("--name", "backend", "--deliverable", "no", "--words-file", words)) == 0
    latest = PK.state(proj.root, PK.SIDES_KEY, "", "backend")["row"]
    assert latest["value"] == {"deliverable": False, "settles_by": ""}                       # the later word overwrites
    assert latest["provenance"]["source"] == "person" and latest["provenance"]["by"] == "conductor" and latest["provenance"]["words"] == WORDS.strip()
    assert latest["provenance"]["story"] == "T-1" and latest["at"]                            # who and when are recorded with the value
    assert len([r for r in proj.rows() if r["element"] == "backend"]) == 2                    # the earlier row is not rewritten
    assert run(side_args("--name", "backend", "--deliverable", "no", "--words-file", words)) == 0
    assert len([r for r in proj.rows() if r["element"] == "backend"]) == 2                    # the same word again is the existing row
    assert run(side_args("--name", "backend", "--deliverable", "yes", "--words-file", words)) == 0
    assert PK.state(proj.root, PK.SIDES_KEY, "", "backend")["row"]["value"]["deliverable"] is True
    assert len([r for r in proj.rows() if r["element"] == "backend"]) == 3                    # flipping back is a row of its own, never silent


def test_side_deliverable_beside_stand_says_it_is_project_wide(proj, capsys):
    """t-2277 batch 2b (critic t-2475 N3): `--stand` beside `--deliverable` is dropped, and the output says so; no `--stand`, no note."""
    words = str(proj.words)
    assert run(side_args("--name", "ui", "--deliverable", "no", "--stand", "dev", "--words-file", words)) == 0
    out = capsys.readouterr().out
    assert "--stand dev was not used" in out and "whole project" in out, out
    assert [r for r in proj.rows() if r["element"] == "ui"][0]["environment"] == ""         # the row is the project's, as before
    assert run(side_args("--name", "api", "--deliverable", "no", "--words-file", words)) == 0
    assert "was not used" not in capsys.readouterr().out
    assert run(side_args("--name", "ui", "--stand", "dev", "--reality", "substituted", "--words-file", words)) == 0
    assert "was not used" not in capsys.readouterr().out                                      # a stand beside `--reality` is used


def test_record_refuses_a_bad_side_value(proj):
    base = dict(environment="dev", element="ui", scope="stand", key=PK.STAND_SIDES_KEY)
    for value in ({"reality": "mocked"}, {"reality": "real", "x": 1}, {}, None, "real"):
        row, problem, _ = proj.record(value=value, **base)
        assert row is None and "references/side-realities.json" not in problem and "reality" in problem, value
    row, problem, _ = proj.record(key=PK.SIDES_KEY, environment="", element="ui", scope="project", value={"settles_by": "x"})
    assert row is None and "deliverable" in problem
    row, problem, _ = proj.record(key=PK.SIDES_KEY, environment="", element="ui", scope="project", value={"deliverable": "yes"})
    assert row is None and "deliverable" in problem
    row, problem, _ = proj.record(key=PK.REFERENCE_KEY, environment="old", element="ui", scope="stand", value={"reference": False})
    assert row is None and "reference" in problem
    row, problem, _ = proj.record(key=PK.SIDES_KEY, environment="", element="ui", scope="project", state="not_needed",
                                  value={"deliverable": True})
    assert row is None and "`known` only" in problem
    row, problem, _ = proj.record(key=PK.SIDES_KEY, environment="", element=" ui", scope="project", value={"deliverable": True})
    assert row is None and "compared exactly" in problem
    for name in ("web.app", "a=b"):     # a key of the story's record (`sides.<name>.<attribute>=<value>`): refused, with the door
        row, problem, _ = proj.record(key=PK.SIDES_KEY, environment="", element=name, scope="project", value={"deliverable": True})
        assert row is None and "without them" in problem and "nothing was recorded" in problem, name
    assert not proj.path().exists()                                                           # nothing was written by any refusal


def test_ui_and_ui_are_two_subjects(proj):
    for name in ("UI", "ui"):
        assert proj.record(key=PK.SIDES_KEY, environment="", element=name, scope="project", value={"deliverable": True})[2] is True
    assert PK.subjects(proj.root, PK.SIDES_KEY) == {"subjects": [("", "UI"), ("", "ui")], "problem": ""}
    assert PK.state(proj.root, PK.SIDES_KEY, "", "UI")["row"]["id"] != PK.state(proj.root, PK.SIDES_KEY, "", "ui")["row"]["id"]
    assert PK.state(proj.root, PK.SIDES_KEY, "", "Ui")["state"] == "unknown"


def test_subjects_skips_revoked_latest_wins_unparseable_at_loses(proj):
    def side_fact(id, env, element, at, **extra):
        return fact(id, PK.STAND_SIDES_KEY, env, element, "known", at, **dict({"scope": "stand", "value": {"reality": "real"}}, **extra))
    proj.facts([side_fact("PK-1", "dev", "ui", "2026-11-01T10:00:00+00:00"),
                side_fact("PK-2", "dev", "ui", "2026-11-02T10:00:00+00:00", value={"reality": "substituted"}),
                side_fact("PK-3", "dev", "ui", "garbage", value={"reality": "absent"}),
                side_fact("PK-4", "dev", "gone", "2026-11-01T10:00:00+00:00", revoked_at="2026-11-03T10:00:00+00:00"),
                side_fact("PK-5", "Dev", "api", "2026-11-01T10:00:00+00:00"),
                fact("PK-6", PK.STAND_SIDES_KEY, "dev", "odd", "asked", "2026-11-01T10:00:00+00:00", scope="stand")])
    assert PK.subjects(proj.root, PK.STAND_SIDES_KEY)["subjects"] == [("Dev", "api"), ("dev", "ui")]       # revoked and `asked` skipped
    assert PK.subjects(proj.root, PK.STAND_SIDES_KEY, "dev")["subjects"] == [("dev", "ui")]               # the stand is exact
    assert PK.state(proj.root, PK.STAND_SIDES_KEY, "dev", "ui")["row"]["id"] == "PK-2"                    # latest wins; the bad `at` loses
    assert PK.subjects(proj.root, PK.REFERENCE_KEY) == {"subjects": [], "problem": ""}


def test_subjects_never_raises_and_says_the_problem(proj):
    proj.path().parent.mkdir(parents=True, exist_ok=True)
    proj.path().write_text("{not json", encoding="utf-8")
    got = PK.subjects(proj.root, PK.SIDES_KEY)
    assert got["subjects"] == [] and got["problem"]
    assert PK.subjects(proj.root / "nowhere", PK.SIDES_KEY) == {"subjects": [], "problem": ""}


def test_side_refused_on_a_no_trace_story_with_the_door(tmp_path, monkeypatch, capsys):
    proj = Proj(tmp_path, monkeypatch, pipeline={"ticket": "T-1", "no_trace": True})
    assert run(side_args("--name", "ui", "--stand", "dev", "--reality", "real", "--words-file", str(proj.words))) == 2
    assert "an experiment leaves no trace" in capsys.readouterr().err and not proj.path().exists()


def test_side_cli_needs_one_mode_and_a_stand(proj, capsys):
    with pytest.raises(SystemExit):
        run(side_args("--name", "ui", "--words-file", str(proj.words)))
    capsys.readouterr()
    assert run(side_args("--name", "ui", "--stand", "dev", "--reality", "mocked", "--words-file", str(proj.words))) == 2
    assert "reality" in capsys.readouterr().err and not proj.path().exists()


# --- SS1-11 B1: what a person taught about the stand (`lesson`, `lessons`) ---------------------------------------------------------

def lesson_args(*more, subject="indexing"):
    return ["lesson", "--task", "T-1", "--subject", subject, "--stand", "dev", *more]


def lesson_fact(id, element, at, *, environment="dev", words="w", value=None, **extra) -> dict:
    return dict({"id": id, "key": PK.LESSONS_KEY, "environment": environment, "element": element, "state": "known", "scope": "stand",
                 "value": {"wait_s": None} if value is None else value,
                 "provenance": {"source": "person", "words": words, "story": "S-1", "by": "conductor", "where": ""}, "at": at}, **extra)


def _lesson_record_problems(element="indexing", value=None, **over):
    args = dict(key=PK.LESSONS_KEY, environment="dev", element=element, state="known", scope="stand", words="w", source="person",
                by="conductor", value={"wait_s": None} if value is None else value)
    args.update(over)
    return PK.record_problems(**args)


@pytest.mark.parametrize("element, value, expected", [
    ("indexing", {"wait_s": None}, ""),                                      # E32: no wait
    ("indexing", {"wait_s": 1}, ""),
    ("indexing", {"wait_s": 86400}, ""),
    ("x" * 80, {"wait_s": None}, ""),                                        # E33: AT the limit
    ("x" * 81, {"wait_s": None}, "81 characters, at most 80"),               # E33: beyond it, refused, never cut
    (NON_ASCII + " " + chr(0x1F600), {"wait_s": None}, ""),   # E34: Cyrillic and an emoji are data
    ("", {"wait_s": None}, "subject is empty"),
    ("   ", {"wait_s": None}, "subject is empty"),
    (" x", {"wait_s": None}, "space at an end"),                             # E35
    ("x\t", {"wait_s": None}, "space at an end"),
    ("a\x00b", {"wait_s": None}, "control character"),
    ("indexing", {"wait_s": True}, "--wait-s <seconds from 1 to 86400>"),    # a bool is not seconds
    ("indexing", {"wait_s": 0}, "--wait-s"),
    ("indexing", {"wait_s": 86401}, "--wait-s"),
    ("indexing", {"wait_s": "7"}, "--wait-s"),
    ("indexing", {"wait_s": 1.5}, "--wait-s"),
    ("indexing", {"wait_s": 5, "x": 1}, "--wait-s"),                         # an extra value key
    ("indexing", {}, "--wait-s"),
    ("indexing", None, ""),                                                  # the helper turns None into {"wait_s": None}
], ids=lambda v: str(v)[:14])
def test_lesson_value_faults(element, value, expected):
    problems = _lesson_record_problems(element, value)
    if expected:
        assert len(problems) == 1 and expected in problems[0] and problems[0].endswith("nothing was recorded"), problems
    else:
        assert problems == []


def test_lesson_subject_never_meets_the_role_rules_and_a_role_key_still_does():
    assert _lesson_record_problems("a,b|c") == []                            # a role rule would refuse the comma and the bar
    assert _lesson_record_problems("env:x") == []                            # and the reserved forms
    assert PK.record_problems(PK.ROLES_KEY, "", "a,b", "known", "project", "w", "person", "conductor", value={"sign_in": "account"})


def test_lesson_empty_words_name_the_lesson_door():
    problems = _lesson_record_problems(words="  ")
    assert len(problems) == 1 and "project_knowledge.py lesson --task <T> --subject <words>" in problems[0] and "role --task" not in problems[0]


@pytest.mark.parametrize("wait, good", [
    ("1", True), ("86400", True), ("007", True),                              # E31: AT the limits and leading zeros
    ("0", False), ("-1", False), ("86401", False), ("abc", False), ("1.5", False), ("1e3", False), (" 7", False), ("+7", False),
    ("1_0", False), ("٣", False), ("9" * 4301, False), ("", False),      # BEYOND them; a Unicode digit; more digits than int() reads
], ids=lambda v: str(v)[:14])
def test_lesson_wait_s_pattern(proj, capsys, wait, good):
    assert run(lesson_args("--wait-s", wait, "--words-file", str(proj.words))) == (0 if good else 2)
    err = capsys.readouterr().err
    if good:
        assert proj.rows()[0]["value"] == {"wait_s": int(wait)}
    else:
        assert "--wait-s takes whole seconds from 1 to 86400" in err and "nothing was recorded" in err and not proj.path().exists()


def test_lesson_verb_scenario(proj, capsys, tmp_path):
    words = str(proj.words)
    assert run(lesson_args("--words-file", words)) == 0                                  # E32: no --wait-s
    out = capsys.readouterr().out
    assert out.startswith("indexing on dev: environments.stand_lessons recorded (PK-1)"), out
    first = proj.rows()[0]
    assert first["value"] == {"wait_s": None} and first["provenance"]["words"] == WORDS.strip() and first["provenance"]["by"] == "conductor"
    assert first["scope"] == "stand" and first["environment"] == "dev" and first["state"] == "known"
    assert run(lesson_args("--words-file", words)) == 0                                  # E37: the same again
    assert "already recorded (PK-1)" in capsys.readouterr().out and len(proj.rows()) == 1
    corrected = tmp_path / "corrected.txt"
    corrected.write_text("it takes ten minutes, not three", encoding="utf-8")
    assert run(lesson_args("--words-file", str(corrected))) == 0                         # E37: NEW words are a new row, never "already"
    out = capsys.readouterr().out
    assert "recorded (PK-2)" in out and "already" not in out
    assert [r["provenance"]["words"] for r in proj.rows()] == [WORDS.strip(), "it takes ten minutes, not three"]
    assert run(lesson_args("--wait-s", "600", "--words-file", str(corrected))) == 0      # a different wait is a new row too
    assert "recorded (PK-3)" in capsys.readouterr().out
    assert PK.lessons(proj.root, "dev")["lines"][0].startswith('indexing: "it takes ten minutes, not three" (at least 600 s)')
    assert run(lesson_args("--words-file", str(tmp_path / "absent.txt"))) == 2          # E36: no words, no row
    capsys.readouterr()
    empty = tmp_path / "empty.txt"
    empty.write_text("  \n", encoding="utf-8")
    assert run(lesson_args("--words-file", str(empty))) == 2 and len(proj.rows()) == 3
    capsys.readouterr()
    assert run(["lesson", "--task", "T-1", "--subject", "indexing", "--stand", "dev"]) == 2 and len(proj.rows()) == 3   # no --words-file
    capsys.readouterr()
    assert run(lesson_args("--words-file", words, subject="Indexing")) == 0              # E34: compared exactly, two lessons
    assert len(PK.lessons(proj.root, "dev")["rows"]) == 2
    capsys.readouterr()
    # E44 (OF3-2 K1): revoke the newest row of the subject: no older row comes back; revoking the older ones still succeeds
    assert run(["revoke", "--task", "T-1", "--id", "PK-3", "--words-file", words]) == 0
    out = capsys.readouterr().out
    assert "no longer read" in out and "no older answer comes back" in out and "account" not in out, out
    assert [r["element"] for r in PK.lessons(proj.root, "dev")["rows"]] == ["Indexing"]       # `indexing` is gone at once: nothing older comes back
    for pk in ("PK-2", "PK-1"):
        assert run(["revoke", "--task", "T-1", "--id", pk, "--words-file", words]) == 0
    assert [r["element"] for r in PK.lessons(proj.root, "dev")["rows"]] == ["Indexing"]


def test_lesson_revoke_of_a_role_keeps_today_sentence(proj, capsys):
    assert run(["role", "--task", "T-1", "--role", "auditor", "--state", "known", "--words-file", str(proj.words)]) == 0
    capsys.readouterr()
    assert run(["revoke", "--task", "T-1", "--id", "PK-1", "--words-file", str(proj.words)]) == 0
    assert "it is asked again where it is needed" in capsys.readouterr().out


def test_lesson_stand_comes_from_the_story_or_is_refused(tmp_path, monkeypatch, capsys):
    proj = Proj(tmp_path, monkeypatch, stands=[{"name": "dev"}, {"name": "prod"}])
    words = str(proj.words)
    assert run(["lesson", "--task", "T-1", "--subject", "x", "--words-file", words]) == 2        # the story chose no stand
    err = capsys.readouterr().err
    assert "pass --stand <name>" in err and "`dev`" in err and "`prod`" in err and "nothing was recorded" in err and not proj.path().exists()
    (proj.task / "pipeline.json").write_text(json.dumps({"ticket": "T-1", "environment": "dev"}), encoding="utf-8")
    assert run(["lesson", "--task", "T-1", "--subject", "x", "--words-file", words]) == 0
    assert proj.rows()[0]["environment"] == "dev"


def test_lesson_refused_on_a_no_trace_story_with_the_door(tmp_path, monkeypatch, capsys):          # E38
    proj = Proj(tmp_path, monkeypatch, pipeline={"ticket": "T-1", "no_trace": True})
    assert run(lesson_args("--words-file", str(proj.words))) == 2
    assert "an experiment leaves no trace" in capsys.readouterr().err and not proj.path().exists()


def test_lessons_reader_and_verb(proj, capsys):
    assert PK.lessons(proj.root, "dev") == {"lines": [], "rows": [], "problem": "", "no_stand": False}     # E39: no file
    assert run(["lessons", "--stand", "dev"]) == 0 and capsys.readouterr().out.strip() == "no lesson is recorded for dev"
    for stand in ("", PK.PLACEHOLDER_STAND):                                                              # E53
        assert PK.lessons(proj.root, stand) == {"lines": [], "rows": [], "problem": "", "no_stand": True}
    assert run(["lessons"]) == 0 and capsys.readouterr().out.strip() == "no stand is chosen; pass --stand <name>"
    proj.facts([lesson_fact("PK-1", "B-wait", "2026-11-01T10:00:00", words="old"),
                lesson_fact("PK-2", "B-wait", "2026-11-02T10:00:00", words="new", value={"wait_s": 90}),
                lesson_fact("PK-3", "A-filter", "2026-11-01T10:00:00", words="narrow it"),
                lesson_fact("PK-4", "other", "2026-11-01T10:00:00", environment="prod"),                  # E41: another stand
                lesson_fact("PK-5", "gone", "2026-11-01T10:00:00", revoked_at="2026-11-03T10:00:00")])
    got = PK.lessons(proj.root, "dev")
    assert got["lines"] == ['A-filter: "narrow it" (given in S-1 on 2026-11-01)',
                            'B-wait: "new" (at least 90 s) (given in S-1 on 2026-11-02)']
    assert [r["id"] for r in got["rows"]] == ["PK-3", "PK-2"] and got["problem"] == ""
    assert run(["lessons", "--stand", "dev"]) == 0 and capsys.readouterr().out.strip().splitlines() == got["lines"]
    assert run(["lessons", "--task", "T-1", "--stand", "prod"]) == 0 and 'other: "w"' in capsys.readouterr().out
    assert run(["lessons", "--task", "T-1"]) == 0 and capsys.readouterr().out.strip().splitlines() == got["lines"]   # the story's one stand
    capsys.readouterr()
    assert run(["lessons", "--task", "T-9", "--stand", "dev"]) == 2                                     # no such story
    err = capsys.readouterr().err                                                                      # F6: a read verb never says "recorded"
    assert "there is no story `T-9`" in err and "--stand <name>" in err and "recorded" not in err


def test_lessons_reader_never_drops_a_hand_edited_row_and_strips_controls_in_the_display(proj):
    esc = "\x1b[31mred\x1b[0m   and\ttabs\x00"
    proj.facts([lesson_fact("PK-1", "str-wait", "2026-11-01T10:00:00", value={"wait_s": "9"}),               # E39a
                lesson_fact("PK-2", "float-wait", "2026-11-01T10:00:00", value={"wait_s": 1.5}),
                lesson_fact("PK-3", "bool-wait", "2026-11-01T10:00:00", value={"wait_s": True}),
                lesson_fact("PK-4", "extra-key", "2026-11-01T10:00:00", value={"wait_s": 5, "x": 1}),
                lesson_fact("PK-5", "not-dict", "2026-11-01T10:00:00", value="oops"),
                lesson_fact("PK-6", "esc", "2026-11-01T10:00:00", words=esc)])
    got = PK.lessons(proj.root, "dev")
    assert len(got["lines"]) == 6 and all("(at least" not in line for line in got["lines"]), got["lines"]
    esc_line = [line for line in got["lines"] if line.startswith("esc:")][0]
    assert "\x1b" not in esc_line and "\x00" not in esc_line and "[31mred[0m and tabs" in esc_line
    assert [r for r in got["rows"] if r["id"] == "PK-6"][0]["provenance"]["words"] == esc          # the store keeps them
    proj.facts([lesson_fact("PK-1", "a\x1bb", "2026-11-01T10:00:00")])
    assert PK.lessons(proj.root, "dev")["lines"][0].startswith('ab: ')


def test_lessons_every_line_and_the_words_whole(proj):          # FV1-4 2a / F9 a: E47, E48, E28
    long_words = "w" * 1000
    proj.facts([lesson_fact(f"PK-{n}", f"s{n:02d}", "2026-11-01T10:00:00", words=long_words) for n in range(1, 12)])
    got = PK.lessons(proj.root, "dev")
    assert len(got["lines"]) == 11 and "more" not in got and not any("more" in line.split('"')[0] for line in got["lines"])
    assert not any(line.endswith(' ..."') or "(+1 more" in line for line in got["lines"])
    assert got["lines"][0].startswith('s01: "' + long_words + '"') and len(got["rows"]) == 11
    assert got["rows"][0]["provenance"]["words"] == long_words                                     # stored whole, shown whole
    assert PK.lessons(proj.root, "dev")["rows"][0]["provenance"]["words"] == long_words           # a reader never writes anything back


def test_lessons_words_of_200_201_and_200000_whole_and_a_stand_with_a_space(tmp_path, monkeypatch):          # E48 AT and BEYOND, E28
    proj = Proj(tmp_path, monkeypatch, stands=[{"name": "staging eu"}])
    sizes = {1: 200, 2: 201, 3: 200_000}
    proj.facts([lesson_fact(f"PK-{n}", f"s{n:02d}", "2026-11-01T10:00:00", environment="staging eu", words="w" * sizes.get(n, 5))
                for n in range(1, 12)])
    got = PK.lessons(proj.root, "staging eu")
    assert len(got["lines"]) == 11 and not any("more:" in line for line in got["lines"])           # 11 lessons: 11 lines
    assert [got["lines"][i].startswith(f's0{i + 1}: "' + "w" * sizes[i + 1] + '"') for i in range(3)] == [True] * 3
    assert not any(" ..." in line for line in got["lines"])


def test_lessons_problem_is_not_no_lesson(proj, monkeypatch):           # E40 and the unreadable registry
    proj.path().parent.mkdir(parents=True, exist_ok=True)
    proj.path().write_text("{not json", encoding="utf-8")
    got = PK.lessons(proj.root, "dev")
    assert got["lines"] == [] and got["problem"] and got["no_stand"] is False
    monkeypatch.setattr(PK, "KEYS", {})
    monkeypatch.setattr(PK, "CATALOGUE_PROBLEM", "the catalogue is damaged; reinstall the plugin")
    assert PK.lessons(proj.root, "dev")["problem"] == "the catalogue is damaged; reinstall the plugin"
    assert PK.lessons(proj.root, "")["no_stand"] is True and PK.lessons(proj.root, "")["problem"] == ""


# --- phase 1 (OF3-1a): the catalogue and the one reader (AR-1, AR-9, AR-13, AR-28) -----------------------------------------------

FIVE_KEYS = ["product.roles", "environments.credentials_by_role", "product.sides", "environments.sides", "environments.reference_for",
             "environments.stand_lessons", "environments.sign_in", "environments.page_load", "environments.extra_instance",
             "manual.accounts_way", "manual.data_way", "manual.data_way.may"]       # the name is kept from the five of PC-1b; later keys appended (OF3-2 K1: the three the seam asks)


def test_keys_are_derived_from_the_catalogue_in_todays_order():
    assert list(PK.KEYS) == FIVE_KEYS and PK.CATALOGUE_PROBLEM == ""
    assert PK.KEYS == {"product.roles": {"scope": "project", "compare": "role_form"},
                       "environments.credentials_by_role": {"scope": "stand", "compare": "role_form"},
                       "product.sides": {"scope": "project", "compare": "exact"},
                       "environments.sides": {"scope": "stand", "compare": "exact"},
                       "environments.reference_for": {"scope": "stand", "compare": "exact"},
                       "environments.stand_lessons": {"scope": "stand", "compare": "exact"},
                       "environments.sign_in": {"scope": "stand", "compare": "exact"},
                       "environments.page_load": {"scope": "stand", "compare": "exact"},
                       "environments.extra_instance": {"scope": "stand", "compare": "exact"},
                       "manual.accounts_way": {"scope": "project", "compare": "exact"},
                       "manual.data_way": {"scope": "project", "compare": "exact"},
                       "manual.data_way.may": {"scope": "project", "compare": "exact"}}
    assert [row["key"] for row in PK.rows() if row["store"] in ("registry", "config+registry")] == FIVE_KEYS[:9]   # the three new rows are config-stored
    assert [row["key"] for row in PK.rows("artifact_root")] == ["artifact_root"] and PK.rows("no.such.key") == []


def test_config_only_key_refused_with_todays_text(proj):
    expected = f"the key 'test_data.seeds' is not a project-knowledge key (the keys: {', '.join(FIVE_KEYS)}); nothing was recorded"
    row, problem, created = proj.record(key="test_data.seeds")
    assert (row, problem, created) == (None, expected, False) and not proj.path().exists()
    assert PK.record_problems("artifact_root", "", "x", "known", "project", "w", "person", "conductor") == \
        [expected.replace("'test_data.seeds'", "'artifact_root'")]


def _table_without_section(real):
    return lambda: {k: v for k, v in real.items() if k != "knowledge"}


def _table_without_scope(real):
    del real["knowledge"][PK.ROLES_KEY]["scope"]
    return lambda: real


def _raises(real=None):
    def fail():
        raise ValueError("references/config-keys.json of the plugin is unreadable (OSError: x); the plugin install is damaged - "
                         "reinstall the plugin")
    return fail


@pytest.mark.parametrize("damage, kept", [(_raises, []), (_table_without_section, []), (_table_without_scope, FIVE_KEYS[1:])],
                         ids=["config_keys_raises", "no_knowledge_section", "registry_row_without_scope"])
def test_damaged_catalogue_refusal_names_the_damage_and_the_door(proj, monkeypatch, damage, kept):
    import importlib
    fake = damage(json.loads(json.dumps(CC.config_keys())))
    monkeypatch.setattr(CC, "config_keys", fake)
    try:
        importlib.reload(PK)                                  # the damaged table is an INPUT: KEYS and CATALOGUE_PROBLEM are rebuilt
        assert list(PK.KEYS) == kept and PK.CATALOGUE_PROBLEM
        row, problem = PK.record(proj.root, key=PK.ROLES_KEY, environment="", element="auditor", state="known", scope="project",
                                 value={"sign_in": "account"}, words="the person said so", source="person", story="T-1", by="conductor")[:2]
        assert row is None and "catalogue is damaged" in problem and "reinstall the plugin" in problem and "nothing was recorded" in problem
        assert PK.CATALOGUE_PROBLEM in problem and "not a project-knowledge key" not in problem and not proj.path().exists()
        assert problem.count("reinstall the plugin") == 1, problem                                 # the door is said once
        if kept:                                              # the other registry keys judge as today
            assert PK.record_problems(PK.ACCOUNTS_KEY, "dev", "auditor", "known", "stand", "w", "person", "conductor") == []
    finally:
        monkeypatch.undo()
        importlib.reload(PK)
    assert list(PK.KEYS) == FIVE_KEYS and PK.CATALOGUE_PROBLEM == ""           # negative control: the healthy table is back


def _put(proj, raw):
    if raw is None:
        proj.config.unlink()
    else:
        proj.config.write_bytes(raw)


BOM = b"\xef\xbb\xbf"


@pytest.mark.parametrize("raw, key, environment", [
    (None, "test_data.seeds", ""),
    (BOM, "test_data.seeds", ""),
    (b"", "test_data.seeds", ""),
    (b"[]", "test_data.seeds", ""),
    (b'"x"', "test_data.seeds", ""),
    (b"null", "test_data.seeds", ""),
    (b'{"test_data": "x"}', "test_data.seeds", ""),
    (b'{"test_data": {"seeds": null}}', "test_data.seeds", ""),
    (b'{"test_data": {}}', "test_data.seeds", ""),
    (b'{"test_data": {"seeds": "s"}}', "test_data.colours", ""),
    (b'{"environments": "x"}', "environments[].safe_to_break", "dev"),
    (b'{"environments": [{"name": "dev"}, {"name": "dev"}]}', "environments[].safe_to_break", "dev"),
    (b'{"environments": [{"name": "Dev", "safe_to_break": "x"}]}', "environments[].safe_to_break", "dev"),
    (b'{"environments": [{"name": "dev", "safe_to_break": "x"}]}', "environments[].safe_to_break", ""),
    (b'{"artifact_root": "x"}', "artifact_root", "__damaged__"),
], ids=["absent_config", "bom_only", "empty_file", "list_document", "string_document", "null_document", "non_dict_parent",
        "stored_none", "path_missing", "key_with_no_row", "environments_not_a_list", "two_stands_one_name", "stand_name_case",
        "stand_name_empty", "damaged_catalogue"])
def test_value_toward_unknown(proj, monkeypatch, raw, key, environment):
    _put(proj, raw)
    if environment == "__damaged__":
        monkeypatch.setattr(CC, "config_keys", _raises())
        environment = ""
    got = PK.value(proj.root, key, environment)
    assert got["state"] == "unknown" and got["value"] is None, got
    assert PK.value(proj.root / "nowhere", key, environment)["state"] == "unknown"      # a root with no config: never known


@pytest.mark.parametrize("raw, key, environment, expected", [
    (BOM + b'{"test_data": {"seeds": "factory-boy"}}', "test_data.seeds", "", "factory-boy"),
    (b'{"test_data": {"seeds": ""}}', "test_data.seeds", "", ""),
    (b'{"test_data": {"seeds": []}}', "test_data.seeds", "", []),
    (b'{"environments": [{"name": "dev", "safe_to_break": "everything"}]}', "environments[].safe_to_break", "dev", "everything"),
    (b'{"artifact_root": "qa-artifacts"}', "artifact_root", "", "qa-artifacts"),
], ids=["bom_value_read", "empty_text_is_known", "empty_list_as_stored", "stand_value", "artifact_root"])
def test_value_known_controls(proj, raw, key, environment, expected):
    _put(proj, raw)
    got = PK.value(proj.root, key, environment)
    assert got["state"] == "known" and got["value"] == expected and got["source"] == "config" and got["problem"] == ""


def test_value_absent_config_and_unreadable_config_say_which(proj):
    proj.config.unlink()
    assert PK.value(proj.root, "test_data.seeds") == {"value": None, "state": "unknown", "source": "absent", "problem": ""}
    proj.config.write_bytes(b"{broken")
    got = PK.value(proj.root, "test_data.seeds")
    assert got["state"] == "unknown" and "not valid JSON" in got["problem"] and len(got["problem"]) <= 200
    assert "no catalogue row for test_data.colours" in PK.value(proj.root, "test_data.colours")["problem"]


def test_value_of_a_registry_row_is_the_state_reader_own_answer(proj):
    proj.write_config(environments=[{"name": "dev", "credentials_by_role": {"auditor": {"user_key": "U", "secret_key": "S"}}}])
    row, problem = PK.record(proj.root, key=PK.ROLES_KEY, environment="", element="auditor", state="known", scope="project",
                             value={"sign_in": "account"}, words="the person said so", source="person", story="T-1", by="conductor")[:2]
    assert row is not None and problem == "", problem
    got = PK.value(proj.root, PK.ROLES_KEY, element="auditor")                                  # a found row: its stored value
    assert got["state"] == PK.state(proj.root, PK.ROLES_KEY, "", "auditor")["state"] == "known"
    assert got["value"] == {"sign_in": "account"} and got["problem"] == ""
    empty = PK.value(proj.root, PK.ROLES_KEY)                                                   # no element: unknown, and it says why
    assert empty["state"] == "unknown" and empty["value"] is None and "no element was named" in empty["problem"] and "element=" in empty["problem"]
    assert PK.value(proj.root, PK.ROLES_KEY, element="nobody")["state"] == "unknown"


def test_stand_by_name_is_one_road_for_a_non_string_name(proj):
    cfg = {"environments": [{"name": 5, "credentials_by_role": {"auditor": {"user_key": "U", "secret_key": "S"}}, "safe_to_break": "x"}]}
    assert PK.environment("5", cfg=cfg)["found"] is False                                       # the card says: no stand is named 5
    assert PK.state(proj.root, PK.ACCOUNTS_KEY, "5", "auditor", cfg)["state"] == "unknown"      # the account reader agrees
    assert PK.value(proj.root, "environments[].safe_to_break", "5", cfg)["state"] == "unknown"


@pytest.mark.parametrize("raw, name, found, problem", [
    (b'{"environments": [{"name": "dev", "base_url": "u"}]}', "dev", True, ""),
    (b'{"environments": []}', "dev", False, "the project records no stand"),
    (b"{}", "dev", False, "the project records no stand"),
    (b'{"environments": "x"}', "dev", False, "environments is not a list"),
    (b'{"environments": [{"name": "dev"}, {"name": "dev"}]}', "dev", False, "two stands are named dev"),
    (b'{"environments": [{"name": "Dev"}]}', "dev", False, "no stand is named dev"),
    (b'{"environments": [{"name": "dev"}]}', "", False, "no stand name was given"),
    (b'{"environments": [{"name": "dev"}]}', None, False, "no stand name was given"),
    (b'{"environments": ["dev", 5, {"name": "dev"}]}', "dev", True, ""),
], ids=["found", "empty_list", "absent_list", "not_a_list", "twins", "case_differs", "empty_name", "none_name", "non_dict_entries_ignored"])
def test_environment_card_edges(proj, raw, name, found, problem):
    _put(proj, raw)
    got = PK.environment(name, proj.root)
    assert got["found"] is found and got["problem"] == problem and (got["entry"] is not None) is found, got
    assert PK.environment(name, cfg=json.loads(raw)) == got                                   # a given config reads the same


def test_environment_card_without_a_config_says_why(proj):
    assert PK.environment("dev")["found"] is False and PK.environment("dev")["problem"] == "no project root was given"
    proj.config.unlink()
    assert PK.environment("dev", proj.root) == {"found": False, "entry": None, "problem": "the project records no stand"}
    proj.config.write_bytes(b"[]")
    got = PK.environment("dev", proj.root)
    assert got["found"] is False and "not a JSON object" in got["problem"]


@pytest.mark.parametrize("raw, problem_names_config", [
    (b"{broken", True),
    (b"[]", True),
    (b"", True),
    (None, False),
    (b'{"environments": []}', False),
    (b'{"product": "x", "environments": "x"}', False),
], ids=["broken_json", "non_object_list", "empty_file", "absent_file_control", "no_roles_key_control", "wrong_type_control"])
def test_roster_says_an_unreadable_config_is_unknown(proj, raw, problem_names_config):
    _put(proj, raw)
    got = PK.roster(proj.root, None, "dev")
    assert set(got) == {"elements", "removed", "problem"} and got["elements"] == [] and got["removed"] == []
    assert bool(got["problem"]) is problem_names_config, got
    if problem_names_config:
        assert "qa-factory/config.json is there but cannot be read (" in got["problem"] and "repair" in got["problem"]
        assert "Traceback" not in got["problem"] and ".py" not in got["problem"]


def _registry_with_answers(proj):
    proj.facts([role_fact("PK-1", "auditor", "not_needed", "2026-11-01T10:00:00+00:00"),
                role_fact("PK-2", "editor", "known", "2026-11-01T10:05:00+00:00")])
    proj.config.write_bytes(b"{broken")


def test_roster_unreadable_config_keeps_the_registry_roles_and_the_account_unknown(proj):
    """PK2-14 fix round (critic t-448 B1): the registry rows do not depend on the config; only the config part and `account` are unknown."""
    _registry_with_answers(proj)
    got = PK.roster(proj.root, None, "dev")
    assert [(e["role"], e["state"], e["account"]) for e in got["elements"]] == [("editor", "known", None)], got
    assert [r["role"] for r in got["removed"]] == ["auditor"] and got["problem"], got
    assert "cannot be read (" in got["problem"] and "not known" in got["problem"]


def test_notice_from_handoff_on_an_unreadable_config_never_overwrites_the_person(proj):
    _registry_with_answers(proj)
    strategist_form(proj, "product_roles:\n  - role: auditor\n    sign_in: account\n    where: R-1\n"
                          "  - role: editor\n    sign_in: account\n    where: R-2\nblocked: none\n")
    assert PK.notice_from_handoff(proj.root, proj.task, "T-1") == []
    assert len(proj.rows()) == 2
    assert PK.state(proj.root, PK.ROLES_KEY, "", "auditor")["state"] == "not_needed"
    assert PK.state(proj.root, PK.ROLES_KEY, "", "editor")["state"] == "known"


def test_roster_unreadable_config_keeps_the_registry_problem_too(proj):
    proj.path().parent.mkdir(parents=True, exist_ok=True)
    proj.path().write_text("{broken", encoding="utf-8")
    proj.config.write_bytes(b"[]")
    got = PK.roster(proj.root, None, "dev")
    assert got["elements"] == [] and got["problem"].count(";") >= 1 and "qa-factory/config.json" in got["problem"], got


def test_state_and_roster_with_a_given_cfg_ignore_the_file(proj):
    proj.config.write_bytes(b"{broken")
    cfg = {"environments": [{"name": "dev", "credentials_by_role": {"auditor": AUDITOR}}]}
    got = PK.roster(proj.root, cfg, "dev")
    assert got["problem"] == "" and [e["role"] for e in got["elements"]] == ["auditor"] and got["elements"][0]["account"] is True
    assert PK.state(proj.root, PK.ACCOUNTS_KEY, "dev", "auditor", cfg)["state"] == "known"


@pytest.mark.parametrize("raw", [b"{broken", b"[]", b""], ids=["broken_json", "non_object_list", "empty_file"])
def test_account_state_on_an_unreadable_config_is_unknown(proj, raw):
    proj.config.write_bytes(raw)
    got = PK.state(proj.root, PK.ACCOUNTS_KEY, "dev", "auditor")
    assert got["state"] == "unknown" and got["row"] is None


DECIDED = [s for s in PK.STATES if s != PK.NOTICED]        # read from the module's own closed set, not listed here


def _noticed_form(proj):
    strategist_form(proj, "product_roles:\n  - role: auditor\n    sign_in: account\n    where: R-1\nblocked: none\n")


@pytest.mark.parametrize("decided", DECIDED)
def test_notice_race_a_person_answer_between_the_read_and_the_write_stays_last(proj, monkeypatch, capsys, decided):     # PK2-18
    _noticed_form(proj)
    real_roster = PK.roster

    def racing(root, cfg, stand):
        got = real_roster(root, cfg, stand)             # the stale read: the role is not there yet
        proj.record(state=decided)                      # a parallel story's answer lands before notice's own write
        return got

    monkeypatch.setattr(PK, "roster", racing)
    capsys.readouterr()
    assert PK.notice_from_handoff(proj.root, proj.task, "T-2") == []
    rows = proj.rows()
    assert [r["state"] for r in rows] == [decided] and PK.state(proj.root, PK.ROLES_KEY, "", "auditor")["row"]["state"] == decided
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("held", ["noticed_row", "no_rows", "no_file"])
def test_notice_writes_when_the_role_is_absent_or_only_noticed(proj, held):                  # PK2-18
    if held == "noticed_row":
        proj.facts([role_fact("PK-1", "auditor", PK.NOTICED, "2026-11-01T10:00:00+00:00")])
    elif held == "no_rows":
        proj.facts([])
    _noticed_form(proj)
    ids = PK.notice_from_handoff(proj.root, proj.task, "T-2")
    assert len(ids) == 1 and len(proj.rows()) == (2 if held == "noticed_row" else 1)       # the fixture row has another value: a new row
    assert proj.rows()[-1]["state"] == PK.NOTICED


@pytest.mark.parametrize("decided", DECIDED)
def test_record_guard_refuses_after_a_decided_state_and_an_unguarded_caller_writes(proj, decided):          # PK2-18
    proj.record(state=decided)
    before = proj.path().read_bytes()
    assert proj.record(state=PK.NOTICED, source="role", words="", only_if_latest=(PK.NOTICED,)) == (None, "", False)
    assert proj.path().read_bytes() == before
    row, problem, created = proj.record(state=PK.NOTICED, source="role", words="")           # no guard: as today
    assert problem == "" and created is True and row["state"] == PK.NOTICED
    assert proj.record(state=PK.NOTICED, source="role", words="", only_if_latest=(PK.NOTICED,))[2] is False   # latest noticed: guard passes, same row


def test_record_guard_on_an_unreadable_registry_is_todays_refusal(proj):                     # PK2-18
    proj.path().parent.mkdir(parents=True, exist_ok=True)
    proj.path().write_text("{broken", encoding="utf-8")
    row, problem, created = proj.record(state=PK.NOTICED, source="role", words="", only_if_latest=(PK.NOTICED,))
    assert row is None and created is False and "nothing was written over it" in problem


def _another_writer_before_the_lock(monkeypatch, act, nth=1):
    """Run `act` once, just before the `nth` lock entry: what a parallel writer does between a caller's old unlocked read and its write."""
    real, seen = PK.lock, []

    def racing(root, *a, **k):
        seen.append(1)
        if len(seen) == nth:
            act()
        return real(root, *a, **k)

    monkeypatch.setattr(PK, "lock", racing)


# (case, held row at start (None: no registry), --sign-in, another writer's sign_in, sign_in written) - PK2-20: the held row is read under the lock
ROLE_CASES = [
    ("held_account_then_another_writer_sets_none", {"sign_in": "account"}, None, "none", "none"),
    ("held_none_kept", {"sign_in": "none"}, None, None, "none"),
    ("outside_SIGN_INS_reads_account", {"sign_in": "kiosk"}, None, None, "account"),
    ("no_registry_reads_account", None, None, None, "account"),
    ("explicit_flag_wins_over_the_held_row", {"sign_in": "none"}, "account", None, "account"),
]


@pytest.mark.parametrize("case", ROLE_CASES, ids=[c[0] for c in ROLE_CASES])
def test_role_cli_carries_the_sign_in_held_under_the_lock(proj, monkeypatch, case):          # PK2-20
    _, held, flag, other, wrote = case
    if held is not None:
        proj.facts([role_fact("PK-1", "auditor", PK.KNOWN, "2026-11-01T10:00:00+00:00", value=held)])
    if other:
        _another_writer_before_the_lock(monkeypatch, lambda: proj.record(value={"sign_in": other}))
    argv = ["role", "--task", "T-1", "--role", "auditor", "--state", "known", "--words-file", str(proj.words)]
    assert run(argv + (["--sign-in", flag] if flag else [])) == 0
    assert proj.rows()[-1]["value"] == {"sign_in": wrote}


@pytest.mark.parametrize("known_meanwhile", [False, True])
def test_account_cli_writes_no_second_role_row_for_a_role_that_became_known(proj, monkeypatch, known_meanwhile):          # PK2-20
    if known_meanwhile:      # the 1st lock entry is the account row's own, the 2nd the role row's
        _another_writer_before_the_lock(monkeypatch, lambda: proj.record(value={"sign_in": "none"}), nth=2)
    assert run(["account", *STAND_ARGS, "--words-file", str(proj.words)]) == 0
    roles = [r for r in proj.rows() if r["key"] == PK.ROLES_KEY]
    assert len(roles) == 1 and roles[0]["value"] == ({"sign_in": "none"} if known_meanwhile else {"sign_in": "account"})


# FV1-28 C1: the data join producer `first_look.put` (`sign_in`) -> `first_look.record_sign_in` -> registry row -> reader `sign_in`.
# (case id, what the walk's dispatch is for the controller, the rows' `blocked_by`, the story's pipeline extras, rows in the registry, text of the line)
SIGN_IN_CASES = [
    ("accepted_with_way", "accepted", None, {}, 1, "recorded the way in to `dev` (ui) as PK-1 for later stories"),
    ("all_rows_access", "accepted", "access", {}, 0, "every requirement of the record was blocked by access"),
    ("no_trace", "accepted", None, {"no_trace": True}, 0, "this run leaves no trace (an experiment)"),
    ("not_accepted", "running", None, {}, 0, "the first look of these heads was not accepted"),
    ("duplicate", "accepted", None, {}, 1, "already recorded as PK-1"),
]


@pytest.mark.parametrize("case", SIGN_IN_CASES, ids=[c[0] for c in SIGN_IN_CASES])
def test_sign_in_record_join(tmp_path, monkeypatch, case):
    name, status, blocked, extra, held, text = case
    import first_look as FL
    import test_first_look as TFL
    monkeypatch.setattr(FL, "_account_secrets", lambda *args: ([], []))          # the secret guard is A1's own row
    proj = Proj(tmp_path, monkeypatch)
    story = TFL.Story(proj.root / "qa-factory" / "artifacts")
    caps = story.ready()
    rows = story.rows(caps)
    if blocked:
        rows = [dict(r, status="unreachable", blocked_by=blocked) for r in rows]
    assert story.put(rows, sign_in=TFL._good_ui(caps))["written"]                  # the producer: A1's `put`
    if extra:
        story.set_pipeline(dict(TFL.PIPELINE, **extra))
    state = {"dispatches": {TFL.WALK: {"status": status}}}
    done = FL.record_sign_in(story.task, by="conductor", controller_state=state)
    if name == "duplicate":
        assert FL.record_sign_in(story.task, by="conductor", controller_state=state)["recorded"] is True
        done = FL.record_sign_in(story.task, by="driver", controller_state=state)
    assert text in done["line"], done["line"]
    assert len(proj.rows()) if held else not proj.path().exists()
    ways = PK.sign_in(proj.root, "dev")
    assert not ways["problem"] and len(ways["ways"]) == held and ways["precedence"] == PK.SIGN_IN_PRECEDENCE
    if held:
        way = ways["ways"][0]
        assert way["surface"] == "ui" and way["id"] == "PK-1" and way["story"] == "QA-1" and len(proj.rows()) == 1
        assert way["value"]["url"] == "/login" and not set(way["value"]) & set(PK.SIGN_IN_NOT_KEPT)     # the reader's value is what the walker found
        assert proj.rows()[0]["provenance"]["source"] == "role" and "Signed in through the page" in proj.rows()[0]["provenance"]["words"]


# --- C3-j1 (t-1132): the stand's page load, measured by the factory (AR-3, AR-13, AR-14, AR-25; P8) --------------------------------

import datetime as _dt  # noqa: E402

import stand_identity as _SI  # noqa: E402

PL_STAND = {"name": "dev", "base_url": "http://localhost:8080", "frontend_url": "http://localhost:5173/start?x=1"}


def _iso_ago(days):
    return (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=days)).isoformat(timespec="seconds")


def pl_value(stand=PL_STAND, **over):
    value = {"load_s": 70.0, "at_least": False, "address": "http://localhost:5173/start", "definition_sha": _SI.definition_sha(stand),
             "at": _iso_ago(0)}
    value.update(over)
    return value


def pl_record(proj, value=None, **over):
    args = dict(key=PK.PAGE_LOAD_KEY, environment="dev", element=PK.PAGE_LOAD_ELEMENT, state="known", scope="stand",
                value=pl_value() if value is None else value, words=PK.HOW_PAGE_LOAD, source="measured", story="T-1", by="gate")
    args.update(over)
    return PK.record(proj.root, **args)


def _pl_proj(tmp_path, monkeypatch, **stand_over):
    return Proj(tmp_path, monkeypatch, stands=[dict(PL_STAND, **stand_over)])


@pytest.mark.parametrize("label, over, element, fault", [
    ("valid", {}, "frontend", ""),
    ("element ui", {}, "ui", "the element of environments.page_load"),
    ("load_s zero", {"load_s": 0}, "frontend", "load_s"),
    ("load_s negative", {"load_s": -1}, "frontend", "load_s"),
    ("load_s a bool", {"load_s": True}, "frontend", "load_s"),
    ("load_s NaN", {"load_s": float("nan")}, "frontend", "load_s"),
    ("load_s a string", {"load_s": "12"}, "frontend", "load_s"),
    ("extra key", {"note": "x"}, "frontend", "carries exactly"),
    ("address with user:pw", {"address": "http://user:pw@host/"}, "frontend", "user name or password"),
    ("address not http", {"address": "ftp://host/"}, "frontend", "http or https"),
    ("missing at", {"at": None}, "frontend", "carries exactly"),
    ("at not a moment", {"at": "yesterday"}, "frontend", "value.at"),
    ("at_least not a bool", {"at_least": "no"}, "frontend", "at_least"),
    ("empty definition_sha", {"definition_sha": ""}, "frontend", "definition_sha"),
], ids=lambda x: x if isinstance(x, str) and " " not in x else None)
def test_page_load_record_shape(label, over, element, fault):
    value = pl_value(**{k: v for k, v in over.items() if v is not None})
    for key, v in over.items():
        if v is None:
            del value[key]
    problems = PK.record_problems(PK.PAGE_LOAD_KEY, "dev", element, "known", "stand", PK.HOW_PAGE_LOAD, "measured", "gate", value=value)
    if fault:
        assert problems and any(fault in p for p in problems) and all(p.endswith("nothing was recorded") for p in problems), problems
    else:
        assert problems == []
    assert not any("user:pw" in p for p in problems)           # no refusal echoes the address


def test_page_load_state_table(tmp_path, monkeypatch):
    proj = _pl_proj(tmp_path, monkeypatch)
    assert PK.page_load(proj.root, None, "dev")["state"] == "none"                                      # absent file
    row, problem, created = pl_record(proj)
    assert (problem, created) == ("", True) and row["provenance"]["source"] == "measured" and row["provenance"]["by"] == "gate"
    got = PK.page_load(proj.root, None, "dev")                                                        # a recorded row reads back
    assert (got["state"], got["load_s"], got["at_least"], got["address"]) == ("measured", 70.0, False, "http://localhost:5173/start")
    assert PK.page_load(proj.root, None, "")["state"] == "none" and PK.page_load(proj.root, None, PK.PLACEHOLDER_STAND)["why"] == "no stand"
    assert PK.page_load(proj.root, None, "other")["state"] == "none"                                   # another stand has no row
    proj.stands[0] = dict(PL_STAND, base_url="http://localhost:9999")                                  # another definition
    proj.write_config()
    got = PK.page_load(proj.root, None, "dev")
    assert (got["state"], got["why"]) == ("none", "another stand definition")
    other = dict(PL_STAND, frontend_url="http://localhost:6000/")                                      # the definition fits, the address does not
    pl_record(proj, value=pl_value(stand=other))
    proj.stands[0] = other
    proj.write_config()
    got = PK.page_load(proj.root, None, "dev")
    assert (got["state"], got["why"]) == ("none", "another address")


def pl_reason(stand=PL_STAND, failed=None, **over):
    kept = {"cause": "unreachable", "why": "connection refused", "at": _iso_ago(0), "attempts": 1}
    kept.update(failed or {})
    value = {"failed": kept, "address": "http://localhost:5173/start", "definition_sha": _SI.definition_sha(stand)}
    value.update(over)
    return value


@pytest.mark.parametrize("label, failed, over, fault", [
    ("valid", {}, {}, ""),
    ("cause not closed", {"cause": "slow"}, {}, "failed.cause"),
    ("no_browser is the machine's fact and never kept (AR-4)", {"cause": "no_browser"}, {}, "failed.cause"),
], ids=lambda x: x if isinstance(x, str) and " " not in x else None)
def test_page_load_kept_reason_shape(label, failed, over, fault):
    value = pl_reason(failed=failed or {}, **{k: v for k, v in over.items() if v is not None and k != "failed"})
    for key, v in over.items():
        if v is None:
            del value[key]
    if "failed" in over:
        value["failed"] = over["failed"]
    problems = PK.record_problems(PK.PAGE_LOAD_KEY, "dev", "frontend", "known", "stand", PK.HOW_PAGE_LOAD, "measured", "gate", value=value)
    if fault:
        assert problems and any(fault in p for p in problems) and all(p.endswith("nothing was recorded") for p in problems), problems
    else:
        assert problems == []
    assert not any("user:pw" in p for p in problems)


def test_page_load_a_reason_has_no_age_and_a_number_appends(tmp_path, monkeypatch):
    proj = _pl_proj(tmp_path, monkeypatch)
    pl_record(proj, value=pl_reason(failed={"at": _iso_ago(8)}))
    assert PK.page_load(proj.root, None, "dev")["state"] == "failed"     # a reason keeps no age
    pl_record(proj)
    pl_record(proj, value=pl_value(load_s=75.0))
    assert len(PK.load(proj.root)[0]) == 2                               # a number is not replaced in place


def test_page_load_a_broken_kept_reason_in_the_file_is_read_as_broken_never_as_a_pass(tmp_path, monkeypatch):
    for label, broken in (("attempts 0", {"attempts": 0}), ("attempts negative", {"attempts": -3}), ("attempts a string", {"attempts": "1"}),
                          ("cause unknown", {"cause": "slow"}), ("a no_browser row an earlier version kept", {"cause": "no_browser"}), ("a field missing", {"attempts": None})):
        (tmp_path / label.replace(" ", "_")).mkdir()
        proj = _pl_proj(tmp_path / label.replace(" ", "_"), monkeypatch)
        row = pl_record(proj, value=pl_reason())[0]
        data = json.loads(proj.path().read_text(encoding="utf-8"))
        failed = data["facts"][0]["value"]["failed"]
        for key, v in broken.items():
            if v is None:
                del failed[key]
            else:
                failed[key] = v
        proj.path().write_text(json.dumps(data), encoding="utf-8")
        got = PK.page_load(proj.root, None, "dev")
        assert (got["state"], got["why"], got["failed"], got["load_s"]) == ("none", "malformed", None, None), label
    assert row


@pytest.mark.parametrize("days, expected", [(6, "measured"), (8, "none")], ids=["six_days", "eight_days"])
def test_page_load_age_is_seven_days(tmp_path, monkeypatch, days, expected):
    proj = _pl_proj(tmp_path, monkeypatch)
    assert pl_record(proj, value=pl_value(at=_iso_ago(days)))[1] == ""
    assert PK.page_load(proj.root, None, "dev")["state"] == expected


def test_page_load_older_than_the_stands_verification_is_none(tmp_path, monkeypatch):
    proj = _pl_proj(tmp_path, monkeypatch, verified=_iso_ago(0)[:10])
    stand = dict(PL_STAND, verified=_iso_ago(0)[:10])
    pl_record(proj, value=pl_value(stand=stand, at=_iso_ago(3)))
    got = PK.page_load(proj.root, None, "dev")
    assert got["state"] == "none" and "may describe another build" in got["why"]


def test_page_load_revoked_unreadable_and_no_trace_and_a_non_ascii_stand(tmp_path, monkeypatch):
    proj = _pl_proj(tmp_path, monkeypatch)
    row = pl_record(proj)[0]
    assert PK.revoke(proj.root, row["id"], "wrong number")[1] == "" and PK.page_load(proj.root, None, "dev")["state"] == "none"   # AR-25
    proj.path().write_text("{not json", encoding="utf-8")
    got = PK.page_load(proj.root, None, "dev")
    assert got["state"] == "unreadable" and got["why"] and got["load_s"] is None                      # an unknown, never a number
    (tmp_path / "b").mkdir()
    plain = Proj(tmp_path / "b", monkeypatch, stands=[dict(PL_STAND, name="stand \u0430")], pipeline={"ticket": "T-1", "no_trace": True})
    row, problem, created = pl_record(plain, environment="stand \u0430", task_root=plain.task)
    assert row is None and problem == PK.NO_TRACE_WORDS and not plain.path().exists()                  # P8: an experiment writes nothing
    assert PK.page_load(plain.root, None, "stand \u0430")["state"] == "none"
    (tmp_path / "c").mkdir()
    keep = Proj(tmp_path / "c", monkeypatch, stands=[dict(PL_STAND, name="stand \u0430")])
    assert pl_record(keep, environment="stand \u0430")[1] == "" and PK.page_load(keep.root, None, "stand \u0430")["state"] == "measured"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))


# --- E7-1: the answer about another instance of the stand or device ------------------------------------------------------------

def instance_args(*extra):
    return ["instance", "--task", "T-1", "--allowed", "yes", "--stand", "dev", *extra]


def test_instance_answer_round_trip_the_none_family_and_value_shapes(proj, tmp_path, capsys):
    ask = lambda stand="dev", need="another_instance": PK.instance_answer(proj.root, stand, need)       # noqa: E731
    assert ask() == {"authorized": None, "row": None, "problem": "", "no_stand": False}             # absent file: asks, no problem
    for stand in ("", PK.PLACEHOLDER_STAND):
        assert ask(stand)["no_stand"] is True and ask(stand)["authorized"] is None
    assert run(instance_args("--words-file", str(proj.words))) == 0
    assert "another_instance on dev: environments.extra_instance recorded (PK-1)" in capsys.readouterr().out
    assert ask()["authorized"] is True and ask()["row"]["provenance"]["words"] == WORDS.strip()
    assert run(instance_args("--words-file", str(proj.words))) == 0 and "already recorded (PK-1)" in capsys.readouterr().out
    assert run(["instance", "--task", "T-1", "--allowed", "no", "--stand", "dev", "--words-file", str(proj.words)]) == 0
    assert ask()["authorized"] is False and len(proj.rows()) == 2                                   # the other answer is a new row and wins
    assert ask("dev ") ["authorized"] is None and ask("other")["authorized"] is None and ask(need="x")["authorized"] is None
    assert run(["revoke", "--task", "T-1", "--id", "PK-2", "--words-file", str(proj.words)]) == 0
    assert "asked again where it is needed" in capsys.readouterr().out and ask()["authorized"] is None   # F1 t-1311: revoked newest "no" asks again, never the older "yes"
    assert run(["revoke", "--task", "T-1", "--id", "PK-1", "--words-file", str(proj.words)]) == 0 and ask()["authorized"] is None
    for allowed in ("yes", "no"):
        assert run(["instance", "--task", "T-1", "--allowed", allowed, "--stand", "dev", "--words-file", str(proj.words)]) == 0
    assert run(["revoke", "--task", "T-1", "--id", "PK-3", "--words-file", str(proj.words)]) == 0 and ask()["authorized"] is False  # older revoked: newer stays
    proj.facts([fact("PK-8", PK.EXTRA_INSTANCE_KEY, "dev", "another_instance", "noticed_unconfirmed", "2026-11-01T10:00:00", scope="stand", value={"authorized": True})])
    assert ask()["authorized"] is None                                                                  # F4 t-1311: only `known` answers
    for value in ({"authorized": "yes"}, {"authorized": True, "x": 1}, None, {}, [True]):              # a typed yes/no only
        assert PK.record_problems(PK.EXTRA_INSTANCE_KEY, "dev", "another_instance", "known", "stand", "w", "person", "conductor", value=value)
        proj.facts([fact("PK-9", PK.EXTRA_INSTANCE_KEY, "dev", "another_instance", "known", "2026-11-01T10:00:00", scope="stand", value=value)])
        assert ask()["authorized"] is None
    assert PK.record_problems(PK.EXTRA_INSTANCE_KEY, "dev", "", "known", "stand", "w", "person", "conductor", value={"authorized": True})
    proj.path().write_text("{not json", encoding="utf-8")
    assert ask()["authorized"] is None and ask()["problem"]                                           # unread is never a "no"


INSTANCE_CLI = [   # (option overrides, None drops one; words bytes, pipeline, exit code, text of the refusal)
    ({}, b"yes" * 70_000, None, 0, ""),                      # 210 KB, no size limit: whole
    ({}, BOM + b"ok", None, 0, ""),                          # a BOM is stripped
    ({}, b"", None, 2, "words"), ({}, BOM, None, 2, "words"), ({}, b" \n\t", None, 2, "words"),
    ({}, "yes".encode("utf-16"), None, 2, "UTF-8"), ({}, bytes([0xC3, 0x28]), None, 2, "UTF-8"),
    ({"--stand": " "}, b"ok", None, 2, "stand"), ({"--stand": PK.PLACEHOLDER_STAND}, b"ok", None, 2, "pass --stand"),   # F3 t-1311
({"--stand": None}, b"ok", None, 2, "pass --stand"),
    ({"--need": "bogus"}, b"ok", None, "exit", ""), ({"--allowed": "YES"}, b"ok", None, "exit", ""), ({"--allowed": ""}, b"ok", None, "exit", ""),
    ({}, b"ok", {"ticket": "T-1", "no_trace": True}, 2, "leaves no trace"),
]


@pytest.mark.parametrize("opts,raw,pipeline,code,needle", INSTANCE_CLI)
def test_instance_cli_battery(tmp_path, monkeypatch, capsys, opts, raw, pipeline, code, needle):
    proj = Proj(tmp_path, monkeypatch, stands=[{"name": "dev"}, {"name": "prod"}], pipeline=pipeline)
    proj.words.write_bytes(raw)
    given = {"--allowed": "yes", "--stand": "dev", "--words-file": str(proj.words), **opts}
    argv = ["instance", "--task", "T-1"] + [x for k, v in given.items() if v is not None for x in (k, v)]
    if code == "exit":
        with pytest.raises(SystemExit):
            run(argv)
    else:
        assert run(argv) == code
    if code == 0:
        assert proj.rows()[0]["provenance"]["words"] == (raw[3:] if raw.startswith(BOM) else raw).decode().strip()
    else:
        assert needle in capsys.readouterr().err and not proj.path().exists()                          # nothing was written


# --- OF3-2 K1: an answer's life - heads, conflict, condition, markers, `fact`, `holds_none` (AR-13, AR-25, AR-28) ------------------

SEAM = "manual.accounts_way"


def row_of(id, key=PK.ROLES_KEY, element="auditor", state="known", day=1, links=None, **extra) -> dict:
    """A hand-written row of any key: `links` None is a LEGACY row (no `supersedes` key), a list is a phase-2 row."""
    scope = PK.KEYS[key]["scope"]
    row = fact(id, key, "dev" if scope == "stand" else "", element, state, f"2026-11-{day:02d}T10:00:00+00:00")
    row.update({"scope": scope, **extra})
    if links is not None:
        row["supersedes"] = links
    return row


def mark(id, day, story="T-1") -> dict:
    row = row_of(id, SEAM, "", "asked", day)
    row["provenance"] = {"source": "factory", "words": "", "story": story, "by": "driver", "where": ""}
    return row


FACT_CASES = [      # id, rows (a list, raw file text, or "damaged"), kwargs of `fact`, step, {row id, conflicts, condition, problem needle}
    ("registry_known_role", [row_of("PK-1")], {"key": PK.ROLES_KEY, "element": "auditor"}, "known", {"row": "PK-1"}),
    ("not_needed", [row_of("PK-1", SEAM, "", "not_needed")], {}, "not_needed", {"row": "PK-1"}),
    ("not_needed_with_condition_never_suppresses", [row_of("PK-1", SEAM, "", "not_needed", condition="only prod")], {}, "unknown",
     {"row": "PK-1", "condition": "only prod"}),
    ("marker_newer_than_conditional_not_needed", [row_of("PK-1", SEAM, "", "not_needed", condition="only prod"), mark("PK-2", 2)], {},
     "asked_before", {"row": "PK-1", "condition": "only prod"}),
    ("marker_older_than_not_needed", [mark("PK-1", 1), row_of("PK-2", SEAM, "", "not_needed", day=2)], {}, "not_needed", {"row": "PK-2"}),
    ("two_heads", [row_of("PK-1", SEAM, "", links=[]), row_of("PK-2", SEAM, "", "not_needed", links=[])], {}, "unknown",
     {"conflicts": ["PK-1", "PK-2"]}),
    ("self_link", [row_of("PK-1", SEAM, "", "not_needed", links=["PK-1"])], {}, "unknown", {"problem": "point at each other"}),
    ("noticed_head", [row_of("PK-1", SEAM, "", PK.NOTICED)], {}, "unknown", {"row": "PK-1"}),
    ("revoked_head", [row_of("PK-1", SEAM, "", "not_needed", revoked_at="2026-11-03T10:00:00+00:00")], {}, "unknown", {}),
    ("head_of_another_scope", [row_of("PK-1", SEAM, "", "not_needed", scope="stand")], {}, "unknown", {}),
    ("head_on_another_stand_case", [row_of("PK-1", PK.LESSONS_KEY, "x")], {"key": PK.LESSONS_KEY, "environment": "Dev", "element": "x"},
     "unknown", {}),
    ("registry_known_but_caller_says_no", [row_of("PK-1", SEAM, "")], {"known": False}, "unknown", {"row": "PK-1"}),
    ("config_known_by_caller", [], {"known": True}, "known", {}),
    ("config_known_keeps_the_condition", [row_of("PK-1", SEAM, "", condition="staging only")], {"known": True}, "known",
     {"condition": "staging only"}),
    ("config_value_read", [], {"cfg": {"manual": {"accounts_way": {"words": "x"}}}}, "known", {}),
    ("placeholder_but_caller_says_no", [], {"cfg": {"manual": {"accounts_way": "not known"}}, "known": False}, "unknown", {}),
    ("marker_of_this_story", [mark("PK-1", 1, "T-2")], {}, "asked_here", {}),
    ("marker_of_another_story", [mark("PK-1", 1, "T-1")], {}, "asked_before", {}),
    ("marker_with_empty_story", [mark("PK-1", 1, "")], {"story": ""}, "asked_before", {}),
    ("list_key_without_element", [], {"key": PK.LESSONS_KEY, "environment": "dev"}, "unknown", {"problem": "is a list"}),
    ("key_with_no_row", [], {"key": "no.such.key"}, "unknown", {"problem": "no catalogue row"}),
    ("unreadable_registry", "{not json", {}, "unknown", {"problem": "project-knowledge"}),
    ("other_schema", json.dumps({"schema_version": 2, "facts": []}), {}, "unknown", {"problem": "schema_version"}),
    ("damaged_catalogue", "damaged", {}, "unknown", {"problem": "damaged"}),
]


@pytest.mark.parametrize("rows, kw, step, extra", [pytest.param(*c[1:], id=c[0]) for c in FACT_CASES])
def test_fact_table(proj, monkeypatch, rows, kw, step, extra):
    if rows == "damaged":
        monkeypatch.setattr(CC, "config_keys", _raises())
    elif isinstance(rows, str):
        proj.path().parent.mkdir(parents=True, exist_ok=True)
        proj.path().write_text(rows, encoding="utf-8")
    elif rows:
        proj.facts(rows)
    got = PK.fact(proj.root, **{"key": SEAM, "story": "T-2", **kw})
    assert got["step"] == step, got
    assert (got["row"] or {}).get("id") == extra.get("row") and got["conflicts"] == extra.get("conflicts", [])
    assert got["condition"] == extra.get("condition", "") and extra.get("problem", "") in got["problem"]
    assert bool(got["problem"]) == bool(extra.get("problem")) and not (proj.root / Path(PK.LOCK_REL)).exists()      # pure


GONE = "2026-11-09T10:00:00+00:00"
HEAD_CASES = [      # id, where (key, stand, element), rows, state, {row id, conflicts, problem needle, asks}
    ("a_link", None, [row_of("PK-1", links=[]), row_of("PK-2", state="not_needed", day=2, links=["PK-1"])], "not_needed", {"row": "PK-2"}),
    ("stale_named_head_is_a_conflict", None, [row_of("PK-1", links=[]), row_of("PK-2", day=2, links=["PK-1"]), row_of("PK-3", day=3, links=["PK-1"])],
     "unknown", {"conflicts": ["PK-2", "PK-3"]}),
    ("revoke_the_head_of_a_role", None, [row_of("PK-1", links=[]), row_of("PK-2", day=2, links=["PK-1"], revoked_at=GONE)], "unknown", {}),
    ("revoke_the_head_of_a_side", (PK.SIDES_KEY, "", "UI"), [row_of("PK-1", PK.SIDES_KEY, "UI", links=[]),
     row_of("PK-2", PK.SIDES_KEY, "UI", day=2, links=["PK-1"], revoked_at=GONE)], "unknown", {}),
    ("revoke_the_head_of_a_lesson", (PK.LESSONS_KEY, "dev", "indexing"), [row_of("PK-1", PK.LESSONS_KEY, "indexing", links=[]),
     row_of("PK-2", PK.LESSONS_KEY, "indexing", day=2, links=["PK-1"], revoked_at=GONE)], "unknown", {}),
    ("revoke_during_a_conflict", None, [row_of("PK-1", links=[]), row_of("PK-2", state="not_needed", links=[], revoked_at=GONE)], "known", {"row": "PK-1"}),
    ("legacy_later_wins", None, [row_of("PK-1"), row_of("PK-2", state="not_needed", day=2)], "not_needed", {"row": "PK-2"}),
    ("legacy_after_a_phase_2_row", None, [row_of("PK-1", links=[]), row_of("PK-2", state="not_needed", day=2, links=["PK-1"]), row_of("PK-3", day=3)],
     "known", {"row": "PK-3"}),
    ("self_link", None, [row_of("PK-1", links=["PK-1"])], "unknown", {"problem": "point at each other"}),
    ("cycle", None, [row_of("PK-1", links=["PK-2"]), row_of("PK-2", day=2, links=["PK-1"])], "unknown", {"problem": "point at each other"}),
    ("a_marker_is_never_a_head", None, [row_of("PK-1", state="not_needed"), row_of("PK-2", state="asked", day=2)], "not_needed", {"row": "PK-1"}),
    ("instance_answer_after_a_revoke_asks", (PK.EXTRA_INSTANCE_KEY, "dev", "another_instance"),
     [row_of("PK-1", PK.EXTRA_INSTANCE_KEY, "another_instance", value={"authorized": True}),
      row_of("PK-2", PK.EXTRA_INSTANCE_KEY, "another_instance", day=2, value={"authorized": True}, revoked_at=GONE)], "unknown", {"asks": True}),
]


@pytest.mark.parametrize("where, rows, state, extra", [pytest.param(*c[1:], id=c[0]) for c in HEAD_CASES])
def test_heads_table(proj, where, rows, state, extra):
    key, env, element = where or (PK.ROLES_KEY, "", "auditor")
    proj.facts(rows)
    got = PK.state(proj.root, key, env, element)
    assert got["state"] == state and (got["row"] or {}).get("id") == extra.get("row") and got["conflicts"] == extra.get("conflicts", [])
    assert extra.get("problem", "") in got["problem"] and bool(got["problem"]) == bool(extra.get("problem")), got["problem"]
    listed = PK.subjects(proj.root, key, env)          # the lists agree with the reader: never a subject without an answer
    assert ((env, element) in listed["subjects"]) == (state != "unknown")
    assert bool(listed.get("conflicts")) == bool(got["conflicts"] or got["problem"])
    if extra.get("asks"):
        assert PK.instance_answer(proj.root, env, element)["authorized"] is None


CONFLICT = [row_of("PK-1", links=[]), row_of("PK-2", state="not_needed", day=2, links=[])]
SEAM_KW = dict(key=SEAM, element="", value=None, scope="project", words="the person said so")
MARK_KW = dict(SEAM_KW, key="manual.data_way", state="asked", source="factory", by="driver", words="", story="T-1")
PL_KW = dict(key=PK.PAGE_LOAD_KEY, environment="dev", element="frontend", scope="stand", words=PK.HOW_PAGE_LOAD, source="measured", by="gate")
OLD = [dict(), dict(state="not_needed", value=None)]       # two writes of one role: PK-1, then PK-2 superseding it
RECORD_CASES = [    # id, hand rows, earlier writes, the call, created, needle, rows after, check(proj, (row, problem, created), held)
    ("condition_is_stripped_and_carried", [], [], dict(condition="  only on staging \n"), True, "", 1,
     lambda p, r, h: all([r[0]["condition"] == "only on staging", p.state()["condition"] == "only on staging",
                          PK.value(p.root, PK.ROLES_KEY, "", None, "auditor")["condition"] == "only on staging",
                          PK.fact(p.root, PK.ROLES_KEY, "", "auditor")["condition"] == "only on staging",
                          PK.roster(p.root, p.cfg(), "dev")["elements"][0]["condition"] == "only on staging"])),
    ("condition_must_be_text", [], [], dict(condition=5), False, "condition", 0, None),
    ("same_answer_and_condition_is_idempotent", [], [dict(condition="x")], dict(condition="x"), False, "", 1, lambda p, r, h: r[0]["id"] == "PK-1"),
    ("another_condition_is_a_new_row", [], [dict(condition="x")], dict(condition="y"), True, "", 2, lambda p, r, h: r[0]["supersedes"] == ["PK-1"]),
    ("foreign_supersedes_id_refused", [], [], dict(supersedes=["PK-9"]), False, "PK-9 is not an answer about product.roles auditor", 0, None),
    ("own_would_be_id_refused", [], [], dict(supersedes=["PK-1"]), False, "PK-1 is not an answer", 0, None),
    ("another_subjects_id_refused", [], [dict(element="viewer")], dict(supersedes=["PK-1"]), False, "PK-1 is not an answer", 1, None),
    ("one_value_key_takes_the_empty_element", [], [], SEAM_KW, True, "", 1, lambda p, r, h: r[0]["element"] == "" and r[0]["supersedes"] == []),
    ("one_value_key_refuses_an_element", [], [], dict(SEAM_KW, element="a,b"), False, "takes no element", 0, lambda p, r, h: "role" not in r[1]),
    ("marker_for_a_first_need_key", [], [], MARK_KW, True, "", 1,
     lambda p, r, h: "supersedes" not in r[0] and "condition" not in r[0] and r[0]["provenance"]["source"] == "factory"),
    ("marker_refused_for_a_role_key", [], [], dict(state="asked", source="factory", by="driver", words=""), False, "asked", 0, None),
    ("marker_idempotent_per_story", [], [MARK_KW], MARK_KW, False, "", 1, lambda p, r, h: r[0]["id"] == "PK-1"),
    ("marker_of_another_story_is_a_new_row", [], [MARK_KW], dict(MARK_KW, story="T-2"), True, "", 2, None),
    ("marker_takes_no_guard", [], [], dict(MARK_KW, only_if_latest=(PK.NOTICED,)), False, "written unconditionally", 0, None),
    ("only_if_latest_in_a_conflict_writes_nothing", CONFLICT, [], dict(state=PK.NOTICED, source="role", by="driver", words="", only_if_latest=(PK.NOTICED,)),
     False, "", 2, lambda p, r, h: r[0] is None),
    ("from_held_gets_none_in_a_conflict", CONFLICT, [], dict(from_held=True), True, "", 3,
     lambda p, r, h: h == [None] and r[0]["supersedes"] == ["PK-1", "PK-2"] and p.state()["state"] == "known"),
    ("missing_supersedes_every_head", [], OLD, dict(), True, "", 3, lambda p, r, h: r[0]["supersedes"] == ["PK-2"]),
    ("a_stale_named_head_makes_a_conflict", [], OLD, dict(supersedes=["PK-1"]), True, "", 3, lambda p, r, h: p.state()["conflicts"] == ["PK-2", "PK-3"]),
    ("page_load_replace_keeps_id_and_links", [row_of("PK-1", PK.PAGE_LOAD_KEY, "frontend", links=[], value=pl_value()),
     row_of("PK-2", PK.PAGE_LOAD_KEY, "frontend", day=2, links=["PK-1"], value=pl_reason())], [], dict(PL_KW, value=pl_value()), True, "", 2,
     lambda p, r, h: r[0]["id"] == "PK-2" and r[0]["supersedes"] == ["PK-1"] and r[0]["condition"] == ""),
    ("page_load_replace_of_a_legacy_row_stays_legacy", [row_of("PK-1", PK.PAGE_LOAD_KEY, "frontend", value=pl_reason())], [], dict(PL_KW, value=pl_value()),
     True, "", 1, lambda p, r, h: r[0]["id"] == "PK-1" and "supersedes" not in r[0]),
]


@pytest.mark.parametrize("hand, pre, call, created, needle, nrows, check", [pytest.param(*c[1:], id=c[0]) for c in RECORD_CASES])
def test_record_table(proj, hand, pre, call, created, needle, nrows, check):
    if hand:
        proj.facts(hand)
    for item in pre:
        assert proj.record(**item)[0], item
    held = []
    if call.get("from_held"):
        call = dict(call, from_held=lambda row: (held.append(row) or ({"sign_in": "account"}, False)))
    res = proj.record(**call)
    assert res[2] is created and needle in res[1] and bool(res[1]) == bool(needle), res
    assert len(proj.rows() if proj.path().exists() else []) == nrows
    assert check is None or check(proj, res, held), res


@pytest.mark.parametrize("keys, expected", [(["manual.accounts_way"], True), (["manual.accounts_way", "manual.data_way", "manual.data_way.may"], True),
                                            (["manual.accounts_way", PK.ROLES_KEY], False), ([PK.ROLES_KEY], False), ([], False),
                                            (["no.such.key"], False), (["manual.accounts_way", 5], False)], ids=lambda v: str(v)[:30])
def test_holds_none(keys, expected):
    assert PK.holds_none(keys) is expected


def test_holds_none_asks_on_a_damaged_catalogue(monkeypatch):
    monkeypatch.setattr(CC, "config_keys", _raises())
    assert PK.holds_none(["manual.accounts_way"]) is False


def test_catalogue_seam_join():
    seam = [r for r in PK.rows() if r.get("ask_when") == "first_need"]
    assert [r["key"] for r in seam] == ["manual.accounts_way", "manual.data_way", "manual.data_way.may"]
    for r in seam:      # AR-22: every field a seam row carries has a reader, and the row is a key
        assert (r["scope"], r["compare"], r["value"], r["holds"]) == ("project", "exact", "one", "none") and r["needed_by"], r["key"]
        assert r["store"].startswith("config:") and r["key"] in PK.KEYS and r["key"] in PK.ONE_VALUE_KEYS
