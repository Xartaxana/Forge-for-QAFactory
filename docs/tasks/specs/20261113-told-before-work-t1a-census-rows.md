# Told-before-work - T1a census rows (lists A / B / C), node T1a-rows

Status: builder DRAFT for Lead acceptance (13.11.2026), node T1a-rows of `docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md`
(sections 0.2, 1.2, 2.1, 3.0a, 3.2). Not committed by the builder. Tree read: `W\` =
`C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\`, branch `wip/tbw-t1`, tip b355384
("Merge wip/p1v-t10 (T1-0) into wip/tbw-t1: base fix B1"). Nothing was written in `W\`.

Numbers at b355384 (measured by the probe below; they bind): `old_units` 1145, `new_units` 1257, |A| 113, |B| 13, |C| 1,
`narrow_lost` `[]`, list-only units not created 2202. Difference from the spec's a2c88d8 expectation (113 / 11 / 1): |A| = 113 and
|C| = 1 as expected; |B| is 13, not 11 (two more units flip after P1-v N1-N4 / T1-0 added code: `waiver.py::run_carry` and
`waiver.py::run_stage`, both class safety, ref `A24:...`). A report line, not a stop (spec 3.2).

Role names below drop the `qa-` prefix (`scout` = `qa-scout`); `conductor` is spelled whole. "all 12 roles" = every `agents/qa-*.md`.

## 0 the probe source and its verbatim output

Source: the script of spec 3.2 step 1, saved verbatim as
`C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\t1a_probe.py` (lines 219-276 of the
spec, nothing changed; not committed). Command:

`python -B C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\t1a_probe.py C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory`
(exit 0, empty stderr, about 2 minutes). Output, verbatim:

```json
{
 "tree": "C:\\QAFactory\\forge-repo\\.claude\\worktrees\\tbw-t1\\ai-packages\\qa-factory",
 "old_units": 1145,
 "new_units": 1257,
 "A": [
  {
   "file": "arch_check.py",
   "function": "main",
   "refs": [],
   "sites": [
    206
   ]
  },
  {
   "file": "archive_task.py",
   "function": "cmd_archive",
   "refs": [],
   "sites": [
    196,
    208
   ]
  },
  {
   "file": "archive_task.py",
   "function": "cmd_undo",
   "refs": [],
   "sites": [
    237
   ]
  },
  {
   "file": "archive_task.py",
   "function": "main",
   "refs": [],
   "sites": [
    379
   ]
  },
  {
   "file": "artifact_packet.py",
   "function": "main",
   "refs": [],
   "sites": [
    75
   ]
  },
  {
   "file": "artifact_producer.py",
   "function": "main",
   "refs": [],
   "sites": [
    292,
    303,
    316
   ]
  },
  {
   "file": "artifact_supersede.py",
   "function": "main",
   "refs": [],
   "sites": [
    126,
    130,
    134,
    137,
    145,
    152,
    158,
    163,
    165,
    173,
    187
   ]
  },
  {
   "file": "blast_radius.py",
   "function": "main",
   "refs": [],
   "sites": [
    870
   ]
  },
  {
   "file": "brief_pack.py",
   "function": "main",
   "refs": [],
   "sites": [
    4613
   ]
  },
  {
   "file": "case_versions.py",
   "function": "_empty_answer",
   "refs": [],
   "sites": [
    655
   ]
  },
  {
   "file": "case_versions.py",
   "function": "main",
   "refs": [],
   "sites": [
    684,
    695,
    709
   ]
  },
  {
   "file": "changelog_assemble.py",
   "function": "main",
   "refs": [],
   "sites": [
    274
   ]
  },
  {
   "file": "check_coverage.py",
   "function": "main",
   "refs": [
    "stages.json:S8/qa-doc-scribe"
   ],
   "sites": [
    241
   ]
  },
  {
   "file": "check_delivery.py",
   "function": "main",
   "refs": [],
   "sites": [
    2641
   ]
  },
  {
   "file": "check_traceability.py",
   "function": "main",
   "refs": [],
   "sites": [
    274,
    291
   ]
  },
  {
   "file": "check_witness.py",
   "function": "main",
   "refs": [],
   "sites": [
    291
   ]
  },
  {
   "file": "collect_pack.py",
   "function": "main",
   "refs": [],
   "sites": [
    1475
   ]
  },
  {
   "file": "config_contract.py",
   "function": "main",
   "refs": [],
   "sites": [
    3003,
    3008
   ]
  },
  {
   "file": "config_view.py",
   "function": "main",
   "refs": [],
   "sites": [
    286,
    295,
    299
   ]
  },
  {
   "file": "controller.py",
   "function": "<module>",
   "refs": [],
   "sites": [
    9972,
    9975
   ]
  },
  {
   "file": "copy_detector.py",
   "function": "main",
   "refs": [],
   "sites": [
    493,
    496
   ]
  },
  {
   "file": "cost_capture.py",
   "function": "_cli_recapture",
   "refs": [],
   "sites": [
    3799
   ]
  },
  {
   "file": "critic_rollcall.py",
   "function": "main",
   "refs": [
    "stages.json:S4/qa-case-critic"
   ],
   "sites": [
    1127,
    1139,
    1147,
    1153
   ]
  },
  {
   "file": "device_stand.py",
   "function": "main",
   "refs": [],
   "sites": [
    626
   ]
  },
  {
   "file": "diff_pass.py",
   "function": "main",
   "refs": [],
   "sites": [
    587,
    591,
    599
   ]
  },
  {
   "file": "diff_scope.py",
   "function": "main",
   "refs": [],
   "sites": [
    422
   ]
  },
  {
   "file": "env_probe.py",
   "function": "main",
   "refs": [],
   "sites": [
    1203,
    1217
   ]
  },
  {
   "file": "environment_preparation.py",
   "function": "main",
   "refs": [],
   "sites": [
    584
   ]
  },
  {
   "file": "execution_scheduler.py",
   "function": "main",
   "refs": [],
   "sites": [
    697,
    708
   ]
  },
  {
   "file": "external_writes.py",
   "function": "main",
   "refs": [],
   "sites": [
    1421,
    1425
   ]
  },
  {
   "file": "external_writes.py",
   "function": "record_result",
   "refs": [],
   "sites": [
    865,
    872,
    883,
    889
   ]
  },
  {
   "file": "first_look.py",
   "function": "_cli",
   "refs": [],
   "sites": [
    754,
    759,
    762
   ]
  },
  {
   "file": "gate_brief.py",
   "function": "main",
   "refs": [],
   "sites": [
    5172,
    5209,
    5219
   ]
  },
  {
   "file": "grounding_section.py",
   "function": "_unplaced",
   "refs": [],
   "sites": [
    94
   ]
  },
  {
   "file": "grounding_section.py",
   "function": "main",
   "refs": [],
   "sites": [
    158,
    164,
    167
   ]
  },
  {
   "file": "handoff_check.py",
   "function": "_apply_one",
   "refs": [],
   "sites": [
    2547,
    2549,
    2551,
    2556,
    2559,
    2576
   ]
  },
  {
   "file": "handoff_init.py",
   "function": "main",
   "refs": [],
   "sites": [
    404
   ]
  },
  {
   "file": "hooklib.py",
   "function": "block",
   "refs": [],
   "sites": [
    991
   ]
  },
  {
   "file": "hooklib.py",
   "function": "require_project_at",
   "refs": [],
   "sites": [
    230
   ]
  },
  {
   "file": "hooklib.py",
   "function": "story_cli",
   "refs": [],
   "sites": [
    579
   ]
  },
  {
   "file": "host_probe.py",
   "function": "main",
   "refs": [],
   "sites": [
    1118,
    1125,
    1131
   ]
  },
  {
   "file": "interim_packet.py",
   "function": "main",
   "refs": [],
   "sites": [
    272
   ]
  },
  {
   "file": "ledger.py",
   "function": "main",
   "refs": [],
   "sites": [
    1884
   ]
  },
  {
   "file": "log_append.py",
   "function": "main",
   "refs": [],
   "sites": [
    214,
    217,
    224,
    244
   ]
  },
  {
   "file": "machine_facts.py",
   "function": "main",
   "refs": [],
   "sites": [
    1099
   ]
  },
  {
   "file": "make_fixture_repo.py",
   "function": "main",
   "refs": [],
   "sites": [
    36,
    39,
    58
   ]
  },
  {
   "file": "manifest_from_tests.py",
   "function": "<module>",
   "refs": [],
   "sites": [
    114
   ]
  },
  {
   "file": "manifest_put.py",
   "function": "_seed_from_legacy",
   "refs": [],
   "sites": [
    2247
   ]
  },
  {
   "file": "manifest_put.py",
   "function": "recover",
   "refs": [],
   "sites": [
    2601
   ]
  },
  {
   "file": "manifest_view.py",
   "function": "main",
   "refs": [],
   "sites": [
    177,
    183,
    191
   ]
  },
  {
   "file": "manual_capture.py",
   "function": "_blocked",
   "refs": [],
   "sites": [
    1625
   ]
  },
  {
   "file": "manual_capture.py",
   "function": "error",
   "refs": [],
   "sites": [
    5447
   ]
  },
  {
   "file": "manual_capture.py",
   "function": "main",
   "refs": [],
   "sites": [
    5512
   ]
  },
  {
   "file": "node_ids.py",
   "function": "main",
   "refs": [],
   "sites": [
    870
   ]
  },
  {
   "file": "onboarding_notes.py",
   "function": "main",
   "refs": [],
   "sites": [
    1049
   ]
  },
  {
   "file": "place_answers.py",
   "function": "_cli",
   "refs": [],
   "sites": [
    972
   ]
  },
  {
   "file": "plan_row.py",
   "function": "add_row",
   "refs": [],
   "sites": [
    155,
    158,
    161,
    165,
    170,
    175
   ]
  },
  {
   "file": "plan_row.py",
   "function": "main",
   "refs": [],
   "sites": [
    399,
    402,
    404,
    407,
    412,
    420,
    422
   ]
  },
  {
   "file": "plan_row.py",
   "function": "put_row",
   "refs": [],
   "sites": [
    289,
    294,
    297,
    302,
    305,
    314,
    322
   ]
  },
  {
   "file": "plan_row.py",
   "function": "row_map",
   "refs": [],
   "sites": [
    216
   ]
  },
  {
   "file": "plan_row.py",
   "function": "set_fields",
   "refs": [],
   "sites": [
    334,
    339,
    347,
    355,
    360
   ]
  },
  {
   "file": "plan_row.py",
   "function": "show_rows",
   "refs": [],
   "sites": [
    203
   ]
  },
  {
   "file": "planning_contract.py",
   "function": "main",
   "refs": [
    "stages.json:S3/qa-test-strategist"
   ],
   "sites": [
    4569
   ]
  },
  {
   "file": "probe_by_code.py",
   "function": "_read_model_file",
   "refs": [],
   "sites": [
    4858,
    4860,
    4863,
    4868,
    4870,
    4872
   ]
  },
  {
   "file": "probe_by_code.py",
   "function": "_unrestored_exit",
   "refs": [],
   "sites": [
    8038
   ]
  },
  {
   "file": "probe_by_code.py",
   "function": "load_models",
   "refs": [],
   "sites": [
    4947
   ]
  },
  {
   "file": "probe_debt.py",
   "function": "main",
   "refs": [],
   "sites": [
    1283,
    1286,
    1293
   ]
  },
  {
   "file": "project_decisions.py",
   "function": "_record_finding",
   "refs": [],
   "sites": [
    863
   ]
  },
  {
   "file": "project_decisions.py",
   "function": "_refusal_as_line",
   "refs": [],
   "sites": [
    874,
    877
   ]
  },
  {
   "file": "project_gitignore.py",
   "function": "main",
   "refs": [],
   "sites": [
    143,
    147
   ]
  },
  {
   "file": "project_knowledge.py",
   "function": "_fail",
   "refs": [],
   "sites": [
    807
   ]
  },
  {
   "file": "question_register.py",
   "function": "main",
   "refs": [],
   "sites": [
    1737
   ]
  },
  {
   "file": "readiness.py",
   "function": "main",
   "refs": [],
   "sites": [
    1413,
    1443
   ]
  },
  {
   "file": "red_sandbox.py",
   "function": "main",
   "refs": [],
   "sites": [
    2261
   ]
  },
  {
   "file": "refusal_registry.py",
   "function": "main",
   "refs": [],
   "sites": [
    1765
   ]
  },
  {
   "file": "release_fingerprint.py",
   "function": "main",
   "refs": [],
   "sites": [
    395
   ]
  },
  {
   "file": "report_adapt.py",
   "function": "cmd_kind",
   "refs": [],
   "sites": [
    328
   ]
  },
  {
   "file": "retro_numbers.py",
   "function": "main",
   "refs": [],
   "sites": [
    3172,
    3179,
    3182,
    3202
   ]
  },
  {
   "file": "role_cli.py",
   "function": "error",
   "refs": [],
   "sites": [
    111
   ]
  },
  {
   "file": "role_cli.py",
   "function": "main",
   "refs": [],
   "sites": [
    186
   ]
  },
  {
   "file": "role_cli.py",
   "function": "run_guarded",
   "refs": [],
   "sites": [
    161,
    164,
    166,
    171
   ]
  },
  {
   "file": "run_py_entry.py",
   "function": "main",
   "refs": [],
   "sites": [
    135
   ]
  },
  {
   "file": "run_suite.py",
   "function": "collect_only",
   "refs": [],
   "sites": [
    2969,
    2977
   ]
  },
  {
   "file": "runtime_probe.py",
   "function": "do_suggest",
   "refs": [],
   "sites": [
    1498,
    1505,
    1520
   ]
  },
  {
   "file": "runtime_probe.py",
   "function": "main",
   "refs": [],
   "sites": [
    1630,
    1640
   ]
  },
  {
   "file": "s5_plan.py",
   "function": "main",
   "refs": [],
   "sites": [
    1522
   ]
  },
  {
   "file": "selftest.py",
   "function": "cmd_slow_tests",
   "refs": [],
   "sites": [
    1158,
    1162,
    1168
   ]
  },
  {
   "file": "selftest.py",
   "function": "main",
   "refs": [],
   "sites": [
    1390,
    1431
   ]
  },
  {
   "file": "source_exclusions.py",
   "function": "main",
   "refs": [],
   "sites": [
    624,
    630,
    646,
    652,
    663,
    668,
    672,
    687,
    690
   ]
  },
  {
   "file": "source_preflight.py",
   "function": "<module>",
   "refs": [],
   "sites": [
    189
   ]
  },
  {
   "file": "stage_done.py",
   "function": "main",
   "refs": [],
   "sites": [
    1547,
    1551,
    1555,
    1560,
    1566
   ]
  },
  {
   "file": "stage_done.py",
   "function": "record_acceptance",
   "refs": [],
   "sites": [
    968,
    975,
    989,
    993,
    999,
    1008,
    1014,
    1022,
    1046
   ]
  },
  {
   "file": "stage_done.py",
   "function": "set_facts",
   "refs": [],
   "sites": [
    918,
    923
   ]
  },
  {
   "file": "stage_guard.py",
   "function": "explain",
   "refs": [],
   "sites": [
    2933
   ]
  },
  {
   "file": "stage_status.py",
   "function": "main",
   "refs": [],
   "sites": [
    410,
    415
   ]
  },
  {
   "file": "stand_lease.py",
   "function": "main",
   "refs": [],
   "sites": [
    403
   ]
  },
  {
   "file": "story_budget.py",
   "function": "main",
   "refs": [],
   "sites": [
    434
   ]
  },
  {
   "file": "story_progress.py",
   "function": "main",
   "refs": [],
   "sites": [
    731
   ]
  },
  {
   "file": "story_version.py",
   "function": "main",
   "refs": [],
   "sites": [
    140
   ]
  },
  {
   "file": "test_repo_base.py",
   "function": "main",
   "refs": [],
   "sites": [
    386,
    389
   ]
  },
  {
   "file": "ticket_adapter.py",
   "function": "_accept_gap_kind",
   "refs": [],
   "sites": [
    1953,
    1968,
    1984
   ]
  },
  {
   "file": "ticket_adapter.py",
   "function": "_query",
   "refs": [],
   "sites": [
    2325,
    2339,
    2345,
    2358
   ]
  },
  {
   "file": "ticket_adapter.py",
   "function": "fail",
   "refs": [],
   "sites": [
    269
   ]
  },
  {
   "file": "tms_publication.py",
   "function": "<module>",
   "refs": [],
   "sites": [
    156
   ]
  },
  {
   "file": "waiver.py",
   "function": "run_remark",
   "refs": [],
   "sites": [
    1230
   ]
  },
  {
   "file": "waiver.py",
   "function": "run_revoke",
   "refs": [],
   "sites": [
    870
   ]
  },
  {
   "file": "waiver.py",
   "function": "show",
   "refs": [],
   "sites": [
    1384
   ]
  },
  {
   "file": "walk_session.py",
   "function": "call",
   "refs": [],
   "sites": [
    1947
   ]
  },
  {
   "file": "walk_session.py",
   "function": "main",
   "refs": [],
   "sites": [
    2081,
    2090
   ]
  },
  {
   "file": "walk_session.py",
   "function": "open_walk",
   "refs": [],
   "sites": [
    1958,
    1964,
    1996,
    1997
   ]
  },
  {
   "file": "window_budget.py",
   "function": "main",
   "refs": [],
   "sites": [
    455
   ]
  },
  {
   "file": "window_files.py",
   "function": "main",
   "refs": [],
   "sites": [
    229
   ]
  },
  {
   "file": "window_record.py",
   "function": "main",
   "refs": [],
   "sites": [
    2103
   ]
  }
 ],
 "B": [
  {
   "file": "controller.py",
   "function": "_refuse_gate_decision",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "environment_record.py",
   "function": "_refuse",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "grounding_section.py",
   "function": "_refuse_missing",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "manifest_put.py",
   "function": "run",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "project_decisions.py",
   "function": "run",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "question_register.py",
   "function": "_refuse",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "report_adapt.py",
   "function": "_refuse",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "run_suite.py",
   "function": "_refuse_phantom_story",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "stand_identity.py",
   "function": "_refuse",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "waiver.py",
   "function": "run",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  },
  {
   "file": "waiver.py",
   "function": "run_carry",
   "roles": [
    "conductor"
   ],
   "class": "safety",
   "ref": "A24:WV-carry-source, A24:WV-carry-target"
  },
  {
   "file": "waiver.py",
   "function": "run_stage",
   "roles": [
    "conductor"
   ],
   "class": "safety",
   "ref": "A24:CTRL-next-blocked"
  },
  {
   "file": "window_record.py",
   "function": "run",
   "roles": [
    "conductor"
   ],
   "class": "shape",
   "ref": null
  }
 ],
 "B0_override_false": [],
 "C": [
  {
   "file": "check_coverage.py",
   "function": "<script>",
   "roles": [
    "qa-doc-scribe"
   ],
   "class": "shape",
   "ref": "stages.json:S8/qa-doc-scribe"
  }
 ],
 "narrow_lost": [],
 "list_only_units_not_created": 2202
}
```

Reading of the probe: `narrow_lost` is `[]` (no unit of the narrow road is lost, E5 holds); `new_units` 1257 = `old_units` 1145 + 113 - 1;
`B0_override_false` is `[]`. The B rows already carry a row each (none is duplicated in list A). `A24:...` refs of the two waiver B rows stay.
Re-measure of the ceilings on b355384 (a second pure read, `cblocks.py` in the scratchpad): per-role effective blocking counts equal the
`ratchet.blocking_per_role` ceilings exactly (True), rows of class safety = 82 = `ratchet.safety`, and the old
`check_coverage.py::<script>` unit is effectively blocking (so its removal lowers `qa-doc-scribe` by 1).

How the rows were decided (spec 3.2 step 2). Roles (F1 (a), in order): (1) the `roles` of the `references/role-commands.json` commands whose
first token is the unit's script; (2) the stage role of a `references/stages.json` detectors script (the probe's `refs`); (3) a role
whose `agents/<role>.md` names the script as something the role runs, or whose `references/slices/<role>/common-rules.md` tells the role to
run it (a slice that only says "writer / reader / written by / a chain" of an artifact is NOT a role running the script, see Q1); (4) else
`["conductor"]` with the parent 2.8 group (G-free unless noted). Class/owner: read from the body at the probe's `sites`; shape = form /
presence of a call or file, xref = a join against another record, safety = a guard that protects another party's data or a restore.
Everything is `blocks: yes` (a unit exists only because a non-list site was seen: the flip loop sets it). No `blocks_override`.

## 1 list A - rows to ADD (113)

Columns: unit | class | roles (step that decided) | owner | `ref` | blocks | one-line reason | evidence (first site file:line, +n further sites).

| # | unit | class | roles (step) | owner | ref | blocks | reason | evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | `arch_check.py::main` | shape | conductor (4: G-free) | data | - | yes | tests root not found: call-input presence | arch_check.py:206 |
| 2 | `archive_task.py::cmd_archive` | safety | conductor (4: G-free) | intent | - | yes | 2nd site stops archiving unfinished work until a person's words (`--force --words-file`); 1st site is a missing-story shape check | archive_task.py:196 (+1) |
| 3 | `archive_task.py::cmd_undo` | shape | conductor (4: G-free) | data | - | yes | no story / pipeline.json at the path | archive_task.py:237 |
| 4 | `archive_task.py::main` | shape | conductor (4: G-free) | data | - | yes | person_words file refused (form of the words file) | archive_task.py:379 |
| 5 | `artifact_packet.py::main` | shape | conductor (4: G-free) | data | - | yes | bad request printed as one JSON error, exit 2 | artifact_packet.py:75 |
| 6 | `artifact_producer.py::main` | shape | bug-reporter, case-designer, failure-analyst, requirements-tester (1) | data | - | yes | story_of error / missing --path via `refuse`: call form | artifact_producer.py:292 (+2) |
| 7 | `artifact_supersede.py::main` | safety | conductor (4: G-free) | data | - | yes | ownership/containment guard: only the role that writes an artifact, inside the task root, may set it aside (sites 145-173); the rest are argument shape | artifact_supersede.py:126 (+10) |
| 8 | `blast_radius.py::main` | shape | conductor (4: G-free) | data | - | yes | story root error printed, exit 3 | blast_radius.py:870 |
| 9 | `brief_pack.py::main` | shape | conductor (4: G-free) | data | - | yes | story not there: one JSON error, exit 2 | brief_pack.py:4613 |
| 10 | `case_versions.py::_empty_answer` | shape | automator, case-designer (1) | data | - | yes | no pinned case: exit 1 with the text, never a pass | case_versions.py:655 |
| 11 | `case_versions.py::main` | xref | automator, case-designer (1) | data | - | yes | cases of the story not pinned in the store (story cases joined to store versions); 1st site story_of error | case_versions.py:684 (+2) |
| 12 | `changelog_assemble.py::main` | shape | conductor (4: G-free) | data | - | yes | `Refusal` of assemble printed, exit 2 | changelog_assemble.py:274 |
| 13 | `check_coverage.py::main` | shape | doc-scribe (2) | data | stages.json:S8/qa-doc-scribe | yes | root not a marked root: refusal printed, exit 2 | check_coverage.py:241 |
| 14 | `check_delivery.py::main` | shape | doc-scribe (3) | data | - | yes | no such artifacts directory | check_delivery.py:2641 |
| 15 | `check_traceability.py::main` | shape | conductor (4: G-free) | data | - | yes | no artifacts directory / no requirement rows: nothing to trace | check_traceability.py:274 (+1) |
| 16 | `check_witness.py::main` | shape | conductor (4: G-free) | data | - | yes | usage line, missing artifact argument | check_witness.py:291 |
| 17 | `collect_pack.py::main` | shape | conductor (4: G-free) | data | - | yes | unexpected-error text, nothing kept | collect_pack.py:1475 |
| 18 | `config_contract.py::main` | shape | conductor (4: G-free) | data | - | yes | unreadable config / refused proposal printed with its door; the judging is in the raisers | config_contract.py:3003 (+1) |
| 19 | `config_view.py::main` | shape | conductor (4: G-free) | data | - | yes | path syntax / config not loaded | config_view.py:286 (+2) |
| 20 | `controller.py::<module>` | shape | conductor (4: G-code) | data | - | yes | request missing a required field / bad request, one JSON line, exit 2 (module-level CLI tail) | controller.py:9972 (+1) |
| 21 | `copy_detector.py::main` | shape | conductor (4: G-free) | data | - | yes | --root not a directory; --min/--window under 1 | copy_detector.py:493 (+1) |
| 22 | `cost_capture.py::_cli_recapture` | shape | conductor (4: G-free) | data | - | yes | `--recapture` without --session / --all-stale | cost_capture.py:3799 |
| 23 | `critic_rollcall.py::main` | shape | case-critic (1) | data | stages.json:S4/qa-case-critic | yes | a flag with no value, via `refuse` | critic_rollcall.py:1127 (+3) |
| 24 | `device_stand.py::main` | shape | conductor (4: G-free) | data | - | yes | no readable qa-factory/config.json under the root | device_stand.py:626 |
| 25 | `diff_pass.py::main` | shape | requirements-tester, scout (3) | data | - | yes | --diff missing / no diff at the path | diff_pass.py:587 (+2) |
| 26 | `diff_scope.py::main` | shape | conductor (4: G-free) | data | - | yes | --file / --since required | diff_scope.py:422 |
| 27 | `env_probe.py::main` | shape | scout (3) | data | - | yes | environment not configured; the stand cannot be used (layer 1) | env_probe.py:1203 (+1) |
| 28 | `environment_preparation.py::main` | shape | conductor (4: G-free) | data | - | yes | one plain-text refusal line, exit 2 | environment_preparation.py:584 |
| 29 | `execution_scheduler.py::main` | shape | conductor (4: G-free) | data | - | yes | config unreadable / invalid schedule JSON, exit 2 | execution_scheduler.py:697 (+1) |
| 30 | `external_writes.py::main` | shape | bug-reporter, retro-analyst (1) | data | - | yes | ticket id missing; unexpected error caught and returned | external_writes.py:1421 (+1) |
| 31 | `external_writes.py::record_result` | shape | bug-reporter, retro-analyst (1) | data | - | yes | unreadable proposal, proposal outside a story, external id / remote revision missing | external_writes.py:865 (+3) |
| 32 | `first_look.py::_cli` | shape | runner (1) | data | - | yes | end/put call form via `refuse` | first_look.py:754 (+2) |
| 33 | `gate_brief.py::main` | shape | conductor (4: G-free) | data | - | yes | --task required; gate message file not writable | gate_brief.py:5172 (+2) |
| 34 | `grounding_section.py::_unplaced` | shape | conductor (4: G-free) | data | - | yes | lines could not be placed with certainty: nothing shown, door named | grounding_section.py:94 |
| 35 | `grounding_section.py::main` | shape | conductor (4: G-free) | data | - | yes | story_of error; grounding file unreadable | grounding_section.py:158 (+2) |
| 36 | `handoff_check.py::_apply_one` | shape | all 12 roles (3) | data | - | yes | malformed `--fix` field line: list written whole / field named / contract-owned / unknown field (form of the values) | handoff_check.py:2547 (+5) |
| 37 | `handoff_init.py::main` | shape | conductor (4: G-free) | data | - | yes | task root error, one JSON line, exit 2 | handoff_init.py:404 |
| 38 | `hooklib.py::block` | shape | conductor (4: G-free, see Q3) | data | - | yes | emitter: prints the guard's message and exits 2 (the decision is the caller's) | hooklib.py:991 |
| 39 | `hooklib.py::require_project_at` | shape | conductor (4: G-free, see Q3) | data | - | yes | not a factory project root: refusal text and exit | hooklib.py:230 |
| 40 | `hooklib.py::story_cli` | shape | conductor (4: G-free, see Q3) | data | - | yes | story key error as one JSON line, exit 2 | hooklib.py:579 |
| 41 | `host_probe.py::main` | shape | conductor (4: G-free) | data | - | yes | not a project / no session id | host_probe.py:1118 (+2) |
| 42 | `interim_packet.py::main` | shape | conductor (4: G-free) | data | - | yes | task root not a story folder | interim_packet.py:272 |
| 43 | `ledger.py::main` | shape | conductor (4: G-free) | data | - | yes | no such artifacts directory | ledger.py:1884 |
| 44 | `log_append.py::main` | shape | conductor (4: G-free) | data | - | yes | reason / event / batch arguments (one of, not both) | log_append.py:214 (+3) |
| 45 | `machine_facts.py::main` | shape | conductor (4: G-free) | data | - | yes | rules file unreadable | machine_facts.py:1099 |
| 46 | `make_fixture_repo.py::main` | shape | conductor (4: G-free) | data | - | yes | fixture not found / target not empty | make_fixture_repo.py:36 (+2) |
| 47 | `manifest_from_tests.py::<module>` | shape | automator (3) | data | - | yes | markers unavailable: CLI refuses with the door (module-level) | manifest_from_tests.py:114 |
| 48 | `manifest_put.py::_seed_from_legacy` | shape | automator, code-critic (1) | data | - | yes | fragment not committed after the legacy seed: projection failure text | manifest_put.py:2247 |
| 49 | `manifest_put.py::recover` | shape | automator, code-critic (1) | data | - | yes | journal could not be replayed: text with its door | manifest_put.py:2601 |
| 50 | `manifest_view.py::main` | shape | conductor (4: G-free) | data | - | yes | --task required / no context-manifest | manifest_view.py:177 (+2) |
| 51 | `manual_capture.py::_blocked` | shape | failure-analyst, runner (1) | data | - | yes | stand/login/device block: the registry's refusal text, exit ENV_BLOCKED | manual_capture.py:1625 |
| 52 | `manual_capture.py::error` | shape | failure-analyst, runner (1) | data | - | yes | argparse error routed through `refuse` | manual_capture.py:5447 |
| 53 | `manual_capture.py::main` | shape | failure-analyst, runner (1) | data | - | yes | story_of error via `refuse` | manual_capture.py:5512 |
| 54 | `node_ids.py::main` | shape | conductor (4: G-free) | data | - | yes | --ids and the test command required | node_ids.py:870 |
| 55 | `onboarding_notes.py::main` | shape | conductor (4: G-free) | data | - | yes | NotesError printed, exit REFUSED | onboarding_notes.py:1049 |
| 56 | `place_answers.py::_cli` | shape | failure-analyst (1) | data | - | yes | answer recorded but the register refused its line | place_answers.py:972 |
| 57 | `plan_row.py::add_row` | xref | case-designer, test-strategist (1) | data | - | yes | duplicate row id against the plan rows; `_row_from` form refusal (site 155) | plan_row.py:155 (+5) |
| 58 | `plan_row.py::main` | shape | case-designer, test-strategist (1) | data | - | yes | one thing per call; story_of error | plan_row.py:399 (+6) |
| 59 | `plan_row.py::put_row` | xref | case-designer, test-strategist (1) | data | - | yes | row id not in the plan (`--put-row` of an absent row); form of the given row | plan_row.py:289 (+6) |
| 60 | `plan_row.py::row_map` | shape | case-designer, test-strategist (1) | data | - | yes | plan map could not be established with certainty | plan_row.py:216 |
| 61 | `plan_row.py::set_fields` | xref | case-designer, test-strategist (1) | data | - | yes | row id not in the plan, field not in the row; `FIELD=VALUE` form | plan_row.py:334 (+4) |
| 62 | `plan_row.py::show_rows` | xref | case-designer, test-strategist (1) | data | - | yes | wanted row id not in the plan | plan_row.py:203 |
| 63 | `planning_contract.py::main` | shape | test-strategist (2) | data | stages.json:S3/qa-test-strategist | yes | argument is a directory / not a plan file | planning_contract.py:4569 |
| 64 | `probe_by_code.py::_read_model_file` | safety | code-critic (3) | data | - | yes | path containment: a model file outside the task base (a link out counts) is refused; missing file | probe_by_code.py:4858 (+5) |
| 65 | `probe_by_code.py::_unrestored_exit` | safety | code-critic (3) | data | - | yes | the author's file bytes could not be verified restored after a probe: STOP text with the restore door | probe_by_code.py:8038 |
| 66 | `probe_by_code.py::load_models` | shape | code-critic (3) | data | - | yes | no model stored in the file | probe_by_code.py:4947 |
| 67 | `probe_debt.py::main` | shape | conductor (4: G-free) | data | - | yes | task / story folder error | probe_debt.py:1283 (+2) |
| 68 | `project_decisions.py::_record_finding` | shape | retro-analyst (3) | data | - | yes | add-finding refused: recorded earlier | project_decisions.py:863 |
| 69 | `project_decisions.py::_refusal_as_line` | shape | retro-analyst (3) | data | - | yes | ValueError / registry-busy turned into one refusal line, exit 2 | project_decisions.py:874 (+1) |
| 70 | `project_gitignore.py::main` | shape | conductor (4: G-free) | data | - | yes | table error / --root not a directory | project_gitignore.py:143 (+1) |
| 71 | `project_knowledge.py::_fail` | shape | conductor (4: G-free) | data | - | yes | prints the message, returns 2 | project_knowledge.py:807 |
| 72 | `question_register.py::main` | shape | conductor (4: G-free) | data | - | yes | vocabulary unreadable (RuntimeError) | question_register.py:1737 |
| 73 | `readiness.py::main` | xref | conductor (4: G-free) | data | - | yes | capabilities a story needs vs what is available (blockers, site 1443); unknown capability name (site 1413) | readiness.py:1413 (+1) |
| 74 | `red_sandbox.py::main` | shape | failure-analyst (1) | data | - | yes | diagnostic request refused: message relayed with the registry's card | red_sandbox.py:2261 |
| 75 | `refusal_registry.py::main` | shape | conductor (4: G-free) | data | - | yes | --census file unreadable | refusal_registry.py:1765 |
| 76 | `release_fingerprint.py::main` | shape | conductor (4: G-free) | data | - | yes | `--write` refused (ReleaseRefusal) | release_fingerprint.py:395 |
| 77 | `report_adapt.py::cmd_kind` | shape | conductor (4: G-free) | data | - | yes | report-kind record row could not be written | report_adapt.py:328 |
| 78 | `retro_numbers.py::main` | shape | retro-analyst (3) | data | - | yes | --task required; story not there | retro_numbers.py:3172 (+3) |
| 79 | `role_cli.py::error` | shape | conductor (4: G-free) | data | - | yes | argparse error routed through `refuse` | role_cli.py:111 |
| 80 | `role_cli.py::main` | shape | conductor (4: G-free) | data | - | yes | name is not a registered role command | role_cli.py:186 |
| 81 | `role_cli.py::run_guarded` | shape | conductor (4: G-free) | data | - | yes | FileNotFoundError / ValueError of a role command turned into a refusal | role_cli.py:161 (+3) |
| 82 | `run_py_entry.py::main` | shape | conductor (4: G-free) | data | - | yes | missing script name | run_py_entry.py:135 |
| 83 | `run_suite.py::collect_only` | shape | automator, code-critic, failure-analyst, runner (3) | data | - | yes | collect gave no test ids: collect_failed JSON, never a pass (FR-59) | run_suite.py:2969 (+1) |
| 84 | `runtime_probe.py::do_suggest` | shape | conductor (4: G-free) | data | - | yes | --no-container and --container exclude each other; refusal line | runtime_probe.py:1498 (+2) |
| 85 | `runtime_probe.py::main` | shape | conductor (4: G-free) | data | - | yes | no running story; --checkout required | runtime_probe.py:1630 (+1) |
| 86 | `s5_plan.py::main` | shape | automator (3) | data | - | yes | PlanUnreadable / StoryRootError printed, REFUSED | s5_plan.py:1522 |
| 87 | `selftest.py::cmd_slow_tests` | shape | conductor (4: G-free) | data | - | yes | unreadable --from-file / shard join problem | selftest.py:1158 (+2) |
| 88 | `selftest.py::main` | shape | conductor (4: G-free) | data | - | yes | layers/slow-tests error; quarantine run failure, exit 2 | selftest.py:1390 (+1) |
| 89 | `source_exclusions.py::main` | shape | conductor (4: G-free) | data | - | yes | exactly-one-of flags, story root, unreadable/fatal list file, --revoke needs the person's --words, no record / unknown id (presence of words is shape) | source_exclusions.py:624 (+8) |
| 90 | `source_preflight.py::<module>` | shape | conductor (4: G-free) | data | - | yes | --repo / --source-ref error as one JSON object (module-level) | source_preflight.py:189 |
| 91 | `stage_done.py::main` | shape | conductor (4: G-free) | data | - | yes | --task / --stage required | stage_done.py:1547 (+4) |
| 92 | `stage_done.py::record_acceptance` | xref | conductor (4: G-free) | data | - | yes | pipeline.json absent; stage without roles in stages.json; form not under the task root; the critic form's dispatch is of another stage; acceptor/verdict/quote pairing | stage_done.py:968 (+8) |
| 93 | `stage_done.py::set_facts` | shape | conductor (4: G-free) | data | - | yes | no pipeline.json; current-code-diff refusal printed | stage_done.py:918 (+1) |
| 94 | `stage_guard.py::explain` | shape | conductor (4: G-free) | data | - | yes | unknown stage id vs stages.json (CLI helper print) | stage_guard.py:2933 |
| 95 | `stage_status.py::main` | shape | conductor (4: G-free) | data | - | yes | --task / --event required | stage_status.py:410 (+1) |
| 96 | `stand_lease.py::main` | shape | conductor (4: G-free) | data | - | yes | lease record held by another process: nothing released | stand_lease.py:403 |
| 97 | `story_budget.py::main` | shape | conductor (4: G-free) | data | - | yes | --task required | story_budget.py:434 |
| 98 | `story_progress.py::main` | shape | conductor (4: G-free) | data | - | yes | StoryProgressError printed, exit 2 | story_progress.py:731 |
| 99 | `story_version.py::main` | shape | conductor (4: G-free) | data | - | yes | exactly one of --check / --record | story_version.py:140 |
| 100 | `test_repo_base.py::main` | shape | conductor (4: G-free) | data | - | yes | task folder error / no such story | test_repo_base.py:386 (+1) |
| 101 | `ticket_adapter.py::_accept_gap_kind` | shape | bug-reporter, code-critic, doc-scribe, failure-analyst, requirements-tester, retro-analyst, runner, scout (3) | data | - | yes | form of the gap-acceptance call; record_gap_class problem | ticket_adapter.py:1953 (+2) |
| 102 | `ticket_adapter.py::_query` | shape | bug-reporter, code-critic, doc-scribe, failure-analyst, requirements-tester, retro-analyst, runner, scout (3) | data | - | yes | usage / --path refused before any request | ticket_adapter.py:2325 (+3) |
| 103 | `ticket_adapter.py::fail` | shape | bug-reporter, code-critic, doc-scribe, failure-analyst, requirements-tester, retro-analyst, runner, scout (3) | data | - | yes | emitter: prints the message and raises Fail(code) | ticket_adapter.py:269 |
| 104 | `tms_publication.py::<module>` | shape | conductor (4: G-free) | data | - | yes | ValueError / JSON error printed, exit 2 (module-level) | tms_publication.py:156 |
| 105 | `waiver.py::run_remark` | shape | conductor (4: G-free) | data | - | yes | no pipeline.json: a remark belongs to an existing story | waiver.py:1230 |
| 106 | `waiver.py::run_revoke` | shape | conductor (4: G-free) | data | - | yes | no live override matching: nothing to revoke | waiver.py:870 |
| 107 | `waiver.py::show` | shape | conductor (4: G-free) | data | - | yes | no readable pipeline.json | waiver.py:1384 |
| 108 | `walk_session.py::call` | shape | failure-analyst, runner (1) | data | - | yes | exit-2 answer of the server relayed through `refuse` | walk_session.py:1947 |
| 109 | `walk_session.py::main` | shape | failure-analyst, runner (1) | data | - | yes | story_of error; exactly one of --steps-file / --line | walk_session.py:2081 (+1) |
| 110 | `walk_session.py::open_walk` | xref | failure-analyst, runner (1) | data | - | yes | open problems (before-order) and the named env against the config's environments (`env_row`) | walk_session.py:1958 (+3) |
| 111 | `window_budget.py::main` | shape | conductor (4: G-free) | data | - | yes | --task and --stage required | window_budget.py:455 |
| 112 | `window_files.py::main` | shape | conductor (4: G-free) | data | - | yes | task folder does not exist | window_files.py:229 |
| 113 | `window_record.py::main` | shape | code-critic (3) | data | - | yes | missing artifact is a finding with an owner: printed, EXIT_BAD_ARGS | window_record.py:2103 |

Evidence of the step for every unit whose roles are not `conductor`:

- `artifact_producer.py` step 1: role-commands.json `artifact_producer.py publish` / `validate-batch` (bug-reporter, case-designer, failure-analyst, requirements-tester).
- `case_versions.py` step 1: `case_versions.py --pin` (automator, case-designer).
- `check_coverage.py` step 2: stages.json S8 detectors, ref `stages.json:S8/qa-doc-scribe` (doc-scribe).
- `critic_rollcall.py` step 1: `critic_rollcall.py --store` (case-critic); also the S4 detector (ref `stages.json:S4/qa-case-critic`).
- `external_writes.py` step 1: `external_writes.py --record` (bug-reporter, retro-analyst).
- `first_look.py` step 1: `first_look.py put` / `show` (runner).
- `manifest_put.py` step 1: `manifest_put.py --fragment` (automator, code-critic).
- `manual_capture.py` step 1: `manual_capture.py ui` / `http` / `app` (failure-analyst, runner).
- `place_answers.py` step 1: `place_answers.py write` (failure-analyst).
- `plan_row.py` step 1: `plan_row.py` (case-designer, test-strategist).
- `planning_contract.py` step 2: stages.json S3 detectors, ref `stages.json:S3/qa-test-strategist` (test-strategist).
- `red_sandbox.py` step 1: `red_sandbox.py --diagnostic` (failure-analyst).
- `walk_session.py` step 1: `walk_session.py open` / `step` / `look` / ... (failure-analyst, runner).
- `check_delivery.py` step 3: `agents/qa-doc-scribe.md:22` (the scribe quotes the word `check_delivery.py` printed).
- `diff_pass.py` step 3: `agents/qa-requirements-tester.md:68`, `agents/qa-scout.md:69` (tool lists).
- `env_probe.py` step 3: `agents/qa-scout.md:71` (tool list).
- `handoff_check.py` step 3: `references/slices/<each of the 12 roles>/common-rules.md`: `handoff_check.py --file <it> --fix --values -`.
- `manifest_from_tests.py` step 3: `agents/qa-automator.md:69,72` (the automator runs it and fills its form).
- `probe_by_code.py` step 3: `agents/qa-code-critic.md:68,70,77` (`--alternatives`, `--judge`).
- `project_decisions.py` step 3: `agents/qa-retro-analyst.md:62` (`project_decisions.py add-finding`).
- `retro_numbers.py` step 3: `agents/qa-retro-analyst.md:3,61,73` (the script is "on your card"; see Q1).
- `run_suite.py` step 3: `agents/qa-automator.md:68`, `agents/qa-code-critic.md:69`, `agents/qa-failure-analyst.md:73`, `agents/qa-runner.md:62`.
- `s5_plan.py` step 3: `agents/qa-automator.md:68` (`s5_plan.py --task <TICKET> --check`).
- `ticket_adapter.py` step 3: `agents/qa-scout.md:68` and `references/slices/<role>/common-rules.md` of bug-reporter, code-critic, doc-scribe, failure-analyst, requirements-tester, retro-analyst, runner, scout ("a ticket through `ticket_adapter.py`").
- `window_record.py` step 3: `agents/qa-code-critic.md:69` (`window_record.py --review-receipt`).

Files named only as data in slices (not a role running them, so step 4): `check_traceability.py`, `check_witness.py`, `cost_capture.py`,
`ledger.py`, `question_register.py`, `readiness.py`, `waiver.py` (see Q1). Files no `agents/` or slice names at all: the rest of the
conductor rows.

## 2 list B - rows that CHANGE (13)

The unit is non-blocking today and becomes blocking when T1a widens `units_of` (probe `B`; `B0_override_false` is empty, so no ceiling
moves are skipped). Class and `ref` stay; roles change only where the F1 (a) rule finds roles for the script (a relabel, named).

| # | unit | class (kept) | old roles | roles after | relabel | note |
|---|---|---|---|---|---|---|
| 1 | `controller.py::_refuse_gate_decision` | shape | conductor | conductor | no | step 4, G-code |
| 2 | `environment_record.py::_refuse` | shape | conductor | conductor | no | step 4, G-free |
| 3 | `grounding_section.py::_refuse_missing` | shape | conductor | conductor | no | step 4, G-free |
| 4 | `manifest_put.py::run` | shape | conductor | automator, code-critic | yes: -conductor, +automator, +code-critic | step 1: `manifest_put.py --fragment` |
| 5 | `project_decisions.py::run` | shape | conductor | retro-analyst | yes: -conductor, +retro-analyst | step 3: `agents/qa-retro-analyst.md:62` |
| 6 | `question_register.py::_refuse` | shape | conductor | conductor | no | step 4, G-free |
| 7 | `report_adapt.py::_refuse` | shape | conductor | conductor | no | step 4, G-free |
| 8 | `run_suite.py::_refuse_phantom_story` | shape | conductor | automator, code-critic, failure-analyst, runner | yes: -conductor, +automator, +code-critic, +failure-analyst, +runner | step 3: the four agents files of `run_suite.py` |
| 9 | `stand_identity.py::_refuse` | shape | conductor | conductor | no | step 4, G-free |
| 10 | `waiver.py::run` | shape | conductor | conductor | no | step 4, G-free |
| 11 | `waiver.py::run_carry` | safety | conductor | conductor | no | step 4, G-free; keeps `ref: A24:WV-carry-source, A24:WV-carry-target` |
| 12 | `waiver.py::run_stage` | safety | conductor | conductor | no | step 4, G-free; keeps `ref: A24:CTRL-next-blocked` |
| 13 | `window_record.py::run` | shape | conductor | code-critic | yes: -conductor, +code-critic | step 3: `agents/qa-code-critic.md:69` |

B0 (`blocks_override: false` rows that would flip, listed for the record): none.

## 3 list C - rows to REMOVE (1)

| # | unit | roles | ref | replaced by |
|---|---|---|---|---|
| 1 | `check_coverage.py::<script>` | doc-scribe | `stages.json:S8/qa-doc-scribe` | `check_coverage.py::main` (A row 13, carries `ref: stages.json:S8/qa-doc-scribe`) |

Other `detectors` scripts that gain units in list A keep their `<script>` row only if they still have no function unit: the probe
found exactly one stale `<script>` row (`C` has one entry); `critic_rollcall.py` and `planning_contract.py` already have function-unit rows
carrying their `ref` (old rows `_budget_errors` ..., `_claim_key_errors` ...), so their A rows (`main`) carry the same `ref`.

## 4 per role - the raises T1a makes

Reason for every line: `T1a: census rows for wide-transport units (told-before-work T0 gate item 2)`. Reconciliation (spec 2.1):
new - old == |A rows naming r| + |B rows naming r (roles after)| - |C rows naming r that were effectively blocking| + relabels adding r -
relabels removing r. A B unit is NON-blocking today, so its old roles were never counted: its roles-after enter the blocking count whole
(the `relabels` terms are therefore folded into the `+B` column, where `conductor` leaving a B row costs nothing).

| role | old ceiling | +A | +B (roles after) | -C (blocking) | new ceiling | new - old |
|---|---|---|---|---|---|---|
| qa-automator | 173 | 8 | 2 | 0 | 183 | +10 |
| qa-bug-reporter | 139 | 7 | 0 | 0 | 146 | +7 |
| qa-case-critic | 164 | 2 | 0 | 0 | 166 | +2 |
| qa-case-designer | 139 | 10 | 0 | 0 | 149 | +10 |
| qa-code-critic | 139 | 11 | 3 | 0 | 153 | +14 |
| qa-doc-scribe | 139 | 6 | 0 | 1 | 144 | +5 |
| qa-failure-analyst | 140 | 14 | 1 | 0 | 155 | +15 |
| qa-requirements-tester | 157 | 6 | 0 | 0 | 163 | +6 |
| qa-retro-analyst | 139 | 9 | 1 | 0 | 149 | +10 |
| qa-runner | 140 | 12 | 1 | 0 | 153 | +13 |
| qa-scout | 139 | 6 | 0 | 0 | 145 | +6 |
| qa-test-strategist | 171 | 8 | 0 | 0 | 179 | +8 |
| conductor | 680 | 71 | 9 | 0 | 760 | +80 |
| (sum) | 2459 | | | | 2645 | +186 |

(Column `+A` per role = the number of list A rows naming it: for example qa-doc-scribe 6 = `check_coverage::main`, `check_delivery::main`,
`handoff_check::_apply_one`, 3 x `ticket_adapter`; conductor 71 = the 71 step-4 rows.)

`safety`: old 82 (counts every ROW of class safety, blocking or not, `_c3`) + 4 (list A rows judged safety: `archive_task.py::cmd_archive`,
`artifact_supersede.py::main`, `probe_by_code.py::_read_model_file`, `probe_by_code.py::_unrestored_exit`) + 0 (list B keeps its classes,
the two safety B rows are already counted) - 0 (the list C row is shape) = 86.

Unchanged (any other move is a stop, T1a E8): `word-list` 0, `meaning-proxy` 8, `meaning` 24, `breach` 1, `blocks_overrides` 10.

### Reconciliation of spec 2.1 (rows and units)

- census rows: old 1145 + |A| 113 - |C| 1 = 1257 = the probe's `new_units`. After T1a the same probe prints `A: []`, `B: []`, `C: []` and `old_units` 1257.
- list B moves no row count (13 rows change in place); the join after T1a must read `units_no_row 0`, `join_share 1.0`.
- per-role sum: +186 = 170 role-entries of the A rows (8+7+2+10+11+6+14+6+9+12+6+8+71) + 17 role-entries of the B rows (automator 2,
  code-critic 3, failure-analyst 1, retro-analyst 1, runner 1, conductor 9) - 1 (the C row, doc-scribe) = 186. The A column was
  recomputed from the table above by a script (`verify_rows.py`, scratchpad): 113 unique units in the probe's order, 101 shape / 8 xref /
  4 safety, per-role counts equal.

## Questions for the Lead

- Q1 (step 3 of the F1 (a) rule, which mentions count): I counted `agents/<role>.md` lines that put a script on the role's tool list or
  have it run it, and `common-rules.md` lines that tell the role to run it. I did NOT count slice lines that only say a script is the
  writer / reader / the check chain of an artifact (`ledger.py`, `check_delivery.py` readers, `check_traceability.py`, `check_witness.py`,
  `cost_capture.py`, `readiness.py`, `question_register.py`, `waiver.py`). Read literally ("a slice names the script") these would add
  roles to 7 more files: A rows `check_traceability::main` (+case-critic, case-designer), `check_witness::main` (+automator, code-critic),
  `cost_capture::_cli_recapture` (+bug-reporter, doc-scribe, retro-analyst), `ledger::main` (+case-critic, case-designer, doc-scribe,
  failure-analyst, runner), `readiness::main` (+bug-reporter, doc-scribe, retro-analyst), `question_register::main` (+requirements-tester),
  `waiver` x3 (+failure-analyst). `retro_numbers.py` (agents file: "on your card", "run retro_numbers.py first") is borderline: counted as retro-analyst.
  Confirm or reverse; reversing moves only the A rows named here and the per-role table of section 4.
- Q2 (B relabel): the F1 (a) rule finds roles for 4 B units (`manifest_put.py::run`, `project_decisions.py::run`,
  `run_suite.py::_refuse_phantom_story`, `window_record.py::run`); I replaced `conductor` by the rule's roles, as for list A. Their sibling
  rows (`manifest_put.py::_merge`, `window_record.py::build`, ...) stay `["conductor"]` today. Confirm replace (done here) vs keep
  `conductor` for B rows.
- Q3 (hooklib): `hooklib.py::block`, `require_project_at`, `story_cli` are the shared exits of the hook guards that every role meets (road
  (a) of parent 2.8); existing `hooklib.py` rows (`append_jsonl_line`, `artifact_root`, ...) carry all 12 roles + conductor. No agents file
  or slice names `hooklib.py`, so by the rule they are step 4 (conductor, G-free); the roles would be the 12 roles if the Lead reads road (a) as step 3.
  Same for `stage_guard.py::explain` and `stage_done.py` (existing rows carry all roles).
- Conductor rows carry the parent-2.8 group in the "roles (step)" cell (G-free, G-code for `controller.py`). The rule's step 4 asks for the
  group in a `note`: T1a writes it into the row's `note` field.

## Undecided - Lead

None. No unit was left out; no unit is read `word-list`, `meaning-proxy`, `meaning` or `breach` (T1a E8). Borderline class calls, all
decided by the rule and listed so the Lead can overrule: `archive_task.py::cmd_archive` (safety/intent, the person-words guard),
`artifact_supersede.py::main` (safety/data), `probe_by_code.py::_read_model_file` and `_unrestored_exit` (safety/data, containment and
restore guards), `source_exclusions.py::main` (shape: the `--words` presence check is form, not a guard), `readiness.py::main`,
`stage_done.py::record_acceptance`, `walk_session.py::open_walk`, `case_versions.py::main`, 4 `plan_row.py` units (xref; 8 xref rows in all).
No unit refuses nothing on reading (E3 note not needed).

## Analog rows noticed in the census (not changed)

Existing rows in the same files stay `["conductor"]` where the F1 (a) rule now says roles (role-command scripts: `plan_row.py::_own_errors`,
`manifest_put.py::_merge`, `case_versions.py::validate_batch`, `artifact_producer.py::publish`, `manual_capture.py::_http_login`,
`external_writes.py::check` ...); the rule gives A rows roles but leaves their siblings, so a role-command script ends with mixed labels.
`hooklib.py` / `stage_guard.py` / `stage_done.py` existing rows carry all 12 roles while their new A rows are conductor (Q3).
`external_writes.py::check|run|list_proposals|refuse_local_key` are safety/intent while the new `main`/`record_result` rows are shape.

## Lead decisions (13.11.2026, acceptance of this file, t-608) - these BIND T1a and override the tables above where they differ

- Q1: CONFIRMED as drafted. A role is named only where an agents file or a slice puts the script on the role's tool list or tells the
  role to run it; a line that only names a script as the writer / reader / check chain of an artifact adds no role. `retro_numbers.py`
  stays retro-analyst.
- Q2: CONFIRMED "replace". The four B units take the rule's roles; `conductor` leaves them. Their mixed-label sibling rows are an
  analog queued to the Lead, not T1a's.
- Q3: OVERRULED. The seven hook-guard rows of list A - `hooklib.py::block`, `hooklib.py::require_project_at`, `hooklib.py::story_cli`,
  `stage_done.py::main`, `stage_done.py::record_acceptance`, `stage_done.py::set_facts`, `stage_guard.py::explain` - take the SAME roles
  list as the existing rows of their own file in `judgment-census.json` (read it there: all 12 roles plus conductor for hooklib; for
  `stage_done.py` and `stage_guard.py` whatever their existing rows carry). Reason: one file, one road, one label (P31); every role meets
  the hook guard. T1a recomputes section 4 for these seven rows (each named role gains +1 per row; conductor's +A does not change if the
  file's existing rows carry conductor too) and prints the recomputed table and the reconciliation in its report. If the existing rows
  of one of these files do NOT agree with each other on roles, STOP for that file and return the row sets.
- The conductor group of step 4 goes into the row's `note` field, as the builder says.
- Class calls listed under "Undecided - Lead": accepted as drafted.
