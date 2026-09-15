from django.urls import path
from django.views.generic import RedirectView

from core import views

app_name = "core"

urlpatterns = [
    path("", views.menu, name="menu"),
    path("menu/", RedirectView.as_view(pattern_name="core:menu"), name="menu-redirect"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("history/", views.history, name="history"),
]
