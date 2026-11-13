import { BasePage } from './BasePage';
import { Locator } from '@playwright/test';

export class CatalogPage extends BasePage {
  readonly homePage: Locator = this.byId('home-page');
  cardAddButton(bookId: number): Locator { return this.byId(`add-to-cart-button-${bookId}`); }

  bookLink(bookId: number): Locator { return this.byId(`book-link-${bookId}`); }

  async open(query?: string): Promise<void> {
    await this.page.goto(query ? `/?query=${encodeURIComponent(query)}` : '/');
    await this.homePage.waitFor();
  }
  async addFromCard(bookId: number): Promise<void> { await this.cardAddButton(bookId).click(); }
}
