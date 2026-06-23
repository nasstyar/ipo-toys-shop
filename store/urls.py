from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from . import views

# Создаём роутер
router = DefaultRouter()

# Регистрируем ViewSets
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='manufacturer')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')

# URL-паттерны
urlpatterns = [
    # API маршруты
    path('api/', include(router.urls)),
    
    # API аутентификация
    path('api/auth/login/', obtain_auth_token, name='api_login'),
    path('api/auth/logout/', auth_views.LogoutView.as_view(), name='api_logout'),
    
    # Обычные маршруты (HTML страницы)
    path('', views.product_list, name='catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
