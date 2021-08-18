# Generated by Django 3.2 on 2021-07-16 10:19

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20210714_2132'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopCardOne',
            new_name='Purchase',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Mahsulot', 'verbose_name_plural': 'Mahsulotlar'},
        ),
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('categories', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('orders', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('products', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='purchase',
            managers=[
                ('purchases', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='shopcard',
            managers=[
                ('shop_cards', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='backend.category', verbose_name='Kategoriya'),
        ),
        migrations.AlterField(
            model_name='shopcard',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_card', to='backend.botuser'),
        ),
    ]
