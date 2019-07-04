import os
import logging

#  LOG LEVEL
logging.basicConfig(level=logging.DEBUG)

# ETL Base Path
BASE_ETL_PATH = os.getenv('BASE_PATH', '/src/data/etl/')
