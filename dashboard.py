import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
import requests

st_autorefresh(interval=5000, key="datarefresh")
st.set_page_config(page_title="Senado Colombia", layout="wide")

st.title("🗳️ Centro de Monitoreo Electoral – Senado Colombia")

SUPABASE_URL = "https://afpmkctzeeonkrlcimjf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmcG1rY3R6ZWVvbmtybGNpbWpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIzODgwNjcsImV4cCI6MjA4Nzk2NDA2N30.RDHiPO4dmwqClJPBLHWXzM-d6OROSQniKypko8GEYkc"

# 🔹 Conexión general
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 🔹 PRECONTEO desde API externa (Render)
   API_PRECONTEO = "https://api-preconteo.onrender.com/preconteo"
    try:
        preconteo = requests.get(API_PRECONTEO, timeout=10).json()
    except:
        preconteo = []

    # 🔹 E14 y mesas desde Supabase
    e14 = supabase.table("resultados_e14").select("*").execute().data
    mesas_totales = supabase.table("mesas").select("id_mesa").execute().data

except Exception as e:
    st.error(f"Error conectando con la base: {e}")
    st.stop()

# 🔹 Validación datos
if not preconteo:
    st.warning("Aún no hay datos de preconteo")
    st.stop()

df_pre = pd.DataFrame(preconteo)

# 🔹 Cobertura nacional
total_mesas = len(mesas_totales)
mesas_reportadas = df_pre["mesa_id"].nunique()

if total_mesas > 0:
    porcentaje = (mesas_reportadas / total_mesas) * 100
    col1, col2, col3 = st.columns(3)
    col1.metric("Mesas del país", total_mesas)
    col2.metric("Mesas reportadas", mesas_reportadas)
    col3.metric("Cobertura nacional", f"{porcentaje:.2f}%")
    st.progress(min(porcentaje / 100, 1.0))
else:
    st.warning("No hay mesas registradas aún en la base")

# 🔹 Consolidación por partido
df_partidos = df_pre.groupby("partido", as_index=False)["votos"].sum()
df_partidos = df_partidos.sort_values(by="votos", ascending=False)

st.subheader("📊 Votación Nacional por Partido")
st.bar_chart(df_partidos.set_index("partido"))

# 🔹 Método D’Hondt
curules = 100
cocientes = []

for _, row in df_partidos.iterrows():
    for i in range(1, curules + 1):
        cocientes.append((row["partido"], row["votos"] / i))

cocientes.sort(key=lambda x: x[1], reverse=True)

resultado = {}
for partido, _ in cocientes[:curules]:
    resultado[partido] = resultado.get(partido, 0) + 1

df_curules = pd.DataFrame(
    list(resultado.items()), columns=["Partido", "Curules"]
).sort_values(by="Curules", ascending=False)

st.subheader("🏛️ Proyección de Curules")
st.dataframe(df_curules, use_container_width=True)
