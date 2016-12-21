from ssm import Market, Stock, Transaction


class TransactionFactory:
    def __init__(self, market, no_of_transactions):
        self.signal_options = ['buy', 'sell']
        for stock in market.stocks:
            for transaction_no in range(no_of_transactions):
                transaction = Transaction()
                stock.add_transaction(transaction)


class StockFactory:
    def __init__(self, no_of_stocks):
        self.stock_list = []
        self.stock_name_options = []
        self.stock_list.append(Stock())


class MarketFactory:
    def __init__(self, no_of_markets):
        self.market_list = []
        for i in range(no_of_markets):
            self.market_list.append(Market())