# Generated by Django 3.2.8 on 2021-10-25 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_meta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('FileId', models.AutoField(primary_key=True, serialize=False)),
                ('FileData', models.FileField(upload_to='')),
                ('FileUrl', models.URLField(unique=True)),
            ],
            options={
                'verbose_name': 'FileUpload',
                'verbose_name_plural': 'FileUpload',
            },
        ),
    ]
