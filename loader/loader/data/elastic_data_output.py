from elasticsearch import Elasticsearch
from loader.bussiness import OutputDataInterface
from loader import settings


class ElasticDataOutput(OutputDataInterface):
    def __init__(self):
        self._driver = Elasticsearch(settings.ELASTICSEARCH_URL)
        self._indice = settings.ELASTICSEARCH_INDICE

        if not self._driver.indices.exists(self._indice):
            self._driver.indices.create(self._indice)

    def save(self, data: dict) -> None:
        self._driver.index(self._indice, data)
