# Technical test Velox

A technical challenge sent by Velox

## Instructions

A market data feed is used to drive various business functions. Given the following url:

wss://stream.binance.com:9443/stream?streams=btcusdt@depth20/ethusdt@depth20/bnbusdt@depth20

write python code that will obtain and store the following information:

1. Raw orderbook
2. Bid, ask spread
3. Price (volume weighted average of orderbook)
4. Average price (30s and 1 minute)

where Price is defined as follows:
price = (bidVwap + askVwap) / 2
bidVwap = volume weighted average price of bids
askVwap = volume weighted average price of asks

The solution should be able to be extended and be scalable to process more symbols and higher volumes of data.

Example code to connect to the websocket:

```
from websocket import WebSocketApp

def on_message(ws, message):
    print(message)

url ='wss://stream.binance.com:9443/stream?streams=btcusdt@depth20/ethusdt@depth20/bnbusdt@depth20'
ws = WebSocketApp(url, on_message = on_message)
ws.run_forever()
```

## How to tackle

The task is left purposefully open to interpretation. The main goal of this I would assume is to persist all data collected from the market feed, save it for later evaluations and use in models. In this case I would save it to some form of database schema. This means that we need some database design that will be expandable and allow for large quantities of data.

I think the end goal is to expose some API's so we can directly pull data from the database when needed. and have a client script running that posts data to the API, this way we can customize what we push to our server and get back speicific results

## Tech Stack

- Python 3.12
- Django 5.0.06
- MySQL 8.0

(see requirements.txt for more info)

## Implementation

I've tried to reduce the number of operations on the client side to make the server handle more of the heavy lifting / calculations. So the client script should ideally just post the order_book to the server. I've tried to keep the database models simple and keep to database normalization standards where possible. I've used MySql here just because of the scale of this mini project. As stated below I would ideally use a database suited towards tims seris analysis. However with some indexing on specific tables to help some lookup operations its still possible to get good results.

## Improvements for future 

Ideally if I had more time these are the features that I would implement.

- Firstly an important goal would be efficieny with requests and pushing / pulling data. Ideally I would not use an sql database for this. Something like InfluxDB. 

- Produce some endpoints for retriving data back from the database. 

- Ideally depending on the number of tickers / volume, multithreading would be used to push more data to the server.

- Intead of running a scheduler on the client script, I would instead like to use cron on the django server itself to execute average price calculations rather than calling it from the client script. The reason being is that I can't run cron without either developing on docker (which would take more time) or using a unix machine. 

- I would use something smaller and more lightweight than django if I had more time, I would ideally use Fast-API just as a more leightweight efficient solution.
