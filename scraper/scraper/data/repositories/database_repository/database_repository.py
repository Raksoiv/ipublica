from scraper.bussiness.interfaces.database_interface import DatabaseInterface
from . import models


class DatabaseRepository(DatabaseInterface):
    def day_scraped(self, objective_day: datetime.datetime) -> bool:
        pass
