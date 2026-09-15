# Study: menu greeting and add-to-cart flash message

Timestamp: 1789461631

## Goal

Add two small pieces to the menu page.

1. A greeting line for a logged-in user, for example "Hi, christine123!".
   The greeting shows only when the user is logged in.
2. A flash message after "Add to cart", for example "Added 1 of
   Americano to your cart".

## Current state, read from the codebase

- `core/templates/base.html` already renders `django.contrib.messages`.
  It has an `{% if messages %}` block that loops over `messages` and
  prints each one in an `<li class="{{ message.tags }}">`. Every page
  that extends `base.html` already gets this block, menu included.
- `core/static/core/style.css` already styles `.messages li.success`
  and `.messages li.error`. A `messages.success(...)` call needs no new
  CSS.
- `MIDDLEWARE` in `digitalcafe/settings.py` already has
  `SessionMiddleware` and `MessageMiddleware`, in that order. The
  default message storage (`FallbackStorage`) needs both, and both are
  present. No settings change is necessary.
- The `TEMPLATES` `OPTIONS.context_processors` list already has
  `django.contrib.auth.context_processors.auth`. This puts `user` in
  the context of every template, menu included, with no view change.
- `core.views.add_to_cart` (`core/views.py`) is `POST` only, and ends
  with `return redirect("core:menu")`. A message added in this view,
  before the redirect, survives the redirect and shows on the next
  render of the menu page. This is the page the user lands on, so no
  extra redirect target logic is necessary.
- `core.views.add_to_cart` always adds one unit: a first add creates a
  `CartItem` with `quantity=1`, a repeat add increases `quantity` by 1.
  "Added 1 of Americano to your cart" reads as this per-click increase,
  not the running total in the cart. The view already has both
  `product` and this increase amount in scope, so the message text
  needs no extra query.

## Where the greeting belongs: base.html vs menu.html

The request scopes this to the menu page, not every page. Two options:

**Put it in `base.html`.** One block serves every page. The cost: the
request only asked for the menu page, and `base.html` has no per-page
condition today. Adding one, for example a check on `request.path` or
a new template block that most pages leave empty, adds a mechanism the
task does not need. `base.html` also already shows the username in the
nav bar (`{{ user.username }}` next to the "Log out" button), so a
second greeting in the header would repeat that line for every page,
not only the menu.

**Put it in `menu.html`.** The check is
`{% if user.is_authenticated %}Hi, {{ user.username }}!{% endif %}`
inside the existing `{% block content %}`. `user` is already in
context through the auth context processor, so this needs no view
change. The greeting shows only where asked, and every other page
stays as it is.

The second option fits the request as given and adds no new mechanism.
The plan should place the greeting in `menu.html`.

## How the flash message should render

`base.html` already renders `messages` for every page. This part of
the task needs no template change at all. The only change is in
`core.views.add_to_cart`: call `messages.success(...)` with the text
before the `return redirect("core:menu")` line. Django's messages
framework carries the message across the redirect through the session,
so it prints once, on the menu page the user already lands on.

## Tradeoffs and open items for the plan step

- The message text needs the product name and the fixed amount "1".
  A view-side f-string is enough: no template filter or tag is
  necessary.
- No change to `base.html`, `style.css`, or `settings.py` is
  necessary for the message. Every dependency for it already exists in
  the merged v1 code.
- The greeting in `menu.html` duplicates the pattern already in the nav
  bar (`{% if user.is_authenticated %}`). If a later feature wants the
  same greeting on more than one page, the plan step should weigh a
  shared include against copy-paste. For two lines of markup on one
  page, copy-paste is enough today.
