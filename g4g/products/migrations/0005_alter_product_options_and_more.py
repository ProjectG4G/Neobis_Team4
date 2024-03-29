# Generated by Django 4.1.7 on 2023-04-21 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_order_address"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={},
        ),
        migrations.AlterModelOptions(
            name="producttranslation",
            options={
                "default_permissions": (),
                "managed": True,
                "verbose_name": "product Translation",
            },
        ),
        migrations.AlterField(
            model_name="product",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="products.productcategory",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="productcolor",
                to="products.productcolor",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=5, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name="product",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="product",
            name="size",
            field=models.SmallIntegerField(
                choices=[(0, "NO"), (1, "S"), (2, "M"), (3, "L"), (4, "XL")], default=0
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="producttranslation",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="producttranslation",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
