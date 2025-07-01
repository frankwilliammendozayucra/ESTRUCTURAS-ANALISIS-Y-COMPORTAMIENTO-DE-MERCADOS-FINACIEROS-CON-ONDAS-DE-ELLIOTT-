# real_time_detector.py

import time
from src.api.yahoo_data_api import descargar_datos_yahoo
from src.analysis.harmonic_patterns import detectar_zigzag, detectar_patrones_armonicos, plot_patron
from src.analysis.candlestick import detectar_patrones_velas

def analizar_en_tiempo_real(ticker="AAPL", intervalo="1h", periodo="7d", umbral_zigzag=0.02, delay=60):
    print(f"\n🔄 Iniciando análisis en tiempo real para {ticker} ({intervalo}) cada {delay} segundos...")

    while True:
        try:
            df = descargar_datos_yahoo(ticker, intervalo, periodo)

            # Detectar pivotes con ZigZag
            pivotes = detectar_zigzag(df, threshold=umbral_zigzag)

            # Detectar patrones armónicos
            patrones_armonicos = detectar_patrones_armonicos(pivotes)

            # Detectar patrones de velas japonesas
            patrones_velas = detectar_patrones_velas(df)

            if patrones_armonicos:
                print(f"\n✅ Patrón armónico detectado en {ticker}: {[p[0] for p in patrones_armonicos]}")
                plot_patron(df, pivotes, patrones_armonicos)
            else:
                print("Sin patrones armónicos detectados en este ciclo.")

            if patrones_velas:
                print(f"\n🕯️ Patrones de velas detectados en {ticker}:")
                for tiempo, tipo in patrones_velas[-5:]:  # Mostrar solo los últimos 5
                    if hasattr(tiempo, 'strftime'):
                        fecha_formateada = tiempo.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        fecha_formateada = str(tiempo)
                    print(f" - {tipo} en {fecha_formateada}")
            else:
                print("Sin patrones de velas detectados en este ciclo.")

        except Exception as e:
            print(f"⚠️ Error durante el análisis: {e}")

        time.sleep(delay)  # Esperar antes de volver a analizar


if __name__ == "__main__":
    analizar_en_tiempo_real(
        ticker="AAPL",       # Puedes cambiar a "AAPL" u otro
        intervalo="15m",        # "5m", "15m", "1h", "1d"
        periodo="7d",         # Cuánto histórico revisar
        umbral_zigzag=0.02,     # Sensibilidad del ZigZag
        delay=60                # Tiempo entre análisis (segundos)
    )
