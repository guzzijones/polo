from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey,Boolean,Float,DateTime
from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker
import sys
import os
user = os.environ["POSTGRES_USER"]
password = os.environ['POSTGRES_PW']

db_engine = create_engine("postgresql+psycopg2://{user}:{pw}@localhost:5432/polo".format(user=user,pw=password))
Base = declarative_base()


class RestTrade(Base):
    __tablename__ = 'rest_trade'
    globalTradeID = Column(Integer,primary_key=True)
    book = Column(String(length=10))
    tradeID = Column(Integer)
    date = Column(DateTime)
    type=Column(String(length=5))
    rate=Column(Float)
    amount=Column(Float)
    total=Column(Float)


class Trade(Base):
    __tablename__ = 'trade'
    cur_id = Column(Integer)
    id = Column(Integer)
    book= Column(String(length=1))
    type = Column(Boolean)
    price = Column(Float)
    quantity = Column(Float)
    active = Column(Boolean)

session_maker = sessionmaker(bind=db_engine)
db_session = session_maker()

#Base.metadata.create_all(db)
