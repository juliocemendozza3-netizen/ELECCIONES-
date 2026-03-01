import time
import requests

while True:
    print("Robot activo. Probando conexión...")

    try:
        r = requests.get("https://www.google.com", timeout=10)
        print("Conexión OK:", r.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(60)
