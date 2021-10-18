from ibapi.contract import *

class Contracts:

    @staticmethod
    def EurUsdFx():
        contract = Contract()
        contract.symbol = 'EUR'
        contract.secType = 'CASH'
        contract.currency = 'USD'
        contract.exchange = 'IDEALPRO'

        return contract