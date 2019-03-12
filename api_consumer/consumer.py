from requests import get
from time import sleep
import datetime
import json
import models
import settings
import sys


def request_api(fecha=None, codigo=None):
    params = {
        'ticket': settings.API_TOKEN
    }
    if fecha:
        params['fecha'] = fecha.strftime('%d%m%Y')
    elif codigo:
        params['codigo'] = codigo

    sleep(settings.TIME_UNTIL_NEXT_REQUEST)
    response = get(settings.API_URL, params)

    if response.status_code != 200:
        return None
    else:
        return response


def parse_bidding_list(response, bidding_list):
    try:
        json_response = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return False
    json_bidding_list = json_response['Listado']
    for json_bidding in json_bidding_list:
        bidding, _ = models.Bidding.get_or_create(
            bidding_id=json_bidding['CodigoExterno'],
            bidding_list=bidding_list)
    bidding_list.finished_ts = datetime.datetime.now()
    bidding_list.save()
    return True


def parse_bidding(response, bidding):
    try:
        json_response = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return None
    if json_response['Cantidad'] > 0:
        json_bidding = json_response['Listado'][0]
    else:
        json_bidding = {}
    bidding.finished_ts = datetime.datetime.now()
    bidding.save()
    return json_bidding


def main(start_date):
    scraper_job, created = models.ScraperJob.get_or_create(
        start_date=start_date)

    filename = (
        f'{settings.DATA_PATH}'
        f'licitaciones_{scraper_job.id}.jsonl')
    if created:
        # Create the output file
        fo = open(filename, 'w')
        fo.close()

    print(scraper_job.id, scraper_job.start_date)
    today = datetime.date.today()
    objective_date = start_date
    while objective_date <= today:
        bidding_list, _ = models.BiddingList.get_or_create(
            objective_date=objective_date,
            scraper_job=scraper_job)
        print(bidding_list.id, bidding_list.objective_date)

        # Check if the bidding list is already fetched
        if bidding_list.finished_ts:
            objective_date += datetime.timedelta(days=1)
        else:
            response = request_api(fecha=objective_date)
            if response and parse_bidding_list(response, bidding_list):
                objective_date += datetime.timedelta(days=1)

        biddings = bidding_list.biddings
        i = 0
        while i < len(biddings):
            print(biddings[i].bidding_id)
            if biddings[i].finished_ts:
                i += 1
                continue
            response = request_api(codigo=biddings[i].bidding_id)
            if not response:
                continue
            json_bidding = parse_bidding(response, biddings[i])
            if json_bidding is not None:
                if json_bidding != {}:
                    with open(filename, 'a') as fo:
                        fo.write(json.dumps(json_bidding))
                        fo.write('\n')
                i += 1


if __name__ == '__main__':
    try:
        start_date = datetime.date(
            *map(int, sys.argv[1].split('-')))
    except IndexError:
        print('1 Argument needed date: YYYY-MM-DD')
        exit(1)
    except (ValueError, TypeError):
        print('Sintax Error on the date argument, iso needed: YYYY-MM-DD')
        exit(1)
    main(start_date)
