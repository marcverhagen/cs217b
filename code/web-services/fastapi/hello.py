"""

pip install fastapi uvicorn
uvicorn post:app --reload

"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"data": "Hello World"}
