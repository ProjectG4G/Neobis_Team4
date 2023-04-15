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
        fields = (
            "id",
            "url",
            "image",
            "product",
        )


class ProductCategoryParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductCategory)

    class Meta:
        model = ProductCategory
        fields = ("id", "name", "translations")


class ProductParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = ProductCategoryParlerSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = [
            "translations",
        ]



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
        fields = (
            "id",
            "url",
            "size",
            "quantity",
            "last_updated",
            "updated_at",
            "product",
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductParlerSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    size = serializers.ChoiceField(
        write_only=True,
        choices=(
            (1, "S"),
            (2, "M"),
            (3, "L"),
            (4, "XL"),
        ),
    )

    class Meta:
        model = CartItem
        fields = (
            "id",
            "url",
            "cart",
            "product",
            "quantity",
            "size",
        )

        read_only_fields = ("cart",)

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]
        size = attrs["size"]

        stock = Stock.objects.filter(product=product, size=size).first()

        if stock is not None and stock.quantity < quantity:
            raise serializers.ValidationError(
                "You can't order more products than we have in stock."
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["cart"] = user.cart

        product = validated_data["product"]
        size = validated_data["size"]
        quantity = validated_data["quantity"]

        stock = Stock.objects.get(product=product, size=size)

        stock.quantity -= quantity
        stock.save()
        validated_data.pop("size")

        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "url",
            "user",
            "created_at",
            "total_price",
            "items",
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "url",
            "user",
            "cart",
            "order_datetime",
            "status",
            "total_price",
        )
        read_only_fields = (
            "user",
            "total_price",
            "order_datetime",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        cart = validated_data["cart"]

        items = CartItem.objects.filter(cart=cart)

        order = Order.objects.create(**validated_data)

        for item in items:
            item.order = order
            item.cart = None
            item.save()

        cart.total_price = 0
        cart.save()

        return order


class ProductFeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    product = ProductParlerSerializer(read_only=True)

    class Meta:
        model = ProductFeedback
        fields = ["id", "user", "product", "created_date", "content"]
