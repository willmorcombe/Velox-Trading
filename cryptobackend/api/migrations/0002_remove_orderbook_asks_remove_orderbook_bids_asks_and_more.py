# Generated by Django 5.0.6 on 2024-06-15 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderbook',
            name='asks',
        ),
        migrations.RemoveField(
            model_name='orderbook',
            name='bids',
        ),
        migrations.CreateModel(
            name='Asks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('order_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderbook')),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('order_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderbook')),
            ],
        ),
    ]
