# Plan: seed the database with three products

Timestamp: 1789463672
Study: doc/study/1789463565_seed-products.md

Design decision carried over from the study: a data migration, not a
fixture, since `migrate` is already the documented first setup step
in `doc/wiki/running.md`.

Nothing here needs input from you. Every value below is something this
session can create on its own.

## Task board

### 1. Add the seed migration

- [x] Write `core/migrations/0003_seed_products.py`, depending on
      `core.0002_cartitem_cart_item_quantity_gt_zero`
- [x] Forward: `get_or_create` on `name` for Americano (110.00),
      Cappuccino (140.00), Espresso (100.00), so a repeat `migrate`
      creates no duplicate
- [x] Reverse: delete the three products by name
- [x] Run `migrate`, then confirm all three rows exist

### 2. Manual verification, before rendezvous

- [x] Confirm `migrate` creates all three products on a database that
      has none of them
- [x] Run `migrate` a second time. Confirm no duplicate row appears
- [x] Confirm `migrate` back to `core.0002` removes all three, then
      `migrate` forward again restores them
- [x] Confirm the menu page lists all three with the right prices

Verified with a temporary Django `TransactionTestCase` run through
`manage.py test`, against an isolated test database. All four checks
passed. The test file was not committed.

A `TransactionTestCase` flushes table data between tests but leaves
the `django_migrations` record alone, so a plain `migrate()` in
`setUp` saw 0003 as already applied and reran nothing. `setUp` had to
step back to `core.0002`, then forward, before each test, to force
the seed to run against the freshly flushed table.
