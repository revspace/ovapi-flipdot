#!/bin/env python3

import requests, sys, dateutil.parser, datetime
import paho.mqtt.publish

j = requests.get('http://kv78turbo.ovapi.nl/stopareacode/1528,7211,Ldv').json()
passes = []
mqttBody = ''

for stopArea in j:
  for timingPoints in j[stopArea]:
    for passTime in j[stopArea][timingPoints]['Passes']:
      p = j[stopArea][timingPoints]['Passes'][passTime]

      departureTimeDiff = max(0, int((dateutil.parser.parse(p['ExpectedDepartureTime']) - datetime.datetime.now()).total_seconds()/60))

      key = '%s I %s' % (p['LinePublicNumber'], p['DestinationName50'])
      passes.append((departureTimeDiff, key))

passes.sort()

for passTime in passes[:6]:
  s = '%s: %s m' % (passTime[1], passTime[0])
  print(s)
  mqttBody += s + '\n '

paho.mqtt.publish.single('revspace/flipdot', payload=mqttBody, hostname='mosquitto.revspace.nl')
