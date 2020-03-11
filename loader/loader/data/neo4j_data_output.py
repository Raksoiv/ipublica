from neo4j import GraphDatabase
from loader.bussiness import OutputDataInterface
from loader import settings


class Neo4jDataOutput(OutputDataInterface):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URL,
            auth=settings.NEO4J_AUTH,
            encrypted=False,
        )

    def save(self, data: dict) -> None:
        for node in data['nodes']:
            node_id = node['id']
            node_label = node['label']
            merge_query = f'MERGE (n:{node_label} {{id: \'{node_id}\'}})\nSET'
            for key, value in node.items():
                if key not in ['id', 'label']:
                    merge_query = f'{merge_query} n.{key} = \'{value}\', '
            merge_query = merge_query.strip(', ')
            with self._driver.session() as session:
                session.run(merge_query)
        for rel in data['relations']:
            start_id = rel['start_id']
            start_label = rel['start_label']
            relation = rel['relation']
            end_id = rel['end_id']
            end_label = rel['end_label']
            merge_query = (
                f'MATCH (s:{start_label} {{ id: \'{start_id}\'}}), '
                f'(e:{end_label} {{ id: \'{end_id}\'}})\n'
                f'MERGE (s)-[r:{relation}]->(e)'
            )
            with self._driver.session() as session:
                session.run(merge_query)
