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

# Codici nazioni aggiornati al 2026
# Abbiamo selezionato i codici serie più recenti per evitare dati vecchi
indicators = {
    'USA': 'CPIAUCSL',
    'Euro Area': 'HICP01EZ19655DYLD',
    'UK': 'GBRCPIALLMINMEI',
    'Japan': 'JPNCPIALLMINMEI'
}

st.title("📊 Il Mio Terminale Macro")
st.markdown("Monitoraggio inflazione in tempo reale via FRED API")
st.markdown("---")

@st.cache_data(ttl=3600)
def get_macro_data():
    df_list = []
    for name, code in indicators.items():
        # Scarichiamo i dati dal 2023 per avere una vista pulita e recente
        series = fred.get_series(code, observation_start='2023-01-01')
        # Calcolo inflazione YoY in percentuale
        inflation = series.pct_change(periods=12) * 100
        df_list.append(pd.DataFrame({name: inflation}))
    return pd.concat(df_list, axis=1).dropna()

try:
    data = get_macro_data()
    
    # Debug: Verifica le date recenti
    with st.expander("🔍 Verifica dati: Date e Valori"):
        st.write(data.tail())

    # Metriche veloci
    cols = st.columns(4)
    for i, nazione in enumerate(indicators.keys()):
        val = data[nazione].iloc[-1]
        diff = val - data[nazione].iloc[-2]
        cols[i].metric(nazione, f"{val:.2f}%", f"{diff:.2f}%", delta_color="inverse")

    # Grafico
    fig = px.line(data, x=data.index, y=data.columns, 
                 template="plotly_dark", title="Inflazione YoY (%) - Dati Aggiornati")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Errore nel caricamento dati: {e}")
