# Generated by Django 4.1.5 on 2023-03-20 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_date',
            new_name='order_datetime',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Общая сумма'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_in_cart', to='products.product', verbose_name='Товар'),
        ),
    ]
