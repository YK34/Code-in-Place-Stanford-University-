"""
File: main.py
Project: Fantasy Trader Simulator (Competitive & Fixed Logic Edition)
Course: Stanford Code in Place 2026
Description: A hybrid graphical and console trading simulator.
Bankruptcy logic is now correctly based on Total Net Worth instead of just Cash.
"""
from graphics import Canvas
import random

# Game Configuration Constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 500
STARTING_CASH = 1000.0
CLASSIC_TOTAL_DAYS = 10

ASSET_INFO = {
    "Bitcoin": {"price": 100.0, "min_change": -0.15, "max_change": 0.25},
    "Ethereum": {"price": 50.0, "min_change": -0.20, "max_change": 0.30},
    "Apple": {"price": 20.0, "min_change": -0.05, "max_change": 0.10}
}

class FantasyTraderGame:
    def __init__(self):
        # Initialize Financial Engine States
        self.cash = STARTING_CASH
        self.day = 1
        self.portfolio = {"Bitcoin": 0, "Ethereum": 0, "Apple": 0}
        self.current_prices = {asset: ASSET_INFO[asset]["price"] for asset in ASSET_INFO}
        self.message = "Welcome! Select your Game Mode in the console."
        self.game_mode = None  # 1 for Classic, 2 for Endless
        self.is_bankrupt = False
        
        # Setup Built-in Code in Place Canvas
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Draw initial title screen state and launch mode selector
        self.draw_dashboard()
        self.select_game_mode()
        
        # Refresh screen and start main loop
        self.draw_dashboard()
        self.run_console_loop()

    def select_game_mode(self):
        """Prompts the user to choose between the two competitive modes."""
        print("=" * 50)
        print("CHOOSE YOUR GAME MODE:")
        print("[1] Classic Mode (10-Day High Score Challenge)")
        print("[2] Endless Mode (Survival - Game over if Total Net Worth <= 0)")
        print("=" * 50)
        
        while True:
            choice = input("Enter Mode (1-2): ").strip()
            if choice == '1':
                self.game_mode = 1
                self.message = "Classic Mode Started! Maximize your Net Worth in 10 Days."
                break
            elif choice == '2':
                self.game_mode = 2
                self.message = "Endless Mode Started! Survival Warning: Don't let Net Worth reach $0."
                break
            print("Invalid mode! Please enter 1 or 2.")

    def get_max_buy(self, asset):
        price = self.current_prices[asset]
        return int(self.cash // price)

    def buy_asset(self, asset, amount):
        if amount <= 0:
            self.message = "Amount must be greater than zero! Canceled."
            return
            
        price = self.current_prices[asset]
        cost = amount * price
        
        if self.cash >= cost:
            self.cash -= cost
            self.portfolio[asset] += amount
            self.message = f"Successfully bought {amount} units of {asset}!"
        else:
            self.message = f"Insufficient funds! Needs ${cost:.2f} but you have ${self.cash:.2f}."

    def sell_asset(self, asset, amount):
        if amount <= 0:
            self.message = "Amount must be greater than zero! Canceled."
            return
            
        owned_amount = self.portfolio[asset]
        if amount > owned_amount:
            self.message = f"Error! You cannot sell more than you own ({owned_amount} units)."
            return
            
        price = self.current_prices[asset]
        earnings = amount * price
        
        self.cash += earnings
        self.portfolio[asset] -= amount
        self.message = f"Successfully sold {amount} units of {asset}!"

    def get_net_worth(self):
        net = self.cash
        for asset, amount in self.portfolio.items():
            net += amount * self.current_prices[asset]
        return net

    def next_day(self):
        # 1. Update Market Prices
        for asset in self.current_prices:
            change = random.uniform(ASSET_INFO[asset]["min_change"], ASSET_INFO[asset]["max_change"])
            self.current_prices[asset] *= (1 + change)
            if self.current_prices[asset] < 0.1:
                self.current_prices[asset] = 0.1
        
        # 2. Advance Day Counter
        self.day += 1
        self.message = "A new day begins! Markets have shifted."
        
        # 3. Endless Mode Corrected Bankruptcy Check (Based on Total Net Worth)
        if self.game_mode == 2 and self.get_net_worth() <= 0:
            self.is_bankrupt = True
            self.message = "BANKRUPTCY! Your Total Net Worth fell to $0 or below."

    def draw_dashboard(self):
        self.canvas.clear()
        
        # Upper Header Banner
        self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, 60, color="#1a365d")
        self.canvas.create_text(20, 40, text="FANTASY TRADER: COMPETITIVE", font="Arial", font_size=18, color="white")
        
        # Game Mode Info String
        mode_str = "Mode: Loading..."
        if self.game_mode == 1: mode_str = "MODE: 10-DAY CHALLENGE"
        elif self.game_mode == 2: mode_str = "MODE: ENDLESS SURVIVAL"
        self.canvas.create_text(400, 40, text=mode_str, font="Arial", font_size=11, color="#cbd5e0")

        # Win/Loss validation states
        is_game_over = False
        if self.game_mode == 1 and self.day > CLASSIC_TOTAL_DAYS:
            is_game_over = True
        elif self.game_mode == 2 and self.is_bankrupt:
            is_game_over = True

        day_text = f"DAY: {self.day} / {CLASSIC_TOTAL_DAYS}" if self.game_mode == 1 else f"DAY: {self.day} (Endless)"
        if is_game_over:
            day_text = "GAME OVER"
            
        self.canvas.create_text(20, 95, text=day_text, font="Arial", font_size=14, color="black")
        self.canvas.create_text(20, 120, text=f"Liquid Cash: ${self.cash:.2f}", font="Arial", font_size=12, color="black")
        self.canvas.create_text(20, 145, text=f"Total Net Worth: ${self.get_net_worth():.2f}", font="Arial", font_size=13, color="darkblue")
        
        # Asset Cards Render Cycle
        y_offset = 170
        assets = ["Bitcoin", "Ethereum", "Apple"]
        
        for asset in assets:
            self.canvas.create_rectangle(20, y_offset, CANVAS_WIDTH - 20, y_offset + 60, color="#f7fafc")
            price = self.current_prices[asset]
            self.canvas.create_text(40, y_offset + 25, text=f"{asset}: ${price:.2f}", font="Arial", font_size=13, color="black")
            
            owned = self.portfolio[asset]
            val = owned * price
            max_buy = self.get_max_buy(asset)
            
            self.canvas.create_text(40, y_offset + 48, text=f"Owned: {owned} units (Value: ${val:.2f}) | Affordable Max: {max_buy}", font="Arial", font_size=10, color="gray")
            y_offset += 75
            
        # Logging notification and footer hints
        self.canvas.create_text(20, 420, text=self.message, font="Arial", font_size=12, color="red" if self.is_bankrupt else "black")
        self.canvas.create_text(20, 460, text="Status: Input command inside the terminal layout...", font="Arial", font_size=10, color="gray")

    def run_console_loop(self):
        while True:
            # Check for win/loss break conditions
            if self.game_mode == 1 and self.day > CLASSIC_TOTAL_DAYS:
                break
            if self.game_mode == 2 and self.is_bankrupt:
                break
                
            print(f"\n--- DAY {self.day} ({'10-Day Challenge' if self.game_mode == 1 else 'Endless Survival'}) ---")
            print("[1] Buy Asset")
            print("[2] Sell Asset")
            print("[3] End Day (Next Day)")
            print("[4] Exit Game")
            
            choice = input("Choose an action (1-4): ").strip()
            
            if choice == '1':
                print("\n  --> Select Asset to BUY:")
                print("  [1] Bitcoin  | [2] Ethereum | [3] Apple")
                sub = input("  Choice (1-3): ").strip()
                asset = "Bitcoin" if sub == '1' else "Ethereum" if sub == '2' else "Apple" if sub == '3' else None
                
                if asset:
                    max_buy = self.get_max_buy(asset)
                    print(f"  Max affordable: {max_buy} units.")
                    try:
                        amount = int(input(f"  How many units of {asset}? "))
                        self.buy_asset(asset, amount)
                    except ValueError:
                        print("  Invalid quantity!")
                else:
                    print("  Invalid selection.")
                    
            elif choice == '2':
                print("\n  --> Select Asset to SELL:")
                print("  [1] Bitcoin  | [2] Ethereum | [3] Apple")
                sub = input("  Choice (1-3): ").strip()
                asset = "Bitcoin" if sub == '1' else "Ethereum" if sub == '2' else "Apple" if sub == '3' else None
                
                if asset:
                    print(f"  You own {self.portfolio[asset]} units.")
                    try:
                        amount = int(input(f"  How many units of {asset}? "))
                        self.sell_asset(asset, amount)
                    except ValueError:
                        print("  Invalid quantity!")
                else:
                    print("  Invalid selection.")
                    
            elif choice == '3':
                print("\nAdvancing day and shifting markets...")
                self.next_day()
                
            elif choice == '4':
                print("Exiting game...")
                break
            else:
                print("Invalid command.")
                continue
            
            self.draw_dashboard()

        # Final Wrap-up screens
        self.draw_dashboard()
        print("\n=============================================")
        print("                 GAME OVER!                  ")
        if self.is_bankrupt:
            print("Reason: You went BANKRUPT! (Total Net Worth fell <= 0)")
        else:
            print("Reason: 10-Day Challenge completed successfully!")
        print(f"Your Final Net Worth is: ${self.get_net_worth():.2f}")
        print("=============================================")

def main():
    FantasyTraderGame()

if __name__ == '__main__':
    main()
