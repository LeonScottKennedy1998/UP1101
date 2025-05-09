from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TagViewSet, ProductViewSet,
    OrderViewSet, OrderItemViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
