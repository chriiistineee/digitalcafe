# Plan: remove the Add to cart button from the menu

Timestamp: 1789464280
Study: doc/study/1789464109_remove-menu-add-to-cart.md

Design decision carried over from the study: this is a template-only
change. Neither the `menu` view nor `add_to_cart` in `core/views.py`
needs a code change. The `else` branch in `add_to_cart` that falls
back to `core:menu` stays as a default, unreached through the UI once
this change lands, but not removed.

Nothing here needs input from you. Every value below is something this
session can create on its own.

## Task board

### 1. Remove the button and column from menu.html

- [ ] Remove the third `<th>`, the one with no header text
- [ ] Remove the third `<td>` in each row: the
      `{% if user.is_authenticated %}` block and the add-to-cart form
      inside it
- [ ] Change the empty-state row from `colspan="3"` to `colspan="2"`

### 2. Manual verification, before rendezvous

- [ ] Confirm the menu table shows two columns: "Product Name" and
      "Price (PHP)"
- [ ] Confirm no "Add to cart" button shows on the menu, logged in or
      logged out
- [ ] Click a product name on the menu. Confirm the detail page opens,
      and its own "Add to cart" form still adds the chosen quantity
- [ ] Confirm the cart, checkout, and history pages still render with
      no error
