import requests
import json

class StockPortfolioTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol]['quantity'] += quantity
        else:
            self.portfolio[symbol] = {'quantity': quantity, 'avg_price': 0.0}

    def remove_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            if quantity >= self.portfolio[symbol]['quantity']:
                del self.portfolio[symbol]
            else:
                self.portfolio[symbol]['quantity'] -= quantity

    def update_portfolio(self):
        total_value = 0.0
        for symbol, stock_info in self.portfolio.items():
            response = self.get_stock_data(symbol)
            if 'Global Quote' in response:
                price = float(response['Global Quote']['05. price'])
                stock_info['avg_price'] = price
                total_value += price * stock_info['quantity']
        return total_value

    def get_stock_data(self, symbol):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        return data

    def display_portfolio(self):
        portfolio_str = "\nStock Portfolio:\n"
        portfolio_str += "Symbol\tQuantity\tAverage Price\n"
        for symbol, stock_info in self.portfolio.items():
            portfolio_str += f"{symbol}\t{stock_info['quantity']}\t\t${stock_info['avg_price']:.2f}\n"
        return portfolio_str

api_key = 'TO6N2XDUU8Y37G12'
tracker = StockPortfolioTracker(api_key)

while True:
    print("\nOptions:")
    print("1. Add stock")
    print("2. Remove stock")
    print("3. Display portfolio")
    print("4. Update portfolio")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        symbol = input("Enter stock symbol: ")
        quantity = int(input("Enter quantity: "))
        tracker.add_stock(symbol, quantity)
    elif choice == '2':
        symbol = input("Enter stock symbol to remove: ")
        quantity = int(input("Enter quantity to remove: "))
        tracker.remove_stock(symbol, quantity)
    elif choice == '3':
        print(tracker.display_portfolio())
    elif choice == '4':
        portfolio_value = tracker.update_portfolio()
        print(f"\nTotal Portfolio Value: ${portfolio_value:.2f}")
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
