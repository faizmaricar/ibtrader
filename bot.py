from app import App

class Bot:
    app = None
    
    def __init__(self):
        app = App()
        app.connect("127.0.0.1", 7497, clientId=0)
        app.run()

bot = Bot()