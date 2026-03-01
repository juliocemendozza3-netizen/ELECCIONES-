import requests
import os

CARPETA = "e14_descargados"
os.makedirs(CARPETA, exist_ok=True)

def descargar(url, nombre):
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        with open(os.path.join(CARPETA, nombre), "wb") as f:
            f.write(r.content)
        print("Descargado:", nombre)
    else:
        print("Error:", r.status_code)

# EJEMPLO CON TU ENLACE
url = "https://congreso2022.registraduria.gov.co/verE14Escru?src=TU_SRC&token=TU_TOKEN"

descargar(url, "mesa_prueba.pdf")
