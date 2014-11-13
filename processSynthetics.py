#!/usr/bin/env python

import os
import obspy
import argparse
import numpy as np

#----- Command line arguments.
parser = argparse.ArgumentParser (description='Generates a BreqFast request.')

parser.add_argument (
  '--seismogram_dir', type=str, help='Directory of (convolved) specfem seismogram', 
  required=True, metavar='Seismo dir')
  
parser.add_argument (
  '--max_period', type=float, help='Long period corner', required=True, metavar='LP corner')
  
parser.add_argument (
  '--min_period', type=float, help='Short period corner', required=True, metavar='SP corner')
  
parser.add_argument (
  '--write_dir', type=str, help='Write directory for processed synthetic seismograms', 
  required=True, metavar='Write dir'
)

args = parser.parse_args ()
#----- End command line arguments.

# For all seismograms in the seismogram directory.
for dirname, dirnames, filenames in os.walk (args.seismogram_dir):  
  for filename in filenames:
      
    # Skip those files which are not convolved.
    if not 'convolved' in filename:
      continue

    # Read ascii file, and calculate dt.
    print 'Processing: ' + filename
    filename = os.path.join (dirname, filename)
    temp     = np.loadtxt(filename, dtype=np.float64)
    t, data  = temp[:, 0], temp[:, 1]
    dt       = (t[-1] - t[0]) / (len(t) - 1)

    # Initialze obspy trace.
    tr             = obspy.Trace(data=temp[:, 1])
    tr.stats.delta = dt
    tr.stats.station, tr.stats.network, tr.stats.channel = \
        os.path.basename(filename).split(".")[:3]

    # Name channels correctly.
    if   'MXN' in tr.stats.channel:
      tr.stats.channel = 'X'
    elif 'MXE' in tr.stats.channel:
      tr.stats.channel = 'Y'
    elif 'MXZ' in tr.stats.channel:
      tr.stats.channel = 'Z'

    # XXX: Set the time of the first sample!!!
    tr.stats.starttime = "2012-06-01T05:07:01.900000Z"

    # Bandpass filter.
    tr.filter ('lowpass',  freq=(1/args.min_period), corners=5, zerophase=True)          
    tr.filter ('highpass', freq=(1/args.max_period), corners=2, zerophase=True)          
    
    # Write to sac file.    
    if not (os.path.isdir (args.write_dir)):
      os.mkdir (args.write_dir)
    sacFileName = os.path.join (
      args.write_dir, tr.stats.station + '.' + tr.stats.network + '.' + tr.stats.channel + '.mseed')    
    tr.write (sacFileName, format='MSEED')