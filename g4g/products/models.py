from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager


User = get_user_model()


class ProductCategory(TranslatableModel):
    objects = TranslatableManager()

    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_("Имя категории"),
            max_length=255,
            blank=True,
            unique=True,
        ),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(TranslatableModel):
    objects = TranslatableManager()

    translations = TranslatedFields(
        name=models.CharField(
            max_length=255,
            verbose_name=_("Имя товара"),
        ),
        description=models.TextField(
            blank=True,
            verbose_name=_("Описание товара"),
        ),
    )

    color = models.ForeignKey(
        to="products.ProductColor",
        verbose_name=_("Расцветки товара"),
        on_delete=models.CASCADE,
        null=True,
        related_name="productcolor",
    )

    price = models.DecimalField(
        verbose_name=_("Цена товара"),
        decimal_places=2,
        max_digits=12,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Дата создания"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Дата изменения"),
        auto_now=True,
    )

    active = models.BooleanField(
        verbose_name=_("Данный товар активен"),
        default=True,
    )

    discount = models.DecimalField(
        verbose_name=_("Скидка"),
        max_digits=5,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        ProductCategory,
        related_name="product",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        null=True,
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_("Количество"),
        default=1,
    )

    size = models.SmallIntegerField(
        verbose_name=_("Размер"),
        choices=(
            (0, "NO"),
            (1, "S"),
            (2, "M"),
            (3, "L"),
            (4, "XL"),
        ),
        default=0,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Дата редактирования"),
        auto_now=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Дата создания"),
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductColor(TranslatableModel):
    objects = TranslatableManager()

    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_("Расцветки товара"),
            max_length=255,
            blank=True,
            unique=True,
        ),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Расцветки товара"
        verbose_name_plural = "Расцветки товара"


class ProductImage(models.Model):
    objects = models.Manager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/product/")

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"


class Cart(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Дата создания"),
        auto_now_add=True,
    )
    total_price = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return f"Cart {self.pk} "

    def add_price(self, price):
        self.total_price += price
        self.save()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Order(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Пользователь"),
    )

    order_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата заказа"),
    )
    total_price = models.FloatField(
        blank=True,
        null=True,
        default=0,
    )

    STATUS_CHOICES = (
        ("P", "Pending"),
        ("C", "Confirmed"),
        ("S", "Sent"),
        ("D", "Delivered"),
        ("X", "Canceled"),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="P",
        verbose_name=_("Статус"),
    )

    def __str__(self):
        return f"{self.user} ({self.get_status_display()})"

    def add_price(self, price):
        self.total_price += price
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class CartItem(models.Model):
    objects = models.Manager()

    cart = models.ForeignKey(
        "products.Cart",
        verbose_name=_("Корзина"),
        on_delete=models.CASCADE,
        null=True,
        related_name="items",
    )
    order = models.ForeignKey(
        "products.Order",
        verbose_name=_("Заказ"),
        on_delete=models.CASCADE,
        related_name="items",
        blank=True,
        null=True,
    )

    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("Товар"),
        on_delete=models.CASCADE,
        related_name="product_in_cart",
        null=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Количество"),
        default=1,
    )

    def __str__(self):
        return f"{self.product} ({self.quantity})"

    class Meta:
        verbose_name = "Детали корзины"
        verbose_name_plural = "Детали корзины"

    @staticmethod
    def get_total_price(price, quantity, discount):
        if discount is None:
            discount = 0
        price = float(price)
        price = price - price * (discount / 100)
        return round(price * quantity)

    def save(self, *args, **kwargs):
        quantity = self.quantity
        if self.pk:  # check if the instance already exists in the database
            old_instance = CartItem.objects.get(pk=self.pk)
            if self.quantity != old_instance.quantity:
                quantity -= old_instance.quantity

        total_price = self.get_total_price(
            self.product.price, quantity, self.product.discount
        )

        self.product.quantity -= quantity
        self.product.save()

        if self.cart is not None:
            self.cart.add_price(total_price)
        if self.order is not None:
            self.order.add_price(total_price)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        total_price = self.get_total_price(
            self.product.price, self.quantity, self.product.discount
        )

        if self.cart:
            self.cart.add_price(-total_price)
        elif self.order:
            self.order.add_price(-total_price)

        super().delete(*args, **kwargs)


class ProductFeedback(models.Model):
    objects = models.Manager()

    content = models.TextField(
        verbose_name=_("Текст"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("Дата создания"),
        auto_now_add=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Товар"),
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Пользователь"),
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
