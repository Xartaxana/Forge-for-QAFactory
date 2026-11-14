"""B-408: the factory's outbound HTTP helper - a User-Agent that names the factory, the error body read, and an
answer told apart by WHO wrote it.

The run this is written from (06.10.2026, a colleague's machine behind a protection layer): every REST read of the
tracker answered 403 with an HTML page, the client sent no User-Agent, never read the error body, and `auth_gate`
took the 403 for a dead token - "renew the token" for a token that was fine. The rule under test: the token is never
declared lost on an answer the service has not been shown to write; a classification errs toward `intermediary` /
`unclear` and never toward `service`.
"""
import contextlib
import io
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import check, check_eq, check_in, check_not_in, finish, temp_dir, cleanup  # noqa: E402

os.environ["no_proxy"] = os.environ["NO_PROXY"] = "127.0.0.1,localhost"   # a company proxy must not sit in front of the stub

import http_client as H  # noqa: E402

CF_HTML = (b'<!DOCTYPE html><html><head><title>Attention Required! | Cloudflare</title></head>'
           b'<body>Sorry, you have been blocked</body></html>')
CF_HEADERS = [("Server", "cloudflare"), ("CF-RAY", "8a1b2c3d4e5f-AMS"), ("Content-Type", "text/html; charset=UTF-8")]
JIRA_JSON = b'{"errorMessages":["You do not have the permission to see the specified issue."],"errors":{}}'


class Stub:
    """A real socket: `route` is (status, [(header, value)], body); every request's headers are kept."""

    def __init__(self):
        self.route = (200, [], b"")
        self.seen = []
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def _answer(self):
                stub.seen.append({"path": self.path, "method": self.command, "headers": dict(self.headers.items())})
                status, headers, body = stub.route
                self.send_response(status)
                for name, value in headers:
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            do_GET = do_POST = _answer  # noqa: N815

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}/rest/api/2/serverInfo"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class StallStub:
    """A loopback server that sends the STATUS and the headers, a few bytes of the body, and then goes quiet for `stall_s`
    seconds (the connection stays open): the body read times out, the status has arrived (B-408 F1). `status` is settable."""

    def __init__(self, status=200, stall_s=3.0):
        self.status = status
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                self.send_response(stub.status)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", "1000")
                self.end_headers()
                self.wfile.write(b"<html><title>par")
                self.wfile.flush()
                import time
                time.sleep(stall_s)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}/health"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def kind(status, headers, body, **kw):
    return H.classify(status, headers, body, **kw)["kind"]


def the_user_agent(stub):
    H._ua_cache = None
    ua = H.user_agent()
    check("AK1: the User-Agent starts with qa-factory/<version> and names neither python nor urllib",
          ua.startswith("qa-factory/") and "python" not in ua.lower() and "urllib" not in ua.lower(), ua)
    stub.route = (200, [("Content-Type", "application/json")], b"{}")
    answer = H.fetch(stub.url, timeout=5)
    check_eq("AK1: the User-Agent the stub server SAW is the helper's", stub.seen[-1]["headers"].get("User-Agent"), ua)
    check_eq("AK1: a 2xx with a body is `ok`", (answer.status, answer.verdict["kind"], answer.body), (200, "ok", b"{}"))
    urllib.request.urlopen(urllib.request.Request(stub.url), timeout=5).read()
    check("AK1 control: a plain urlopen arrives as Python-urllib/", stub.seen[-1]["headers"].get("User-Agent", "").startswith("Python-urllib/"),
          str(stub.seen[-1]["headers"]))
    # E3: the caller's own User-Agent wins, in any case, and is not duplicated
    for name in ("User-Agent", "user-agent", "USER-AGENT"):
        H.fetch(stub.url, headers={name: "role-agent/1"}, timeout=5)
        check_eq(f"E3: a caller's `{name}` is kept, once", stub.seen[-1]["headers"].get("User-Agent"), "role-agent/1")
    # E1 / E2: the version cannot be read; non-ASCII in it
    import story_version
    real = story_version.installed_version
    try:
        for label, version, want in (("E1: unreadable", None, "qa-factory/unknown"), ("E1: empty", "", "qa-factory/unknown"),
                                     ("E2: non-ASCII dropped", "0.9é.0 beta", "qa-factory/0.9.0beta")):
            def fake(version=version):
                if version is None:
                    raise OSError("no manifest")
                return version
            story_version.installed_version = fake
            H._ua_cache = None
            got = H.user_agent()
            check_eq(label, got, want)
            got.encode("latin-1")
    finally:
        story_version.installed_version = real
        H._ua_cache = None
    check_eq("the User-Agent is cached per process", H.user_agent() is H.user_agent(), True)
    H._ua_cache = None


def the_four_kinds(stub):
    stub.route = (403, CF_HEADERS, CF_HTML)
    a = H.fetch(stub.url, timeout=5, service="jira")
    check_eq("AK2: 403 + a Cloudflare HTML page -> intermediary, the title and the path named",
             (a.status, a.verdict["kind"], a.verdict["title"], a.verdict["via"]),
             (403, "intermediary", "Attention Required! | Cloudflare", "Cloudflare"))
    stub.route = (403, [("Content-Type", "application/json;charset=UTF-8")], JIRA_JSON)
    a = H.fetch(stub.url, timeout=5, service="jira")
    check_eq("AK2: 403 + Jira's own JSON -> service", a.verdict["kind"], "service")
    stub.route = (302, [("Location", "https://user:pw@idp.example.invalid/login?next=%2Fsecret&token=abc#frag")], b"")
    a = H.fetch(stub.url, timeout=5)
    check_eq("AK2 / E12: a 302 is NOT followed: redirect, with the Location in the safe form",
             (a.status, a.verdict["kind"], a.location), (302, "redirect", "https://idp.example.invalid/login"))
    check_eq("E12: no request went to the other host: the stub saw only the one request it was asked for", stub.seen[-1]["path"], "/rest/api/2/serverInfo")
    stub.route = (200, [("Content-Type", "text/html")], b"<html><head><title>Sign in</title></head></html>")
    a = H.fetch(stub.url, timeout=5, expect="json")
    check_eq("AK2: a 200 HTML where JSON was expected -> page", (a.verdict["kind"], a.verdict["title"]), ("page", "Sign in"))
    a = H.fetch(stub.url, timeout=5)
    check_eq("control: the same 200 HTML with nothing expected -> ok", a.verdict["kind"], "ok")
    check_eq("fetch gives case-insensitive header lookup", a.headers.get("content-TYPE"), "text/html")


def the_error_direction():
    seraph = [("X-Seraph-LoginReason", "AUTHENTICATION_DENIED")]
    cf = [("Server", "cloudflare"), ("CF-RAY", "abc"), ("Content-Type", "text/html")]
    safe = {  # every one must end on the safe side: never `service`
        "a Cloudflare 403 HTML page": (403, cf, CF_HTML, {}),
        "a 403 HTML page with no headers at all (the 2-tuple seam)": (403, None, CF_HTML, {}),
        "a 403 JSON with cf-mitigated": (403, [("cf-mitigated", "challenge"), ("Content-Type", "application/json")], JIRA_JSON, {}),
        "a gateway's JSON 403 {message: Forbidden}, service=jira": (403, [("Content-Type", "application/json")], b'{"message":"Forbidden"}', {"service": "jira"}),
        "a 401 HTML page with no service header": (401, [("Content-Type", "text/html")], b"<html><title>x</title></html>", {}),
        "a 403 plain-text body": (403, [("Content-Type", "text/plain")], b"Forbidden by policy", {}),
        "a gzip-encoded 401 (E14)": (401, [("Content-Encoding", "gzip")], b"\x1f\x8b\x08\x00binary", {}),
        "a failed body read (E14)": (401, [], b"", {"unreadable": True}),
        "a body that is not UTF-8": (401, [], b"\xff\xfe\xfa\x80", {}),
        "a 401 plain text that was cut": (401, [], b"x" * 70000, {"truncated": True}),
    }
    for label, (status, headers, body, kw) in safe.items():
        got = kind(status, headers, body, **kw)
        check(f"AK3 safe side: {label} -> intermediary/unclear, never service/empty (got {got})", got in ("intermediary", "unclear"))
    big = b"<html><head>" + b" " * 70000 + b"<title>late</title></head></html>"
    verdict = H.classify(403, [("Content-Type", "text/html")], big)
    check_eq("AK3 / E6: an HTML body bigger than the bound -> intermediary by its SHAPE, the title (beyond the bound) is None",
             (verdict["kind"], verdict["title"]), ("intermediary", None))
    check_eq("AK3: a 200 challenge page where JSON was expected -> page (not ok)", kind(200, cf, CF_HTML, expect="json"), "page")
    # the controls: these must still be the SERVICE (a lost login stays lost)
    controls = {
        "a 401 with an empty body": (401, [], b"", "empty"),
        "a 401 with an empty body and a text/html Content-Type": (401, [("Content-Type", "text/html")], b"", "empty"),
        "a CAPTCHA header with an empty body": (403, [("X-Seraph-LoginReason", "CAPTCHA_CHALLENGE")], b"", "service"),
        "a CAPTCHA header with an HTML body (E8)": (403, [("X-Seraph-LoginReason", "CAPTCHA_CHALLENGE"), ("Content-Type", "text/html")], CF_HTML, "service"),
        "a CAPTCHA header behind Cloudflare (E8)": (403, cf + seraph[:0] + [("X-Seraph-LoginReason", "CAPTCHA_CHALLENGE")], CF_HTML, "service"),
        "a CAPTCHA header together with an AUTHORSHIP marker (the service's own header outranks, E8)": (403, [("cf-mitigated", "challenge"), ("X-Seraph-LoginReason", "CAPTCHA_CHALLENGE"), ("Content-Type", "text/html")], CF_HTML, "service"),
        "a Seraph denied header on a 401": (401, seraph, b"", "service"),
        "an X-Authentication-Denied-Reason header": (403, [("X-Authentication-Denied-Reason", "AUTHENTICATION_DENIED")], b"", "service"),
        "a JSON 401 with errorMessages plus cf-ray (E9)": (401, [("CF-RAY", "abc"), ("Content-Type", "application/json")], JIRA_JSON, "service"),
        "a plain-text 401 (the generic rule 9)": (401, [("Content-Type", "text/plain")], b"Unauthorized", "service"),
    }
    for label, (status, headers, body, want) in controls.items():
        check_eq(f"AK3 control: {label}", kind(status, headers, body, service="jira"), want)
    check_eq("E8 control: Seraph LoginReason OK is NOT a denial (a 403 HTML behind it is foreign)",
             kind(403, [("X-Seraph-LoginReason", "OK"), ("Content-Type", "text/html")], CF_HTML), "intermediary")
    check_eq("E9: a path marker alone never makes JSON foreign when the service's key is there",
             kind(403, [("server", "cloudflare")], JIRA_JSON, service="jira"), "service")
    check_eq("E9: an authorship marker does, even with the service's key", kind(403, [("cf-mitigated", "challenge")], JIRA_JSON, service="jira"), "intermediary")
    check_eq("E10: a gateway's JSON with no key of its service -> unclear", kind(403, [], b'{"message":"Forbidden"}', service="jira"), "unclear")
    check_eq("E10: the same JSON for service=any (the generic keys) -> service", kind(403, [], b'{"message":"Forbidden"}'), "service")
    check_eq("E10: an unknown service name falls back to the generic keys", kind(403, [], b'{"message":"Forbidden"}', service="nobody"), "service")
    check_eq("E10: a JSON list has no message -> unclear", kind(403, [], b'[1,2]', service="jira"), "unclear")
    check_eq("E11: HTML with no headers -> unclear, nobody named",
             (H.classify(403, None, CF_HTML)["kind"], H.classify(403, None, CF_HTML)["via"]), ("unclear", None))
    check_eq("E32 (pinned as it behaves today): a reverse proxy's 401 + WWW-Authenticate -> service (the forbidden side, named residual)",
             kind(401, [("WWW-Authenticate", 'Basic realm="proxy"')], b"", service="jira"), "service")
    check_eq("WWW-Authenticate on a 403 is not the login's request for credentials", kind(403, [("WWW-Authenticate", "Basic")], b"", service="jira"), "empty")
    check_eq("3xx -> redirect", kind(302, [("Location", "/x")], b""), "redirect")
    # rule 5 before rule 8: an unreadable body is never taken for an empty one
    check_eq("E14: an unreadable read is unclear, not empty", kind(401, [], b"", unreadable=True), "unclear")
    check_eq("E14: a readable empty body is empty", kind(401, [], b"", unreadable=False), "empty")
    check_eq("a multi-byte character cut by the bound is not 'not UTF-8'",
             kind(401, [], ("x" * 65535 + "é").encode("utf-8"), truncated=True), "unclear")   # cut text, not 401->service
    check_eq("a BOM before the page does not hide it", kind(403, [("Content-Type", "text/plain")], b"\xef\xbb\xbf  <!DOCTYPE HTML><html></html>"), "intermediary")


def the_bounds(stub):
    n = 1000
    for size, want_cut in ((n - 1, False), (n, False), (n + 1, True), (n + 500, True)):
        stub.route = (200, [("Content-Type", "application/octet-stream")], b"a" * size)
        a = H.fetch(stub.url, timeout=5, max_body=n)
        check_eq(f"E5: {size} bytes against a bound of {n} -> truncated {want_cut}, never more than {n} kept",
                 (a.truncated, len(a.body)), (want_cut, min(size, n)))
    stub.route = (403, CF_HEADERS, b"<html><title>t</title>" + b"z" * 3000)
    a = H.fetch(stub.url, timeout=5, max_body=100)
    check_eq("E5: the error body is bounded the same way", (a.truncated, len(a.body), a.verdict["kind"]), (True, 100, "intermediary"))
    for bad in (None, 0, -1, "5"):
        try:
            H.fetch(stub.url, timeout=bad)
            ok = False
        except ValueError:
            ok = True
        check(f"the timeout is required: {bad!r} -> ValueError", ok)
    try:
        H.fetch(stub.url, timeout=5, max_body=-1)
        ok = False
    except ValueError:
        ok = True
    check("a negative max_body -> ValueError", ok)


def the_stalled_body():
    """B-408 F1: a timeout while reading the body AFTER the status arrived is `unreadable` on EVERY status, the status is kept,
    nothing is raised (a raised timeout would turn a stand that answered into 'no answer')."""
    stall = StallStub(200)
    try:
        for status in (200, 500, 403):
            stall.status = status
            answer = H.fetch(stall.url, timeout=1, max_body=1000)
            check_eq(f"F1: a {status} whose body stalls keeps its status and is unreadable (not raised, not empty)",
                     (answer.status, answer.unreadable, answer.body), (status, True, b""))
            check_eq(f"F1: ... and an unreadable body is `unclear` on a {status} unless the status itself decides",
                     answer.verdict["kind"], "ok" if status == 200 else "unclear")
    finally:
        stall.close()
    # the timeout BEFORE any status is still urllib's own exception (E15)
    import socket
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen(1)
    try:
        try:
            H.fetch(f"http://127.0.0.1:{sock.getsockname()[1]}/", timeout=0.5)
            said = "answered"
        except (TimeoutError, urllib.error.URLError):
            said = "raised"
        check_eq("F1 / E15: no status at all (the server accepted and said nothing) is still the raised timeout", said, "raised")
    finally:
        sock.close()


def the_boundary_of_an_error_body():
    """B-408 F2: ONE construction path for an `Answer` of an error: `fetch` and `error_answer` (the Jira client's caller) read
    N+1 bytes and call a body cut only when it is MORE than N (E5)."""
    stub = Stub()
    try:
        for size in (H_LIMIT - 1, H_LIMIT, H_LIMIT + 1):
            text = b"x" * size
            stub.route = (401, [("Content-Type", "text/plain")], text)
            via_fetch = H.fetch(stub.url, timeout=5, max_body=H_LIMIT)
            error = urllib.error.HTTPError("http://x", 401, "u", {"Content-Type": "text/plain"}, io.BytesIO(text))
            via_error = H.error_answer(error, "http://x", max_body=H_LIMIT)
            want = (size > H_LIMIT, len(text[:H_LIMIT]), "unclear" if size > H_LIMIT else "service")
            check_eq(f"F2: a {size}-byte 401 text through fetch: truncated only beyond {H_LIMIT}, kind follows",
                     (via_fetch.truncated, len(via_fetch.body), via_fetch.verdict["kind"]), want)
            check_eq("F2: ... and through error_answer, the same", (via_error.truncated, len(via_error.body), via_error.verdict["kind"]), want)
    finally:
        stub.close()


H_LIMIT = 65536


def the_read_error():
    class Broken(urllib.error.HTTPError):
        def read(self, *a):
            raise OSError("reset")

    broken = Broken("http://x", 403, "f", {}, None)
    check_eq("read_error: a read that raises -> (b'', unreadable)", H.read_error(broken, 100), (b"", True))
    empty = urllib.error.HTTPError("http://x", 403, "f", {}, None)
    check_eq("read_error: an empty body that read fine -> (b'', not unreadable)", H.read_error(empty, 100), (b"", False))
    full = urllib.error.HTTPError("http://x", 403, "f", {}, io.BytesIO(b"0123456789"))
    check_eq("read_error: bounded by the limit", H.read_error(full, 4), (b"0123", False))


def the_text_cleanup():
    html_page = ("<html><head><title>  Bl&amp;ocked\u0007\n &lt;by&gt;  " + "w" * 200 + "</title></head></html>").encode("utf-8")
    v = H.classify(403, [("Content-Type", "text/html")], html_page)
    title = v["title"]
    check("E18: entities unescaped, whitespace collapsed, control byte gone", title.startswith("Bl&ocked <by> www") and "\u0007" not in title and "\n" not in title, repr(title))
    check_eq("E18: at most 120 characters plus '...'", (len(title), title.endswith("...")), (123, True))
    leaky = b"<html><title>Denied for s3cr3t-value</title></html>"
    v = H.classify(403, [("Content-Type", "text/html")], leaky, secrets=("s3cr3t-value", ""))
    check_eq("E17: a secret value in the page is redacted, in the title and in the sentence",
             ("s3cr3t-value" in json.dumps(v), "<redacted>" in v["title"], "s3cr3t-value" in H.describe(403, v)), (False, True, False))
    check_eq("E17: an empty secret does not blank the text", "Denied" in v["title"], True)
    sentence = H.describe(403, H.classify(403, [("Server", "cloudflare"), ("Content-Type", "text/html")], CF_HTML))
    check_in("describe names the title", "Attention Required! | Cloudflare", sentence)
    check_in("describe names the path", "Cloudflare", sentence)
    check_not_in("describe never says 'token' or 'renew'", "renew", sentence)
    unclear = H.describe(403, H.classify(403, None, CF_HTML))
    check_in("FR-41: an `unclear` sentence says it could not be told, and names no author", "could not be told", unclear)
    check_not_in("FR-41: ... and no protection service", "protection", unclear)
    long = H.describe(403, {"kind": "unclear", "said": "x" * 1000})
    check("describe is bounded", len(long) <= 300, str(len(long)))


def the_table_world():
    real = H.ANSWERS_PATH
    root = temp_dir("qa-http-answers-")
    try:
        H.ANSWERS_PATH = root / "absent.json"          # E19: before the file exists / a broken install
        H.reload_tables()
        v = H.classify(403, [("X-Seraph-LoginReason", "CAPTCHA_CHALLENGE"), ("Content-Type", "text/html")], CF_HTML)
        check_eq("E19: no table: a CAPTCHA 403 with an HTML body -> intermediary, the safe side; table says unreadable",
                 (v["kind"], v["table"]), ("intermediary", "unreadable"))
        check_eq("E19: no table: JSON with a message key is `unclear`, never service", kind(403, [], JIRA_JSON), "unclear")
        broken = root / "broken.json"
        broken.write_text("{not json", encoding="utf-8")
        H.ANSWERS_PATH = broken
        H.reload_tables()
        check_eq("E19: an unreadable table gives the same empty tables", H.classify(403, [], CF_HTML)["table"], "unreadable")
        H.ANSWERS_PATH = real
        H.reload_tables()
        check_eq("control: the shipped table is read", H.classify(403, [], CF_HTML)["table"], "ok")
        data = json.loads(real.read_text(encoding="utf-8"))
        check("the shipped table has every key the code reads",
              {"classify_limit_bytes", "title_limit_chars", "service_auth_headers", "authorship_markers", "path_markers",
               "message_keys", "service_message_keys"} <= set(data))
    finally:
        H.ANSWERS_PATH = real
        H.reload_tables()
        cleanup(root)


def the_door():
    real = sys.platform
    try:
        sys.platform = "win32"
        win = H.curl_line("https://user:pw@jira.example.invalid:8443/rest/api/2/serverInfo?token=abc#x")
        sys.platform = "linux"
        nix = H.curl_line("https://user:pw@jira.example.invalid:8443/rest/api/2/serverInfo?token=abc#x")
    finally:
        sys.platform = real
    check_eq("E26: curl.exe on win32, a GET that prints the status and content type, the safe address, no credential",
             win, 'curl.exe -sS -o NUL -w "%{http_code} %{content_type}\\n" https://jira.example.invalid:8443/rest/api/2/serverInfo')
    check_eq("E26: curl elsewhere writes to /dev/null", nix,
             'curl -sS -o /dev/null -w "%{http_code} %{content_type}\\n" https://jira.example.invalid:8443/rest/api/2/serverInfo')
    check("E26: no userinfo, query or fragment in either", all(x not in win + nix for x in ("pw", "token", "abc", "#", "?", "-I ")))
    check_eq("safe_url of an address with nothing to strip is unchanged", H.safe_url("http://127.0.0.1:81/a/b"), "http://127.0.0.1:81/a/b")


def the_failures_pass_through():
    stub = Stub()
    url = stub.url
    stub.close()           # nothing listens there now
    try:
        H.fetch(url, timeout=2)
        said = "answered"
    except urllib.error.URLError:
        said = "URLError"
    check_eq("E15: a refused connection is urllib's own URLError, unchanged", said, "URLError")
    out, err = io.StringIO(), io.StringIO()
    old = os.environ.get("http_proxy")
    os.environ["http_proxy"] = os.environ["HTTP_PROXY"] = "http://proxyuser:proxypass@127.0.0.1:1/"
    os.environ["no_proxy"] = os.environ["NO_PROXY"] = ""
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                H.fetch("http://jira.example.invalid/x", timeout=2)
            except Exception:  # noqa: BLE001 - what matters is what was PRINTED
                pass
    finally:
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("http_proxy", None)
        if old is not None:
            os.environ["http_proxy"] = old
        os.environ["no_proxy"] = os.environ["NO_PROXY"] = "127.0.0.1,localhost"
    check("E16: urllib's proxy handling is kept and the helper prints nothing (a proxy URL's value is never printed)",
          out.getvalue() == "" and err.getvalue() == "" and "proxypass" not in repr(H.classify(502, None, b"")))


# ---- the sign-in answers built on the client (FV1-17a): one table, the host's answer and the project's config are the input ----
import stand_access as SA  # noqa: E402
import config_contract as CC  # noqa: E402
import env_probe as EP  # noqa: E402

VALUES = {"U": "admin@example.invalid", "S": "not-a-real-secret"}
LOCAL = {"kind": "local_login", "url": "/login", "user_key": "U", "secret_key": "S", "user_field": "email",
         "secret_field": "password"}
FORM = {"kind": "form_login", "user_key": "U", "secret_key": "S", "user_field": "email", "secret_field": "password"}
FORM_UNRECORDED = {"kind": "form_login", "user_key": "U", "secret_key": "S"}


def jb(node, status=200):
    return (status, [("Content-Type", "application/json")], json.dumps(node).encode())


HTML = (200, [("Content-Type", "text/html")], b"<html><head><title>Sign in</title></head><body>token</body></html>")


class SignStub:
    """A routed loopback stub: `routes[(METHOD, path)]` is (status, headers, body) or a callable of the seen request."""

    def __init__(self):
        self.routes, self.seen = {}, []
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def _answer(self):
                size = int(self.headers.get("Content-Length") or 0)
                request = {"method": self.command, "path": self.path.split("?")[0], "headers": dict(self.headers.items()),
                           "body": self.rfile.read(size) if size else b""}
                stub.seen.append(request)
                route = stub.routes.get((self.command, request["path"]), (404, [], b""))
                if route == "STALL":
                    self.send_response(200)
                    self.send_header("Content-Length", "1000")
                    self.end_headers()
                    self.wfile.write(b"{")
                    self.wfile.flush()
                    time.sleep(1.5)
                    return
                status, headers, body = route(request) if callable(route) else route
                self.send_response(status)
                for name, value in headers:
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            do_GET = do_POST = _answer  # noqa: N815

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.handle_error = lambda *a: None
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def form_routes(stub, session_kind="user", location=None):
    def submit(req):
        form = urllib.parse.parse_qs(req["body"].decode())
        cookie = req["headers"].get("Cookie", "")
        good = (form.get("email") == ["admin@example.invalid"] and form.get("password") == ["not-a-real-secret"]
                and form.get("csrfToken") == ["csrf-tok-123"] and form.get("json") == ["true"] and "a=1" in cookie and "b=2" in cookie)
        if good:
            return (302, [("Location", location or "/"), ("Set-Cookie", "session=sess-val-999; Path=/")], b"")
        return (302, [("Location", stub.base + "/api/auth/signin?error=CredentialsSignin")], b"")

    def session(req):
        if session_kind == "html":
            return HTML
        signed = "session=sess-val-999" in req["headers"].get("Cookie", "")
        return jb({"user": {"name": "x"}} if signed and session_kind == "user" else {})
    stub.routes[("GET", "/api/auth/csrf")] = (200, [("Content-Type", "application/json"), ("Set-Cookie", "a=1; Path=/"),
                                                    ("Set-Cookie", "b=2; HttpOnly")], b'{"csrfToken": "csrf-tok-123"}')
    stub.routes[("POST", "/api/auth/callback/credentials")] = submit
    stub.routes[("GET", "/api/auth/session")] = session


def padded(total, token_first):
    head = '{"token": "t-ok", "pad": "' if token_first else '{"pad": "'
    tail = '"}' if token_first else '", "token": "t-ok"}'
    return (head + "x" * (total - len(head) - len(tail)) + tail).encode()


def sign_in_rows():
    """(id, route for POST /login, access, wanted answer)"""
    short = {"timeout": 0.5}
    rows = [("H-404-local", (404, [], b""), "wrong_door"), ("H-405-local", (405, [], b""), "wrong_door"),
            ("H-200-html-token-word", HTML, "wrong_door"), ("H-200-json-no-token", jb({"ok": True}), "wrong_door"),
            ("H-200-empty", (200, [], b""), "wrong_door"),
            ("H-302-local", (302, [("Location", "/signin")], b""), "wrong_door"),
            ("H-401-empty", (401, [], b""), "unjudged"),
            ("H-401-detail-json", jb({"detail": "Invalid credentials"}, 401), "credentials_refused"),
            ("H-403-csrf-json", jb({"message": "CSRF token missing"}, 403), "unjudged"),
            ("H-403-html", (403, [("Content-Type", "text/html")], b"<html><title>Denied</title></html>"), "unjudged"),
            ("H-400-sent-fields-service", jb({"detail": [{"loc": ["body", "email"], "msg": "bad"}]}, 400), "credentials_refused"),
            ("H-400-unsent-field", jb({"detail": [{"loc": ["body", "login"], "msg": "required"}]}, 400), "body_shape"),
            ("H-429", (429, [], b""), "throttled"), ("H-503", (503, [], b""), "stand_error"),
            ("H-timeout", lambda r: (time.sleep(1.2), (200, [], b"{}"))[1], "no_answer"), ("H-stalled-2xx", "STALL", "no_answer"),
            ("adv-token-true", jb({"token": True}), "wrong_door"), ("adv-token-list", jb({"token": [1]}), "wrong_door"),
            ("adv-token-empty", jb({"token": "  "}), "wrong_door"), ("adv-token-null", jb({"token": None}), "wrong_door"),
            ("body-at-262144", (200, [], padded(262144, True)), "in"),
            ("body-beyond-262144", (200, [], padded(262150, False)), "wrong_door")]
    for case, route, want in rows:
        yield case, route, want, short if case in ("H-timeout", "H-stalled-2xx") else {}


def the_sign_in_rows():
    stub = SignStub()
    try:
        for case, route, want, extra in sign_in_rows():
            stub.routes, stub.seen = {("POST", "/login"): route}, []
            receipt = SA.login(LOCAL, VALUES, stub.base, extra.get("timeout", 4.0))
            check_eq(f"{case}: answer", receipt["answer"], want)
            check_eq(f"{case}: status follows the answer", receipt["status"], "ok" if want == "in" else "failed")
            check(f"{case}: no credential in the receipt", all(v not in json.dumps(receipt) for v in VALUES.values()))
        stub.routes, stub.seen = {("POST", "/login"): jb({"access_token": "tok-value-1"})}, []
        check_eq("H-200-token: in, once", (SA.login(LOCAL, VALUES, stub.base)["answer"], len(stub.seen)), ("in", 1))
        closed = SignStub()
        base = closed.base
        closed.close()
        check_eq("H-refused: no_answer", SA.login(LOCAL, VALUES, base, 2.0)["answer"], "no_answer")
        # the form road
        for case, access, session, values, want, posts in (
                ("form-csrf-ok-in", FORM, "user", VALUES, "in", 1),
                ("form-wrong-password", FORM, "user", dict(VALUES, S="wrong-one-x"), "credentials_refused", 1),
                ("form-unrecorded-fields-refused", FORM_UNRECORDED, "user", dict(VALUES, S="wrong-one-x"), "fields_unconfirmed", 1),
                ("form-session-empty", FORM, "empty", VALUES, "unjudged", 1), ("form-session-html", FORM, "html", VALUES, "wrong_door", 1)):
            stub.routes, stub.seen = {}, []
            form_routes(stub, session)
            receipt = SA.login(access, values, stub.base, 4.0)
            check_eq(f"{case}: answer", receipt["answer"], want)
            check_eq(f"{case}: at most 3 requests, one submit", (len(stub.seen) <= 3, sum(r["method"] == "POST" for r in stub.seen)), (True, posts))
            blob = json.dumps(receipt)
            check(f"{case}: the secret, csrf and cookie values and the raw query are absent",
                  all(x not in blob for x in (*values.values(), "csrf-tok-123", "sess-val-999", "CredentialsSignin", "error=")))
            if case == "form-csrf-ok-in":
                cookie = next(r for r in stub.seen if r["method"] == "POST")["headers"].get("Cookie", "")
                check_eq("form-two-set-cookie: both csrf-step cookies are sent back", ("a=1" in cookie, "b=2" in cookie), (True, True))
        stub.routes, stub.seen = {}, []
        form_routes(stub, location="http://other.invalid/x?next=1")
        receipt = SA.login(FORM, VALUES, stub.base, 4.0)
        check_eq("form-location-other-host: decided by the session, the url never printed",
                 (receipt["answer"], "other.invalid" in json.dumps(receipt)), ("in", False))
        stub.routes, stub.seen = {}, []
        check_eq("form-csrf-404: wrong_door, nothing submitted", (SA.login(FORM, VALUES, stub.base)["answer"], len(stub.seen)), ("wrong_door", 1))
        stub.routes[("GET", "/api/auth/csrf")] = jb({})
        stub.seen = []
        check_eq("form-csrf-no-token: wrong_door, nothing submitted",
                 (SA.login(FORM, VALUES, stub.base)["answer"], [r["method"] for r in stub.seen[1:]]), ("wrong_door", []))
        # the table is unreadable: a proof still stands, an HTTP answer is unjudged, an exception stays no_answer (I2, I3)
        root = temp_dir("qa-sign-in-")
        real = EP.STAND_ANSWERS_PATH
        try:
            EP.STAND_ANSWERS_PATH = root / "absent.json"
            EP.reload_stand_answers()
            stub.routes, stub.seen = {("POST", "/login"): (404, [], b"")}, []
            got = [SA.login(LOCAL, VALUES, stub.base)["answer"]]
            stub.routes[("POST", "/login")] = jb({"access_token": "tok-value-1"})
            got.append(SA.login(LOCAL, VALUES, stub.base)["answer"])
            got.append(SA.login(LOCAL, VALUES, base, 2.0)["answer"])
            check_eq("table-unreadable: HTTP -> unjudged, token -> in, exception -> no_answer", got, ["unjudged", "in", "no_answer"])
        finally:
            EP.STAND_ANSWERS_PATH = real
            EP.reload_stand_answers()
            cleanup(root)
        check_eq("table-control: the shipped table is read again", SA.answer_of(405, "", road="local_login"), "wrong_door")
        the_roads(stub)
    finally:
        stub.close()
    the_contract_joins()


def the_roads(stub):
    root = temp_dir("qa-roads-")
    saved = {k: os.environ.get(k) for k in ("SIGN_BASE", "U", "S")}
    os.environ.update({"SIGN_BASE": stub.base, "U": VALUES["U"], "S": VALUES["S"]})
    real_path = SA.LOGIN_ROADS_PATH

    def cfg(access=None):
        env = {"base_url_key": "SIGN_BASE", "user_key": "U", "secret_keys": ["S"], "health_path": "/health", "env_file": ""}
        if access:
            env["access"] = access
        return {"environment": env}

    def fresh(login_route=None, forms=True):
        stub.routes, stub.seen = {("GET", "/health"): jb({"status": "ok"})}, []
        if login_route:
            stub.routes[("POST", "/login")] = login_route
        if forms:
            form_routes(stub)

    def answers(out):
        return [e["answer"] for e in out["roads"]]
    try:
        fresh((405, [], b""))
        out = SA.try_roads(cfg(LOCAL), root)
        check_eq("roads-e1-shape: recorded /login is a wrong door, the form road gets in, first_in is the form road",
                 (answers(out), out["first_in"], out["spent"], [e["road"] for e in out["roads"]]),
                 (["wrong_door", "in"], 1, 0, ["a", "b:csrf-credentials-form"]))
        for case, route, want_b, spent in (("budget-refused-stops", jb({"detail": "Invalid credentials"}, 401), "refused at road 1", 1),
                                           ("budget-unjudged-spends-1", (401, [], b""), "budget of this run is spent", 1),
                                           ("budget-throttled-stops", (429, [], b""), "HTTP 429", 0)):
            fresh(route)
            out = SA.try_roads(cfg(LOCAL), root)
            check_eq(f"{case}: the later road is not tried, nothing reaches the form routes",
                     (out["roads"][1]["answer"], want_b in out["roads"][1]["why"], out["spent"],
                      [r["path"] for r in stub.seen if r["path"].startswith("/api/auth")]), ("not_tried", True, spent, []))
        out = SA.try_roads(cfg(), root)
        check_eq("no-key-names: every road not_tried, tried 0",
                 (answers(out), out["tried"], out["first_in"], "key names" in out["roads"][0]["why"]), (["not_tried"], 0, None, True))
        # candidates: at the cap and beyond it (wrong doors do not spend)
        fresh(forms=False)
        for case, count, noted in (("candidates-5-at", 5, False), ("candidates-6-beyond", 6, True)):
            out = SA.try_roads(cfg(), root, user_key="U", secret_key="S",
                               candidates=[f"local_login=/c{i}" for i in range(count)])
            check_eq(f"{case}: five tried at most", (sum(e["kind"] == "local_login" for e in out["roads"]), "candidates_note" in out),
                     (5, noted))
        code = SA.main(["--project-root", str(root), "--roads", "--candidate", "harness_command=x"])
        check_eq("candidate-bad-kind: refused, exit 2", code, 2)
        # the negative control of a harness road
        script = root / "login.py"
        for case, body, want in (("negative-refused", "import os,sys; sys.exit(0 if os.environ.get('S') == 'not-a-real-secret' else 1)", "refused"),
                                 ("negative-passed", "import sys; sys.exit(0)", "passed")):
            script.write_text(body, encoding="utf-8")
            fresh(forms=False)
            out = SA.try_roads(cfg(), root, command=f'"{sys.executable}" "{script}"', user_key="U", secret_key="S")
            road = next(e for e in out["roads"] if e["road"] == "c")
            check_eq(f"{case}: the answer stays in", (road["answer"], road.get("negative"), out["first_in"] is not None), ("in", want, True))
            check(f"{case}: the junk secret is never printed", "qa-factory-wrong-" not in json.dumps(out))
        out = SA.try_roads(cfg(), root, command=f'"{sys.executable}" "{script}"', user_key="U", secret_key="S", negative=False)
        check_eq("negative off: not_run", next(e for e in out["roads"] if e["road"] == "c").get("negative"), "not_run")
        # the budget numbers are data, clamped by the code
        for case, raw, want, noted in (("budget-value-absent", None, 1, False), ("budget-value-0", 0, 1, False),
                                       ("budget-value-x", "x", 1, False), ("budget-value-3", 3, 3, False), ("budget-value-4", 4, 3, True)):
            SA.LOGIN_ROADS_PATH = root / f"{case}.json"
            SA.LOGIN_ROADS_PATH.write_text(json.dumps({"budget": {} if raw is None else {"real_secret_failures": raw}, "forms": []}), encoding="utf-8")
            got = SA.login_roads()
            check_eq(f"{case}: clamped", (got["budget"]["real_secret_failures"], "budget_note" in got, got["table"]), (want, noted, "unreadable"))
    finally:
        SA.LOGIN_ROADS_PATH = real_path
        for key, value in saved.items():
            os.environ.pop(key, None) if value is None else os.environ.__setitem__(key, value)
        cleanup(root)


def the_contract_joins():
    ui = {"kind": "ui_only"}
    receipt = SA.login(ui, {}, "http://x.invalid")
    check_eq("ui-only: skipped, not_tried, no key needed", (receipt["status"], receipt["answer"], SA.login_keys(ui), SA.code_login_declined(ui)),
             ("skipped", "not_tried", [], True))
    check_eq("source-registry: set by login(), `access` by default",
             (SA.login(ui, {}, "", source="registry")["source"], receipt["source"]), ("registry", "access"))
    e5 = {"login_probe": {"user_key": "U", "outcome": "ok", "status": 0, "checked_at": "2026-11-12T10:00:00", "seconds": 60}}
    got = SA.recorded_login(e5)
    check_eq("recorded-login-e5-status-0: status None, answer never guessed", (got["recorded"], got["status"], got["answer"], got["outcome"]),
             (True, None, None, "ok"))
    check_eq("recorded-login: not a dict -> not recorded", SA.recorded_login({"login_probe": "x"})["recorded"], False)
    probe = {"user_key": "AUTH_USER", "outcome": "ok", "checked_at": "2026-11-12T10:00:00"}
    check_eq("record-answer-validates", CC.access_errors({"kind": "form_login", "form": "csrf-credentials-form",
                                                          "login_probe": dict(probe, answer="in", status=200)}), [])
    check_in("form-unknown-id-refused", "environment.access.form must be one of", CC.access_errors({"kind": "form_login", "form": "nope"})[0])
    check_in("answer-word-refused", "login_probe.answer must be one of", " ".join(CC.access_errors({"kind": "none", "login_probe": dict(probe, answer="maybe")})))
    check_in("status-0-refused", "must be an HTTP code (100..599)", " ".join(CC.access_errors({"kind": "none", "login_probe": dict(probe, status=0)})))
    check_eq("one tuple: ACCESS_KINDS and LOGIN_ANSWERS are the module's own", (CC.ACCESS_KINDS is SA.KINDS, CC.LOGIN_ANSWERS is SA.ANSWERS), (True, True))


def the_stand_login_joins():
    """FV1-15 join rows: the story-time search (`project_decisions.record_stand_login`), the probe that follows it, and the readers
    of a recorded answer (`stand_health._login_receipt`, remedy L0). Expected values are the card's (docs/tasks/specs/
    20261114-fv1-17-15-cards-redraft-spec.md, FV1-15 D6, P4, P5, edges E-D5), not read from the code they judge."""
    import project_decisions as PD
    import stand_health as SH
    stub = SignStub()
    root = temp_dir("qa-stand-login-")
    saved = {k: os.environ.get(k) for k in ("SIGN_BASE", "SIGN_U", "SIGN_S")}
    os.environ.update({"SIGN_BASE": stub.base, "SIGN_U": VALUES["U"], "SIGN_S": VALUES["S"]})
    named = dict(LOCAL, user_key="SIGN_U", secret_key="SIGN_S")   # the contract wants variable NAMES of two characters or more
    config_path = root / "qa-factory" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    words = root / "words.txt"
    words.write_text("find the way in", encoding="utf-8")

    def write_config(access, extra=None):
        env = {"base_url_key": "SIGN_BASE", "user_key": "SIGN_U", "secret_keys": ["SIGN_S"], "health_path": "/health", "env_file": ""}
        if access:
            env["access"] = access
        config_path.write_text(json.dumps({"environment": env, **(extra or {})}, indent=2), encoding="utf-8")

    def fresh(login_route):
        stub.routes, stub.seen = {("GET", "/health"): jb({"status": "ok"}), ("POST", "/login"): login_route}, []
        form_routes(stub)
    try:
        # E1: the recorded `local_login /login` is a wrong door (405); the form road signs in -> recorded, and the probe exits 0
        write_config(named)
        fresh((405, [], b""))
        got = PD.record_stand_login(root, words="find the way in")
        saved_config = json.loads(config_path.read_text(encoding="utf-8"))
        access = saved_config["environment"]["access"]
        check_eq("stand-login-e1: the form road is recorded, replacing the local login",
                 (got["road"], got["kind"], got["replaced"], access["kind"], access["form"], access["login_probe"]["answer"],
                  access["login_probe"]["outcome"]), ("b:csrf-credentials-form", "form_login", "local_login", "form_login",
                                                      "csrf-credentials-form", "in", "ok"))
        check("stand-login-e1: the decision row keeps the person's words, no credential in the record",
              got["decision"].startswith("DD-") and all(v not in json.dumps(saved_config) for v in VALUES.values()))
        result = EP.probe(saved_config, "", root=root)
        check_eq("stand-login-e1: the probe that follows exits 0 (no Layer-1 line), login in", (result["layer1"], result["login"]["answer"]),
                 ([], "in"))
        # none in: refused, the config bytes unchanged, no registry row left open
        for case, route in (("stand-login-none-in-401-empty", (401, [], b"")), ("stand-login-none-in-429", (429, [], b""))):
            write_config(named)
            before = config_path.read_bytes()
            backlog = root / "qa-factory" / "factory-backlog.md"
            had = backlog.read_bytes() if backlog.exists() else None
            fresh(route)
            try:
                PD.record_stand_login(root, words="find the way in")
                refusal = ""
            except ValueError as exc:
                refusal = str(exc)
            check_in(f"{case}: refused, naming the roads and their answers", "no way in signed in (a: ", refusal)
            check_in(f"{case}: ...and that nothing was written", "nothing was written", refusal)
            check(f"{case}: the config bytes and the registry are unchanged",
                  config_path.read_bytes() == before and (backlog.read_bytes() if backlog.exists() else None) == had)
        # the recorded way already signs in: unchanged
        write_config(named)
        before = config_path.read_bytes()
        fresh(jb({"access_token": "tok-value-1"}))
        check_eq("stand-login-a-in: unchanged, nothing written", (PD.record_stand_login(root, words="find the way in"),
                                                                  config_path.read_bytes() == before), ({"unchanged": True}, True))
        # no config file: today's refusal; the CLI turns a refusal into one stderr line and exit 2
        lone = temp_dir("qa-stand-login-none-")
        try:
            PD.record_stand_login(lone, words="x")
            none_refusal = ""
        except ValueError as exc:
            none_refusal = str(exc)
        check_in("stand-login-no-config: today's `_project_config` refusal", "does not exist", none_refusal)
        cleanup(lone)
        write_config(named)
        fresh((401, [], b""))
        args = PD._build_parser().parse_args(["--root", str(root), "stand-login", "--words-file", str(words)])
        err = io.StringIO()
        code = None
        with contextlib.redirect_stderr(err):
            try:
                PD._record_stand_login(args)
            except SystemExit as exc:
                code = exc.code
        check_eq("stand-login-cli-refusal: one stderr line, exit 2", (code, err.getvalue().count("\n"), "stand-login refused" in err.getvalue()),
                 (2, 1, True))
        # the readers of a recorded answer
        probe = {"user_key": "SIGN_U", "outcome": "ok", "status": 0, "checked_at": "2026-11-12T10:00:00", "seconds": 60}
        got = SH._login_receipt({"environment": {"access": {"kind": "harness_command", "login_probe": probe}}})
        check_eq("stand-health-e5: status 0 is no code: proved by the project's login command",
                 (got["outcome"], "proved" in got["sentence"], "login command" in got["sentence"], "contradicts" in got["sentence"]),
                 ("proved", True, True, False))
        failed = {"user_key": "SIGN_U", "outcome": "failed", "status": 405, "checked_at": "2026-11-12T10:00:00"}
        wrong = SH._login_receipt({"environment": {"access": {"kind": "local_login", "login_probe": dict(failed, answer="wrong_door")}}})["sentence"]
        old = SH._login_receipt({"environment": {"access": {"kind": "local_login", "login_probe": failed}}})["sentence"]
        check_eq("remedy-l0: answer wrong_door -> the door's remedy and the plain words; no answer + 405 -> today's, nothing guessed",
                 ("find the way in" in wrong, "its answer did not look like a sign-in" in wrong, "find the way in" in old,
                  "its answer did not" in old), (True, True, False, False))
        unjudged = SH._login_receipt({"environment": {"access": {"kind": "local_login", "login_probe": dict(failed, answer="unjudged")}}})["sentence"]
        check_eq("remedy-l0: unjudged says it did not show, and offers no door", ("its answer did not show whether a sign-in is there" in unjudged,
                                                                                  "find the way in" in unjudged), (True, False))
        check_eq("remedy-answer-not-a-word: read as absent", "its answer did not" in SH._login_receipt(
            {"environment": {"access": {"kind": "local_login", "login_probe": dict(failed, answer="maybe")}}})["sentence"], False)
        # _derived_frontend reads the record through `recorded_login`: a harness access whose record is not `ok` derives nothing
        check_eq("derived-frontend-reads-recorded-login: outcome ` ok ` (padded) and `maybe`",
                 [SA.recorded_login({"login_probe": {"user_key": "SIGN_U", "outcome": o}})["outcome"] for o in (" ok ", "maybe")], ["ok", None])
    finally:
        stub.close()
        for key, value in saved.items():
            os.environ.pop(key, None) if value is None else os.environ.__setitem__(key, value)
        cleanup(root)


def main():
    stub = Stub()
    try:
        the_user_agent(stub)
        the_four_kinds(stub)
        the_bounds(stub)
    finally:
        stub.close()
    the_error_direction()
    the_stalled_body()
    the_boundary_of_an_error_body()
    the_read_error()
    the_text_cleanup()
    the_table_world()
    the_door()
    the_failures_pass_through()
    the_sign_in_rows()
    the_stand_login_joins()
    finish("http_client")


if __name__ == "__main__":
    main()
