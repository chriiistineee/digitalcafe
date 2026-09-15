# Overview

Digital Cafe is a multi-page web app for a coffee shop. A customer
registers, logs in, browses the menu, adds items to a cart, and checks
out. Checkout creates a transaction with line items. The customer views
own transaction history. Staff manage all data through the Django admin.

## Stack

- Django 5.2, Python
- SQLite
- Django templates, plain CSS, no JavaScript framework
- The built-in auth and admin of Django
- Project `digitalcafe`, single app `core`

## Status

Version 1 is complete and merged to `main`. It covers registration,
login, logout, the menu, the cart, checkout, and transaction history.

The menu page greets a logged-in user by username, and links each
product name to a detail page. The detail page holds the only
add-to-cart form, with a quantity field. A successful add shows a
flash message on the menu, for example "Added 2 of Americano to your
cart," and a rejected quantity keeps the visitor on the detail page.

A data migration seeds three products, so a fresh clone shows a
working menu right after `migrate`. See `doc/wiki/running.md`.

Out of scope for v1: payments, email, product images, search, and
styling beyond a readable stylesheet.

## Where things live

- `digitalcafe/`: project settings and the top-level `urls.py`
- `core/`: the one app. Models, views, admin, templates, and static files
- `doc/study/`: feasibility and tradeoff notes, one file per feature
- `doc/plan/`: task boards, one file per feature
- `doc/wiki/`: this directory, the current state of the codebase
