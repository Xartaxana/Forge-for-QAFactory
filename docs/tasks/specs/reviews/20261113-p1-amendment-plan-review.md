# Критик на план: поправка к П1-б / П1-в по словам владельца 13.11.2026

Предмет: `docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` (дальше — «поправка», ссылки `A:<строка>`).
Базовые спеки не пересматривались (t-401 их уже прошёл); смотрел только поправку и её стыки с ними.
Факты пакета — только `.claude/worktrees/read-main/ai-packages/qa-factory/` (HEAD `fb36ae5`, 2026-11-13 15:05 +0100; `PKG` ниже).
Планы: «план» = `20261113-plan-fabrika-ne-huzhe-agenta.md`, П1-б = `20261113-p1b-dry-story-spec.md`,
П1-в = `20261113-p1v-run-scoreboard-spec.md`, механизм = `20261113-told-before-work-mechanism-spec.md`.

Итог: **fit after fixes** (годится после правок), блокирующих — **7**, неблокирующих — 12.

---

## Блокирующие находки

### Б1. Тип для спайка (MyBooks `local-1-0108`) попадает под край A1-E1 из самой поправки: сырых ответов трекера в снимке нет (K6, K9, K10)
- Поправка берёт из снимка только «сырые ответы трекера/VCS (`raw.json`, `*.diff`)»; `ticket.json` снимка «НЕ вход» (A:85).
  A1-E1 (A:149): снимок без сырых ответов → тип строится только по F-A1-4; Lead выбрал F-A1-4 (б) «тип не берётся» (план `:474`).
  При этом F-A1-1 (а) — спайк N0 на MyBooks `local-1-0108` (A:160, план `:472`).
- Проверил: `find PKG/scripts/tests/fixtures/stories/local-1-0108 -name raw.json` → 0 файлов; в `work/sources/` 29 источников, внутри
  только `ticket.json` (58 файлов, `uniq -c` → `58 ticket.json`). Первый же `ticket.json`
  (`work/sources/SRC-1a8882c6347d792501ee/assessment/ticket.json`) — нормализованная форма фабрики (`acceptance_criteria`,
  `attachment_names`, `depth`), то есть выход кода 0.10.8. Положительный контроль той же командой: у `investigation-14857/TP1-14857`
  `raw.json` есть в 8 источниках (`.../SRC-5ed252fcfa756899ddd1/assessment/raw.json` — ответ Jira REST `{"expand":…,"key":"TP1-217"…}`).
- Итог: по правилам самой поправки тип MyBooks строить не из чего; выбранный спайк неисполним без конвертера, который Lead
  запретил (F-A1-4 (б)). Строка таблицы A1 (A:70) про «~30 источников» верна, но умалчивает, что это `ticket.json`, а не сырые ответы.
- Минимальная правка (выбор за Lead): либо (i) F-A1-1 → (б) CodeMie 14857 (сырые ответы есть, корпус вычищен, K5), MyBooks — после
  того, как названо, где лежит ВХОД трекера LOCAL (если `LOCAL-1` берётся из файла проекта MyBooks — назвать этот файл и строку
  раннера, тогда A1-E1 не срабатывает); либо (ii) явное исключение «`ticket.json` трекера LOCAL — это и есть сырой ответ, потому что
  у LOCAL нет API» с проверкой на файле, записанное в A1 и A1-E1. Без одного из двух узел N0 упрётся в A1-E1 в первый же день.

### Б2. C11 / N3a читают записанный бриф — против принятого решения F9 механизма (K6, K10)
- Поправка: C11 — «id проверки есть в карточке „что у тебя проверят“ её брифа того же диспатча» (A:175-176), источник «сказано» —
  «бриф диспатча — `work/briefs/<dispatch>.md`» (A:187-188), отрицательный контроль N3a — «на КОПИИ брифа без строки карточки →
  красное» (A:205), A2-E3 — «бриф не найден / нечитаем → красное с путём» (A:216).
- Механизм §7 (`told-before-work-mechanism-spec.md:156`): C11 вызывает `brief_pack.requirement_rows(role, stage, kind)` — «no brief
  parse, F9»; §9 F9 (`:181`) рекомендует «call (one reader)»; Lead принял: «F9 — C11 вызывает `brief_pack.requirement_rows`» (план `:468`).
  Также механизм §2 (`:76`): `{"card": true}` удовлетворяется, когда `requirement_rows` возвращает строку, «the walker CALLS it; no anchor copy».
- Поправка оставляет заглушку `<told_rows reader>` (A:187), хотя имя читателя уже назначено. Две дороги к одному факту (разбор
  брифа и вызов читателя) — то, что F-A2-1 (а) и P31 запрещают.
- Минимальная правка: C11 и `told_before_work` вызывают `brief_pack.requirement_rows(role, stage, dispatch_kind)`; отрицательный
  контроль — на КОПИИ файла строк требований без строки для (роль, стадия) или с чужой ролью; A2-E3 переписать на «читатель
  строк не отвечает / файл строк нечитаем → красное с путём». Мир «до посадки механизма» (A:191-194, `stage_joints`) остаётся.

### Б3. Требование 1 узла FV1-30 по нетеговой дороге возвращает t-108 для всех семейств (K3)
- Требование 1 (A:272-273): «`_passable`: проходимо любое семейство, КРОМЕ тегов исключения 2 и `then-remainder-unrecorded-*`».
  Требование 3 (A:275-279) правильно называет запрещённое направление — «провести находку, которую слово НЕ называло (t-108)».
  Но дорогу сопоставления поправка не выбирает, а сегодняшний код даёт две дороги:
  `s5_precheck.py:3997-3999` — находка, проходимая по ТЕГУ, видит только слова, называющие тег, или `*` (`tag_words`, `:3983-3987`);
  находка, проходимая по СЕМЕЙСТВУ, видит ВСЕ слова стадии (`pipeline`). `waiver.split_overridden` (`waiver.py:216-217`)
  пропускает строку, если слово `*` или `contract.names_whole(match, text)`, а `text` = id + message + fix + напечатанная строка
  (`s5_precheck.py:3995`), и id несёт id кейса (`<check>:<case>:<tag>`, `:266-268`).
- Сценарий: в `stage_overrides` лежит слово `{match: "TP1-13797_TC_002", decision: "run row not needed"}`, данное на находку
  `run_mapping:TP1-13797_TC_002:no-row-…`. Если `_passable` просто расширить семействами (буквальное требование 1), находка
  `bindings:TP1-13797_TC_002:no-bindings` идёт нетеговой дорогой, `names_whole("TP1-13797_TC_002", text)` → True, и Then проходит
  молча словом, которое о нём ничего не говорило. Это ровно t-108 (`:3968-3972`), только теперь на семь семейств, а не на одно.
- Строка неудобных входов «слово, совпадающее со словом в сообщении (`case`), но не с тегом» (A:278) называет вход, но не говорит,
  каким должен быть исход и через какую дорогу; поведение `*` A3-E2 оставлено узлу («решает узел FV1-30; в строке обхода оба
  варианта», A:291) — против PROJECT.md «Командная работа» п. 11 (направление выбрано, а не перечислено).
- Минимальная правка: в требование 1 дописать дорогу: «каждая находка, ставшая проходимой, проходит только словом, чей `match`
  называет её ТЕГ или её id целиком, или `*` (та же дорога, что `tag_words`, `:3983-3987`); названное по id кейса или по тексту
  сообщения её не проводит»; для `*` выбрать одно поведение (рекомендация: `*` проводит, как сегодня у тегов, `:3985`; проход
  записан — P13) и записать его в A3-E2. Строки неудобных входов дополнить исходами.

### Б4. F-A3-5 (а): писателя-дороги нет — контроллер вывод `s5_precheck` не читает, а узел FV1-30 не владеет `controller.py` (K3, K8, K9)
- F-A3-5 (а) (A:302; план `:477`): «`s5_precheck` возвращает структурное поле `passed_by_word: [{id, decision}]`, контроллер/exit gate
  пишет через `_record_person_pass`».
- Проверил: `_record_person_pass` — метод `Controller` (`controller.py:2389`), единственный писатель `state/passed-by-person.jsonl`
  (Grep `passed.by.person` `-i` по `PKG` → в `scripts/` пишет только `controller.py:2402`; утверждение поправки о едином писателе
  верно). Но Grep `exit_gate|precheck` (`-i`) по `controller.py` → одна строка-комментарий (`:990`); контроллер не вызывает ни
  `s5_precheck`, ни `exit_gate` и их вывод не читает. `exit_gate` — хук (`exit_gate.main`), его импортируют `story_step`,
  `driver_dispatch`, `driver_stage_plan`, `brief_pack` (Grep `import exit_gate`), а не контроллер. Вызвать метод контроллера из
  хука без экземпляра нельзя; писать файл из хука — второй писатель (AR-14) и запись из проверяющего кода (FR-45).
- Строка узла FV1-30 в пачке владеет `scripts/s5_precheck.py`, `scripts/exit_gate.py` (`findings-1413c/.../batch-1-live-run-fvf.md:63`),
  `controller.py` в ней нет.
- Имя поля `passed_by_word` уже занято: булево поле пар и функция (`s5_precheck.py:3952, 4018-4023`; Grep `passed_by_word` →
  73 вхождения в 15 файлах, в том числе `window_record.py`, `report_facts.py`, `manifest_put.py`). Новое поле верхнего уровня с тем
  же именем и другим типом ломает чтение по имени.
- Минимальная правка: назвать в F-A3-5 конкретный ход данных, например «при `stage_complete` S5 контроллер читает сохранённый
  JSON-вывод `s5_precheck` (путь назвать) и вызывает `_record_person_pass` по полю `word_passes: [{finding_id, decision, at}]`»
  (или другой выбранный путь, но один и названный); добавить `controller.py (функция …)` в owns узла FV1-30; переименовать поле.

### Б5. F-A3-1 обещает «в отчёте — пройдено словом», но у журнала прохода нет читателя, а ниже по течению тот же факт может отказать снова (K3, K9)
- A3-E1 (A:290): «факт (экземпляр не прогнан, Then не привязан) остаётся в данных и в отчёте как „пройдено словом“»; OQ3 (A:627-629)
  обещает владельцу именно это.
- Проверил: Grep `passed.by.person` (`-i`) по всему `PKG` — 21 файл; в коде фабрики журнал читают только тесты, `collect-sets.json`
  (сборщик истории) и контроллер-писатель; ни `report_facts.py`, ни `gate_brief.py`, ни отчёт его не читают. Значит, в отчёте сегодня
  нет ничего, что показало бы «пройдено словом», а требования к узлу (A:272-281) читателя не заказывают (AR-22: у поля есть
  производитель — должен быть и читатель).
- Последствия для следующих стадий не прослежены: Then без привязки и экземпляр без строки прогона читают проверки позже (S7/S8,
  доставка). Если они отказывают снова на тот же факт, человеку задают тот же вопрос второй раз (FR-7) или фабрика встаёт. То же
  касается F-A3-2 (а): сама поправка пишет «ниже по течению читатели плана отказывают» (A:299) и всё равно выбирает (а), не сказав,
  что эти читатели делают с «план не прочитан, пройдено словом».
- Минимальная правка: (1) в требования узла FV1-30 добавить читателя прохода в отчёте (какой раздел, какая функция, например
  `report_facts`) с тестом; (2) одной таблицей назвать нижних читателей каждого факта, который проводит слово (Then не привязан,
  нет строки прогона, план не прочитан), и их поведение: факт показан как пробел, «пройдено словом <кто, когда>», без повторного
  вопроса. Если поиск читателей шире карты — запрос скаута через координатора.

### Б6. Строка X1: подпись и форма `task_price` неверны; статусы `incomplete` и `not_cross_checked` не разобраны; две ставки цен в одном сравнении (K4)
- Поправка: «value — `task_price.task_price(task_root)` … `{"value": <usd>}` при согласии источников, или
  `{"low", "high", "note"}`»; state `measured / range / unknown` (A:394-396). В следе прямо сказано: «`task_price.py` … не
  прочитано» (A:678).
- Проверил `PKG/scripts/task_price.py:764-798`: подпись `task_price(root, task, sessions=None, driver=None, catalogue=None, cfg=None)`;
  ответ — `status` ∈ {`differs`, `incomplete`, `not_cross_checked`, `agrees`} и `price_low_usd` / `price_high_usd` (ключей нет,
  если ни у одной сессии нет записи). `incomplete` — «the price is at least the figure shown»: НИЖНЯЯ граница, при этом low == high.
  По схеме поправки такой ответ попадает в `measured` как точное число; заниженная цена фабрики читается как «дешевле агента»,
  и по B2 такую строку можно закрепить, а будущий неполный релиз пройдёт как «не хуже» (AR-28, FR-41, P18).
- Две метрики: фабрика берётся через `task_price`, который пересчитывает цену по каталогу и `rate_overrides` проекта
  («Always passed through `revalue_document`, never read at their pinned money», `:767-769, 783-785`); планка — `total_cost_usd`
  из result JSON свободного плеча, то есть цена самого хоста (A:399). Отношение «фабрика / агент» тогда сравнивает две разные
  ставки — против гигиены 6(b) («одна метрика») и FR-25.
- Минимальная правка: (1) исправить подпись (`task_price(root, task)`) и связать состояния с ответом: `agrees` → `measured`;
  `differs` → `range`; `incomplete` → `at_least <low>` (может дать «хуже», если low > сравниваемого, но никогда «лучше» или
  «не хуже»); `not_cross_checked` → значение с пометкой «один источник» (как его сравнивать — решает Lead и пишет строкой);
  ключей цены нет → `unknown`. (2) Обе стороны на одной ставке: свободное плечо пересчитывается тем же каталогом
  (`revalue_document` по его транскрипту), либо обе — по цене хоста; выбранное записать в B1 и проверять строкой N7 на `free-N.log`.

### Б7. Храповик пропускает ухудшение молча в трёх местах (K4)
- (а) Диапазон у закреплённой строки: B1-E2 даёт `not decided: range` (A:415), B2-E6 — «не судится „хуже“ без `low`» (A:460).
  В выводе `compare` четыре вида строк (A:445-448), `not decided` среди них нет; `release-check` возвращает 1 только на
  `owner's word needed` (A:449-450). Пример: прошлый релиз 10 USD, сейчас диапазон [9; 14] → `not decided` → выход 0, хотя
  ухудшение до 14 возможно. Неизвестное стало проходом (AR-28, FR-41).
- (б) Закреплённой строки нет в табло текущего релиза (сравнительный прогон для этой пары «модель × стори» не делали, или
  табло нет вообще). B2-E3 разбирает только состояние `unknown` ВНУТРИ табло (A:457); база П1-в K3 говорит о «the newest live
  scoreboard» (П1-в `:108`). Если обход строится по строкам текущего табло, то нет табло → нет строк → `release: ok -- 0 ratcheted
  rows not worse` → выход 0.
- (в) Прошлый релиз сам дал диапазон (X1 или любая строка с `range`) — сравнение «диапазон с диапазоном» не определено.
- Минимальная правка: `compare --release` перебирает закреплённые строки из `norms.json` (не из текущего табло) для каждой пары
  «модель × стори»; у закреплённой строки `not decided: range`, нет значения в текущем релизе, `unknown`, `at_least` (Б6) →
  `release: owner's word needed -- <row> <why>`; диапазон против диапазона — «хуже», если `low_now > high_prev`, «не хуже»,
  если `high_now <= low_prev`, иначе `owner's word needed`. Тест-строки N6/N7 — по одной на каждое.

---

## Неблокирующие находки

1. **Перечень B4 «что есть сегодня» неполный** (K2). Пропущены: `SD_HEAD_MAX_BYTES = 1024` (`brief_pack.py:55`) — «HARD cap … the DoD
   leads are cut first, from the end (down to one)» (`:3700-3712`), то есть срезка содержимого брифа по размеру в прогоне;
   `DECISION_CHARS = 400` (`:59`) — первая ступень лестницы слов (`_short(line, DECISION_CHARS)`, `:1694, 1708, 1716`), а правка E9
   называет границы только 240 и 6144 (A:566-567). Сводки со ссылкой на целый файл (`MAX_REQUEST_LINES = 12` `:3235`,
   `FUNCTIONS_SHOWN = 8` `:3237`, `DIGEST_CHARS = 200` `:57`, `DISPATCH_DIGESTS = 4` `:58`) — их судит Lead: при наличии файла с полным
   текстом это не срезка. Номера строк B4 съехали примерно на +30–40 (лестница сейчас `:4452-4478`, `files.pop` `:4512`,
   `over_ceiling` `:4515-4521`); поправка читалась на более старом read-main. Исправление: дописать `SD_HEAD_MAX_BYTES` и 400 в
   «Что сделать» FV1-4 (тем же ходом F-B4-2), а DoD узла FV1-4 сформулировать по классу («ни одна срезка по размеру»), а не по списку.
2. **Переименование `test_scenario_dry_1.py` → `test_scenario_dry.py` и `stories/dry-1` → `dry-<type>` не прошло по всей П1-б** (K8, K10).
   Старые имена стоят в П1-б `:16-22` (owns), `:180, 191, 236, 498, 515, 603, 611` (DoD N3 `--part main`), `:621` (строка `keep`, covers
   `fixtures/stories/dry-1`), `:622` (`TEST_TIMEOUTS`), `:633, 650, 677` (R-L9), `:853, 940, 952`. Узлы режутся «из спек С ЭТОЙ ПОПРАВКОЙ»
   (A:5) — более слабая модель получит противоречивые имена. Исправление: одна строка-перенос «каждое вхождение … → …» с этим списком.
3. **Владение у N3a и N3t** (K8). DoD N3a печатает `told-before-work: …` из `test_scenario_dry.py --part main:<default>` (A:206-207),
   а файл теста принадлежит N3 (П1-б `:603`); у N3a в owns только функция в `dry_exits.py` (A:200). Добавить место вызова (функцию в
   `test_scenario_dry.py`) в owns N3a, или пусть N3 поставит вызов. Несколько N3t, которые идут параллельно и каждый правит «одну
   строку `types[]`» одного `dry-types.json` (A:129-130), пересекаются в одном файле — нужна строка `очередь:` или пусть строки пишет один узел.
4. **Дорога «без автотестов» до OQ1 не видна** (K6, правило 19). A1-E7 правильно требует её обходить (A:155), но оба типа, которые
   берутся до ответа (MyBooks, 14857), с автотестами; ни строки `known_red`/`live_only` «нет типа без автотестов — ждёт OQ1» нет, и
   пробел ничем не отмечен. Исправление: одна такая строка с меткой, снимает её N3t третьего типа.
5. **Неудобный вход «слово 24 КБ» без исхода** (K3, K7). A:279 называет вход, но не говорит, что должно получиться;
   `_record_person_pass` режет `decision` до 1000 знаков и `block` до 400 (`controller.py:2410-2411`). Нужно сказать: журнал хранит
   слово целиком или ссылку на его запись в `stage_overrides` (AR-24); 400/1000 — граница с вариантами строки AT и BEYOND.
6. **Текст отказа и причина после FV1-30** (K3, P15/FR-1). Хвост `s5_precheck.py:4693-4702` строит дверь из `PASSABLE` и говорит «no
   recorded word, `*` included, passes any other finding here»; `refusal_cause` вернёт `family` (`:3947-3948`) и для тегов исключения 2,
   чья семья (`oracle`) теперь проходима, — причина будет названа неверно. Добавить в требования узла: переписать хвост (что проходит,
   что ждёт ответа на вопрос, что ждёт слова по имени Then) и завести причину для тега исключения (например `awaits_answer`) с читателем
   `exit_gate.word_class`.
7. **F-A3-3 (а) и узел «допущения» правят один тег** (`case-is-oracle`, `s5_precheck.py:1883-1889`; автоматор вправе делать допущения,
   которые видны на гейте B — план `:382-386`). Нужна строка `очередь: FV1-30 → узел допущений` и в узле допущений — пункт «сверить
   `case-is-oracle`».
8. **Исключение 2 ссылается на `<id>` ещё не открытого узла** (A:258, 266). PROJECT.md п. 6 (г): узел открывает Lead; до нарезки N4:gates
   id должен существовать, иначе строку NOTE не к чему привязать.
9. **QA7: в словаре нет «тест есть, прогона нет»** (K5). При обязательной улике «строка прогона красного» (A:490) тест свободного плеча
   без вывода прогона нельзя записать ни как `red_on_bug`, ни как `green_on_bug`. Добавить `not_run` (отдельно от `no_test`) или
   оговорить, что форж прогоняет тесты обоих плеч одной дорогой (P31). QA10 (изоляция) словом владельца не названа («и т.д.»); это
   добавление дизайнера по t-354 §C — так её и пометить.
10. **Сравнение релизов, сделанных на разных моделях фабрики** (Sonnet и Terra, P7/FR-52) в B2 не разобрано; B2-E5 называет только
    версию правды и `run_class`. Дописать: другая модель фабрики → `not comparable` или отдельная планка — решает Lead.
11. **Черновой текст в N3t п. 3** (A:134): «`kit` — из снимка руками Lead-узла? нет: из полей снимка…» — переписать одной
    утвердительной фразой; `ac` и каналы берутся из реестра и плана снимка (выход ролей 0.10.x) только как метаданные типа — сказать
    это прямо, чтобы это не читалось как нарушение правила A:87.
12. **`worsened_passes.word` подписывает кто угодно** (A:439). Это держится на дисциплине; детектор назван (§8.1, A:466) — допустимо,
    но запишите в §M (d) явной строкой «на дисциплине, детектор — §8.1».

---

## Ответы по ключам

**K1 — полнота против слов владельца: fit с оговорками.** Прошёл §0 (A:29-54) строку за строкой против плана `:277-311, 315-386`.
Каждое слово 13.11 стоит в таблице и где-то исполнено: деньги → B1 (прочитано верно: P18 касается того, что ФАБРИКА пишет в проект;
форж хранит цену, A:357, план `:277-279`); храповик → B2 (против прошлого РЕЛИЗА, только строки «лучше агента», F-B2-3 (а) — ровно
по слову, план `:280-281`); «потолка в прогоне нет, следит фордж, максимум отметка в ретро» → B4 + B4-E3 (по смыслу верно; перечень
неполный — неблок. 1); типы → A1 (по слову «один проект — одна история», план `:349`); качество тестов → B3 (QA7 ловят баги, QA8
архитектура, QA9 группировка и параметризация — три названных аспекта покрыты, план `:307-309`); дымовой «все стадии параллельно» —
верно отнесено к П2-г, вне П1 (A:45); планка «модель × стори», правда = последняя со словом (6 багов), время без пауз → B5 (A:594-601).
Изменений без слова или решения Lead не нашёл: QA10 и `stand_answers` — добавления дизайнера, выведенные из t-354 §C и слов о первом
взгляде (неблок. 9). Где слово прочитано уже, чем сказано: «примеры как минимум 3х» → до OQ1 два типа (честно вынесено в OQ1), и
из-за Б1 на деле может остаться один. Деньги «один из самых важных критериев» исполнены строкой, но сама строка неверна (Б6, Б7).

**K2 — факты по следу: в основном fit; один ложный по смыслу факт (Б1), одна неверная подпись (Б6).** Проверил сам:
- `s5_precheck.py:72` `CHECKS` (9 семейств) ✓; `:82` `PASSABLE = {"environment", "obligations"}` ✓; `:101` `WORD_PASSABLE_TAGS` ✓;
  `_passable` `:3930-3933` ✓; `refusal_cause` `:3945-3946` (`then-remainder` ждёт) ✓; id `<check>:<case>:<tag>` `:266-268` ✓;
  заметка `:4013-4014` ✓; t-108 `:3968-3972` ✓; `predating` `:4000-4009` ✓; `run_mapping` `:1951-1971` ✓; `sides` `:2391` ✓;
  строка отказа `:4679` и хвост `:4693-4702` ✓; `detector_verdict.py:67, 117` ✓; `exit_gate.py:1796-1797` (`refused`), `:1802-1803` (`star`) ✓.
- Отрицание «у `smell` нет блокирующего производителя» — ПОДТВЕРЖДЕНО: многострочный Grep `_finding\(\s*"(sides|smell|run_mapping)"`
  (`-i`) → находит `run_mapping` (`:1951, 1963`) и `sides` (`:2391`) — это положительный контроль той же формы — и ни одного `smell`;
  все 13 вхождений `"smell"` (Grep `-i`) стоят внутри `_advice(` / `_hint(` (проверил строку перед каждым); переменная форма
  `_finding(check` встречается только в `_hint`/`_advice` (`:278, 285`); других мест, где задаётся `level`, нет (Grep `level` по файлу).
- «Единственный писатель `passed-by-person` — `_record_person_pass`» — ПОДТВЕРЖДЕНО (Grep `passed.by.person` `-i` по `PKG`; вызовы
  `:5875, 6877, 6961, 6970, 7043, 7169, 7409, 7516` совпадают). Попутно найдено: читателя в отчёте нет (Б5).
- Список B4: константы и лестница есть, номера строк съехали, `SD_HEAD_MAX_BYTES` и 400 пропущены (неблок. 1).
- A1: `local-1-0108/story.json:2-6` (`synthetic: true`, `task: LOCAL-1`, `package_version: 0.10.8`, `red_then` S7) ✓; слова гейтов в
  `state/words/` ✓; `TP1-14857/state/events.jsonl:3` `"package_version": "0.10.2"` ✓, 103 события ✓; K5 корпус
  (`test_synthetic_corpus.py:5-14`) ✓; `scenario_walk.load_story` `:102-116` ✓. **Но в `local-1-0108` нет ни одного `raw.json`** (Б1).
  У 14857 нет `state/words` — строка типа без слов, это закрывает A1-E3.
- `execution_request.py:293-296` (строка FV1-18) ✓ — по смыслу верно, хотя дизайнер её не читал.
- `task_price` — подпись и форма в B1 не совпадают с `task_price.py:764-798` (Б6).

**K3 — A3 / FV1-30: defect.** Направление «ГЕЙТ: слово проводит» по P13 верно в каждой строке; «слово проводит ШАГ, факт не
переписывает» (F-A3-1) записано в строках 2 и 4 и в A3-E1, а для строк 1, 6, 7 это следует из того же A3-E1 — годится. FR-45 соблюдён
(`s5_precheck` не пишет). Направление ошибки `split_overridden` в новой роли указано верно (допустимо — ложный отказ, запрещено —
пройти неназванное), но выбранная дорога это направление не обеспечивает (Б3); путь записи несуществующий (Б4); обещанного факта в
отчёте нет (Б5); текст и причина отказа (неблок. 6). Неудобных входов в целом достаточно; не хватает исходов у двух из них (Б3,
неблок. 5). Исключение 2 оставлено своему узлу корректно: сегодняшняя дверь «ответить на вопрос об ожидании» (`:90-94`) остаётся
и в промежутке, тупика нет; нужно только открыть id узла (неблок. 8).

**K4 — деньги и храповик: defect.** X1 = `task_price` (не наивная сумма) — направление верное; форма, статусы и ставки — Б6.
Форма `norms.json` (A:433-439) годится; закрепляет Lead (F-B2-1 (а)) — верно; `norms --check` отказывает, если закрепление снимают без
слова, — верно. `release-check` пропускает молча в трёх случаях — Б7.

**K5 — качество тестов: fit с одной дырой.** QA7–QA10 — суждение слепого критика с обязательной уликой (A:487-497), код проверяет
только наличие и форму (A:499-501) — AR-29 и P27 соблюдены. Пределы слепоты названы (B3-E3, F-B3-3 (б)). Три аспекта владельца
покрыты. Дыра — в QA7 нет вердикта «не прогнан» (неблок. 9).

**K6 — сухая история: defect.** Типы — данные (`dry-types.json`, один читатель, AR-1) ✓; из старого снимка — только данные мира,
выходы старого кода на вход не идут (A:83-90, A1-E1) ✓ — но выбранный спайк этому правилу не удовлетворяет (Б1); слова ключуются
видом вопроса (A:86, A1-E2) ✓; тип «без автотестов» обходится, а не исключается (A1-E7) ✓, но до OQ1 этот пробел не отмечен
(неблок. 4). C11 расходится с механизмом §7 / F9 (Б2).

**K7 — края: в основном fit.** Временные края заданы для обоих миров: A1-E6, A2-E4, A3-E4, B4-E2, B1-E3/B2-E1. Решены неверно или не
полностью: B1-E2/B2-E6 для закреплённых строк (Б7 а), B2-E3 без случая «строки нет» (Б7 б), «слово 24 КБ» (неблок. 5); нет края
«другая модель фабрики» (неблок. 10).

**K8 — правки узлов: defect в частях.** У N3t и N3a названы файл, функция, поведение и тест на каждый пункт (A:127-140, 197-208).
Недостатки: owns N3a не покрывает её DoD, N3t параллельно правят один файл (неблок. 3); старые имена по П1-б (неблок. 2); узлу FV1-30
нужен `controller.py` (Б4). По `docs/TESTING.md`: один `test_scenario_dry.py` с частями (F-A1-3 (а)) соответствует `TESTING.md:116`
(«новый тестовый файл не создаётся; случай идёт строкой»); случаи — строки таблиц, а не отдельные тесты ✓.

**K9 — решения Lead по развилкам (план §15):**
- F-A1-1 (а) — **упущено**: в `local-1-0108` нет сырых ответов, F-A1-4 (б) его исключает (Б1).
- F-A1-2 (а, условно) — fit; до ответа исполнимо на двух типах (с неблок. 4).
- F-A1-3 (а) — fit. F-A1-4 (б) — fit сам по себе; из него и вытекает Б1.
- F-A2-1 (а) — fit, но текст C11 надо привести к нему и к F9 механизма (Б2). F-A2-2 (а) — fit.
- F-A3-1 (а) — fit по сути; **упущено**: читатель в отчёте и нижние читатели (Б5).
- F-A3-2 (а) — fit по P13; **упущено** то же, что в Б5: что делают нижние читатели плана.
- F-A3-3 (а) — fit; нужна очередь с узлом допущений (неблок. 7).
- F-A3-4 (а) — fit (отрицание про `smell` подтверждено).
- F-A3-5 (а) — **упущено**: хода данных к `_record_person_pass` нет, `controller.py` не в owns узла, имя поля занято (Б4).
- F-B1-1 (а) — fit (пакет денег не печатает — P18 в пакете не менялся; раздел владельца П1-в `:687-688`).
- F-B1-2 (B1-E2) — fit для незакреплённых строк; **упущено** для закреплённых (Б7 а).
- F-B2-1 (а), F-B2-2 (а), F-B2-3 (а) — fit. F-B3-1 (а), F-B3-2 (б), F-B3-3 (б) — fit. F-B4-1 (а) — fit (`SLICE_BYTES` — предел
  чтения стража, а не срезка). F-B4-2 (а) — fit, плюс пропущенные места (неблок. 1).
- **OQ1** — действительно вопрос владельцу: можно ли коммитить вычищенный реальный тикет и стоит ли этот тип чистки (данные и
  договорённости владельца); исполнимо по рекомендации — да, на двух типах. **OQ2** — вопрос владельцу (политика выпуска,
  P13-класс); исполнимо — да, консервативный вариант (а) ничего не снимает. **OQ3** — по сути уже решено словом владельца к Q2
  (план `:285`) и AR-28 / FR-18; спросить для подтверждения допустимо, исполнимо по рекомендации — да. Но нельзя обещать
  владельцу «в отчёте останется … пройдено вашим словом», пока не сделан Б5.

**K10 — внутренние противоречия: defect.** F-B1-1 (раздел владельца: «test rows "no money key" are replaced» против «`run_counters` in
the PACKAGE still prints no money», П1-в `:686-688`) разобрано верно — вариант (а) совпадает с обоими предложениями, если читать
первое как правило про форж. Найдены другие противоречия: F-A1-1 против A1-E1/F-A1-4 (Б1); C11 поправки против механизма §7 / F9 и
решения Lead (Б2); старые имена файла и каталога по П1-б (неблок. 2). Правка K3 П1-в (A:363) согласована с разделом владельца п. 2.

---

## Постоянные вопросы

- **ДУБЛИРОВАНИЕ И СОГЛАСОВАННОСТЬ:** найдено — две дороги к «сказано» (разбор брифа и `requirement_rows`, Б2); имя `passed_by_word`
  с двумя значениями (Б4). Что искал: Grep `C11|requirement_rows` по механизму; `passed_by_word` по `PKG/scripts` (73/15).
- **КАЧЕСТВО КОДА / СПЕКИ:** черновая фраза в N3t (неблок. 11); номера строк B4 съехали (неблок. 1). Кода нет — судил текст узлов.
- **ОДНО ДЕЙСТВИЕ — ОДНА ДОРОГА (P31, п. 12 брифа):** тип — строка данных, а не ветка по имени проекта (A1, ось 34) ✓; цена планки и
  цена фабрики считаются разными дорогами и на разных ставках (Б6) — **блок**; QA7 у двух плеч берёт улики разными дорогами
  (неблок. 9); исключения «по проекту» без строки данных не нашёл.

## Полнота класса (карта SIBLING_MAP)
Поправка заявляет оси 17, 18, 34 (A:22, §M). Ось 34 (одна дорога): Б2 и Б6 — её нарушения внутри поправки. Ось 17 (одна форма
вывода): у `compare` четыре вида строк, но для «не решено / нет значения» формы нет (Б7). Ось 18 (храповики): `told/*` и
`ratcheted_since` названы ✓. Класс Б3 (сопоставление слова по тексту вместо имени) живёт везде, где `split_overridden` получает
`pipeline` целиком; внутри поправки это только узел FV1-30. Были ли сестринские места у `_passed_by_person` контроллера — вне
этой поправки; по карте я их не обходил (просьба к координатору: если нужно, скаут на вопрос «где `split_overridden` получает
весь `stage_overrides` для находок с id кейса»).

## След
Прочитано: поправка целиком (`:1-682`); план `:200-485`; П1-в `:640-695` и строки `:23, 28, 106, 108, 252, 260, 353, 361, 448, 451, 452`;
П1-б строки `:347, 487, 499, 675, 812, 852` и Grep `dry_exits.py|dry_world.py|test_scenario_dry`; механизм — Grep
`C11|requirement_rows|^## |told_before_work|dry_exits` (`:52, 76, 107, 148, 156, 181-182`); `PKG/scripts/s5_precheck.py:60-119,
258-297, 1840-1890, 3900-4029, 4640-4708`; `waiver.py:202-242`; `contract.py:134-173`; `controller.py:2380-2419, 6935-6971`;
`exit_gate.py:1770-1814`; `brief_pack.py:52-61, 1682-1724, 3230-3256, 4434-4521` и Grep констант; `task_price.py:764-804` и
Grep `^def`; `retro_numbers.py:15-30`; `execution_request.py:285-300`; `scenario_walk.py:95-120`; `test_synthetic_corpus.py:1-16`;
`test_investigation.py:1-8`; фикстуры `local-1-0108` (`story.json:1-9`, листинги `work/`, `work/sources` по именам файлов,
`state/words`) и `investigation-14857/TP1-14857` (`events.jsonl` Grep `package_version`, листинги `state/`, `work/`, `sources/`);
`findings-1413c/.../batch-1-live-run-fvf.md:60-63`, `README.md:73-76`; `docs/TESTING.md:112-132`; `tools/critic_verdict.schema.json`.
Поиски с контролями: `smell` (контроль `run_mapping`/`sides` той же формы); `passed.by.person` (`-i`, весь `PKG`); `raw.json` в
`local-1-0108` → 0 (контроль: та же команда в `TP1-14857` → 10); `exit_gate|precheck` (`-i`) в `controller.py` → 1 комментарий.
Не делал: перепрогонов (кода нет); не читал `story.json` целиком, `references/artifact-contract-first-look.md`, `stage_joints.py`;
нижних читателей фактов Б5 полностью не обходил (это требование к поправке, а не мой вывод об их поведении).

Вердикт: **fit after fixes** — блокирующих 7 (Б1–Б7), неблокирующих 12. Решение принять поправку остаётся за Lead.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 F-A1-1 spike type MyBooks local-1-0108 has no raw tracker answers (only factory ticket.json; find raw.json = 0), so by A1-E1 and F-A1-4(b) the type cannot be built; pick 14857 or name the LOCAL tracker input",
    "B2 C11/N3a parse the written brief (work/briefs/<dispatch>.md, negative control on a brief copy) against mechanism spec section 7 and Lead F9: C11 calls brief_pack.requirement_rows",
    "B3 FV1-30 requirement 1 widens _passable without choosing the matching road; family-passable findings see the whole pipeline (s5_precheck.py:3999) and names_whole over case id reintroduces t-108 for all families; star behaviour left to the node",
    "B4 F-A3-5(a) has no data path: controller never reads s5_precheck/exit_gate output, _record_person_pass is a Controller method, FV1-30 node does not own controller.py, field name passed_by_word already used (73 hits)",
    "B5 F-A3-1 promises the fact shows in the report as passed by word but passed-by-person.jsonl has no report reader; downstream readers of unbound Then / missing run row / unread plan (F-A3-2) not traced (FR-7 re-ask risk)",
    "B6 X1: task_price signature and shape wrong (task_price(root, task), status agrees/differs/incomplete/not_cross_checked, price_low_usd/high_usd); incomplete is a lower bound read as exact; factory re-priced via catalogue and rate_overrides vs agent host total_cost_usd = two metrics",
    "B7 ratchet silent passes: ratcheted row with range gives not decided which release-check does not count; ratcheted row absent from the current release scoreboard yields ok; range vs range undefined"
  ],
  "fixes": [
    "B1: re-decide F-A1-1 to CodeMie 14857 or record where the LOCAL-1 tracker input lives and state it in A1/A1-E1",
    "B2: C11 and told_before_work call brief_pack.requirement_rows(role, stage, kind); negative control on a copy of the requirement rows; rewrite A2-E3",
    "B3: newly passable findings pass only by a word naming their tag or whole finding id, or star; record star choice in A3-E2; give outcomes to awkward inputs",
    "B4: name one data path (e.g. controller at S5 stage_complete reads saved s5_precheck JSON and calls _record_person_pass), add controller.py function to FV1-30 owns, rename the field",
    "B5: add a report reader of the pass with a test to FV1-30 requirements; one table of downstream readers per passed fact and their behaviour (gap shown, no re-ask)",
    "B6: fix signature; map agrees->measured, differs->range, incomplete->at_least (never better/not worse), not_cross_checked->single-source labelled, no keys->unknown; price both arms on one rate base",
    "B7: compare --release iterates ratcheted rows from norms.json per model x story; not decided, missing, unknown, at_least on a ratcheted row -> owner's word needed; define range vs range; one test row each",
    "Non-blocking 1-12 per the review file (B4 inventory, rename sweep, N3a/N3t owns, no-autotest row, 24 KB word, refusal text and cause, queue with assumptions node, open exception-2 node id, QA7 not_run, factory model change edge, N3t wording, worsened_passes on discipline)"
  ],
  "class_completeness": "Declared axes 17, 18, 34. Axis 34 violated inside the amendment by B2 (two roads to told) and B6 (two pricing roads). Axis 17: compare output lacks a form for undecided/missing (B7). Axis 18 covered. Class of B3 (word matched by text not name) beyond the FV1-30 node not walked: request to coordinator for a scout on where split_overridden receives the whole stage_overrides for findings carrying a case id.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:1-682",
      "docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:200-485",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md:640-695 and spot lines",
      "docs/tasks/specs/20261113-p1b-dry-story-spec.md spot lines and Grep of file names",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md Grep C11/requirement_rows",
      "read-main PKG scripts/s5_precheck.py:60-119,258-297,1840-1890,3900-4029,4640-4708",
      "read-main PKG scripts/waiver.py:202-242, contract.py:134-173",
      "read-main PKG scripts/controller.py:2380-2419,6935-6971",
      "read-main PKG scripts/exit_gate.py:1770-1814",
      "read-main PKG scripts/brief_pack.py:52-61,1682-1724,3230-3256,4434-4521",
      "read-main PKG scripts/task_price.py:764-804, retro_numbers.py:15-30, execution_request.py:285-300",
      "read-main PKG scripts/tests/scenario_walk.py:95-120, test_synthetic_corpus.py:1-16, test_investigation.py:1-8",
      "fixtures stories/local-1-0108 and investigation-14857/TP1-14857 listings",
      "findings-1413c live-run-fvf batch-1 rows 60-63 and README rows 73-76",
      "docs/TESTING.md:112-132"
    ],
    "reruns": [
      {"command": "find fixtures/stories/local-1-0108 -name raw.json; same in investigation-14857/TP1-14857", "result": "0 files in local-1-0108; 10 in TP1-14857 (control); local-1-0108 sources hold 58 ticket.json only"},
      {"command": "Grep multiline -i _finding(\\s*\"(sides|smell|run_mapping)\" in s5_precheck.py", "result": "run_mapping 1951,1963; sides 2391; no smell (negative confirmed with same-shape control)"},
      {"command": "Grep -i passed.by.person over read-main PKG", "result": "only controller.py:2402 writes; no report reader in package code"},
      {"command": "Grep -i exit_gate|precheck in controller.py", "result": "1 comment line (990); controller does not read s5_precheck output"},
      {"command": "Grep passed_by_word count over PKG scripts", "result": "73 occurrences in 15 files (name already taken)"}
    ]
  }
}
```
