# Гейт B не несёт строки «что вы одобряете», которую GW1-11 построил кодом для гейта A (t-520 G6)

id: — | кучка: `driver-hosts` | от: критик t-520, G6 (`docs/tasks/specs/reviews/t-520-small-nodes-critic.md`), 31.10.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

GW1-11 дал гейту A первую строку, которую строит код: `gate_brief.gate_a_approval_line()` (:1755) из `GATE_A_DOCUMENTS`. Сиблинг-пункт 5 находки `20261022-gejt-a-chetyre-dokumenta-vmesto-dvuh.md`
требует того же для гейта B; коммит GW1-11 сказал «unchanged» и больше нигде не записан. `gate_brief.render_gate_b` (:3807) начинает с `# Gate B — <task>`, а два документа
называет только в конце: «## The long documents» (:3942–3946, пути `delivery-summary.md` и `test-report.md`, литералы). Слово одобрения гейта B есть в данных
(`references/gate-approval-words.json`: `approve`, `gates: ["A","B"]`), читатель `gate_brief.approval_words("B")` (:641) — но в сообщении оно не названо. Ось «двойники стадий» (AR-19).

## Что именно менять (направление выбрано: та же строка и для гейта B)

1. `gate_brief.py`: рядом с `GATE_A_DOCUMENTS` — `GATE_B_DOCUMENTS = (("delivery summary", "delivery-summary.md"), ("test report", "test-report.md"))` (имена сверить с :3943–3946: сейчас литералы,
   после правки их берёт этот кортеж); `gate_b_approval_line()` — тот же построитель, что у A (один `_approval_line(gate, documents)`, AR-13/AR-19): «**Approve: `delivery-summary.md`, `test-report.md`.** Answer by number to file bugs;
   the word `approve` approves as shown.» (формулировка из `approval_words("B")["approve"]["says"]`, не литерал).
2. `render_gate_b` (:3813): вторая строка после заголовка — эта строка. Раздел «The long documents» берёт пути из `GATE_B_DOCUMENTS`.
3. Тесты (`scripts/tests/test_gate_a_two_documents.py` + таблица для B; K6 сверяет текст `phases/s8.md` с кортежем): сообщение гейта B называет ровно два документа и слово `approve` из данных; мутация: переименовать слово
   в `gate-approval-words.json` — строка меняется без правки кода.

## Принципы и правила

P9; FR-6, FR-10, FR-13; AR-16, AR-19. Связи: GW1-11, `findings/20261022-gejt-a-chetyre-dokumenta-vmesto-dvuh.md` (п. 5).

Решение владельца нужно: нет.
