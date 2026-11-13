import { test, expect } from '@playwright/test';
import { CartSession, BookRow, userAccount } from '../../../core/clients/cartClient';
import { cfg } from '../../../core/config';

// Both cases use the one seeded user account, so the file runs in order in one worker and
// empties that account's cart before and after each test.
test.describe.configure({ mode: 'default' });

const tag = `QA-LOCAL1-OWN-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;

let admin: CartSession;
let bookA: BookRow;
let bookB: BookRow;
let bookC: BookRow;

async function userSession(): Promise<CartSession> {
  const u = userAccount();
  const s = await CartSession.open();
  await s.signIn(u.email, u.password);
  return s;
}

test.beforeAll(async () => {
  admin = await CartSession.open();
  await admin.signIn(cfg.EMAIL_USER, cfg.EMAIL_PASS);
  bookA = await admin.createBook(`${tag}-A`, 11.5, 10);
  bookB = await admin.createBook(`${tag}-B`, 7.25, 10);
  bookC = await admin.createBook(`${tag}-C`, 5.0, 10);
});

test.afterAll(async () => {
  const u = await userSession();
  await u.clear();
  await u.dispose();
  for (const b of [bookA, bookB, bookC]) await admin.deleteBook(b.id);
  await admin.dispose();
});

test.beforeEach(async () => {
  const u = await userSession();
  await u.clear();
  await u.dispose();
});

const linesOf = (lines: { bookId: number; quantity: number }[]) =>
  lines.map((l) => [l.bookId, l.quantity]).sort((a, b) => a[0] - b[0]);

test.describe('TC-004 sign-in merges the guest cart', () => {
  test('@api TC-004 Then 1 P-guest-only: a guest-only book appears in the user cart with its quantity', async () => {
    const jar = await CartSession.open();
    try {
      expect((await jar.add(bookA.id, 2)).status(), 'guest add').toBe(201);
      const u = userAccount();
      await jar.signIn(u.email, u.password);
      expect((await jar.merge()).status(), 'merge after sign-in').toBe(200);
      const lines = await jar.cart();
      expect(lines.length, 'Then 1: one merged line').toBe(1);
      expect(linesOf(lines), 'Then 1: book A with quantity 2').toEqual([[bookA.id, 2]]);
    } finally {
      await jar.clear();
      await jar.dispose();
    }
  });

  test('@api TC-004 Then 2 P-both: the book in both carts keeps the higher quantity, not the sum, once', async () => {
    const pre = await userSession();
    expect((await pre.add(bookB.id, 5)).status(), 'user cart before').toBe(201);
    expect(linesOf(await pre.cart()), 'base: user cart holds B x5 before sign-in').toEqual([[bookB.id, 5]]);
    await pre.dispose();

    const jar = await CartSession.open();
    try {
      expect((await jar.add(bookB.id, 3)).status(), 'guest add B').toBe(201);
      expect((await jar.add(bookC.id, 2)).status(), 'guest add guest-only C').toBe(201);
      const u = userAccount();
      await jar.signIn(u.email, u.password);
      expect((await jar.merge()).status()).toBe(200);
      const lines = await jar.cart();
      // Q12 answered: the higher quantity wins (AUTH.md). User 5 / guest 3: higher = 5, sum = 8,
      // guest replaces = 3; guest-only C x2 proves the merge ran (a no-op merge gives only [B,5]).
      expect(lines.length, 'Then 2: B once and C merged, none missing or duplicated').toBe(2);
      expect(linesOf(lines), 'Then 2: B quantity 5 (higher wins, not 8 or 3), C x2 from the guest').toEqual([
        [bookB.id, 5],
        [bookC.id, 2],
      ]);
    } finally {
      await jar.clear();
      await jar.dispose();
    }
  });

  test('@api TC-004 Then 4 P-above-stock: no merged line exceeds stock; pre-existing user lines stay', async () => {
    const pre = await userSession();
    expect((await pre.add(bookC.id, 1)).status(), 'user cart before').toBe(201);
    await pre.dispose();

    const jar = await CartSession.open();
    try {
      expect((await jar.add(bookA.id, 8)).status(), 'guest adds 8 of stock 10').toBe(201);
      // Stock falls under the guest quantity between the add and the sign-in.
      const lower = await admin.ctx.put(`books/${bookA.id}`, { data: { stockQuantity: 3 } });
      expect(lower.ok(), 'own book stock lowered').toBe(true);
      const u = userAccount();
      await jar.signIn(u.email, u.password);
      expect((await jar.merge()).status()).toBe(200);
      const lines = await jar.cart();
      const merged = lines.find((l) => l.bookId === bookA.id);
      expect(merged, 'Then 4: the book is merged').toBeDefined();
      expect(merged!.quantity, 'Then 4: merged quantity does not exceed stock 3').toBeLessThanOrEqual(3);
      expect(lines.find((l) => l.bookId === bookC.id)?.quantity, 'Then 4: pre-existing line unchanged').toBe(1);
    } finally {
      await jar.clear();
      await jar.dispose();
      await admin.ctx.put(`books/${bookA.id}`, { data: { stockQuantity: 10 } });
    }
  });
});

test.describe('TC-005 a cart belongs to its owner only', () => {
  test('@api TC-005 Thens 1-3 guests stay apart and the user add touches no guest cart', async () => {
    const g1 = await CartSession.open();
    const g2 = await CartSession.open();
    const u = await userSession();
    try {
      expect((await g1.add(bookA.id, 1)).status()).toBe(201);
      expect((await g2.add(bookB.id, 1)).status()).toBe(201);
      expect.soft(linesOf(await g1.cart()), 'Then 1: G1 holds only A').toEqual([[bookA.id, 1]]);
      expect.soft(linesOf(await g2.cart()), 'Then 1: G2 holds only B').toEqual([[bookB.id, 1]]);

      expect((await u.add(bookC.id, 1)).status(), 'Then 3: the account adds').toBe(201);
      expect(linesOf(await g1.cart()), 'Then 2: G1 unchanged').toEqual([[bookA.id, 1]]);
      expect(linesOf(await g2.cart()), 'Then 2: G2 unchanged').toEqual([[bookB.id, 1]]);
      expect(linesOf(await u.cart()), 'Then 3: user holds C and no guest book').toEqual([[bookC.id, 1]]);
    } finally {
      await g1.clear();
      await g2.clear();
      await u.clear();
      for (const s of [g1, g2, u]) await s.dispose();
    }
  });
});
