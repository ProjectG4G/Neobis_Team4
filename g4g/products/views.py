from rest_framework import viewsets
from django.shortcuts import redirect
from .models import (
    ProductCategory,
    Stock,
    Order,
    Cart,
    CartItem,
    Product,
    ProductFeedback,
)
from .serializers import (
    ProductCategoryParlerSerializer,
    StockSerializer,
    OrderSerializer,
    CartSerializer,
    CartItemSerializer,
    ProductParlerSerializer,
    ProductFeedbackSerializer,
)


class ProductParlerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductParlerSerializer


class ProductCategoryParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryParlerSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=["put"])
    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        CartItem.objects.filter(cart=cart).delete()
        return Response({"detail": "Cart cleared successfully."})


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
