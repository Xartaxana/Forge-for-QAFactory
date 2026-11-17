# Ход ходока после ответа длится одну границу драйвера: пять маршрутов и шесть стыков стоят «только живьём» без нужды в живом прогоне

id: — | кучка: `live-run-fvf` | от: Lead, 17.11.2026 (вердикт t-1077, находка F5; отчёт t-1037 «Walker defects noticed», пункты 3 и 2) | приоритет: П1 | кандидат наверх: нет

## Что не так

Класс фабрики: **предел ходока выдан за причину «нужен живой прогон» (`live_only` должно значить «нужен живой»), и у строк нет очереди, из которой они выйдут, когда предел снят (AR-25: у записанного состояния есть выход; AR-28: неизвестное не проходит)**.

Факты (вердикт t-1077, F5):

- Дефект 3 ходока: ход после ответа — одна граница драйвера (`--max-boundaries 1`); он кончается раньше, чем работает роль S2, поэтому отказ по результату роли не читается никогда.
- Дефект 2 ходока: номера стыков (joint ids) не печатаются, и строка выхода не связана с запросом, который её породил.
- От этого пять маршрутов (`marked_repair`, `form_vocabulary`, `handover_form`, `missing_output`, `handoff_form`) и стык `exit_gate:digest` стоят `live_only` с измеренной причиной «the walker's post-answer turn is one driver boundary»; остальные пять стыков `exit_gate` идут той же дорогой (оценка).
- Поиск по `plans/piles/*/findings` и файлам пачек на «post-answer», «max-boundaries 1», «one driver boundary» дал 0 попаданий (контроль «dry-priced|walker» — 5): очереди у дефектов не было.

## Что именно менять

1. Ходок получает более длинное окно после ответа: число границ драйвера за ход после ответа задаётся данными строки (по умолчанию — как сейчас), так, чтобы роль S2 отработала и её результат был прочитан. Файлы: `ai-packages/qa-factory/scripts/tests/dry_world.py` (`run_exit_row`, вызов с `--max-boundaries 1`), `ai-packages/qa-factory/scripts/tests/dry_exits.py` (грамматика строки).
2. Ходок печатает номера стыков для строки выхода (дефект 2): `dry_world.py`, `dry_exits.py`.
3. Затем строки `live_only` из `scripts/tests/fixtures/driver-exits/gates.json` ходятся: пять маршрутов выше, `exit_gate:digest` и остальные пять стыков `exit_gate` с причиной «estimate». Каждая строка либо становится `reach: story` со своим ожидаемым исходом, либо остаётся `live_only` с причиной, которая уже не про окно; `raised_by` сжимается на каждую снятую строку (храповик только вниз).
4. Тест — строки таблицы `dry_exits.py --selftest`: окно из N границ доходит до читаемого отказа; окно по умолчанию ведёт себя как прежде.

Свидетель: `scripts/tests/fixtures/driver-exits/gates.json`, поля `why_unreached` строк `route:marked_repair/code move`, `route:form_vocabulary/code move`, `route:handover_form/code move`, `route:missing_output/code move`, `route:handoff_form/code move` и стыка `exit_gate:digest`; вердикт `docs/tasks/specs/reviews/t-1077-p1b-n4-gates-topic-code.md`, F5.

Принципы и правила: AR-25, AR-28.

Решение владельца нужно: нет.
