# Routes

## Project level

Defined in `digitalcafe/urls.py`.

| Path | Name | View |
|---|---|---|
| `/register/` | `register` | `core.views.register` |
| `/login/` | `login` | the built-in `LoginView` of Django |
| `/logout/` | `logout` | the built-in `LogoutView` of Django, POST only |

| Path | Name | View |
|---|---|---|
| `/admin/` | (Django default) | the Django admin site |
| `/` | (none) | includes `core.urls` |

## App level

Defined in `core/urls.py`, under the `core` namespace.

### Browsing

| Path | Name | Method | Auth |
|---|---|---|---|
| `/` | `core:menu` | GET | No |
| `/menu/` | `core:menu-redirect` | GET | No |

### Cart and checkout

| Path | Name | Method | Auth |
|---|---|---|---|
| `/cart/` | `core:cart` | GET | Yes |
| `/cart/add/<product_id>/` | `core:add_to_cart` | POST | Yes |
| `/cart/remove/<item_id>/` | `core:remove_from_cart` | POST | Yes |
| `/checkout/` | `core:checkout` | POST | Yes |

### History

| Path | Name | Method | Auth |
|---|---|---|---|
| `/history/` | `core:history` | GET | Yes |

## Notes

- `/menu/` redirects to `core:menu`.
- `core:add_to_cart` increases the quantity of an existing cart row on
  a repeat add, then sets a flash message, for example "Added 1 of
  Americano to your cart."
- `core:menu` greets a logged-in user by username, for example "Hi,
  christine123!". The greeting does not show when logged out.
- `core:remove_from_cart` and `core:history` filter by `request.user`.
- `core:checkout` rejects an empty cart, then writes inside one atomic
  block.
- `digitalcafe/settings.py` sets `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and
  `LOGOUT_REDIRECT_URL`. A page that needs login sends an anonymous
  visitor to `/login/`, then back to itself after login.
