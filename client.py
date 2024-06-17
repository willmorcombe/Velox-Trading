import asyncio
import websockets
import json
import requests
from datetime import datetime, timezone
import schedule


def post_average_price(duration):
    data = {
        'duration' : duration,
    }
    response = requests.post('http://localhost:8000/api/average_price_set/', json=data)
    if response.status_code != 201:
        print(f'Error occoured while posting average price, status code: {response.status_code}')

def average_price_30():
    post_average_price(30)
def average_price_60():
    post_average_price(60)


async def binance_stream():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@depth20/ethusdt@depth20/bnbusdt@depth20"
    
    async with websockets.connect(url) as websocket:
        while True:
            schedule.run_pending()
            try:
                message = await websocket.recv()
                data = json.loads(message)
                data = {
                    'ticker' : data['stream'].split('@')[0],
                    'bids' : data['data']['bids'],
                    'asks' : data['data']['asks'],
                    'timestamp' : str(datetime.now(timezone.utc))
                    }

                response = requests.post('http://localhost:8000/api/order_book/', json=data)
                if response.status_code != 201:
                    print(f'Error occoured while posting order bookd data, status code: {response.status_code}')

            except websockets.ConnectionClosed:
                print("Connection closed")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

# schedule events to post averages
schedule.every(30).seconds.do(average_price_30)
schedule.every(60).seconds.do(average_price_60)

# Run the stream
asyncio.get_event_loop().run_until_complete(binance_stream())



