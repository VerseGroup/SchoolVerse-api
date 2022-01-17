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

if [ $INVENV -eq 1 ]
then
    pip install virtualenv
    virtualenv env 
    /env/bin/activate
    pip install -r requirements.txt
fi