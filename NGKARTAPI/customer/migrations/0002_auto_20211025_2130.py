# Generated by Django 3.2.8 on 2021-10-25 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='ShippingName',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='ShippingAddressLine1',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
