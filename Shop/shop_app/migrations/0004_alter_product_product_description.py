# Generated by Django 4.0.2 on 2022-03-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0003_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.CharField(max_length=500, verbose_name='Product Description'),
        ),
    ]
