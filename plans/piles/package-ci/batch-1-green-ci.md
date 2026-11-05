# Пакет: тесты, Linux, CI — пачка 1: полный прогон зелёный на Linux и на второй Windows-машине, тесты стабильны и в лимите

кучка: `package-ci` | статус: закрыта | взял: — | ветка: — | MR: `855d4e5c` | стенд: не нужен (CI) | приоритет: П1 | issue: https://git.example.com/dev1/yml-text-factory/-/issues/9

очередь: conductor/1 → package-ci/1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, `package-full`
(ночной полный прогон) зелёный на образе CI, а полный набор проверок на второй Windows-машине пройден или причина
каждого красного названа строкой в «Остатках».

Решения владельца: слово 03.10 о разборе красных файлов Linux «после релиза» (строка `plans/BACKLOG.md:251`); D-0030 (места тестов — слово проекта, находка `findings/B-415-d-0030-mesta-testov-v-repozitorii-prilozheniya.md`, в пачку не входит).
Порядок по общим файлам: `selftest.py`: PC1-1 → PC1-4 → PC1-5; `install_smoke.py`: PC1-1 → PC1-2; `stage_done.py`: PC1-2 → PC1-3.
`controller.py` (PC1-3) — после узлов C1-5…C1-7 `conductor/1`. Файлы `controller.py`, `stage_done.py`, `manifest_put.py` — общие с `driver-controller/1` (DC1-1, DC1-2): строки `очередь:` ставит интегратор при `take` второй из двух пачек.
Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`, прочие — от корня репозитория.
Скоуп свидетеля: PC1-1 — `package-fast` и красные файлы из списка скаута; PC1-2 — `install_smoke.py` на машине с `autocrlf=true`
(или образ CI с тем же флагом), `test_ticket_light.py`; PC1-3 — `test_obligation_join.py` под 4 воркерами,
`test_event_store.py`; PC1-4 и PC1-5 — разрезанный файл идёт в лимите на образе CI (`python:3.12`), строка в
`TEST_TIMEOUTS`; PC1-6 — `test_audit_rules.py`; всем — `python -B scripts/selftest.py --limits --lang`.
Полный канон — интегратор при слиянии, CI `package-fast`.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); строки `plans/BACKLOG.md` узла; `plans/builder-rules.md`;
`PROJECT.md` «Как принимается изменение пакета» п. 2; FR-31, FR-32, FR-59; вернуть спеку в `docs/tasks/specs/t-nnn-pc1-n.md`
с развилками наверх; что именно красно сейчас — по свежему прогону CI, не по цифрам строк (они датированы 03–09.10).

## Бриф

Что сделать: свести красное на Linux и второй Windows-машине к списку причин и починить причины (POSIX-пути в гейтах,
Windows-пути в фикстурах, CRLF); убрать гонку замены файла и вложенный замок; разрезать самые долгие файлы тестов так,
чтобы каждый шёл в лимите и под нагрузкой, и снять временный потолок 600 с; привести реестр гейтов и тексты к коду.
НЕ делать: универсальность форм (трекер, VCS, монорепо — находки «Содержания» вне пачки 1); правки логики стадий
ради скорости тестов; перенос `SLOW_TESTS` без прогона на образе CI.
Первые 10 минут: (1) в карточке прочитать «Бриф пачки 1», «Дороги», «Вопросы владельцу»; в этом файле — преамбулу и этот «Бриф».
(2) Открыть `plans/PILES.md`, найти активные пачки, пишущие те же файлы; если строки `очередь:` нет в обеих — попросить интегратора дописать.
(3) Интегратор на `main` запускает `python tools/piles.py take package-ci 1 --who <кто>`, коммитит и пушит; взявший режет ветку от `origin/main` по напечатанной команде.
(4) Первая строка «Хода»; первый диспатч — скаут по «Дорогам» с вопросом «какие файлы красны на свежем прогоне CI и живы ли номера строк и пункты "проверить по коду"».

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| PC1-1 | П1 | B-307, B-301, B-302: красные файлы первых прогонов на Linux сведены к причинам и починены (гейты не узнают POSIX-пути, фикстуры с Windows-путями); `allow_failure` снимается там, где причина устранена | designer → builder → critic | `.gitlab-ci.yml`, `scripts/selftest.py`, `scripts/install_smoke.py` | — | принято: e2c3f507 |
| PC1-2 | П1 | B-386, B-446, B-448: вторая Windows-машина — `.gitattributes` с `text eol=lf` (план находки `findings/B-409-gitattributes-u-paketa-net-svezhiy-klon.md`), `compare_trees` не говорит «одинаково» при `true`/`1`, ASCII-запасные варианты кодировки консоли | designer → builder → critic | `.gitattributes`, `scripts/install_smoke.py`, `scripts/onboard_apply.py`, `scripts/project_gitignore.py`, `scripts/stage_done.py`, `scripts/tests/test_ticket_light.py` | PC1-1 | закрыта: перенесено 01.11.2026 → onboarding-forge/1 |
| PC1-3 | П1 | B-326, B-320, B-333, B-318: гонка замены файла (M8) и вложенный замок журнала; `test_obligation_join` под нагрузкой — причина и печать `report["left"]` | designer → critic на план → builder → critic | `scripts/stand_lease.py`, `scripts/stage_done.py`, `scripts/manifest_put.py`, `scripts/controller.py`, `scripts/tests/test_obligation_join.py` | PC1-2 | закрыта: перенесено 01.11.2026 → onboarding-forge/1 |
| PC1-4 | П2 | B-344, B-381: самые долгие файлы семейства `test_story_run_*.py` (файла `test_story_run.py` уже нет — какие дольше лимита, по свежему прогону CI) и `test_words_doors` идут в лимите; строка `test_words_doors` в `TEST_TIMEOUTS` | designer → builder → critic | `scripts/selftest.py`, `scripts/tests/test_words_doors.py` | PC1-1 | закрыта: перенесено 01.11.2026 → onboarding-forge/1 |
| PC1-5 | П2 | B-460, B-297: `test_story_run_freshness` разрезан по сценариям, `test_story_run_s0` и `test_story_run_gate_repair` в лимите; временный потолок 600 с снят | designer → builder → critic | `scripts/selftest.py`, `scripts/tests/test_story_run_freshness.py`, `scripts/tests/test_story_run_s0.py`, `scripts/tests/test_story_run_gate_repair.py` | PC1-4 | закрыта: перенесено 01.11.2026 → onboarding-forge/1 |
| PC1-6 | П2 | B-368, B-403: строка `red_sandbox.verify` в реестре гейтов; тексты не называют несуществующую `story_run.ticket_freshness` (`phases/s8.md` §2b и три R11-текста — имена проверить по коду) | designer → builder → critic | `references/gate-registry.json`, `skills/qa-story/phases/s8.md` | — | закрыта: перенесено 01.11.2026 → words-gates/1 |
| PC1-7 | П2 | `test_stand_lease` «a free stand is taken without waiting» краснеет под нагрузкой: `waited_s == 0` утверждает стенные часы, не факт ожидания — кейс проверяет `queued_behind is None` и отсутствие `_sleep`, `waited_s` остаётся измерением (`findings/20261021-test-stand-lease-waited-s-pod-nagruzkoj-fr-31.md`; FR-31, сосед PC1-3) | builder | `scripts/stand_lease.py` (`--selftest`), `scripts/tests/test_stand_lease.py` | PC1-3 (общий файл `stand_lease.py`: PC1-3 → PC1-7) | закрыта: перенесено 01.11.2026 → onboarding-forge/1 |
| PC1-8 | П2 | `test_brief_pack_roles` K9 и K6 зелёные: скрипт `branch_accounting.py` из устава `qa-requirements-tester.md:48`/`:78` на карточке роли (или убран из устава, P14); хэш `## Commands` у `qa-automator` перепинен после чтения диффа раздела, с комментарием-дверью (`findings/20261030-test-brief-pack-roles-k6-k9-krasnye-na-baze-reliza.md`; билдер GW1-16 и критик S1c 0.10.7; P14; FR-34, FR-56, FR-15; AR-8, AR-11) | builder → critic | `scripts/brief_pack.py` (карточка роли), `agents/qa-requirements-tester.md`, `scripts/tests/test_brief_pack_roles.py` | — | принято: 5f105e1e |
| PC1-9 | П3 | `test_triage_control` A-K9: перепись слов `CASE_DEFECT`/`ASSERT_STRICTER` считает код (`ast`), не docstring, либо список содержит `traceability.py` и `s7_pretriage.py` с причиной; контроль со старым словом обновлён (`findings/20261030-a-k9-test-triage-control-perechen-ne-znaet-traceability-i-s7-pretriage.md`; билдер HF8-19 N1b, критик S5b rest 0.10.7; FR-34, FR-28; AR-19) | builder | `scripts/tests/test_triage_control.py` | — | принято: 945a26da |
| PC1-10 | П2 | `lint_ratchet.py --check` возвращается к `0 new`: 21 новая находка (неиспользуемые импорты, f-строки без подстановок) убраны одним проходом; `lint_ratchet --check` по своим файлам входит в DoD узла, добавляющего тест (`findings/20261030-lint-ratchet-check-21-novyj-na-baze-reliza.md`; фикс-раунд SC2-37 0.10.7, замер на базе; FR-28, FR-32; AR-20) | builder | список файлов в находке, `tools/lint_ratchet.py` (только запуск; `--update` не вызывать) | PC1-11 (`project_decisions.py`) | принято: 391120e7 |
| PC1-11 | П2 | Два красных на базе 0.10.7: `test_read_json` G5 (убрать строку KEPT `hooklib.load_config`; `manual_evidence._read_json` на `hooklib.read_json(kind=dict)` или строка KEPT с причиной) и `test_project_decisions_change_request` P21 (`project_decisions.main` 70 строк → не больше 60) (`findings/20261030-test-read-json-380-382-i-p21-main-bolshe-60-strok-krasnye-na-baze.md`; билдер OH3-23, фикс-раунд HF7 0.10.7; FR-34, FR-54; AR-13) | builder → critic | `scripts/tests/test_read_json.py`, `scripts/manual_evidence.py`, `scripts/project_decisions.py`, `scripts/tests/test_project_decisions_change_request.py` | — | принято: 391120e7 |
| PC1-12 | П2 | **Находка 01.11.2026 (долг координатора релизов 0.10.7/0.10.8).** `test_run_suite_mine`: пины времени фаз по wall-clock (`build_s >= 0.35`, `collect_s >= 0.3`) заменить ступенчатыми часами, 20 прогонов подряд без падения (`findings/20261101-test-run-suite-mine-pin-vremeni-fazy-flake.md`; FR-31, FR-28) | builder | `scripts/tests/test_run_suite_mine.py` | — | закрыта: перенесено 01.11.2026 → onboarding-forge/2 |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → words-gates/1, onboarding-forge/1, onboarding-forge/2

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Ночной `package-full` зелёный на образе CI после PC1-1…PC1-5 | CI (`python:3.12`) | интегратор | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Полный набор проверок пройден на второй Windows-машине (Python 3.13.5, `autocrlf=true`) | вторая Windows-машина | — | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пункт — КАЖДАЯ непустая строка раздела вне комментария: абзац, заголовок и строка внутри блока кода тоже пункты. Одно
исключение: строка с отступом в 2 и более пробелов, которая сама не начинает маркер (`-`, `*`, `•`, `1.`), продолжает пункт
выше, и ключи читаются по всему пункту. Подпункт с маркером, строка с табуляцией и строка с отступом без пункта выше —
пункты сами по себе. Скрыть строку может только комментарий; комментарий без закрытия — отказ.
Цель `перенос:` должна существовать: файл — в дереве и в индексе (`git add` до `close`), `пачка N` — строка карточки этой
кучки, не эта пачка и не закрытая. `подтвердил` пишет человек, не агент сам. Пустой раздел — можно закрывать.
-->
