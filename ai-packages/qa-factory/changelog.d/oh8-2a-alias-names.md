- no other spelling of a story key reaches that story's folder (OH8-2): `hooklib.artifacts_dir` refuses a key that is another spelling of an existing
  story folder (`t`, `T.`, `T `, the 8.3 short name, a junction or symlink alias) with a `StoryRootError` that names the folder and says to pass its exact
  name, and refuses a key with a blank at either end or a trailing dot on every file system; an exact key and a new clean key give the path as before
- new leaves in `hooklib`: `clean_key` (the shape of a story key), `alias_twins`, `landing_name` (the listed folder a write lands in, by `os.path.samefile`),
  `other_spelling` (the one predicate "another spelling of an existing folder") and `is_story_with_pipeline`; `is_story_folder` calls `clean_key`, so an existing
  folder whose name ends in a dot or a blank is no longer a story to any reader, on any OS
- the story-key probes of the resolver and the gates ask `is_story_with_pipeline` (`stage_guard` steps 1, 1b, 2 and 5, `exit_gate._named_ticket`,
  `bug_records._story_exists`) and `host_dispatch` asks `is_story_folder` (`controller_record`, the spawn receipt): an alias is no story, and the deny names the identity facts
- `exit_gate._identity`: an explicit task id that is another spelling of a story folder is `unknown-task` (a full audit, never a pass), and the audit header says
  `explicit id 'T.' is another spelling of folder 'T'; keys are matched exactly`
- the pre-tool guard judges the story folder a write actually lands in (`guard_pre_tool._path_story`, never raises): a write through an alias spelling is
  judged by that story's owner rule instead of passing as an absent story
