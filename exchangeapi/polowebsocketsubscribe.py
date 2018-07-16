import logging
import traceback
LOG = logging.getLogger(__name__)
import websocket
import _thread
import time
import json
import argparse
from poloniex.app import SyncApp
from exchangeapi.interface.trade import Trade
from datetime import datetime
import sys
import exchangeapi.interface.orderbook as ord
import exchangeapi.interface.triangle as tri
import sys

class PoloWebSocket(tri.SockerWorker):
    DECIMALS=8
    CHANNEL_MAP={
        1001:1001, #trollbox
        1002:1002, #ticker
        1003:1003, #base coin 24 hour stats
        1010:1010  #heartbeat
    }

    def __init__(self,tickers,channels=None,process_trades=False):
        """

        :param tickers: dict
        :param channels: list of slugs
        :param process_trades:  boolean
        :param ws_address: string
        """
        super(PoloWebSocket,self).__init__()

        self.channels=channels
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.tickers=tickers
        self.orderbooks={}
        #set reverse lookup on code instead of channel order book
        self.code_map = {}
        for key,value in self.tickers.items():
            self.code_map[value['id']]=key

        self.message_count={}
        self.ord_book = ord.Books("Poloniex")
        self.process_trades=process_trades



    def get_float_dict(self,in_dict):
        new_dict = in_dict
        index=0
        for instance in new_dict["orderBook"]:
            new_instance = {}
            for key,value in instance.items():
                new_instance[ord.Rounded(float(key),PoloWebSocket.DECIMALS)]=ord.Rounded(float(value),PoloWebSocket.DECIMALS)
            new_dict["orderBook"][index]=new_instance
            index+=1
        return new_dict

    def handle_cur(self,data_list_str):
        data_list = eval(data_list_str)
        LOG.debug(data_list)
        channel_id=data_list[0]
        LOG.info("channelid " + str(channel_id))
        if channel_id in self.code_map.keys():
            book = self.code_map[channel_id]
            seq =  data_list[1]
            data = data_list[2]
            for entry in data:
                type_record = entry[0]
                if type_record == "i":
                    orderbook_data = entry[1]
                    LOG.debug("handle header")

                    book_details=self.get_float_dict(orderbook_data)
                    market_book = ord.MarketOrderBook(book,book_details["orderBook"][0],
                                                  book_details["orderBook"][1])
                    self.ord_book.add_market(market_book)
                    self.post_orderbook_load(market_book)
                    #raise RuntimeError("test")
                if type_record == "o":
                    ask_bid=entry[1]
                    price= entry[2]
                    amount = entry[3]
                    ask_bid_const = ord.MarketOrderBook.ASK if ask_bid==0 else ord.MarketOrderBook.BID
                    if amount=='0.00000000':
                        if ask_bid_const==ord.MarketOrderBook.ASK:
                            self.ord_book.markets[book].asks.pop(ord.Rounded(float(price),PoloWebSocket.DECIMALS))
                            self.post_ask_pop(book=book,ask_bid=ask_bid_const,price=ord.Rounded(float(price),decimals=PoloWebSocket.DECIMALS))
                        else:
                            self.ord_book.markets[book].bids.pop(ord.Rounded(float(price),PoloWebSocket.DECIMALS))
                            self.post_bid_pop(book=book,ask_bid=ask_bid_const,price=ord.Rounded(float(price),decimals=PoloWebSocket.DECIMALS))
                    else:
                        if ask_bid_const==ord.MarketOrderBook.ASK:
                            self.ord_book.markets[book].asks[ord.Rounded(float(price),PoloWebSocket.DECIMALS)]=\
                                ord.Rounded(float(amount),PoloWebSocket.DECIMALS)
                        else:
                            self.ord_book.markets[book].bids[ord.Rounded(float(price),PoloWebSocket.DECIMALS)]=\
                                ord.Rounded(float(amount),PoloWebSocket.DECIMALS)
                        self.post_orderbook_handle_askbid(book=book,ask_bid=ask_bid_const,price=ord.Rounded(float(price),decimals=PoloWebSocket.DECIMALS))
                    # 1 = bids
                    # 0 = asks
                if type_record =="t" and self.process_trades:
                    date_time = datetime.utcfromtimestamp(int(entry[5])).strftime('%Y-%m-%d %H:%M:%S')
                    buy_sell = "buy" if entry[2]== 0 else "sell"
                    trade = Trade(entry[0],
                                  int(entry[1]),
                                  date_time,
                                  book,
                                  buy_sell,
                                  float(entry[3]),
                                  float(entry[4])
                                  )
                    trade.commit()

    def handle_1001(self,data_list):
        pass

    def handle_1002(self,data_list):
        pass

    def handle_1003(self,data_list):
        LOG.debug("handle_1003")
        pass

    def on_message(self,ws, message):
        # call handler
        LOG.debug(message)
        try:
            self.handle_cur(message)
        except Exception as e:
            LOG.error(traceback.format_exc())
            sys.exit(1)

    def on_error(self,ws, error):
        LOG.error("an error occured:" + error.__str__())

    def on_close(self,ws):
        LOG.debug("### closed ###")

    def on_open(self,ws):
        LOG.info("ONOPEN")
        def run(*args):
            #ws.send(json.dumps({'command':'subscribe','channel':1001}))
            #ws.send(json.dumps({'command':'subscribe','channel':1002}))
            #ws.send(json.dumps({'command':'subscribe','channel':1003}))
            for channel in self.channels:
                ws.send(json.dumps({'command':'subscribe','channel':channel}))
            while True:
                time.sleep(1)
            ws.close()
            LOG.info("thread terminating...")
        _thread.start_new_thread(run, ())

    def run(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key",help="api key", required=True)
    parser.add_argument("--api_secret",help="api secret", required=True)
    parser.add_argument("--pair",action='append',help="pair slug", required=True)
    parser.add_argument("--process_trades",action='store_true',help="process trades ; upload to slug")
    parser.add_argument("--log_file",help="log file")
    parser.add_argument("--log_level",help="log level")
    args = parser.parse_args()

    if args.log_file is not None:
        logging.basicConfig(filename=args.log_file,level=getattr(logging,args.log_level.upper()),
                            format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s'
                            )
    else:
        logging.basicConfig(level=getattr(logging,args.log_level.upper()),
                            format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s'
                            )

    channels=args.pair
    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)

    tickers = app.public.returnTicker()
    polosock = PoloWebSocket(tickers,channels,process_trades=args.process_trades)
    websocket.enableTrace(True)
    polosock.run()
    #ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
    #                          on_message = on_message,
    #                          on_error = on_error,
    #                          on_close = on_close)
    #ws.on_open = on_open
    #ws.run_forever()
    #channels=['BTC_XMR',1001,1002,1003]

if __name__ == "__main__":
    main()
