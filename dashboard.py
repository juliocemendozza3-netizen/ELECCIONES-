import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 🔹 Auto-refresh cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

st.title("Proyección Senado Colombia en Tiempo Real")

# 🔹 Conexión a Supabase
SUPABASE_URL = "https://afpmkctzeeonkrlcimjf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmcG1rY3R6ZWVvbmtybGNpbWpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIzODgwNjcsImV4cCI6MjA4Nzk2NDA2N30.RDHiPO4dmwqClJPBLHWXzM-d6OROSQniKypko8GEYkc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Leer datos en tiempo real
response = supabase.table("votos").select("*").execute()
data = response.data

if not data:
    st.warning("Aún no hay datos en la base")
    st.stop()

df = pd.DataFrame(data)

# 🔹 Consolidar votos por partido
df_partidos = df.groupby("partido", as_index=False)["votos"].sum()

st.subheader("Votos por partido")
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

st.subheader("Curules proyectadas")
st.write(resultado)

st.caption("Actualización automática cada 5 segundos")
