import { BasePage } from './BasePage';
import { Locator } from '@playwright/test';

export class CartPage extends BasePage {
  readonly cartPageElement: Locator = this.byId('cart-page');
  readonly emptyCartMessage: Locator = this.byId('empty-cart-message');
  readonly navCartButton: Locator = this.byId('nav-cart-button');
  readonly cartCountBadge: Locator = this.byId('cart-count-badge');
  readonly lines: Locator = this.page.locator('[data-testid^="cart-item-"]:not([data-testid^="cart-item-quantity-"]):not([data-testid^="cart-item-subtotal-"])');

  line(cartItemId: number): Locator { return this.byId(`cart-item-${cartItemId}`); }
  quantityInput(cartItemId: number): Locator { return this.byId(`cart-item-quantity-${cartItemId}`); }
  subtotal(cartItemId: number): Locator { return this.byId(`cart-item-subtotal-${cartItemId}`); }

  async openFromNav(): Promise<void> {
    await this.navCartButton.click();
    await this.cartPageElement.waitFor();
  }

  async badgeText(): Promise<string | null> {
    return (await this.cartCountBadge.count()) === 0 ? null : (await this.cartCountBadge.innerText()).trim();
  }

  /** Sum of the quantity inputs of all lines on the cart page. */
  async unitsOnPage(): Promise<number> {
    const inputs = this.page.locator('[data-testid^="cart-item-quantity-"]');
    const n = await inputs.count();
    let total = 0;
    for (let i = 0; i < n; i++) total += Number(await inputs.nth(i).inputValue());
    return total;
  }
}
