"""Answering https://www.thedataincubator.com/challenge.html (login required).

Answers question 2 on the challenge, by reading and cleaning nyc taxi data,
then using it for the results.

Question was (and the answers are):

Q2: The files trip_data_3.csv.zip and trip_fare_3.csv.zip contain travel and
fare data for NYC taxicabs in March 2013. [Use them to answer these]

What fraction of payments under $5 use a credit card? (8.88%)
What fraction of payments over $50 use a credit card? (68.17%)
What is the mean fare per minute driven? (1.412929)
What is the median of the taxi's fare per mile driven? (5.0)
What is the 95 percentile of the taxi's average driving speed
    in miles per hour? (26.60869565217391)
What is the average ratio of the distance between the pickup and dropoff
    divided by the distance driven? (3.64816470898)
What is the average tip for rides from JFK? (4.475241258619489)
What is the median March revenue of a taxi driver? (7221.199999999995)

NOTE:
    The average tip for rides from JFK where the tip was > $0 is 9.403738
    The "average ratio..." question is answered last in this script.
    It is pretty slow.

Usage Example:

      $ python3 taxi.py

"""
__author__ = 'dlamblin'
import math

import pandas
import numpy


# Load
trip_data = pandas.read_csv('trip_data_3.csv', skipinitialspace=True, dtype={
    'rate_code': str, 'passenger_count': numpy.int,
    'trip_time_in_secs': numpy.int, 'trip_distance': numpy.float},
                            parse_dates=[6, 7])
trip_fare = pandas.read_csv('trip_fare_3.csv', skipinitialspace=True,
                            parse_dates=[4])
# Clean up
trip_data.passenger_count.replace({'0': numpy.nan, '255': numpy.nan},
                                  inplace=True)
trip_data.trip_time_in_secs.replace({0: numpy.nan}, inplace=True)
trip_data.trip_distance.replace({0: numpy.nan}, inplace=True)
trip_fare.payment_type.replace({'UNK': numpy.nan}, inplace=True)

# Join
taxis = pandas.merge(trip_data, trip_fare,
                     on=['medallion', 'hack_license',
                         'vendor_id', 'pickup_datetime'])

total_under_five = taxis['total_amount'] < 5
total_over_fifty = taxis['total_amount'] > 50
uses_credit = taxis['payment_type'] == 'CRD'
# "CRD" -- card, debit or credit
# "CSH" -- cash
# "DIS" -- disputed fare
# "NOC" -- no charge
# "UNK"/NaN -- unknown

print("Fraction of payments under $5 use a credit card (percent):",
      len(taxis[total_under_five & uses_credit])
      / len(taxis[total_under_five]) * 100)

print("Fraction of payments over $50 use a credit card (percent):",
      len(taxis[total_over_fifty & uses_credit])
      / len(taxis[total_over_fifty]) * 100)

print("The mean fare per minute driven:",
      (taxis['fare_amount'] / (taxis['trip_time_in_secs'] / 60)).mean())

print("The median of the taxi's fare per mile driven:",
      (taxis['fare_amount'] / (taxis['trip_distance'])).median())

print("The 95 percentile of the taxi's average driving speed"
      "in miles per hour:",
      (taxis['trip_distance'] / (taxis['trip_time_in_secs'] / 3600)
       ).quantile(0.95))

pkup_lat_in_jfk_max = taxis['pickup_latitude'] < 40.649256
pkup_lat_in_jfk_min = taxis['pickup_latitude'] > 40.639955
pkup_lon_in_jfk_min = taxis['pickup_longitude'] > -73.793245
pkup_lon_in_jfk_max = taxis['pickup_longitude'] < -73.774793
tipped = taxis['tip_amount'] > 0
print("The average tip for rides from JFK:",
      taxis[pkup_lat_in_jfk_max & pkup_lat_in_jfk_min & pkup_lon_in_jfk_max &
            pkup_lon_in_jfk_min]['tip_amount'].mean())

print("The average tip when tipped for rides from JFK:",
      taxis[pkup_lat_in_jfk_max & pkup_lat_in_jfk_min & pkup_lon_in_jfk_max &
            pkup_lon_in_jfk_min & tipped]['tip_amount'].mean())

print("The median March revenue of a taxi driver:",
      taxis.groupby('hack_license')['total_amount'].sum().median())


def distance_on_unit_sphere(lat1, lon1, lat2, lon2):
    """ From JohnDCook.com with minor modification.
    Arc cosine might not be well suited for accuracy.

    Args:
        :param lat1 (float): latitude of point 1
        :param lon1 (float): longitude of point 1
        :param lat2 (float): latitude of point 2
        :param lon2 (float): longitude of point 2
    Returns:
        :return: The arc length on a unit sphere of the lat-lon 1-2 arc
        :rtype: (float)
    """
    # phi = 90 - latitude
    phi1 = math.radians(90.0 - lat1)
    phi2 = math.radians(90.0 - lat2)

    # theta = longitude
    theta1 = math.radians(lon1)
    theta2 = math.radians(lon2)

    # Compute spherical distance from spherical coordinates

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #     sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc


def distance_on_unit_sphere_miles(lat1, lon1, lat2, lon2):
    return distance_on_unit_sphere(lat1, lon1, lat2, lon2) * 3960


def distance_on_unit_sphere_kilometers(lat1, lon1, lat2, lon2):
    return distance_on_unit_sphere(lat1, lon1, lat2, lon2) * 6373


def haversine(lat1, lon1, lat2, lon2):
    """ From http://www.cs.nyu.edu/visual/home/proj/tiger/gisfaq.html
    via http://stackoverflow.com/questions/4913349

    Args:
        :param lat1 (float): latitude of point 1
        :param lon1 (float): longitude of point 1
        :param lat2 (float): latitude of point 2
        :param lon2 (float): longitude of point 2
    Returns:
        :return: The arc length on a unit sphere of the lat-lon 1-2 arc
        :rtype: (float)
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) \
                                  * math.sin(dlon / 2) ** 2
    # return 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 2 * math.asin(math.sqrt(a))


def haversine_miles(lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2) * 3960


def haversine_kilometers(lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2) * 6373


def dist_by_miles(x):
    if x['trip_distance'] > 0:
        hm = haversine_miles(x['pickup_latitude'], x['pickup_longitude'],
                             x['dropoff_latitude'], x['dropoff_longitude'])
        if hm > 0:
            return x['trip_distance'] / hm
    return numpy.nan


print("The average ratio of the distance between the pickup and dropoff "
      "divided by the distance driven:",
      taxis[
          ['pickup_latitude', 'pickup_longitude',
           'dropoff_latitude', 'dropoff_longitude',
           'trip_distance']
      ].apply(dist_by_miles, axis=1, reduce=True).mean())

