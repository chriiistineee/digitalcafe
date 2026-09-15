from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from core.models import Product


def menu(request):
    products = Product.objects.all()
    return render(request, "core/menu.html", {"products": products})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:menu")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
