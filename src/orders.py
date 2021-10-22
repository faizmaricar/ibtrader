from ibapi.order import *

class Orders:
    @staticmethod
    def Pip(n: float):
        return n * 0.0001
    
    @staticmethod
    def Order(action:str, quantity:float):
        order = Order()
        order.action = action
        order.totalQuantity = quantity

        return order

    @staticmethod
    def BracketOrder(parentOrderId:int, action:str, quantity:float, 
                     limitPrice:float, takeProfitLimitPrice:float, 
                     stopLossPrice:float, parentOcaGroup: str):

        brackerOrderAction = "SELL" if action == "BUY" else "BUY"

        parent = Orders.MarketIfTouched(action, quantity, limitPrice)
        parent.orderId = parentOrderId
        parent.ocaType = 1
        parent.ocaGroup = parentOcaGroup
        parent.transmit = False

        takeProfit = Orders.LimitOrder(brackerOrderAction, quantity, takeProfitLimitPrice)
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
        order = Orders.Order(action, quantity)
        order.orderType = "LMT"
        order.lmtPrice = limitPrice

        return order
    
    def LimitIfTouchedOrder(action:str, quantity:float, limitPrice:float):
        triggerGap = Orders.Pip(1)
        triggerPrice = limitPrice + triggerGap if action == 'BUY' else limitPrice - triggerGap
        order = Orders.LimitOrder(action, quantity, limitPrice)
        order.orderType = "LIT"
        order.auxPrice = triggerPrice

        return order
    @staticmethod
    def MarketIfTouched(action:str, quantity: float, price: float):
        order = Orders.Order(action, quantity)
        order.orderType = "MIT"
        order.auxPrice = price

        return order

    @staticmethod
    def TrailingStop(action:str, quantity:float, trailingPercent:float,
                     trailStopPrice:float):
    
        order = Orders.Order(action, quantity)
        order.orderType = "TRAIL"
        order.trailingPercent = trailingPercent
        order.trailStopPrice = trailStopPrice

        return order

    @staticmethod
    def TrailingStopLimit(action:str, quantity:float, lmtPriceOffset:float, 
                          trailingAmount:float, trailStopPrice:float):
    
        order = Orders.Order(action, quantity)
        order.orderType = "TRAIL LIMIT"
        order.trailStopPrice = trailStopPrice
        order.lmtPriceOffset = lmtPriceOffset
        order.auxPrice = trailingAmount

        return order