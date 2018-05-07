#Install Instructions
1. install postgres
2. install python dependency  https://github.com/absortium/poloniex-api
3. create database named polo
4. set environment variable POSTGRES_USER
5. set environment variable POSTGRES_PW
6. run from root folder ```PYTHONPATH=. alembic upgrade head```


#Initial DB Creation Only (not needed)
3. run ```PYTHONPATH=. alembic revision --autogenerate -m "Initial"```
