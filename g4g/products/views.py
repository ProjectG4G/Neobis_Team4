# def clear_cart(request, pk):
#     cart = Cart.objects.get(id=pk)
#     cart.products.clear()
#     cart.total_price = 0
#     cart.save()
#     return redirect("swagger-ui")

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

    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        cart.products.clear()
        cart.total_price = 0
        cart.save()
        return redirect("swagger-ui")


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
