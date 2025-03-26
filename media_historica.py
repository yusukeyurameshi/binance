from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import key
import matplotlib.pyplot as plt

# Insira suas chaves aqui
api_key = key.return_config("APIKey")
secret_key = key.return_config("SecretKey")

# Configuração da API (não é necessário API Key para dados públicos)
client = Client(api_key=api_key, api_secret=secret_key)  # Deixe vazio se não for operar

# Parâmetros
symbol = "BNBUSDT"  # Ativo desejado (ex.: BTCUSDT, ETHUSDT)
days = 5  # Período em dias

# Calcula a data de início (200 dias atrás)
end_date = datetime.now()
start_date = end_date - timedelta(days=days)

# Coleta os dados históricos (velas diárias)
klines = client.get_historical_klines(
    symbol=symbol,
    interval=Client.KLINE_INTERVAL_1DAY,  # Intervalo diário
    start_str=start_date.strftime("%d %b %Y %H:%M:%S"),
    end_str=end_date.strftime("%d %b %Y %H:%M:%S")
)

# Processa os dados em um DataFrame
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
])

# Converte timestamp para data e preço para numérico
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df["close"] = pd.to_numeric(df["close"])
df["high"] = pd.to_numeric(df["high"])
df["low"] = pd.to_numeric(df["low"])

# Calcula a média do preço de fechamento
media = df["close"].mean()

print(f"\nMédia de preço (últimos {days} dias): ${media:.2f}")

#df.plot(x="timestamp", y="close", title=f"Preço de {symbol} (Últimos {days} dias)")
#plt.show()

# Cria o gráfico
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["close"], label="Preço de Fechamento")
plt.plot(df["timestamp"], df["high"], label="Preço Máximo")
plt.plot(df["timestamp"], df["low"], label="Preço Mínimo")
plt.title(f"Preço de {symbol} (Últimos {days} dias)")
plt.xlabel("Data")
plt.ylabel("Preço (USD)")
plt.legend()

# Salva a figura
plt.savefig("grafico_preco.png")  # Pode ser .jpg, .svg, etc.
print("Gráfico salvo como 'grafico_preco.png'")
