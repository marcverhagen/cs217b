# Assignment 1 example solution

The code assumes that version 3.7 or higher of Python is installed.

Requirements for running all examples

```bash
$ pip install spacy 
$ python -m spacy download en_core_web_sm
$ pip install flask flask_restful
$ pip install fastapi uvicorn
$ pip install streamlit
```

The first two lines are for all applications, the third for `app.py`, the fourth for `app_fastapi.py` and the fifth for `app_streamlit.py`.


### Flask server and API

To run the Flask code, which includes both the web server and the API:

```bash
$ python app.py
```

Accessing the API:

```bash
$ curl http://127.0.0.1:5000/api
$ curl -H "Content-Type: text/plain" -X POST -d@input.txt http://127.0.0.1:5000/api
```

To access the website point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000). In `app.py` there are two ways to implement the server, one with a single resource `'/'` and one with two resources: `/get` and `/post`. This is to illustrate how the HTML form accesses the resource.


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


### Streamlit

To run:

```bash
$ streamlit run app_streamlit.py
```

