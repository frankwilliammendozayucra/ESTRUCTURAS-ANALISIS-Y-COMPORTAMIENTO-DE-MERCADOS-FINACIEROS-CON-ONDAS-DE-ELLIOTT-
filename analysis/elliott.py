# analysis/elliott.py

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from config import ORDEN_EXTREMOS, UMBRAL_RCI_ONDA3, UMBRAL_RCI_ONDA5


def detectar_extremos(df: pd.DataFrame, columna: str = "Close", orden: int = ORDEN_EXTREMOS) -> list:
    """
    Encuentra índices de máximos y mínimos locales en la serie de precios.
    """
    precios = df[columna].values
    if len(precios) < orden * 2 + 1:
        return []
    maximos = argrelextrema(precios, np.greater, order=orden)[0]
    minimos = argrelextrema(precios, np.less, order=orden)[0]
    extremos = sorted(np.concatenate((maximos, minimos)))
    return extremos


def es_valida_onda(puntos: np.ndarray) -> bool:
    """
    Validación muy permisiva de ondas de Elliott: sólo requiere 6 puntos y
    al menos un movimiento alcista y uno bajista.
    """
    # Debe tener 6 puntos para formar 5 movimientos
    if len(puntos) != 6:
        return False
    # Calcular direcciones de cada segmento
    direccion = [puntos[i+1] > puntos[i] for i in range(5)]
    # Requiere al menos una subida y una bajada
    if not any(direccion) or not any(not d for d in direccion):
        return False
    return True


def detectar_ondas_elliott(df: pd.DataFrame, extremos: list, rci: pd.Series) -> list:
    """
    Detecta secuencias de ondas de Elliott impulsivas (1-5) usando criterios permisivos,
    y filtra con umbrales de RCI.

    Parámetros:
        df: DataFrame con al menos la columna 'Close'.
        extremos: lista de índices de picos y valles.
        rci: Serie de Ranking Correlation Index.

    Retorna:
        Lista de listas de 6 índices que cumplen la estructura y el umbral de RCI.
    """
    ondas_detectadas = []
    # Necesita al menos 6 extremos
    if len(extremos) < 6:
        return ondas_detectadas

    for i in range(len(extremos) - 5):
        idx = extremos[i:i+6]
        # Verificar índices válidos
        if any(j >= len(df) for j in idx):
            continue
        puntos = df['Close'].iloc[idx].values
        # Validar forma básica de onda
        if not es_valida_onda(puntos):
            continue
        # Filtrar por RCI si se proporciona
        if rci is not None:
            try:
                rci3 = rci.iloc[idx[3]]
                rci5 = rci.iloc[idx[5]]
            except Exception:
                continue
            if rci3 <= UMBRAL_RCI_ONDA3 or rci5 <= UMBRAL_RCI_ONDA5:
                continue
        ondas_detectadas.append(idx)
    return ondas_detectadas

def detectar_correctivas(df: pd.DataFrame, onda_impulso: list, orden: int = ORDEN_EXTREMOS) -> list:
    """
    Dada una onda impulsiva (6 índices), busca el siguiente patrón correctivo A-B-C.
    Devuelve [idxA, idxB, idxC] o [] si no lo encuentra.

    - A: primer extremo tras idx5 (valle si la onda fue alcista, pico si fue bajista)
    - B: pico/valle opuesto tras A
    - C: siguiente extremo de mismo tipo que A tras B
    """
    precios = df['Close'].values
    ultima_v = onda_impulso[-1]
    # toma sólo precios posteriores a la onda
    sub = precios[ultima_v:]
    # índices globales
    offset = ultima_v

    # detecta todos los extremos posteriores
    maxs = argrelextrema(sub, np.greater, order=orden)[0] + offset
    mins = argrelextrema(sub, np.less,   order=orden)[0] + offset

    # determina si la onda fue alcista o bajista
    onda_alcista = precios[onda_impulso[-1]] > precios[onda_impulso[-2]]

    # 1) A = primer mínimo tras impulso si la onda fue alcista, o primer máximo si bajista
    poolA = mins if onda_alcista else maxs
    if len(poolA)==0: return []
    idxA = poolA[0]

    # 2) B = primer extremo opuesto tras A
    poolB = maxs if onda_alcista else mins
    poolB = poolB[poolB > idxA]
    if len(poolB)==0: return []
    idxB = poolB[0]

    # 3) C = siguiente extremo del mismo tipo que A tras B
    poolC = poolA[poolA > idxB]
    if len(poolC)==0: return []
    idxC = poolC[0]

    return [idxA, idxB, idxC]
