import json
import time
import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(settings.ELASTIC_DATABASE)


def execute_query(query_id):
    query_path = f'{settings.ELASTIC_QUERY_PATH}/query{query_id}.json'
    with open(query_path, 'r') as fq:
        start = time.time()
        # body = {
        #     'query': json.loads(fq.read())
        # }
        result = es.search(
            index=settings.ELASTIC_INDEX,
            body=json.loads(fq.read()))
        delta = round(time.time() - start, 4)
        return {
            'time': f'{delta}s',
            'data': result,
        }
