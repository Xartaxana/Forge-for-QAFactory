- one column helper for markdown tables (`contract.md_column`, `critic_rollcall.py`): the roll-call reader, the merge-candidates reader and the
  round reader find a column by one exact, case-insensitive, backtick-free name; a roll-call with no `note` column now reads each row's `note` as
  None (no note written) instead of an empty note, and the second reader of that fact (`_has_note_column`) is gone (AR-13)
