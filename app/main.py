from typing import Union
from config.mongodb import mongo_test_connection
from fastapi import FastAPI

app = FastAPI()
mongo_test_connection()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}