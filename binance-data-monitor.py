import tkinter as tk
from tkinter import ttk
import requests
import threading
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")

class BinanceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Dados Binance")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        self.base_url = 'https://api.binance.com/api/v3'
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
        self.interval = '5m'
        self.update_interval = 300  # 5 minutos em segundos
        self.is_running = True
        
        self.setup_ui()
        self.start_update_thread()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg="#2c3e50")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(header_frame, text="MONITOR DE DADOS BINANCE", 
                              font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)
        
        self.time_label = tk.Label(header_frame, text=f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                  font=("Arial", 10), bg="#2c3e50", fg="white")
        self.time_label.pack(pady=(0, 10))
        
        # Container para as abas
        tab_control = ttk.Notebook(main_frame)
        
        # Aba de visão geral
        overview_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(overview_tab, text="Visão Geral")
        
        # Aba de gráficos
        charts_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(charts_tab, text="Gráficos")
        
        tab_control.pack(expand=1, fill=tk.BOTH)
        
        # Configuração da aba de visão geral
        self.setup_overview_tab(overview_tab)
        
        # Configuração da aba de gráficos
        self.setup_charts_tab(charts_tab)
        
        # Barra de status
        status_frame = tk.Frame(main_frame, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="Monitorando dados...", 
                                    bg="#34495e", fg="white", anchor="w")
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão para atualizar manualmente
        update_button = tk.Button(status_frame, text="Atualizar Agora", 
                                 command=self.update_data, bg="#3498db", fg="white")
        update_button.pack(side=tk.RIGHT, padx=10, pady=2)

    def setup_overview_tab(self, parent):
        # Frame para os cards de cada moeda
        self.cards_frame = tk.Frame(parent, bg="#f0f0f0")
        self.cards_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criando cards para cada símbolo
        self.symbol_frames = {}
        for symbol in self.symbols:
            card = tk.Frame(self.cards_frame, bg="white", relief=tk.RAISED, borderwidth=1)
            card.pack(fill=tk.X, pady=5, padx=5)
            
            # Cabeçalho do card
            header = tk.Frame(card, bg="#3498db")
            header.pack(fill=tk.X)
            
            name_label = tk.Label(header, text=symbol, font=("Arial", 12, "bold"), 
                                 bg="#3498db", fg="white")
            name_label.pack(pady=5)
            
            # Conteúdo do card
            content = tk.Frame(card, bg="white")
            content.pack(fill=tk.X, padx=10, pady=10)
            
            # Layout em grid para os dados
            content.columnconfigure(0, weight=1)
            content.columnconfigure(1, weight=1)
            
            # Rótulos para os dados
            price_label = tk.Label(content, text="Preço Atual:", font=("Arial", 10, "bold"), 
                                  bg="white", anchor="w")
            price_label.grid(row=0, column=0, sticky="w", pady=2)
            
            change_label = tk.Label(content, text="Variação 24h:", font=("Arial", 10, "bold"), 
                                   bg="white", anchor="w")
            change_label.grid(row=1, column=0, sticky="w", pady=2)
            
            volume_label = tk.Label(content, text="Volume 24h:", font=("Arial", 10, "bold"), 
                                   bg="white", anchor="w")
            volume_label.grid(row=2, column=0, sticky="w", pady=2)
            
            high_label = tk.Label(content, text="Máxima 24h:", font=("Arial", 10, "bold"), 
                                 bg="white", anchor="w")
            high_label.grid(row=3, column=0, sticky="w", pady=2)
            
            low_label = tk.Label(content, text="Mínima 24h:", font=("Arial", 10, "bold"), 
                                bg="white", anchor="w")
            low_label.grid(row=4, column=0, sticky="w", pady=2)
            
            # Valores (serão atualizados)
            price_value = tk.Label(content, text="Carregando...", font=("Arial", 10), 
                                  bg="white", anchor="e")
            price_value.grid(row=0, column=1, sticky="e", pady=2)
            
            change_value = tk.Label(content, text="Carregando...", font=("Arial", 10), 
                                   bg="white", anchor="e")
            change_value.grid(row=1, column=1, sticky="e", pady=2)
            
            volume_value = tk.Label(content, text="Carregando...", font=("Arial", 10), 
                                   bg="white", anchor="e")
            volume_value.grid(row=2, column=1, sticky="e", pady=2)
            
            high_value = tk.Label(content, text="Carregando...", font=("Arial", 10), 
                                 bg="white", anchor="e")
            high_value.grid(row=3, column=1, sticky="e", pady=2)
            
            low_value = tk.Label(content, text="Carregando...", font=("Arial", 10), 
                                bg="white", anchor="e")
            low_value.grid(row=4, column=1, sticky="e", pady=2)
            
            # Tabela para os últimos candles
            table_label = tk.Label(card, text="Últimos Candles", font=("Arial", 10, "bold"), 
                                  bg="white")
            table_label.pack(pady=(10, 5))
            
            # Frame para a tabela
            table_frame = tk.Frame(card, bg="white")
            table_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # Treeview para os dados dos candles
            columns = ("Tempo", "Abertura", "Máxima", "Mínima", "Fechamento", "Volume")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=80, anchor="center")
            
            tree.pack(fill=tk.X)
            
            # Armazenamos as referências para atualização posterior
            self.symbol_frames[symbol] = {
                "price": price_value,
                "change": change_value,
                "volume": volume_value,
                "high": high_value,
                "low": low_value,
                "tree": tree
            }

    def setup_charts_tab(self, parent):
        # Frame para gráficos
        charts_container = tk.Frame(parent, bg="#f0f0f0")
        charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dropdown para selecionar a moeda
        selector_frame = tk.Frame(charts_container, bg="#f0f0f0")
        selector_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(selector_frame, text="Selecione a moeda:", bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.selected_symbol = tk.StringVar()
        self.selected_symbol.set(self.symbols[0])
        
        symbol_dropdown = ttk.Combobox(selector_frame, textvariable=self.selected_symbol, 
                                      values=self.symbols, state="readonly")
        symbol_dropdown.pack(side=tk.LEFT, padx=10)
        symbol_dropdown.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Frame para o gráfico
        self.chart_frame = tk.Frame(charts_container, bg="white")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criando o gráfico inicial
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Inicialmente o gráfico está vazio
        self.ax.set_title(f"Carregando dados para {self.selected_symbol.get()}")
        self.fig.tight_layout()
        self.canvas.draw()

    def get_ticker_data(self, symbol):
        """Obtém dados atuais de preço e volume para um símbolo"""
        endpoint = f'/ticker/24hr'
        params = {'symbol': symbol}
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao obter ticker para {symbol}: {e}")
            return None
    
    def get_kline_data(self, symbol):
        """Obtém dados de candles para um símbolo específico"""
        endpoint = f'/klines'
        params = {
            'symbol': symbol,
            'interval': self.interval,
            'limit': 30  # Últimos 30 candles para o gráfico
        }
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            
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
        
        except Exception as e:
            print(f"Erro ao obter dados para {symbol}: {e}")
            return None

    def update_chart(self, event=None):
        symbol = self.selected_symbol.get()
        
        # Limpar o gráfico anterior
        self.ax.clear()
        
        # Buscar dados
        df = self.get_kline_data(symbol)
        
        if df is not None and not df.empty:
            # Criar gráfico de preço
            self.ax.plot(df['open_time'], df['close'], label='Preço de Fechamento', color='#3498db')
            
            # Configurações do gráfico
            self.ax.set_title(f"Histórico de Preço para {symbol}")
            self.ax.set_xlabel('Data/Hora')
            self.ax.set_ylabel('Preço (USDT)')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # Formatar o eixo x para mostrar apenas algumas datas
            self.ax.set_xticks(df['open_time'][::5])
            self.ax.set_xticklabels([d.strftime('%H:%M') for d in df['open_time'][::5]], rotation=45)
            
            self.fig.tight_layout()
            self.canvas.draw()
        else:
            self.ax.set_title(f"Erro ao carregar dados para {symbol}")
            self.canvas.draw()

    def update_data(self):
        self.status_label.config(text="Atualizando dados...")
        self.time_label.config(text=f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for symbol in self.symbols:
            # Atualizar ticker data
            ticker_data = self.get_ticker_data(symbol)
            if ticker_data:
                # Atualizar os widgets com os dados
                frame = self.symbol_frames[symbol]
                
                # Formatar o preço com precisão apropriada
                price = float(ticker_data['lastPrice'])
                if price < 0.1:
                    price_str = f"{price:.8f}"
                elif price < 1:
                    price_str = f"{price:.6f}"
                elif price < 100:
                    price_str = f"{price:.4f}"
                else:
                    price_str = f"{price:.2f}"
                    
                frame["price"].config(text=price_str)
                
                # Variação com cor (verde para positivo, vermelho para negativo)
                change = float(ticker_data['priceChangePercent'])
                change_str = f"{change:+.2f}%"
                if change >= 0:
                    frame["change"].config(text=change_str, fg="green")
                else:
                    frame["change"].config(text=change_str, fg="red")
                
                # Outros dados
                frame["volume"].config(text=f"{float(ticker_data['volume']):.2f}")
                
                high = float(ticker_data['highPrice'])
                if high < 0.1:
                    high_str = f"{high:.8f}"
                else:
                    high_str = f"{high:.4f}"
                frame["high"].config(text=high_str)
                
                low = float(ticker_data['lowPrice'])
                if low < 0.1:
                    low_str = f"{low:.8f}"
                else:
                    low_str = f"{low:.4f}"
                frame["low"].config(text=low_str)
            
            # Atualizar dados de candles
            kline_data = self.get_kline_data(symbol)
            if kline_data is not None and not kline_data.empty:
                # Limpar a tabela existente
                tree = self.symbol_frames[symbol]["tree"]
                for item in tree.get_children():
                    tree.delete(item)
                
                # Adicionar os novos dados (últimos 5 candles)
                for i in range(min(5, len(kline_data))):
                    row = kline_data.iloc[i]
                    time_str = row['open_time'].strftime('%H:%M:%S')
                    
                    # Formatar os valores numéricos
                    values = (
                        time_str,
                        f"{row['open']:.6f}",
                        f"{row['high']:.6f}",
                        f"{row['low']:.6f}",
                        f"{row['close']:.6f}",
                        f"{row['volume']:.2f}"
                    )
                    
                    tree.insert("", 0, values=values)
        
        # Atualizar o gráfico se necessário
        self.update_chart()
        
        self.status_label.config(text=f"Dados atualizados com sucesso. Próxima atualização em {self.update_interval} segundos.")

    def update_loop(self):
        while self.is_running:
            try:
                # Atualizar dados na thread principal
                self.root.after(0, self.update_data)
                # Esperar pelo próximo ciclo
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Erro no loop de atualização: {e}")

    def start_update_thread(self):
        # Iniciar thread para atualização periódica
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def on_closing(self):
        self.is_running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BinanceMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
