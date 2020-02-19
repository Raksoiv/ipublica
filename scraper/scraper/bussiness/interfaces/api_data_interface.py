import datetime


class APIDataInterface:
    def get_day(objective_day: datetime.datetime) -> tuple:
        raise NotImplementedError

    def get_bidding(bidding_id: str) -> dict:
        raise NotImplementedError
