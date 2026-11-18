"""The S0 scenarios of the story runner (t-017 D1, B-155 piece 2 of the split of test_story_run.py).

S0 by code: the story's one ticket snapshot is `work/ticket-snapshot.json`, the adapter's stdout byte for
byte; a story in flight with only the old `.md` gets it once; and every stop S0 raises is a question with
doors the next entry READS - `go on` passes that block only and is written down, a stand's name or a kept
launch source corrects the launch, a pasted ticket becomes the ticket, and anything else comes back as a
question with a changed body - with no conductor call anywhere on the way. The stub `claude`, the temp-project
builders, the helpers and `run_scenarios` live in `story_run_common.py`.

t-267 / t-278 (D-06): the ticket is read by REST in a light form and never through the tracker agent. A fake Jira
on localhost (`FakeJira`) serves the TP1-15045 fixture to the real adapter in a real driver process; the keys
printed as `K5`, `K6`, `K11`, `K13` (and the person-vs-tracker line, F27) are the spec's own.
"""
# Shared helpers of test_story_run_s0.py, split by tools/test_split.py (TD-11c).
import json
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from story_run_common import s0_project, stub_calls


UNREAD_LEAD = "is not one of the answers this question takes, so nothing has moved yet."      # the ONE lead of an unread answer (G17)


# A conductor that gives no usable options (`ask_person` with none): the seam answers with the SITE's own question again (G2).
NO_USABLE = {"conductor": {"action": "ask_person", "question": "", "did": "no options"}}


def conductor_count(root: Path) -> int:
    """The conductor calls the stub saw: D-0041 - every unread `--answer` is exactly one."""
    return len([c for c in stub_calls(root) if c["kind"] == "conductor"])


def price_broken(text: str) -> list:
    """The options of a question's priced section that lack their three price lines (item 6), token or not: [] is clean."""
    import human_text
    return human_text.price_problems(text, None)


FIX = harness.FIXTURES / "ticket-15045"


RAW_15045 = (FIX / "raw-issue.json").read_bytes()


FIELDS_15045 = (FIX / "field.json").read_bytes()


KEY = "TP1-15045"


PERSON_TOKEN_ENV = {"QA_JIRA_EMAIL": "reader@example.invalid", "QA_JIRA_API_TOKEN": "test-only-token"}


class FakeJira:
    """A Jira on localhost for a REAL driver process: the first route whose text is in the request path answers
    (bytes = 200, an int = that status); every request path is logged. `routes` can be swapped between two
    runs (`serve`), which is how a tracker that was down comes back."""

    def __init__(self, routes=()):
        self.routes, self.log = list(routes), []
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.log.append(self.path)
                for needle, answer in owner.routes:
                    if needle in self.path:
                        if isinstance(answer, int):
                            self.send_response(answer)
                            self.end_headers()
                            return
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(answer)
                        return
                self.send_response(500)
                self.end_headers()

            def log_message(self, *_args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def serve(self, routes) -> None:
        self.routes = list(routes)

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def direct_api(self, **extra) -> dict:
        return {"base_url": self.base_url, "api_version": "2", "auth_type": "basic_token",
                "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN",
                "acceptance_criteria_fields": [], "custom_fields": [], **extra}


def story_15045(*extra):
    """The routes of a healthy read of the TP1-15045 fixture: the issue with every field, the remote links, `/field`."""
    return [*extra, (f"/issue/{KEY}/remotelink", b"[]"), (f"/issue/{KEY}?fields=*all", RAW_15045), ("/rest/api/2/field", FIELDS_15045)]


def rest_project(jira: "FakeJira", task: str = KEY, *, git: bool = True, method: str = "agent", **adapter):
    """A project whose ticket is read by REST from `jira`, with `method: agent` (the WRITE channel, as on cmp2) beside
    the `direct_api`, and a probe receipt so that readiness finds the tracker proven: S0 can run to its end."""
    ticket_cfg = {"kind": "jira", "method": method, "invoke": "jira-assistant", "direct_api": jira.direct_api(), **adapter}
    root, task_root, env = s0_project(task, git=git, config={"adapters": {"ticket": ticket_cfg}})
    env.update(PERSON_TOKEN_ENV)
    receipt = root / "qa-factory" / "state" / "integrations" / "jira-direct-probe.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    direct = ticket_cfg["direct_api"]
    receipt.write_text(json.dumps({
        "status": "available", "checked_at": datetime.now(timezone.utc).isoformat(),
        "base_url": direct["base_url"], "auth_type": direct["auth_type"], "secret_ref": direct["secret_ref"],
        "username_ref": direct["username_ref"], "api_version": direct["api_version"],
        "checks": [{"name": name, "status": "available"} for name in
                   ("authenticated_identity", "sample_issue", "paginated_comments", "attachment_original")]}), encoding="utf-8")
    return root, task_root, env


def snapshot_of(task_root: Path) -> dict:
    return json.loads((task_root / "work" / "ticket-snapshot.json").read_text(encoding="utf-8"))


# --- the person's list of sources not to read, before the run (t-172 / B-231, wave B: P4, C1, C2, C5) --------------
EM = chr(0x2014)      # the dash the owner types between a source and why: `testproject1-ui!1924 - Draft MR ...`


DRAFT = "Draft MR of an earlier factory run, not a product change"


def _record(task_root: Path) -> dict:
    return json.loads((task_root / "work" / "source-exclusions.json").read_text(encoding="utf-8"))


def _no_record(task_root: Path) -> bool:
    return not (task_root / "work" / "source-exclusions.json").exists()
