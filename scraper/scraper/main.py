from scraper.bussiness.controllers import MercadoPublicoAPIController
from scraper.data.repositories.database_repository import DatabaseRepository

def main():
    database_repository = DatabaseRepository()
    mercado_publico_api_controller = MercadoPublicoAPIController(database_repository=database_repository)

if __name__ == '__main__':
    main()
