"""registry: a part of test_story_sides.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_common."""
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
import contract  # noqa: E402
from story_sides_common import ABSENT, REAL, SUBSTITUTED, side, stderr_of  # noqa: E402


def registry_cases():
    """t-2181 PC-1b: the registry leg of the reader (through `project_knowledge.subjects` + `state`), its order, its unknowns and
    the `registry_key` each registry side carries."""
    import project_knowledge as PK

    def put(root, key, element, value, environment="", scope=None):
        row, problem, _ = PK.record(root, key=key, environment=environment, element=element, state="known",
                                    scope=scope or ("project" if key == PK.SIDES_KEY else "stand"), value=value, words="the person said",
                                    source="person", story="S-1", by="conductor")
        check(f"fixture row {key} {element}", row is not None, problem)

    def read(root, record=None, env=None):
        return stderr_of(lambda: contract.story_sides(record if record is not None else {}, {}, env, root=root))

    with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
        root = Path(td)
        check_eq("no registry file: the default, as before", (read(root)[0]["product"]["source"], read(root)[1]), ("default", ""))
        put(root, PK.SIDES_KEY, "ui", {"deliverable": False, "settles_by": "platform team"})
        sides, _ = read(root)
        check_eq("a project row: source registry, registry_key product.sides, deliverable and settles_by read",
                 {k: sides["ui"][k] for k in ("source", "registry_key", "deliverable", "settles_by", "reality")},
                 {"source": "registry", "registry_key": PK.SIDES_KEY, "deliverable": False, "settles_by": "platform team", "reality": REAL})
        check("a product.sides row of a real side that is another team's (deliverable false) does not name this team's part: `product` is implied",
              "product" in sides, sorted(sides))
        put(root, PK.STAND_SIDES_KEY, "backend", {"reality": SUBSTITUTED}, environment="dev")
        sides, _ = read(root, env="dev")
        check_eq("a stand row of the chosen stand: reality read, registry_key environments.sides; deliverable unknown reads true",
                 {k: sides["backend"][k] for k in ("reality", "registry_key", "deliverable", "source")},
                 {"reality": SUBSTITUTED, "registry_key": PK.STAND_SIDES_KEY, "deliverable": True, "source": "registry"})
        check_eq("another stand's row is not read for this stand", "backend" in read(root, env="prod")[0], False)
        check_eq("no stand chosen: no stand row is read", "backend" in read(root)[0], False)
        put(root, PK.REFERENCE_KEY, "ui", {"reference": True}, environment="old")
        check_eq("a reference found on another stand's row (all stands are read), the key stays the one that set the side",
                 (read(root, env="dev")[0]["ui"]["reference"], read(root, env="dev")[0]["ui"]["registry_key"]), ("old", PK.SIDES_KEY))
        check_eq("pipeline.sides wins over the registry, and carries no registry_key",
                 ("registry_key" in read(root, {"sides": {"ui": side(ABSENT)}}, "dev")[0]["ui"],
                  read(root, {"sides": {"ui": side(ABSENT)}}, "dev")[0]["ui"]["reality"]), (False, ABSENT))
        check_eq("the default product carries no registry_key", "registry_key" in contract.story_sides({})["product"], False)
    with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
        root = Path(td)
        put(root, PK.REFERENCE_KEY, "ui", {"reference": True}, environment="old")
        sides, _ = read(root)
        check_eq("a reference row alone: registry_key environments.reference_for, reality real, deliverable reads true: no implicit product",
                 ({k: sides["ui"][k] for k in ("registry_key", "reference", "reality")}, "product" in sides),
                 ({"registry_key": PK.REFERENCE_KEY, "reference": "old", "reality": REAL}, False))
    with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
        root = Path(td)
        put(root, PK.SIDES_KEY, "UI", {"deliverable": True})
        put(root, PK.SIDES_KEY, "ui", {"deliverable": False})
        sides, _ = read(root)
        check_eq("`UI` and `ui` are two sides", sorted(sides), ["UI", "ui"])
        check_eq("registry_sides names every recorded side", contract.registry_sides(root)["names"], ["UI", "ui"])
    for label, body in (("a malformed value", {"deliverable": "maybe"}), ("a word outside the data file", None)):
        with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
            root = Path(td)
            put(root, PK.SIDES_KEY, "ui", {"deliverable": True})
            path = PK.record_path(root)
            data = json.loads(path.read_text(encoding="utf-8"))
            data["facts"].append({"id": "PK-9", "key": PK.STAND_SIDES_KEY, "environment": "dev", "element": "backend", "state": "known",
                                  "scope": "stand", "value": {"reality": "mocked"} if body is None else body, "provenance": {}, "at": "2026-12-01T10:00:00+00:00"})
            path.write_text(json.dumps(data), encoding="utf-8")
            got = contract.registry_sides(root, "dev")
            check_eq(f"{label} on a side row: the side reads unknown (never real, never 'no row') and the problem is said",
                     (got["sides"]["backend"]["reality"], bool(got["problem"]), got["unreadable"]), ("", True, False))
    with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
        root = Path(td)
        put(root, PK.SIDES_KEY, "ui", {"deliverable": True})
        path = PK.record_path(root)
        data = json.loads(path.read_text(encoding="utf-8"))
        for number, bad in enumerate(("web.app", "a=b")):       # a hand-edited row the writer would refuse (F3)
            data["facts"].append({"id": f"PK-{number + 8}", "key": PK.SIDES_KEY, "environment": "", "element": bad, "state": "known",
                                  "scope": "project", "value": {"deliverable": True}, "provenance": {}, "at": "2026-12-01T10:00:00+00:00"})
        path.write_text(json.dumps(data), encoding="utf-8")
        got = contract.registry_sides(root)
        check_eq("F3: a side name holding a dot or an equals sign reads malformed (unknown, problem said), never real",
                 (got["sides"]["web.app"]["reality"], got["sides"]["a=b"]["reality"], bool(got["problem"]), got["unreadable"],
                  got["sides"]["ui"]["reality"]), ("", "", True, False, REAL))
    for label, content in (("the file unreadable", "{not json"), ("a foreign schema_version", json.dumps({"schema_version": 99, "facts": []}))):
        with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
            root = Path(td)
            PK.record_path(root).parent.mkdir(parents=True)
            PK.record_path(root).write_text(content, encoding="utf-8")
            sides, err = read(root)
            check_eq(f"{label}: the default side reads unknown, never real, one line on stderr",
                     (sides["product"]["reality"], "unknown" in err, err.count("\n")), ("", True, 1))
            check_eq(f"{label}: registry_sides says unreadable", contract.registry_sides(root)["unreadable"], True)
    with tempfile.TemporaryDirectory(prefix="qa-sides-reg-") as td:
        root = Path(td)
        put(root, PK.STAND_SIDES_KEY, "backend", {"reality": SUBSTITUTED}, environment="Dev")
        check_eq("stand names are exact: `Dev` is not `dev`", "backend" in read(root, env="dev")[0], False)
        put(root, PK.REFERENCE_KEY, "ui", {"reference": True}, environment="a")
        put(root, PK.REFERENCE_KEY, "ui", {"reference": True}, environment="b")
        check_eq("two reference stands for one side read unknown, not a pick",
                 (contract.registry_sides(root)["sides"]["ui"]["reality"], bool(contract.registry_sides(root)["problem"])), ("", True))


def main() -> None:
    registry_cases()
    harness.finish("test_story_sides_registry")


# split: runner piece 1
if __name__ == "__main__":
    main()
