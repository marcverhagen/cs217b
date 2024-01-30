"""app.py

Simple Web interface and API to spaCy entity recognition.

Usage via the API (on the local host):

$ curl http://127.0.0.1:5000/api
$ curl -H "Content-Type: text/plain" -X POST -d@input.txt http://127.0.0.1:5000/api

For the web pages point your browser at http://127.0.0.1:5000

"""


from flask import Flask, request, render_template
from flask_restful import Resource, Api

import ner

app = Flask(__name__)
api = Api(app)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        doc = ner.SpacyDocument(text)
        markup = doc.get_entities_with_markup()
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        return render_template('result.html', markup=markup_paragraphed)

# alternative where we use two resources

@app.get('/get')
def index_get():
    return render_template('form2.html', input=open('input.txt').read())

@app.post('/post')
def index_post():
    text = request.form['text']
    doc = ner.SpacyDocument(text)
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    return render_template('result2.html', markup=markup_paragraphed)


# But for the API we use the RESTful extension and return JSON.

class EntityParserAPI(Resource):

    def get(self):
        # curl http://127.0.0.1:5000/api
        content = "Content-Type: text/plain"
        url = 'http://127.0.0.1:5000/api'
        return \
            {"description": "Interface to the spaCy entity extractor",
             "usage": 'curl -v -H "%s" -X POST -d@input.txt %s' % (content, url)}

    def post(self):
        # curl -d@input.txt http://127.0.0.1:5000/api
        text = request.get_data(as_text=True)
        doc = ner.SpacyDocument(text)
        markup = doc.get_entities_with_markup()
        return {"input": text,
                "output": markup}, 200


api.add_resource(EntityParserAPI, "/api")


if __name__ == '__main__':

    app.run(debug=True)
