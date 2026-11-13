"""Synthetic hook-chain regressions; these do not certify live host activation."""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from host_probe import prepare, observe, inspect
from native_context import pending_path


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.factory = self.root / 'qa-factory'
        self.factory.mkdir()
        (self.factory / 'config.json').write_text('{"schema_version": 1}', encoding='utf-8')
        self.add_story('QA-1')
        self.event = dict(host='codex', cwd=str(self.root), session_id='parent', tool_use_id='spawn',
                          hook_event_name='PreToolUse', tool_name='collaborationspawn_agent',
                          tool_input={'task_name': 'qa_factory_context_probe',
                                      'message': 'opaque-native-message', 'fork_turns': 'none'})
        self.probe_path = self.factory / 'state/host-probe.json'
        self.prepare_guard()

    def add_story(self, task):
        path = self.factory / 'artifacts' / task / 'pipeline.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'ticket': task, 'stages': {'S0': {'status': 'pending'}}}))

    def prepare_guard(self):
        data = prepare(self.root, 'parent')
        transcript = self.root / 'rollout.jsonl'
        rows = [{'type': 'session_meta', 'payload': {'id': 'parent'}}]
        for index, command in enumerate(data['commands']):
            call = str(index)
            code = 'text(await tools.exec_command(' + json.dumps({'cmd': command}) + '));'
            output = (json.dumps({'exit_code': 0, 'output': command[5:]}) if index == 0
                      else 'Command blocked by PreToolUse hook: expected deny. Command: ' + command)
            rows.extend([
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'name': 'exec', 'call_id': call, 'input': code}},
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output', 'call_id': call, 'output': [{'type': 'input_text', 'text': output}]}}])
            event = dict(session_id='parent', tool_input={'cmd': command}, hook_event_name='PreToolUse',
                         tool_use_id='exec-' + call, transcript_path=str(transcript))
            observe(self.root, event, 'guard_pre_tool.py', 0 if index == 0 else 2)
            if index == 0:
                observe(self.root, dict(event, hook_event_name='PostToolUse'), 'host_probe.py', 0)
        transcript.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
        self.event['transcript_path'] = str(transcript)
        self.assertEqual(inspect(self.root)['status'], 'verified')

    def hook(self, script, event=None):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root), CLAUDE_PLUGIN_ROOT=str(SCRIPTS.parent))
        return subprocess.run([sys.executable, '-B', str(SCRIPTS / script)],
                              input=json.dumps(event or self.event), cwd=self.root, env=env,
                              capture_output=True, text=True, encoding='utf-8', timeout=30)


class DoctorContext(Base):
    def test_probe_passes_actual_hooks_with_existing_stories(self):
        for count in (1, 2):
            with self.subTest(stories=count):
                if count == 2:
                    self.add_story('QA-2')
                before = {p: p.read_bytes() for p in self.factory.glob('artifacts/*/pipeline.json')}
                for script in ('guard_pre_tool.py', 'inject_context.py'):
                    result = self.hook(script)
                    self.assertEqual(result.returncode, 0, result.stderr)
                packet = json.loads(pending_path(self.root, 'parent').read_text())
                self.assertTrue(packet['diagnostic'])
                self.assertEqual(packet['role'], 'qa-scout')
                self.assertEqual(packet['task_id'], '')
                self.assertIn('QA_CONTEXT_RECEIVED_', packet['context'])
                self.assertNotIn('QA_CONTEXT_RECEIVED_', self.event['tool_input']['message'])
                child = self.root / 'child.jsonl'
                child.write_text(json.dumps({'type': 'session_meta', 'payload': {
                    'id': 'child', 'agent_path': '/root/qa_factory_context_probe', 'parent_thread_id': 'parent'}}) + '\n')
                start = dict(self.event, hook_event_name='SubagentStart', agent_id='child',
                             agent_type='default', agent_transcript_path=str(child))
                result = self.hook('native_context.py', start)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('QA_CONTEXT_RECEIVED_', result.stdout)
                self.assertEqual(json.loads(pending_path(self.root, 'parent').read_text())['status'], 'delivered')
                child_tool = dict(self.event, session_id='child', tool_name='exec_command',
                                  tool_input={'cmd': 'echo forbidden'})
                result = self.hook('guard_pre_tool.py', child_tool)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('without tools', result.stderr)
                for path, content in before.items():
                    self.assertEqual(path.read_bytes(), content)
                self.assertEqual(inspect(self.root)['injection'], 'unverified')

    def test_an_unwritable_packet_refuses_the_launch_and_the_door_opens_when_the_obstacle_goes(self):
        """A6 + A7: a directory sits on the packet's path (the write raises OSError on every OS, whatever the path length)."""
        for script in ('guard_pre_tool.py', 'inject_context.py'):
            self.assertEqual(self.hook(script).returncode, 0)
        packet = pending_path(self.root, 'parent')
        packet.unlink()
        packet.mkdir()
        result = self.hook('inject_context.py')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('could not be written', result.stderr)
        self.assertTrue(any(name in result.stderr for name in ('IsADirectoryError', 'PermissionError', 'FileExistsError')),
                        result.stderr)
        self.assertTrue(packet.is_dir())
        rows = [json.loads(x) for x in (self.factory / 'state/dispatch-denials.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertTrue(any(r['reason'].startswith('INJECT: the factory context of qa-scout') for r in rows), rows)
        packet.rmdir()                                                   # A7: the door the refusal names
        result = self.hook('inject_context.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(pending_path(self.root, 'parent').read_text(encoding='utf-8'))['status'], 'pending')

    def test_probe_requires_current_same_session_guard_evidence(self):
        original = self.probe_path.read_text()
        for variant in ('missing', 'unverified', 'stale', 'foreign', 'malformed'):
            with self.subTest(variant=variant):
                data = json.loads(original)
                if variant == 'unverified': data['checks'] = {}
                if variant == 'stale': data['created_at'] = '2000-01-01T00:00:00+00:00'
                if variant == 'foreign': data['session_id'] = 'another-parent'
                if variant == 'malformed': data['created_at'] = 'invalid'
                self.probe_path.write_text(json.dumps(data))
                if variant == 'missing': self.probe_path.unlink()
                result = self.hook('inject_context.py')
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('diagnostic', result.stderr.lower())
                self.assertFalse(pending_path(self.root, 'parent').exists())

    def test_diagnostic_is_not_a_story_dispatch_exemption(self):
        variants = [dict(self.event, task_id='QA-1'),
                    dict(self.event, tool_input=dict(self.event['tool_input'], agent_type='qa-automator')),
                    dict(self.event, tool_input={'task_name': 'qa_scout', 'message': 'ordinary work'})]
        for event in variants:
            with self.subTest(event=event['tool_input']):
                result = self.hook('inject_context.py', event)
                self.assertEqual(result.returncode, 2, result.stderr)
        self.add_story('QA-2')
        result = self.hook('inject_context.py', variants[-1])
        self.assertEqual(result.returncode, 2)


class PacketNameLength(unittest.TestCase):
    """t-417: the packet name is 32+1+32 hex, so a project root up to PACKET_ROOT_LIMIT characters writes."""

    def root_of(self, length):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        pad = length - len(tmp.name) - 1
        if pad < 1:
            self.skipTest('TEMP is already longer than the root under test')
        root = Path(tmp.name) / ('p' * pad)
        root.mkdir()
        self.assertEqual(len(str(root)), length)
        return root

    def event(self, session='s', task_name='qa_scout__qa_1'):
        return {'session_id': session, 'tool_use_id': 'u1', 'transcript_path': 't',
                '_qa_host': {'input': {'task_name': task_name}}}

    def test_root_at_the_limit_writes_and_one_beyond_exceeds_the_windows_path(self):
        import native_context as N
        self.assertEqual(N.PACKET_ROOT_LIMIT, 143)
        at = self.root_of(N.PACKET_ROOT_LIMIT)
        N.stage(at, self.event(), 'qa-scout', 'ctx', 'QA-1')   # writes through event_store's `.<8 hex>.tmp` name
        path = N.pending_path(at, 's', 'qa_scout__qa_1')
        self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['context'], 'ctx')
        temp_name_extra = len('.' + 'f' * 8 + '.tmp')
        self.assertEqual(len(str(path)) + temp_name_extra, 259)          # the longest the host path allows
        beyond = N._slot(Path('p' * (N.PACKET_ROOT_LIMIT + 1)), 's', 'qa_scout__qa_1')
        self.assertEqual(len(str(beyond)) + temp_name_extra, 260)         # the old failing length, one past the limit

    def test_the_old_failing_path_of_260_now_writes(self):
        import native_context as N
        old_root = 260 - 33 - (64 + 1 + 64 + 5 + 37)                     # 56: the root where the long name failed
        root = self.root_of(old_root)
        N.stage(root, self.event(), 'qa-scout', 'ctx', 'QA-1')
        self.assertTrue(N.pending_path(root, 's', 'qa_scout__qa_1').is_file())

    def test_a_packet_under_the_old_long_name_is_its_own_sessions_never_anothers(self):
        import hashlib
        import native_context as N
        root = self.root_of(60)
        folder = root / 'qa-factory/state/native-context'
        folder.mkdir(parents=True)
        old = folder / (hashlib.sha256(b's').hexdigest() + '-' + hashlib.sha256(b'qa_scout__qa_1').hexdigest() + '.json')
        old.write_text(json.dumps({'status': 'pending', 'session_id': 's', 'role': 'qa-scout'}), encoding='utf-8')
        self.assertEqual([p for p, _ in N._session_packets(root, 's')], [old])
        self.assertEqual(list(N._session_packets(root, 'other')), [])
        self.assertNotEqual(N.pending_path(root, 's', 'qa_scout__qa_1'), old)   # a rebuilt packet gets the new name

    def test_length_arithmetic_is_pure_and_pins_the_limits(self):
        """A1: string roots only, no disk, no TEMP."""
        import native_context as N
        self.assertEqual((N.NAME_HEX, N.PACKET_ROOT_LIMIT, N.SUPPORTED_ROOT), (32, 143, 143))
        self.assertEqual(N.TEMP_NAME_EXTRA, 13)
        root = lambda length: 'C:\\' + 'p' * (length - 3)
        for length, total in ((143, 259), (144, 260)):
            with self.subTest(root=length):
                self.assertEqual(N.write_path_length(root(length), 's', 'qa_scout__qa_1'), length + 116)
                self.assertEqual(N.write_path_length(root(length), 's', 'qa_scout__qa_1'), total)
        self.assertEqual(N.write_path_length(root(176), 's'), 259)
        self.assertEqual(N.write_path_length(root(177), 's'), 260)

    def test_unwritten_facts_table(self):
        """A4: which cause text applies; string roots, explicit platform."""
        import errno
        import native_context as N

        class Winerror206(OSError):
            winerror = 206

        def padded(prefix, length):
            return prefix + 'p' * (length - len(prefix))

        fnf, drive = FileNotFoundError('x'), 'C:\\'
        rows = {
            'at_limit_nt': (padded(drive, 143), fnf, 'nt', 'q', 'write_error'),
            'over_nt': (padded(drive, 144), fnf, 'nt', 'q', 'path_limit'),
            'over_permission': (padded(drive, 144), PermissionError('x'), 'nt', 'q', 'write_error'),
            'over_enametoolong': (padded(drive, 144), OSError(errno.ENAMETOOLONG, 'x'), 'nt', 'q', 'path_limit'),
            'over_winerror206': (padded(drive, 144), Winerror206('x'), 'nt', 'q', 'path_limit'),
            'unc_over': (padded('\\\\srv\\share\\', 144), fnf, 'nt', 'q', 'path_limit'),
            'extended': (padded('\\\\?\\C:\\', 200), fnf, 'nt', 'q', 'write_error'),
            'extended_unc': (padded('\\\\?\\UNC\\srv\\share\\', 200), fnf, 'nt', 'q', 'write_error'),
            'extended_forward_slash': (padded('//?/C:/', 200), fnf, 'nt', 'q', 'write_error'),
            'posix_long': (padded('/', 300), fnf, 'posix', 'q', 'write_error'),
            'unnamed_177': (padded(drive, 177), fnf, 'nt', None, 'path_limit'),
            'empty_message': (padded(drive, 144), FileNotFoundError(), 'nt', 'q', 'path_limit'),
        }
        for name, (root, exc, platform, task, cause) in rows.items():
            with self.subTest(row=name):
                facts = N.unwritten_facts(root, 's', task, exc, platform)
                self.assertEqual(facts['cause'], cause, facts)
                if name == 'over_nt':
                    self.assertEqual((facts['length'], facts['root_length'], facts['packet_limit'], facts['supported']),
                                     (260, 144, 143, 143))
                if name == 'posix_long':
                    self.assertIsNone(facts['limit'])
                if name == 'empty_message':
                    self.assertEqual(facts['error'], '')

    def refuse(self, root, exc, ticket='', stage=None, platform_limits=None):
        """Call refuse_native_packet in process; returns (SystemExit code or None, stderr, denial spy calls)."""
        import contextlib
        import io
        import native_context as N
        import inject_context as IC
        event = self.event()
        spy = mock.Mock()
        err, code = io.StringIO(), None
        with contextlib.redirect_stderr(err), mock.patch.object(IC, 'note_denial', spy), \
                mock.patch.object(N, 'PATH_LIMITS', platform_limits or {os.name: 259}):
            try:
                IC.refuse_native_packet(event, ticket, 'qa-scout', root, exc, stage)
            except SystemExit as stop:
                code = stop.code
        return code, err.getvalue(), spy

    def test_refusal_text_names_cause_door_and_never_151(self):
        """A5: no pass road (ticket empty); the text is a machine line to the orchestrator."""
        from hooklib import TRAPPED
        cases = {
            'path': ('C:\\' + 'p' * 141, FileNotFoundError('gone'),
                     ('qa-scout', 'refused', '144', '260', '259', 'at most 143 characters', 'shorter is safer', 'long paths',
                      'if they can and want to', '(owner: environment)')),
            'write': ('C:\\' + 'p' * 20, PermissionError('locked'), ('qa-scout', 'refused', 'PermissionError', 'again once')),
        }
        for name, (root, exc, facts) in cases.items():
            with self.subTest(case=name):
                code, text, spy = self.refuse(root, exc)
                self.assertEqual(code, 2)
                for fact in facts:
                    self.assertIn(fact, text)
                self.assertNotIn('151', text)
                self.assertNotIn('waiver.py', text)
                spy.assert_called_once()
                self.assertEqual(spy.call_args[0][4], text.split(TRAPPED)[0].rstrip())

    def test_the_recorded_word_passes_only_the_line_it_names(self):
        """A5b (F-1): one scratch project; the pass is journaled, a refusal says the door."""
        import inject_context as IC
        rows = {
            'live_named': ({'stage': 'S1', 'match': 'could not be written', 'decision': 'go on'}, 'S1', None),
            'live_star': ({'stage': 'S1', 'match': '*', 'decision': 'go on'}, 'S1', None),
            'revoked': ({'stage': 'S1', 'match': 'could not be written', 'decision': 'go on', 'revoked_at': 'now'}, 'S1', 2),
            'other_stage': ({'stage': 'S2', 'match': 'could not be written', 'decision': 'go on'}, 'S1', 2),
            'no_pipeline': (None, 'S1', 2),
            'no_stage': ({'stage': 'S1', 'match': 'could not be written', 'decision': 'go on'}, None, 2),
        }
        for name, (override, stage, expected) in rows.items():
            with self.subTest(row=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / 'qa-factory').mkdir()
                (root / 'qa-factory/config.json').write_text('{"schema_version": 1}', encoding='utf-8')
                if override is not None:
                    story = root / 'qa-factory/artifacts/T'
                    story.mkdir(parents=True)
                    (story / 'pipeline.json').write_text(json.dumps(
                        {'ticket': 'T', 'stages': {'S1': {'status': 'running'}}, 'stage_overrides': [override]}), encoding='utf-8')
                import hooklib
                with mock.patch.dict(os.environ, {'CLAUDE_PROJECT_DIR': str(root)}), \
                        mock.patch.object(hooklib, '_PROJECT_ROOT_CACHE', None):
                    event = dict(self.event(), cwd=str(root))
                    import contextlib
                    import io
                    spy, err, code = mock.Mock(), io.StringIO(), None
                    with contextlib.redirect_stderr(err), mock.patch.object(IC, 'note_denial', spy):
                        try:
                            IC.refuse_native_packet(event, 'T', 'qa-scout', root, PermissionError('x'), stage)
                        except SystemExit as stop:
                            code = stop.code
                    import runtime_paths as RP
                    journal = RP.configured(root, None, 'journal.jsonl')
                    rows_logged = [json.loads(x) for x in journal.read_text(encoding='utf-8').splitlines()] if journal.is_file() else []
                self.assertEqual(code, expected, err.getvalue())
                if expected is None:
                    spy.assert_not_called()
                    self.assertEqual([r['event'] for r in rows_logged], ['gate_override'])
                else:
                    spy.assert_called_once()
                    self.assertEqual(rows_logged, [])
                    self.assertEqual('waiver.py --task T --stage S1' in err.getvalue(), stage is not None)
                    if name in ('revoked', 'other_stage', 'no_pipeline'):
                        self.assertIn('--block "could not be written"', err.getvalue())


class NativeStageRefusal(unittest.TestCase):
    """OH6-4: a refused native launch leaves a denial row (named, or inert while a launch of its key is pending); the
    refusal itself (stderr text, exit 2) is unchanged."""

    def setUp(self):
        import hooklib
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'qa-factory').mkdir()
        (self.root / 'qa-factory/config.json').write_text('{"schema_version": 1}', encoding='utf-8')
        self.story = self.root / 'qa-factory/artifacts/QA-1'
        self.story.mkdir(parents=True)
        (self.story / 'pipeline.json').write_text(json.dumps({'ticket': 'QA-1', 'stages': {'S1': {'status': 'running'}}}),
                                                  encoding='utf-8')
        patches = (mock.patch.dict(os.environ, {'CLAUDE_PROJECT_DIR': str(self.root)}),
                   mock.patch.object(hooklib, '_PROJECT_ROOT_CACHE', None))
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def event(self, **drop):
        ev = {'host': 'codex', 'cwd': str(self.root), 'session_id': 's', 'tool_use_id': 'u1', 'tool_name': 'Agent',
              'tool_input': {'subagent_type': 'qa-scout', 'prompt': 'Dispatch id: D-1\nwork'},
              '_qa_host': {'input': {'task_name': 'qa_scout__qa_1'}}}
        for key in drop:
            ev.pop(key)
        return ev

    def staged(self, ev, context='ctx'):
        import native_context as N
        N.stage(self.root, ev, 'qa-scout', context, 'QA-1')

    def refused(self, ev, exc, ticket='QA-1'):
        import inject_context as IC
        err = io.StringIO()
        with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as stop:
            IC.refuse_native_stage(ev, ticket, 'qa-scout', self.root, exc)
        return stop.exception.code, err.getvalue()

    def raised(self, ev, context='ctx'):
        with self.assertRaises(ValueError) as caught:
            self.staged(ev, context)
        return caught.exception

    def rows(self, path=None):
        path = path or self.story / 'state/dispatch-denials.jsonl'
        if not path.is_file():
            return []
        return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines()]

    def belongs(self):
        from controller import Controller
        return Controller(self.story)._denial_times({'id': 'D-1', 'role': 'qa-scout', 'stage': 'S1'}, {}, {})

    def test_native_stage_refusals(self):
        big = 'x' * 100001

        def too_large():
            return self.event(), self.raised(self.event(), big), 'QA-1'

        def no_identity():
            ev = self.event(tool_use_id=None)
            return ev, self.raised(ev), 'QA-1'

        def pending():
            ev = self.event()
            self.staged(ev)
            return ev, self.raised(ev), 'QA-1'

        def busy_lock():
            from event_store import StateConflict
            return self.event(), StateConflict('task has an active state writer'), 'QA-1'

        def big_while_pending():
            ev = self.event()
            self.staged(ev)
            return ev, self.raised(ev, big), 'QA-1'

        def unreadable_pending():
            import native_context as N
            ev = self.event()
            self.staged(ev)
            N._slot(self.root, 's', 'qa_scout__qa_1').write_text('{broken', encoding='utf-8')
            return ev, self.raised(ev, big), 'QA-1'

        def list_pending():
            import native_context as N
            ev = self.event()
            self.staged(ev)
            N._slot(self.root, 's', 'qa_scout__qa_1').write_text('[1]', encoding='utf-8')
            return ev, self.raised(ev, big), 'QA-1'

        def no_ticket():
            return self.event(), self.raised(self.event(), big), ''

        rows = [('B-1 too_large', too_large, 'named'), ('B-2 no_identity', no_identity, 'named'),
                ('B-3 pending', pending, 'inert'), ('B-4 busy_lock', busy_lock, 'inert'),
                ('B-5 too_large_while_pending', big_while_pending, 'inert'),
                ('B-6 unreadable_pending', unreadable_pending, 'inert'),
                ('B-6b list_pending', list_pending, 'inert'), ('B-7 no_ticket', no_ticket, 'project')]
        for name, build, kind in rows:
            with self.subTest(row=name):
                self.reset_story_state()
                ev, exc, ticket = build()
                code, err = self.refused(ev, exc, ticket)
                self.assertEqual((code, err), (2, 'INJECT: ' + str(exc) + '\n'))
                if kind == 'project':
                    self.assertEqual(self.rows(), [])
                    project = self.rows(self.root / 'qa-factory/state/dispatch-denials.jsonl')
                    self.assertEqual([r['reason'] for r in project], ['INJECT: ' + str(exc)])
                    continue
                story_rows = self.rows()
                self.assertEqual(len(story_rows), 1)
                if kind == 'named':
                    self.assertEqual(story_rows[0]['dispatch_id'], 'D-1')
                    self.assertEqual(len(self.belongs()), 1)
                else:
                    self.assertEqual((story_rows[0]['dispatch_id'], story_rows[0]['stage']), (None, None))
                    self.assertEqual(self.belongs(), [])

    def test_native_packet_refusal_rows(self):
        """P-1: an OSError from `stage` leaves a NAMED row, or an INERT one while a same-key packet is pending."""
        import inject_context as IC
        for name, pending, kind in (('P-1a nothing_pending', False, 'named'), ('P-1b pending', True, 'inert')):
            with self.subTest(row=name):
                self.reset_story_state()
                ev = self.event()
                if pending:
                    self.staged(ev)
                err = io.StringIO()
                with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as stop:
                    IC.refuse_native_packet(ev, 'QA-1', 'qa-scout', self.root, OSError('disk'), None)
                self.assertEqual(stop.exception.code, 2)
                story_rows = self.rows()
                self.assertEqual(len(story_rows), 1)
                if kind == 'named':
                    self.assertEqual(story_rows[0]['dispatch_id'], 'D-1')
                else:
                    self.assertEqual((story_rows[0]['dispatch_id'], story_rows[0]['stage']), (None, None))
                    self.assertEqual(self.belongs(), [])

    def reset_story_state(self):
        """Each row starts from an empty story state and an empty packet folder."""
        import shutil
        shutil.rmtree(self.story / 'state', ignore_errors=True)
        shutil.rmtree(self.root / 'qa-factory/state', ignore_errors=True)

    def test_dispatch_refusals_without_a_packet_leave_a_named_row(self):
        """B-8 (check_override) and B-9 (rewritten_input): `dispatch` refuses, writes the row, exits 2 as before."""
        import inject_context as IC
        import host_adapter
        import codex_roles
        import stage_guard
        (self.story / 'state').mkdir()
        (self.story / 'state/controller.json').write_text(json.dumps({'dispatches': {'D-1': {
            'id': 'D-1', 'role': 'qa-scout', 'stage': 'S1', 'status': 'running', 'resolved_model': {}}}}), encoding='utf-8')
        imap = {'roles': {'qa-scout': {}}}
        cases = [('B-8 check_override', 'check_override', True), ('B-9 rewritten_input', 'rewritten_input', False)]
        for name, target, codex in cases:
            with self.subTest(row=name):
                ev = self.event()
                if codex:
                    ev['_qa_host']['input']['agent_type'] = 'qa_scout'
                else:
                    ev['host'] = 'claude'
                (self.story / 'state/dispatch-denials.jsonl').unlink(missing_ok=True)
                err = io.StringIO()
                module = codex_roles if codex else host_adapter
                with contextlib.ExitStack() as stack, contextlib.redirect_stderr(err):
                    stack.enter_context(mock.patch.object(IC, 'load_map', return_value=imap))
                    stack.enter_context(mock.patch.object(IC, 'run_stage_guard'))
                    stack.enter_context(mock.patch.object(IC, 'collect_blocks', return_value=['\nblock']))
                    stack.enter_context(mock.patch.object(stage_guard, 'requested_ticket', return_value='QA-1'))
                    stack.enter_context(mock.patch.object(module, target, side_effect=ValueError('refused: ' + target)))
                    if codex:
                        import worker_lifecycle
                        stack.enter_context(mock.patch.object(worker_lifecycle, 'guard'))
                        stack.enter_context(mock.patch.object(host_adapter, 'role_policy'))
                        stack.enter_context(mock.patch.object(IC, 'codex_role_instructions'))
                    with self.assertRaises(SystemExit) as stop:
                        IC.dispatch(ev, {'rewritten': False})
                self.assertEqual(stop.exception.code, 2, err.getvalue())
                self.assertEqual(err.getvalue(), 'refused: ' + target + '\n')
                rows = self.rows()
                self.assertEqual([(r['dispatch_id'], r['reason']) for r in rows], [('D-1', 'refused: ' + target)])

    def test_launch_pending_table(self):
        import native_context as N
        ev = self.event()
        self.assertFalse(N.launch_pending(self.root, 's', 'qa_scout__qa_1'))      # absent
        self.assertFalse(N.launch_pending(self.root, '', 'qa_scout__qa_1'))       # no session
        self.staged(ev)
        self.assertTrue(N.launch_pending(self.root, 's', 'qa_scout__qa_1'))
        self.assertFalse(N.launch_pending(self.root, 's', 'other_task'))          # another key is another launch
        path = N._slot(self.root, 's', 'qa_scout__qa_1')
        path.write_text(json.dumps({'status': 'delivered'}), encoding='utf-8')
        self.assertFalse(N.launch_pending(self.root, 's', 'qa_scout__qa_1'))
        path.write_bytes(b'\xff\xfe')
        self.assertTrue(N.launch_pending(self.root, 's', 'qa_scout__qa_1'))       # undecodable counts as pending
        with mock.patch.object(N, '_slot', side_effect=RuntimeError('boom')):
            self.assertTrue(N.launch_pending(self.root, 's', 'qa_scout__qa_1'))   # never raises

    def test_one_a24_row_per_native_refusal(self):
        import refusal_registry as RR
        ids = ('NC-context-too-large', 'NC-launch-identity-missing', 'NC-launch-pending')
        entries = {e['id']: e for e in RR.REGISTRY if e['id'] in ids}
        self.assertEqual(sorted(entries), sorted(ids))
        live = RR.sites(RR.PLUGIN_ROOT)
        for ident, entry in entries.items():
            with self.subTest(entry=ident):
                self.assertEqual((entry['file'], entry['function']), ('native_context.py', 'stage'))
                self.assertTrue(entry['unpassable_because'])
                covered = [s for s in live if s['file'] == 'native_context.py' and s['function'] == 'stage'
                           and s['call'].startswith(entry['call'])]
                self.assertEqual(len(covered), 1)

    def test_dispatch_valueerrors_and_every_other_raise_of_the_host_modules_have_an_a24_row(self):
        """OH7-2: B-8 (`check_override`, two raises) and B-9 (`rewritten_input`) are keyed by the text they raise,
        and so is every other refusal of the two files the scanner now reads."""
        import refusal_registry as RR
        self.assertIn('codex_roles.py', RR.SCANNED)
        self.assertIn('host_adapter.py', RR.SCANNED)
        line_entries = [e for e in RR.REGISTRY if e.get('kind') != 'operation']
        live = [s for s in RR.sites(RR.PLUGIN_ROOT) if s['file'] in ('codex_roles.py', 'host_adapter.py')]
        wanted = [('codex_roles.py', 'check_override', 'Native Codex role missing'),
                  ('codex_roles.py', 'check_override', 'Native {role} {key} mismatch'),
                  ('host_adapter.py', 'rewritten_input', 'Explicit desktop model/effort overrides')]
        for file, function, head in wanted:
            with self.subTest(refusal=head):
                sites = [s for s in live if (s['file'], s['function']) == (file, function) and s['call'].startswith(head)]
                self.assertEqual(len(sites), 1, 'the scanner no longer sees the raise')
                rows = [e for e in line_entries if RR._covers(e, sites[0])]
                self.assertEqual(len(rows), 1, f'{file}:{function} `{head}` has no single A24 row')
                self.assertTrue(rows[0]['unpassable_because'] or rows[0]['override'])
        for site in live:
            with self.subTest(site=f"{site['file']}:{site['function']}:{site['call'][:40]}"):
                self.assertEqual(sum(1 for e in line_entries if RR._covers(e, site)), 1)

    def test_every_host_adapter_refusal_speaks_its_registry_text(self):
        """OH7-2 fix round (F2-1): one table drives each refusal row of `host_adapter.py` through its PUBLIC function
        and asserts the raised or blocked text starts with the registry row's `call` (the row's test field is this test).
        Rows keyed by source text rather than by the rendered message (HA-call-shape, HA-no-command-text,
        HA-role-read-only, the connector rows) are not in the table: their test fields name the test that reaches them."""
        import host_adapter as HA
        import refusal_registry as RR
        by_id = {e['id']: e for e in RR.REGISTRY}
        begin, end = '*** Begin Patch', '*** End Patch'

        def wrap(*body):
            return '\n'.join((begin,) + body + (end,))

        def raises(fn, *args):
            try:
                fn(*args)
            except ValueError as error:
                return str(error)
            self.fail('no ValueError raised')

        def blocks(event):
            err = io.StringIO()
            with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as caught:
                HA.role_policy(event, {'schema_version': 1})
            self.assertEqual(caught.exception.code, 2)
            return err.getvalue()

        def call_of(ident):
            return by_id[ident]['call']

        codex = {'host': 'codex'}
        cases = [
            ('HA-event-not-object', lambda: raises(HA.normalize, 5), call_of('HA-event-not-object')),
            ('HA-event-not-object-list', lambda: raises(HA.normalize, ['x']), call_of('HA-event-not-object')),
            ('HA-tool-input-not-object', lambda: raises(HA.normalize, dict(codex, tool_name='Read', tool_input=5)),
             call_of('HA-tool-input-not-object')),
            ('HA-patch-not-text', lambda: raises(HA.patch_operations, 5), call_of('HA-patch-not-text')),
            ('HA-patch-envelope', lambda: raises(HA.patch_operations, 'garbage'), call_of('HA-patch-envelope')),
            ('HA-patch-path', lambda: raises(HA.patch_operations, wrap('*** Add File: ')), call_of('HA-patch-path')),
            ('HA-patch-orphan-content', lambda: raises(HA.patch_operations, wrap('+x')),
             call_of('HA-patch-orphan-content')),
            ('HA-patch-move', lambda: raises(HA.patch_operations, wrap('*** Add File: a', '*** Move to: b')),
             call_of('HA-patch-move')),
            ('HA-patch-move-empty', lambda: raises(HA.patch_operations, wrap('*** Update File: a', '*** Move to: ')),
             call_of('HA-patch-move-empty')),
            ('HA-patch-line', lambda: raises(HA.patch_operations, wrap('*** Update File: a', '???')),
             call_of('HA-patch-line')),
            ('HA-patch-empty', lambda: raises(HA.patch_operations, wrap()), call_of('HA-patch-empty')),
            ('HA-role-nested-delegation',
             lambda: blocks(dict(codex, tool_name='Agent', agent_type='qa-scout', tool_input={})),
             call_of('HA-role-nested-delegation')),
            ('HA-doctor-no-tools',
             lambda: blocks(dict(codex, tool_name='Read', factory_diagnostic=True, tool_input={})),
             call_of('HA-doctor-no-tools')),
            ('HA-stdin-chars',
             lambda: blocks(HA.normalize(dict(codex, tool_name='write_stdin', tool_input={'chars': 'x'}))),
             call_of('HA-stdin-chars')),
            ('HA-exec-tty',
             lambda: blocks(HA.normalize(dict(codex, tool_name='exec_command', tool_input={'cmd': 'ls', 'tty': True}))),
             call_of('HA-exec-tty')),
        ]
        rows = {ident for ident, _, _ in cases}
        for ident in ('HA-event-not-object', 'HA-tool-input-not-object', 'HA-patch-not-text', 'HA-patch-envelope',
                      'HA-patch-path', 'HA-patch-orphan-content', 'HA-patch-move', 'HA-patch-move-empty',
                      'HA-patch-line', 'HA-patch-empty', 'HA-role-nested-delegation', 'HA-doctor-no-tools',
                      'HA-stdin-chars', 'HA-exec-tty'):
            self.assertIn(ident, rows)
            self.assertIn('test_doctor_context.py', by_id[ident]['test'], f'{ident} must cite this test')
        for ident, run, head in cases:
            with self.subTest(row=ident):
                self.assertTrue(run().startswith(head))


DOOR = ('context diagnostic requires current allow/deny evidence in this host session; '
        'run host_probe.py --prepare, its two native commands, then --check')
OTHER = 'belongs to another host session'


class ProbeRefusal(Base):
    """RH2-5: the refusal and the note name the condition that failed (the tail never decides `ready`)."""

    def refuse(self, event=None):
        import stage_guard
        event = dict(event or self.event)
        event['tool_input'] = dict(event['tool_input'], subagent_type='qa-scout')   # what the host adapter adds on the hook path
        err = io.StringIO()
        import hooklib
        # `project_root` is cached per process (a hook is one short call); each case here is its own project
        with (contextlib.redirect_stderr(err), mock.patch.dict(os.environ, {'CLAUDE_PROJECT_DIR': str(self.root)}),
              mock.patch.object(hooklib, '_PROJECT_ROOT_CACHE', None)):
            code = stage_guard.check_dispatch(event)
        return code, err.getvalue()

    def store(self, **change):
        data = json.loads(self.probe_path.read_text())
        data.update(change)
        self.probe_path.write_text(json.dumps(data))

    def test_unverified_keeps_the_door_and_lists_every_unmet_id_in_order(self):
        self.store(checks={})
        code, text = self.refuse()
        ids = [m['id'] for m in inspect(self.root)['missing']]
        self.assertEqual(code, 2)
        self.assertTrue(ids)
        self.assertIn('STAGE GUARD: ' + DOOR + ' Unmet: ', text)
        at = [text.index(i) for i in ids]
        self.assertEqual(at, sorted(at), text)
        self.assertNotIn(OTHER, text)

    def test_verified_probe_of_another_session_says_so_and_names_the_door(self):
        code, text = self.refuse(dict(self.event, session_id='other-session'))
        self.assertEqual(code, 2)
        self.assertIn(DOOR, text)
        self.assertIn('The probe on record ' + OTHER + ': run the pair in this session.', text)
        self.assertNotIn('Unmet', text)
        self.assertNotIn('other-session', text)   # ids of sessions are never printed
        self.assertNotIn('parent', text)

    def test_unverified_probe_of_another_session_says_both(self):
        self.store(checks={})
        code, text = self.refuse(dict(self.event, session_id='other-session'))
        self.assertEqual(code, 2)
        self.assertLess(text.index('Unmet:'), text.index(OTHER))

    def test_no_store_gives_no_sentence_about_another_session(self):
        self.probe_path.unlink()
        code, text = self.refuse()
        self.assertEqual(code, 2)
        self.assertIn('no_probe_file', text)
        self.assertNotIn(OTHER, text)

    def test_empty_missing_says_the_reason_is_not_established(self):
        import stage_guard
        for probe in ({'status': 'unverified', 'missing': []}, {'status': 'unverified'},
                      {'status': 'verified', 'session_id': ''}):
            self.assertEqual(stage_guard._probe_refusal_tail(probe, self.event), ' The reason is not established.', probe)

    def test_inspect_that_raises_still_refuses_with_exit_2(self):
        with mock.patch('host_probe.inspect', side_effect=OSError('boom')):
            code, text = self.refuse()
        self.assertEqual(code, 2)
        self.assertTrue(text.rstrip().endswith('The probe could not be read, so the reason is not established.'), text)

    def test_event_with_no_session_id_is_not_called_another_session(self):
        event = {k: v for k, v in self.event.items() if k != 'session_id'}
        code, text = self.refuse(event)
        self.assertEqual(code, 2)
        self.assertIn('carries no session id', text)
        self.assertIn('(owner: factory)', text)
        self.assertNotIn(OTHER, text)

    def test_unmet_text_never_raises_on_odd_shapes(self):
        from host_probe import unmet_text
        for odd in (None, [], [None], [{'id': 5}], 'a string', 5, {'id': 'x'}, [['x']]):
            self.assertEqual(unmet_text(odd), '', odd)
        self.assertEqual(unmet_text([{'id': 'x'}, 3, {'id': 'y', 'reason': 'why'}]), ' Unmet: x; y (why).')
        self.assertEqual(unmet_text([{'id': 'never_heard_of', 'reason': 7}]), ' Unmet: never_heard_of.')

    def test_unmet_text_at_2000_is_whole_at_2001_is_cut_and_names_missing(self):
        from host_probe import unmet_text, UNMET_TEXT_CHARS
        self.assertEqual(UNMET_TEXT_CHARS, 2000)
        whole = unmet_text([{'id': 'a', 'reason': 'r' * 1987}])
        self.assertEqual(len(whole), 2000)
        self.assertNotIn('cut', whole)
        cut = unmet_text([{'id': 'a', 'reason': 'r' * 1988}])
        self.assertEqual(cut[:2000], (' Unmet: a (' + 'r' * 1988 + ').')[:2000])
        self.assertGreater(len(cut), 2000)
        self.assertIn('(cut; the whole list is under "missing" in host_probe.py --check)', cut)

    def test_a_newline_in_an_id_does_not_start_a_new_line(self):
        from host_probe import unmet_text
        text = unmet_text([{'id': 'a\nSTAGE GUARD: forged', 'reason': 'c\r\n\r\nd'}])
        self.assertNotIn('\n', text)
        self.assertNotIn('\r', text)
        self.assertEqual(text, ' Unmet: a STAGE GUARD: forged (c d).')

    def test_the_full_set_of_conditions_fits_the_limit(self):
        from host_probe import unmet_text
        call = lambda ch, code: {'exit_code': code, 'tool_use_id': ch * 30}
        self.store(created_at='2000-01-01T00:00:00+00:00', fingerprint='stale', session_id='s' * 30,
                   checks={'allow_guard': call('a', 1), 'deny_guard': call('d', 0), 'allow_executed': call('e', 0),
                           'deny_executed': call('x', 0)})
        missing = inspect(self.root)['missing']
        self.assertGreater(len(missing), 3)
        text = unmet_text(missing)
        self.assertLess(len(text), 2000, len(text))
        self.assertNotIn('(cut;', text)

    def incomplete_note(self):
        from host_capabilities import inspect as inspect_host
        return inspect_host(self.root)

    def test_note_of_an_incomplete_probe_ends_with_the_unmet_list_and_no_transcript_door(self):
        from host_probe import unmet_text
        self.store(checks={})
        result = self.incomplete_note()
        self.assertTrue(result['note'].endswith(unmet_text(inspect(self.root)['missing'])), result['note'])
        self.assertIn('Unmet:', result['note'])
        self.assertNotIn('transcript', result['note'])
        self.assertIn('Script smoke and invocation receipts alone do not certify live behavior.', result['note'])

    def test_note_with_empty_missing_says_not_established(self):
        from host_capabilities import inspect as inspect_host
        with mock.patch('host_probe.inspect', return_value={'status': 'unverified', 'missing': []}):
            note = inspect_host(self.root)['note']
        self.assertTrue(note.endswith(' The reason is not established.'), note)

    def test_note_of_a_verified_probe_is_unchanged_by_the_tail(self):
        result = self.incomplete_note()
        self.assertTrue(result['guard_probe']['status'] == 'verified' and not result['story_ready'])
        self.assertTrue(result['note'].startswith('Live allow/deny guard verified; role-context delivery not yet verified.'))
        self.assertNotIn('Unmet', result['note'])
        self.assertNotIn('not established', result['note'])
        self.assertEqual(result['live_parity'], 'not_certified')

    def test_note_of_a_delivered_probe_is_unchanged_by_the_tail(self):
        # kills a tail appended in the story_ready branch (F6)
        from host_capabilities import inspect as inspect_host
        with mock.patch('host_probe.inspect', return_value={'status': 'verified', 'injection': 'verified', 'missing': []}):
            result = inspect_host(self.root)
        self.assertTrue(result['story_ready'], result)
        self.assertEqual(result['note'], 'Live guard and role-context delivery verified; other mechanisms retain '
                                         'their separate evidence status.')

    def test_require_host_hooks_at_an_incomplete_probe_prints_one_warn_line_with_the_unmet_list_no_line_break(self):
        self.store(checks={})
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root), CLAUDE_PLUGIN_ROOT=str(SCRIPTS.parent))
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'readiness.py'), '--require', 'host_hooks'],
                                cwd=self.root, env=env, capture_output=True, text=True, encoding='utf-8', timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [ln for ln in result.stdout.splitlines() if ln.startswith('WARN host_hooks:')]
        self.assertEqual(len(lines), 1, result.stdout)
        self.assertIn('Unmet: ', lines[0])
        self.assertTrue(lines[0].endswith('(owner: factory)'), lines[0])


if __name__ == '__main__':
    unittest.main()
