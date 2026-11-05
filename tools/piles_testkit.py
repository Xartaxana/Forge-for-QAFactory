"""Shared helpers of the tests of tools/piles.py (test_piles*.py): fixture builders, git and file helpers.

Not a test module. The pytest fixtures built on it (`session_tree`, `tree`, `cli`) live in tools/conftest.py. One session
fixture builds a small git repo (a mini BACKLOG, two piles, one batch); every test works on a COPY of it under tmp_path
(--repo), with the GIT_* variables scrubbed (a hook run must not point the tests at the real index).
"""
import hashlib
import os
import pathlib
import shutil
import subprocess

GIT_VARS = ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_PREFIX", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY")


def clean_env():
    return {k: v for k, v in os.environ.items() if k not in GIT_VARS}


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                        *args], capture_output=True, env=clean_env())
    assert p.returncode == 0, (args, p.stderr.decode("utf-8", "replace"))
    return p.stdout.decode("utf-8", "replace")


def put(root, rel, text):
    p = pathlib.Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))
    return p


# ---------------------------------------------------------------- fixture builders

BACKLOG = """# Бэклог фабрики

## Как вести

Текст.

## 1. Сравнительный прогон

| id | что | детали |
|---|---|---|
| B-015 | Прогон сравнения. | детали прогона |

## 7. Релизы, приёмки, инфраструктура разработки

| id | что сделать | почему | источник | принципы |
|---|---|---|---|---|
| B-102 | **Дыра в `a|b` разборе.** ждёт слова владельца. | свидетель `x|y` | источник 1 | P1 |
| B-135 | **Сессия.** `tools/session_context.py` | почему 135 | closed by code: X; remainder: B-171 | P2 |
| B-219 | **Развилка F10.** `scripts/traceability.py` | почему 219 | источник 219 | P3 |
| B-230 | **Кучки.** | почему 230 | владелец | P4 |

## 12. Миграция исправлений

| id | что сделать | почему | источник | принципы |
|---|---|---|---|---|
| B-308 | **Два тега** [F13, F15] (= B-303) | почему 308 | источник 308 | P5 |

## Закрыто

| id | что сделать | почему | источник | принципы |
|---|---|---|---|---|
| B-001 | **Старое.** | почему | закрыто кодом: model-rates.json:83 | P1 |
| B-314 | **Кодом.** | почему | закрыто кодом: `0275882` | P1 |
| B-399 | **Чтением.** | Закрыто 06.10.2026 чтением (`06b835b`) | источник | P1 |
| B-417 | **Храповик.** | почему | влито `7848917` + база `7ed70ac` | P1 |
| B-420 | **Красный main.** | пайплайны после: 7883565 и 7876821 | источник | P1 |
| B-462 | **Мера.** | почему | закрыто кодом: bac83cb | P1 |
"""

FEATURES = '{"schema_version": 1, "features": []}\n'

LEFTOVER_OK = "- x | сделано: t-1"           # the default «Остатки» line of batch_text: finished, so `close` may pass
PROOF_WAITING = "ждёт фазы 1"                 # the default «Статус» cell of batch_text's proof row: waiting, so `close` refuses (F5-5)
PROOF_DONE = "сделано: t-1"                   # a finished proof row; accept_batch1 and batch2 put it there


def card_text(slug, name, rows=(), feats="F19"):
    out = ["# %s (`%s`)" % (name, slug), "", "приоритет: П1 | фичи: %s | стенд: не нужен | зона: `tools/`" % feats, "",
           "## Зачем", "", "Текст.", "", "## Пачки", "",
           "| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |",
           "|---|---|---|---|---|---|---|---|"]
    out += ["| %s |" % " | ".join(r) for r in rows]
    out += ["", "## Входящие", "", "x"]
    return "\n".join(out) + "\n"


def batch_text(slug, n, status="в работе", nodes=(), pre="", who="Ира", branch="`main` (x)", leftovers=LEFTOVER_OK,
               proof=PROOF_WAITING, brief=True):
    out = ["# %s — пачка %d: что-то" % (slug, n), "",
           "кучка: `%s` | статус: %s | взял: %s | ветка: %s | MR: — | стенд: не нужен" % (slug, status, who, branch), "",
           "Правило готовности.", pre, *(["## Бриф", "", "Бриф.", ""] if brief and "## Бриф" not in pre else []), "## Узлы", "",
           "| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |", "|---|---|---|---|---|---|---|"]
    out += ["| %s |" % " | ".join(nd) for nd in nodes]
    out += ["", "## Ход", "", "- x", "", "## Живые доказательства", "", "| Что | Стенд | Кто | Статус |", "|---|---|---|---|",
            "| a | b | c | %s |" % proof, "", "## Остатки", ""]
    out += [leftovers] if leftovers else []
    return "\n".join(out) + "\n"


def node(i, writes="`tools/a.py`", status="в работе", executor="builder", prio="П1"):
    return [i, prio, "что", executor, writes, "—", status]


def finding_text(ident="B-102", pile="forge", title="Находка"):
    return "# %s\n\nid: %s | кучка: `%s` | от: x | приоритет: — | кандидат наверх: нет\n\nЧто не так: …\n" % (title, ident, pile)


ROW1 = ["1", "фундамент", "B-230", "L", "в работе", "Ира", "`main` (x)", "—"]
ROW2 = ["2", "потом", "B-015", "M", "ожидает", "—", "—", "—"]

B1 = "plans/piles/forge/batch-1-foundation.md"
B2 = "plans/piles/forge/batch-2-next.md"
CARD = "plans/piles/forge/README.md"
ROW1_LINE = "| 1 | фундамент | B-230 | L | в работе | Ира | `main` (x) | — |"


def build_mini(root):
    put(root, "plans/BACKLOG.md", BACKLOG)
    put(root, "plans/features.json", FEATURES)
    put(root, "plans/piles/forge/README.md", card_text("forge", "Forge", [ROW1, ROW2]))
    put(root, "plans/piles/forge/batch-1-foundation.md",
        batch_text("forge", 1, nodes=[node("F0-1", "`tools/a.py`"), node("F0-2", "`plans/PILES.md`", "ожидает")]))
    put(root, "plans/piles/report-delivery/README.md", card_text("report-delivery", "Report", [], "F08"))
    put(root, "plans/piles/_template/README.md", "# <Название> (`<slug>`)\n")
    empty = pathlib.Path(root).parent / "empty-template"          # no sample hooks: the fixture is copied once per test
    empty.mkdir()
    git(root, "init", "-q", "--template=" + str(empty))
    git(root, "config", "core.autocrlf", "false")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "mini tree")
    # no origin/main here: (в) says NOT CHECKED for the item tests; the (в) tests call fetch_origin()
    git(root, "gc", "-q", "--prune=now")                        # a pack instead of loose objects: far fewer files to copy
    shutil.rmtree(pathlib.Path(root) / ".git" / "logs", ignore_errors=True)


def needs_git(fn):
    """The test stages or commits: its tree keeps the fixture's .git (copying it is the slow part of a test)."""
    fn._needs_git = True
    return fn


def stage(root, *rels):
    git(root, "add", "-A", "--", *rels)


def commit(root, msg="c"):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg)


def freeze(root, extra_findings=True, commit_it=True):
    """Freeze the mini backlog: a lock line above the first '## ', every open id placed, committed."""
    p = root / "plans/BACKLOG.md"
    text = p.read_bytes().decode("utf-8").replace("## Как вести", "piles-freeze: 2026-10-08 open=6 closed=6\n\n## Как вести", 1)
    p.write_bytes(text.encode("utf-8"))
    if extra_findings:
        for ident in ("B-102", "B-135", "B-219", "B-308"):
            put(root, "plans/piles/forge/findings/%s-x.md" % ident, finding_text(ident))
    if commit_it:
        commit(root, "freeze")


def edit(root, rel, old, new):
    p = root / rel
    t = p.read_bytes().decode("utf-8")
    assert old in t, (rel, old)
    p.write_bytes(t.replace(old, new, 1).encode("utf-8"))


def fetch_origin(root):
    """origin/main := HEAD, the way `git fetch` would leave it (the fixture has no remote)."""
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")


def rd(root, rel):
    return (root / rel).read_bytes().decode("utf-8")


def tree_state(tree):
    """sha256 of every file under plans/: a refusal must leave it unchanged."""
    return {str(p.relative_to(tree)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((tree / "plans").rglob("*")) if p.is_file()}


def lines_with(out, tag):
    return [l for l in out.splitlines() if l.startswith(tag)]


def board_text(tree, cli):
    cli(tree, "board")
    return (tree / "plans/PILES.md").read_bytes().decode("utf-8")


def dup_finding(tree):
    put(tree, "plans/piles/forge/findings/B-135-a.md", finding_text("B-135"))
    put(tree, "plans/piles/report-delivery/findings/B-135-b.md", finding_text("B-135", "report-delivery"))


def msg(tree, text):
    """A commit-message file for `check --msg-file`; -> its path."""
    p = tree / "msg.txt"
    p.write_bytes(text.encode("utf-8"))
    return str(p)


def batch2(tree, status="ожидает", writes="`tools/b.py`", pre=""):
    put(tree, B2, batch_text("forge", 2, status, [node("F0-3", writes, "ожидает")], pre=pre, who="—", branch="—",
                                                                                proof=PROOF_DONE))


def accept_batch1(tree):
    """Batch 1 accepted AND closable: its proof row (still waiting in batch_text) is finished, as `close` demands."""
    if PROOF_WAITING in rd(tree, B1):
        edit(tree, B1, PROOF_WAITING, PROOF_DONE)
    edit(tree, B1, "статус: в работе", "статус: принято")
    edit(tree, CARD, "| L | в работе | Ира", "| L | принято | Ира")


def head_hash(tree, short=False):
    return git(tree, "rev-parse", "--short=7" if short else "--verify", "HEAD").strip()


def closed_rows(tree):
    below = rd(tree, "plans/BACKLOG.md").split("\n## Закрыто\n", 1)[1]
    return {l.split(" | ")[0][2:]: l for l in below.split("\n") if l.startswith("| B-")}


def _no_network(monkeypatch):
    """Make any urllib network call fail the test (take and close touch files only)."""
    import urllib.request

    def refuse(*a, **k):
        raise AssertionError("a network call was made")
    monkeypatch.setattr(urllib.request, "urlopen", refuse)
