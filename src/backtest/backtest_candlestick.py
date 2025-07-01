def backtest_patrones_velas(df, patrones):
    """
    Simula operaciones basadas en patrones de velas. 
    Compra en 'bullish', venta en 'bearish'.
    """
    capital = 1000
    posicion = 0
    historial = []

    for tiempo, tipo in patrones:
        precio = df[df['datetime'] == tiempo]['close'].values
        if len(precio) == 0:
            continue
        precio = precio[0]

        if tipo == 'bullish' and capital > 0:
            posicion = capital / precio
            capital = 0
            historial.append((tiempo, 'BUY', precio))

        elif tipo == 'bearish' and posicion > 0:
            capital = posicion * precio
            posicion = 0
            historial.append((tiempo, 'SELL', precio))

    valor_final = capital if capital > 0 else posicion * df.iloc[-1]['close']
    return historial, valor_final
