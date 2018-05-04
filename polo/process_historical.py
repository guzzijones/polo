from poloniex.app import SyncApp
import argparse
from polo.model import Trade,db_session,RestTrade
from datetime import datetime,timedelta
from sqlalchemy import func

def get_dates(start):
    date_list = []
    end = datetime.today()+timedelta(days=1)
    while start < end:
        date_list.append(start)
        start = start+timedelta(days=1)
    return date_list

def load_results(results,pair):
    print("Results to upload:" + str(len(results)))
    i = 1
    for result in results:
        print("submitting row " + str(i) + " " + str(result["globalTradeID"]) )
        #if len(queryid) > 0:
        #    pass
        #else:
        i+=1
        trade = RestTrade()
        trade.globalTradeID=result["globalTradeID"]
        trade.tradeID=result['tradeID']
        trade.date = result['date']
        trade.book = pair
        trade.type= result['type']
        trade.rate = result['rate']
        trade.amount= result['amount']
        trade.total=result['total']
        db_session.add(trade)
        db_session.commit()


def get_results(app,pair,start_datetime_obj,end_datetime_obj):
    return app.public.returnTradeHistory(currency_pair=pair,
                                         start=start_datetime_obj,
                                         end=end_datetime_obj)


def main():
    HIST_WINDOWS = [
        ['2018-01-01','2018-01-31'],
        ['2018-02-01','2018-02-28'],
        ['2018-03-01','2018-03-31']
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key",help="api key", required=True)
    parser.add_argument("--api_secret",help="api secret", required=True)
    parser.add_argument("--pair",help="pair slug", required=True)
    parser.add_argument("--hist",help="run hist", action='store_true')
    parser.add_argument("--start",help="start yyyy-mm-dd")
    args = parser.parse_args()


    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)


    curs = app.public.returnCurrencies()
    balances = app.trading.returnBalances()
    tickers = app.public.returnTicker()
    pair = args.pair

    #truncate table for now
    #db_session.query(RestTrade).delete()
    #db_session.commit()

    # get max date from database.
    # if empty then use start date from script.
    # else use max date from db.

    start_datetime_obj = datetime.strptime(args.start,"%Y-%m-%d")
    dates = get_dates(start_datetime_obj)

    if args.hist:
        db_session.query(RestTrade).delete()
        db_session.commit()
        for entry in dates:
            end_datetime_obj = entry+timedelta(days=1)-timedelta(seconds=1)
            continue_paging=True
            while continue_paging==True:
                results = app.public.returnTradeHistory(currency_pair=pair,
                                         start=start_datetime_obj,
                                         end=end_datetime_obj)
                load_results(results,pair)
                if len(results) == 50000:
                    continue_paging=True
                    start_datetime_obj=db_session.query(func.max(RestTrade.date)).one()[0]+timedelta(seconds=1)
                else:
                    #done
                    continue_paging=False

    # normal daily run
    # catch up to midnight today
    # get max datetime + 1 second
    start= db_session.query(func.max(RestTrade.date)).one()[0]+1
    # pull result
    midnight_today=datetime.today()
    while start < midnight_today :
        results = app.public.returnTradeHistory(currency_pair=pair,
                                         start=start)
        load_results(results,pair)
        start= db_session.query(func.max(RestTrade.date)).one()[0]+1


if __name__== "__main__":
    #todo(aj) arg for key and sec
    #todo(aj) arg for currency pairs
    main()