from rest_framework import serializers
from .models import (
    Product,
    ProductCategory,
    Stock,
    Order,
    Cart,
    CartItem,
    ProductFeedback,
    ProductImage,
)
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductCategoryParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductCategory)

    class Meta:
        model = ProductCategory
        fields = ("id", "name", "translations")


# class ProductCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ["id", "name"]


class ProductParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = ProductCategoryParlerSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = [
            "translations",
        ]


#
# class ProductSerializer(serializers.ModelSerializer):
#     category = ProductCategorySerializer()
#
#     class Meta:
#         model = Product
#         fields = "__all__"
#


class SizeSerializer(serializers.ModelSerializer):
    size_name = serializers.CharField(source="get_size_display")

    class Meta:
        model = Stock
        fields = ["size", "size_name"]


class StockSerializer(serializers.ModelSerializer):
    product = ProductParlerSerializer()
    # size = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductParlerSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "total_price"]

    def get_total_price(self, obj):
        price = obj.product.price - obj.product.price * (obj.product.discount / 100)
        return round(price * obj.quantity)

    get_total_price.short_description = "Общая сумма"

    def get_price(self, obj):
        return round(obj.product.price)

    price.short_description = "Цена"


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_price(self, obj):
        price = obj.product.price - obj.product.price * (obj.product.discount / 100)
        return round(price * obj.quantity)

    get_total_price.short_description = "Общая сумма"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "created_date"]
        read_only_fields = ["id", "created_date"]


class ProductFeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    product = ProductParlerSerializer(read_only=True)

    class Meta:
        model = ProductFeedback
        fields = ["id", "user", "product", "created_date", "content"]
