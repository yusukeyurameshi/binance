#!/usr/bin/python3

from src.binance_analyzer import BinanceAnalyzer

def main():
    analyzer = BinanceAnalyzer()
    
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