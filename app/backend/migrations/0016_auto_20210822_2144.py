# Generated by Django 3.2.6 on 2021-08-22 16:44

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_merge_20210822_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=100, verbose_name='Nomi')),
                ('title_ru', models.CharField(max_length=100, verbose_name='Название')),
                ('title_en', models.CharField(max_length=100, verbose_name='Title')),
                ('description_uz', tinymce.models.HTMLField(verbose_name='haqida')),
                ('description_ru', tinymce.models.HTMLField(verbose_name='Описание')),
                ('description_en', tinymce.models.HTMLField(verbose_name='Description')),
            ],
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-updated']},
        ),
    ]
