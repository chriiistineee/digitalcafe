# Study: redirect add to cart to the menu, not the detail page

Timestamp: 1789464788

## Goal

Change the product detail page's "Add to cart" form so a successful
submission redirects to the menu page, with the flash message shown
there. A rejected quantity keeps the redirect on the detail page, so
the visitor can fix the value and resubmit without a trip back through
the menu. Decide whether the `next` whitelist logic in `add_to_cart`
is still necessary, or should shrink.

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

No. The two destinations still exist, `core:menu` on success and
`core:product_detail` on a rejected quantity, but which one applies no
longer depends on which page the form was submitted from. Only one
page submits it. It depends entirely on whether the quantity was
valid, a fact `add_to_cart` already computes for itself. The view does
not need a caller to tell it where to go; it already knows, from its
own validation result and the `product_id` already in the URL.

This removes the `next` field, the hidden input that sets it, and the
whitelist read from `request.POST`, replacing all three with two plain
`redirect(...)` calls, one on each existing branch. It is a stronger
simplification than dropping `next` down to a single fixed value: no
value taken from the request body decides a redirect target anymore,
so the open-redirect concern the original whitelist existed to guard
against no longer has anything to guard.

## What the template needs

Remove the `<input type="hidden" name="next" value="detail">` line
from `core/templates/core/product_detail.html`. Nothing else on that
page changes.

## What the view needs

In `add_to_cart`, delete the `if request.POST.get("next") ==
"detail": ... else: ...` block. In its place:

- On a rejected quantity (a non-integer or a value under 1), redirect
  to `redirect("core:product_detail", pk=product_id)`, in the same
  branch that already sets the error message.
- On success, redirect to `redirect("core:menu")`, in the same branch
  that already sets the success message.

No other line in `add_to_cart` changes: the quantity parsing, the
`get_or_create`, and the flash message text are unaffected.

## A previously verified requirement is partly preserved, partly changed

`doc/plan/1789462739_product-detail-page.md`, section 6, verified:
"From the detail page, submit quantity 0, then 'abc'. Confirm an
error message, no CartItem write, and the redirect stays on the
detail page." With this design, that line stays true: an invalid
quantity still redirects back to the detail page. What changes is the
success path, which used to also land on the detail page (through
`next=detail`) and now lands on the menu instead. The plan step should
verify both: the error case stays on the detail page, matching the
earlier requirement, and the success case now goes to the menu.

## Wiki impact for the sync docs step

`doc/wiki/routes.md`, under "Notes", documents the current `next`
field and its two caller-supplied values. Once `next` is gone, this
note describes code that no longer exists. The `sync docs` step for
this feature should replace it with a line describing the new,
outcome-based behavior: a valid quantity redirects to `core:menu`; a
rejected one redirects back to `core:product_detail`.

## Tradeoffs and open items for the plan step

- No model change, no migration, no new route.
- A visitor on the detail page who submits a bad quantity stays there
  and can fix it. One who successfully adds a product moves on to the
  menu. This matches the request.
- If a later feature adds a second caller with its own idea of where
  success should land, a `next`-style field would earn its cost again
  at that point. Nothing here should try to anticipate that.
