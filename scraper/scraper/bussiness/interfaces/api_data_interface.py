import datetime


class APIDataInterface:
    def get_day(self, objective_day: datetime.datetime) -> tuple:
        raise NotImplementedError

    def get_bidding(self, bidding_id: str) -> dict:
        raise NotImplementedError
