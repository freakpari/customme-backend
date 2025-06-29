# Generated by Django 4.2.23 on 2025-06-28 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_product_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_orders', models.PositiveIntegerField(default=0, verbose_name='سفارش جاری')),
                ('delivered_orders', models.PositiveIntegerField(default=0, verbose_name='ارسال شده')),
                ('gallery_products', models.PositiveIntegerField(default=0, verbose_name='محصول در گالری')),
                ('physical_products', models.PositiveIntegerField(default=0, verbose_name='محصول فیزیکی')),
                ('canceled_orders', models.PositiveIntegerField(default=0, verbose_name='سفارش لغو شده')),
                ('comments', models.PositiveIntegerField(default=0, verbose_name='تعداد نظر')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
