# Plan: product detail page with a quantity field

Timestamp: 1789462739
Study: doc/study/1789462532_product-detail-page.md

Design decisions carried over from the study:

- Route: `path("product/<int:pk>/", views.product_detail,
  name="product_detail")` in `core/urls.py`, GET only, no login.
- `add_to_cart` gains two optional POST fields: `quantity` (default
  "1") and `next` (one of "menu" or "detail", resolved with
  `reverse()`, never a raw path).
- The success message reads the submitted quantity, not a fixed "1".
- `CartItem.quantity` gets a database-level `CheckConstraint`, so an
  invalid quantity cannot reach the database even if the view-level
  check is ever bypassed or a future caller writes to `CartItem`
  directly.

Nothing here needs input from you. Every value below is something this
session can create on its own.

## Task board

### 1. Add a database check constraint on CartItem.quantity

- [x] In `core/models.py`, add
      `models.CheckConstraint(condition=models.Q(quantity__gt=0),
      name="cart_item_quantity_gt_zero")` to `CartItem.Meta.constraints`
- [x] Run `makemigrations` and `migrate`

### 2. Add the product detail route and 3. extend add_to_cart

`core/urls.py` calls `views.product_detail` directly in a `path()`
entry, not by string, so the route and the view must exist in the same
commit. A route added alone would raise `AttributeError` on import at
the section 2 checkpoint. Sections 2 and 3 build as one commit.

- [x] In `core/urls.py`, add `path("product/<int:pk>/",
      views.product_detail, name="product_detail")`
- [x] Write the `product_detail` view: fetch the product with
      `get_object_or_404`, render `core/product_detail.html`
- [x] In `add_to_cart`, read `quantity` from POST, default `"1"`.
      Reject a non-integer or a value under 1 with an error message.
      Do not write to `CartItem` on rejection
- [x] Read `next` from POST. Accept only `"detail"` as a special case,
      resolved with `redirect("core:product_detail", pk=product_id)`
      using the `product_id` already in the URL. Fall back to
      `core:menu` for any other value, including a missing field
- [x] Change the `get_or_create` defaults and the repeat-add branch to
      use the submitted quantity, not a fixed 1
- [x] Update the success message to read the submitted quantity, for
      example "Added 3 of Americano to your cart."

### 4. Add the product detail template

- [ ] Write `core/templates/core/product_detail.html`, extending
      `base.html`. Show the product name and price
- [ ] When `user.is_authenticated`, show a form posting to
      `core:add_to_cart`: a `quantity` number input (`min="1"`,
      `value="1"`), a hidden `next` field set to `"detail"`, and the
      product id

### 5. Update the menu template

- [ ] Rename the "Product" header to "Product Name"
- [ ] Wrap `{{ product.name }}` in a link to `core:product_detail`
- [ ] Add a hidden `next` field set to `"menu"` to the existing
      add-to-cart form

### 6. Manual verification, before rendezvous

- [ ] Confirm `makemigrations` and `migrate` run with no error
- [ ] Confirm the new constraint holds: a direct attempt to save a
      `CartItem` with `quantity=0` raises an `IntegrityError`
- [ ] View a product detail page while logged out. Confirm no
      add-to-cart form shows
- [ ] View a product detail page while logged in. Add a quantity of 3.
      Confirm `CartItem.quantity` is 3 and the message reads "Added 3
      of \<product name\> to your cart."
- [ ] From the detail page, submit quantity 0, then "abc". Confirm an
      error message, no `CartItem` write, and the redirect stays on
      the detail page
- [ ] From the menu page, use the one-click button. Confirm quantity 1
      and the redirect returns to the menu
- [ ] Click a product name on the menu. Confirm it opens the detail
      page for that product
- [ ] Confirm the menu header reads "Product Name"
