# FastAPI

This directory may exhaust all the FastAPI that you need for this course.

Some of the following examples and prose were taken from [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/) and [https://refine.dev/blog/introduction-to-fast-api/](https://refine.dev/blog/introduction-to-fast-api/#introduction).


## Getting started

Installation:

```bash
$ pip install fastapi uvicorn
```

Create a simple file named `hello.py` with the following content:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"data": "Hello World"}
```

Start the FastAPI server from the directory that contains the script with:

```bash
$ uvicorn hello:app --reload
```

Then access the server at [http:/127.0.0.1:8000](http:/127.0.0.1:8000).


## GET and POST examples

In [get.py](get.py) there are some examples of using path parameters and query parameters. When you run it with `uvicorn get:app --reload` you will notice that for FastAPI the type hints are doing more than documenting the code.

Try these URLs:

- [http://127.0.0.1:8000/repeat/2](http://127.0.0.1:8000/repeat/2)
- [http://127.0.0.1:8000/repeat/two](http://127.0.0.1:8000/repeat/two)

Or alternatively these curl commands from a terminal:

```bash
curl http://127.0.0.1:8000/repeat/2
curl http://127.0.0.1:8000/repeat/two
```
The second request will fail. This is because under the hood the Pydantic data valication library is used and the definition of the resource requires that the count variable is an integer.

```python
@app.get("/repeat/{count}")
def repeat(count: int, double: bool = False):
    return again(count, double)
```

In [post.py](post.py) we take that one step further by using the Pydantic library explicitly. With that FastAPI performs type checks on the JSON object that you hand in to a post request.

For both APIs you can get the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). This UI can be very helpful especially when getting an idea on how to create the body to be sent via a POST request.
