class InputDataInterface:
    def list_data_ids(self) -> list:
        raise NotImplementedError

    def get_data(self, data_id: str) -> dict:
        raise NotImplementedError
