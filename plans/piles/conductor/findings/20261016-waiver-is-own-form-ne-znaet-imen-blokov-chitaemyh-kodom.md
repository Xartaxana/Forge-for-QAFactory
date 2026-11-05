# `waiver._is_own_form` не знает имён блоков, которые читает код («keep it local», «executor unavailable: <profile>»): писатель K4 отвергает их при стоящей записи отказа — скрытый дефект C2-5s

id: — | кучка: `conductor` | от: билдер t-875 (C3-10, вопрос Q1; проба `waiver.block_standing` → `unmatched`/`unknown`), записал Lead 16.10.2026 07:5x | приоритет: П2 | кандидат наверх: нет

## Что

C2-5s (t-835) сделал писатель пропуска строгим: `--block` обязан совпасть со строкой стоящего отказа (`state/standing-refusal.json`)
или быть собственной формой (`_is_own_form`: id карточки, `wait_existing_job`, …). Но два блока — не строки отказа, а ИМЕНА, которые
читает код: `keep it local` (`external_writes.local_only_decision` читает `decision + match`; `s8.md:191-197` — «the block text is part
of the recognition»; отказ NO_ADAPTER говорит «keep local», не «keep it local») и `executor unavailable: <profile>` (`s4.md:92`,
`SKILL.md:233`; читает `contract.handed_profiles`). Проба билдера: при любой другой строке в записи S8 `block_standing` возвращает
`unmatched` (писатель отказывает), без записи — `unknown`. `--remark` эти читатели не читают — подмена сломала бы распознавание
(фабрика попытается записать то, что человек запретил).

Что сделать: (а) `_is_own_form` узнаёт оба имени (данные, не код — FR-13: список имён-блоков, читаемых кодом, с указателем на
читателя); пины: оба имени проходят при стоящей записи с другой строкой и без записи; (б) после этого — тексты `s8.md:337`,
`:191-192`, `s4.md:92`, `SKILL.md:233` остаются как есть (имя блока — форма). Аналоги из переписи t-875: `conductor-actions.json:100`
(`<the block>`, C2-7), `artifact-contract-json.md:71`, `design/state-exits.md:73` (`<text>`), комментарий `external_writes.py:288`.
Очередь `waiver.py`: C2-6 (t-856) → этот узел.

## Куда

Строка C4-3 пачки `conductor/batch-4-vhodyashchie-2.md` (D-0044); остаток C3-10 (s8) закрывается им.
