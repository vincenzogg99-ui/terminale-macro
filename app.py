import streamlit as st
import pandas as pd
from fredapi import Fred

# Configurazione
st.set_page_config(page_title="Macro Terminal", layout="wide")

# Prova a prendere la chiave, se fallisce avvisa ma non bloccare tutto
API_KEY = st.secrets.get("FRED_API_KEY", "")
fred = Fred(api_key=API_KEY)

indicators = {
    'USA': 'CPIAUCSL',
    'Euro Area': 'HICP01EZ19655DYLD'
}

st.title("📊 Macro Terminal (Modalità Sicura)")

@st.cache_data(ttl=3600)
def get_safe_data():
    data = {}
    for name, code in indicators.items():
        try:
            series = fred.get_series(code, observation_start='2024-01-01')
            data[name] = series.pct_change(periods=12) * 100
        except Exception:
            continue # Se una nazione fallisce, passa alla prossima
    return pd.DataFrame(data).dropna()

try:
    df = get_safe_data()
    if not df.empty:
        st.line_chart(df)
        st.write("Ultimi dati:", df.tail())
    else:
        st.error("Nessun dato recuperato. Controlla la API KEY o la connessione a FRED.")
except Exception as e:
    st.write(f"Errore: {e}")
