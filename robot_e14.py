import time
import requests
from supabase import create_client

SUPABASE_URL = "https://afpmkctzeeonkrlcimjf.supabase.co"
SUPABASE_KEY = "TU_ANON_KEY_AQUI"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def procesar_pdf(url):
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        print("PDF descargado correctamente")
        # Aquí luego pondremos OCR real
    else:
        print("Error descargando PDF")

while True:
    print("Robot activo, esperando tareas...")
    time.sleep(60)
