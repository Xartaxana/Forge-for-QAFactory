import { test, expect, Page } from '@playwright/test';
import { CartSession, BookRow } from '../../../core/clients/cartClient';
import { CartApi } from '../../../core/clients/cartApi';
import { CartPage } from '../../../core/pages/CartPage';
import { CatalogPage } from '../../../core/pages/CatalogPage';
import { BookDetailPage } from '../../../core/pages/BookDetailPage';
import { WishlistPage } from '../../../core/pages/WishlistPage';
import { cfg } from '../../../core/config';

// Own data: books created through the admin API with a run-unique tag, removed afterwards.
const PRICE = 12.34;
const tag = `QA-LOCAL1-UI-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
let admin: CartSession;
let bookA: BookRow;
let bookB: BookRow;
let soldOut: BookRow;

test.beforeAll(async () => {
  admin = await CartSession.open();
  await admin.signIn(cfg.EMAIL_USER, cfg.EMAIL_PASS);
  bookA = await admin.createBook(`${tag}-A`, PRICE, 10);
  bookB = await admin.createBook(`${tag}-B`, 7.5, 10);
  soldOut = await admin.createBook(`${tag}-soldout`, 9.99, 0);
});

test.afterAll(async () => {
  for (const b of [bookA, bookB, soldOut]) if (b) await admin.deleteBook(b.id);
  await admin?.dispose();
});

// The browser starts signed in as the project's user account, so its cart and wishlist
// outlive a test: both are emptied before and after each one.
test.beforeEach(async ({ page }) => {
  const api = new CartApi(page.request);
  await api.clear();
  await api.wishlistRemove(bookA.id);
});
test.afterEach(async ({ page }) => {
  const api = new CartApi(page.request);
  await api.clear();
  await api.wishlistRemove(bookA.id);
});

type Path = 'detail' | 'card' | 'wishlist';
const paths: Path[] = ['detail', 'card', 'wishlist'];

async function addPathScenario(page: Page, path: Path, startsWith: number) {
  const api = new CartApi(page.request); // the page's own cookies: one session for the UI and the API reads
  const cart = new CartPage(page);
  if (path === 'wishlist') await api.signIn(cfg.EMAIL_USER, cfg.EMAIL_PASS); // a guest gets 401 from the wishlist
  if (startsWith === 1) {
    expect((await api.add(bookA.id, 1)).ok(), 'setup: A is already in the cart').toBeTruthy();
  }
  const expectedQty = startsWith + 1;

  if (path === 'detail') {
    const detail = new BookDetailPage(page);
    await detail.open(bookA.id);
    await detail.addToCart();
  } else if (path === 'card') {
    const catalog = new CatalogPage(page);
    await catalog.open(`${tag}-A`);
    await catalog.addFromCard(bookA.id);
  } else {
    await api.wishlistAdd(bookA.id);
    const wishlist = new WishlistPage(page);
    await new CatalogPage(page).open();
    await wishlist.open();
    await wishlist.moveToCart(bookA.id);
  }

  await expect.poll(async () => (await api.cart()).map((l) => l.quantity), {
    message: `the add by path ${path} reaches the cart`,
  }).toEqual([expectedQty]);
  await cart.openFromNav();

  const stored = await api.cart();
  expect(stored.length, 'Then: exactly one stored line for A, no duplicate').toBe(1);
  expect(stored[0].bookId).toBe(bookA.id);
  const id = stored[0].id;
  await expect(cart.lines, 'Then: exactly one line for A on the cart page').toHaveCount(1);
  await expect(cart.quantityInput(id), `Then: quantity ${expectedQty} on the page`).toHaveValue(String(expectedQty));
  await expect(cart.line(id), 'Then: A price shown on the line').toContainText(`$${PRICE.toFixed(2)} each`);
  await expect(cart.subtotal(id), 'Then: subtotal = price x quantity').toContainText(`$${(PRICE * expectedQty).toFixed(2)}`);
  expect(stored[0].quantity, 'Then: stored quantity').toBe(expectedQty);
}

test.describe('TC-006 every add-to-cart entry path gives the same cart line', () => {
  test('@e2e @cart TC-006 Then 1 detail from an empty cart', async ({ page }) => {
    await addPathScenario(page, 'detail', 0);
  });
  test('@e2e @cart TC-006 Then 1 card from an empty cart', async ({ page }) => {
    await addPathScenario(page, 'card', 0);
  });
  test('@e2e @cart TC-006 Then 1 wishlist from an empty cart', async ({ page }) => {
    await addPathScenario(page, 'wishlist', 0);
  });
  test('@e2e @cart TC-006 Then 2 detail with A already in the cart', async ({ page }) => {
    await addPathScenario(page, 'detail', 1);
  });
  test('@e2e @cart TC-006 Then 2 card with A already in the cart', async ({ page }) => {
    await addPathScenario(page, 'card', 1);
  });
  test('@e2e @cart TC-006 Then 2 wishlist with A already in the cart', async ({ page }) => {
    await addPathScenario(page, 'wishlist', 1);
  });
});

test.describe('TC-007 header count and cart page agree', () => {
  test('@e2e @cart TC-007 header badge vs cart page after adds and after a refused add', async ({ page }) => {
    const api = new CartApi(page.request);
    const cart = new CartPage(page);
    const catalog = new CatalogPage(page);
    const detail = new BookDetailPage(page);

    // Then 1: empty cart, badge hidden (wait for the cart read the header makes, then look)
    const cartRead = page.waitForResponse((r) => r.url().endsWith('/api/cart') && r.request().method() === 'GET');
    await catalog.open(tag);
    await cartRead;
    await page.waitForLoadState('networkidle');
    await expect(cart.cartCountBadge, 'Then 1: badge hidden at an empty cart').toHaveCount(0);

    // Step 2: A x1 from its card, then B x3 from its detail page, no reload in between
    await catalog.addFromCard(bookA.id);
    await expect(cart.cartCountBadge, 'badge appears after the first add without a reload').toBeVisible();
    await expect(cart.cartCountBadge, 'one line of one unit: both readings of the count give 1').toHaveText('1');
    const badgeFirst = Number(await cart.badgeText());
    expect(Number.isFinite(badgeFirst), 'base: the first badge read is a number').toBeTruthy();
    await catalog.bookLink(bookB.id).click();
    await detail.detailPage.waitFor();
    await detail.setQuantity(3);
    await detail.addToCart();
    await expect.poll(async () => (await api.cart()).length, { message: 'second add reaches the cart' }).toBe(2);
    await expect.poll(async () => {
      const t = await cart.badgeText();
      const n = Number(t);
      return t !== null && t.trim() !== '' && Number.isFinite(n) && n !== badgeFirst;
    }, { message: 'Then 2: badge shows a number different from the first read after the second add, no reload' }).toBe(true);
    await cart.openFromNav();
    await expect(cart.lines, 'Then 2: cart page shows 2 lines').toHaveCount(2);
    expect(await cart.unitsOnPage(), 'Then 2: cart page shows 4 units').toBe(4);
    // Then 2, the badge value: lines or units is open (Q19), no literal asserted

    // Step 3: refused add as an API call with the same session, then reload and compare
    const badgeBefore = await cart.badgeText();
    expect(badgeBefore, 'base: the badge is shown before the refused add').not.toBeNull();
    const refused = await api.add(soldOut.id, 1);
    expect(refused.ok(), 'the add of a stock-0 book is refused').toBeFalsy(); // broad_status: range per R-3
    await page.reload();
    await cart.cartPageElement.waitFor();
    await expect(cart.lines, 'Then 3: still 2 lines after the refused add').toHaveCount(2);
    expect(await cart.unitsOnPage(), 'Then 3: still 4 units after the refused add').toBe(4);
    await expect(cart.cartCountBadge).toBeVisible();
    expect(await cart.badgeText(), 'Then 3: badge unchanged by the refused add').toBe(badgeBefore);

    // Step 4: the same session still adds; both rise together
    expect((await api.add(bookA.id, 1)).ok(), 'working base: an allowed add by the same session').toBeTruthy();
    await page.reload();
    await cart.cartPageElement.waitFor();
    await expect(cart.lines, 'Then 3: cart page lines after the allowed add').toHaveCount(2);
    expect(await cart.unitsOnPage(), 'Then 3: cart page units rose to 5').toBe(5);
    await expect(cart.cartCountBadge).toBeVisible();
    expect(Number(await cart.badgeText()), 'Then 3: badge rose with the cart').toBeGreaterThan(Number(badgeBefore));
  });
});
// the factory runs these by title (--grep '@e2e @cart TC-00'): its line selectors do not hit these tests
