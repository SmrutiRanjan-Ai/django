# Generated by Django 3.2.8 on 2021-10-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20211025_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='ShippingName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]