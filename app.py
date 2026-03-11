import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.express as px

# Configurazione Pagina
st.set_page_config(page_title="Macro Terminal", layout="wide", page_icon="📈")

# Recupero API Key dai Secrets di Streamlit
try:
    API_KEY = st.secrets["FRED_API_KEY"]
except:
    st.error("Errore: Inserisci la tua FRED_API_KEY nei 'Secrets' di Streamlit!")
    st.stop()

fred = Fred(api_key=API_KEY)

# Codici nazioni (USA, Eurozona, UK, Giappone)
indicators = {
    'USA': 'CPIAUCSL',
    'Euro Area': 'CP0000EZ19M086NEST',
    'UK': 'GBRCPIALLMINMEI',
    'Japan': 'JPNCPIALLMINMEI'
}

st.title("📊 Il Mio Terminale Macro")
st.markdown("---")

@st.cache_data(ttl=3600)
def get_macro_data():
    df_list = []
    for name, code in indicators.items():
        # Scarichiamo dal 2021
        series = fred.get_series(code, observation_start='2021-01-01')
        # Calcolo inflazione YoY in percentuale
        inflation = series.pct_change(periods=12) * 100
        df_list.append(pd.DataFrame({name: inflation}))
    return pd.concat(df_list, axis=1).dropna()

try:
    data = get_macro_data()
    
    # --- DEBUG: Questa tabella ti mostra le date esatte ---
    with st.expander("🔍 Debug: Vedi dati grezzi e date"):
        st.write(data.tail())
    # ------------------------------------------------------

    # Metriche veloci
    cols = st.columns(4)
    for i, nazione in enumerate(indicators.keys()):
        val = data[nazione].iloc[-1]
        diff = val - data[nazione].iloc[-2]
        cols[i].metric(nazione, f"{val:.2f}%", f"{diff:.2f}%", delta_color="inverse")

    # Grafico
    fig = px.line(data, x=data.index, y=data.columns, 
                 template="plotly_dark", title="Andamento Inflazione YoY %")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Errore: {e}")
