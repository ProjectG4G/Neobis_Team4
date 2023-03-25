

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name=_('Имя категории'),
        max_length=255,
        blank=True,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(
        max_length=125,
        verbose_name=_('Имя товара')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание товара')
    )

    price = models.DecimalField(
        verbose_name=_('Цена товара'),
        decimal_places=2,
        max_digits=12
    )
    pictures = models.ImageField(
        upload_to='images/',
        verbose_name=_('Фото товара'),
        default=list
    )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True
    )
    active = models.BooleanField(
        verbose_name=_('Данный товар активен'),
        default=True
    )
    color = models.CharField(
        max_length=50,
        verbose_name=_('Расцветки товара')
    )
    discount = models.DecimalField(
        verbose_name=_('Скидка'),
        max_digits=5,
        decimal_places=2,
        default=0
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name='product',
        verbose_name=_('Категория'),
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Stock(models.Model):
    size = models.SmallIntegerField(
        verbose_name=_('Размер'),
        choices=(
            (1, 'S'),
            (2, 'M'),
            (3, 'L'),
            (4, 'XL'),
        ))
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество'),
        default=1
    )
    last_updated = models.DateTimeField(
        verbose_name=_('Последнее обновление'),
        auto_now=True
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата нового поступления'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('Продукт'),
        related_name='stocks'
    )

    def __str__(self):
        return f'{self.product}{self.get_size_display()}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'
        ordering = ('product', 'last_updated')


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        Product,
        through='CartItem'
    )

    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )

    def __str__(self):
        return f"Cart {self.id} {self.user}"

    def calculate_total_price(self):
        items = self.cartitem_set.all()
        return sum(item.total_price for item in items)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name=_('Корзина'),
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Товар'),
        on_delete=models.CASCADE,
        related_name='product_in_cart'
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество'),
        default=1
    )
    price = models.DecimalField(
        verbose_name=_('Цена'),
        max_digits=9,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.product} ({self.quantity})"

    @property
    def total_price(self):
        return round(self.product.price * (1 - self.product.discount / 100) * self.quantity)

    class Meta:
        verbose_name = 'Детали корзины'
        verbose_name_plural = 'Детали корзины'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Пользователь'),
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name=_('Корзина'),
        on_delete=models.CASCADE,
        null=True
    )
    order_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата заказа'),
    )
    STATUS_CHOICES = (
        ('P', 'В ожидании'),
        ('C', 'Подтвержден'),
        ('S', 'Отправлен'),
        ('D', 'Доставлен'),
        ('X', 'Отменен'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
        verbose_name=_('Статус'),
    )

    def __str__(self):
        return f'{self.user} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Comment(models.Model):
    content = models.TextField(
        verbose_name=_('Текст'),
        )
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Товар'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Пользователь'),
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


