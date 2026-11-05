# Квитанция осмотра MR: `inspect --media-url` отказывает без двери, скаут пишет ложный пробел

id: — | кучка: `hotfix-12586` | от: прогон TP1-12586 на 0.10.5, `testproject1-dev-010`, 29.10.2026 ~11:10, S1; слово владельца 29.10 («да» на оформление) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Скаут S1 сообщил человеку пробел: «Inspection gap: The scout could not record inspection receipts for the five MRs. ticket_adapter.py
inspect --media-url rejected them, saying the source id and URL must identify exactly one media item. The MR diffs are saved under
work/sources/mr/. That is a gap on the factory's side». Пробела по сути нет: все пять MR прочитаны целиком.

| Что | Носитель (стенд, `qa-factory/artifacts/TP1-12586/work/`) |
|---|---|
| пять MR со `status: read`, описанием, заметками, обсуждениями и `diffs` (testproject1 !3988, testproject1-sdk !803, !810, testproject1-ui !1652, !2167) | `sources/mr/*.json` |
| MR входят в пакет контекста S2 | `context-bundle.json`, `context-manifest.json`, `handoffs/S1-qa-scout-1.yaml` |
| у источника-задачи `external_media: count 0` — MR в этом списке нет и не должно быть | `source-inventory.json` |

Отказ дал `source_inventory.record_external_media` (`len(matches) != 1` → «source_id and URL must identify exactly one external media item»):
он ищет URL только среди ссылок на материалы из описания и комментариев. MR приходят другим путём — ссылки разработки
(`ticket_light.py`, строки `merge_request`) и свою запись в `work/sources/mr/`; квитанция `inspect` им не нужна.

## Влияние на стори

Данные не потеряны, выход S1 не держится (в инвентаре нет `pending`). Вред — текст человеку: ложный «пробел на стороне фабрики» в
сообщении гейта A или в «Left with you» отчёта; если пробел дойдёт до вердикта доставки как непроверенное — ошибка отчёта (P21, FR-35).

## Класс

Отказ верен по сути, но не называет двери и не говорит, что не так с вызовом (FR-1, FR-2, AR-9): роль не может отличить «этот URL
не материал инвентаря — квитанция не нужна» от «квитанцию записать нельзя», и пишет второе. Плюс S1 (`skills/qa-story/phases/s1.md`,
«URLs to documents, images, and videos…») не говорит, что ссылки на MR / коммиты / ветки этим правилом не покрыты (FR-38, AR-10).
Сосед по классу — отказ `accept-gap --point` (тот же файл, строки 2408–2425): проверить ту же форму.

## Направление

(1) Отказ `record_external_media` при нуле совпадений различает: URL — известный MR / источник реализации (есть в `work/sources/mr/` или
строках `merge_request`) → текст «это источник реализации, он записан в `work/sources/mr/<file>`; квитанция `inspect` не нужна, ничего
делать не надо»; иначе — перечень URL материалов источника (≤ 5) и команда, как добавить новую ссылку. (2) S1: одна строка — ссылки
на MR / коммиты / ветки учитываются ссылками разработки, `inspect --media-url` к ним не применяется. (3) Тест: URL MR в инвентаре без
материалов → текст отказа называет файл MR; неизвестный URL → перечень. Узел HF8-5.

Принципы и правила: FR-1, FR-2, FR-38, P15, AR-9, AR-10.

Решение владельца нужно: нет (слово на оформление дано 29.10.2026).
