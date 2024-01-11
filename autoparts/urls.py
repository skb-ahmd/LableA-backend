from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .api import CartItemViewSet, CartViewSet, ProductViewSet,OrderViewSet

router=DefaultRouter()
router.register(prefix=r'products',viewset=ProductViewSet,basename='product')
router.register(r'carts', CartViewSet)
router.register(r'cartitems', CartItemViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns=[
    path('api/',include(router.urls))
]