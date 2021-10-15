import threading
import time

from ibapi.contract import Contract

from app import App

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

    def __init__(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, clientId=0) 
        
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()

        time.sleep(1)

        symbol = input('Enter symbol you want to trade: ')

        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        self.ib.reqRealTimeBars(0, contract, 5, 'TRADES', 1, [])

    def run_loop(self):
        self.ib.run()

    def onBarUpdate(self, reqId, time, open, high, low, close, volume, wap, count):
        print(close)

bot = Bot()