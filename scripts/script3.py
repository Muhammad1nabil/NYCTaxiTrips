#!/usr/bin/python

import math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVR, SVR
from sklearn.compose import ColumnTransformer

train = pd.read_pickle('data09.pk1')

train['fare_amount'] = train['fare_amount'] + train['tolls_amount']

train = train[['fare_amount', 'pickup_datetime', 'pickup_longitude', 
'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']]

# print(train.info())
train = train.dropna()

train["pickup_datetime"] = pd.to_datetime(train["pickup_datetime"])
train["pickup_month"] = train["pickup_datetime"].dt.month
train["pickup_dow"] = train["pickup_datetime"].dt.dayofweek
train["pickup_hour"] = train["pickup_datetime"].dt.hour

# train.groupby("pickup_month")["fare_amount"].mean().plot()
# plt.show()
# calculate line distance between pickup and dropoff point.
# convert coordinate to distance in km 
# because latitude and longitude have different distance(one degree of lat = 111km; one degree of long = 85km).
train["move_latitude"] = (train["dropoff_latitude"] - train["pickup_latitude"]) * 111
train["move_longitude"] = (train["dropoff_longitude"] - train["pickup_longitude"]) * 85
train["abs_distance"] = np.hypot(train["move_latitude"], train["move_longitude"])
# plt.scatter(train["abs_distance"], train["fare_amount"])

# plt.show()

# plt.scatter(train["pickup_longitude"], train["pickup_latitude"])
# plt.show()

train = train[train["fare_amount"] > 0]

longtitude_range = (train["pickup_longitude"] <= -73.4) & (train["pickup_longitude"]  >= -74.4)
latitude_range = (train["pickup_latitude"] <= 41.2) & (train["pickup_latitude"] >= 40.2)
train_trim = train[longtitude_range & latitude_range]

train_trim = train_trim[(train_trim["abs_distance"] < 100) & (train_trim["abs_distance"] > 0)]

# print(train_trim.shape[0]/train.shape[0])

# sc = plt.scatter(train_trim["pickup_longitude"], train_trim["pickup_latitude"], c = train_trim["fare_amount"], cmap = "summer")
# plt.colorbar(sc)
# plt.scatter(train_trim["abs_distance"], train_trim["fare_amount"])
# plt.show()
# print(train_trim.corr()["fare_amount"].sort_values(ascending = False))

train_trim["toward_east"] = train_trim["move_longitude"] > 0
train_trim["toward_north"] = train_trim["move_latitude"] > 0

##################################################################################
##################################################################################
##################################################################################

## group pickup hour into bins in order to reduce model runtime
class HourlyBins(BaseEstimator, TransformerMixin): 
    def __init__(self, bins = 8):
        self.bins = bins
    def fit(self, X, y = None):
        return self
    def transform(self, X, y = None):    
        pickup_hour_bin = np.array(pd.cut(X[X.columns[0]], self.bins))
        return pickup_hour_bin.reshape(-1, 1)

hour_pipe = Pipeline([
    ('hourlybins', HourlyBins()),
    ('encoder', OneHotEncoder(categories='auto', sparse = False)),
])

ct_pipe = ColumnTransformer(transformers=[
    ('hourly_cat', hour_pipe, ["pickup_hour"]),
    ('encoder', OneHotEncoder(categories='auto', sparse = False), ["pickup_dow"]),
    ('std_scaler', StandardScaler(), ["pickup_month", "abs_distance", "pickup_longitude", "dropoff_longitude"])
])
##############################################################################
##############################################################################
##############################################################################

def XandY(df, test_set = False):
    df = df.copy()
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["pickup_month"] = df["pickup_datetime"].dt.month.astype(float)
    df["pickup_dow"] = df["pickup_datetime"].dt.dayofweek
    df["pickup_hour"] = df["pickup_datetime"].dt.hour
    df["abs_distance"] = np.hypot(df["dropoff_latitude"]-df["pickup_latitude"], df["dropoff_longitude"]-df["pickup_longitude"])
    df_X = df[["pickup_month", "pickup_dow", "pickup_hour", "abs_distance", "pickup_longitude", "dropoff_longitude"]]
    if test_set == True:
        return df_X
    else:
        df_y = df["fare_amount"]
        return df_X, df_y

train_X, train_y = XandY(train_trim)

lr_pipe = Pipeline([
    ('ct', ct_pipe),
    ('lin_reg', LinearRegression())
]) 
lr_score = cross_val_score(lr_pipe, train_X, train_y, scoring = "neg_mean_squared_error", cv = 5)
lr_rmse = np.sqrt(-lr_score)
print(lr_rmse.mean())

poly_pipe = Pipeline([
    ('poly_features', PolynomialFeatures()),
    ('std_scaler', StandardScaler())
])

poly_ct_pipe = ColumnTransformer(transformers=[
    ('hourly_cat', hour_pipe, ["pickup_hour"]),
    ('encoder', OneHotEncoder(categories='auto', sparse = False), ["pickup_dow"]),
    ('poly', poly_pipe, ["pickup_month", "abs_distance", "pickup_longitude", "dropoff_longitude"])
])

polyreg_pipe = Pipeline([
    ('poly_ct', poly_ct_pipe),
    ('reg', LinearRegression())
])

param_grid = {'poly_ct__poly__poly_features__degree': [2,3,5], 'poly_ct__poly__poly_features__include_bias': [False, True]}
polyreg_gs = GridSearchCV(polyreg_pipe, param_grid, cv = 5, scoring = "neg_mean_squared_error")
polyreg_gs.fit(train_X, train_y)
print(polyreg_gs.best_params_)

print(np.sqrt(-polyreg_gs.best_score_))

