# Plan: redirect add to cart by outcome

Timestamp: 1789464996
Study: doc/study/1789464788_add-to-cart-redirect-to-menu.md

Design decision carried over from the study: drop the `next` field
entirely. `add_to_cart` decides the redirect from its own validation
result, not from a caller-supplied value. A rejected quantity
redirects to `core:product_detail`. A successful add redirects to
`core:menu`.

Nothing here needs input from you. Every value below is something this
session can create on its own.

## Task board

### 1. Remove next and branch by outcome in add_to_cart

- [x] In `core/templates/core/product_detail.html`, remove the
      `<input type="hidden" name="next" value="detail">` line
- [x] In `core/views.py` `add_to_cart`, delete the
      `if request.POST.get("next") == "detail": ... else: ...` block
- [x] On a rejected quantity, redirect to
      `redirect("core:product_detail", pk=product_id)`, in the branch
      that sets the error message
- [x] On success, redirect to `redirect("core:menu")`, in the branch
      that sets the success message

### 2. Manual verification, before rendezvous

- [x] From the detail page, submit a valid quantity. Confirm the
      redirect lands on the menu, and the flash message shows there
- [x] From the detail page, submit quantity 0, then "abc". Confirm an
      error message each time, no `CartItem` write, and the redirect
      stays on the detail page
- [x] Confirm the detail page needs no other change: the quantity
      input, the CSRF token, and the button stay as they are
- [x] Confirm the cart, checkout, and history pages still render with
      no error

Verified with a temporary Django `TestCase` run through
`manage.py test`, against an isolated test database. All four checks
passed, including a direct check that the detail page renders no
`next` field anymore. The test file was not committed.
