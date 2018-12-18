#!/usr/bin/env python3

import json
import sys
import argparse
import time
import requests
import singer
import backoff

from datetime import date, datetime, timedelta

REQUIRED_CONFIG_KEYS = [
    "access_key",
]

base_url = 'https://api.darksky.net/forecast/'

logger = singer.get_logger()
session = requests.Session()
DATE_FORMAT='%Y-%m-%d'

def parse_response(r):
    flattened = r['daily']['data'][0]
    return flattened

schema = {'type': 'object',
          'properties':
          {'date': {'type': 'string',
                    'format': 'date-time'}},
          'additionalProperties': True}

def giveup(error):
    logger.error(error.response.text)
    response = error.response
    return not (response.status_code == 429 or
                response.status_code >= 500)

@backoff.on_exception(backoff.constant,
                      (requests.exceptions.RequestException),
                      jitter=backoff.random_jitter,
                      max_tries=5,
                      giveup=giveup,
                      interval=30)
def request(url, params):
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return response

def do_sync(lat_long, start_date, access_key):
    logger.info('Replicating exchange rate data from fixer.io starting from {}'.format(start_date))
    singer.write_schema('forecast', schema, 'date')

    state = {'start_date': start_date}
    next_date = start_date

    try:
        while True:
            timestamp = str(int(datetime.strptime(next_date, DATE_FORMAT).timestamp()))
            response = request(base_url + access_key + '/' + str(lat_long[0]) + ',' + str(lat_long[1]) + ',' + timestamp, {'exclude': 'minutely'})
            payload = response.json()
            if datetime.strptime(next_date, DATE_FORMAT) > datetime.utcnow():
                break
            elif payload.get('error'):
                raise RuntimeError(payload['error'])
            else:
                singer.write_records('forecast', [parse_response(payload)])
                state = {'start_date': next_date}
                next_date = (datetime.strptime(next_date, DATE_FORMAT) + timedelta(days=1)).strftime(DATE_FORMAT)

    except requests.exceptions.RequestException as e:
        logger.fatal('Error on ' + e.request.url +
                     '; received status ' + str(e.response.status_code) +
                     ': ' + e.response.text)
        singer.write_state(state)
        sys.exit(-1)

    singer.write_state(state)
    logger.info('Tap exiting normally')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config', help='Config file', required=False)
    parser.add_argument(
        '-s', '--state', help='State file', required=False)

    #args = parser.parse_args()
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.config:
        config = args.config
    else:
        config = {}

    if args.state:
        state = args.state
    else:
        state = {}

    start_date = state.get('start_date',
                           config.get('start_date', datetime.utcnow().strftime(DATE_FORMAT)))
    access_key = state.get('access_key', config.get('access_key'))
    lat_long = (config.get('lat', 37.7749),
                config.get('long', -122.4194))

    do_sync(lat_long, start_date, access_key)


if __name__ == '__main__':
    main()
