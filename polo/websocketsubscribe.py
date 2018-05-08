import websocket
import _thread
import time
import json
import argparse
from poloniex.app import SyncApp
from polo.model import TradeSocket,OrderBookSocket
import sys
#todo(aj) create model based on https://stackoverflow.com/questions/32154121/how-to-connect-to-poloniex-com-websocket-api-using-a-python-library
#todo

class PoloWebSocket(object):
    CHANNEL_MAP={
        1001:1001, #trollbox
        1002:1002, #ticker
        1003:1003, #base coin 24 hour stats
        1010:1010  #heartbeat
    }
    def __init__(self,tickers,channels=None):

        pass
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


    def handle_cur(self,data_list_str):
        #todo(aj) initial message can be handled via a decorator
        data_list = eval(data_list_str)
        print(data_list)
        channel_id=data_list[0]
        print("channelid " + str(channel_id))
        #print("codemap " + str(self.code_map))
        if channel_id in self.code_map.keys():
            book = self.code_map[channel_id]
            seq =  data_list[1]
            data = data_list[2]
            for entry in data:
                type_record = entry[0]
                if type_record == "i":
                    orderbook_data = entry[1]
                    print("handle header")
                    self.orderbooks[book]=orderbook_data
                if type_record == "o":
                    type_record=entry[0]
                    ask_bid=entry[1]
                    price= entry[2]
                    amount = entry[3]
                    if amount=='0.00000000':
                        self.orderbooks[book]['orderBook'][ask_bid].pop(price)
                    else:
                        self.orderbooks[book]['orderBook'][ask_bid][price]=amount
                    # 1 = bids
                    # 0 = asks
                #todo(aj) type_record=="t"

    def handle_1001(self,data_list):
        pass

    def handle_1002(self,data_list):
        pass

    def handle_1003(self,data_list):
        print("handle_1003")
        pass

    def on_message(self,ws, message):
        # call handler
        print(message)
        self.handle_cur(message)

    def on_error(self,ws, error):
        print(error)

    def on_close(self,ws):
        print("### closed ###")

    def on_open(self,ws):
        print("ONOPEN")
        def run(*args):
            #ws.send(json.dumps({'command':'subscribe','channel':1001}))
            #ws.send(json.dumps({'command':'subscribe','channel':1002}))
            #ws.send(json.dumps({'command':'subscribe','channel':1003}))
            for channel in self.channels:
                ws.send(json.dumps({'command':'subscribe','channel':channel}))
            while True:
                time.sleep(1)
            ws.close()
            print("thread terminating...")
        _thread.start_new_thread(run, ())

    def run(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever()

if __name__ == "__main__":
    #todo(aj) sqlalchemy clear orderbook.
    #channels=['BTC_XMR',1001,1002,1003]
    parser = argparse.ArgumentParser()
    subparser= parser.add_subparsers(help="subcommand help")
    parser.add_argument("--api_key",help="api key", required=True)
    parser.add_argument("--api_secret",help="api secret", required=True)
    parser.add_argument("--pair",action='append',help="pair slug", required=True)
    args = parser.parse_args()

    channels=args.pair
    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)

    tickers = app.public.returnTicker()
    polosock = PoloWebSocket(tickers,channels)
    websocket.enableTrace(True)
    polosock.run()
    #ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
    #                          on_message = on_message,
    #                          on_error = on_error,
    #                          on_close = on_close)
    #ws.on_open = on_open
    #ws.run_forever()