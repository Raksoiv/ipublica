from neo4j.v1 import GraphDatabase
import os

NEO4J_BOLT = os.getenv('NEO4J_BOLT')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASS = os.getenv('NEO4J_PASS')

class Neo4jConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_BOLT,
            auth=(NEO4J_USER, NEO4J_PASS))

    def close(self):
        self.driver.close()
