# Generated by Django 3.2.6 on 2021-08-21 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20210821_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.info'),
            preserve_default=False,
        ),
    ]