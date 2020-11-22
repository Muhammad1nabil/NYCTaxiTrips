import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data09 = pd.read_pickle('data09.pk1')
data10 = pd.read_pickle('data10.pk1')
data11 = pd.read_pickle('data11.pk1')
data12 = pd.read_pickle('data12.pk1')

# Q1 = data09[data09['passenger_count'] <= 2]['trip_distance'].mean() 
# Q1 += data10[data10['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 += data11[data11['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 += data12[data12['passenger_count'] <= 2]['trip_distance'].mean()
# Q1 /= 4

# Q2 = data09.groupby(['vendor_id'])['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 += data10.groupby(['vendor_id'])['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 += data11.groupby(['vendor_id'])['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 += data12.groupby(['vendor_id'])['total_amount'].agg('sum').sort_values(ascending=False).head(3)
# Q2 = list(Q2.index)

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
#     data09[data09['payment_type'].isin(['Cas', 'CAS','Cash','CASH', 'CSH'])].groupby(per09)['trip_distance'].agg('count'),
#     data10[data10['payment_type'].isin(['Cas', 'CAS','Cash','CASH', 'CSH'])].groupby(per10)['trip_distance'].agg('count'),
#     data11[data11['payment_type'].isin(['Cas', 'CAS','Cash','CASH', 'CSH'])].groupby(per11)['trip_distance'].agg('count'),
#     data12[data12['payment_type'].isin(['Cas', 'CAS','Cash','CASH', 'CSH'])].groupby(per12)['trip_distance'].agg('count')
# ])
# Q3 = {"month": list(result.index.to_series().astype(str)), "trips": list(result)}
# Q3 = pd.DataFrame(Q3, columns=['month', 'trips'])
# Q3.set_index('month', inplace=True)


data09['pickup_datetime'] = pd.DatetimeIndex(data09['pickup_datetime'])
per09 = data09.pickup_datetime.dt.to_period("D")
data10['pickup_datetime'] = pd.DatetimeIndex(data10['pickup_datetime'])
per10 = data10.pickup_datetime.dt.to_period("D")
data11['pickup_datetime'] = pd.DatetimeIndex(data11['pickup_datetime'])
per11 = data11.pickup_datetime.dt.to_period("D")
data12['pickup_datetime'] = pd.DatetimeIndex(data12['pickup_datetime'])
per12 = data12.pickup_datetime.dt.to_period("D")

result = pd.concat([
    data09.groupby(per09)['trip_distance'].agg('count'),
    data10.groupby(per10)['trip_distance'].agg('count'),
    data11.groupby(per11)['trip_distance'].agg('count'),
    data12.groupby(per12)['trip_distance'].agg('count'),
])

# Q4 = {"day": list(result.index.to_series().astype(str)), "trips": list(result)}
# Q4 = pd.DataFrame(Q4, columns=['day', 'trips'])
# Q4.set_index('day', inplace=True)
# plt.plot(Q4)
# plt.show()


# print(Q1)
# print()
# print(Q2)
# plt.figure(figsize=(12,8))
# plt.hist(Q3)
# plt.show()