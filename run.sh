#!/bin/bash

############ HELP #############
Help()
{
   echo "OPTIONS"
   echo
   echo "Syntax: sh run.sh -[h|t|d|v]"
   echo "options:"
   echo "h     Help"
   echo "t     Run tests"
   echo "d     Check dependencies"
   echo "v     Create test virtualenv"
   echo "f     First time setup"
   echo
   echo "Example: sh run.sh -t -d"
}

############ DEPENDENCIES #############
DEPENDENCIES()
{
    if [[ "$VIRTUAL_ENV" != "" ]]
    then
        pip uninstall -r requirements.txt -y
        pip install -r requirements.txt
    else
        echo "Activate a virtual environment to run"
    fi
}

############ RUN TESTS #############
TESTS()
{
    pytest
}

############ CHECK VIRTUAL ENV #############
CHECK_VIRTUAL_ENV()
{
    if [[ "$VIRTUAL_ENV" != "" ]]
    then
        INVENV=1
        echo VENV FOUND
    else
        INVENV=0
        echo NO VENV ACTIVATED...

        echo TRYING TO ACTIVATE...
        source env/bin/activate
        
        if [[ "$VIRTUAL_ENV" != "" ]]
        then
            INVENV=1
            echo VENV ACTIVATED
        else
            INVENV=0
            echo NO VENV INSTALLED
            echo TRYING TO INSTALL VENV...
            
            pip install virtualenv
            echo INSTALLED VENV
            virtualenv env
            echo STARTED ENV
            source env/bin/activate

            if [[ "$VIRTUAL_ENV" != "" ]]
            then
                INVENV=1
                echo ACTIVATED ENV
            else
                INVENV=0
                echo ERROR: FAILED TO ACTIVATE VENV
            fi
        fi
        
    fi
}

############ RUN SERVER #############
RUN_SERVER()
{
    uvicorn main:app --reload
}

############ FIRST TIME SETUP #############
FIRST_TIME_SETUP()
{
    sleep 1
    if [[ "$INVENV" == "1" ]]
    then
        pip install -r requirements.txt
        TESTS
        RUN_SERVER
    else
        echo Some error occured
    fi
}

############ RUN #############

# Process Options
while getopts ":htdvf:" option; do
    case $option in
        h) 
            Help
            exit
            ;;
        d) 
            CHECK_VIRTUAL_ENV
            DEPENDENCIES
            ;;
        t)
            CHECK_VIRTUAL_ENV
            TESTS
            ;;
        v)
            CHECK_VIRTUAL_ENV
            ;;
        f)
            CHECK_VIRTUAL_ENV
            FIRST_TIME_SETUP
            ;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

RUN_SERVER