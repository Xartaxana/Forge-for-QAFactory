# Строитель «мира» красной песочницы скопирован в `test_red_sandbox_probe.py` и `test_red_sandbox_diagnostic.py` (аналог K1a, B1 критика темы K10)

id: — | кучка: `live-run-fvf` | от: критик темы «K10 pay-down» (`docs/tasks/specs/reviews/20261114-k10-paydown-topic-critic.md`, B1: «the K1a builder's analog has no carrier», «Queue lines» 3); слово владельца 14.11.2026: «только B1, остальное завести узлами» | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **копия помощника теста рядом с оригиналом (FR-54, AR-15)**. Билдер K1a скопировал строитель мира в `ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py` из `test_red_sandbox_diagnostic.py`; носителя у замечания не было (grep по `plans/piles`: 0; на `world builder` и `test_red_sandbox_diagnostic` — только находка EP4-2 про другой класс).
Оба файла медленные («судит канон пачки»).

## Что именно менять

1. Один общий помощник строителя мира в тестовом пакете: `ai-packages/qa-factory/scripts/tests/red_sandbox_world.py` (или существующее общее место помощников, если оно есть; выбор по месту, одно имя в отчёте).
2. `test_red_sandbox_probe.py` и `test_red_sandbox_diagnostic.py` берут мир оттуда; собственных копий в файлах не остаётся.
3. Тест: правки поведения нет; свидетель — числа проверок обоих файлов до и после совпадают (оба файла медленные — «судит канон пачки», билдер их локально не гоняет, свидетель — `scenario_walk.py --witness-for` на новый помощник и сбор файлов без запуска медленных).

Принципы и правила: FR-54; AR-15; P12.

Решение владельцу нужно: нет.
