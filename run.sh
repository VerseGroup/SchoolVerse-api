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
   echo "f     Run server with full prep"
   echo
   echo "Example: sh run.sh -f"
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
        echo "No VENV found. Please create a virtualenv first."
        exit
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
                exit
            fi
        fi
        
    fi
}

############ RUN SERVER #############
RUN_SERVER()
{
    if [ -n "$PORT" ]
    then
        PORT_=$PORT
    else
        PORT_=80
    fi

    echo "Starting server on port $PORT_"

    # add --reload flag for auto reload during development
    uvicorn src.main:app --host 0.0.0.0 --port $PORT_
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
            echo "Option: Complete Execution"
            CHECK_VIRTUAL_ENV
            DEPENDENCIES
            TESTS
            ;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

echo ""
echo "Running Server..."
echo "Press Ctrl + C to exit"
echo "Steven is very nice and handsome"
echo ""

RUN_SERVER