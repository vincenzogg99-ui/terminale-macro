import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.express as px

st.set_page_config(page_title="Macro Terminal 4.0", layout="wide")

# Configurazione API
API_KEY = st.secrets.get("FRED_API_KEY", "")
fred = Fred(api_key=API_KEY)

# CODICI AGGIORNATI E TESTATI (Questi sono i più stabili su FRED)
indicators = {
    'USA': 'CPIAUCSL',
    'Euro Area': 'CP0000EZ19M086NEST', 
    'UK': 'GBRCPIALLMINMEI',
    'Japan': 'JPNCPIALLMINMEI'
}

st.title("📊 Terminale Macro Aggiornato")

@st.cache_data(ttl=3600)
def get_data():
    all_data = {}
    for name, code in indicators.items():
        try:
            # Scarichiamo serie lunghe per assicurarci di coprire il 2026
            series = fred.get_series(code, observation_start='2022-01-01')
            all_data[name] = series.pct_change(periods=12) * 100
        except Exception as e:
            all_data[name] = None
            st.warning(f"Impossibile caricare {name}: {e}")
    return all_data

data_dict = get_data()

# Layout a 4 colonne
cols = st.columns(2)

for i, (nazione, series) in enumerate(data_dict.items()):
    col = cols[i % 2]
    with col:
        st.subheader(f"📈 {nazione}")
        if series is not None and not series.dropna().empty:
            # Ultimi 5 dati
            df_table = series.dropna().tail(5).sort_index(ascending=False)
            
            # Grafico
            fig = px.line(series.dropna().tail(24), title=f"Inflazione {nazione} (YoY %)")
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabella
            st.dataframe(df_table.rename("Inflazione %"), use_container_width=True)
        else:
            st.error(f"Dati non disponibili per {nazione}")
        st.markdown("---")
