from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OrderBookSerializer, BidsSerializer, AsksSerializer, AdditionalStatsSerializer, AveragePriceSerializer
from .utils import update_structure_bids_asks, calculate_vwap
from .models import Bids, Asks, OrderBook
from datetime import datetime, timedelta, timezone

# Create your views here.

@api_view(['POST'])
def order_book_with_addons(request):
    # only one allowed
    if request.method == 'POST':
        serializer_order_book = OrderBookSerializer(data=request.data)
        serializer_order_book.is_valid(raise_exception=True)
        order_book_obj = serializer_order_book.save()

        # get bids
        bids = request.data.get('bids', None)
        if bids == None:
            return Response(status = 400, data = "no bids specified")
        
        bids = update_structure_bids_asks(order_book_obj, bids)
        for bid_data in bids:
            serializer_bids = BidsSerializer(data=bid_data)
            serializer_bids.is_valid(raise_exception=True)
            serializer_bids.save()
        
        # get asks
        asks = request.data.get('asks', None)
        if asks == None:
            return Response(status = 400, data = "no asks specified")
        
        asks = update_structure_bids_asks(order_book_obj, asks)
        for ask_data in asks:
            serializer_asks = AsksSerializer(data=ask_data)
            serializer_asks.is_valid(raise_exception=True)
            serializer_asks.save()

        # create addons

        bids =  Bids.objects.filter(order_book = order_book_obj)
        asks = Asks.objects.filter(order_book = order_book_obj)
        bid_ask_spread = asks.order_by('price').first().price - bids.order_by('price').last().price

        bid_vwap = calculate_vwap( [[x['price'], x['quantity']] for x in bids.values()] )
        ask_vwap = calculate_vwap([[x['price'], x['quantity']] for x in asks.values()] )

        price = (bid_vwap + ask_vwap) / 2
        
        # save to database through serialization
        data = {'order_book' : order_book_obj.id, 'price' : price, 'bid_ask_spread' : bid_ask_spread}
        add_stats_serializer = AdditionalStatsSerializer(data = data)
        add_stats_serializer.is_valid(raise_exception=True)
        add_stats_serializer.save()

        return Response(status=201)

@api_view(['POST'])
def average_price_set(request):
    if request.method == 'POST':
        avg_price_serializer = AveragePriceSerializer(data=request.data)
        avg_price_serializer.is_valid(raise_exception=True)
        avg_price_serializer.save()
        return Response(status=201)


    
    
    
