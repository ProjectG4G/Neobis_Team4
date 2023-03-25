from django.urls import path
from .views import (ProductList, ProductDetail, ProductCategoryList,
                    ProductCategoryDetail, StockList, StockDetail, OrderList,
                    OrderDetail, CartList, CartDetail, CartItemList,
                    CartItemDetail, FeedbackList, clear_cart)

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product-categories/', ProductCategoryList.as_view(), name='product-category-list'),
    path('product-categories/<int:pk>/', ProductCategoryDetail.as_view(), name='product-category-detail'),
    path('stocks/', StockList.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', StockDetail.as_view(), name='stock-detail'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('carts/', CartList.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
    path('cart-items/', CartItemList.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemDetail.as_view(), name='cart-item-detail'),
    path('feedback/', FeedbackList.as_view(), name='feedback-list'),
    path('carts/<int:pk>/clear/', clear_cart, name='clear-cart'),
]
