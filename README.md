#Install Instructions
1. install postgres
2. install python dependency  https://github.com/absortium/poloniex-api
using ```python setup.py install```
3. create database named polo
4. set environment variable POSTGRES_USER
5. set environment variable POSTGRES_PW
6. run from root folder ```PYTHONPATH=. alembic upgrade head```
7. install package ```python setup.py install```


#Usage:
1. polo_history - gathers historical info for market or multiple markets
2. polo_websocket - reads poloniex websocket updates trades to db and maintains orderbook 
for a market or markets.

#Initial DB Creation Only (not needed)
3. run ```PYTHONPATH=. alembic revision --autogenerate -m "Initial"```
