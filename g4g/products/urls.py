from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductParlerViewSet,
    ProductCategoryParlerViewSet,
    StockViewSet,
    OrderViewSet,
    CartViewSet,
    CartItemViewSet,
    ProductFeedbackViewSet,
    ProductImageViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductParlerViewSet, basename="product")
router.register(
    r"product-categories", ProductCategoryParlerViewSet, basename="productcategory"
)
router.register(r"product-images", ProductImageViewSet, basename="productimage")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cartitem")
router.register(r"feedbacks", ProductFeedbackViewSet, basename="productfeedback")

urlpatterns = [
    path("", include(router.urls)),
]
