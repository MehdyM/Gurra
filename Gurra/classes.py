class Coin:
    def __init__(self, symbol, current_price):
        self.symbol = symbol
        self.current_price = current_price
        self.purchase_price = 0 
        self.qty = 0 
        self.step_size = 0
        self.min_qty = 0
        self.new_price = 0 
        self.precision = 0
        self.static_win_price = 1000000
        self.sell_price = 0 #self.new_price * 0.97
        self.stop_loss = 0 #self.purchase_price * 0.97