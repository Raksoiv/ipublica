from datetime import date
from time import sleep
from models import Licitacion, Organismo, Unidad, Usuario
import requests
import json
import os

API_TOKEN = os.getenv('API_TOKEN')
API_URL_BASE = os.getenv('API_URL_BASE')


def licitacion_detail(code):
    api_url = f'{API_URL_BASE}licitaciones.json'
    params = {
        'ticket': API_TOKEN,
        'codigo': code,
    }

    response = requests.get(api_url, params)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json['Listado'][0]
    else:
        print(response.text)
        return None


def licitacion_list(d):
    api_url = f'{API_URL_BASE}licitaciones.json'
    params = {
        'fecha': d.strftime('%d%m%Y'),
        'ticket': API_TOKEN,
    }

    response = requests.get(api_url, params)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json['Listado']
    else:
        print(response.text)
        return None


if __name__ == '__main__':
    date_str = input('Ingrese una fecha para extraer (DD/MM/YYY): ')
    day, month, year = map(int, date_str.split('/'))
    lista_licitaciones = licitacion_list(date(year, month, day))
    sleep(2)
    for licitacion in lista_licitaciones:
        detalle_licitacion = licitacion_detail(licitacion['CodigoExterno'])
        licitacion_obj = Licitacion(detalle_licitacion)
        licitacion_obj.save()
        organismo_obj = Organismo(detalle_licitacion['Comprador'])
        organismo_obj.save()
        unidad_obj = Unidad(detalle_licitacion['Comprador'])
        unidad_obj.save(organismo_obj)
        user = Usuario(detalle_licitacion['Comprador'])
        user.save(licitacion_obj, unidad_obj)
        print('Licitacion Creada!')
        sleep(2)
