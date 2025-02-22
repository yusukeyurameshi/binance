#!/usr/bin/python3

import cx_Oracle
import requests
import hmac
import hashlib
import time
import key
import json

user = key.return_config("user")
senha = key.return_secret("adbinvest")
db = key.return_config("db")

conn = cx_Oracle.connect(f"{user}/{senha}@{db}")
cursor = conn.cursor()
cursor.execute("alter session set nls_date_format='mm/dd/yyyy hh24:mi:ss'")

cursor.execute("select sysdate from dual")

rows = cursor.fetchall()

for row in rows:

    print(row[0])

cursor.close()
conn.close()


# Insira suas chaves aqui
api_key = key.return_config("APIKey")
secret_key = key.return_config("SecretKey")

base_url = key.return_config("base_url")
endpoint = '/api/v3/account'
timestamp = int(time.time() * 1000)

query_string = f'timestamp={timestamp}'
signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

headers = {
    'X-MBX-APIKEY': api_key
}

url = f'{base_url}{endpoint}?{query_string}&signature={signature}'
response = requests.get(url, headers=headers)
account_info = response.json()

for balance in account_info['balances']:
    if float(balance['free']) != 0 or float(balance['locked']) != 0:
        print(f"{balance['asset']}: {balance['free']} (free), {balance['locked']} (locked)")
        print(balance)
        print("##########")

endpoint = '/api/v3/myTrades'
timestamp = int(time.time() * 1000)

query_string = f'timestamp={timestamp}&symbol=BNBUSDT'
signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

headers = {
    'X-MBX-APIKEY': api_key
}

url = f'{base_url}{endpoint}?{query_string}&signature={signature}'
print(url)
response = requests.get(url, headers=headers)
account_info = response.json()

print(json.dumps(account_info,indent=2))

