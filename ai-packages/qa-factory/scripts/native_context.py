"""Deliver Codex context at SubagentStart without modifying opaque spawn messages."""
import errno
import hashlib
import json
import os
import sys
from pathlib import Path, PureWindowsPath
from event_store import EventStore, StateConflict, atomic_json
from hooklib import person_signal, sorted_paths

PROBE_TASK = 'qa_factory_context_probe'
NAME_HEX = 32
# Longest project root (characters) for which the packet, written through event_store's temp
# name (`.json.<32 hex>.tmp`), stays within the Windows 259-character path limit:
# root + len('\qa-factory\state\native-context\') 33 + 32 + 1 + 32 + len('.json') 5 + len('.<32 hex>.tmp') 37 <= 259.
# The binding receipt `host_dispatch.binding_path` (64 hex) has the same limit, root + 140.
PACKET_ROOT_LIMIT = 119
# Length of `.<uuid4 hex>.tmp`, the temp name `event_store._publish` adds.
TEMP_NAME_EXTRA = 37
# The longest path an ordinary Windows open accepts when long paths are off; a platform not in the table has no
# limit the factory knows.
PATH_LIMITS = {'nt': 259}
# The longest project root the factory's bounded-suffix writers fit under the Windows limit (the native packet and the
# host-dispatch binding, root + 140; measured across the package by t-216); not this file's packet alone. Writers with
# uncapped components are not covered by it.
SUPPORTED_ROOT = 119

DELIVER_WRITE_FAILED = 'FACTORY CONTEXT: the context of {role} ({task}) was delivered, but {what} ({error_type}: {error}).{tail}'
BINDING_UNWRITTEN = ('its launch receipt could not be written; the duplicate-spawn guard and recovery cannot see this '
                     'worker until it stops')
PACKET_UNMARKED = ('its packet could not be marked delivered; it stays pending, so a later launch of this role in this '
                   'session may find two launches waiting and get no context (said when it happens)')
# The closing advice follows the write that failed: the receipt (F-7) can fail on path length, the packet rewrite
# (F-9, same path as the packet already written) never does. A `what` not in the table gets NO tail - never the
# long-path one.
LONG_PATH_TAIL = ' If the project folder is long, a shorter folder or Windows long paths fix it.'
REWRITE_TAIL = ' Check that the project folder is writable and the file is not locked by another process.'
WRITE_FAILURE_TAILS = {BINDING_UNWRITTEN: LONG_PATH_TAIL, PACKET_UNMARKED: REWRITE_TAIL}


def _folder(root):
    return Path(root)/'qa-factory/state/native-context'


def _slot(root, session, task_name=None):
    """The file of ONE launch: <32 hex of sha256(session)>-<32 hex of sha256(task_name)> when
    the launch has a name, <32 hex of sha256(session)> when it has none. The session comes
    first so that one session's packets are found by prefix. 32 hex is 128 bits, so a
    collision is practically none. The short name keeps the packet and its temp file under
    the Windows 259-character path limit for a project root up to PACKET_ROOT_LIMIT characters.
    A packet written under the old 64-hex name is still found by the same prefix and, being
    checked by the session stored inside it, is its own launch's packet, never another's."""
    name = _session_key(session) + ('-' + _digest(task_name) if task_name else '')
    return _folder(root)/(name+'.json')


def _digest(value):
    return hashlib.sha256(str(value).encode()).hexdigest()[:NAME_HEX]


def _session_key(session):
    return _digest(session)


def _session_packets(root, session):
    """(path, packet) of every readable packet of this host session.

    Only files with the session's prefix are opened (the folder is never emptied, and a
    delivery runs under the lock at every SubagentStart); the session stored INSIDE the
    packet is still checked. An unreadable file is skipped: one broken file must not stop
    the delivery of the others."""
    for path in sorted_paths(_folder(root).glob(_session_key(session) + '*.json')):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and data.get('session_id') == session:
            yield path, data


def pending_path(root, session, task_name=None):
    """Where a launch's packet lives. With a task_name, its own file. Without one, the
    session-only packet, or, when there is none, the session's only packet (readers that
    know no task name, such as the doctor's tests, still find the one launch in flight)."""
    if task_name:
        return _slot(root, session, task_name)
    plain = _slot(root, session)
    if plain.is_file():
        return plain
    found = [path for path, _ in _session_packets(root, session)]
    return found[0] if len(found) == 1 else plain


def launch_pending(root, session, task_name=None) -> bool:
    """True when the packet of EXACTLY this launch key (`_slot`) is pending, or exists but cannot be read, parsed or is
    not an object. False for an empty session, an absent file, or another status. Reads only: no lock, no write, never
    raises (any exception is True). Error direction: toward "pending" - the answer decides whether a refused dispatch's
    denial may close it, and a launch that may still be live must never be closed on a guess."""
    try:
        if not session:
            return False
        path = _slot(root, session, task_name)
        if not path.is_file():
            return False
        data = json.loads(path.read_text(encoding='utf-8'))
        return not isinstance(data, dict) or data.get('status') == 'pending'
    except Exception:
        return True


def is_probe_task(name):
    """True for PROBE_TASK itself or PROBE_TASK + '__' + a non-empty suffix.

    A host refuses to reuse a consumed task name, so a second probe after a fix needs a
    fresh one; the suffix follows the same `__suffix` convention a story's task name uses.
    A single underscore, an empty suffix or another prefix is not a probe. Both
    host_adapter.native_role and diagnostic() ask this one predicate."""
    name = str(name or '')
    return name == PROBE_TASK or (name.startswith(PROBE_TASK + '__') and len(name) > len(PROBE_TASK) + 2)


def diagnostic(event):
    ti = event.get('tool_input') or {}
    raw = (event.get('_qa_host') or {}).get('input') or ti
    return ti.get('prompt') == 'QA_FACTORY_CONTEXT_PROBE' or is_probe_task(raw.get('task_name'))


def write_path_length(root, session, task_name=None) -> int:
    """Characters of the packet's path plus the temp name the atomic write adds. Pure, touches no disk."""
    return len(str(_slot(root, session, task_name))) + TEMP_NAME_EXTRA


def unwritten_facts(root, session, task_name, exc, platform=None) -> dict:
    """Facts for the text of a refusal when the packet could not be written; decides nothing about passing.
    `cause` is `path_limit` only when the machine has a known path limit, the path (with its temp name) is over it,
    the path is not an extended-length one and the error is the kind a too-long path raises; else `write_error`."""
    platform = os.name if platform is None else platform
    limit = PATH_LIMITS.get(platform)
    slot = str(_slot(root, session, task_name))
    if platform == 'nt':
        slot = str(PureWindowsPath(slot))   # `//?/C:/...` becomes `\\?\C:\...` on every OS
    extended = slot.startswith('\\\\?\\')
    length = write_path_length(root, session, task_name)
    too_long = bool(limit) and not extended and length > limit and (
        isinstance(exc, FileNotFoundError) or getattr(exc, 'winerror', None) == 206
        or getattr(exc, 'errno', None) == errno.ENAMETOOLONG)
    return {'cause': 'path_limit' if too_long else 'write_error', 'length': length, 'limit': limit,
            'root_length': len(str(root)), 'packet_limit': PACKET_ROOT_LIMIT, 'supported': SUPPORTED_ROOT,
            'error_type': type(exc).__name__, 'error': str(exc)}


def ambiguous_once_key(role, names) -> str:
    """One key per role AND per set of waiting names: the same ambiguity is said once, a different one again."""
    joined = '\n'.join(sorted(str(n or '') for n in names))
    return 'native-ambiguous:' + str(role) + ':' + hashlib.sha256(joined.encode()).hexdigest()[:16]


def _said_write_failure(event, data, what, exc) -> None:
    """A side write of `deliver` failed: say it on stderr and in the journal; the context is still delivered.
    No once key: every failed launch is its own fact. Never raises."""
    text = DELIVER_WRITE_FAILED.format(role=data.get('role'), task=data.get('task_name') or '(no task name)',
                                       what=what, error_type=type(exc).__name__, error=exc,
                                       tail=WRITE_FAILURE_TAILS.get(what, ''))
    try:
        print(text, file=sys.stderr)
    except Exception:
        pass
    person_signal(event, 'inject', text, task=data.get('task_id'))


def stage(root, event, role, context, ticket):
    if len(context) > 100000:
        raise ValueError('Native context exceeds 100000 characters; reduce project slices instead of silently truncating')
    session = event.get('session_id')
    if not session or not event.get('tool_use_id'):
        raise ValueError('Native context requires host session and tool call identities')
    raw = (event.get('_qa_host') or {}).get('input') or {}
    # Every launch keeps its OWN packet, keyed by (session, raw task_name). One slot per
    # session could not tell a stale packet (a failed native launch emits no SubagentStart)
    # from a live one: replacing it handed a running child another story's context, and
    # refusing it blocked every later task of the session. A pending packet under the SAME
    # key is the same launch staged twice (two unnamed launches share the session-only key)
    # and is refused; nothing under another key is read or overwritten. The check stays
    # inside the lock and ahead of the write, so two concurrent stagings cannot both pass it.
    path = _slot(root, session, raw.get('task_name'))
    with EventStore(path.parent).lock():
        if path.is_file() and json.loads(path.read_text(encoding='utf-8')).get('status') == 'pending':
            raise StateConflict('A factory launch is awaiting SubagentStart; retry after it starts, do not replace it')
        atomic_json(path, {'status':'pending', 'role':role, 'context':context,
                          'session_id':session, 'tool_use_id':event['tool_use_id'],
                          'transcript_path':event.get('transcript_path'), 'task_id':ticket,
                          'task_name':raw.get('task_name'), 'diagnostic':diagnostic(event)})


def deliver(root, event):
    from host_adapter import native_role, context_output
    session = event.get('session_id')
    if not session or not event.get('agent_id') or not _folder(root).is_dir():
        return
    with EventStore(_folder(root)).lock():
        pending = [(path, data) for path, data in _session_packets(root, session)
                   if data.get('status') == 'pending']
        if not pending:
            return
        # Which launch is this child? Its own task name when the host exposes it, else its
        # role. A packet whose task_name is known and differs from the child's is never the
        # child's; when more than one packet could be, nothing is delivered and nothing
        # changes (a child that may belong to another launch gets no one's context).
        from host_dispatch import child_identity, record
        child_name = str(child_identity(event).get('task_path') or '').rsplit('/', 1)[-1]
        role = native_role(event.get('agent_type'))
        if child_name:
            chosen = [x for x in pending if x[1].get('task_name') == child_name]
            if not chosen:  # no launch of that name: only an unnamed one, and only of this role
                chosen = [x for x in pending if not x[1].get('task_name') and x[1].get('role') == role]
        else:
            chosen = [x for x in pending if x[1].get('role') == role]
        if len(chosen) > 1:
            # Never silent: a stale packet of a failed launch would otherwise starve every
            # later launch of this role with no trace. stderr only (stdout is the context
            # channel), names only (never the context), and the child's start is not blocked.
            names = ', '.join(str(x[1].get('task_name') or '(no task name)') for x in chosen)
            ambiguity = ('FACTORY CONTEXT: several factory launches of ' + str(role) + ' are waiting in this host '
                         'session (' + names + ') and the host did not say which one this child belongs to, so no '
                         'context was delivered; relaunch the role under a unique task name.')
            print(ambiguity, file=sys.stderr)
            person_signal(event, 'inject', ambiguity, task=None,
                          once_key=ambiguous_once_key(role, [x[1].get('task_name') for x in chosen]))
        if len(chosen) != 1:
            return
        path, data = chosen[0]
        # Both writes below are side records of the delivery; the context is the delivery. A failure of either is
        # said (stderr + one signal) and never costs the child its context: `context_output` runs in every case.
        try:
            record({'hook_event_name':'PostToolUse', 'tool_name':'Agent',
                    'session_id':data['session_id'], 'tool_use_id':data['tool_use_id'],
                    'task_id':data.get('task_id'), 'transcript_path':data.get('transcript_path'),
                    'tool_input':{'subagent_type':data['role']},
                    '_qa_host':{'input':{'task_name':data.get('task_name')}},
                    'tool_response':{'agent_id':event['agent_id'], 'task_name':data.get('task_name')}})
        except Exception as exc:
            _said_write_failure(event, data, BINDING_UNWRITTEN, exc)
        text = data.pop('context', '')
        data.update(status='delivered', agent_id=event['agent_id'])
        try:
            atomic_json(path,data)  # the record keeps identities, not up to 100 KB of context
        except Exception as exc:
            _said_write_failure(event, data, PACKET_UNMARKED, exc)
        context_output(event,text)


def main():
    from hooklib import read_event, project_root
    event = read_event() or {}
    if event.get('hook_event_name') == 'SubagentStart':
        deliver(project_root(event),event)


if __name__ == '__main__':
    main()
