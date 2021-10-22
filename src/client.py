from ibapi.client import EClient

class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)