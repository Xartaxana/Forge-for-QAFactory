"""Onboarding understands the access scheme and writes only the keys it used.

The trap this file reproduces, from another checkout of one test harness (23.09.2026): a
`cli/constants.py` listing ~100 `KEY_X = "X"` names, a login that reads four of them with a
default of `""`, an env file that holds none of those four — and an onboarding that put them
into `secret_keys`, where they stopped the project's first story.
"""
import json
import sys
from pathlib import Path

from harness import check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_contract import (ACCESS_KINDS, access_errors, canonical_template,
                             environment_errors, environment_key_errors, validate)
from project_inventory import (KIND_PRIORITY, access_discovery, key_role, render_access)

PHASES = Path(__file__).resolve().parents[2] / "skills" / "qa-onboarding" / "phases"

CLIENT_FACTORY = '''
from testproject1_sdk import TestProject1Client
from .credentials_manager import CredentialsManager


def get_client(username=None, password=None):
    return TestProject1Client(
        auth_server_url=CredentialsManager.get_parameter("AUTH_SERVER_URL", ""),
        auth_client_id=CredentialsManager.get_parameter("AUTH_CLIENT_ID", ""),
        auth_client_secret=CredentialsManager.get_parameter("AUTH_CLIENT_SECRET", ""),
        testproject1_api_domain=CredentialsManager.get_parameter("TESTPROJECT1_API_DOMAIN"),
        username=username or CredentialsManager.get_parameter("AUTH_USERNAME"),
        password=password or CredentialsManager.get_parameter("AUTH_PASSWORD"),
    )
    # the SDK posts to "/v1/local-auth/login" when the realm keys are empty
'''

CONSTANTS = "\n".join(f'KEY_{n} = "{n}"' for n in (
    "AUTH_SERVER_URL", "AUTH_CLIENT_ID", "AUTH_CLIENT_SECRET", "AUTH_PASSWORD",
    "AUTH_USERNAME", "AUTH_REALM_NAME", "TESTPROJECT1_API_DOMAIN", "HEADLESS", "RP_API_KEY"))

CREDENTIALS = '''
import os


def aws_fallback():
    return (os.getenv("AWS_ACCESS_KEY", ""), os.getenv("AWS_SESSION_TOKEN", ""),
            os.getenv("AWS_PROFILE", ""))
'''

ENV_FILE = ("# names only, never values\n"
            "AUTH_USERNAME=someone@example.test\n"
            "AUTH_PASSWORD=PLACEHOLDER-VALUE-1234\n"
            "TESTPROJECT1_API_DOMAIN=http://localhost:8080\n"
            "AUTH_SERVER_URL=\n"
            "VERIFY_SSL=False\n")


def make_project(root: Path) -> None:
    pkg = root / "harness" / "tests" / "utils"
    pkg.mkdir(parents=True)
    (pkg / "client_factory.py").write_text(CLIENT_FACTORY, encoding="utf-8")
    (pkg / "credentials_manager.py").write_text(CREDENTIALS, encoding="utf-8")
    cli = root / "harness" / "cli"
    cli.mkdir(parents=True)
    (cli / "constants.py").write_text(CONSTANTS, encoding="utf-8")
    (root / "harness" / ".env").write_text(ENV_FILE, encoding="utf-8")


def main() -> None:
    check_eq("the closed kind list and discovery's priority agree",
             sorted(set(KIND_PRIORITY) | {"none"}), sorted(ACCESS_KINDS))
    check_eq("a password key reads as the secret slot", key_role("AUTH_PASSWORD"), "secret_key")
    check_eq("a client id is not mistaken for a user", key_role("AUTH_CLIENT_ID"), "client_id_key")

    root = temp_dir("qa-access-discovery-")
    try:
        make_project(root)
        found = access_discovery(root)
        keys_absent = [row["key"] for row in found["keys_absent_from_env_file"]]
        env_keys = found["env_keys"]

        check_eq("the project's env file is the one chosen", found["env_file"], "harness/.env")
        check_eq("the login site decides the kind", found["proposed_access"]["kind"], "local_login")
        check_eq("the user key comes from the env file", found["proposed_access"]["user_key"],
                 "AUTH_USERNAME")
        check_eq("the secret key comes from the env file", found["proposed_access"]["secret_key"],
                 "AUTH_PASSWORD")
        check("a key read in code but absent from the file is listed apart",
              "AUTH_CLIENT_SECRET" in keys_absent and "AWS_SESSION_TOKEN" in keys_absent
              and "AWS_PROFILE" in keys_absent, f"got {keys_absent}")
        check("a key the file holds is not in the absent list", "AUTH_USERNAME" not in keys_absent)
        check("an inventory constant is not a read", "RP_API_KEY" not in
              [row["key"] for row in found["keys_read_in_code"]])
        check("a factory-owned key is flagged where it is read", all(
            row["owned_by_factory"] is False for row in found["keys_read_in_code"]))
        check("a client switch is recognised by name", any(
            row["key"] == "AWS_PROFILE" and row["client_switch"]
            for row in found["keys_read_in_code"]))
        check("the env file's names are reported", "TESTPROJECT1_API_DOMAIN" in env_keys)
        check_eq("a key the login itself reads is asked about by name",
                 [row["key"] for row in found["login_keys_absent_from_env_file"]],
                 ["AUTH_CLIENT_ID", "AUTH_CLIENT_SECRET"])
        check_eq("every other absent key is grouped by prefix, not listed one by one",
                 [(g["prefix"], g["count"]) for g in found["absent_key_groups"]], [("AWS", 3)])

        # Nothing that came out of an env file may be a value. The file's placeholder values
        # are checked by hand because this is the one rule with no second line of defence.
        dumped = json.dumps(found)
        for secret in ("someone@example.test", "PLACEHOLDER-VALUE-1234", "localhost:8080"):
            check_not_in(f"no value leaves discovery ({secret[:12]})", secret, dumped)
        check_in("the rendered proposal names the two lists", "integrations[]",
                 render_access(found))

        # An identity provider is one instance of oidc_password, not the design.
        (root / "harness" / "tests" / "utils" / "idp.py").write_text(
            'TOKEN_URL = "https://idp.example.test/realms/prod/protocol/openid-connect/token"\n'
            'def token():\n    return {"grant_type": "password"}\n', encoding="utf-8")
        oidc = access_discovery(root)
        check_eq("an OIDC token endpoint outranks a login path",
                 oidc["proposed_access"]["kind"], "oidc_password")

        # The harness's own login command is offered first when one exists.
        (root / "harness" / "cli" / "commands.py").write_text(
            'import click\n\n\n@cli.command("login")\ndef login():\n    pass\n', encoding="utf-8")
        harness_first = access_discovery(root)
        check_eq("the harness's own login command wins",
                 harness_first["proposed_access"]["kind"], "harness_command")

        # A scheme the five kinds do not model is asked, never bent into a neighbour.
        other = temp_dir("qa-access-unknown-")
        try:
            (other / "app.py").write_text(
                'from http.cookiejar import CookieJar\njar = CookieJar()\n', encoding="utf-8")
            (other / ".env").write_text("APP_URL=http://x.test\n", encoding="utf-8")
            unknown = access_discovery(other)
            check_eq("an unmodelled scheme proposes no kind",
                     unknown["proposed_access"]["kind"], "")
            check_in("and says what to ask instead", "cookie_session", unknown["proposal_note"])
        finally:
            cleanup(other)
    finally:
        cleanup(root)

    # --- shapes -------------------------------------------------------------------------
    check_eq("the canonical template still validates", validate(canonical_template()), [])
    check_eq("a config with no access block is still valid",
             environment_errors({"env_file": ".env", "user_key": "AUTH_USERNAME",
                                 "secret_keys": ["AUTH_PASSWORD"],
                                 "integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"]}]}), [])
    good = {"kind": "oidc_password", "url": "https://idp.test/realms/prod",
            "client_id_key": "AUTH_CLIENT_ID", "realm_key": "AUTH_REALM_NAME",
            "user_key": "AUTH_USERNAME", "secret_key": "AUTH_PASSWORD", "token_key": "",
            "unauth_status": [302, 401],
            "login_probe": {"user_key": "AUTH_USERNAME", "status": 200,
                            "checked_at": "2026-09-23T10:00:00+00:00"}}
    check_eq("a complete access block passes", access_errors(good), [])
    check_eq("the template's empty access block is 'not recorded', not malformed",
             access_errors(canonical_template()["environment"]["access"]), [])
    check_in("an unknown kind is refused", "access.kind must be one of",
             access_errors({**good, "kind": "keycloak"}))
    check_in("a value in a key field is refused", "must be a variable NAME",
             access_errors({**good, "user_key": "someone@example.test"}))
    check_in("a status that is not a code is refused", "unauth_status must contain HTTP codes",
             access_errors({**good, "unauth_status": ["302"]}))
    check_in("a proof without a date is prose", "checked_at is empty",
             access_errors({**good, "login_probe": {"user_key": "AUTH_USERNAME", "status": 200}}))
    check_in("bearer_env without its token key is refused", "token_key is required",
             access_errors({"kind": "bearer_env", "unauth_status": []}))
    # OH3-10 D3: the login body's field names are validated; equal names would drop the user from the body.
    local = {"kind": "local_login", "url": "/v1/local-auth/login", "user_key": "AUTH_USERNAME",
             "secret_key": "AUTH_PASSWORD", "unauth_status": []}
    check_eq("OH3-10 D3: the template's empty user_field / secret_field are valid",
             access_errors({**local, "user_field": "", "secret_field": ""}), [])
    check_eq("OH3-10 D3: absent field names (a 0.7.x config) are valid", access_errors(local), [])
    check_eq("OH3-10 D3: two different field names are valid",
             access_errors({**local, "user_field": "email", "secret_field": "password"}), [])
    check_in("OH3-10 D3: two equal field names are refused", "both name the body field `x`",
             access_errors({**local, "user_field": "x", "secret_field": "x"}))
    check_in("OH3-10 D3: a user field equal to the DEFAULT secret field is refused", "`password`",
             access_errors({**local, "user_field": "password"}))
    check_in("OH3-10 D3: a non-string field name is refused", "user_field must be a JSON body field NAME",
             access_errors({**local, "user_field": ["email"]}))
    check_in("OH3-10 D3: a number is refused", "secret_field must be a JSON body field NAME",
             access_errors({**local, "secret_field": 5}))
    check_in("OH3-10 D3: a value (an address) in a field name is refused", "user_field must be a JSON body field NAME",
             access_errors({**local, "user_field": "someone@example.test"}))
    check_in("OH3-10 D3: the refusal reaches the whole-config validator", "user_field",
             " ".join(environment_errors({"access": {**local, "user_field": "x", "secret_field": "x"}})))
    check_not_in("OH3-10 D3: ... and a refusal prints no value", "someone@example.test",
                 " ".join(access_errors({**local, "user_field": "someone@example.test"})))
    check_in("an integration's required_by may not be empty", "required_by must be a non-empty",
             environment_errors({"integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"],
                                                   "required_by": []}]}))

    # --- the config must survive its own probe ------------------------------------------
    present = ["AUTH_USERNAME", "AUTH_PASSWORD", "TESTPROJECT1_API_DOMAIN"]
    trap = {"env_file": "harness/.env", "base_url_key": "TESTPROJECT1_API_DOMAIN",
            "user_key": "AUTH_USERNAME",
            "secret_keys": ["AUTH_PASSWORD", "AUTH_CLIENT_SECRET", "AWS_SESSION_TOKEN",
                            "AWS_PROFILE", "HEADLESS"],
            "integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"], "owner": "user"}]}
    errors = environment_key_errors(trap, present)
    check_in("a key the file does not hold is named", "AUTH_CLIENT_SECRET", errors)
    check_in("and both places it may go are named", "integrations[] with required_by", errors)
    check_in("a factory-set key is named as the factory's", "HEADLESS", errors)
    check_in("a client switch is named as one", "client-side switch", errors)
    check_eq("the keys that are present raise nothing",
             [e for e in errors if e.startswith("AUTH_PASSWORD") or e.startswith("AUTH_USERNAME")], [])
    check_eq("integrations are silent unless the check is strict",
             [e for e in errors if "integrations[0]" in e], [])
    strict = environment_key_errors(trap, present, strict_integrations=True)
    check_in("strict: an integration key with no required_by is named", "without required_by", strict)
    ok_block = {"env_file": "harness/.env", "base_url_key": "TESTPROJECT1_API_DOMAIN",
                "user_key": "AUTH_USERNAME", "secret_keys": ["AUTH_PASSWORD"],
                "access": {"kind": "local_login", "url": "/v1/local-auth/login",
                           "user_key": "AUTH_USERNAME", "secret_key": "AUTH_PASSWORD"},
                "integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"], "owner": "user",
                                  "required_by": ["api"]}]}
    check_eq("a config written by this version passes its own probe",
             environment_key_errors(ok_block, present, strict_integrations=True), [])

    # --- the phases carry the rule ------------------------------------------------------
    p1 = (PHASES / "p1-discovery.md").read_text(encoding="utf-8")
    p2 = (PHASES / "p2-interview.md").read_text(encoding="utf-8")
    p4 = (PHASES / "p4-generate.md").read_text(encoding="utf-8")
    check_in("p1 runs the access discovery", "--access", p1)
    check_in("p2 asks which access scheme is the one", "access.kind", p2)
    # OH3-8 (old -> new): p2 asked "which area or profile needs a code-only key" (pin: `required_by` in p2). The person is not
    # asked about keys any more: the keys of the DoD are quoted verbatim from the spec, with a control that CAN fail (a
    # string known to stand in p2 is found by the same helper)
    def says(text: str, needle: str) -> bool:
        return needle in text
    check("K-B5 control: the helper finds a string that is in p2", says(p2, "access.kind"))
    check("K-B5 negative control: and a string that is not in p2 is not found", not says(p2, "no such sentence 7f3a"))
    for needle in ("who owns", "required_by", "which area or profile"):
        check(f"K-B5: p2 no longer asks about keys: {needle!r} is gone", not says(p2, needle))
    for needle in ("integration_proposals", "credential_alternatives"):
        check(f"K-B5: p1 carries the writer's rule: {needle!r}", says(p1, needle))
    for needle in ("read_at", "credential_alternatives"):
        check(f"K-B5: p4 writes the new fields: {needle!r}", says(p4, needle))
    check("K-B5: p4 no longer writes the old row form", not says(p4, "{name, keys, owner, required_by}"))

    # --- HF8-11: the form of the new row fields, and the legal row with a place and no area -----------------------
    def errs(**fields) -> list:
        return environment_errors({"integrations": [dict({"name": "j", "keys": ["A_ONE", "B_ONE"]}, **fields)]})
    check_eq("K-A11: the right form has no error", errs(credential_alternatives=[["A_ONE"], ["B_ONE"]],
                                                       read_at=["tests/x/test_a.py:12"], read_at_more=1, required_by_more=2), [])
    check_eq("K-A11: absent fields are no error", errs(), [])
    check_eq("F-9 boundary: names that only CONTAIN dots or a tilde are places", errs(read_at=[
        "tests/a..b/test_a.py:3", "tests/..hidden/test_a.py:3", "tests/a~/test_a.py:3", ".github/x.py:3"]), [])
    for label, fields in (("an empty list", dict(credential_alternatives=[])), ("an empty set", dict(credential_alternatives=[[]])),
                          ("not a list", dict(credential_alternatives="A_ONE")),
                          ("a name that is a value", dict(credential_alternatives=[["someone@example.test", "B_ONE"]])),
                          ("a union that differs from keys", dict(credential_alternatives=[["A_ONE"], ["C_ONE"]])),
                          ("an absolute read_at", dict(read_at=["/home/x/test_a.py:3"])),
                          ("a drive read_at", dict(read_at=["C:\\x\\test_a.py:3"])),
                          ("a read_at that leaves the project (F-9)", dict(read_at=["../../outside/test_a.py:3"])),
                          ("a read_at with a .. segment inside (F-9)", dict(read_at=["tests/../x/test_a.py:3"])),
                          ("a read_at that is a home directory (F-9)", dict(read_at=["~/x/test_a.py:3"])),
                          ("a read_at with a trailing newline (F-9)", dict(read_at=["tests/test_a.py:3\n"])),
                          ("a read_at with no line", dict(read_at=["tests/test_a.py"])),
                          ("an empty read_at", dict(read_at=[])),
                          ("read_at_more 0", dict(read_at_more=0)), ("required_by_more 0", dict(required_by_more=0)),
                          ("read_at_more a bool", dict(read_at_more=True))):
        found = errs(**fields)
        check(f"K-A11: {label} is refused, with the field named", found and any(
            name in e for e in found for name in ("credential_alternatives", "read_at", "required_by_more", "keys")), found)
    check_in("K-A11: the union error names the names that differ", "differ in: B_ONE, C_ONE",
             " ".join(errs(credential_alternatives=[["A_ONE"], ["C_ONE"]])))
    check_not_in("K-A11: no error prints a value", "someone@example.test", " ".join(errs(credential_alternatives=[["someone@example.test"]])))
    legal = {"env_file": "harness/.env", "integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"],
                                                          "read_at": ["tests/test_a.py:4"]}]}
    check_eq("K-A12: strict: no required_by, but a place the code reads it: no error",
             environment_key_errors(legal, present, strict_integrations=True), [])
    bare = environment_key_errors({"integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"]}]}, present, strict_integrations=True)
    check_in("K-A12: neither: the old text stays", "without required_by", bare)
    check_in("K-A12: and its door names read_at", "read_at", bare)
    empty_place = environment_key_errors({"integrations": [{"name": "aws", "keys": ["AWS_ACCESS_KEY"], "read_at": []}]},
                                         present, strict_integrations=True)
    check_in("K-A12: an empty read_at is no place", "without required_by", empty_place)
    sets = {"integrations": [{"name": "j", "keys": ["A_ONE", "B_ONE"], "credential_alternatives": [["A_ONE"], ["B_ONE"]]}]}
    check_in("K-A12: sets with neither area nor place: the old error", "without required_by",
             environment_key_errors(sets, present, strict_integrations=True))
    sets["integrations"][0]["read_at"] = ["tests/test_a.py:4"]
    check_eq("K-A12: sets with a place: an unset set is no error", environment_key_errors(sets, present, strict_integrations=True), [])
    accounts_tests(p1, p2, p4)
    check_in("p4 stores the proof, not prose", "login_probe", p4)
    check_in("p4 runs the deterministic key check", "--check-environment", p4)
    check_in("OH3-10: p2 has the person confirm the login body fields phase 1 found", "confirm what phase 1 found", p2)
    check_in("OH3-10: p2 names both body field keys", "`user_field`, `secret_field`", p2)
    check_in("OH3-10: p4 writes the body field names from the login proof (login.accepted_fields)",
             "`login.accepted_fields`", p4)
    check_in("OH3-10: ... into access.user_field", "access.user_field", p4)
    # EP1-31 (t-506 5.4 #7): the keys are quoted from the spec's DoD; the negative control is `says` above
    flat4 = " ".join(p4.split())
    for needle in ("only through the sign-in page", "url_not", "manual_capture.login.http", "I do not know"):
        check(f"EP1-31: p4 tells the role how a manual capture signs in: {needle!r}", says(flat4, needle))
    check("EP1-31 negative control: a sentence p4 does not hold is not found", not says(flat4, "sign in through the moon 7f3a"))
    # RN1-3: the UI on the API's own address; the keys are quoted verbatim from the spec's DoD (§2.1.c, §2.1.d), the control CAN fail
    flat2, flat1 = " ".join(p2.split()), " ".join(p1.split())
    check("K-RN3-P0 negative control: a sentence the phases do not hold is not found", not says(flat4, "the UI lives on the moon 9c1e")
          and not says(flat2, "the UI lives on the moon 9c1e"))
    check("K-RN3-P1: p2 says where the UI is when the UI tests open the base key", says(flat2, "the UI is on the API's own address"))
    check("K-RN3-P2: p2 proposes the base key by name", says(flat2, "propose <base_url_key>"))
    check("K-RN3-P3: p4 writes url_key = the base key when topic 2 confirmed it", says(flat4, "url_key = <base_url_key>"))
    check("K-RN3-P4: p4 leaves url_key empty only for a stand with no UI", says(flat4, "no UI tests and no UI profile"))
    check("K-RN3-P5: p4's login.record paragraph carries the duration", says(flat4, "seconds"))
    check("K-RN3-P6: p1 hands the role the fact it judges from", says(flat1, "`frontend_same_origin`"))
    finish("test_env_access_onboarding")


def accounts_tests(p1: str, p2: str, p4: str) -> None:
    """HF8-9: the accounts of a stand - the check of the names a role's note holds (K-9.7) and the phases that carry the rule (K-9.8)."""
    from config_contract import environments_account_errors, reserved_role
    held = ["AUTH_USERNAME", "AUTH_PASSWORD", "QA_SECOND_USER_EMAIL", "QA_SECOND_USER_PASSWORD"]

    def one(roles: dict) -> list:
        return environments_account_errors([{"name": "s", "credentials_by_role": roles}], held)

    check_eq("K-9.7 a role whose names the file holds: no error", one({"admin": "AUTH_USERNAME / AUTH_PASSWORD",
                                                                      "second": "QA_SECOND_USER_EMAIL / QA_SECOND_USER_PASSWORD"}), [])
    check_eq("K-9.7 the notes of the 12586 stand (prose after the names) read as before", one(
        {"default user": "AUTH_USERNAME / AUTH_PASSWORD in testproject1_test_harness/.env"}), [])
    gone = one({"second": "QA_GONE_EMAIL / AUTH_PASSWORD"})
    check_eq("K-9.7 a name the file does not hold is ONE error, naming it", (len(gone), "QA_GONE_EMAIL" in gone[0] and "AUTH_PASSWORD" not in gone[0]), (1, True))
    check_in("K-9.7 ... and both doors: add to the file, or remove the role", "add the name(s) to the file", gone[0])
    check_in("K-9.7 ... and the other door", "or remove the role", gone[0])
    check_eq("K-9.7 `NOT provisioned` names no key: a legal record of a gap, no error", one({"third": "NOT provisioned locally"}), [])
    check_eq("K-9.7 an empty note names none: no error", one({"third": ""}), [])
    for label, environments in (("no environments", None), ("an empty list", []), ("an entry that is not an object", ["x"]),
                                ("an entry with no credentials_by_role", [{"name": "s"}]),
                                ("a credentials_by_role that is not an object", [{"name": "s", "credentials_by_role": "text"}])):
        check_eq(f"K-9.7 {label}: no error, no crash", environments_account_errors(environments, held), [])
    for label, roles, needle in (("an empty role", {"  ": "A_B / C_D"}, "role is empty"), ("the reserved role default", {"default": "A_B / C_D"}, "read before any role"),
                                 ("a role env:x", {"env:x": "A_B / C_D"}, "read before any role"),
                                 ("a role created:x", {"created:x": "A_B / C_D"}, "read before any role"),
                                 ("a note that is not text", {"x": ["A_B"]}, "must be text")):
        found = one(roles)
        check(f"K-9.7 {label} is refused, naming the form", len(found) == 1 and needle in found[0], found)
    check_eq("K-9.7 the reserved forms, by name", [reserved_role(r) for r in ("default", " default ", "env:A/B", "created:x", "Default", "default user")],
             [True, True, True, True, False, False])
    # the error index counts the ENTRY: the second stand is environments[1]
    second = environments_account_errors([{"name": "a"}, {"name": "b", "credentials_by_role": {"r": "A_GONE / AUTH_PASSWORD"}}], held)
    check_in("K-9.7 the error names the entry that holds the role", "environments[1].credentials_by_role", second[0])
    # the command: `--check-environment` carries it into its exit code
    root = temp_dir("qa-check-accounts-")
    try:
        (root / "qa-factory").mkdir()
        (root / "harness").mkdir()
        (root / "harness" / ".env").write_text("AUTH_USERNAME=sentinel-a\nAUTH_PASSWORD=sentinel-b\n", encoding="utf-8")
        config = {"environment": {"env_file": "harness/.env", "user_key": "AUTH_USERNAME", "secret_keys": ["AUTH_PASSWORD"]},
                  "environments": [{"name": "s", "credentials_by_role": {"second": "QA_GONE_EMAIL / QA_GONE_PASSWORD"}}]}
        path = root / "qa-factory" / "config.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        result = run_script("config_contract.py", "--root", root, "--check-environment")
        out = json.loads(result.stdout)
        check_eq("K-9.7 --check-environment on a role whose key is absent: a non-zero exit", (result.returncode, out["ok"]), (1, False))
        check_in("K-9.7 ... naming the missing name", "QA_GONE_EMAIL", " ".join(out["errors"]))
        check_not_in("K-9.7 ... and printing no value", "sentinel-", result.stdout + result.stderr)
        config["environments"][0]["credentials_by_role"] = {"second": "AUTH_USERNAME / AUTH_PASSWORD"}
        path.write_text(json.dumps(config), encoding="utf-8")
        result = run_script("config_contract.py", "--root", root, "--check-environment")
        check_eq("K-9.7 the same config with names the file holds: exit 0", (result.returncode, json.loads(result.stdout)["ok"]), (0, True))
        config["environments"][0]["credentials_by_role"] = {"second": "NOT provisioned"}
        path.write_text(json.dumps(config), encoding="utf-8")
        check_eq("K-9.7 a role with no names (NOT provisioned): exit 0", run_script("config_contract.py", "--root", root, "--check-environment").returncode, 0)
    finally:
        cleanup(root)
    # the person's question (K-9.7): the refusals a person may read through the conductor obey the question form
    import human_text
    asked = ("# Question\n\nThe env file holds two sets of login and password names: QA_SECOND_USER_EMAIL / QA_SECOND_USER_PASSWORD and "
             "AUTH_USERNAME / AUTH_PASSWORD. Which role is each account on the stand - an administrator, a plain user, or not an account "
             "of the stand at all?\n\n## How to answer\n\nWrite one role for each pair, in your own words.\n")
    check_eq("K-9.7 the question about the accounts breaks no rule of human-questions.md", human_text.problems(asked), [])
    # K-9.8: the keys of the phase texts, quoted from the DoD before the run; the control CAN fail
    def says(text: str, needle: str) -> bool:
        return needle in text
    check("K-9.8 control: the helper finds a string that is in p2", says(p2, "access.kind"))
    check("K-9.8 negative control: and a string that is not in p4 is not found", not says(p4, "no such sentence 91cc"))
    for name, text, needle in (("p2", p2, "account_pairs"), ("p2", p2, "which role"), ("p4", p4, "credentials_by_role"),
                               ("p1", p1, "account_pairs"), ("p1", p1, "not a sign-in to the stand")):
        check(f"K-9.8 {name} carries {needle!r}", says(text, needle))
    # F10 (fix round 2): the re-onboarding paragraph that calls the access question "the whole of topic 2" names the pairs question too
    flat = " ".join(p2.split())
    check("F10 p2 re-onboarding: the access question is the whole of topic 2 together with the pairs question",
          says(flat, "*whole* of topic 2 together with the pairs question above (for `account_pairs` not yet recorded as roles)"))
    check("F10 negative control: the old wording alone is gone", not says(flat, "this question is the *whole* of topic 2 — stands,"))
    # OH3-40: S4's door for an account already recorded with another pair names `--replace` (the CART-1 case); the first-move question
    # of the node ("does `account_pairs` read a `.env.local`?") is answered by a fixture, not by a line of the remainder
    s4 = (PHASES.parents[1] / "qa-story" / "phases" / "s4.md").read_text(encoding="utf-8")
    flat_s4 = " ".join(s4.split())
    check("OH3-40 s4 names `--replace` beside `stand-account` for a role recorded with another pair",
          says(flat_s4, "stand-account --role \"<role>\" --user-key <U> --secret-key <S> --words-file <file>` (a role the stand already records "
                        "with another pair is refused until the person's words say to change it: then add `--replace`)"))
    check("OH3-40 s4 negative control: the old sentence without the flag is not there", not says(flat_s4, "--words-file <file>`; for the address,"))
    root = temp_dir("qa-oh3-40-pairs-")
    try:
        (root / ".env.local").write_text("USER_EMAIL=sentinel-a\nUSER_PASSWORD=sentinel-b\n", encoding="utf-8")
        found = access_discovery(root)
        check_eq("OH3-40 `account_pairs` reads a `.env.local` (no remainder line needed)",
                 [(p["user_key"], p["secret_key"]) for p in found["account_pairs"]], [("USER_EMAIL", "USER_PASSWORD")])
        check_not_in("OH3-40 ... and no value in what discovery returns", "sentinel-", json.dumps(found))
    finally:
        cleanup(root)
    # F6: one name for both keys is not a pair (the hand-written notes surface)
    twice = environments_account_errors([{"name": "s", "credentials_by_role": {"x": "QA_USER / QA_USER"}}], ["QA_USER"])
    check_eq("F6 a note that names one variable twice is ONE error naming it", (len(twice), "QA_USER twice" in twice[0] if twice else False), (1, True))


if __name__ == "__main__": main()
