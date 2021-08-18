# Generated by Django 3.2 on 2021-07-14 16:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20210714_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='address',
        ),
        migrations.AddField(
            model_name='botuser',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shopcard',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcard',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='shopcard',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='shop_card_ones', to='backend.botuser'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ShopCardOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('In queue', 'In Queue'), ('Canceled', 'Canceled'), ('Processed', 'Processed'), ('Completed', 'Completed')], default='In queue', max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('purchases', models.ManyToManyField(to='backend.ShopCardOne')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='backend.botuser')),
            ],
        ),
        migrations.AddField(
            model_name='shopcard',
            name='purchases',
            field=models.ManyToManyField(to='backend.ShopCardOne'),
        ),
    ]