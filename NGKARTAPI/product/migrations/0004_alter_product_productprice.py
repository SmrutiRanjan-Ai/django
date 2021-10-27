# Generated by Django 3.2.8 on 2021-10-19 11:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_tax_taxslug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ProductPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
