# Отказанный ручной кейс не получает терминального исхода в трассировке — третий вердикт доставки (P21) недостижим для `person_checks`

id: — | кучка: `conductor` | от: Lead, 21.10 (измерение билдера C1-6b t-1163, хэндофф t-1221; подтверждено критиком t-1177) | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: когда человек на вопросе `s6.stand_login` отвечает `by hand`, кейс записывается как
`refused.by: person_checks`, и `check_delivery.py` (C1-5c, `mark_handed`) верно переводит строку леджера в
`not_executed:handed_to_person` с пунктом «handed» в «Left with you». Но `check_traceability._case_chain`
(`check_traceability.py:38-87`) не даёт отказанному ручному кейсу терминального исхода: требование остаётся «R-n has no
terminal outcome (TC-m: neither in automation-manifest tests[] nor unresolved[])», и вердикт доставки — `no`, а не
`after_checks`. Третий вердикт P21 («готово после завершения проверок человеком») для кейсов, отданных человеку, недостижим;
строка цены `by hand` в `question-prices.json` сегодня честно говорит «not ready to ship as is» (FR-41) и обязана
перевернуться на `after_checks`, когда это починят. Сделать: `_case_chain` читает `refused.by: person_checks`
(и `left_unchecked`) как терминальный исход «отдано человеку» (тот же смысл, что `handed` в леджере — один источник для
двух читателей, AR-13), `delivery_verdict` даёт `after_checks`; пины в `test_check_traceability`/`test_story_run_s6`
(строка цены `by hand` → `after_checks`); узел кучки C1-5 (класс «ничьи результаты»), после слияния C1-6b.

Свидетель: хэндофф `docs/tasks/handoffs/t-1221-c1-6b-s6.md` (измерение 1: три прогона `check_delivery.py` на копии GOOD-фикстуры
с `refused.by` ∈ {—, person_checks, left_unchecked} — все `delivery_ready: no`; при `person_checks` причина леджера ушла, причина
трассировки осталась); обзор `docs/tasks/specs/reviews/t-1228-c1-6b-c1-6c.md` («The by hand line … is true today: `_case_chain`
gives a refused manual case no terminal outcome»); `ai-packages/qa-factory/scripts/check_traceability.py:38-87`.

Принципы и правила: P21, P19 (ступени 3–5), P20; FR-21, FR-41, FR-49; AR-13, AR-26, AR-28; D-0039.

Решение владельца нужно: нет (техническое; P21 — слово владельца 02–03.10).
