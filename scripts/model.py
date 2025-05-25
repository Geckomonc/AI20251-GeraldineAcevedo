# IMPORTING PACKAGES

# Se utiliza para descomprimir archivos .zip
import zipfile

# DATA PREPROCESSING
import pandas as pd
import datetime
import re

# VISUALIZATION: Estas bibliotecas permiten crear gráficos de distintos tipos
import warnings
warnings.filterwarnings('ignore')

# MACHINE LEARNING PACKAGES: herramientas de aprendizaje automático supervisado
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#Other libraries
from sklearn.metrics import mean_squared_error, r2_score
import pickle
#################################################
import os 
from kaggle.api.kaggle_api_extended import KaggleApi

# Autenticación
api = KaggleApi()
api.authenticate()

# Descargar los archivos de la competencia
api.competition_download_files(
    'pkdd-15-predict-taxi-service-trajectory-i',
    path='.'  # Puedes cambiar esta ruta si quieres otro destino
)
###################################################
# Ruta del ZIP subido
zip_path = "pkdd-15-predict-taxi-service-trajectory-i.zip"
extract_path = "kaggle_data"

# Descomprimir el archivo ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Descomprimir individualmente cada .csv.zip
import pandas as pd

def unzip_csv(zip_path, csv_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        return pd.read_csv(zip_ref.open(csv_name))

# Ruta base donde se extrajeron los .csv.zip
zip_folder = "kaggle_data"

# Cargar los DataFrames
sample = unzip_csv(f"{zip_folder}/sampleSubmission.csv.zip", "sampleSubmission.csv")
train = unzip_csv(f"{zip_folder}/train.csv.zip", "train.csv")
test = unzip_csv(f"{zip_folder}/test.csv.zip", "test.csv")
location = unzip_csv(f"{zip_folder}/metaData_taxistandsID_name_GPSlocation.csv.zip", "metaData_taxistandsID_name_GPSlocation.csv")

train = train.sample(1000, random_state=42).reset_index(drop=True)

# DROPPING "DAY_TYPE" COLUMN
train = train.drop("DAY_TYPE", axis=1)


# DROPPING "DAY_TYPE" COLUMN
test = test.drop("DAY_TYPE", axis=1)

# DECODING TIME SIGNATURE TRAIN DATA
train["TIMESTAMP"] = [float(time) for time in train["TIMESTAMP"]]
train["data_time"] = [datetime.datetime.fromtimestamp(time, datetime.timezone.utc) for time in train["TIMESTAMP"]]

# DECODING TIME SIGNATURE TEST DATA
test["TIMESTAMP"] = [float(time) for time in test["TIMESTAMP"]]
test["data_time"] = [datetime.datetime.fromtimestamp(time, datetime.timezone.utc) for time in test["TIMESTAMP"]]

# CREATING TIME BASED FEATURES TRAINING DATA

train["year"] = train["data_time"].dt.year
train["month"] = train["data_time"].dt.month

train["day"] = train["data_time"].dt.day
train["hour"] = train["data_time"].dt.hour
train["min"] = train["data_time"].dt.minute
train["weekday"] = train["data_time"].dt.weekday

# CREATING TIME BASED FEATURES TESTING DATA

test["year"] = test["data_time"].dt.year
test["month"] = test["data_time"].dt.month

test["day"] = test["data_time"].dt.day
test["hour"] = test["data_time"].dt.hour
test["min"] = test["data_time"].dt.minute
test["weekday"] = test["data_time"].dt.weekday

# ENCODING CALL TYPE FOR TRAINING DATA TO PREPARE FOR MODELING

encoder = OneHotEncoder(handle_unknown='ignore')

encoder_df = pd.DataFrame(encoder.fit_transform(train[['CALL_TYPE']]).toarray())

final_train = train.join(encoder_df)

final_train.rename(columns={0:'call_type_a', 1:'call_type_b',2:'call_type_c'}, inplace=True)

# ENCODING CALL TYPE FOR TEST DATA

encoder = OneHotEncoder(handle_unknown='ignore')

encoder_df = pd.DataFrame(encoder.fit_transform(test[['CALL_TYPE']]).toarray())

final_test = test.join(encoder_df)

final_test.rename(columns={0:'call_type_a', 1:'call_type_b',2:'call_type_c'}, inplace=True)

# EXTRACTING 1st LATITUDE FOR PLOTTING IT ON THE MAP FROM TRAINING DATA

# 1st lon
lists_1st_lon = []
for i in range(0,len(final_train["POLYLINE"])):
    if final_train["POLYLINE"][i] == '[]':
        k=0
        lists_1st_lon.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_train["POLYLINE"][i]).split(",")[0]
        lists_1st_lon.append(k)

final_train["lon_1st"] = lists_1st_lon

# 1st lat
lists_1st_lat = []
for i in range(0,len(final_train["POLYLINE"])):
    if final_train["POLYLINE"][i] == '[]':
        k=0
        lists_1st_lat.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_train["POLYLINE"][i]).split(",")[1]
        lists_1st_lat.append(k)

final_train["lat_1st"] = lists_1st_lat

# EXTRACTING Last LONGITUDE FOR PLOTTING IT ON THE MAP FROM TRAINING DATA

# last long
lists_last_lon = []
for i in range(0,len(final_train["POLYLINE"])):
        if final_train["POLYLINE"][i] == '[]':
            k=0
            lists_last_lon.append(k)
        else:
            k = re.sub(r"[[|[|]|]|]]", "", final_train["POLYLINE"][i]).split(",")[-2]
            lists_last_lon.append(k)

final_train["lon_last"] = lists_last_lon

# last lat
lists_last_lat = []
for i in range(0,len(final_train["POLYLINE"])):
    if final_train["POLYLINE"][i] == '[]':
        k=0
        lists_last_lat.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_train["POLYLINE"][i]).split(",")[-1]
        lists_last_lat.append(k)

final_train["lat_last"] = lists_last_lat

# DELETE LON & LAT HAVE "0"
train = final_train.query("lon_last != 0")

## CHANGING DATA TYPE FOR MODELING TRAINING DATA

train["lon_1st"] = [float(k) for k in train["lon_1st"]]
train["lat_1st"] = [float(k) for k in train["lat_1st"]]
train["lon_last"] = [float(k) for k in train["lon_last"]]
train["lat_last"] = [float(k) for k in train["lat_last"]]
train['call_type_a']= [int(k) for k in train["call_type_a"]]
train['call_type_b'] =[int(k) for k in train["call_type_b"]]
train['call_type_c']= [int(k) for k in train["call_type_c"]]

# EXTRACTING 1st LATITUDE FROM TESTING DATA

# 1st lon
lists_1st_lon = []
for i in range(0,len(final_test["POLYLINE"])):
    if final_test["POLYLINE"][i] == '[]':
        k=0
        lists_1st_lon.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_test["POLYLINE"][i]).split(",")[0]
        lists_1st_lon.append(k)

final_test["lon_1st"] = lists_1st_lon

# 1st lat
lists_1st_lat = []
for i in range(0,len(final_test["POLYLINE"])):
    if final_test["POLYLINE"][i] == '[]':
        k=0
        lists_1st_lat.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_test["POLYLINE"][i]).split(",")[1]
        lists_1st_lat.append(k)

final_test["lat_1st"] = lists_1st_lat

# EXTRACTING Last LONGITUDE FROM TESTING DATA

lists_last_lon = []
for i in range(0,len(final_test["POLYLINE"])):
        if final_test["POLYLINE"][i] == '[]':
            k=0
            lists_last_lon.append(k)
        else:
            k = re.sub(r"[[|[|]|]|]]", "", final_test["POLYLINE"][i]).split(",")[-2]
            lists_last_lon.append(k)

final_test["lon_last"] = lists_last_lon

# last lat
lists_last_lat = []
for i in range(0,len(final_test["POLYLINE"])):
    if final_test["POLYLINE"][i] == '[]':
        k=0
        lists_last_lat.append(k)
    else:
        k = re.sub(r"[[|[|]|]|]]", "", final_test["POLYLINE"][i]).split(",")[-1]
        lists_last_lat.append(k)

final_test["lat_last"] = lists_last_lat

# Delete lon & lat have "0".
test = final_test.query("lon_last != 0")

## CHANGING DATA TYPE FOR TESTING DATA

test["lon_1st"] = [float(k) for k in test["lon_1st"]]
test["lat_1st"] = [float(k) for k in test["lat_1st"]]
test["lon_last"] = [float(k) for k in test["lon_last"]]
test["lat_last"] = [float(k) for k in test["lat_last"]]
test['call_type_a']= [int(k) for k in test["call_type_a"]]
test['call_type_b'] =[int(k) for k in test["call_type_b"]]
test['call_type_c']= [int(k) for k in test["call_type_c"]]

# DROPPING CALL_TYPE
del train['CALL_TYPE']

# FILLING MISSING VALUES
train['ORIGIN_CALL'] = train[['ORIGIN_CALL']].fillna('')
train['ORIGIN_STAND'] = train[['ORIGIN_STAND']].fillna('')

# COPYING DATAFRAME
new_train = train.copy()
new_train

# CREATING DELTA PARAMETER FOR DISTANCE COMPUTATION FOR TRAINING DATA
train["delta_lon"] = train["lon_last"] - train["lon_1st"]
train["delta_lat"] = train["lat_last"] - train["lat_1st"]

# CREATING DELTA PARAMETER FOR DISTANCE COMPUTATION FOR TEST DATA
# Creating Delta parameter for distance computation test data
test["delta_lon"] = test["lon_last"] - test["lon_1st"]
test["delta_lat"] = test["lat_last"] - test["lat_1st"]

# COPYING DATAFRAME FOR MODEL TRAINING
ml_train = train.copy()

#############################################################################################################

# Origin_call
def origin_call_flg(x):
    if x["ORIGIN_CALL"] == None:
        res = 0
    else:
        res = 1
    return res
ml_train["ORIGIN_CALL"] = ml_train.apply(origin_call_flg, axis=1)

# Origin_stand
def origin_stand_flg(x):
    if x["ORIGIN_STAND"] == None:
        res = 0
    else:
        res=1
    return res
ml_train["ORIGIN_STAND"] = ml_train.apply(origin_stand_flg, axis=1)


# Missing data
def miss_flg(x):
    if x["MISSING_DATA"] == "False":
        res = 0
    else:
        res = 1
    return res
ml_train["MISSING_DATA"] = ml_train.apply(miss_flg, axis=1)

# COPYING DATAFRAME FOR MODEL TESTING
ml_test = test.copy()

# Origin_call
def origin_call_flg(x):
    if x["ORIGIN_CALL"] == None:
        res = 0
    else:
        res = 1
    return res
ml_test["ORIGIN_CALL"] = ml_test.apply(origin_call_flg, axis=1)

# Origin_stand
def origin_stand_flg(x):
    if x["ORIGIN_STAND"] == None:
        res = 0
    else:
        res=1
    return res
ml_test["ORIGIN_STAND"] = ml_test.apply(origin_stand_flg, axis=1)


# Missing data
def miss_flg(x):
    if x["MISSING_DATA"] == "False":
        res = 0
    else:
        res = 1
    return res
ml_test["MISSING_DATA"] = ml_test.apply(miss_flg, axis=1)

#########################################################################################################

ml_train = ml_train.sample(10) # A random sampling of 136000(*%) of data point will be used to train as 1.7M is large

X = ml_train[["call_type_a","call_type_b","call_type_c",'ORIGIN_CALL','ORIGIN_STAND', 'MISSING_DATA', 'lon_1st', 'lat_1st', 'delta_lon', 'delta_lat']]

y = ml_train[["lon_last","lat_last"]]

X_Test = ml_test[["call_type_a","call_type_b","call_type_c",'ORIGIN_CALL','ORIGIN_STAND', 'MISSING_DATA', 'lon_1st', 'lat_1st', 'delta_lon', 'delta_lat']]

# TRAIN, TEST SPIT 70 % FOR TRAINING & 30 % FOR TESTING
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Guardar datasets como CSV
pd.concat([X, y], axis=1).to_csv("train_data.csv", index=False)
X_Test.to_csv("test_data_input.csv", index=False)
test[["lon_last", "lat_last"]].to_csv("test_data_target.csv", index=False) 

# Entrenamiento del modelo

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

lr = MultiOutputRegressor(LinearRegression(n_jobs=1))
lr = lr.fit(X_train, y_train)

y_train_pred = lr.predict(X_train)
y_test_pred = lr.predict(X_test)

#Evaluación y guardado del modelo

from sklearn.metrics import mean_squared_error, r2_score

print("Train MSE:", mean_squared_error(y_train, y_train_pred))
print("Test MSE:", mean_squared_error(y_test, y_test_pred))
print("Train R2:", r2_score(y_train, y_train_pred))
print("Test R2:", r2_score(y_test, y_test_pred))

# Guardar modelo
import pickle
with open("model.pkl", "wb") as f:
    pickle.dump(lr, f)

# Cargar modelo y datos para predecir
with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

X_loaded = pd.read_csv("test_data_input.csv").values
y_true = pd.read_csv("test_data_target.csv").values

y_pred = loaded_model.predict(X_loaded)

print("R2 (cargado):", r2_score(y_true, y_pred))