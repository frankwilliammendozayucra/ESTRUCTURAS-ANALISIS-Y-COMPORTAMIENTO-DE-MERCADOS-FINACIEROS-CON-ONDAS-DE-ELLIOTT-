import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from data.fetcher import obtener_datos
from analysis.elliott import detectar_extremos, detectar_ondas_elliott, detectar_correctivas
from config import ACTIVOS, TEMPORALIDADES, LIMITE_DIAS

with open("style.css") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ————————————————————————————————————————————————————————

st.title("🎯 Backtest Ondas de Elliott")

# Parámetros en sidebar
st.sidebar.header("⚙️ Parámetros")
interv_select = st.sidebar.multiselect("Intervalos:", TEMPORALIDADES, default=TEMPORALIDADES)
activos_select = st.sidebar.multiselect("Activos:", ACTIVOS, default=ACTIVOS)

if st.sidebar.button("▶️ Ejecutar análisis"):
    for intervalo in interv_select:
        st.header(f"⏱ Intervalo: {intervalo}")
        dias = LIMITE_DIAS.get(intervalo, 30)
        fecha_inicio = datetime.today().date() - timedelta(days=dias)
        fecha_fin = datetime.today().date()

        resumen = []
        for ticker in activos_select:
            df = obtener_datos(ticker, intervalo, fecha_inicio, fecha_fin)
            if df is None or df.empty:
                resumen.append({
                    "Activo": ticker, "Señales": 0,
                    "Aciertos": 0, "% Acierto": 0.0,
                    "P&L Medio (%)": 0.0
                })
                continue

            close = df["Close"].squeeze()
            extremos = detectar_extremos(df)
            ondas = detectar_ondas_elliott(df, extremos, rci=None)

            total, hits, pl_list = 0, 0, []
            detalle = []
            for onda in ondas:
                corr = detectar_correctivas(df, onda)
                if not corr:
                    continue
                idxC = corr[2]
                try:
                    precioC = float(close.iloc[idxC])
                    siguiente = float(close.iloc[idxC + 1])
                except Exception:
                    continue
                total += 1
                acierto = siguiente > precioC
                if acierto:
                    hits += 1
                pl_list.append((siguiente - precioC) / precioC * 100)
                detalle.append({
                    "Timestamp": df.index[idxC],
                    "Precio C": round(precioC, 4),
                    "Acierto": "✅" if acierto else "❌"
                })

            tasa   = hits / total * 100 if total else 0.0
            avg_pl = sum(pl_list) / len(pl_list) if pl_list else 0.0
            resumen.append({
                "Activo": ticker,
                "Señales": total,
                "Aciertos": hits,
                "% Acierto": round(tasa, 2),
            })

            if detalle:
                st.subheader(f"Detalle de señales para {ticker}")
                df_det = pd.DataFrame(detalle).set_index("Timestamp")
                st.table(df_det)

        st.subheader("📊 Resumen general")
        df_res = pd.DataFrame(resumen).set_index("Activo")
        st.dataframe(df_res)
