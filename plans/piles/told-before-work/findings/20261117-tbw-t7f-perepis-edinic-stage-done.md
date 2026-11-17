# Перепись единиц `stage_done` → conductor

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: единицы без строки роли числятся за ролью: ни один файл агента и ни одна запись role-commands не называет `stage_done` (AR-20, AR-29).

Что именно менять: `scripts/tests/fixtures/judgment-census.json`: единицы `stage_done.py` → `roles: ["conductor"]` с `note` «no agent file and no role-commands entry names stage_done (wave0 §3e trail §T)»; `refused` (хелпер самопроверки, census :952) — вместе с остальными, `note` говорит об этом. Потолки только вниз (E-T4b-1). Код `stage_done.py` и `test_stage_done.py` (карантин) не трогать. Файл данных одним узлом; фрагмент changelog — по слову Lead (S-4).

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T7f» — читать там, не копировать сюда.

Свидетель: спека wave0 §3e; F-W2 (a).

Принципы и правила: AR-20, AR-29.

Решение владельца нужно: нет.
