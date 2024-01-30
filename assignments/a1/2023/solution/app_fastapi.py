"""
FastAPI interface to spaCy NER

$ curl http:/127.0.0.1:8000
$ curl -X POST -H 'accept: application/json' -H 'Content-Type: application/json' -d@input.json http:/127.0.0.1:8000

"""

from fastapi import FastAPI
from pydantic import BaseModel
import ner

app = FastAPI()


class Item(BaseModel):
	text: str = ''


@app.get('/')
def index():
	content = "Content-Type: text/plain"
	url = "http://127.0.0.1:5000/api"
	return \
		{"description": "Interface to the spaCy entity extractor",
		"usage": 'curl -v -H "%s" -X POST -d@input.txt %s' % (content, url)}

@app.post('/')
def process(item: Item):
	doc = ner.SpacyDocument(item.text)
	markup = doc.get_entities_with_markup()
	return {"input": item.text, "output": markup}

	