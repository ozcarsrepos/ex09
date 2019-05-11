#!/usr/bin/env python3

import sys  # NOQA
import argparse
import logging  # NOQA
import requests
import json
import time
from geojsonio import display
from geocoder import ip
# logger = log.get_logger(__name__)
logger = logging.getLogger(__name__)    # NOQA
logger.setLevel(logging.DEBUG)  # NOQA


# Make feature geojson data
def feature(obj):
    result = {"type": "Feature"}
    result["geometry"] = {"type": "Point"}
    result["geometry"]["coordinates"] = [
        float(obj['geometry']['location']['lng']),
        float(obj['geometry']['location']['lat'])]
    # format of GeoJSON ('coordinates': [lng, lat])
    result["properties"] = dict()
    result["properties"]["name"] = obj['name']
    result["properties"]["Address"] = obj['vicinity']
    result["properties"]["rating"] = obj['rating']
    return result


# Get result from googlemaps with num & locate, default locate = 'DHGTVT',
# default radius = 2000 meters, keyword is optional in command line
def geo_result(num=50, **locate):
    locate.setdefault("location", "10.8048982,106.7170081")
    # format of Googlemap API ('location': [lat, lon])
    locate.setdefault("radius", "2000")
    locate.setdefault("type", "restaurant")
    locate.setdefault("key", "AIzaSyCLYmd6U1YQhHPDJn9jL8ihulOc4yUmuzg")

    googlemaps_api_url = (
        'https://maps.googleapis.com/maps/api/place/nearbysearch/json')
    ses = requests.Session()
    req = ses.get(googlemaps_api_url, params=locate)
    resp = req.json()
    # Establishing GeoJSON data
    geo_data = {"type": "FeatureCollection", "features": [
        {"type": "Feature",
         "geometry": {"type": "Point",
                      "coordinates": []},
         "properties": {
            "marker-color": "#dc4e4c",
            "marker-size": "medium",
            "marker-symbol": "star",
            "name": "Your location here!",
            }}
        ]}

    if locate["location"] == "10.8048982,106.7170081":
        geo_data["features"][0]["geometry"]["coordinates"] = [106.7170081,
                                                              10.8048982]
        geo_data["features"][0]["properties"]["Address"] = (
            "Trường Đại học Giao thông Vận tải TP.HCM")
    else:
        geo_data["features"][0]["geometry"]["coordinates"] = (
            float(i) for i in locate["location"].split(',')[::-1])
    n = min(num, 20)    # each result page (pagesize) has 20 records
    for rs in resp['results'][:n]:
        geo_data["features"].append(feature(rs))
    num -= 20
    while num > 0 and len(geo_data["features"]) > 1:
        time.sleep(2)
        locate_next = dict()
        locate_next['pagetoken'] = resp['next_page_token']
        locate_next['key'] = "AIzaSyCLYmd6U1YQhHPDJn9jL8ihulOc4yUmuzg"
        req = ses.get(googlemaps_api_url, params=locate_next)
        resp = req.json()
        n = min(num, 20)
        for rs in resp['results'][:n]:
            geo_data["features"].append(feature(rs))
        num -= 20
    else:
        logger.debug('Get enough data or over your daily quotas for '
                     'accessing to Google maps API')

    return geo_data


def main():
    if len(sys.argv) == 1:
        geojson_data = geo_result()
    else:
        try:
            parser = argparse.ArgumentParser(description=(
                'display a type (default is restaurants) map in radius '
                '(default is 2000 m) of a location (default is Dai hoc '
                'giao thong van tai - duong Vo Oanh, Q. Binh Thanh)'))
            parser.add_argument('--lat', '-l', default="10.8048982",
                                help='input the latitude of your location')
            parser.add_argument('--lng', '-g', default="106.7170081",
                                help='input the longtitude of your location')
            parser.add_argument('--type', '-t', default='restaurant',
                                dest='maptype', help='type of your map default'
                                ' is restaurant')
            parser.add_argument('--numpage', '-n', default=50, type=int,
                                dest='num', help='input the pagesize, '
                                'default is 50')
            parser.add_argument('--radius_map', '-r', default="2000",
                                dest='mapradius', help='input the radius of '
                                'your searching (default is 2000 m)')
            args = parser.parse_known_args()
            locate = dict()
            if args[0].lat == 'me':
                position = ip(args.lat)
                locate["location"] = '.'.join(str(i) for i in position.latlng)
            else:
                locate["location"] = (','
                                      .join([args[0].lat, args[0].lng]))
            locate["type"] = args[0].maptype
            locate["radius"] = args[0].mapradius
            geojson_data = geo_result(args[0].num, locate)
        except Exception as e:
            logger.debug('Appear exception:', e)

    # Output to a file (JSON serialization)
    with open('pymi_beer.geojson', 'w', encoding='utf8') as f:
        json.dump(geojson_data, f, indent=2)

    # Convert to a JSON string and display on geojson.io
    display(json.dumps(geojson_data))


if __name__ == '__main__':
    main()
