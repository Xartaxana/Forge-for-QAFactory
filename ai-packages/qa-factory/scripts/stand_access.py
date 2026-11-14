"""Log in to the stand the way THIS project logs in — the recorded scheme, never a guess.

Why. 23.09.2026, a second checkout of the same harness: every path of the stand answered
302 to an identity provider without a token, and the orchestrator reported "env_probe
(Layer 1) still failing ... HTTP 302 on all endpoints ... likely clears once the auth
credentials above are in place". Nothing in the factory had ever tried to log in, so the
sentence was a guess dressed as a diagnosis. A stand is three separate facts — is it
answering, did we get in, are the keys there — and only the second one needs a login recipe.

The recipe is a fact of the project, recorded at onboarding as `environment.access`:

    "access": {
      "kind": "harness_command" | "local_login" | "oidc_password" | "bearer_env" | "form_login" | "ui_only" | "none",
      "command": "<shell command, for harness_command>",
      "url": "<login or token endpoint, or the NAME of the key that holds it; for form_login the base address, empty =
               the stand's own>",
      "form": "<form_login: the id of a row of references/login-roads.json; empty = the first valid row>",
      "client_id_key": "", "realm_key": "", "user_key": "", "secret_key": "",
      "user_field": "" (local_login: the JSON body field the endpoint expects; empty = the probe tries the
                        pairs of references/login-body-fields.json in order and reports the accepted one),
      "secret_field": "" (local_login: likewise),
      "token_key": "<for bearer_env>", "unauth_status": [302, 401],
      "login_probe": {"user_key": "", "status": 200, "checked_at": "<ISO>",
                      "outcome": "ok|failed|skipped|not_recorded" (what the login came to; only `ok` is a proof - a
                                 record without it predates the field and is not confirmed),
                      "answer": a word of ANSWERS (WHAT the attempt came to; absent = the record predates the field and
                                 is never guessed),
                      "user_field": "" (optional), "secret_field": "" (optional),
                      "seconds": <float> (harness_command only: how long the ok login took; the ceiling of the next
                                 login is twice it, 60..300 s; absent = 300 s)}
                      (`env_probe.py --json` emits this object whole as `login.record`)
    }

Every value here is a key NAME or a URL. No value of a secret is read from config, printed,
or stored: the receipt this module returns carries the NAME of the user key and a status
code, which is what a person needs to tell "wrong account" from "wrong password" from
"the stand never asked".

An identity provider is one instance of `oidc_password`, not the design: a project that
issues its own token, or whose own harness knows how to log in, is served by the other
kinds. When the harness can log in by itself, the factory calls IT rather than
reimplementing a protocol it would get subtly wrong.

Every receipt carries `answer` (one word of ANSWERS: what ONE attempt came to) and `source` (who recorded the way:
`access`, or `registry` for a way a story found). `in` is decided HERE, by positive proof only (a non-empty string
token, a form session with a value, a harness exit 0, a bearer 2xx), before any table is read; every other HTTP answer
is worded by the `login_answers` rows of references/stand-answers.json, read through `env_probe` (`answer_of`), and an
unreadable table reads as `unjudged`, never as a refusal. `try_roads` / `--roads` runs every road the project could
sign in by and reports what each answered; it writes nothing.

Note the double import: run as `python stand_access.py`, `import env_probe` loads a SECOND copy of this module under its
own name; both read the same files, so their answers agree.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import re
import secrets as _secrets
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

KINDS = ("harness_command", "local_login", "oidc_password", "bearer_env", "form_login", "ui_only", "none")
# What ONE sign-in attempt came to (FV1-17a): the one tuple; config_contract.LOGIN_ANSWERS is this object.
ANSWERS = ("in", "credentials_refused", "fields_unconfirmed", "body_shape", "wrong_door", "unjudged", "throttled",
           "stand_error", "no_answer", "did_not_finish", "command_failed", "command_missing", "not_tried")
# The words a `login_answers` row of references/stand-answers.json may give: the rest are decided by the code that saw the
# proof or the exception (`in`, `no_answer`, `body_shape`, the three command words, `not_tried`).
TABLE_ANSWERS = ("credentials_refused", "fields_unconfirmed", "wrong_door", "unjudged", "throttled", "stand_error")
NOT_RECORDED_WHY = "schema not recorded - onboarding gap"
WRONG_DOOR_WHY = " - the address answered, but its answer does not look like a sign-in"
UNJUDGED_WHY = " - its answer does not show whether a sign-in is there"
# The roads run (FV1-17a, §2.3): what a run may spend on the account, and the ceilings the data may not raise.
LOGIN_ROADS_PATH = Path(__file__).resolve().parents[1] / "references" / "login-roads.json"
REAL_SECRET_FAILURES_CEILING = 3
CANDIDATES_CEILING = 5
FORMS_CEILING = 20
BUDGET_DEFAULTS = {"real_secret_failures": 1, "candidates": CANDIDATES_CEILING}
# The answers that cost the account an attempt (a road that sent the real secret and did not get in, nor was it the wrong door).
SPENDING_ANSWERS = ("credentials_refused", "fields_unconfirmed", "body_shape", "unjudged", "stand_error", "no_answer",
                    "did_not_finish", "command_failed")
FORM_REQUESTS_MAX = 3
BODY_MAX = 262144
# A login that answers with one of these carries a session we can prove. `data`/`result` are
# unwrapped one level: a wrapper object is the commonest shape after a bare token.
TOKEN_FIELDS = ("access_token", "accessToken", "token", "id_token", "idToken", "jwt")
ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# The data row of the shapes a 400/422 login answer names its complained body fields in (OH3-10, FR-13).
LOGIN_ERROR_SHAPES_PATH = Path(__file__).resolve().parents[1] / "references" / "login-error-shapes.json"
# A command login is a whole test-harness start-up, not one request: five seconds is the
# budget of an HTTP probe and would call a healthy harness broken.
COMMAND_MIN_TIMEOUT_S = 60.0
# RN1-3: the ceiling of the next harness login is twice the duration the onboarding recorded, kept inside [60, 300] s; with no
# usable record it is the declared default (300 s, half the host's 600 s call limit), never the floor - an 80 s harness is not "broken".
COMMAND_TIMEOUT_FACTOR = 2.0
COMMAND_MAX_TIMEOUT_S = 300.0
COMMAND_UNRECORDED_TIMEOUT_S = 300.0


def recorded_seconds(access):
    """`access.login_probe.seconds` when it is an int or float (not a bool), finite and > 0, else None. The ONE validity test of
    the field (AR-13): absent, 0, negative, a string, NaN, Infinity and a `login_probe` that is not an object are all None."""
    probe = access.get("login_probe") if isinstance(access, dict) else None
    value = probe.get("seconds") if isinstance(probe, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) and value > 0 else None


def command_timeout(access, timeout) -> float:
    """The ceiling, in seconds, of one harness-command login: twice the recorded duration (at least 60), 300 when none is
    recorded; the caller's `timeout` may raise it; the cap binds every input, so the result is always inside [60, 300]."""
    seconds = recorded_seconds(access)
    wanted = (COMMAND_UNRECORDED_TIMEOUT_S if seconds is None
              else max(COMMAND_MIN_TIMEOUT_S, COMMAND_TIMEOUT_FACTOR * seconds))
    return min(COMMAND_MAX_TIMEOUT_S, max(float(timeout), wanted))


def _safe(url: str) -> str:
    """A URL with the userinfo, query and fragment removed — the same rule `stand_health`
    prints by. A stand address routinely carries credentials in one of the three."""
    try:
        parts = urlsplit(str(url))
        host = parts.hostname or ""
        if parts.port:
            host += f":{parts.port}"
        return urlunsplit((parts.scheme, host, parts.path, "", "")) or "(no url)"
    except ValueError:
        return "(unprintable url)"


def _value(values: dict, key: str) -> str:
    return str((values or {}).get(str(key or ""), "") or "").strip()


def resolve_url(raw: str, values: dict, base_url: str = "") -> str:
    """A URL from config, from the key it names, or glued to the stand's address.

    `url` is allowed to be a key NAME because that is where a project usually keeps the
    address of its identity provider — the same place the harness reads it from, so the two
    can never drift apart."""
    raw = str(raw or "").strip()
    if not raw:
        return ""
    if raw.lower().startswith(("http://", "https://")):
        return raw
    if ENV_NAME.match(raw):
        return _value(values, raw)
    if raw.startswith("/") and base_url:
        return base_url.rstrip("/") + raw
    return ""


def _exchange(url: str, method: str, data: bytes | None, headers: dict, timeout: float, expect: str = "any"):
    """The `http_client.Answer` of one request (status, headers, body), redirects NOT followed. Raises when nothing
    answered, and when the body of a 2xx did not arrive: the helper keeps the status and says `unreadable`, but a stalled
    2xx body was always a timeout of the login (`NO ANSWER`), and a form road must not read it as an answer either (B-408
    F1). The ONE place the body limit and that rule live; `_open` and the form road both go through it."""
    import http_client
    answer = http_client.fetch(url, method=method, data=data, headers=headers, timeout=timeout, max_body=BODY_MAX,
                               expect=expect)
    if answer.unreadable and 200 <= answer.status < 300:
        raise TimeoutError("the body of the answer did not arrive")
    return answer


def _open(url: str, method: str, data: bytes | None, headers: dict, timeout: float) -> tuple:
    """(code, body) of one request, redirects NOT followed. Raises when nothing answered.

    Mirrors `gate_preflight.http_get`: following a redirect lands on a login page and
    reports 200, which is the probe artifact that once recorded a healthy stand as dead.
    B-408: through the factory's one HTTP helper (its User-Agent), and the body of an ERROR answer is kept too
    (it used to be dropped), so a failed login can say what answered."""
    answer = _exchange(url, method, data, headers, timeout)
    return (answer.status, answer.body.decode("utf-8", errors="replace"))


def _who_answered(code, text: str, secrets: tuple, expect: str = "json") -> str:
    """` (the answer is ...)` when what came back is NOT shown to be the stand's own (a page, a JSON no known message
    key is in, a text), else ``. The body is classified with no headers - this seam carries none (E11) - so nobody is
    named as the author. The credential values this call used are redacted from what is said."""
    import http_client
    said = http_client.unattributed(code, str(text or ""), None, expect=expect, secrets=secrets)
    return f" (the answer: {said})" if said else ""


def _scrub(text: str, secrets) -> str:
    """`text` with every non-empty value of `secrets` (strings) replaced - longest first, so a value that holds another
    is gone whole. The last line of defence of a form road's `why` (the user, the secret, the csrf token and every cookie
    value); the texts built here name no value, this keeps one that arrives through an answer's title out as well."""
    for value in sorted({s for s in secrets or () if isinstance(s, str) and s}, key=len, reverse=True):
        text = text.replace(value, "***")
    return text


def _cause_of(exc) -> str:
    """The words class of an exception, from the ONE classifier (`env_probe.no_answer_cause`, the `no_answer` rows of
    references/stand-answers.json): `timeout`, `nothing_listens`, ... ; the class name when that cannot be read."""
    try:
        import env_probe
        return str(env_probe.no_answer_cause(exc).get("cause") or type(exc).__name__)
    except Exception:  # noqa: BLE001 - the words only; the answer is `no_answer` either way
        return type(exc).__name__


def answer_of(code, text, *, road: str, headers=None) -> str:
    """What an HTTP answer that is NOT a proof means, by the `login_answers` rows of references/stand-answers.json (FV1-17a).
    The caller has ALREADY checked the positive proof (a token, a session value, a bearer 2xx): no row yields `in`, and an
    unreadable table - or no row that fits - is `unjudged`, never a refusal and never a wrong door. Rows are matched by the
    ONE matcher `env_probe._row_takes` on the `http_client.classify` kind (`expect` json for a sign-in call, any for the
    bearer GET) and the road kind. Never returns `in`, `no_answer`, `body_shape`, `not_tried` or a command word."""
    try:
        import env_probe
        import http_client
        kind = http_client.classify(code, headers, text, expect="any" if road == "bearer_env" else "json")["kind"]
        tables = env_probe.stand_answers()
        if tables["table"] != "ok":
            return "unjudged"
        for row in tables["login_answers"]:
            if row.get("answer") in TABLE_ANSWERS and env_probe._row_takes(row, code, kind, road=road):   # a row giving `in` is ignored (I1)
                return row["answer"]
    except Exception:  # noqa: BLE001 - an answer this reader could not place is an unknown, the safe direction
        return "unjudged"
    return "unjudged"


def token_value(body: str):
    """The session token a login answer carries, else None - the ONE walk of the answer (AR-13): the top object, then its
    `data` and `result` wrappers, each by the names of TOKEN_FIELDS in order. A caller that only needs to know whether
    there is one asks `_token_in`; a caller that signs in with it (the manual capture) takes the value, and the value
    never goes into a receipt, a message or a file."""
    try:
        parsed = json.loads(body or "")
    except ValueError:
        return None
    for node in (parsed, (parsed or {}).get("data") if isinstance(parsed, dict) else None,
                 (parsed or {}).get("result") if isinstance(parsed, dict) else None):
        if isinstance(node, dict):
            for name in TOKEN_FIELDS:
                value = node.get(name)
                if isinstance(value, str) and value.strip():   # A3: `true`, a number, a list or an object is no token
                    return value.strip()
    return None


def _token_in(body: str) -> bool:
    """Whether the answer carries a session token - the same walk as `token_value`; nothing from the body is ever put
    into the receipt."""
    return token_value(body) is not None


def _receipt(status: str, why: str, code=None, user_key: str = "", *, answer: str) -> dict:
    """One receipt: the four-word `status`, and `answer` - what the attempt came to (a word of ANSWERS; required)."""
    return {"status": status, "code": code, "user_key": str(user_key or ""), "why": why, "answer": answer}


def _argv(command: str) -> list:
    """The command line as a list, the way `readiness.executable_of` reads one: split without
    POSIX escaping (a Windows path is full of backslashes) and then unquoted token by token."""
    try:
        parts = shlex.split(str(command or ""), posix=False)
    except ValueError:
        parts = str(command or "").split()
    return [p.strip('"').strip("'") for p in parts if p.strip()]


def _harness_command(access: dict, values: dict, timeout: float, cwd=None) -> dict:
    """The harness proves its own login: exit 0 and we are in.

    Its output is never shown. A login command routinely prints the token it just obtained,
    and this receipt travels into a role's context and from there into the transcript."""
    command = str(access.get("command") or "").strip()
    user_key = str(access.get("user_key") or "")
    if not command:
        return _receipt("not_recorded", "access.kind is harness_command but access.command is empty", answer="not_tried")
    argv = _argv(command)
    if not argv:
        return _receipt("not_recorded", "access.command is empty", answer="not_tried")
    child = dict(os.environ)
    child.update({k: v for k, v in (values or {}).items() if isinstance(v, str)})
    child["PYTHONDONTWRITEBYTECODE"] = "1"
    ceiling = command_timeout(access, timeout)
    started = time.monotonic()
    try:
        done = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=child, cwd=str(cwd) if cwd else None,
                              timeout=ceiling)
    except FileNotFoundError:
        return _receipt("failed", f"`{argv[0]}` is not on PATH - access.command names a program "
                                  "this machine does not have", answer="command_missing")
    except subprocess.TimeoutExpired:
        seconds = recorded_seconds(access)
        if seconds is None:
            why = (f"`{argv[0]}` did not finish within {int(ceiling)}s (no login duration is recorded in "
                   "environment.access.login_probe.seconds; run the onboarding's login proof to record one)")
        else:
            why = (f"`{argv[0]}` did not finish within {int(ceiling)}s (the login took ~{int(round(seconds))}s when onboarding "
                   "recorded it; the ceiling is twice that, at least 60s and at most 300s)")
        receipt = _receipt("failed", why, answer="did_not_finish")
        receipt["refusal"] = "timeout"
        return receipt
    except OSError as exc:
        return _receipt("failed", f"`{argv[0]}` could not be run ({type(exc).__name__})", answer="command_missing")
    if done.returncode == 0:
        receipt = _receipt("ok", f"the project's own login command `{argv[0]}` exited 0", None, user_key, answer="in")
        receipt["seconds"] = round(time.monotonic() - started, 1)   # only an ok login sets the next ceiling (RN1-3)
        return receipt
    return _receipt("failed", f"the project's own login command `{argv[0]}` exited "
                              f"{done.returncode}; its output is not shown here because a login "
                              "command prints tokens", None, user_key, answer="command_failed")


def _login_error_shapes() -> dict:
    """references/login-error-shapes.json - the data row of the shapes a 400/422 names its complained fields in. An
    unreadable or damaged file reads as no shapes: the receipt then says the status and names no field (FR-59)."""
    import hooklib  # the one JSON reader (AR-13); imported here like `http_client` below, so the module's import surface is unchanged
    return hooklib.read_json(LOGIN_ERROR_SHAPES_PATH, {}, kind=dict)


def _name_at(item, path) -> str:
    """The string at `path` (object keys) inside one list item; a list there yields its LAST string element (FastAPI's
    `loc` is [\"body\", \"email\"]). Empty when the item does not have that shape."""
    node = item
    for step in path:
        if not isinstance(node, dict) or not isinstance(step, str):
            return ""
        node = node.get(step)
    if isinstance(node, list):
        node = next((x for x in reversed(node) if isinstance(x, str)), "")
    return node if isinstance(node, str) else ""


def complained_fields(text: str, secrets: tuple = ()) -> list:
    """The body field NAMES a stand's 400/422 answer complains about, read through the shapes of
    references/login-error-shapes.json (OH3-10). NAMES only: a candidate must match the row's `name_pattern`, is not
    a place word (`body`, `query`), and contains none of the credential values this call used (a stand that echoed a
    value as a key would otherwise print it); at most the row's `max_names` come out, in the order the answer gave
    them. No other part of the answer is read out. Empty when the answer is not JSON or no shape in the row fits."""
    row = _login_error_shapes()
    limit, raw_pattern = row.get("max_names"), row.get("name_pattern")
    if not isinstance(raw_pattern, str) or not raw_pattern or not isinstance(limit, int) or isinstance(limit, bool) \
            or limit < 1:
        return []
    try:
        pattern = re.compile(raw_pattern)
    except re.error:
        return []
    try:
        parsed = json.loads(text or "")
    except ValueError:
        return []
    if not isinstance(parsed, dict):
        return []
    candidates: list = []
    for shape in row.get("shapes") or []:
        if not isinstance(shape, dict):
            continue
        where, path = shape.get("list") or shape.get("map"), shape.get("name_at")
        node = parsed.get(where) if isinstance(where, str) else None
        if shape.get("kind") == "list_item_path" and isinstance(node, list) and isinstance(path, list):
            candidates.extend(_name_at(item, path) for item in node)
        elif shape.get("kind") == "key_names" and isinstance(node, dict):
            candidates.extend(str(key) for key in node)
    places = {str(p).lower() for p in row.get("not_fields") or []}
    held = [s.lower() for s in secrets if isinstance(s, str) and s]
    names: list = []
    for name in candidates:
        if (name and name not in names and pattern.match(name) and name.lower() not in places
                and not any(value in name.lower() for value in held)):
            names.append(name)
    return names[:limit]


# FB-3 / FB-5: the one line a body-shape refusal ends in. A constant with no slot, at most 155 characters: the gate's
# `missing` environment note is shown cut at 160 (gate_preflight.check_stand), and the fix is the FIRST thing in it.
LOGIN_FIELD_FIX = ("login field name unknown: write the body field names the login endpoint expects into "
                   "environment.access.user_field / secret_field (qa-factory/config.json)")


def shape_refused(code, text: str, secrets: tuple = (), sent: tuple = ()) -> bool:
    """Whether a login answer asks for a body field that was NOT sent - the ONE rule that moves a login to its next pair.
    True only for a 400/422 whose answer names (through `complained_fields`) at least one field outside `sent`
    (case-insensitive). Everything else is False: another code, no answer, an answer naming nothing, naming only
    fields that were sent (a wrong password or a throttle judged the account - it is never re-sent), non-JSON."""
    if code not in (400, 422):
        return False
    held = {str(name).lower() for name in sent}
    return any(name.lower() not in held for name in complained_fields(text, secrets))


def try_body_pairs(candidates, send, secrets: tuple = ()) -> list:
    """The ONE attempt loop of a body-field login (the probe and the manual capture both call it). For each (user field,
    secret field) in order `send(u, s)` returns (code, text) or raises; an exception is no answer and ends the loop. The
    loop goes on only while the answer is `shape_refused`. Returns the attempts; `text` is the caller's own and never
    goes into a receipt or a message."""
    attempts: list = []
    for u, s in candidates:
        try:
            code, text = send(u, s)
        except Exception as exc:
            attempts.append({"user_field": u, "secret_field": s, "code": None, "error": type(exc).__name__,
                             "cause": _cause_of(exc)})
            break
        attempts.append({"user_field": u, "secret_field": s, "code": code, "text": text,
                         "complained": complained_fields(text, secrets) if code in (400, 422) else []})
        if not shape_refused(code, text, secrets, (u, s)):
            break
    return attempts


def ran_out_of_pairs(attempts: list, secrets: tuple = ()) -> bool:
    """Whether every pair of a `try_body_pairs` run was asked for other field names: the loop goes on only while the
    answer is shape-refused, so this is whether the LAST attempt was (an exception attempt never is)."""
    last = attempts[-1] if attempts else None
    return bool(last) and shape_refused(last["code"], last.get("text") or "", secrets,
                                        (last["user_field"], last["secret_field"]))


def _answer_words(answer: str) -> str:
    """The closing words a `wrong_door` / `unjudged` why carries (an unknown is said as an unknown, FR-41)."""
    return WRONG_DOOR_WHY if answer == "wrong_door" else UNJUDGED_WHY if answer == "unjudged" else ""


def _login_why(url: str, att: dict, secrets: tuple, road: str = "local_login", shape: bool = False) -> tuple:
    """(status, answer, why) of ONE attempt, the receipt texts of a single-body login. The positive proof - a 2xx with a
    session token - is decided here, before any table; an exception is `no_answer`; a 400/422 that asked for a field not
    sent, with no pair left (`shape`), is `body_shape` (the code's own rule); every other answer goes to `answer_of`."""
    code, text = att["code"], att.get("text") or ""
    if att.get("error"):
        return "failed", "no_answer", f"POST {_safe(url)} -> NO ANSWER ({att.get('cause') or att['error']})"
    if 200 <= code < 300 and _token_in(text):
        return "ok", "in", f"POST {_safe(url)} -> HTTP {code} with a session token"
    answer = "body_shape" if shape else answer_of(code, text, road=road)
    if 200 <= code < 300:
        return "failed", answer, (f"POST {_safe(url)} -> HTTP {code}, but the answer carries none of "
                                  f"{', '.join(TOKEN_FIELDS[:3])} - the endpoint in access.url may not "
                                  "be the login one" + _who_answered(code, text, secrets) + _answer_words(answer))
    door = ""
    if code in (400, 422):
        named = att["complained"]
        door = (f" - the endpoint rejected the body shape (sent the fields `{att['user_field']}` and "
                f"`{att['secret_field']}`)"
                + (f"; its answer complains about {', '.join(f'`{n}`' for n in named)}" if named else "")
                + "; `access.user_field` / `access.secret_field` in qa-factory/config.json name the fields it expects")
    return "failed", answer, (f"POST {_safe(url)} -> HTTP {code}" + door + _who_answered(code, text, secrets)
                              + _answer_words(answer))


def _local_login(access: dict, values: dict, base_url: str, timeout: float) -> dict:
    """POST {<user_field>, <secret_field>} to the endpoint the project logs in through. The two field NAMES are
    data: recorded in `access` (one request), else the pairs of references/login-body-fields.json tried in order
    through `try_body_pairs` (FR-13, OH3-10, FB-3). The probe writes nothing; the accepted pair rides in the receipt."""
    from config_contract import body_field_candidates, body_field_errors, body_fields_recorded
    user_key = str(access.get("user_key") or "")
    secret_key = str(access.get("secret_key") or "")
    url = resolve_url(access.get("url"), values, base_url)
    if not url:
        return _receipt("not_recorded", "access.url does not resolve to a login endpoint", None, user_key, answer="not_tried")
    user, secret = _value(values, user_key), _value(values, secret_key)
    if not user or not secret:
        missing = " and ".join(k for k, v in ((user_key, user), (secret_key, secret)) if not v)
        return _receipt("skipped", f"{missing or 'the login key'} is not set, so nothing was tried",
                        None, user_key, answer="not_tried")
    refused = body_field_errors(access)
    if refused:
        # equal or malformed field names would send a body without the user while the login read `ok`: nothing is sent
        return _receipt("not_recorded", refused[0], None, user_key, answer="not_tried")
    secrets = (user, secret)

    def send(u: str, s: str) -> tuple:
        return _open(url, "POST", json.dumps({u: user, s: secret}).encode("utf-8"),
                     {"Content-Type": "application/json", "Accept": "application/json"}, timeout)

    attempts = try_body_pairs(body_field_candidates(access), send, secrets)
    last = attempts[-1]
    status, answer, why = _login_why(url, last, secrets, "local_login", ran_out_of_pairs(attempts, secrets))
    receipt = _receipt(status, "".join(
        f"tried the body fields `{a['user_field']}` / `{a['secret_field']}` (HTTP {a['code']}); then "
        for a in attempts[:-1]) + why, last["code"], user_key, answer=answer)
    receipt["tried"] = [{k: a[k] for k in ("user_field", "secret_field", "code")} for a in attempts]
    receipt["fields_recorded"] = body_fields_recorded(access)
    if last["code"] in (400, 422):
        receipt["complained"] = list(last["complained"])
    if status == "ok":
        receipt["accepted_fields"] = {"user_field": last["user_field"], "secret_field": last["secret_field"]}
        if not receipt["fields_recorded"]:
            receipt["why"] += (f"; the body fields `{last['user_field']}` / `{last['secret_field']}` are not "
                               "recorded in environment.access (onboarding records them)")
    elif ran_out_of_pairs(attempts, secrets):
        receipt["refusal"], receipt["fix"] = "body_shape", LOGIN_FIELD_FIX
    return receipt


def _oidc_password(access: dict, values: dict, base_url: str, timeout: float) -> dict:
    """The password grant, for a project whose stand is fronted by an identity provider.

    `url` is the token endpoint. A realm key is honoured when the project keeps its realm
    separately (one provider's layout), and then the endpoint is composed the way that
    provider publishes it — but a project that simply records its token endpoint is served
    without the factory knowing whose provider it is."""
    user_key = str(access.get("user_key") or "")
    secret_key = str(access.get("secret_key") or "")
    base = resolve_url(access.get("url"), values, base_url)
    if not base:
        return _receipt("not_recorded", "access.url does not resolve to a token endpoint", None, user_key, answer="not_tried")
    realm = _value(values, access.get("realm_key")) if access.get("realm_key") else ""
    url = base
    if realm and "/token" not in base:
        url = base.rstrip("/") + f"/realms/{urllib.parse.quote(realm)}/protocol/openid-connect/token"
    client_id = _value(values, access.get("client_id_key")) if access.get("client_id_key") else ""
    user, secret = _value(values, user_key), _value(values, secret_key)
    if not user or not secret:
        missing = " and ".join(k for k, v in ((user_key, user), (secret_key, secret)) if not v)
        return _receipt("skipped", f"{missing or 'the login key'} is not set, so nothing was tried",
                        None, user_key, answer="not_tried")
    form = {"grant_type": "password", "username": user, "password": secret}
    if client_id:
        form["client_id"] = client_id
    data = urllib.parse.urlencode(form).encode("utf-8")
    try:
        code, text = _open(url, "POST", data,
                           {"Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "application/json"}, timeout)
    except Exception as exc:
        return _receipt("failed", f"POST {_safe(url)} -> NO ANSWER ({_cause_of(exc)})",
                        None, user_key, answer="no_answer")
    if 200 <= code < 300 and _token_in(text):
        return _receipt("ok", f"password grant at {_safe(url)} -> HTTP {code} with an access token",
                        code, user_key, answer="in")
    answer = answer_of(code, text, road="oidc_password")
    if 200 <= code < 300:
        return _receipt("failed", f"password grant at {_safe(url)} -> HTTP {code} without an "
                                  "access_token - access.url may not be the token endpoint"
                                  + _who_answered(code, text, (user, secret)) + _answer_words(answer),
                        code, user_key, answer=answer)
    return _receipt("failed", f"password grant at {_safe(url)} -> HTTP {code}"
                    + _who_answered(code, text, (user, secret)) + _answer_words(answer), code, user_key, answer=answer)


def _bearer_env(access: dict, values: dict, base_url: str, health_url: str, timeout: float) -> dict:
    """A token the project already holds: the proof is that the stand accepts it."""
    token_key = str(access.get("token_key") or "")
    token = _value(values, token_key)
    url = resolve_url(access.get("url"), values, base_url) or health_url or base_url
    if not token_key:
        return _receipt("not_recorded", "access.kind is bearer_env but access.token_key is empty", answer="not_tried")
    if not token:
        return _receipt("skipped", f"{token_key} is not set, so nothing was tried", None, token_key, answer="not_tried")
    if not url:
        return _receipt("not_recorded", "there is no address to present the token to "
                                        "(access.url, health_path/health_url, base_url_key)",
                        None, token_key, answer="not_tried")
    try:
        code, text = _open(url, "GET", None, {"Authorization": f"Bearer {token}",
                                              "Accept": "application/json"}, timeout)
    except Exception as exc:
        return _receipt("failed", f"GET {_safe(url)} -> NO ANSWER ({_cause_of(exc)})",
                        None, token_key, answer="no_answer")
    if 200 <= code < 300:
        return _receipt("ok", f"GET {_safe(url)} with the token in {token_key} -> HTTP {code}",
                        code, token_key, answer="in")
    answer = answer_of(code, text, road="bearer_env")
    return _receipt("failed", f"GET {_safe(url)} with the token in {token_key} -> HTTP {code}"
                    + _who_answered(code, text, (token,), expect="any") + _answer_words(answer), code, token_key, answer=answer)


def _path_value(node, path):
    """The value under a path of object keys, else None."""
    for step in path:
        if not isinstance(node, dict):
            return None
        node = node.get(step)
    return node


def _cookies_into(jar: dict, headers) -> None:
    """Add the cookies of a response to `jar`: EVERY `Set-Cookie` pair of the headers list (never `Headers.get`, which
    keeps only the first), each as `name=value` - the text before the first `;`, split at the first `=`; a later name
    overwrites an earlier one."""
    for name, value in headers or ():
        if str(name).lower() != "set-cookie":
            continue
        key, sep, val = str(value).split(";", 1)[0].partition("=")
        if sep and key.strip():
            jar[key.strip()] = val.strip()


def _form_login(access: dict, values: dict, base_url: str, timeout: float) -> dict:
    """The sign-in FORM road (FV1-17a): a csrf step, ONE submit, a session step - the shape of a row of
    references/login-roads.json (the framework's name lives there, never here). At most three requests; the submit is
    never repeated (a lockout), and nothing is submitted when the first step does not hand out its token. The proof is
    the session step: a non-empty value at the row's `proof_at`. Every text built here redacts the user, the secret, the
    csrf token and every cookie value; the raw Location of the submit is read for the row's marker and never kept."""
    import config_contract
    user_key = str(access.get("user_key") or "")
    secret_key = str(access.get("secret_key") or "")
    held: list = []   # every value that must not appear in anything printed: the user, the secret, the token, the cookies

    def done(status: str, answer: str, why: str, code=None) -> dict:
        return _receipt(status, _scrub(why, held), code, user_key, answer=answer)

    def not_tried(status: str, why: str) -> dict:
        return done(status, "not_tried", why)

    forms = login_roads()["forms"]
    if not forms:
        return not_tried("not_recorded", "no sign-in form is known (references/login-roads.json has no valid row)")
    wanted = str(access.get("form") or "").strip()
    row = next((r for r in forms if r["id"] == wanted), None) if wanted else forms[0]
    if row is None:
        return not_tried("not_recorded", f"access.form `{wanted[:64]}` is not a known sign-in form (known: "
                                         + ", ".join(r["id"] for r in forms) + ")")
    raw_url = str(access.get("url") or "").strip()
    base = (resolve_url(raw_url, values, base_url) if raw_url else str(base_url or "")).strip().rstrip("/")
    if not base:
        return not_tried("not_recorded", "there is no address to sign in at (access.url, or the stand's own base address)")
    user, secret = _value(values, user_key), _value(values, secret_key)
    if not user or not secret:
        missing = " and ".join(k for k, v in ((user_key, user), (secret_key, secret)) if not v)
        return not_tried("skipped", f"{missing or 'the login key'} is not set, so nothing was tried")
    refused = config_contract.body_field_errors(access)
    user_field = str(access.get("user_field") or "").strip() or row["fields"][0]
    secret_field = str(access.get("secret_field") or "").strip() or row["fields"][1]
    if not refused and user_field == secret_field:
        refused = [f"the sign-in form's user field and secret field are both `{user_field}`: give environment.access."
                   "user_field / secret_field two different names"]
    if refused:
        return not_tried("not_recorded", refused[0])
    held.extend((user, secret))
    fields_recorded = config_contract.body_fields_recorded(access)
    jar: dict = {}

    def remember(headers) -> None:
        _cookies_into(jar, headers)
        held.extend(jar.values())

    def cookie_header() -> dict:
        return {"Cookie": "; ".join(f"{k}={v}" for k, v in jar.items())} if jar else {}

    def failed_step(verb: str, url: str, answer_obj, what: str = "") -> dict:
        """A failed step: the answer the table gives it (the code's own proofs were checked before), worded."""
        code, text = answer_obj.status, answer_obj.body.decode("utf-8", errors="replace")
        answer = answer_of(code, text, road="form_login", headers=answer_obj.headers)
        return done("failed", answer, f"{verb} {_safe(url)} -> HTTP {code}{what}" + _who_answered(code, text, tuple(held))
                    + _answer_words(answer), code)

    def no_answer(verb: str, url: str, exc) -> dict:
        return done("failed", "no_answer", f"{verb} {_safe(url)} -> NO ANSWER ({_cause_of(exc)})")

    # step 1: the first step hands out the token
    url1 = base + row["csrf"]["path"]
    try:
        first = _exchange(url1, "GET", None, {"Accept": "application/json"}, timeout, expect="json")
    except Exception as exc:  # noqa: BLE001 - any exception is no answer (I3)
        return no_answer("GET", url1, exc)
    if not 200 <= first.status < 300:
        return failed_step("GET", url1, first)
    try:
        token = _path_value(json.loads(first.body.decode("utf-8", errors="replace")), row["csrf"]["token_at"])
    except ValueError:
        token = None
    if not (isinstance(token, str) and token.strip()):
        text = first.body.decode("utf-8", errors="replace")
        return done("failed", "wrong_door",
                    f"GET {_safe(url1)} -> HTTP {first.status}, but the sign-in form's first step answered without the "
                    "token it hands out" + _who_answered(first.status, text, tuple(held)) + WRONG_DOOR_WHY, first.status)
    token = token.strip()
    held.append(token)
    remember(first.headers)
    # step 2: ONE submit
    fields = {row["submit"]["csrf_field"]: token, user_field: user, secret_field: secret, **row["submit"]["extra"]}
    if row["submit"]["encoding"] == "json":
        data, content_type = json.dumps(fields).encode("utf-8"), "application/json"
    else:
        data, content_type = urllib.parse.urlencode(fields).encode("utf-8"), "application/x-www-form-urlencoded"
    url2 = base + row["submit"]["path"]
    try:
        second = _exchange(url2, "POST", data, {"Content-Type": content_type, "Accept": "application/json",
                                                **cookie_header()}, timeout, expect="json")
    except Exception as exc:  # noqa: BLE001
        return no_answer("POST", url2, exc)
    if not (200 <= second.status < 400):
        return failed_step("POST", url2, second)
    remember(second.headers)
    marker = row["refused_marker"]
    hit = marker in str(second.headers.get("Location") or "")      # the RAW Location (`Answer.location` has no query)
    if not hit and 200 <= second.status < 300:
        try:
            said_url = (json.loads(second.body.decode("utf-8", errors="replace")) or {}).get("url")
        except (ValueError, AttributeError):
            said_url = None
        hit = isinstance(said_url, str) and marker in said_url
    if hit:
        if not fields_recorded and not row["field_errors_reported"]:
            return done("failed", "fields_unconfirmed",
                        f"POST {_safe(url2)} -> HTTP {second.status}, the form refused the sign-in; it does not say whether "
                        "the account or the body field names were wrong, and the field names are not recorded in "
                        "environment.access", second.status)
        return done("failed", "credentials_refused",
                    f"POST {_safe(url2)} -> HTTP {second.status}, the form refused the account", second.status)
    # step 3: the session decides
    url3 = base + row["session"]["path"]
    try:
        third = _exchange(url3, "GET", None, {"Accept": "application/json", **cookie_header()}, timeout, expect="json")
    except Exception as exc:  # noqa: BLE001
        return no_answer("GET", url3, exc)
    if 200 <= third.status < 300:
        try:
            proof = _path_value(json.loads(third.body.decode("utf-8", errors="replace")), row["session"]["proof_at"])
        except ValueError:
            proof = None
        if (isinstance(proof, dict) and proof) or (isinstance(proof, str) and proof.strip()):
            return done("ok", "in", f"form sign-in at {_safe(url2)}, then GET {_safe(url3)} -> HTTP {third.status} with a session",
                        third.status)
    return failed_step("GET", url3, third,", but it shows no session after the sign-in")


def _login(access, values: dict, base_url: str, timeout: float, health_url: str, cwd) -> dict:
    if not isinstance(access, dict) or not str(access.get("kind") or "").strip():
        return _receipt("not_recorded", NOT_RECORDED_WHY, answer="not_tried")
    kind = str(access.get("kind")).strip()
    if kind not in KINDS:
        return _receipt("not_recorded", f"access.kind `{kind}` is outside {' | '.join(KINDS)}", answer="not_tried")
    if kind == "none":
        return _receipt("skipped", "this stand needs no login (access.kind: none) - liveness is "
                                   "the whole answer", answer="not_tried")
    if kind == "ui_only":
        return _receipt("skipped", "this project signs in through its UI only (the person's word at onboarding); there is "
                                   "no sign-in by code to check", answer="not_tried")
    try:
        timeout = float(timeout)
    except (TypeError, ValueError):
        timeout = 8.0
    values = values if isinstance(values, dict) else {}
    if kind == "harness_command":
        return _harness_command(access, values, timeout, cwd)
    if kind == "local_login":
        return _local_login(access, values, base_url, timeout)
    if kind == "oidc_password":
        return _oidc_password(access, values, base_url, timeout)
    if kind == "form_login":
        return _form_login(access, values, base_url, timeout)
    return _bearer_env(access, values, base_url, health_url, timeout)


def login(access, values: dict, base_url: str = "", timeout: float = 8.0,
          health_url: str = "", cwd=None, *, source: str = "access") -> dict:
    """{"status", "code", "user_key", "why", "answer", "source"} — did we get in, and how do we know.

    status: `ok` (we are in) · `failed` (the stand refused us) · `not_recorded` (this project
    never recorded how it logs in — an onboarding gap, never the person's fault) · `skipped`
    (the stand needs no login, or a key the login needs is not set, so nothing was tried).
    `answer` is what the attempt came to (a word of ANSWERS). `source` says who recorded the way - `access` (the
    onboarding's `environment.access`), or `registry` for a way a story found - and is set HERE, on every receipt.

    `user_key` is a NAME. Nothing this function returns contains a credential."""
    receipt = _login(access, values, base_url, timeout, health_url, cwd)
    receipt["source"] = source
    return receipt


def code_login_declined(access) -> bool:
    """Whether the person said the tests sign in through the UI only (`access.kind: ui_only`): the ONE reader of that word
    (AR-13), for every reader that would otherwise probe a sign-in by code or turn a role's record into a stop."""
    return isinstance(access, dict) and str(access.get("kind") or "").strip() == "ui_only"


def valid_status(value):
    """`value` when it is an HTTP code - an int, not a bool, in 100..599 - else None. The ONE test of a recorded code
    (AR-13): `recorded_login` reads it and `config_contract.access_errors` refuses by it (a hand-written 0 included)."""
    return value if isinstance(value, int) and not isinstance(value, bool) and 100 <= value <= 599 else None


def recorded_login(access) -> dict:
    """THE reader of `environment.access.login_probe` (AR-13): {recorded, user_key, outcome, answer, status, checked_at,
    seconds, user_field, secret_field}. `recorded` = a `login_probe` object with a non-empty user_key; a string is stripped
    and a non-string is ""; `outcome` / `answer` are a word of LOGIN_OUTCOMES / ANSWERS or None (a record that predates
    `answer` reads None - never guessed); `status` through `valid_status`; `seconds` through `recorded_seconds`. Never raises."""
    blank = {"recorded": False, "user_key": "", "outcome": None, "answer": None, "status": None, "checked_at": "",
             "seconds": None, "user_field": "", "secret_field": ""}
    try:
        import config_contract  # lazy: it imports this module at load
        probe = access.get("login_probe") if isinstance(access, dict) else None
        if not isinstance(probe, dict):
            return blank

        def text(key: str) -> str:
            value = probe.get(key)
            return value.strip() if isinstance(value, str) else ""
        outcome, answer = text("outcome"), text("answer")
        return {"recorded": bool(text("user_key")), "user_key": text("user_key"),
                "outcome": outcome if outcome in config_contract.LOGIN_OUTCOMES else None,
                "answer": answer if answer in ANSWERS else None, "status": valid_status(probe.get("status")),
                "checked_at": text("checked_at"), "seconds": recorded_seconds({"login_probe": probe}),
                "user_field": text("user_field"), "secret_field": text("secret_field")}
    except Exception:  # noqa: BLE001 - a reader of a record never raises: an unreadable one is not recorded
        return blank


# ---- the roads: every way this project could sign in by, tried and reported (FV1-17a) --------------------------------

def _limit(raw, default: int, ceiling: int, name: str) -> tuple:
    """(value, note) of one budget number: absent, not an int, a bool, 0 or negative -> `default` (the safe side, FR-59);
    above `ceiling` -> the ceiling and a note - the data may lower the risk, never raise it past the code's ceiling."""
    if isinstance(raw, int) and not isinstance(raw, bool) and raw > 0:
        if raw > ceiling:
            return ceiling, f"budget.{name} {raw} is above the ceiling {ceiling}; {ceiling} is used"
        return raw, ""
    return default, ""


def _form_row(raw) -> dict | None:
    """One `forms` row of references/login-roads.json when it has every key of the right type, else None."""
    import config_contract

    def text(value) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def path_ok(value) -> bool:
        return text(value) and bool(config_contract.API_PATH_RE.match(value.strip()))

    def keys_ok(value) -> bool:
        return isinstance(value, list) and bool(value) and all(text(k) for k in value)
    try:
        csrf, submit, session, fields = raw["csrf"], raw["submit"], raw["session"], raw["fields"]
        if not (text(raw["id"]) and re.fullmatch(r"[A-Za-z0-9_.\-]{1,64}", raw["id"].strip()) and text(raw["seen_in"])
                and text(raw["refused_marker"]) and isinstance(raw["field_errors_reported"], bool)
                and isinstance(csrf, dict) and path_ok(csrf["path"]) and keys_ok(csrf["token_at"])
                and isinstance(submit, dict) and path_ok(submit["path"]) and submit["encoding"] in ("form", "json")
                and text(submit["csrf_field"]) and isinstance(submit["extra"], dict)
                and all(text(k) and isinstance(v, str) for k, v in submit["extra"].items())
                and isinstance(session, dict) and path_ok(session["path"]) and keys_ok(session["proof_at"])
                and isinstance(fields, list) and len(fields) == 2 and all(text(f) for f in fields)
                and fields[0].strip() != fields[1].strip()):
            return None
    except (KeyError, TypeError, AttributeError):
        return None
    return {"id": raw["id"].strip(), "seen_in": raw["seen_in"].strip(),
            "csrf": {"path": csrf["path"].strip(), "token_at": [k.strip() for k in csrf["token_at"]]},
            "submit": {"path": submit["path"].strip(), "encoding": submit["encoding"],
                       "csrf_field": submit["csrf_field"].strip(), "extra": dict(submit["extra"])},
            "session": {"path": session["path"].strip(), "proof_at": [k.strip() for k in session["proof_at"]]},
            "refused_marker": raw["refused_marker"], "fields": [f.strip() for f in fields],
            "field_errors_reported": raw["field_errors_reported"]}


def login_roads() -> dict:
    """THE reader of references/login-roads.json (AR-13, through `hooklib.read_json`): {"forms": [valid rows], "budget":
    {real_secret_failures, candidates}, "table": "ok" | "unreadable"}, plus `forms_note` / `budget_note` when something was cut.
    A row with a missing key, a wrong type or a path that is not one `/path` is dropped; a repeated id is dropped; at most
    FORMS_CEILING rows are read. No row, or an unreadable file: `forms` empty and `table` `unreadable` (the budget is still the
    default one) - never an exception."""
    import hooklib  # the one JSON reader (AR-13); imported here like `_login_error_shapes`
    data = hooklib.read_json(LOGIN_ROADS_PATH, {}, kind=dict)
    rows = data.get("forms") if isinstance(data.get("forms"), list) else []
    forms: list = []
    for raw in rows:
        row = _form_row(raw)
        if row is not None and all(row["id"] != kept["id"] for kept in forms):
            forms.append(row)
    out: dict = {"forms": forms[:FORMS_CEILING], "table": "ok" if forms else "unreadable"}
    if len(forms) > FORMS_CEILING:
        out["forms_note"] = f"{len(forms) - FORMS_CEILING} sign-in form(s) beyond {FORMS_CEILING} were not read"
    budget = data.get("budget") if isinstance(data.get("budget"), dict) else {}
    failures, note_a = _limit(budget.get("real_secret_failures"), BUDGET_DEFAULTS["real_secret_failures"],
                              REAL_SECRET_FAILURES_CEILING, "real_secret_failures")
    candidates, note_b = _limit(budget.get("candidates"), BUDGET_DEFAULTS["candidates"], CANDIDATES_CEILING, "candidates")
    out["budget"] = {"real_secret_failures": failures, "candidates": candidates}
    if note_a or note_b:
        out["budget_note"] = "; ".join(n for n in (note_a, note_b) if n)
    return out


CANDIDATE_KINDS = ("local_login", "oidc_password")
CANDIDATE_USAGE = "a candidate is <local_login|oidc_password>=<url or path>"


def parse_candidate(text) -> tuple:
    """(kind, url) of one `--candidate <kind>=<url>`; ValueError (the usage, never the value) for another shape."""
    kind, sep, url = str(text or "").partition("=")
    if not sep or kind.strip() not in CANDIDATE_KINDS or not url.strip():
        raise ValueError(CANDIDATE_USAGE)
    return kind.strip(), url.strip()


def _shown_access(access: dict) -> dict:
    """The road's access as the report shows it: its names and its command, with the address through `_safe` (userinfo,
    query and fragment removed); `login_probe` is not part of a road."""
    shown = {k: v for k, v in access.items() if k != "login_probe"}
    if isinstance(shown.get("url"), str) and shown["url"].strip():
        shown["url"] = _safe(shown["url"])
    return shown


def _negative_control(access: dict, full_cfg: dict, env_name: str, root, secret_key: str) -> str:
    """`refused` (the command exits non-zero with a JUNK secret: it reads the secret it was given), `passed` (it exits 0 with
    the junk secret too, or reads the secret from elsewhere) or `not_run` (the run gave neither). The junk value is made here,
    goes only into the child's environment and is never printed or written."""
    import env_probe
    values = dict(env_probe.load_env(env_probe.selected_probe_config(full_cfg, env_name)[0], root)[0])
    values[secret_key] = "qa-factory-wrong-" + _secrets.token_hex(12)
    receipt = login(access, values, "", env_probe.LOGIN_TIMEOUT_S, "", root)
    return {"in": "passed", "command_failed": "refused"}.get(receipt.get("answer"), "not_run")


def try_roads(full_cfg, root, *, env_name: str = "", command: str = "", candidates=(), user_key: str = "",
              secret_key: str = "", negative: bool = True) -> dict:
    """Run every road the project could sign in by, each THE PROBE'S way (a deep copy of the config whose
    `environment.access` is the road's, through `env_probe.probe`, whose `login` receipt is the road's), and report what
    each answered. Roads in this order: (a) the recorded access, (b) one form road per valid row of
    references/login-roads.json, (c) the harness `command` the role composed, (d) each candidate `(kind, url)`. Budget and
    stops (references/login-roads.json `budget`): `throttled` ends the run; `credentials_refused` ends every later road
    (another way only fails the same account); the Nth failed real-secret sign-in ends it. The harness road that is `in`
    first gets ONE junk-secret run. Writes nothing; prints nothing. `first_in` is an index into `roads` - a HINT, the role
    chooses."""
    import env_probe
    data = login_roads()
    budget = data["budget"]
    cfg_env = (full_cfg or {}).get("environment") if isinstance((full_cfg or {}).get("environment"), dict) else {}
    recorded = cfg_env.get("access") if isinstance(cfg_env.get("access"), dict) else {}
    rec_kind = str(recorded.get("kind") or "").strip()
    rec_url = str(recorded.get("url") or "").strip()
    user_name = str(recorded.get("user_key") or "").strip() or str(user_key or "").strip()
    secret_name = str(recorded.get("secret_key") or "").strip() or str(secret_key or "").strip()
    roads: list = []   # (road id, access or None)
    if rec_kind in KINDS and rec_kind not in ("none", "ui_only"):
        roads.append(("a", copy.deepcopy(recorded)))
    for index, row in enumerate(data["forms"]):
        same = rec_kind == "form_login" and (str(recorded.get("form") or "").strip() == row["id"]
                                             or (not str(recorded.get("form") or "").strip() and index == 0))
        if not same:
            roads.append((f"b:{row['id']}", {"kind": "form_login", "form": row["id"], "user_key": user_name,
                                             "secret_key": secret_name}))
    command = str(command or "").strip()
    if command and not (rec_kind == "harness_command" and str(recorded.get("command") or "").strip() == command):
        roads.append(("c", {"kind": "harness_command", "command": command, "user_key": user_name, "secret_key": secret_name}))
    wanted = [parse_candidate(c) if isinstance(c, str) else (str(c[0]), str(c[1]).strip()) for c in candidates or ()]
    fresh = [(n, kind, url) for n, (kind, url) in enumerate(wanted, 1) if not (rec_kind == kind and rec_url == url)]
    for n, kind, url in fresh[:budget["candidates"]]:
        roads.append((f"d:{n}", {"kind": kind, "url": url, "user_key": user_name, "secret_key": secret_name}))
    entries: list = []
    spent, stop, did_negative = 0, "", False
    for position, (road_id, access) in enumerate(roads, 1):
        entry = {"road": road_id, "kind": str(access["kind"]).strip(), "access": _shown_access(access)}
        if stop:
            entry.update(status="skipped", answer="not_tried", why=stop)
        elif road_id != "a" and not (user_name and secret_name):
            entry.update(status="skipped", answer="not_tried", why="no sign-in key names are recorded or given")
        else:
            try:
                road_cfg = copy.deepcopy(full_cfg) if isinstance(full_cfg, dict) else {}
                if not isinstance(road_cfg.get("environment"), dict):
                    road_cfg["environment"] = {}
                road_cfg["environment"]["access"] = access
                receipt = env_probe.probe(road_cfg, env_name, root=root)["login"]
            except Exception as exc:  # noqa: BLE001 - a road that could not be run is not a pass and not an attempt
                receipt = {"status": "skipped", "answer": "not_tried",
                           "why": f"this road could not be run ({type(exc).__name__})"}
            answer = receipt.get("answer") if receipt.get("answer") in ANSWERS else "not_tried"
            entry.update(status=receipt.get("status"), answer=answer, why=str(receipt.get("why") or ""))
            if isinstance(receipt.get("record"), dict):
                entry["record"] = receipt["record"]
            if answer in SPENDING_ANSWERS:
                spent += 1
            if answer == "in" and entry["kind"] == "harness_command" and not did_negative:
                did_negative = True    # the junk-secret run belongs to the FIRST harness road that is `in`, once per run
                named = str(access.get("secret_key") or "").strip()
                entry["negative"] = _negative_control(access, full_cfg, env_name, root, named) if negative and named else "not_run"
                if entry["negative"] == "passed":
                    entry["why"] += (" - it passes with a wrong secret too (or reads the secret from elsewhere), so it may "
                                     "not prove a sign-in: judge it")
            if answer == "throttled":
                stop = "the stand limits requests (HTTP 429); nothing more was sent in this run"
            elif answer == "credentials_refused":
                stop = (f"the account was refused at road {position}; another way would only fail the same account - fix the "
                        "account first (its values in the env file)")
            elif spent >= budget["real_secret_failures"]:
                stop = f"the attempt budget of this run is spent ({spent} failed sign-in(s) with the real account)"
        entries.append(entry)
    out = {"roads": entries,
           "first_in": next((i for i, e in enumerate(entries) if e["answer"] == "in"), None),
           "tried": sum(1 for e in entries if e["answer"] != "not_tried"), "spent": spent,
           "budget": budget, "table": data["table"]}
    if data.get("budget_note"):
        out["budget_note"] = data["budget_note"]
    if data.get("forms_note"):
        out["forms_note"] = data["forms_note"]
    if len(fresh) > budget["candidates"]:
        out["candidates_note"] = f"{len(fresh) - budget['candidates']} candidate(s) beyond {budget['candidates']} were not tried"
    return out


def _refuse(text: str) -> int:
    print(text, file=sys.stderr)
    return 2


def main(argv=None) -> int:
    """`python -B stand_access.py --project-root DIR --roads [--env NAME] [--command "<cmd>"] [--candidate <kind>=<url>]...
    [--user-key NAME --secret-key NAME] [--no-negative] --json`: the report of `try_roads` as JSON on stdout, exit 0 (a report,
    not a verdict; it writes nothing). Exit 2, nothing sent: an argument it refuses, or a project config it cannot read."""
    parser = argparse.ArgumentParser(prog="stand_access.py", description="Try every way this project could sign in to its stand.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--roads", action="store_true")
    parser.add_argument("--env", default="")
    parser.add_argument("--command", default="")
    parser.add_argument("--candidate", action="append", default=[])
    parser.add_argument("--user-key", default="")
    parser.add_argument("--secret-key", default="")
    parser.add_argument("--no-negative", action="store_true")
    parser.add_argument("--json", action="store_true")   # the report is JSON either way; the flag is the documented spelling
    args = parser.parse_args(argv)
    if not args.roads:
        return _refuse("nothing to do: --roads is what this script runs")
    import config_contract
    import hooklib
    for flag, name in (("--user-key", args.user_key), ("--secret-key", args.secret_key)):
        if name and not config_contract.KEY_NAME_RE.match(name):
            return _refuse(f"{flag} is the NAME of a variable in the env file (letters, digits, _), never its value")
    try:
        for candidate in args.candidate:
            parse_candidate(candidate)
    except ValueError as exc:
        return _refuse(str(exc))
    root = Path(args.project_root).resolve()
    full_cfg = hooklib.read_json(root / "qa-factory" / "config.json", None, kind=dict)
    if full_cfg is None:
        return _refuse(f"{root / 'qa-factory' / 'config.json'} cannot be read as a JSON object, so no road was tried")
    print(json.dumps(try_roads(full_cfg, root, env_name=args.env, command=args.command, candidates=args.candidate,
                               user_key=args.user_key, secret_key=args.secret_key, negative=not args.no_negative), indent=2))
    return 0


def login_keys(access) -> list:
    """The key NAMES this project's login itself needs — the only keys whose absence stops a
    story. Everything else a config lists blocks an area at most, and saying otherwise is how
    one story halted on four keys no test in it ever read."""
    if not isinstance(access, dict):
        return []
    kind = str(access.get("kind") or "").strip()
    if kind in ("none", "ui_only") or kind not in KINDS:
        return []
    fields = ("token_key",) if kind == "bearer_env" else ("user_key", "secret_key")
    return [str(access.get(f) or "").strip() for f in fields if str(access.get(f) or "").strip()]


if __name__ == "__main__":
    sys.exit(main())
