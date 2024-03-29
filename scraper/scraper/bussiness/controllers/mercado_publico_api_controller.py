import datetime
import logging
from time import sleep

from scraper.bussiness.interfaces.api_data_interface import APIDataInterface
from scraper.bussiness.interfaces.database_interface import DatabaseInterface
from scraper.bussiness.interfaces.json_data_interface import JsonDataInterface
from scraper.bussiness.parsers.api_parser import APIParser

logger = logging.getLogger(__name__)


class MercadoPublicoAPIController:
    def __init__(
        self,
        database_repository: DatabaseInterface,
        api_data_repository: APIDataInterface,
        json_data_respository: JsonDataInterface,
    ):
        self.database_repository = database_repository
        self.api_data_repository = api_data_repository
        self.parser = APIParser()
        self.json_data_respository = json_data_respository
        self.time_until_next_request = 5.0

    def run_day(self, objective_day: datetime.datetime):
        logger.debug(
            f'Day not scraped ({objective_day}), begining fetcher job')
        bidding_list = None
        while bidding_list is None:
            sleep(self.time_until_next_request)
            status_code, json = self.api_data_repository.get_day(objective_day)
            logger.debug(f'status_code: {status_code}')
            if status_code == 200:
                bidding_list = self.parser.parse_day(json)
        self.database_repository.save_day_job(objective_day, bidding_list)

    def run_bidding(self, bidding_id: str):
        logger.debug(f'Obtaining bidding_id: {bidding_id}')
        bidding = None
        while bidding is None:
            sleep(self.time_until_next_request)
            status_code, json = self.api_data_repository.get_bidding(
                bidding_id)
            logger.debug(f'status_code: {status_code}')
            if status_code == 200:
                bidding = self.parser.parse_bidding(json)
        self.json_data_respository.save_bidding(bidding)
        self.database_repository.mark_bidding(bidding_id)

    def main(self, objective_day: datetime.datetime):
        logger.info('MercadoPublicoAPIController stating...')
        while objective_day <= datetime.datetime.today():
            if not self.database_repository.day_scraped(objective_day):
                self.run_day(objective_day)
            logger.debug('Bidding list obtained, stating bidding items fetch')
            for bidding_id in (
                self.database_repository.get_pending_bidding_list(
                    objective_day)
            ):
                self.run_bidding(bidding_id)
            objective_day += datetime.timedelta(days=1)
