class Process:
    def __init__(self):
        self.cottage_prices = {
            "A": 500,
            "B": 300,
            "C": 150,
            "D": 0
        }

    def payment_calculator(self, pax, cottage):
        cottage_price = self.cottage_prices.get(cottage.upper(), 0)  # default to 0
        return pax * 50 + cottage_price  # per-person fee + cottage price
