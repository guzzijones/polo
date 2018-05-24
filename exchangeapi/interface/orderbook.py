
class Rounded(object):
    def __init__(self,number,decimals):
        self.value = round(number,decimals)
        self.decimals=decimals

    def key(self):
        return (self.value,self.decimals)

    def __add__(self, other):
        round(self.value+other.value,self.decimals)

    def __sub__(self, other):
        round(self.value - other.value,self.decimals)

    def __mul__(self,number):
        return round(self.value * number.value,self.decimals)

    def __truediv__(self, other):
        return round(self.value / other.value,self.decimals)

    def __eq__(self,other):
        return self.key()==other.key()

    def __lt__(self,other):
        return self.value < other.value

    def __gt__(self,other):
        return self.value > other.value

    def __le__(self,other):
        return self.value <= other.value

    def __ge__(self,other):
        return self.value >= other.value

    def __ne__(self,other):
        return self.value != other.value

    def __hash__(self):
        return hash(self.key())

    def __str__(self):
        return str(self.value)



class MarketOrderBook(object):
    """orderbook interface class
        """
    ASK="ASK"
    BID="BID"
    def __init__(self,slug,asks,bids):
        """slug = string ie - BTC_XMR,
            asks = dict keys-Rounded price, value- Rounded amount
            bids = dict keys-Rounded price , value- Rounded amount"""
        #todo(aj) check types of incoming parameters
        self.slug = slug
        self.asks = asks
        self.bids = bids

class Books(object):
    """all books interface class
    """
    def __init__(self,site_name):
        self.site_name=site_name
        self.markets={}
    def add_market(self, order_book):
        """order_book = MarketOrderBook"""
        #todo(aj) check type of order_book
        self.markets[order_book.slug]=order_book

