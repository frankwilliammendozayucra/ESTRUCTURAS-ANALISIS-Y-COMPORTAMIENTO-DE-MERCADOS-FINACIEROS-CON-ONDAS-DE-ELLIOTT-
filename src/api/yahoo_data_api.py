# src/api/yahoo_data_api.py

import yfinance as yf
import pandas as pd

def descargar_datos_yahoo(ticker="AAPL", intervalo="1h", periodo="60d"):
   
    df = yf.download(ticker, interval=intervalo, period=periodo, progress=False, auto_adjust=False)
    df = df.reset_index()
    df = df.rename(columns=str.lower)

    # Formatear nombres y columnas necesarias
    df = df[["datetime", "open", "high", "low", "close", "volume"]]
    return df
