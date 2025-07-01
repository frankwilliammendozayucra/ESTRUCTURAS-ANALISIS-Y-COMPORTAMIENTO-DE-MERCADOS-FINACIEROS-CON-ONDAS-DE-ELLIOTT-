from src.api.yahoo_data_api import descargar_datos_yahoo

df = descargar_datos_yahoo("AAPL", "1h", "60d")
print(df.tail())
