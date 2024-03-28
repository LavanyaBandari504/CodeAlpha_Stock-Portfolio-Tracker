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
        print("\nStock Portfolio:")
        print("Symbol\tQuantity\tAverage Price")
        for symbol, stock_info in self.portfolio.items():
            print(f"{symbol}\t{stock_info['quantity']}\t\t${stock_info['avg_price']:.2f}")

# Replace 'YOUR_ALPHA_VANTAGE_API_KEY' with your actual API key
api_key = 'TO6N2XDUU8Y37G11'
tracker = StockPortfolioTracker(api_key)

# Adding stocks to the portfolio
tracker.add_stock('AAPL', 5)
tracker.add_stock('GOOGL', 2)

# Displaying the initial portfolio
tracker.display_portfolio()

# Updating portfolio and displaying total portfolio value
portfolio_value = tracker.update_portfolio()
print(f"\nTotal Portfolio Value: ${portfolio_value:.2f}")

# Removing stocks from the portfolio
tracker.remove_stock('AAPL', 3)
tracker.remove_stock('GOOGL', 2)

# Displaying the updated portfolio
tracker.display_portfolio()

# Updating portfolio and displaying total portfolio value after removal
portfolio_value = tracker.update_portfolio()
print(f"\nUpdated Total Portfolio Value: ${portfolio_value:.2f}")
 
 
