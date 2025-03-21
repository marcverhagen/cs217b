# FastAPI

This directory may exhausts all the FastAPI that you need for this course.


## Getting started

Mostly taken from [https://refine.dev/blog/introduction-to-fast-api/#introduction](https://refine.dev/blog/introduction-to-fast-api/#introduction).

Installation:

```bash
$ pip install fastapi uvicorn
```

Simple file (named `main.py`):

```python
from fastapi import FastAPI

fastapi = FastAPI()

@fastapi.get("/")
async def home():
    return {"data": "Hello World"}
```

Running:

```bash
$ uvicorn main:app --reload
```


## More

With [get.py](get.py) we already get some very bare-bones type checking. When you run it (with `uvicorn main:app --reload`) you will notice that the type hints are actually doing more than documenting the code:

- [http://127.0.0.1:8000/repeat/2](http://127.0.0.1:8000/repeat/2)
- [http://127.0.0.1:8000/repeat/two](http://127.0.0.1:8000/repeat/two)

The second one will fail.

Also, I had a brain fart in class when I said that the `double` parameter in `repeat()` is ignored. Wrong, you can access it with [http://127.0.0.1:8000/repeat/12?double=True](http://127.0.0.1:8000/repeat/12?double=True).

And in [post.py](post.py) we take that one step further by using the pydantic library. With that FastAPI performs meaningful type checks on the JSON that you hand into a post request. Try some of the Curl POST requests from a terminal and notice how some of them will fail.

For both APIs you can get the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
