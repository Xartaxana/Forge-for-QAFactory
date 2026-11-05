# Measurers

Stand-alone scripts that measure a factory run from the files it leaves behind: money by agent
(`report_run.py`, `report_to_gate.py`, `spend_by_dispatch.py`), stage and role tables
(`stage_compare.py`, `stage_role_table.py`), friction with our code (`code_friction.py`,
`context_shape.py`), contract checks (`check_all_contracts.py`) and the helpers that prepare a run copy
(`prepare_copy.py`, `run_headless.py`). A measurer is code and has a test like any other code (FR-28).

## Run one

From the repository root (never change the working directory):

    python -B experiments/measurers/stage_compare.py s0 --run <run> --ticket <TICKET>

`<run>` is the suffix of a run copy folder. A name the runs table does not list becomes the folder
`<copy_prefix><run>` under the runs base; a name with a separator or `..` is refused.

## Where the runs are

- Runs base: the `QA_RUNS_BASE` environment variable, else `stand_copy_root` of `tools/dev.config.yaml`.
  With neither, reads report a missing path and nothing is written.
- Runs table: the `QA_RUNS_TABLE` environment variable names a JSON file (a relative value is resolved
  from the repository root). Unset or empty means an empty table; a table that is named but cannot be
  read is a refusal, never a partial table. Known keys (an unknown key is refused): `task`,
  `copy_prefix`, `baselines`, `story_runs`, `default_left`, `default_right`, `story_ticket`, `caches`, `runs_dir`,
  `sample_task`, `live_repo`, `toolchain`, `installed_plugins`, `_comment`. Without a table,
  `--left`, `--right`, `--run`, `--ref-run` and `--ticket` have no default and must be passed.
  `installed_plugins` is a list of plugin ids the copy disables (`prepare_copy.py` writes each `false`;
  an empty list or no key disables nothing). `copy_prefix` is letters, digits, `.`, `-`, `_` only, and
  `toolchain.import` a dotted Python name (`pkg`, `pkg.sub`); anything else is refused naming the key.

## Prove them

    python -B experiments/measurers/test_measurers.py
    python -B experiments/measurers/test_prepare_copy.py

Both are self-running scripts that print `=== <name>: N/N ok ===` and exit 1 on any FAIL.
`pytest` over `test_measurers.py` collects no tests and is not the judge.
