from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductCategory, Stock, Order, Cart, CartItem, Reply


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
        if obj.cart:
            items = obj.cart.cartitem_set.all()
            return ", ".join([f"{item.product.name} x {item.quantity}" for item in items])
        else:
            return "-"

    cart_details.short_description = _("Корзина")

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="C")
        self.message_user(request, _("Выбранные заказы отмечены как подтвержденные."))

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="S")
        self.message_user(request, _("Выбранные заказы отмечены как отправленные."))

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="D")
        self.message_user(request, _("Выбранные заказы отмечены как доставленные."))

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="X")
        self.message_user(request, _("Выбранные заказы отмечены как отмененные."))

    mark_as_confirmed.short_description = _("Отметить выбранное как подтвержденное")
    mark_as_shipped.short_description = _("Отметить выбранное как отправленное")
    mark_as_delivered.short_description = _("Отметить выбранное как доставленное")
    mark_as_cancelled.short_description = _("Отметить выбранное как отмененное")

    def get_total_price(self, obj):
        items = obj.cart.cartitem_set.all()
        return sum(item.total_price for item in items)

    get_total_price.short_description = "Общая сумма"


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "get_products", "created_date", "get_total_price")

    def get_products(self, obj):
        return "\n".join([p.name for p in obj.products.all()])

    get_products.short_description = "Товары"

    def get_total_price(self, obj):
        items = obj.cartitem_set.all()
        return sum(item.total_price for item in items)

    get_total_price.short_description = "Общая сумма"


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Stock)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Reply)
