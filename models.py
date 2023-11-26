from datetime import datetime

class Stock:
    def __init__(self, symbol, name, sector):
        self.symbol = symbol
        self.name = name
        self.sector = sector
    
class StockValue:
    def __init__(self, symbol, date, open, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class TimeSeries:
    '''
    A TimeSeries instance represents a series of stock data for a given stock symbol over a given date range.
    Series data will be filtered to only include data within the specified date range.
    '''
    def __init__(self, symbol: str, series_type: str, start_date: datetime, end_date: datetime, series: list):
        self.symbol = symbol
        self.series_type = series_type
        self.start_date = start_date
        self.end_date = end_date
        self.series = self.__filter_date_range(series)

    def __filter_date_range(self, series: list):
        # find the date format of the series
        date_format = '%Y-%m-%d'
        if len(series) > 0:
            date_format = '%Y-%m-%d %H:%M:%S' if ' ' in series[0].date else '%Y-%m-%d'

        filtered_series = [data for data in series if self.start_date <= datetime.strptime(data.date, date_format) <= self.end_date]
        return filtered_series

    

