#!/bin/env python3

import requests, sys, dateutil.parser, datetime
import paho.mqtt.client as mqtt

j = requests.get('http://kv78turbo.ovapi.nl/stopareacode/1528,7211,Ldv').json()
passes = {}

for stopArea in j:
  for timingPoints in j[stopArea]:
    for passTime in j[stopArea][timingPoints]['Passes']:
      p = j[stopArea][timingPoints]['Passes'][passTime]

      departureTimeDiff = max(0, int((dateutil.parser.parse(p['ExpectedDepartureTime']) - datetime.datetime.now()).total_seconds()/60))

      key = '%s I %s' % (p['LinePublicNumber'], p['DestinationName50'])

      # print('%s: %s m (%s)' % (key, departureTimeDiff, p['ExpectedDepartureTime']))

      if key in passes.keys():
        passes[key] = min(passes[key], departureTimeDiff)
      else:
        passes[key] = departureTimeDiff

print('total', len(passes))

for passTime in passes:
  print('%s: %s m' % (passTime, passes[passTime]))
