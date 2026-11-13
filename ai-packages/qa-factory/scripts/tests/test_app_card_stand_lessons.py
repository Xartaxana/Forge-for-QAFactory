#!/usr/bin/env python3
"""SS1-11 F5 (t-405): what a person taught about the stand reaches the app card and rebuilds it.

Moved out of test_app_card.py (quarantined, so a test there never runs in the canon); the helpers `make`, `card_of` and
`body` are imported from it (importing it has no side effects: sys.path and `import app_card` only).

Run: python -B scripts/tests/test_app_card_stand_lessons.py    or    python -m pytest scripts/tests/test_app_card_stand_lessons.py -q
"""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import app_card as AC  # noqa: E402
from test_app_card import body, card_of, fl_row, headers, make, write_first_look  # noqa: E402


def test_stand_lessons_reach_the_card_and_rebuild_it(tmp_path):
    """F5 (t-405): what a person taught about the stand is a line of the card's Stand section (the walk road); a lesson recorded
    after the card was built changes the hash and the card is rebuilt; no registry file: no line, the hash is stable."""
    import project_knowledge as PK
    task = make(tmp_path)
    project = task.parents[2]
    AC.build(task)
    assert "Stand lessons" not in card_of(task)                                       # no registry file: no line
    assert AC.build(task).startswith("app-card: unchanged")                          # ... and the hash is stable
    row, problem, _ = PK.record(project, key=PK.LESSONS_KEY, environment="local", element="indexing", state=PK.KNOWN, scope="stand",
                                value={"wait_s": 300}, words="Indexing takes minutes", source="person", story="S-1", by="conductor")
    assert problem == ""
    assert AC.build(task).startswith("app-card: written")                            # the lesson changed the inputs: rebuilt
    stand = body(card_of(task), "Stand")
    assert '- Stand lessons: indexing: "Indexing takes minutes" (at least 300 s)' in stand
    assert AC.build(task).startswith("app-card: unchanged")
    row, problem, _ = PK.record(project, key=PK.LESSONS_KEY, environment="local", element="login", state=PK.KNOWN, scope="stand",
                                value={"wait_s": None}, words="Login is slow", source="person", story="S-1", by="conductor")
    assert problem == "" and AC.build(task).startswith("app-card: written")          # a second record changes the hash
    assert "- Stand lessons: login:" in body(card_of(task), "Stand")


LESSON_STAND = "local"


def _words(n: int) -> str:
    """`n` characters of plain words: a run of nine letters, a space, ... (no digit, no secret-looking shape)."""
    return ("abcdefghi " * (n // 10 + 1))[:n - 1] + "z"


def _cfg(**over) -> dict:
    cfg = {"environment": {"env_file": "qa-factory/env.local", "user_key": "AUTH_USERNAME", "secret_keys": ["AUTH_PASSWORD"]},
           "environments": [{"name": LESSON_STAND, "base_url": "http://localhost:8000", "frontend": {"url": "http://localhost:5173"},
                             "credentials_by_role": {"admin": "ADMIN_USER / ADMIN_PASS"}}]}
    cfg.update(over)
    return cfg


def _login(**ui) -> dict:
    recipe = {"path": "/login", "username": {"role": "textbox", "name": "User"}, "password": {"role": "textbox", "name": "Pass"},
              "submit": {"role": "button", "name": "Go"}}
    recipe.update(ui)
    return {"manual_capture": {"login": {"ui": recipe}}}


def _built(tmp_path, **kw) -> tuple:
    task = make(tmp_path, **kw)
    AC.build(task)
    return task, card_of(task)


def _lesson(project, words: str, element: str = "indexing") -> None:
    import project_knowledge as PK
    row, problem, _ = PK.record(project, key=PK.LESSONS_KEY, environment=LESSON_STAND, element=element, state=PK.KNOWN, scope="stand",
                                value={"wait_s": None}, words=words, source="person", story="S-1", by="conductor")
    assert problem == ""


def _write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


CASES = {}


def case(name):
    def register(fn):
        CASES[name] = fn
        return fn
    return register


def _lesson_case(words):
    def run(tmp_path):
        task = make(tmp_path)
        _lesson(task.parents[2], words)
        AC.build(task)
        assert f'- Stand lessons: indexing: "{words}"' in body(card_of(task), "Stand")          # C1: a person's words, never cut
    return run


for _n in (400, 401, 1000):
    CASES[f"LESSON-{_n}"] = _lesson_case(_words(_n))
CASES["LESSON-CYR401"] = _lesson_case("".join(chr(0x430 + i % 32) for i in range(401)))          # E4: 401 characters, 802 bytes


@case("LESSON-SAFE")
def _(tmp_path):
    task = make(tmp_path)
    _lesson(task.parents[2], "when slow, password: hunter2 " + _words(450))      # E9: whole never means unredacted
    AC.build(task)
    stand = body(card_of(task), "Stand")
    assert "hunter2" not in stand and "password: [not printed]" in stand and _words(450) in stand


@case("ACCOUNTS-30-ROLES")
def _(tmp_path):
    roles = [f"role{i:02d}" + "r" * 14 for i in range(30)]          # 30 roles of 20 characters (C3)
    stand = {"name": LESSON_STAND, "base_url": "http://localhost:8000", "frontend": {"url": "http://localhost:5173"},
             "credentials_by_role": {r: f"U{i} / P{i}" for i, r in enumerate(roles)}}
    task, text = _built(tmp_path, config=_cfg(environments=[stand]))
    accounts = body(text, "Accounts")
    assert [r for r in roles if f'--as "{r}"' not in accounts] == []


@case("PROFILE-301")
def _(tmp_path):
    line = _words(301)
    task, text = _built(tmp_path, profile=f"# Project profile\n\n- **Components and entry points** — {line}\n- **Test data** — {line}\n")
    assert f"- {line}" in body(text, "Entry routes").splitlines() and f"- {line}" in body(text, "Test data").splitlines()   # C4


@case("TD-VALUE-301")
def _(tmp_path):
    value = _words(301)
    task, text = _built(tmp_path, config=_cfg(test_data={"note": value, "ten_k": _words(3010)}))
    data = body(text, "Test data")
    assert f"- config test_data.note: {value}" in data and f"- config test_data.ten_k: {_words(3010)}" in data      # C5


@case("TD-SECRET")
def _(tmp_path):
    key = "x" * 55 + "_password"                                  # 64 characters ending in a secret-looking name (C6, E9)
    task, text = _built(tmp_path, config=_cfg(test_data={key: "Hunt3rPl4ntedValue", "y" * 70 + "_token": "Pl4ntedTokenValue"}))
    assert f"- config test_data.{key}: (value not printed)" in text and "Hunt3rPl4ntedValue" not in text
    assert "Pl4ntedTokenValue" not in text and "y" * 70 + "_token: (value not printed)" in text


def _names_case(count, name_len=8):
    def run(tmp_path):
        names = [f"n{i:03d}".ljust(name_len, "e") for i in range(count)]
        task, text = _built(tmp_path, config=_cfg(test_data={"catalogue": {n: 1 for n in names}}))
        line = [x for x in body(text, "Test data").splitlines() if x.startswith("- config test_data.catalogue:")][0]
        shown = ", ".join(names[:AC.TEST_DATA_NAMES])
        if count <= AC.TEST_DATA_NAMES:
            assert line == f"- config test_data.catalogue: {count} entries (names: {shown})"
        else:       # C7: how many were left out, and where they are
            assert line == (f"- config test_data.catalogue: {count} entries (names: {shown}; "
                            f"+{count - AC.TEST_DATA_NAMES} more: qa-factory/config.json `test_data.catalogue`)")
    return run


for _n in (8, 9, 100):
    CASES[f"TD-NAMES-{_n}"] = _names_case(_n)
CASES["TD-NAME-41"] = _names_case(2, name_len=41)


@case("TD-EMPTY-DICT")
def _(tmp_path):
    task, text = _built(tmp_path, config=_cfg(test_data={"catalogue": {}}))      # E1: no names, no pointer
    assert "- config test_data.catalogue: 0 entries" in body(text, "Test data").splitlines() or "test_data.catalogue: not set" in text


@case("ROUTE-METHOD-13")
def _(tmp_path):
    task = make(tmp_path)
    method, src = "M" * 13, "src/" + "d" * 130 + "/orders_api.ts"
    _write_json(task / "work" / "flow-requests.json", {"schema_version": 1, "requests": [
        {"method": method, "url_template": "https://x.test/api/a?token=Pl4ntedQueryTok#frag", "source": "code", "path": src, "line": 7}]})
    AC.build(task)
    routes = body(card_of(task), "Entry routes")
    assert f"- {method} https://x.test/api/a ({src}:7)" in routes and "Pl4ntedQueryTok" not in routes      # C9, C22 stays


@case("ROUTE-PATH-121")
def _(tmp_path):
    task = make(tmp_path)
    src = "p" * 121
    _write_json(task / "work" / "flow-requests.json", {"schema_version": 1, "requests": [
        {"method": "GET", "url_template": "https://x.test/api/a", "source": "code", "path": src, "line": 1}]})
    AC.build(task)
    assert f"({src}:1)" in body(card_of(task), "Entry routes")


@case("SELECTOR-81")
def _(tmp_path):
    name = "n" * 70 + "-field"
    testid = '[data-testid="checkout-submit-button-v2' + "s" * 60 + '"]'     # a long data-testid is no secret: whole (E9, tokens=False)
    task, text = _built(tmp_path, config=_cfg(**_login(username={"role": "textbox", "name": name}, submit=testid)))
    signin = body(text, "Sign-in")
    assert f'username textbox "{name}"' in signin and f"submit {testid}" in signin


@case("RECIPE-121")
def _(tmp_path):
    path = "/" + "r" * 120 + "/login"
    task, text = _built(tmp_path, config=_cfg(**_login(path=path)))
    assert f"- Sign-in route: {path};" in body(text, "Sign-in")


@case("RECIPE-USERINFO")
def _(tmp_path):
    task, text = _built(tmp_path, config=_cfg(**_login(path="https://user:Pl4ntedSecret@host.test/" + "q" * 130)))
    signin = body(text, "Sign-in")
    assert "Pl4ntedSecret" not in signin and "- Sign-in route: https://host.test/" + "q" * 130 + ";" in signin     # E9: _USERINFO removed


@case("SELECTOR-EMPTY")
def _(tmp_path):
    task, text = _built(tmp_path, config=_cfg(**_login(username={})))
    assert 'fields: username field ""' in body(text, "Sign-in")      # E1: today's line


def _proven_case(count):
    def run(tmp_path):
        import manual_capture as MC
        task = make(tmp_path, config=_cfg(**_login()))
        cfg = json.loads((task.parents[1] / "config.json").read_text(encoding="utf-8"))
        sha = MC.recipe_sha(MC.login_recipe(cfg, MC.spec(), "ui"))
        accounts = [f"account-{i}-" + "a" * 60 for i in range(count)]      # names of 60+ characters
        _write_json(task / "state" / "sign-in-probe.json", {a: {"outcome": "ok", "recipe_sha": sha} for a in accounts})
        AC.build(task)
        assert "Sign-in: proven at gate A for " + ", ".join(accounts) + " (a `ui --session <account>` call" in body(card_of(task), "Sign-in")     # C12
    return run


for _n in (8, 9, 30):
    CASES[f"PROVEN-{_n}"] = _proven_case(_n)


@case("KEYS-61")
def _(tmp_path):
    user_key, pass_key = "USER_" + "K" * 56, "PASS_" + "K" * 56         # 61 characters each
    spaced = "qa-factory/my env dir/" + "e" * 100 + "/.env"             # a path with spaces, over 121 characters (C13, E6)
    task = make(tmp_path, config=_cfg(environment={"env_file": spaced, "user_key": user_key, "secret_keys": [pass_key]}))
    env = task.parents[2] / spaced
    env.parent.mkdir(parents=True)
    env.write_text(f"{user_key}=u1\n{pass_key}=Pl4ntedEnvPw\n", encoding="utf-8")
    AC.build(task)
    accounts = body(card_of(task), "Accounts")
    assert f"- Default account: keys {user_key} / {pass_key} in {spaced} (`--as default`; names only)" in accounts
    assert "Pl4ntedEnvPw" not in card_of(task)


@case("CREATED-401")
def _(tmp_path):
    task = make(tmp_path)
    why = _words(401)
    _write_json(task / "state" / "created-accounts.json", {"accounts": [
        {"name": "qa-user-1", "password": "Pl4ntedCreatedPw", "case": "c1", "confirmed_by": "walker", "why": why}]})
    AC.build(task)
    accounts = body(card_of(task), "Accounts")
    assert f"(on the walker's word: {why})" in accounts and "Pl4ntedCreatedPw" not in accounts      # C14


@case("PAGE-201")
def _(tmp_path):
    task = make(tmp_path)
    (task / "work" / "briefs").mkdir()
    line = "- `pages/books_page.py` (1,200 B): " + _words(201)
    (task / "work" / "briefs" / "repo-map-abc.md").write_text(f"# Repo map\n\n## Utils, page objects and test data, ranked\n\n{line}\n", encoding="utf-8")
    AC.build(task)
    assert line in body(card_of(task), "Page objects").splitlines()                              # C15


def _note_case(note, expect=None):
    def run(tmp_path):
        task = make(tmp_path)
        (task / "work" / "app-card-notes.jsonl").write_text(json.dumps({"about": "card", "note": note}) + "\n", encoding="utf-8")
        AC.build(task)
        lines = body(card_of(task), "Notes from walkers").splitlines()
        assert lines == [f"- {expect if expect is not None else note}"]                          # C16: one line, no character dropped
    return run


CASES["NOTE-201"] = _note_case(_words(201))
CASES["NOTE-EMOJI-201"] = _note_case("n" * 150 + " \U0001F600 " + "m" * 50)
CASES["NOTE-MULTILINE"] = _note_case("first part\n\n## Sign-in\n\t- second part\r\nthird part", "first part ## Sign-in - second part third part")      # E3


@case("NOTE-SAFE")
def _(tmp_path):
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwbGFudGVkIn0.c2lnbmF0dXJl"
    task = make(tmp_path)
    note = f"login failed with {jwt} then token=abc123 and a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6 " + _words(300)
    (task / "work" / "app-card-notes.jsonl").write_text(json.dumps({"about": "card", "note": note}) + "\n", encoding="utf-8")
    AC.build(task)
    notes = body(card_of(task), "Notes from walkers")
    assert jwt not in notes and "abc123" not in notes and "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" not in notes      # E9
    assert "[not printed]" in notes and _words(300) in notes


@case("FL-SELECTOR-300")
def _(tmp_path):
    task = make(tmp_path)
    selector = '[data-testid="' + "s" * 300 + '"]'
    row = fl_row(1)
    row["path"]["locators"] = [{"what": "Pay button", "selector": selector, "seen": "yes"}]
    write_first_look(task, [row])
    AC.build(task)
    assert f"  - locator Pay button: {selector} (seen yes)" in body(card_of(task), "First look").splitlines()      # C17


@case("FL-REASON-121")
def _(tmp_path):
    import first_look as FL
    long_text = _words(121)
    for kind, got in (("null", {"null": long_text.replace(" ", "_")}), ("stale", {"problem": long_text}), ("unreadable", {"problem": long_text})):
        real = FL.state
        FL.state = lambda root, kind=kind, got=got: {"kind": kind, "got": got, "error": ""}
        try:
            task = make(tmp_path / kind)
            AC.build(task)
        finally:
            FL.state = real
        look = body(card_of(task), "First look")
        assert long_text in look, kind                                                              # C18: the reason whole, no pointer (E5)


@case("WHY-161")
def _(tmp_path):
    import user_path_failures as UPF
    task = make(tmp_path)
    reason = _words(161)
    real = UPF.read_requests

    def boom(root):
        raise RuntimeError(reason)
    UPF.read_requests = boom
    try:
        AC.build(task)
    finally:
        UPF.read_requests = real
    assert f"cannot be read (RuntimeError: {reason})" in body(card_of(task), "Entry routes")        # C19, E5


@case("EMPTY-ABSENT")
def _(tmp_path):
    bare = tmp_path / "bare story"
    bare.mkdir()
    AC.build(bare)
    text = card_of(bare)                                            # E1: every absent input is said, byte-identical lines
    assert body(text, "Stand") == "not known: no qa-factory/config.json above the task root (the project is not onboarded)"
    assert body(text, "Notes from walkers") == "not known: no walker has left a note yet (work/app-card-notes.jsonl)"
    assert body(text, "First look") == "not known: there was no first look"


@case("FORMAT-REBUILD")
def _(tmp_path):
    task = make(tmp_path)
    old = AC.FORMAT
    AC.FORMAT = "1"
    try:
        assert AC.build(task).startswith("app-card: written")        # a card as FV1-4 wrote it
    finally:
        AC.FORMAT = old
    assert old != "1" and AC.build(task).startswith("app-card: written")        # E7: rebuilt once
    assert AC.build(task).startswith("app-card: unchanged")


@case("FULL-CARD")
def _(tmp_path):
    task = make(tmp_path, config=_cfg(test_data={"note": _words(9000)}))
    _write_json(task / "work" / "flow-requests.json", {"schema_version": 1, "requests": [
        {"method": "GET", "url_template": f"https://x.test/api/r{i}", "source": "code", "path": f"src/a{i}.ts", "line": i + 1} for i in range(5)]})
    write_first_look(task, [fl_row(1)])
    AC.build(task)
    text = card_of(task)
    assert len(text.encode("utf-8")) > AC.CARD_MAX_BYTES                                    # E8: the fixed sections alone pass the limit
    assert f"- config test_data.note: {_words(9000)}" in text and headers(text) == list(AC.SECTIONS)
    assert body(text, "First look") == AC.FIRST_LOOK_POINTER and "- +5 more: work/flow-requests.json" in body(text, "Entry routes")
    assert "x.test/api/r0" not in text


@pytest.mark.parametrize("name", list(CASES))
def test_card_values_whole_or_counted(tmp_path, name):
    """FV1-4 L1 (item 1): the card shows no character-clipped value - every value is whole (through `scrub` only, whole never means
    unredacted), and a list the card caps by count says how many were left out and in which file. One row per site of the L1 table
    (C1-C22), each at, one beyond and far beyond the old bound; the id names the row."""
    CASES[name](tmp_path)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
