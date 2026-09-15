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

Version 1 is complete and merged to `master`. It covers registration,
login, logout, the menu, the cart, checkout, and transaction history.

Out of scope for v1: payments, email, product images, search, and
styling beyond a readable stylesheet.

## Where things live

- `digitalcafe/`: project settings and the top-level `urls.py`
- `core/`: the one app. Models, views, admin, templates, and static files
- `doc/study/`: feasibility and tradeoff notes, one file per feature
- `doc/plan/`: task boards, one file per feature
- `doc/wiki/`: this directory, the current state of the codebase
