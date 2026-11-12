# Навигация устарела: указатели в документах пережили объекты, на которые ссылались (переезд на GitHub, перепись `CLAUDE.md`, резка `story_run.py`)

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 6), записал builder t-093 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс: «указатель (путь, номер строки, ссылка на блок, ключ поиска) переживает изменение объекта, на который указывал: перенос
репозитория, перепись файла, резку модуля, и ни один шаг изменения не выметает носителей указателя». Каждый экземпляр — отдельный
дефект; вместе они — повторяющийся класс первой же калибровки (аналог в старой: `20261014-kalibrovka-1-...`).

Экземпляры (свидетель — улики p2/p3/p4, пути проверены в тех же частях):
1. `CURRENT_CONTEXT.md` не менялся с импорта (`git log -- CURRENT_CONTEXT.md` → только `9ac00f0`), обещает `continues_from: t-NNNN`, которого
   в журнале нет (строка 1 журнала без поля, номера с `t-001`); ничего из окна (TD-11, PC2, канон) в нём нет (p3, проверка 26).
2. `PROJECT.md:10` ссылается на «блок Supervised-Delegation в `CLAUDE.md`»: после `94702be` блока нет (p3, 26).
3. `.claude/skills/session-handoff/SKILL.md:20` читает `logs/routing-log.jsonl` — файла нет; ту же ссылку несут `tools/forge_metrics.py`
   (карта, p1, проверка 12) и протокол калибровки 13(l) (p2).
4. `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: проверка 18(e) «more than 4 WRITING workers» против `PARALLEL_CAP = 6`
   (`tools/dispatch_gate.py:1512`, D-0054); снимок хуков (строки 541–551) — 12 против 13 в `.claude/settings.json` (нет `agent_budget`,
   `handoff_gate`, `compact_snapshot`); `handoff_gate` нигде не назван; проверка 38 ищет `waiver.py` в `scripts/story_run.py`, после резки
   (32858bd) — в `scripts/driver_*.py` (p3, 19; p4, 38); снимок README (хуки pre-commit/commit-msg, p3, 26).
5. `docs/SIBLING_MAP.md` — около 10 мёртвых путей: `.gitlab-ci.yml`, `tools/test_ci_layout.py` (строка 518), `experiments/driver-golden*` и
   `freeze_package.sh` (166), `logs/routing-log.jsonl` (165), `skills/qa-story/index.yaml` (135, есть `handoffs/index.yaml`),
   `references/controller-paths.md` (217, есть `design/controller-paths.md`), путь находки `onboarding-hooks/...` (255, лежит в
   `onboarding-forge/`) (p1, 12); карта выросла 589 → 637 строк.
6. Решения: D-0045 нет ни в `DECISIONS.md`, ни в `docs/DECISIONS_ARCHIVE.md` (`grep` с контролем `D-0046`: 2 и 4 совпадения);
   D-0046 в архиве записан дважды (строки 55 и 82) (p1, 12).

## Что именно менять

Направление выбрано: правятся экземпляры; ПРОВЕРКУ мёртвых путей карты делает узел F6-10 (`../../onboarding-forge/batch-1-onboarding-roles-forge.md`,
`piles.py check` читает пути карты), этот узел её не повторяет, а после неё не должен оставлять красного.

1. `CURRENT_CONTEXT.md` (только состояние `main`, ≤ 10 КБ, `PROJECT.md` п. «Общие файлы»): переписать по `git log` окна; убрать обещание
   `continues_from`. Свидетель: `wc -c CURRENT_CONTEXT.md` ≤ 10240; ключ-прогон документа.
2. `.claude/skills/session-handoff/SKILL.md:20`: вместо `logs/routing-log.jsonl` — `logs/journal/<dev>.jsonl` (слаг из
   `python tools/journal_keys.py where`). `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: 18(e) «4» → «6 (D-0054)»; снимок хуков 541–551 → 13 строк
   по факту `.claude/settings.json`, `handoff_gate` назван; проверка 38: ключ поиска `scripts/driver_*.py`; 13(l): носитель
   `logs/journal/<dev>.jsonl`.
3. `docs/SIBLING_MAP.md`: убрать/исправить шесть названных в п. 5 путей (строки 135, 165, 166, 217, 255, 518); путь, у которого объекта нет и
   замены нет, удаляется со строкой (строка карты без объекта — дефект самой карты, правило обслуживания карты в её шапке). Правка
   `PROJECT.md:10` — Lead (файл правил).
4. `docs/DECISIONS_ARCHIVE.md`: убрать дубль D-0046 (оставить полную запись). D-0045 — выдача номера решает Lead (`git log -S"D-0045"`);
   до ответа строка не пишется (развилка).
5. Тест/свидетель: ключ-прогон документов (правило 11 `CLAUDE.md`, DOC-DISPATCH WITNESS: ключи из DoD заранее, скрипт в отчёте,
   негативный контроль), плюс `python -B tools/piles.py check --all` и `python -B tools/forge_metrics.py --check --base origin/main`.

Исполнитель: builder (узел-документ; `PROJECT.md:10`, D-0045 — Lead). Пункт 3 — после слияния проверки путей карты (F6-10), если её возьмут первой.

## Связи

`../../onboarding-forge/findings/20261014-kalibrovka-1-slepye-detektory-i-ustarevshaya-navigaciya.md` (F6-10: тот же класс «навигация»,
другие экземпляры, проверка путей карты — там); `20261030-strochki-sibling-map-os-7-klyuch-pamyati-i-stroka-120-zhdut-gejta-lead.md` (F6-53,
тот же файл карты); `20261027-sibling-map-dolgi-osey-posle-relisa-0-10-3.md` (F6-41).

Принципы и правила: P31; AR-19, AR-22; FR-37, FR-54.

Решение владельца нужно: нет (D-0045 решает Lead).

<!-- id выдаёт интегратор при сборке пачки. -->
