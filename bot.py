import threading
import time
from datetime import datetime

from ibapi.common import BarData, ListOfPriceIncrements

from app import App
from contracts import Contracts
from orders import Orders

class IBApi(App):
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        super().historicalDataUpdate(reqId, bar)
        try:
            bot.onHistoricalUpdate(reqId, bar)
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
    high = None
    low = None
    quantity = 70000

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, clientId=0) 
        
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()

        time.sleep(1)
        
        # Setup EUR/USD contract
        self.contract = Contracts.EurUsdFx()

        self.ib.reqHistoricalData(4102, self.contract, '', "1 D", "1 hour", "MIDPOINT", 1, 1, True, [])

    def run_loop(self):
        self.ib.run()
    
    def onHistoricalUpdate(self, reqId, bar):
        print(bar)

        hour = datetime.strptime(bar.date, '%Y%m%d %H:%M:%S').utcnow().hour
        trade = True

        if hour == 7:
            self.high = round(bar.high, 6)
            self.low = round(bar.low, 6)
        
        if hour == 8 and trade:
            profit = 0.004
            stop = 0.0001

            long_TP_price = self.high + profit
            long_SL_price = self.high - stop

            short_TP_price = self.low - profit
            short_SL_price = self.low + stop

            long_entry_bracket_order = Orders.BracketOrder(1, 'BUY', self.quantity, self.high, long_TP_price, long_SL_price, 'ENTRY')
            
            for long_order in long_entry_bracket_order:
                self.ib.placeOrder(long_order.orderId, self.contract, long_order)
            
            short_entry_bracket_order = Orders.BracketOrder(4, 'SELL', self.quantity, self.low, short_TP_price, short_SL_price, 'ENTRY')
            
            for short_order in short_entry_bracket_order:
                self.ib.placeOrder(short_order.orderId, self.contract, short_order)
            
            trade = False

bot = Bot()