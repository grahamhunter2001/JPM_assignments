from unittest import TestCase, skip
import datetime
from ssm import Market, Stock

"""
Requirements
1. Provide working source code that will :-
a. For a given stock,
    i. calculate the dividend yield
    ii. calculate the P/E Ratio
    iii. record a trade, with timestamp, quantity of shares, buy or sell indicator and price
    iv. Calculate Stock Price based on trades recorded in past 15 minutes

b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
"""


class MarketTests(TestCase):

    def setUp(self):
        pass

    def test_create_new_market(self):
        market1 = Market()
        self.assertIsInstance(market1, Market)

    def test_add_stock_to_market(self):
        market1 = Market()
        stock1 = Stock('GOOG')
        market1.add_stock_to_market(stock1)
        self.assertIn(stock1, market1.stocks)

    def test_remove_stock_from_market(self):
        market1 = Market()
        stock1 = Stock('GOOG')
        market1.add_stock_to_market(stock1)
        market1.remove_stock_from_market(stock1)
        self.assertNotIn(stock1, market1.stocks)

    def test_stocks_in_different_markets_are_separate(self):
        market1 = Market()
        market2 = Market()
        stock1 = Stock('APPL')
        market1.add_stock_to_market(stock1)
        stock2 = Stock('GOOG')
        market2.add_stock_to_market(stock2)
        self.assertIn(stock1, market1.stocks)
        self.assertIn(stock2, market2.stocks)
        self.assertNotIn(stock2, market1.stocks)
        self.assertNotIn(stock1, market2.stocks)


class AddStockTest(TestCase):

    def setUp(self):
        self.market1 = Market()

    def test_add_new_stock(self):
        stock = Stock('APPL')
        self.market1.add_stock_to_market(stock)
        self.assertIn(stock, self.market1.stocks)

    def test_add_bad_stock(self):
        self.assertRaises(AttributeError, self.market1.add_stock_to_market,'APPL')

    def test_remove_bad_stock(self):
        self.assertRaises(AttributeError, self.market1.remove_stock_from_market, 'APPL')
        stock = Stock('APPL')
        self.assertRaises(ValueError, self.market1.remove_stock_from_market, stock)

    def test_empty_stock_ticker(self):
        self.assertRaises(Exception, Stock(''))

    def test_ticker_length(self):
        self.assertIsInstance(Stock('A'), Stock)
        self.assertIsInstance(Stock('AAAAA'), Stock)
        self.assertIsInstance(Stock('AB123'), Stock)
        self.assertRaises(TypeError, Stock(123))
        self.assertRaises(Exception, Stock(' A'))
        self.assertRaises(Exception, Stock('A '))
        self.assertRaises(Exception, Stock('!@£$%'))
        self.assertRaises(Exception, Stock('AAAAAA'))

    def test_good_stock_type(self):
        stock1 = Stock('APPL', 'common')
        self.assertIsInstance(stock1, Stock)
        stock2 = Stock('APPL', 'preferred')
        self.assertIsInstance(stock2, Stock)

    def test_bad_stock_type(self):
        self.assertRaises(Exception, Stock('APPL', 'other type'))

    def test_good_last_dividend(self):
        stock1 = Stock('APPL', last_dividend=0)
        stock2 = Stock('APPL', last_dividend=5)
        stock3 = Stock('APPL', last_dividend=12.3)
        self.assertIsInstance(stock1, Stock)
        self.assertIsInstance(stock2, Stock)
        self.assertIsInstance(stock3, Stock)

    def test_bad_last_dividend(self):
        self.assertRaises(Exception, Stock('APPL', last_dividend=-1))
        self.assertRaises(Exception, Stock('APPL', last_dividend='sadf'))

    def test_good_fixed_dividend(self):
        stock1 = Stock('APPL', fixed_dividend=0)
        stock2 = Stock('APPL', fixed_dividend=5)
        stock3 = Stock('APPL', fixed_dividend=12.3)
        self.assertIsInstance(stock1, Stock)
        self.assertIsInstance(stock2, Stock)
        self.assertIsInstance(stock3, Stock)

    def test_bad_fixed_dividend(self):
        self.assertRaises(Exception, Stock('APPL', fixed_dividend=-1))
        self.assertRaises(Exception, Stock('APPL', fixed_dividend='sadf'))

    def test_good_par_value(self):
        stock1 = Stock('APPL', par_value=0)
        stock2 = Stock('APPL', par_value=5)
        stock3 = Stock('APPL', par_value=12.3)
        self.assertIsInstance(stock1, Stock)
        self.assertIsInstance(stock2, Stock)
        self.assertIsInstance(stock3, Stock)

    def test_bad_par_value(self):
        self.assertRaises(Exception, Stock('APPL', par_value=-1))
        self.assertRaises(Exception, Stock('APPL', par_value='sadf'))

    def test_duplicate_stock_throws_error(self):
        stock1 = Stock('GOOG')
        stock2 = Stock('GOOG')
        stock3 = Stock('GOOG', 'preferred')
        self.market1.add_stock_to_market(stock1)
        self.assertRaises(LookupError, self.market1.add_stock_to_market, stock2)
        self.assertEqual(len(self.market1.list_stocks()),1)


class RemoveStockTest(TestCase):

    def setUp(self):
        pass

    @skip
    def test_remove_stock(self):
        self.fail()

    @skip
    def test_removing_non_existent_stock(self):
        self.fail()


class AmmendStockTest(TestCase):

    def setUp(self):
        pass

    @skip
    def test_ammend_stock_price(self):
        self.fail()

    @skip
    def test_ammend_stock_ticker(self):
        self.fail()

    @skip
    def test_ammend_stock_last_dividend(self):
        self.fail()

    @skip
    def test_ammend_stock_type(self):
        self.fail()

    @skip
    def test_ammend_stock_parvalue(self):
        self.fail()

    @skip
    def test_ammend_stock_fixed_dividend(self):
        self.fail()


class StockCalculationTest(TestCase):

    def setUp(self):
        pass

    def test_get_latest_transactions(self):
        time_now = datetime.datetime.now()
        stock1 = Stock('GOOG')
        stock1.add_transaction('buy', 10, 100, time_now)
        stock1.add_transaction('buy', 10, 100, time_now - datetime.timedelta(minutes=10))
        latest_transactions = stock1.get_transactions_for_last_x_min()
        self.assertEqual(len(latest_transactions), 2)
        stock1.add_transaction('buy', 10, 100, time_now - datetime.timedelta(minutes=30))
        self.assertEqual(len(latest_transactions), 2)

    def test_dividend_yield_common(self):
        stock1 = Stock("GOOG", last_dividend=10)
        divi_yield = stock1.dividend_yield(200)
        self.assertEqual(divi_yield, 10/200.)

    def test_dividend_yield_preferred(self):
        stock1 = Stock("GOOG", stock_type='preferred', fixed_dividend=10, par_value=2)
        divi_yield = stock1.dividend_yield(200)
        self.assertEqual(divi_yield, (10*2)/200.)

    def test_zero_ticker_price(self):
        stock1 = Stock("GOOG", last_dividend=10)
        self.assertRaises(ValueError, stock1.dividend_yield, 0)

    def test_negative_ticker_price(self):
        stock1 = Stock("GOOG", last_dividend=10)
        self.assertRaises(ValueError, stock1.dividend_yield, -4)

    def test_bad_ticker_price(self):
        stock1 = Stock("GOOG", last_dividend=10)
        self.assertRaises(TypeError, stock1.dividend_yield, 'blah')

    def test_PE_ratio(self):
        stock1 = Stock("GOOG", last_dividend=10)
        self.assertEqual(stock1.PE_ratio(200), 200/10.)

    def test_calculate_stock_price(self):
        stock1 = Stock("GOOG")
        stock1.add_transaction('buy', 10, 100)
        stock1.add_transaction('buy', 10, 100)
        stock_price = ((10*100)+(10*100))/(100+100.)
        self.assertEqual(stock1.price(), stock_price)


class AllStockCalculationTests(TestCase):

    def setUp(self):
        pass

    def test_GBCE_calculation(self):
        market1 = Market()
        stock1 = Stock("GOOG")
        stock2 = Stock("APPL")

        market1.add_stock_to_market(stock1)
        market1.add_stock_to_market(stock2)

        stock1.add_transaction('buy', 10, 100)
        stock2.add_transaction('buy', 10, 100)

        s1_price = stock1.price()
        s2_price = stock2.price()
        no_of_stocks = len(market1.list_stocks())
        asi = (s1_price*s2_price)**(1/no_of_stocks)
        self.assertEqual(market1.all_share_index(), asi)


class TestTransactions(TestCase):

    def setUp(self):
        self.stock = Stock('GOOG')

    def test_add_transaction_to_stock(self):
        self.stock.add_transaction('buy', 12.3, 100)
        self.assertEqual(self.stock.transactions[-1].signal, 'buy')
        self.assertEqual(self.stock.transactions[-1].price, 12.3)
        self.assertEqual(self.stock.transactions[-1].volume, 100)

    def test_add_bad_transaction(self):
        self.assertRaises(ValueError ,self.stock.add_transaction('blah', 12.3, 100))
        self.assertRaises(ValueError, self.stock.add_transaction('buy', -1, 100))
        self.assertRaises(TypeError, self.stock.add_transaction('buy', 'asfkjh', 100))
        self.assertRaises(ValueError, self.stock.add_transaction('buy', 12.3, -1))
        self.assertRaises(TypeError, self.stock.add_transaction('buy', 12.3, 'dsfjh'))