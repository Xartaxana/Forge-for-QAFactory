# TD-11 — резка больших файлов: бриф лида для дизайнеров

Lead, 11.11.2026. Носитель узла — `docs/tasks/test-diet.md`, строка TD-11. Этот файл — замысел и измеренные факты;
спеки пишут дизайнеры (три темы, раздел «Спеки»). Развилки дизайнер возвращает, не решает.

## Слова владельца (11.11.2026, сессия с владельцем)

1. Цель: параллельная работа билдеров и скорость тестов; большие файлы режем.
2. «Если эти файлы не в карантине, то их тоже режем» — про медленные тестовые файлы.
3. «Если они большие и мешают параллельности, то их тоже режем» — про остальные горячие файлы пакета.
4. `story_run.py` режется ДО первого релиза на GitHub (пачка `github-move/3`).

## Решения лида (технические, владельцу показаны 11.11.2026)

- Граница `story_run.py` — по карте слоёв `scripts/tests/fixtures/driver-layers.json` (t-301 N0), а не «по областям
  тестов», как стояло в TD-11. Слой `driver_stages` (230 имён) дополнительно делится по стадиям модулями одного ранга.
- Переносит ЗАКОММИЧЕННЫЙ СКРИПТ, читающий карту, а не модель руками: перенос повторим поверх свежего `main`
  (прецедент — `tools/piles_split.py`). Свидетель переноса — вывод скрипта и тесты, не пересказ.
- Один способ для всех файлов (P31): та же схема карты (`names`: `{name, kind, home}`) и тот же инструмент.
- Имена `story_run.py` и `controller.py` остаются входными файлами и фасадами: старые импорты и команды работают.
- 91 ожидающий узел пачек не переписывается: где теперь функция, исполнитель узнаёт по карте (строка в
  `plans/builder-rules.md`); список горячих файлов в `PROJECT.md` («Командная работа», п. 3) правится после резки.
- Узел C3-24 (разбить функцию `Controller.validate`) идёт ПОСЛЕ резки `controller.py`.
- Вторая волна исходников (`contract.py`, `brief_pack.py`, `planning_contract.py`, `s5_precheck.py`) и
  `factory_dashboard.py` — вне этих спек.
- Чтение правила тестов: части разрезанного оставленного файла — не «новые тесты» (`docs/TESTING.md`, «новый тестовый
  файл не создаётся»); каждая часть наследует строку `keep` исходного. Владелец не возразила; правка текста правила —
  в спеке тестов.
- Карантинные тесты не чинятся и не правятся; покрасневшие от переноса помечает лид («перенос TD-11»).

## Измеренные факты (скауты t-015…t-022, 11.11.2026; пути от `ai-packages/qa-factory/`)

### story_run.py (22 171 строка)

- Уровень модуля — строки 1–1080 (константы, таблицы `KNOWN_REFUSALS`, `GATE_REPAIRS`, классы исключений, чтение
  состояния, разбор Codex); ОДИН класс `class Driver(DriverChains)` — 1081–22091, 769 методов; `main()` — 22092.
- Карта: 13 домов, строк `home` — core 57, chains 33, runner 57, timing 25, dialog 50, conductor 56, dispatch 181,
  s0 103, sources 36, stages 230, gates 64, machine 129, story_run 2. Ранги: `layers` в шапке карты. Правило карты:
  модуль `driver_<x>.py`, класс `Driver<Suffix>`, миксины друг друга не импортируют, ребро вверх — только из
  `exceptions` (14 строк, только убывают). `test_driver_layers.py` (L1–L10) зелёный: 54/54 на `main` a4329e9.
- Уже есть: `driver_chains.py` (миксин-основа, t-2147 часть A — образец переноса), `driver_timing.py` (НЕ миксин,
  читатель времени, импортируется лениво), `driver_journal.py` (`not_driver`).
- Общее состояние живёт на экземпляре (`self.state` 410 упоминаний, `self.py(` 116, обёртки контроллера 347);
  `global` нет. Около 520 ленивых импортов внутри методов едут вместе с телами.
- Помощники, которых зовут почти все области: `closed_question`, `held_question`, `site_seam_person`, `no_move`,
  `run_role`, `finish`, `handoff`, `resume_role`. `take_answer` (21246) раздаёт ответы обработчикам `_answer_*`,
  живущим в областях стадий.
- Импортёры: 146 тестовых файлов (`import story_run`), из не-тестов — только `experiments/measurers/
  conductor_families.py` (`story_run.KNOWN_REFUSALS`). Тесты читают через модуль: `EXIT_*`, `KNOWN_REFUSALS`,
  `match_known`, `route_known`, `question_body_sha`, `finding_key`, `gate_refusal`, `last_json_line`, `_answer_note`,
  `_read_json`, `main`, `Driver`, `Refusal`, `Person`, `Stop`.
- Подмена атрибутов МОДУЛЯ (ломается, когда код уезжает в другой модуль): `test_silent_passes.py` (`story_run._now`,
  `story_run.json_record`), `test_story_run_words.py:286` (`story_run.open`), `test_story_run_wait.py:93,110`
  (`story_run.time`), `test_s7_investigation_replay.py:124` (`setattr(story_run.Driver, …)`), `test_refuse_case.py`.
  Подмена через псевдоним (`sr.x = …`) не искалась — спека называет команду поиска.
- Тесты, читающие ТЕКСТ `story_run.py`: 21 файл; 12 в `keep` (`test_conductor_doors`, `test_driver_stop_record`,
  `test_gate_brief_and_retro`, `test_knowledge_notice`, `test_story_run_refusals`, `test_story_run_s0`,
  `test_story_run_s6`, `test_story_run_words`, `test_story_run_stand_identity`, `test_walk_lanes_parallel`,
  `test_window_record`, `test_words_doors`), 9 в карантине. Полная перепись — строки `source_readers` и
  `source_mentions` карты (L8).
- Носители, привязанные к имени файла, функции или номеру строки: `references/gate-registry.json` (4 строки
  `{file, function}`), `references/null-outcomes.json` (`story_run.py::stage_S5` и ещё 3), `references/
  block-names.json` (7, `story_run:Driver.<fn>`), `references/artifact-writers.json:195`, `field-producers.json`,
  `place-answers.json`, `question-vocabulary.json` (проза `story_run.<fn>`); `scripts/audit_factory.py` (таблицы
  `('story_run.py','Driver.<fn>',…)`, уже читает `story_run.py` + `driver_*.py`); `tests/fixtures/
  judgment-census.json` (21 строка `{file, function}`, храповик); `tests/fixtures/env-facts-baseline.json` (номера
  строк); `design/factory-rules-debt.md:84`, `design/architecture.md:249` (номера строк); `tests/test-layers.json`
  (59 упоминаний, в том числе списки `covers` — по ним `scenario_walk.py --witness-for` находит свидетеля);
  `tools/lint-baseline.json` (ключ — путь), `tools/dup-baseline.json` (отпечаток кода; перенос даёт GONE, снимается
  `--update`); `tools/crap_report.py` (`GOLDEN_FILE = "story_run.py"`), `tests/driver_golden.py` (`story_run_sha256`;
  данные golden в дереве отсутствуют, `test_driver_golden.py` в карантине); `tools/piles.py` (разбор
  `story_run.py (f1, f2)` в `owns`); `docs/SIBLING_MAP.md:122,126`; `references/release-fingerprint.json`
  (пересобирается при релизе). Команда запуска — `INSTALL.md:27`, `docs/RUNBOOK.md:277,320`,
  `experiments/measurers/prepare_copy.py:203`.
- Свидетель узла, пишущего `story_run.py` (`plans/builder-rules.md` 7b–7d): `scenario_walk.py --witness-for <owns>`,
  `test_story_run_words.py`, `test_driver_layers.py`; большие файлы и канон — CI.

### controller.py (9 951 строка)

- 52–1591 — словарь стадий, статусы, чистые помощники (в них нет ссылок на `Controller`); 1592–1993 —
  `projection(events)`; `class Controller` 2018–9093 (227 методов; `validate` 5311–6055, 745 строк); 9094–9951 —
  кортежи операций, исполнитель решения гейта (9236–9564), `--brief`, `main` (9730).
- Состояние экземпляра — только `self.store` и `self._items_memo`. В классе около 27 вызовов `Controller.<static>`
  по имени класса.
- Импортёры: 187 файлов (37 не-тестовых, `story_run` — 45 мест); снаружи берут `Controller`, статусы, `s5_part_of`,
  `lane_keys`, `manual_blocks`, `walk_lanes`, `stop_after` и другие; `story_run` лезет в приватные
  `_dispatch_starts`, `_pinned_links`, `_lane_beside_running`. Взаимные ленивые импорты с `acceptance`, `s5_plan`,
  `window_record`, `planning_contract`, `stage_guard`, `gate_preflight`.
- Подмена атрибутов модуля: `controller.atomic_json`, `controller_module.validate_record`, `Controller = factory`.
- Привязки к имени файла: `refusal_registry.py` (`"file": "controller.py"`, 8 строк), `runtime_paths.py:225`,
  `tools/controller-blocks-gen.py:22` (читает ОДИН файл, пишет `design/controller-blocks.md`), 8 тестов читают текст,
  около 116 строк текстов-дверей в 26 скриптах печатают `controller.py --operation …`.
- Карты слоёв для контроллера нет. Тестовый файл-фикстура: `test_controller_state.py` — его импортируют около 50
  тестов как `BASE`.

### Остальные исходники (открытые узлы пачек, называющие файл / кучки)

`gate_preflight.py` 6 097 строк — 29 / 7; `gate_brief.py` 5 117 — 27 / 6; `report_facts.py` 4 894 — 21 / 5;
`story_step.py` 3 388 — 20 / 4; `probe_by_code.py` 8 347 — 17 / 5; `hooklib.py` 2 789 — 15 / 5;
`stage_guard.py` 3 523 — 14 / 5. Для сравнения `story_run.py` — 67.

- `gate_preflight.py`: `class Rehearsal` 1258–5753, около 165 методов, по методу `check_*` на проверку; 70 импортёров.
  Ветка `origin/held/tr2-9` (не в `main`) правит файл на 19 строк.
- `gate_brief.py`: 203 функции верхнего уровня; швы — гейт A / гейт B и темы (маркеры 642, 1033, 1285, 3231, 3614,
  3968).
- `report_facts.py`: 12 маркеров секций; `story_step.py`: по подкомандам (start, materialize, bind, finish, decide,
  pause, resume, card, where); `probe_by_code.py`: 23 маркера, после `main` (3976) ещё 4 350 строк.
- `hooklib.py`: библиотека без CLI, 327 импортирующих файлов — фасад обязателен; швы — корни проекта и стори,
  сканер слов шелла (1111–1694), тела heredoc, сигналы, согласованность версий.
- `stage_guard.py`: правила хука 134–1859, формы команд 1860–2895, CLI со встроенным `selftest` 3043–3503.
- Размерных лимитов на `.py` в `selftest.py --limits` нет. Перепись суждений и база линтера привязаны к имени файла.

### Тесты (`scripts/tests/`, `test-layers.json`: keep 322, quarantine 432, pin_holds 4)

- Файл вне разделов красит канон (`unlisted:`); строка `keep` уходит только через `tools/test_quarantine.py
  drop-keep`. Реестры с именами тестовых файлов: `test-layers.json` (ключи и 223 строки `covers`),
  `scripts/slow_tests.json` (122 файла, веса шардов), `selftest.py` `TEST_TIMEOUTS` (16) и `CONTRACT_TESTS` (3),
  `references/gate-registry.json` (28), `references/stage-joints.json` (4), `design/state-exits.md` (137),
  `.github/workflows/forge-check.yml:173`.
- Оставленные файлы дольше 100 с в CI (`slow_tests.json`, замер 11.11): `probe_by_code_alternative` 337.0
  (619 строк — не случай резки, отдельный разбор), `infra_failure` 320.6, `story_run_refusals` 308.2,
  `story_run_s0` 286.3, `no_move_seam` 283.0, `story_run_stand_identity` 274.3, `story_run_s6` 219.4,
  `story_run_freshness` 159.0, `words_doors` 134.3, `story_run_loop_b` 119.0, `handoff_values` 116.4,
  `controller_rework` 107.0, `probe_by_code` 105.8, `grounding_table` 105.8, `probe_by_code_languages` 103.7.
  Три `test_scenario_*` (200–400 с) — заглушки ходока, резать нечего.
- Большие, но быстрые оставленные файлы разрезаемых исходников: `test_gate_preflight.py` 5 460 строк,
  `test_report_facts.py` 4 970, `test_gate_brief_and_retro.py` 3 545, `test_stage_guard.py` 2 236,
  `test_controller_state.py` 2 423 (фикстура для ~50 файлов).
- Прецеденты: `test_story_step.py` — заглушка на 60 строк после резки по командам, помощники в
  `story_step_common.py`; `tools/test_piles*.py` — по командам, «каждый файл < 60 с».
- Открытые записи про резку тестов: B-460 / PC1-5 (`test_story_run_freshness.py` по сценариям), B-344, B-381 / PC1-4
  (`test_words_doors.py`), SC2-34 (`test_red_window.py`, сейчас 85.8 с), B-214 (`infra_failure`, `story_run_s0`).
- Резка тестового файла общее время не уменьшает: она даёт части, которые билдер гоняет у себя до минуты, и ровнее
  шарды. Время съедает мир драйвера на каждую проверку (`docs/TESTING.md`: один мир на файл).

### Окно

Эксперимент слит в `main` (`origin/experiment-merge` — предок `main`). В работе одна пачка `github-move/3` (dev1),
`story_run.py` и `controller.py` она не называет. Правила про интеграцию большого переноса при живых ветках нет
(D-0048 — только про непересекающиеся функции).

## Спеки (три дизайнера параллельно)

| Спека | Тема | Файл |
|---|---|---|
| A | Инструмент переноса, протокол общих реестров, фазы 0–1: `story_run.py` по карте | `docs/tasks/specs/td-11a-driver-split.md` |
| B | Карты и границы: `controller.py` и семь исходников первой волны | `docs/tasks/specs/td-11b-source-maps.md` |
| C | Резка тестовых файлов вне карантина | `docs/tasks/specs/td-11c-test-split.md` |

Общий стык спек: формат карты файла — массив `names` строк `{name, kind, home}` по образцу `driver-layers.json`;
спека A владеет инструментом и протоколом реестров, B и C на них ссылаются и не определяют своих.

## Инварианты и правила, которые перенос обязан назвать и сохранить

AR-13 (читатель факта один), AR-14 (один писатель артефакта), AR-15, AR-19 (близнецы меняются вместе), AR-20
(храповики только убывают: `exceptions` карты, перепись суждений, базы линтера и клонов), AR-22 (производитель и
читатели — одним коммитом), AR-29; FR-30, FR-31, FR-32, FR-37 (путь в тексте — путь в коде), FR-54; P12, P27, P31.
Поведение не меняется: любой дифф поведения — дефект узла.
