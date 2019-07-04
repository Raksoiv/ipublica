import click
import json
import logging
import models
import time


@click.command()
@click.argument('jsonl')
def loaddata(jsonl):
    with open(jsonl, 'r') as jsonl_file:
        logging.info(f'Start reading of file {jsonl}')

        # Init Files
        models.Bidding.init_file()
        models.User.init_file()
        models.Unit.init_file()
        models.Organism.init_file()
        models.Product.init_file()
        models.Provider.init_file()

        # Init id_buffers
        bidding_buf = []
        user_buf = []
        unit_buf = []
        organism_buf = []
        product_buf = []
        provider_buf = []
        user_bidding_buf = []
        user_unit_buf = []
        unit_organism_buf = []
        bidding_product_buf = []
        provider_bidding_buf = []

        lines_readed = 0
        start = time.time()
        iteration = time.time()
        for line in jsonl_file:
            if lines_readed % 100 == 0:
                end = time.time()
                logging.info(f'Number of lines readed: {lines_readed}')
                logging.info(f'Seconds in the iteration: {round(end - iteration)}')
                logging.info(f'Total seconds elapsed: {round(end - start)}')
                iteration = time.time()
            line = line.replace(
                '\\n', '').replace(
                '\\r', '').replace(
                '\\t', '')
            # Create Base Objects
            data = json.loads(line)
            bidding = models.Bidding(data)
            user = models.User(data)
            unit = models.Unit(data)
            organism = models.Organism(data)
            products = [models.Product(p) for p in data['Items']['Listado']]
            providers = []
            providers_data = []
            for p in data['Items']['Listado']:
                if p['Adjudicacion']:
                    providers.append(models.Provider(p['Adjudicacion']))
                    providers_data.append([
                        p['CodigoProducto'],
                        p['Adjudicacion']['Cantidad'],
                        p['Adjudicacion']['MontoUnitario'],
                    ])

            # Save objects
            bidding.save(bidding_buf)
            user.save(user_buf)
            unit.save(unit_buf)
            organism.save(organism_buf)
            [p.save(product_buf) for p in products]
            [p.save(provider_buf) for p in providers]

            # Save Relations
            user.save_relation(bidding, user_bidding_buf)
            user.save_relation(unit, user_unit_buf)
            unit.save_relation(organism, unit_organism_buf)
            [bidding.save_relation(p, bidding_product_buf) for p in products]
            for p, pd in zip(providers, providers_data):
                p.save_relation(bidding, provider_bidding_buf, pd)

            lines_readed += 1


if __name__ == '__main__':
    loaddata()
