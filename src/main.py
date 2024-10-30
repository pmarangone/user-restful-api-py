from fastapi import FastAPI
from sqlmodel import Field, SQLModel
from src.db import create_db_and_tables
from .routes import user


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


app = FastAPI()
app.include_router(user.router)
# app.include_router(event.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"v0.1"}


# @app.post("/reset")
# def reset():
#     db_wrapper.db.reset()
#     return response.OK()
