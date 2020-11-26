#!/usr/bin/python

import pandas as pd
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()


def save_to_db(picklefile):
    data = pd.read_pickle(picklefile)
    data["pickup_datetime"] = pd.to_datetime(data["pickup_datetime"])
    data["dropoff_datetime"] = pd.to_datetime(data["dropoff_datetime"])

    data.to_sql('Trips', con=conn, if_exists='append', chunksize=1000)

# save_to_db('data09.pk1')
# save_to_db('data10.pk1')
# save_to_db('data11.pk1')
# save_to_db('data12.pk1')


r1 = c.execute(
    'select avg(trip_distance) from Trips where passenger_count <= 2').fetchone()[0]
r2 = c.execute('select vendor_id, sum(total_amount) as total_money_raised from Trips \
group by vendor_id order by total_money_raised desc limit 3').fetchall()
r3 = c.execute("select strftime('%Y-%m', pickup_datetime) as pmonth, \
                count(trip_distance) from Trips\
                where\
                payment_type in ('Cas', 'CAS','Cash','CASH', 'CSH')\
                group by pmonth\
                order by pmonth asc").fetchall()
r4 = c.execute("select date(pickup_datetime) as pday, count(trip_distance)\
                from Trips\
                where \
                pday >= '2012-10'\
                group by pday \
                order by pday asc").fetchall()

print('sql query result is:\n', '\nQuestion 1\n',
      r1, '\nQuestion 2\n',  '{:.2f}'.format(r2), '\nQuestion 3\n', r3,
      '\nQuestion 2\n', r4)
