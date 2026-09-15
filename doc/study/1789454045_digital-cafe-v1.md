# Study: Digital Cafe v1

Timestamp: 1789454045

## Goal

A multi-page Django app for a coffee shop. A customer registers, logs in,
browses a menu, adds items to a cart, and checks out. Checkout creates a
transaction with line items. The customer views their own transaction
history. Staff manage all data through the Django admin.

## Tech stack

- Django 5.2 (Python), the latest stable release
- SQLite as the database (the Django default)
- Django templates, plain CSS, no JavaScript framework
- The built-in auth and built-in admin of Django
- Project `digitalcafe`, single app `core`

The system has Python 3.13.5 and Django 5.2 already installed. No new
dependency is necessary for v1.

## Data model

Four models, all in the `core` app.

| Model | Fields |
|---|---|
| Product | name (CharField), price (DecimalField, PHP) |
| CartItem | user (FK to User), product (FK to Product), quantity (PositiveIntegerField) |
| Transaction | user (FK to User), timestamp (DateTimeField, auto_now_add) |
| LineItem | transaction (FK to Transaction), product (FK to Product), quantity (PositiveIntegerField), price (DecimalField) |

Notes on the design:

- `LineItem.price` copies `Product.price` at checkout time. This keeps a
  past transaction correct even if a staff member changes a product price
  later. This is a deliberate denormalization, not an oversight.

- `CartItem` needs a unique constraint on `(user, product)`. Without it,
  a user could add the same product twice and get two separate cart rows
  instead of one row with an increased quantity. This affects the design
  of the "add to cart" view. That view must look up an existing row
  before it creates a new one.

- Money uses `DecimalField(max_digits=10, decimal_places=2)`. PHP has no
  subunit smaller than centavos, so two decimal places are correct. A
  FloatField would risk rounding errors in a sum.

- `PositiveIntegerField` on quantity enforces "quantity must be a positive
  integer" at the database level. Django admin and forms also validate
  this before save. The database constraint is redundant but cheap
  insurance.

## Page and route list

| Path | View | Auth required | Notes |
|---|---|---|---|
| `/register/` | register | No | Django `UserCreationForm` or a thin subclass |
| `/login/` | login | No | The built-in `LoginView` of Django |
| `/logout/` | logout | Yes | The built-in `LogoutView` of Django |
| `/` or `/menu/` | menu | No | Lists all products. An "Add to cart" button appears per row when logged in |
| `/cart/` | cart | Yes | Lists cart items, quantity, subtotal, a remove link, a checkout button |
| `/cart/add/<product_id>/` | add_to_cart | Yes | POST only |
| `/cart/remove/<item_id>/` | remove_from_cart | Yes | POST only |
| `/checkout/` | checkout | Yes | POST only. Turns the cart into a Transaction |
| `/history/` | history | Yes | Lists the own transactions of the logged-in user |

The built-in `LoginView` and `LogoutView` of Django remove the need to
write session handling by hand. `LoginRequiredMixin` or the
`login_required` decorator protects the cart, checkout, and history views.

## Checkout logic

1. Reject an empty cart. Check `CartItem.objects.filter(user=request.user)`
   for at least one row before any write. If empty, show an error message
   and redirect back to the cart page.

2. Wrap the write in `transaction.atomic()`. This is the
   `django.db.transaction` module of Django, distinct from our
   `Transaction` model. The name collision is a naming risk, noted below.

3. Create one `Transaction` row for the user.

4. For each `CartItem`, create a `LineItem` row that copies the product,
   quantity, and current price.

5. Delete all `CartItem` rows that belong to the user.

Step 2 matters. A crash between step 3 and step 5 must not leave a
half-built transaction or a stale cart. `atomic()` makes the whole
operation succeed or fail as one unit.

## Naming risk

Django ships a module `django.db.transaction`. Our data model also needs a
model named `Transaction`. Both names can coexist. Import the module as
`from django.db import transaction` and the model as
`from core.models import Transaction`. The plan doc will call this out
explicitly so the executing session does not shadow one with the other.

## Authorization: a user cannot view the history of another user

The history view must filter `Transaction.objects.filter(user=request.user)`
and never accept a transaction ID from the URL for a list view. If a detail
view per transaction is added later, it must also filter by
`user=request.user` and return 404 (not 403) for a transaction owned by
another user, to avoid confirming that the ID exists.

v1 scope, per the request, only needs a list view (transaction number,
date, line items) with no separate per-transaction detail page. This
removes the ID-in-URL exposure entirely for v1.

## Admin registration

Register all four models (`Product`, `CartItem`, `LineItem`, `Transaction`)
in `core/admin.py` with `admin.site.register(...)`. No custom `ModelAdmin`
class is necessary for v1. The default list view of Django is enough for
staff to manage the four tables.

## Feasibility

Every listed feature maps to a standard Django pattern: model forms,
class-based auth views, `login_required`, and `atomic()` for the checkout
transaction. No third-party package is necessary. The four-model schema is
small enough to build and test in one plan.

## Out of scope, confirmed

Payments, email, product images, search, and styling beyond readable CSS.
No pagination on the menu or history page in v1 (acceptable at small
product and transaction counts).

## Open items for the plan step

- Decide the exact template inheritance structure (a single `base.html`
  with a nav bar showing login state).

- Decide whether "remove from cart" is a link with a POST form or a plain
  GET link. POST is correct for a state-changing action. A GET link is
  easier to build but violates HTTP semantics. The plan should pick POST
  with a small form per row.

- Decide the CSS file location: `core/static/core/style.css`, following
  the static file app-namespacing convention of Django.
