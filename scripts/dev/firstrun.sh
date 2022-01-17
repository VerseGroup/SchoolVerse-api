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
    pip3 install -r requirements.txt
fi