# Generated by Django 3.2.8 on 2021-10-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_shippingaddress_shippingname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='ShippingName',
            field=models.CharField(blank=True, default=None, max_length=200),
        ),
    ]