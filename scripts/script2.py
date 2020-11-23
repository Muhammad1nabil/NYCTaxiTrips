import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# d = pd.concat(
#     pd.read_json("data09.json", lines=True, chunksize=1000))

################# loading data func #################
data09 = pd.read_pickle('data09.pk1')
# data10 = pd.read_pickle('data10.pk1')
# data11 = pd.read_pickle('data11.pk1')
# data12 = pd.read_pickle('data12.pk1')

################# Question 1 #################
# Q1 = data09[data09['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 += data10[data10['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 += data11[data11['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 += data12[data12['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 /= 4

################# Question 2 #################
# Q2 = data09.groupby(['vendor_id'])['total_amount'].agg(
#     'sum').sort_values(ascending=False).head(3)
# Q2 += data10.groupby(['vendor_id']
#                      )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 += data11.groupby(['vendor_id']
#                      )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 += data12.groupby(['vendor_id']
#                      )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 = list(Q2.index)


# data09["pickup_datetime"] = pd.to_datetime(data09["pickup_datetime"])
################# Question 3 #################
# hanshel dah we n7ot to_datetime fo2 le kolo b2a
# data09['pickup_datetime'] = pd.DatetimeIndex(data09['pickup_datetime'])
# per09 = data09.pickup_datetime.dt.to_period("M")
# p = data09.pickup_datetime.dt.to_period("D")
# data10['pickup_datetime'] = pd.DatetimeIndex(data10['pickup_datetime'])
# per10 = data10.pickup_datetime.dt.to_period("M")
# data11['pickup_datetime'] = pd.DatetimeIndex(data11['pickup_datetime'])
# per11 = data11.pickup_datetime.dt.to_period("M")
# data12['pickup_datetime'] = pd.DatetimeIndex(data12['pickup_datetime'])
# per12 = data12.pickup_datetime.dt.to_period("M")
# g = data09.groupby(p)['trip_distance'].agg('count')

# result = pd.concat([
    # data09[data09['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
    #     per09)['trip_distance'].agg('count'),
#     data10[data10['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
#         per10)['trip_distance'].agg('count'),
#     data11[data11['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
#         per11)['trip_distance'].agg('count'),
#     data12[data12['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
#         per12)['trip_distance'].agg('count')
# ])
# Q3 = {"month": list(result.index.to_series().astype(str)),
#       "trips": list(result)}
# Q3 = pd.DataFrame(Q3, columns=['month', 'trips'])
# Q3.set_index('month', inplace=True)

################# Question 4 #################
# data09['pickup_datetime'] = pd.DatetimeIndex(data09['pickup_datetime'])
# per09 = data09.pickup_datetime.dt.to_period("D")
# data10['pickup_datetime'] = pd.DatetimeIndex(data10['pickup_datetime'])
# per10 = data10.pickup_datetime.dt.to_period("D")
# data11['pickup_datetime'] = pd.DatetimeIndex(data11['pickup_datetime'])
# per11 = data11.pickup_datetime.dt.to_period("D")
# data12['pickup_datetime'] = pd.DatetimeIndex(data12['pickup_datetime'])
# per12 = data12.pickup_datetime.dt.to_period("D")

# result = pd.concat([
#     data09.groupby(per09)['trip_distance'].agg('count'),
#     data10.groupby(per10)['trip_distance'].agg('count'),
#     data11.groupby(per11)['trip_distance'].agg('count'),
#     data12.groupby(per12)['trip_distance'].agg('count'),
# ])

# Q4 = {"day": list(result.index.to_series().astype(str)), "trips": list(result)}
# Q4 = pd.DataFrame(Q4, columns=['day', 'trips'])
# Q4.set_index('day', inplace=True)
# plt.plot(Q4)
# plt.show()

################# Bonus 1 #################
# data09["pickup_datetime"] = pd.to_datetime(data09["pickup_datetime"])
# data09["dropoff_datetime"] = pd.to_datetime(data09["dropoff_datetime"])
# data09["pickup_weekday_name"] = data09['pickup_datetime'].dt.day_name()
# data09["trip_duration"] = (
#     data09['dropoff_datetime'] - data09['pickup_datetime']).values.astype(np.int64)

# avgSatSun = pd.to_timedelta(data09[data09['pickup_weekday_name'].isin(
#     ['Saturday', 'Sunday'])].groupby(
#         'pickup_weekday_name').mean().trip_duration)
# print(avgSatSun)


################# bonus 4 #################
# data  = data09[[
#     'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
#     ]]
# data['charge'] = data09['tolls_amount'] + data09['fare_amount']
# data.to_pickle('data.pk1')

data = pd.read_pickle('data.pk1')


def great_circle_distance(lon1, lat1, lon2, lat2):
    R = 6371000  # Approximate mean radius of earth (in m)

    # Convert decimal degrees to ridians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Distance of lons and lats in radians
    dis_lon = lon2 - lon1
    dis_lat = lat2 - lat1

    # Haversine implementation
    a = np.sin(dis_lat/2)**2 + np.cos(lat1) * \
        np.cos(lat2) * np.sin(dis_lon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    dis_m = R*c  # Distance in meters
    dis_km = dis_m/1000  # Distance in km
    return dis_km


data['distance'] = great_circle_distance(
    data.pickup_longitude, data.pickup_latitude, data.dropoff_longitude,
     data.dropoff_latitude)

# data.to_pickle('data.pk1')

from sklearn import linear_model
from sklearn.model_selection import train_test_split

reg = linear_model.LinearRegression()

x_train, x_test, y_train, y_test = train_test_split(
    data['distance'], data['charge'], test_size=0.33, random_state=42)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(x_test.shape)

reg.fit(x_train, y_train)

print(reg.score())

# print(Q1)
# print()
# print(Q2)
# plt.figure(figsize=(12, 8))
# plt.hist(Q3)
# plt.show()
