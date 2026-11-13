import { test, expect } from '@playwright/test';
import { CartSession, errorOf, BookRow } from '../../../core/clients/cartClient';
import { cfg } from '../../../core/config';

// Own data: books per run with a known price and stock, removed afterwards.
const STOCK = 5;
const PRICE = 12.34;
const tag = `QA-LOCAL1-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;

let admin: CartSession;
let book: BookRow;
let soldOut: BookRow;

test.beforeAll(async () => {
  admin = await CartSession.open();
  await admin.signIn(cfg.EMAIL_USER, cfg.EMAIL_PASS);
  book = await admin.createBook(`${tag}-stocked`, PRICE, STOCK);
  soldOut = await admin.createBook(`${tag}-soldout`, 9.99, 0);
});

test.afterAll(async () => {
  await admin.deleteBook(book.id);
  await admin.deleteBook(soldOut.id);
  await admin.dispose();
});

test.describe('TC-001 add to cart: price, quantity, stock, invalid input', () => {
  test('@api TC-001 Then 1 quantity 1 gives one line with quantity 1 at the catalog price', async () => {
    const g = await CartSession.open();
    try {
      const r = await g.add(book.id, 1);
      expect(r.status(), 'add of quantity 1 is accepted').toBe(201);
      const lines = await g.cart();
      expect(lines.length, 'Then 1: one line after one add').toBe(1);
      expect(lines[0].bookId).toBe(book.id);
      expect(lines[0].quantity).toBe(1);
      expect(await g.total(), 'Then 1: cart total = catalog price x 1').toBeCloseTo(PRICE, 2);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });

  test('@api TC-001 Then 2 quantity 3 gives quantity 3 and subtotal price x 3', async () => {
    const g = await CartSession.open();
    try {
      expect((await g.add(book.id, 3)).status()).toBe(201);
      const lines = await g.cart();
      expect(lines.length, 'Then 2: one line').toBe(1);
      expect(lines[0].quantity).toBe(3);
      // The cart line carries no subtotal field (shape: CartItem, MyBooks/src/types/index.ts:36); the cart total route is the separate reader.
      expect(await g.total(), 'Then 2: subtotal = price x 3').toBeCloseTo(PRICE * 3, 2);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });

  test('@api TC-001 Then 3 repeat add keeps one line with the summed quantity', async () => {
    const g = await CartSession.open();
    try {
      expect((await g.add(book.id, 1)).status()).toBe(201);
      expect((await g.add(book.id, 2)).status()).toBe(201);
      const lines = await g.cart();
      expect(lines.length, 'Then 3: no duplicate line').toBe(1);
      expect(lines[0].quantity, 'Then 3: summed quantity').toBe(3);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });

  test('@api TC-001 Then 4 the cart never exceeds stock; the add beyond stock is refused', async () => {
    const g = await CartSession.open();
    try {
      expect((await g.add(book.id, STOCK)).status(), 'up to stock is accepted').toBe(201);
      const over = await g.add(book.id, 1);
      expect(over.status(), 'Then 4: one more than stock is refused').toBe(400);
      expect((await errorOf(over)).code).toBe('INSUFFICIENT_STOCK');
      const lines = await g.cart();
      expect(lines.length).toBe(1);
      expect(lines[0].quantity, 'Then 4: quantity stays at stock').toBe(STOCK);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });

  test('@api TC-001 Then 4 fresh session add above stock is refused and nothing is added', async () => {
    const g2 = await CartSession.open();
    try {
      const fresh = await g2.add(book.id, STOCK + 1);
      expect.soft(fresh.status(), 'Then 4: stock+1 in a fresh session is refused').toBe(400);
      expect.soft((await errorOf(fresh)).code).toBe('INSUFFICIENT_STOCK');
      expect(await g2.cart(), 'Then 4: nothing added').toEqual([]); // RED vs R-3/R-12 (doubt for S7): expected [] for a fresh guest jar; observed one line qty 5
    } finally {
      await g2.clear();
      await g2.dispose();
    }
  });

  test('@api TC-001 Thens 5-6 invalid input is refused with one error class, cart unchanged, session still adds', async () => {
    const g = await CartSession.open();
    const badQuantities: Array<[string, unknown]> = [
      ['qty-0', 0],
      ['qty-1000', 1000],
      ['qty-minus-1', -1],
      ['qty-1.5', 1.5],
      ['qty-abc', 'abc'],
    ];
    const badBooks: Array<[string, unknown]> = [
      ['book-missing', undefined],
      ['book-0', 0],
      ['book-unknown', 2_000_000_000],
    ];
    try {
      expect((await g.add(book.id, 1)).status(), 'base: the session adds').toBe(201);
      const before = await g.cart();
      expect(before.length).toBe(1);

      const codes: Record<string, string> = {};
      for (const [name, q] of badQuantities) {
        const r = await g.add(book.id, q);
        expect(r.status(), `Then 5: ${name} refused`).toBe(400);
        codes[name] = (await errorOf(r)).code;
        expect(await g.cart(), `Then 6: cart unchanged after ${name}`).toEqual(before);
      }
      expect(new Set(Object.values(codes)).size, `Then 5: one error code for bad quantities, got ${JSON.stringify(codes)}`).toBe(1);

      const bookCodes: Record<string, string> = {};
      for (const [name, id] of badBooks) {
        const r = await g.add(id, 1);
        expect(r.ok(), `Then 5: ${name} is not a 2xx`).toBe(false);
        bookCodes[name] = (await errorOf(r)).code;
        expect(await g.cart(), `Then 6: cart unchanged after ${name}`).toEqual(before);
      }
      expect(bookCodes['book-missing'], 'Then 5: same class of input, same code').toBe(bookCodes['book-0']);

      expect((await g.add(book.id, 1)).status(), 'Then 6: an allowed add by the same session succeeds').toBe(201);
      expect((await g.cart())[0].quantity).toBe(2);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });
});

test.describe('TC-002 out-of-stock book', () => {
  test('@api TC-002 Thens 1-2 stock-0 add is refused with an out-of-stock reason; cart unchanged', async () => {
    const g = await CartSession.open();
    try {
      const before = await g.cart();
      expect(before, 'empty own session').toEqual([]);
      const r = await g.add(soldOut.id, 1);
      expect(r.ok(), 'Then 1: not a 2xx').toBe(false);
      // Wording is open (Q1): only the out-of-stock reason is asserted.
      expect((await errorOf(r)).code, 'Then 1: out-of-stock reason').toBe('OUT_OF_STOCK');
      expect(await g.cart(), 'Then 2: no line, cart as before').toEqual(before);
      expect((await g.add(book.id, 1)).status(), 'control: the session still adds an in-stock book').toBe(201);
    } finally {
      await g.clear();
      await g.dispose();
    }
  });
});
