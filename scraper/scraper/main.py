import datetime
import logging
import sys

from scraper.bussiness.controllers import MercadoPublicoAPIController
from scraper.data.repositories import APIDataRepository, DatabaseRepository

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    database_repository = DatabaseRepository()
    api_data_repository = APIDataRepository()
    mercado_publico_api_controller = MercadoPublicoAPIController(
        database_repository=database_repository,
        api_data_repository=api_data_repository,
        json_data_respository=None)
    mercado_publico_api_controller.main(datetime.datetime(2020, 2, 25))


if __name__ == '__main__':
    main()
