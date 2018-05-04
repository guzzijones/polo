import websocket
import _thread
import time
import json
import sys
#todo(aj) create model based on https://stackoverflow.com/questions/32154121/how-to-connect-to-poloniex-com-websocket-api-using-a-python-library
#todo

class PoloWebSocket(object):
    CHANNEL_MAP={
        "BTC_XMR":114,
        1001:1001,
        1002:1002,
        1003:1003
    }
    def __init__(self,channels=None):

        pass
        self.channels=channels
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)

        self.message_count={}
        for channel in self.channels:
            self.message_count[PoloWebSocket.CHANNEL_MAP[channel]]=0

    #todo(aj) make this a decorator
    def handle_orderbook_header(self,data_list):
        pass
        print("handle header orderbook")

    def handle_cur(self,data_list):
        #todo(aj) initial message can be handled via a decorator
        channel_id=data_list[0]
        if self.message_count[channel_id]==0:
            print("handle header")
            self.handle_orderbook_header(data_list)
            self.message_count[channel_id]+=1
        else:
            print("handle_cur")

    def handle_1001(self,data_list):
        pass

    def handle_1002(self,data_list):
        pass

    def handle_1003(self,data_list):
        print("handle_1003")
        pass

    def on_message(self,ws, message):
        handler = message[0]
        # call handler
        #getattr(sys.modules[__name__], "handle_%s" % handler)(message)
        print(message)

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
    channels=['BTC_XMR',1001,1002,1003]
    polosock = PoloWebSocket(channels)
    websocket.enableTrace(True)
    polosock.run()
    #ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
    #                          on_message = on_message,
    #                          on_error = on_error,
    #                          on_close = on_close)
    #ws.on_open = on_open
    #ws.run_forever()