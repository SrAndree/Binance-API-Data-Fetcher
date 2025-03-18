# Binance-API-Data-Fetcher
Este projeto consiste em duas ferramentas para monitorar dados em tempo real da API da Binance

Console Data Fetcher: Uma aplicação de terminal que busca e exibe dados de criptomoedas a cada 5 minutos.
Interface Gráfica: Um monitor visual completo com cards informativos e gráficos interativos.

Funcionalidades
Versão de Console

Busca dados de múltiplos pares de trading (BTC, ETH, BNB, ADA, SOL)
Exibe informações de ticker atualizadas (preço, variação 24h, volume)
Mostra os últimos 5 candles para cada par de trading
Atualiza automaticamente a cada 5 minutos

Versão com Interface Gráfica

Interface organizada com sistema de abas e cards informativos
Visualização em tabela dos dados históricos de candles
Gráficos interativos de preço com seleção de criptomoeda
Indicadores visuais (verde/vermelho) para variações de preço
Atualizações automáticas e opção de atualização manual

Requisitos

Python 3.6+
Bibliotecas: requests, pandas, matplotlib, tkinter (incluída no Python padrão)
