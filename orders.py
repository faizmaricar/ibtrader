from ibapi.order import *

class Orders:

    @staticmethod
    def BracketOrder(parentOrderId:int, action:str, quantity:float, 
                     limitPrice:float, takeProfitLimitPrice:float, 
                     stopLossPrice:float, lmtPriceOffset: float, parentOcaGroup: str):
    
        parent = Order()
        parent.orderId = parentOrderId
        parent.action = action
        parent.orderType = "LMT"
        parent.totalQuantity = quantity
        parent.lmtPrice = limitPrice
        parent.ocaType = 1
        parent.ocaGroup = parentOcaGroup
        parent.transmit = False

        takeProfit = Order()
        takeProfit.orderId = parent.orderId + 1
        takeProfit.action = "SELL" if action == "BUY" else "BUY"
        takeProfit.orderType = "LMT"
        takeProfit.totalQuantity = quantity
        takeProfit.lmtPrice = takeProfitLimitPrice
        takeProfit.parentId = parentOrderId
        takeProfit.transmit = False

        stopLoss = Order()
        stopLoss.orderId = parent.orderId + 2
        stopLoss.action = "SELL" if action == "BUY" else "BUY"
        stopLoss.orderType = "TRAIL LIMIT"
        stopLoss.auxPrice = stopLossPrice
        stopLoss.lmtPriceOffset = lmtPriceOffset
        stopLoss.totalQuantity = quantity
        stopLoss.parentId = parentOrderId
        stopLoss.transmit = True

        bracketOrder = [parent, takeProfit, stopLoss]
        return bracketOrder