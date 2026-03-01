import streamlit as st
import pandas as pd

st.title("Proyección Senado Colombia")
# Leer datos reales desde CSV
df = pd.read_csv("datos.csv")
st.subheader("Votos por partido")
st.bar_chart(df.set_index("Partido"))

# Método D’Hondt
curules = 100
cocientes = []

for _, row in df.iterrows():
    for i in range(1, curules+1):
        cocientes.append((row["Partido"], row["Votos"]/i))

cocientes.sort(key=lambda x: x[1], reverse=True)

resultado = {}
for partido, _ in cocientes[:curules]:
    resultado[partido] = resultado.get(partido, 0) + 1

st.subheader("Curules proyectadas")
st.write(resultado)
