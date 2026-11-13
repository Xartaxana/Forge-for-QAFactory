import { BasePage } from './BasePage';
import { Locator } from '@playwright/test';

export class WishlistPage extends BasePage {
  readonly navWishlistButton: Locator = this.byId('nav-wishlist-button');
  readonly wishlistPage: Locator = this.byId('wishlist-page');
  moveButton(bookId: number): Locator { return this.byId(`wishlist-move-${bookId}`); }

  async open(): Promise<void> {
    await this.navWishlistButton.click();
    await this.wishlistPage.waitFor();
  }
  async moveToCart(bookId: number): Promise<void> { await this.moveButton(bookId).click(); }
}
