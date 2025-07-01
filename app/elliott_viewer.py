import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go
from src.api.yahoo_data_api import descargar_datos_yahoo
from src.analysis.elliott import detectar_ondas_elliott

st.set_page_config(page_title="Ondas de Elliott", layout="wide")

st.title("📈 Detección Automática de Ondas de Elliott")
ticker = st.text_input("Símbolo (ej. BTC-USD, AAPL)", "BTC-USD")
intervalo = st.selectbox("Intervalo", ["5m", "15m", "1h", "1d"], index=2)
periodo = st.selectbox("Periodo", ["7d", "30d", "60d", "1y"], index=2)
umbral = st.slider("Umbral ZigZag (%)", 0.5, 10.0, 2.0) / 100

if st.button("📈 Detectar Ondas"):
    with st.spinner("Procesando datos..."):
        try:
            df = descargar_datos_yahoo(ticker, intervalo, periodo)
            ondas = detectar_ondas_elliott(df, umbral)
            st.write("🔍 Debug - Ondas detectadas:", ondas)

            st.success(f"Se detectaron {len(ondas)} secuencias de ondas.")
            fig = go.Figure()

            # Candlestick base
            fig.add_trace(go.Candlestick(
                x=df['datetime'],
                open=df['open'], high=df['high'],
                low=df['low'], close=df['close'],
                name='Precio'
            ))

            # Ondas detectadas
            for i, onda in enumerate(ondas):
                x = [p[0] for p in onda]
                y = [p[1] for p in onda]
                fig.add_trace(go.Scatter(
                    x=x, y=y,
                    mode='lines+markers+text',
                    name=f'Onda {i+1}',
                    text=[f'{j+1}' for j in range(len(x))],
                    textposition="top center"
                ))

            fig.update_layout(title="Ondas de Elliott Detectadas", xaxis_title="Fecha", yaxis_title="Precio")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")
