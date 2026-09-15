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

- [ ] Write `core/migrations/0003_seed_products.py`, depending on
      `core.0002_cartitem_cart_item_quantity_gt_zero`
- [ ] Forward: `get_or_create` on `name` for Americano (110.00),
      Cappuccino (140.00), Espresso (100.00), so a repeat `migrate`
      creates no duplicate
- [ ] Reverse: delete the three products by name
- [ ] Run `migrate`, then confirm all three rows exist

### 2. Manual verification, before rendezvous

- [ ] Confirm `migrate` creates all three products on a database that
      has none of them
- [ ] Run `migrate` a second time. Confirm no duplicate row appears
- [ ] Confirm `migrate` back to `core.0002` removes all three, then
      `migrate` forward again restores them
- [ ] Confirm the menu page lists all three with the right prices
