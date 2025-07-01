from .harmonic_patterns import detectar_zigzag

def detectar_ondas_elliott(df, threshold=0.02):
    """
    Detecta ondas de Elliott basadas en ZigZag simples.
    Retorna una lista de secuencias de 5 puntos.
    """
    pivotes = detectar_zigzag(df, threshold=threshold)
    ondas = []

    # Reglas muy básicas: cualquier secuencia de 5 puntos consecutivos
    for i in range(len(pivotes) - 4):
        secuencia = pivotes[i:i + 5]
        ondas.append(secuencia)

    return ondas
