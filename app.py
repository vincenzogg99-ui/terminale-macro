import streamlit as st
import pandas as pd
from fredapi import Fred
import plotly.express as px

st.set_page_config(page_title="Macro Terminal Pro", layout="wide")

# Configurazione API
API_KEY = st.secrets.get("FRED_API_KEY", "")
fred = Fred(api_key=API_KEY)

# Codici serie aggiornati per i 4 stati
indicators = {
    'USA': 'CPIAUCSL',
    'Euro Area': 'HICP01EZ19655DYLD',
    'UK': 'GBRCPIALLMINMEI',
    'Japan': 'JPNCPIALLMINMEI'
}

st.title("📊 Terminale Macro Economico: 4 Nazioni")

@st.cache_data(ttl=3600)
def get_data():
    full_data = {}
    for name, code in indicators.items():
        try:
            series = fred.get_series(code, observation_start='2023-01-01')
            full_data[name] = series.pct_change(periods=12) * 100
        except:
            continue
    return full_data

data_dict = get_data()

# Creazione delle 4 colonne per i grafici
cols = st.columns(2) # 2x2 grid

for i, (nazione, series) in enumerate(data_dict.items()):
    col = cols[i % 2]
    
    with col:
        st.subheader(f"📈 {nazione}")
        # Pulizia dati per mostrare solo gli ultimi 5
        df_plot = series.dropna().tail(24) # Dati per il grafico
        df_table = series.dropna().tail(5).sort_index(ascending=False) # Solo ultimi 5
        
        # Grafico
        fig = px.line(df_plot, title=f"Inflazione {nazione} (YoY %)")
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabella ultimi 5
        st.write("Ultimi 5 mesi:")
        st.dataframe(df_table.rename("Inflazione %"), use_container_width=True)
        st.markdown("---")

st.caption("Dati estratti via FRED API")
