import json, time
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers.errors import BulkIndexError


CERTIFICATE = '/Applications/ADDED/search/elasticsearch-8.7.0/config/certs/http_ca.crt'
ES_PASSWORD = '*HSDisuvIddkAwI+4Gry'
#ES_PASSWORD = 'tKLpVnCS5a+zNa37SS7Z'


ES = Elasticsearch(
        "https://127.0.0.1:9200",
        ca_certs=CERTIFICATE,
        http_auth=("elastic", ES_PASSWORD))


entities = [
    {"name": "jane doe", "age": 26, "interests": ["rap music"]},
    {"name": "judy doe", "age": 27, "interests": ["rap", "music"]},
    {"name": "june doe", "age": 65, "hobbies": ["forestry"]},
    {"name": "jill doe", "age": 28, "hobbies": None},
    {"name": "jill doe", "age": 29, "hobbies": 20},
    {"name": {"first": "june", "last": "doe"}, "age": 65} ]


def load_entities(index_name: str):
    for i, entity in enumerate(entities):
        try:
            ES.index(index=index_name, id=i, document=entity)
        except Exception as e:
            print(f'Warning: error loading {entity}')
            print(e)

def print_entities(index_name: str):
    query = {'match_all': {}}
    result = ES.search(index=index_name, query=query)
    print()
    for hit in result['hits']['hits']:
        print(hit['_id'], hit['_source'])

def docs(index_name: str, file_name: str):
    with open(file_name) as fh:
        for line in fh:
            doc = {"_index": index_name, "_source": json.loads(line) }
            yield doc

def bulk_load_entities(index_name: str, file_name: str):
    try:
        helpers.bulk(ES, docs(index_name, file_name))
    except BulkIndexError as e:
        print(e)

def delete_index(name: str):
    ES.indices.delete(index=name, ignore=[400, 404])


if __name__ == '__main__':

    if False:
        print('\n>>> loading entities')
        delete_index('entities1')
        load_entities('entities1')
        time.sleep(1)
        print_entities('entities1')

    if True:
        print('\n>>> bulk loading entities')
        delete_index('entities2')
        bulk_load_entities('entities2', 'entities.json')
        time.sleep(1)
        print_entities('entities2')
