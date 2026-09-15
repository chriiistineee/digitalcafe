# Study: remove the Add to cart button from the menu

Timestamp: 1789464109

## Goal

Remove the "Add to cart" button and its column from the menu table.
Adding a product to the cart happens only from the product detail
page, which already has its own "Add to cart" form with a quantity
field.

## Correction: there is no menu.py

`core/` has no `menu.py`. The menu view is the `menu` function in
`core/views.py`, and it only queries `Product.objects.all()` and
renders `core/menu.html` with that list. It carries no cart logic of
its own. The rest of this study reads "menu.py" as this function.

## Current state, read from the codebase

`core/templates/core/menu.html` has a three-column table: "Product
Name", "Price (PHP)", and a third column with no header text. Each
row's third cell holds, only when `user.is_authenticated`, a form:

```
<form class="inline" method="post" action="{% url 'core:add_to_cart' product.id %}">
    {% csrf_token %}
    <input type="hidden" name="next" value="menu">
    <button type="submit">Add to cart</button>
</form>
```

The empty-state row, shown when there are no products, has
`colspan="3"`, matching the current three columns.

`core/views.py` `add_to_cart` already branches on the `next` field:
`"detail"` sends the visitor back to `core:product_detail`, and any
other value, including a missing field, sends them to `core:menu`.
The product detail page already posts to this same view with
`next=detail` and its own `quantity` input.

## What menu.html needs

- Remove the third `<th>`, the one with no header text.
- Remove the third `<td>` in each row: the whole
  `{% if user.is_authenticated %}` block and the form inside it.
- Change the empty-state row from `colspan="3"` to `colspan="2"`, to
  match the two remaining columns.

No other line in `menu.html` needs a change. The greeting,
"Hi, {{ user.username }}!", stays. It sits above the table and does
not depend on the third column.

## What core/views.py needs

Nothing, for the `menu` view. It never referenced `add_to_cart` or the
cart at all. It only ever fetched products and rendered the template.

## Does add_to_cart need a change

No. The request asks to confirm this, and the code supports the
answer: `add_to_cart` takes a `product_id` from the URL and a
`quantity` and `next` from `POST`. The product detail page already
sends `next=detail` and a real quantity through this same view, on a
route this change does not touch. Removing the menu's form removes
one of the two callers of `add_to_cart`, not the view itself.

One note, not a required change: once the menu's form is gone,
nothing in the app sends `next=menu` or omits `next` anymore. The
`else` branch in `add_to_cart` that falls back to `core:menu` becomes
unreached through the UI. It stays correct as a default for any
future caller, or a handcrafted request, so removing it is not
necessary and not requested. The plan step should leave it as is.

## Wiki impact for the sync docs step

`doc/wiki/routes.md` documents the menu's add-to-cart form and its
`next=menu` example under "Notes". Once the form is gone, that
example no longer matches a real button on the page, even though the
underlying view behavior is unchanged. The `sync docs` step for this
feature should update that note to describe the detail page as the
only add-to-cart entry point.

## Tradeoffs and open items for the plan step

- No model change, no migration, no view change. This is a
  template-only removal.
- The only remaining way to add a product to the cart is the detail
  page. A user on the menu must click a product name first. This
  matches the request as given.
- No change to `core/static/core/style.css`. Its table rules are not
  column-count specific.
