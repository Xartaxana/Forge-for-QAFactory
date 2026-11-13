- `execution_request.profiles_owning` reads a profile's `roots.test` with the same refusals as `probe_by_code._in_test_root`: an empty or
  absolute root and one that ends above the project own nothing (a root `/tests` was read as the project's `tests`); the docstrings of
  `_path_key`, `path_under` and `profiles_owning` name the readers as they are now
