# Run the app locally

1. Apply migrations: `python manage.py migrate`
2. Create a staff account: `python manage.py createsuperuser`
3. Start the dev server: `python manage.py runserver`
4. Open `http://127.0.0.1:8000/`

Add a product through `/admin/` first. The menu page has no rows to
show until a product exists.

## Tests

No automated test suite ships in the repo. The v1 verification ran
through a temporary Django `TestCase`, then the file reverted to its
scaffold stub. See section 10 of
`doc/plan/1789454328_digital-cafe-v1.md` for the checklist and result.
