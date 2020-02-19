import datetime


class JsonDataInterface:
    def save_bidding(
        objective_day: datetime.datetime, bidding_id: dict
    ) -> None:
        raise NotImplementedError
