# Study: redirect add to cart to the menu, not the detail page

Timestamp: 1789464788

## Goal

Change the product detail page's "Add to cart" form so a submission
redirects to the menu page, not back to the detail page. The flash
message shows on the menu. Decide whether the `next` whitelist logic
in `add_to_cart` is still necessary, or should shrink.

## Correction: the menu row has no add-to-cart button anymore

The request describes "the menu-row add-to-cart button" as already
redirecting to the menu correctly. That button no longer exists.
`doc/study/1789464109_remove-menu-add-to-cart.md` and
`doc/plan/1789464280_remove-menu-add-to-cart.md`, both merged to
`main`, removed it. Today the product detail page is the only place
in the app that posts to `core:add_to_cart`. This study reads the
request as: make that one remaining form redirect to the menu, in
place of the detail page it redirects to now.

## Current state, read from the codebase

`core/templates/core/product_detail.html` posts with a hidden field:

```
<form method="post" action="{% url 'core:add_to_cart' product.id %}">
    {% csrf_token %}
    <input type="hidden" name="next" value="detail">
    <label for="quantity">Quantity</label>
    <input type="number" id="quantity" name="quantity" min="1" value="1">
    <button type="submit">Add to cart</button>
</form>
```

`core/views.py` `add_to_cart` branches on that field:

```
if request.POST.get("next") == "detail":
    redirect_target = redirect("core:product_detail", pk=product_id)
else:
    redirect_target = redirect("core:menu")
```

`redirect_target` is used on both the validation-failure path (a
non-integer or a sub-1 quantity) and the success path.

## Is the next whitelist still needed

No caller other than the detail page exists. After this change, the
detail page wants `core:menu` too, on both success and failure. That
makes every current caller want the same single destination. A
whitelist earns its keep when more than one destination is real and
in use; with one destination and one caller, the branch decides
nothing. The `next` field, the hidden input that sets it, and the
`if/else` in `add_to_cart` should all go. `add_to_cart` should
unconditionally `return redirect("core:menu")` wherever it redirects
today, on both the failure branch and the success branch.

Keeping the field "for later" is not free: it is one more input to
read, one more value to validate against a whitelist, and one more
thing a future reader has to trace to learn it can only ever be
`"detail"` today. A future feature that needs a second destination can
reintroduce a `next` field then, sized to what it needs at that time.

## What the template needs

Remove the `<input type="hidden" name="next" value="detail">` line
from `core/templates/core/product_detail.html`. Nothing else on that
page changes.

## What the view needs

In `add_to_cart`, replace the `if request.POST.get("next") ==
"detail": ... else: ...` block with a single
`redirect_target = redirect("core:menu")`, used on both branches as it
is today. No other line in `add_to_cart` changes: the quantity
parsing, the `get_or_create`, and the flash messages are unaffected.

## This reverses a previously verified requirement

`doc/plan/1789462739_product-detail-page.md`, section 6, verified:
"From the detail page, submit quantity 0, then 'abc'. Confirm an
error message, no CartItem write, and the redirect stays on the
detail page." That was correct when the detail page was one of two
callers with two distinct destinations. After this change, a bad
quantity from the detail page redirects to the menu, with the error
message shown there, not on the page the visitor was just looking at.
This is a deliberate change in this feature's direction, not a defect
in the earlier one. The plan step should verify the new behavior, not
try to preserve the old one.

## Wiki impact for the sync docs step

`doc/wiki/routes.md`, under "Notes", documents the current `next`
field and its two values. Once `next` is gone, this note describes
code that no longer exists. The `sync docs` step for this feature
should replace it with a single line: `add_to_cart` always redirects
to `core:menu`.

## Tradeoffs and open items for the plan step

- No model change, no migration, no new route.
- A visitor on the detail page who adds a product now leaves that
  page on submission, success or failure. This matches the request.
- If a later feature wants to keep the visitor on the detail page
  after adding (for example, adding several different quantities in a
  row without a trip back through the menu), it would need to
  reintroduce a redirect target then, not now.
