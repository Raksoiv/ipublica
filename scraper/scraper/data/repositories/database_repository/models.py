import peewee
from datetime import datetime


db = peewee.SqliteDatabase('ipublica.db')


class DayJob(peewee.Model):
    objective_date = peewee.DateField()

    class Meta:
        database = db


class Bidding(peewee.Model):
    bidding_id = peewee.CharField(max_length=13)
    day_job = peewee.ForeignKeyField(DayJob, backref='biddings')

    class Meta:
        database = db
