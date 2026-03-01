import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 🔄 Auto-refresh cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

st.set_page_config(page_title="Senado Colombia", layout="wide")

st.title("🗳️ Proyección Senado Colombia en Tiempo Real")

# 🔐 Conexión a Supabase
SUPABASE_URL = "https://afpmkctzeeonkrlcimjf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmcG1rY3R6ZWVvbmtybGNpbWpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIzODgwNjcsImV4cCI6MjA4Nzk2NDA2N30.RDHiPO4dmwqClJPBLHWXzM-d6OROSQniKypko8GEYkc"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("votos").select("*").execute()
    data = response.data
except Exception as e:
    st.error("Error conectando a la base de datos")
    st.stop()

# 🚫 Si no hay datos
if not data:
    st.warning("Aún no hay datos en la base")
    st.stop()

# 📊 DataFrame
df = pd.DataFrame(data)

# 🧮 Consolidar votos por partido
df_partidos = df.groupby("partido", as_index=False)["votos"].sum()
df_partidos = df_partidos.sort_values(by="votos", ascending=False)

st.subheader("📊 Votos por Partido")
st.bar_chart(df_partidos.set_index("partido"))

# 🏛️ Método D’Hondt
curules = 100
cocientes = []

for _, row in df_partidos.iterrows():
    for i in range(1, curules + 1):
        cocientes.append((row["partido"], row["votos"] / i))

cocientes.sort(key=lambda x: x[1], reverse=True)

resultado = {}
for partido, _ in cocientes[:curules]:
    resultado[partido] = resultado.get(partido, 0) + 1

# 📈 Mostrar curules ordenadas
df_curules = pd.DataFrame(
    list(resultado.items()), columns=["Partido", "Curules"]
).sort_values(by="Curules", ascending=False)

st.subheader("🏛️ Curules Proyectadas")
st.dataframe(df_curules, use_container_width=True)

st.caption("🔄 Actualización automática cada 5 segundos")

# 📤 Sección futura para OCR
st.divider()
st.subheader("📎 Subir E14 (Próximamente OCR automático)")
uploaded_file = st.file_uploader("Cargar PDF o imagen", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    st.info("Archivo recibido. Próximo paso: procesar OCR y subir votos automáticamente.")
