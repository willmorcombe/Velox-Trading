from rest_framework import serializers 
  
# import model from models.py 
from .models import OrderBook, Bids, Asks, AdditionalStats, AveragePrice
from datetime import datetime, timedelta, timezone
  
# Create a model serializer  
class OrderBookSerializer(serializers.ModelSerializer): 
    # specify model and fields 
    class Meta: 
        model = OrderBook 
        fields = ('ticker', 'timestamp') 

class BidsSerializer(serializers.ModelSerializer): 
    # specify model and fields 
    class Meta: 
        model = Bids 
        fields = ('order_book', 'price', 'quantity') 

class AsksSerializer(serializers.ModelSerializer): 
    # specify model and fields 
    class Meta: 
        model = Asks 
        fields = ('order_book', 'price', 'quantity') 

class AdditionalStatsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AdditionalStats
        fields = ('order_book', 'price', 'bid_ask_spread')

class AveragePriceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AveragePrice
        fields = ('duration',)

    def save(self):
        # loop through each ticker
        for ticker in OrderBook.objects.all().values_list('ticker', flat=True).distinct():

            date_time = datetime.now(timezone.utc) - timedelta(seconds = self.validated_data['duration'])
            # get price from date_time and greater
            prices = AdditionalStats.objects.filter(order_book__timestamp__gte=date_time, order_book__ticker=ticker).values_list('price', flat=True)
            avg = sum(prices) / len(prices)
            print(avg)
            print(prices)
            AveragePrice(
                ticker = ticker,
                price = avg,
                duration = self.validated_data['duration'],
                timestamp_upper = datetime.now(timezone.utc),
                timestamp_lower = date_time,
            ).save()
            


