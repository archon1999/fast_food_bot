# Generated by Django 4.0.4 on 2022-08-25 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_adminpanel'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='full_register',
            field=models.BooleanField(default=False),
        ),
    ]
