from django.db import models

# Create your models here.

class OrderBook(models.Model):
    ticker = models.CharField(max_length=10)
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'timestamp']),
        ]

class Bids(models.Model):
    # Many to one relationship
    order_book = models.ForeignKey(OrderBook, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()

class Asks(models.Model):
    # Many to one relationship
    order_book = models.ForeignKey(OrderBook, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    
class AdditionalStats(models.Model):
    order_book = models.OneToOneField(
        OrderBook,
        on_delete=models.CASCADE,
        primary_key=True
    )
    bid_ask_spread = models.FloatField(default=None)
    price = models.FloatField(default=None)

class AveragePrice(models.Model):
    ticker = models.CharField(max_length=10)
    duration = models.IntegerField(default=None)
    price = models.FloatField(default=None)
    timestamp_upper = models.DateTimeField()
    timestamp_lower = models.DateTimeField()

