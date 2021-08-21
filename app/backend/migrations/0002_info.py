# Generated by Django 3.2.6 on 2021-08-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='backend/images/default.png', upload_to='backend/images/', verbose_name='Rasm')),
            ],
            options={
                'verbose_name': 'Malumot',
                'verbose_name_plural': 'Malumotlar',
            },
        ),
    ]