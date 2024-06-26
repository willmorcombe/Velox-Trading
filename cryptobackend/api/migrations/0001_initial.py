# Generated by Django 5.0.6 on 2024-06-15 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('bids', models.JSONField()),
                ('asks', models.JSONField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalStats',
            fields=[
                ('order_book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.orderbook')),
                ('bid_ask_spread', models.FloatField(default=None)),
                ('price', models.FloatField(default=None)),
            ],
        ),
        migrations.AddIndex(
            model_name='orderbook',
            index=models.Index(fields=['ticker', 'timestamp'], name='api_orderbo_ticker_99ef76_idx'),
        ),
    ]
