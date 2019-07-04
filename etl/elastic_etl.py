from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import click
import datetime
import json


def datagen(jsonl):
    with open(jsonl, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            for key, val in data['Fechas'].items():
                try:
                    date = datetime.datetime.strptime(
                        val.split('.')[0],
                        '%Y-%m-%dT%H:%M:%S')
                    data['Fechas'][key] = date
                except (ValueError, AttributeError):
                    pass
            yield {
                'index': 'licitaciones',
                'id': data['CodigoExterno'],
                'body': data,
            }


@click.command()
@click.argument('jsonl')
def elastic_etl(jsonl):
    config = {}
    with open('/src/etl/elasticsearch_config.json', 'r') as json_file:
        config = json.loads(json_file.read())

    es = Elasticsearch('elastic')
    es.indices.delete(index='licitaciones', ignore_unavailable=True)
    es.indices.create(
        index='licitaciones',
        body=config)
    for data in datagen(jsonl):
        es.create(**data)


if __name__ == '__main__':
    elastic_etl()
