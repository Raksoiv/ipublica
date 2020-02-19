from scraper.bussiness.interfaces.database_interface import DatabaseInterface

import datetime
import logging


logger = logging.getLogger(__name__)


class MercadoPublicoAPIController:
    def __init__(
        self,
        database_repository: DatabaseInterface,
        api_data_repository,
        api_parser,
        json_data_respository
    ):
        self.database_repository = database_repository
        self.api_data_repository = api_data_repository
        self.parser = api_parser
        self.json_data_respository = json_data_respository

    def run_day(self, objective_day: datetime.datetime):
        logger.debug(
            f'Day not scraped ({objective_day}), begining fetcher job')
        status_code = None
        while status_code != 200:
            sleep(self.time_until_next_request)
            json, status_code = self.api_data_repository.get_day(objective_day)
        bidding_list = self.parser.parse_day(json)
        self.database_repository.save_day_job(objective_day, bidding_list)

    def run_bidding(self, bidding_id: str):
        logger.debug(f'Obtaining bidding_id: {bidding_id}')
        status_code = None
        while status_code != 200:
            sleep(self.time_until_next_request)
            json, status_code = self.api_data_repository.get_bidding(
                bidding_id)
        bidding = self.parser.parse_bidding(json)
        self.json_data_respository.save_bidding(objective_day, bidding_id)
        self.database_repository.mark_bidding(bidding_id)

    def main(self, objective_day: datetime.datetime):
        logger.info('MercadoPublicoAPIController stating...')
        while objective_day <= datetime.date.today():
            if not self.database_repository.day_scraped(objective_day):
                self.run_day(objective_day)
            logger.debug('Bidding list obtained, stating bidding items fetch')
            for (
                bidding_id in
                self.database_repository.get_pending_bidding_list(
                    objective_day)
            ):
                self.run_bidding(bidding_id)
            objective_day += datetime.timedelta(days=1)
