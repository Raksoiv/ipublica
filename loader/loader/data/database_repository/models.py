import peewee

from loader import settings

db = peewee.SqliteDatabase(settings.DATABASE_URL)


class Item(peewee.Model):
    item_id = peewee.CharField()
    neo4j = peewee.BooleanField(default=False)
    elastic = peewee.BooleanField(default=False)

    class Meta:
        database = db
