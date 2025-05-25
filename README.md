# AI20251-GeraldineAcevedo
Modelo para la competencia Kaggle [https://www.kaggle.com/competitions/pkdd-15-predict-taxi-service-trajectory-i/data)
## Estudiante
- Geraldine Acevedo Restrepo 1036689211 Ingenieria de Sistemas

## Entregas
Fase-1:
1. Descargar el .zip de la competición ECML/PKDD 15: Taxi Trajectory Prediction (I),
   se encuentra en el siguiente link: https://drive.google.com/drive/folders/1jw602ytQua9qFIC9btD-ZqdIAd1TGhyo?usp=sharing
3. Dar clic en fase-1.ipynb que se encuentra en este github, es el colab en el que se realizó el entrenamiento y la predicción del modelo.
4. En la previsualización del colab fase-1.ipynb dar clic en open in colab que te dirigirá al colab.
5. Subir el .zip que has descargado del link del punto 1 a la parte de archivos de colab, en la carpeta content. (Si no lo haces de esta forma no va a funcionar)
   ![image](https://github.com/user-attachments/assets/180785c3-b5e0-408d-8a20-927d6a24f7f4)
6. Cuando haya terminado de cargar el .zip en la carpeta, proceder a correr los códigos de colab de arriba hacia abajo. (Es importante seguir este orden)
7. El resto de información se encuentran dentro del colab, tanto las descripciones de lo que hace cada celda de código como para que sirve cada paso.
8. Cuando hayas corrido todas las lineas se generará la predicción para Kaggle en la carpeta content y se llamará submission.csv


Fase-2:
Contenido del repositorio:

![image](https://github.com/user-attachments/assets/a8f2d06e-7773-4ff7-9833-cbcb3e407de1)

Tenemos la carpeta scripts que contiene los scripts:
- model.py  : Este script realiza lo que pasa en la primera entrega (preparación de datos, uso del modelo escogido y evaluación de modelo).
- train.py  : Este script se encarga de entrenar los datos del modelo.
- predict.py : Este script se encarga de hacer las predicciones.
- evaluation.py  : Carga las predicciones y los valores reales desde archivos CSV, compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia), imprime la precisión como promedio de aciertos por fila.

Tenemos el archivo dockerfile que me permite construir la imagen docker para el proyecto, este archivo contiene:
- Tenga Python 3.11.
- Instale todas las dependencias necesarias.
- Copie el código y datos.
- Ejecutar los scripts (model.py, predict.py, evaluation.py, etc.) dentro del contenedor.

Tenemos el archivo requirements.txt que contiene las dependencias necesarias para ejecutar el proyecto.

Paso a paso para ejecutar el proyecto:

1. Descargar el .zip o clonar el repositorio con toda la información necesaria para el modelo dockerizado.
   
   ![image](https://github.com/user-attachments/assets/08193430-85b2-4781-9179-975144f0df69)

2. Guardar la key de kaggle llamada kaggle.json (Es la que te permite autentificarte y descargar la información del modelo) en la carpeta principal.
![image](https://github.com/user-attachments/assets/6be967e3-c3f5-4286-9f83-1999d26ee0ed)

3. En la terminal donde se encuentra el proyecto usar el comando que nos permitira construir una imagen Docker usando el Dockerfile que está en el directorio actual (.). El flag -t kaggle_model significa que estamos nombrando a la imagen: kaggle_model.
   comando: docker build -t kaggle_model .
   
   ![image](https://github.com/user-attachments/assets/b04d4353-df78-4834-98f2-eb42fe220acf)

4. Luego utilizar el comando que nos permitira ejecutar un contenedor interactivo desde la imagen que hemos construido (kaggle_model)
   comando: docker run -it kaggle_model
   
   ![image](https://github.com/user-attachments/assets/09388966-f84c-47f6-adf3-745068302e55)

5. Al entrar al contenedor ejecutaremos el script:python3 scripts/model.py que se encargara de correr el modelo predictivo
   - Este script realiza lo que pasa en la primera entrega (preparación de datos)
   - Además se crean los archivos csv (train_data.csv, test_data_input.csv, test_data_target.csv)
   - Se crear el archivo model.pkl que es quien guarda el modelo

6. Luego ejecutaremos el script:python3 scripts/train.py --data_file train_data.csv --model_file model.pkl --overwrite_model
   - Haremos el entrenamiento del modelo

7. Luego ejecutaremos el script:python3 scripts/predict.py --input_file test_data_input.csv --model_file model.pkl --predictions_file test_predictions.csv
   - Haremos las predicciones

8. Ejecutaremos el script:python3 scripts/evaluation.py
    - Carga las predicciones y los valores reales desde archivos CSV
    - Compara si cada par de predicción y valor real son "casi iguales" (dentro de una tolerancia)
    - Imprime la precisión como promedio de aciertos por fila
