from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('delete_product_physical', 'Может физически удалять товар'),
            ("restore_product", "Can restore deleted product"),
        ]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь', null=True)
    number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    full_name = models.CharField(max_length=100, verbose_name='ФИО клиента')

    def __str__(self):
        return f"Заказ {self.number}"

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity - item.discount
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Скидка за единицу товара')

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (заказ {self.order.number})"