import datetime


class JsonDataInterface:
    def save_bidding(self, bidding_id: dict) -> None:
        raise NotImplementedError
