#!/bin/bash

cd lib/resets

COMPLETED="n/a"

while getopts ":fted:" option; do
    case $option in
        f)
            echo "Option: Reset Flik"
            python3 reset_flik.py
            COMPLETED="flik"
            ;;
        t)
            echo "Option: Reset Tasks"
            python3 reset_tasks.py
            COMPLETED="tasks"
            ;;
        e)
            echo "Option: Reset Events"
            python3 reset_events.py
            COMPLETED="events"
            ;;
        d)
            echo "Option: Reset Days"
            python3 reset_days.py
            COMPLETED="days"
            ;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

echo "completed reset: $COMPLETED"
exit