import time

from loader.bussiness.input_data_interface import InputDataInterface
from loader.bussiness.output_data_interface import OutputDataInterface
from loader.bussiness.database_interface import DatabaseInterface


class MercadoPublicoController:
    def __init__(
        self,
        input_data: InputDataInterface,
        neo4j: OutputDataInterface,
        elastic: OutputDataInterface,
        database: DatabaseInterface,
    ):
        self.input_data = input_data
        self.neo4j = neo4j
        self.elastic = elastic
        self.database = database

    def send_neo4j(self, data_id: str):
        if self.database.check_false(data_id, 'neo4j'):
            neo4j_data = data_id  # Process data id to get neo4j base
            self.neo4j.save(neo4j_data)
            self.database.mark_true(data_id, 'neo4j')

    def send_elastic(self, data_id: str):
        if self.database.check_false(data_id, 'elastic'):
            elastic_doc = data_id  # Process data id to get elastic doc
            self.elastic.save(elastic_doc)
            self.database.mark_true(data_id, 'elastic')

    def main(self):
        while True:
            for data_id in self.input_data.list_data_ids():
                self.send_neo4j(data_id)
                self.send_elastic(data_id)
            time.sleep(30 * 60)
