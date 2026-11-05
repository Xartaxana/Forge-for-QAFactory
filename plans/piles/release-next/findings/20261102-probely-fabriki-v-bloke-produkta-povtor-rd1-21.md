# В итоговой сводке в блоке «product side» стоят дефекты кейсов и пробел стенда, а вердикт S7 не переписывает строки S5: регрессия узла RD1-21

id: — | кучка: `release-next` | от: прогон LOCAL-1, разбор t-1672 П-11 (БОЛЬШАЯ), 02.11.2026 | приоритет: П1 | кандидат наверх: нет

Сокращения: `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`.
Разбор: `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` (П-11).

## Что наблюдалось

- Финальные `A/work/delivery-summary.md:72-123` и `A/work/ledger.md` (версии 10:50–10:51, после гейта B не пересобраны) в блоке «What blocks delivery on the product side» держат 13 `CASE_DEFECT` как «unresolved (contradicts_requirement) with no decision attached», TC_022/023 как «neither in automation-manifest» (пробел стенда, принятый человеком) и `coverage red: OB-n — none`.
- Узел RD1-21 (0.10.8, «принято, слито», `report-delivery/findings/20261031-probely-pokrytiya-i-instrumentov-pokazany-kak-produktovye.md`) обещал не показывать пробелы фабрики и инструментов как продуктовые. Заголовок блока: `scripts/delivery_summary.py:25` (`'product': 'What blocks delivery on the product side'`).

## Причина

Вердикт S7 (`CASE_DEFECT`) не переписывает `unresolved[]` S5; принятый человеком пробел стенда не записан в строку; пробел покрытия без причины отнесён к продукту (`scripts/check_delivery.py` `reason_owner`, `:198`, `_owner_decided`, `:228`).

## Класс

Причина в чужом блоке: у причины должен быть владелец, и неизвестный владелец — дефект классификатора, а не продукт (FR-19, FR-20, AR-27). Регрессия/не починено: RD1-21 (и сосед RD1-19, `20261031-prichina-triazha-i-plana-teryaetsya-pri-sborke-otcheta.md`: «вердикт S7 не доезжает»). Фабричный класс.

## Что именно менять

Направление выбрано (Lead, 02.11.2026).

1. **Вердикт S7 переписывает строку.** `scripts/delivery_summary.py` `build` (`:224`) и `scripts/check_delivery.py`: строка с триажем `CASE_DEFECT` из `triage.json` получает владельца factory и идёт в блок «what blocks delivery from the factory side», не product. Тест: фикстура с 13 `CASE_DEFECT` → блок product их не содержит.
2. **Принятый пробел стенда.** Слово человека о пробеле стенда (`state/words/s6-manual-login-gap.txt`) записывается в строку каждого кейса, на который оно распространено (TC_022, TC_023, TS-24, TS-25) с владельцем environment; тест: строка TC_023 несёт слово.
3. **Пробел без причины — не продукт.** `coverage red: OB-n — none` не относится к product: код отказывает с дверью «назови причину» (`classifier_findings`, `check_delivery.py:176`). Тест на фикстуре.
4. **Пересборка после гейта B.** `delivery-summary.md` и `ledger.md` пересобираются вместе с отчётом (см. RN1-33 в `release-next`, регрессия RD1-20).

## Принципы и правила

P21; FR-19, FR-20, FR-35; AR-27.

## Связи

- RD1-21, RD1-19; RN1-16 (порядок причин); RN1-17; `release-next/findings/20261102-svodka-dostavki-ne-peresobrana-posle-gejta-b-povtor-rd1-20.md`.
- Разбор t-1672 П-11.

Решение владельца нужно: нет.
