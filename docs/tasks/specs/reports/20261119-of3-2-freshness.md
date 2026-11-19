# OF3-2 spec freshness on main 6266f2b0 (scouts t-1571 K1-K3, t-1572 K4-K8; Lead digest, 19.11.2026)

Spec: `docs/tasks/specs/of3-2-knowledge-phase2-spec.md` (round 2, facts read on fb36ae5, 13.11). Nothing of K1-K5, K7, K8 has
landed (K6 merged 665fb82). Behaviour of the cited code mostly holds; line numbers moved almost everywhere. Objects below are the
drift a builder would build wrongly from; P = `ai-packages/qa-factory`.

## Drift in substance

- q1 (K1, keys count): the registry has 9 keys, not 6: `environments.sign_in`, `environments.page_load`, `environments.extra_instance`
  added (17.11). Test list `FIVE_KEYS` P/scripts/tests/test_project_knowledge.py:987-1003 already holds 9; refusal text test :1006-1011
  names 9. After K1: 12 keys. Catalogue knowledge rows P/references/config-keys.json:706-714 (9 rows); new rows go after :714.
  Same stale count in spec §0 F-9, F-9b, F-25b. `report_facts.py` reads `PK.KEYS` at :2037, :2039, :2226.
- q2 (K1, record_problems branch order): P/scripts/project_knowledge.py:902-972; lesson, page_load, extra_instance and sign_in branches
  come BEFORE the role rules, which are the final `else` (:935-959); `record_problems` has a new `value=None` parameter. The spec's
  "role rules only for role_form" must say where the new `first_need` (`manual.*`, `value: one`) keys go relative to these branches.
- q3 (K1, record): `record` :975 has `only_if_latest` (PK2-18, :997), an in-place page_load replacement (:1007-1015) and a lesson
  same-words check (:999-1006). The spec's record changes (condition, supersedes, marker idempotence) must compose with all three.
  PK2-13/PK2-20 (merged 19.11, t-1574) moved the lock into an `event_store` helper and made `cmd_role`/`cmd_account` read the held
  role row under the lock: re-read `lock`, `cmd_role`, `cmd_account` before citing them.
- q4 (K1, cmd_revoke and state-exits): `cmd_revoke` :1231-1245, the "asked again" sentence also covers `EXTRA_INSTANCE_KEY` (:1239),
  non-role sentence :1243-1244. P/design/state-exits.md section :163-173 (sentences to edit :165, :169; a `sign_in` row :170).
- q5 (K3/K5 driver lines): `Person.__init__` P/scripts/driver_core.py:232-263 (`holds` :263); `deferrable` P/scripts/driver_dialog.py:442-457
  (tuple line :452); `say_once` P/scripts/driver_dispatch.py:2939; person builders driver_dispatch.py:3509-3706 (none has `earlier` or
  `fact_keys` yet); `walk_supply_raise(self, facts)` P/scripts/driver_stage_s6.py:1472-1491 takes ONE dict argument; `walk_asked`
  :1466, `walk_ask_once` :1493, `walk_account_raise` :91. driver-layers.json rows :1022 (say_once), :1170 (no_hold), :1252/:1254
  (state keys); layer order at :10.
- q6 (K4 conductor rows): P/references/conductor-actions.json gained an `instance` door at :30; revoke row is now :31; TR3-10 rows
  :38-40; the new `remember`/`kind` row goes after :31. No `remember`/`kind` subparser exists; parsers: account :1397, role :1405,
  revoke :1412, side :1417, lesson :1428, instance :1435, lessons :1442. Margin check test_conductor_doors.py:176 (cap 12000 at :31);
  byte sizes of conductor-actions.json and conductor.md NOT measured by the scouts.
- q7 (K7 axis number): SIBLING_MAP axes 37 (repeat stop), 38 (dry census), 39 (a check's requirement, 19.11) are taken: K7 takes
  axis 40.
- q8 (K8): still only a Lead direction (spec :1018-1030); `## Deferred decisions` HEADING project_decisions.py:112; audit A13 in
  audit_factory.py (:32, :938). The dashboard reader of deferred decisions was not verified.
- q9 (census classes): test_judgment_census.py:93 `CLASSES` includes `safety`; `BREACH_CLASSES` (:95) are word-list, meaning-proxy,
  meaning. The spec's "ceilinged classes ... safety" needs reading against :93-95.

## Holds (line moves only)

K1: about 28 facts (`_derive_keys` :142-158, `STATES` :161, `_usable` :234, `_latest` :247, `state` :328, `value` :385, `roster`
:674, `revoke` :1020, `notice_from_handoff` :1061, E44 test :876-884, `test_asked_row_is_skipped` :267). K2: about 13 (`_context`
:1127, `_write_prologue` :1154, `cmd_show` :1381, project_decisions `upsert` :445 / `resolve` :495, install-paths :32). K3: about 22.
K5: triggers, builders' behaviour, price keys question-prices.json:235-245, `walk_supply_keys` config_contract.py:847.

## Not checked by the scouts

`git log -S` (no Bash in the scout role); byte sizes; §0 facts F-13/14, F-16, F-17, F-21/22, F-24, F-25 outside the K sections.
