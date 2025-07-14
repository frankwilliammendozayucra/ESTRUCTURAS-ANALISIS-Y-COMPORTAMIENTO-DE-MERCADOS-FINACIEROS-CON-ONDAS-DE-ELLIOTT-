# config.py

# Lista de activos a analizar
ACTIVOS = [
    "BTC-USD",
    "ETH-USD",
    "EURUSD=X",
    "GBPUSD=X",   # Libra / Dólar
    "USDJPY=X",   # Dólar / Yen japonés
    "XAGUSD=X",   # Plata spot
    "DIA",        # ETF Dow Jones
    "GLD"         # ETF Oro'
]

# Temporalidades compatibles
TEMPORALIDADES = [
    "1h",
    "15m",
    "5m",
    "1d"
]

# Rango de fechas para backtesting (opcional)
BACKTEST_FECHA_INICIO = "2025-01-01"
BACKTEST_FECHA_FIN    = "2025-07-14"

# Parámetros del análisis técnico
ORDEN_EXTREMOS      = 3
RCI_PERIODO         = 9
UMBRAL_RCI_ONDA3    = 20
UMBRAL_RCI_ONDA5    = 0
RSI_PERIODO         = 14
UMBRAL_RSI_COMPRA   = 30
UMBRAL_RSI_VENTA    = 70

# Validación Fibonacci
FIBONACCI_VALIDACION = {
    "onda2": (0.2, 0.9),
    "onda3": (0.7, 3.5),
    "onda4": (0.1, 0.7),
    "onda5": (0.2, 3.0)
}

# Mostrar gráficas automáticamente
MOSTRAR_GRAFICAS = True

# ————————————————
# Límites reales de Yahoo Finance
LIMITE_DIAS = {
    "5m": 59,
    "15m": 59,
    "1h": 365,   # aprox. último año
    "1d": 730    # aprox. últimos 2 años
}

# Gestión de riesgo
PROFIT_PCT   = 0.038   # 3.8% de take-profit
UMBRAL_RSI_C = 30      # RSI mínimo en punto C para validar señal
MA_PERIOD    = 20      # Periodo de la media móvil de confirmación
RSI_PERIODO = 14
UMBRAL_RSI_COMPRA = 30
TAKE_PROFIT_PCT = 0.05  # por ejemplo un 5%


TIEMPO_ESPERA = 30

# Rango global ampliado de tolerancia Fibonacci (mínimo, máximo)
FIBO_MIN_GLOBAL = 0.30
FIBO_MAX_GLOBAL = 0.70