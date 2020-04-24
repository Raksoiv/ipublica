import time

from flask import Flask
from flask_restful import Resource, Api

from api.data.neo4j_repository import Neo4jRepository

neo4j_repo = Neo4jRepository()


#
# NEO4J Resources
#
class Top5OrganizationsByUnitAmount(Resource):
    '''
    Top 5 de los organismos ordenados por precio unitario
    algoritmo complementamente dentro de Neo4j
    '''
    def get(self):
        start_t = time.time()
        result = neo4j_repo.top5_organizations_by_amount()
        elapsed_t = time.time() - start_t
        return {
            'took': f'{round(elapsed_t, 4)} s',
            'result': result,
        }


class Top5ProvidersByUnitAmount(Resource):
    '''
    Top 5 de los proveedores ordenados por precio unitario
    algoritmo complementamente dentro de Neo4j
    '''
    def get(self):
        start_t = time.time()
        result = neo4j_repo.top5_providers_by_amount()
        elapsed_t = time.time() - start_t
        return {
            'took': f'{round(elapsed_t, 4)} s',
            'result': result,
        }


class Top5OrganismProviderRelations(Resource):
    '''
    Top 5 del conjunto de organismos y proveedores cuya conexión
    esta marcada por una suma de sus transacciones unitarias
    algoritmo Neo4j
    '''
    def get(self):
        start_t = time.time()
        result = neo4j_repo.top5_organism_provider_relations()
        elapsed_t = time.time() - start_t
        return {
            'took': f'{round(elapsed_t, 4)} s',
            'result': result,
        }


#
# Server Class
#
class APIServer:
    def __init__(self):
        pass

    def start_server(self):
        app.run(debug=True)


# Basic app configuration
app = Flask(__name__)
api = Api(app)

# Resource register
api.add_resource(
    Top5OrganizationsByUnitAmount,
    '/neo4j/1`'
)

api.add_resource(
    Top5ProvidersByUnitAmount,
    '/neo4j/2'
)

api.add_resource(
    Top5OrganismProviderRelations,
    '/neo4j/3'
)
