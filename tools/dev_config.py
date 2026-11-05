"""dev_config.py -- the one reader of tools/dev.config.yaml: the per-developer settings (team-work plan 3.6,
node F0-6; B-162, B-267; GM1-2).

  python tools/dev_config.py        prints each key, its value and where it came from (file / default / absent)

  from dev_config import load, developer_slug
  cfg = load()                      keys: developer, stand_copy_root, release_repo_root (each None when not set),
                                    github_token_env, gitlab_token_env (None when not set), source ("file" /
                                    "defaults"), path
  slug, reason = developer_slug()   the developer's slug and "", or None and a one-line reason (the one reader
                                    for everything that needs "who am I": the per-developer journal)

The real file `tools/dev.config.yaml` is git-ignored; `tools/dev.config.example.yaml` is its template. Only
`github_token_env` has a default (GITHUB_TOKEN), and only when there is NO file; no path and no developer is ever
guessed: a key that is not set is None, and whatever needs it checks at use. With no file there is ONE WARN line on
stderr. A token variable has no default in a file that exists (NO_DEFAULT_IN_A_FILE: its readers refuse such a
file, so the token of one host never goes to another), and the WARN and the CLI say that, never "the default is in
use" (F-8, FX-1). A key missing from a file that exists gets one WARN line naming it.

Old files keep working: LEGACY_KEYS are accepted. `public_skills_root` is read as `release_repo_root` (one WARN
says to rename it; if both are given the new one wins, one WARN, the values are not printed); `gitlab_token_env`
is read as it was (cfg["gitlab_token_env"], checked for shape like the new token key) for the GitLab backend that
still exists. A malformed file, an unknown key (a typo), an empty value, a slug that is not a file name or a config
door that points nowhere is a refusal: DevConfigError when imported, exit 2 when run.

The file is read with the standard library only (no pyyaml: every measurer imports this through paths.py). Its
grammar is a flat mapping of text values, one `key: value` per line: a value may stand in single or
double quotes (the quotes are only stripped, nothing inside them is an escape, so a Windows path is written as it
is), `#` starts a comment on a line of its own or after a space behind the value (inside quotes it is text), blank
lines, a leading BOM and CRLF are fine. Anything else -- a nested key, a list, an indented line, a tab, a
duplicate key, a line without `:` -- is refused naming the line number (never the value).

Which file is read (first match wins):
  load(path=...)               an explicit file: the test door
  QA_DEV_CONFIG                an environment variable holding a file path (empty = unset): a per-process door,
                               so a test or a one-off run reads another file without touching the real one
  <root>/tools/dev.config.yaml the default; root is the repository this file sits in unless load(root) says
                               otherwise
An explicit path or a QA_DEV_CONFIG that is not a file is a refusal naming its source; only the default location
falls back to the defaults with the WARN. The CLI's `source =` line prints the file actually used.

`developer` is a slug: SLUG_RE (the same bound as journal_keys.LABEL_RE, 24 characters at most); `main` is
reserved. A token key is the NAME of an environment variable (capitals, digits and '_', starting with a
capital letter, at most 64 characters: TOKEN_ENV_RE); a value that is not of that shape -- a token pasted by
mistake included -- is refused without echoing it (this holds for `github_token_env` and `gitlab_token_env`
alike). The CLI says whether such a variable is SET or NOT SET and never prints its value (same discipline as
tools/ci_read.py). `stand_copy_root` and `release_repo_root` are not checked for existence here: the scripts that
use them check at use. Paths are taken as given (no normalisation)."""

import argparse
import os
import re
import sys
from pathlib import Path

KEYS = ("developer", "stand_copy_root", "release_repo_root", "github_token_env")
LEGACY_KEYS = {"public_skills_root": "release_repo_root", "gitlab_token_env": None}   # old name -> new name / kept
TOKEN_KEYS = ("github_token_env", "gitlab_token_env")
DEFAULTS = {"github_token_env": "GITHUB_TOKEN"}   # no path and no developer is ever guessed: None when not set
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,23}$")
NO_DEFAULT_IN_A_FILE = ("github_token_env", "gitlab_token_env")   # a default applies only when there is NO file
ACCEPTED_KEYS = KEYS + tuple(LEGACY_KEYS)
RESERVED_SLUGS = frozenset({"main"})
TOKEN_ENV_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
LINE_SPLIT_RE = re.compile(r"\r\n|\r|\n")
INLINE_COMMENT_RE = re.compile(r"\s#")
FLOW_OPENERS = "[{|>"
ENV_DOOR = "QA_DEV_CONFIG"
CONFIG_NAME = "dev.config.yaml"
EXAMPLE_NAME = "dev.config.example.yaml"


class DevConfigError(ValueError):
    """The config file cannot be used; the message says what is wrong, what was expected, how to pass."""


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _locate(root, path):
    """(file, door): the file to read and the door that chose it (None = the default location)."""
    if path is not None:
        return Path(path), "path"
    door = os.environ.get(ENV_DOOR)
    if door:
        return Path(door), ENV_DOOR
    return Path(root if root is not None else _default_root()) / "tools" / CONFIG_NAME, None


def _refusal(path: Path, wrong: str, expected: str, line=None) -> DevConfigError:
    where = CONFIG_NAME if line is None else "%s line %d" % (CONFIG_NAME, line)
    return DevConfigError("%s: %s; expected %s. Fix it in %s (template: tools/%s), or delete the file to use "
                          "the defaults." % (where, wrong, expected, path, EXAMPLE_NAME))


def _scalar(raw: str):
    """(value, problem) for the text after `key:`; the problem is None when the value is fine."""
    raw = raw.strip()
    if raw[:1] in ("'", '"'):
        end = raw.find(raw[0], 1)
        if end < 0:
            return None, "a quote that is opened and not closed"
        rest = raw[end + 1:]
        if rest.strip() and not (rest[0].isspace() and rest.strip().startswith("#")):
            return None, "text after the closing quote"
        return raw[1:end], None
    if raw and raw[0] in FLOW_OPENERS:
        return None, ("a list, a mapping or a block scalar (write the text itself, in quotes if it starts with %s)"
                      % " ".join(FLOW_OPENERS))
    if raw.startswith("#"):
        return "", None
    return INLINE_COMMENT_RE.split(raw, 1)[0].strip(), None


def _parse_line(path: Path, number: int, line: str, found: dict) -> None:
    """Add the `key: value` of one line to `found` as key -> (value, line number); a refusal otherwise."""
    shape = "lines of the form `key: value` with the keys %s" % ", ".join(ACCEPTED_KEYS)
    if line[0] in " \t":
        raise _refusal(path, "a tab-indented line" if line[0] == "\t"
                       else "an indented line (nested keys and continuations are not supported)",
                       "flat `key: value` lines starting in column 1", number)
    key, colon, rest = line.partition(":")
    key = key.rstrip()
    if not colon:
        raise _refusal(path, "a line without `:`", shape, number)
    if not KEY_RE.fullmatch(key):
        raise _refusal(path, "something that is not a key name before the first `:`", shape, number)
    if key not in ACCEPTED_KEYS:
        raise _refusal(path, "unknown key %r" % key, "only the keys %s" % ", ".join(ACCEPTED_KEYS), number)
    if rest and not rest[0].isspace():
        raise _refusal(path, "the key %r has no space after the `:`" % key, "`%s: value`" % key, number)
    if key in found:
        raise _refusal(path, "the key %r is given twice (first on line %d)" % (key, found[key][1]),
                       "each key once", number)
    value, problem = _scalar(rest)
    if problem:
        raise _refusal(path, "the key %r has %s" % (key, problem), "a single text value", number)
    if not value.strip():
        raise _refusal(path, "the key %r has an empty value" % key,
                       "a non-empty text value (a path, a slug or an environment variable name)", number)
    found[key] = (value, number)


def _parse(path: Path):
    """{key: (value, line number)}; empty when the file holds nothing (empty or only comments)."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (UnicodeDecodeError, OSError) as exc:
        raise _refusal(path, "cannot be read (%s)" % type(exc).__name__,
                       "a UTF-8 text file of lines `key: value` with the keys %s" % ", ".join(ACCEPTED_KEYS)) from None
    found = {}
    for number, line in enumerate(LINE_SPLIT_RE.split(text), start=1):
        if line.strip() and not line.strip().startswith("#"):
            _parse_line(path, number, line, found)
    return found


def _check(path: Path, data: dict) -> None:
    slug, slug_line = data.get("developer", (None, None))
    if slug in RESERVED_SLUGS:
        raise _refusal(path, "developer %r is a reserved word" % slug,
                       "your own slug, not one of %s" % ", ".join(sorted(RESERVED_SLUGS)), slug_line)
    if slug is not None and not SLUG_RE.fullmatch(slug):
        raise _refusal(path, "developer %r is not a slug" % slug,
                       "lowercase letters, digits and '-', starting with a letter, 2 to 24 characters "
                       "(%s): it becomes a file name" % SLUG_RE.pattern, slug_line)
    for key in TOKEN_KEYS:
        token_env, token_line = data.get(key, (None, None))
        if token_env is not None and not TOKEN_ENV_RE.fullmatch(token_env):
            # the value is not echoed: it may be a token pasted by mistake
            raise _refusal(path, "the key %r is not the name of an environment variable" % key,
                           "the NAME of the variable that holds the token, not the token: capitals, digits and "
                           "'_', starting with a capital letter, at most 64 characters (%s)" % TOKEN_ENV_RE.pattern,
                           token_line)


def refused_default(key: str, cfg: dict, origins: dict) -> bool:
    """True when `key` is a NO_DEFAULT_IN_A_FILE key that a file which EXISTS does not name: its default is not in
    use -- whatever needs the key refuses (the one truth for the WARN, the CLI and the token readers)."""
    return key in NO_DEFAULT_IN_A_FILE and origins[key] != "file" and Path(cfg["path"]).is_file()


def _missing_key_warning(key: str, path: Path) -> str:
    return ("WARN %s has no `%s` at %s: it has no default, so whatever needs it refuses until you set it "
            "(see tools/%s)\n" % (CONFIG_NAME, key, path, EXAMPLE_NAME))


def _legacy_warning(path: Path, data: dict) -> str:
    """One WARN line when the file says `public_skills_root` (the values are never printed), else ''."""
    if "public_skills_root" not in data:
        return ""
    if "release_repo_root" in data and data["release_repo_root"][0] != data["public_skills_root"][0]:
        return ("WARN %s at %s names both `release_repo_root` and `public_skills_root` with different values: "
                "`release_repo_root` is used; delete `public_skills_root`\n" % (CONFIG_NAME, path))
    return ("WARN %s at %s: rename `public_skills_root` to `release_repo_root` (the old name is still read)\n"
            % (CONFIG_NAME, path))


def _not_a_file(path: Path, door: str) -> DevConfigError:
    if door == ENV_DOOR:
        return DevConfigError("%s points to %s, which is not a file; set it to your config or unset it"
                              % (ENV_DOOR, path))
    return DevConfigError("the config path passed to load() is %s, which is not a file; pass your config file "
                          "or leave the path out" % path)


def _read(root, path):
    """(config, origins, warnings): resolve() without the printing."""
    path, door = _locate(root, path)
    warnings, data = [], {}
    if path.is_file():
        data = _parse(path)
        if not data:
            warnings.append("WARN %s is empty at %s: no key is set, and %s have no default in a file that exists, so "
                            "whatever needs them refuses until you set them (fill it from tools/%s)\n"
                            % (CONFIG_NAME, path, ", ".join(NO_DEFAULT_IN_A_FILE), EXAMPLE_NAME))
        else:
            _check(path, data)
            legacy = _legacy_warning(path, data)
            if legacy:
                warnings.append(legacy)
            # a path given through its old name is not missing
            renamed = {new for old, new in LEGACY_KEYS.items() if new and old in data}
            warnings.extend(_missing_key_warning(key, path) for key in KEYS
                            if key not in data and key not in renamed)
    elif door:
        raise _not_a_file(path, door)
    else:
        warnings.append("WARN %s not found at %s: no path is set (a path is never guessed), %s uses its default "
                        "(copy tools/%s)\n" % (CONFIG_NAME, path, "github_token_env", EXAMPLE_NAME))
    for old, new in LEGACY_KEYS.items():       # the new name wins; the old one fills in only when the new is absent
        if new and old in data and new not in data:
            data[new] = data[old]
    cfg = {key: DEFAULTS.get(key) for key in KEYS + ("gitlab_token_env",)}
    cfg.update({key: value for key, (value, _line) in data.items() if key in cfg})
    origins = {key: "file" if key in data else "default" if key in DEFAULTS else "absent" for key in cfg}
    cfg["source"] = "file" if data else "defaults"
    cfg["path"] = str(path)
    return cfg, origins, warnings


def resolve(root=None, path=None):
    """(config, origins): config as load() returns it, origins = key -> "file" / "default" / "absent"."""
    cfg, origins, warnings = _read(root, path)
    for warning in warnings:
        sys.stderr.write(warning)
    return cfg, origins


def load(root=None, path=None) -> dict:
    return resolve(root, path)[0]


def developer_slug(root=None, path=None):
    """(slug, reason): the developer's slug and "", or None and a one-line reason. Prints nothing: a caller that
    needs the slug often must not repeat the WARN lines of load()."""
    try:
        cfg = _read(root, path)[0]
    except DevConfigError as exc:
        return None, str(exc)
    if cfg["developer"] is not None:
        return cfg["developer"], ""
    if not Path(cfg["path"]).is_file():
        return None, "no config file at %s" % cfg["path"]
    return None, "developer key absent in %s" % cfg["path"]


def main(argv=None, root=None) -> int:
    argparse.ArgumentParser(prog="dev_config.py", description="Print each key of tools/dev.config.yaml, its "
                            "value and where it came from; no options.").parse_args(argv)
    try:
        cfg, origins = resolve(root)
    except DevConfigError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    for key in KEYS + ("gitlab_token_env",):
        if key == "gitlab_token_env" and cfg[key] is None:
            # the old key: only the GitLab backend reads it, so this line never tells anyone to set it (F-13);
            # refused_default stays for that backend and for github_token_env
            print("%s = (not set)  [old key: only the GitLab backend reads it]" % key)
        elif refused_default(key, cfg, origins):
            print("%s = (not set)  [refused: %s has no default in a file that exists, so whatever needs it refuses; "
                  "set it in tools/%s]" % (key, key, CONFIG_NAME))
        elif cfg[key] is None:
            print("%s = (not set)  [absent: set it in tools/%s]" % (key, CONFIG_NAME))
        else:
            print("%s = %s  [%s]" % (key, cfg[key], origins[key]))
    for key in TOKEN_KEYS:
        if key == "gitlab_token_env" and cfg[key] is None:
            continue                                  # no environment line for the old key when it is not set
        if refused_default(key, cfg, origins):
            print("environment variable: none to check -- %s is not set in the file" % key)
        elif cfg[key] is not None:
            state = "SET" if os.environ.get(cfg[key]) else "NOT SET"
            print("environment variable %s: %s" % (cfg[key], state))
    print("source = %s  (%s)" % (cfg["source"], cfg["path"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
