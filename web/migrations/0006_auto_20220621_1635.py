# Generated by Django 3.2.10 on 2022-06-21 06:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20220620_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, upload_to='product/images/')),
            ],
            options={
                'verbose_name': 'Изображения товаров',
                'verbose_name_plural': 'Изображения товаров',
            },
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'Блог', 'verbose_name_plural': 'Блог'},
        ),
        migrations.AddField(
            model_name='product',
            name='Description',
            field=models.TextField(blank=True, verbose_name='Описание товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='Short_description',
            field=models.TextField(blank=True, verbose_name='Краткое описание карточки'),
        ),
        migrations.AddField(
            model_name='product',
            name='Video',
            field=models.FileField(null=True, upload_to='product/video/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='Видеообзор'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='Color',
            field=models.CharField(max_length=50, verbose_name='Цвет (html color code)  #'),
        ),
        migrations.AlterField(
            model_name='category',
            name='Color',
            field=models.CharField(max_length=50, verbose_name='Цвет (html color code)  #'),
        ),
    ]
