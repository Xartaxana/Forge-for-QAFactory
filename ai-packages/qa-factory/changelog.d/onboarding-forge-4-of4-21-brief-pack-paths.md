- brief pack story and home paths (`brief_pack.py`, `runtime_paths.py`): every story path a brief prints is now the story folder read
  through `hooklib.artifact_root`, relative to the story's project, by the new `runtime_paths.story_text`; the home paths come from
  `runtime_paths.HOME` / `home_dir`. A configured `artifact_root` is named as it is, a story outside its project is named by its
  absolute posix path, and the default world prints the same text as before. The blast-radius cap now bounds the reason only, so a
  long path is never cut; an excluded file written under another root is still left out of the brief (OF4-21).
