from datetime import datetime

import peewee

from scraper import settings

db = peewee.SqliteDatabase(settings.DATABASE_URL)


class DayJob(peewee.Model):
    objective_date = peewee.DateField()

    class Meta:
        database = db


class Bidding(peewee.Model):
    bidding_id = peewee.CharField(max_length=13)
    finished = peewee.BooleanField(default=False)
    day_job = peewee.ForeignKeyField(DayJob, backref='biddings')

    class Meta:
        database = db
