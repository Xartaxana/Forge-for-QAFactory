# Потоки работы: кучки онбординга (onboarding-forge/1-3, onboarding-hooks/4)

Слово владельца 12.11.2026: «берём в работу все пачки обоих кучек про онбординг, разложи на параллельные потоки и
запускай разработку». Координатор — сессия на Opus (окно `lead_degraded` 18:18): механизмы форджа, вердикты класса
критика и статусы таблиц — в очередь полного Lead. Разведка — t-129 (скаут: узел → файлы, зависимости, блокеры).

Правило потоков: внутри потока узлы идут последовательно; у потоков одной волны нет общих файлов; каждый поток — своя
ветка-ворктри `wip/of-<поток>` от `origin/main`, принятые коммиты координатор вливает в ветку пачки
`pile/<кучка>/batch-<N>`. Пишущих билдеров одновременно ≤ 6 (правило 12). Критик — один проход на пачку (R13-g).

## Волна 1 (запущена 12.11)

| Поток | Пачка | Узлы по порядку | Владеет файлами (пакет — от `ai-packages/qa-factory/`) | task | Статус |
|---|---|---|---|---|---|
| hooks4 | onboarding-hooks/4 | OH4-1 | `scripts/gate_brief.py`, `scripts/tests/test_gate_brief_and_retro.py` | t-131 | в работе |
| of3-design | onboarding-forge/3 | OF3-1 (спека дизайнера → критик на план) | `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` | t-130 | в работе |
| handoff | onboarding-forge/2 | SC2-42 → HF8-28 → HF8-29 | `scripts/handoff_init.py`, `scripts/handoff_check.py`, их тесты | t-132 | в работе |
| hooklib | onboarding-forge/1 | LR1-5 → CD1-11 → OH3-37 | `scripts/hooklib.py` (функции узлов), `scripts/install_smoke.py`, `hooks/run-py.cmd`, `references/launch-causes.json`, `scripts/cost_capture.py`, `scripts/factory_dashboard.py`, их тесты, `changelog.d/` | t-133 | в работе |
| hot | onboarding-forge/2 | DC1-28 → DC1-27 | `scripts/stage_guard.py`, `scripts/controller.py`, `scripts/story_run.py`, `scripts/question_register.py`, их тесты | t-134 | в работе |
| tests | onboarding-forge/2 | PC1-12 → SC2-34 → OH3-25 | `scripts/tests/test_run_suite_mine.py`, `scripts/tests/test_red_window.py`, `scripts/tests/harness.py`, 13 тестов OH3-25, `scripts/tests/test_sizing.py` | t-135 | в работе |
| small | onboarding-forge/2 | CX2-12 → TQ1-28 → RC1-15 → EP1-19 | `scripts/dispatch_liveness.py`, `scripts/story_progress.py`, `scripts/codex_usage.py`, `references/code-review-rubric.md`, `references/test-code-patterns.md`, `references/common-rules.md`, `references/slices/`, `agents/qa-runner.md`, их тесты | t-136 | в работе |

## Волна 2 (по освобождению слотов; порядок — приоритет)

- doctor (b1): OH3-6 + OH3-12 → OH3-7 (b2) → OF1-4 — `skills/qa-doctor/`, `readiness.py`, `gate_preflight.py` (браузерная проба).
- install (b1): OH3-9 → OF1-2 — `install-paths.json`, `onboard_apply.py`; OF1-2 трогает `config_contract.py`/`config-keys.json` — после принятия спеки фазы 1 (OF3-1), с непересекающимися функциями.
- bundle (b1+b2): SC2-2 (b1) → дизайнер SC2-23 → критик на план → SC2-23 → SC2-28 → SC2-29 → SC2-30 (критик на план) → SC2-31.
- hot-2 (b2, после hot): C3-15 → HF8-4 (L, дизайнер) — `story_run.py`, `controller.py`, `planning_contract.py`, `validate_artifacts.py`.
- misc (b1/b2): SC2-43 (после SC2-42), OF1-3, PC1-4 → PC1-5, SC2-26, DC1-10, EP1-33, RC1-3, RC1-10, TQ1-29, OH1-3, DC1-7, OH3-36 (сначала замер стендов), SC2-10 → SC2-11, OH1-5, OH1-9, OH3-24, SC2-32.

## Ждут фаз пачки 3 (узлы поглощены фазами, отдельно не делаются)

- Фаза 1 (OF3-1): OH1-6, B-319, GW1-38, OH3-42, мёртвые ключи OH3-35; после неё — OF1-1.
- Фаза 3 (OF3-3): OH3-17, SS1-11, SC5-13.
- Фаза 4 (OF3-4): OH3-35 целиком, OH3-2, OH1-7.
- Фаза 5 (OF3-5): RC1-2 (B-133).
- Пачка 3 идёт строго 1 → 2 → (3, 4) → 5 → 6; у каждой фазы дизайнер → критик на план → билдер → критик; фазы 4 и 6 — живой онбординг на стенде.

## Очередь полного Lead (механизмы форджа, слово владельца, живые прогоны)

- Механизмы форджа (`tools/`, `CLAUDE.md`, `PROJECT.md`, `docs/SIBLING_MAP.md`, правила): F6-10, F6-12, F6-13, F6-32, F6-34, F6-37, F6-39, F6-40, F6-43, F6-45, F6-46, F6-47, F6-48, F6-49, F6-52, F6-58, F6-59, F6-41, F6-53, G2-4, SC2-35.
- Слово владельца / живой прогон / проба хоста: F3-1, F3-2, F3-3, F6-2, F6-31, F6-35, F6-36, F6-42, KB1-5, PR1-1.
- Узлы со внешней зависимостью вне этих пачек: F6-55 (F6-54), F6-17 (forge/5, conductor/2 — проверить).

## Уже закрыты (сверить при закрытии пачки)

PC1-2, PC1-7, F6-28, F6-30, F6-33, F6-44, F6-50 — «принято» с хэшами; PC1-3 — перенос с подтверждением владельца.
