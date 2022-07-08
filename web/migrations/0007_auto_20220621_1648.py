# Generated by Django 3.2.10 on 2022-06-21 06:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20220621_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Images',
            field=models.ManyToManyField(blank=True, to='web.ProductImage', verbose_name='Изображения товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Video',
            field=models.FileField(blank=True, null=True, upload_to='product/video/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='Видеообзор'),
        ),
    ]
