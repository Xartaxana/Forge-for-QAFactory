# Ответы человека применены к флагам строк, но тексты для человека остались «открыт», а слово о пробеле стенда дошло не до всех экземпляров

id: — | кучка: `words-gates` | от: прогон LOCAL-1, разборы t-1671 Н-13 (МАЛАЯ) и t-1672 П-12 (МАЛАЯ), 02.11.2026 | приоритет: П2 | кандидат наверх: нет

Сокращения: `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`; `TC` = `mybooks-stand/test-automation-framework/test-cases/cart`.
Разборы: `docs/tasks/specs/reviews/t-1671-local-1-gates-vs-analysis.md` (Н-13), `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` (П-12).

## Что наблюдалось

- Н-13. Ответ Q3 применён (`A/work/question-answers.jsonl:15` rows TS-14), но: `TC/LOCAL-1_TC_013.md:31,36` «999… is open question Q3»; `A/work/test-plan.md:20,29,32` TS-2/TS-11/TS-14 `oracle_unknown` (BN-4, BN-7); `A/test-report.md:116` BN-7 «"maximum allowed" is not defined». Ответ Q3 до отчёта не дошёл.
- П-12. Человек принял пробел стенда для TC_022 и TC_023 (`A/state/words/s6-manual-login-gap.txt`), но TC_023 не диспатчился вообще, причина — «no record was written» (`A/test-report.md:50`); TS-24/25 — «not_executed: no result recorded» (`A/work/delivery-summary.md:19-20,102-103`); runner-2 scope только TC_022 (E:240 `A/state/events.jsonl`).

## Причина

Применение ответа пишет флаги строк плана (`question_register`, `planning_contract.apply_recorded_answers`), а тексты в кейсах/плане/отчёте остаются прежними, потому что их читатель отдельный; решение класса («пробел стенда принят») исполняется по одному экземпляру (TC_022), не по перечню экземпляров, названных в слове.

## Класс

Слово человека доходит до каждого читателя целиком (FR-8, AR-24); решение класса действует на все экземпляры (D-0043, P5 уточнение). Регрессия по классу GW1-43 (там — повторный вопрос, здесь — неприменение к соседям). Фабричный класс.

## Что именно менять

Направление выбрано (Lead, 02.11.2026).

1. **Тексты за флагами.** Когда ответ применён к строке плана, код пересобирает строки `oracle_unknown`, «open question Qn», BN-n в `test-plan.md`, в `test-cases/*.md` (маркер «open question») и в отчёте от одного регистра ответов (`scripts/planning_contract.py` + `scripts/report_facts.py`, читатель — один, `question_register`). Тест: Q3 отвечен на фикстуре → ни план, ни кейс, ни отчёт не содержат «open question Q3»/BN-7.
2. **Слово о пробеле стенда — на все экземпляры класса.** `scripts/story_run.py` (S6, где пишется scope runner): слово класса, названное с перечнем кейсов (TC_022, TC_023), применяется к каждому кейсу перечня и к строкам плана TS-24/25, привязанным к ним; тест: слово на два ручных кейса → обоим записан исход «пробел стенда, принят человеком», `not_executed: no result recorded` не печатается.

## Принципы и правила

P5, P13; FR-7, FR-8, FR-10; AR-24.

## Связи

- GW1-43 (регрессия по классу), RN1-11 (Q9), RN1-10 (вход ручной проверки), RN1-23.
- Разборы t-1671 Н-13, t-1672 П-12.

Решение владельца нужно: нет.
