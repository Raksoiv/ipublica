import peewee
from datetime import datetime

db = peewee.SqliteDatabase('ipublica.db')


class ScraperJob(peewee.Model):
    start_date = peewee.DateField()
    created_ts = peewee.DateTimeField(default=datetime.now())
    finished_ts = peewee.DateTimeField(null=True)

    class Meta:
        database = db


class BiddingList(peewee.Model):
    objective_date = peewee.DateField()
    created_ts = peewee.DateTimeField(default=datetime.now())
    finished_ts = peewee.DateTimeField(null=True)
    scraper_job = peewee.ForeignKeyField(ScraperJob, backref='bidding_lists')

    class Meta:
        database = db


class Bidding(peewee.Model):
    bidding_id = peewee.CharField(max_length=13)
    created_ts = peewee.DateTimeField(default=datetime.now())
    finished_ts = peewee.DateTimeField(null=True)
    bidding_list = peewee.ForeignKeyField(BiddingList, backref='biddings')

    class Meta:
        database = db
