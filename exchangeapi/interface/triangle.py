import logging
import json
import time
import sys
import _thread
import websocket
from exchangeapi.interface.orderbook import Rounded
from datetime import datetime
from exchangeapi.interface.trade import Trade
import exchangeapi.interface.orderbook as ord
LOG = logging.getLogger(__name__)

class SockerWorker(object):
    def __init__(self):
        pass

    def post_orderbook_handle_askbid(self,book,ask_bid,price):
        """abstract function to override
        book = MarketOrderBook
        ask_bid = MarketOrderBook.BID or MarketOrderBook.ASK
        price = Rounded
        decimals = int'"""
        pass

    def post_ask_pop(self,book,ask_bid,price):
        """abstract function to override
        book = MarketOrderBook
        ask_bid = MarketOrderBook.BID or MarketOrderBook.ASK
        price = Rounded
        decimals = int'"""
        pass

    def post_bid_pop(self,book,ask_bid,price):
        """abstract function to override
        book = MarketOrderBook
        ask_bid = MarketOrderBook.BID or MarketOrderBook.ASK
        price = Rounded
        decimals = int'"""
        pass

    def post_orderbook_load(self,book):
        pass

    def get_balances(self,instance,decimals):
        """return dict - String:Rounded"""
        new_instance = {}
        for key, value in instance.items():
            new_instance[key] = Rounded(float(value), decimals)
        return new_instance


class WebSocket(SockerWorker):
    def __init__(self,tickers,channels=None,process_trades=False,socket_addr=None,name=None,decimals=None):
        super(WebSocket,self).__init__()
        """
        :param tickers: dict
        :param channels: list of slugs 
        :param process_trades:  boolean
        :param ws_address: string
        :param socket_addr: string
        :param name: string
        :param decimals: int
        """
        self.decimals=decimals
        self.channels=channels
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(socket_addr,
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
        self.ord_book = ord.Books(name)
        self.process_trades=process_trades



    def get_float_dict(self,in_dict):
        new_dict = in_dict
        index=0
        for instance in new_dict["orderBook"]:
            new_instance = {}
            for key,value in instance.items():
                new_instance[ord.Rounded(float(key),self.decimals)]=ord.Rounded(float(value),self.decimals)
            new_dict["orderBook"][index]=new_instance
            index+=1
        return new_dict

    def handle_cur(self,data_list_str):
        pass

    def on_message(self,ws, message):
        # call handler
        LOG.debug(message)
        try:
            self.handle_cur(message)
        except Exception as e:
            LOG.error(str(e))
            sys.exit(1)

    def on_error(self,ws, error):
        LOG.error(error)
        #sys.exit(1)

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


