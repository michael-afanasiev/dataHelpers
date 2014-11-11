#!/usr/bin/env python

import ftplib
import urllib
import argparse

parser = argparse.ArgumentParser (description='Downloads relevant data files from IRIS.')

parser.add_argument (
    "--user_name", type=str, help="IRIS public directory name (e.g. Michael_Afanasiev)", 
    required=True, 
    metavar='ftp directory name')

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