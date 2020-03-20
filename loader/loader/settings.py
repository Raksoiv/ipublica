import os.path
from os import getenv

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = getenv('DATA_PATH', os.path.join(BASE_PATH, 'data'))
SCRAPER_DATA_PATH = getenv(
    'SCRAPER_DATA_PATH',
    os.path.join(BASE_PATH, 'scraper_data')
)
DATABASE_URL = getenv(
    'DATABASE_URL',
    os.path.join(BASE_PATH, 'data', 'loader.db')
)
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
