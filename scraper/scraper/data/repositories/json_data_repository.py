import os.path
import json

from scraper.bussiness.interfaces import JsonDataInterface
from scraper import settings


class JsonDataRepository(JsonDataInterface):
    def __init__(self):
        self.base_path = settings.DATA_PATH

    def save_bidding(self, bidding: dict) -> None:
        bidding_id = bidding['codigoExterno']
        filename = os.path.join(
            self.base_path,
            f'{bidding_id}.json')
        with open(filename, 'w') as fo:
            fo.write(json.dumps(bidding))
