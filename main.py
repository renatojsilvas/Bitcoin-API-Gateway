from typing import Optional

from fastapi import FastAPI

from exchanges.walltime import Walltime
from models import Information
from repositories.walltime import WalltimeRepository

from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/general")
def read_root(response_model=Information):
    exchange = Walltime(WalltimeRepository())
    teste = exchange.get_general_info()
    return jsonable_encoder(teste)


@app.get("/bookorder")
def read_item():
    exchange = Walltime(WalltimeRepository())
    teste = exchange.get_book_order()
    return jsonable_encoder(teste)
