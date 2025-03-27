#!/usr/bin/python3

import pandas as pd
from datetime import datetime, timedelta
from binance.client import Client
import matplotlib.pyplot as plt
from .database_manager import DatabaseManager
from .binance_api import BinanceAPI

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