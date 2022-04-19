#!/bin/bash

cd lib/resets

COMPLETED="n/a"

while getopts ":ft:" option; do
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
        \?) # Invalid option
            echo "Error: Invalid option"
            exit
            ;;
    esac
done

echo "completed reset: $COMPLETED"
exit