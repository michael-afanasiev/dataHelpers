#!/bin/bash

breqFastFolder=./MISC/breqFastRequests
storeFolder=./MISC/breqFastRequests_downloaded
seedFolder=./MISC/seedFiles
ftpPath='ftp://ftp.iris.washington.edu/pub/userdata/Michael_Afanasiev/'

mkdir -p $seedFolder
mkdir -p $storeFolder

iter=0
for file in $breqFastFolder/*.bqFast; do
  
  trimFile=$(basename ${file%.bqFast})
  echo "Searching for $trimFile"
  wget --quiet -P $seedFolder -m -nd -np -r -A $trimFile*.seed $ftpPath &

  mv $file $storeFolder
  
  let iter+=1
  if [ "$iter" -eq 8 ]; then

    wait
    break

  fi

  echo "Done."

done
