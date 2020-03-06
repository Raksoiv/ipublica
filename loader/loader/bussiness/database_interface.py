class DatabaseInterface:
    def check_false(self, data_id: str, column: str):
        raise NotImplementedError

    def mark_true(self, data_id: str, column: str):
        raise NotImplementedError
