#!/usr/bin/python3

import requests
import hmac
import hashlib
import time
from binance.client import Client
import key

class BinanceAPI:
    def __init__(self):
        self.api_key = key.return_config("APIKey")
        self.secret_key = key.return_config("SecretKey")
        self.base_url = key.return_config("base_url")
        self.client = Client(api_key=self.api_key, api_secret=self.secret_key)

    def _generate_signature(self, query_string):
        return hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def get_account_info(self):
        timestamp = int(time.time() * 1000)
        query_string = f'timestamp={timestamp}'
        signature = self._generate_signature(query_string)
        
        headers = {'X-MBX-APIKEY': self.api_key}
        url = f'{self.base_url}/api/v3/account?{query_string}&signature={signature}'
        
        response = requests.get(url, headers=headers)
        return response.json()

    def get_trades(self, symbol='BNBUSDT'):
        timestamp = int(time.time() * 1000)
        query_string = f'timestamp={timestamp}&symbol={symbol}'
        signature = self._generate_signature(query_string)
        
        headers = {'X-MBX-APIKEY': self.api_key}
        url = f'{self.base_url}/api/v3/myTrades?{query_string}&signature={signature}'
        
        response = requests.get(url, headers=headers)
        return response.json()

    def get_avg_price(self, symbol='BNBUSDT'):
        timestamp = int(time.time() * 1000)
        query_string = f'timestamp={timestamp}&symbol={symbol}'
        signature = self._generate_signature(query_string)
        
        headers = {'X-MBX-APIKEY': self.api_key}
        url = f'{self.base_url}/api/v3/avgPrice?{query_string}&signature={signature}'
        
        response = requests.get(url, headers=headers)
        return response.json() 