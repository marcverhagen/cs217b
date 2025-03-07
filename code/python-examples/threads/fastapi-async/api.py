import time

from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def index():
    time.sleep(2)
    return "done"

@api.get("/async")
async def async_index():
    time.sleep(2)
    return "done"
