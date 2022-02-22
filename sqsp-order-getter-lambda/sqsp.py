from squarespace import Squarespace


# get most recent 40 orders, reduces the lambda seconds. 
def get_orders(key):
    store = Squarespace(key)
    orders = store.orders()
    orders = orders + (store.next_page())
    return orders

def get_order(key, id):

    store = Squarespace(key)
    return store.order(id)

def all_orders(key):

    store = Squarespace(key)
    return store.all_orders()