from models import Stock
import csv
from stock_exceptions import StockLoadException

# load stocks from csv file stocks.csv into list of Stock instances
class StockLoader:
    def __init__(self, stocks_file_path: str):
        self.stocks_file_path = stocks_file_path
        self.stocks = self.__load_stocks()

    def __load_stocks(self):
        try:
            stocks = []
            with open(self.stocks_file_path, newline='') as stocks_file:
                reader = csv.DictReader(stocks_file)
                for row in reader:
                    stocks.append(Stock(row['Symbol'], row['Name'], row['Sector']))
            return stocks
        except Exception as e:
            raise StockLoadException(f"Error loading stock data: {e}")

