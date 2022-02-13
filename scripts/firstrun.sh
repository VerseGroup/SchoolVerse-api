#!/bin/bash

cd ..

pip -help 1> /dev/null || python -m ensurepip --upgrade
pip cache purge

if [[ "$VIRTUAL_ENV" != "" ]]
then
  INVENV=1
  echo VENV FOUND
else
  INVENV=0
  echo NO VENV FOUND
fi

if [ $INVENV -eq 0 ]
then
    pip install virtualenv || pip3 install virtualenv
    sleep 3
    virtualenv env 
    /env/bin/activate
fi

sleep 3

if [[ "$VIRTUAL_ENV" != "" ]]
then
  INVENV=1
  echo ACTIVATED VENV
else
  INVENV=0
  echo FAILED TO ACTIVATE
fi

if [ $INVENV -eq 1 ]
then
    pip install -r requirements.txt || pip3 install -r requirements.txt
    echo INSTALLED REQUIREMENTS 
fi

