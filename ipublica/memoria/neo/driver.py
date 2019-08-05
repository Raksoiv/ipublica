from py2neo import Graph
import settings
import time

graph = Graph(
    settings.NEO4J_DATABASE,
    auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))


def execute_query(query_id):
    query_path = f'{settings.NEO4J_QUERY_PATH}/query{query_id}.cypher'
    with open(query_path, 'r') as fq:
        start = time.time()
        result = graph.run(fq.read())
        delta = round(time.time() - start, 4)
        return {
            'time': f'{delta}s',
            'data': result.data(),
        }
