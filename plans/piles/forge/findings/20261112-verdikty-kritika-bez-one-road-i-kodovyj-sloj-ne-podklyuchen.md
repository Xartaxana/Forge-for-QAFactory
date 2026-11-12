# Вердикты критика без строки `ONE ROAD:`, а кодовый слой проверки «одной дороги» не подключён: нет файла baseline

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 10), записал builder t-093 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс: «детектор зарегистрирован (D-0063, критик-правило 19, вопрос 12, ось 34), но стоит выключенным: ни код-слой (`tools/language_sites.py`),
ни проверка текста вердикта не на пути исполнения, так что правило P31 держится на памяти критика».

Свидетель (часть p4, `docs/tasks/specs/reports/calibration-20261112-p4.md`, проверка 42):
- (b) из 50 файлов `docs/tasks/specs/reviews/` строку `ONE ROAD` несут 14, не несут 36; после спеки TR2-15 (t-2065) без строки: t-2076, t-2153,
  t-2227, t-2263, t-2306, t-2331 и пять план-критиков `20261110-*`; из своих сессий репозитория — `t-013-critic-on-plan`, `t-042-critic-on-plan`,
  `td-11-plan-critic`, `td-15-plan-critic`, `td-5-plan-critic`, `td-15-cart-1-reds`, `td-15-local-1-0108-reds` (11 после t-2065 — п. 10 записи Lead).
  Вопрос 12 — `docs/tasks/critic-diff-brief.md:77`; правило 19 — `.claude/agents/critic.md:154`. Датой считается дата прихода (слияние
  2026-11-11), не дата написания (p4, «ambiguous»).
- (d) `python -B tools/language_sites.py --totals` → «cannot judge -- tools/language-sites-baseline.json is missing (W3)»; файла нет
  (`ls`); `docs/SIBLING_MAP.md:586` называет слой INERT; модуль-докстринг: «INERT until wired (node N3): no hook, no CI line calls it».
- (c) остатки класса: находка `20261106-odna-doroga-proby-na-vse-yazyki.md` одна; ключевая фраза проверки в находках нигде.

## Что именно менять

Направление выбрано: подключить имеющееся (AR-15: один выживший, провод везде), не писать второй детектор.

1. `tools/language-sites-baseline.json`: создать baseline командой модуля (`python -B tools/language_sites.py --help` назовёт режим
   записи; проверить по коду, имя флага не угадывать), закоммитить отдельным коммитом с `architecture:`/`axes:` блоком (механизм, правило 10).
   Свидетель: `python -B tools/language_sites.py --totals` — вместо «cannot judge» печатает итоги; `python -m pytest tools/test_language_sites.py -q`.
2. Провод: строка в `.github/workflows/forge-check.yml` и в `.githooks/pre-commit` (режим `--staged`, если он есть в модуле) по образцу
   `tools/lint_ratchet.py --check`; красный на новый сайт ветвления по языку без записи в baseline. Тест провода — существующий
   `tools/test_wiring_check.py` (расширить: строка обязана быть на обоих путях).
3. Вердикты: `tools/handoff_gate.py` не трогать; вместо него — проверка формы вердикта критика в калибровке: `tools/calibration_counts.py`
   печатает список файлов `docs/tasks/specs/reviews/*.md` новее t-2065 без литерала `ONE ROAD:` (данные: `grep`-подобный счёт, смысл строки
   судит Lead). Тест: `tools/test_calibration_counts.py`, таблица: файл со строкой / без строки / старый файл (не считается).

Края: baseline пуст или отсутствует — слой молчит с «cannot judge» и это строка отчёта, не ноль (FR-41, FR-59); дата вердикта — дата
первого коммита файла (`git log --diff-filter=A`), не дата слияния.

Исполнитель: designer → builder → critic (механизм).

## Связи

`20261106-odna-doroga-proby-na-vse-yazyki.md` (класс P31); `20261111-svidetel-dlya-putej-vne-paketa-odin-put.md` (FG7-15, «два пути для одного
действия»); D-0063; ось 34 карты. Детектор: калибровка проверка 42.

Принципы и правила: P31, P27; AR-15, AR-20; FR-17.

Решение владельца нужно: нет.

<!-- id выдаёт интегратор при сборке пачки. -->
