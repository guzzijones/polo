
from polo.model import TradeSocket,db_session,RestTrade,LargeTrade

class Trade(object):
    def __init__(self,
                 trade_type,
                 id,
                 date,
                 pair,
                 sell_buy,
                 price,
                 amount,
                 threshold):
        self.trade=TradeSocket()
        self.trade.trade=trade_type
        self.trade.id=id
        self.trade.timestamp=date
        self.trade.book= pair
        self.trade.type= sell_buy
        self.trade.price = price
        self.trade.amount= amount
        db_session.add(self.trade)

    def commit(self):
        db_session.commit()
