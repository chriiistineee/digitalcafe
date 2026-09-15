# Run the app locally

1. Apply migrations: `python manage.py migrate`
2. Create a staff account: `python manage.py createsuperuser`
3. Start the dev server: `python manage.py runserver`
4. Open `http://127.0.0.1:8000/`

Step 1 also seeds three products through a data migration
(`core/migrations/0003_seed_products.py`): Americano (110.00),
Cappuccino (140.00), and Espresso (100.00). The menu shows these three
with no extra step. Add more through `/admin/`.

## Tests

No automated test suite ships in the repo. The v1 verification ran
through a temporary Django `TestCase`, then the file reverted to its
scaffold stub. See section 10 of
`doc/plan/1789454328_digital-cafe-v1.md` for the checklist and result.
