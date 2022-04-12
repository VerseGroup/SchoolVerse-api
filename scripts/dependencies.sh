#!/bin/bash

cd ..

if [[ "$VIRTUAL_ENV" != "" ]]
then
  INVENV=1
else
  INVENV=0
  echo "No virtual environment found"
  exit
fi

if [ $INVENV -eq 1 ]
then
    pip cache purge 
    pip uninstall -r requirements.txt -y
    pip install -r requirements.txt
fi