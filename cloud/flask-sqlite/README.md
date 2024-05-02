# A simple database backed Flask applicaiton

Requirements:

```bash
$ pip install spacy flask flask-sqlalchemy
$ python -m spacy download en_core_web_sm
```

To run the code:

```bash
$ python app.py
```

To access the website point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

Building the Docker image:

```bash
$ docker build -t ner .
```

Starting a container:

```bash
$ docker run --rm -d -p 5000:5000 -v ${PWD}/instance:/app/instance --name ner ner
```

Access to the website is as before.
