import models
import peewee


def main():
    db = peewee.SqliteDatabase('ipublica.db')
    db.connect()
    db.create_tables([
        models.ScraperJob,
        models.BiddingList,
        models.Bidding,
    ])


if __name__ == '__main__':
    main()
