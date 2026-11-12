# Гейт A показан человеку, когда сама репетиция говорит «S5 can start: no … this gate should not have been shown yet»

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0), 12.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что не так

Оба показа гейта A: «S5 cannot start yet: 10 thing(s) the factory still has to repair itself — this gate should not have been
shown yet»; «Gate A rehearsal — LOCAL-1: S5 can start: no»; среди пунктов «the derived scope of S5 is empty — an empty
scope passes every later check and closes the stage having tested nothing», ревью кейсов P-2/P-4/P-5/P-10 — `reject`.
Человек получает одобрение плана, который фабрика сама не считает готовым; владельцу пришлось решать «approve as is».

Класс: фабрика просит человека решить то, что её собственное (FR-3: причина, принадлежащая фабрике, сообщается, а не
выносится выбором); P22 — дирижёр разбирается сам до вопроса.

Свидетель: `runs/factory-8.log`, `runs/factory-9.log`; `notebook.md`, «Ход прогона», 18:47–18:56.

## Что сделать (предложение оператора)

Пока репетиция гейта говорит «S5 can start: no» по пунктам фабрики, гейт не показывается — идёт дирижёр (ремонт или один
вопрос «фабрика не может починить X: идём с дырой / стоп» с ценой). Тест: репетиция с пунктом `prepare-1` → гейт не
показан, вопрос дирижёра.

Принципы и правила: P22; FR-3, FR-48; AR-17.

Решение владельца нужно: нет.
