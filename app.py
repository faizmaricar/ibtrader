from ibapi.common import OrderId
from ibapi.contract import Contract
from ibapi.order import Order
from wrapper import Wrapper
from client import Client

class App(Wrapper, Client):
    def __init__(self):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

    def placeOrder(self, orderId: OrderId, contract: Contract, order: Order):
        print('{} {} {} at {}'.format(order.action, order.totalQuantity, contract.symbol, order.lmtPrice))
        return super().placeOrder(orderId, contract, order)