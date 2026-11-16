"""Tests for tools/tier_ladder.py -- the ladder home (spec 20261116-architect-tier-spec, S2).

One parameterised table per behaviour; the parameter id names the case. Two config fixtures are the two worlds:
TODAY (lead = fable, no architect key -- the live delegation.config.yaml) and AFTER (lead = opus, architect = fable).
"""
import subprocess
import sys
from pathlib import Path

import pytest

import tier_ladder as tl

FABLE, OPUS, SONNET = "claude-fable-5-1", "claude-opus-5-5", "claude-sonnet-5-5"


def _cfg(**roles):
    """A config text; each keyword is roles.<function>.subscription.model."""
    lines = ["roles:"]
    for function, model in roles.items():
        lines += [f"  {function}:", "    subscription:", f"      model: {model}"]
    return "\n".join(lines) + "\n"


TODAY = _cfg(lead=FABLE, critic=OPUS, builder=SONNET, scout=SONNET)
AFTER = _cfg(lead=OPUS, architect=FABLE, critic=OPUS, builder=SONNET, scout=SONNET)
AFTER_NO_ARCHITECT = _cfg(lead=OPUS, critic=OPUS, builder=SONNET, scout=SONNET)
CRITIC_ON_FABLE = _cfg(lead=OPUS, critic=FABLE, builder=SONNET)
LEAD_IS_ARCHITECT = _cfg(lead=FABLE, architect=FABLE, builder=SONNET, scout=SONNET)
ARCHITECT_NON_CLAUDE = _cfg(lead=OPUS, architect="llama-3.3-70b-versatile")
ARCHITECT_WEAKER = _cfg(lead=OPUS, architect=SONNET)
LEAD_NON_CLAUDE = _cfg(lead="llama-3.3-70b-versatile", critic="gpt-x")
ALIAS_BOMB = "a: &a [*a, *a]\nroles:\n  lead:\n    subscription:\n      model: claude-opus-5-5\n"
RESERVE_UNCOMMENTED = _cfg(lead=OPUS, reserve="zz-reserve-model")
LEAD_MISSING = _cfg(critic=OPUS, reserve=FABLE)
BROKEN_YAML = "not: yaml: [broken\n"


CONFIGS = {"TODAY": TODAY, "AFTER": AFTER, "AFTER_NO_ARCHITECT": AFTER_NO_ARCHITECT, "CRITIC_ON_FABLE": CRITIC_ON_FABLE,
           "LEAD_IS_ARCHITECT": LEAD_IS_ARCHITECT, "ARCHITECT_NON_CLAUDE": ARCHITECT_NON_CLAUDE,
           "ARCHITECT_WEAKER": ARCHITECT_WEAKER, "LEAD_NON_CLAUDE": LEAD_NON_CLAUDE, "ALIAS_BOMB": ALIAS_BOMB,
           "BROKEN_YAML": BROKEN_YAML, "RESERVE_UNCOMMENTED": RESERVE_UNCOMMENTED, "LEAD_MISSING": LEAD_MISSING,
           "ABSENT": None, "EMPTY": "", "ROLES_LIST": "roles: [1, 2]\n"}


def _padded(size):
    base = TODAY
    pad = size - len(base.encode("utf-8")) - 3
    return base + "# " + "x" * pad + "\n"


@pytest.mark.parametrize("model, config, rank", [
    # TODAY: the order is today's (fable = lead, opus = critic, sonnet = builder, haiku below the floor)
    ("fable", "TODAY", 3), (FABLE, "TODAY", 3), ("claude-fable-5-2", "TODAY", 3), ("mythos", "TODAY", 3),
    ("opus", "TODAY", 2), (OPUS, "TODAY", 2), ("sonnet", "TODAY", 1), ("claude-haiku-4", "TODAY", -1), ("haiku", "TODAY", -1),
    # the same words in the AFTER world: opus is the lead, fable the architect
    ("fable", "AFTER", 4), ("claude-fable-5-2", "AFTER", 4), (FABLE, "AFTER", 4), ("opus", "AFTER", 3), (OPUS, "AFTER", 3),
    ("sonnet", "AFTER", 1), ("haiku", "AFTER", -1),
    # architect key absent: fable still ranks above lead by family (case c); never MORE than with the key
    ("fable", "AFTER_NO_ARCHITECT", 4), ("claude-fable-5-2", "AFTER_NO_ARCHITECT", 4), ("opus", "AFTER_NO_ARCHITECT", 3),
    # adversarial words: spelled differently, never a rank above what the bindings give
    ("Opus", "TODAY", 2), (" opus ", "TODAY", 2), ("opus-lead", "TODAY", 2),
    ("lead", "TODAY", None), ("architect", "TODAY", None), ("", "TODAY", None), ("   ", "TODAY", None),
    (None, "TODAY", None), (5, "TODAY", None), (["fable"], "TODAY", None), ("llama-3.3-70b-versatile", "TODAY", None),
    # a lower function bound to a stronger family does not rise above lead
    ("fable", "CRITIC_ON_FABLE", 2), ("opus", "CRITIC_ON_FABLE", 3),
    # lead and architect on one id: the exact match takes the max; an unbound opus rounds DOWN to builder
    (FABLE, "LEAD_IS_ARCHITECT", 4), ("fable", "LEAD_IS_ARCHITECT", 4), ("opus", "LEAD_IS_ARCHITECT", 1),
    # architect on a non-Claude id: that id is trusted at its position, fable still ranks above lead
    ("llama-3.3-70b-versatile", "ARCHITECT_NON_CLAUDE", 4), ("fable", "ARCHITECT_NON_CLAUDE", 4),
    # architect bound WEAKER than lead never inherits rank >= lead
    (SONNET, "ARCHITECT_WEAKER", -1), ("sonnet", "ARCHITECT_WEAKER", -1),
    # non-Claude lead with no architect: a family cannot be placed -> refused as None
    ("llama-3.3-70b-versatile", "LEAD_NON_CLAUDE", 3), ("gpt-x", "LEAD_NON_CLAUDE", 2), ("fable", "LEAD_NON_CLAUDE", None),
    # a config the home cannot use -> DEFAULT_BINDINGS (today's ranks), never a refusal of the caller
    ("fable", "ALIAS_BOMB", 3), ("opus", "ALIAS_BOMB", 2), ("fable", "BROKEN_YAML", 3), ("opus", "ABSENT", 2),
    ("fable", "EMPTY", 3), ("sonnet", "ROLES_LIST", 1),
    # roles.reserve is not read: its id is unknown, a key the code does not read never raises a rank
    ("zz-reserve-model", "RESERVE_UNCOMMENTED", None), ("fable", "RESERVE_UNCOMMENTED", 4),
    # no lead model: DEFAULT_BINDINGS (opus never becomes lead through a reserve rung)
    ("opus", "LEAD_MISSING", 2), ("fable", "LEAD_MISSING", 3),
])
def test_rank_of_model_table(model, config, rank):
    assert tl.rank_of_model(model, CONFIGS[config]) == rank


@pytest.mark.parametrize("config, expected", [
    (_padded(65536), True), (_padded(65537), False),
], ids=["exactly-64KB-parsed", "64KB-plus-1-default"])
def test_config_size_limit(config, expected):
    assert len(config.encode("utf-8")) in (65536, 65537)
    found, note = tl.bindings(config)
    assert (found.get("lead") == FABLE) is expected
    assert (note is None) is expected and (expected or "64 KB" in note)


@pytest.mark.parametrize("config, found, note_part", [
    (TODAY, {"scout": SONNET, "builder": SONNET, "critic": OPUS, "lead": FABLE}, None),
    (AFTER, {"scout": SONNET, "builder": SONNET, "critic": OPUS, "lead": OPUS, "architect": FABLE}, None),
    (None, {}, "absent"), ("", {}, "absent"), (ALIAS_BOMB, {}, "alias"), (BROKEN_YAML, {}, "not readable"),
    ("roles: [1]\n", {}, "no roles mapping"), ("roles: {}\n", {}, "no coordination function"),
    (RESERVE_UNCOMMENTED, {"lead": OPUS}, "rename it to roles.architect"),
    ("roles:\n  lead:\n    subscription:\n      model:\n    api:\n      model: llama-x\n", {"lead": "llama-x"}, None),
    ("roles:\n  lead:\n    subscription:\n      model: 12\n", {}, "no coordination function"),
], ids=["today", "after", "none", "empty", "alias-bomb", "broken-yaml", "roles-not-mapping", "roles-empty",
        "reserve-not-read", "api-fallback", "non-string-model"])
def test_bindings_table(config, found, note_part):
    got, note = tl.bindings(config)
    assert got == found
    assert (note is None) if note_part is None else (note_part in note)


def test_pyyaml_import_failure_gives_default_bindings_and_a_note(monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)  # `import yaml` now raises ImportError
    assert tl.bindings(AFTER) == ({}, "pyyaml is not installed")
    found, note = tl.effective_bindings(AFTER)
    assert found == tl.DEFAULT_BINDINGS and "pyyaml" in note
    assert tl.rank_of_model("fable", AFTER) == 3  # DEFAULT lead, stricter than the AFTER world


@pytest.mark.parametrize("config, found, note_part", [
    (AFTER, tl.bindings(AFTER)[0], None),
    (None, tl.DEFAULT_BINDINGS, "absent"),
    (LEAD_MISSING, tl.DEFAULT_BINDINGS, "roles.lead names no model"),
], ids=["read", "absent-default", "no-lead-default"])
def test_effective_bindings_table(config, found, note_part):
    got, note = tl.effective_bindings(config)
    assert got == found and got is not tl.DEFAULT_BINDINGS
    assert (note is None) if note_part is None else (note_part in note)


@pytest.mark.parametrize("config, lead, architect", [
    (TODAY, FABLE, None), (AFTER, OPUS, FABLE), (None, "fable", None), (BROKEN_YAML, "fable", None),
    (LEAD_MISSING, "fable", None),
], ids=["today", "after", "absent", "broken", "no-lead"])
def test_lead_and_architect_binding(config, lead, architect):
    assert (tl.lead_binding(config), tl.architect_binding(config)) == (lead, architect)


@pytest.mark.parametrize("name, rank", [
    ("scout", 0), ("builder", 1), ("critic", 2), ("designer", 2), ("lead", 3), ("architect", 4),
    ("reserve", None), ("judge", None), ("", None), (None, None), (3, None),
])
def test_rank_of_function_table(name, rank):
    assert tl.rank_of_function(name) == rank


@pytest.mark.parametrize("model, config, expected", [
    ("claude-fable-5-2", TODAY, ("lead", f"family match: {FABLE}")),
    ("claude-fable-5-2", AFTER, ("architect", f"family match: {FABLE}")),
    (FABLE, AFTER, ("architect", "")), (OPUS, AFTER, ("lead", "")), (SONNET, TODAY, ("builder", "")),
    ("opus", TODAY, ("critic", f"family match: {OPUS}")),
    ("claude-fable-5-2", AFTER_NO_ARCHITECT, ("architect", "no architect binding")),
    ("opus", LEAD_IS_ARCHITECT, ("builder", "unbound family")),
    ("haiku", TODAY, (None, "below builder")), ("lead", TODAY, (None, "matches no binding")),
    (None, TODAY, (None, "matches no binding")),
    ("fable", BROKEN_YAML, ("lead", "config unreadable: default bindings")),
    ("sonnet", None, ("builder", "config unreadable: default bindings")),
], ids=["today-family", "after-family", "after-exact-fable", "after-exact-opus", "today-exact-sonnet", "today-opus-family",
        "after-no-key", "unbound-family", "below-builder", "function-word", "none", "broken-config", "absent-config"])
def test_function_of_session_table(model, config, expected):
    assert tl.function_of_session(model, config) == expected


def test_families_aliases_and_default_bindings_are_one_order_one_table():
    assert tl.FAMILIES == ("haiku", "sonnet", "opus", "fable") and tl.ALIASES == {"mythos": "fable"}
    assert tl.COORDINATION_FUNCTIONS == ("scout", "builder", "critic", "lead", "architect")
    assert "designer" not in tl.COORDINATION_FUNCTIONS and tl.FUNCTION_RANKS["designer"] == tl.FUNCTION_RANKS["critic"]
    assert tl.DEFAULT_BINDINGS == {"lead": "fable", "critic": "opus", "builder": "sonnet", "scout": "sonnet"}
    assert [tl.family_of(m) for m in ("claude-opus-5-5", "MYTHOS", "llama-3", "", None, 7)] == [
        "opus", "fable", None, None, None, None]


def test_importing_the_home_does_not_import_yaml():
    tools = str(Path(tl.__file__).resolve().parent)
    code = ("import sys; sys.path.insert(0, sys.argv[1]); import tier_ladder; "
            "assert 'yaml' not in sys.modules, 'yaml was imported'; tier_ladder.bindings('roles: {}\\n'); "
            "assert 'yaml' in sys.modules; print('ok')")
    out = subprocess.run([sys.executable, "-I", "-c", code, tools], capture_output=True, text=True)
    assert out.returncode == 0 and out.stdout.strip() == "ok", out.stderr
