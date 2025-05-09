from rest_framework import viewsets
from firstproject.models import Category, Tag, Product, Order, OrderItem
from django.contrib.auth.models import User
from .serializers import (
    CategorySerializer, TagSerializer, ProductSerializer,
    OrderSerializer, OrderItemSerializer, UserSerializer
)
from rest_framework.permissions import DjangoModelPermissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [DjangoModelPermissions]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [DjangoModelPermissions]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [DjangoModelPermissions]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]
