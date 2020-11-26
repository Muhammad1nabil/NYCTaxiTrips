#!/usr/bin/python

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle

# d = pd.concat(
#     pd.read_json("data09.json", lines=True, chunksize=1000))

################# loading data func #################

# all data saved to pickle files from another script 
# to save time loading it and while developing/debugging process

data09 = pd.read_pickle('data09.pk1')
data10 = pd.read_pickle('data10.pk1')
data11 = pd.read_pickle('data11.pk1')
data12 = pd.read_pickle('data12.pk1')

# allData = pd.read_pickle('allData.pk1')

data09['pickup_datetime'] = pd.to_datetime(data09['pickup_datetime'])
data10['pickup_datetime'] = pd.to_datetime(data10['pickup_datetime'])
data11['pickup_datetime'] = pd.to_datetime(data11['pickup_datetime'])
data12['pickup_datetime'] = pd.to_datetime(data12['pickup_datetime'])
# allData['pickup_datetime'] = pd.to_datetime(allData['pickup_datetime'])
################# Question 1 #################

# concatinating to calculate the answer from 4 years data

# calculating the average distance traveled by trips with a maximum of 2 passengers
# Q1 = allData[allData['passenger_count'] <= 2]['trip_distance'].agg('mean')

Q1 = data09[data09['passenger_count'] <= 2]['trip_distance'].agg('mean')
Q1 += data10[data10['passenger_count'] <= 2]['trip_distance'].agg('mean')
Q1 += data11[data11['passenger_count'] <= 2]['trip_distance'].agg('mean')
Q1 += data12[data12['passenger_count'] <= 2]['trip_distance'].agg('mean')
Q1 /= 4
# format to show only 2 digits after the dot
print('Avrage trip distance for trips with a max of 2 passengers: {:.2f}'.format(Q1), 'KM\n')
################# Question 2 #################
# Q2 = allData.groupby(['vendor_id'])['total_amount'].agg('sum').sort_values(ascending=False).head(3)

# getting the 3 biggest vendors based on the total amount of money raised 
Q2 = data09.groupby(['vendor_id']
                     )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
Q2 += data10.groupby(['vendor_id']
                     )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
Q2 += data11.groupby(['vendor_id']
                     )['total_amount'].agg('sum').sort_values(ascending=False).head(3)
Q2 += data12.groupby(['vendor_id']
                     )['total_amount'].agg('sum').sort_values(ascending=False).head(3)

print('top 3 vendors based on total money raied in order: \n')
for i in range(len(Q2)):
    print(i+1, '-', Q2.index[i], '{:.2f}'.format(Q2[i]))
print()
# bar chart to show top 3 vendors

################# Question 3 #################
# casting pickup_datetime from datetime format to month
per09 = data09.pickup_datetime.dt.to_period("M")
per10 = data10.pickup_datetime.dt.to_period("M")
per11 = data11.pickup_datetime.dt.to_period("M")
per12 = data12.pickup_datetime.dt.to_period("M")

# calculating a monthly distribution over 4 years of rides paid with cash
# count trips can be done by using count on any column as it's only counting records(trips)
result = pd.concat([
    data09[data09['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
        per09)['trip_distance'].agg('count'),
    data10[data10['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
        per10)['trip_distance'].agg('count'),
    data11[data11['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
        per11)['trip_distance'].agg('count'),
    data12[data12['payment_type'].isin(['Cas', 'CAS', 'Cash', 'CASH', 'CSH'])].groupby(
        per12)['trip_distance'].agg('count')
])
Q3 = {"month": list(result.index.values),
      "trips": result.values}
Q3 = pd.DataFrame(Q3, columns=['month', 'trips'])
Q3.set_index('month', inplace=True)
print('no. trips in each month:\n',Q3, '\n')
################# Question 4 #################
per09 = data09.pickup_datetime.dt.to_period("D")
per10 = data10.pickup_datetime.dt.to_period("D")
per11 = data11.pickup_datetime.dt.to_period("D")
per12 = data12.pickup_datetime.dt.to_period("D")

result = pd.concat([
    data09.groupby(per09)['trip_distance'].agg('count'),
    data10.groupby(per10)['trip_distance'].agg('count'),
    data11.groupby(per11)['trip_distance'].agg('count'),
    data12.groupby(per12)['trip_distance'].agg('count'),
])

Q4 = {"day": result.index.values, "trips": result.values}
Q4 = pd.DataFrame(Q4, columns=['day', 'trips'])
Q4.set_index('day', inplace=True)
# plt.plot(Q4)
# plt.show()
print('no. trips in each day for the last 3 months of 2012\n', Q4, '\n')
################# Bonus 1 #################
data09["dropoff_datetime"] = pd.to_datetime(data09["dropoff_datetime"])
data09["pickup_weekday_name"] = data09['pickup_datetime'].dt.day_name()
data09["trip_duration"] = (
    data09['dropoff_datetime'] - data09['pickup_datetime']).values.astype(np.int64)

avgTripsSatSun = pd.to_timedelta(data09[data09['pickup_weekday_name'].isin(
    ['Saturday', 'Sunday'])].groupby(
        'pickup_weekday_name')['trip_duration'].agg('mean'))

print('Avrage no. Trips at Saturdays and Sundays\n')

for i in range(2):
    print('-', avgTripsSatSun.index[i], '{:.2f}'.format(avgTripsSatSun[i]/pd.Timedelta(minutes=1)), 'min')
print()