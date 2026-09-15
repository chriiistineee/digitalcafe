# Study: seed the database with three products

Timestamp: 1789463565

## Goal

Anyone who clones the repo gets a working menu right away: Americano
110, Cappuccino 140, Espresso 100.

## Fixture versus data migration

**A fixture** (`core/fixtures/products.json`, loaded with `python
manage.py loaddata products`) is not loaded by `migrate`. Nothing in
the standard Django setup path runs `loaddata` on its own. A person
who clones the repo, follows `doc/wiki/running.md`, and runs `migrate`
still lands on an empty menu. Getting the seed products would need an
extra, easy-to-forget command that the current setup steps do not
mention.

**A data migration** (`core/migrations/0003_seed_products.py`, a
`RunPython` operation) runs as part of `python manage.py migrate`,
which is already step 1 in `doc/wiki/running.md`. A person who clones
the repo and runs that one command gets the three products, with no
new step to remember or document.

`doc/wiki/running.md` also has this line, right after the numbered
setup steps: "Add a product through `/admin/` first. The menu page has
no rows to show until a product exists." A migration removes the need
for this line. The `sync docs` step for this feature should delete it.

## Recommendation

A data migration. The request is "immediately," on a plain clone plus
the standard setup. Only a migration satisfies that without adding a
new step.

## How the migration should work

- A single `RunPython` operation, forward function only.
- The forward function uses `get_or_create` keyed on `name`, so
  running `migrate` twice, or running it against a database that
  already has one of these three products by name, does not create a
  duplicate row.
- A reverse function deletes the three products by name. Django
  migrations should stay reversible where practical, and a delete by
  name costs nothing to write.
- The migration declares a dependency on the latest existing `core`
  migration, `core.0002_cartitem_cart_item_quantity_gt_zero`, so it
  runs after the schema exists.
- The three rows: Americano at 110.00, Cappuccino at 140.00, Espresso
  at 100.00, matching the prices given in the request. All three are
  already in `christine`'s local `db.sqlite3` from earlier manual
  testing, gitignored and never committed, so this migration is what
  turns that local, ad hoc state into something every clone gets.

## Tradeoffs and open items for the plan step

- A migration bakes specific product rows into migration history,
  which is unusual for environment-specific or sensitive data. These
  three rows are neither: a small, fixed, public product catalog for
  a coffee shop demo app, so this is a reasonable use of a data
  migration, not a shortcut around a real production seeding process.
- `core.tests.py` is the scaffold stub today, per
  `doc/plan/1789461818_menu-greeting-and-add-to-cart-message.md` and
  `doc/plan/1789462739_product-detail-page.md`, both of which reverted
  their temporary verification `TestCase` after running it. The same
  pattern applies here: verify with a temporary test against an
  isolated test database, then revert, matching every prior feature
  in this repo.
- No settings change, no new dependency, no template change.
