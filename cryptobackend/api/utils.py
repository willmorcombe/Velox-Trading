# util functions
import numpy as np

def update_structure_bids_asks(order_book, x):
    return [{'order_book': order_book.id, 'price' : float(price), 'quantity' : float(quantity)} for price, quantity in x]
    
def calculate_vwap(orders):
    prices = np.array([order[0] for order in orders])
    quantities = np.array([order[1] for order in orders])
    vwap = np.sum(prices * quantities) / np.sum(quantities)
    return vwap