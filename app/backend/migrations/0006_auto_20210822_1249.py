# Generated by Django 3.2 on 2021-08-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20210821_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='image',
            field=models.ImageField(upload_to='backend/images/', verbose_name='Rasm'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
