import threading
import time
import math
from datetime import datetime

from ibapi.common import ListOfPriceIncrements

from app import App
from contracts import Contracts
from orders import Orders

class IBApi(App):
    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)

        try:
            bot.onBarUpdate(reqId, time, open, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)
    def reqIds(self, numIds: int):
        return super().reqIds(numIds)

    def marketRule(self, marketRuleId: int, priceIncrements: ListOfPriceIncrements):
        super().marketRule(marketRuleId, priceIncrements)
        print("Market Rule ID: ", marketRuleId)
        
        for priceIncrement in priceIncrements:
            print("Price Increment.", priceIncrement)

class Bot:
    ib = None
    contract = None
    seven_am_one_hour_bar = []
    quantity = 70000

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, clientId=0) 
        
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()

        time.sleep(1)
        
        # Setup EUR/USD contract
        self.contract = Contracts.EurUsdFx()

        self.ib.reqRealTimeBars(0, self.contract, 5, 'MIDPOINT', 1, [])

    def run_loop(self):
        self.ib.run()
    
    def onBarUpdate(self, reqId, time, open, high, low, close, volume, wap, count):
        hour = datetime.fromtimestamp(time).utcnow().hour
        print(datetime.fromtimestamp(time).utcnow(), close)
        
        if hour == 7:
            self.seven_am_one_hour_bar.append(close)
        
        if hour == 8 and len(self.seven_am_one_hour_bar) > 0:
            high = round(max(self.seven_am_one_hour_bar), 5)
            low = round(min(self.seven_am_one_hour_bar), 5)
            profit = 0.004
            stop = 0.0005

            long_entry_bracket_order = Orders.BracketOrder(1, 'BUY', self.quantity, high, high + profit, high - stop, 'ENTRY')
            
            for long_order in long_entry_bracket_order:
                self.ib.placeOrder(long_order.orderId, self.contract, long_order)
            
            short_entry_bracket_order = Orders.BracketOrder(4, 'SELL', self.quantity, low, low - profit, low + stop, 'ENTRY')
            
            for short_order in short_entry_bracket_order:
                self.ib.placeOrder(short_order.orderId, self.contract, short_order)
        
            self.seven_am_one_hour_bar.clear()

bot = Bot()