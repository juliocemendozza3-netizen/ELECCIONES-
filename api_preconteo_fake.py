from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

PARTIDOS = [
    "Partido A",
    "Partido B",
    "Partido C",
    "Partido D"
]

@app.route("/preconteo")
def preconteo():
    data = []

    for mesa in range(1, 21):  # 20 mesas simuladas
        for partido in PARTIDOS:
            data.append({
                "mesa_id": mesa,
                "partido": partido,
                "candidato": f"Candidato {random.randint(1,5)}",
                "votos": random.randint(0, 300),
                "timestamp": str(datetime.datetime.now())
            })

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
