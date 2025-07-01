# src/analysis/fibonacci.py
import pandas as pd
def calcular_fibonacci(df):
    """
    Calcula niveles de retroceso de Fibonacci a partir del máximo y mínimo reciente.
    :param df: DataFrame con columna 'close'
    :return: Diccionario con niveles y precios correspondientes
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        df=df.copy()
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        
    if df.empty or "close" not in df.columns:
        return {}

    max_price = float (df['close'].max().item())
    min_price = float (df['close'].min().item())

    diff = max_price - min_price
    niveles = {
        "0.0%": max_price,
        "23.6%": max_price - 0.236 * diff,
        "38.2%": max_price - 0.382 * diff,
        "50.0%": max_price - 0.500 * diff,
        "61.8%": max_price - 0.618 * diff,
        "100.0%": min_price
    }

    return niveles
