"""

pip install fastapi uvicorn
uvicorn get:app --reload

http://127.0.0.1:8000
http://127.0.0.1:8000/repeat/12
http://127.0.0.1:8000/repeat/12?double=True
http://127.0.0.1:8000/repeat/twelve
http://127.0.0.1:8000/iterate?count=2
http://127.0.0.1:8000/iterate?count=2&double=true
http://127.0.0.1:8000/docs

"""

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def howdy():
    """Return a basic Howdy message."""
    return {"message": "Howdy"}

@app.get("/repeat/{count}")
def repeat(count: int, double: bool = False):
    """Repeat "Howdy" a number of times, doubling the total if requested."""
    return again(count, double)

@app.get("/iterate")
def iterate(count: int, double: bool = False):
    return again(count, double)

def again(count: int, double: bool = False):
    result = 'Howdy' * count
    if double:
        result *= 2
    return {"result": result}
