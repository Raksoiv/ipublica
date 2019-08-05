import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'bolt://localhost:7687')
NEO4J_QUERY_PATH = os.path.join(BASE_PATH, 'neo', 'cypher')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', None)
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', None)

ELASTIC_DATABASE = os.getenv('ELASTIC_DATABASE', 'http://localhost:9200')
ELASTIC_QUERY_PATH = os.path.join(BASE_PATH, 'elastic', 'json')
ELASTIC_INDEX = os.getenv('ELASTIC_INDEX', 'licitaciones')
