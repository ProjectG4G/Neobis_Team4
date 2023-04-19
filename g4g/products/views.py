from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .permissions import IsOwnerOrReadOnly, IsOwner, IsSupplierOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    permission_classes = [IsSupplierOrReadOnly]


@extend_schema(tags=["Products"])
class ProductParlerViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductParlerSerializer
    permission_classes = [IsSupplierOrReadOnly]


@extend_schema(tags=["Product Category"])
class ProductCategoryParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryParlerSerializer
    permission_classes = [IsSupplierOrReadOnly]


@extend_schema(tags=["Product Colors"])
class ProductColorParlerViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorParlerSerializer
    permission_classes = [IsSupplierOrReadOnly]


@extend_schema(tags=["Orders"])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(tags=["Carts"])
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]


@extend_schema(tags=["Product Feedback"])
class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
