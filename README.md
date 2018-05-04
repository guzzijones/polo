#Install Instructions
1. install postgres
2. install python dependency  https://github.com/absortium/poloniex-api
2. create database named polo
3. run from root folder ```PYTHONPATH=. alembic upgrade head```


#Initial DB Creation Only
3. run ```PYTHONPATH=. alembic revision --autogenerate -m "Initial"```
