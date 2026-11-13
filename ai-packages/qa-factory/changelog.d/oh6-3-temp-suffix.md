- atomic writes (`event_store`): the temp file name of every atomic write is now 8 hex characters instead of 32, and the
  file is created exclusively, so a colliding temp name takes a fresh name instead of sharing bytes; the longest project
  root supported on Windows without long paths is 143 characters, raised from 119 (OH6-3)
