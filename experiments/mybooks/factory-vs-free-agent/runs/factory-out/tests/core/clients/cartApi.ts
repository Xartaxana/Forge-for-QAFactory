import { APIRequestContext, expect } from '@playwright/test';

export interface CartLine { id: number; bookId: number; quantity: number }

/** Reads and cleans state through the stand's API, with the browser context's own cookies. */
export class CartApi {
  constructor(private readonly request: APIRequestContext) {}

  /** Signs the context in through the stand's credentials endpoint (the cookies stay in this context). */
  async signIn(email: string, password: string): Promise<void> {
    const csrf = (await (await this.request.get('/api/auth/csrf')).json()) as { csrfToken: string };
    const r = await this.request.post('/api/auth/callback/credentials', {
      form: { csrfToken: csrf.csrfToken, email, password, json: 'true' },
    });
    expect(r.ok(), `sign-in answered ${r.status()}`).toBeTruthy();
    const session = (await (await this.request.get('/api/auth/session')).json()) as { user?: { email: string } };
    expect(session.user, 'sign-in started a session').toBeTruthy();
  }
  async cart(): Promise<CartLine[]> {
    const res = await this.request.get('/api/cart');
    expect(res.ok()).toBeTruthy();
    return await res.json();
  }
  async add(bookId: number, quantity: number) {
    return this.request.post('/api/cart', { data: { bookId, quantity } });
  }
  async clear(): Promise<void> {
    await this.request.delete('/api/cart');
  }
  async wishlistAdd(bookId: number): Promise<void> {
    const res = await this.request.post('/api/wishlist', { data: { bookId } });
    expect(res.ok(), `setup: wishlist add answered ${res.status()} ${await res.text()}`).toBeTruthy();
  }
  async wishlistRemove(bookId: number): Promise<void> {
    await this.request.delete(`/api/wishlist/${bookId}`);
  }
}
