# Generated by Django 3.2.8 on 2021-10-25 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_shippingaddress_shippingname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='ShippingName',
        ),
    ]