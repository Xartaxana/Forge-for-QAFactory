# Три вопроса замысла по свипу «роль послана читать плагин»: значения в формах `handoffs/*.yaml`, «verifying `scripts/hooklib.py`», указатель на `phases/s0.md`

id: — | кучка: `roles-context` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Свип класса OH3-14 («роль отправляют читать плагин», узел HF1-11, скаут t-063) дал 0 красных строк в группах путей плагина и 2 строки
RED по `vocabulary.` (q2-red1, q2-red2 — переданы узлу HF1-13 пачки hotfix-12586/1); остались три группы «неясно» — вопросы о замысле, которые скаут
не решает (digest `docs/tasks/specs/reports/t-063-hf1-11-sweeps.md`, раздел «Forks»). Они вынесены владельцу одной находкой.

(a) q2-hf-bare — формы `handoffs/*.yaml` несут `<one of vocabulary.X>` без значений (43 строки: `header_verdicts` в 17 формах, `row_states`
в 8, `unresolved_reasons` в 13, `critic_verdicts`, `repair_causes`, `execution_status`, `staleness_causes`). Роль заполняет форму,
скопированную `handoff_init` дословно (digest g2: `scripts/handoff_init.py:45-56,86-99`), и узнаёт допустимые значения только когда
`handoff_check` отказывает («One of: …», digest g3: `scripts/handoff_check.py:1159-1161,1182-1184`). Ни один текст не велит открывать
`vocabulary.yaml`, но значения `header_verdicts` не лежат ни в одном файле `references/` — роль узнаёт их только отказом. Рядом ряд полей тех же форм уже
даёт значения inline (`<one of vocabulary.X - a/b/c>`, группа q2-hf-inline: GREEN). Варианты: (i) форма сама перечисляет значения —
`handoff_init` подставляет их из словаря, как уже делают inline-формы вручную; (ii) как сейчас: значения узнаёт роль отказом
`handoff_check`; (iii) значения даёт справочник, который инжектируется роли. Рекомендация Lead пачки: (i) — один читатель словаря, ни
отказа ради знания, ни второй копии списка.

(b) q2-common — `references/common-rules.md:142-146`, инжектируется КАЖДОЙ роли (`inject-map.json:4-7`): «a nonempty CLAUDE_PLUGIN_ROOT after
verifying `scripts/hooklib.py`, else … `<root>/skills/<skill>/SKILL.md`». «Проверить» файл плагина через Read/Glob гард отказывает, через Bash — можно.
Вопрос: оставить ли формулировку, которая роли в части инструментов недоступна. Рекомендация Lead: убрать «after verifying `scripts/hooklib.py`».

(c) q2-adapters — `references/adapters-read.md:101,109`, инжектируется `qa-scout` (`inject-map.json:13`): «Mechanics: `phases/s0.md` §2b.» —
указатель на файл плагина, который гард роли не отдаёт; шаг свежести S0 исполняет оркестратор. Вопрос: нужен ли указатель в файле, инжектируемом
роли. Рекомендация Lead: убрать или вписать нужное inline.

Что сделать: после слова владельца — узел: (a) по выбранному варианту, (b) и (c) правка двух файлов с перегенерацией slices
(`contract_slices.py --write`) и проверкой `--limits` (потолки размеров общего слоя). До слова ничего не меняется.

Свидетель: `docs/tasks/specs/reports/t-063-hf1-11-sweeps.md`: строки q2-hf-bare, q2-hf-inline, q2-adapters, q2-common, g2, g3; «Forks» (Q2 UNCLEAR
groups: «(a) whether the first-fill form should list its closed values ... (b) whether "verifying `scripts/hooklib.py`" ... may be done through
Read/Glob ... (c) whether the "Mechanics: `phases/s0.md`" pointer ... belongs in a role-injected file»).

Принципы и правила: P15, FR-2, FR-15, FR-38, AR-8, AR-10.

Решение владельца нужно: да — три вопроса: (a) формы показывают допустимые значения сами (i), знают их из отказа (ii) или из справочника (iii); (b) убрать ли «verifying
`scripts/hooklib.py`» из общих правил; (c) убрать ли указатель на `phases/s0.md` из `adapters-read.md`. Рекомендации Lead: (a) i, (b) убрать, (c) убрать
или вписать inline.

Слово владельца 23.10.2026: (a) — вариант (i): `handoff_init` подставляет допустимые значения словаря в форму (ссылка на файл не обязывает
роль читать — получили бы и отказ, и длинный контекст; форма не входит в инжект A22); (b) — убрать; (c) — убрать (S0 делает код по фазе:
дирижёр в сессии скилла, драйвер в headless; скаут получает снимок). (b) и (c) сделаны в пачке `hotfix-12586/1` (t-072, d01cb502);
(a) — узел этой кучки.
