import streamlit as st
import pandas as pd
from supabase import create_client
from streamlit_autorefresh import st_autorefresh

# 🔄 Auto-refresh cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

st.set_page_config(page_title="Senado Colombia", layout="wide")

st.title("🗳️ Centro de Monitoreo Electoral – Senado Colombia")

# 🔐 Conexión a Supabase
SUPABASE_URL = "https://afpmkctzeeonkrlcimjf.supabase.co"
SUPABASE_KEY = "TU_ANON_KEY_AQUI"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    preconteo = supabase.table("resultados_preconteo").select("*").execute().data
    e14 = supabase.table("resultados_e14").select("*").execute().data
    mesas_totales = supabase.table("mesas").select("id_mesa").execute().data

except Exception:
    st.error("Error conectando con la base")
    st.stop()

# 🚫 Si no hay datos
if not preconteo:
    st.warning("Aún no hay datos de preconteo")
    st.stop()

df_pre = pd.DataFrame(preconteo)

# 📍 COBERTURA NACIONAL DE MESAS
total_mesas = len(mesas_totales)
mesas_reportadas = df_pre["mesa_id"].nunique()

if total_mesas > 0:
    porcentaje = (mesas_reportadas / total_mesas) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Mesas del país", total_mesas)
    col2.metric("Mesas reportadas", mesas_reportadas)
    col3.metric("Cobertura nacional", f"{porcentaje:.2f}%")

    st.progress(min(porcentaje / 100, 1.0))

    # 📈 INDICADOR DE ESTABILIDAD
    if porcentaje < 30:
        st.warning("Proyección temprana: resultados aún muy volátiles")
    elif porcentaje < 70:
        st.info("Proyección en consolidación: pueden existir cambios")
    else:
        st.success("Resultado altamente estable: tendencia casi definitiva")
else:
    st.warning("No hay mesas registradas aún en la base")

# 🧮 CONSOLIDACIÓN NACIONAL (base para D’Hondt)
df_partidos = df_pre.groupby("partido", as_index=False)["votos"].sum()
df_partidos = df_partidos.sort_values(by="votos", ascending=False)

st.subheader("📊 Votación Nacional por Partido")
st.bar_chart(df_partidos.set_index("partido"))

# 🏛️ MÉTODO D’HONDT
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

# 🏆 IDENTIFICAR SENADORES PROYECTADOS (listas preferentes)
st.subheader("🏆 Senadores proyectados por candidato")

df_candidatos = df_pre.groupby(
    ["partido", "candidato"], as_index=False
)["votos"].sum()

senadores = []

for partido, curules_partido in resultado.items():
    df_partido = df_candidatos[df_candidatos["partido"] == partido]
    df_partido = df_partido.sort_values(by="votos", ascending=False)
    ganadores = df_partido.head(curules_partido)

    if not ganadores.empty:
        senadores.append(ganadores)

if senadores:
    df_senadores = pd.concat(senadores)
    df_senadores = df_senadores.sort_values(by="votos", ascending=False)
    st.dataframe(df_senadores, use_container_width=True)
else:
    st.info("Aún no hay suficientes datos para proyectar candidatos")

# 🔍 COMPARACIÓN PRECONTEO VS E14
if preconteo and e14:
    df_e14 = pd.DataFrame(e14)

    df_compare = pd.merge(
        df_pre,
        df_e14,
        on=["mesa_id", "partido", "candidato"],
        suffixes=("_pre", "_e14"),
        how="inner"
    )

    df_compare["diferencia"] = df_compare["votos_pre"] - df_compare["votos_e14"]
    df_compare["porcentaje"] = (
        df_compare["diferencia"].abs() / df_compare["votos_e14"].replace(0, 1)
    ) * 100

    alertas = df_compare[df_compare["porcentaje"] > 5]

    st.subheader("🚨 Mesas con inconsistencias detectadas")

    if len(alertas) > 0:
        st.dataframe(alertas, use_container_width=True)
    else:
        st.success("No se detectan inconsistencias relevantes")

    # 📄 DETECCIÓN DE E14 ILEGIBLE
    df_e14_check = df_e14[
        (df_e14["votos"].isna()) |
        (df_e14["votos"] == 0)
    ]

    if len(df_e14_check) > 0:
        st.subheader("⚠️ E14 con posibles problemas de legibilidad")
        st.dataframe(df_e14_check, use_container_width=True)
        st.error("Estas mesas requieren revisión y posible reclamación")

# 📤 SECCIÓN OCR
st.divider()
st.subheader("📎 Subir E14 (OCR automático en desarrollo)")
uploaded_file = st.file_uploader("Cargar PDF o imagen", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    st.info("Archivo recibido. Próximo paso: procesar OCR y registrar votos automáticamente.")

st.caption("🔄 Sistema en actualización continua cada 5 segundos")
