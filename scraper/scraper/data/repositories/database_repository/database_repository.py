import datetime

from scraper.bussiness.interfaces import DatabaseInterface

from . import models


class DatabaseRepository(DatabaseInterface):
    def day_scraped(self, objective_day: datetime.datetime) -> bool:
        query = models.DayJob.select().where(
            models.DayJob.objective_date == objective_day)
        if query.exists():
            return True
        return False

    def save_day_job(
        self,
        objective_day: datetime.datetime,
        bidding_list: list
    ) -> None:
        day_job = models.DayJob.create(objective_date=objective_day)
        for bidding_id in bidding_list:
            models.Bidding.create(bidding_id=bidding_id, day_job=day_job)

    def get_pending_bidding_list(
        self,
        objective_day: datetime.datetime
    ) -> list:
        day_job = models.DayJob.select().where(
            models.DayJob.objective_date == objective_day)
        return [
            bidding.bidding_id
            for bidding in
            models.Bidding.select().where(
                models.Bidding.day_job == day_job).where(
                    models.Bidding.finished == 0)
        ]

    def mark_bidding(self, bidding_id: str) -> None:
        bidding = models.Bidding.get(models.Bidding.bidding_id == bidding_id)
        bidding.finished = True
        bidding.save()
