# Data model

Four models, all in `core/models.py`.

## Product

| Field | Type | Notes |
|---|---|---|
| name | CharField(200) | |
| price | DecimalField(10, 2) | PHP |

## CartItem

| Field | Type | Notes |
|---|---|---|
| user | ForeignKey(User) | on_delete=CASCADE |
| product | ForeignKey(Product) | on_delete=CASCADE |
| quantity | PositiveIntegerField | |

A unique constraint on `(user, product)` keeps one row per product in a
cart. The `add_to_cart` view increases the quantity on a repeat add
instead of creating a second row.

A `CheckConstraint` (`quantity > 0`) rejects an invalid quantity at
the database layer. This backs up the same check in `add_to_cart`,
which is the only check once a quantity value comes from a request.

`CartItem.subtotal` is a property, not a stored field:
`quantity * product.price`.

## Transaction

| Field | Type | Notes |
|---|---|---|
| user | ForeignKey(User) | on_delete=CASCADE |
| timestamp | DateTimeField | auto_now_add |

## LineItem

| Field | Type | Notes |
|---|---|---|
| transaction | ForeignKey(Transaction) | on_delete=CASCADE, related_name `line_items` |
| product | ForeignKey(Product) | on_delete=PROTECT |
| quantity | PositiveIntegerField | |
| price | DecimalField(10, 2) | copied from Product at checkout time |

`LineItem.price` copies `Product.price` at checkout time. A later price
change does not alter a past transaction.

`LineItem.product` uses `PROTECT`. Staff cannot delete a product that
appears in a past transaction from the admin.
