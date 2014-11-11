#!/usr/bin/env python

import os
import time
import ftplib
import urllib
import argparse

from threading import Thread

def reportHook (a, b, c):

  print "% 3.1f%% of %d megabytes\r" % (min(100, float(a * b) / c * 100), c * 1.0e-6),

def requestData (file, baseUrl, saveDir):

  if file in os.listdir (args.save_dir):
    return

  fullPath = os.path.join (baseUrl, file)
  savePath = os.path.join (saveDir, file)
  print "Retrieving: " + file
  urllib.urlretrieve (fullPath, savePath)


parser = argparse.ArgumentParser (description='Downloads relevant data files from IRIS.')

parser.add_argument (
    "--user_name", type=str, help="IRIS public directory name (e.g. Michael_Afanasiev)", 
    required=True, 
    metavar='ftp directory name')

parser.add_argument (
    "--save_dir", type=str, help="Directory to save .seed files in (recommended: ./MISC/seedFiles)",
    required=True,
    metavar="save directory name")

args = parser.parse_args ()

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
numThreads = 8
threads    = []
getFiles   = []
for file in files:

  # Skip those files already downloaded.
  if file in os.listdir (saveDir):
    continue

  # Fill up the file request until we hit max threads.
  if counter < numThreads:
    getFiles.append (file)
    counter = counter + 1
    continue

  # set up threads.
  for requestFile in getFiles:
    threads.append (Thread (target=requestData, args=(requestFile, baseUrl, saveDir)))

  # start threads.
  [thread.start () for thread in threads]

  # wait threads.
  [thread.join () for thread in threads]

  # reset for next loop.
  threads  = []
  getFiles = []
  counter  = 0
