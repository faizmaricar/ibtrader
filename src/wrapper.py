from ibapi.wrapper import EWrapper
from ibapi.contract import ContractDetails

class Wrapper(EWrapper):
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)