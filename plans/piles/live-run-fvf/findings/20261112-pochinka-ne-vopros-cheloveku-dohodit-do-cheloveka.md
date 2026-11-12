# S5 требует `obligation_refs`, которые для тестов на TypeScript фабрика произвести не может; проверка при этом принимает рукописное значение и ставит человеку «починку, не вопрос»

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0 + FV1-1), 12.11.2026 | приоритет: П1 | кандидат наверх: да

## Что не так

S5, оба окна, тесты проекта на Playwright/TypeScript (`tests/api/cart/*.spec.ts`). Проверка выхода `s5_precheck.py` отказывает
каждой строке манифеста без `obligation_refs` и пишет: «`obligation_refs` is written by the marker, not by hand (a hand-written
value would not carry the hash the plan's obligation has): put `qa(obligations=[…])` on the test and run `manifest_from_tests.py`
again … (This is a repair, not a question for the person)».

Три дефекта:

1. **Поле нельзя произвести.** `scripts/manifest_from_tests.py` читает маркеры только из Python (`import ast`, `ast.parse`,
   строка 311; `typescript`/`.spec.ts` в файле нет, положительный контроль — `parametrize` находится 11 раз). Маркер на тесте
   `.spec.ts` прочитать некому. Автоматор окна 1 (`S5-qa-automator-4`) сказал это сам: «The manifest writer reads no obligation
   marker from TypeScript. The plan carries no obligation hash… This needs a person's waiver or a TypeScript marker reader in
   the factory» (`state/driver-question-details.md` копии плеча, 21:09). FR-5 (стадия требует артефакт, который ничто в фабрике
   не производит), FR-11, P31 (разные пути для языков — баг).
2. **Проверка принимает то, что сама объявляет негодным.** Окно 2 (TC-006/007) прошло после второго `round`: автоматор-3
   вписал руками `obligation_refs: {"obligation_id": "OB-6"}` / `OB-7` — без хэша (`work/automation-manifest.json` копии плеча).
   Значение взято из отклонённого ответа оператора (`answers/s5-exit-limit-round-mapping.md`), который дирижёр перенёс в текст
   вопроса. Гейт пропустил рукописное значение вопреки собственному тексту отказа (FR-1: отказ говорит, чего ждёт; AR-29).
   Для сравнения прогонов: проход окна 2 — **помощь оператора**.
3. **Починка, помеченная «not a question for the person», доходит до человека** вопросом `exit_limit` (`round / fresh / go on /
   stop`) дважды в каждом окне (окно 2: 20:3x, 20:46; окно 1: 21:04, 21:09). Человек не знает ничего сверх проверки;
   выбор «round или fresh» — фабрики (FR-3, P22, FR-48). При невозможной починке (п. 1) единственный не останавливающий ход —
   `go on` с пробелом в гейт B: ответ оператора 21:10 (`answers/s5-exit-limit-go-on.md`).

Свидетели: `runs/factory-18.log` … `runs/factory-22.log`; `notebook.md`, «Ход прогона», 20:3x–21:10.

## Что сделать (предложение оператора)

1. Маркер обязательств читается из тестов каждого языка, который фабрика автоматизирует (TS/Playwright — как минимум), одним
   путём (P31): читатель маркера TS в `manifest_from_tests.py` или путь, который не зависит от языка. До этого — проверка не
   требует поля там, где читателя нет, и пишет пробел, а не отказ (FR-5, FR-59).
2. Проверка `obligation_refs` отказывает рукописному значению без хэша (как обещает её текст) — или текст отказа перестаёт это
   обещать; одно из двух, не оба.
3. Находки, помеченные «repair, not a question for the person», после исчерпания возвратов идут дирижёру, не человеку; дирижёр
   сам выбирает `round`/`fresh`/пробел (P22). Тест: exit_limit, у которого все находки — repair, → ход дирижёра без
   `driver-question.md`.

Принципы и правила: P22, P27, P31; FR-1, FR-3, FR-5, FR-11, FR-48, FR-59; AR-10, AR-17, AR-29.

Решение владельца нужно: нет.
