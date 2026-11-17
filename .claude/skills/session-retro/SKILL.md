---
name: session-retro
description: End-of-session retro of a coordinator session — what got in the agents' way and where the forge or the factory can be optimised. Counts come from tools/session_retro.py, the reasons from the session's own context; the result is ONE file in docs/retro/inbox/, never a chat answer and never a node. Run it before the context is compacted, from session-handoff, or when the operator says "retro".
---

# session-retro — what got in the way, written while the reasons are still in context

Goal (the owner's word 17.11.2026): find what hinders the agents and where the forge or the factory can be
optimised. The reasons live only in this session's context, so the retro runs HERE, before a compaction and
before the session closes; a week later the transcript still shows what happened but not why.

A retro entry is raw material, not a task. It goes to a separate place (`docs/retro/inbox/`); nodes are opened
only after the weekly reduction has merged the repeats and chosen a SYSTEMIC fix (section «Недельное сведение» below).
A patch per entry per session is exactly what this skill must not produce.

## Steps

1. **Counts by code.** `python -B tools/session_retro.py --last 1` (several sessions: `--session <id> ...`).
   Copy its output into the entry verbatim. Do not count by reading the transcript.
2. **Answer the questions** — a short list under each, every item with: a NUMBER where one exists (turns,
   tokens, repeats — from step 1, or "not measured"), the CARRIER (file and line, hook, tool, dispatch id), and a
   proposal of WHERE the fix belongs: code / rule text / spec / tool / nothing.
   1. What caused difficulty.
   2. Which instruction, hook or tool made the session do extra work.
   3. What had to be found out by the session itself although it belonged in the dispatch or in the boot files.
   4. What was read at the start and never needed.
   5. Which gate or hook caught something rightly; which refused wrongly or made noise.
   6. Which decisions the session took itself and is not sure about.
   7. Questions to the owner — only what the owner alone can know or decide.
   An empty answer is written as "nothing: <why>", not left out.
3. **Write ONE file** `docs/retro/inbox/<YYYYMMDD>-<HHMM>-<dev>.md` (`<dev>` — the slug of
   `tools/dev.config.yaml`): a header line (date, the session's model, what the session worked on), the output of
   step 1, the seven answers. No money figures (P18). Russian or English, as the session's chat.
4. **Questions to the owner** (item 7) are also said to the owner in chat, as one list — the file alone does not
   reach her. Everything else stays in the file.
5. **Do not** open findings or nodes, edit rules, or fix anything from the entry in this session. One exception:
   a defect that blocks the session's own current work is fixed on the usual road and the entry says so.
6. Commit the file with the session's last journal commit.

## What happens to the entries

Section «Недельное сведение» below — the weekly reduction: who reads the inbox, how repeats become one class, when a class
becomes a finding and a node, where processed entries go.

Detector for a skipped retro: `session-handoff` step 6 reports "retro: written <path>" or "retro: skipped --
<reason>"; a week with coordinator sessions and an empty inbox is a line of the weekly reduction.

## Недельное сведение (weekly reduction)

### Что где лежит

| Путь | Что |
|---|---|
| `docs/retro/inbox/` | сырые записи сессий, файл на сессию: `<ГГГГММДД>-<ЧЧММ>-<dev>.md`. Пишет только скилл `session-retro` |
| `docs/retro/classes.md` | классы после сведения: класс, сколько записей и каких, выбранная починка, находка и узел |
| `docs/retro/done/` | сведённые записи (переносятся из `inbox/` тем же ходом, что строка класса) |


### Порядок

Делает Архитектор при включении (пока его функция не введена — Lead на еженедельной калибровке). Порядок:

1. Прочитать все файлы `inbox/`.
2. Сгруппировать пункты по классу фабрики или форджа (не по сессии и не по файлу): «диспатч не называет читателей
   файла», а не «в t-889 не нашли пин».
3. По каждому классу решить одно из трёх и записать строкой в `classes.md`:
   - **чиним системно** — названо, что меняется (код, правило, инструмент) и почему это закрывает все записи класса;
     тогда — находка в `findings/` своей кучки и узел в невзятой пачке (PROJECT «Командная работа» п. 2);
   - **уже чинится** — ссылка на узел, который закрывает класс;
   - **не чиним** — причина; класс остаётся в `classes.md`, чтобы следующая запись того же класса увеличила счёт,
     а не открыла разбор заново.
4. Класс с одной записью узла не получает, пока не повторится, — кроме случая, когда запись называет дефект, из-за
   которого работа встала.
5. Вопросы владельцу из записей, оставшиеся без ответа, — одним списком владельцу.
6. Перенести сведённые файлы в `done/`.

Запись в `inbox/` старше двух недель — строка недельного сведения «сведение пропущено».
