from ibapi.order import *

class Orders:

    @staticmethod
    def BracketOrder(parentOrderId:int, action:str, quantity:float, 
                     limitPrice:float, takeProfitLimitPrice:float, 
                     stopLossPrice:float, parentOcaGroup: str):

        brackerOrderAction = "SELL" if action == "BUY" else "BUY"

        parent = Orders.LimitIfTouchedOrder(action, quantity, limitPrice)
        parent.orderId = parentOrderId
        parent.ocaType = 1
        parent.ocaGroup = parentOcaGroup
        parent.transmit = False

        takeProfit = Orders.LimitIfTouchedOrder(brackerOrderAction, quantity, takeProfitLimitPrice)
        takeProfit.orderId = parent.orderId + 1
        takeProfit.parentId = parentOrderId
        takeProfit.transmit = False

        stopLoss = Orders.TrailingStop(brackerOrderAction, quantity, 0.1, stopLossPrice)
        stopLoss.orderId = parent.orderId + 2
        stopLoss.parentId = parentOrderId
        stopLoss.transmit = True

        bracketOrder = [parent, takeProfit, stopLoss]
        
        return bracketOrder

    @staticmethod
    def LimitOrder(action:str, quantity:float, limitPrice:float):
    
        order = Order()
        order.action = action
        order.orderType = "LMT"
        order.totalQuantity = quantity
        order.lmtPrice = limitPrice

        return order
    
    def LimitIfTouchedOrder(action:str, quantity:float, limitPrice:float):
        triggerPrice = limitPrice - 0.00001 if action == 'BUY' else limitPrice + 0.00001
        order = Orders.LimitOrder(action, quantity, limitPrice)
        order.orderType = "LIT"
        order.auxPrice = triggerPrice

        return order

    @staticmethod
    def TrailingStop(action:str, quantity:float, trailingPercent:float,
                     trailStopPrice:float):
    
        order = Order()
        order.action = action
        order.orderType = "TRAIL"
        order.totalQuantity = quantity
        order.trailingPercent = trailingPercent
        order.trailStopPrice = trailStopPrice

        return order

    @staticmethod
    def TrailingStopLimit(action:str, quantity:float, lmtPriceOffset:float, 
                          trailingAmount:float, trailStopPrice:float):
    
        order = Order()
        order.action = action
        order.orderType = "TRAIL LIMIT"
        order.totalQuantity = quantity
        order.trailStopPrice = trailStopPrice
        order.lmtPriceOffset = lmtPriceOffset
        order.auxPrice = trailingAmount

        return order