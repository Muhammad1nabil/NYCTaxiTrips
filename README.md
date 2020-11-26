# Technical test in Data Science on NYC taxi trips data

this repo is a answer for technical test as described
it has scripts folder contains all python scripts and created database from json files and also pickle files generated from json files to speed debugging/developing process. -no data included here becuz of its size- also analysis.html file

## folder Tree
```
NYCTaxiTrips>

----env>

----scripts>

--------answers_script.py

--------draft_script1.py

--------draft_script2.py

--------db.sqlite

--------data-payment_lookup-csv.csv

--------data09.json

--------data10.json

--------data11.json

--------data12.json

--------data09.pk1

--------data10.pk1

--------data11.pk1

--------data12.pk1
```
## Packages

this repo developed in virtual environment which has its own packages:
- matplotlib==3.3.3
- numpy==1.19.4
- pandas==1.1.4

## scripts
### answer_scripts.py
this is the main script which coded to answer all basic requirement and some bonus items.
when answer_script.py runs it will opt all answers in figures and command line prints.

to run this script, pass the data in json or pickle-extention '.pk1'- or mix, pass all data as a parameter and the script will parse and execute.

```bash
python answer_script.py data09.json data10.json data11.json data12.json
```
or 
```bash
python answer_script.py data09.pk1 data10.pk1 data11.pk1 data12.pk1
```

this will generate a db.sqlite database filled with all the data passed to it.

the script after fill the database will start execute queries to answer the question

### First Query
```SQL
select avg(trip_distance) from Trips where passenger_count <= 2
```
### Output

```bash
2.66252699620309
```
this is the average distance traveled with maximum 2 passengers. calculated by selecting all trips with passengers less than or equal to 2 then averaging trip distance to get the result 2.66252699620309 as its in kilo meters.

The script prints on the command line screen the opt
```avg trip distance for trips with max 2 passengers: 2.66 KM```

### Second Query
```SQL
select vendor_id, sum(total_amount) as total_money_raised
from Trips 
group by vendor_id order by total_money_raised desc limit 3
```
### Output

```bash
- CMT 19549084.2799961
- VTS 19043433.9999962
- DDS 19043433.9999962
```
those are the top 3 vendors along with total money raised over 4 years. this query limit the output for only 3 records which what we need to identify top 3 vendors where CMT is the highest.
this output is not showed in command line like the query before. But the data is presented in bar chart showing the output. (Figure 1)
### Third Query
```SQL
select strftime('%Y-%m', pickup_datetime) as pmonth,
count(trip_distance)
from Trips
where 
payment_type in ('Cas', 'CAS', 'Cash', 'CASH', 'CSH')
group by pmonth
order by pmonth asc
```
### Output

```bash
- 2009-1  66824
- ...       ...
- 2012-10 72783

45 rows returned
```
this query count trips which paid with cash and present it as number of trips in each month.
this query shows there's data missing in months like
(2011-12 / 2012-11 / 2012-12) as its suppose to get 48 rows not 45 rows.

in this query, counting trips made using ```count()``` function and it can be done using any column(has no null)

The third question was asking about histogram. the opt will display a histogram about frequency of no. trips each month (figure 2)
### Fourth Query
```SQL
select date(pickup_datetime) as pday, count(trip_distance)
from Trips
where
pday >= '2012-08' 
and pday < '2013-01' 
group by pday 
order by pday asc
```
### Output

```bash
- 2012-08-01  3292
- ...          ...
- 2012-10-27  3297

88 rows returned
```
### Fifth Query
```SQL
select avg(strftime("%s", dropoff_datetime)-strftime("%s", pickup_datetime))/60,
cast (strftime("%w", pickup_datetime) as integer) as weekday
from Trips
group by weekday
```
### Output

```bash
- 8.74402217497446  0
- 8.74692475558862  1
- 8.75049772466244  2
- 8.74889401208074  3
- 8.74704682369261  4
- 8.74906998379256  5
- 8.74900352763194  6
```
The query gets avg time in minutes for each week day presented as number from 0 to 6 (Sunday to Saturday).
this shows similar number for each day. so for Sunday and Saturday the script will print on command line screen the numbers.
```bash
Average num of trips in:

- Sunday        8.74 min

- Saturday      8.74 min
```
and also a figure with bar chart showing avg for all week days and Saturday-Sunday colored with yellow.

this query get number of trips each day to presented it as time series chart.
as we see the data is missing the last 4 days of October 2012 and as I mentioned that data hasn't Nov and Dec data so the last 3 months this data has are Aug-Sep-Oct so the time series begins from 2012-08-01 to 2012-10-27.

The chart shows significant change events happened. those changes is a peak (high/low) and mainly around end of the week (Friday)

### Sixth Query
```SQL
select strftime("%H",pickup_datetime) as hour, count(trip_distance) as num_Trips 
from Trips 
group by hour
```
### Output
```bash
- 00  166829
- 01  167200
- 02  166983
- ..     ...
- 21  167409
- 22  165984
- 23  166539

24 rows returned
```

this is hourly distribution of trips across the day. also shows similar numbers all the day which is strange that number of trips in mid day almost equals mid night.

The script generates a bar chart to display this data to be more visual.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
