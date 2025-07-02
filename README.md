# AI20251-GeraldineAcevedo
Modelo para la competencia Kaggle [https://www.kaggle.com/competitions/pkdd-15-predict-taxi-service-trajectory-i/data)
## Estudiante
- Geraldine Acevedo Restrepo 1036689211 Ingenieria de Sistemas

## Entregas

### Fase-1:
1. Abrir el archivo fase-1.ipynb en colab que se encuentra en la carpeta fase-1.
2. Guardar la key de kaggle llamada kaggle.json (Es la que te permite autentificarte y descargar la información del modelo) en la carpeta de archivos de colab.

   ![image](https://github.com/user-attachments/assets/403e93af-9514-4cbf-8c4b-793ea7b01709)

3. Correr los códigos de colab de arriba hacia abajo. (Es importante seguir este orden)
4. El resto de información se encuentran dentro del colab, tanto las descripciones de lo que hace cada celda de código como para que sirve cada paso.
5. Cuando hayas corrido todas las lineas se generará la predicción para Kaggle en la carpeta content y se llamará submission.csv


### Fase-2:
Contenido de la carpeta fase-2:

![image](https://github.com/user-attachments/assets/41659755-a864-4e95-bb50-18c71f4efc86)

Tenemos la carpeta scripts que contiene los scripts:
- model.py  : Este script realiza lo que pasa en la primera entrega (preparación de datos).
- train.py  : Este script se encarga de entrenar los datos del modelo.
- predict.py : Este script se encarga de hacer las predicciones.
- evaluation.py  : Carga las predicciones y los valores reales desde archivos CSV, compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia), imprime la precisión como promedio de aciertos por fila.

Tenemos el archivo dockerfile que me permite construir la imagen docker para el proyecto, con:
- Python 3.11.
- Todas las dependencias necesarias.
- Scripts (model.py, predict.py, evaluation.py, etc.) dentro del contenedor.

Tenemos el archivo requirements.txt que contiene las dependencias necesarias para ejecutar el proyecto.

Paso a paso para ejecutar el proyecto:

1. Descargar el .zip o clonar el repositorio con toda la información necesaria para el modelo dockerizado.

   ![image](https://github.com/user-attachments/assets/08193430-85b2-4781-9179-975144f0df69)

2. Guardar la key de kaggle llamada kaggle.json (Es la que te permite autentificarte y descargar la información del modelo) en la carpeta principal.

   ![image](https://github.com/user-attachments/assets/6be967e3-c3f5-4286-9f83-1999d26ee0ed)

NOTA: La key debe llamarse exactamente como se ve en la imagen

3. En la terminal donde se encuentra el proyecto usar el comando que nos permitira construir una imagen Docker usando el Dockerfile que está en el directorio actual (.). El flag -t kaggle_model significa que estamos nombrando a la imagen: kaggle_model.

   ```
   docker build -t kaggle_model .
   ```
   ![image](https://github.com/user-attachments/assets/b04d4353-df78-4834-98f2-eb42fe220acf)

4. Luego utilizar el comando que nos permitira ejecutar un contenedor interactivo desde la imagen que hemos construido (kaggle_model)
   
   ```
   docker run -it kaggle_model
   ```
   ![image](https://github.com/user-attachments/assets/09388966-f84c-47f6-adf3-745068302e55)

5. Al entrar al contenedor ejecutaremos el script que se encargara de correr la preparación de datos del modelo
   
   ```
   python3 scripts/model.py
   ```
   - Este script realiza lo que pasa en la primera entrega (preparación de datos)
   - Además se crean los archivos csv (train_data.csv, test_data_input.csv, test_data_target.csv)
   
   ![image](https://github.com/user-attachments/assets/0e72ff82-3f5b-46ac-a916-a6c78f5cc1e0)

6. Luego ejecutaremos el script:
   
   ```
   python3 scripts/train.py --data_file train_data.csv --model_file model.pkl --overwrite_model
   ```
   - Haremos el entrenamiento del modelo
   
   ![image](https://github.com/user-attachments/assets/5a4c7d9b-d8e8-4eca-a697-2ff69023b35c)

7. Luego ejecutaremos el script:
    
   ```
   python3 scripts/predict.py --input_file test_data_input.csv --model_file model.pkl --predictions_file test_predictions.csv
   ```
   - Haremos las predicciones

   ![image](https://github.com/user-attachments/assets/64740d77-209c-4c7a-976d-91937ec14a48)


8. Ejecutaremos el script:

   ```
   python3 scripts/evaluation.py
   ```
   - Carga las predicciones y los valores reales desde archivos CSV
   - Compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia)
   - Imprime la precisión como promedio de aciertos por fila

   ![image](https://github.com/user-attachments/assets/2c1610d3-65d4-4ca1-9828-1ce14e08e5d4)

Finalmente por consola deberas tener en la terminal:

![image](https://github.com/user-attachments/assets/5b67d0fb-373d-46a5-9ded-a8bc57b8f5cf)

Los archivos finales en el container se verán así:

![image](https://github.com/user-attachments/assets/993683ce-7ad0-4a4c-a678-97d0c491b69b)

Y en los logs del Docker Desktop del container de docker tendremos una salida similar a la de la terminal

![image](https://github.com/user-attachments/assets/4d3f4875-f614-47c4-9e59-4003edb442fe)

### Fase-3:
Contenido de la carpeta fase-3:

![image](https://github.com/user-attachments/assets/e6509e33-1186-484b-8345-7e74ddb64a23)

Tenemos la carpeta scripts que contiene los scripts:
- model.py  : Este script realiza lo que pasa en la primera entrega (preparación de datos).
- train.py  : Este script se encarga de entrenar los datos del modelo.
- predict.py : Este script se encarga de hacer las predicciones.
- evaluation.py  : Carga las predicciones y los valores reales desde archivos CSV, compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia), imprime la precisión como promedio de aciertos por fila.
- apirest.py: Este script se encarga de implementar una API REST con Flask. Expone dos endpoints:
  - /train: reentrena el modelo al recibir una petición GET.
  - /predict: recibe un JSON con features y devuelve la predicción del modelo.
- client.py :  Cliente HTTP para probar los endpoints /train y /predict mediante peticiones programadas con requests.
  
Los archivos
- model.pkl : Archivo binario que contiene el modelo entrenado con scikit-learn.
- train_data.csv : Archivo generado por model.py que contiene las características y las etiquetas de entrenamiento utilizadas para entrenar el modelo.
  
Tenemos el archivo dockerfile que me permite construir la imagen docker para el proyecto, con:
- Python 3.11.
- Todas las dependencias necesarias.
- Scripts (model.py, predict.py, evaluation.py, etc.) dentro del contenedor.

Tenemos el archivo requirements.txt que contiene las dependencias necesarias para ejecutar el proyecto.

Paso a paso para ejecutar el proyecto:

1. Descargar el .zip o clonar el repositorio con toda la información necesaria para el modelo dockerizado.

   ![image](https://github.com/user-attachments/assets/08193430-85b2-4781-9179-975144f0df69)

2. Guardar la key de kaggle llamada kaggle.json (Es la que te permite autentificarte y descargar la información del modelo) en la carpeta principal.

   ![image](https://github.com/user-attachments/assets/409128a6-720b-4cd4-b1fb-cc69367f627a)

   NOTA: La key debe llamarse exactamente como se ve en la imagen

3. Construir la imagen Docker con el siguiente comando:
   ```
   docker build -t api-rest .
   ```
   Este comando crea una imagen llamada api-rest utilizando el Dockerfile ubicado en el directorio actual. Se instalarán las dependencias necesarias y se copiarán todos los archivos al     contenedor.
   
   ![image](https://github.com/user-attachments/assets/730d30a2-b570-4019-a7be-3aef8256c9c5)

4. Ejecutar el contenedor y exponer la API en el puerto 5001:
      ```
   docker run -p 5001:5001 api-rest
   ```
   Este comando inicia el contenedor con la API REST en ejecución. Podrás acceder a los endpoints http://localhost:5001/train y http://localhost:5001/predict.

   ![image](https://github.com/user-attachments/assets/6133f8e5-8508-4268-b854-417664e53caf)

Finalmente al hacer las pruebas en postman se debería ver como algo así:

- http://localhost:5001/train
  
![image](https://github.com/user-attachments/assets/3d15795a-916b-4c73-9042-d2a1f9ebac12)

- http://localhost:5001/predict
  
Escoger en body la opción raw

json hipotético
{
  "features": [1, 0, 0, 1, 0, 0, -8.611, 41.145, 0.005, 0.003]
}

![image](https://github.com/user-attachments/assets/84a33141-d1bc-48e5-8f49-953b62be26a3)

Nota: Recuerde colocar en el body de la petición el json y escoger raw, como se ve en la imagen.


