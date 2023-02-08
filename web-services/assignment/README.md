# Assignment 1 - Web Services

There are three parts to this assignment:

1. Create a RESTful API to access spaCy NER
2. Create a Flask webserver to access spacy NER
3. Create a Streamlit application to access spacy NER


### RESTful API

You can do this using Flask or FastAPI.

The API needs to respond to both a GET and a POST request at the same URL:

```bash
$ curl http://127.0.0.1:5000/api
$ curl -H "Content-Type: text/plain" -X POST -d@input.txt http://127.0.0.1:5000/api
```

The GET request should return something informative about the service and the post request should return the result of processing. In both cases what comes back should be JSON.

If you want you can use the code in `ner.py` to access spaCy processing.


### Flask webserver

Create a Flask webserver that provides two pages: one that presents a form that you can use to send a request to spaCy and one that shows the result.

All the user should have to do to access the website is to point a browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

To access spaCy you can again use the code in `ner.py`. In particular, there is a method `get_entities_with_markup()` which returns an XML string. There is also a spreadsheet in `static/css/main.css` which when applied to the XML will give a result that looks like the screenshot below.

<img src="images/ner-result.png" width="600">


### Streamlit

Create a small Streamlit application that you can access at [http://localhost:8501/](http://localhost:8501/). It should show the result of spaCy processing in any way you see fit, but at least it should have a list of the named entities found and one other way to present the result (or anything else that you can get from spaCy.

The goal here is to play around with Streamlit a bit.


### Wat to hand in?

You should hand in a link to a Git repository. That repository will be also used for future assignments. There shuld be a top-level directory `assignment1` which should have a `README.md` file that explains exactly what to do to run your code. This should include:

- The required Python version. Just list what you ran it on, no need to test on other versions of Python. I hope you are all at least on Python 3.8.
- What modules need to be installed.
- How to start the RESTFull API, the Flask webserver and the Streamlit application. It is possible, but not necessary that the API and webserver are tarted with the same command.
- How use the API or what URL to load.


### How will this be graded?

Pretty leniently. It should run of course and it should be easy to use. Clear understandable code is a definitely a plus.


