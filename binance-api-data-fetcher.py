import requests
import time
import pandas as pd
from datetime import datetime
import os

class BinanceDataFetcher:
    def __init__(self, symbols=None, interval='5m'):
        """
        Inicializa o fetcher de dados da Binance
        
        Args:
            symbols: Lista de símbolos de pares de trading (ex: ['BTCUSDT', 'ETHUSDT'])
            interval: Intervalo de tempo para os dados (padrão: 5m)
        """
        self.base_url = 'https://api.binance.com/api/v3'
        self.symbols = symbols or ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
        self.interval = interval
        
    def get_kline_data(self, symbol):
        """Obtém dados de candles para um símbolo específico"""
        endpoint = f'/klines'
        params = {
            'symbol': symbol,
            'interval': self.interval,
            'limit': 5  # Últimos 5 candles
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()  # Lança exceção para erros HTTP
            
            data = response.json()
            
            # Converter para DataFrame
            df = pd.DataFrame(data, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Converter timestamps para datetime
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
            
            # Converter valores numéricos
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
                
            return df
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados para {symbol}: {e}")
            return None
    
    def get_ticker_data(self, symbol):
        """Obtém dados atuais de preço e volume para um símbolo"""
        endpoint = f'/ticker/24hr'
        params = {
            'symbol': symbol
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter ticker para {symbol}: {e}")
            return None
    
    def display_data(self):
        """Exibe os dados obtidos de forma organizada no terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
        
        print(f"\n{'='*80}")
        print(f"DADOS DA BINANCE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        for symbol in self.symbols:
            print(f"\n{'-'*80}")
            print(f"SÍMBOLO: {symbol}")
            print(f"{'-'*80}")
            
            # Obter e exibir dados de ticker
            ticker_data = self.get_ticker_data(symbol)
            if ticker_data:
                print(f"Preço atual: {float(ticker_data['lastPrice']):.8f}")
                print(f"Variação 24h: {float(ticker_data['priceChangePercent']):+.2f}%")
                print(f"Volume 24h: {float(ticker_data['volume']):.2f}")
                print(f"Máxima 24h: {float(ticker_data['highPrice']):.8f}")
                print(f"Mínima 24h: {float(ticker_data['lowPrice']):.8f}")
            
            # Obter e exibir dados de candles
            kline_data = self.get_kline_data(symbol)
            if kline_data is not None and not kline_data.empty:
                print("\nÚltimos 5 candles:")
                
                # Criar visualização simplificada do DataFrame
                view_df = kline_data[['open_time', 'open', 'high', 'low', 'close', 'volume']].copy()
                view_df['open_time'] = view_df['open_time'].dt.strftime('%H:%M:%S')
                
                print(view_df.to_string(index=False, float_format=lambda x: f"{x:.8f}"))
            
            print("")
    
    def run(self, interval_seconds=300):
        """
        Executa o loop principal para buscar dados periodicamente
        
        Args:
            interval_seconds: Intervalo em segundos entre cada busca (padrão: 300s = 5min)
        """
        try:
            while True:
                self.display_data()
                print(f"\nPróxima atualização em {interval_seconds} segundos. Pressione Ctrl+C para sair.")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nPrograma encerrado pelo usuário.")


if __name__ == "__main__":
    # Lista de símbolos que você deseja monitorar
    symbols_to_monitor = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
    
    # Criando instância do fetcher com os símbolos desejados
    fetcher = BinanceDataFetcher(symbols=symbols_to_monitor)
    
    # Iniciar o monitoramento com intervalo de 5 minutos (300 segundos)
    fetcher.run(interval_seconds=300)
