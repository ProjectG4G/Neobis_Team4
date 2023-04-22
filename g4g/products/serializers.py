from rest_framework import serializers
from .models import (
    Product,
    ProductCategory,
    ProductColor,
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


class ProductColorParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductColor)

    class Meta:
        model = ProductColor
        fields = (
            "id",
            "url",
            "translations",
        )


class ProductParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Product)
    images = ProductImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        allow_empty=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "url",
            "translations",
            "color",
            "size",
            "category",
            "images",
            "uploaded_images",
            "price",
            "quantity",
            "active",
            "discount",
            "created_at",
            "updated_at",
        )

        write_only_fields = ("category", "color")

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
        model = Product
        fields = ["size", "size_name"]


class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductParlerSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "url",
            "cart",
            "order",
            "product",
            "quantity",
        )

        read_only_fields = (
            "cart",
            "order",
        )

        depth = 1

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")

        if not product.active:
            raise serializers.ValidationError(
                {"detail": "This product is unavailable!"}
            )

        if self.instance:
            product.quantity += self.instance.quantity
            product.save()
            self.instance.quantity = 0
            self.instance.save()

        if product.quantity < quantity:
            raise serializers.ValidationError(
                {"detail": "You can't order more products than we have in stock."}
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["cart"] = Cart.objects.get(user=user)

        product = validated_data["product"]
        quantity = validated_data["quantity"]

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
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "url",
            "user",
            "order_datetime",
            "status",
            "total_price",
            "items",
            "address",
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
        # validated_data["total_price"] = int(cart.total_price)
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
        fields = ["id", "user", "product", "created_at", "content"]
