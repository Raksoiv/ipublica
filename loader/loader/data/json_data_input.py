import os
import json

from loader.bussiness import InputDataInterface
from loader import settings


class JsonDataInput(InputDataInterface):
    def __init__(self):
        self.scraper_data_path = settings.SCRAPER_DATA_PATH

    def list_data_ids(self) -> list:
        return list(map(
            lambda name: '.'.join(name.split('.')[:-1]),
            filter(
                lambda f: True if 'scraper' not in f else False,
                os.listdir(self.scraper_data_path)
            )
        ))

    def get_data(self, data_id: str) -> dict:
        filename = os.path.join(self.scraper_data_path, f'{data_id}.json')
        with open(filename, 'r') as fi:
            data = json.loads(fi.read())
        return data
