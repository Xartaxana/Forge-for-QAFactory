- the S5 handoff forms (`artifacts.runtime_provenance`, `probes.runtime_provenance`, `runtime.provenance`) name the runtime
  provenance record of the form's OWN run: `handoff_check.window_runtime_record` reads the newest run block of the form's dispatch
  that carries one and resolves its `evidence_refs[0]` inside the story; a record chosen by file name, another dispatch's record
  and a file outside the story are never named. When the record cannot be established the field stays blank and the refusal
  says why (`Code could not fill it: ...`) (P1B-9)
