from wrapper import Wrapper
from client import Client

class App(Wrapper, Client):
    def __init__(self):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)