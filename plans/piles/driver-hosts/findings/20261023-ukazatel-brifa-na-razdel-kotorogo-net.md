# Бриф гейта A при переполнении отсылает к разделу «Rehearsal of gate A», которого в `work/gate-a-brief.md` нет

id: — | кучка: `driver-hosts` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: `gate_preflight.brief_lines` (`scripts/gate_preflight.py:4062`) при переполнении лимита строк (по умолчанию 5) печатает
счётчик и указатель «the whole list is under "Rehearsal of gate A" below» (`scripts/gate_preflight.py:4113`). Такой раздел есть только
в тексте гейта драйвера (`scripts/story_run.py:11137`, `parts.append(f"## Rehearsal of gate {gate}\n" + rehearsal)`); файл
`work/gate-a-brief.md`, который пишет `gate_brief.py --output`, раздела не содержит. Человек, читающий файл, получает указатель
в пустоту; задевает каждую находку гейта A после пятой.

Свидетель: `docs/tasks/specs/t-051-hf1-9-gw1-13.md` §8 Q3; отчёт `docs/tasks/handoffs/t-062-hf1-9.md` (R0, причина H1: поиск
`grep -n "Rehearsal of gate"` находит только `story_run.py:11137`, в `gate_brief.py` — ничего; контроль той же формой — «After your
approval» найден в `gate_brief.py:2135`). В HF1-9 указатель не правился: F-5 ((a) строки интеграции первыми) оставила дыру для
остальных проверок.

Что сделать: один из двух — `gate_brief.py --output` пишет раздел «Rehearsal of gate A» с полным списком, или указатель называет
то, что файл содержит; тест: бриф с шестью находками — каждая указанная точка существует в файле. Тот же класс, что L3 узла HF1-9
(«лимит режет, но не прячет»).

Принципы и правила: FR-10, FR-37, AR-13.

Решение владельца нужно: нет.
