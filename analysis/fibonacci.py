import pandas as pd


def calcular_retroceso(precio_ini: float, precio_fin: float, pct: float) -> float:
    """
    Calcula el nivel de retroceso de Fibonacci:
      precio_fin + (precio_ini - precio_fin) * pct
    """
    return precio_fin + (precio_ini - precio_fin) * pct


def validar_fibonacci(
    impulsos: list[tuple[int, int, int]],
    df: pd.DataFrame,
    min_global: float = 0.382,
    max_global: float = 0.618
) -> list[tuple[int, int, int]]:
    """
    Filtra las correcciones A-B-C aplicando un rango global de tolerancia Fibonacci.

    Parámetros:
        impulsos: lista de tripletas (idxA, idxB, idxC)
        df: DataFrame con columna 'Close'
        min_global, max_global: límites de % de retroceso permitidos

    Retorna:
        Lista de tripletas A-B-C que cumplen el rango global.
    """
    validas = []

    for idxA, idxB, idxC in impulsos:
        precio_ini = float(df['Close'].iloc[idxA])
        precio_fin = float(df['Close'].iloc[idxB])
        precio_act = float(df['Close'].iloc[idxC])

        delta = precio_ini - precio_fin
        if delta == 0:
            continue

        ratio = (precio_ini - precio_act) / delta
        if min_global <= ratio <= max_global:
            validas.append((idxA, idxB, idxC))

    total = len(impulsos)
    passes = len(validas)
    tasa = (passes / total * 100) if total > 0 else 0.0
    print(f"📊 Ondas tras filtro Fibonacci: {passes}/{total} → Tasa: {tasa:.2f}%")
    return validas
