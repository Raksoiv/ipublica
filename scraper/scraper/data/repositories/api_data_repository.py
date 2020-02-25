import requests
import datetime

from scraper.bussiness.interfaces import APIDataInterface


class APIDataRepository(APIDataInterface):
    def __init__(self):
        host = 'http://api.mercadopublico.cl'
        uri = '/servicios/v1/publico/licitaciones.json'
        self.API_URL = f'{host}{uri}'
        self.API_TOKEN = 'C3BF85EC-610C-4781-B79D-AC7AB0900743'

    def request_api(self, params={}):
        params['ticket'] = self.API_TOKEN
        response = requests.get(self.API_URL, params)

        return response.status_code, response.text

    def get_day(self, objective_day: datetime.datetime) -> tuple:
        params = {
            'fecha': objective_day.strftime('%d%m%Y'),
        }

        return self.request_api(params)

    def get_bidding(self, bidding_id: str) -> dict:
        params = {
            'codigo': bidding_id,
        }

        return self.request_api(params)
