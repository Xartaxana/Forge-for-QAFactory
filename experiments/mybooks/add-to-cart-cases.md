# MyBooks — «Add to Cart»: недостающие кейсы

Запрос: «проверить всё, что связано с "Add to Cart" functionality in MyBooks» — не только историю XPANBFLFA-44.
Сверка 31.10.2026: 23 открытых кейса Jira (XPANBFLFA-45, 141–148, 151–152, 156–167) против кода MyBooks `main` a25b080
(карта кода — скаут t-1628, ключевые правила перепроверены по `src/lib/cartRules.ts`, `prisma/schema.prisma`,
`src/lib/validation/schemas.ts`). Файл — эталон: с ним сравниваются кейсы, которые напишет фабрика на этом запросе.
В Jira не записано (P8). Утверждения о поведении взяты из кода и **не прогонялись** на стенде; код — не оракул (P20):
где кейс Jira расходится с кодом, это вопрос к требованиям, а не правка кейса под код.

Стенд и данные: RUNBOOK §11. Данные сида (`npm run db:seed`): «1984» $13.99 остаток 15; «Dune» $16.99 остаток 14;
«Ariel» $11.99 остаток 5; «Moby-Dick» $17.99 остаток 4; «Last Copy» $20.00 остаток 1; «Out of Print Classic» $9.99 остаток 0.
Книги искать по названию, не по id (id меняется при пересидировании). Цену и остаток читать во время прогона.

## Покрытие: что уже есть, чего нет

| Область | Кейсы Jira | Новые кейсы |
|---|---|---|
| Страница книги: добавить 1 / N, отказы по остатку и количеству | 141–148, 151–152, 162–163 | — |
| Кнопка на карточке каталога | — | AC-01, AC-02 |
| «Move to cart» из вишлиста | — | AC-03, AC-04, AC-05 |
| Повторное добавление складывает количество | 159 (шаги не написаны) | AC-06 (вместо шагов 159) |
| Бейдж и заголовок корзины: штуки, а не строки | — | AC-07 |
| Слияние гостевой корзины при входе | 156, 157 — только сохранность | AC-08, AC-09, AC-10 |
| Остаток уменьшен после добавления; последний экземпляр у двоих | — | AC-11, AC-12 |
| Книга удалена, пока лежит в корзине | — | AC-13 |
| Поле количества на странице корзины: пустое значение | — | AC-14 |
| API добавления: коды и сообщения ошибок | 45 (размытый) | AC-15 (вместо 45) |
| Чужая строка корзины: гость и пользователь не трогают строки друг друга | — | AC-16 (из прогона фабрики, TS-2) |
| Параллельные добавления одной книги не превышают остаток | — | AC-17 (из прогона фабрики, TS-10) |
| После заказа корзина пуста | — | AC-11 шаг 5 (из прогона фабрики, TS-11) |

Дополнено 31.10.2026 сверкой с прогоном фабрики ADD-TO-CART (`qa-factory/artifacts/ADD-TO-CART/` копии
`mybooks-stand/test-automation-framework`): фабрика нашла три сценария и два вопроса, которых здесь не было (AC-16, AC-17,
шаг 5 AC-11, вопросы Q2 и Q3 ниже). Чего фабрика не нашла — находки `grounding/findings/20261031-trebovanie-iz-tekushchego-koda-stanovitsya-orakulom.md`
и уточнение OH3-36 в `onboarding-hooks`.

Уровень по пирамиде (P16/P19): правила `mergedQuantity` и `fitsInStock` уже покрыты юнит-тестами приложения
(`src/lib/cartRules.test.ts`), граница схемы количества — `src/lib/validation/schemas.test.ts` (только для обновления
строки; для добавления — только `bookId`). Поэтому слияние в e2e — один параметризованный сценарий, а ошибки API — уровень API.

## Расхождения существующих кейсов с приложением — вопросы к требованиям

| Кейс | Что ждёт кейс | Что делает приложение | Вопрос человеку |
|---|---|---|---|
| 164 Add product during price update | платит цену, которую видел при добавлении | цена в строке корзины не хранится (`CartItem` без цены); корзина и оформление показывают текущую цену, фиксируется она в момент заказа | Должна ли корзина держать цену на момент добавления? Если нет — кейс переписать: «после смены цены корзина и итог показывают новую цену» |
| 166 Add product with session timeout | после истечения сессии просит войти | добавлять в корзину можно без входа: товар уйдёт в гостевую корзину и сольётся при следующем входе (AC-08) | Переписать кейс через гостевую корзину и слияние? |
| 160 Add product from quick view | добавить из быстрого просмотра | быстрого просмотра в приложении нет | Кейс снять или это недостающая функция (тогда — баг/пробел, FR-21)? |
| 161 Maximum allowed quantity | «максимальное количество» | предел = меньшее из остатка и 999 (`Quantity must be at most 999`); в UI поле ограничено остатком атрибутом `max`, сервер — единственная проверка | Какой максимум имеется в виду: остаток или 999? |

Кроме того, у 158–167 нет шагов («To be authored»): их пишет автор кейсов или фабрика.

Вопросы к требованиям без кейса Jira (два — из прогона фабрики):

| Тема | Что делает приложение | Вопрос человеку |
|---|---|---|
| Q2 Слияние одинаковой книги | остаётся большее количество (гость 2 + аккаунт 3 → 3), а повторное добавление складывает | Так задумано, или слияние должно складывать (→ 5)? До ответа строки `merge-higher-wins` и `merge-account-higher` в AC-08 — не ожидание, а вопрос (P20) |
| Q3 Ошибка слияния при входе | ошибка только пишется в лог, вход проходит, гостевая корзина молча не сливается | Так задумано, или пользователь должен узнать, что корзина не перенесена? |
| Перенос из вишлиста | два запроса (добавить, затем удалить из вишлиста), не одна операция | Должен ли перенос быть атомарным (см. AC-04)? |
| Остаток упал после добавления | первый сигнал — отказ на оформлении | Должна ли корзина предупреждать заранее (см. AC-11)? |

## Новые кейсы

### AC-01 Add a book to the cart from the catalog card
*Type:* positive · *Level:* end-to-end · *Priority:* high

*Preconditions:* guest or signed-in user; cart empty; «Dune» in stock.

| # | Step | Expected |
|---|---|---|
| 1 | Open the catalog, search «Dune» | Card «Dune» is listed with `add-to-cart-button-{id}` enabled |
| 2 | Click the card's Add to Cart | Toast «Book added to cart»; `cart-count-badge` shows 1; page stays on the catalog |
| 3 | Click the card's Add to Cart again | Toast «Book added to cart»; badge shows 2 |
| 4 | Open the cart | One line «Dune», quantity 2, subtotal $33.98 |

*Postconditions:* cart emptied.

### AC-02 Catalog card of an out-of-stock book
*Type:* negative · *Level:* end-to-end · *Priority:* medium

| # | Step | Expected |
|---|---|---|
| 1 | Search «Out of Print Classic» in the catalog | Card's add button is disabled and reads «Out of Stock» |
| 2 | Try to click it | Nothing is added; badge absent or 0 |

### AC-03 Move a book from the wishlist to the cart
*Type:* positive · *Level:* end-to-end · *Priority:* high

*Preconditions:* signed-in user; cart empty; «1984» saved to the wishlist (`wishlist-toggle-button` on its page).

| # | Step | Expected |
|---|---|---|
| 1 | Open the wishlist | Row `wishlist-item-{bookId}` «1984» is listed |
| 2 | Click `wishlist-move-{bookId}` | Toast «Moved to cart»; the row disappears from the wishlist; badge shows 1 |
| 3 | Reload the wishlist | «1984» is not in the wishlist (removal was saved, not only hidden) |
| 4 | Open the cart | One line «1984», quantity 1, $13.99 |

### AC-04 Move to cart is refused by stock — the book stays in the wishlist
*Type:* negative · *Level:* end-to-end · *Priority:* medium

*Preconditions:* signed-in user; «Last Copy» (stock 1) already in the cart with quantity 1 and saved to the wishlist.

| # | Step | Expected |
|---|---|---|
| 1 | Open the wishlist, click `wishlist-move-{bookId}` for «Last Copy» | Error toast «Only 1 in stock and 1 already in your cart» |
| 2 | Look at the wishlist | «Last Copy» is still listed |
| 3 | Open the cart | «Last Copy», quantity 1 (unchanged) |

Note: move is two requests (add to cart, then remove from wishlist), not one operation. A failure of the second request
leaves the book in both places; worth a lower-level check if the requirements say «move» must be atomic (question).

### AC-05 Wishlist row of an out-of-stock book
*Type:* negative · *Level:* end-to-end · *Priority:* low

*Preconditions:* «Out of Print Classic» saved to the wishlist.

| # | Step | Expected |
|---|---|---|
| 1 | Open the wishlist | Out-of-stock badge `wishlist-out-{bookId}` is shown; `wishlist-move-{bookId}` is disabled |

### AC-06 Adding the same book again adds to the existing line (authors steps for XPANBFLFA-159)
*Type:* positive · *Level:* end-to-end · *Priority:* medium

*Preconditions:* signed-in user; cart empty; «1984» in stock (≥ 5).

| # | Step | Expected |
|---|---|---|
| 1 | On «1984» detail page set quantity 2, Add to Cart | Toast «2 copies added to cart»; badge 2 |
| 2 | Set quantity 3, Add to Cart | Toast «3 copies added to cart»; badge 5 |
| 3 | Open the cart | ONE line «1984», quantity 5, subtotal $69.95 (not two lines) |

### AC-07 Cart badge counts copies, not titles
*Type:* positive · *Level:* end-to-end · *Priority:* medium

*Preconditions:* cart empty.

| # | Step | Expected |
|---|---|---|
| 1 | Add «1984» with quantity 2 and «Dune» with quantity 1 | Badge shows 3 |
| 2 | Open the cart | Header reads «2 titles, 3 copies»; total $44.97 |
| 3 | Remove «1984» (`remove-cart-item-{id}`) | Toast «Item removed from cart»; badge shows 1; header «1 title, 1 copy» |

### AC-08 Guest cart merges into the account cart at sign-in
*Type:* positive · *Level:* end-to-end · *Priority:* critical

One scenario, parameterised by the row; the parameter id names the row so a red row says which rule broke.
The rule itself is unit-tested (`mergedQuantity`); this case proves the sign-in actually calls it.

Rows `merge-higher-wins` and `merge-account-higher` state what the code does, not a confirmed requirement: they stay open
until question Q2 is answered (higher quantity or sum). The other rows do not depend on Q2.

*Preconditions:* the regular user's cart is prepared while signed in, then the user signs out; the guest cart is filled
as a guest in the same browser; then the user signs in on the login page.

| id | Account cart before | Guest cart before | Expected account cart after sign-in |
|---|---|---|---|
| merge-only-guest | empty | «Dune» ×2 | «Dune» ×2 (guest line moved) |
| merge-higher-wins | «1984» ×1 | «1984» ×3 | «1984» ×3 — the higher quantity, **not** 4 |
| merge-account-higher | «1984» ×4 | «1984» ×2 | «1984» ×4 (unchanged) |
| merge-capped-at-stock | «Ariel» ×2, then stock set to 3 by admin | «Ariel» ×5 added while stock was 5 | «Ariel» ×3 |
| merge-different-books | «1984» ×1 | «Dune» ×1 | both lines, badge 2 |

*Expected for every row:* badge equals the sum of the quantities after sign-in; the guest's lines are no longer shown
after a later sign-out (they belong to the account now).

### AC-09 Guest line of a book that went out of stock is dropped at sign-in
*Type:* negative · *Level:* end-to-end · *Priority:* medium

*Preconditions:* as a guest add «Moby-Dick» ×1; admin then sets «Moby-Dick» stock to 0.

| # | Step | Expected |
|---|---|---|
| 1 | Sign in as the regular user (account cart empty) | Sign-in succeeds |
| 2 | Open the cart | «Moby-Dick» is not in the cart; badge absent or 0 |

*Postconditions:* restore «Moby-Dick» stock (or reseed).

### AC-10 Guest cart survives registration and merges at the first sign-in
*Type:* positive · *Level:* end-to-end · *Priority:* medium

Registration does not sign the user in (only the login page calls `signIn` and the merge), so the guest cart must wait
for the first sign-in.

| # | Step | Expected |
|---|---|---|
| 1 | As a guest add «Dune» ×1 | Badge 1 |
| 2 | Register a new account (confirm the email through Mailpit `http://localhost:8025` if verification is on) | Account created |
| 3 | Sign in with the new account | Cart has «Dune» ×1; badge 1 |

### AC-11 Stock reduced after adding: the cart keeps the line, checkout refuses
*Type:* negative · *Level:* end-to-end · *Priority:* high

*Preconditions:* signed-in user; «Ariel» (stock 5) ×4 in the cart.

| # | Step | Expected |
|---|---|---|
| 1 | Admin sets «Ariel» stock to 2 | Saved |
| 2 | User opens the cart | Line «Ariel» ×4 is still shown (the cart does not trim lines) |
| 3 | Proceed to checkout, place the order with test card 4242424242424242 | Order is refused: «Insufficient stock for book: Ariel»; no order is created; stock stays 2 |
| 4 | In the cart set «Ariel» quantity to 2 | Accepted; checkout now succeeds |
| 5 | Open the cart after the order | The cart is empty; badge absent or 0 |

Question to the person: should the cart warn about the drop before checkout? Today the first signal is the checkout refusal.

### AC-12 Last copy in two carts: the first order wins
*Type:* negative · *Level:* end-to-end · *Priority:* high

*Preconditions:* two signed-in users (two browser contexts); «Last Copy» stock 1.

| # | Step | Expected |
|---|---|---|
| 1 | User A adds «Last Copy» ×1 | Accepted (no reservation is made) |
| 2 | User B adds «Last Copy» ×1 | Accepted |
| 3 | User A places the order | Order created; stock becomes 0 |
| 4 | User B places the order | Refused «Insufficient stock for book: Last Copy»; if B's card was already charged, the charge is refunded (TEST_IDS_REFERENCE «Checkout»); no order for B |

### AC-13 Book deleted while it is in a cart
*Type:* negative · *Level:* end-to-end · *Priority:* medium

*Preconditions:* admin creates a book «QA Temp Book», stock 5, with no orders; the user adds it ×1.

| # | Step | Expected |
|---|---|---|
| 1 | Admin deletes «QA Temp Book» | Deleted (allowed: the book has no orders) |
| 2 | User opens the cart | The cart page loads without an error; the line is gone; badge 0 |

Risk from code reading: the cart page loads each line's book by id; a missing book may break the page. Not run.

### AC-14 Cart quantity field cleared or given a non-number
*Type:* negative · *Level:* end-to-end · *Priority:* low

*Preconditions:* «1984» ×2 in the cart.

| # | Step | Expected |
|---|---|---|
| 1 | Clear `cart-item-quantity-{id}` | No silent change of the stored quantity; at most a validation message |
| 2 | Reload the cart | «1984» quantity is still 2 |

Observation from code: the field sends an update on every keystroke and its guard is `quantity < 1`, so an empty field
sends a non-number and the server answers with a validation error toast. Not run.

### AC-15 Add-to-cart API: success and every refusal (replaces XPANBFLFA-45)
*Type:* positive + negative · *Level:* API · *Priority:* high

`POST /api/cart`, JSON body `{bookId, quantity}`; errors look like `{error, code}`. One parameterised test; the id names the row.
Guest calls are allowed (a guest cookie `bookstore_session_id` is created on demand) — no 401 on add.

| id | Request | Expected |
|---|---|---|
| api-add-ok | 1984, quantity 1, empty cart | 201; body is the cart line, quantity 1 |
| api-add-additive | 1984, quantity 2 twice | second answer: line quantity 4 |
| api-unknown-book | bookId 999999 | 404 `BOOK_NOT_FOUND` «Book not found» |
| api-out-of-stock | Out of Print Classic, 1 | 400 `OUT_OF_STOCK` «"Out of Print Classic" is out of stock» |
| api-over-stock | Ariel, 6 | 400 `INSUFFICIENT_STOCK` «Only 5 in stock» |
| api-over-stock-with-cart | Ariel 3, then Ariel 3 | 400 `INSUFFICIENT_STOCK` «Only 5 in stock and 3 already in your cart» |
| api-qty-0 / -1 / 1.5 | quantity 0, -1, 1.5 | 400 `VALIDATION_ERROR`; messages «Quantity must be at least 1» / same / «Quantity must be a whole number» |
| api-qty-1000 | quantity 1000 | 400 `VALIDATION_ERROR` «Quantity must be at most 999» |
| api-qty-string | quantity "2" | 400 `VALIDATION_ERROR` «Valid quantity is required» |
| api-qty-missing | no quantity | 400 `VALIDATION_ERROR` «Valid quantity is required» |
| api-bad-book-id | bookId 0, -1, "abc" | 400 `VALIDATION_ERROR` «Valid book ID is required» |
| api-bad-json | body `{` | 400 `INVALID_JSON` «Request body must be valid JSON» |

After every refusal: `GET /api/cart` shows the cart unchanged.

### AC-16 One owner cannot change another owner's cart line
*Type:* negative · *Level:* API · *Priority:* high · *Source:* factory run ADD-TO-CART, TS-2

*Preconditions:* user A has «1984» ×1 in the cart (line id L); a guest session G has its own cart.

| id | Request | Expected |
|---|---|---|
| other-user-update | user B: update line L to quantity 3 | refused (not found or forbidden); A's line stays ×1 |
| other-user-remove | user B: remove line L | refused; A's line is still there |
| guest-update-user-line | guest G: update line L | refused; A's line unchanged |
| clear-own-only | user B: clear the cart | only B's lines go; A's line stays |

Expected status codes are not stated by the requirements: what the code returns is a question, not the oracle (P20).

### AC-17 Parallel adds of the same book do not exceed stock
*Type:* negative · *Level:* API · *Priority:* medium · *Source:* factory run ADD-TO-CART, TS-10

*Preconditions:* signed-in user; cart empty; «Moby-Dick» stock 4.

| # | Step | Expected |
|---|---|---|
| 1 | Send 5 `POST /api/cart` {Moby-Dick, 1} at once | At most 4 succeed; the rest get 400 `INSUFFICIENT_STOCK` |
| 2 | `GET /api/cart` | «Moby-Dick» quantity ≤ 4 |

Risk from code reading: the stock check and the write are separate steps, not one transaction. One clean burst does not prove
the race is absent; a red burst proves it is present.

Прогнано на стенде 31.10.2026 (гостевая корзина, curl): все строки таблицы совпали — коды, `code` и тексты ошибок;
сложение количества подтверждено (1 + 2 → 3). Кейсы AC-01…AC-14 не прогонялись.
