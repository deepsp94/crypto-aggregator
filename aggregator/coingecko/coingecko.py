# standard library:
import sqlite3, json, time, datetime, traceback

# third party libraries:
import requests
from abc import ABC, abstractmethod

class CryptoAPI(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

class CoinGeckoAPI(CryptoAPI):
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3/coins"

    def convert_data_list_to_market_id_dict(self, raw_data):
        return {d['id']:d for d in raw_data}

    def convert_data_list_to_mcap_dict(self, raw_data):
        return {d['market_cap']:d for d in raw_data}

    def convert_timestamp_to_unixtime(self, timestamp):
        unix_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        return unix_datetime.timestamp()

    def fetch_data_from_disk(self, market_ids, filename="test_data.json"):
        with open(filename) as file:
            raw_data = list()
            json_data = json.load(file)
            for row in json_data:
                if row['id'] in market_ids:
                    row['last_updated_unixtime'] = self.convert_timestamp_to_unixtime(row['last_updated'])
                    raw_data.append(row)
                market_data = self.convert_data_list_to_market_id_dict(raw_data)
            return market_data

    def fetch_data_by_mcap(self, N):
        per_page = 250 # max allowed by API is 250
        pages = N // per_page + 1
        market_data = dict()
        try:
            for page in range(1, pages + 1):
                url = f'{self.coingecko_url}/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}'
                response = requests.get(url)
                raw_data = response.json()
                for row in raw_data:
                    row['last_updated_unixtime'] = self.convert_timestamp_to_unixtime(row['last_updated'])
                market_data.update(self.convert_data_list_to_mcap_dict(raw_data))

        except Exception as e:
            print('CoinGecko Error: ', e)
            print('Traceback: ', traceback.format_exc())
            return None

        return market_data

    def fetch_markets(self):
        response = requests.get(f"{self.coingecko_url}/list")
        raw_data = response.json()
        return raw_data

    def fetch_data_from_web(self, market_ids):
        try:
            market_ids = ','.join(market_ids)
            url = f"{self.coingecko_url}/markets?vs_currency=usd&ids={market_ids}"
            response = requests.get(url)
            raw_data = response.json()
            for row in raw_data:
                row['last_updated_unixtime'] = self.convert_timestamp_to_unixtime(row['last_updated'])
            market_data = self.convert_data_list_to_market_id_dict(raw_data)
            return market_data

        except Exception as e:
            print('CoinGecko Error: ', e)
            print('Traceback: ', traceback.format_exc())
            return None

    def fetch_data(self, market_ids=None, top_mcap=None):
        if market_ids is not None:
            return self.fetch_data_from_web(market_ids)
        elif top_mcap is not None:
            return self.fetch_data_by_mcap(top_mcap)
        else:
            return None

# Other functions and classes such as dict_factory, fetch_most_recent_data_from_db,
