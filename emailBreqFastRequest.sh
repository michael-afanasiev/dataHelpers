#!/bin/bash

for file in ./*.bqFast; do
  echo "cat $file | mail -s 'bqFast Request.' breq_fast@iris.washington.edu"
  sleep 5
done
