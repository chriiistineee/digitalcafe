from django.urls import path
from django.views.generic import RedirectView

from core import views

app_name = "core"

urlpatterns = [
    path("", views.menu, name="menu"),
    path("menu/", RedirectView.as_view(pattern_name="core:menu"), name="menu-redirect"),
]
