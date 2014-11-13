#!/usr/bin/env python


import tarfile
import time
import os
import sys
import ftplib
import urllib
import shutil
import argparse
import subprocess
import dataModule as dm

from obspy import read
from fnmatch import fnmatch

from itertools import repeat
from multiprocessing import Pool

def reportHook (a, b, c):

  print "% 3.1f%% of %d megabytes\r" % (min(100, float(a * b) / c * 100), c * 1.0e-6),

def requestData ((file, baseUrl, saveDir)):

  fullPath = os.path.join (baseUrl, file)
  savePath = os.path.join (saveDir, file)
  print "Retrieving: " + file
  urllib.urlretrieve (fullPath, savePath)
  
def unpackData (args):
  
  for dataDir in os.listdir (args.data_dir):
    for saveDir in os.listdir (args.save_dir):

      if dataDir in saveDir:

        print dm.colours.HEADER + "Extracting .sac files for: " + dm.colours.OKBLUE + saveDir + dm.colours.ENDC
        seedFile    = os.path.join (os.path.abspath (args.save_dir), saveDir) 
        destination = os.path.join (os.path.abspath (args.data_dir), dataDir)
        rawDir      = os.path.join (os.path.abspath (args.data_dir), dataDir, 'raw')
       
        # Make the extraction directory.
        if not (os.path.exists ('./sacFiles')):
          os.makedirs ('./sacFiles')

        # Ensure extraction directory is clean.
        for file in os.listdir ('./sacFiles'):
          os.remove (os.path.join ('./sacFiles', file))
        
        # Make the raw directory.
        if not (os.path.exists (rawDir)):
          os.makedirs (rawDir)
        else:
          print dm.colours.WARNING + "Raw file for " + seedFile + " already exisited..." + dm.colours.ENDC

        # Extract the .sac files to a local scratch directory.
        shutil.copyfile (seedFile, './extract.seed')
        proc = subprocess.Popen ([args.rdseed_binary, '-d', '-f', './extract.seed', '-q', './sacFiles'], 
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate ()
        retcode = proc.wait ()
        os.remove ('./extract.seed')

        # Convert all sac files to miniseed.
        print dm.colours.HEADER + "Converting to miniSeed." + dm.colours.ENDC 
        for filename in os.listdir ('./sacFiles'):
          if fnmatch (filename, '*BH[Z,N,E]*') or fnmatch (filename, '*LH[Z,N,E]*'):
        
            st = read (os.path.join ('./sacFiles', filename))
            fname = st[0].stats.station + '.' + st[0].stats.network + '.' + st[0].stats.location + '.' + st[0].stats.channel + '.mseed'
            st.write (os.path.join ('./sacFiles', fname), format='MSEED')
        
        # Tar the sac files.
        print dm.colours.HEADER + 'Tarring seismograms.' + dm.colours.ENDC
        tar = tarfile.open ('./rawData.tar', 'w')
        for filename in os.listdir ('./sacFiles'):
          if filename.endswith ('.mseed'):
            tar.add (os.path.join ('./sacFiles', filename), arcname=filename)
        tar.close ()

        # Mv the tar-ed file to the DATA directory.
        if os.path.exists (os.path.join (rawDir, 'rawData.tar')):
          os.remove (os.path.join (rawDir, 'rawData.tar'))
        shutil.move ('./rawData.tar', rawDir)
        
        if retcode == 0:
          print dm.colours.OKGREEN + "Completed succesfully.\n" + dm.colours.ENDC
        else:
          print dm.colours.WARNING + "Something fishy happened with " + seedFile + dm.colours.ENDC + "\n"

  shutil.rmtree ('./sacFiles')
          
#----- Command line arguments.
parser = argparse.ArgumentParser (description='Downloads relevant data files from IRIS.')

parser.add_argument (
    "--rdseed_binary", type=str, help="Path to rdseed binary", metavar="rdseed binary",
    required=True)

parser.add_argument (
  "--data_dir", type=str, help="Lasif DATA directory.", metavar="Lasif data dir.")

parser.add_argument (
  "--num_threads", type=int, help="Number of threads for simultaneous downloads",
  default=8, metavar='Nthreads')
  
parser.add_argument (
  "--skip_download", action='store_true', help="Skips downloading, and goes straight to unpacking "
    "data", default=False)

parser.add_argument (
  "--user_name", type=str, help="IRIS public directory name (e.g. Michael_Afanasiev)", 
  required=True, 
  metavar='ftp directory name')

parser.add_argument (
  "--save_dir", type=str, help="Directory to save .seed files in (recommended: ./MISC/seedFiles)",
  required=True,
  metavar="save directory name")

args = parser.parse_args ()
#----- End command line arguments.

directoryPath = '/pub/userdata/' + args.user_name

# connect to server.
server = ftplib.FTP ('ftp.iris.washington.edu')
server.login        ()

# change to directory.
server.cwd       (directoryPath)
files = server.nlst ()

# we've got our file list, move on.
server.close () 

baseUrl = os.path.join ('ftp://ftp.iris.washington.edu' + directoryPath) 
saveDir = args.save_dir

counter    = 0
numThreads = args.num_threads
threads    = []
getFiles   = []
for file in files:

  # Skip those files already downloaded.
  if file in os.listdir (saveDir):
    continue
  else:
    getFiles.append (file)

# Open a thread pool to do the downloading in parallel.
if (not args.skip_download):
  if __name__ == '__main__':

    pool = Pool (processes=numThreads)
    pool.map (requestData, zip (getFiles, repeat (baseUrl), repeat (saveDir)))
    
unpackData (args)
