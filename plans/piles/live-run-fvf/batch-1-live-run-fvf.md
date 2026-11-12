# Находки живого прогона LR2-1 — пачка 1: фабрика доходит до тестов без ручной помощи оператора

кучка: `live-run-fvf` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен | приоритет: П1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 12.11.2026 на прогоне LR2-1: «код не должен урезать бриф, фордж следит за длинной брифа»;
«а роль адаптировать слова человека для кода и запустить его не может? Дирижёр именно для этого и создавался»; «скажи фабрике
посмотреть список тестов ролью и автоматизировать все какие запланированно».
Порядок по общим файлам: `scripts/driver_gates.py`: FV1-7 → FV1-8; `scripts/question_register.py`: FV1-3 → FV1-9.
Скоуп свидетеля: по узлам, при взятии.
Общий бриф дизайнерам: находка узла + `experiments/mybooks/factory-vs-free-agent/notebook.md` («Ход прогона», «Журнал вопросов и
ответов») + логи `experiments/mybooks/factory-vs-free-agent/runs/factory-N.log`.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`; это оценка оператора прогона по сообщениям фабрики, Lead пачки уточняет
их скаутом при взятии.

Пополняется по ходу прогона LR2-1 (слово владельца 12.11.2026: «пополняй по мере прохождения прогона»).

## Бриф

Что сделать: узлы таблицы ниже; первыми FV1-1 и FV1-3 — без них фабрика не доходит до автотестов и спрашивает одно и то же
дважды. Направление в каждой находке — предложение оператора прогона (сессия Opus), Lead пачки выбирает его до дизайнера.
FV1-12 ждёт слова владельца о замысле S2. НЕ делать: правки в замороженном дереве релиза `C:\QAFactory\exp-fvf\pkg`.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV1-1 | П1 | Область S5 пуста: кейсы пишут строку плана `P-1`, читатель узнаёт только `TS-1` (`findings/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md`) | designer → builder → critic | `scripts/planning_contract.py` | — | ожидает |
| FV1-2 | П1 | Дирижёр не исполнил слово владельца на S5 — нет хода «область по слову человека / суждению роли» (`findings/20261112-dirizher-ne-ispolnil-slovo-vladelca-na-s5.md`) | designer → builder → critic | `scripts/driver_dispatch.py` | FV1-1 | ожидает |
| FV1-3 | П1 | Свободный ответ на пакет вопросов не идёт к дирижёру, роль не может закрыть вопрос (`findings/20261112-svobodnyj-otvet-na-paket-voprosov-ne-idet-dirizheru.md`) | designer → builder → critic | `scripts/question_register.py`, `scripts/driver_dispatch.py` | — | ожидает |
| FV1-4 | П1 | Срезка брифа на ходу режет слова человека; длину держит фордж (`findings/20261112-srezka-briefa-rezhet-slova-cheloveka.md`) | designer → builder → critic | `scripts/brief_pack.py` | — | ожидает |
| FV1-5 | П1 | Проба стенда ложно «не отвечает»: вход `POST /login` → 405 (`findings/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md`) | designer → builder → critic | `scripts/env_probe.py` | — | ожидает |
| FV1-6 | П1 | S2: нет двери «вернуть работу тестеру со словами критика» после исчерпания раундов (`findings/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md`) | designer → builder → critic | `scripts/driver_machine.py` | — | ожидает |
| FV1-7 | П2 | Гейт A показан до готовности («S5 can start: no») (`findings/20261112-gejt-a-pokazan-do-gotovnosti.md`) | designer → builder → critic | `scripts/driver_gates.py` | FV1-1 | ожидает |
| FV1-8 | П2 | Гейт A требует ответ на вопрос, отложенный «до отчёта» (`findings/20261112-gejt-a-trebuet-otvet-na-vopros-otlozhennyj-do-otcheta.md`) | designer → builder → critic | `scripts/driver_gates.py` | FV1-7 | ожидает |
| FV1-9 | П2 | Пакет вопросов: повторы, нет источников вариантов, «нельзя ответить как есть» показано человеку (`findings/20261112-s4-paket-voprosov-s-povtorami-i-bez-istochnikov.md`) | designer → builder → critic | `scripts/question_register.py` | FV1-3 | ожидает |
| FV1-10 | П2 | S1 не взяла выгрузку, названную в тексте стори (`findings/20261112-s1-ne-vzyala-vygruzku-nazvannuyu-v-tekste-stori.md`) | designer → builder → critic | `scripts/context_bundle.py` | — | ожидает |
| FV1-11 | П2 | S0 останавливается на тикете без `# ` (`findings/20261112-s0-ostanovka-na-tikete-bez-zagolovka.md`) | builder → critic | `scripts/ticket_adapter.py` | — | ожидает |
| FV1-12 | П2 | Карточка S2 и реестр стадий расходятся; замысел S2 — слово владельца (`findings/20261112-s2-kartochka-i-reestr-stadij-rashodyatsya.md`) | ждёт слова владельца → builder | `skills/qa-story/phases/s2.md`, `references/stages.json` | — | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 12.11 19:10 — пачка открыта оператором прогона LR2-1 (сессия Opus) по слову владельца; 12 находок первых полутора часов
  прогона (17:39–19:05).

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
