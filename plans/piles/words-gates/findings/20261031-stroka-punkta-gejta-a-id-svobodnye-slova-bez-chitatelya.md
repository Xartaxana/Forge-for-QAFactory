# Строка пункта гейта A вида `vcs-1: <свободные слова>` не читается никем: ответ «approve» плюс такие строки по-прежнему уходит дирижёру целиком (RL-4:8)

id: — | кучка: `words-gates` | от: критик t-542 (F7, `docs/tasks/specs/reviews/t-542-gate-answers-critic.md`) и прогон 14857 (RL-4:8), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

- Ночной прогон 14857, RL-4:8: ответ «approve; Q1: a; vcs-1: go on on this branch; case_environment-1: accept the gap; …» — «9 строк ответа похожи на ответ о пробелах
  стенда и не прочитаны; ответ уходит дирижёру» (`experiments/run-14857/runs/r14857-4.log`). Находка GW1-33 (`findings/20261030-otvet-approve-s-punktami-ne-zapisyvaetsya-dve-dorogi-dva-slova.md`)
  чинила слово `approve` над открытыми пунктами, но критик t-542 F7 показал по чтению: настоящий RL-4:8 — исход 2. `vcs` и `case_environment` — пункты класса
  `PERSON_DECIDES` БЕЗ `waives` (`gate_preflight.check_vcs`, :1675/:1682; `check_case_environment_gaps`, :1738), поэтому их дверь в `gate_brief._open_item` (:458)
  — `words` или `none`, а не `line`; строка `vcs-1: <слова>` не читается: `story_run.Driver.read_finding_doors` (:15621) читает `<id>: <слово закрытого списка> [причина]` ТОЛЬКО для
  находки с `waives`, остальное «never read». Узел GW1-33 свой же пример не чинит.
- Следствие: открытый пункт остаётся открытым, контроллер (`controller.open_gate_items`, :2874; отказ в записи гейта) отказывает, ответ идёт дирижёру через
  `open_items_text` (`story_run.py:14756`), платный вызов нужен только чтобы переложить слова человека в `waiver.py --block …`.
- Класс: слова человека на пункт не доходят до читателя в форме, которую пакет сам показал (FR-8, FR-42, AR-24); сосед — GW1-32 (какие формы ответа читает код).

## Что именно менять (направление выбрано Lead пачки, 31.10.2026, по рекомендации; свободные слова код НЕ читает, FR-12, P22)

1. `story_run.py`, `Driver.read_finding_doors` (:15621) и его читатель строки `_FINDING_LINE_RE` (:15619): строка `<id>: <слова>` для id ОТКРЫТОГО ПУНКТА гейта
   (id из `gate_brief.open_rehearsal_items`, как человек его видел в пакете), не попавшая ни в `read`, ни в `probes`, возвращается в новом списке
   `item_words` = `[{id, line}]` — а не молча в «похожи на ответ о пробелах и не прочитаны». Код ничего не записывает по смыслу этих слов.
2. `story_run.py`, `open_items_text` (:14756): под каждым пунктом, на который есть строка человека, печатается `- the person wrote for [<id>]: "<строка целиком>"`
   (обрезка `MAX_NOTICE_LINE`, как у `question_register._shown_line`), и подсказка дирижёру: слова — это слово человека на пункт; записать командой пункта
   (`waiver.py --block <door.block>`; файл начинается `accept - the person wrote: `), если слова это принимают; если нет — один закрытый вопрос про этот пункт.
   Это снимает «дирижёр может только снова предложить `approve`».
3. `gate_preflight.py`: `check_vcs` (обе ветки) и `check_case_environment_gaps` получают `waives` (блок и опцию `accept`), чтобы закрытая форма `vcs-1: accept <причина>` читалась
   кодом без дирижёра: `fix` называет эту строку словами (`reply with the line "vcs-1: accept <why>"`, P9, без скрипта). Если узел S1a (`t-538` П7, `check_vcs` с дверью) уже
   в дереве — этот пункт для `vcs` выполнен им, остаётся `case_environment`; сверить по коду при взятии.
4. Тесты (новый `scripts/tests/test_item_words_unread.py` рядом с `test_question_lines_unread.py`; фикстура — реальный RL-4:8 из `experiments/run-14857/`): (а) ответ
   «approve» + `vcs-1: go on on this branch` + `case_environment-1: accept the gap` на настоящем контроллере: запись не сделана, дирижёру ушёл `open_items_text` с обеими
   строками человека под своими пунктами; (б) `vcs-1: accept my branch is fine` после п. 3 читается кодом, пункт закрыт одной записью; (в) строка с `?` не читается кодом;
   (г) id, которого нет среди пунктов, не попадает в `item_words`. Мутация: убрать `item_words` из `open_items_text` — красит (а).

## Принципы и правила

P13, P22, P9; FR-8, FR-12, FR-42, FR-9; AR-15, AR-18, AR-24. Связи: `findings/20261030-otvet-approve-s-punktami-ne-zapisyvaetsya-dve-dorogi-dva-slova.md` (GW1-33),
`findings/20261028-gejt-a-pyat-form-otveta-v-odnom-pakete.md` (GW1-32).

Решение владельца нужно: нет (направление: код не записывает свободные слова как проход; запись — закрытая форма `accept` или дирижёр).
