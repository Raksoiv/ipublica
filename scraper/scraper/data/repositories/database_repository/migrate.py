from scraper.data.repositories.database_repository.models import (Bidding,
                                                                  DayJob, db)

db.create_tables([DayJob, Bidding])
