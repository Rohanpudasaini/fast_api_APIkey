from sqlalchemy.orm import Session
from sqlalchemy import create_engine, URL
from decouple import config

host = config('host')
database = config('database')
user = config('user')
password = config('password')

url = URL.create(
    database=database,
    username=user,
    password=password,
    host=host,
    drivername="postgresql"
)
# print(url)
engine = create_engine(url, echo=True)
session = Session(bind=engine)


