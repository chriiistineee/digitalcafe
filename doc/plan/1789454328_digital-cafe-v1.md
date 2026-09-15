# Plan: Digital Cafe v1

Timestamp: 1789454328
Study: doc/study/1789454045_digital-cafe-v1.md

Design decisions carried over from the study open items:

- Base template: a single `base.html` with a nav bar. The nav bar shows
  login state, a link to the menu, the cart, and history when logged in.
- Remove-from-cart: a small POST form per row, not a GET link.
- Static files: `core/static/core/style.css`.

Nothing here needs input from you. Every value below (seed products,
config) is something this session can create on its own.

## Task board

### 1. Project scaffolding

- [x] Run `django-admin startproject digitalcafe .`
- [x] Run `python manage.py startapp core`
- [x] Add `core` to `INSTALLED_APPS`
- [x] Add `core.urls` to the project `urls.py`
- [x] Run `python manage.py migrate` for the default Django apps

### 2. Data model

- [x] Write `Product` in `core/models.py`
- [x] Write `CartItem`, with a unique constraint on `(user, product)`
- [x] Write `Transaction`
- [x] Write `LineItem`
- [x] Run `makemigrations` and `migrate`

### 3. Admin

- [x] Register `Product`, `CartItem`, `LineItem`, and `Transaction` in
      `core/admin.py`

### 4. Auth

- [x] Write a registration view, form, and template at `/register/`
- [x] Wire `/login/` to the built-in `LoginView`
- [x] Wire `/logout/` to the built-in `LogoutView`
- [x] Set `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` in settings
- [x] Write `templates/registration/login.html`

### 5. Base template and CSS

- [x] Write `base.html` with the nav bar described above
- [x] Write `core/static/core/style.css` and link it in `base.html`

### 6. Menu page

- [x] Write the menu view at `/` and `/menu/`
- [x] Write `menu.html`. List every product with an "Add to cart" form
      per row, shown only when logged in

### 7. Cart

- [ ] Write `add_to_cart` (POST only). Look up an existing `CartItem`
      before it creates a new one, then increase the quantity
- [ ] Write the cart view (GET). Show each item, its subtotal, and a
      cart total
- [ ] Write `remove_from_cart` (POST only)
- [ ] Write `cart.html`

### 8. Checkout

- [ ] Write the checkout view (POST only)
- [ ] Reject an empty cart before any write
- [ ] Wrap the `Transaction` and `LineItem` creation, plus the cart
      deletion, in `transaction.atomic()`
- [ ] Redirect to the history page after checkout

### 9. Transaction history

- [ ] Write the history view. Filter `Transaction` by
      `user=request.user`
- [ ] Write `history.html`. List each transaction with its number,
      date, and line items

### 10. Manual verification, before rendezvous

- [ ] Confirm `makemigrations` and `migrate` run with no error
- [ ] Register a user, log in, log out
- [ ] Add two or three sample products through the admin
- [ ] Add a product to the cart, then remove it
- [ ] Add a product to the cart twice. Confirm the quantity increases
      on one row instead of a duplicate row
- [ ] Check out a non-empty cart. Confirm the cart empties and the
      transaction appears in history
- [ ] Try to check out an empty cart. Confirm the app rejects it
- [ ] Register a second user. Confirm this user cannot see the first
      user's history
