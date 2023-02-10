from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def howdy():
    return {"message": "Howdy"}

@app.get("/repeat/{count}")
def repeat(count: int, double: bool = False):
    return again(count, double)

@app.get("/iterate")
def iterate(count: int, double: bool = False):
    return again(count, double)

def again(count: int, double: bool = False):
    result = 'Howdy' * count
    if double:
        result *= 2
    return {"result": result}
