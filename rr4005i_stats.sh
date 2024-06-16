#!/bin/bash
#
# RR4005 -> InfluxDB Collection Script
#
# Run with cron on whatever update rate you want
#

# Enter the URL to your RR4005i status page here
# e.g. http://192.168.1.100:8073/status.xml
export RR4005I_URL="http://10.0.0.1/status.xml"
export RR4005I_NAME="Rack 12V PSU"


# InfluxDB Settings
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN=""
export INFLUXDB_ORG=""
export INFLUXDB_BUCKET=""
export INFLUXDB_MEASNAME="rr4005i_power"

# Use a local venv if it exists
VENV_DIR=venv
if [ -d "$VENV_DIR" ]; then
    echo "Entering venv."
    source $VENV_DIR/bin/activate
fi

python3 rr4005i_stats.py
