# -*- coding: utf-8 -*-
"""Tests for tools/savings_report.py (the savings/trend calibration
check): counterfactual math, window splitting, the API-contour slice --
against a tmp database covering both schemas."""
import json
import sqlite3
import shutil
from pathlib import Path

import pytest

import savings_report
import usage_report
from savings_report import (
    api_contour_summary,
    counterfactual_summary,
    main,
    read_contour,
    top_tier_model,
    window_summary,
)
from usage_report import PricesError, load_prices

_TABLE = load_prices()
TOP = "claude-fable-5-1"  # the model the test config binds to roles.lead (the real delegation.config.yaml binds the same)
_LEAD_CONFIG = ("# comment\ncontour: subscription   # subscription | api-keys | both\n"
                "roles:\n  lead:\n    subscription:\n      model: {model}\n")


@pytest.fixture(autouse=True)
def _lead_binding(tmp_path, monkeypatch):
    """Every test reads a temp delegation.config.yaml binding roles.lead to TOP; a test that needs another
    binding (or none) rewrites the file or points CONFIG_PATH elsewhere."""
    path = tmp_path / "lead.config.yaml"
    path.write_text(_LEAD_CONFIG.format(model=TOP), encoding="utf-8")
    monkeypatch.setattr(savings_report, "CONFIG_PATH", path)
    return path


@pytest.fixture()
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "t.db")
    conn.execute(
        "CREATE TABLE cc_usage (ts TEXT, project TEXT, session_id TEXT,"
        " model TEXT, input_tokens INT, output_tokens INT,"
        " cache_creation_tokens INT, cache_read_tokens INT,"
        " accounted_cost_usd REAL, is_sidechain INT, agent_type TEXT)")
    conn.execute(
        "CREATE TABLE requests (ts TEXT, model TEXT, cost_usd REAL,"
        " traffic_kind TEXT)")
    return conn


def _cc(conn, ts, model, side, i=100, o=50, cw=0, cr=0, cost=1.0,
        agent=None, sess="s1"):
    conn.execute(
        "INSERT INTO cc_usage VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (ts, "p", sess, model, i, o, cw, cr, cost, side, agent))


def _as_top(db, binding, config_path):
    """The counterfactual of ONE sidechain turn (1000 in + 500 out + 400 cache-write + 10000 cache-read on a
    cheaper model), priced at `binding` through the config file."""
    config_path.write_text(_LEAD_CONFIG.format(model=binding), encoding="utf-8")
    _cc(db, "2026-07-09T10:00:00", "claude-sonnet-5", 1, i=1000, o=500, cw=400, cr=10000, cost=0.01, agent="scout")
    return counterfactual_summary(db, "ts >= ?", ("2026-07-08",))["as_fable"]


def test_the_counterfactual_prices_at_the_lead_binding_with_its_own_cache_multiplier(db, _lead_binding):
    # F-2 control values by hand. Fable 5.1 reads at 0.025x: 1000*1e-05 + 500*5e-05 + 400*1e-05*1.25 + 10000*1e-05*0.025
    #   = 0.01 + 0.025 + 0.005 + 0.0025 = 0.0425
    assert _as_top(db, "claude-fable-5-1", config_path=_lead_binding) == pytest.approx(0.0425, rel=1e-9)
    # the SAME turn priced at claude-fable-5 (the file's 0.1x read) is dearer: 0.01 + 0.025 + 0.005 + 0.01 = 0.05
    db.execute("DELETE FROM cc_usage")
    assert _as_top(db, "claude-fable-5", config_path=_lead_binding) == pytest.approx(0.05, rel=1e-9)


def test_the_counterfactual_math_matches_the_one_cost_function(db, _lead_binding):
    fp = _TABLE["models"][TOP]
    expected = (1000 * fp.input + 500 * fp.output + 400 * fp.input * fp.cache_write_multiplier
                + 10000 * fp.input * fp.cache_read_multiplier)
    assert _as_top(db, TOP, config_path=_lead_binding) == pytest.approx(expected)
    assert usage_report.accounted_cost(TOP, 1000, 500, 400, 10000)[0] == pytest.approx(expected)


def test_no_model_id_of_a_tier_is_written_in_the_tool():
    # the counterfactual model comes from the Lead binding; a literal id in the tool goes stale with the next model
    source = Path(savings_report.__file__).read_text(encoding="utf-8")
    assert "claude-fable" not in source


def test_a_binding_the_price_file_does_not_know_is_unpriced_never_zero(db, _lead_binding):
    _as_top(db, "claude-fable-9", config_path=_lead_binding)
    c = counterfactual_summary(db, "ts >= ?", ("2026-07-08",))
    assert len(c["detail"]) == 1 and c["detail"][0]["as_fable"] is None and c["gross_savings"] is None
    assert c["unpriced_models"] == ["claude-fable-9"] and c["counterfactual_partial"] is True


@pytest.mark.parametrize("text", ["contour: subscription\n", "roles: {}\n", "roles:\n  lead:\n    subscription:\n      model:\n",
                                  "not: yaml: [broken\n"], ids=["no-roles", "empty-roles", "empty-model", "broken-yaml"])
def test_an_unresolvable_binding_is_a_prices_error_naming_the_config_never_a_default(db, _lead_binding, text):
    _lead_binding.write_text(text, encoding="utf-8")
    with pytest.raises(PricesError, match="roles.lead names no model") as e:
        top_tier_model()
    assert str(_lead_binding) in str(e.value)
    with pytest.raises(PricesError):
        counterfactual_summary(db, "ts >= ?", ("2026-07-08",))


def test_a_missing_config_is_a_prices_error_and_exit_2_before_the_first_report_line(tmp_path, capsys, monkeypatch):
    path = _make_db(tmp_path / "t.db")
    monkeypatch.setattr(savings_report, "CONFIG_PATH", tmp_path / "absent.yaml")
    assert main(["--db", str(path)] + _ARGS) == 2
    out, err = capsys.readouterr()
    assert out == "" and err.startswith("savings_report: delegation config ") and "cannot be read" in err
    assert len(err.splitlines()) == 1


def test_window_split_pre_vs_routed(db):
    _cc(db, "2026-07-05T10:00:00", "claude-sonnet-5", 0, cost=2.0)
    _cc(db, "2026-07-09T10:00:00", "claude-fable-5", 0, cost=5.0)
    pre = window_summary(db, "ts < ?", ("2026-07-08",))
    routed = window_summary(db, "ts >= ?", ("2026-07-08",))
    assert pre["total_cost"] == pytest.approx(2.0)
    assert routed["total_cost"] == pytest.approx(5.0)
    assert pre["days"] == 1 and routed["days"] == 1


def test_counterfactual_only_sidechains_in_window(db):
    # a sidechain inside the window counts; main and a pre-window sidechain don't
    _cc(db, "2026-07-09T10:00:00", "claude-haiku-4-5-20251001", 1,
        i=1000, o=100, cost=0.002, agent="scout")
    _cc(db, "2026-07-09T11:00:00", "claude-fable-5", 0, cost=9.0)
    _cc(db, "2026-07-01T10:00:00", "claude-sonnet-5", 1, cost=1.0, agent="builder")
    c = counterfactual_summary(db, "ts >= ?", ("2026-07-08",))
    assert len(c["detail"]) == 1
    assert c["detail"][0]["agent_type"] == "scout"
    assert c["actual"] == pytest.approx(0.002)
    assert c["as_fable"] == pytest.approx(0.015)  # by hand at fable 5.1: 1000*1e-05 + 100*5e-05
    assert c["gross_savings"] == pytest.approx(c["as_fable"] - 0.002)


def test_api_contour_summary_groups_by_kind(db):
    db.execute("INSERT INTO requests VALUES ('2026-07-09','judge-groq',0.01,'judge')")
    db.execute("INSERT INTO requests VALUES ('2026-07-09','lead-sonnet',0.02,'synthetic')")
    db.execute("INSERT INTO requests VALUES ('2026-07-10','lead-sonnet',0.03,'synthetic')")
    a = api_contour_summary(db)
    assert a["total_n"] == 3
    assert a["total_cost"] == pytest.approx(0.06)
    kinds = {k: (n, c) for k, n, c in a["kinds"]}
    assert kinds["synthetic"][0] == 2


# --- F6-5: no usage database -> ONE n/a line, exit 0 (FR-41); a bad price file -> exit 2, no traceback ---

_ARGS = ["--routed-start", "2026-10-07", "--until", "2026-10-16"]


@pytest.fixture()
def config(tmp_path, monkeypatch):
    """A temp delegation.config.yaml carrying `contour: subscription` and the lead binding, wired in as the tool's config."""
    path = tmp_path / "delegation.config.yaml"
    path.write_text(_LEAD_CONFIG.format(model=TOP), encoding="utf-8")
    monkeypatch.setattr(savings_report, "CONFIG_PATH", path)
    return path


def _make_db(path, tables=("cc_usage", "requests")):
    conn = sqlite3.connect(path)
    if "cc_usage" in tables:
        conn.execute(
            "CREATE TABLE cc_usage (ts TEXT, project TEXT, session_id TEXT,"
            " model TEXT, input_tokens INT, output_tokens INT,"
            " cache_creation_tokens INT, cache_read_tokens INT,"
            " accounted_cost_usd REAL, is_sidechain INT, agent_type TEXT)")
    if "requests" in tables:
        conn.execute("CREATE TABLE requests (ts TEXT, model TEXT, cost_usd REAL, traffic_kind TEXT)")
    conn.commit()
    conn.close()
    return path


def _na(capsys, db_path, contour="subscription", reason=""):
    out, err = capsys.readouterr()
    extra = f"; reason: {reason}" if reason else ""
    assert out == (f"savings report: n/a — no usage database for check 18"
                   f" (contour {contour}; source: {db_path}{extra})\n")
    assert err == ""


def test_no_database_file_prints_the_na_line_and_creates_nothing(tmp_path, capsys, config):
    missing = tmp_path / "nowhere" / "requests.db"
    assert main(["--db", str(missing)] + _ARGS) == 0
    _na(capsys, missing)
    assert not missing.exists() and not missing.parent.exists()
    here = tmp_path / "requests.db"
    assert main(["--db", str(here)] + _ARGS) == 0
    _na(capsys, here)
    assert not here.exists()  # the probe is read-only: sqlite3.connect alone would have created the file


def test_database_with_neither_table_prints_the_na_line(tmp_path, capsys, config):
    path = tmp_path / "t.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE other (x INT)")  # a real sqlite file, just not the report's tables
    conn.commit()
    conn.close()
    assert main(["--db", str(path)] + _ARGS) == 0
    _na(capsys, path)


def test_cc_usage_only_prints_the_subscription_sections_and_marks_the_api_one(tmp_path, capsys, config):
    path = _make_db(tmp_path / "t.db", tables=("cc_usage",))
    conn = sqlite3.connect(path)
    _cc(conn, "2026-10-09T10:00:00", "claude-sonnet-5", 1, i=1000, o=100, cost=0.5, agent="builder")
    conn.commit()
    conn.close()
    assert main(["--db", str(path)] + _ARGS) == 0
    out, err = capsys.readouterr()
    assert err == "" and "savings report: n/a" not in out
    assert "claude-sonnet-5" in out and "TOTAL: 1 turns, $0.50, 1 days" in out
    assert "builder" in out and "gross savings=" in out  # the counterfactual is measured
    assert out.count("not measured") == 1
    assert ("===== API CONTOUR (requests.db, full history) =====\n"
            "  not measured (no `requests` table)\n") in out
    assert ("Sections measured: subscription windows + counterfactual (cc_usage)."
            " Not measured (table absent): requests.") in out


def test_requests_only_prints_the_api_section_and_marks_the_subscription_ones(tmp_path, capsys, config):
    path = _make_db(tmp_path / "t.db", tables=("requests",))
    conn = sqlite3.connect(path)
    conn.execute("INSERT INTO requests VALUES ('2026-10-09','judge-groq',0.01,'judge')")
    conn.commit()
    conn.close()
    assert main(["--db", str(path)] + _ARGS) == 0
    out, err = capsys.readouterr()
    assert err == "" and "savings report: n/a" not in out
    assert out.count("not measured (no `cc_usage` table)") == 3  # PRE, ROUTED, COUNTERFACTUAL
    assert "TOTAL: 1 requests, $0.0100 accounted" in out
    assert "Sections measured: API contour (requests). Not measured (table absent): cc_usage." in out


def test_requests_only_does_not_need_the_price_file(tmp_path, capsys, config, monkeypatch):
    path = _make_db(tmp_path / "t.db", tables=("requests",))
    _use_prices(monkeypatch, tmp_path / "missing_prices.json")
    assert main(["--db", str(path)] + _ARGS) == 0  # nothing is priced without cc_usage
    assert "TOTAL: 0 requests" in capsys.readouterr().out


def test_both_tables_measured_line_names_both(tmp_path, capsys, config):
    path = _make_db(tmp_path / "t.db")
    assert main(["--db", str(path)] + _ARGS) == 0
    out = capsys.readouterr().out
    assert "not measured" not in out
    assert "Sections measured: subscription windows + counterfactual (cc_usage); API contour (requests).\n" in out


def test_empty_database_file_prints_the_na_line(tmp_path, capsys, config):
    path = tmp_path / "t.db"
    path.write_bytes(b"")
    assert main(["--db", str(path)] + _ARGS) == 0
    _na(capsys, path)


def test_not_a_sqlite_file_prints_the_na_line_with_the_reason(tmp_path, capsys, config):
    path = tmp_path / "t.db"
    path.write_text("this is not a database " * 40, encoding="utf-8")
    assert main(["--db", str(path)] + _ARGS) == 0
    _na(capsys, path, reason="unreadable")


def test_both_tables_empty_is_the_report_with_zeros_not_na(tmp_path, capsys, config):
    path = _make_db(tmp_path / "t.db")
    assert main(["--db", str(path)] + _ARGS) == 0
    out, err = capsys.readouterr()
    assert "n/a" not in out and err == ""
    assert "TOTAL: 0 turns, $0.00, 0 days, $0.00/day" in out
    assert "TOTAL: 0 requests, $0.0000 accounted" in out


def test_database_with_data_prints_the_report(tmp_path, capsys, config):
    path = _make_db(tmp_path / "t.db")
    conn = sqlite3.connect(path)
    _cc(conn, "2026-10-09T10:00:00", "claude-sonnet-5", 1, i=1000, o=100, cost=0.5, agent="builder")
    conn.commit()
    conn.close()
    assert main(["--db", str(path)] + _ARGS) == 0
    out, err = capsys.readouterr()
    assert "===== ROUTED (>= 2026-10-07 .. 2026-10-16) =====" in out
    assert "claude-sonnet-5" in out and "n/a" not in out and err == ""


def test_the_contour_word_comes_from_the_config(tmp_path, capsys, config):
    assert read_contour(config) == "subscription"
    config.write_text("contour: api-keys\n", encoding="utf-8")
    assert main(["--db", str(tmp_path / "none.db")] + _ARGS) == 0
    assert "(contour api-keys; source:" in capsys.readouterr().out


def test_no_config_or_no_contour_line_is_unknown(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(savings_report, "CONFIG_PATH", tmp_path / "absent.yaml")
    assert read_contour() == "unknown"
    assert main(["--db", str(tmp_path / "none.db")] + _ARGS) == 0
    assert "(contour unknown; source:" in capsys.readouterr().out
    (tmp_path / "absent.yaml").write_text("roles:\n  contour: nested\n", encoding="utf-8")
    assert read_contour() == "unknown"  # only the top-level key counts


@pytest.mark.parametrize("flag, value", [("--routed-start", "yesterday"), ("--until", "2026-13-40"),
                                         ("--routed-start", "2026-10-7")])
def test_a_bad_date_is_an_argument_error_before_the_probe(tmp_path, capsys, config, flag, value):
    args = ["--db", str(tmp_path / "none.db"), "--routed-start", "2026-10-07", "--until", "2026-10-16"]
    args[args.index(flag) + 1] = value
    with pytest.raises(SystemExit) as e:
        main(args)
    assert e.value.code == 2
    out, err = capsys.readouterr()
    assert out == "" and "YYYY-MM-DD" in err


def _use_prices(monkeypatch, path):
    monkeypatch.setattr(usage_report, "PRICES_FILE", path)
    monkeypatch.setattr(usage_report, "_DEFAULT_PRICES", None)  # the memo is restored with the test


def test_a_corrupted_price_file_is_exit_2_one_stderr_line_no_traceback(tmp_path, capsys, config, monkeypatch):
    path = _make_db(tmp_path / "t.db")
    good = tmp_path / "prices.json"
    shutil.copy(usage_report.PRICES_FILE, good)
    _use_prices(monkeypatch, good)
    assert main(["--db", str(path)] + _ARGS) == 0  # control: the intact copy reports
    assert "COUNTERFACTUAL" in capsys.readouterr().out
    bad = tmp_path / "bad_prices.json"
    bad.write_text(good.read_text(encoding="utf-8")[:60], encoding="utf-8")  # cut mid-object
    _use_prices(monkeypatch, bad)
    assert main(["--db", str(path)] + _ARGS) == 2
    out, err = capsys.readouterr()
    assert out == ""  # no half-printed report before the failure
    assert err.startswith("savings_report: price file ") and str(bad) in err
    assert len(err.splitlines()) == 1 and "Traceback" not in err
    _use_prices(monkeypatch, tmp_path / "missing_prices.json")
    assert main(["--db", str(path)] + _ARGS) == 2
    assert "cannot be read" in capsys.readouterr().err


# --- F6-21: turns of a model with no price are never a $0 actual: the savings are "not measurable" (FR-41, FR-25) ---

_NULL_MODEL = "claude-sonnet-5-5"  # left out of the temp price files of _prices_to (priced in the real file since F6-24)
_ROUTED_TS = "2026-10-09T10:00:00"
_PRE_TS = "2026-10-01T10:00:00"


def _prices_to(tmp_path, monkeypatch, models):
    """A temp price file holding `models` ({id: (input, output)}, None = unpriced) plus the top-tier model priced
    unless the caller lists it, wired in as the tool's prices."""
    rows = {m: {"input": p[0], "output": p[1]} for m, p in models.items()}
    rows.setdefault(TOP, {"input": 1e-05, "output": 5e-05})
    path = tmp_path / "prices_f621.json"
    path.write_text(json.dumps({"as_of": "2026-10-16", "unit": "usd_per_token", "cache_write_multiplier": 1.25,
                                "cache_write_1h_multiplier": 2, "cache_read_multiplier": 0.1, "models": rows}),
                    encoding="utf-8")
    _use_prices(monkeypatch, path)


def _db_with(path, rows):
    """A both-tables database holding `rows`: (ts, model, is_sidechain, stored cost or None, tokens in/out)."""
    _make_db(path)
    conn = sqlite3.connect(path)
    for ts, model, side, cost, tokens in rows:
        _cc(conn, ts, model, side, i=tokens, o=tokens, cost=cost, agent="builder" if side else None)
    conn.commit()
    conn.close()
    return path


def _totals(out):
    """The TOTAL lines in report order: PRE, ROUTED, counterfactual, API."""
    return [line for line in out.splitlines() if line.startswith("  TOTAL:")]


def _run_report(path, capsys):
    assert main(["--db", str(path)] + _ARGS) == 0
    out, err = capsys.readouterr()
    assert err == ""
    return out


def test_unpriced_actuals_make_the_savings_not_measurable_never_100_percent(tmp_path, capsys, config, monkeypatch):
    _prices_to(tmp_path, monkeypatch, {})
    path = _db_with(tmp_path / "t.db", [(_ROUTED_TS, _NULL_MODEL, 1, None, 1000)] * 3
                    + [(_ROUTED_TS, "claude-sonnet-5", 1, 0.01, 1000)])
    out = _run_report(path, capsys)
    assert "gross savings: not measurable (partial: 3 turn(s) without a price — claude-sonnet-5-5)" in out
    assert "100%" not in out and "gross savings=" not in out
    cf_line = _totals(out)[2]
    assert "actual=$0.01 (actual partial)" in cf_line and "as-top-tier=$" in cf_line  # both totals still print
    assert "(counterfactual partial)" not in cf_line


def test_the_same_database_fully_priced_prints_the_percent_as_before(tmp_path, capsys, config, monkeypatch):
    # the NEGATIVE control: the very rows of the test above, the model now priced and its turns costed
    _prices_to(tmp_path, monkeypatch, {_NULL_MODEL: (3e-06, 1.5e-05)})
    path = _db_with(tmp_path / "t.db", [(_ROUTED_TS, _NULL_MODEL, 1, 0.01, 1000)] * 3
                    + [(_ROUTED_TS, "claude-sonnet-5", 1, 0.01, 1000)])
    out = _run_report(path, capsys)
    cf_line = _totals(out)[2]
    fable = (1000 * 1e-05 + 1000 * 5e-05) * 4  # by hand at the top tier: 0.06 a turn
    assert cf_line == (f"  TOTAL: actual=$0.04  as-top-tier=${fable:.2f}"
                       f"  gross savings=${fable - 0.04:.2f} ({(1 - 0.04 / fable) * 100:.0f}%)")
    assert "not measurable" not in out and "partial" not in out


def test_the_mark_names_every_unpriced_model_and_the_turns_of_all_of_them(tmp_path, capsys, config, monkeypatch):
    _prices_to(tmp_path, monkeypatch, {"half-priced": (3e-06, None)})  # input set, output null: unpriced (F6-6)
    rows = ([(_ROUTED_TS, _NULL_MODEL, 1, None, 1000)] * 2 + [(_ROUTED_TS, "claude-opus-5-5", 1, None, 1000)]
            + [(_ROUTED_TS, "half-priced", 1, None, 1000)])
    out = _run_report(_db_with(tmp_path / "t.db", rows), capsys)
    assert ("gross savings: not measurable (partial: 4 turn(s) without a price —"
            " claude-opus-5-5, claude-sonnet-5-5, half-priced)") in out


def test_all_turns_unpriced_is_not_measurable_with_zero_totals_and_no_division(tmp_path, capsys, config, monkeypatch):
    _prices_to(tmp_path, monkeypatch, {})
    for tokens in (1000, 0):  # zero tokens too: the counterfactual total is $0, nothing is divided by it
        path = _db_with(tmp_path / f"t{tokens}.db", [(_ROUTED_TS, _NULL_MODEL, 1, None, tokens)] * 5)
        out = _run_report(path, capsys)
        cf_line = _totals(out)[2]
        assert "actual=$0.00 (actual partial)" in cf_line
        assert "gross savings: not measurable (partial: 5 turn(s) without a price — claude-sonnet-5-5)" in cf_line
        assert "%" not in cf_line


def test_an_unpriced_top_tier_model_marks_the_counterfactual_side_too(tmp_path, capsys, config, monkeypatch):
    _prices_to(tmp_path, monkeypatch, {TOP: (None, None)})
    path = _db_with(tmp_path / "t.db", [(_ROUTED_TS, "claude-sonnet-5", 1, 0.01, 1000)] * 2)
    out = _run_report(path, capsys)  # the priced actual side alone is not enough; no TypeError on a None counterfactual
    cf_line = _totals(out)[2]
    assert "as-top-tier=$0.00 (counterfactual partial)" in cf_line and "(actual partial)" not in cf_line
    assert "gross savings: not measurable (partial: 2 turn(s) without a price — claude-fable-5-1)" in cf_line
    assert "as-top-tier=unpriced" in out and "%" not in cf_line


def test_each_window_is_judged_on_its_own(tmp_path, capsys, config, monkeypatch):
    _prices_to(tmp_path, monkeypatch, {})
    # PRE holds unpriced turns, ROUTED is whole: only the PRE total is marked, the savings are measured
    path = _db_with(tmp_path / "a.db", [(_PRE_TS, _NULL_MODEL, 0, None, 1000)] * 2
                    + [(_ROUTED_TS, "claude-sonnet-5", 1, 0.01, 1000)])
    pre, routed, cf = _totals(_run_report(path, capsys))[:3]
    assert pre.endswith("(partial: 2 turn(s) without a price — claude-sonnet-5-5)")
    assert "partial" not in routed and "partial" not in cf and "gross savings=$" in cf
    # the reverse: PRE whole, ROUTED has unpriced turns of a main session -- the ROUTED total is marked; the
    # savings read the routed SIDECHAINS only, and those are whole
    path = _db_with(tmp_path / "b.db", [(_PRE_TS, "claude-sonnet-5", 0, 0.01, 1000)]
                    + [(_ROUTED_TS, _NULL_MODEL, 0, None, 1000)] * 3
                    + [(_ROUTED_TS, "claude-sonnet-5", 1, 0.01, 1000)])
    pre, routed, cf = _totals(_run_report(path, capsys))[:3]
    assert "partial" not in pre and "partial" not in cf and "gross savings=$" in cf
    assert routed.endswith("(partial: 3 turn(s) without a price — claude-sonnet-5-5)")
