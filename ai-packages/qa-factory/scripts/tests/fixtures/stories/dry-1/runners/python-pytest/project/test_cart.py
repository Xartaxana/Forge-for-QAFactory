"""The one test the synthetic project holds: the cart total of lines with a quantity (the subject of story dry-1)."""


def cart_total(lines):
    return sum(line["price"] * line.get("quantity", 1) for line in lines)


def test_cart_total_multiplies_price_by_quantity():
    assert cart_total([{"price": 5, "quantity": 2}, {"price": 3}]) == 13
