# Проба TypeScript убивает тест на мутированной строке, но вердикт «incomplete»: сообщение Playwright не читается, человеку сказано «инструмент не читает TypeScript»

id: — | кучка: `release-next` | от: живой прогон LOCAL-1 (MyBooks add to cart, 0.10.8), S5 окно `S5-qa-code-critic-2`, 02.11.2026; вопрос владельца 02.11.2026 («почему мутационные пробы проходят только на одном языке… мы же вроде чинили это») | приоритет: П1 | кандидат наверх: нет

## Что наблюдалось

`A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1` (копия проекта вне репозитория).

- Все 4 пробы окна построены и исполнены кодом: `A/work/probes/LOCAL-1_TC_004…json`, `…TC_005…`, `…TC_011…`, `…TC_013…`, у каждой
  `language: typescript`, `mutation: invert`, `restore.verified: true`. Пример TC_004: `expect(added.status(), 'add accepted').toBe(201)` →
  `.not.toBe(201)`; прогон `A/evidence/runs/b38f395fa66a976ca8ec/red_probe-…-023513.log` упал **на строке 12, на мутированном утверждении**:
  `expect(received).not.toBe(expected) // Object.is equality … Expected: not 201`. Так же у TC_005 (:29), TC_011 (:63), TC_013 (:93).
- Вердикт всех четырёх — `incomplete`, `cause: tooling`; заметка кода: «the run failed at the mutated statement, but its message
  (`cart.spec.ts:7:1 @api @regression LOCAL-1_TC_004 …`) does not match … the row is the factory's to correct (E15)».
- Дирижёр по `s5.md:170` («When the tool cannot read this language … `cause: tooling`») спросил человека «можно оставить TypeScript-тесты без
  мутационной пробы: инструмент проб не читает TypeScript», человек ответил «Да» (`A/state/words/s5-probe-gap-typescript.txt`, `pipeline.json`,
  класс `probe_gap_accepted`). В манифесте у всех 4 тестов `critic_verdict: unverified`, причина «probe tool cannot read TypeScript».

## Причина (проверено по коду 02.11.2026)

1. **Сравнение сообщения привязано к форме pytest.** `scripts/probe_by_code.py` `fires_on` (стр. ~1664) сверяет `fires_as` сначала с атрибутом
   `message` строки JUnit, потом с `text_head(text)` — текстом до первого кадра. `assertion_detectors.fires_matches` — `re.search` без флагов,
   `^` в образце значит начало ВСЕГО текста. У Playwright:
   - `message` = `cart.spec.ts:7:1 <заголовок теста>` (место и имя, не ошибка);
   - текст начинается строкой-шапкой `  [chromium] › api\cart\cart.spec.ts:7:1 › <заголовок>`, затем `Error: add accepted` (своё сообщение
     утверждения — второй аргумент `expect`), и только потом, с отступом, `expect(received).not.toBe(expected)`.
   Образец `^(?:Error: )?expect\(received\)…\.not\.to[A-Z]…` не может совпасть ни с одним из двух субъектов. У pytest `message` — сам текст
   утверждения, поэтому там проба работает: «проходит на одном языке» — это форма отчёта раннера, не язык.
2. **Тесты видели только придуманную форму.** `scripts/tests/fixtures/probe-languages/samples.json` (T1, T2) даёт субъекты, начинающиеся с
   `Error: expect(received)…`; ни одного реального отчёта Playwright со шапкой, своим сообщением `expect(x, 'msg')` и отступом. Фикстура
   `fixtures/playwright-junit/basic.xml` есть, но через `judge_detector` не проходит.
3. **E15 записан как «инструмент не читает язык».** `judge_detector` (стр. ~1751) отдаёт E15 (упало на мутированной строке, расходится только
   формулировка — данные фабрики) с `cause: tooling` — той же причиной, что «нет записи языка / не найдено объявление». `s5.md:170` читает любую
   `cause: tooling` как «the tool cannot read this language» и велит спросить человека. Человеку сказана неправда, и вопрос задан о дефекте
   данных фабрики (FR-3: причина фабрики сообщается, а не ставится выбором; FR-41; P9).
4. **Роль не взвесила улику.** Критик кода видел лог с `expect(received).not.toBe` на строке 12 — то есть ровно то, что должна показать
   обращённая форма, — и записал `unverified`. P1: код сообщает, роль решает; двери «убит по моей проверке лога» у критика нет.

## Почему опять

Чинили узлом EP1-36 (0.10.8, находка `execution-probes/findings/20261031-proba-chuvstvitelnosti-ne-chitaet-playwright-ts-18-iz-18.md`):
сопоставление заголовка с объявлением, теги, циклы, `selectors.verified`. Эта половина работает: в CART-1 не построилась ни одна проба из 18,
в LOCAL-1 построены и исполнены 4 из 4, мутация и восстановление верны. Сломан следующий шаг — чтение вердикта, — который в EP1-36 не входил и
был покрыт только придуманными строками. Живое доказательство EP1-36 (FR-33: «прогон CART-1-подобной истории, not probed не 18 из 18») до релиза
не делалось; LOCAL-1 и есть это доказательство, и формально оно «прошло» (пробы есть), а по смыслу нет (все `unverified`).

## Класс

Шаг, переведённый в код, проверен на придуманной форме данных, а не на снятом с живого раннера образце (PROJECT.md «Как принимается
изменение пакета» п. 5; FR-28, FR-33). Сиблинги по `docs/SIBLING_MAP.md` — все читатели сообщения JUnit не-pytest раннера: `fires_on`,
`text_head`, детектор «изменено после красного» (EP1-37), `reporters.assertion_site`; узел проверяет их тем же реальным отчётом.

## Что именно менять

Направление выбрано (Lead, 02.11.2026).

1. **`scripts/probe_by_code.py` `fires_on`:** субъект сравнения — каждая строка `message` и `text_head(text)` по отдельности, с отрезанным
   ведущим пробелом; совпала любая строка → совпадение. `fires_matches` и данные `references/detectors.json` не меняются (AR-1: правило одно
   для всех языков, не ветка по раннеру). Тест: реальный отчёт `A/evidence/runs/b38f395fa66a976ca8ec/red_probe-…-023513.junit.xml`, скопированный
   в `scripts/tests/fixtures/probe-languages/playwright-red-probe.junit.xml` (пути заменены на относительные), через `judge_detector` с деталью
   TC_004 (строка 12, пара T2) → `intended_failure`. Отрицательный контроль: тот же отчёт с `expect(received).toBe(expected)` вместо `.not.toBe` →
   не `intended_failure`.
2. **`samples.json`:** в T1 и T2 добавить реальные формы Playwright — шапку `[chromium] › …`, своё сообщение `Error: <msg>` отдельной строкой,
   строку `expect(…)` с отступом; ожидание — `fires` для своей пары, `not` для обратной.
3. **E15 получает свою причину:** `judge_detector` пишет для E15 `cause: data_row` (не `tooling`); `s5.md:170` спрашивает «класс языка» только
   при `refused: tool` или непрочитанном месте падения. E15 — строка отчёта «не пробован: формулировка ошибки не узнана, дефект данных фабрики»
   без вопроса человеку (FR-3, FR-41); тест: E15 → `cause: data_row`, вопрос `probe gap: tooling:<язык>` не ставится.
4. **Дверь роли:** `agents/qa-code-critic.md` — при `incomplete` с падением на мутированной строке критик читает лог прогона пробы и, если
   видит обращённую форму утверждения, пишет `critic_verdict: killed` со ссылкой на строку лога (`evidence_ref`); код это не запрещает
   (FR-39). Тест присутствия правила в уставе.
5. **Почему дирижёр сам не увидел, что проба прошла** (вопрос владельца 02.11.2026) — не чинится здесь построчно: по слову владельца это
   общее правило «дирижёр всегда сначала разбирается сам», узел RN1-9 (`findings/20261102-dirizhyor-sprashivaet-cheloveka-ne-razobravshis-sam.md`),
   строка `s5.md:170` переписывается там.
6. **Живое доказательство (FR-33) до закрытия узла:** повтор `probe_by_code` на `A` (MyBooks `a25b080`, `cart.spec.ts`) → 4 из 4
   `intended_failure`; строка в «Живых доказательствах» пачки.

## Принципы и правила

P1, P2, P9; FR-3, FR-28, FR-33, FR-39, FR-41, FR-54, FR-59; AR-1, AR-2, AR-28.

Связи: EP1-36, EP1-37 (`execution-probes`), EP1-22 (JUnit Playwright читается), GW1-43 (слово класса `tooling:<язык>`),
`gates-and-words/findings/20261031-otvechennoe-reshenie-klassa-sprashivaetsya-snova-na-sleduyushchem-okne.md`.

Решение владельца нужно: нет.
