#!/usr/bin/python

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import sys
import os

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

# save_to_db function to load data from json file or pickle file based on picklef flag
# and then insert loaded data into a database
# this function only used for personal -not production- use as it's using sqlite database engine
def save_to_db(fileName, picklef=True):
    if not os.path.exists(fileName):
        print('[-] This file name is not found!')
        os._exit(0)
    if picklef:
        data = pd.read_pickle(fileName)
    else:
        data = pd.concat(
            pd.read_json(fileName, lines=True, chunksize=1000)
        )
        data.to_pickle(fileName.split('.')[0] + '.pk1')
    data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
    data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])
    # data.to_sql('Trips', con=conn, if_exists='append', chunksize=1000)
    
# saving data in pickle files to save time while developing/debugging
for i in range(len(sys.argv) - 1):
    fn = sys.argv[i+1]
    if not fn.endswith('pk1'):
        print('[+] loading json file: ', fn)
        save_to_db(fn, False)
        print('[+]', fn, 'saved successfully into the database')
    else:
        print('[+] loading pickle file: ', fn)
        save_to_db(fn)
        print('[+]', fn, 'saved successfully into the database')
# os._exit(0)


# calculating the average distance traveled by trips with a maximum of 2 passengers
Q1 = c.execute(
    'select avg(trip_distance) from Trips where passenger_count <= 2'
    ).fetchone()[0]

# getting the 3 biggest vendors based on the total amount of money raised 
Q2 = c.execute('select vendor_id, sum(total_amount) as total_money_raised\
                from Trips \
                group by vendor_id order by total_money_raised desc limit 3'
                ).fetchall()

# extracting data from query output
vendors =  [i[0] for i in Q2] 
totalMoney = [i[1] for i in Q2]

plotQ2 = plt.figure(1)
plt.bar(vendors, totalMoney, color='green')
plt.title('Top 3 vendors')
plt.xlabel('Vendors')
plt.ylabel('Money Raised over 4 years')

# geting payment types that refer to Cash payment
paymentInfo = pd.read_csv("data-payment_lookup-csv.csv", names=['type', 'lookup'])
cashTypeNames = list(paymentInfo[paymentInfo['lookup'] == 'Cash']['type'])

# sql query to calculating a monthly distribution over 4 years of rides paid with cash
sql = "select strftime('%Y-%m', pickup_datetime) as pmonth, \
                count(trip_distance) from Trips\
                where\
                payment_type in ('" + \
                "','".join(cashTypeNames) + "') " \
                "group by pmonth\
                order by pmonth asc"

Q3 = c.execute(sql).fetchall()
# extracting trips distribution
tripsWithCash = [i[1] for i in Q3]

plotQ3 = plt.figure(2)
plt.hist(tripsWithCash)
plt.title('monthly distribution over 4 years of rides paid with cash')
plt.xlabel('no. trips in a single month')
plt.ylabel('frequency')

# calculating last month in 2012 according to this data
lastMonth = Q3[-1][0].split('-')[1]
lastMonth = str(int(lastMonth) - 2)
if len(lastMonth) == 1:
    lastMonth = '0' + lastMonth
Q4 = c.execute("select date(pickup_datetime) as pday, count(trip_distance)\
                from Trips\
                where \
                pday >= '2012-"+ lastMonth + "' \
                and pday < '2013-01' \
                group by pday \
                order by pday asc").fetchall()
days =  [i[0] for i in Q4] 
totalTrips = [i[1] for i in Q4]
plotQ4 = plt.figure(3, (14,10))
plt.plot(days, totalTrips, color='red')
plt.xticks(rotation=85)
plt.xlabel("day")
plt.ylabel("no. Trips")
plt.show()
print('avg trip distance for trips with max 2 passengers: {:.2f} KM'.format(Q1))

b1 = c.execute('select avg(strftime("%s", dropoff_datetime)-strftime("%s", pickup_datetime))/60,\
cast (strftime("%w", pickup_datetime) as integer) as weekday \
from Trips \
group by weekday').fetchall()

avgSunSat = [b1[0][0], b1[-1][0]]
print('\nAverage num of trips in:\n')
print('- Sunday\t{:.2f}'.format(avgSunSat[0]), 'min\n')
print('- Saturday\t{:.2f}'.format(avgSunSat[0]), 'min\n')
avgRestOfWeek = [b1[i][0] for i in range(1,len(b1)-1)]
plotB1 = plt.figure(4)
plt.bar(['Sunday', 'Saturday'], avgSunSat, color='yellow')
plt.bar(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], avgRestOfWeek)
plt.title('avg no. trips each day')
plt.xlabel('week day')
plt.ylabel('avg no. trips')
plt.show()

b2 = c.execute('select strftime("%H",pickup_datetime) as hour, count(trip_distance) as num_Trips \
from Trips group by hour').fetchall()

hours = [int(i[0])+1 for i in b2]
trips = [i[1] for i in b2]

plotB2 = plt.figure(5)
plt.bar(hours, trips, color='magenta')
plt.xlabel('hours')
plt.ylabel('no. trips')
plt.title('no. trips each hour chart')
plt.show()
