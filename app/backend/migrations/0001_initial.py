# Generated by Django 3.2.6 on 2021-08-18 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('cook', 'Cook'), ('driver', 'Driver')], default='user', max_length=10)),
                ('chat_id', models.IntegerField(unique=True)),
                ('full_name', models.CharField(max_length=255, verbose_name="To'liq ismi")),
                ('contact', models.CharField(max_length=50)),
                ('balance', models.IntegerField(default=0)),
                ('lang', models.CharField(choices=[('uz', 'Uz'), ('ru', 'Ru'), ('en', 'En')], default='uz', max_length=10)),
                ('bot_state', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('referal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referals', to='backend.botuser')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=100, verbose_name='Nomi')),
                ('name_ru', models.CharField(max_length=100, verbose_name='Название')),
                ('name_en', models.CharField(max_length=100, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='backend.category', verbose_name='Ota kategoriya')),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Kategoriyalar',
            },
            managers=[
                ('categories', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=100, verbose_name='Nomi')),
                ('title_ru', models.CharField(max_length=100, verbose_name='Название')),
                ('title_en', models.CharField(max_length=100, verbose_name='Title')),
                ('description_uz', models.TextField(verbose_name='Mahsulot haqida')),
                ('description_ru', models.TextField(verbose_name='Описание')),
                ('description_en', models.TextField(verbose_name='Description')),
                ('price', models.IntegerField(verbose_name='Narxi')),
                ('image', models.ImageField(default='backend/images/default.png', upload_to='backend/images/', verbose_name='Rasm')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='backend.category', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Mahsulot',
                'verbose_name_plural': 'Mahsulotlar',
            },
            managers=[
                ('products', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.product')),
            ],
            managers=[
                ('purchases', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TaskManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Other', 'Other')], max_length=30)),
                ('info', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date'],
            },
            managers=[
                ('tasks', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Key', 'Key'), ('Message', 'Message'), ('Smile', 'Smile')], max_length=10)),
                ('body_uz', models.TextField()),
                ('body_ru', models.TextField()),
                ('body_en', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('templates', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ShopCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('purchases', models.ManyToManyField(to='backend.Purchase')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop_card', to='backend.botuser')),
            ],
            managers=[
                ('shop_cards', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Reserved', 'Reserved'), ('In queue', 'In Queue'), ('Processed', 'Processed'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Reserved', max_length=25)),
                ('delivery_type', models.CharField(choices=[('Self call', 'Self Call'), ('Payment delivery', 'Payment Delivery')], max_length=20)),
                ('payment_type', models.CharField(choices=[('Cash', 'Cash'), ('Payme', 'Payme')], max_length=20)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('purchases', models.ManyToManyField(to='backend.Purchase')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='backend.botuser')),
            ],
            options={
                'verbose_name': 'Buyurtmalar',
                'verbose_name_plural': 'Buyurtmalarlar',
            },
            managers=[
                ('orders', django.db.models.manager.Manager()),
            ],
        ),
    ]
