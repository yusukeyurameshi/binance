#!/usr/bin/python3

import cx_Oracle
import requests
import hmac
import hashlib
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from binance.client import Client
import matplotlib.pyplot as plt
import key

class DatabaseManager:
    def __init__(self):
        KeyManager = key.KeyManager()
        self.user = KeyManager.return_config("user")
        self.senha = KeyManager.return_secret("adbinvest")
        self.db = KeyManager.return_config("db")
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = cx_Oracle.connect(f"{self.user}/{self.senha}@{self.db}")
        self.cursor = self.conn.cursor()
        self.cursor.execute("alter session set nls_date_format='mm/dd/yyyy hh24:mi:ss'")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_current_time(self):
        self.cursor.execute("select sysdate from dual")
        return self.cursor.fetchall()[0][0]

class BinanceAPI:
    def __init__(self):
        KeyManager = key.KeyManager()
        self.api_key = KeyManager.return_config("APIKey")
        self.secret_key = KeyManager.return_config("SecretKey")
        self.base_url = KeyManager.return_config("base_url")
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

class BinanceAnalyzer:
    def __init__(self):
        self.api = BinanceAPI()
        self.db = DatabaseManager()

    def analyze_historical_data(self, symbol="BNBUSDT", days=5):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        klines = self.api.client.get_historical_klines(
            symbol=symbol,
            interval=Client.KLINE_INTERVAL_1DAY,
            start_str=start_date.strftime("%d %b %Y %H:%M:%S"),
            end_str=end_date.strftime("%d %b %Y %H:%M:%S")
        )

        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = pd.to_numeric(df["close"])
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])

        return df

    def generate_price_graph(self, df, symbol="BNBUSDT", days=5):
        plt.figure(figsize=(12, 6))
        plt.plot(df["timestamp"], df["close"], label="Preço de Fechamento")
        plt.plot(df["timestamp"], df["high"], label="Preço Máximo")
        plt.plot(df["timestamp"], df["low"], label="Preço Mínimo")
        plt.title(f"Preço de {symbol} (Últimos {days} dias)")
        plt.xlabel("Data")
        plt.ylabel("Preço (USD)")
        plt.legend()
        plt.savefig("grafico_preco.png")
        print("Gráfico salvo como 'grafico_preco.png'")

    def print_account_balance(self):
        account_info = self.api.get_account_info()
        for balance in account_info['balances']:
            if float(balance['free']) != 0 or float(balance['locked']) != 0:
                print(f"{balance['asset']}: {balance['free']} (free), {balance['locked']} (locked)")
                print(balance)
                print("##########")

def main():
    analyzer = BinanceAnalyzer()
    DBConn = DatabaseManager()
    DBConn.connect()
    DBConn.close()
    
    # Exemplo de uso
    print("=== Informações da Conta ===")
    analyzer.print_account_balance()
    
    print("\n=== Análise Histórica ===")
    df = analyzer.analyze_historical_data(days=5)
    media = df["close"].mean()
    print(f"Média de preço (últimos 5 dias): ${media:.2f}")
    
    print("\n=== Gerando Gráfico ===")
    analyzer.generate_price_graph(df)

if __name__ == "__main__":
    main() 