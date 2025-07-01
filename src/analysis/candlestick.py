# src/analysis/candlestick.py
def detectar_patrones_velas(df):
    patrones = []

    for i in range(1, len(df)):
        o, h, l, c = df.loc[i, ["open", "high", "low", "close"]]
        cuerpo = abs(c - o)
        sombra_inferior = o - l if c > o else c - l
        sombra_superior = h - c if c > o else h - o

        o_ant, c_ant = df.loc[i - 1, ["open", "close"]]

        # Martillo
        if cuerpo < (h - l) * 0.3 and sombra_inferior > cuerpo * 2 and sombra_superior < cuerpo:
            patrones.append((df[ "datetime"].iloc[i], "Martillo"))

        # Envolvente Alcista
        if c_ant < o_ant and c > o and c > o_ant and o < c_ant:
            patrones.append((df[ "datetime"].iloc[i], "Envolvente Alcista"))

        # Doji
        if cuerpo < (h - l) * 0.1:
            patrones.append((df[ "datetime"].iloc[i], "Doji"))

        # Estrella Fugaz
        if cuerpo < (h - l) * 0.3 and sombra_superior > cuerpo * 2 and sombra_inferior < cuerpo:
            patrones.append((df[ "datetime"].iloc[i], "Estrella Fugaz"))

        # Hombre Colgado
        if cuerpo < (h - l) * 0.3 and sombra_inferior > cuerpo * 2 and sombra_superior < cuerpo and c < o:
            patrones.append((df[ "datetime"].iloc[i], "Hombre Colgado"))

        # Martillo Invertido
        if cuerpo < (h - l) * 0.3 and sombra_superior > cuerpo * 2 and sombra_inferior < cuerpo and c > o:
            patrones.append((df[ "datetime"].iloc[i], "Martillo Invertido"))

    return patrones
