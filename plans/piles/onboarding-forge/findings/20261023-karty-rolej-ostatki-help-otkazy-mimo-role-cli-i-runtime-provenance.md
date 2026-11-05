# Карты команд ролей: `critic_rollcall.py --help` читается как файл находок, часть отказов идёт мимо `role_cli.refuse` и не цитирует карточку, оговорка `runtime_provenance`

id: — | кучка: `onboarding-forge` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Остатки узла HF1-12 (семь карточек `references/role-commands.json` приведены к парсерам; тест кормит каждую из 14 карточек её же примером).
Все — об одном: роль получает от команды не то, что карточка обещает, или отказ без карточки. Чинятся одним узлом в карточках и `role_cli`.

(1) `critic_rollcall.py --help` читается как имя файла находок и отвечает `REJECT - no such findings file: --help`. Поэтому ключ «карточка равна `--help`
слово в слово» покрывает 13 скриптов из 14. Кандидат: ветка `--help` в `critic_rollcall.main`.

(2) Отказы, идущие мимо `role_cli.refuse` и потому не цитирующие карточку: argparse `parser.error` в `manual_evidence.py export` (`export requires --output`),
`artifact_producer.py` (`--kind is required`), `plan_row.py` (`--task`); `external_writes.record_result` печатает `REJECT: --external-id is required` и
`REJECT: a published case receipt needs --remote-revision` без карточки. Тест называет флаг в каждом отказе и карточку не требует. Класс FR-1 / AR-9;
одно исправление — общий `_Parser.error`, как в `manual_capture.py`. Рядом: отказ `artifact_producer.py` «existing artifact requires its exact previous
sha256» не называет `--expected-hash`, хотя карточка называет.

(3) Оговорка q1-13c дайджеста t-063: карточка `execution_fingerprint.py` говорит, что `runtime_provenance` — «the interpreter identity the runner recorded», а
`build()` требует проверенную запись идентичности стенда; пример теста — именно такая запись. Не исправлено (вне спеки HF1-12; названо в отчёте t-064 как оговорка, оставленная нецелью).

Что сделать: (1) `--help` у `critic_rollcall`; (2) общий разбор ошибок разбора аргументов с цитатой карточки и текст отказа
`artifact_producer` с `--expected-hash`; (3) строка карточки о `runtime_provenance` сверена с `build()` и тестом (карточка = парсер). Тест: каждая из 14
карточек отвечает `--help` тем же текстом; каждый отказ ошибки аргументов содержит цитату карточки (отрицательный контроль — отказ без цитаты).

Свидетель: `docs/tasks/handoffs/t-064-hf1-12.md`, «Findings and siblings (not fixed, out of owns)», п. 1–4; `docs/tasks/specs/reports/t-063-hf1-11-sweeps.md`
(строка q1-13c).

Принципы и правила: P15, FR-1, FR-11, FR-14, AR-9, AR-13.

Решение владельца нужно: нет.
