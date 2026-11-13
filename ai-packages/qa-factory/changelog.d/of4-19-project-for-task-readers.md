- the walk-timing report and the gate brief's proved-capability check take the story's project through `runtime_paths.project_for_task`, no longer by
  folder depth: a story under a configured `artifact_root` reads its own project's config and is asked about its own project; a story no project
  holds keeps the old "config absent" answer in the timing report and keeps every capability line in the brief (OF4-19)
