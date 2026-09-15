from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.models import CartItem, LineItem, Product, Transaction


def menu(request):
    products = Product.objects.all()
    return render(request, "core/menu.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "core/product_detail.html", {"product": product})


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 0
    if quantity < 1:
        messages.error(request, "Quantity must be a positive integer.")
        return redirect("core:product_detail", pk=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product, defaults={"quantity": quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    messages.success(request, f"Added {quantity} of {product.name} to your cart.")
    return redirect("core:menu")


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.subtotal for item in cart_items)
    return render(request, "core/cart.html", {"cart_items": cart_items, "total": total})


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    cart_item.delete()
    return redirect("core:cart")


@login_required
@require_POST
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    if not cart_items:
        messages.error(request, "The cart is empty. Add a product before you check out.")
        return redirect("core:cart")

    with db_transaction.atomic():
        order = Transaction.objects.create(user=request.user)
        for item in cart_items:
            LineItem.objects.create(
                transaction=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        cart_items.delete()

    messages.success(request, "Checkout complete.")
    return redirect("core:history")


@login_required
def history(request):
    transactions = (
        Transaction.objects.filter(user=request.user)
        .order_by("-timestamp")
        .prefetch_related("line_items")
    )
    return render(request, "core/history.html", {"transactions": transactions})


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
