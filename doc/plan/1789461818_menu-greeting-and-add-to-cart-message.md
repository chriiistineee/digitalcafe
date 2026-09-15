# Plan: menu greeting and add-to-cart flash message

Timestamp: 1789461818
Study: doc/study/1789461631_menu-greeting-and-add-to-cart-message.md

Design decisions carried over from the study:

- The greeting goes in `menu.html`, not `base.html`. The request scopes
  it to the menu page, and `base.html` already shows the username in
  the nav bar.
- The flash message needs no template or settings change. `base.html`,
  `style.css`, `SessionMiddleware`, and `MessageMiddleware` already
  support it. Only `add_to_cart` in `core/views.py` changes.

Nothing here needs input from you. Every value below is something this
session can create on its own.

## Task board

### 1. Add the greeting to the menu page

- [ ] In `core/templates/core/menu.html`, inside `{% block content %}`,
      add a line shown only when `user.is_authenticated`: "Hi,
      {{ user.username }}!"

### 2. Add the add-to-cart flash message

- [ ] In `core/views.py`, in `add_to_cart`, call `messages.success`
      with the product name before `return redirect("core:menu")`
- [ ] Match the wording style of the existing checkout messages, for
      example "Added 1 of Americano to your cart."

### 3. Manual verification, before rendezvous

- [ ] Log in, view the menu. Confirm the greeting shows the username
- [ ] Log out, view the menu. Confirm the greeting does not show
- [ ] Log in, add a product to the cart. Confirm the menu page shows
      "Added 1 of \<product name\> to your cart" after the redirect
- [ ] Confirm the flash message renders with the `success` style, not
      the `error` style
- [ ] Add the same product a second time. Confirm the message still
      reads "Added 1 of \<product name\>", not the running cart total
- [ ] Confirm the cart page and history page still render with no
      error
