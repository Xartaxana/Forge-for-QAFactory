import { APIRequestContext, APIResponse, request as pwRequest } from '@playwright/test';
import { cfg } from '../config';

export interface CartLine {
  id: number;
  bookId: number;
  quantity: number;
  userId: number | null;
  sessionId: string | null;
}

export interface ApiErrorBody {
  error: string;
  code: string;
}

export interface BookRow {
  id: number;
  stockQuantity: number;
  price: number;
}

// One cookie jar = one owner of a cart (a guest, or a signed-in account).
export class CartSession {
  private constructor(readonly ctx: APIRequestContext) {}

  static async open(): Promise<CartSession> {
    // A fresh context without the project's storageState: the jar starts as a guest.
    const ctx = await pwRequest.newContext({ baseURL: cfg.API_URL + '/' });
    return new CartSession(ctx);
  }

  async signIn(email: string, password: string): Promise<void> {
    const csrf = (await (await this.ctx.get('auth/csrf')).json()) as { csrfToken: string };
    const r = await this.ctx.post('auth/callback/credentials', {
      form: { csrfToken: csrf.csrfToken, email, password, json: 'true' },
    });
    if (!r.ok()) throw new Error(`sign-in answered ${r.status()}`);
    const session = (await (await this.ctx.get('auth/session')).json()) as { user?: { email: string } };
    if (!session.user) throw new Error('sign-in did not start a session');
  }

  add(bookId: unknown, quantity: unknown): Promise<APIResponse> {
    return this.ctx.post('cart', { data: { bookId, quantity } });
  }

  async cart(): Promise<CartLine[]> {
    const r = await this.ctx.get('cart');
    if (!r.ok()) throw new Error(`GET cart answered ${r.status()}`);
    return (await r.json()) as CartLine[];
  }

  async total(): Promise<number> {
    return (await (await this.ctx.get('cart/total')).json()) as number;
  }

  merge(): Promise<APIResponse> {
    return this.ctx.post('cart/merge');
  }

  async clear(): Promise<void> {
    await this.ctx.delete('cart');
  }

  // Admin-side data owned by a test: a book with a chosen stock, removed afterwards.
  async createBook(title: string, price: number, stockQuantity: number): Promise<BookRow> {
    const r = await this.ctx.post('books', { data: { title, author: 'QA Factory', price, stockQuantity } });
    if (r.status() !== 201) throw new Error(`createBook answered ${r.status()}`);
    return (await r.json()) as BookRow;
  }

  async deleteBook(id: number): Promise<void> {
    await this.ctx.delete(`books/${id}`);
  }

  async dispose(): Promise<void> {
    await this.ctx.dispose();
  }
}

export async function errorOf(r: APIResponse): Promise<ApiErrorBody> {
  return (await r.json()) as ApiErrorBody;
}

export const userAccount = () => ({
  email: process.env.USER_EMAIL ?? '',
  password: process.env.USER_PASSWORD ?? process.env.USER_PASS ?? '',
});
