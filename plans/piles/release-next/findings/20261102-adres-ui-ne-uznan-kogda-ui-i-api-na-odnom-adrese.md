# Фабрика спрашивает адрес UI стенда, на котором сама прошла UI-вход: UI и API на одном адресе приняты за «стенд без UI»

id: — | кучка: `release-next` | от: живой прогон LOCAL-1 (MyBooks, 0.10.8), гейт A, 02.11.2026; вопрос владельца 02.11.2026 («почему фабрика спрашивает
адрес UI стенда, когда сама уже проверила этот стенд на работоспособность?») | приоритет: П1 | кандидат наверх: нет

## Что наблюдалось

Носители — проект `D:/ws1/mybooks-stand\test-automation-framework`:

- `qa-factory/config.json`: `environment.frontend.url_key: ""` (по тексту `note` самого блока «empty = an API-only stand»);
  `environments[0]` = `{name: local, base_url: http://localhost:3000}` без `frontend`; `environment.access.kind: harness_command` —
  `tests/e2e/auth/login.spec.ts` (Playwright, UI), `login_probe.outcome: ok` (онбординг 31.10).
- `playwright.config.ts:33` — `baseURL: cfg.BASE_URL`; `.env`: `BASE_URL=http://localhost:3000`, `API_URL=http://localhost:3000/api` — UI и API на
  одном адресе (Next.js).
- Гейт A: требование кейса `{"stand_frontend": …}` → `gate_preflight._stand_frontend` (`scripts/gate_preflight.py:4232-4256`) →
  `env_probe.frontend_of` (`scripts/env_probe.py:347-391`) ищет только `frontend.url`/`frontend_url` записи стенда и `environment.frontend.url_key`
  → пусто → `unmet` → вопрос человеку об адресе UI.
- `pipeline.json` прогона: `"env_probe login: failed - node did not finish within 60s (the login test passes in ~80s); passed by the person's word"` —
  проба входа (тот самый UI-тест) отрезана жёстким потолком 60 с.

## Класс

Факт стенда, который фабрика уже доказала своей пробой (UI-тест проекта прошёл на `BASE_URL`), не засчитывается тем читателем, который
решает «известен ли адрес UI» (FR-18 наоборот, FR-41, AR-13, AR-28); онбординг монолита (UI и API на одном origin — Next.js, Rails, Django)
пишет «стенд только с API». Родственник W-2 (`plans/piles/hotfix-12586/findings/20261029-preduprezhdeniya-geita-a-stend-ne-uznan.md`: там
отдельный ключ `FRONTEND_URL` не связан); здесь отдельного ключа нет — адрес UI и есть `BASE_URL`. Не правило MyBooks.

## Что именно менять

Направление выбрано (Lead, 02.11.2026).

1. **Онбординг.** Когда UI-тесты проекта (профиль e2e/ui, `access.kind: harness_command` с UI-тестом, или `baseURL` раннера) ходят на значение
   `base_url_key`, онбординг пишет `environment.frontend.url_key = <base_url_key>` (и `api_path` — путь API под тем же origin, если он есть, как
   `API_URL`), а не пустое значение; пустое — только когда у проекта нет ни одного UI-теста и UI-профиля. Предложение показывается человеку
   именем ключа (не значением), подтверждение — одной строкой темы 2 (`skills/qa-onboarding/phases/p2-interview.md:168`). Тест: фикстура проекта
   с Playwright `baseURL: BASE_URL` и `API_URL` под тем же origin → `url_key: BASE_URL`; API-only фикстура → пусто.
2. **Чтение.** `env_probe.frontend_of` (один читатель, AR-13): если у записи стенда нет своего адреса UI, а у проекта есть UI-профиль и проба входа
   через UI-тест прошла (`access.login_probe.outcome: ok` на этом стенде), адресом UI считается `base_url` стенда, `source: "base_url (ui login
   probe)"`. Без UI-профиля — по-прежнему пусто (API-only). Тест: эта конфигурация MyBooks → `url` = base_url; та же без UI-профиля → пусто.
3. **Потолок пробы входа.** Потолок `env_probe login` берётся из записанной длительности проверки входа (онбординг пишет `access.login_probe.seconds`;
   потолок = 2 × записанного, не меньше 60 с), а не фиксированные 60 с; таймаут говорит «проба не уложилась в N с (тест идёт ~M с)», не «failed».
   Тест: записано 80 с → потолок 160 с.
   Точное место (разбор t-1666, П-5): `scripts/stand_access.py:61` `COMMAND_MIN_TIMEOUT_S = 60.0` и `:181` `max(timeout, 60)`; в `config.json`
   `access` ключа срока нет, команда гоняет весь `login.spec.ts`, онбординг длительность пробы не сохранил — предупреждение тянется через все 44 события
   прогона. Правка: потолок идёт из `access.login_probe.seconds` (ключ с запасным значением, AR-3), константа остаётся только запасным дном.

Сосед: W-2 (адрес в отдельном ключе) и HF5-* («один читатель адреса фронтенда») — пп. 1–2 закрывают оба случая одним путём; дизайнер сверяет, что
W-2 сделан в 0.10.7, и если нет — включает его в этот узел.

## Принципы и правила

P5, P13; FR-18, FR-41, FR-50, FR-59; AR-3, AR-13, AR-28.

## Связи

- Разбор прогона: `docs/tasks/specs/reports/t-1666-local-1-run-review.md`.

Решение владельца нужно: нет.

## Повтор LOCAL-1 (02.11.2026)

Прогон LOCAL-1 (t-1671 Н-15): адрес UI снова спрошен на гейте A (`case_preconditions-1…16`), хотя фабрика сама прошла UI-вход. Узел RN1-3 не выполнен к моменту прогона; новых требований нет, тест п. 2 (`env_probe.frontend_of` засчитывает пройденную UI-пробу) должен покрыть карточку гейта A: вопрос об адресе UI не строится, если проба входа по UI прошла.
