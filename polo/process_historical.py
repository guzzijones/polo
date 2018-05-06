from poloniex.app import SyncApp
import argparse
from polo.model import Trade,db_session,RestTrade
from datetime import datetime,timedelta
from sqlalchemy import func

def get_dates(start,end=datetime.today()+timedelta(days=1)):
    date_list = []
    while start < end:
        date_list.append(start)
        start = start+timedelta(days=1)
    return date_list

def load_results(results,pair):
    print("Results to upload:" + str(len(results)))
    i = 1
    for result in results:
        print("submitting row " + str(i) + " " + str(result["globalTradeID"]) )
        print("date"+result["date"])
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

def load_paged(app,pair,entry,end=None):
    continue_paging=True
    end_datetime_obj=None
    if end is None:
        end_datetime_obj = entry+timedelta(days=1)-timedelta(seconds=1)
    else:
        end_datetime_obj=end
    while continue_paging==True:
        results = app.public.returnTradeHistory(currency_pair=pair,
                                 start=entry,
                                 end=end_datetime_obj)
        if len(results) > 0:
            load_results(results,pair)

        # check for paging results
        if len(results) == 50000:
            print("len hit 50000")
            continue_paging=True
            entry=datetime.strptime(results[-1]["date"],'%Y-%m-%d %H:%M:%S')+timedelta(seconds=1)
            print("new start:"+ str(entry))
        else:
            #done
            continue_paging=False

def parse_startend(args):
    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)

    pair = args.pair

    start_datetime_obj = datetime.strptime(args.start,"%Y-%m-%d %H:%M:%S")
    end_datetime_obj = datetime.strptime(args.end,"%Y-%m-%d %H:%M:%S")
    dates = get_dates(start_datetime_obj,end_datetime_obj)
    dates.append(end_datetime_obj)
    if not args.start:
        raise RuntimeError("missing arg start_date")
    #db_session.query(RestTrade).delete()
    #db_session.commit()
    index_count = len(dates)
    i = 1
    for entry in dates:
        print("starting date: " + str(entry))
        if i==index_count:
            load_paged(app,pair,entry,end_datetime_obj)
        else:
            load_paged(app,pair,entry)

def parse_hist(args):
    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)

    pair = args.pair

    start_datetime_obj = datetime.strptime(args.start,"%Y-%m-%d")
    dates = get_dates(start_datetime_obj)

    if not args.start:
        raise RuntimeError("missing arg start_date")
    #db_session.query(RestTrade).delete()
    #db_session.commit()
    for entry in dates:
        print("starting date: " + str(entry))
        load_paged(app,pair,entry)

def parse_current(args):
    app = SyncApp(api_key=args.api_key,
                  api_sec=args.api_secret)

    pair = args.pair
    start_date = db_session.query(func.max(RestTrade.date)).one() + timedelta(seconds=1)
    dates = get_dates(start_date)
    for entry in dates:
        print("starting datetime: " + str(entry))
        load_paged(app,pair,entry)


def main():
    parser = argparse.ArgumentParser()
    subparser= parser.add_subparsers(help="subcommand help")
    parser.add_argument("--api_key",help="api key", required=True)
    parser.add_argument("--api_secret",help="api secret", required=True)
    parser.add_argument("--pair",help="pair slug", required=True)
    parser_hist = subparser.add_parser("hist",help="run hist")
    parser_hist.add_argument("--start",help="start yyyy-mm-dd")
    parser_hist.set_defaults(func=parse_hist)
    parser_current = subparser.add_parser("current", help="run current")
    parser_current.set_defaults(func=parse_current)
    parser_startend = subparser.add_parser("startend", help="run start end")
    parser_startend.add_argument("--start",help="start yyyy-mm-dd hh:mm:ss")
    parser_startend.add_argument("--end",help="start yyyy-mm-dd hh:mm:ss")

    args = parser.parse_args()
    args.func(args)


if __name__== "__main__":
    #todo(aj) arg for key and sec
    #todo(aj) arg for currency pairs
    main()
