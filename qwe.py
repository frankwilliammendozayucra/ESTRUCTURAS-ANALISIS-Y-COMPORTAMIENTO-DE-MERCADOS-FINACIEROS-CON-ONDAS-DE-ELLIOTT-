import time
from datetime import datetime, timedelta

import pandas as pd

from data.fetcher import obtener_datos
from analysis.elliott import detectar_extremos, detectar_ondas_elliott, detectar_correctivas
from config import ACTIVOS, TEMPORALIDADES, LIMITE_DIAS, TIEMPO_ESPERA

def calcular_fecha_inicio(intervalo: str) -> datetime.date:
    dias = LIMITE_DIAS.get(intervalo, 30)
    return datetime.today().date() - timedelta(days=dias)

def rotar_temporalidades(activos, temporalidades):
    while True:
        for intervalo in temporalidades:
            print(f"\n🔄 Intervalo: {intervalo}")
            # Inicializar estadísticas
            stats = {t: {'total': 0, 'hits': 0, 'pl': []} for t in activos}

            inicio = calcular_fecha_inicio(intervalo)
            fin = datetime.today().date()

            for ticker in activos:
                df = obtener_datos(ticker, intervalo, inicio, fin)
                if df is None or df.empty:
                    continue

                # Unificar la serie de cierres
                close = df['Close']
                if isinstance(close, pd.DataFrame):
                    close = close.squeeze()

                # 1) Detección de extremos y ondas de Elliott
                extremos = detectar_extremos(df)
                ondas = detectar_ondas_elliott(df, extremos, rci=None)

                # 2) Para cada onda impulsiva, buscar A-B-C y evaluar señal en C
                for onda in ondas:
                    correctiva = detectar_correctivas(df, onda)
                    if not correctiva:
                        continue
                    idxC = correctiva[2]

                    # Precio en C y precio siguiente
                    try:
                        precioC   = close.iat[idxC]
                        siguiente = close.iat[idxC + 1]
                    except (IndexError, KeyError):
                        continue

                    stats[ticker]['total'] += 1
                    if siguiente > precioC:
                        stats[ticker]['hits'] += 1
                    stats[ticker]['pl'].append((siguiente - precioC) / precioC)

            # 3) Imprimir resumen para este intervalo
            for ticker in activos:
                tot  = stats[ticker]['total']
                hits = stats[ticker]['hits']
                rate = hits / tot * 100 if tot else 0.0
                avg_pl = (sum(stats[ticker]['pl']) / len(stats[ticker]['pl']) * 100) if stats[ticker]['pl'] else 0.0

                print(f"  📊 {ticker}: señales={tot}, aciertos={hits} → tasa={rate:.2f}%"
                      f"  P&L medio={avg_pl:.2f}%")

        time.sleep(TIEMPO_ESPERA)


if __name__ == "__main__":
    rotar_temporalidades(ACTIVOS, TEMPORALIDADES)