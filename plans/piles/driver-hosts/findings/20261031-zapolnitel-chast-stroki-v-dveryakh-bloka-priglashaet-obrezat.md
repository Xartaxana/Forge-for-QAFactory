# Заполнитель `<part of the line>` в шести напечатанных дверях `waiver.py --block` приглашает вписать кусок строки, а читает код целый идентификатор

id: — | кучка: `driver-hosts` | от: отчёты S1a/GW1-1 (`docs/tasks/handoffs/s1a-gw1-1-report.md:80,98`) и критик t-542, 31.10.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

После GW1-1 слово человека сопоставляется со строкой целым идентификатором (`contract.names_whole`, `contract.py:128`), а двери всё ещё печатают
`waiver.py --task <T> --stage <S> --block "<part of the line>"` — «часть строки». Хвост `person_words.WHOLE_PART` (`person_words.py:55`) поправляет смысл ПОСЛЕ заполнителя, но
сам заполнитель остался приглашением обрезать. Он напечатан в шести местах пакета (по `Grep` «part of the line» в `scripts/`):
`branch_accounting.py:1780`, `controller.py:6751`, `critic_rollcall.py:808`, `planning_contract.py:2937`, `s5_precheck.py:4018`, `refusal_registry.py:64` (константа `WAIVER`), плюс
четыре строки текста роли в `skills/qa-story/phases/s3.md` (:29, :84, :129, :153) и генератор `tools/controller-blocks-gen.py:453` (с ним — `design/controller-blocks.md:20`).
Читатель заполнителя — `waiver.door_blocks` (`waiver.py:445`): любое `<…>` в имени блока — «не имя блока», дверью не считается. Один текст, шесть носителей: правка одного места
оставит пять (AR-13, AR-15, FR-54).

## Что именно менять

1. `person_words.py`: константа `BLOCK_PLACEHOLDER = "<whole words of the line>"` рядом с `WHOLE_PART`; шесть мест выше собирают дверь через неё (`door(f'… --block "{BLOCK_PLACEHOLDER}"')`),
   `refusal_registry.WAIVER` — тоже. Слово «part» из заполнителя уходит; хвост `WHOLE_PART` остаётся.
2. `waiver.door_blocks` и `waiver.py` (проверка записи блока `<…>`): без правки — любое `<…>` по-прежнему не дверь; добавить в список не нужно (проверка по форме, FR-12).
   Старый заполнитель на диске в `stage_overrides` ничего не снимает и не снимал (`t-503` §«заполнитель не слово»): записи не мигрируют.
3. `skills/qa-story/phases/s3.md` — четыре вхождения: тот же текст, что в коде (`test_audit_rules.py` / соседний текстовый тест сверяет фразу из кода с текстом фазы — проверить имя по коду).
   `tools/controller-blocks-gen.py:453` читает константу из `person_words`, не литерал; `design/controller-blocks.md` пересобрать генератором (`python tools/controller-blocks-gen.py`).
4. Тесты: `scripts/tests/test_words_doors.py` + `test_branch_accounting.py:554,561` (там заполнитель назван в ожидании — поменять на константу): (а) во всех шести напечатанных
   дверях стоит `BLOCK_PLACEHOLDER` и нет `<part of the line>`; (б) `door_blocks` на каждой из шести дверей даёт []; (в) строка из фазы `s3.md` равна коду. Мутация: вернуть старый литерал в
   `critic_rollcall.py` — красит (а).

## Принципы и правила

P9, P15; FR-1, FR-6, FR-54; AR-9, AR-13, AR-15, AR-16. Связи: GW1-1 (`names_whole`), `findings/20261022-gejt-a-chetyre-dokumenta-vmesto-dvuh.md` (текст человеку — одна форма).

Решение владельца нужно: нет.
