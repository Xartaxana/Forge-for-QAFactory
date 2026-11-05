"""Tests for tools/dev_config.py: the per-developer config, its defaults, refusals and the token discipline.

Run from the repo root: python -m pytest tools/test_dev_config.py -q
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import dev_config  # noqa: E402

SECRET = "hidden_secret_value"      # not of the shape of a key or a token (F-12): the scanners stay quiet
TOKEN_VAR = "DEV_CONFIG_TEST_TOKEN_VAR"
FULL = {"developer": "dev1",
        "stand_copy_root": "D:/stand",
        "release_repo_root": "D:/release",
        "github_token_env": "GITHUB_TOKEN"}
DEFAULTS = {"github_token_env": "GITHUB_TOKEN"}


def put(tmp_path, text, newline=None, encoding="utf-8"):
    """tmp_path as a repo root holding tools/dev.config.yaml with `text`; returns the root."""
    (tmp_path / "tools").mkdir(exist_ok=True)
    with open(tmp_path / "tools" / "dev.config.yaml", "w", encoding=encoding, newline=newline) as f:
        f.write(text)
    return tmp_path


def full_text(**override):
    """A file that names all four keys (so no missing-key WARN), single-quoted."""
    return "".join("%s: '%s'\n" % item for item in dict(FULL, **override).items())


def refusal(root):
    with pytest.raises(dev_config.DevConfigError) as info:
        dev_config.load(root)
    return str(info.value)


def test_only_the_token_variable_has_a_default_and_no_path_or_developer_is_guessed():
    assert dev_config.DEFAULTS == DEFAULTS
    assert dev_config.KEYS == ("developer", "stand_copy_root", "release_repo_root", "github_token_env")
    assert dev_config.NO_DEFAULT_IN_A_FILE == ("github_token_env", "gitlab_token_env")
    assert dev_config.LEGACY_KEYS == {"public_skills_root": "release_repo_root", "gitlab_token_env": None}


def test_example_file_is_a_valid_config_with_a_neutral_slug_and_no_internal_names():
    data = dev_config._parse(HERE / "dev.config.example.yaml")
    values = {k: v for k, (v, _line) in data.items()}
    assert values == {"developer": "dev1", "stand_copy_root": "../stand", "release_repo_root": "../QAFactory",
                      "github_token_env": "GITHUB_TOKEN"}
    # neutral: no drive letter and no absolute path (F-16: the old pin on two internal names is gone with the names;
    # the name list is the scanner's rules file, docs/migration/scrub_rules.json, and is not repeated here)
    text = (HERE / "dev.config.example.yaml").read_text(encoding="utf-8").lower()
    assert "c:\\" not in text and not any(Path(v).is_absolute() for v in values.values())


def test_no_file_gives_none_paths_one_warn_line_and_no_developer(tmp_path, capsys):
    cfg = dev_config.load(tmp_path)
    err = capsys.readouterr().err
    path = tmp_path / "tools" / "dev.config.yaml"
    assert err.count("WARN") == 1 and err.startswith("WARN dev.config.yaml not found at %s:" % path)
    assert "tools/dev.config.example.yaml" in err
    assert cfg["developer"] is None and cfg["stand_copy_root"] is None and cfg["release_repo_root"] is None
    assert cfg["github_token_env"] == "GITHUB_TOKEN" and cfg["gitlab_token_env"] is None
    assert "public_skills_root" not in cfg
    assert cfg["source"] == "defaults" and cfg["path"] == str(path)


def test_file_values_win_and_each_missing_key_gets_its_own_warn(tmp_path, capsys):
    cfg = dev_config.load(put(tmp_path, "developer: devtwo\nstand_copy_root: D:/runs/copies\n"))
    err = capsys.readouterr().err.splitlines()
    assert cfg["developer"] == "devtwo"
    assert cfg["stand_copy_root"] == "D:/runs/copies"      # forward slashes: kept as given
    assert cfg["release_repo_root"] is None
    assert cfg["source"] == "file"
    assert [line.split("`")[1] for line in err] == ["release_repo_root", "github_token_env"]
    assert all(line.startswith("WARN dev.config.yaml has no `") for line in err)
    assert all("no default, so whatever needs it refuses" in line and "is in use" not in line for line in err)
    assert dev_config.resolve(tmp_path)[1] == {"developer": "file", "stand_copy_root": "file",
                                               "release_repo_root": "absent", "github_token_env": "default",
                                               "gitlab_token_env": "absent"}


def test_old_keys_only_file_is_not_refused_and_aliases_are_filled(tmp_path, capsys):
    """The temporal edge: a file written before the move keeps working -- no hook and no tool refuses it. The old
    path name fills release_repo_root; there is NO public_skills_root in cfg (F-8: it has no readers)."""
    root = put(tmp_path, "developer: devtwo\nstand_copy_root: D:/s\npublic_skills_root: D:/p\n"
                         "gitlab_token_env: MY_GL_TOKEN\n")
    cfg, origins = dev_config.resolve(root)
    err = capsys.readouterr().err.splitlines()
    assert cfg["release_repo_root"] == "D:/p" and origins["release_repo_root"] == "file"
    assert cfg["gitlab_token_env"] == "MY_GL_TOKEN" and origins["gitlab_token_env"] == "file"
    assert "public_skills_root" not in cfg and "public_skills_root" not in origins
    assert [line.split("`")[1] for line in err] == ["public_skills_root", "github_token_env"]
    assert err[0].startswith("WARN") and "rename `public_skills_root` to `release_repo_root`" in err[0]
    assert "D:/p" not in err[0]
    assert dev_config.developer_slug(root) == ("devtwo", "")        # the journal goes through this


def test_both_names_new_wins_one_warn(tmp_path, capsys):
    cfg = dev_config.load(put(tmp_path, "release_repo_root: D:/new\npublic_skills_root: D:/old\n"))
    err = capsys.readouterr().err.splitlines()
    assert cfg["release_repo_root"] == "D:/new"
    both = [line for line in err if "public_skills_root" in line]
    assert len(both) == 1 and "different values" in both[0] and "`release_repo_root` is used" in both[0]
    assert "D:/new" not in both[0] and "D:/old" not in both[0]        # values are not printed


def test_unknown_key_still_refused(tmp_path):
    message = refusal(put(tmp_path, "developer: devtwo\npublic_skills_roots: D:/x\n"))
    assert "unknown key 'public_skills_roots'" in message and "line 2" in message


def test_old_token_key_bad_shape_refused_without_echo(tmp_path):
    for value in (SECRET, "lower_case_name"):
        message = refusal(put(tmp_path, "gitlab_token_env: '%s'\n" % value))
        assert "'gitlab_token_env' is not the name of an environment variable" in message
        assert value not in message
    message = refusal(put(tmp_path, "github_token_env: '%s'\n" % SECRET))
    assert "'github_token_env'" in message and SECRET not in message


def test_a_file_that_names_every_key_is_silent(tmp_path, capsys):
    cfg = dev_config.load(put(tmp_path, full_text(developer="devtwo")))
    assert capsys.readouterr().err == "" and cfg["developer"] == "devtwo"


def test_missing_developer_in_an_existing_file_is_none_with_a_warn_that_says_no_default(tmp_path, capsys):
    text = "".join("%s: x\n" % k for k in ("stand_copy_root", "release_repo_root")) + "github_token_env: T\n"
    cfg, origins = dev_config.resolve(put(tmp_path, text))
    err = capsys.readouterr().err
    assert cfg["developer"] is None and origins["developer"] == "absent"
    assert err.count("WARN") == 1 and "`developer`" in err and "no default" in err


def test_crlf_file_is_fine(tmp_path):
    cfg = dev_config.load(put(tmp_path, "developer: devtwo\r\ngithub_token_env: MY_TOKEN\r\n", newline=""))
    assert cfg["developer"] == "devtwo" and cfg["github_token_env"] == "MY_TOKEN"


def test_leading_bom_is_fine(tmp_path):
    cfg = dev_config.load(put(tmp_path, "developer: devtwo\n", encoding="utf-8-sig"))
    assert cfg["developer"] == "devtwo"


@pytest.mark.parametrize("text", ["", "# only a comment\n", "\n\n  # indented comment\n"])
def test_empty_file_is_defaults_with_one_warn_not_per_key(tmp_path, capsys, text):
    cfg = dev_config.load(put(tmp_path, text))
    err = capsys.readouterr().err
    assert err.startswith("WARN dev.config.yaml is empty at ") and err.count("WARN") == 1
    assert cfg["source"] == "defaults" and cfg["developer"] is None
    # FX-1: no default is said to be in use; the token variables are said to have none in a file
    assert "github_token_env, gitlab_token_env have no default in a file that exists" in err
    assert "is in use" not in err and "so whatever needs them refuses until you set them" in err


def test_refused_default_is_true_only_for_a_token_key_of_a_file_that_exists_and_does_not_name_it(tmp_path):
    def state(root):
        cfg, origins = dev_config.resolve(root)
        return {key: dev_config.refused_default(key, cfg, origins) for key in dev_config.TOKEN_KEYS}

    none = dict.fromkeys(dev_config.TOKEN_KEYS, False)
    assert state(tmp_path) == none                                              # no file: the fallback is used
    both = dict.fromkeys(dev_config.TOKEN_KEYS, True)
    assert state(put(tmp_path, "developer: devtwo\n")) == both                  # keys absent
    assert state(put(tmp_path, "")) == both                                      # empty file
    assert state(put(tmp_path, "github_token_env: MY_TOKEN\n")) == dict(none, gitlab_token_env=True)   # one named
    assert state(put(tmp_path, "gitlab_token_env: MY_TOKEN\n")) == dict(none, github_token_env=True)   # the old one
    assert state(put(tmp_path, "gitlab_token_env: A\ngithub_token_env: B\n")) == none


@pytest.mark.parametrize("text", ["developer:\n", "developer: ''\n", "stand_copy_root:   \n", "developer: # c\n",
                                  'developer: "  "\n'])
def test_empty_value_is_refused_naming_the_key_and_the_line(tmp_path, text):
    key = text.split(":")[0]
    message = refusal(put(tmp_path, "# top\n" + text))
    assert "'%s'" % key in message and "non-empty" in message and "tools/dev.config.example.yaml" in message
    assert "dev.config.yaml line 2:" in message


def test_unknown_key_is_refused_naming_it_and_the_allowed_keys(tmp_path):
    message = refusal(put(tmp_path, "developer: devtwo\ngitlab_token: oops\n"))
    assert "unknown key 'gitlab_token'" in message and "line 2" in message
    assert all(k in message for k in dev_config.KEYS)


@pytest.mark.parametrize("slug", ["Devtwo", "1abc", "a", "x" * 25, "x" * 32, "dev_two", "dev two", "-abc"])
def test_bad_slug_is_refused(tmp_path, slug):
    message = refusal(put(tmp_path, "developer: '%s'\n" % slug))
    assert "is not a slug" in message and "[a-z][a-z0-9-]{1,23}" in message and "line 1" in message


@pytest.mark.parametrize("slug", ["ab", "devtwo", "a1-b2", "x" * 24])
def test_good_slug_is_accepted(tmp_path, slug):
    assert dev_config.load(put(tmp_path, "developer: %s\n" % slug))["developer"] == slug


@pytest.mark.parametrize("text", ["developer: main\n", 'developer: "main"\n'])
def test_main_is_a_reserved_slug(tmp_path, text):
    message = refusal(put(tmp_path, text))
    assert "'main'" in message and "reserved" in message and "line 1" in message


def test_slug_grammar_is_the_journal_label_bound():
    import journal_keys  # tools/journal_keys.py: its LABEL_RE is the wider rule (1-24, no leading letter)
    for length in (2, 24):
        assert dev_config.SLUG_RE.match("a" * length) and journal_keys.LABEL_RE.match("a" * length)
    assert not dev_config.SLUG_RE.match("a" * 25) and not journal_keys.LABEL_RE.match("a" * 25)


@pytest.mark.parametrize("text,fragment", [
    ("developer: [unclosed\n", "line 1"),
    ("developer: [a, b]\n", "a list"),
    ("developer: {a: b}\n", "a list"),
    ("- a\n- b\n", "line 1"),
    ("just text\n", "a line without `:`"),
    ("a: b: c\n", "unknown key 'a'"),
    ("{}\n", "a line without `:`"),
    ("developer: x\ndeveloper: y\n", "given twice (first on line 1)"),
    ("developer: x\n  stand_copy_root: y\n", "line 2: an indented line"),
    ("developer: x\n\tstand_copy_root: y\n", "line 2: a tab-indented line"),
    ("stand_copy_root:\n  nested: y\n", "line 1: the key 'stand_copy_root' has an empty value"),
    ("developer: 'unclosed\n", "a quote that is opened and not closed"),
    ("developer: 'a' b\n", "text after the closing quote"),
    ("developer:devtwo\n", "no space after the `:`"),
    ("- a: b\n", "not a key name"),
])
def test_malformed_file_is_refused_with_the_line(tmp_path, text, fragment):
    message = refusal(put(tmp_path, text))
    assert "dev.config.yaml" in message and "expected" in message and fragment in message


def test_refusals_name_the_line_never_the_value(tmp_path):
    for text in ("stand_copy_root: '%s\n" % SECRET, "%s\n" % SECRET, "developer: x\n  %s: y\n" % SECRET,
                 "gitlab_token_env: '%s'\n" % SECRET, "gitlab_token_env: %s\n%s\n" % (SECRET, SECRET)):
        message = refusal(put(tmp_path, text))
        assert SECRET not in message and "line " in message


@pytest.mark.parametrize("text,key,value", [
    ("stand_copy_root: 'D:/a#b'\n", "stand_copy_root", "D:/a#b"),
    ('stand_copy_root: "D:/a #b"   # trailing\n', "stand_copy_root", "D:/a #b"),
    ("stand_copy_root: D:/runs  # note\n", "stand_copy_root", "D:/runs"),
    ("stand_copy_root: D:/a#b\n", "stand_copy_root", "D:/a#b"),            # '#' glued to text is not a comment
    ("stand_copy_root: 'C:\\work\\x'\n", "stand_copy_root", "C:\\work\\x"),     # no escapes in either kind of quote
    ('stand_copy_root: "C:\\work\\x"\n', "stand_copy_root", "C:\\work\\x"),
    ("stand_copy_root: C:\\work\\x\n", "stand_copy_root", "C:\\work\\x"),
    ("stand_copy_root:    spaced   \n", "stand_copy_root", "spaced"),
])
def test_scalar_grammar(tmp_path, text, key, value):
    assert dev_config.load(put(tmp_path, text))[key] == value


def test_non_utf8_file_is_refused_not_a_traceback(tmp_path):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "dev.config.yaml").write_bytes(b"developer: \xff\xfe\x00bad\n")
    assert "cannot be read" in refusal(tmp_path)


def test_stand_copy_root_that_does_not_exist_is_not_checked(tmp_path):
    cfg = dev_config.load(put(tmp_path, "stand_copy_root: Z:\\no\\such\\folder\n"))
    assert cfg["stand_copy_root"] == "Z:\\no\\such\\folder"


def test_module_is_stdlib_only():
    source = (HERE / "dev_config.py").read_text(encoding="utf-8")
    assert "import yaml" not in source and "from yaml" not in source


# --- developer_slug ----------------------------------------------------------------------------------------

def test_developer_slug_of_a_good_file_prints_nothing(tmp_path, capsys):
    assert dev_config.developer_slug(put(tmp_path, "developer: devtwo\n")) == ("devtwo", "")
    assert capsys.readouterr().err == ""


def test_developer_slug_without_a_file_names_the_path_and_prints_nothing(tmp_path, capsys):
    slug, reason = dev_config.developer_slug(tmp_path)
    assert slug is None and reason == "no config file at %s" % (tmp_path / "tools" / "dev.config.yaml")
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("text", ["", "# nothing\n", "stand_copy_root: D:/x\n"])
def test_developer_slug_with_the_key_absent_never_falls_back_to_a_default(tmp_path, text):
    slug, reason = dev_config.developer_slug(put(tmp_path, text))
    assert slug is None and reason == "developer key absent in %s" % (tmp_path / "tools" / "dev.config.yaml")


@pytest.mark.parametrize("text", ["developer: Bad\n", "developer: main\n", "developer: [a]\n", "just text\n"])
def test_developer_slug_of_a_refused_file_is_none_and_the_refusal_on_one_line(tmp_path, text):
    slug, reason = dev_config.developer_slug(put(tmp_path, text))
    assert slug is None and reason.startswith("dev.config.yaml") and "\n" not in reason


def test_developer_slug_keeps_the_doors(tmp_path, monkeypatch):
    other = door_file(tmp_path)
    assert dev_config.developer_slug(path=other) == ("viaenv", "")
    monkeypatch.setenv("QA_DEV_CONFIG", str(other))
    assert dev_config.developer_slug(put(tmp_path, "developer: indefault\n")) == ("viaenv", "")
    slug, reason = dev_config.developer_slug(path=tmp_path / "gone.yaml")
    assert slug is None and "not a file" in reason


def run_script(tmp_path, env_extra=None, args=()):
    """The real script in a copy of the tree: its root is the copy, so the real config is never read."""
    (tmp_path / "tools").mkdir(exist_ok=True)
    shutil.copy(HERE / "dev_config.py", tmp_path / "tools" / "dev_config.py")
    env = {k: v for k, v in os.environ.items() if k != TOKEN_VAR}
    env.update(env_extra or {})
    return subprocess.run([sys.executable, "-B", str(tmp_path / "tools" / "dev_config.py"), *args],
                          capture_output=True, text=True, env=env)


def test_cli_without_file_exits_0_with_warn_and_not_set(tmp_path):
    done = run_script(tmp_path)
    assert done.returncode == 0
    assert done.stderr.startswith("WARN dev.config.yaml not found at ")
    assert "developer = (not set)  [absent: set it in tools/dev.config.yaml]" in done.stdout
    assert "stand_copy_root = (not set)  [absent: set it in tools/dev.config.yaml]" in done.stdout
    assert "release_repo_root = (not set)  [absent: set it in tools/dev.config.yaml]" in done.stdout
    assert "environment variable GITHUB_TOKEN: " in done.stdout
    assert "github_token_env = GITHUB_TOKEN  [default]" in done.stdout     # no file: the fallback IS used (FX-1 edge)


@pytest.mark.parametrize("text", ["developer: devtwo\n", "# only a comment\n"], ids=["key-absent", "empty-file"])
def test_cli_for_a_file_that_does_not_name_a_token_variable_shows_the_refusal_not_the_default(tmp_path, text):
    """FX-1: the token readers refuse such a file, so the CLI must not show GITHUB_TOKEN as in use."""
    put(tmp_path, text)
    done = run_script(tmp_path)
    assert done.returncode == 0
    assert ("github_token_env = (not set)  [refused: github_token_env has no default in a file that exists, so "
            "whatever needs it refuses; set it in tools/dev.config.yaml]") in done.stdout
    assert "environment variable: none to check -- github_token_env is not set in the file" in done.stdout
    # F-13: the old key is told as old, never as something to set, and has no environment line
    assert "gitlab_token_env = (not set)  [old key: only the GitLab backend reads it]" in done.stdout
    assert "refused: gitlab_token_env" not in done.stdout and "none to check -- gitlab_token_env" not in done.stdout
    assert [ln for ln in done.stdout.splitlines() if "GITHUB_TOKEN" in ln] == []      # not shown as in use, not probed
    # the stderr WARN of the same run agrees: no "default is in use" sentence about a token key
    assert not [ln for ln in done.stderr.splitlines() if "token_env" in ln and "is in use" in ln]


def test_cli_says_set_and_never_prints_the_value(tmp_path):
    put(tmp_path, full_text(github_token_env=TOKEN_VAR))
    done = run_script(tmp_path, {TOKEN_VAR: SECRET})
    assert done.returncode == 0 and done.stderr == ""
    assert "environment variable %s: SET" % TOKEN_VAR in done.stdout
    assert "github_token_env = %s  [file]" % TOKEN_VAR in done.stdout
    assert SECRET not in done.stdout and SECRET not in done.stderr
    unset = run_script(tmp_path)
    assert "environment variable %s: NOT SET" % TOKEN_VAR in unset.stdout


def test_cli_refusal_exits_2_with_the_message_on_stderr(tmp_path):
    put(tmp_path, "developer: Devtwo\n")
    done = run_script(tmp_path)
    assert done.returncode == 2 and done.stdout == ""
    assert "is not a slug" in done.stderr and "Traceback" not in done.stderr


def test_cli_takes_no_arguments_and_help_works(tmp_path):
    put(tmp_path, full_text())
    helped = run_script(tmp_path, args=("--help",))
    assert helped.returncode == 0 and "usage: dev_config.py" in helped.stdout and "developer =" not in helped.stdout
    for args in (("--verbose",), ("extra",)):
        refused = run_script(tmp_path, args=args)
        assert refused.returncode == 2 and refused.stdout == "" and "usage: dev_config.py" in refused.stderr


def test_main_returns_2_on_refusal_and_0_on_a_good_file(tmp_path, capsys):
    assert dev_config.main([], root=put(tmp_path, "developer: Bad\n")) == 2
    assert "is not a slug" in capsys.readouterr().err
    assert dev_config.main([], root=put(tmp_path, "developer: fine\n")) == 0


def test_main_refuses_an_argument_with_exit_2(tmp_path):
    with pytest.raises(SystemExit) as info:
        dev_config.main(["--nope"], root=put(tmp_path, full_text()))
    assert info.value.code == 2


# --- F0-6 part 2 (t-584): the token-variable shape, the test doors, and paths.BASE from the config ----------

REPO = HERE.parent
MEASURERS = REPO / "experiments" / "measurers"
TOKEN_LOOKING = "glpat-" + "abcdefghijklmnopqrstuvwxyz0123456789ab"


@pytest.fixture(autouse=True)
def _no_ambient_door(monkeypatch):
    """A developer's own QA_DEV_CONFIG must not leak into these tests."""
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)


@pytest.mark.parametrize("value", ["glvar_lower", "GITLAB-TOKEN", "1TOKEN", "A" * 65, TOKEN_LOOKING])
def test_token_env_that_is_not_a_variable_name_is_refused_without_echoing_it(tmp_path, value):
    text = refusal(put(tmp_path, "gitlab_token_env: '%s'\n" % value))
    assert "gitlab_token_env" in text and "[A-Z][A-Z0-9_]{0,63}" in text
    assert value not in text
    run = run_script(tmp_path)
    assert run.returncode == 2
    assert value not in run.stdout and value not in run.stderr and "gitlab_token_env" in run.stderr


@pytest.mark.parametrize("value", ["G", "GITLAB_TOKEN", "MY_TOKEN_2", "A" * 64])
def test_token_env_names_at_the_boundary_are_accepted(tmp_path, value):
    assert dev_config.load(put(tmp_path, "gitlab_token_env: %s\n" % value))["gitlab_token_env"] == value


def door_file(tmp_path, text="developer: viaenv\n"):
    path = tmp_path / "door" / "other.yaml"
    path.parent.mkdir(exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_env_door_wins_over_the_default_location(tmp_path, monkeypatch, capsys):
    root = put(tmp_path, "developer: indefault\n")
    monkeypatch.setenv("QA_DEV_CONFIG", str(door_file(tmp_path, full_text(developer="viaenv"))))
    cfg = dev_config.load(root)
    assert cfg["developer"] == "viaenv" and cfg["path"] == str(tmp_path / "door" / "other.yaml")
    assert capsys.readouterr().err == ""


def test_explicit_path_wins_over_the_env_door(tmp_path, monkeypatch):
    monkeypatch.setenv("QA_DEV_CONFIG", str(door_file(tmp_path)))
    explicit = tmp_path / "explicit.yaml"
    explicit.write_text("developer: explicit\n", encoding="utf-8")
    cfg = dev_config.load(tmp_path, path=explicit)
    assert cfg["developer"] == "explicit" and cfg["path"] == str(explicit)


def test_empty_env_door_is_unset(tmp_path, monkeypatch):
    monkeypatch.setenv("QA_DEV_CONFIG", "")
    cfg = dev_config.load(put(tmp_path, "developer: indefault\n"))
    assert cfg["developer"] == "indefault"


def test_explicit_path_that_is_not_a_file_is_a_refusal_naming_the_source(tmp_path, capsys):
    missing = tmp_path / "nowhere.yaml"
    with pytest.raises(dev_config.DevConfigError) as info:
        dev_config.load(path=missing)
    assert "load()" in str(info.value) and str(missing) in str(info.value) and "not a file" in str(info.value)
    assert capsys.readouterr().err == ""                           # a refusal, not a WARN with defaults


def test_env_door_that_is_not_a_file_is_a_refusal_naming_the_variable(tmp_path, monkeypatch, capsys):
    for target in (tmp_path / "nowhere.yaml", tmp_path):           # a missing file, and a folder
        monkeypatch.setenv("QA_DEV_CONFIG", str(target))
        with pytest.raises(dev_config.DevConfigError) as info:
            dev_config.load(put(tmp_path, full_text()))
        assert str(info.value) == ("QA_DEV_CONFIG points to %s, which is not a file; set it to your config or "
                                   "unset it" % target)
    assert capsys.readouterr().err == ""


def test_the_default_location_alone_falls_back_with_the_warn(tmp_path, capsys):
    cfg = dev_config.load(tmp_path)
    assert capsys.readouterr().err.count("WARN") == 1 and cfg["source"] == "defaults"


def test_cli_env_door_that_is_not_a_file_exits_2(tmp_path):
    run = run_script(tmp_path, {"QA_DEV_CONFIG": str(tmp_path / "nowhere.yaml")})
    assert run.returncode == 2 and run.stdout == "" and "QA_DEV_CONFIG points to" in run.stderr


def test_cli_source_line_prints_the_file_actually_used(tmp_path):
    put(tmp_path, "developer: indefault\n")
    door = door_file(tmp_path)
    run = run_script(tmp_path, {"QA_DEV_CONFIG": str(door)})
    assert run.returncode == 0 and "developer = viaenv  [file]" in run.stdout
    assert "source = file  (%s)" % door in run.stdout


def run_paths(env_extra, args=("-B",), cwd=MEASURERS, prelude="", code="import paths; import paths; print(paths.BASE)"):
    """`import paths` in a fresh interpreter, as a reader script does; returns the completed process."""
    env = {k: v for k, v in os.environ.items() if k not in ("QA_RUNS_BASE", "QA_DEV_CONFIG", "QA_RUNS_TABLE")}
    env.update(env_extra)
    return subprocess.run([sys.executable, *args, "-c", prelude + code], cwd=cwd, env=env,
                          capture_output=True, text=True)


def warns(run):
    return [line for line in run.stderr.splitlines() if line.startswith("WARN")]


def config_file(tmp_path, text):
    cfg = tmp_path / "c.yaml"
    cfg.write_text(text, encoding="utf-8")
    return cfg


def test_paths_base_takes_the_env_variable_first(tmp_path):
    cfg = config_file(tmp_path, "stand_copy_root: %s\n" % (tmp_path / "cfgroot"))
    run = run_paths({"QA_RUNS_BASE": str(tmp_path / "env"), "QA_DEV_CONFIG": str(cfg)})
    assert run.returncode == 0 and run.stdout.strip() == str(tmp_path / "env") and warns(run) == []


def test_paths_base_empty_env_variable_is_unset(tmp_path):
    cfg = config_file(tmp_path, "stand_copy_root: %s\n" % (tmp_path / "cfgroot"))
    run = run_paths({"QA_RUNS_BASE": "", "QA_DEV_CONFIG": str(cfg)})
    assert run.stdout.strip() == str(tmp_path / "cfgroot")


def test_paths_base_comes_from_the_config_without_a_warn(tmp_path):
    cfg = config_file(tmp_path, full_text(stand_copy_root=str(tmp_path / "cfgroot")))
    run = run_paths({"QA_DEV_CONFIG": str(cfg)})
    assert run.returncode == 0 and run.stdout.strip() == str(tmp_path / "cfgroot") and run.stderr == ""


def test_paths_base_relative_value_resolves_against_the_repo_not_the_cwd(tmp_path):
    """F-12: the example's `../stand` is read from any cwd as <repo>/../stand, in both forms of the value."""
    expected = os.path.normpath(REPO / ".." / "stand")
    for cwd in (MEASURERS, tmp_path):
        run = run_paths({"QA_DEV_CONFIG": str(config_file(tmp_path, full_text(stand_copy_root="../stand")))},
                        cwd=cwd, prelude="import sys; sys.path.insert(0, %r); " % str(MEASURERS))
        assert run.returncode == 0 and run.stdout.strip() == expected, run.stderr
    assert ".." not in Path(expected).parts
    absolute = tmp_path / "abs"
    run = run_paths({"QA_DEV_CONFIG": str(config_file(tmp_path, full_text(stand_copy_root=str(absolute))))})
    assert run.stdout.strip() == str(absolute)                       # an absolute value is untouched


@pytest.mark.parametrize("script", ["prepare_copy.py", "run_headless.py"])
def test_writers_help_works_with_no_stand_copy_root(tmp_path, script):
    """F-14: the guard runs after parse_args, so --help exits 0 with no config; a real run still refuses (above)."""
    cfg = config_file(tmp_path, "developer: someone\n")
    env = {**{k: v for k, v in os.environ.items() if k not in ("QA_RUNS_BASE", "QA_RUNS_TABLE")},
           "QA_DEV_CONFIG": str(cfg)}
    done = subprocess.run([sys.executable, "-B", str(MEASURERS / script), "--help"], cwd=MEASURERS, capture_output=True,
                          text=True, env=env)
    assert done.returncode == 0 and "usage:" in done.stdout


def test_paths_imports_silently_without_a_runs_table(tmp_path):
    """I2: with no QA_RUNS_TABLE (the developer's own stripped by run_paths) importing the measurers' paths module
    exits 0 and prints nothing on stderr -- the CI pin of the runs-table loader (experiments/ is not run by CI)."""
    run = run_paths({"QA_RUNS_BASE": str(tmp_path / "env")}, code="import paths\nprint(paths.TABLE)\n")
    assert run.returncode == 0 and run.stdout.strip() == "{}" and run.stderr == ""


def test_paths_refuses_a_runs_table_that_is_not_a_file(tmp_path):
    """I1: a table that was asked for and is not there is a refusal naming the variable, never an empty table."""
    run = run_paths({"QA_RUNS_BASE": str(tmp_path / "env"), "QA_RUNS_TABLE": str(tmp_path / "nowhere.json")},
                    code="import paths\n")
    assert run.returncode != 0 and "QA_RUNS_TABLE" in run.stderr


def test_paths_base_trailing_separator_is_normalised_not_refused(tmp_path):
    cfg = config_file(tmp_path, "stand_copy_root: '%s%s'\n" % (tmp_path / "cfgroot", os.sep))
    run = run_paths({"QA_DEV_CONFIG": str(cfg)})
    assert run.returncode == 0 and run.stdout.strip() == str(tmp_path / "cfgroot")


def test_paths_base_door_that_is_not_a_file_fails_loudly(tmp_path):
    run = run_paths({"QA_DEV_CONFIG": str(tmp_path / "nowhere.yaml")})
    assert run.returncode != 0 and "QA_DEV_CONFIG points to" in run.stderr and warns(run) == []


def test_paths_base_with_no_key_imports_and_require_base_refuses(tmp_path):
    """F-9 (lead decision): BASE stays a Path -- 12 measurers read it at import -- and is a folder that must never
    be created; importing does not fail; require_base() refuses naming what to set; the writers call it first."""
    cfg = config_file(tmp_path, "developer: someone\n")
    no_base = str(REPO / ".no-stand-copy-root")
    code = ("import paths; import paths\nprint(paths.BASE)\n"
            "try:\n    paths.require_base()\nexcept paths.BaseNotSet as exc:\n    print(exc)\n")
    run = run_paths({"QA_DEV_CONFIG": str(cfg)}, code=code)
    assert run.returncode == 0
    assert run.stdout.splitlines() == [no_base, "set stand_copy_root in tools/dev.config.yaml or QA_RUNS_BASE"]
    assert len(warns(run)) == 3 and "`stand_copy_root`" in run.stderr    # `import paths` twice: still three
    assert not Path(no_base).exists()                                    # reading it never creates it
    set_by_env = run_paths({"QA_DEV_CONFIG": str(cfg), "QA_RUNS_BASE": str(tmp_path / "env")},
                           code="import paths\nprint(paths.require_base())\n")
    assert set_by_env.stdout.strip() == str(tmp_path / "env")
    for script, extra in (("prepare_copy.py", []), ("run_headless.py", ["--out", str(tmp_path / "o")])):
        # the writers refuse before they write (right after parsing: F-14), each with its own valid arguments
        done = subprocess.run([sys.executable, "-B", str(MEASURERS / script), "--name", "x", *extra],
                              cwd=MEASURERS, capture_output=True, text=True,
                              env={**{k: v for k, v in os.environ.items() if k not in ("QA_RUNS_BASE", "QA_RUNS_TABLE")},
                                   "QA_DEV_CONFIG": str(cfg)})
        assert done.returncode == 2 and "set stand_copy_root in tools/dev.config.yaml or QA_RUNS_BASE" in done.stderr
    assert not Path(no_base).exists()


@pytest.mark.parametrize("text,key", [("stand_copy_root: ''\n", "stand_copy_root"),
                                      ("github_token_env: not-a-name\n", "github_token_env"),
                                      ("stand_copy_root: [unclosed\n", "dev.config.yaml")])
def test_paths_base_malformed_config_fails_loudly_with_the_refusal(tmp_path, text, key):
    run = run_paths({"QA_DEV_CONFIG": str(config_file(tmp_path, text))})
    assert run.returncode != 0 and "DevConfigError" in run.stderr and key in run.stderr


def test_paths_base_refusal_is_the_real_dev_config_error_and_sys_path_is_restored(tmp_path):
    code = ("import sys\nbefore = list(sys.path)\n"
            "try:\n    import paths\nexcept Exception as exc:\n    import dev_config\n"
            "    print(isinstance(exc, dev_config.DevConfigError), sys.path == before)\n")
    run = run_paths({"QA_DEV_CONFIG": str(config_file(tmp_path, "stand_copy_root: [x\n"))}, code=code)
    assert run.stdout.split() == ["True", "True"], run.stderr
    ok = run_paths({"QA_DEV_CONFIG": str(config_file(tmp_path, full_text()))},
                   code="import sys\nbefore = list(sys.path)\nimport paths\nprint(sys.path == before)\n")
    assert ok.stdout.split() == ["True"], ok.stderr


def test_paths_imports_without_pyyaml(tmp_path):
    """The config reader is stdlib-only: a missing pyyaml is not an import-time failure of every measurer."""
    cfg = config_file(tmp_path, full_text(stand_copy_root=str(tmp_path / "cfgroot")))
    run = run_paths({"QA_DEV_CONFIG": str(cfg)}, prelude="import sys; sys.modules['yaml'] = None; ")
    assert run.returncode == 0 and run.stdout.strip() == str(tmp_path / "cfgroot") and run.stderr == ""


def test_paths_base_isolated_mode_still_finds_dev_config(tmp_path):
    """-I drops cwd and PYTHON* from sys.path; the config module is found from REPO, and a module called
    dev_config planted ahead of everything on sys.path does not shadow it."""
    (tmp_path / "dev_config.py").write_text("raise SystemExit('shadow loaded')\n", encoding="utf-8")
    cfg = config_file(tmp_path, "stand_copy_root: %s\n" % (tmp_path / "cfgroot"))
    prelude = "import sys; sys.path[:0] = [%r, %r]; " % (str(tmp_path), str(MEASURERS))
    run = run_paths({"QA_DEV_CONFIG": str(cfg)}, args=("-I", "-B"), cwd=tmp_path, prelude=prelude)
    assert run.returncode == 0 and run.stdout.strip() == str(tmp_path / "cfgroot")
