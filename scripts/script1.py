import pandas as pd
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

# d09 = pd.read_pickle('data09.pk1')
# d09['id'] = range(1000000)
# d09["pickup_datetime"] = pd.to_datetime(d09["pickup_datetime"])
# d09["dropoff_datetime"] = pd.to_datetime(d09["dropoff_datetime"])
# d09["pickup_month"] = d09.pickup_datetime.dt.month
# d09.to_pickle('ndata09.pk1')

# d10 = pd.read_pickle('data10.pk1')
# d10['id'] = range(1000000, 2000000)
# d10["pickup_datetime"] = pd.to_datetime(d10["pickup_datetime"])
# d10["dropoff_datetime"] = pd.to_datetime(d10["dropoff_datetime"])
# d10["pickup_month"] = d10.pickup_datetime.dt.month
# d10.to_pickle('ndata10.pk1')

# d11 = pd.read_pickle('data11.pk1')
# d11['id'] = range(2000000, 3000000)
# d11["pickup_datetime"] = pd.to_datetime(d11["pickup_datetime"])
# d11["dropoff_datetime"] = pd.to_datetime(d11["dropoff_datetime"])
# d11["pickup_month"] = d11.pickup_datetime.dt.month
# d11.to_pickle('ndata11.pk1')

# d12 = pd.read_pickle('data12.pk1')
# d12['id'] = range(3000000, 4000000)
# d12["pickup_datetime"] = pd.to_datetime(d12["pickup_datetime"])
# d12["dropoff_datetime"] = pd.to_datetime(d12["dropoff_datetime"])
# d12["pickup_month"] = d12.pickup_datetime.dt.month
# d12.to_pickle('ndata12.pk1')

# dataframes = [d09, d10, d11, d12]

# allData = pd.concat(dataframes)



allData = pd.read_pickle("allData.pk1")
# allData["pickup_datetime"] = pd.to_datetime(allData["pickup_datetime"])
# allData["dropoff_datetime"] = pd.to_datetime(allData["dropoff_datetime"])
# allData["pickup_dayofmonth"] = allData.pickup_datetime.dt.day
# print("concat is complete!")

# allData.to_pickle('allData.pk1')
# print("saving to pickle file is complete!")

# allData.to_sql('newTrips', con=conn, if_exists='append', chunksize=1000)
# print("storing in database is complete!")
# r1 = c.execute('select avg(trip_distance) from newTrips where passenger_count <= 2').fetchall()
# r2 = c.execute('select vendor_id, sum(total_amount) as total_money_raised from newTrips \
# group by vendor_id order by total_money_raised desc limit 3').fetchall()
# r3 = c.execute("select distinct pickup_month, distinct count(id) from newTrips \
#     where payment_type in ('Cas', 'CAS','Cash','CASH', 'CSH') group by pickup_month \
#         order by pickup_month asc").fetchall()
# print('sql query result is:\n', '\nQuestion 1\n',
#       r1, '\nQuestion 2\n',  r2, '\nQuestion 3\n', r3)
# r4 = c.execute("select pickup_month, count(id) from newTrips where pickup_datetime >= '2012-8-01 00:00:00'")
# print(r4.fetchall())
# allData[allData["payment_type"].isin(['Cas', 'CAS','Cash','CASH', 'CSH'])]
