from loader.bussiness import MercadoPublicoController
from loader.data import JsonDataInput
from loader.data import DatabaseRepository
from loader.data import Neo4jDataOutput
from loader.data import ElasticDataOutput


def main():
    json_data_input = JsonDataInput()
    database_repository = DatabaseRepository()
    neo4j_data_output = Neo4jDataOutput()
    elastic_data_output = ElasticDataOutput()
    mp_controller = MercadoPublicoController(
        input=json_data_input,
        neo4j=neo4j_data_output,
        elastic=elastic_data_output,
        database=database_repository,
    )
    mp_controller.main()


if __name__ == '__main__':
    main()
