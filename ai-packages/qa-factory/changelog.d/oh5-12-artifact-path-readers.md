- the lease registry's job-store lookup, the late-source commands of `source_exclusions.py` and `ticket_adapter.snapshot_hint` take the
  story's folder from the artifact root's one reader (`hooklib.artifact_root`) instead of a literal `qa-factory/artifacts`: a project
  with its own `artifact_root` is followed, a broken config is the reader's refusal, nothing changes for a project without the key (OH5-12)
