from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

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


@extend_schema(tags=["Product Images"])
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=["Products"])
class ProductParlerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductParlerSerializer


@extend_schema(tags=["Product Category"])
class ProductCategoryParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryParlerSerializer


@extend_schema(tags=["Product Colors"])
class ProductColorParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorParlerSerializer


@extend_schema(tags=["Orders"])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@extend_schema(tags=["Carts"])
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


@extend_schema(tags=["Cart Items"])
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


@extend_schema(tags=["Product Feedback"])
class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
