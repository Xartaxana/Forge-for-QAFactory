# Стенд без docker: ручная проверка уходит в тупик вместо вопроса «та ли версия на стенде»

id: — | кучка: `execution-probes` | от: Lead (Opus, деградированное окно), 31.10.2026, прогон CART-1 (MyBooks, `mybooks-stand`) | приоритет: П1 | кандидат наверх: нет

Слово владельца 31.10.2026 на вопрос «почему фабрика не может, если приложение открывается в браузере»: «Так она должна спросить
в таком случае пользователя, правильная ли версия на стенде, и всё».

## Что наблюдалось

Прогон CART-1 на втором проекте, MyBooks: Next.js запущен на хосте через `npm start`; в docker крутятся только `mybooks-mailpit-1`
и `mybooks-db-1`; тесты — Playwright на node; в `qa-factory/config.json` один профиль `web` (capabilities `web`, `api`). На S6
`qa-runner` вызвал `manual_capture.py http` и `ui` для CART-1_TC_011/012. Оба кейса ушли в `env_blocked` с `do_not_retry`, owner
`factory`: «no runtime probe is registered for profile api / e2e-ui (config execution.runtime_probes)». При этом env_probe прошёл:
health 200, вход по логину работает. Подсказка «`runtime_probe.py --suggest --profile e2e-ui --write`» не помогла: сначала «pass
--checkout», потом «more than one container is running (mybooks-mailpit-1, mybooks-db-1). Which one runs the application under
test?». Приложение не работает ни в одном контейнере.

Проверено Lead на копии конфига стенда (scratch, без записи на стенд):
- `runtime_probe.py --task CART-1 --profile web --environment local --checkout <MyBooks> --no-evidence` без `--container` →
  `result: unknown`, `asks_person: how`, «no container is named for this profile»;
- после `stand_identity.py confirm --task CART-1 --environment local --profile web --revision a25b0801… --words "..."` та же проба →
  `result: person_confirmed`, `identity_kind: person_confirmed`; `manual_capture.stand_probe` такой ответ принимает
  (`profile_contract.acceptable_provenance`, ACCEPTS);
- строка реестра `stand_identity.py record --method command --command "git -C ../MyBooks rev-parse HEAD"` → `matched` (вторая,
  кодовая дверь для проекта, который хочет не отвечать на вопрос в каждой истории).

Механизм вопроса есть и для стенда без docker работает. Фабрика до него не доходит по трём причинам.

## Класс

Ручная проверка и проба версии стенда рассчитаны на устройство проекта Test Project 1: профили с именами `api` и `e2e-ui`, приложение в
docker-контейнере, браузер из python-харнесса с pytest. Проект другого устройства получает тупик, где код должен задать закрытый
вопрос человеку (P2, P22; AR-1, AR-3, AR-17, AR-28; FR-2, FR-59).

## Что именно менять

1. **`scripts/manual_capture.py`: профиль — из конфига проекта, не литерал.** Сегодня в коде `profile = "e2e-ui"` (команда `ui`,
   ~стр. 1544) и `profile = "api"` (команда `http`, ~стр. 2077); оба попадают в `stand_probe` → `execution_request.registered_probe`.
   Нужно: одна функция «профиль проекта для поверхности» — профиль, в `capabilities` которого есть `web` (для `ui`) или `api` (для
   `http`), с выбором `e2e-ui`/`api` по имени только как правилом совпадения, а не единственным вариантом. Ни одного профиля с такой
   capability → отказ с дверью (FR-1). Несколько → берётся профиль из запроса или сцены кейса; неоднозначно → вопрос дирижёру, не
   выбор наугад. Тест: фикстура с одним профилем `web` (capabilities web+api) — `http` и `ui` идут в `stand_probe` с `web`; фикстура
   Test Project 1 (`api` + `e2e-ui`) — поведение прежнее.
2. **Нет записи о пробе или ответ `unknown` у стенда без docker — вопрос человеку, не `env_blocked`.** Сегодня `stand_probe` бросает
   `EnvBlocked(..., "factory")` с советом `--suggest` (~стр. 947). Нужно: при отсутствии записи `runtime_probes` проба запускается
   с умолчанием из конфига (`--profile <профиль>`, `--environment <среда>`, `--checkout` из `implementation_repos[role=application]`,
   без `--container`). `unknown` с `asks_person` ведёт к одному закрытому вопросу по `human-questions.md` через шов к дирижёру
   (AR-17, P22): «На стенде <base_url> работает версия <короткий sha> (<ветка>, `git rev-parse HEAD` в <checkout>)? да / нет,
   другая / не знаю». «Да» исполняется кодом: `stand_identity.py confirm --task <T> ... --revision <HEAD>` со словами человека.
   «Нет» — кейс ждёт; дирижёр предлагает обновить стенд (`bring_up` среды). «Не знаю» — пробел в отчёте, без зелёного (FR-59).
   Одно слово действует на всю историю, пока не сдвинулся HEAD (это уже делает `voided.checkout`). Тест: фикстура без
   `runtime_probes` и без контейнеров — первый вызов возвращает вопрос, а не `env_blocked`; после `confirm` захват идёт.
3. **`scripts/runtime_probe.py --suggest` для стенда без docker.** В `suggest()` (~стр. 1268) нет ветки «приложение не в
   контейнере»: отказ «more than one container is running… Pass --container»; а в отказе «no running container» стоит дверь «pass
   --container <name> if the stand is not a docker one» — по ней пройти нельзя (FR-2). Нужно: вариант «приложение не в
   контейнере» (флаг или ответ на вопрос о контейнере) пишет запись без `--container`; тогда версию подтверждает человек по п. 2,
   либо проект записывает кодовый способ строкой реестра `method: command`. Тест: `--suggest` при двух чужих контейнерах и флаге
   «не в контейнере» пишет запись без `--container`.
4. **Соседний класс (сделать тем же узлом или записать остатком):** `harness_argv()` выводит интерпретатор браузера только из
   профиля `e2e-ui`, в команде которого есть `pytest`; `_browser_door` советует `poetry run python -m playwright install`. У проекта
   с Playwright на node такого профиля нет. Пока у python фабрики есть Playwright, перезапуск в харнессе не нужен, но дверь в отказе
   описывает только устройство Test Project 1.

Сосед: EP1-24 (`runtime_probes` пишется до S5: онбординг и гейт A зовут `--suggest`, несколько контейнеров → вопрос). П. 3 этой
находки — ветка того же `--suggest`, делать одним ходом. EP1-41 (desktop/mobile: руки агента только http и браузер).

Обход для текущего прогона CART-1 (передан сессии прогона 31.10.2026): запись `execution.runtime_probes."*"` с `--profile web
--checkout ../MyBooks` без контейнера, вопрос человеку, `stand_identity.py confirm`. Живьём захват после обхода не проверен.

Принципы и правила: P2, P22, FR-1, FR-2, FR-59, AR-1, AR-3, AR-9, AR-17, AR-28.

Решение владельца нужно: нет. Направление задано словом 31.10.2026.
