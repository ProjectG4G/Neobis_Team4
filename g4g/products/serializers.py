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
        fields = (
            "id",
            "url",
            "translations",
        )


class ProductParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    category = ProductCategoryParlerSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        allow_empty=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = (
            "url",
            "translations",
            "images",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(image=image, product=product)

        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        for image in uploaded_images:
            ProductImage.objects.create(image=image, product=instance)

        return super().update(instance, validated_data)


class SizeSerializer(serializers.ModelSerializer):
    size_name = serializers.CharField(source="get_size_display")

    class Meta:
        model = Stock
        fields = ["size", "size_name"]


class StockSerializer(serializers.ModelSerializer):
    # product = ProductParlerSerializer(read_only=True)

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
    # product = ProductParlerSerializer(read_only=True)

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
            "order",
            "product",
            "quantity",
            "size",
        )

        read_only_fields = ("cart",)

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        size = attrs.get("size")

        stock = Stock.objects.filter(product=product, size=size).first()

        if stock is not None and stock.quantity < quantity:
            raise serializers.ValidationError(
                "You can't order more products than we have in stock."
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["cart"] = Cart.objects.get(user=user)

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

        cart = Cart.objects.get(user=user)

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
