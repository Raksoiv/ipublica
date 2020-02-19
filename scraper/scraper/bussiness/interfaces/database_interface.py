import datetime


class DatabaseInterface:
    def day_scraped(self, objective_day: datetime.datetime) -> bool:
        raise NotImplementedError

    def save_day_job(
        self,
        objective_day: datetime.datetime,
        bidding_list: list
    ) -> None:
        raise NotImplementedError

    def get_pending_bidding_list(
        self,
        objective_day: datetime.datetime
    ) -> list:
        raise NotImplementedError

    def mark_bidding(self, bidding_id: str) -> None:
        raise NotImplementedError
