class Process:
    def payment_calculator(self, pax, cottage):
        entrance_fee = 100

        cottage_prices = {
            "Big Cottage": 500,
            "Small Cottage": 300,
            "Umbrella": 150,
            "None": 0
        }

        total = (pax * entrance_fee) + cottage_prices.get(cottage)
        return total
