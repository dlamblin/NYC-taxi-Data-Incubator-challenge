__author__ = 'dlamblin'
import pandas

trip_data = pandas.read_csv('trip_data_3.csv', skipinitialspace=True, dtype={'rate_code': str}, parse_dates=[6, 7])
trip_fare = pandas.read_csv('trip_fare_3.csv', skipinitialspace=True, parse_dates=[4])
taxis = pandas.merge(trip_data, trip_fare, on=['medallion', 'hack_license', 'vendor_id', 'pickup_datetime'])

print(taxis[:3])