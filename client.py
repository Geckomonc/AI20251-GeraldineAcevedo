import requests

# Llamar al endpoint de predicción
data = {
    "features": [1, 0, 0, 1, 0, 0, -8.611, 41.145, 0.005, 0.003]  # ejemplo
}
res = requests.post("http://localhost:5001/predict", json=data)
print("Predicción:", res.json())

# Llamar al endpoint de entrenamiento
res = requests.get("http://localhost:5001/train")
print("Entrenamiento:", res.json())
