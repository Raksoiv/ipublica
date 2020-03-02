import datetime
import logging
import sys

from scraper.bussiness.controllers import MercadoPublicoAPIController
from scraper.data.repositories import (APIDataRepository, DatabaseRepository,
                                       JsonDataRepository)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    database_repository = DatabaseRepository()
    api_data_repository = APIDataRepository()
    json_data_respository = JsonDataRepository()
    mercado_publico_api_controller = MercadoPublicoAPIController(
        database_repository=database_repository,
        api_data_repository=api_data_repository,
        json_data_respository=json_data_respository,)
    mercado_publico_api_controller.main(datetime.datetime(2019, 1, 1))


if __name__ == '__main__':
    main()
