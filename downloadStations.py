#!/usr/bin/env python

import dataModule

from obspy.fdsn import Client
client = Client ('IRIS')

stations, networks = dataModule.getStations ('./stationList.txt', format='nospace')

for station, network in zip (stations, networks):
  
  print "Downloading: " + station + " " + network + "."
  stationXmlName = 'station.' + network + '_' + station + '.xml'
  inventory      = client.get_stations (network=network, station=station, level="response")
  
  inventory.write (stationXmlName, 'StationXML')
  