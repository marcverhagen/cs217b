"""

pip install fastapi uvicorn
uvicorn post:app --reload

"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    action: str = 'bounce'
    body: str

@app.get("/")
def synopsis():
    return {"message": "bounces or processes a message body"}

@app.post("/")
def process(item: Item):
    if item.action == 'bounce':
        return {"bouncing": item.body}
    else:
        return {"processing": item.body}

@app.post("/repeat")
def repeat(count: int, item: Item):
    return {"result": item.body * count}


'''

curl http://127.0.0.1:8000/


curl -X 'POST' 'http://127.0.0.1:8000/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{ "body": "hoppa" }'

curl 'http://127.0.0.1:8000/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{ "body": "hoppa" }'

curl -X 'POST' 'http://127.0.0.1:8000/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{ "body": "hoppa", "action": "stop" }'


curl -X 'POST' \
  'http://127.0.0.1:8000/repeat?count=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "action": "bounce", "body": "string" }'

curl -X 'POST' \
  'http://127.0.0.1:8000/repeat?count=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @item.json

curl -X 'POST' \
  'http://127.0.0.1:8000/repeat?count=iii' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @item.json

curl -X 'POST' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @item.json

'''
