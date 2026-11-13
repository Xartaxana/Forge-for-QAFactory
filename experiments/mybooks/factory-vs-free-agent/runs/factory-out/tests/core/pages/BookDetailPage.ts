import { BasePage } from './BasePage';
import { Locator } from '@playwright/test';

export class BookDetailPage extends BasePage {
  readonly detailPage: Locator = this.byId('book-detail-page');
  readonly quantityInput: Locator = this.byId('book-detail-quantity-input');
  readonly addToCartButton: Locator = this.byId('book-detail-add-to-cart-button');
  readonly wishlistToggle: Locator = this.byId('wishlist-toggle-button');

  async open(bookId: number): Promise<void> {
    await this.page.goto(`/books/${bookId}`);
    await this.detailPage.waitFor();
  }
  async setQuantity(q: number): Promise<void> { await this.quantityInput.fill(String(q)); }
  async addToCart(): Promise<void> { await this.addToCartButton.click(); }
}
