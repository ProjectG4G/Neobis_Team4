from rest_framework import serializers
from .models import (
 Product,
 ProductCategory,
 Stock,
 Order,
 Cart,
 CartItem,
 Feedback,
)


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    size_name = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = ['size', 'size_name']


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # size = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    products = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self):
        pass


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_date']
        read_only_fields = ['id', 'created_date']


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'product', 'created_date', 'content']
