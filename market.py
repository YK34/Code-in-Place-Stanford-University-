"""
File: market.py
Description: The core economic engine for the Fantasy Trader game.
Handles prices, portfolio tracking, and financial validation.
"""
import random

STARTING_CASH = 1000.0
TOTAL_DAYS = 10

ASSET_INFO = {
    "Bitcoin": {"price": 100.0, "min_change": -0.15, "max_change": 0.25, "color": "orange"},
    "Ethereum": {"price": 50.0, "min_change": -0.20, "max_change": 0.30, "color": "purple"},
    "Apple": {"price": 20.0, "min_change": -0.05, "max_change": 0.10, "color": "gray"}
}

class MarketEngine:
    def __init__(self):
        self.cash = STARTING_CASH
        self.day = 1
        self.portfolio = {"Bitcoin": 0, "Ethereum": 0, "Apple": 0}
        self.current_prices = {asset: ASSET_INFO[asset]["price"] for asset in ASSET_INFO}
        self.message = "Welcome! Press B/E/A to buy, S to sell, SPACE for Next Day."
        self.msg_color = "black"

    def buy_asset(self, asset):
        price = self.current_prices[asset]
        if self.cash >= price:
            self.cash -= price
            self.portfolio[asset] += 1
            self.message = f"Successfully bought 1 unit of {asset}!"
            self.msg_color = "darkgreen"
        else:
            self.message = f"Insufficient funds to buy {asset}!"
            self.msg_color = "red"

    def sell_asset(self, asset):
        if self.portfolio[asset] > 0:
            self.cash += self.current_prices[asset]
            self.portfolio[asset] -= 1
            self.message = f"Successfully sold 1 unit of {asset}!"
            self.msg_color = "blue"
        else:
            self.message = f"You don't own any {asset} to sell!"
            self.msg_color = "red"

    def next_day(self):
        if self.day < TOTAL_DAYS:
            self.day += 1
            for asset in self.current_prices:
                change = random.uniform(ASSET_INFO[asset]["min_change"], ASSET_INFO[asset]["max_change"])
                self.current_prices[asset] *= (1 + change)
                if self.current_prices[asset] < 0.1:
                    self.current_prices[asset] = 0.1
            self.message = "A new day begins! Markets have shifted."
            self.msg_color = "black"
        else:
            self.message = "Game Over! Check your final Net Worth."
            self.msg_color = "darkblue"

    def get_net_worth(self):
        net = self.cash
        for asset, amount in self.portfolio.items():
            net += amount * self.current_prices[asset]
        return net
