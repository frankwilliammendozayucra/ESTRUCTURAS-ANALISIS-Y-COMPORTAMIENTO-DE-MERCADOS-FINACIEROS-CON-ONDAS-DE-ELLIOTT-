import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.utils.alertas import enviar_alerta_telegram
from src.analysis.fibonacci import calcular_fibonacci
from src.api.yahoo_data_api import descargar_datos_yahoo
from src.analysis.candlestick import detectar_patrones_velas
from src.analysis.harmonic_patterns import detectar_zigzag, detectar_patrones_armonicos
from src.analysis.elliott import detectar_ondas_elliott
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.set_page_config(page_title="Análisis Técnico", layout="wide")
st_autorefresh(interval=60000, key="refresh")

st.title("📈 Análisis Técnico en Tiempo Real")
st.markdown("Este panel detecta **patrones de velas japonesas**, **patrones armónicos** y muestra un **gráfico de velas japonesas** utilizando datos de Yahoo Finance.")

# Parámetros de entrada
ticker = st.text_input("Símbolo del activo", "BTC-USD")
intervalo = st.selectbox("Intervalo de velas", ["5m", "15m", "1h", "1d"], index=2)
periodo = st.selectbox("Rango de datos", ["7d", "30d", "60d", "1y"], index=2)
umbral_zigzag = st.slider("Umbral ZigZag (%)", 0.5, 10.0, 2.0) / 100


with st.spinner("Descargando y analizando datos..."):
    
        try:
            TOKEN = "7975412807:AAEg-0KMYXC6uoKR-q2XKnxwsTKkYXNSWHk"  # ➤ reemplaza por el token real que te dio @BotFather
            CHAT_ID = "7284817188"  # ➤ tu chat ID numérico
            
            df = descargar_datos_yahoo(ticker, intervalo, periodo)
            st.success("Datos cargados correctamente.")

# Gráfico de velas japonesas
            st.subheader("📊 Gráfico de Velas Japonesas (Candlestick)")
            fig_candle = go.Figure(data=[go.Candlestick(
                x=df['datetime'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )])
            fig_candle.update_layout(
                xaxis_title="Fecha",
                yaxis_title="Precio",
                template="plotly_dark",
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig_candle, use_container_width=True)

# Análisis de velas
            patrones_velas = detectar_patrones_velas(df)
            st.subheader("🕯️ Patrones de Velas Detectados")
            if patrones_velas:
                for tiempo, tipo in patrones_velas[-5:]:
                    try:
                        fecha_formateada = pd.to_datetime(tiempo).strftime("%Y-%m-%d ")
                    except:
                        fecha_formateada = str(tiempo)

                    st.markdown(f"🔹 **{tipo}** detectado el **{fecha_formateada}**")

            else:
                st.info("No se detectaron patrones de velas.")


            # Enviar alerta si se detectan patrones de vela
            if patrones_velas:
                ultimo_patron = patrones_velas[-1]
                mensaje = f"🚨 patron de vela detectado: {ultimo_patron[1]} en {ultimo_patron[0]}"
                enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje)



# Análisis armónico
            pivotes = detectar_zigzag(df, threshold=umbral_zigzag)
            patrones_armonicos = detectar_patrones_armonicos(pivotes)
            st.subheader("🔺 Patrones Armónicos")

            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(df["datetime"], df["close"], label="Precio", color="black")

            if patrones_armonicos:
                for nombre, i in patrones_armonicos:
                    puntos = pivotes[i:i+5]
                    x = [p[0] for p in puntos]
                    y = [p[1] for p in puntos]
                    ax.plot(x, y, marker='o', label=nombre)
                ax.set_title(f"Patrones Armónicos - {ticker}")
                ax.legend()
                st.success(f"Se detectaron: {[p[0] for p in patrones_armonicos]}")
            else:
                st.warning("No se detectaron patrones armónicos.")

            ax.set_xlabel("Fecha")
            ax.set_ylabel("Precio")
            ax.grid(True)
            st.pyplot(fig)

            for nombre, i in patrones_armonicos[-1:]:
                mensaje = f"🔺 Patrón armónico detectado: {nombre} en punto {pivotes[i][0] if isinstance(pivotes, list) else pivotes.iloc[i, 0]}"
                enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje)

#fibonacci
            st.subheader("📐 Retrocesos de Fibonacci")

            niveles = calcular_fibonacci(df)

            fig_fibo, ax_fibo = plt.subplots(figsize=(12, 5))
            ax_fibo.plot(df.index, df['close'], label='Precio', color='black')

            for nivel, precio in niveles.items():
                ax_fibo.axhline(y=precio, linestyle='--', alpha=0.7, label=f"{nivel} - {precio:.2f}")

            ax_fibo.set_title(f"Niveles de Fibonacci - {ticker}")
            ax_fibo.set_xlabel("Tiempo")
            ax_fibo.set_ylabel("Precio")
            ax_fibo.legend()
            st.pyplot(fig_fibo)
            for nombre, i in patrones_armonicos[-1:]:
                mensaje = f"🔺 Patrón armónico detectado: {nombre} en punto {pivotes[i][0]}"
                enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje)
            



            precio_actual = df['close'].iloc[-1]
            for nivel, precio in niveles.items():
                if abs(precio_actual - precio) / precio < 0.01:  # 1% de tolerancia
                    mensaje = f"📐 Precio cerca del nivel Fibonacci {nivel} ({precio:.2f})"
                    enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje)

#ondas de elliott

            st.subheader("🌊 Ondas de Elliott Detectadas")
            ondas = detectar_ondas_elliott(df, umbral_zigzag)

            if ondas:
                fig_elliott = go.Figure()

                # Velas base
                fig_elliott.add_trace(go.Candlestick(
                    x=df['datetime'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='Precio'
                ))  

                # Ondas detectadas
                for i, onda in enumerate(ondas):
                    x = [p[0] for p in onda]
                    y = [p[1] for p in onda]
                    fig_elliott.add_trace(go.Scatter(
                        x=x, y=y,
                        mode='lines+markers+text',
                        name=f'Onda {i+1}',
                        text=[f'{j+1}' for j in range(len(x))],
                        textposition="top center"
                    ))

                fig_elliott.update_layout(
                    title=f"Ondas de Elliott - {ticker}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_elliott, use_container_width=True)
                st.success(f"Se detectaron {len(ondas)} secuencias de ondas.")
            else:
                st.warning("No se detectaron ondas de Elliott.")
            mensaje = f"🌊 Se detectaron {len(ondas)} secuencias de ondas de Elliott"
            enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje)

        except Exception as e:
            st.error(f"❌ Error durante el análisis: {e}")
        if st.button("📲 Probar Alerta Telegram"):
                mensaje_prueba = "✅ Alerta de prueba enviada desde Streamlit"
                if enviar_alerta_telegram(TOKEN, CHAT_ID, mensaje_prueba):
                    st.success("Mensaje de prueba enviado a Telegram ✅")
                else:
                    st.error("❌ Error al enviar mensaje. Verifica el token o el chat ID.")
