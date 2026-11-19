import { test, expect } from "@playwright/test";

type Line = { price: number; quantity?: number };

function cartTotal(lines: Line[]): number {
  return lines.reduce((sum, line) => sum + line.price * (line.quantity ?? 1), 0);
}

// The page is opened for real: a missing browser fails this test, whatever the installer exit code said.
test("cart total multiplies price by quantity", async ({ page }) => {
  const total = cartTotal([{ price: 5, quantity: 2 }, { price: 3 }]);
  await page.setContent(`<p id="total">${total}</p>`);
  await expect(page.locator("#total")).toHaveText("13");
});
