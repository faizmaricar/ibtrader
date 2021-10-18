import threading
import time
from datetime import datetime

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

class Bot:
    ib = None
    contract = None
    seven_am_one_hour_bar = []
    quantity = 75000

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
            high = max(self.seven_am_one_hour_bar)
            low = min(self.seven_am_one_hour_bar)

            long_entry_bracket_order = Orders.BracketOrder(1, 'BUY', self.quantity, high, high + 0.004, high - 0.0003, high - 0.00001, 'ENTRY')
            short_entry_bracket_order = Orders.BracketOrder(4, 'SELL', self.quantity, low, low - 0.004, low + 0.0003, low + 0.00001, 'ENTRY')
            
            for order in long_entry_bracket_order:
                self.ib.placeOrder(order.orderId, self.contract, order)
            
            for order in short_entry_bracket_order:
                self.ib.placeOrder(order.orderId, self.contract, order)

bot = Bot()