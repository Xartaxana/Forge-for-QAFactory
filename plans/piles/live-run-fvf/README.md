# Находки живого прогона «фабрика против свободного агента» (`live-run-fvf`)

приоритет: П1 | фичи: F19 | стенд: нужен | зона: —

## Зачем

Прогон LR2-1 (12.11.2026, релиз 0.11.0, стори MyBooks «Add to Cart») сравнивает фабрику со свободным агентом. Свободный агент
закончил за 13 минут с двумя багами и 20 автотестами; фабрика за полтора часа остановилась у человека больше десяти раз и
дошла до S5 с пустой областью автоматизации. Здесь — всё, что прогон показал работающим неправильно: остановки без нужды,
слова человека, которые не доходят, и стыки ролей, которые не читаются. Слово владельца: «создай кучку находок по живому
прогону… пополняй по мере прохождения прогона».

## Что не так сегодня (факты)

- S5 без единого теста: кейсы пишут строку плана `P-1`, читатель — `TS-1` (`experiments/mybooks/factory-vs-free-agent/runs/factory-10.log`).
- Ответ человека на 18 вопросов дошёл до стратега обрезанным до 240 символов (`work/briefs/S3-qa-test-strategist-3.md` копии плеча, строка 49).
- Ход прогона и каждый ответ с пометкой, чьи слова: `experiments/mybooks/factory-vs-free-agent/notebook.md`.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | фабрика доходит до тестов без ручной помощи оператора; слова человека доходят и исполняются | FV1-1…FV1-30 | L | ожидает | — | — | — |
| 2 | читатели и носители, найденные критиками 13.11.2026: `_plan_row_of`, `BY_LEAF`, `py.test`, выходы без читателя и мелкие хвосты | FV2-1…FV2-9 | M | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с FV1-1 и FV1-3: без них фабрика не доходит до автотестов и спрашивает одно и то же дважды. Стенд нужен (живое
доказательство — повтор прогона LR2-1). FV1-12 ждёт слова владельца о замысле S2. Подробно — `batch-1-live-run-fvf.md`.

## Дороги

Читать по порядку: эта карточка → `batch-1-live-run-fvf.md` → находка узла → `experiments/mybooks/factory-vs-free-agent/notebook.md`
(«Ход прогона», «Журнал вопросов и ответов») → логи `runs/factory-N.log` → код по именам из находки.
Слова: `question_register.parse_choices`, `brief_pack`, `env_probe`, `stage-scope`, `driver_gates`, `waiver.py`, `stages.json`.
Не читать: соседние кучки — находки этого прогона собраны здесь.

## Содержание

Снимок 12.11.2026; пути — от корня форджа; суть — из файлов находок. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md` | находка | Кейсы пишут строку плана `P-1`, читатель узнаёт `TS-1` — область S5 пуста, ни одного теста | `scripts/` (stage-scope) | пачка 1, FV1-1 | нет | FB-5 дирижёра; LR2-1 |
| `findings/20261112-dirizher-ne-ispolnil-slovo-vladelca-na-s5.md` | находка | Дирижёр не исполнил «роль сама смотрит список тестов и автоматизирует» — записал находкой | `scripts/` (дирижёр, S5) | пачка 1, FV1-2 | да, 12.11.2026 | FB-6 дирижёра; LR2-1 |
| `findings/20261112-svobodnyj-otvet-na-paket-voprosov-ne-idet-dirizheru.md` | находка | Ответ своими словами обходит дирижёра; роль не закрывает вопрос; пакет спрошен второй раз | `scripts/question_register.py` | пачка 1, FV1-3 | да, 12.11.2026 | LR2-1 |
| `findings/20261112-srezka-briefa-rezhet-slova-cheloveka.md` | находка | Код урезает бриф на ходу, ответ человека обрезан до 240 символов | `scripts/brief_pack.py` | пачка 1, FV1-4 | да, 12.11.2026 | LR2-1 |
| `findings/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md` | находка | Проба стенда «не ответил»: вход `POST /login` → 405, стенд жив | `scripts/env_probe.py` | пачка 1, FV1-5 | нет | LR2-1 |
| `findings/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md` | находка | После исчерпания раундов S2 `restart` перезапускает критика, к тестеру хода нет | `scripts/` (дирижёр, S2) | пачка 1, FV1-6 | нет | LR2-1 |
| `findings/20261112-gejt-a-pokazan-do-gotovnosti.md` | находка | Гейт A показан, хотя репетиция: «S5 can start: no» | `scripts/driver_gates.py` | пачка 1, FV1-7 | нет | LR2-1 |
| `findings/20261112-gejt-a-trebuet-otvet-na-vopros-otlozhennyj-do-otcheta.md` | находка | Решение гейта A не пишется из-за вопроса, отложенного «до отчёта» | `scripts/driver_gates.py` | пачка 1, FV1-8 | нет | LR2-1 |
| `findings/20261112-s4-paket-voprosov-s-povtorami-i-bez-istochnikov.md` | находка | 18 вопросов, шесть повторов, варианты «from ?», дефектные вопросы показаны человеку | `scripts/question_register.py` | пачка 1, FV1-9 | нет | LR2-1 |
| `findings/20261112-s1-ne-vzyala-vygruzku-nazvannuyu-v-tekste-stori.md` | находка | Выгрузка, названная в тексте локальной стори, не стала источником S1 | `scripts/` (источники S1) | пачка 1, FV1-10 | нет | LR2-1 |
| `findings/20261112-s0-ostanovka-na-tikete-bez-zagolovka.md` | находка | S0 останавливает стори вопросом, когда в тексте нет `# ` | `scripts/` (адаптер `file`) | пачка 1, FV1-11 | нет | LR2-1 |
| `findings/20261112-dirizher-ne-ispolnil-vybrannyj-variant-go-on.md` | находка | Ответ `go on` из предложенных вариантов не исполнен: дирижёр судил по прежним словам, спросил третий раз | `scripts/driver_dispatch.py` | пачка 1, FV1-13 | да, 12.11.2026 | LR2-1 |
| `findings/20261112-onbording-zapisal-vhod-kodom-nevozmozhen-oshibochno.md` | находка | Онбординг ошибочно записал «вход кодом невозможен» (POST на страницу); S5 стоит на этом отказе | `scripts/stand_access.py`, `scripts/env_probe.py` | пачка 1, FV1-15 | да, 12.11.2026 | FV1-5; LR2-1 |
| `findings/20261112-s5-lichnost-stenda-sprashivaet-kommit-repo-testov.md` | находка | Вопрос о сборке стенда называет коммит репозитория тестов; «current code» с S0 не учтён | `scripts/driver_gates.py` | пачка 1, FV1-16 | нет | LR2-1 |
| `findings/20261112-onbording-ne-umeet-opredelit-kak-vojti-na-stend.md` | баг | Онбординг не определяет вход на стенд: POST на страницу → «кодом нельзя»; NextAuth и обвязка не испробованы | `scripts/stand_access.py`, онбординг | пачка 1, FV1-17 | да, 12.11.2026 | FV1-15; LR2-1 |
| `findings/20261112-kontrakt-selektorov-nikogda-ne-proveren.md` | находка | Регрессия: без проверенных селекторов раннер отказывает запускать тесты; запись первого взгляда не читается | `scripts/execution_request.py`, `scripts/profile_contract.py` | пачка 1, FV1-18 | да, 12.11.2026 | LR2-1 |
| `findings/20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md` | находка | S5 требует `obligation_refs`, которые для тестов на TS не произвести (читатель маркера только Python); рукописное значение проверка пропускает; починка «не вопрос человеку» ставится человеку | `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, `scripts/story_run.py` | пачка 1, FV1-19 | нет | LR2-1, FV1-13 |
| `findings/20261112-kritik-koda-ne-zapuskaet-proby.md` | находка | Критик кода S5 не запускает пробы чувствительности и не называет причину; дирижёр ложно говорит человеку, что фабрика пробы не может | хартия S5 qa-code-critic, `scripts/driver_dispatch.py` | пачка 1, FV1-20 | нет | LR2-1, FV1-13 |
| `findings/20261112-cena-lozhno-nepolnaya-iz-za-shagov-koda.md` | находка | Цена помечена «not every session is recorded», хотя записаны все сессии: ходы кода `gate_repair` считаются звонками без сессии | `scripts/task_price.py` | пачка 1, FV1-21 | нет | LR2-1 |
| `findings/20261113-s7-petlya-dirizhera-na-prieme-s6.md` | находка | S7 по кругу: приёмка S6 из формы аналитика требует полей, которых в форме нет; дирижёр без конца повторяет разбор аналитика с причиной `tooling` | `scripts/stage_done.py`, `scripts/driver_dispatch.py` | пачка 1, FV1-22 | нет | LR2-1, FV1-13 |
| `findings/20261113-sravnenie-dokumenty-produkta-ne-prochitany.md` | находка | Сравнение (а, е): документы продукта не в реестре требований, вопросы владельцу о записанном | инвентарь источников S0/S2 | пачка 1, FV1-23 | нет | LR2-1 сравнение |
| `findings/20261113-sravnenie-chernoviki-bagov-ne-podtverzhdeny.md` | находка | Сравнение (б, в): черновики багов ручного прохода без вердикта; ожидание «выведено» без вопроса | хартия S6/S7 | пачка 1, FV1-24 | нет | LR2-1 сравнение, FV1-22 |
| `findings/20261113-sravnenie-net-krasnyh-testov-na-bagi.md` | находка | Сравнение (ж): ни один автотест не падает на найденной поломке | хартия S5/S7 | пачка 1, FV1-25 | нет | LR2-1 сравнение, FV1-20 |
| `findings/20261113-sravnenie-ne-udalos-eto-svoya-nedodelka.md` | находка | Сравнение (з): «не удалось проверить» смешивает невозможность и недоделку | форма отчёта | пачка 1, FV1-26 | нет | LR2-1 сравнение, FV1-18 |
| `findings/20261112-s2-kartochka-i-reestr-stadij-rashodyatsya.md` | находка | Карточка S2 «один диспатч», `stages.json` — критик-приёмщик; замысел S2 — вопрос владельцу | `skills/qa-story/phases/s2.md`, `references/stages.json` | пачка 1, FV1-12 | нужно | LR2-1 |
| `findings/20261113-trebovanie-proverki-rol-uznaet-v-moment-otkaza.md` | находка | Требование проверки роль узнаёт в момент отказа: три новых экземпляра; один механизм на класс, не строка на отказ | `scripts/hooklib.py`, `scripts/guard_pre_tool.py`, `scripts/refusal_registry.py` | пачка 1, FV1-27 | дано 13.11.2026 | LR2-1, FV1-18, FV1-19; `onboarding-hooks`, `driver-hosts`, `execution-probes` |
| `findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md` | находка | «Первый взгляд» не доходит до автоматора S5 по существу, в прогоне он к тому же пуст по ложному «no stand» | `scripts/brief_pack.py`, `scripts/first_look.py` | пачка 1, FV1-28 | дано 13.11.2026 | LR2-1, FV1-5, FV1-29 |
| `findings/20261113-avtomatoru-ne-dan-hodok-po-stendu.md` | находка | У автоматора S5 нет ходока по стенду: не может сам посмотреть, когда первый взгляд пуст или неверен | `agents/qa-automator.md`, `scripts/brief_pack.py` | пачка 1, FV1-29 | дано 13.11.2026 | LR2-1, FV1-28, FV1-18 |
| `findings/20261113-zapret-bez-dveri-s5-precheck-slovo-ne-provodit.md` | находка | 7 семейств `s5_precheck` не проходят ни по какому слову человека; класс — проход словом с записью | `scripts/s5_precheck.py`, `scripts/exit_gate.py` | пачка 1, FV1-30 | дано по классу; открытое ожидание — отдельная идея | спека сухой стори R-L5; FV1-19 |
| **Пачка 2** | | | | | | |
| `findings/20261113-chitatel-plan-row-chitaet-klyuch-kotorogo-net-v-kontrakte.md` | находка, id — | `_plan_row_of` читает ключ шапки `plan_row:`, которого нет в контракте кейса; читать через `contract.case_plan_row` | `scripts/handoff_check.py`, `references/form-rounds.json` | пачка 2, FV2-1 | нет | критик P1-a (P2); FV1-14 |
| `findings/20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md` | находка, id — | Метка «заполняет код» по имени листа `requirements` покрывает поля S3/S8, которых код не заполняет; ключ — полный путь | `scripts/handoff_check.py` | пачка 2, FV2-2 | нет | критик P1-a (P5); FV2-1 |
| `findings/20261113-py-test-dva-chitatelya-odnogo-voprosa-vybor-po-id-uzla.md` | находка | `is_pytest_command` и `node_id_selection` по-разному отвечают на `py.test`; единственный ответ — ключ данных | `scripts/execution_request.py`, `scripts/run_suite.py` | пачка 2, FV2-3 | нет | FV1-18 (K2, FIX-1) |
| `findings/20261113-vyhody-stadii-kotorye-ne-otkazyvaet-ni-odin-chitatel.md` | находка | 8 выходов стадий, которых не отказывает ни один читатель, 6 не покрыты; `requirements-readiness.json` без `verdict` проходит | `scripts/validate_artifacts.py` | пачка 2, FV2-4 | нет | критик P1-a (P6, Q1) |
| `findings/20261113-ledger-krasnyh-strok-sklevaet-povtornyj-id-cherez-i.md` | находка | Реестр красных строк сливает повторный id через И, второй кейс скрыт; повторный id — отказ | реестр красных строк P1-a | пачка 2, FV2-5 | нет | критик P1-a (Q2) |
| `findings/20261113-chastnyj-vyzov-i-dvojnoj-gard-papki-zhurnala-progona.md` | находка | Частный `runtime_paths._package_fingerprint` из `driver_journal`; гард «строка не создаёт папку стори» в двух копиях | `scripts/runtime_paths.py`, `scripts/driver_machine.py` | пачка 2, FV2-6 | нет | критик P1-v (QUEUE-3, QUEUE-4) |
| `findings/20261113-tekst-s5-md-ob-otkazah-markera-ustarel-posle-fv1-19.md` | находка | `s5.md:309-311` называет отказ маркера «не в строке плана кейса», маркер судится по всему плану | `skills/qa-story/phases/s5.md` | пачка 2, FV2-7 | нет | FV1-19 (Q-2) |
| `findings/20261113-role-load-ne-proveryaet-tipy-allowances-brief.md` | находка | `role_load.settings` не проверяет типы `allowances.brief` / `brief_charter_head`: сырой `ValueError` | `scripts/role_load.py` | пачка 2, FV2-8 | нет | FV1-4 (Q7) |
| `findings/20261113-formy-vybora-testa-tolko-dlya-pytest-i-playwright.md` | находка | «Селекторы проверены» читается только у `pytest` и `playwright-test`; jest, vitest, dotnet-test навсегда `no_selection_form` | `references/launch-causes.json` | пачка 2, FV2-9 | нет | FV1-18 (QUEUE); FV2-3 |
| `findings/20261113-tri-razbiratelya-id-nahodki-i-chetvyortyj-chitatel-strok-slova.md` | находка, id — | три разборщика тега id находки и четвёртый читатель строк слова человека: один выживший в модуле без `waiver` | `scripts/waiver.py`, `scripts/s5_precheck.py`, `scripts/exit_gate.py`, `scripts/controller.py` | пачка 2, FV2-10 | нет | критик темы FV1-30b (F5); FV1-30 |
| `findings/20261113-left-with-you-pod-b-ne-odna-stroka-dannyh-build-left-items.md` | находка, id — | «Left with you» под (b) — строка данных плюс ветка `build_left_items`: поправить фразу спеки F4 (или перенести в таблицу) | `docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md`, `scripts/check_delivery.py` | пачка 2, FV2-11 | нет | критик темы FV1-30b (F8); FV1-30 |
| `findings/20261113-record-person-pass-pishet-jsonl-mimo-hooklib-append-jsonl-line.md` | находка, id — | `_record_person_pass` дописывает jsonl мимо `hooklib.append_jsonl_line` (ось карты 29) | `scripts/controller.py` | пачка 2, FV2-12 | нет | критик темы FV1-30b (Axis 29); FV1-30 |
| `findings/20261113-perepis-vyhodov-draivera-dva-klona-chitatel-json-i-hesh-prompta.md` | находка, id — | два клона переписи выходов драйвера: строгий читатель JSON (`known_red`) и хэш промпта (`author_input_sha`) | `scripts/tests/dry_exits.py`, `scripts/tests/known_red.py`, `scripts/tests/dry_stub.py` | пачка 2, FV2-13 | нет | критик узла P1-b N1 (F9, F10) |
| `findings/20261113-perepis-vyhodov-draivera-dolgi-lead-n-l-i-put-ci.md` | находка, id — | долги слияния N1 (N-L: оси карты 18/34/17, вопрос 9, путь реестра, ключ `keep` N3) и перепись вне пути CI | `docs/SIBLING_MAP.md`, `docs/tasks/critic-diff-brief.md`, `scripts/tests/test-layers.json` | пачка 2, FV2-14 | нет | критик узла P1-b N1 (F12) |
| `findings/20261113-run-suite-i-story-budget-bez-zapisi-v-reestre-otkazov-klass-po-route.md` | находка, id — | у текстов `executor_unavailable` и `STORY BUDGET` нет записи в реестре отказов; класс — строками `route:<name>` переписи | `scripts/tests/fixtures/driver-exits/classes.json`, `scripts/tests/dry_exits.py` | пачка 2, FV2-15 | нет | критик узла P1-b N1 (F1, Q1); слово Lead |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- FV1-12: что такое S2 по замыслу — «первый взгляд, смоук» или «реестр требований и размер»; нужен ли на S2 критик-приёмщик.
