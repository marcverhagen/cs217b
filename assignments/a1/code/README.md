# Assignment 1 starter code

The code assumes Python version 3.8 or higher.


### FastAPI

To run:

```bash
$ uvicorn app_fastapi:app --reload
```

Accessing the API:

```bash
$ curl http:/127.0.0.1:8000
$ curl -X POST http:/127.0.0.1:8000 \
       -H 'accept: application/json' \
       -H 'Content-Type: application/json' \
       -d@input.json 
```

### Flask server

To run:

```bash
$ python app_flask.py
```

To access the website point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000). In `app_flask.py` there are two ways to implement the server, one with a single resource `'/'` and one with two resources: `/get` and `/post`. This is to illustrate how the HTML form accesses the resource.


### Streamlit

To run:

```bash
$ streamlit run app_streamlit.py
```
