from decimal import Decimal

from django.db import migrations

SEED_PRODUCTS = [
    ("Americano", Decimal("110.00")),
    ("Cappuccino", Decimal("140.00")),
    ("Espresso", Decimal("100.00")),
]


def seed_products(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    for name, price in SEED_PRODUCTS:
        Product.objects.get_or_create(name=name, defaults={"price": price})


def remove_seed_products(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    Product.objects.filter(name__in=[name for name, _ in SEED_PRODUCTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_cartitem_cart_item_quantity_gt_zero"),
    ]

    operations = [
        migrations.RunPython(seed_products, remove_seed_products),
    ]
