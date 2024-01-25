#!/bin/sh
#
cd /opt/radar-display/src

while true
do
  echo "Starting"
  /usr/bin/python3 epd_weather.py
  sleep 30m
done
