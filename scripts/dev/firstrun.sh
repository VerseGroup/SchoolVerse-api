cd ..
cd ..

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
    pip3 install virtualenv
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
    pip3 install -r requirements.txt

    echo 
    echo INSTALLED REQUIREMENTS AND ACTIVATED VENV
fi

