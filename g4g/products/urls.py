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
)

router = DefaultRouter()
router.register(r"products", ProductParlerViewSet)
router.register(r"product-category", ProductCategoryParlerViewSet)
router.register(r"stock", StockViewSet)
router.register(r"order", OrderViewSet)
router.register(r"cart", CartViewSet)
router.register(r"cart-item", CartItemViewSet)
router.register(r"product-feedback", ProductFeedbackViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
