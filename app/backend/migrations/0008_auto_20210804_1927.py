# Generated by Django 3.2 on 2021-08-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_botuser_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Buyurtmalar', 'verbose_name_plural': 'Buyurtmalarlar'},
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Payme', 'Payme')], default='Cash', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='botuser',
            name='type',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('cook', 'Cook'), ('driver', 'Driver')], default='user', max_length=10),
        ),
    ]