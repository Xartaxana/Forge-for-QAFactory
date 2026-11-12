#!/usr/bin/env python3
"""repo_words.py - the ONE executor of the words of gate A's test-repository question that act on the person's repository.

FG7-8 part B (B-13, AR-19: both roads call it). A word whose row in `question-vocabulary.json` (`finding_door_words`) names the
executor `git_commit` or `git_stash` is carried out HERE and nowhere else: the driver (`Driver._record_door_lines`) calls `run`, the
conductor of the skill road calls the CLI.

    repo_words.py --task <T> --word <word> --words-file <file> [--by <who>]
    repo_words.py --reminder --task <T>

`run` takes exactly what the person was SHOWN (the shown block = the stored block = a fresh digest of their changes), refuses
before any write on every difference or blocker, writes a tree of the index, runs ONE git command with the person's hooks (no
`--no-verify`, no `-c`) and LITERAL pathspecs (a person's `q[a]-factory/z.txt` is never a glob that also names the factory's folder),
judges the result on the repository's STATE (never on the exit code alone), and returns facts: the caller records the person's word
with them (`record_args`) and tells the person (`done_line`). A failure restores the index from the tree written before the add
(`read-tree`), never `reset -- <paths>`. Every git form is one the measurement ran
(`docs/tasks/specs/reports/t-118-b0-2-git-measure.md`). The factory never deletes an `index.lock`.

`main` exits 0 when done (the line printed), 2 when the request is not the exact word of a question that was shown, 3 when
nothing could be done or the write landed wrong (the problem and the command to ask again are printed).
"""
import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO_WORD_TIMEOUT = 120      # seconds one git command may take; a hook that waits for a person is the person's, and no retry follows
EXECUTORS = ("git_commit", "git_stash")
STASH_SENTENCE = "this word also passes a tree made dirty again at this HEAD"      # F-16: the record says what the pass covers


def message(task, word) -> str:
    """THE one builder of the commit / stash message (AR-13): the writer is `run`, the reader is `reminder_line`. `word` is the git verb
    of the executor (`commit` / `stash`); the message names the story and says whose changes these are."""
    return f"qa-factory {task}: your changes from before the tests ({word})"


def _short(sha) -> str:
    return str(sha or "")[:12]


def _no(problem: str, door: str = "") -> tuple:
    """`({}, problem)`: nothing was done in the repository and nothing is passed; the problem is one paragraph with its door."""
    return {}, " ".join(f"{problem} {door}".split())


def _own_door(rows, finding_id) -> str:
    """What the person can do themselves: do it, then answer with the item's own word that only records (`go on`), named from the data.
    `finding_id` is the id of the question as the person was shown it (given by the caller, never a constant of this file)."""
    word = next((r["word"] for r in rows if r["executor"] == "record"), "")
    return (f"To go on without this: commit or stash it yourself, then answer `{finding_id}: {word}`." if word
            else "To go on without this: commit or stash it yourself, then ask for the gate again.")


def _env() -> dict:
    """The environment of the executor's git calls: the package's one (`gate_preflight.git_env`) with LITERAL pathspecs (BL-1)."""
    import gate_preflight
    return gate_preflight.git_env(literal=True)


def _kill_tree(child) -> None:
    """Kill the git child AND everything it started (a hook): Windows `taskkill /F /T`, POSIX the child's own process group.
    A pipe would be kept open by an orphaned hook; the output goes to files (the caller)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(child.pid)], capture_output=True, timeout=30)
        else:
            os.killpg(os.getpgid(child.pid), signal.SIGKILL)
    except Exception:
        pass
    try:
        child.kill()
    except Exception:
        pass


def _exec(top, argv: list, timeout) -> tuple:
    """`(exit code, stdout, stderr, timed_out)` of ONE git command run in `top` with the person's own configuration and hooks. Started with
    `Popen` so that the whole process tree can be killed on a timeout; output to temp files, never pipes. After a kill the code is -9."""
    options = {"cwd": str(top), "env": _env(), "stdin": subprocess.DEVNULL}
    if os.name != "nt":
        options["start_new_session"] = True
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            child = subprocess.Popen(argv, stdout=out, stderr=err, **options)
        except OSError as exc:
            return -1, "", f"git could not be started ({exc})", False
        timed_out = False
        try:
            code = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_tree(child)
            try:
                code = child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                code = -9
        out.seek(0)
        err.seek(0)
        return code, out.read().decode("utf-8", "replace"), err.read().decode("utf-8", "replace"), timed_out


def _tail(text: str, size: int = 600) -> str:
    text = " ".join(str(text or "").split())
    return text[-size:] if len(text) > size else text


def _names(raw) -> set:
    """The paths of `git diff --name-status -z` output: a status token, then one path (a rename or a copy: OLD, then NEW - both count)."""
    tokens = [t for t in str(raw or "").split("\0")]
    found, at = set(), 0
    while at < len(tokens):
        status = tokens[at]
        at += 1
        if not status:
            continue
        for _ in range(2 if status[0] in "RC" else 1):
            if at < len(tokens) and tokens[at]:
                found.add(tokens[at])
            at += 1
    return found


def _stash_sha(top) -> str:
    import gate_preflight as GP
    return GP._git(top, "rev-parse", "-q", "--verify", "refs/stash") or ""


def _lock_exists(top) -> bool:
    import gate_preflight as GP
    where = GP._git(top, "rev-parse", "--git-path", "index.lock")
    return bool(where) and (Path(top) / where).exists()


def _commit_undo(head_before: str, tree: str, spans: bool = False) -> str:
    """The person's own two commands that undo the commit: plain for the record, each in its own backtick span for text a person reads."""
    first, second = f"git reset --soft {_short(head_before)}", f"git read-tree {_short(tree)}"
    return f"`{first}`, then `{second}`" if spans else f"{first}, then {second}"


def _stash_undo(sha: str, spans: bool = False) -> str:
    apply_, listing, drop = f"git stash apply --index {_short(sha)}", "git stash list", "git stash drop stash@{N}"
    if spans:
        return (f"`{apply_}`; then remove the entry: `{listing}` shows it as `stash@{{N}}` with the message above, and `{drop}` drops it")
    return (f"{apply_}; then remove the entry: {listing} shows it as stash@{{N}} with the message above, and {drop} drops it")


def _plan(task_root, project_root, config, option, door, finding_id) -> tuple:
    """`(plan, None)` for a word that may be carried out, or `(None, (done, problem))`: the refusal. Steps 1-4 of `run`; nothing is written."""
    import external_writes
    import gate_brief
    import gate_preflight as GP
    import stage_guard
    rows = gate_brief.finding_door_words()
    row = next((r for r in rows if r["option"] == option), None)
    if row is None or row["executor"] not in EXECUTORS:
        return None, _no(f"`{option}` is not a word that writes into your repository, so nothing was done in it.")
    own, verb = _own_door(rows, finding_id), row["executor"].removeprefix("git_")
    is_commit = row["executor"] == EXECUTORS[0]
    closed = external_writes.closed_by_run(task_root, unreadable_closes=True)
    if closed:
        return None, _no(f"Nothing was done in your repository: {closed}.", own)
    state = GP.vcs_changes(project_root, config, task_root)
    if state is None or not state["top"]:
        return None, _no("Your test repository could not be read by git, so nothing was done in it.", own)
    if not state["person"]:
        return None, _no("Nothing of yours is uncommitted now, so nothing was done.")
    if GP.vcs_state_block(state["head"], state["digest"]) != str((door or {}).get("block") or ""):
        return None, _no("Your repository changed since you were shown the list of your changes, so nothing was done. Show the question "
                         "again to see the list as it stands now.", own)
    blockers = GP.vcs_blockers(state)[verb]
    if blockers:
        return None, _no(f"The word cannot be carried out on this repository: {blockers[0]}.", own)
    person = state["person"]
    paths = list(dict.fromkeys(p for e in person for p in (e["path"], e["orig"]) if p))
    msg = message(Path(task_root).name, verb)
    adds = [e["path"] for e in person if e["xy"][1] != " "]
    commit_argv = ["git", "commit", "-m", msg, "--", *paths]
    stash_argv = ["git", "stash", "push", "--include-untracked", "-m", msg, "--", *paths]
    guard = stage_guard.rule_pathspec(shlex.join(commit_argv)) if is_commit else stage_guard.rule_stash(shlex.join(stash_argv))
    if guard:
        return None, _no(f"The safety guard of the factory refuses this command: {guard}", own)
    steps = ([["git", "add", "--", *adds]] if adds else []) + [commit_argv] if is_commit else [stash_argv]
    return {"project_root": project_root, "config": config, "task_root": task_root, "option": option, "stage": str((door or {}).get("stage") or ""),
            "own": own, "is_commit": is_commit, "state": state, "top": state["top"], "person": person, "paths": paths, "msg": msg,
            "steps": steps}, None


def _write(plan, timeout) -> tuple:
    """`(ran, None)`: the facts of the one write (steps 5-6): `{code, out, err, timed_out, timeout, tree, head_before, stash_before, head_after,
    after, still, unread}`; or `(None, (done, problem))` when the tree of the index could not be written first (a commit's undo needs it)."""
    import gate_preflight as GP
    top, state = plan["top"], plan["state"]
    ran = {"timeout": timeout, "head_before": state["head"], "stash_before": _stash_sha(top), "tree": ""}
    if plan["is_commit"]:
        ran["tree"] = GP._git(top, "write-tree") or ""
        if not ran["tree"]:
            return None, _no("Git could not write down your staged changes before the commit (an undo needs it), so nothing was done.", plan["own"])
    code, out, err, timed_out = 0, "", "", False
    for argv in plan["steps"]:
        code, out, err, timed_out = _exec(top, argv, timeout)
        if code or timed_out:
            break
    after = GP.vcs_changes(plan["project_root"], plan["config"], plan["task_root"])
    ran.update(code=code, out=out, err=err, timed_out=timed_out, head_after=GP._git(top, "rev-parse", "HEAD") or "", after=after,
               still=[e["path"] for e in (after or {}).get("person", [])], unread=after is None)
    return ran, None


def _judge_commit(plan, ran) -> tuple:
    """`(facts, problem)` of a commit, judged on the repository: `facts` empty with no problem = nothing landed; `facts["kept"]` = a commit
    landed that is not exactly the shown set (the caller records a remark); otherwise the facts of a commit that holds exactly the paths."""
    import gate_preflight as GP
    top, head_before, head_after = plan["top"], ran["head_before"], ran["head_after"]
    landed = bool(head_after) and head_after != head_before
    exact = (landed and GP._git(top, "rev-parse", "HEAD^") == head_before
             and _names(GP._git_raw(top, "diff", "--name-status", "-z", head_before, "HEAD")) == set(plan["paths"]))
    undo = _commit_undo(head_before, ran["tree"])
    spans = _commit_undo(head_before, ran["tree"], spans=True)
    if landed and not exact:
        return ({"kept": f"a commit {_short(head_after)} was made that does not hold exactly the changes shown", "stash_sha": "", "undo": undo},
                f"A commit {_short(head_after)} was made, but it does not hold exactly the changes you were shown, so nothing is passed. "
                f"To undo it: {spans}.")
    if not exact:
        return {}, ""
    return {"stash_sha": "", "undo": undo, "spans": spans,
            "text": f"committed {len(plan['person'])} change(s) as {_short(head_after)} on branch {plan['state']['branch']} (message: {plan['msg']})"}, ""


def _judge_stash(plan, ran) -> tuple:
    """`(facts, problem)` of a stash, same shape as `_judge_commit`: a stored entry that is not this word's is a problem with no facts
    (nothing was dropped); an entry left by a stash that did not end cleanly is `facts["kept"]` (a remark)."""
    import gate_preflight as GP
    top, msg, after, state = plan["top"], plan["msg"], ran["after"], plan["state"]
    stash_after = _stash_sha(top)
    saved = bool(stash_after) and stash_after != ran["stash_before"]
    carries = saved and msg in (GP._git(top, "log", "-1", "--format=%s", stash_after) or "")
    if saved and not carries:
        return {}, (f"A stash entry {_short(stash_after)} appeared but it is not the one this word makes, so nothing is passed and nothing "
                    "was dropped.")
    if not carries:
        return {}, ""
    undo, spans = _stash_undo(stash_after), _stash_undo(stash_after, spans=True)
    if not ran["unread"] and (ran["code"] == 0 or ran["timed_out"]) and after["digest"] != state["digest"]:
        return {"stash_sha": stash_after, "undo": undo, "spans": spans,
                "text": f"put {len(plan['person'])} change(s) aside in git stash {_short(stash_after)} ({msg})"}, ""
    changed = sorted({e["path"] for e in plan["person"]} - set(ran["still"]))
    tree = ("could not be read afterwards." if ran["unread"] else "unchanged." if after["digest"] == state["digest"]
            else f"changed in these paths: {', '.join(changed[:5]) or 'unknown'}.")
    return ({"kept": f"a stash entry {_short(stash_after)} was left by a git stash that did not end cleanly", "stash_sha": stash_after, "undo": undo},
            f"A stash entry was left: {_short(stash_after)}; it was not dropped and nothing is passed. Your tree {tree} "
            f"To take the entry back: `git stash apply --index {_short(stash_after)}`.")


def _said(plan, line, replaced) -> str:
    """The person's decision text, by THE one writer (`contract.person_decision`): the word, their line whole, the earlier lines it replaces."""
    import contract as C
    return C.person_decision(plan["option"], " ".join(str(line).split()), [" ".join(str(r).split()) for r in replaced or ()])


def _kept(plan, facts, problem, line, replaced) -> tuple:
    """A write that landed but is not what the word promises (F-5): the person's word, what landed and the undo are recorded as a REMARK by
    the same `record_args` road (`failed`), nothing is passed, and the problem reaches the conductor once."""
    done = {"failed": True, "stage": plan["stage"], "still": [], "unread": False, "stash_sha": facts["stash_sha"], "undo": facts["undo"],
            "decision": f"{_said(plan, line, replaced)}; the write did not end as the word promises: {facts['kept']}; to undo: {facts['undo']}"}
    return done, _no(problem, plan["own"])[1]


def _done(plan, ran, facts, line, replaced) -> tuple:
    """The `done` of a write that stands (step 8) and, when changes of the person are still dirty or the state could not be read, the problem."""
    import gate_preflight as GP
    head_after, still, unread = ran["head_after"], ran["still"], ran["unread"]
    done = {"word": plan["option"], "head_before": ran["head_before"], "head_after": head_after, "tree": ran["tree"], "stash_sha": facts["stash_sha"],
            "paths": len(plan["person"]), "block": GP.vcs_state_block(head_after), "stage": plan["stage"], "undo": facts["undo"], "still": still,
            "unread": unread, "branch": plan["state"]["branch"], "message": plan["msg"]}
    done["decision"] = (f"{_said(plan, line, replaced)}; done: {facts['text']}; to undo: {facts['undo']}"
                        + ("" if plan["is_commit"] else f"; {STASH_SENTENCE}"))
    problem = ""
    if still:
        problem = (f"The change IS made ({facts['text']}), but these of your changes are still uncommitted: {', '.join(still[:5])}. "
                   "Nothing is passed; the question will ask again about what is left.")
    elif unread:
        problem = (f"The change IS made ({facts['text']}), but your repository could not be read afterwards, so the result is not known. "
                   f"Nothing is passed; the question will ask again. To undo it: {facts['spans']}.")
    return done, problem


def run(task_root, project_root, config, option, line, replaced, door, finding_id, timeout=REPO_WORD_TIMEOUT) -> tuple:
    """`(done, problem)` for the word `option` (a row of `finding_door_words`) the person wrote as `line` (their earlier lines `replaced`), on the
    SHOWN door `door` = `{block, stage, option}` of the question `finding_id`. Nothing is recorded here. `done` is `{}` when nothing was done
    (the problem says why and names a door); otherwise `{word, head_before, head_after, tree, stash_sha, paths, block, stage, decision, undo,
    still, unread, branch, message}`; a `done` WITH a problem is a write that happened but left the person's changes dirty (`still`) or
    could not be read afterwards (`unread`); a `done` with `failed` is a write that landed wrong (a commit that is not the shown set, a stash
    entry left): the caller records a REMARK for each of these, no pass, and tells the conductor the problem.
    Order: the word and the run (1-2), the shown list against a fresh read (3), the blockers and the guard (4) - `_plan`; the tree before the
    add (5), the command (6) - `_write`; the judgment on the state (7) - `_judge_commit` / `_judge_stash`; the facts (8). Every step before 6
    writes nothing."""
    plan, refusal = _plan(task_root, project_root, config, option, door, finding_id)
    if refusal:
        return refusal
    ran, refusal = _write(plan, timeout)
    if refusal:
        return refusal
    facts, problem = (_judge_commit if plan["is_commit"] else _judge_stash)(plan, ran)
    if facts.get("kept"):
        return _kept(plan, facts, problem, line, replaced)
    if not facts:
        return _no(problem, plan["own"]) if problem else _failed(plan, ran)
    return _done(plan, ran, facts, line, replaced)


def _failed(plan, ran) -> tuple:
    """The result when the command did not do what the word promises: the index is put back from the tree written before the add
    (a commit only), the problem carries git's own text and the true state, and nothing is passed."""
    import gate_preflight as GP
    top, own, tree = plan["top"], plan["own"], ran["tree"]
    lock = _lock_exists(top)
    if ran["timed_out"]:
        text = (f"The git command did not finish in {ran['timeout']} s and was stopped; HEAD is {_short(ran['head_after'])} "
                f"(was {_short(ran['head_before'])}).")
    else:
        text = f"Git did not do it (exit {ran['code']}): {_tail(ran['err'] or ran['out'])}."
    if not plan["is_commit"]:
        return _no(text + " Nothing is passed and your changes were not moved." + (" A leftover `.git/index.lock` blocks git: if no git is "
                   "running, remove that file yourself, then look at `git status`." if lock else ""), own)
    if lock:
        return _no(text + f" A leftover `.git/index.lock` blocks git: if no git is running, remove that file yourself, then `git read-tree "
                   f"{_short(tree)}` restores what you had staged. Nothing is passed.", own)
    if GP._git(top, "read-tree", tree) is None:
        return _no(text + f" Restoring what you had staged failed; `git read-tree {_short(tree)}` restores it. Nothing is passed; the "
                   "question stays open.", own)
    return _no(text + " Your staged changes are as they were. Nothing is passed; the question stays open.", own)


def record_args(task, done) -> list:
    """THE one builder of the `waiver.py` arguments that record what `run` did (AR-13, both roads): the pass of the block the next rehearsal
    asks (`--stage --block --decision`), or - when the person's changes are STILL dirty after a hook (`done["still"]`), the state could not be
    read afterwards (`unread`) or the write landed wrong (`failed`) - a remark that keeps the words and passes nothing (`--remark --stage
    --text`), so the next rehearsal asks again about what is left."""
    if done.get("still") or done.get("unread") or done.get("failed"):
        return ["--remark", "--task", str(task), "--stage", done["stage"], "--text", done["decision"]]
    return ["--task", str(task), "--stage", done["stage"], "--block", done["block"], "--decision", done["decision"]]


def _prefix(verb: str) -> str:
    """The lead of the line that carries the command which undoes a SUCCESSFUL action (F-7): a row of `references/human-text.json`
    `action_lines.done_prefixes` (data, AR-1), so a done line does not read as a failure's `the fix:`. A row that cannot be read falls back
    to `the fix:`, the lead every action line has; a failure keeps its own wording."""
    try:
        import human_text
        found = ((human_text.rules().get("action_lines") or {}).get("done_prefixes") or {}).get(verb)
    except Exception:
        found = None
    return found if isinstance(found, str) and found.strip() else "the fix:"


def done_line(done) -> str:
    """The sentence the person is told right after the action (OW-1): what was done and its true undo, in the person's words."""
    msg, count = done["message"], done["paths"]
    # The command lives on a line that starts with an action prefix of `references/human-text.json` (`action_lines.prefixes`): that is the
    # one place `human_text.problems` lets a command's flags stand, in backticks (a flag anywhere else in text a person reads is a problem).
    if done.get("stash_sha"):
        return (f"Your {count} uncommitted change(s) are put aside in a git stash, \"{msg}\" ({_short(done['stash_sha'])}).\n"
                f"{_prefix('stash')} {_stash_undo(done['stash_sha'], spans=True)}.")
    return (f"Your {count} uncommitted change(s) are now commit {_short(done['head_after'])} on branch `{done['branch']}`, message "
            f"\"{msg}\".\n{_prefix('commit')} {_commit_undo(done['head_before'], done['tree'], spans=True)}.")


def reminder_line(project_root, config, task) -> str:
    """The end-of-run line (OW-1), read from git and never from prose: the stash entry the word made is still in the stash list (found by its
    message; its current `stash@{N}` is printed), or the commit it made is in the history of the branch (a subject EQUAL to the message: the
    grep is a substring test). "" when neither stands (popped already, or nothing was done) and when git cannot answer (one stderr line:
    a reminder never stops the end)."""
    import gate_preflight as GP
    try:
        tests_root = (Path(project_root) / str((config or {}).get("tests_root") or ".")).resolve()
        top = GP._git(tests_root, "rev-parse", "--show-toplevel") if tests_root.is_dir() else None
        if not top:
            return ""
        lines = []
        commit_msg, stash_msg = (message(task, executor.removeprefix("git_")) for executor in EXECUTORS)
        listing = GP._git(top, "stash", "list", "--format=%H %gd %s")
        if listing is None:
            print("repo_words.py: the git stash list could not be read; no reminder is made", file=sys.stderr)
            return ""
        for row in listing.splitlines():
            sha, _, rest = row.partition(" ")
            ref, _, subject = rest.partition(" ")
            if stash_msg in subject:
                lines.append(f"Your changes from before the tests are still in the git stash \"{stash_msg}\" ({_short(sha)}, now `{ref}`).\n"
                             f"{_prefix('stash')} `git stash apply --index {_short(sha)}`; afterwards `git stash drop {ref}` removes the entry.")
                break
        found = GP._git(top, "log", "--fixed-strings", f"--grep={commit_msg}", "--format=%H%x00%s", "-n", "20")
        for row in (found or "").splitlines():
            sha, _, subject = row.partition("\0")
            if subject == commit_msg:
                branch = GP._git(top, "rev-parse", "--abbrev-ref", "HEAD")
                where = f" on branch `{branch}`" if branch and branch != "HEAD" else ""
                lines.append(f"Before the tests, your changes were committed as {_short(sha)} \"{commit_msg}\"{where}; they stay in its history.")
                break
        return "\n".join(lines)
    except Exception as exc:
        print(f"repo_words.py: the reminder could not be built ({type(exc).__name__})", file=sys.stderr)
        return ""


def _project_of(task_root) -> tuple:
    import hooklib
    from critic_rollcall import project_root_of
    project = project_root_of(Path(task_root))
    config = hooklib.read_json((project or Path(task_root)) / "qa-factory" / "config.json", {}, errors=Exception)
    return project, config if isinstance(config, dict) else {}


def _exact_line(text: str, finding_id: str, option: str, rows: list) -> tuple:
    """`(line, replaced, why)`: the person's line that is EXACTLY the word `option` for the finding `finding_id` (the driver's own reader: the line
    `<id>: <rest>` read by `DriverMachine._FINDING_LINE_RE`, the LAST line for the id decides, its `rest` read by `gate_brief.finding_door_option`),
    or - with no line for that id - the whole text. `why` is the refusal, "" when the word is exact."""
    import gate_brief
    from story_run import Driver       # the facade: a part of the driver family is reached through it only (AR-13, `driver-layers.json` L11)
    mine = []
    for raw in str(text or "").splitlines():
        hit = Driver._FINDING_LINE_RE.match(raw)
        if hit and hit.group("id") == finding_id:
            mine.append((" ".join(raw.split()), hit.group("rest")))
    if not mine:
        mine = [(" ".join(str(text or "").split()), str(text or "").strip())]
    line, rest = mine[-1]
    if "?" in line:
        return "", [], "the line asks a question, and a question is never consent"
    if gate_brief.finding_door_option(rest, rows)[0] != option:
        return "", [], "the line is not exactly that word"
    return line, [earlier for earlier, _rest in mine[:-1]], ""


def main(argv=None) -> int:
    import gate_brief
    import gate_preflight
    import hooklib
    import person_words
    ap = argparse.ArgumentParser(prog="repo_words.py")
    ap.add_argument("--task", required=True)
    ap.add_argument("--word", help="the word the person answered with, exactly (`finding_door_words`)")
    ap.add_argument("--words-file", help="the file holding the person's answer as they gave it")
    ap.add_argument("--by", default="human")
    ap.add_argument("--reminder", action="store_true", help="print the end-of-run line as one JSON object")
    try:
        ns = hooklib.exact_options(ap).parse_args(argv)
    except SystemExit:
        return 2
    if ns.reminder:
        line = ""
        try:
            task_root = hooklib.story_cli("repo_words.py", key=ns.task, exit=False)
            project, config = _project_of(task_root)
            line = reminder_line(project, config, ns.task) if project else ""
        except Exception as exc:
            print(f"repo_words.py: the reminder could not be built ({type(exc).__name__})", file=sys.stderr)
        print(json.dumps({"line": line}))
        return 0
    if not (ns.word and ns.words_file):
        print("repo_words.py needs --word and --words-file (the person's answer as a file): "
              "repo_words.py --task <T> --word <word> --words-file <file>")
        return 2
    task_root = hooklib.story_cli("repo_words.py", key=ns.task)
    command = f"repo_words.py --task {ns.task} --word {shlex.quote(ns.word)}"
    try:
        text = person_words.read(None, ns.words_file, "--words")
    except person_words.WordsRefused as exc:
        print(str(exc))
        return 2
    rows = gate_brief.finding_door_words()
    option = gate_brief.finding_door_option(ns.word, rows)[0]
    if not option:
        print("That is not a word of the test-repository question. Nothing was done.")
        return 2
    doors = gate_brief.shown_doors_of(task_root)
    if doors is None:
        print(f"What gate A showed cannot be read, so nothing was done; show gate A again (`gate_brief.py --task {ns.task} --gate A`) "
              "and ask the person.")
        return 3
    shown = [(fid, d) for fid, held in doors.items() if isinstance(held, list)
             for d in held if isinstance(d, dict) and d.get("option") == option]
    if len(shown) != 1:
        print("The question you were shown does not offer that word, so nothing was done." if not shown else
              "More than one question you were shown offers that word, so nothing was done.")
        return 2
    finding_id, door = shown[0]
    line, replaced, why = _exact_line(text, finding_id, option, rows)
    if why:
        print(f"The person's answer is not the exact word ({why}): ask them once to answer `{finding_id}: {ns.word}`. Nothing was done.")
        return 2
    project, config = _project_of(task_root)
    done, problem = run(task_root, project, config, option, line, replaced, door, finding_id)
    if not done:
        print(problem + " Once that is settled: " + person_words.door(command, path=ns.words_file))
        return 3
    waiver = Path(__file__).resolve().parent / "waiver.py"
    recorded = subprocess.run([sys.executable, "-B", str(waiver), *record_args(ns.task, done), "--by", ns.by], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", cwd=str(project or Path.cwd()), env=gate_preflight.git_env())
    if recorded.returncode:
        print(f"The change IS made ({done['undo']} undoes it), only the record of the person's word failed: "
              f"{_tail(recorded.stdout + ' ' + recorded.stderr)}. Record it with: waiver.py {shlex.join(record_args(ns.task, done))}")
        return 3
    if done.get("failed"):
        print(problem + " Once that is settled: " + person_words.door(command, path=ns.words_file))
        return 3
    print(done_line(done) + ("\n" + problem if problem else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
