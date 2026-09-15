# Study: product detail page with a quantity field

Timestamp: 1789462532

## Goal

Add a product detail page. It shows the product name, the price, and
an "Add to cart" form with a quantity field. On the menu page, rename
the "Product" column header to "Product Name", and turn each product
name into a link to its detail page.

## Current state, read from the codebase

- `core/urls.py` names every route in the `core` namespace with a
  snake_case name: `menu`, `cart`, `add_to_cart`, `remove_from_cart`,
  `checkout`, `history`. A detail page fits this pattern as
  `core:product_detail`.
- `core.views.add_to_cart` (`core/views.py`) is `POST` only, and reads
  no field from the request body. It always adds exactly one unit: a
  first add creates a `CartItem` with `quantity=1`, a repeat add runs
  `cart_item.quantity += 1`. It ends with
  `messages.success(request, f"Added 1 of {product.name} to your
  cart.")`, then `return redirect("core:menu")`, a fixed target.
- `core/models.py` defines `CartItem.quantity` as `PositiveIntegerField`
  with no `Meta.constraints` entry for it and no call to `full_clean()`
  anywhere in the view layer. Django does not add a database check
  constraint for `PositiveIntegerField` on its own. Today this is safe
  because the view is the only writer and it only ever adds 1. Once a
  quantity value comes from a request body, the view becomes the only
  place that enforces "quantity must be a positive integer" from the
  original scope.
- `core/templates/core/menu.html` has a three-column table: "Product",
  "Price (PHP)", and an empty header for the "Add to cart" button. The
  product name renders as plain text, `{{ product.name }}`, inside a
  `<td>`, not a link. Each row's form posts to
  `{% url 'core:add_to_cart' product.id %}` with no hidden fields
  beyond the CSRF token.

## The URL pattern

Add `path("product/<int:pk>/", views.product_detail,
name="product_detail")` to `core/urls.py`. This matches the existing
style: an `int` converter, a trailing slash, a `core:`-namespaced name.
The view needs no login, matching the menu page. It fits alongside the
"Browsing" section of `doc/wiki/routes.md`, next to `core:menu`.

## Does add_to_cart need a quantity parameter

The request asks for a form that matches the existing `add_to_cart`
view rather than a second view with its own cart logic. Reuse keeps
the `get_or_create` and quantity-increase logic in one place. To serve
both the menu's single-click button and the detail page's quantity
field, `add_to_cart` needs two optional `POST` fields, both absent
today:

- `quantity`, read with `request.POST.get("quantity", "1")`. The menu
  form sends no `quantity` field, so it keeps adding 1 with no markup
  change. The detail page form sends a real value from a number input.
- A redirect target, so a bad quantity on the detail page does not
  bounce the visitor to the menu. See "Where should an error send the
  visitor" below.

Two consequences follow from reuse:

1. `cart_item.quantity += 1` must become
   `cart_item.quantity += quantity`, and the `defaults` on
   `get_or_create` must use the submitted quantity, not a fixed `1`.
2. The flash message must read the submitted amount, for example
   "Added 3 of Americano to your cart.", not the fixed "Added 1 of
   Americano to your cart." from the prior feature. This changes text
   that `doc/wiki/routes.md` already documents. The `sync docs` step
   for this feature needs to update that line.

## Validating the quantity

`request.POST.get("quantity", "1")` arrives as a string with no
guarantee it parses to a positive integer. A visitor could submit
`0`, `-5`, or `abc` through the same form field a browser's number
input normally blocks. Since `PositiveIntegerField` enforces nothing
at the database layer here, the view must:

1. Try `int(...)` on the value. Treat a `ValueError` the same as an
   out-of-range value, not a server error.
2. Reject a result under 1.
3. On rejection, set an error message and redirect without writing to
   `CartItem`, the same pattern `checkout` already uses for an empty
   cart.

## Where should an error send the visitor

`add_to_cart` today always redirects to `core:menu`. That is correct
for the menu's single-click button. It is wrong for the detail page: a
bad quantity there should redisplay the detail page, not jump away
from it.

**Option A: keep the fixed redirect to `core:menu`.** No new field. A
quantity error on the detail page sends the visitor to the menu
instead of back to the product they were looking at. Simple, but a
worse experience for the one form that can actually produce a
quantity error.

**Option B: add a `next` field to both forms.** The menu form sends
`next=menu`. The detail page form sends `next=product_detail` with the
product id. `add_to_cart` reads this value and redirects to whichever
page the request came from, on both success and failure.

A `next` field taken as a raw path and passed to `redirect()` would
open a redirect vulnerability: a crafted form or request could point
`next` at an external URL. The fix is to never treat `next` as a path.
Treat it as one of two known names (`"menu"` or `"detail"`), resolve
it server-side with `reverse()`, and fall back to `core:menu` for any
other value. This keeps the field data-driven without trusting
attacker-controlled input as a URL.

Option B fits the request better and costs one small, whitelisted
branch in the view. The plan should build option B.

## Menu template changes

- Change the header cell text from "Product" to "Product Name".
- Wrap `{{ product.name }}` in
  `<a href="{% url 'core:product_detail' product.id %}">`.
- Add a hidden `<input type="hidden" name="next" value="menu">` to the
  existing add-to-cart form, so it keeps redirecting to the menu after
  the `add_to_cart` view learns to honor `next`.

## Detail page template

A new `core/templates/core/product_detail.html`, extending `base.html`
like every other page. Content: the product name and price, and, only
when `user.is_authenticated` (the same guard the menu button already
uses), a form posting to `core:add_to_cart` with:

- a number input named `quantity`, `min="1"`, `value="1"`
- a hidden `next` field set to `"detail"`
- a hidden field carrying the product id, so a rejected submission can
  redirect back to this same detail page

## Tradeoffs and open items for the plan step

- Reuse of `add_to_cart` versus a second, detail-page-only view: reuse
  wins here, given the small size of the app and the request's own
  wording ("matching the existing add_to_cart view").
- The `next` field is a closed set of known names, not a raw path,
  to avoid an open redirect.
- This feature changes the wording of an existing flash message. The
  `sync docs` step must update `doc/wiki/routes.md` to match.
- No model change and no migration. `CartItem.quantity` already stores
  any positive integer.
