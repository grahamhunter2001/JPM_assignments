#-------------------------------------------------------------------------------
# Name:        simple stock market
# Purpose:     JPM programming assignment
#
# Author:      Graham
#
# Created:     24-05-2016
# Copyright:   (c) Graham 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
# Used for timestamp
import weakref
# Used for class object instances
import random
#Used for testing

trade_lst = []
# Initiate list object for storing trade data
# Trades stored as a list as there may be many trades for the same company at the
# same time.

#Create a class for stocks so new stocks can be added and old ones removed
class stock():
    # Create a set for the stock instances
    _instances = set()
    # initialise variables
    def __init__(self, sym, typ, last_div, fixed_div, par_val):
        try:
            self._instances.add(weakref.ref(self))
            self.sym = str(sym).upper()
            self.typ = str(typ)
            self.last_div = int(last_div)
            self.fixed_div = float(fixed_div)
            self.par_val = int(par_val)
        except: print("error creating stock")

    def getinstances(Class):
        # function for getting instances of a class
        # Used to get stock class objects
        dead = set()
        for ref in Class._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        Class._instances -= dead

    def div_yield(self, price):
        # Check price is positive
        if price <= 0:
            print("trade price is negative")
        if self.typ.lower() == "common":
            div_yield = self.last_div/price
        elif self.typ.lower() == "preferred":
            div_yield = (self.fixed_div*self.par_val)/price
        else:
            print("stock type not defined - needs to be either 'common' or 'preferred'")
        return div_yield

    def pe_ratio(self, price):
        if price <= 0:
            print("price is negative")
        if self.last_div == 0:
            pe_ratio = "N/A - last div = 0"
        else:
            pe_ratio = price/self.last_div
        return pe_ratio

    def vol_w_sp(self):
        now = time.time()
        five_min_ago = time.time() - 5*60
        vol_w_sp = 0
        counter = -1
        numerator = 0
        denominator = 0
        # trade list timestamps run from oldest to newest therefore, run up the
        # list so we don't have a long wait for a large set of trades
        while trade_lst[counter][0] > five_min_ago and abs(counter) < len(trade_lst):
            price = trade_lst[counter][4]
            vol = trade_lst[counter][3]
            numerator += price*vol
            denominator += vol
            counter += -1
        try:
            vol_w_sp = numerator/denominator
        except: print("Error in volume weighted share price calculation")
        return vol_w_sp

# Record a trade, with timestamp, quantity, buy or sell indicator and price
def trade(sym, bs, vol, price):
    #Check sym against defined stocks
    curr_stocks = []
    for i in stock.getinstances(stock):
        curr_stocks.append(i.sym)
    if sym.upper() not in curr_stocks:
        print("stock not defined")
    #Check price and vol are positive
    if price < 0 or vol < 0:
        print("Error: Price or Volume are negative")
    timestamp = time.time()
    trade_lst.append([timestamp, sym, bs, vol, price])

# Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks
def gbce():
    data = []
    for i in stock.getinstances(stock):
        data.append(i.vol_w_sp())
    n = len(data)
    prod = 1
    for i in data:
        prod *= i
    gbce = prod*(1/n)
    return gbce

#Testing

# Add stocks
TEA = stock("TEA", "common", 0, 0, 100)
POP = stock("POP", "common", 8, 0, 100)
ALE = stock("ALE", "common", 23,0, 60)
GIN = stock("GIN", "preferred", 8, 0.02, 100)
JOE = stock("JOE", "common", 13, 0, 250)

# Record trades
for i in range(10):
    sym = ["TEA", "POP", "ALE", "GIN", "JOE"]
    bs = ["b", "s"]
    trade(random.choice(sym), random.choice(bs), random.randint(1,100), random.randint(1,100))

print(trade_lst)
price = 1
print(TEA.div_yield(price))
print(TEA.pe_ratio(price))
print(TEA.vol_w_sp())
print(gbce())
