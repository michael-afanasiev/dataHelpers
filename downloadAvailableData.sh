#!/bin/bash

breqFastFolder=./MISC/breqFastRequests
seedFolder=./MISC/seedFiles
ftpPath='ftp://ftp.iris.washington.edu/pub/userdata/Michael_Afanasiev/'

mkdir -p $seedFolder

for file in $breqFastFolder/*.bqFast; do
  
  trimFile=$(basename ${file%.bqFast})
  echo "Searching for $trimFile"
  echo "wget -P $seedFolder -m -nd -np -r -A $trimFile*.seed $ftpPath"

done
