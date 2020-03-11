from loader.data.database_repository.models import Item, db

db.create_tables((Item, ))
