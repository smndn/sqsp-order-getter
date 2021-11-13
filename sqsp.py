from squarespace import Squarespace


#returns list of all orders
def get_orders(key):
    store = Squarespace(key)
    orders = store.orders()
    return orders

def get_order(key, id):

    store = Squarespace(key)
    return store.order(id)

def all_orders(key):

    store = Squarespace(key)
    return store.all_orders()