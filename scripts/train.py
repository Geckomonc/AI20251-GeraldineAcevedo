import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from loguru import logger
import os
import pandas as pd
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--data_file', required=True, type=str, help='a csv file with train data')
parser.add_argument('--model_file', required=True, type=str, help='where the trained model will be stored')
parser.add_argument('--overwrite_model', default=False, action='store_true', help='if sets overwrites the model file if it exists')

args = parser.parse_args()

model_file = args.model_file
data_file  = args.data_file
overwrite = args.overwrite_model

if os.path.isfile(model_file):
    if overwrite:
        logger.info(f"overwriting existing model file {model_file}")
    else:
        logger.info(f"model file {model_file} exists. exitting. use --overwrite_model option")
        exit(-1)

logger.info("loading train data")
z = pd.read_csv(data_file).values
Xtr = z[:, :10]
ytr = z[:, 10:]

logger.info("fitting model")
m = MultiOutputRegressor(LinearRegression(n_jobs=1))
m.fit(Xtr, ytr)

logger.info(f"saving model to {model_file}")
with open(model_file, "wb") as f:
    pickle.dump(m, f)