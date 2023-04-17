from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    ProductCategory,
    ProductColor,
    Order,
    Cart,
    CartItem,
    Product,
    ProductFeedback,
    ProductImage,
)

from .serializers import (
    ProductCategoryParlerSerializer,
    ProductColorParlerSerializer,
    OrderSerializer,
    CartSerializer,
    CartItemSerializer,
    ProductParlerSerializer,
    ProductFeedbackSerializer,
    ProductImageSerializer,
)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductParlerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductParlerSerializer


class ProductCategoryParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryParlerSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class ProductColorParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductCategoryParlerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=["put"])
    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        cart.total_price = 0
        cart.save()
        CartItem.objects.filter(cart=cart).delete()
        return Response({"detail": "Cart cleared successfully."})


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
