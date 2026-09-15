from django.contrib import admin

from core.models import CartItem, LineItem, Product, Transaction

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Transaction)
admin.site.register(LineItem)
