from loader.bussiness import MercadoPublicoController
from loader.data import JsonDataInput
from loader.data import DatabaseRepository
from loader.data import Neo4jDataOutput


def main():
    json_data_input = JsonDataInput()
    database_repository = DatabaseRepository()
    neo4j_data_output = Neo4jDataOutput()
    mp_controller = MercadoPublicoController(
        input=json_data_input,
        neo4j=neo4j_data_output,
        elastic=None,
        database=database_repository,
    )
    mp_controller.main()


if __name__ == '__main__':
    main()
