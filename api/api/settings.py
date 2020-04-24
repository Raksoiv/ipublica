import os.path
from os import getenv

NEO4J_URL = getenv(
    'NEO4J_URL',
    'bolt://localhost:7687',
)
NEO4J_AUTH = tuple(getenv(
    'NEO4J_AUTH',
    'neo4j,unholster'
).split(','))
ELASTICSEARCH_URL = getenv(
    'ELASTICSEARCH_URL',
    'http://localhost:9200'
)
ELASTICSEARCH_INDICE = getenv(
    'ELASTICSEARCH_INDICE',
    'mercado_publico'
)
