from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import os

user = os.environ["USER"]
password = os.environ["PASSWORD"]
host = os.environ["HOST"]
port = os.environ["PORT"]
database = os.environ["DATABASE"]

MYSQL = {
    "engine": "mysql",
    "username": user,
    "password": password,
    "host": host,
    "port": port,
    "db_name": database,
}

con = "{engine}://{username}:{password}@{host}:{port}/{db_name}".format(**MYSQL)

engine = create_engine(con)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]
