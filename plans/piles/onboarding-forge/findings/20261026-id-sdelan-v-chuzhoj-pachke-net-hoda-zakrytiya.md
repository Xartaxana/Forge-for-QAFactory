# Id, сделанный в чужой пачке, нельзя закрыть: `close` и проверка (а) читают указатель по-разному (B-331 в forge/5), B-164 сделан в conductor/1, а дом — driver-controller

id: — | кучка: `onboarding-forge` | от: Lead (Fable), 26.10.2026; скаут t-1234 | приоритет: П2 | кандидат наверх: нет

Класс (решение Lead 26.10.2026, техническое, подсвечено владельцу): id, чья РАБОТА легла в пачку другой кучки, чем его дом, не
имеет хода закрытия в `tools/piles.py`. Два случая.

## Что не так / что сделать

1. **B-331 в forge/5 (закрытие пачки, ночное окно 17.10).** Строка-указатель F5-12 (`plans/piles/forge/batch-5-vhodyashchie.md:35`,
   форма `перенос: <кучка>` в ячейке «Зависит от», карточка forge `README.md:70`) вводит id в пачку без дома в ней. Два места кода
   читают эту форму по-разному, и ни одно не читает её как члена: `closing_items` (`tools/piles.py:2493-2502`) требует для id текст
   (открытая строка BACKLOG или файл находки) и отказывает «B-331 has no text anywhere (not open in plans/BACKLOG.md, no finding
   file) -- nothing was written; fix the card row or write its finding»; а проверка (а) `_placement_dupes` (`piles.py:1236-1237`)
   отказывает, когда находки одного id лежат в двух кучках: «B-331 has homes in 2 piles … an id lives in one pile». Две находки
   B-331 (`forge/findings/20261009-b-331-zakryt-kommentariem.md` и `driver-controller/findings/20261009-b-331-vopros-cheloveku-pered-relaunch.md`)
   обе несут `id: —`, так что ни одна не размещает id по ключу.
2. **B-164 сделан в conductor/1 C1-5b1, дом — driver-controller.** Работа слита: ветка `worktree-agent-aea14976578835fef`,
   диапазон `729dac8c…cb8c4b26`, исполнитель t-733, критик слияния t-758, фикс-раунд t-760; строка «Хода» conductor/1
   (`plans/piles/conductor/batch-1-p22-seams.md:209`) пишет «B-164 закрыт слиянием». Дом id — `driver-controller`: строка карточки
   (`plans/piles/driver-controller/README.md:87`) «открыто», находка
   `plans/piles/driver-controller/findings/B-164-completion-for-story-run-py-3575-3592-put.md`, открытая строка
   `plans/BACKLOG.md:155`, `plans/PILES.md:175`. Закрыть id нечем: `close <slug> <N>` двигает членов ТОЛЬКО своей пачки;
   `close --id --word` — слово владельца, а здесь слова нет, есть хэш слияния. Id висит открытым, хотя работа в `main` (PROJECT.md
   «Командная работа» п. 4, 9: закрывает код по хэшу или слово владельца).

Тот же класс уже называла спека t-717 (развилка Р6, `docs/tasks/specs/t-717-pile-cards-form.md:246-249`: «Двойное планирование
B-331» — строку замороженной пачки дополнить нельзя, закрытие id отрывается от работы); кода для этого класса нет и теперь.

**Что сделать (дизайнер решает форму; предложение Lead):**

- Дверь `piles.py close --id B-nnn --hash <h> --by <slug>/<N>`: переносит строку BACKLOG в «Закрыто» хэшем `<h>`, достижимым из
  `origin/main`, когда пачка `--by` закрыта ИЛИ её «Ход» называет id. Не слово владельца и не пачка дома: третий путь закрытия, по
  хэшу работы.
- `closing_items` и проверка (а) узнают строку-указатель `перенос: <кучка>` как форму члена: у id-указателя ОДИН дом — кучка, на
  которую он указывает; в пачке указателя он не требует находки и не считается вторым домом.
- Первый случай — B-164 (conductor/1 C1-5b1, `cb8c4b26`): закрывается этой дверью, затем строка карточки driver-controller и
  находка снимаются обычным ходом.
- Края для дизайнера: хэш не из `origin/main` — отказ с именем; `--by` назвал пачку, у которой id не упомянут ни в «Ходе», ни в
  членах, — отказ; id уже закрыт — отказ; пачка `--by` не закрыта и «Ход» молчит — отказ с дверью.

## Свидетель

- `tools/piles.py:2493-2502` (`closing_items`, отказ «has no text anywhere»);
- `tools/piles.py:1236-1237` (`_placement_dupes`, «has homes in %d piles … an id lives in one pile»);
- `plans/piles/forge/batch-5-vhodyashchie.md:35` (строка F5-12, форма `перенос: driver-controller`), `plans/piles/forge/README.md:70`;
- `plans/piles/forge/findings/20261009-b-331-zakryt-kommentariem.md:3` и
  `plans/piles/driver-controller/findings/20261009-b-331-vopros-cheloveku-pered-relaunch.md:3` (обе `id: —`);
- `plans/piles/conductor/batch-1-p22-seams.md:202-210` (слияние C1-5b1, «B-164 закрыт слиянием» на :209);
- `plans/piles/driver-controller/README.md:87`, `plans/BACKLOG.md:155`, `plans/PILES.md:175` (B-164 открыт во всех трёх);
- `docs/tasks/specs/t-717-pile-cards-form.md:246-249` (Р6).

## Принципы и правила

P13 (слово человека проводит гейт; здесь слова нет, и выход не должен его требовать), FR-40 (всякое записанное состояние имеет
санкционированный выход), FR-42 (на каждое состояние другой стороны у этой есть ход или отказ, называющий исполнителя),
`docs/SIBLING_MAP.md` ось 12 (близнецы: читатель строки карточки и читатель члена пачки читают одну форму).

Решение владельца нужно: нет (техническое; B-164 закрывается хэшем слияния, не словом).
