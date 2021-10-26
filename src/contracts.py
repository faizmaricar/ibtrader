from ibapi.contract import *

class Contracts:

    @staticmethod
    def Fx(symbol: str, currency: str):
        contract = Contract()
        contract.symbol = symbol
        contract.currency = currency
        contract.secType = 'CASH'
        contract.exchange = 'IDEALPRO'

        return contract
    
    @staticmethod
    def EurUsdFx():
        contract = Contracts.Fx('EUR', 'USD')
        return contract

    @staticmethod
    def GbpUsdFx():
        contract = Contracts.Fx('GBP', 'USD')
        return contract