from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# 🔹 Datos simulados (luego vendrán de OCR/API real)
preconteo_simulado = [
    {"mesa_id": 1, "partido": "Partido A", "votos": 120},
    {"mesa_id": 1, "partido": "Partido B", "votos": 80},
    {"mesa_id": 2, "partido": "Partido A", "votos": 95},
    {"mesa_id": 2, "partido": "Partido B", "votos": 110},
]

@app.get("/")
def home():
    return {"status": "Robot electoral activo", "hora": str(datetime.now())}

@app.get("/preconteo")
def obtener_preconteo():
    return preconteo_simulado
