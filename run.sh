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
        cd scripts 
        sh dependencies.sh
        cd ..
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
        echo "Found virtual environment"
    else
        INVENV=0
        echo "No virtual environment activated"

        echo "Activating virtual environment..."
        source env/bin/activate

        sleep 3
        
        if [[ "$VIRTUAL_ENV" != "" ]]
        then
            INVENV=1
            echo "Activated Venv"
        else
            INVENV=0
            echo "No virtual environment found"
            
            echo "installing virtualenv..."
            pip install virtualenv
            
            echo "starting venv: env"
            virtualenv env
            
            echo "Activating env"          
            source env/bin/activate

            if [[ "$VIRTUAL_ENV" != "" ]]
            then
                INVENV=1
                echo "Activated VENV"
            else
                INVENV=0
                echo "Error: Failed to activate the VENV"
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
        cd scripts
        sh firstrun.sh
        cd ..
        TESTS
    else
        echo "Some error with the VENV"
    fi
}

############ RUN #############

# Process Options
while getopts ":htdvf:" option; do
    case $option in
        h) 
            echo "Option: Help"
            Help
            exit
            ;;
        d) 
            echo "Option: Dependencies"
            CHECK_VIRTUAL_ENV
            DEPENDENCIES
            ;;
        t)
            echo "Option: Tests"
            CHECK_VIRTUAL_ENV
            TESTS
            ;;
        v)
            echo "Option: Virtual Env"
            CHECK_VIRTUAL_ENV
            ;;
        f)
            echo "Option: First Time Setup"
            CHECK_VIRTUAL_ENV
            FIRST_TIME_SETUP
            ;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

echo "Running Server..."
echo "Press Ctrl+C to exit"
echo ""
RUN_SERVER