#!/usr/bin/env python
#
# RR4005i to InfluxDB Collection
#
import xmltodict
import requests, sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint

# Collect Environment Variables
RR4005I_URL = os.environ.get("RR4005I_URL")
RR4005I_NAME = os.environ.get("RR4005I_NAME")
INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
INFLUXDB_MEASNAME = os.environ.get("INFLUXDB_MEASNAME")


print(f"RR4005i Hostname: \t{RR4005I_URL}")
print(f"RR4005i Name: \t{RR4005I_NAME}")

print(f"InfluxDB URL: \t{INFLUXDB_URL}")
print(f"InfluxDB Token: \t{INFLUXDB_TOKEN}")
print(f"InfluxDB Org: \t{INFLUXDB_ORG}")
print(f"InfluxDB Bucket: \t{INFLUXDB_BUCKET}")
print(f"InfluxDB Measurement Name: \t{INFLUXDB_MEASNAME}")

# Collect KiwiSDR Status Data

try:
    r = requests.get(RR4005I_URL)
except Exception as e:
    print(f"Error getting RR4005i status: {str(e)}")
    sys.exit(1)


response = xmltodict.parse(r.text)

# {'rr4005i': {'SUPPLY': '13.71', 'RAILLOAD0': '1.30', 'RAILLOAD1': '1.47', 'RAILLOAD2': '1.74', 'RAILLOAD3': '1.13', 'RAILLOAD4': '0.58', 
# 'RAILENA0': '1', 'RAILENA1': '1', 'RAILENA2': '1', 'RAILENA3': '1', 'RAILENA4': '1'}}

fields = {}

try:
    fields['supply_voltage'] = float(response['rr4005i']['SUPPLY'])
    fields['rail_load_0'] = float(response['rr4005i']['RAILLOAD0'])
    fields['rail_load_1'] = float(response['rr4005i']['RAILLOAD1'])
    fields['rail_load_2'] = float(response['rr4005i']['RAILLOAD2'])
    fields['rail_load_3'] = float(response['rr4005i']['RAILLOAD3'])
    fields['rail_load_4'] = float(response['rr4005i']['RAILLOAD4'])

except Exception as e:
    print(f"Error parsing response: {response}")


meas_point = {
    "measurement": INFLUXDB_MEASNAME,
    "tags": {"name": RR4005I_NAME},
    "fields": fields
}

print(meas_point)

# Push into InfluxDB
write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=meas_point)

print("Done!")