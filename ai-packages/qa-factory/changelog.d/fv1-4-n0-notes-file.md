### Fixed
- A person's answer now reaches the story journal whole at any size: the driver keeps the journal note in a file under `state/words` and passes it with the new `log_append.py --notes-file <path>` (read by the same reader as `--reason-file`), instead of a command-line argument that cuts a long or multi-line text.
- An owed `human_answer` row keeps the file path, so its replay writes the whole note; rows owed by an older release (`--notes <text>`) replay as before. `person_words.lf` is the one place of the CRLF to LF rule.
