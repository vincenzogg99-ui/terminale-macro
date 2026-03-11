import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import plotly.express as px

st.set_page_config(page_title="Macro Terminal 5.0", layout="wide")

# Lista paesi OCSE (Codici standard)
# USA, GBR (UK), JPN (Giappone), EA19 (Euro Area)
countries = ['USA', 'GBR', 'JPN', 'EA19']

@st.cache_data(ttl=3600)
def get_oecd_data():
    # L'OCSE pubblica l'inflazione (CPI) sotto il set di dati "PRICES_CPI"
    try:
        # Recuperiamo i dati dall'OCSE
        df = web.DataReader('PRICES_CPI', 'oecd', start='2025-01-01')
        # Filtriamo per la variazione annuale (YoY)
        # Nota: L'OCSE richiede una pulizia dei dati più accurata
        return df
    except Exception as e:
        st.error(f"Errore caricamento OCSE: {e}")
        return None

st.title("📊 Terminale Macro (Fonte: OECD - Dati aggiornati)")

data = get_oecd_data()

if data is not None:
    st.write("Dati caricati correttamente!")
    st.write(data.tail()) # Controlliamo subito l'ultima data disponibile
else:
    st.warning("Stiamo riscontrando problemi con l'API OCSE. Considera il caricamento via file CSV.")
