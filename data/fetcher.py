# data/fetcher.py

import yfinance as yf
import pandas as pd
import datetime

def obtener_datos(ticker: str, intervalo: str, fecha_inicio=None, fecha_fin=None, minimo_filas=500) -> pd.DataFrame:
    """
    Descarga datos desde Yahoo Finance. Calcula una fecha de inicio suficiente
    para obtener al menos `minimo_filas` registros si no se indica fecha_inicio.
    """

    if fecha_fin is None:
        fecha_fin = datetime.date.today()

    if fecha_inicio is None:
        # Estimar días hacia atrás según la temporalidad
        if intervalo == "1d":
            dias = minimo_filas + 30  # margen de seguridad
        elif intervalo == "1h":
            dias = int(minimo_filas / 6) + 10
        elif intervalo == "15m":
            dias = int(minimo_filas / 26) + 5
        else:
            dias = minimo_filas

        fecha_inicio = fecha_fin - datetime.timedelta(days=dias)

    df = yf.download(
        ticker,
        interval=intervalo,
        start=fecha_inicio,
        end=fecha_fin,
        progress=False,
        auto_adjust=True
    )

    df.dropna(inplace=True)
    return df

def recortar_por_fecha(df: pd.DataFrame, inicio: str, fin: str) -> pd.DataFrame:
    """
    Recorta el DataFrame al rango definido.
    """
    return df.loc[inicio:fin]
