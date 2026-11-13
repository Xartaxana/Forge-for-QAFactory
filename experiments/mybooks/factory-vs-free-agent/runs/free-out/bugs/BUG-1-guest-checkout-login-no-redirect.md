# BUG-1: Гость из корзины нажимает «Proceed to Checkout», логинится — остаётся на странице логина, на checkout не попадает

**Область:** корзина → оформление заказа для гостя (основной путь воронки покупки).

## Шаги
1. Открыть стенд как гость (без cookies), на главной нажать «Add to Cart» у любой книги в наличии.
2. Перейти в корзину (nav «Cart») — переход клиентский, без перезагрузки страницы.
3. Нажать «Proceed to Checkout». Открывается `/login?callbackUrl=%2Fcheckout` (ожидаемо).
4. Ввести `user@bookstore.com` / пароль, нажать Sign In.

## Ожидаемо
После успешного входа пользователь возвращается на `/checkout` с корзиной (гостевая корзина слита с аккаунтом).
Источник ожидания: письменное требование — `TEST_IDS_REFERENCE.md` («Guests opening a private page are redirected to /login?callbackUrl=<page> and return there after signing in»), `docs/AUTH.md`.

## Фактически
Тост «Successfully logged in!», сессия создана, гостевая корзина слита (бейдж корзины обновился), но URL остаётся `/login?callbackUrl=%2Fcheckout`; страница логина остаётся на экране. Повторный Sign In — то же самое. Пользователь вынужден вручную перейти в корзину и снова нажать Proceed.

Воспроизводится стабильно (3 из 3). Если же открыть `/checkout` полной загрузкой страницы (или сразу `/login?callbackUrl=/checkout`), редирект после входа работает. То есть ломается именно путь «клиентская навигация корзина → checkout → логин».
Вероятная причина (гипотеза по коду, не проверена в продукте): `LoginRoute` делает `router.push(callbackUrl)`, а клиентский роутер Next.js закэшировал редирект на /login, полученный от middleware при первом `router.push('/checkout')` из корзины.

## Доказательства
- `out/evidence/ui-login-stuck.png`, `out/evidence/ui-guest-checkout-login.png`
- автотест `tests/e2e/cart/add_to_cart.spec.ts` («guest who proceeds to checkout from the cart lands on checkout after signing in») падает: `out/evidence/automated-run.txt`, `out/evidence/bug1-test-failure.png`

Серьёзность: высокая для воронки (гость с полной корзиной не доходит до оплаты с первого раза без подсказки), есть обходной путь.
