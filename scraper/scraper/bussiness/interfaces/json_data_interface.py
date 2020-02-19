import datetime


class JsonDataInterface:
    def save_bidding(bidding_id: dict) -> None:
        raise NotImplementedError
