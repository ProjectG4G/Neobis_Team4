from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from parler.admin import TranslatableAdmin

from .models import (
    Product,
    ProductCategory,
    ProductColor,
    Order,
    Cart,
    CartItem,
    ProductFeedback,
)


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
        "price1",
        "total_price",
    )

    @admin.display(empty_value=0)
    def total_price(self, obj):
        price = obj.product.price - obj.product.price * (obj.product.discount / 100)
        return round(price * obj.quantity)

    total_price.short_description = "Общая сумма"

    @admin.display(empty_value=0)
    def price1(self, obj):
        return round(obj.product.price)

    price1.short_description = "Цена"


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "cart_details",
        "order_datetime",
        "status",
        "get_total_price",
    ]
    list_filter = ["status"]
    actions = [
        "mark_as_confirmed",
        "mark_as_shipped",
        "mark_as_delivered",
        "mark_as_cancelled",
    ]

    def cart_details(self, obj):
        cart = getattr(obj, "cart", None)
        if cart:
            items = cart.cartitem_set.all()
            return ", ".join([f"{item.product.name} x {item.quantity}" for item in items])
        else:
            return "-"

    cart_details.short_description = _("Корзина")

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="C")
        self.message_user(request, _("Selected orders are marked as confirmed."))

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="S")
        self.message_user(request, _("Selected orders are marked as shipped."))

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="D")
        self.message_user(request, _("Selected orders are marked as delivered."))

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="X")
        self.message_user(request, _("Selected orders are marked as canceled."))

    mark_as_confirmed.short_description = _("Mark selection as confirmed")
    mark_as_shipped.short_description = _("Mark selected as sent")
    mark_as_delivered.short_description = _("Mark selected as delivered")
    mark_as_cancelled.short_description = _("Mark selected as canceled")

    @admin.display(empty_value=0)
    def get_total_price(self, obj):
        return obj.cart.total_price

    get_total_price.short_description = "Общая сумма"


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "get_products", "get_total_price")

    @admin.display(empty_value=0)
    def get_products(self, obj):
        items = CartItem.objects.filter(cart=obj)
        return "\n".join([p.product.name for p in items.all()])

    get_products.short_description = "Товары"

    @admin.display(empty_value=0)
    def get_total_price(self, obj):
        return obj.total_price

    get_total_price.short_description = "Общая сумма"


admin.site.register(Product, TranslatableAdmin)
admin.site.register(ProductCategory, TranslatableAdmin)
admin.site.register(ProductColor, TranslatableAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ProductFeedback)
