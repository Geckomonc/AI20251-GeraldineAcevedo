from flask import Flask, jsonify, request
from loguru import logger
import pickle
import pandas as pd
import os
import subprocess

app = Flask(__name__)
train_status = "not training"
MODEL_PATH = "model.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

@app.route("/")
def index():
    return jsonify({"message": "API activa"})

@app.route("/train", methods=["GET"])
def train():
    global train_status
    if train_status == "training":
        return jsonify({"error": "ya se está entrenando el modelo"})

    train_status = "training"
    logger.info("Entrenando modelo...")

    result = subprocess.run([
        "python", "train.py",
        "--data_file", "train_data.csv",
        "--model_file", MODEL_PATH,
        "--overwrite_model"
    ], capture_output=True, text=True)

    train_status = "not training"

    if result.returncode == 0:
        logger.info("Entrenamiento completado")
        return jsonify({"message": "Entrenamiento completado correctamente"})
    else:
        logger.error("Error durante el entrenamiento")
        return jsonify({"error": result.stderr})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = data.get("features", None)
        if features is None:
            return jsonify({"error": "Debes enviar un JSON con la llave 'features'"})
        
        model = load_model()
        df = pd.DataFrame([features])
        pred = model.predict(df).tolist()[0]

        return jsonify({"prediction": pred})

    except Exception as e:
        logger.error(f"Error en la predicción: {e}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
