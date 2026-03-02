from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "API de preconteo activa"

@app.route("/preconteo")
def preconteo():

    partidos = ["Partido A", "Partido B", "Partido C"]

    data = []

    for mesa in range(1, 50):
        for partido in partidos:
            data.append({
                "mesa_id": mesa,
                "partido": partido,
                "candidato": f"Candidato {random.randint(1,10)}",
                "votos": random.randint(0, 300)
            })

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
