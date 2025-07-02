import pandas as pd
import numpy as np

# Carga las predicciones y los valores reales desde archivos CSV
preds = pd.read_csv('/app/test_predictions.csv').values
targets = pd.read_csv('/app/test_data_target.csv').values

# Compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia)
acc = np.mean(np.all(np.isclose(preds, targets), axis=1))

# Imprime la precisión como promedio de aciertos por fila
print(f'accuracy on test {acc:.3f}')
