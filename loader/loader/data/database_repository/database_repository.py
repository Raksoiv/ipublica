from loader.bussiness import DatabaseInterface
from loader.data.database_repository.models import Item


class DatabaseRepository(DatabaseInterface):
    def check_false(self, data_id: str, column: str) -> bool:
        return (
            not
            Item.select()
            .where(Item.item_id == data_id)
            .where(getattr(Item, column) == 1)
            .exists()
        )

    def mark_true(self, data_id: str, column: str) -> None:
        data_id_exists = (
            Item.select()
            .where(Item.item_id == data_id)
            .exists()
        )
        if data_id_exists:
            q = (
                Item.update({column: True})
                .where(Item.item_id == data_id)
            )
            q.execute()
        else:
            Item.create(**{'item_id': data_id, column: True})
