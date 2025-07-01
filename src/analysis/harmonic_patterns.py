# harmonic_patterns.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Proporciones armónicas comunes para detección
PATTERNS = {
    "Bat": {
        "AB": (0.382, 0.5),
        "BC": (0.382, 0.886),
        "CD": (1.618, 2.618),
    },
    "Gartley": {
        "AB": (0.618, 0.618),
        "BC": (0.382, 0.886),
        "CD": (1.272, 1.618),
    },
    "Butterfly": {
        "AB": (0.786, 0.786),
        "BC": (0.382, 0.886),
        "CD": (1.618, 2.618),
    }
}

# Detección simple de zigzag por cambios porcentuales

def detectar_zigzag(df, threshold=0.02):
    precios = df['close'].values
    pivotes = []
    last_pivot = precios[0]
    direction = 0

    for i in range(1, len(precios)):
        change = (precios[i] - last_pivot) / last_pivot

        if direction == 0 and abs(change) > threshold:
            direction = 1 if change > 0 else -1
            last_pivot = precios[i]
            pivotes.append((i, precios[i]))

        elif direction == 1 and change < -threshold:
            direction = -1
            last_pivot = precios[i]
            pivotes.append((i, precios[i]))

        elif direction == -1 and change > threshold:
            direction = 1
            last_pivot = precios[i]
            pivotes.append((i, precios[i]))

    return pivotes

# Evaluar si los pivotes cumplen las proporciones del patrón

def detectar_patrones_armonicos(pivotes, tolerancia=0.05):
    patrones = []

    for i in range(len(pivotes) - 4):
        X, A, B, C, D = [p[1] for p in pivotes[i:i+5]]

        AB = abs(B - A) / abs(X - A)
        BC = abs(C - B) / abs(A - B)
        CD = abs(D - C) / abs(B - C)

        for nombre, reglas in PATTERNS.items():
            ab_r = reglas["AB"]
            bc_r = reglas["BC"]
            cd_r = reglas["CD"]

            if (ab_r[0] <= AB <= ab_r[1]) and (bc_r[0] <= BC <= bc_r[1]) and (cd_r[0] <= CD <= cd_r[1]):
                patrones.append((nombre, [p[0] for p in pivotes[i:i+5]]))

    return patrones

# Visualizar precios, pivotes y patrones

def plot_patron(df, pivotes, patrones):
    plt.figure(figsize=(12, 6))
    plt.plot(df['close'].values, label='Precio', linewidth=1)

    for idx, price in pivotes:
        plt.scatter(idx, price, color='red')

    for nombre, puntos in patrones:
        x = puntos
        y = [df['close'].iloc[i] for i in puntos]
        plt.plot(x, y, label=f"Patrón: {nombre}", linewidth=2)

    plt.legend()
    plt.title("Patrones armónicos detectados")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
