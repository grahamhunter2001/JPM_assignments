import datetime
from warnings import warn
import operator
from regex import match

"""
Version: Python 3.5.2 :: Anaconda 4.0.0 (64 bit)
This file contains 3 classes: Market, Stock and Transaction

Market:
    Contains a list of stocks and carries out calculations on collections of Stock objects.
    Usage:
        LSE = Market()

    Implemented Methods:
        add_stock_to_market
        remove_stock_from_market
        list_stocks
        all_share_index

Stock:
    Contains stock data and a list of transactions. Carries out calculations on individual Stock objects and collections
    of stock transactions.

    Usage:
        GOOG = Stock(ticker='GOOG', stock_type='common', last_dividend=5, fixed_dividend=1.2, par_value=13)

    Implemented Methods:
        add_transaction
        dividend_yield
        PE_ratio
        validate_ticker_price
        get_transactions_for_last_x_min
        price

Transaction:
    Contains data for a single transaction. Note: A list within Stock could do this but it'd be more difficult to add
    functionality later e.g. recording the transaction history for audit purposes.

    Usage:
        recommended to use add_transaction method of Stock

    Implemented Methods:
        None

"""

class Market:
    """
    Object to hold all the stock objects and carry out market calculations
    """
    def __init__(self):
        """
            Args:
                None
        """
        self.stocks = []

    def add_stock_to_market(self, stock):
        """
        Adds stock object to the market
        :param stock:
        :return:
        """
        if not isinstance(stock, Stock):
            raise AttributeError("Error adding stock to market - not a valid stock object")

        for stocks in self.stocks:
            if stock.ticker == stocks.ticker and stock.stock_type == stocks.stock_type:
                raise LookupError("Stock already in market")

        self.stocks.append(stock)
        print("stock %s successfully added" % stock.ticker)

    def remove_stock_from_market(self, stock):
        """
        Removes a stock object from the market
        :param stock:
        :return:
        """
        if not isinstance(stock,Stock):
            raise AttributeError("stock must be a valid Stock object")
        try:
            self.stocks.remove(stock)
        except ValueError:
            raise ValueError("Error removing stock from market - stock not in market")

    def list_stocks(self):
        """
        Lists stocks in market
        :return: list of stocks
        """
        stock_list = []
        if len(self.stocks)>500:
            warn("There are over 500 stocks, are you sure you want to list them?")
            # TODO: Must be a way to get user input for continue/cancel options
        for stock in self.stocks:
            stock_list.append(stock)
        return stock_list

    def all_share_index(self):
        """
        Calculates and returns All Share Index
        :return: Market All Share Index
        """
        price_product = 1
        for stock in self.stocks:
            price_product *= stock.price()
        return price_product**(1/len(self.stocks))


class Stock:
    """
    Object to hold the stock data, list of transactions and carry out stock calculations
    """
    def __str__(self):
        return str(self._ticker)

    def __init__(self, ticker, stock_type='common', last_dividend=0, fixed_dividend=0, par_value=0):
        self._ticker = ticker
        self._stock_type = stock_type
        self._last_dividend = last_dividend
        self._fixed_dividend = fixed_dividend
        self._par_value = par_value
        self.transactions = []

    ticker = property(operator.attrgetter('_ticker'))
    stock_type = property(operator.attrgetter('_stock_type'))
    last_dividend = property(operator.attrgetter('_last_dividend'))
    fixed_dividend = property(operator.attrgetter('_fixed_dividend'))
    par_value = property(operator.attrgetter('_par_value'))

    @ticker.setter
    def ticker(self, t):
        if not isinstance(t, str):
            raise TypeError("Ticker must be a string")
        if len(t) not in range(1,6):
            raise Exception("Ticker must be between 1 and 5 letters")
        if not match(r'[aA-zZ]+', t):
            raise Exception("Ticker may not have numbers, punctuation or special characters")
        self._ticker = t

    @stock_type.setter
    def stock_type(self, st):
        if st not in ('common', 'preferred'):
            raise Exception("stock type must be 'common' or 'preferred'")
        self._stock_type = st

    @last_dividend.setter
    def last_dividend(self, ld):
        if not isinstance(ld, (int, float)):
            raise Exception("last dividend must be a number")
        if ld < 0:
            raise Exception("Cannot have negative last dividend")
        self._last_dividend = ld

    @fixed_dividend.setter
    def fixed_dividend(self, fd):
        if not isinstance(fd, (int, float)):
            raise Exception("fixed dividend must be a number")
        if fd < 0:
            raise Exception("Cannot have negative fixed dividend")
        self._fixed_dividend = fd

    @par_value.setter
    def par_value(self, v):
        if not isinstance(v, (int, float)):
            raise Exception("Par Value must be a number")
        if v < 0:
            raise Exception("Par Value must be positive")
        self._par_value = v

    def add_transaction(self, signal, price, volume, timestamp=datetime.datetime.now()):
        """
        Adds a transaction to a stock
        :param signal: 'buy' or 'sell'
        :param price: positive real number
        :param volume: positive real number
        :param timestamp: datetime object
        :return:
        """
        self.transactions.append(Transaction(signal, price, volume, timestamp))

    def dividend_yield(self, ticker_price):
        """
        Calculates the stock dividend yield given a ticker price
        :param ticker_price: positive real number
        :return: dividend yield
        """
        validator = self.validate_ticker_price(ticker_price)
        if isinstance(validator, Exception):
            raise validator
        if self.stock_type == 'common':
            dividend_yield = self.last_dividend/float(ticker_price)
        elif self.stock_type == 'preferred':
            dividend_yield = self.fixed_dividend*self.par_value/float(ticker_price)
        else:
            raise Exception('stock type not supported')
        return dividend_yield

    def PE_ratio(self, ticker_price):
        """
        Calculates the stock PE ratio given a ticker price
        :param ticker_price:
        :return: PE ratio
        """
        self.validate_ticker_price(ticker_price)
        return float(ticker_price)/self.last_dividend

    def validate_ticker_price(self, ticker_price):
        """
        Validates the ticker price is a positive real number
        :param ticker_price:
        :return:
        """
        if not isinstance(ticker_price, (int, float)):
            return TypeError("ticker price must be a number")
        if ticker_price <= 0:
            return ValueError("ticker price must be greater than zero")

    def get_transactions_for_last_x_min(self, x=datetime.timedelta(minutes=15)):
        """
        helper method for getting transactions over a period of time
        :param x: datetime.timedelta object
        :return: list of transactions from now to now - x
        """
        latest_trans_list = []
        time_now = datetime.datetime.now()
        sorted_transactions = sorted(self.transactions, key=operator.attrgetter("timestamp"), reverse=True)
        loop_stop = False
        while loop_stop == False and len(sorted_transactions) > 0:
            last_transaction = sorted_transactions.pop()
            if (time_now - last_transaction.timestamp) < x:
                latest_trans_list.append(last_transaction)
            else:
                loop_stop = True
        return latest_trans_list

    def price(self):
        total_volume = 0
        numerator = 0
        latest_transactions = self.get_transactions_for_last_x_min()
        try:
            for transaction in latest_transactions:
                numerator += transaction.price*transaction.volume
                total_volume += transaction.volume
            return numerator/total_volume
        except ZeroDivisionError:
            print("Error in calculation - no transactions in interval")

    # TODO: Useful methods to implement
    def remove_stock(self):
        # for each market object remove the stock then delete self
        pass

    def ammend_stock(self, property, value):
        pass

    def get_transactions_by_date(self,date):
        pass

    def get_transactions_by_price_range(self, low, high):
        pass

    def get_transactions_by_volume_range(self, low, high):
        pass

    def get_transactions_by_signal(self, signal):
        pass


class Transaction:
    """
    Object to hold the transaction data
    """
    def __init__(self, signal, price, volume, timestamp=datetime.datetime.now()):

        self._signal = signal
        self._price = price
        self._volume = volume
        self._timestamp = timestamp

    signal = property(operator.attrgetter('_signal'))
    price = property(operator.attrgetter('_price'))
    volume = property(operator.attrgetter('_volume'))
    timestamp = property(operator.attrgetter('_timestamp'))

    @signal.setter
    def signal(self, s):
        if s.lower() not in ('buy', 'sell'):
            raise ValueError("Signal must be either 'buy' or 'sell'")
        self._signal = s.lower()

    @price.setter
    def price(self, p):
        if not isinstance(p, (int, float)):
            raise TypeError("Price must be a number")
        if p < 0:
            raise ValueError("Price must be positive")
        self._price = p

    @volume.setter
    def volume(self,v):
        if not isinstance(v, (int, float)):
            raise TypeError("Volume must be a number")
        if v < 0:
            raise ValueError("Volume must be positive")
        self._volume = v

    @timestamp.setter
    def timestamp(self,ts):
        if not isinstance(ts, datetime.datetime):
            raise TypeError("Timestamp must be datetime object")
        self._timestamp = ts
    # this class could be extended to record changes to transactions for audit purposes
