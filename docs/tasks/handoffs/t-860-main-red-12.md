# t-860 report

Fix: `ai-packages/qa-factory/scripts/retro_numbers.py:2843` now `from story_run import DriverDialog` (local import kept). story_run.py already re-exports DriverDialog (line 79), so it was not touched. No cycle: retro_numbers is only launched as a subprocess by driver_stage_s8s9.py. Introduced by ef5bdcfe (FV1-9 fix round t-710) per `git log -S`.
Commit fefc18df on fix/main-red-12 (pushed, not merged).

Witness:
- test_driver_layers.py: `=== test_driver_layers: 283/283 ok ===`
- selftest.py --lang: `PASS lang: no control byte ...` / `=== qa-factory selftest: 2/2 ok ===`
- scenario_walk --witness-for retro_numbers.py named scenarios cart-1, local-1-0108, local-1-arm-b and keep files; fast ones run: test_retro_numbers 316/316, test_friction 220/220, test_read_json 500/500, test_silent_passes 326/326, test_whole_identifier 166/166, test_cost_capture_settled 159/159 ok. Not run (slow, judged by canon): scenario tests, test_gate_brief_and_retro, test_role_load, test_story_run_refusals.

Other part-imports flagged: none (L11 clean, 283/283).
Deviations: first commit attempt was refused by the gate (judgment line needs ` -- why`); fixed, recommitted. A first push (before the commit succeeded) pushed the branch at base only; later push updated it.
