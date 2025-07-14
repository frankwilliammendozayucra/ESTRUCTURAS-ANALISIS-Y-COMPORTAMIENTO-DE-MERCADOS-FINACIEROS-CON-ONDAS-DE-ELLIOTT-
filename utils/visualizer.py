# utils/visualizer.py

import matplotlib.pyplot as plt
import pandas as pd


def graficar_ondas(df: pd.DataFrame, ondas_detectadas, rci: pd.Series, titulo="Análisis de Ondas de Elliott"):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Gráfico de precios con ondas
    ax1.plot(df['Close'].values, label='Precio', color='black')
    for idx in ondas_detectadas:
        puntos = df['Close'].iloc[idx].values
        ax1.plot(idx, puntos, 'ro-')
        for i, val in zip(idx, puntos):
            ax1.text(i, val, str(i), fontsize=9, color='blue')
    ax1.set_title(titulo)
    ax1.legend()
    ax1.grid(True)

    # Gráfico del RCI
    ax2.plot(rci, label='RCI', color='purple')
    ax2.axhline(80, color='green', linestyle='--', label='Sobrecompra')
    ax2.axhline(-80, color='red', linestyle='--', label='Sobreventa')
    ax2.set_title("Ranking Correlation Index (RCI)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
