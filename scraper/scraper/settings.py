import os.path
from os import getenv

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = getenv('DATA_PATH', os.path.join(BASE_PATH, 'data'))

DATABASE_URL = getenv('DATABASE_URL', os.path.join(
    BASE_PATH,
    'data',
    'ipublica.db'))
